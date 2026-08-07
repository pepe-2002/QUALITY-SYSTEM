"""Couleurs : mesures objectives pour le critique de design.

Un critique qui dit « le contraste est faible » sans le mesurer ne sert à rien.
Ce module calcule ce qui est calculable — luminance, contraste WCAG, teinte —
pour que la note du critique repose sur des nombres, pas sur une impression.
"""

from __future__ import annotations

import colorsys
import re

_HEX = re.compile(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

#: Seuils WCAG 2.1 pour le texte
WCAG_AA_NORMAL = 4.5
WCAG_AA_LARGE = 3.0
WCAG_AAA_NORMAL = 7.0


def parse(color: str) -> tuple[int, int, int]:
    """Convertit `#0a2550`, `0a2550` ou `#abc` en `(r, g, b)`.

    >>> parse("#0a2550")
    (10, 37, 80)
    >>> parse("#fff")
    (255, 255, 255)
    """
    match = _HEX.match((color or "").strip())
    if not match:
        raise ValueError(f"Couleur invalide : {color!r} (attendu #rrggbb)")
    value = match.group(1)
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*(max(0, min(255, int(c))) for c in rgb))


def luminance(color: str) -> float:
    """Luminance relative WCAG (0 = noir, 1 = blanc)."""
    channels = []
    for value in parse(color):
        ratio = value / 255
        channels.append(ratio / 12.92 if ratio <= 0.04045 else ((ratio + 0.055) / 1.055) ** 2.4)
    red, green, blue = channels
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast(foreground: str, background: str) -> float:
    """Rapport de contraste WCAG entre 1 (nul) et 21 (noir sur blanc).

    >>> round(contrast("#ffffff", "#000000"), 1)
    21.0
    """
    light, dark = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def readable_on(background: str, candidates: tuple[str, ...] = ("#ffffff", "#0b1220")) -> str:
    """Choisit, parmi des candidats, la couleur de texte la plus lisible."""
    return max(candidates, key=lambda color: contrast(color, background))


def hue(color: str) -> float:
    """Teinte en degrés (0-360)."""
    red, green, blue = (c / 255 for c in parse(color))
    return colorsys.rgb_to_hsv(red, green, blue)[0] * 360


def saturation(color: str) -> float:
    red, green, blue = (c / 255 for c in parse(color))
    return colorsys.rgb_to_hsv(red, green, blue)[1]


def mix(first: str, second: str, ratio: float = 0.5) -> str:
    """Mélange deux couleurs (`ratio` = part de la seconde)."""
    a, b = parse(first), parse(second)
    return to_hex(tuple(round(x + (y - x) * ratio) for x, y in zip(a, b)))


def darken(color: str, amount: float = 0.2) -> str:
    return mix(color, "#000000", amount)


def lighten(color: str, amount: float = 0.2) -> str:
    return mix(color, "#ffffff", amount)


def distinct_hues(colors: list[str], *, threshold: float = 25.0) -> int:
    """Nombre de teintes réellement différentes dans une palette.

    Sert à mesurer la cohérence chromatique : une affiche avec sept teintes
    sans lien paraît brouillonne, quel que soit le talent du dessin.
    """
    hues: list[float] = []
    for color in colors:
        try:
            if saturation(color) < 0.12:  # gris et neutres : hors comptage
                continue
            value = hue(color)
        except ValueError:
            continue
        if all(min(abs(value - h), 360 - abs(value - h)) > threshold for h in hues):
            hues.append(value)
    return len(hues)
