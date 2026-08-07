"""Outils fichiers : écrire, lister, lire, supprimer.

`delete_file` est déclaré **sensible** et absent de la liste blanche par
défaut : une suppression exige à la fois une autorisation explicite et une
confirmation humaine (spec §15 et §16).
"""

from __future__ import annotations

from typing import Any

from ..core.context import TaskContext
from ..core.errors import ToolError
from .registry import tool


@tool(
    "save_file",
    "Écrit un fichier texte dans l'espace de travail de la tâche.",
    params={"filename": "nom du fichier", "content": "contenu texte"},
)
def save_file(ctx: TaskContext, filename: str, content: str) -> dict[str, Any]:
    stored = ctx.storage.write_text(ctx.task_id, filename, content)
    ctx.journal.add_file(stored.name)
    return stored.to_dict()


@tool("list_files", "Liste les fichiers produits par la tâche en cours.")
def list_files(ctx: TaskContext) -> list[dict[str, Any]]:
    return [stored.to_dict() for stored in ctx.storage.list(ctx.task_id)]


@tool(
    "read_file",
    "Relit un fichier texte produit par la tâche.",
    params={"filename": "nom du fichier"},
)
def read_file(ctx: TaskContext, filename: str) -> dict[str, Any]:
    raw = ctx.storage.read_bytes(ctx.task_id, filename)
    try:
        return {"filename": filename, "content": raw.decode("utf-8")}
    except UnicodeDecodeError as exc:
        raise ToolError(f"{filename} n'est pas un fichier texte.") from exc


@tool(
    "delete_file",
    "Supprime un fichier de la tâche. Action irréversible.",
    params={"filename": "nom du fichier"},
    sensitive=True,
)
def delete_file(ctx: TaskContext, filename: str) -> dict[str, Any]:
    path = ctx.storage.path_for(ctx.task_id, filename)
    if not path.is_file():
        raise ToolError(f"Fichier introuvable : {filename}")
    path.unlink()
    return {"deleted": filename}
