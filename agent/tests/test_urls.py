"""Normalisation d'URL et dédoublonnage des sources."""

from __future__ import annotations

import pytest

from ara.core.urls import canonical


@pytest.mark.parametrize(
    "a, b",
    [
        ("https://exemple.test/page", "https://exemple.test/page/"),
        ("https://exemple.test/page", "https://www.exemple.test/page"),
        ("https://exemple.test/page", "https://EXEMPLE.test/page"),
        ("https://exemple.test/page", "https://exemple.test/page?lang=fr"),
        ("https://exemple.test/page", "https://exemple.test/page?utm_source=fb&fbclid=x"),
        ("https://exemple.test/page", "https://exemple.test/page#section"),
    ],
)
def test_les_variantes_cosmetiques_sont_fusionnees(a, b):
    assert canonical(a) == canonical(b)


@pytest.mark.parametrize(
    "a, b",
    [
        ("https://exemple.test/page", "https://exemple.test/page?id=7"),
        ("https://exemple.test/page", "https://exemple.test/autre"),
        ("https://exemple.test/page?p=1", "https://exemple.test/page?p=2"),
        ("https://exemple.test/page", "https://autre.test/page"),
    ],
)
def test_les_pages_differentes_restent_distinctes(a, b):
    assert canonical(a) != canonical(b)


def test_lordre_des_parametres_nimporte_pas():
    assert canonical("https://a.test/p?b=2&a=1") == canonical("https://a.test/p?a=1&b=2")


def test_une_url_invalide_ne_leve_pas():
    assert canonical("pas une url")


def test_un_titre_demesure_est_tronque(toolbox, monkeypatch):
    """Constaté en réel : un post Facebook met tout son texte dans <title>."""
    from ara.core import http
    from ara.tools.web import MAX_TITLE_CHARS

    url = "https://reseau.test/post"
    titre = "DÉCLARATION DES CAPITAINES " * 20
    monkeypatch.setattr(
        http, "get",
        lambda u, **kw: http.HttpResponse(
            url=u, status=200,
            body=f"<html><head><title>{titre}</title></head><body><p>Corps du message.</p></body></html>".encode(),
            content_type="text/html; charset=utf-8",
        ),
    )

    payload = toolbox.call("fetch_page", url=url)
    assert len(payload["title"]) <= MAX_TITLE_CHARS + 2
    assert payload["title"].endswith("…")
