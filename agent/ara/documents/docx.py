"""Génération DOCX en pur Python (bibliothèque standard).

Un `.docx` est une archive ZIP de fichiers XML : on l'écrit directement avec
`zipfile`, sans `python-docx`. Zéro dépendance = installation possible sur un
téléphone, et aucune surface de compilation.

Couvre : page de titre, titres 1-3, paragraphes, listes, citations, tableaux,
bloc de sources, pied de page paginé.
"""

from __future__ import annotations

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from .model import Block, Document, Run

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CT = "http://schemas.openxmlformats.org/package/2006/content-types"
PR = "http://schemas.openxmlformats.org/package/2006/relationships"
DOC_CT = "application/vnd.openxmlformats-officedocument.wordprocessingml"

_XML_HEAD = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

_CONTENT_TYPES = f"""{_XML_HEAD}<Types xmlns="{CT}">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="{DOC_CT}.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="{DOC_CT}.styles+xml"/>
<Override PartName="/word/footer1.xml" ContentType="{DOC_CT}.footer+xml"/>
</Types>"""

_ROOT_RELS = f"""{_XML_HEAD}<Relationships xmlns="{PR}">
<Relationship Id="rId1" Type="{R}/officeDocument" Target="word/document.xml"/>
</Relationships>"""

_DOC_RELS = f"""{_XML_HEAD}<Relationships xmlns="{PR}">
<Relationship Id="rId1" Type="{R}/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="{R}/footer" Target="footer1.xml"/>
</Relationships>"""


def _style(style_id: str, name: str, size_half_pt: int, *, bold: bool, color: str,
           space_before: int = 0, space_after: int = 120) -> str:
    return (
        f'<w:style w:type="paragraph" w:styleId="{style_id}">'
        f'<w:name w:val="{name}"/><w:basedOn w:val="Normal"/>'
        f'<w:pPr><w:spacing w:before="{space_before}" w:after="{space_after}"/></w:pPr>'
        f'<w:rPr><w:b w:val="{"1" if bold else "0"}"/>'
        f'<w:color w:val="{color}"/><w:sz w:val="{size_half_pt}"/></w:rPr></w:style>'
    )


_STYLES = f"""{_XML_HEAD}<w:styles xmlns:w="{W}">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="21"/>
</w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>
<w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:style>
{_style("Title", "Title", 52, bold=True, color="0A2550", space_after=60)}
{_style("Subtitle", "Subtitle", 24, bold=False, color="5A6B85", space_after=360)}
{_style("Heading1", "heading 1", 34, bold=True, color="0A2550", space_before=320)}
{_style("Heading2", "heading 2", 27, bold=True, color="12386E", space_before=240)}
{_style("Heading3", "heading 3", 23, bold=True, color="12386E", space_before=180)}
{_style("Quote", "Quote", 21, bold=False, color="4A5568")}
{_style("SourceItem", "Source", 17, bold=False, color="40506B", space_after=60)}
</w:styles>"""

_FOOTER = f"""{_XML_HEAD}<w:ftr xmlns:w="{W}"><w:p>
<w:pPr><w:jc w:val="center"/></w:pPr>
<w:r><w:rPr><w:sz w:val="16"/><w:color w:val="8A97AB"/></w:rPr>
<w:t xml:space="preserve">Généré par ARA — page </w:t></w:r>
<w:r><w:fldChar w:fldCharType="begin"/></w:r>
<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
<w:r><w:fldChar w:fldCharType="end"/></w:r>
</w:p></w:ftr>"""


def _runs_xml(runs: list[Run]) -> str:
    out: list[str] = []
    for run in runs:
        if not run.text:
            continue
        props = []
        if run.bold:
            props.append("<w:b/>")
        if run.italic:
            props.append("<w:i/>")
        if run.code:
            props.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="18"/>')
        rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
        text = escape(run.text).replace("\n", "</w:t></w:r><w:r><w:br/><w:t xml:space=\"preserve\">")
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r>')
    return "".join(out) or '<w:r><w:t xml:space="preserve"></w:t></w:r>'


def _para(runs: list[Run], style: str = "", *, indent: int = 0, bullet: str = "") -> str:
    props = []
    if style:
        props.append(f'<w:pStyle w:val="{style}"/>')
    if indent:
        props.append(f'<w:ind w:left="{indent}"/>')
    ppr = f"<w:pPr>{''.join(props)}</w:pPr>" if props else ""
    prefix = _runs_xml([Run(bullet)]) if bullet else ""
    return f"<w:p>{ppr}{prefix}{_runs_xml(runs)}</w:p>"


def _table_xml(block: Block) -> str:
    if not block.rows:
        return ""
    columns = max(len(row) for row in block.rows)
    grid = "".join(f'<w:gridCol w:w="{int(9000 / columns)}"/>' for _ in range(columns))

    rows_xml = []
    for index, row in enumerate(block.rows):
        cells = list(row) + [""] * (columns - len(row))
        header = index == 0
        cells_xml = []
        for cell in cells:
            shading = '<w:shd w:val="clear" w:fill="0A2550"/>' if header else ""
            runs = [Run(cell, bold=header)]
            cell_para = _para(runs)
            if header:
                cell_para = cell_para.replace(
                    "<w:r>", '<w:r><w:rPr><w:color w:val="FFFFFF"/><w:b/></w:rPr>', 1
                )
            cells_xml.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{int(9000 / columns)}" w:type="dxa"/>'
                f"{shading}</w:tcPr>{cell_para}</w:tc>"
            )
        rows_xml.append(f"<w:tr>{''.join(cells_xml)}</w:tr>")

    borders = "".join(
        f'<w:{side} w:val="single" w:sz="4" w:color="C8D0DD"/>'
        for side in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    return (
        f'<w:tbl><w:tblPr><w:tblW w:w="9000" w:type="dxa"/>'
        f"<w:tblBorders>{borders}</w:tblBorders></w:tblPr>"
        f"<w:tblGrid>{grid}</w:tblGrid>{''.join(rows_xml)}</w:tbl><w:p/>"
    )


def _document_xml(document: Document) -> str:
    body: list[str] = [
        _para([Run(document.title)], "Title"),
        _para([Run(document.subtitle or f"Document généré le {document.created}")], "Subtitle"),
    ]

    for block in document.blocks:
        if block.kind == "table":
            body.append(_table_xml(block))
        elif block.kind == "rule":
            body.append(_para([Run("")]))
        elif block.kind == "bullet":
            body.append(_para(block.runs, indent=360, bullet="• "))
        elif block.kind == "numbered":
            body.append(_para(block.runs, indent=360, bullet="— "))
        elif block.kind in {"h1", "h2", "h3"}:
            body.append(_para(block.runs, f"Heading{block.kind[1]}"))
        elif block.kind == "quote":
            body.append(_para(block.runs, "Quote", indent=360))
        elif block.kind == "code":
            body.append(_para([Run(block.text, code=True)], indent=240))
        else:
            body.append(_para(block.runs))

    if document.sources:
        body.append(_para([Run("Sources")], "Heading1"))
        for index, source in enumerate(document.sources, start=1):
            label = source.get("title") or source.get("url", "")
            body.append(_para([Run(f"[S{index}] {label}", bold=True)], "SourceItem"))
            body.append(_para([Run(source.get("url", ""))], "SourceItem", indent=360))

    sect = (
        '<w:sectPr><w:footerReference w:type="default" r:id="rId2"/>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" w:footer="567"/>'
        "</w:sectPr>"
    )
    return (
        f'{_XML_HEAD}<w:document xmlns:w="{W}" xmlns:r="{R}">'
        f"<w:body>{''.join(body)}{sect}</w:body></w:document>"
    )


def render(document: Document, path: Path) -> tuple[Path, str]:
    """Écrit le DOCX. Retourne `(chemin, avertissement)`."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", _CONTENT_TYPES)
        archive.writestr("_rels/.rels", _ROOT_RELS)
        archive.writestr("word/_rels/document.xml.rels", _DOC_RELS)
        archive.writestr("word/styles.xml", _STYLES)
        archive.writestr("word/footer1.xml", _FOOTER)
        archive.writestr("word/document.xml", _document_xml(document))

    return path, ""
