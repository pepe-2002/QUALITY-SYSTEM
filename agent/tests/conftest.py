"""Fixtures partagées : environnement isolé, corpus figé, aucun accès réseau.

Toute la suite doit tourner **hors ligne** et de façon déterministe : c'est la
condition pour que « les tests passent » veuille dire quelque chose.
"""

from __future__ import annotations

import pytest

from ara.core import config as config_module
from ara.core import http
from ara.core.config import Settings, set_settings
from ara.core.context import TaskContext
from ara.core.events import EventBus
from ara.core.journal import ResearchLog
from ara.core.permissions import PermissionManager
from ara.providers.llm.offline import OfflineLLM
from ara.providers.search.fixture import FixtureSearch
from ara.providers.storage import LocalStorage

# --- Corpus de test -----------------------------------------------------------

PAGES = {
    "https://exemple.test/traversees": """
        <html><head><title>Traversées Grande Comore – Mohéli</title></head><body>
        <h1>Horaires</h1>
        <p>La traversée entre Ouroveni et Hoani dure environ trois heures selon
        l'état de la mer et les conditions météorologiques du jour.</p>
        <p>Le tarif d'une traversée simple est de 15 000 francs comoriens par
        adulte, bagages de cabine inclus dans la limite de vingt kilogrammes.</p>
        <script>var pub = "ne doit pas apparaitre";</script>
        </body></html>
    """,
    "https://autre.test/tarifs": """
        <html><head><title>Tarifs des vedettes rapides</title></head><body>
        <p>Les compagnies pratiquent un tarif compris entre 15 000 et 17 500
        francs comoriens pour une traversée entre la Grande Comore et Mohéli.</p>
        <p>Les enfants de moins de cinq ans voyagent gratuitement sur présentation
        d'un justificatif d'identité au moment de l'embarquement.</p>
        </body></html>
    """,
    "https://troisieme.test/meteo": """
        <html><head><title>Météo maritime aux Comores</title></head><body>
        <p>La saison des pluies s'étend de décembre à avril, période durant
        laquelle les traversées maritimes sont plus fréquemment annulées.</p>
        </body></html>
    """,
}

RESULTS = {
    "traversées comores tarifs": [
        {"title": "Traversées Grande Comore – Mohéli", "url": "https://exemple.test/traversees",
         "snippet": "Horaires et tarifs des traversées."},
        {"title": "Tarifs des vedettes rapides", "url": "https://autre.test/tarifs",
         "snippet": "Entre 15 000 et 17 500 francs comoriens."},
        {"title": "Météo maritime aux Comores", "url": "https://troisieme.test/meteo",
         "snippet": "Saison des pluies de décembre à avril."},
    ]
}


# --- Environnement ------------------------------------------------------------


@pytest.fixture(autouse=True)
def isolated_settings(tmp_path, monkeypatch):
    """Espace de travail temporaire + réglages hors ligne pour chaque test."""
    for key in list(config_module.os.environ):
        if key.startswith("ARA_"):
            monkeypatch.delenv(key, raising=False)

    settings = Settings(
        llm_provider="offline",
        search_provider="fixture",
        workspace=tmp_path / "workspace",
        max_research_steps=3,
        max_task_seconds=30,
        search_delay=0,  # pas d'attente en test
    )
    set_settings(settings)
    yield settings
    set_settings(Settings.from_env())


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Sert le corpus local et interdit toute sortie réseau réelle."""

    def fake_request(url, **kwargs):
        if url in PAGES:
            return http.HttpResponse(
                url=url, status=200, body=PAGES[url].encode("utf-8"),
                content_type="text/html; charset=utf-8",
            )
        raise http.ToolError(f"Réseau coupé pendant les tests : {url}")

    monkeypatch.setattr(http, "request", fake_request)
    monkeypatch.setattr(http, "get", lambda url, **kw: fake_request(url, **kw))
    monkeypatch.setattr(http, "post", lambda url, data, **kw: fake_request(url, **kw))


@pytest.fixture(autouse=True)
def no_phone(monkeypatch):
    """Aucun test ne part du principe qu'un téléphone est branché.

    Le pont Android retient ce qu'il a détecté ; sans remise à zéro, un test
    qui simule Termux contaminerait les suivants.
    """
    from ara.android import bridge

    monkeypatch.setattr(bridge, "_cache", None, raising=False)
    monkeypatch.setattr(bridge, "_runner", bridge._default_runner, raising=False)
    yield
    bridge._cache = None
    bridge._runner = bridge._default_runner


@pytest.fixture
def search_provider():
    return FixtureSearch(dict(RESULTS))


@pytest.fixture
def ctx(isolated_settings, search_provider) -> TaskContext:
    """Contexte de tâche prêt à l'emploi, tous outils par défaut autorisés."""
    from ara.core.complexity import assess

    settings = isolated_settings
    return TaskContext(
        task_id="test-task",
        prompt="test",
        settings=settings,
        bus=EventBus(),
        journal=ResearchLog(task_id="test-task", task="test"),
        permissions=PermissionManager(settings),
        storage=LocalStorage(settings.tasks_dir()),
        llm=OfflineLLM(),
        search=search_provider,
        budget=assess("test"),
    )


@pytest.fixture
def toolbox(ctx):
    from ara.tools.registry import ToolBox

    return ToolBox(ctx)
