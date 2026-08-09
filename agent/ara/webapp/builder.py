"""Génération de sites et d'applications web — zéro dépendance, comme le reste.

Ce que produit ce module tient en trois fichiers — `index.html`, `style.css`,
`app.js` — plus un manifeste et un service worker quand on demande une
application installable. Aucun CDN, aucune police distante, aucun script
extérieur : le site doit fonctionner hors ligne, sur un téléphone, derrière
une connexion comorienne. C'est la même contrainte que celle qui a guidé tout
le projet, appliquée à ce qu'il fabrique.

Pourquoi générer du HTML à la main plutôt qu'appeler un modèle
---------------------------------------------------------------
Parce qu'il faut pouvoir **critiquer mécaniquement** le résultat. Un fichier
produit par gabarit a une structure connue : on peut mesurer son contraste,
vérifier qu'aucune ressource externe n'est référencée, qu'un bouton fait plus
de 44 pixels. Un HTML sorti d'un modèle de langage se contrôle beaucoup moins
bien — et le critique est ici plus important que le générateur.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field

#: Types de site reconnus, et ce qu'ils impliquent comme sections par défaut.
KINDS = {
    "vitrine": ["accueil", "services", "contact"],
    "landing": ["accueil", "offre", "contact"],
    "app": ["accueil", "outil", "a-propos"],
    "portfolio": ["accueil", "travaux", "contact"],
}

#: Taille de touche minimale, en pixels. En dessous, un doigt rate la cible.
MIN_TAP_TARGET = 44

#: Texte que le générateur pose quand la demande ne fournit rien à dire.
#: Il est **volontairement reconnaissable** : le critique doit pouvoir le
#: détecter, et un site livré avec ce texte est un site raté.
PLACEHOLDER = "À remplacer par le texte réel."


def slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "section"


@dataclass
class Section:
    """Une section de page : un titre, un texte, éventuellement des points."""

    title: str
    body: str = ""
    bullets: list[str] = field(default_factory=list)
    cta: str = ""
    cta_href: str = ""

    @property
    def anchor(self) -> str:
        return slug(self.title)


@dataclass
class SiteSpec:
    """Ce qu'il faut savoir pour bâtir un site. Rien de plus."""

    title: str
    tagline: str = ""
    kind: str = "vitrine"
    sections: list[Section] = field(default_factory=list)
    lang: str = "fr"
    #: couleurs — reprises de la mémoire de marque quand elle existe
    background: str = "#0b1220"
    surface: str = "#131c2e"
    text: str = "#e8eefc"
    accent: str = "#3ddc97"
    installable: bool = False
    forbidden: list[str] = field(default_factory=list)
    #: phrases dont on dispose réellement pour remplir les sections — texte de
    #: la demande, faits confirmés par la recherche. Rien n'est inventé ici :
    #: une section sans matière reçoit un bouche-trou que le critique refuse.
    material: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title, "kind": self.kind, "lang": self.lang,
            "sections": [s.title for s in self.sections],
            "installable": self.installable,
        }


def spec_from_brief(
    brief: str, *, brand=None, kind: str = "", material: list[str] | None = None
) -> SiteSpec:
    """Lit une demande en français et en tire une structure de site.

    Volontairement modeste : le titre, l'accroche, le type et les sections.
    Ce qui compte n'est pas la finesse de cette lecture — c'est que le
    résultat soit **mesurable** ensuite.
    """
    texte = " ".join(str(brief or "").split())
    minuscule = texte.lower()

    if not kind:
        for nom in KINDS:
            if nom in minuscule:
                kind = nom
                break
        else:
            kind = "app" if "application" in minuscule else "vitrine"

    # Le titre : ce qui suit « pour », « de », sinon les premiers mots utiles.
    titre = ""
    for marqueur in (" pour ", " de ", " sur "):
        if marqueur in minuscule:
            titre = texte[minuscule.index(marqueur) + len(marqueur):]
            break
    titre = titre or texte
    mots = [m for m in re.split(r"[,.;:]", titre)[0].split() if m][:6]
    titre = " ".join(mots).strip(" ,.;:—-") or "Nouveau site"
    titre = titre[:1].upper() + titre[1:]

    # La matière disponible est répartie entre les sections, dans l'ordre. Une
    # section qui n'en reçoit pas garde le bouche-trou : c'est un défaut, il
    # sera mesuré, et le studio choisira de retirer la section plutôt que
    # d'inventer du texte.
    matiere = [phrase.strip() for phrase in (material or []) if phrase and phrase.strip()]
    sections = []
    for index, nom in enumerate(KINDS[kind]):
        corps = matiere[index] if index < len(matiere) else (
            f"Contenu de la section « {nom.replace('-', ' ')} ». {PLACEHOLDER}"
        )
        sections.append(Section(title=nom.replace("-", " ").capitalize(), body=corps))
    if len(matiere) > len(sections):
        sections[-1].bullets = matiere[len(sections):][:6]

    sections[0].cta = "Nous contacter"
    sections[0].cta_href = f"#{sections[-1].anchor}"

    spec = SiteSpec(
        title=titre,
        tagline=texte[:120],
        kind=kind,
        sections=sections,
        installable="application" in minuscule or "installable" in minuscule,
        material=matiere,
    )

    if brand is not None:
        apply_brand(spec, brand)
    return spec


def apply_brand(spec: SiteSpec, brand) -> SiteSpec:
    """Reprend les couleurs et les interdits d'un :class:`BrandProfile`.

    On prend la marque **telle qu'elle est**, y compris quand elle donne un
    mauvais contraste : c'est au critique de le mesurer et au studio de le
    corriger. Choisir déjà de belles couleurs ici rendrait la boucle inutile
    et masquerait le seul défaut que la mémoire des leçons sait retenir.
    """
    spec.background = getattr(brand, "ink", spec.background)
    spec.surface = getattr(brand, "primary", spec.surface)
    spec.text = getattr(brand, "paper", spec.text)
    spec.accent = getattr(brand, "accent", spec.accent)
    spec.forbidden = list(getattr(brand, "avoid", []) or [])
    return spec


# --- Génération -----------------------------------------------------------------


def _escape(text: str) -> str:
    return (
        str(text or "")
        .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_html(spec: SiteSpec) -> str:
    nav = "\n".join(
        f'      <a href="#{s.anchor}">{_escape(s.title)}</a>'
        for s in spec.sections
    )
    corps = []
    for section in spec.sections:
        points = ""
        if section.bullets:
            points = "\n      <ul>\n" + "\n".join(
                f"        <li>{_escape(b)}</li>" for b in section.bullets
            ) + "\n      </ul>"
        bouton = ""
        if section.cta:
            bouton = (
                f'\n      <a class="cta" href="{_escape(section.cta_href or "#")}">'
                f"{_escape(section.cta)}</a>"
            )
        corps.append(
            f'    <section id="{section.anchor}">\n'
            f"      <h2>{_escape(section.title)}</h2>\n"
            f"      <p>{_escape(section.body)}</p>{points}{bouton}\n"
            f"    </section>"
        )

    manifeste = (
        '\n<link rel="manifest" href="manifest.webmanifest">'
        if spec.installable else ""
    )
    return f"""<!DOCTYPE html>
<html lang="{spec.lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{_escape(spec.tagline)}">
<title>{_escape(spec.title)}</title>
<link rel="stylesheet" href="style.css">{manifeste}
</head>
<body>

<header>
  <h1>{_escape(spec.title)}</h1>
  <p class="tagline">{_escape(spec.tagline)}</p>
  <nav>
{nav}
  </nav>
</header>

<main>
{chr(10).join(corps)}
</main>

<footer>
  <p>{_escape(spec.title)}</p>
</footer>

<script src="app.js"></script>
</body>
</html>
"""


def build_css(spec: SiteSpec) -> str:
    # La couleur du texte du bouton n'est pas choisie : elle est **calculée**
    # pour être lisible sur l'accent, et exposée en variable pour que le
    # critique puisse la mesurer sans avoir à lire nos intentions.
    from ..design.color import readable_on

    bouton = readable_on(spec.accent)
    return f""":root {{
  --fond: {spec.background};
  --surface: {spec.surface};
  --texte: {spec.text};
  --accent: {spec.accent};
  --bouton: {bouton};
  --rayon: 14px;
}}

* {{ box-sizing: border-box; }}

body {{
  margin: 0;
  background: var(--fond);
  color: var(--texte);
  font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
}}

header, main, footer {{ max-width: 900px; margin: 0 auto; padding: 24px 16px; }}

h1 {{ font-size: clamp(1.6rem, 5vw, 2.4rem); margin: 0 0 8px; }}
h2 {{ font-size: clamp(1.2rem, 4vw, 1.6rem); margin: 0 0 12px; }}
.tagline {{ color: var(--accent); margin: 0 0 20px; }}

nav {{ display: flex; flex-wrap: wrap; gap: 10px; }}
nav a {{
  display: inline-flex; align-items: center;
  min-height: {MIN_TAP_TARGET}px; padding: 0 16px;
  background: var(--surface); color: var(--texte);
  border-radius: 999px; text-decoration: none;
}}

section {{
  background: var(--surface);
  border-radius: var(--rayon);
  padding: 20px 18px;
  margin-bottom: 16px;
}}

ul {{ margin: 12px 0 0; padding-left: 20px; }}

.cta {{
  display: inline-flex; align-items: center; justify-content: center;
  min-height: {MIN_TAP_TARGET}px; min-width: 160px; margin-top: 16px;
  padding: 0 20px; border-radius: var(--rayon);
  background: var(--accent); color: var(--bouton);
  font-weight: 700; text-decoration: none;
}}

footer {{ color: var(--texte); opacity: .7; font-size: .9rem; }}

@media (prefers-reduced-motion: no-preference) {{
  html {{ scroll-behavior: smooth; }}
}}
"""


def build_js(spec: SiteSpec) -> str:
    enregistrement = (
        "\n  if ('serviceWorker' in navigator) {\n"
        "    navigator.serviceWorker.register('sw.js').catch(function () {});\n"
        "  }\n"
        if spec.installable else "\n"
    )
    return f"""/* {spec.title} — aucun script externe, aucune bibliothèque. */
'use strict';

document.addEventListener('DOMContentLoaded', function () {{
  document.querySelectorAll('nav a').forEach(function (lien) {{
    lien.addEventListener('click', function (evenement) {{
      var cible = document.querySelector(lien.getAttribute('href'));
      if (!cible) return;
      evenement.preventDefault();
      cible.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }});
  }});
{enregistrement}}});
"""


def build_manifest(spec: SiteSpec) -> str:
    return json.dumps(
        {
            "name": spec.title,
            "short_name": spec.title[:12],
            "start_url": ".",
            "display": "standalone",
            "background_color": spec.background,
            "theme_color": spec.accent,
            "lang": spec.lang,
            "icons": [],
        },
        ensure_ascii=False,
        indent=2,
    )


def build_sw(spec: SiteSpec) -> str:
    return """/* Coquille en cache : le site s'ouvre hors ligne. */
const CACHE = 'site-v1';
const SHELL = ['./', 'index.html', 'style.css', 'app.js'];

self.addEventListener('install', function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(SHELL); }));
});

self.addEventListener('fetch', function (e) {
  e.respondWith(caches.match(e.request).then(function (r) {
    return r || fetch(e.request);
  }));
});
"""


def build_site(spec: SiteSpec) -> dict[str, str]:
    """Retourne `{nom de fichier: contenu}`. Rien n'est écrit sur disque ici."""
    fichiers = {
        "index.html": build_html(spec),
        "style.css": build_css(spec),
        "app.js": build_js(spec),
    }
    if spec.installable:
        fichiers["manifest.webmanifest"] = build_manifest(spec)
        fichiers["sw.js"] = build_sw(spec)
    return fichiers


__all__ = [
    "KINDS", "MIN_TAP_TARGET", "PLACEHOLDER", "Section", "SiteSpec",
    "apply_brand", "build_css", "build_html", "build_js", "build_manifest",
    "build_site", "build_sw", "slug", "spec_from_brief",
]
