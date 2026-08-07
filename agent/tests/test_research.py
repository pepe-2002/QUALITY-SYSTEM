"""Recherche, extraction et citations (spec §20)."""

from __future__ import annotations

import re

from ara.agents.gather import collect
from ara.agents.planner import plan
from ara.core.html_text import extract
from ara.providers.llm.base import LLMRequest
from ara.providers.llm.offline import OfflineLLM
from ara.providers.search.engines import MultiSearch, _unwrap_ddg
from ara.providers.search.fixture import FixtureSearch

from .conftest import RESULTS


# --- Extraction ---------------------------------------------------------------


def test_extraction_supprime_scripts_et_recupere_le_titre():
    html = "<html><head><title>Titre</title></head><body><p>Bonjour</p><script>var x=1;</script></body></html>"
    title, text = extract(html)
    assert title == "Titre"
    assert "Bonjour" in text
    assert "var x" not in text


def test_extraction_tolere_du_html_casse():
    title, text = extract("<p>Texte non fermé <b>gras")
    assert "Texte non fermé" in text


def test_extraction_tronque_les_pages_longues():
    _, text = extract("<p>" + ("mot " * 20_000) + "</p>", max_chars=500)
    assert len(text) <= 520
    assert text.endswith("[…]")


# --- Moteurs ------------------------------------------------------------------


def test_le_moteur_de_test_rejoue_le_corpus(search_provider):
    results = search_provider.search("traversées comores tarifs")
    assert len(results) == 3
    assert results[0].url.startswith("https://")


def test_duckduckgo_deballe_ses_liens_de_redirection():
    wrapped = "//duckduckgo.com/l/?uddg=https%3A%2F%2Fexemple.test%2Fpage&rut=abc"
    assert _unwrap_ddg(wrapped) == "https://exemple.test/page"


def test_multisearch_dedoublonne_et_survit_a_un_moteur_en_panne():
    class Cassé(FixtureSearch):
        name = "cassé"

        def search(self, query, *, limit=8):
            raise RuntimeError("panne simulée")

    from ara.core.errors import ProviderError

    class CasséPropre(Cassé):
        def search(self, query, *, limit=8):
            raise ProviderError("panne simulée")

    multi = MultiSearch([CasséPropre(), FixtureSearch(dict(RESULTS)), FixtureSearch(dict(RESULTS))])
    results = multi.search("traversées comores tarifs")

    assert len(results) == 3, "les doublons entre moteurs doivent être fusionnés"
    assert any("panne simulée" in failure for failure in multi.failures)


# --- Collecte -----------------------------------------------------------------


def test_la_collecte_consulte_plusieurs_sources(ctx, toolbox):
    ctx.prompt = "Recherche les tarifs des traversées aux Comores"
    task_plan = plan(ctx.prompt, max_search_steps=3)
    ctx.budget = task_plan.budget

    docs = collect(ctx, task_plan, toolbox)

    assert len(docs) >= 2, "l'agent ne doit jamais se contenter d'une seule source"
    assert len({doc.domain for doc in docs}) >= 2
    assert all(doc.text for doc in docs)


def test_la_collecte_respecte_le_budget_de_recherche(ctx, toolbox):
    task_plan = plan("Compare et vérifie les tarifs et fais un PDF", max_search_steps=2)
    ctx.budget = task_plan.budget
    collect(ctx, task_plan, toolbox)
    assert ctx.budget.used_searches <= 2


def test_une_url_illisible_ne_casse_pas_la_tache(ctx, toolbox):
    task_plan = plan("Analyse https://inconnue.test/page")
    ctx.budget = task_plan.budget
    docs = collect(ctx, task_plan, toolbox)
    assert docs == []
    assert any("inconnue.test" in error for error in ctx.journal.errors)


# --- Citations ----------------------------------------------------------------


def test_la_synthese_hors_ligne_cite_ses_sources(ctx, toolbox):
    task_plan = plan("Recherche les tarifs des traversées aux Comores", max_search_steps=3)
    ctx.budget = task_plan.budget
    docs = collect(ctx, task_plan, toolbox)

    answer = OfflineLLM().complete(
        LLMRequest(task="synthesis", question=ctx.prompt, documents=docs)
    ).text

    assert "[S1]" in answer
    assert "Sources" in answer
    for doc in docs:
        assert doc.url in answer


def test_la_synthese_hors_ligne_ne_fabrique_rien(ctx, toolbox):
    """Les phrases restituées doivent provenir des sources, mot pour mot."""
    question = "Quel est le tarif d'une traversée entre la Grande Comore et Mohéli ?"
    task_plan = plan(question, max_search_steps=3)
    ctx.budget = task_plan.budget
    docs = collect(ctx, task_plan, toolbox)
    corpus = " ".join(" ".join(doc.text.split()) for doc in docs)

    answer = OfflineLLM().complete(
        LLMRequest(task="synthesis", question=question, documents=docs)
    ).text

    # Les phrases citées ont la forme « - <phrase> [Sn] ».
    # (La liste des sources, elle, commence par « - [Sn] » : on l'ignore.)
    quoted = [
        match.group(1).strip()
        for match in (re.match(r"^- (?!\[S)(.*) \[S\d+\]$", line) for line in answer.splitlines())
        if match
    ]
    assert quoted, "la synthèse doit contenir des phrases citées"
    for sentence in quoted:
        assert sentence in corpus


def test_sans_source_le_moteur_hors_ligne_le_dit():
    answer = OfflineLLM().complete(LLMRequest(task="answer", question="Qui es-tu ?")).text
    assert "hors-ligne" in answer.lower()


# --- Filtrage des sources hors sujet ------------------------------------------


def test_une_page_hors_sujet_est_ecartee(ctx, toolbox, monkeypatch):
    """Défaut constaté en réel : un moteur ramène une page sans rapport."""
    from ara.core import http
    from ara.providers.search.fixture import FixtureSearch

    hors_sujet = "https://hors-sujet.test/algerie"
    page = (
        "<html><head><title>Algérie française</title></head><body><p>"
        "La régence d'Alger jouissait d'une grande autonomie au XIXe siècle."
        "</p></body></html>"
    )
    vraie_requete = http.request

    def servir(url, **kwargs):
        if url == hors_sujet:
            return http.HttpResponse(
                url=url, status=200, body=page.encode("utf-8"),
                content_type="text/html; charset=utf-8",
            )
        return vraie_requete(url, **kwargs)

    monkeypatch.setattr(http, "get", servir)

    corpus = {
        "tarifs traversées Comores Mohéli": [
            {"title": "Tarifs des vedettes rapides", "url": "https://autre.test/tarifs"},
            {"title": "Algérie française", "url": hors_sujet},
        ]
    }
    ctx.search = FixtureSearch(corpus)

    task_plan = plan("Recherche les tarifs des traversées aux Comores vers Mohéli",
                     max_search_steps=2)
    ctx.budget = task_plan.budget
    docs = collect(ctx, task_plan, toolbox)

    domaines = {doc.domain for doc in docs}
    assert "autre.test" in domaines
    assert "hors-sujet.test" not in domaines
    assert any(step["kind"] == "reject" for step in ctx.journal.research_steps)


def test_le_filtre_ne_sactive_pas_sur_une_question_trop_courte(ctx, toolbox):
    """Sans mots-clés distinctifs, mieux vaut tout garder que tout jeter."""
    from ara.providers.search.fixture import FixtureSearch

    ctx.search = FixtureSearch(
        {"meteo": [{"title": "Météo maritime", "url": "https://troisieme.test/meteo"}]}
    )
    task_plan = plan("meteo", max_search_steps=1)
    ctx.budget = task_plan.budget
    assert len(collect(ctx, task_plan, toolbox)) == 1
