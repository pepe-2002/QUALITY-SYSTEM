"""Boucle créative : designer ↔ critique (spec §7 et §11).

    DESIGNER → FLYER V1 → CRITIQUE → CORRECTIONS → FLYER V2 → … → FINAL

Deux règles de la spec commandent tout ce module :

* §11 — **interdiction de considérer sa première production comme correcte**.
  Chaque version est notée, y compris la première.
* §11 — le système doit pouvoir dire « **version précédente meilleure** » et
  revenir en arrière. Une correction qui dégrade la note est annulée.

Les corrections sont **mécaniques** : le critique mesure un défaut, une
transformation le corrige. Un critique qui se contenterait d'écrire « améliorer
le contraste » laisserait la boucle tourner à vide.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field

from . import color as colors
from .brand import BrandProfile
from .brief import Brief
from .canvas import Canvas, estimate_width, wrap
from .concepts import propose
from .critic import Critique, critique


@dataclass
class Version:
    """Un état de la création et sa note."""

    number: int
    canvas: Canvas
    critique: Critique
    origin: str = ""          # ce qui a produit cette version
    applied: list[str] = field(default_factory=list)
    kept: bool = True

    @property
    def score(self) -> int:
        return self.critique.score

    def to_dict(self) -> dict:
        return {
            "version": self.number,
            "name": self.canvas.name,
            "score": self.score,
            "origin": self.origin,
            "applied": self.applied,
            "kept": self.kept,
            "blocking": self.critique.blocking,
        }


@dataclass
class StudioResult:
    """Sortie complète de la boucle créative."""

    brief: Brief
    concepts: list[Version] = field(default_factory=list)
    iterations: list[Version] = field(default_factory=list)
    final: Version | None = None
    stopped_because: str = ""

    @property
    def history(self) -> list[Version]:
        return self.concepts + self.iterations

    def to_dict(self) -> dict:
        return {
            "brief": self.brief.to_dict(),
            "concepts": [v.to_dict() for v in self.concepts],
            "iterations": [v.to_dict() for v in self.iterations],
            "final": self.final.to_dict() if self.final else None,
            "stopped_because": self.stopped_because,
        }

    def report(self) -> str:
        retenu = self.final.canvas.name if self.final else ""
        lines = ["## Concepts proposés", ""]
        for version in self.concepts:
            marque = " **← retenu**" if version.canvas.name == retenu else ""
            lines.append(
                f"- **{version.canvas.name}** — {version.score}/100. "
                f"{version.canvas.note}{marque}"
            )

        if self.iterations:
            lines += ["", "## Itérations", ""]
            for version in self.iterations:
                verdict = "conservée" if version.kept else "**annulée — version précédente meilleure**"
                lines.append(f"- V{version.number} : {version.score}/100 ({verdict})")
                for item in version.applied:
                    lines.append(f"  - {item}")

        if self.final:
            lines += ["", "## Version finale", "",
                      f"**{self.final.canvas.name} — {self.final.score}/100**", "",
                      self.final.critique.report()]
        lines += ["", f"*Arrêt : {self.stopped_because}*"]
        return "\n".join(lines)


# --- Corrections mécaniques ---------------------------------------------------


def _clone(canvas: Canvas) -> Canvas:
    return copy.deepcopy(canvas)


def _fix_contraste(canvas: Canvas, brand: BrandProfile) -> str | None:
    worst, ratio = None, 99.0
    for element in canvas.text_elements():
        value = element.contrast()
        if value < ratio:
            worst, ratio = element, value
    if worst is None or ratio >= colors.WCAG_AA_NORMAL:
        return None
    worst.fill = colors.readable_on(worst.on, ("#ffffff", brand.ink, "#000000"))
    return f"contraste de « {worst.text[:26]} » porté à {worst.contrast():.1f}:1"


def _fix_hierarchie(canvas: Canvas, brand: BrandProfile) -> str | None:
    titre = canvas.first("titre")
    corps = [e for e in canvas.text_elements() if e.role in {"corps", "contact", "mention"}]
    if titre is None or not corps:
        return None
    plus_petit = min(corps, key=lambda e: e.size)
    if titre.size / plus_petit.size >= 2.5:
        return None
    avant = titre.size
    titre.size = round(titre.size * 1.12)
    titre.height = titre.size * 1.3 * (titre.text.count("\n") + 1)
    titre.text = wrap(titre.text.replace("\n", " "), titre.size, titre.width,
                      titre.font, max_lines=4)
    return f"titre agrandi de {avant:.0f} à {titre.size:.0f} px"


def _fix_lisibilite(canvas: Canvas, brand: BrandProfile) -> str | None:
    ref = min(canvas.width, canvas.height)
    texts = canvas.text_elements()
    if not texts:
        return None

    plus_petit = min(texts, key=lambda e: e.size)
    if plus_petit.size / ref * 100 < 1.2:
        avant = plus_petit.size
        plus_petit.size = round(ref * 0.014)
        plus_petit.height = plus_petit.size * 1.3
        return f"texte « {plus_petit.text[:22]} » agrandi de {avant:.0f} à {plus_petit.size:.0f} px"

    for element in texts:
        longest = max(element.text.split("\n"), key=len)
        if len(longest) > 70:
            element.text = wrap(element.text.replace("\n", " "), element.size,
                                element.width, element.font, max_lines=5)
            return f"« {longest[:26]}… » recoupé en lignes plus courtes"
    return None


def _fix_alignement(canvas: Canvas, brand: BrandProfile) -> str | None:
    elements = [
        e for e in canvas.elements
        if e.role not in {"fond", "bandeau", "decor", "qr"} and e.align != "middle"
    ]
    if len(elements) < 2:
        return None
    tolerance = canvas.width * 0.01
    marges = sorted(e.x for e in elements)
    dominante = min(marges)
    deplaces = [e for e in elements if abs(e.x - dominante) > tolerance]
    if not deplaces:
        return None
    for element in deplaces:
        decalage = element.x - dominante
        element.x = dominante
        element.width += decalage
    return f"{len(deplaces)} élément(s) recalés sur la marge de gauche"


def _fix_espace(canvas: Canvas, brand: BrandProfile) -> str | None:
    coverage = canvas.ink_area() / canvas.area if canvas.area else 0
    if coverage > 0.65:
        secondaires = canvas.by_role("mention", "contact")
        if secondaires:
            canvas.elements.remove(secondaires[-1])
            return "un bloc secondaire retiré pour désencombrer"
        for element in canvas.by_role("corps"):
            element.size = round(element.size * 0.92)
        return "corps de texte réduit pour laisser respirer"
    if coverage < 0.12:
        titre = canvas.first("titre")
        if titre:
            titre.size = round(titre.size * 1.15)
            titre.text = wrap(titre.text.replace("\n", " "), titre.size,
                              titre.width, titre.font, max_lines=4)
            return "titre agrandi pour occuper l'espace"
    return None


def _fix_couleurs(canvas: Canvas, brand: BrandProfile) -> str | None:
    palette = [c for c in brand.palette]
    if not palette:
        return None
    changés = 0
    for element in canvas.elements:
        if element.role in {"fond"} or not element.fill:
            continue
        try:
            if colors.saturation(element.fill) <= 0.25:
                continue
        except ValueError:
            continue
        if element.fill.lower() in {c.lower() for c in palette}:
            continue
        proche = min(palette, key=lambda c: abs(colors.hue(c) - colors.hue(element.fill)))
        if colors.contrast(proche, element.on) >= colors.WCAG_AA_LARGE:
            element.fill = proche
            changés += 1
    return f"{changés} couleur(s) ramenée(s) dans la palette de marque" if changés else None


def _fix_cta(canvas: Canvas, brand: BrandProfile) -> str | None:
    cta = canvas.first("cta")
    titre = canvas.first("titre")
    if cta is None or titre is None or not titre.size:
        return None
    if cta.size / titre.size >= 0.16:
        return None
    avant = cta.size
    cta.size = round(titre.size * 0.20)
    cta.height = cta.size * 1.3
    return f"appel à l'action agrandi de {avant:.0f} à {cta.size:.0f} px"


def _fix_debordement(canvas: Canvas, brand: BrandProfile) -> str | None:
    for element in canvas.text_elements():
        longest = max(element.text.split("\n"), key=len)
        largeur = estimate_width(longest, element.size, element.font)
        if element.width and largeur > element.width * 1.08:
            element.text = wrap(element.text.replace("\n", " "), element.size,
                                element.width, element.font, max_lines=5)
            still = estimate_width(
                max(element.text.split("\n"), key=len), element.size, element.font
            )
            if still > element.width:
                element.size = round(element.size * element.width / still * 0.98)
            return f"« {longest[:24]}… » remis dans son cadre"

    for element in canvas.overflows(margin=1):
        element.x = max(0, min(element.x, canvas.width - element.width))
        element.y = max(0, min(element.y, canvas.height - element.height))
        return f"« {element.text[:24] or element.role} » ramené dans la page"
    return None


def _fix_logo(canvas: Canvas, brand: BrandProfile) -> str | None:
    """Ajoute la signature de marque : sans elle, la création ne sert personne."""
    if canvas.by_role("logo") or not brand.name:
        return None
    titre = canvas.first("titre")
    if titre is None:
        return None

    size = round(min(canvas.width, canvas.height) * 0.026)
    marge = titre.x
    fond = titre.on
    from .canvas import Element as _Element

    canvas.elements.insert(0, _Element(
        "text", "logo", marge, max(0.0, titre.y - size * 2.2),
        titre.width, size * 1.2, text=brand.name.upper(), size=size,
        font=brand.title_font, weight="700", letter_spacing=size * 0.14,
        fill=colors.readable_on(fond, (brand.accent, "#ffffff", brand.ink)),
        on=fond, align=titre.align,
    ))
    return f"signature « {brand.name} » ajoutée au-dessus du titre"


#: Ordre d'application : les défauts bloquants d'abord, puis par gravité.
FIXES = (
    ("débordement", _fix_debordement),
    ("contraste", _fix_contraste),
    ("lisibilité", _fix_lisibilite),
    ("hiérarchie", _fix_hierarchie),
    ("appel à l'action", _fix_cta),
    ("cohérence du logo", _fix_logo),
    ("alignement", _fix_alignement),
    ("espace négatif", _fix_espace),
    ("couleurs", _fix_couleurs),
)


def improve(canvas: Canvas, verdict: Critique, brand: BrandProfile) -> tuple[Canvas, list[str]]:
    """Applique les corrections que le critique a rendues exploitables.

    Retourne une **nouvelle** composition : l'ancienne reste intacte pour
    permettre le retour arrière.
    """
    candidate = _clone(canvas)
    applied: list[str] = []

    faibles = {c.key for c in verdict.weaknesses}
    for label, fix in FIXES:
        if label == "débordement" and not verdict.blocking:
            continue
        if label != "débordement":
            cle = {
                "contraste": "contraste", "lisibilité": "lisibilite",
                "hiérarchie": "hierarchie", "appel à l'action": "cta",
                "alignement": "alignement", "espace négatif": "espace",
                "couleurs": "couleurs", "cohérence du logo": "logo",
            }[label]
            if cle not in faibles:
                continue
        note = fix(candidate, brand)
        if note:
            applied.append(note)
        if len(applied) >= 3:
            break

    return candidate, applied


# --- Boucle --------------------------------------------------------------------


class Studio:
    """Conduit la création : concepts, critique, itérations, version finale."""

    def __init__(
        self,
        brand: BrandProfile | None = None,
        *,
        max_iterations: int = 5,
        target: int = 85,
    ) -> None:
        self.brand = brand or BrandProfile()
        self.max_iterations = max_iterations
        self.target = target

    def run(self, brief: Brief, *, on_step=None) -> StudioResult:
        result = StudioResult(brief=brief)
        brand = brief.brand or self.brand

        # 1. Plusieurs concepts, chacun noté — jamais un seul jet (spec §5, §11).
        for index, canvas in enumerate(propose(brief), start=1):
            verdict = critique(canvas, brand)
            version = Version(number=0, canvas=canvas, critique=verdict,
                              origin=f"concept {canvas.name}")
            result.concepts.append(version)
            if on_step:
                on_step("concept", version)

        best = max(result.concepts, key=lambda v: v.score)
        current = Version(number=1, canvas=best.canvas, critique=best.critique,
                          origin=f"retenu : {best.canvas.name}")
        result.iterations.append(current)
        if on_step:
            on_step("retenu", current)

        # 2. Boucle designer ↔ critique.
        if current.score >= self.target:
            result.stopped_because = (
                f"objectif atteint dès le premier jet ({current.score} ≥ {self.target})"
            )
            result.final = current
            return result

        for number in range(2, self.max_iterations + 2):
            candidate_canvas, applied = improve(current.canvas, current.critique, brand)
            if not applied:
                result.stopped_because = "plus aucune correction mécanique à appliquer"
                break

            verdict = critique(candidate_canvas, brand)
            candidate = Version(
                number=number, canvas=candidate_canvas, critique=verdict,
                origin="corrections du critique", applied=applied,
            )

            # 3. Retour arrière si la correction dégrade (spec §11).
            if verdict.score < current.score:
                candidate.kept = False
                result.iterations.append(candidate)
                if on_step:
                    on_step("annulee", candidate)
                result.stopped_because = (
                    f"version précédente meilleure ({current.score} > {verdict.score}) "
                    "— retour à la version antérieure"
                )
                break

            result.iterations.append(candidate)
            current = candidate
            if on_step:
                on_step("iteration", candidate)

            if current.score >= self.target:
                result.stopped_because = f"objectif atteint ({current.score} ≥ {self.target})"
                break
        else:
            result.stopped_because = f"nombre maximal d'itérations atteint ({self.max_iterations})"

        result.final = current
        return result
