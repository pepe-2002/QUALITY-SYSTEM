"""Interface HTTP : lancement de tâche, flux d'événements, historique, fichiers."""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request

import pytest

from ara.api.server import build_server
from ara.core.config import Settings, set_settings


@pytest.fixture
def server(isolated_settings, monkeypatch):
    """Serveur réel sur un port libre, branché sur le corpus figé."""
    from ara.agents import orchestrator as module
    from ara.providers.search.fixture import FixtureSearch

    from .conftest import RESULTS

    monkeypatch.setattr(module, "get_search", lambda name: (FixtureSearch(dict(RESULTS)), ""))

    settings = Settings(
        llm_provider="offline",
        search_provider="fixture",
        workspace=isolated_settings.workspace,
        host="127.0.0.1",
        port=0,
        max_research_steps=3,
        max_task_seconds=30,
        search_delay=0,
    )
    set_settings(settings)

    httpd = build_server(settings)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{httpd.server_address[1]}"
    try:
        yield base, httpd
    finally:
        httpd.shutdown()
        httpd.server_close()


def _get(url: str):
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def _post(url: str, payload: dict):
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def _wait(base: str, task_id: str, timeout: float = 30) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        _, task = _get(f"{base}/api/tasks/{task_id}")
        if task["status"] in {"done", "error"}:
            return task
        time.sleep(0.2)
    raise AssertionError("la tâche n'a pas abouti dans le temps imparti")


# --- Routes de base -----------------------------------------------------------


def test_sante(server):
    base, _ = server
    status, payload = _get(f"{base}/api/health")
    assert status == 200 and payload["status"] == "ok"


def test_page_daccueil_servie(server):
    base, _ = server
    with urllib.request.urlopen(f"{base}/", timeout=10) as response:
        html = response.read().decode("utf-8")
    assert response.status == 200
    assert 'name="viewport"' in html, "l'interface doit être adaptée au téléphone"


def test_config_liste_outils_et_fournisseurs(server):
    base, _ = server
    _, config = _get(f"{base}/api/config")
    assert [s for s in config["stages"]] == [
        "TACHE", "RECHERCHE", "ANALYSE", "CREATION", "VERIFICATION", "RESULTAT",
    ]
    noms = {tool["name"] for tool in config["tools"]}
    assert {"web_search", "create_pdf", "delete_file"} <= noms

    sensibles = {t["name"] for t in config["tools"] if t["sensitive"]}
    assert "delete_file" in sensibles
    assert not any(t["allowed"] for t in config["tools"] if t["name"] == "delete_file")


# --- Cycle complet ------------------------------------------------------------


def test_lancement_dune_tache_et_recuperation_du_fichier(server):
    base, _ = server
    status, created = _post(
        f"{base}/api/tasks",
        {"prompt": "Recherche les tarifs des traversées aux Comores et fais-moi un PDF"},
    )
    assert status == 201

    task = _wait(base, created["task_id"])
    assert task["status"] == "done"
    assert task["files"], "un PDF devait être produit"

    name = task["files"][0]["name"]
    with urllib.request.urlopen(
        f"{base}/api/tasks/{task['task_id']}/files/{name}", timeout=10
    ) as response:
        body = response.read()
    assert response.headers["Content-Type"] == "application/pdf"
    assert body.startswith(b"%PDF-")


def test_historique_persistant(server):
    base, httpd = server
    _, created = _post(f"{base}/api/tasks", {"prompt": "bonjour"})
    _wait(base, created["task_id"])

    _, payload = _get(f"{base}/api/tasks")
    assert any(task["task_id"] == created["task_id"] for task in payload["tasks"])

    # Un nouveau service relit l'historique depuis le disque.
    from ara.service import TaskService

    relu = TaskService(httpd.settings).get(created["task_id"])
    assert relu is not None and relu.prompt == "bonjour"


def test_flux_devenements(server):
    base, _ = server
    _, created = _post(f"{base}/api/tasks", {"prompt": "bonjour"})

    events = []
    with urllib.request.urlopen(
        f"{base}/api/tasks/{created['task_id']}/events", timeout=30
    ) as stream:
        for raw in stream:
            line = raw.decode("utf-8").strip()
            if line.startswith("data: "):
                events.append(json.loads(line[6:]))
                if events[-1].get("type") == "final":
                    break

    stages = [e["stage"] for e in events if e.get("type") == "stage"]
    assert "TACHE" in stages and "RESULTAT" in stages
    assert events[-1]["type"] == "final"


# --- Erreurs ------------------------------------------------------------------


def test_demande_vide_refusee(server):
    base, _ = server
    with pytest.raises(urllib.error.HTTPError) as exc:
        _post(f"{base}/api/tasks", {"prompt": "   "})
    assert exc.value.code == 400


def test_tache_inconnue(server):
    base, _ = server
    with pytest.raises(urllib.error.HTTPError) as exc:
        _get(f"{base}/api/tasks/inexistante")
    assert exc.value.code == 404


def test_pas_devasion_par_le_chemin_de_fichier(server):
    base, _ = server
    with pytest.raises(urllib.error.HTTPError) as exc:
        urllib.request.urlopen(f"{base}/api/tasks/abc/files/..%2F..%2Ftask.json", timeout=10)
    assert exc.value.code == 404


def test_le_jeton_protege_lapi(server, monkeypatch):
    base, _ = server
    monkeypatch.setenv("ARA_TOKEN", "secret-de-test")

    with pytest.raises(urllib.error.HTTPError) as exc:
        _get(f"{base}/api/health")
    assert exc.value.code == 401

    status, _ = _get(f"{base}/api/health?token=secret-de-test")
    assert status == 200
