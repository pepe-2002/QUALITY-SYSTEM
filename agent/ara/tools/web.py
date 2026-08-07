"""Outils web : recherche, récupération de page, extraction de texte."""

from __future__ import annotations

from typing import Any

from ..core import http
from ..core.context import TaskContext
from ..core.errors import AraError
from ..core.html_text import extract
from ..core.models import SourceDoc
from .registry import tool

#: Un titre plus long qu'une ligne d'écran de téléphone est illisible
MAX_TITLE_CHARS = 120


@tool(
    "web_search",
    "Interroge les moteurs de recherche configurés et retourne des résultats.",
    params={"query": "texte de la requête", "limit": "nombre de résultats (défaut 8)"},
)
def web_search(ctx: TaskContext, query: str, limit: int = 8) -> list[dict[str, Any]]:
    results = ctx.search.search(query, limit=limit)
    ctx.journal.add_step("search", query, engine=ctx.search.name, results=len(results))
    for result in results:
        ctx.journal.add_source(result.url, result.title, via=result.engine)

    # Un moteur du groupe « auto » peut échouer sans bloquer : on le signale.
    for failure in getattr(ctx.search, "failures", []):
        ctx.notice(f"Moteur indisponible — {failure}")

    # « Zéro résultat » n'est pas « pas de recherche » : sans ce message,
    # l'utilisateur voit une tâche sans source et sans explication.
    if not results:
        ctx.notice(f"Aucun résultat pour « {query} »")

    return [result.to_dict() for result in results]


@tool(
    "fetch_page",
    "Télécharge une page web et en extrait le texte lisible.",
    params={"url": "adresse http(s)"},
)
def fetch_page(ctx: TaskContext, url: str) -> dict[str, Any]:
    doc = SourceDoc(url=url)
    try:
        response = http.get(url)
        content_type = response.content_type.lower()
        if "html" in content_type or not content_type:
            title, text = extract(response.text())
        else:
            title, text = "", response.text()
        # Certaines pages (réseaux sociaux) mettent tout leur texte dans <title>.
        doc.title = title if len(title) <= MAX_TITLE_CHARS else title[:MAX_TITLE_CHARS].rsplit(" ", 1)[0] + "…"
        doc.text = text
        doc.fetched = True
        if response.truncated:
            ctx.notice(f"Page volumineuse tronquée : {doc.domain}")
    except AraError as exc:
        doc.error = str(exc)
        ctx.journal.add_error(f"fetch_page {url}: {exc}")

    ctx.journal.add_step("fetch", url, ok=doc.fetched, chars=len(doc.text))
    return doc.to_dict(with_text=True)


@tool(
    "extract_text",
    "Extrait le texte lisible d'un fragment HTML déjà en mémoire.",
    params={"html": "code HTML", "max_chars": "longueur maximale (défaut 20000)"},
)
def extract_text(ctx: TaskContext, html: str, max_chars: int = 20_000) -> dict[str, str]:
    title, text = extract(html, max_chars=max_chars)
    return {"title": title, "text": text}
