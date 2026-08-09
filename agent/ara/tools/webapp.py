"""Outil `create_site` — fabrique un site ou une application web (Phase 6).

Les fichiers sont écrits à plat dans le dossier de la tâche : `index.html`,
`style.css`, `app.js` s'y trouvent côte à côte, donc les liens relatifs
fonctionnent et le site s'ouvre d'un double-clic, sans serveur.

L'outil ne décide de rien : il assemble la demande, la mémoire de marque et la
matière issue de la recherche, puis laisse le studio construire, mesurer et
corriger. Ce qu'il ajoute, c'est la **mémoire des leçons** — chargée avant,
sauvegardée après, partagée par toutes les tâches.
"""

from __future__ import annotations

from typing import Any

from ..core.context import TaskContext
from ..core.errors import ToolError
from ..design.brand import BrandProfile
from ..webapp.builder import apply_brand, spec_from_brief
from ..webapp.lessons import Lessons
from ..webapp.studio import SiteStudio
from .registry import tool


@tool(
    "create_site",
    "Crée un site web ou une application installable, la critique et la corrige.",
    params={
        "brief": "ce que le site doit être",
        "kind": "vitrine, landing, app ou portfolio",
        "material": "phrases réelles à placer dans les sections",
        "title": "titre imposé (facultatif)",
        "installable": "vrai pour une application installable hors ligne",
    },
)
def create_site(
    ctx: TaskContext,
    brief: str = "",
    kind: str = "",
    material: list[str] | None = None,
    title: str = "",
    installable: bool | None = None,
) -> dict[str, Any]:
    brand = BrandProfile.load(ctx.settings.brand_profile_path())
    lessons = Lessons.load(ctx.settings.lessons_path())

    spec = spec_from_brief(
        brief or ctx.prompt, kind=kind, material=list(material or [])
    )
    apply_brand(spec, brand)
    if title:
        spec.title = title
    if installable is not None:
        spec.installable = bool(installable)

    studio = SiteStudio(lessons)
    result = studio.run(spec, task=ctx.task_id)
    if result.final is None:
        raise ToolError("Aucun site n'a pu être produit.")

    files: list[dict[str, Any]] = []
    for nom, contenu in result.files.items():
        stored = ctx.storage.write_text(ctx.task_id, nom, contenu)
        ctx.journal.add_file(stored.name)
        files.append({**stored.to_dict(), "role": nom})

    ctx.journal.iterations = max(ctx.journal.iterations, len(result.versions))
    ctx.journal.final_score = result.score
    ctx.journal.add_summary(
        f"site : {len(result.versions)} version(s), note finale {result.score}/100, "
        f"{len(result.prevented)} défaut(s) évité(s) d'avance"
    )

    for item in result.prevented:
        ctx.notice(f"Défaut évité grâce à une tâche précédente — {item}")
    for version in result.versions:
        if not version.kept:
            ctx.notice(
                f"Version {version.number} annulée — version précédente meilleure "
                f"({version.score} < {result.score})."
            )
    for item in result.unfixable:
        ctx.notice(f"Limite du site livré — {item}")

    ctx.bus.log(
        f"Site livré : {result.spec.title} — {result.score}/100",
        kind="site", site=result.to_dict(),
    )
    return {
        "files": files,
        "report": result.report(),
        "site": result.to_dict(),
        "score": result.score,
        "entry": "index.html",
        "lessons": lessons.report(),
    }


@tool(
    "forget_lessons",
    "Efface la mémoire des défauts de fabrication web.",
    params={},
    sensitive=True,
)
def forget_lessons(ctx: TaskContext) -> dict[str, Any]:
    """Le patron doit pouvoir désapprendre l'agent.

    Une mémoire qu'on ne peut pas vider finit par imposer des règles que
    personne ne sait plus justifier. Action sensible : confirmation requise.
    """
    path = ctx.settings.lessons_path()
    avant = len(Lessons.load(path).items)
    Lessons(path=path).save()
    ctx.journal.add_step("lessons", f"{avant} leçon(s) effacée(s)")
    return {"forgotten": avant, "path": str(path)}


__all__ = ["create_site", "forget_lessons"]
