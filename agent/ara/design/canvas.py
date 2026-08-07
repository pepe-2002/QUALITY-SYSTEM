"""Modèle de composition et rendu SVG (spec §5).

Pourquoi du SVG et pas une image
--------------------------------
Trois raisons, toutes structurantes :

1. **Zéro dépendance** — du texte, produit avec la bibliothèque standard, donc
   installable sur un téléphone. Une image demanderait Pillow ou un navigateur.
2. **Mesurable** — le critique (spec §6) peut calculer contraste, hiérarchie,
   alignement et espace négatif à partir de la géométrie, pas d'une impression.
   Sur une image matricielle, il faudrait deviner.
3. **Imprimable sans perte** — un flyer se tire en A3 comme en 2160×2700.

Un rendu PNG reste possible via un navigateur si l'utilisateur en a un, mais il
n'est jamais requis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal
from xml.sax.saxutils import escape

from . import color as colors

Role = Literal[
    "fond", "bandeau", "titre", "sous-titre", "accroche", "corps",
    "prix", "cta", "contact", "logo", "qr", "decor", "mention",
]

#: Largeur moyenne d'un glyphe rapportée à la taille de police.
#: Approximation suffisante pour détecter un débordement ou mesurer l'équilibre.
_GLYPH_RATIO = {"serif": 0.50, "sans": 0.53, "mono": 0.60}


def estimate_width(text: str, size: float, font: str = "") -> float:
    """Largeur approchée d'un texte, sans moteur de rendu."""
    family = "mono" if "mono" in font.lower() or "consol" in font.lower() else (
        "serif" if "serif" in font.lower() or "georgia" in font.lower() else "sans"
    )
    ratio = _GLYPH_RATIO[family]
    # Les capitales et les chiffres sont plus larges que la moyenne.
    upper = sum(1 for ch in text if ch.isupper() or ch.isdigit())
    bonus = 0.08 * (upper / len(text)) if text else 0
    return len(text) * size * (ratio + bonus)


@dataclass
class Element:
    """Un élément posé sur la composition."""

    kind: Literal["rect", "text", "line", "qr", "image", "icon"]
    role: Role = "corps"
    x: float = 0
    y: float = 0
    width: float = 0
    height: float = 0

    # texte
    text: str = ""
    size: float = 32
    font: str = ""
    weight: str = "normal"
    align: Literal["start", "middle", "end"] = "start"
    letter_spacing: float = 0
    line_height: float = 1.25

    # apparence
    fill: str = "#000000"
    stroke: str = ""
    stroke_width: float = 0
    opacity: float = 1.0
    radius: float = 0

    # ressources
    href: str = ""
    path: str = ""

    #: couleur du fond sur lequel l'élément repose (calculée à la composition)
    on: str = "#ffffff"

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height

    @property
    def area(self) -> float:
        return max(0.0, self.width) * max(0.0, self.height)

    @property
    def center(self) -> tuple[float, float]:
        return self.x + self.width / 2, self.y + self.height / 2

    def contrast(self) -> float:
        """Contraste de l'élément sur son fond."""
        try:
            return colors.contrast(self.fill, self.on)
        except ValueError:
            return 21.0

    def to_dict(self) -> dict:
        return {
            "kind": self.kind, "role": self.role, "x": self.x, "y": self.y,
            "width": self.width, "height": self.height, "text": self.text[:80],
            "size": self.size, "fill": self.fill, "on": self.on,
        }


@dataclass
class Canvas:
    """Une composition complète, prête à être rendue et critiquée."""

    width: float
    height: float
    background: str = "#ffffff"
    elements: list[Element] = field(default_factory=list)
    name: str = "concept"
    note: str = ""

    def add(self, element: Element) -> Element:
        self.elements.append(element)
        return element

    # -- mesures utilisées par le critique ---------------------------------

    @property
    def area(self) -> float:
        return self.width * self.height

    def by_role(self, *roles: str) -> list[Element]:
        return [e for e in self.elements if e.role in roles]

    def first(self, role: str) -> Element | None:
        for element in self.elements:
            if element.role == role:
                return element
        return None

    def ink_area(self) -> float:
        """Surface occupée, hors fond et hors décor de fond."""
        return sum(e.area for e in self.elements if e.role not in {"fond", "bandeau", "decor"})

    def text_elements(self) -> list[Element]:
        return [e for e in self.elements if e.kind == "text" and e.text.strip()]

    def overflows(self, margin: float = 0) -> list[Element]:
        """Éléments qui sortent du cadre — défaut rédhibitoire à l'impression."""
        out = []
        for element in self.elements:
            if element.role in {"fond", "decor"}:
                continue
            if (
                element.x < -margin
                or element.y < -margin
                or element.right > self.width + margin
                or element.bottom > self.height + margin
            ):
                out.append(element)
        return out

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "background": self.background,
            "note": self.note,
            "elements": [e.to_dict() for e in self.elements],
        }

    # -- rendu -------------------------------------------------------------

    def to_svg(self) -> str:
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{self.width:g}" height="{self.height:g}" '
            f'viewBox="0 0 {self.width:g} {self.height:g}" '
            f'role="img" aria-label="{escape(self.name)}">',
            f'<rect width="{self.width:g}" height="{self.height:g}" fill="{self.background}"/>',
        ]
        for element in self.elements:
            parts.append(_render(element))
        parts.append("</svg>")
        return "\n".join(parts)


def _opacity(element: Element) -> str:
    return f' opacity="{element.opacity:g}"' if element.opacity < 1 else ""


def _render(element: Element) -> str:
    if element.kind == "rect":
        radius = f' rx="{element.radius:g}"' if element.radius else ""
        stroke = (
            f' stroke="{element.stroke}" stroke-width="{element.stroke_width:g}"'
            if element.stroke
            else ""
        )
        return (
            f'<rect x="{element.x:g}" y="{element.y:g}" width="{element.width:g}" '
            f'height="{element.height:g}" fill="{element.fill}"{radius}{stroke}'
            f"{_opacity(element)}/>"
        )

    if element.kind == "line":
        return (
            f'<line x1="{element.x:g}" y1="{element.y:g}" '
            f'x2="{element.right:g}" y2="{element.bottom:g}" '
            f'stroke="{element.stroke or element.fill}" '
            f'stroke-width="{element.stroke_width or 2:g}" stroke-linecap="round"'
            f"{_opacity(element)}/>"
        )

    if element.kind in {"qr", "icon"} and element.path:
        return (
            f'<g transform="translate({element.x:g},{element.y:g})">'
            f'<path d="{element.path}" fill="{element.fill}"{_opacity(element)}/></g>'
        )

    if element.kind == "image" and element.href:
        return (
            f'<image x="{element.x:g}" y="{element.y:g}" width="{element.width:g}" '
            f'height="{element.height:g}" href="{escape(element.href, {chr(34): "&quot;"})}" '
            f'preserveAspectRatio="xMidYMid slice"{_opacity(element)}/>'
        )

    if element.kind == "text":
        return _render_text(element)

    return ""


def _render_text(element: Element) -> str:
    anchor = {"start": element.x, "middle": element.x + element.width / 2,
              "end": element.right}[element.align]
    spacing = (
        f' letter-spacing="{element.letter_spacing:g}"' if element.letter_spacing else ""
    )
    common = (
        f'font-family="{escape(element.font)}" font-size="{element.size:g}" '
        f'font-weight="{element.weight}" fill="{element.fill}" '
        f'text-anchor="{element.align}"{spacing}{_opacity(element)}'
    )

    lines = element.text.split("\n")
    if len(lines) == 1:
        baseline = element.y + element.size * 0.82
        return f'<text x="{anchor:g}" y="{baseline:g}" {common}>{escape(element.text)}</text>'

    step = element.size * element.line_height
    spans = "".join(
        f'<tspan x="{anchor:g}" dy="{0 if i == 0 else step:g}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)
    )
    baseline = element.y + element.size * 0.82
    return f'<text x="{anchor:g}" y="{baseline:g}" {common}>{spans}</text>'


def wrap(text: str, size: float, max_width: float, font: str = "", max_lines: int = 4) -> str:
    """Coupe un texte pour qu'il tienne dans une largeur donnée.

    Sans cela, un titre un peu long sort du cadre — et un flyer dont le texte
    déborde n'est pas rattrapable à l'impression.
    """
    words = text.split()
    if not words:
        return ""
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if estimate_width(candidate, size, font) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
            if len(lines) == max_lines:
                break
    if len(lines) < max_lines:
        lines.append(current)
    return "\n".join(lines[:max_lines])
