"""Validation des anomalies — deuxième étage de la détection de contradictions.

    Données brutes
      ↓
    Détection déterministe        (ara/analysis/compare.py)
      ↓
    Anomalie trouvée
      ↓
    Agent contexte                (ce module)
      ↓
    « Est-ce une vraie contradiction ? »
      ↓
    Validation

Pourquoi deux étages
--------------------
Le détecteur déterministe est réglé pour le **rappel** : il voit tous les
écarts chiffrés, quitte à en signaler qui n'en sont pas. C'est la bonne
propriété pour un premier filtre — rater une vraie contradiction est bien plus
grave que d'en proposer une fausse.

La **précision**, elle, demande de comprendre le contexte. « 312 m » et
« 330 m » pour la tour Eiffel ne se contredisent pas : l'une est la hauteur
d'origine, l'autre celle d'aujourd'hui avec l'antenne. Aucun seuil numérique ne
peut trancher cela ; il faut lire autour du chiffre.

Ce module tranche donc à deux niveaux :

1. **Règles déterministes** (toujours, coût nul) — repèrent les explications
   classiques d'un écart : époques différentes, variantes différentes de la même
   grandeur, portées différentes.
2. **Jugement du LLM** (si un vrai modèle est configuré) — pour ce que les
   règles ne savent pas décider.

Une anomalie non tranchée n'est jamais présentée comme un fait : elle est
marquée « à vérifier », pas « contradiction ».
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from ..core.errors import AraError
from ..core.models import SourceDoc
from ..providers.llm.base import LLMProvider, LLMRequest
from .compare import Contradiction

#: Verdicts possibles
CONFIRMED = "confirmed"    # vraie contradiction : les sources se contredisent
REJECTED = "rejected"      # faux positif : l'écart s'explique
UNCERTAIN = "uncertain"    # indécidable : à signaler comme « à vérifier »

_YEAR = re.compile(r"\b(1[89]\d{2}|20\d{2})\b")

#: Marqueurs d'époque — s'ils diffèrent, les deux chiffres ne parlent pas du
#: même moment, donc ne se contredisent pas.
_PAST = {
    "origine", "initial", "initiale", "initialement", "autrefois", "jadis",
    "ancien", "ancienne", "anciennement", "avant", "construction", "epoque",
    "historique", "premiere", "depart", "lancement", "inauguration",
    "originally", "initially", "formerly", "previously",
}
_PRESENT = {
    "aujourd", "actuel", "actuelle", "actuellement", "desormais", "maintenant",
    "depuis", "recent", "recente", "nouvelle", "nouveau", "renove", "renovee",
    "today", "currently", "now", "since",
}

#: Marqueurs de variante — deux mesures d'objets ou de cas différents.
_VARIANTS = {
    # parties d'un objet
    "premier", "deuxieme", "troisieme", "etage", "niveau", "sommet", "base",
    "socle", "antenne", "mat", "pointe", "cote", "largeur", "profondeur",
    "hauteur", "longueur", "diametre", "surface",
    # variantes commerciales
    "adulte", "enfant", "bebe", "etudiant", "senior", "groupe", "resident",
    "aller", "retour", "simple", "double", "classe", "cabine", "pont",
    "haute", "basse", "saison", "weekend", "semaine", "promotion", "reduit",
    "plein", "tarif", "abonnement",
    # portée du chiffre
    "minimum", "maximum", "moyen", "moyenne", "median", "total", "partiel",
    "hors", "taxe", "taxes", "inclus", "incluse", "supplement", "net", "brut",
    "aller-retour", "par", "personne",
}

#: Marqueurs d'approximation : un chiffre approché ne contredit pas un chiffre exact
_APPROX = {"environ", "pres", "quelque", "approximativement", "about", "around", "roughly"}


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _words(text: str) -> set[str]:
    return set(re.findall(r"[a-z]{3,}", _normalize(text)))


@dataclass
class Verdict:
    """Décision sur une anomalie détectée."""

    status: str
    reason: str
    decided_by: str = "regles"   # regles | llm | defaut
    confidence: str = "moyenne"  # faible | moyenne | forte

    @property
    def is_contradiction(self) -> bool:
        return self.status in {CONFIRMED, UNCERTAIN}

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "reason": self.reason,
            "decided_by": self.decided_by,
            "confidence": self.confidence,
        }


@dataclass
class ValidatedContradiction:
    """Une anomalie et son verdict."""

    contradiction: Contradiction
    verdict: Verdict

    def to_dict(self) -> dict:
        payload = self.contradiction.to_dict()
        payload["verdict"] = self.verdict.to_dict()
        return payload

    def describe(self) -> str:
        label = self.contradiction.describe()
        if self.verdict.status == UNCERTAIN:
            return f"{label} — à vérifier ({self.verdict.reason})"
        return label


# --- Étage 1 : règles déterministes ------------------------------------------


def _temporal_anchor(sentence: str) -> tuple[set[str], str]:
    """Années citées et orientation temporelle d'une phrase."""
    years = set(_YEAR.findall(sentence))
    words = _words(sentence)
    if words & _PAST and not (words & _PRESENT):
        return years, "passe"
    if words & _PRESENT and not (words & _PAST):
        return years, "present"
    return years, ""


def rule_verdict(contradiction: Contradiction) -> Verdict | None:
    """Tranche par règles, ou retourne None si les règles ne savent pas."""
    sentences = [fact.sentence for fact in contradiction.facts]
    if len(sentences) < 2:
        return None

    # 1. Époques différentes → évolution, pas désaccord.
    anchors = [_temporal_anchor(s) for s in sentences]
    orientations = {orientation for _years, orientation in anchors if orientation}
    if len(orientations) > 1:
        return Verdict(
            REJECTED,
            "les valeurs ne portent pas sur la même époque (une d'origine, une actuelle)",
            confidence="forte",
        )

    # Une seule source datée, et d'une année ancienne : c'est l'explication la
    # plus probable de l'écart. Sans cette règle, une archive de 2019 faisait
    # relancer la recherche indéfiniment — constaté au laboratoire.
    from datetime import date as _date

    annee_courante = _date.today().year
    datees = [years for years, _o in anchors if years]
    if len(datees) == 1:
        ancienne = min(int(y) for y in datees[0])
        if annee_courante - ancienne >= 2:
            return Verdict(
                REJECTED,
                f"l'une des valeurs est datée de {ancienne}, l'autre non : "
                "l'écart s'explique par l'ancienneté",
                confidence="moyenne",
            )

    year_sets = [years for years, _o in anchors if years]
    if len(year_sets) >= 2 and not set.intersection(*year_sets):
        return Verdict(
            REJECTED,
            "les valeurs sont datées d'années différentes ("
            + " vs ".join(", ".join(sorted(y)) for y in year_sets[:2])
            + ")",
            confidence="forte",
        )

    # 2. Variantes différentes de la même grandeur → objets différents.
    contexts = [fact.context for fact in contradiction.facts]
    variants = [context & _VARIANTS for context in contexts]
    distinctive = [v - set.union(*(o for i, o in enumerate(variants) if i != j))
                   for j, v in enumerate(variants)]
    if sum(1 for d in distinctive if d) >= 2:
        details = " vs ".join(
            ", ".join(sorted(d)[:2]) for d in distinctive if d
        )
        return Verdict(
            REJECTED,
            f"les valeurs mesurent des variantes différentes ({details})",
            confidence="moyenne",
        )

    # 3. Un chiffre approché face à un chiffre exact : pas un désaccord de fond.
    approx = [bool(_words(s) & _APPROX) for s in sentences]
    if any(approx) and not all(approx):
        return Verdict(
            REJECTED,
            "l'une des valeurs est donnée comme approximative",
            confidence="faible",
        )

    return None


# --- Étage 2 : jugement du LLM ------------------------------------------------

_PROMPT = (
    "Deux sources indépendantes donnent des valeurs différentes. Détermine s'il "
    "s'agit d'une VRAIE contradiction (les deux ne peuvent pas être vraies "
    "ensemble sur le même objet, au même moment) ou d'un FAUX POSITIF (elles "
    "mesurent des choses différentes, des époques différentes, ou des variantes "
    "différentes).\n\n"
    "Réponds en deux lignes exactement :\n"
    "VERDICT: CONTRADICTION | FAUX_POSITIF | INCERTAIN\n"
    "RAISON: une phrase courte, en français."
)


def _parse_llm(text: str) -> Verdict | None:
    verdict = reason = ""
    for line in text.splitlines():
        upper = _normalize(line).strip()
        if upper.startswith("verdict"):
            verdict = upper.split(":", 1)[-1].strip()
        elif upper.startswith("raison"):
            reason = line.split(":", 1)[-1].strip()

    if "faux" in verdict:
        return Verdict(REJECTED, reason or "écart explicable", "llm", "moyenne")
    if "contradiction" in verdict:
        return Verdict(CONFIRMED, reason or "valeurs incompatibles", "llm", "forte")
    if "incertain" in verdict:
        return Verdict(UNCERTAIN, reason or "indécidable", "llm", "faible")
    return None


class ContradictionValidator:
    """Agent contexte : décide si une anomalie est une vraie contradiction."""

    def __init__(self, llm: LLMProvider | None = None, question: str = "") -> None:
        self.llm = llm
        self.question = question
        #: raisons des rejets, pour le journal et la transparence
        self.rejected: list[tuple[Contradiction, Verdict]] = []

    def validate(
        self, contradictions: list[Contradiction], docs: list[SourceDoc] | None = None
    ) -> list[ValidatedContradiction]:
        """Filtre les anomalies. Ne conserve que ce qui mérite d'alerter."""
        kept: list[ValidatedContradiction] = []
        self.rejected = []

        for contradiction in contradictions:
            verdict = rule_verdict(contradiction)
            if verdict is None:
                verdict = self._ask_llm(contradiction) or Verdict(
                    UNCERTAIN,
                    "aucune règle ni aucun modèle n'a pu trancher",
                    "defaut",
                    "faible",
                )
            if verdict.is_contradiction:
                kept.append(ValidatedContradiction(contradiction, verdict))
            else:
                self.rejected.append((contradiction, verdict))

        return kept

    def _ask_llm(self, contradiction: Contradiction) -> Verdict | None:
        """Interroge le modèle. Un moteur dégradé ne juge rien : il s'abstient."""
        if self.llm is None or self.llm.degraded:
            return None

        extraits = "\n".join(
            f"- Source [S{fact.source}] : « {fact.sentence[:300]} » "
            f"→ valeur relevée : {fact.describe()}"
            for fact in contradiction.facts[:4]
        )
        question = (
            f"Question posée par l'utilisateur : {self.question}\n\n{extraits}"
            if self.question
            else extraits
        )

        try:
            result = self.llm.complete(
                LLMRequest(
                    task="answer",
                    question=question,
                    instructions=_PROMPT,
                    max_tokens=150,
                    temperature=0.0,
                )
            )
        except AraError:
            return None
        return _parse_llm(result.text)


__all__ = [
    "CONFIRMED",
    "REJECTED",
    "UNCERTAIN",
    "Verdict",
    "ValidatedContradiction",
    "ContradictionValidator",
    "rule_verdict",
]
