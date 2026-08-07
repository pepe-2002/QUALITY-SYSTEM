"""Mesures du laboratoire (spec §18).

Ce qu'on mesure, et pourquoi :

* **exactitude** — la valeur attendue figure-t-elle dans la réponse ? Vérifié
  par extraction de faits, jamais par jugement humain : c'est ce qui rend la
  mesure reproductible.
* **bruit** — une valeur piège est-elle présentée comme la réponse ? Une
  stratégie qui trouve la bonne valeur *et* en avance trois fausses n'a pas
  bien travaillé.
* **qualité de restitution** — citations, diversité des sources, aveu de ce qui
  manque. Indépendante de l'exactitude : on peut avoir raison sans le prouver.
* **coût** — recherches, pages, appels d'outils, jetons, temps.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ..analysis.facts import extract_facts
from .dataset import Gold, Task
from .harness import Outcome

#: Tolérance relative d'appariement d'une valeur attendue
TOLERANCE = 0.02


def _matches(fact, gold: Gold) -> bool:
    if fact.kind != gold.kind:
        return False
    marge = abs(gold.value) * TOLERANCE
    return (fact.low - marge) <= gold.value <= (fact.high + marge)


def _found(answer: str, gold: Gold) -> bool:
    return any(_matches(fact, gold) for fact in extract_facts(answer, 1, max_facts=200))


@dataclass
class Score:
    """Note d'une exécution sur une tâche."""

    accuracy: float = 0.0        # 0..1 — valeurs attendues retrouvées
    noise: float = 0.0           # 0..1 — valeurs pièges présentées
    quality: float = 0.0         # 0..1 — citations, diversité, transparence
    found: list[str] = None      # type: ignore[assignment]
    missed: list[str] = None     # type: ignore[assignment]
    traps: list[str] = None      # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.found = self.found or []
        self.missed = self.missed or []
        self.traps = self.traps or []

    @property
    def net(self) -> float:
        """Exactitude nette : trouver le bon, sans avancer le faux."""
        return max(0.0, self.accuracy - 0.5 * self.noise)

    def to_dict(self) -> dict:
        return {
            "accuracy": round(self.accuracy, 3),
            "noise": round(self.noise, 3),
            "net": round(self.net, 3),
            "quality": round(self.quality, 3),
            "found": self.found, "missed": self.missed, "traps": self.traps,
        }


def score(task: Task, outcome: Outcome) -> Score:
    """Note une exécution contre la vérité de référence."""
    result = Score()
    if not outcome.answer:
        result.missed = [g.label for g in task.gold]
        return result

    for gold in task.gold:
        if _found(outcome.answer, gold):
            result.found.append(gold.label)
        else:
            result.missed.append(gold.label)
    result.accuracy = len(result.found) / len(task.gold) if task.gold else 0.0

    for piege in task.distractors:
        if _found(outcome.answer, piege):
            result.traps.append(piege.label)
    result.noise = (
        len(result.traps) / len(task.distractors) if task.distractors else 0.0
    )

    result.quality = _quality(outcome, result)
    return result


def _quality(outcome: Outcome, result: Score) -> float:
    """Quatre exigences de restitution, à poids égal."""
    points = 0.0

    # 1. Ce qui est avancé est cité.
    if not outcome.sources or re.search(r"\[S\d+\]", outcome.answer):
        points += 0.25

    # 2. Les sources sont diversifiées.
    if outcome.domains >= 2 or not outcome.sources:
        points += 0.25

    # 3. Ce qui manque est dit. Une réponse incomplète qui l'avoue vaut mieux
    #    qu'une réponse incomplète qui se tait.
    avoue = bool(outcome.gaps) or "manquante" in outcome.answer.lower()
    if not result.missed or avoue:
        points += 0.25

    # 4. Aucune valeur piège n'est présentée.
    if not result.traps:
        points += 0.25

    return points


@dataclass
class Row:
    """Une ligne du tableau de résultats : une stratégie sur une tâche."""

    task: Task
    outcome: Outcome
    score: Score
    #: erreurs relevées après coup (H2) — voir `lab/stops.py`
    errors: object = None

    def to_dict(self) -> dict:
        data = {**self.outcome.to_dict(), **self.score.to_dict(),
                "family": self.task.family}
        if self.errors is not None:
            data["errors"] = self.errors.to_dict()
        return data


def cost(outcome: Outcome, price_per_1k_tokens: float = 0.0) -> float:
    """Coût monétaire estimé.

    Nul avec le moteur hors-ligne : c'est la vérité, et le rapport doit le
    dire plutôt que d'inventer un chiffre. Le paramètre existe pour rejouer la
    même expérience avec un fournisseur payant.
    """
    return outcome.tokens / 1000 * price_per_1k_tokens
