"""Génération PDF.

Deux moteurs :

1. **ReportLab** (recommandé) — mise en page professionnelle : page de titre,
   logo, titres hiérarchisés, tableaux, pagination, date, bloc de sources.
2. **Repli intégré** — écrit un PDF valide avec la seule bibliothèque standard.
   Moins beau, mais garantit qu'un PDF sort toujours, même sur un téléphone où
   ReportLab ne s'installe pas. Fiabilité avant complexité (règle finale).
"""

from __future__ import annotations

import textwrap
from pathlib import Path

from .model import Block, Document, Run

try:  # pragma: no cover - dépend de l'environnement
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        Image,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    REPORTLAB = True
except ImportError:  # pragma: no cover
    REPORTLAB = False


ACCENT = "#0a2550"


def available() -> bool:
    return REPORTLAB


# --- Moteur ReportLab ---------------------------------------------------------


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _markup(runs: list[Run]) -> str:
    """Convertit des runs en balisage ReportLab."""
    parts: list[str] = []
    for run in runs:
        text = _escape(run.text)
        if run.code:
            text = f'<font face="Courier" size="9">{text}</font>'
        if run.bold:
            text = f"<b>{text}</b>"
        if run.italic:
            text = f"<i>{text}</i>"
        parts.append(text)
    return "".join(parts) or "&nbsp;"


def _styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "AraTitle", parent=base["Title"], fontSize=26, leading=31,
            textColor=colors.HexColor(ACCENT), spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "AraSubtitle", parent=base["Normal"], fontSize=12, leading=16,
            textColor=colors.HexColor("#5a6b85"), spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "AraH1", parent=base["Heading1"], fontSize=17, leading=21,
            textColor=colors.HexColor(ACCENT), spaceBefore=16, spaceAfter=7,
        ),
        "h2": ParagraphStyle(
            "AraH2", parent=base["Heading2"], fontSize=13.5, leading=17,
            textColor=colors.HexColor("#12386e"), spaceBefore=12, spaceAfter=5,
        ),
        "h3": ParagraphStyle(
            "AraH3", parent=base["Heading3"], fontSize=11.5, leading=15,
            textColor=colors.HexColor("#12386e"), spaceBefore=9, spaceAfter=4,
        ),
        "p": ParagraphStyle(
            "AraBody", parent=base["Normal"], fontSize=10.5, leading=15.5,
            alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "AraBullet", parent=base["Normal"], fontSize=10.5, leading=15.5,
            leftIndent=12, bulletIndent=3, spaceAfter=4,
        ),
        "quote": ParagraphStyle(
            "AraQuote", parent=base["Normal"], fontSize=10, leading=14.5,
            leftIndent=14, textColor=colors.HexColor("#4a5568"),
            borderPadding=(0, 0, 0, 6), spaceAfter=8,
        ),
        "code": ParagraphStyle(
            "AraCode", parent=base["Code"], fontSize=8.5, leading=11,
            backColor=colors.HexColor("#f3f5f9"), borderPadding=6, spaceAfter=8,
        ),
        "source": ParagraphStyle(
            "AraSource", parent=base["Normal"], fontSize=8.5, leading=12,
            textColor=colors.HexColor("#40506b"), spaceAfter=3,
        ),
    }


def _decorate(canvas, doc, *, title: str, created: str) -> None:
    """En-tête discret + pied de page paginé (spec §8)."""
    canvas.saveState()
    width, height = A4

    canvas.setStrokeColor(colors.HexColor("#dfe4ec"))
    canvas.setLineWidth(0.5)
    canvas.line(20 * mm, height - 15 * mm, width - 20 * mm, height - 15 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#8a97ab"))
    canvas.drawString(20 * mm, height - 13 * mm, title[:70])
    canvas.drawRightString(width - 20 * mm, height - 13 * mm, created)

    canvas.line(20 * mm, 15 * mm, width - 20 * mm, 15 * mm)
    canvas.drawString(20 * mm, 11 * mm, "Généré par ARA — vérifier les sources avant diffusion")
    canvas.drawRightString(width - 20 * mm, 11 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def _table(block: Block, styles) -> Table:
    data = [
        [Paragraph(_escape(cell), styles["p"]) for cell in row]
        for row in block.rows
    ]
    table = Table(data, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(ACCENT)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c8d0dd")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f8fb")]),
            ]
        )
    )
    return table


def _render_reportlab(document: Document, path: Path) -> Path:
    styles = _styles()
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=22 * mm,
        bottomMargin=20 * mm,
        title=document.title,
        author=document.author,
    )

    story: list = []
    if document.logo and Path(document.logo).is_file():
        try:
            story.append(Image(str(document.logo), width=38 * mm, height=38 * mm, kind="proportional"))
            story.append(Spacer(1, 8))
        except Exception:
            pass  # un logo illisible ne doit pas empêcher le document

    story.append(Paragraph(_escape(document.title), styles["title"]))
    subtitle = document.subtitle or f"Document généré le {document.created}"
    story.append(Paragraph(_escape(subtitle), styles["subtitle"]))

    for block in document.blocks:
        if block.kind == "table" and block.rows:
            story.append(_table(block, styles))
            story.append(Spacer(1, 10))
        elif block.kind == "rule":
            story.append(Spacer(1, 6))
        elif block.kind == "bullet":
            story.append(Paragraph(_markup(block.runs), styles["bullet"], bulletText="•"))
        elif block.kind == "numbered":
            story.append(Paragraph(_markup(block.runs), styles["bullet"], bulletText="—"))
        elif block.kind in {"h1", "h2", "h3"}:
            story.append(Paragraph(_markup(block.runs), styles[block.kind]))
        elif block.kind == "quote":
            story.append(Paragraph(_markup(block.runs), styles["quote"]))
        elif block.kind == "code":
            story.append(Paragraph(_escape(block.text).replace("\n", "<br/>"), styles["code"]))
        else:
            story.append(Paragraph(_markup(block.runs), styles["p"]))

    if document.sources:
        story.append(PageBreak())
        story.append(Paragraph("Sources", styles["h1"]))
        for index, source in enumerate(document.sources, start=1):
            label = _escape(source.get("title") or source.get("url", ""))
            url = _escape(source.get("url", ""))
            story.append(
                Paragraph(f"[S{index}] {label}<br/><font color='#0a63c2'>{url}</font>",
                          styles["source"])
            )

    decorate = lambda canvas, d: _decorate(  # noqa: E731
        canvas, d, title=document.title, created=document.created
    )
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    return path


# --- Moteur de repli (bibliothèque standard uniquement) -----------------------


def _pdf_escape(text: str) -> bytes:
    encoded = text.encode("latin-1", errors="replace")
    return encoded.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def _render_fallback(document: Document, path: Path) -> Path:
    """PDF minimal mais valide : Helvetica, A4, pagination.

    Suffisant pour lire le contenu ; on prévient l'utilisateur que la mise en
    page riche exige ReportLab.
    """
    lines: list[tuple[str, int]] = [(document.title, 18)]
    if document.subtitle:
        lines.append((document.subtitle, 11))
    lines.append(("", 11))

    sizes = {"h1": 15, "h2": 13, "h3": 12}
    for block in document.blocks:
        if block.kind == "rule":
            lines.append(("─" * 60, 10))
            continue
        if block.kind == "table":
            for row in block.rows:
                lines.append((" | ".join(row), 9))
            lines.append(("", 10))
            continue
        prefix = {"bullet": "• ", "numbered": "— ", "quote": "> "}.get(block.kind, "")
        size = sizes.get(block.kind, 10)
        wrapped = textwrap.wrap(prefix + block.text, width=95 if size <= 10 else 70) or [""]
        lines.extend((line, size) for line in wrapped)
        if block.kind in sizes:
            lines.append(("", size))

    if document.sources:
        lines += [("", 10), ("Sources", 15)]
        for index, source in enumerate(document.sources, start=1):
            label = source.get("title") or source.get("url", "")
            lines.append((f"[S{index}] {label}", 9))
            lines.append((f"      {source.get('url', '')}", 8))

    # Pagination : 60 lignes utiles par page A4 en 12 pt d'interligne.
    per_page = 58
    pages = [lines[i : i + per_page] for i in range(0, len(lines), per_page)] or [[]]

    objects: list[bytes] = []
    page_ids = [4 + i for i in range(len(pages))]
    content_ids = [4 + len(pages) + i for i in range(len(pages))]

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")

    for index, page_lines in enumerate(pages):
        objects.append(
            (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 3 0 R >> >> "
                f"/Contents {content_ids[index]} 0 R >>"
            ).encode()
        )

    for index, page_lines in enumerate(pages):
        stream = bytearray(b"BT\n")
        y = 800
        for text, size in page_lines:
            stream += f"/F1 {size} Tf\n1 0 0 1 57 {y} Tm\n".encode()
            stream += b"(" + _pdf_escape(text) + b") Tj\n"
            y -= max(12, size + 3)
        stream += f"/F1 8 Tf\n1 0 0 1 57 40 Tm\n".encode()
        stream += b"(" + _pdf_escape(
            f"{document.created} — page {index + 1}/{len(pages)} — genere par ARA"
        ) + b") Tj\nET\n"
        objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n"
                       + bytes(stream) + b"\nendstream")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_at = len(out)
    out += f"xref\n0 {len(objects) + 1}\n".encode()
    out += b"0000000000 65535 f \n"
    for offset in offsets[1:]:
        out += f"{offset:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_at}\n%%EOF\n"
    ).encode()

    path.write_bytes(bytes(out))
    return path


def render(document: Document, path: Path) -> tuple[Path, str]:
    """Écrit le PDF. Retourne `(chemin, avertissement)`."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if REPORTLAB:
        return _render_reportlab(document, path), ""
    _render_fallback(document, path)
    return path, (
        "PDF produit en mode simplifié : ReportLab n'est pas installé. "
        "`pip install reportlab` pour la mise en page complète (tableaux, logo, styles)."
    )
