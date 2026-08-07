"""DESIGN CRITIC AGENT — note une composition de 0 à 100 (spec §6).

Un critique qui dit « ça manque de peps » ne sert à rien : on ne sait pas quoi
corriger. Chacun des douze critères de la spec est donc **mesuré** sur la
géométrie et les couleurs de la composition, et chaque faiblesse produit une
**correction applicable**, pas un commentaire.

Le critique est indépendant du créateur : il ne sait pas quel concept il note,
et il ne dessine pas. C'est ce qui rend la boucle d'itération honnête.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from . import color as colors
from .brand import BrandProfile
from .canvas import Canvas, Element, estimate_width

#: Poids des critères. La lisibilité et le contraste priment : une affiche
#: illisible ne se rattrape pas avec un bel équilibre.
WEIGHTS = {
    "hierarchie": 12,
    "lisibilite": 14,
    "contraste": 14,
    "typographie": 8,
    "alignement": 9,
    "equilibre": 7,
    "espace": 9,
    "logo": 5,
    "images": 4,
    "couleurs": 8,
    "impact": 6,
    "cta": 4,
}

LABELS = {
    "hierarchie": "hiérarchie visuelle",
    "lisibilite": "lisibilité",
    "contraste": "contraste",
    "typographie": "typographie",
    "alignement": "alignement",
    "equilibre": "équilibre",
    "espace": "espace négatif",
    "logo": "cohérence du logo",
    "images": "qualité des images",
    "couleurs": "cohérence des couleurs",
    "impact": "impact marketing",
    "cta": "clarté de l'appel à l'action",
}


@dataclass
class Criterion:
    key: str
    score: int              # 0-100
    detail: str             # ce qui a été mesuré
    correction: str = ""    # quoi faire si le score est faible

    @property
    def label(self) -> str:
        return LABELS.get(self.key, self.key)

    def to_dict(self) -> dict:
        return {
            "key": self.key, "label": self.label, "score": self.score,
            "detail": self.detail, "correction": self.correction,
        }


@dataclass
class Critique:
    """Le verdict complet sur une composition."""

    score: int = 0
    criteria: list[Criterion] = field(default_factory=list)
    blocking: list[str] = field(default_factory=list)

    @property
    def strengths(self) -> list[Criterion]:
        return sorted(
            [c for c in self.criteria if c.score >= 80], key=lambda c: -c.score
        )

    @property
    def weaknesses(self) -> list[Criterion]:
        return sorted([c for c in self.criteria if c.score < 70], key=lambda c: c.score)

    @property
    def corrections(self) -> list[str]:
        return [c.correction for c in self.weaknesses if c.correction]

    def get(self, key: str) -> Criterion | None:
        return next((c for c in self.criteria if c.key == key), None)

    def report(self) -> str:
        lines = [f"**Note : {self.score}/100**", ""]
        if self.blocking:
            lines += ["**Défauts bloquants**", ""]
            lines += [f"- {item}" for item in self.blocking] + [""]
        if self.strengths:
            lines += ["**Points forts**", ""]
            lines += [f"- {c.label} ({c.score}) — {c.detail}" for c in self.strengths[:4]]
            lines.append("")
        if self.weaknesses:
            lines += ["**Points faibles**", ""]
            lines += [f"- {c.label} ({c.score}) — {c.detail}" for c in self.weaknesses[:5]]
            lines.append("")
        if self.corrections:
            lines += ["**Corrections nécessaires**", ""]
            lines += [f"- {item}" for item in self.corrections[:5]]
        return "\n".join(lines).strip()

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "blocking": self.blocking,
            "criteria": [c.to_dict() for c in self.criteria],
            "strengths": [c.label for c in self.strengths],
            "weaknesses": [c.label for c in self.weaknesses],
            "corrections": self.corrections,
        }


# --- Critères ------------------------------------------------------------------


def _scale(value: float, bad: float, good: float) -> int:
    """Convertit une mesure en note 0-100, linéairement entre `bad` et `good`."""
    if good == bad:
        return 100
    ratio = (value - bad) / (good - bad)
    return max(0, min(100, round(ratio * 100)))


def _contraste(canvas: Canvas) -> Criterion:
    texts = canvas.text_elements()
    if not texts:
        return Criterion("contraste", 0, "aucun texte à évaluer",
                         "Ajouter au moins un texte lisible.")
    ratios = [(e, e.contrast()) for e in texts]
    worst_el, worst = min(ratios, key=lambda item: item[1])
    score = _scale(worst, 1.5, colors.WCAG_AAA_NORMAL)
    detail = f"contraste le plus faible : {worst:.1f}:1 sur « {worst_el.text[:28]} »"
    correction = ""
    if worst < colors.WCAG_AA_NORMAL:
        lisible = colors.readable_on(worst_el.on)
        correction = (
            f"Le texte « {worst_el.text[:28]} » n'atteint pas le seuil WCAG AA "
            f"({worst:.1f}:1 < 4.5). Passer sa couleur à {lisible}."
        )
    return Criterion("contraste", score, detail, correction)


def _hierarchie(canvas: Canvas) -> Criterion:
    texts = canvas.text_elements()
    if not texts:
        return Criterion("hierarchie", 0, "aucun texte", "Structurer le message.")
    sizes = sorted({round(e.size) for e in texts}, reverse=True)
    if len(sizes) < 2:
        return Criterion(
            "hierarchie", 25, "une seule taille de texte : rien ne ressort",
            "Agrandir nettement le titre et réduire le corps de texte.",
        )
    ratio = sizes[0] / sizes[-1]
    levels = min(len(sizes), 5)
    score = round(0.6 * _scale(ratio, 1.2, 3.5) + 0.4 * _scale(levels, 1, 4))
    detail = f"{len(sizes)} niveaux, rapport titre/corps de {ratio:.1f}"
    correction = ""
    if ratio < 2.2:
        correction = (
            f"Le titre n'est que {ratio:.1f}× le corps de texte : porter ce "
            "rapport à au moins 2,5 pour que la hiérarchie se lise."
        )
    return Criterion("hierarchie", score, detail, correction)


def _lisibilite(canvas: Canvas) -> Criterion:
    texts = canvas.text_elements()
    if not texts:
        return Criterion("lisibilite", 0, "aucun texte", "Ajouter le message.")

    # Une taille se juge en proportion du format, pas en pixels absolus.
    ref = min(canvas.width, canvas.height)
    smallest = min(texts, key=lambda e: e.size)
    relative = smallest.size / ref * 100
    size_score = _scale(relative, 0.8, 2.2)

    # Une ligne trop longue fatigue : au-delà de ~70 signes, on décroche.
    longest = 0
    for element in texts:
        for line in element.text.split("\n"):
            longest = max(longest, len(line))
    length_score = 100 if longest <= 60 else _scale(longest, 110, 60)

    score = round(0.6 * size_score + 0.4 * length_score)
    detail = (
        f"plus petit texte à {relative:.1f}% du format, "
        f"ligne la plus longue : {longest} signes"
    )
    corrections = []
    if relative < 1.2:
        corrections.append(
            f"Le texte « {smallest.text[:24]} » fait {relative:.1f}% du format : "
            "l'agrandir à au moins 1,4% pour rester lisible imprimé."
        )
    if longest > 70:
        corrections.append(
            f"Une ligne atteint {longest} signes : la couper vers 55-60 signes."
        )
    return Criterion("lisibilite", score, detail, " ".join(corrections))


def _typographie(canvas: Canvas) -> Criterion:
    texts = canvas.text_elements()
    if not texts:
        return Criterion("typographie", 50, "aucun texte", "")
    families = {e.font.split(",")[0].strip().lower() for e in texts if e.font}
    sizes = {round(e.size) for e in texts}
    family_score = 100 if len(families) <= 2 else max(0, 100 - 30 * (len(families) - 2))
    size_score = 100 if len(sizes) <= 5 else max(0, 100 - 15 * (len(sizes) - 5))
    score = round(0.6 * family_score + 0.4 * size_score)
    detail = f"{len(families)} famille(s), {len(sizes)} taille(s)"
    correction = ""
    if len(families) > 2:
        correction = (
            f"{len(families)} polices différentes : n'en garder que deux, "
            "une pour les titres, une pour le corps."
        )
    elif len(sizes) > 6:
        correction = f"{len(sizes)} tailles de texte : les ramener à quatre ou cinq."
    return Criterion("typographie", score, detail, correction)


def _alignement(canvas: Canvas) -> Criterion:
    elements = [e for e in canvas.elements if e.role not in {"fond", "bandeau", "decor"}]
    if not elements:
        return Criterion("alignement", 50, "rien à aligner", "")
    tolerance = canvas.width * 0.01
    edges: list[float] = []
    for element in elements:
        edge = element.x if element.align != "middle" else element.x + element.width / 2
        if all(abs(edge - other) > tolerance for other in edges):
            edges.append(edge)
    score = 100 if len(edges) <= 2 else max(0, 100 - 22 * (len(edges) - 2))
    detail = f"{len(edges)} ligne(s) de fuite verticale pour {len(elements)} éléments"
    correction = ""
    if len(edges) > 3:
        correction = (
            f"{len(edges)} points de départ horizontaux différents : caler tous "
            "les éléments sur une seule marge de gauche."
        )
    return Criterion("alignement", score, detail, correction)


def _equilibre(canvas: Canvas) -> Criterion:
    elements = [e for e in canvas.elements if e.role not in {"fond", "bandeau"} and e.area > 0]
    if not elements:
        return Criterion("equilibre", 50, "composition vide", "Ajouter du contenu.")
    total = sum(e.area for e in elements)
    cx = sum(e.center[0] * e.area for e in elements) / total
    cy = sum(e.center[1] * e.area for e in elements) / total
    dx = abs(cx - canvas.width / 2) / canvas.width
    dy = abs(cy - canvas.height / 2) / canvas.height
    drift = math.hypot(dx, dy)
    score = _scale(drift, 0.35, 0.05)
    detail = f"centre de masse décalé de {drift * 100:.0f}% du format"
    correction = ""
    if drift > 0.20:
        cote = "le haut" if cy < canvas.height / 2 else "le bas"
        correction = (
            f"La composition penche vers {cote} ({drift * 100:.0f}% de décalage) : "
            "répartir les blocs plus régulièrement sur la hauteur."
        )
    return Criterion("equilibre", score, detail, correction)


def _espace(canvas: Canvas) -> Criterion:
    coverage = canvas.ink_area() / canvas.area if canvas.area else 0
    # Trop vide comme trop chargé sont des défauts : la note culmine vers 35%.
    if coverage <= 0.35:
        score = _scale(coverage, 0.04, 0.35)
    else:
        score = _scale(coverage, 0.80, 0.35)
    detail = f"{coverage * 100:.0f}% de la surface occupée"
    correction = ""
    if coverage > 0.65:
        correction = (
            f"La page est chargée à {coverage * 100:.0f}% : retirer un bloc "
            "secondaire ou augmenter les marges."
        )
    elif coverage < 0.12:
        correction = (
            f"La page est vide à {(1 - coverage) * 100:.0f}% : agrandir le titre "
            "ou ajouter un argument."
        )
    return Criterion("espace", score, detail, correction)


def _logo(canvas: Canvas, brand: BrandProfile) -> Criterion:
    marks = canvas.by_role("logo")
    if not marks:
        return Criterion(
            "logo", 35, "aucune marque identifiable",
            f"Ajouter le nom « {brand.name} » ou le logo : sans signature, "
            "la création ne sert pas la marque.",
        )
    mark = marks[0]
    ratio = mark.area / canvas.area
    if ratio < 0.002:
        return Criterion("logo", 55, f"marque très discrète ({ratio * 100:.1f}% du format)",
                         "Agrandir la signature de marque.")
    if ratio > 0.20:
        return Criterion("logo", 55, f"marque envahissante ({ratio * 100:.0f}% du format)",
                         "Réduire le logo : il écrase le message.")
    return Criterion("logo", 92, f"marque présente et proportionnée ({ratio * 100:.1f}%)")


def _images(canvas: Canvas) -> Criterion:
    images = [e for e in canvas.elements if e.kind == "image"]
    if not images:
        return Criterion(
            "images", 60, "composition typographique, sans photo",
            "Une photo réelle du sujet renforcerait l'ancrage — à fournir.",
        )
    petites = [e for e in images if e.area / canvas.area < 0.05]
    score = 90 if not petites else 65
    return Criterion("images", score, f"{len(images)} image(s)",
                     "Agrandir les visuels trop petits." if petites else "")


def _couleurs(canvas: Canvas, brand: BrandProfile) -> Criterion:
    used = [canvas.background] + [
        e.fill for e in canvas.elements if e.fill and e.role != "fond"
    ]
    hues = colors.distinct_hues(used)
    palette = {c.lower() for c in brand.palette}
    hors_palette = {
        c.lower() for c in used
        if c.lower() not in palette and colors.saturation(c) > 0.25
    }
    hue_score = 100 if hues <= 3 else max(0, 100 - 25 * (hues - 3))
    palette_score = 100 if not hors_palette else max(40, 100 - 20 * len(hors_palette))
    score = round(0.5 * hue_score + 0.5 * palette_score)
    detail = f"{hues} teinte(s) dominante(s), {len(hors_palette)} couleur(s) hors palette"
    correction = ""
    if hues > 3:
        correction = f"{hues} teintes en présence : revenir à trois au maximum."
    elif hors_palette:
        correction = (
            "Des couleurs ne viennent pas de la palette de marque : "
            + ", ".join(sorted(hors_palette)[:3])
        )
    return Criterion("couleurs", score, detail, correction)


def _impact(canvas: Canvas, brand: BrandProfile) -> Criterion:
    présents = {e.role for e in canvas.elements}
    attendus = {"titre": 30, "prix": 20, "cta": 25, "qr": 15, "contact": 10}
    score = sum(poids for role, poids in attendus.items() if role in présents)
    manquants = [role for role in attendus if role not in présents]
    detail = "présents : " + ", ".join(sorted(présents & set(attendus))) or "rien d'accrocheur"
    correction = ""
    if manquants:
        correction = (
            "Éléments qui font vendre et qui manquent : " + ", ".join(manquants) + "."
        )
    return Criterion("impact", score, detail, correction)


def _cta(canvas: Canvas) -> Criterion:
    cta = canvas.first("cta")
    if cta is None:
        return Criterion("cta", 0, "aucun appel à l'action",
                         "Ajouter une action claire : adresse du site, réservation…")
    titre = canvas.first("titre")
    rapport = cta.size / titre.size if titre and titre.size else 0.3
    contraste = cta.contrast()
    size_score = _scale(rapport, 0.10, 0.28)
    contrast_score = _scale(contraste, 2.0, colors.WCAG_AA_NORMAL)
    score = round(0.5 * size_score + 0.5 * contrast_score)
    detail = f"« {cta.text[:30]} », {rapport:.2f}× le titre, contraste {contraste:.1f}:1"
    correction = ""
    if rapport < 0.16:
        correction = "L'appel à l'action est trop petit face au titre : l'agrandir."
    elif contraste < colors.WCAG_AA_NORMAL:
        correction = "L'appel à l'action manque de contraste : le rendre plus franc."
    return Criterion("cta", score, detail, correction)


# --- Verdict -------------------------------------------------------------------


#: Plages Unicode réellement pictographiques. Les flèches (U+2190–U+21FF) et
#: la ponctuation générale n'en font pas partie : « → » est un signe
#: typographique, pas un emoji — faux positif constaté sur un vrai titre.
_EMOJI_RANGES = (
    (0x1F000, 0x1FAFF),   # pictogrammes, émoticônes, drapeaux
    (0x2600, 0x26FF),     # symboles divers
    (0x2700, 0x27BF),     # casseau
    (0x2B00, 0x2BFF),     # flèches décoratives et formes
    (0xFE0F, 0xFE0F),     # sélecteur de variante emoji
)


def _is_emoji(char: str) -> bool:
    point = ord(char)
    return any(low <= point <= high for low, high in _EMOJI_RANGES)


def _overlaps(canvas: Canvas) -> list[tuple[Element, Element, float]]:
    """Blocs de contenu qui se recouvrent.

    Sans ce contrôle, une maquette où le sous-titre passe **sur** le prix
    obtenait 93/100 : tous les critères étaient bons, mais le résultat était
    illisible. Constaté en regardant le rendu, pas en lisant la note.
    """
    blocs = [
        e for e in canvas.elements
        if e.role not in {"fond", "bandeau", "decor"} and e.area > 0
    ]
    trouves = []
    for i, a in enumerate(blocs):
        for b in blocs[i + 1 :]:
            largeur = min(a.right, b.right) - max(a.x, b.x)
            hauteur = min(a.bottom, b.bottom) - max(a.y, b.y)
            if largeur <= 0 or hauteur <= 0:
                continue
            recouvrement = (largeur * hauteur) / min(a.area, b.area)
            if recouvrement > 0.12:      # un frôlement n'est pas une collision
                trouves.append((a, b, recouvrement))
    return trouves


def _blocking(canvas: Canvas, brand: BrandProfile) -> list[str]:
    """Défauts rédhibitoires : aucune note ne les rachète."""
    problems = []

    for a, b, part in _overlaps(canvas):
        problems.append(
            f"« {a.text[:24] or a.role} » et « {b.text[:24] or b.role} » se "
            f"chevauchent sur {part * 100:.0f}% de leur surface."
        )
    for element in canvas.overflows(margin=1):
        problems.append(
            f"« {element.text[:30] or element.role} » sort du cadre "
            f"(x={element.x:.0f}, y={element.y:.0f})."
        )
    for element in canvas.text_elements():
        largeur = estimate_width(
            max(element.text.split("\n"), key=len), element.size, element.font
        )
        if element.width and largeur > element.width * 1.08:
            problems.append(
                f"« {element.text[:30]} » déborde de sa zone "
                f"({largeur:.0f}px pour {element.width:.0f}px)."
            )
    # Un QR clair sur fond sombre n'est pas scanné par la plupart des lecteurs :
    # c'est un défaut fonctionnel, pas esthétique.
    for element in canvas.by_role("qr"):
        if colors.luminance(element.fill) > colors.luminance(element.on):
            problems.append(
                "Le QR code est clair sur fond sombre : la plupart des lecteurs "
                "ne le scanneront pas. Poser des modules sombres sur plaque claire."
            )
        elif element.contrast() < 7:
            problems.append(
                f"Le QR code n'a que {element.contrast():.1f}:1 de contraste : "
                "insuffisant pour un scan fiable."
            )

    # Les interdits de la marque sont des défauts bloquants, pas des détails.
    if brand.forbids("emoji"):
        for element in canvas.text_elements():
            fautifs = [ch for ch in element.text if _is_emoji(ch)]
            if fautifs:
                problems.append(
                    f"« {element.text[:30]} » contient l'emoji {fautifs[0]!r}, "
                    "que la marque interdit."
                )
    return problems[:6]


def critique(canvas: Canvas, brand: BrandProfile | None = None) -> Critique:
    """Note une composition sur 100 et dit quoi corriger.

    >>> from .brief import Brief
    >>> from .concepts import concept_bandeau
    >>> c = critique(concept_bandeau(Brief(subject="Traversée", price="15 000 FC")))
    >>> 0 <= c.score <= 100
    True
    """
    brand = brand or BrandProfile()
    criteria = [
        _hierarchie(canvas),
        _lisibilite(canvas),
        _contraste(canvas),
        _typographie(canvas),
        _alignement(canvas),
        _equilibre(canvas),
        _espace(canvas),
        _logo(canvas, brand),
        _images(canvas),
        _couleurs(canvas, brand),
        _impact(canvas, brand),
        _cta(canvas),
    ]

    total = sum(WEIGHTS[c.key] for c in criteria)
    score = round(sum(c.score * WEIGHTS[c.key] for c in criteria) / total)

    blocking = _blocking(canvas, brand)
    if blocking:
        # Un défaut bloquant plafonne la note : il faut le corriger avant tout.
        score = min(score, 55 - 5 * (len(blocking) - 1))

    return Critique(score=max(0, score), criteria=criteria, blocking=blocking)
