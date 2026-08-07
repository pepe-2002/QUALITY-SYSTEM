"""Contrôleur TASK_COMPLEXITY (spec §4)."""

from __future__ import annotations

import pytest

from ara.core.complexity import BUDGETS, Complexity, assess


@pytest.mark.parametrize(
    "prompt, expected",
    [
        ("bonjour", Complexity.LOW),
        ("merci", Complexity.LOW),
        ("Recherche les horaires des traversées", Complexity.MEDIUM),
        (
            "Compare les tarifs de trois compagnies, vérifie les horaires "
            "et fais-moi un rapport PDF avec les sources",
            Complexity.HIGH,
        ),
    ],
)
def test_niveaux_de_complexite(prompt, expected):
    assert assess(prompt).complexity is expected


def test_budget_croit_avec_la_complexite():
    low = BUDGETS[Complexity.LOW][0]
    high = BUDGETS[Complexity.HIGH][0]
    assert low < high


def test_le_plafond_dur_est_respecte():
    budget = assess("compare analyse vérifie et fais un PDF et un docx", max_search_steps=2)
    assert budget.search_steps <= 2


def test_escalade_et_desescalade():
    budget = assess("bonjour")
    assert budget.complexity is Complexity.LOW

    assert budget.escalate("information manquante") is True
    assert budget.complexity is Complexity.MEDIUM
    assert budget.escalate("contradiction") is True
    assert budget.complexity is Complexity.HIGH

    # Au sommet, on ne peut plus qu'élargir jusqu'au plafond dur, puis s'arrêter.
    while budget.escalate():
        pass
    assert budget.search_steps <= budget.max_search_steps
    assert budget.escalate() is False

    assert budget.de_escalate() is True
    assert budget.complexity is Complexity.MEDIUM


def test_consommation_des_recherches_borne_le_travail():
    budget = assess("recherche les tarifs et compare les sources")
    total = budget.search_steps
    for _ in range(total):
        assert budget.remaining_searches > 0
        budget.consume_search()
    assert budget.remaining_searches == 0
