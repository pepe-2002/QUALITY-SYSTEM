"""CREATIVE / DESIGN AGENT — production de plusieurs concepts (spec §5).

La spec est explicite : **au moins trois concepts**, puis comparaison. Un seul
jet, c'est le réflexe du chatbot ; proposer et confronter, c'est le travail d'un
studio.

Les trois partis pris ne sont pas des variations cosmétiques, ils répondent à
des situations différentes :

* **A — Bandeau** : un en-tête coloré porte le titre, le corps respire en
  dessous. Le plus lisible de loin ; le choix par défaut d'une affiche de gare.
* **B — Plein cadre** : la couleur de marque occupe tout, le message est
  centré. Le plus mémorable en vignette sur un fil d'actualité.
* **C — Colonne** : une bande latérale tient la marque et le QR, le contenu
  s'aligne à droite. Le plus dense ; utile quand il y a beaucoup à dire.

Chaque concept est construit sur une **grille** : marge unique, gouttière
unique, tailles issues d'une progression. C'est ce qui rend l'alignement et la
hiérarchie mesurables par le critique, au lieu d'être affaire de goût.
"""

from __future__ import annotations

from dataclasses import replace

from . import color as colors
from . import qr as qrcode
from .brief import Brief
from .canvas import Canvas, Element, estimate_width, wrap

#: Progression typographique : chaque niveau est nettement plus petit que le
#: précédent. Un écart insuffisant, et la hiérarchie ne se lit pas.
SCALE = {"titre": 1.0, "sous-titre": 0.42, "prix": 0.52, "accroche": 0.30,
         "corps": 0.22, "cta": 0.26, "contact": 0.18, "mention": 0.14}


def _qr_block(brief: Brief, x: float, y: float, size: float, ink: str) -> list[Element]:
    """QR vérifié, posé sur sa propre plaque claire.

    ⚠️ Un QR clair sur fond sombre est refusé par beaucoup de lecteurs : ils
    cherchent des modules **sombres sur fond clair**. On ajoute donc toujours
    une plaque blanche sous le code, quelle que soit la maquette — défaut
    constaté en regardant le rendu du concept plein cadre.
    """
    if not brief.url:
        return []
    try:
        code = qrcode.make_verified(brief.url, "H")
    except qrcode.QRError:
        return []

    modules = code.size + 8  # zone de silence comprise
    unit = size / modules
    return [
        Element("rect", "decor", x, y, size, size, fill="#ffffff",
                radius=size * 0.04, on="#ffffff"),
        Element(
            kind="qr", role="qr", x=x, y=y, width=size, height=size,
            path=code.to_svg_path(module=unit, quiet=4.0),
            fill=ink, on="#ffffff", text=brief.url,
        ),
    ]


def _title_of(brief: Brief) -> str:
    if brief.title:
        return brief.title
    words = brief.subject.split()
    return " ".join(words[:7]) if words else "Sans titre"


def _lines(brief: Brief) -> list[str]:
    """Points saillants : ceux du brief, sinon ceux tirés de la recherche."""
    if brief.bullets:
        return brief.bullets[:4]
    return [item for item in brief.market[:3] if item]


def _cta(brief: Brief) -> str:
    """Appel à l'action, en respectant les interdits de la marque."""
    if brief.brand.forbids("embarquez"):
        return brief.url.replace("https://", "").replace("http://", "").rstrip("/")
    return {
        "conversion": "Réservez en ligne",
        "trafic": "Rendez-vous sur le site",
        "fidelisation": "Rejoignez-nous",
    }.get(brief.objective, brief.url.replace("https://", "").rstrip("/") or "En savoir plus")


# --- Concept A : bandeau ------------------------------------------------------


def concept_bandeau(brief: Brief) -> Canvas:
    brand = brief.brand
    width, height = brief.width, brief.height
    margin = round(width * 0.075)
    inner = width - 2 * margin
    band = round(height * 0.30)

    canvas = Canvas(width, height, background=brand.paper, name="A — Bandeau",
                    note="En-tête coloré, corps aéré. Le plus lisible de loin.")
    canvas.add(Element("rect", "bandeau", 0, 0, width, band, fill=brand.primary))

    title_size = round(width * 0.082)
    title = wrap(_title_of(brief), title_size, inner, brand.title_font, max_lines=3)
    ink = colors.readable_on(brand.primary, ("#ffffff", brand.ink))

    # Une création sans signature de marque ne sert pas la marque : le nom
    # fait partie du concept, ce n'est pas une correction d'après-coup.
    mark_size = round(width * 0.022)
    canvas.add(Element(
        "text", "logo", margin, round(band * 0.10), inner, mark_size * 1.2,
        text=brand.name.upper(), size=mark_size, font=brand.title_font,
        weight="700", letter_spacing=mark_size * 0.16,
        fill=colors.readable_on(brand.primary, (brand.accent, "#ffffff")),
        on=brand.primary,
    ))
    canvas.add(Element(
        "text", "titre", margin, round(band * 0.24), inner, title_size * 1.3,
        text=title, size=title_size, font=brand.title_font, weight="700",
        fill=ink, on=brand.primary, line_height=1.15,
    ))

    y = band + round(height * 0.05)
    if brief.subtitle or brief.subject:
        sub_size = round(title_size * SCALE["sous-titre"])
        sub = wrap(brief.subtitle or brief.subject, sub_size, inner, brand.body_font, 2)
        canvas.add(Element(
            "text", "sous-titre", margin, y, inner, sub_size * 1.4, text=sub,
            size=sub_size, font=brand.body_font, fill=colors.mix(brand.ink, brand.paper, 0.35),
            on=brand.paper,
        ))
        y += sub_size * 1.6 + round(height * 0.02)

    body_size = round(title_size * SCALE["corps"])
    for line in _lines(brief):
        canvas.add(Element(
            "rect", "decor", margin, y + body_size * 0.35, body_size * 0.35,
            body_size * 0.35, fill=brand.accent, radius=body_size * 0.2, on=brand.paper,
        ))
        canvas.add(Element(
            "text", "corps", margin + body_size, y, inner - body_size,
            body_size * 1.3, text=wrap(line, body_size, inner - body_size, brand.body_font, 2),
            size=body_size, font=brand.body_font, fill=brand.ink, on=brand.paper,
        ))
        y += body_size * 1.9

    if brief.price:
        price_size = round(title_size * SCALE["prix"])
        pad = price_size * 0.45
        badge_w = estimate_width(brief.price, price_size, brand.title_font) + pad * 2
        badge_y = height - round(height * 0.30)
        canvas.add(Element("rect", "decor", margin, badge_y, badge_w,
                           price_size * 1.7, fill=brand.accent,
                           radius=price_size * 0.25, on=brand.paper))
        canvas.add(Element(
            "text", "prix", margin + pad, badge_y + price_size * 0.35, badge_w - pad * 2,
            price_size * 1.2, text=brief.price, size=price_size, font=brand.title_font,
            weight="700", fill=colors.readable_on(brand.accent, (brand.ink, "#ffffff")),
            on=brand.accent,
        ))

    qr_size = round(width * 0.20)
    qr_parts = _qr_block(brief, width - margin - qr_size, height - margin - qr_size,
                         qr_size, brand.ink)
    for part in qr_parts:
        canvas.add(part)
    qr = bool(qr_parts)

    cta_size = round(title_size * SCALE["cta"])
    canvas.add(Element(
        "text", "cta", margin, height - margin - cta_size * 2.2,
        inner - (qr_size + margin if qr else 0), cta_size * 1.3,
        text=_cta(brief), size=cta_size, font=brand.title_font, weight="700",
        fill=brand.primary, on=brand.paper,
    ))
    if brief.contact:
        small = round(title_size * SCALE["contact"])
        canvas.add(Element(
            "text", "contact", margin, height - margin - small * 1.2,
            inner - (qr_size + margin if qr else 0), small * 1.2, text=brief.contact,
            size=small, font=brand.body_font,
            fill=colors.mix(brand.ink, brand.paper, 0.4), on=brand.paper,
        ))
    return canvas


# --- Concept B : plein cadre --------------------------------------------------


def concept_plein_cadre(brief: Brief) -> Canvas:
    brand = brief.brand
    width, height = brief.width, brief.height
    margin = round(width * 0.10)
    inner = width - 2 * margin
    deep = colors.darken(brand.primary, 0.25)

    canvas = Canvas(width, height, background=deep, name="B — Plein cadre",
                    note="Couleur de marque plein cadre, message centré. Le plus mémorable en vignette.")
    canvas.add(Element("rect", "decor", 0, round(height * 0.62), width,
                       round(height * 0.38), fill=brand.primary, opacity=0.55, on=deep))

    ink = colors.readable_on(deep, ("#ffffff", brand.ink))

    mark_size = round(width * 0.024)
    canvas.add(Element(
        "text", "logo", margin, round(height * 0.09), inner, mark_size * 1.2,
        text=brand.name.upper(), size=mark_size, font=brand.title_font,
        weight="700", letter_spacing=mark_size * 0.18,
        fill=colors.readable_on(deep, (brand.accent, "#ffffff")),
        on=deep, align="middle",
    ))

    title_size = round(width * 0.095)
    title = wrap(_title_of(brief), title_size, inner, brand.title_font, 3)
    title_y = round(height * 0.20)
    canvas.add(Element(
        "text", "titre", margin, title_y, inner, title_size * 1.25 * (title.count("\n") + 1),
        text=title, size=title_size, font=brand.title_font, weight="700",
        fill=ink, on=deep, align="middle", line_height=1.15,
    ))

    rule_y = title_y + title_size * 1.25 * (title.count("\n") + 1) + round(height * 0.025)
    canvas.add(Element("line", "decor", width / 2 - inner * 0.12, rule_y,
                       inner * 0.24, 0, stroke=brand.accent, stroke_width=width * 0.006, on=deep))

    y = rule_y + round(height * 0.05)
    sub_size = round(title_size * SCALE["sous-titre"])
    if brief.subtitle or brief.subject:
        sub = wrap(brief.subtitle or brief.subject, sub_size, inner, brand.body_font, 3)
        canvas.add(Element(
            "text", "sous-titre", margin, y, inner,
            sub_size * 1.4 * (sub.count("\n") + 1), text=sub, size=sub_size,
            font=brand.body_font, fill=colors.mix(ink, deep, 0.25), on=deep, align="middle",
        ))
        y += sub_size * 1.5 * (sub.count("\n") + 1) + round(height * 0.03)

    if brief.price:
        price_size = round(title_size * SCALE["prix"])
        canvas.add(Element(
            "text", "prix", margin, round(height * 0.60), inner, price_size * 1.3,
            text=brief.price, size=price_size, font=brand.title_font, weight="700",
            fill=brand.accent, on=deep, align="middle",
        ))

    qr_size = round(width * 0.22)
    for part in _qr_block(brief, (width - qr_size) / 2, round(height * 0.71),
                          qr_size, brand.ink):
        canvas.add(part)

    cta_size = round(title_size * SCALE["cta"])
    canvas.add(Element(
        "text", "cta", margin, height - margin - cta_size * 2.4, inner, cta_size * 1.3,
        text=_cta(brief), size=cta_size, font=brand.title_font, weight="700",
        fill=ink, on=deep, align="middle",
    ))
    if brief.contact:
        small = round(title_size * SCALE["contact"])
        canvas.add(Element(
            "text", "contact", margin, height - margin - small * 1.1, inner, small * 1.2,
            text=brief.contact, size=small, font=brand.body_font,
            fill=colors.mix(ink, deep, 0.35), on=deep, align="middle",
        ))
    return canvas


# --- Concept C : colonne ------------------------------------------------------


def concept_colonne(brief: Brief) -> Canvas:
    brand = brief.brand
    width, height = brief.width, brief.height
    rail = round(width * 0.28)
    margin = round(width * 0.06)
    inner = width - rail - margin * 2

    canvas = Canvas(width, height, background=brand.paper, name="C — Colonne",
                    note="Bande latérale pour la marque et le QR, contenu aligné à droite. Le plus dense.")
    canvas.add(Element("rect", "bandeau", 0, 0, rail, height, fill=brand.primary))

    rail_ink = colors.readable_on(brand.primary, ("#ffffff", brand.ink))
    name_size = round(rail * 0.16)
    canvas.add(Element(
        "text", "logo", round(rail * 0.12), round(height * 0.07),
        rail - round(rail * 0.24), name_size * 1.3,
        text=wrap(brand.name, name_size, rail - round(rail * 0.24), brand.title_font, 2),
        size=name_size, font=brand.title_font, weight="700", fill=rail_ink,
        on=brand.primary, line_height=1.1,
    ))

    qr_size = round(rail * 0.62)
    for part in _qr_block(brief, (rail - qr_size) / 2,
                          height - round(height * 0.14) - qr_size, qr_size, brand.ink):
        canvas.add(part)

    title_size = round(width * 0.070)
    x = rail + margin
    title = wrap(_title_of(brief), title_size, inner, brand.title_font, 4)
    canvas.add(Element(
        "text", "titre", x, round(height * 0.10), inner,
        title_size * 1.2 * (title.count("\n") + 1), text=title, size=title_size,
        font=brand.title_font, weight="700", fill=brand.primary, on=brand.paper,
        line_height=1.12,
    ))

    y = round(height * 0.10) + title_size * 1.2 * (title.count("\n") + 1) + round(height * 0.035)
    canvas.add(Element("line", "decor", x, y, inner * 0.30, 0,
                       stroke=brand.accent, stroke_width=width * 0.005, on=brand.paper))
    y += round(height * 0.04)

    sub_size = round(title_size * SCALE["sous-titre"])
    if brief.subtitle or brief.subject:
        sub = wrap(brief.subtitle or brief.subject, sub_size, inner, brand.body_font, 3)
        canvas.add(Element(
            "text", "sous-titre", x, y, inner, sub_size * 1.4 * (sub.count("\n") + 1),
            text=sub, size=sub_size, font=brand.body_font,
            fill=colors.mix(brand.ink, brand.paper, 0.3), on=brand.paper,
        ))
        y += sub_size * 1.5 * (sub.count("\n") + 1) + round(height * 0.03)

    body_size = round(title_size * SCALE["corps"])
    for line in _lines(brief):
        canvas.add(Element(
            "text", "corps", x, y, inner, body_size * 1.3,
            text="• " + wrap(line, body_size, inner, brand.body_font, 2),
            size=body_size, font=brand.body_font, fill=brand.ink, on=brand.paper,
        ))
        y += body_size * 2.0

    if brief.price:
        price_size = round(title_size * SCALE["prix"])
        canvas.add(Element(
            "text", "prix", x, height - round(height * 0.26), inner, price_size * 1.3,
            text=brief.price, size=price_size, font=brand.title_font, weight="700",
            fill=brand.primary, on=brand.paper,
        ))

    cta_size = round(title_size * SCALE["cta"])
    canvas.add(Element(
        "text", "cta", x, height - round(height * 0.15), inner, cta_size * 1.3,
        text=_cta(brief), size=cta_size, font=brand.title_font, weight="700",
        fill=brand.accent if colors.contrast(brand.accent, brand.paper) >= 3 else brand.primary,
        on=brand.paper,
    ))
    if brief.contact:
        small = round(title_size * SCALE["contact"])
        canvas.add(Element(
            "text", "contact", x, height - round(height * 0.10), inner, small * 1.2,
            text=brief.contact, size=small, font=brand.body_font,
            fill=colors.mix(brand.ink, brand.paper, 0.4), on=brand.paper,
        ))
    return canvas


#: Les trois partis pris, dans l'ordre de présentation
CONCEPTS = (concept_bandeau, concept_plein_cadre, concept_colonne)


def propose(brief: Brief) -> list[Canvas]:
    """Produit les concepts. Jamais un seul (spec §5)."""
    return [build(brief) for build in CONCEPTS]
