"""Où l'agent échoue — attribution d'une panne à une étape du pipeline.

Savoir qu'une réponse est fausse ne dit pas quoi corriger. Ce module range
chaque échec à l'étape où l'information a été perdue :

    RECHERCHE        la bonne source n'a jamais été trouvée
    EXTRACTION       la bonne information était là, mal extraite
    CONTEXTUALISATION la bonne information, mais mauvais lieu / date / contexte
    COMPARAISON      sources correctes, mal confrontées
    RAISONNEMENT     informations correctes, conclusion incorrecte
    GÉNÉRATION       conclusion correcte, réponse finale incorrecte

L'attribution suit l'ordre du pipeline et s'arrête à la **première** étape
fautive : une information jamais trouvée ne peut pas être mal extraite. C'est
ce qui rend le comptage lisible — sinon un même échec apparaîtrait partout.

Chaque règle est mécanique et vérifiable. Aucune ne demande de juger la
qualité d'une réponse : on compare des ensembles de faits.

⚠️ Limite assumée sur GÉNÉRATION. L'exactitude est mesurée sur la réponse
**entière**, bilan d'analyse compris ; une valeur qui n'apparaît que dans le
bilan est donc comptée comme trouvée, et cette étape ne se déclenche jamais.
La corriger demanderait de changer la métrique de H1 et H2, donc de rendre
leurs chiffres irreproductibles. Un test fige ce comportement pour que la
limite reste visible.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..analysis.facts import extract_facts
from .dataset import Gold, Task
from .harness import Outcome
from .metrics import Score, _matches

#: Étapes, dans l'ordre du pipeline.
STAGES = (
    "recherche",
    "extraction",
    "contextualisation",
    "comparaison",
    "raisonnement",
    "generation",
)

STAGE_LABELS = {
    "recherche": "RECHERCHE",
    "extraction": "EXTRACTION",
    "contextualisation": "CONTEXTUALISATION",
    "comparaison": "COMPARAISON",
    "raisonnement": "RAISONNEMENT",
    "generation": "GÉNÉRATION",
    "aucune": "réponse correcte",
}

STAGE_MEANING = {
    "recherche": "mauvaise source trouvée",
    "extraction": "bonne information présente mais mal extraite",
    "contextualisation": "bonne information mais mauvais lieu, date ou contexte",
    "comparaison": "sources correctes mais mal confrontées",
    "raisonnement": "informations correctes mais conclusion incorrecte",
    "generation": "conclusion correcte mais réponse finale incorrecte",
    "aucune": "aucune panne",
}


@dataclass
class Diagnosis:
    """Où la chaîne a lâché, et pourquoi on le pense."""

    stage: str
    reason: str

    @property
    def failed(self) -> bool:
        return self.stage != "aucune"

    @property
    def label(self) -> str:
        return STAGE_LABELS.get(self.stage, self.stage)

    def to_dict(self) -> dict:
        return {"stage": self.stage, "label": self.label, "reason": self.reason}


def _number_forms(value: float) -> list[str]:
    """Écritures plausibles d'un nombre dans une page (« 15000 », « 15 000 »)."""
    entier = int(round(value))
    brut = str(entier)
    formes = {brut}
    if len(brut) > 3:
        # groupes de trois, séparateur quelconque
        groupes = []
        reste = brut
        while len(reste) > 3:
            groupes.insert(0, reste[-3:])
            reste = reste[:-3]
        groupes.insert(0, reste)
        formes.add(" ".join(groupes))
    return sorted(formes)


def _in_raw_text(gold: Gold, text: str) -> bool:
    """La valeur attendue figure-t-elle **littéralement** dans le texte ?

    Sert à distinguer « jamais trouvé » de « trouvé mais mal lu » : si le
    nombre est écrit noir sur blanc dans une source retenue et que l'extracteur
    ne l'a pas produit, la panne est à l'extraction.
    """
    normalise = re.sub(r"[   ]", " ", text)
    for forme in _number_forms(gold.value):
        motif = re.escape(forme).replace(r"\ ", r"[\s.,]?")
        if re.search(rf"(?<!\d){motif}(?!\d)", normalise):
            return True
    return False


def _facts_of(outcome: Outcome) -> list:
    faits = []
    for index, doc in enumerate(outcome.sources, start=1):
        faits.extend(extract_facts(f"{doc.title} {doc.content}", index, max_facts=200))
    return faits


def _split_answer(answer: str) -> tuple[str, str]:
    """Sépare la synthèse rendue du bilan de recherche qui la suit."""
    marqueur = "## Déroulé de la recherche"
    if marqueur in answer:
        avant, _, apres = answer.partition(marqueur)
        return avant, apres
    return answer, ""


def diagnose(task: Task, outcome: Outcome, score: Score) -> Diagnosis:
    """Range l'échec d'une exécution à une étape du pipeline."""
    if score.accuracy >= 0.999 and score.noise <= 0:
        return Diagnosis("aucune", "la réponse contient la valeur attendue")

    manquants = [g for g in task.gold if g.label in score.missed]
    texte_sources = " ".join(
        f"{doc.title} {doc.content}" for doc in outcome.sources
    )
    faits = _facts_of(outcome)

    # 1. RECHERCHE — l'information n'est jamais entrée dans le pipeline.
    if manquants:
        litteral = [g for g in manquants if _in_raw_text(g, texte_sources)]
        if not litteral:
            return Diagnosis(
                "recherche",
                "la valeur attendue ne figure dans aucune source retenue : "
                f"{len(outcome.sources)} source(s) lue(s), aucune ne la contient",
            )

        # 2. EXTRACTION — elle est écrite dans une page, mais mal lue.
        extraits = [g for g in litteral if any(_matches(f, g) for f in faits)]
        non_extraits = [g for g in litteral if g not in extraits]
        if non_extraits:
            return Diagnosis(
                "extraction",
                f"« {non_extraits[0].label} » est écrit dans une source retenue "
                "mais l'extracteur ne l'a pas produit comme fait chiffré",
            )

    # 3. CONTEXTUALISATION — une valeur piège est avancée comme la réponse.
    if score.noise > 0:
        return Diagnosis(
            "contextualisation",
            f"une valeur d'un autre contexte est présentée comme la réponse : "
            f"{', '.join(score.traps)}",
        )

    # 4. COMPARAISON — le désaccord existait et n'a pas été tranché.
    if manquants and task.distractors:
        pieges_presents = [
            d for d in task.distractors if any(_matches(f, d) for f in faits)
        ]
        if pieges_presents and not outcome.contradictions:
            return Diagnosis(
                "comparaison",
                "la bonne valeur et une valeur incompatible étaient toutes deux "
                "extraites, sans qu'aucun désaccord ne soit signalé",
            )

    # 5/6. La valeur était disponible et non contredite : la panne est en aval.
    if manquants:
        synthese, bilan = _split_answer(outcome.answer)
        dans_le_bilan = any(_in_raw_text(g, bilan) for g in manquants)
        if dans_le_bilan:
            return Diagnosis(
                "generation",
                "la valeur figure dans le bilan d'analyse mais pas dans la "
                "réponse rendue à l'utilisateur",
            )
        return Diagnosis(
            "raisonnement",
            "la valeur était extraite, cohérente et non contredite, mais la "
            "réponse ne la retient pas",
        )

    return Diagnosis("aucune", "aucune valeur attendue manquante")


def tally(diagnoses) -> dict[str, int]:
    """Compte les pannes par étape."""
    compte: dict[str, int] = {}
    for diagnosis in diagnoses:
        compte[diagnosis.stage] = compte.get(diagnosis.stage, 0) + 1
    return compte


__all__ = ["Diagnosis", "STAGES", "STAGE_LABELS", "STAGE_MEANING", "diagnose", "tally"]
