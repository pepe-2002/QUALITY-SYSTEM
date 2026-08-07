"""Rendu multi-format et **vérification** des fichiers produits.

Spec §8 : « Le système doit vérifier que le document final peut être ouvert
avant de le présenter à l'utilisateur. » `verify()` est donc appelé
systématiquement après génération ; un fichier qui échoue n'est jamais annoncé
comme livrable.
"""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from . import docx as docx_engine
from . import pdf as pdf_engine
from .model import Block, Document

FORMATS = ("pdf", "docx", "md", "txt")


class VerificationError(Exception):
    """Le fichier produit est illisible ou incomplet."""


# --- Rendus texte -------------------------------------------------------------


def _to_markdown(document: Document) -> str:
    lines = [f"# {document.title}", ""]
    if document.subtitle:
        lines += [f"*{document.subtitle}*", ""]
    lines += [f"*Généré le {document.created}*", "", "---", ""]

    for block in document.blocks:
        if block.kind == "table":
            if not block.rows:
                continue
            lines.append("| " + " | ".join(block.rows[0]) + " |")
            lines.append("| " + " | ".join("---" for _ in block.rows[0]) + " |")
            for row in block.rows[1:]:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("")
        elif block.kind == "rule":
            lines += ["---", ""]
        elif block.kind == "bullet":
            lines.append(f"- {block.text}")
        elif block.kind == "numbered":
            lines.append(f"1. {block.text}")
        elif block.kind in {"h1", "h2", "h3"}:
            lines += ["", "#" * (int(block.kind[1]) + 1) + f" {block.text}", ""]
        elif block.kind == "quote":
            lines += [f"> {block.text}", ""]
        elif block.kind == "code":
            lines += ["```", block.text, "```", ""]
        else:
            lines += [block.text, ""]

    if document.sources:
        lines += ["", "## Sources", ""]
        for index, source in enumerate(document.sources, start=1):
            label = source.get("title") or source.get("url", "")
            lines.append(f"{index}. [{label}]({source.get('url', '')})")

    return "\n".join(lines).strip() + "\n"


def _to_text(document: Document) -> str:
    lines = [document.title, "=" * len(document.title)]
    if document.subtitle:
        lines.append(document.subtitle)
    lines += [f"Généré le {document.created}", ""]

    for block in document.blocks:
        if block.kind == "table":
            for row in block.rows:
                lines.append("  " + " | ".join(row))
            lines.append("")
        elif block.kind == "rule":
            lines += ["-" * 60, ""]
        elif block.kind == "bullet":
            lines.append(f"  - {block.text}")
        elif block.kind == "numbered":
            lines.append(f"  1. {block.text}")
        elif block.kind in {"h1", "h2", "h3"}:
            lines += ["", block.text.upper(), "-" * len(block.text), ""]
        elif block.kind == "quote":
            lines += [f"  > {block.text}", ""]
        else:
            lines += [block.text, ""]

    if document.sources:
        lines += ["", "SOURCES", "-------"]
        for index, source in enumerate(document.sources, start=1):
            label = source.get("title") or source.get("url", "")
            lines.append(f"[S{index}] {label}")
            lines.append(f"       {source.get('url', '')}")

    return "\n".join(lines).strip() + "\n"


# --- Vérification -------------------------------------------------------------


def verify(path: Path) -> dict[str, object]:
    """Vérifie qu'un fichier généré est ouvrable. Lève `VerificationError`.

    Les contrôles sont structurels et sans dépendance : en-tête et table des
    objets pour un PDF, intégrité de l'archive et bonne formation du XML pour
    un DOCX, décodage UTF-8 pour le texte.
    """
    path = Path(path)
    if not path.is_file():
        raise VerificationError(f"Fichier absent : {path.name}")
    size = path.stat().st_size
    if size == 0:
        raise VerificationError(f"Fichier vide : {path.name}")

    suffix = path.suffix.lower()
    info: dict[str, object] = {"name": path.name, "size": size, "kind": suffix.lstrip(".")}

    if suffix == ".pdf":
        raw = path.read_bytes()
        if not raw.startswith(b"%PDF-"):
            raise VerificationError(f"{path.name} : en-tête PDF absent.")
        if b"%%EOF" not in raw[-2048:]:
            raise VerificationError(f"{path.name} : fin de fichier PDF absente (tronqué ?).")
        pages = len(re.findall(rb"/Type\s*/Page[^s]", raw))
        if pages == 0:
            raise VerificationError(f"{path.name} : aucune page détectée.")
        info["pages"] = pages

    elif suffix == ".docx":
        try:
            with zipfile.ZipFile(path) as archive:
                broken = archive.testzip()
                if broken:
                    raise VerificationError(f"{path.name} : archive corrompue ({broken}).")
                names = set(archive.namelist())
                for required in ("[Content_Types].xml", "word/document.xml"):
                    if required not in names:
                        raise VerificationError(f"{path.name} : {required} manquant.")
                ElementTree.fromstring(archive.read("word/document.xml"))
        except zipfile.BadZipFile as exc:
            raise VerificationError(f"{path.name} : ZIP illisible ({exc}).") from exc
        except ElementTree.ParseError as exc:
            raise VerificationError(f"{path.name} : XML mal formé ({exc}).") from exc

    elif suffix == ".svg":
        try:
            root = ElementTree.fromstring(path.read_text(encoding="utf-8"))
        except (ElementTree.ParseError, UnicodeDecodeError) as exc:
            raise VerificationError(f"{path.name} : SVG mal formé ({exc}).") from exc
        if not root.tag.endswith("svg"):
            raise VerificationError(f"{path.name} : la racine n'est pas un <svg>.")
        info["elements"] = len(list(root))

    elif suffix in {".md", ".txt", ".json", ".html"}:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise VerificationError(f"{path.name} : texte non décodable ({exc}).") from exc
        if not text.strip():
            raise VerificationError(f"{path.name} : contenu vide.")
        info["chars"] = len(text)

    return info


# --- Point d'entrée -----------------------------------------------------------


def generate(document: Document, path: Path, fmt: str | None = None) -> dict[str, object]:
    """Génère puis vérifie un document. Retourne les infos du fichier.

    Lève `VerificationError` si le fichier produit n'est pas ouvrable.
    """
    path = Path(path)
    fmt = (fmt or path.suffix.lstrip(".") or "md").lower()
    if fmt not in FORMATS:
        raise VerificationError(f"Format non pris en charge : {fmt} (attendu : {', '.join(FORMATS)})")

    path.parent.mkdir(parents=True, exist_ok=True)
    warning = ""

    if fmt == "pdf":
        _, warning = pdf_engine.render(document, path)
    elif fmt == "docx":
        _, warning = docx_engine.render(document, path)
    elif fmt == "md":
        path.write_text(_to_markdown(document), encoding="utf-8")
    else:
        path.write_text(_to_text(document), encoding="utf-8")

    info = verify(path)
    info["format"] = fmt
    if warning:
        info["warning"] = warning
    return info


def document_from_markdown(
    title: str,
    markdown: str,
    *,
    subtitle: str = "",
    sources: list[dict[str, str]] | None = None,
    logo: Path | None = None,
) -> Document:
    """Raccourci : construit un :class:`Document` depuis du Markdown."""
    from .model import from_markdown

    blocks: list[Block] = from_markdown(markdown)
    return Document(
        title=title,
        subtitle=subtitle,
        blocks=blocks,
        sources=sources or [],
        logo=logo,
    )
