"""Pourquoi l'agent s'est arrêté, et où il s'est trompé.

Deux analyses distinctes, et il faut les garder distinctes :

* **la raison d'arrêt** est ce que le contrôleur *déclare*. Elle se lit sans
  connaître la bonne réponse.
* **l'erreur** est ce que la vérité de référence *révèle après coup*. Elle ne
  se lit qu'en comparant à l'or, et parfois qu'en comparant les stratégies
  entre elles.

Confondre les deux serait commode et faux : un contrôleur qui déclare
« information suffisante » sur une réponse fausse n'a pas mal déclaré, il a
mal jugé — et c'est précisément ce qu'on veut compter séparément.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..analysis.report import STOP_CODES
from .dataset import Task
from .harness import Outcome
from .metrics import Score

#: Raisons d'arrêt, dans l'ordre où on aime les lire.
STOP_ORDER = (
    "information_suffisante",
    "difficulte_faible",
    "contradiction_tranchee",
    "manque_information",
    "limite_budget",
    "erreur_controleur",
)

STOP_LABELS = {
    "information_suffisante": "information suffisante",
    "difficulte_faible": "difficulté faible",
    "contradiction_tranchee": "contradiction vérifiée",
    "manque_information": "manque d'information",
    "limite_budget": "limite de budget",
    "erreur_controleur": "erreur du contrôleur",
    "passe_unique": "passe unique (pas de décision d'arrêt)",
}

#: Catégories d'erreur, telles que définies avant l'expérience.
ERROR_ORDER = (
    "arret_trop_tot",
    "recherche_inutile",
    "mauvaise_detection_suffisance",
    "fausse_contradiction",
    "contradiction_manquee",
)

ERROR_LABELS = {
    "arret_trop_tot": "arrêt trop tôt",
    "recherche_inutile": "recherche inutile",
    "mauvaise_detection_suffisance": "mauvaise détection de suffisance",
    "fausse_contradiction": "contradiction signalée à tort",
    "contradiction_manquee": "contradiction non détectée",
}


def stop_reason(outcome: Outcome) -> str:
    """Raison d'arrêt normalisée d'une exécution.

    Les stratégies à passe unique (FIXED, ADAPTIVE REASONING, MODEL ONLY) ne
    prennent aucune décision d'arrêt : elles dépensent leur budget puis
    répondent. Les ranger dans « limite de budget » gonflerait artificiellement
    cette case ; elles ont donc leur propre étiquette.
    """
    if outcome.error:
        return "erreur_controleur"
    if outcome.stop_code in STOP_CODES:
        return outcome.stop_code
    return "passe_unique"


@dataclass
class ErrorTally:
    """Erreurs relevées sur une exécution, une fois la vérité connue."""

    kinds: set[str] = field(default_factory=set)
    wasted_searches: int = 0
    detail: list[str] = field(default_factory=list)

    def add(self, kind: str, detail: str = "") -> None:
        self.kinds.add(kind)
        if detail:
            self.detail.append(detail)

    def to_dict(self) -> dict:
        return {
            "kinds": sorted(self.kinds),
            "wasted_searches": self.wasted_searches,
            "detail": self.detail,
        }


def classify_errors(
    task: Task,
    outcome: Outcome,
    score: Score,
    *,
    best_searches: int | None,
    someone_found: bool,
) -> ErrorTally:
    """Classe les erreurs d'une exécution.

    `best_searches` : le plus petit nombre de recherches avec lequel une
    stratégie a trouvé la bonne réponse sur *cette* tâche et *cette* graine.
    `someone_found` : au moins une stratégie a trouvé. Ces deux informations
    viennent de la comparaison entre stratégies — c'est le seul moyen honnête
    de dire qu'une réponse manquée était **atteignable**.
    """
    tally = ErrorTally()
    trouve = score.accuracy >= 0.999
    raison = stop_reason(outcome)

    # 1. Arrêt trop tôt — la réponse existait, une autre stratégie l'a eue.
    if not trouve and someone_found:
        tally.add(
            "arret_trop_tot",
            f"arrêté après {outcome.searches} recherche(s) alors que la réponse "
            "était atteignable",
        )

    # 2. Recherche inutile — trouvé, mais plus cher que nécessaire.
    if trouve and best_searches is not None and outcome.searches > best_searches:
        tally.wasted_searches = outcome.searches - best_searches
        tally.add(
            "recherche_inutile",
            f"{tally.wasted_searches} recherche(s) de plus que le minimum "
            f"suffisant ({best_searches})",
        )

    # 3. Suffisance mal jugée — « plus rien ne manque », et pourtant si.
    if not trouve and raison in {"information_suffisante", "contradiction_tranchee"}:
        tally.add(
            "mauvaise_detection_suffisance",
            "le contrôleur a déclaré l'information suffisante sur une réponse fausse",
        )

    # 4. Contradictions : signalée à tort, ou manquée.
    #    Une tâche sans valeur piège n'a pas de désaccord à trouver dans le
    #    corpus : y signaler une contradiction est une fausse alerte.
    if outcome.contradictions and not task.distractors:
        tally.add(
            "fausse_contradiction",
            f"{len(outcome.contradictions)} désaccord(s) signalé(s) sur une "
            "tâche qui n'en contient pas",
        )
    if score.noise > 0 and not outcome.contradictions:
        tally.add(
            "contradiction_manquee",
            "une valeur piège est présentée comme la réponse sans qu'aucun "
            "désaccord n'ait été signalé",
        )

    return tally


def tally_stops(rows) -> dict[str, int]:
    """Compte les raisons d'arrêt d'un ensemble de lignes."""
    compte: dict[str, int] = {}
    for row in rows:
        code = stop_reason(row.outcome)
        compte[code] = compte.get(code, 0) + 1
    return compte


__all__ = [
    "ERROR_LABELS",
    "ERROR_ORDER",
    "ErrorTally",
    "STOP_LABELS",
    "STOP_ORDER",
    "classify_errors",
    "stop_reason",
    "tally_stops",
]
