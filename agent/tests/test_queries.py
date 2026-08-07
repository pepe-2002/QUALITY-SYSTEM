"""Construction des requêtes de recherche.

Défaut constaté en conditions réelles : envoyer la consigne telle quelle
(« … et fais-moi un PDF ») à un moteur ramène des convertisseurs de fichiers.
Les requêtes doivent porter sur le **sujet**, pas sur le livrable.
"""

from __future__ import annotations

from datetime import date

from ara.agents.gather import build_queries
from ara.agents.planner import plan
from ara.providers.llm.base import LLMRequest
from ara.providers.llm.offline import OfflineLLM

BRUIT = {"pdf", "docx", "word", "fais", "fais-moi", "rapport", "document", "recherche"}


def _queries(question: str) -> list[str]:
    return OfflineLLM().complete(LLMRequest(task="queries", question=question)).text.splitlines()


def test_les_consignes_sont_retirees_des_requetes():
    for query in _queries("Recherche les tarifs des traversées aux Comores et fais-moi un PDF"):
        mots = {mot.lower().strip(",.") for mot in query.split()}
        assert not (mots & BRUIT), f"requête polluée par une consigne : {query!r}"


def test_le_sujet_est_conserve():
    queries = _queries("Recherche les tarifs des traversées aux Comores et fais-moi un PDF")
    assert any("tarifs" in q.lower() and "comores" in q.lower() for q in queries)


def test_plusieurs_angles_sont_proposes():
    queries = _queries("Quels sont les horaires des traversées entre Ouroveni et Hoani ?")
    assert len(queries) >= 2, "l'agent ne doit pas se contenter d'une seule formulation"
    assert len(set(queries)) == len(queries), "pas de requête en double"


def test_la_variante_datee_utilise_lannee_courante():
    queries = _queries("Quels sont les tarifs des traversées maritimes aux Comores ?")
    assert any(str(date.today().year) in q for q in queries)


def test_une_question_courte_donne_une_seule_requete(ctx):
    task_plan = plan("bonjour", max_search_steps=3)
    ctx.budget = task_plan.budget
    assert len(build_queries(ctx, task_plan)) == 1


def test_le_budget_borne_le_nombre_de_requetes(ctx):
    task_plan = plan(
        "Compare et vérifie les tarifs et les horaires des traversées, fais un PDF",
        max_search_steps=2,
    )
    ctx.budget = task_plan.budget
    assert len(build_queries(ctx, task_plan)) <= 2
