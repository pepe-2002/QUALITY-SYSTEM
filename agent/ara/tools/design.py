"""Outils créatifs : flyer, QR code, mémoire de marque (spec §5, §9, §10)."""

from __future__ import annotations

from typing import Any

from ..core.context import TaskContext
from ..core.errors import ToolError
from ..design import qr as qrcode
from ..design.brand import BrandProfile
from ..design.brief import Brief
from ..design.studio import Studio
from .registry import tool


@tool(
    "create_qr",
    "Crée un QR code vérifié (SVG) à partir d'une adresse.",
    params={"url": "adresse à encoder", "filename": "nom du fichier",
            "level": "correction L, M, Q ou H (défaut H)"},
)
def create_qr(
    ctx: TaskContext, url: str, filename: str = "qr", level: str = "H"
) -> dict[str, Any]:
    """Le QR est **relu** avant d'être écrit : un code douteux n'est pas livré."""
    try:
        code = qrcode.make_verified(url, level)
    except qrcode.QRError as exc:
        raise ToolError(f"QR code refusé : {exc}") from exc

    module = 16
    side = (code.size + 8) * module
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{side}" height="{side}" '
        f'viewBox="0 0 {side} {side}">'
        f'<rect width="{side}" height="{side}" fill="#ffffff"/>'
        f'<path d="{code.to_svg_path(module=module, quiet=4)}" fill="#0b1220"/></svg>'
    )
    stored = ctx.storage.write_text(ctx.task_id, f"{filename}.svg", svg)
    ctx.journal.add_file(stored.name)
    ctx.journal.add_step("qr", f"QR vérifié vers {url}", version=code.version)
    return {**stored.to_dict(), "url": url, "version": code.version,
            "level": code.level, "verified": True}


@tool(
    "create_flyer",
    "Crée plusieurs concepts de flyer, les critique, les améliore et livre le meilleur.",
    params={
        "title": "titre principal", "subtitle": "sous-titre",
        "bullets": "liste d'arguments", "price": "prix affiché",
        "contact": "coordonnées", "url": "adresse pour le QR",
        "format": "flyer, affiche, carre, story ou banniere",
        "filename": "nom de base des fichiers",
    },
)
def create_flyer(
    ctx: TaskContext,
    title: str = "",
    subtitle: str = "",
    bullets: list[str] | None = None,
    price: str = "",
    contact: str = "",
    url: str = "",
    format: str = "flyer",
    filename: str = "flyer",
    market: list[str] | None = None,
    competitors: list[str] | None = None,
    subject: str = "",
) -> dict[str, Any]:
    from ..design.brief import FORMATS

    brand = BrandProfile.load(ctx.settings.brand_profile_path())
    width, height = FORMATS.get(format, FORMATS["flyer"])

    brief = Brief(
        subject=subject or title or ctx.prompt,
        title=title, subtitle=subtitle, bullets=list(bullets or []),
        price=price, contact=contact or brand.contact, url=url or brand.website,
        format=format, width=width, height=height, brand=brand,
        market=list(market or []), competitors=list(competitors or []),
    )

    studio = Studio(
        brand,
        max_iterations=ctx.settings.max_design_iterations,
        target=ctx.settings.design_target_score,
    )
    result = studio.run(brief)
    if result.final is None:
        raise ToolError("Aucun concept n'a pu être produit.")

    files: list[dict[str, Any]] = []

    # Les trois concepts sont livrés : le patron doit pouvoir choisir.
    for index, version in enumerate(result.concepts, start=1):
        stored = ctx.storage.write_text(
            ctx.task_id, f"{filename}-concept-{chr(64 + index)}.svg",
            version.canvas.to_svg(),
        )
        ctx.journal.add_file(stored.name)
        files.append({**stored.to_dict(), "format": "svg",
                      "concept": version.canvas.name, "score": version.score})

    final = ctx.storage.write_text(
        ctx.task_id, f"{filename}-final.svg", result.final.canvas.to_svg()
    )
    ctx.journal.add_file(final.name)
    files.append({**final.to_dict(), "format": "svg", "final": True,
                  "concept": result.final.canvas.name, "score": result.final.score})

    ctx.journal.iterations = max(ctx.journal.iterations, len(result.iterations))
    ctx.journal.final_score = result.final.score
    ctx.journal.add_summary(
        f"création : {len(result.concepts)} concepts, "
        f"{len(result.iterations)} itération(s), note finale {result.final.score}"
    )
    for version in result.iterations:
        if not version.kept:
            ctx.notice(
                f"Version {version.number} annulée — version précédente meilleure "
                f"({version.score} < {result.final.score})."
            )

    ctx.bus.log(
        f"Version finale : {result.final.canvas.name} — {result.final.score}/100",
        kind="design", design=result.to_dict(),
    )
    return {
        "files": files,
        "report": result.report(),
        "studio": result.to_dict(),
        "score": result.final.score,
        "name": final.name,
    }


@tool(
    "remember_brand",
    "Enregistre ou complète la mémoire de marque (couleurs, ton, interdits).",
    params={"name": "nom de la marque", "palette": "liste de couleurs #rrggbb",
            "avoid": "liste d'interdits", "website": "adresse du site"},
)
def remember_brand(
    ctx: TaskContext,
    name: str = "",
    palette: list[str] | None = None,
    fonts: list[str] | None = None,
    slogans: list[str] | None = None,
    avoid: list[str] | None = None,
    website: str = "",
    contact: str = "",
    tone: str = "",
) -> dict[str, Any]:
    path = ctx.settings.brand_profile_path()
    brand = BrandProfile.load(path)
    brand.remember(
        name=name, palette=palette, fonts=fonts, slogans=slogans,
        avoid=avoid, website=website, contact=contact, tone=tone,
    )
    brand.save(path)
    ctx.journal.add_step("brand", f"mémoire de marque mise à jour : {brand.name}")
    return {"brand": brand.name, "avoid": brand.avoid, "palette": brand.palette}
