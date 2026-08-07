"""Agent documentaire : transforme une réponse en livrables vérifiés."""

from __future__ import annotations

from typing import Any

from ..core.context import TaskContext
from ..core.errors import AraError
from ..core.events import Stage, Status
from ..core.models import SourceDoc
from ..documents.render import verify
from ..tools.registry import ToolBox
from .planner import Plan

#: Format → outil correspondant
_TOOLS = {
    "pdf": "create_pdf",
    "docx": "create_docx",
    "md": "create_markdown",
    "txt": "create_txt",
}


def _title(prompt: str) -> str:
    words = " ".join(prompt.split())
    if len(words) <= 70:
        return words.rstrip(" .!?") or "Document"
    return words[:70].rsplit(" ", 1)[0] + "…"


def produce(
    ctx: TaskContext,
    plan: Plan,
    toolbox: ToolBox,
    answer: str,
    sources: list[SourceDoc],
) -> list[dict[str, Any]]:
    """Génère les fichiers demandés. Retourne les fiches des fichiers créés."""
    if not plan.formats:
        ctx.stage(Stage.CREATION, Status.SKIPPED, "Aucun fichier demandé")
        return []

    ctx.stage(Stage.CREATION, Status.RUNNING, f"Création : {', '.join(plan.formats)}")

    title = _title(plan.prompt)
    source_list = [
        {"title": doc.title or doc.domain, "url": doc.url} for doc in sources
    ]
    files: list[dict[str, Any]] = []

    for fmt in plan.formats:
        tool_name = _TOOLS.get(fmt)
        if not tool_name or not toolbox.has(tool_name):
            ctx.notice(f"Format « {fmt} » indisponible (outil {tool_name} non autorisé).")
            continue
        try:
            info = toolbox.call(
                tool_name,
                filename=plan.filename_hint,
                title=title,
                markdown=answer,
                subtitle=f"Demande : {' '.join(plan.prompt.split())[:120]}",
                sources=source_list,
            )
            files.append(info)
            ctx.bus.log(f"Fichier créé : {info.get('name')}", file=info)
        except AraError as exc:
            ctx.journal.add_error(f"{tool_name}: {exc}")
            ctx.notice(f"Échec de création {fmt.upper()} : {exc}")

    ctx.stage(
        Stage.CREATION,
        Status.DONE if files else Status.FAILED,
        f"{len(files)} fichier(s) créé(s)",
        files=files,
    )
    return files


def verify_all(ctx: TaskContext, files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rouvre chaque fichier livré — dernière barrière avant l'utilisateur.

    N'émet pas d'événement d'étape : c'est l'orchestrateur qui publie un seul
    verdict de VÉRIFICATION, couvrant la réponse **et** les fichiers.
    """
    if not files:
        return []

    checked: list[dict[str, Any]] = []
    for info in files:
        name = str(info.get("name", ""))
        try:
            path = ctx.storage.path_for(ctx.task_id, name)
            result = verify(path)
            result["format"] = info.get("format", result.get("kind"))
            if info.get("warning"):
                result["warning"] = info["warning"]
            checked.append(result)
        except Exception as exc:
            ctx.journal.add_error(f"vérification {name}: {exc}")
            ctx.notice(f"Fichier écarté (illisible) : {name} — {exc}")

    return checked
