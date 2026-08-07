"""Bout en bout : le pipeline complet, hors ligne (spec §1, §14, §20)."""

from __future__ import annotations

import pytest

from ara.agents.orchestrator import Orchestrator
from ara.core.events import STAGE_ORDER, EventBus, Stage, Status
from ara.core.journal import JournalStore


@pytest.fixture
def orchestrator(isolated_settings, monkeypatch):
    """Orchestrateur branché sur le corpus figé."""
    from ara.agents import orchestrator as module
    from ara.providers.search.fixture import FixtureSearch

    from .conftest import RESULTS

    monkeypatch.setattr(module, "get_search", lambda name: (FixtureSearch(dict(RESULTS)), ""))
    return Orchestrator(isolated_settings)


def _stages(bus: EventBus) -> dict[str, str]:
    return {
        event.stage.value: event.status.value
        for event in bus.history
        if event.type == "stage"
    }


def test_tache_simple_saute_recherche_et_creation(orchestrator):
    bus = EventBus()
    result = orchestrator.run("bonjour", bus=bus)

    stages = _stages(bus)
    assert stages[Stage.RESEARCH.value] == Status.SKIPPED.value
    assert stages[Stage.CREATION.value] == Status.SKIPPED.value
    assert result.complexity == "LOW"
    assert result.answer


def test_tache_complete_traverse_tout_le_pipeline(orchestrator):
    bus = EventBus()
    result = orchestrator.run(
        "Recherche les tarifs des traversées aux Comores et fais-moi un PDF", bus=bus
    )

    stages = _stages(bus)
    for stage in STAGE_ORDER:
        assert stage.value in stages, f"étape absente : {stage.value}"

    assert stages[Stage.RESEARCH.value] == Status.DONE.value
    assert stages[Stage.VERIFICATION.value] == Status.DONE.value
    assert result.errors == []
    assert len(result.sources) >= 2
    assert [f["format"] for f in result.files] == ["pdf"]


def test_le_pdf_produit_est_reellement_ouvrable(orchestrator, isolated_settings):
    from ara.documents.render import verify

    result = orchestrator.run(
        "Recherche les tarifs des traversées aux Comores et fais-moi un PDF"
    )
    path = isolated_settings.tasks_dir() / result.task_id / "files" / result.files[0]["name"]
    assert verify(path)["pages"] >= 1


def test_la_reponse_cite_les_sources_collectees(orchestrator):
    result = orchestrator.run("Recherche les tarifs des traversées aux Comores")
    assert "[S1]" in result.answer
    assert result.sources


def test_le_journal_est_ecrit_pour_chaque_tache(orchestrator, isolated_settings):
    orchestrator.run("Recherche les tarifs des traversées aux Comores et fais un PDF")
    entries = JournalStore(isolated_settings.journal_path()).read_all()

    assert len(entries) == 1
    entry = entries[0]
    assert entry["tools_used"]
    assert entry["sources"]
    assert entry["files_created"]
    assert entry["research_steps"]
    assert entry["duration_ms"] >= 0


def test_le_moteur_hors_ligne_previent_de_sa_degradation(orchestrator):
    result = orchestrator.run("Recherche les tarifs des traversées aux Comores")
    assert result.degraded is True
    assert any("extractive" in notice.lower() for notice in result.notices)


def test_deux_formats_demandes_produisent_deux_fichiers(orchestrator):
    result = orchestrator.run(
        "Recherche les tarifs des traversées et fais-moi un PDF et un fichier Word"
    )
    assert {f["format"] for f in result.files} == {"pdf", "docx"}


def test_une_panne_de_recherche_ne_fait_pas_echouer_la_tache(orchestrator, monkeypatch):
    from ara.core.errors import ProviderError
    from ara.providers.search.fixture import FixtureSearch

    def panne(self, query, *, limit=8):
        raise ProviderError("moteur hors service")

    monkeypatch.setattr(FixtureSearch, "search", panne)

    result = orchestrator.run("Recherche les tarifs des traversées aux Comores")
    assert result.answer, "une réponse doit être rendue malgré la panne"
    assert any("moteur hors service" in notice for notice in result.notices)


def test_une_panne_du_llm_laisse_une_reponse_de_repli(orchestrator, monkeypatch):
    from ara.core.errors import ProviderError
    from ara.providers.llm.offline import OfflineLLM

    monkeypatch.setattr(
        OfflineLLM, "complete",
        lambda self, request: (_ for _ in ()).throw(ProviderError("LLM indisponible")),
    )

    result = orchestrator.run("Recherche les tarifs des traversées aux Comores")
    assert "matière brute" in result.answer or result.answer
    assert any("LLM indisponible" in notice for notice in result.notices)


def test_le_systeme_sarrete_quand_le_temps_est_ecoule(orchestrator):
    """Règle finale : le système doit savoir s'arrêter."""
    import dataclasses

    orchestrator.settings = dataclasses.replace(orchestrator.settings, max_task_seconds=0)

    result = orchestrator.run("Recherche les tarifs des traversées aux Comores et fais un PDF")
    assert any("Temps maximal" in message for message in result.errors + result.notices)


def test_chaque_tache_a_son_propre_espace(orchestrator, isolated_settings):
    first = orchestrator.run("Recherche les tarifs des traversées et fais un PDF")
    second = orchestrator.run("Recherche les tarifs des traversées et fais un PDF")

    assert first.task_id != second.task_id
    for result in (first, second):
        directory = isolated_settings.tasks_dir() / result.task_id / "files"
        assert directory.is_dir()
        assert len(list(directory.iterdir())) == 1
