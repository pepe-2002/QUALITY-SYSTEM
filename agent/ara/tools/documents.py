"""Outils de création de documents : PDF, DOCX, MD, TXT.

Chaque outil génère **puis vérifie** le fichier. Un document qui ne s'ouvre pas
n'est jamais retourné comme réussi (spec §8).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..core.context import TaskContext
from ..core.errors import ToolError
from ..documents.render import VerificationError, document_from_markdown, generate
from .registry import tool


def _create(
    ctx: TaskContext,
    fmt: str,
    filename: str,
    title: str,
    markdown: str,
    subtitle: str = "",
    sources: list[dict[str, str]] | None = None,
    logo: str = "",
) -> dict[str, Any]:
    if not filename.lower().endswith(f".{fmt}"):
        filename = f"{filename}.{fmt}"
    path = ctx.storage.path_for(ctx.task_id, filename)

    logo_path = Path(logo) if logo and Path(logo).is_file() else None
    document = document_from_markdown(
        title, markdown, subtitle=subtitle, sources=sources, logo=logo_path
    )

    try:
        info = generate(document, path, fmt)
    except VerificationError as exc:
        # Le fichier existe peut-être mais est inutilisable : on ne le livre pas.
        path.unlink(missing_ok=True)
        raise ToolError(f"Document rejeté à la vérification — {exc}") from exc

    ctx.journal.add_file(path.name)
    if info.get("warning"):
        ctx.notice(str(info["warning"]))
    ctx.bus.log(f"Document vérifié : {path.name}", file=info)
    return info


@tool(
    "create_pdf",
    "Crée un PDF mis en page (titres, tableaux, pagination, sources) depuis du Markdown.",
    params={
        "filename": "nom du fichier",
        "title": "titre du document",
        "markdown": "contenu au format Markdown",
        "subtitle": "sous-titre (optionnel)",
        "sources": "liste [{title, url}] (optionnel)",
    },
)
def create_pdf(
    ctx: TaskContext,
    filename: str,
    title: str,
    markdown: str,
    subtitle: str = "",
    sources: list[dict[str, str]] | None = None,
    logo: str = "",
) -> dict[str, Any]:
    return _create(ctx, "pdf", filename, title, markdown, subtitle, sources, logo)


@tool(
    "create_docx",
    "Crée un document Word (.docx) depuis du Markdown.",
    params={
        "filename": "nom du fichier",
        "title": "titre du document",
        "markdown": "contenu au format Markdown",
        "subtitle": "sous-titre (optionnel)",
        "sources": "liste [{title, url}] (optionnel)",
    },
)
def create_docx(
    ctx: TaskContext,
    filename: str,
    title: str,
    markdown: str,
    subtitle: str = "",
    sources: list[dict[str, str]] | None = None,
    logo: str = "",
) -> dict[str, Any]:
    return _create(ctx, "docx", filename, title, markdown, subtitle, sources, logo)


@tool(
    "create_markdown",
    "Crée un fichier Markdown structuré (titre, sources).",
    params={"filename": "nom du fichier", "title": "titre", "markdown": "contenu"},
)
def create_markdown(
    ctx: TaskContext,
    filename: str,
    title: str,
    markdown: str,
    subtitle: str = "",
    sources: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return _create(ctx, "md", filename, title, markdown, subtitle, sources)


@tool(
    "create_txt",
    "Crée un fichier texte brut structuré.",
    params={"filename": "nom du fichier", "title": "titre", "markdown": "contenu"},
)
def create_txt(
    ctx: TaskContext,
    filename: str,
    title: str,
    markdown: str,
    subtitle: str = "",
    sources: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    return _create(ctx, "txt", filename, title, markdown, subtitle, sources)
