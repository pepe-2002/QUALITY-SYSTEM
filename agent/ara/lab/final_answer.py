"""FINAL_ANSWER_ACCURACY — noter ce que l'utilisateur lit, et rien d'autre.

Le diagnostic avait relevé une faiblesse de la métrique historique :
l'exactitude était mesurée sur la réponse **entière**, bilan d'analyse compris.
Une valeur enfouie dans les traces comptait donc comme une réponse — alors que
personne ne l'avait lue.

Cette métrique-ci est séparée, et elle le reste :

* elle **ne réécrit pas** H1 ni H2, qui gardent la leur ;
* elle s'applique aux expériences **nouvelles** ;
* elle ne regarde que la partie effectivement présentée : ce qui suit le
  marqueur de bilan est retiré, ainsi que les sections d'analyse.

Trois pannes qu'elle doit attraper, et qui échappaient à l'ancienne :

1. une information cachée dans le diagnostic comptée comme réponse ;
2. « je n'ai pas trouvé » alors que le système avait la valeur ;
3. une valeur **fausse** affichée alors que la bonne existait dans les traces.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..analysis.facts import extract_facts
from .dataset import Task
from .harness import Outcome
from .metrics import TOLERANCE, _matches

#: Marqueurs qui ouvrent la partie « traces » d'une réponse. Tout ce qui suit
#: est du travail interne rendu visible, pas la réponse elle-même.
TRACE_MARKERS = (
    "## Déroulé de la recherche",
    "## Sources",
    "**Sources :**",
    "CONTRADICTION DÉTECTÉE",
    "**Informations manquantes**",
    "## Limites",
)

#: Formules par lesquelles un agent déclare ne pas savoir.
_ADMISSIONS = re.compile(
    r"\b(?:je\s+n'ai\s+(?:pas\s+)?trouv|aucune\s+information|pas\s+d'information"
    r"|introuvable|non\s+trouv|aucune\s+source|rien\s+trouv"
    r"|impossible\s+de\s+d[ée]terminer)\w*",
    re.IGNORECASE,
)


def user_facing(answer: str) -> str:
    """Partie de la réponse réellement adressée à l'utilisateur.

    Tout ce qui suit le premier marqueur de trace est retiré. C'est volontaire
    et un peu brutal : mieux vaut sous-estimer ce que l'utilisateur lit que
    compter comme lue une valeur enfouie dans un bilan.
    """
    texte = str(answer or "")
    coupures = [texte.find(marqueur) for marqueur in TRACE_MARKERS]
    coupures = [position for position in coupures if position >= 0]
    if coupures:
        texte = texte[: min(coupures)]
    return texte.strip()


@dataclass
class FinalAnswerScore:
    """Note d'une réponse, jugée sur ce qui est affiché."""

    accuracy: float = 0.0
    found: list[str] = field(default_factory=list)
    missed: list[str] = field(default_factory=list)
    wrong: list[str] = field(default_factory=list)
    hidden: list[str] = field(default_factory=list)
    admits_failure: bool = False

    @property
    def silent_success(self) -> bool:
        """Le système avait la réponse et ne l'a pas dite."""
        return bool(self.hidden) and not self.found

    @property
    def confidently_wrong(self) -> bool:
        """Une valeur fausse est affichée alors que la bonne était connue."""
        return bool(self.wrong) and bool(self.hidden)

    def to_dict(self) -> dict:
        return {
            "final_answer_accuracy": round(self.accuracy, 3),
            "found": self.found, "missed": self.missed, "wrong": self.wrong,
            "hidden": self.hidden, "admits_failure": self.admits_failure,
            "silent_success": self.silent_success,
            "confidently_wrong": self.confidently_wrong,
        }


def _contains(text: str, gold) -> bool:
    facts = extract_facts(text, 1, max_facts=200)
    return any(_matches(fact, gold) for fact in facts)


def final_answer_accuracy(task: Task, outcome: Outcome) -> FinalAnswerScore:
    """Note la réponse sur ce qu'elle **montre**.

    `hidden` recense les valeurs que le système possédait — dans ses traces ou
    dans ses sources — mais n'a pas affichées. C'est ce qui distingue « il ne
    savait pas » de « il savait et s'est tu ».
    """
    note = FinalAnswerScore()
    visible = user_facing(outcome.answer)
    interne = str(outcome.answer or "")[len(visible):]
    sources = " ".join(f"{doc.title} {doc.content}" for doc in outcome.sources)

    note.admits_failure = bool(_ADMISSIONS.search(visible))

    for gold in task.gold:
        if _contains(visible, gold):
            note.found.append(gold.label)
            continue
        note.missed.append(gold.label)
        if _contains(interne, gold) or _contains(sources, gold):
            note.hidden.append(gold.label)

    note.accuracy = len(note.found) / len(task.gold) if task.gold else 0.0

    for piege in task.distractors:
        if _contains(visible, piege):
            note.wrong.append(piege.label)

    return note


__all__ = [
    "FinalAnswerScore",
    "TOLERANCE",
    "TRACE_MARKERS",
    "final_answer_accuracy",
    "user_facing",
]
