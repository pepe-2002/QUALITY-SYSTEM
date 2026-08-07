"""Détection des informations manquantes (spec §3).

C'est ce qui décide si la boucle de recherche continue. Trois manques
distincts, du plus grave au plus discret :

1. **Aspect non couvert** — on demande un prix, aucune source n'en donne.
2. **Mot-clé absent** — un terme distinctif de la question n'apparaît nulle part.
3. **Fait non confirmé** — une valeur n'est donnée que par une seule source.

Le troisième mérite d'exister : une information isolée n'est pas une
information vérifiée, et c'est précisément le cas où une recherche
supplémentaire apporte quelque chose.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from ..core.models import SourceDoc
from .compare import COMPARABLE, agreements
from .facts import Fact, context_words

#: Aspect → (famille de faits attendue, mots déclencheurs, mot pour relancer)
ASPECTS: dict[str, tuple[str, set[str], str]] = {
    "prix": (
        "money",
        {"prix", "tarif", "tarifs", "cout", "coute", "coutent", "combien",
         "payer", "budget", "montant", "cher", "gratuit", "price", "cost"},
        "tarif officiel",
    ),
    "duree": (
        "duration",
        {"duree", "dure", "durent", "temps", "long", "longtemps", "heures",
         "minutes", "duration", "how long"},
        "durée du trajet",
    ),
    "distance": (
        "distance",
        {"distance", "kilometres", "loin", "eloigne", "trajet", "distance"},
        "distance en km",
    ),
    "date": (
        "year",
        {"date", "annee", "calendrier", "millesime", "edition"},
        "date officielle",
    ),
    "horaire": (
        "time",
        {"heure", "heures", "horaire", "horaires", "quand", "depart",
         "departs", "arrivee", "matin", "soir", "planning", "schedule",
         "when", "time"},
        "horaire officiel",
    ),
    "proportion": (
        "percent",
        # ⚠️ « part » est ambigu : dans « à quelle heure part le bateau », c'est
        # un verbe. Le garder faisait chercher un pourcentage à l'agent.
        {"pourcentage", "taux", "proportion", "percent"},
        "chiffres officiels",
    ),
}

#: Tous les mots déclencheurs d'aspect confondus
_ALL_TRIGGERS: set[str] = set()

_STOP = {
    "les", "des", "une", "un", "le", "la", "de", "du", "et", "ou", "que",
    "qui", "quoi", "est", "sont", "pour", "avec", "dans", "sur", "par",
    "aux", "au", "en", "ce", "cette", "ces", "son", "sa", "ses", "plus",
    "entre", "vers", "quel", "quelle", "quels", "quelles", "comment",
    "pourquoi", "combien", "the", "of", "and", "to", "in", "is", "for",
}


for _kind, _triggers, _hint in ASPECTS.values():
    _ALL_TRIGGERS |= {t.replace(" ", "") for t in _triggers} | _triggers


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _stems(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]{3,}", _normalize(text))
    return {
        (w[:-1] if len(w) > 4 and w.endswith("s") else w)
        for w in words
        if w not in _STOP
    }


def _stem_set(words: set[str]) -> set[str]:
    """Applique la même réduction du pluriel que :func:`_stems`."""
    return {w[:-1] if len(w) > 4 and w.endswith("s") else w for w in words}


@dataclass
class Gap:
    """Une information qui manque, et de quoi la chercher."""

    kind: str        # aspect | keyword | confirmation
    label: str       # explication lisible par l'utilisateur
    hint: str        # complément à ajouter à la requête de relance
    priority: int = 1  # 1 = le plus urgent

    def to_dict(self) -> dict:
        return {"kind": self.kind, "label": self.label, "hint": self.hint}


def detect_aspects(question: str) -> set[str]:
    """Ce que la question réclame explicitement.

    >>> sorted(detect_aspects("Combien coûte la traversée et combien de temps dure-t-elle ?"))
    ['duree', 'prix']
    """
    words = _stems(question) | set(_normalize(question).split())
    found = set()
    for aspect, (_, triggers, _hint) in ASPECTS.items():
        if words & {_normalize(t) for t in triggers}:
            found.add(aspect)
    return found


def find_gaps(
    question: str,
    docs: list[SourceDoc],
    facts: list[Fact],
    *,
    subject_keywords: set[str] | None = None,
    domains: dict[int, str] | None = None,
) -> list[Gap]:
    """Liste les manques constatés après une passe de recherche."""
    gaps: list[Gap] = []
    kinds_found = {fact.kind for fact in facts}

    # 1. Aspects réclamés mais non couverts
    for aspect in sorted(detect_aspects(question)):
        expected, _triggers, hint = ASPECTS[aspect]
        if expected not in kinds_found:
            gaps.append(
                Gap(
                    kind="aspect",
                    label=f"aucune donnée chiffrée pour « {aspect} »",
                    hint=hint,
                    priority=1,
                )
            )

    # 2. Mots-clés du sujet absents de toutes les sources
    keywords = subject_keywords if subject_keywords is not None else _stems(question)
    # Les verbes déclencheurs d'aspect (« coûte », « dure »…) sont déjà traités
    # au point 1 ; les chercher tels quels dans les pages produisait de faux
    # manques du type « “coute” n'apparaît dans aucune source ».
    keywords = keywords - _ALL_TRIGGERS
    if keywords and docs:
        corpus = set()
        for doc in docs:
            corpus |= _stems(f"{doc.title} {doc.content}")
        for missing in sorted(keywords - corpus):
            if len(missing) < 4:
                continue  # trop court pour être discriminant
            gaps.append(
                Gap(
                    kind="keyword",
                    label=f"« {missing} » n'apparaît dans aucune source",
                    hint=missing,
                    priority=2,
                )
            )

    # 3. Toutes les sources viennent du même site : rien n'est croisé.
    #    Spec §2 : « consulter différentes sources » — un seul domaine, même
    #    lu trois fois, ne vaut qu'une source.
    sites = {doc.domain for doc in docs if doc.domain}
    if docs and len(sites) < 2:
        gaps.append(
            Gap(
                kind="diversity",
                label=(
                    f"toutes les sources viennent du même site ({next(iter(sites), '?')}) "
                    "— rien n'est recoupé"
                ),
                hint="autre source",
                priority=2,
            )
        )

    # 4. Valeurs avancées par une seule source — uniquement sur ce qui est
    #    demandé. Une page de voyage contient des dizaines de chiffres non
    #    confirmés dont l'utilisateur n'a que faire.
    expected = {ASPECTS[aspect][0] for aspect in detect_aspects(question)}
    if expected:
        focus = keywords or _stems(question)
        relevant = [
            fact
            for fact in facts
            if fact.kind in expected
            and fact.kind in COMPARABLE
            # …et qui parlent bien du sujet demandé : une page de voyage cite
            # des prix d'hôtel et de repas qui n'ont rien à voir.
            and (not focus or (_stem_set(fact.context) & focus))
        ]
        confirmed = {
            id(fact)
            for cluster in agreements(relevant, domains=domains)
            for fact in cluster
        }
        lonely = [fact for fact in relevant if id(fact) not in confirmed]
        if relevant and not confirmed:
            gaps.append(
                Gap(
                    kind="confirmation",
                    label=(
                        f"{len(lonely)} valeur(s) sur le sujet demandé, "
                        "aucune confirmée par une seconde source"
                    ),
                    hint="confirmation officielle",
                    priority=3,
                )
            )

    gaps.sort(key=lambda gap: gap.priority)
    return gaps


def coverage_ratio(question: str, docs: list[SourceDoc]) -> float:
    """Part des mots-clés de la question retrouvés dans les sources (0 → 1)."""
    keywords = _stems(question)
    if not keywords or not docs:
        return 0.0
    corpus: set[str] = set()
    for doc in docs:
        corpus |= _stems(f"{doc.title} {doc.content}")
    return len(keywords & corpus) / len(keywords)


__all__ = ["Gap", "find_gaps", "detect_aspects", "coverage_ratio", "ASPECTS", "context_words"]
