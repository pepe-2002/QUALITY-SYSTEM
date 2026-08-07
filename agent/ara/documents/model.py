"""Modèle de document intermédiaire, indépendant du format de sortie.

Le LLM produit du Markdown ; on le convertit une seule fois en blocs
structurés, puis chaque générateur (PDF, DOCX, TXT, MD) rend ces blocs. Cela
évite d'écrire un parseur Markdown par format.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Literal

BlockKind = Literal["h1", "h2", "h3", "p", "bullet", "numbered", "quote", "table", "rule", "code"]


@dataclass
class Run:
    """Fragment de texte avec son style."""

    text: str
    bold: bool = False
    italic: bool = False
    code: bool = False


@dataclass
class Block:
    kind: BlockKind
    runs: list[Run] = field(default_factory=list)
    #: pour `table` : lignes de cellules (la première ligne est l'en-tête)
    rows: list[list[str]] = field(default_factory=list)
    level: int = 0

    @property
    def text(self) -> str:
        return "".join(run.text for run in self.runs)

    @classmethod
    def para(cls, kind: BlockKind, text: str, level: int = 0) -> "Block":
        return cls(kind=kind, runs=parse_inline(text), level=level)


@dataclass
class Document:
    """Document prêt à être rendu."""

    title: str
    subtitle: str = ""
    blocks: list[Block] = field(default_factory=list)
    sources: list[dict[str, str]] = field(default_factory=list)
    created: str = field(default_factory=lambda: date.today().isoformat())
    author: str = "ARA — agent de recherche"
    logo: Path | None = None

    def add(self, block: Block) -> "Document":
        self.blocks.append(block)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "blocks": len(self.blocks),
            "sources": len(self.sources),
            "created": self.created,
        }


# --- Analyse Markdown → blocs -------------------------------------------------

_INLINE_RE = re.compile(r"(\*\*.+?\*\*|__.+?__|\*.+?\*|_.+?_|`.+?`)", re.DOTALL)
_BULLET_RE = re.compile(r"^\s*[-*•]\s+(.*)$")
_NUMBERED_RE = re.compile(r"^\s*\d+[.)]\s+(.*)$")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:-]*\|[\s|:-]*$")


def parse_inline(text: str) -> list[Run]:
    """Découpe une ligne en fragments stylés (**gras**, *italique*, `code`)."""
    runs: list[Run] = []
    for piece in _INLINE_RE.split(text):
        if not piece:
            continue
        if (piece.startswith("**") and piece.endswith("**")) or (
            piece.startswith("__") and piece.endswith("__")
        ):
            runs.append(Run(piece[2:-2], bold=True))
        elif piece.startswith("`") and piece.endswith("`") and len(piece) > 2:
            runs.append(Run(piece[1:-1], code=True))
        elif (
            (piece.startswith("*") and piece.endswith("*"))
            or (piece.startswith("_") and piece.endswith("_"))
        ) and len(piece) > 2:
            runs.append(Run(piece[1:-1], italic=True))
        else:
            runs.append(Run(piece))
    return runs or [Run(text)]


def _split_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [cell.strip() for cell in cells]


def from_markdown(markdown: str) -> list[Block]:
    """Convertit du Markdown simple en blocs.

    Gère : titres, listes à puces et numérotées, citations, tableaux, règles
    horizontales, blocs de code. Le reste devient du paragraphe.
    """
    blocks: list[Block] = []
    lines = (markdown or "").replace("\r\n", "\n").split("\n")
    index = 0
    paragraph: list[str] = []

    def flush() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(Block.para("p", " ".join(paragraph).strip()))
            paragraph = []

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            flush()
            index += 1
            continue

        if stripped.startswith("```"):
            flush()
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            blocks.append(Block(kind="code", runs=[Run("\n".join(code_lines), code=True)]))
            continue

        if stripped in {"---", "***", "___"}:
            flush()
            blocks.append(Block(kind="rule"))
            index += 1
            continue

        heading = _HEADING_RE.match(stripped)
        if heading:
            flush()
            level = min(len(heading.group(1)), 3)
            blocks.append(Block.para(f"h{level}", heading.group(2).strip(), level))
            index += 1
            continue

        # Tableau : ligne de cellules suivie d'une ligne de séparation
        if "|" in stripped and index + 1 < len(lines) and _TABLE_SEP_RE.match(lines[index + 1]):
            flush()
            rows = [_split_row(stripped)]
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append(_split_row(lines[index]))
                index += 1
            blocks.append(Block(kind="table", rows=rows))
            continue

        quote = _QUOTE_RE.match(line)
        if quote:
            flush()
            blocks.append(Block.para("quote", quote.group(1).strip()))
            index += 1
            continue

        bullet = _BULLET_RE.match(line)
        if bullet:
            flush()
            blocks.append(Block.para("bullet", bullet.group(1).strip()))
            index += 1
            continue

        numbered = _NUMBERED_RE.match(line)
        if numbered:
            flush()
            blocks.append(Block.para("numbered", numbered.group(1).strip()))
            index += 1
            continue

        paragraph.append(stripped)
        index += 1

    flush()
    return blocks
