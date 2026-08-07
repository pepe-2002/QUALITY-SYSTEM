"""Planificateur : décider avant d'agir."""

from __future__ import annotations

import pytest

from ara.agents.planner import plan


def test_demande_simple_ne_declenche_ni_recherche_ni_fichier():
    result = plan("bonjour")
    assert result.needs_research is False
    assert result.needs_documents is False


def test_detecte_recherche_et_pdf():
    result = plan("Recherche les horaires des traversées et fais-moi un PDF")
    assert result.needs_research is True
    assert result.formats == ["pdf"]


def test_detecte_plusieurs_formats():
    result = plan("Fais-moi un rapport en PDF et en Word sur le tourisme")
    assert set(result.formats) == {"pdf", "docx"}


def test_mot_rapport_implique_un_pdf():
    result = plan("Prépare un rapport sur les traversées maritimes")
    assert "pdf" in result.formats


def test_url_fournie_est_collectee_et_declenche_la_recherche():
    result = plan("Analyse https://exemple.test/traversees pour moi")
    assert result.urls == ["https://exemple.test/traversees"]
    assert result.needs_research is True


def test_nom_de_fichier_derive_de_la_demande():
    result = plan("Recherche les tarifs des traversées aux Comores")
    assert result.filename_hint
    assert "/" not in result.filename_hint
    assert " " not in result.filename_hint


# --- Questions factuelles -----------------------------------------------------


@pytest.mark.parametrize(
    "question",
    [
        "Qui a écrit Le Petit Prince ?",
        "Combien coûte une traversée ?",
        "Quand part la prochaine vedette ?",
        "Pourquoi la mer est agitée en février ?",
        "Où se trouve Hoani",
    ],
)
def test_une_question_factuelle_declenche_une_recherche(question):
    """L'agent n'a pas de connaissance propre : une question exige des sources."""
    assert plan(question).needs_research is True


@pytest.mark.parametrize(
    "politesse",
    ["bonjour", "salut", "merci", "ça va ?", "qui es-tu ?", "comment vas-tu ?"],
)
def test_les_politesses_ne_declenchent_pas_de_recherche(politesse):
    assert plan(politesse).needs_research is False


def test_le_nom_de_fichier_ignore_les_consignes():
    """« fais-moi un PDF » ne doit pas se retrouver dans le nom du fichier."""
    hint = plan("Qui a écrit Le Petit Prince ? Fais-moi un PDF").filename_hint
    for consigne in ("fais", "pdf", "moi"):
        assert consigne not in hint.split("-")
    assert "prince" in hint
