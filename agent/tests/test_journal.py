"""Journal de recherche (spec §17)."""

from __future__ import annotations

from ara.core.journal import MAX_SUMMARY_CHARS, JournalStore, ResearchLog

CHAMPS_REQUIS = {
    "timestamp",
    "task",
    "research_steps",
    "sources",
    "tools_used",
    "reasoning_steps_summary",
    "files_created",
    "iterations",
    "final_score",
    "errors",
}


def test_le_journal_contient_tous_les_champs_demandes():
    log = ResearchLog(task_id="abc", task="une tâche")
    assert CHAMPS_REQUIS <= set(log.to_dict())


def test_les_resumes_sont_tronques():
    """Garde-fou contre l'enregistrement d'un raisonnement complet."""
    log = ResearchLog(task_id="abc", task="t")
    log.add_summary("raisonnement " * 200)
    assert len(log.to_dict()["reasoning_steps_summary"][0]) <= MAX_SUMMARY_CHARS


def test_aucune_chaine_de_pensee_privee_nest_stockee():
    """Le journal n'expose que des champs opérationnels, pas de texte libre long."""
    log = ResearchLog(task_id="abc", task="t")
    log.add_step("search", "tarifs traversées")
    log.add_source("https://exemple.test/a", "Titre")

    payload = log.to_dict()
    assert set(payload) == CHAMPS_REQUIS | {
        "task_id", "complexity", "duration_ms",
    }
    assert "thoughts" not in payload
    assert "chain_of_thought" not in payload


def test_les_sources_ne_sont_pas_dupliquees():
    log = ResearchLog(task_id="abc", task="t")
    log.add_source("https://exemple.test/a", "Titre")
    log.add_source("https://exemple.test/a", "Titre bis")
    assert len(log.sources) == 1


def test_ecriture_et_relecture(tmp_path):
    store = JournalStore(tmp_path / "journal.jsonl")
    log = ResearchLog(task_id="abc", task="une tâche")
    log.add_tool("web_search")
    log.add_file("rapport.pdf")

    store.append(log)
    store.append(ResearchLog(task_id="def", task="autre tâche"))

    entries = store.read_all()
    assert len(entries) == 2
    assert entries[0]["tools_used"] == ["web_search"]
    assert entries[0]["files_created"] == ["rapport.pdf"]


def test_une_ligne_corrompue_ne_casse_pas_la_relecture(tmp_path):
    path = tmp_path / "journal.jsonl"
    store = JournalStore(path)
    store.append(ResearchLog(task_id="abc", task="ok"))
    with path.open("a", encoding="utf-8") as handle:
        handle.write("{ceci n'est pas du json}\n")

    assert len(store.read_all()) == 1
