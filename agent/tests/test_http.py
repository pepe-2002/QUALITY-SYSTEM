"""Client HTTP : garde-fous, réessais et gestion des erreurs (spec §20)."""

from __future__ import annotations

import urllib.error

import pytest

from ara.core import http
from ara.core.errors import ToolError


@pytest.fixture
def reseau_reel(monkeypatch):
    """Retire le faux réseau global pour tester le vrai client."""
    monkeypatch.undo()
    return monkeypatch


class _FausseReponse:
    status = 200
    headers = {"Content-Type": "text/plain; charset=utf-8", "Content-Encoding": ""}

    def __init__(self, body: bytes = b"ok"):
        self._body = body

    def read(self, size=None):
        return self._body

    def geturl(self):
        return "https://exemple.test/"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def _erreur_http(code: int, retry_after: str | None = None) -> urllib.error.HTTPError:
    headers = {"Retry-After": retry_after} if retry_after else {}
    return urllib.error.HTTPError("https://exemple.test/", code, "erreur", headers, None)


# --- Garde-fous ---------------------------------------------------------------


@pytest.mark.parametrize(
    "url",
    ["file:///etc/passwd", "ftp://exemple.test/x", "javascript:alert(1)", "pas-une-url"],
)
def test_schemas_refuses(reseau_reel, url):
    with pytest.raises(ToolError):
        http.request(url)


def test_adresse_privee_refusee(reseau_reel):
    with pytest.raises(ToolError, match="locale ou privée"):
        http.request("http://192.168.1.1/")


def test_le_corps_est_tronque_a_la_taille_maximale(reseau_reel, monkeypatch):
    monkeypatch.setattr(
        http.urllib.request, "urlopen",
        lambda *a, **kw: _FausseReponse(b"x" * 5000),
    )
    response = http.request("https://exemple.test/", max_bytes=1024)
    assert len(response.body) == 1024
    assert response.truncated is True


# --- Réessais -----------------------------------------------------------------


def test_reessai_sur_limitation_de_debit(reseau_reel, monkeypatch):
    """Constaté en réel : l'API Wikipédia répond 429 si on enchaîne trop vite."""
    appels = []
    monkeypatch.setattr(http.time, "sleep", lambda d: appels.append(d))

    tentatives = {"n": 0}

    def urlopen(*args, **kwargs):
        tentatives["n"] += 1
        if tentatives["n"] < 3:
            raise _erreur_http(429)
        return _FausseReponse()

    monkeypatch.setattr(http.urllib.request, "urlopen", urlopen)

    assert http.request("https://exemple.test/").status == 200
    assert tentatives["n"] == 3
    assert appels, "un retrait progressif doit être appliqué"
    assert appels[1] > appels[0], "le délai doit croître"


def test_lentete_retry_after_est_respectee(reseau_reel, monkeypatch):
    attentes = []
    monkeypatch.setattr(http.time, "sleep", lambda d: attentes.append(d))
    monkeypatch.setattr(
        http.urllib.request, "urlopen",
        lambda *a, **kw: (_ for _ in ()).throw(_erreur_http(429, retry_after="3")),
    )

    with pytest.raises(ToolError, match="HTTP 429"):
        http.request("https://exemple.test/")
    assert attentes[0] == 3.0


def test_pas_de_reessai_sur_une_erreur_definitive(reseau_reel, monkeypatch):
    tentatives = {"n": 0}

    def urlopen(*args, **kwargs):
        tentatives["n"] += 1
        raise _erreur_http(404)

    monkeypatch.setattr(http.urllib.request, "urlopen", urlopen)

    with pytest.raises(ToolError, match="HTTP 404"):
        http.request("https://exemple.test/")
    assert tentatives["n"] == 1, "un 404 ne se répare pas en réessayant"


def test_le_nombre_de_reessais_est_borne(reseau_reel, monkeypatch):
    tentatives = {"n": 0}
    monkeypatch.setattr(http.time, "sleep", lambda d: None)

    def urlopen(*args, **kwargs):
        tentatives["n"] += 1
        raise _erreur_http(503)

    monkeypatch.setattr(http.urllib.request, "urlopen", urlopen)

    with pytest.raises(ToolError):
        http.request("https://exemple.test/")
    assert tentatives["n"] == http.MAX_RETRIES + 1


# --- Temporisation entre recherches -------------------------------------------


def test_une_pause_separe_deux_recherches(ctx, toolbox, monkeypatch):
    import dataclasses

    from ara.agents.gather import collect
    from ara.agents.planner import plan

    pauses = []
    monkeypatch.setattr("ara.agents.gather.time.sleep", lambda d: pauses.append(d))
    ctx.settings = dataclasses.replace(ctx.settings, search_delay=0.5)

    # Il faut au moins deux requêtes pour qu'une pause existe. V2 juge cette
    # question simple et n'en lance qu'une — ce qui est le comportement voulu.
    # Ce test-ci porte sur la politesse réseau, pas sur la décision de chercher.
    task_plan = plan(
        "Recherche les tarifs des traversées aux Comores",
        max_search_steps=3,
        controller="v1",
    )
    ctx.budget = task_plan.budget
    collect(ctx, task_plan, toolbox)

    assert pauses, "les recherches doivent être espacées"
    assert all(pause == 0.5 for pause in pauses)
