"""Boucle de recherche adaptative (spec §3, §4) — Phase 2.

Scénarios joués sur un web scripté : on contrôle exactement ce que chaque
requête ramène, donc ce que l'agent doit décider. C'est la seule façon de
tester une boucle de décision sans dépendre de l'état réel d'Internet.
"""

from __future__ import annotations

import dataclasses

import pytest

from ara.agents.planner import plan
from ara.agents.research import MAX_CYCLES, ResearchAgent
from ara.core.models import SearchResult
from ara.providers.search.base import SearchProvider

# --- Web scripté --------------------------------------------------------------

PAGE_BON_MARCHE = """
<html><head><title>Tarifs des traversées</title></head><body>
<p>Le billet de la traversée entre Grande Comore et Mohéli coûte
15 000 francs comoriens par adulte.</p></body></html>
"""

PAGE_CHER = """
<html><head><title>Voyager aux Comores</title></head><body>
<p>Le billet de la traversée entre Grande Comore et Mohéli coûte
45 000 francs comoriens par adulte.</p></body></html>
"""

PAGE_OFFICIELLE = """
<html><head><title>Autorité maritime — tarifs officiels</title></head><body>
<p>Le billet de la traversée entre Grande Comore et Mohéli coûte
15 000 francs comoriens par adulte, tarif officiel homologué.</p></body></html>
"""

PAGE_SANS_CHIFFRE = """
<html><head><title>Traversées Grande Comore Mohéli</title></head><body>
<p>Les traversées entre Grande Comore et Mohéli sont assurées par plusieurs
vedettes rapides tout au long de l'année selon la météo marine.</p></body></html>
"""

QUESTION = "Combien coûte la traversée entre Grande Comore et Mohéli ?"


class ScriptedSearch(SearchProvider):
    """Moteur dont les résultats dépendent du contenu de la requête."""

    name = "scripted"

    def __init__(self, rules: list[tuple[str, list[tuple[str, str]]]]) -> None:
        #: liste de (mot déclencheur ou "", [(titre, url)])
        self.rules = rules
        self.queries: list[str] = []

    def search(self, query: str, *, limit: int = 8) -> list[SearchResult]:
        self.queries.append(query)
        for trigger, results in self.rules:
            if not trigger or trigger.lower() in query.lower():
                return [
                    SearchResult(title=titre, url=url, engine=self.name, rank=rank)
                    for rank, (titre, url) in enumerate(results, start=1)
                ]
        return []


@pytest.fixture
def web(monkeypatch):
    """Sert un ensemble de pages nommées et retourne le dictionnaire."""
    from ara.core import http

    pages: dict[str, str] = {}

    def servir(url, **kwargs):
        if url in pages:
            return http.HttpResponse(
                url=url, status=200, body=pages[url].encode("utf-8"),
                content_type="text/html; charset=utf-8",
            )
        raise http.ToolError(f"page absente du scénario : {url}")

    monkeypatch.setattr(http, "get", servir)
    return pages


def _run(ctx, toolbox, question=QUESTION, max_steps=6):
    task_plan = plan(question, max_search_steps=max_steps)
    ctx.budget = task_plan.budget
    ctx.settings = dataclasses.replace(ctx.settings, max_research_steps=max_steps)
    return ResearchAgent(ctx, toolbox, task_plan).run()


# --- Contradiction → relance --------------------------------------------------


def test_une_contradiction_declenche_un_second_cycle(ctx, toolbox, web):
    web.update(
        {
            "https://pas-cher.test/tarifs": PAGE_BON_MARCHE,
            "https://cher.test/voyage": PAGE_CHER,
            "https://officiel.test/tarifs": PAGE_OFFICIELLE,
        }
    )
    ctx.search = ScriptedSearch(
        [
            ("officiel", [("Autorité maritime", "https://officiel.test/tarifs")]),
            ("", [("Tarifs", "https://pas-cher.test/tarifs"),
                  ("Voyager", "https://cher.test/voyage")]),
        ]
    )

    docs, report = _run(ctx, toolbox)

    assert report.contradictions, "45 000 contre 15 000 doit être détecté"
    assert report.iterations >= 2, "une contradiction doit provoquer une relance"
    assert any("officiel" in q.lower() for q in report.queries), (
        "la relance doit viser une source officielle"
    )
    assert any(doc.domain == "officiel.test" for doc in docs)


def test_la_contradiction_apparait_dans_le_rapport(ctx, toolbox, web):
    web.update(
        {
            "https://pas-cher.test/tarifs": PAGE_BON_MARCHE,
            "https://cher.test/voyage": PAGE_CHER,
        }
    )
    ctx.search = ScriptedSearch(
        [("", [("Tarifs", "https://pas-cher.test/tarifs"),
               ("Voyager", "https://cher.test/voyage")])]
    )

    _docs, report = _run(ctx, toolbox)
    sections = report.sections()

    assert "CONTRADICTION DÉTECTÉE" in sections
    assert "15 000" in sections and "45 000" in sections
    assert "[S1]" in sections and "[S2]" in sections


def test_la_contradiction_est_annoncee_dans_le_flux(ctx, toolbox, web):
    web.update(
        {
            "https://pas-cher.test/tarifs": PAGE_BON_MARCHE,
            "https://cher.test/voyage": PAGE_CHER,
        }
    )
    ctx.search = ScriptedSearch(
        [("", [("Tarifs", "https://pas-cher.test/tarifs"),
               ("Voyager", "https://cher.test/voyage")])]
    )

    _run(ctx, toolbox)
    messages = [event.message for event in ctx.bus.history]
    assert any("CONTRADICTION DÉTECTÉE" in message for message in messages)


# --- Manque → relance ---------------------------------------------------------


def test_un_aspect_non_couvert_declenche_une_relance_ciblee(ctx, toolbox, web):
    """Aucune source ne donne de prix : l'agent doit relancer sur le tarif."""
    web.update(
        {
            "https://info.test/traversees": PAGE_SANS_CHIFFRE,
            "https://officiel.test/tarifs": PAGE_OFFICIELLE,
        }
    )
    ctx.search = ScriptedSearch(
        [
            ("tarif", [("Autorité maritime", "https://officiel.test/tarifs")]),
            ("", [("Traversées", "https://info.test/traversees")]),
        ]
    )

    docs, report = _run(ctx, toolbox)

    assert report.iterations >= 2
    assert any(doc.domain == "officiel.test" for doc in docs)
    assert any(fact.kind == "money" for fact in report.facts)


# --- Arrêt --------------------------------------------------------------------


def test_larret_est_immediat_quand_tout_est_couvert(ctx, toolbox, web):
    """Deux sources concordantes sur le prix : rien ne justifie une relance."""
    web.update(
        {
            "https://pas-cher.test/tarifs": PAGE_BON_MARCHE,
            "https://officiel.test/tarifs": PAGE_OFFICIELLE,
        }
    )
    ctx.search = ScriptedSearch(
        [("", [("Tarifs", "https://pas-cher.test/tarifs"),
               ("Officiel", "https://officiel.test/tarifs")])]
    )

    _docs, report = _run(ctx, toolbox)

    assert report.iterations == 1
    assert not report.contradictions
    assert "aucune information manquante" in report.stopped_because


def test_le_budget_est_reduit_quand_la_tache_est_plus_simple_que_prevu(ctx, toolbox, web):
    """Spec §4 : le système doit savoir *diminuer* le nombre d'étapes."""
    web.update(
        {
            "https://pas-cher.test/tarifs": PAGE_BON_MARCHE,
            "https://officiel.test/tarifs": PAGE_OFFICIELLE,
        }
    )
    ctx.search = ScriptedSearch(
        [("", [("Tarifs", "https://pas-cher.test/tarifs"),
               ("Officiel", "https://officiel.test/tarifs")])]
    )

    _run(ctx, toolbox)
    assert any(step["kind"] == "de-escalate" for step in ctx.journal.research_steps)


def test_le_budget_de_recherche_borne_la_boucle(ctx, toolbox, web):
    """Même en cas de manque permanent, MAX_RESEARCH_STEPS s'impose."""
    web["https://info.test/traversees"] = PAGE_SANS_CHIFFRE
    ctx.search = ScriptedSearch(
        [("", [("Traversées", "https://info.test/traversees")])]
    )

    _docs, report = _run(ctx, toolbox, max_steps=2)

    assert report.queries and len(report.queries) <= 2
    assert report.stopped_because


def test_le_plafond_de_cycles_est_respecte(ctx, toolbox, web):
    """Un web qui ne répond jamais vraiment ne doit pas boucler sans fin."""
    for index in range(30):
        web[f"https://source{index}.test/p"] = PAGE_SANS_CHIFFRE

    class Inepuisable(ScriptedSearch):
        def __init__(self):
            super().__init__([])
            self.n = 0

        def search(self, query, *, limit=8):
            self.queries.append(query)
            self.n += 1
            return [
                SearchResult(
                    title="Traversées",
                    url=f"https://source{self.n * 2 + i}.test/p",
                    engine="scripted",
                )
                for i in range(2)
            ]

    ctx.search = Inepuisable()
    _docs, report = _run(ctx, toolbox, max_steps=10)

    assert report.iterations <= MAX_CYCLES
    assert report.stopped_because


def test_larret_est_toujours_motive(ctx, toolbox, web):
    web["https://info.test/traversees"] = PAGE_SANS_CHIFFRE
    ctx.search = ScriptedSearch([("", [("Traversées", "https://info.test/traversees")])])
    _docs, report = _run(ctx, toolbox)
    assert report.stopped_because, "l'agent doit toujours dire pourquoi il s'arrête"


def test_aucune_source_nest_relue_deux_fois(ctx, toolbox, web):
    web["https://info.test/traversees"] = PAGE_SANS_CHIFFRE
    ctx.search = ScriptedSearch([("", [("Traversées", "https://info.test/traversees")])])

    docs, _report = _run(ctx, toolbox)
    urls = [doc.url for doc in docs]
    assert len(urls) == len(set(urls))


def test_les_requetes_ne_se_repetent_pas(ctx, toolbox, web):
    web["https://info.test/traversees"] = PAGE_SANS_CHIFFRE
    ctx.search = ScriptedSearch([("", [("Traversées", "https://info.test/traversees")])])

    _docs, report = _run(ctx, toolbox)
    normalisees = [" ".join(q.lower().split()) for q in report.queries]
    assert len(normalisees) == len(set(normalisees))


# --- Journal ------------------------------------------------------------------


def test_le_journal_retrace_les_cycles(ctx, toolbox, web):
    web.update(
        {
            "https://pas-cher.test/tarifs": PAGE_BON_MARCHE,
            "https://cher.test/voyage": PAGE_CHER,
            "https://officiel.test/tarifs": PAGE_OFFICIELLE,
        }
    )
    ctx.search = ScriptedSearch(
        [
            ("officiel", [("Autorité", "https://officiel.test/tarifs")]),
            ("", [("Tarifs", "https://pas-cher.test/tarifs"),
                  ("Voyager", "https://cher.test/voyage")]),
        ]
    )

    _docs, report = _run(ctx, toolbox)
    kinds = [step["kind"] for step in ctx.journal.research_steps]

    assert "analysis" in kinds
    assert "escalate" in kinds
    assert ctx.journal.iterations == report.iterations
    # La spec §17 interdit d'y stocker un raisonnement : on ne garde que des
    # résumés courts.
    for step in ctx.journal.research_steps:
        assert len(step["detail"]) <= 200


# --- Diversité des sources ----------------------------------------------------


def test_un_seul_site_ne_peut_pas_monopoliser_les_sources(ctx, toolbox, web):
    """Dix pages d'un même site ne font pas dix sources."""
    from ara.agents.gather import MAX_PER_DOMAIN

    for index in range(12):
        web[f"https://unique.test/page{index}"] = PAGE_SANS_CHIFFRE

    class UnSeulSite(ScriptedSearch):
        def __init__(self):
            super().__init__([])
            self.n = 0

        def search(self, query, *, limit=8):
            self.queries.append(query)
            self.n += 1
            return [
                SearchResult(
                    title="Traversées",
                    url=f"https://unique.test/page{self.n * 3 + i}",
                    engine="scripted",
                )
                for i in range(3)
            ]

    ctx.search = UnSeulSite()
    docs, _report = _run(ctx, toolbox, max_steps=8)

    assert len(docs) <= MAX_PER_DOMAIN
