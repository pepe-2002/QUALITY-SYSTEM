"""Contrôleur TASK_COMPLEXITY (spec §4).

L'agent ne doit pas dépenser la même quantité de calcul pour « quelle heure
est-il ? » et pour « compare les horaires de trois compagnies et fais-moi un
PDF ». Ce module estime la complexité **avant** d'engager des ressources, puis
alloue un budget d'étapes.

Deux versions coexistent, et c'est voulu
----------------------------------------
**ADAPTIVE-V1** (`assess`) — *gelée définitivement*. C'est la baseline des
expériences H1 et H2 : elle ne doit plus bouger, sans quoi ces résultats
deviendraient irreproductibles. Elle note la **forme** de la demande —
comparaison, livrable, longueur, conjonctions — puis alloue un budget une fois
pour toutes.

**ADAPTIVE-V2** (`assess_v2`) — corrige le défaut que H2 a mis au jour : V1 ne
distingue pas une question facile d'une question profonde, parce qu'elle
mesure la forme de la demande et non la difficulté à **trouver** la réponse.
« À quelle heure ouvre le centre ? » tient en huit mots et n'existe qu'à un
seul endroit ; V1 lui donne le budget minimal.

V2 procède en deux temps :

1. **estimation de la difficulté AVANT de chercher** (`estimate_difficulty`),
   à partir de caractéristiques de la question seule — jamais du corpus, jamais
   de la réponse ;
2. **révision en cours de route** (`TaskBudget.revise`), sur des signaux
   explicites :

   ===================== ==========================================
   FACILE                 la réponse est là → arrêt, budget rendu
   DIFFICILE              rien de ce qui est demandé → recherches en plus
   CONTRADICTION          deux valeurs incompatibles → vérification
   INFORMATION SUFFISANTE plus rien ne manque → arrêt
   ===================== ==========================================

Statut scientifique — à lire avant d'en tirer des conclusions
------------------------------------------------------------
V2 n'est **pas** une preuve de H2. C'est une correction de défaut, qui devra
faire l'objet de sa propre expérience, sur son propre jeu de test. Les seuils
restent des heuristiques sans validation externe.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import Enum


class Complexity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


#: Budgets par niveau : (étapes de recherche, passes d'analyse)
BUDGETS: dict[Complexity, tuple[int, int]] = {
    Complexity.LOW: (1, 1),
    Complexity.MEDIUM: (3, 2),
    Complexity.HIGH: (6, 3),
}

# --- Signaux lexicaux (français + anglais, sans accents après normalisation) ---

_RESEARCH_WORDS = {
    "recherche", "cherche", "chercher", "trouve", "trouver", "actualite",
    "actualites", "horaire", "horaires", "prix", "tarif", "tarifs", "meteo",
    "source", "sources", "qui est", "combien", "quand", "ou est", "search",
    "find", "latest", "news", "documente", "documenter", "verifie", "verifier",
}

_COMPARE_WORDS = {
    "compare", "comparer", "comparaison", "versus", "vs", "difference",
    "differences", "meilleur", "meilleure", "avantages", "inconvenients",
    "pour et contre", "analyse", "analyser", "evalue", "evaluer", "synthese",
    "benchmark", "compare",
}

_DELIVERABLE_WORDS = {
    "pdf", "docx", "word", "document", "rapport", "dossier", "flyer",
    "affiche", "presentation", "note", "memo", "fiche", "tableau", "md",
    "markdown", "txt", "fichier",
}

_TRIVIAL_WORDS = {
    "bonjour", "salut", "merci", "ok", "test", "coucou", "hello", "hi",
    "ca va", "comment vas tu",
}

#: Mots qui réclament une valeur **faisant autorité**.
#:
#: Ajoutés après l'expérience H2, qui a montré que le contrôleur estimait la
#: forme de la demande (comparaison, livrable, longueur) et non la difficulté
#: à *trouver* la réponse. Or ces deux choses n'ont rien à voir : « à quelle
#: heure ouvre le centre ? » tient en huit mots et n'est publié qu'à un seul
#: endroit. Une valeur officielle, exacte ou réglementaire vit rarement sur la
#: première page venue — il faut aller la chercher.
_AUTHORITY_WORDS = {
    "officiel", "officielle", "officiels", "officielles", "exact", "exacte",
    "precis", "precise", "reglement", "reglementaire", "legal", "legale",
    "vigueur", "homologue", "homologuee", "certifie", "certifiee", "arrete",
    "decret", "norme", "official", "exact", "regulation",
}


def _normalize(text: str) -> str:
    """Minuscule, sans accents, ponctuation réduite à des espaces."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _count_hits(haystack: str, needles: set[str]) -> int:
    """Nombre de termes du lexique présents (mots entiers ou expressions)."""
    padded = f" {haystack} "
    return sum(1 for needle in needles if f" {needle} " in padded)


@dataclass
class TaskBudget:
    """Décision du contrôleur pour une tâche donnée."""

    complexity: Complexity
    search_steps: int
    analysis_passes: int
    signals: dict[str, int]
    max_search_steps: int = 10

    #: nombre de recherches réellement consommées
    used_searches: int = 0
    #: version du contrôleur qui a produit ce budget — « v1 » est gelée
    controller: str = "v1"
    #: estimation de difficulté (V2 uniquement)
    difficulty: str = ""
    difficulty_reason: str = ""
    #: historique des révisions sur preuve — (action, motif)
    revisions: list = None  # type: ignore[assignment]
    #: raison d'arrêt de la collecte, quand le budget est révisable (V2)
    stop_code: str = ""

    def __post_init__(self) -> None:
        if self.revisions is None:
            self.revisions = []

    @property
    def remaining_searches(self) -> int:
        return max(0, min(self.search_steps, self.max_search_steps) - self.used_searches)

    def consume_search(self) -> None:
        self.used_searches += 1

    def escalate(self, reason: str = "") -> bool:
        """Augmente le budget d'un cran. Retourne False si déjà au maximum.

        Appelé quand l'analyse détecte un manque d'information ou une
        contradiction (spec §3).
        """
        if self.complexity is Complexity.HIGH:
            # déjà au maximum : on peut encore élargir jusqu'au plafond dur
            if self.search_steps >= self.max_search_steps:
                return False
            self.search_steps = min(self.search_steps + 1, self.max_search_steps)
            return True
        order = [Complexity.LOW, Complexity.MEDIUM, Complexity.HIGH]
        self.complexity = order[order.index(self.complexity) + 1]
        steps, passes = BUDGETS[self.complexity]
        self.search_steps = min(max(self.search_steps, steps), self.max_search_steps)
        self.analysis_passes = max(self.analysis_passes, passes)
        return True

    def revise(self, verdict: str, reason: str = "") -> str:
        """Révise le budget d'après ce que la recherche a **ramené**.

        C'est l'apport de la correction post-H2 : jusque-là, le contrôleur
        décidait une fois pour toutes avant de chercher, à partir des seuls
        mots de la question. Il pouvait donc allouer un budget minimal à une
        question dont la réponse n'existe que sur une page difficile à
        atteindre — et c'est exactement ce que l'expérience a mesuré.

        `verdict` vaut :

        * ``"difficile"`` — ce qui est demandé n'a pas été trouvé : on monte ;
        * ``"suffisant"`` — la réponse est là : on s'arrête, et on rend ce qui
          n'a pas servi ;
        * ``"indetermine"`` — on ne sait pas : on ne touche à rien. Ne rien
          faire est une décision, et c'est la bonne quand on ignore.

        Retourne l'action effectivement appliquée, pour le journal.
        """
        # Garde-fou anti-boucle : au-delà de MAX_REVISIONS, le contrôleur a eu
        # ses chances. Continuer à réviser ne ferait que consommer le plafond
        # dur en journalisant à chaque tour.
        if len(self.revisions) >= MAX_REVISIONS:
            return "plafond_revisions"
        if verdict == "difficile":
            monte = self.escalate(reason or "information demandée introuvable")
            self.revisions.append(("escalate" if monte else "plafond", reason))
            return "escalate" if monte else "plafond"
        if verdict == "suffisant":
            baisse = self.de_escalate(reason or "réponse trouvée")
            self.revisions.append(("de-escalate" if baisse else "deja_minimal", reason))
            return "de-escalate" if baisse else "deja_minimal"
        self.revisions.append(("aucune", reason))
        return "aucune"

    def de_escalate(self, reason: str = "") -> bool:
        """Réduit le budget d'un cran (tâche plus simple que prévu)."""
        order = [Complexity.LOW, Complexity.MEDIUM, Complexity.HIGH]
        index = order.index(self.complexity)
        if index == 0:
            return False
        self.complexity = order[index - 1]
        steps, passes = BUDGETS[self.complexity]
        self.search_steps = max(self.used_searches, min(self.search_steps, steps))
        self.analysis_passes = min(self.analysis_passes, passes)
        return True

    def to_dict(self) -> dict[str, object]:
        return {
            "complexity": self.complexity.value,
            "search_steps": self.search_steps,
            "analysis_passes": self.analysis_passes,
            "used_searches": self.used_searches,
            "signals": self.signals,
            "controller": self.controller,
            "stop_code": self.stop_code,
            "difficulty": self.difficulty,
            "difficulty_reason": self.difficulty_reason,
            "revisions": [{"action": a, "reason": r} for a, r in self.revisions],
        }


#: Version du contrôleur utilisée par défaut dans l'application.
#:
#: Passée à « v2 » sur décision du propriétaire du projet, après l'expérience
#: qui l'a jugée : sur le jeu 3 — jamais utilisé auparavant — V2 corrige le
#: défaut visé (elle alloue enfin plus aux questions profondes qu'aux faciles),
#: gagne en exactitude et garde l'économie.
#:
#: Ce que cette adoption ne dit pas : la validation porte sur dix tâches
#: écrites par l'auteur du système. C'est un choix de produit appuyé sur une
#: mesure, pas une preuve.
#:
#: V1 reste figée et reste la baseline de H1 et H2 : le laboratoire épingle
#: explicitement la version de chaque bras, donc ce changement ne touche pas
#: aux résultats publiés.
DEFAULT_CONTROLLER = "v2"

#: Nombre maximal de révisions de budget pour une tâche. Garde-fou contre la
#: boucle : sans lui, « difficile → +1 recherche → toujours difficile → … »
#: tournerait jusqu'au plafond dur en journalisant à chaque tour.
MAX_REVISIONS = 4

#: Grandeurs demandées et ce qu'elles coûtent à trouver, *a priori*.
#:
#: Ce n'est pas une connaissance de la réponse : c'est une propriété de la
#: **question**. Un prix courant est répété partout ; un horaire officiel, un
#: taux statistique ou une règle sont publiés à un seul endroit, souvent par
#: une autorité, et les pages généralistes s'en approchent sans les donner.
#: Provenance assumée : ce classement a été formé en lisant les jeux 1 et 2,
#: donc avant le jeu de test final, et il ne dépend d'aucune valeur d'or.
ASPECT_DIFFICULTY: dict[str, int] = {
    "money": 0,
    "distance": 0,
    "duration": 0,
    "weight": 1,
    "percent": 2,
    "time": 2,
    "year": 1,
}


@dataclass(frozen=True)
class DifficultyEstimate:
    """Ce que le contrôleur croit de la question **avant** de chercher."""

    level: str                    # simple | intermediaire | profonde
    score: int
    features: dict
    reason: str

    def to_dict(self) -> dict:
        return {
            "level": self.level, "score": self.score,
            "features": self.features, "reason": self.reason,
        }


#: Difficulté → complexité allouée. Trois niveaux, comme demandé.
DIFFICULTY_TO_COMPLEXITY = {
    "simple": Complexity.LOW,
    "intermediaire": Complexity.MEDIUM,
    "profonde": Complexity.HIGH,
}


def _expected_kinds(text: str) -> set[str]:
    """Grandeurs que la question réclame, d'après ses seuls mots.

    Import local et tardif : `core` ne doit pas dépendre de `analysis` au
    chargement, sous peine de cycle. La dépendance est ici purement lexicale.
    """
    try:
        from ..analysis.coverage import ASPECTS, detect_aspects
    except ImportError:  # pragma: no cover — sécurité de chargement
        return set()
    return {ASPECTS[aspect][0] for aspect in detect_aspects(text)}


def estimate_difficulty(prompt: str) -> DifficultyEstimate:
    """Estime la difficulté d'une question **avant** toute recherche.

    Quatre caractéristiques, toutes disponibles sans avoir rien cherché :

    1. **la grandeur demandée** — un horaire ou un taux officiel se trouve à un
       seul endroit, un prix courant se trouve partout ;
    2. **l'exigence d'autorité** — « officiel », « exact », « règlement » : on
       ne veut pas la première valeur venue, on veut la bonne ;
    3. **l'ampleur de la demande** — comparaison, plusieurs grandeurs,
       plusieurs propositions enchaînées ;
    4. **la brièveté trompeuse** — une question courte qui réclame une valeur
       rare n'est pas une question facile, et c'est exactement l'erreur de V1.

    Ne regarde jamais le corpus, ni les résultats, ni la réponse attendue.
    """
    text = _normalize(prompt)
    words = text.split()
    kinds = _expected_kinds(prompt)

    features = {
        "length": len(words),
        "kinds": sorted(kinds),
        "kind_cost": max((ASPECT_DIFFICULTY.get(k, 1) for k in kinds), default=1),
        "authority": _count_hits(text, _AUTHORITY_WORDS),
        "compare": _count_hits(text, _COMPARE_WORDS),
        "deliverable": _count_hits(text, _DELIVERABLE_WORDS),
        "conjunctions": len(re.findall(r"\b(et|puis|ensuite|and|then)\b", text)),
        "aspects": len(kinds),
    }

    if len(words) <= 4 and _count_hits(text, _TRIVIAL_WORDS):
        return DifficultyEstimate(
            "simple", 0, features, "salutation : aucune recherche à prévoir"
        )

    score = (
        features["kind_cost"] * 2
        + features["authority"] * 2
        + features["compare"] * 3
        + features["deliverable"]
        + max(0, features["aspects"] - 1) * 2
        + min(features["conjunctions"], 2)
        + (2 if features["length"] > 25 else 1 if features["length"] > 12 else 0)
    )

    if score >= 6:
        level, motif = "profonde", "grandeur rare ou demande d'autorité"
    elif score >= 3:
        level, motif = "intermediaire", "demande ordinaire, plusieurs angles possibles"
    else:
        level, motif = "simple", "grandeur courante, demande directe"

    detail = []
    if features["kind_cost"] >= 2:
        detail.append("la grandeur demandée est publiée à un seul endroit")
    if features["authority"]:
        detail.append("une valeur faisant autorité est exigée")
    if features["aspects"] > 1:
        detail.append(f"{features['aspects']} grandeurs demandées")
    if features["compare"]:
        detail.append("comparaison demandée")
    raison = motif + (" — " + ", ".join(detail) if detail else "")
    return DifficultyEstimate(level, score, features, raison)


def assess_v2(prompt: str, *, max_search_steps: int = 10) -> TaskBudget:
    """ADAPTIVE-V2 : le budget découle d'une estimation **explicite** de la difficulté.

    >>> assess_v2("bonjour").complexity
    <Complexity.LOW: 'LOW'>
    >>> assess_v2("À quelle heure ouvre le centre ?").complexity
    <Complexity.HIGH: 'HIGH'>
    """
    estimate = estimate_difficulty(prompt)
    complexity = DIFFICULTY_TO_COMPLEXITY[estimate.level]
    steps, passes = BUDGETS[complexity]

    signals = dict(estimate.features)
    signals["score"] = estimate.score
    signals["difficulty"] = estimate.level

    return TaskBudget(
        complexity=complexity,
        # Le plafond dur n'est jamais franchi, quelle que soit l'estimation.
        search_steps=min(steps, max_search_steps),
        analysis_passes=passes,
        signals=signals,
        max_search_steps=max_search_steps,
        controller="v2",
        difficulty=estimate.level,
        difficulty_reason=estimate.reason,
    )


def assess_for(
    controller: str, prompt: str, *, max_search_steps: int = 10
) -> TaskBudget:
    """Alloue un budget avec la version de contrôleur demandée."""
    if controller == "v1":
        return assess(prompt, max_search_steps=max_search_steps)
    if controller == "v2":
        return assess_v2(prompt, max_search_steps=max_search_steps)
    raise ValueError(f"version de contrôleur inconnue : {controller}")


def assess(prompt: str, *, max_search_steps: int = 10) -> TaskBudget:
    """Estime la complexité d'une tâche et alloue son budget.

    >>> assess("bonjour").complexity
    <Complexity.LOW: 'LOW'>
    >>> assess("compare les horaires des 3 compagnies et fais un PDF").complexity
    <Complexity.HIGH: 'HIGH'>
    """
    text = _normalize(prompt)
    words = text.split()

    signals = {
        "length": len(words),
        "research": _count_hits(text, _RESEARCH_WORDS),
        "compare": _count_hits(text, _COMPARE_WORDS),
        "deliverable": _count_hits(text, _DELIVERABLE_WORDS),
        "authority": _count_hits(text, _AUTHORITY_WORDS),
        "questions": prompt.count("?"),
        "conjunctions": len(re.findall(r"\b(et|puis|ensuite|and|then)\b", text)),
    }

    # Salutation seule → toujours LOW, quel que soit le reste du score.
    if len(words) <= 4 and _count_hits(text, _TRIVIAL_WORDS):
        score = 0
    else:
        score = (
            signals["research"] * 2
            + signals["compare"] * 3
            + signals["deliverable"] * 2
            + min(signals["conjunctions"], 3)
            + (2 if signals["length"] > 25 else 1 if signals["length"] > 12 else 0)
        )

    if score >= 7:
        complexity = Complexity.HIGH
    elif score >= 3:
        complexity = Complexity.MEDIUM
    else:
        complexity = Complexity.LOW

    steps, passes = BUDGETS[complexity]
    signals["score"] = score
    return TaskBudget(
        complexity=complexity,
        search_steps=min(steps, max_search_steps),
        analysis_passes=passes,
        signals=signals,
        max_search_steps=max_search_steps,
    )
