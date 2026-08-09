"""WEB CRITIC — note un site produit, de 0 à 100, sur les fichiers eux-mêmes.

Le critique ne regarde **pas** la `SiteSpec` qui a servi à générer les
fichiers : il ouvre `index.html`, `style.css`, `app.js` et mesure. C'est la
même règle que pour le critique de flyers — un critique qui interroge
l'intention du créateur ne peut pas le contredire.

Chaque faiblesse porte un **code de défaut** (`DEFECTS`). Ce code est ce qui
circule ensuite : le studio s'en sert pour choisir une correction, et la
mémoire des leçons pour se souvenir, d'une tâche à l'autre, de ce qui rate
souvent. Un message en français libre ne servirait ni à l'un ni à l'autre.

Ce qui est mesuré, et pourquoi
------------------------------
* **autonomie** — une ressource distante casse le site hors ligne, et une
  connexion comorienne n'est pas une connexion de bureau ;
* **contraste** — WCAG 2.1, calculé, pas estimé ;
* **cibles tactiles** — 44 px : en dessous, un doigt rate le bouton ;
* **liens** — une ancre qui ne mène nulle part est un bug silencieux ;
* **contenu** — le texte bouche-trou du générateur ne doit jamais survivre ;
* **interdits de marque** — ce que le patron a interdit une fois vaut pour
  toujours (`BrandProfile.avoid`).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser

from ..design import color as colors
from .builder import MIN_TAP_TARGET, PLACEHOLDER

#: Codes de défaut. Stables : la mémoire des leçons les stocke sur disque.
DEFECTS = {
    "structure_invalide": "HTML mal formé ou balise non refermée",
    "ressource_externe": "ressource chargée depuis un autre serveur",
    "contraste_insuffisant": "texte sous le seuil WCAG AA",
    "cible_trop_petite": "élément tactile de moins de 44 px",
    "viewport_absent": "pas de meta viewport : le site sera illisible au téléphone",
    "lien_mort": "lien interne qui ne mène nulle part",
    "titre_manquant": "titre, langue ou description absents",
    "texte_bouche_trou": "texte de remplissage laissé dans la page",
    "contenu_pauvre": "page trop maigre faute de matière fournie",
    "interdit_de_marque": "élément explicitement interdit par la marque",
    "poids_excessif": "fichiers trop lourds pour une connexion lente",
    "manifeste_invalide": "application déclarée installable mais manifeste incomplet",
}

#: Poids des critères, sur 100.
WEIGHTS = {
    "structure": 14,
    "autonomie": 14,
    "contraste": 16,
    "mobile": 12,
    "liens": 10,
    "semantique": 10,
    "contenu": 12,
    "interdits": 6,
    "poids": 3,
    "installable": 3,
}

LABELS = {
    "structure": "structure du document",
    "autonomie": "autonomie (aucune ressource distante)",
    "contraste": "contraste du texte",
    "mobile": "usage au téléphone",
    "liens": "liens internes",
    "semantique": "titre, langue, description",
    "contenu": "contenu réel",
    "interdits": "interdits de marque",
    "poids": "poids des fichiers",
    "installable": "installation hors ligne",
}

#: Un défaut de cette liste interdit la livraison, quelle que soit la note.
BLOCKING = {
    "structure_invalide", "ressource_externe", "contraste_insuffisant",
    "lien_mort", "texte_bouche_trou",
}

#: Au-delà, le site devient pénible à charger sur une connexion lente.
MAX_TOTAL_BYTES = 150_000

_EXTERNAL = re.compile(r"""(?:src|href)\s*=\s*["'](\s*(?:https?:)?//[^"']+)["']""", re.I)
_CSS_URL = re.compile(r"url\(\s*['\"]?\s*(?:https?:)?//", re.I)
_IMPORT = re.compile(r"@import\s+(?:url\()?['\"]?\s*(?:https?:)?//", re.I)
_VAR = re.compile(r"--([a-z-]+)\s*:\s*(#[0-9a-fA-F]{3,8})\s*;")
_MIN_HEIGHT = re.compile(r"min-height\s*:\s*(\d+(?:\.\d+)?)px")
_EMOJI = re.compile(
    "[\U0001f300-\U0001faff☀-➿⬀-⯿️]"
)

#: Balises sans fermeture : les compter comme ouvertes ferait un faux défaut.
_VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


@dataclass
class Criterion:
    key: str
    score: int
    detail: str
    correction: str = ""
    defect: str = ""

    @property
    def label(self) -> str:
        return LABELS.get(self.key, self.key)

    def to_dict(self) -> dict:
        return {
            "key": self.key, "label": self.label, "score": self.score,
            "detail": self.detail, "correction": self.correction,
            "defect": self.defect,
        }


@dataclass
class Critique:
    """Verdict complet sur un site."""

    score: int = 0
    criteria: list[Criterion] = field(default_factory=list)
    blocking: list[str] = field(default_factory=list)
    defects: list[str] = field(default_factory=list)

    @property
    def deliverable(self) -> bool:
        return not self.blocking

    def worst(self) -> list[Criterion]:
        """Critères à corriger, du plus coûteux au moins coûteux.

        Le coût, c'est le poids du critère multiplié par ce qui lui manque —
        pas la note brute. Corriger un critère à 40 qui pèse 3 points rapporte
        moins que corriger un critère à 70 qui en pèse 16.
        """
        faibles = [c for c in self.criteria if c.score < 100 and c.correction]
        return sorted(
            faibles,
            key=lambda c: WEIGHTS.get(c.key, 1) * (100 - c.score),
            reverse=True,
        )

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "deliverable": self.deliverable,
            "blocking": self.blocking,
            "defects": self.defects,
            "criteria": [c.to_dict() for c in self.criteria],
        }

    def report(self) -> str:
        lignes = [f"**Note : {self.score}/100**", ""]
        for critere in sorted(self.criteria, key=lambda c: c.score):
            marque = "✕" if critere.defect else "✓"
            lignes.append(f"- {marque} **{critere.label}** — {critere.score}/100. {critere.detail}")
            if critere.correction:
                lignes.append(f"  - correction : {critere.correction}")
        if self.blocking:
            lignes += ["", "**Bloquant :**"] + [f"- {b}" for b in self.blocking]
        return "\n".join(lignes)


class _Page(HTMLParser):
    """Lecture mécanique du HTML : ids, liens, métadonnées, balises ouvertes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []
        self.assets: list[str] = []
        self.lang = ""
        self.title = ""
        self.description = ""
        self.viewport = ""
        self.h1 = 0
        self.classes: set[str] = set()
        self.tags: list[str] = []
        self.unclosed: list[str] = []
        self.stray: list[str] = []
        self._in_title = False
        self.text_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "html":
            self.lang = attributes.get("lang", "") or ""
        if tag == "title":
            self._in_title = True
        if tag == "h1":
            self.h1 += 1
        if "id" in attributes and attributes["id"]:
            self.ids.add(attributes["id"])
        for nom in (attributes.get("class") or "").split():
            self.classes.add(nom)
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        for cle in ("src", "href"):
            valeur = attributes.get(cle)
            if valeur and tag in {"script", "link", "img", "iframe", "source"}:
                self.assets.append(valeur)
        if tag == "meta":
            nom = (attributes.get("name") or "").lower()
            if nom == "description":
                self.description = attributes.get("content", "")
            elif nom == "viewport":
                self.viewport = attributes.get("content", "")
        if tag not in _VOID:
            self.tags.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.tags and self.tags[-1] == tag:
            self.tags.pop()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in _VOID:
            return
        if tag in self.tags:
            while self.tags and self.tags.pop() != tag:
                pass
        else:
            self.stray.append(tag)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif data.strip():
            self.text_parts.append(data.strip())

    def close(self):  # type: ignore[override]
        super().close()
        self.unclosed = list(self.tags)


def _css_blocks(css: str) -> list[tuple[str, str]]:
    """[(sélecteur, déclarations)] — suffisant pour ce que l'on mesure."""
    blocs: list[tuple[str, str]] = []
    for morceau in re.split(r"\}", css):
        if "{" not in morceau:
            continue
        selecteur, _, declarations = morceau.partition("{")
        selecteur = selecteur.strip().splitlines()[-1].strip()
        blocs.append((selecteur, declarations))
    return blocs


def _variables(css: str) -> dict[str, str]:
    return {nom: valeur for nom, valeur in _VAR.findall(css)}


# --- Les critères, un par un --------------------------------------------------


def _structure(page: _Page, html: str) -> Criterion:
    problemes = []
    if "<!DOCTYPE html>" not in html and "<!doctype html>" not in html:
        problemes.append("pas de DOCTYPE")
    if page.unclosed:
        problemes.append("balise(s) non refermée(s) : " + ", ".join(page.unclosed[:4]))
    if page.stray:
        problemes.append("fermeture(s) orpheline(s) : " + ", ".join(page.stray[:4]))
    if not problemes:
        return Criterion("structure", 100, f"{len(page.ids)} ancre(s), document bien formé")
    return Criterion(
        "structure", 30, " ; ".join(problemes),
        correction="régénérer le document depuis le gabarit",
        defect="structure_invalide",
    )


def _autonomie(files: dict[str, str]) -> Criterion:
    externes: list[str] = []
    for nom, contenu in files.items():
        if nom.endswith((".html", ".htm")):
            externes += [m.strip() for m in _EXTERNAL.findall(contenu)]
        if nom.endswith(".css") and (_CSS_URL.search(contenu) or _IMPORT.search(contenu)):
            externes.append(f"{nom} : ressource distante en CSS")
        if nom.endswith(".js") and re.search(r"""fetch\(\s*['"](?:https?:)?//""", contenu):
            externes.append(f"{nom} : appel réseau distant")
    if not externes:
        return Criterion("autonomie", 100, "aucune ressource distante : le site tient hors ligne")
    return Criterion(
        "autonomie", 0,
        f"{len(externes)} ressource(s) distante(s) : " + ", ".join(externes[:3]),
        correction="supprimer la référence externe ou embarquer la ressource",
        defect="ressource_externe",
    )


def _contraste(css: str) -> Criterion:
    variables = _variables(css)
    fond = variables.get("fond") or variables.get("surface") or "#ffffff"
    surface = variables.get("surface", fond)
    texte = variables.get("texte", "#000000")
    accent = variables.get("accent", texte)
    bouton = variables.get("bouton", fond)

    mesures = {
        "texte sur fond": (texte, fond),
        "texte sur surface": (texte, surface),
        "accroche (accent) sur fond": (accent, fond),
        "texte du bouton sur accent": (bouton, accent),
    }
    ratios = {}
    for nom, (avant, arriere) in mesures.items():
        try:
            ratios[nom] = colors.contrast(avant, arriere)
        except ValueError:
            ratios[nom] = 0.0

    pire_nom = min(ratios, key=ratios.get)
    pire = ratios[pire_nom]
    detail = " · ".join(f"{nom} {valeur:.1f}:1" for nom, valeur in ratios.items())

    if pire >= colors.WCAG_AA_NORMAL:
        return Criterion("contraste", 100, detail)
    note = max(0, int(pire / colors.WCAG_AA_NORMAL * 70))
    return Criterion(
        "contraste", note, f"{detail} — le plus faible : {pire_nom}",
        correction="éclaircir ou assombrir la couleur de texte jusqu'à 4,5:1",
        defect="contraste_insuffisant",
    )


def _mobile(page: _Page, css: str) -> Criterion:
    if not page.viewport or "width=device-width" not in page.viewport:
        return Criterion(
            "mobile", 0, "meta viewport absente ou incomplète",
            correction="ajouter <meta name=viewport content=width=device-width>",
            defect="viewport_absent",
        )

    interactifs = {"nav a": "nav" in page.tags or bool(page.links), ".cta": "cta" in page.classes}
    trop_petits: list[str] = []
    absents: list[str] = []
    for selecteur, present in interactifs.items():
        if not present:
            continue
        tailles = [
            float(v)
            for sel, decl in _css_blocks(css) if selecteur in sel
            for v in _MIN_HEIGHT.findall(decl)
        ]
        if not tailles:
            absents.append(selecteur)
        elif min(tailles) < MIN_TAP_TARGET:
            trop_petits.append(f"{selecteur} : {min(tailles):.0f}px")

    if not trop_petits and not absents:
        return Criterion("mobile", 100, f"cibles tactiles ≥ {MIN_TAP_TARGET}px, viewport correcte")
    detail = "; ".join(trop_petits + [f"{s} : aucune hauteur minimale" for s in absents])
    return Criterion(
        "mobile", 45, detail,
        correction=f"porter la hauteur des éléments tactiles à {MIN_TAP_TARGET}px",
        defect="cible_trop_petite",
    )


def _liens(page: _Page, files: dict[str, str]) -> Criterion:
    morts: list[str] = []
    for lien in page.links:
        if lien.startswith("#"):
            if lien[1:] and lien[1:] not in page.ids:
                morts.append(lien)
        elif "://" not in lien and not lien.startswith(("mailto:", "tel:")):
            cible = lien.split("#")[0].split("?")[0]
            if cible and cible not in files and not cible.startswith("."):
                morts.append(lien)
    for asset in page.assets:
        if "://" in asset or asset.startswith("//"):
            continue
        if asset not in files:
            morts.append(asset)

    if not morts:
        return Criterion("liens", 100, f"{len(page.links)} lien(s) interne(s), tous résolus")
    return Criterion(
        "liens", 20, "cible(s) introuvable(s) : " + ", ".join(sorted(set(morts))[:4]),
        correction="pointer chaque lien vers une ancre ou un fichier existant",
        defect="lien_mort",
    )


def _semantique(page: _Page) -> Criterion:
    manques = []
    if not page.title.strip():
        manques.append("titre vide")
    if not page.lang.strip():
        manques.append("langue non déclarée")
    if not page.description.strip():
        manques.append("description absente")
    if page.h1 != 1:
        manques.append(f"{page.h1} balise(s) h1 au lieu d'une")
    if not manques:
        return Criterion("semantique", 100, f"« {page.title.strip()} », langue {page.lang}")
    return Criterion(
        "semantique", max(0, 100 - 30 * len(manques)), " ; ".join(manques),
        correction="compléter le titre, la langue, la description et l'unique h1",
        defect="titre_manquant",
    )


def _contenu(page: _Page) -> Criterion:
    texte = " ".join(page.text_parts)
    bouche_trous = [
        marqueur for marqueur in (PLACEHOLDER, "Lorem ipsum", "À remplacer", "TODO")
        if marqueur.lower() in texte.lower()
    ]
    if bouche_trous:
        return Criterion(
            "contenu", 10,
            f"texte de remplissage présent ({bouche_trous[0]})",
            correction="écrire le contenu réel de chaque section, ou retirer la section",
            defect="texte_bouche_trou",
        )
    mots = len(texte.split())
    if mots < 40:
        # Défaut distinct, et **non bloquant** : une page maigre parce que la
        # demande ne fournissait rien est un manque de matière, pas une faute
        # de fabrication. Le studio ne sait pas la corriger sans inventer, et
        # c'est exactement ce qu'on lui interdit.
        return Criterion(
            "contenu", 55, f"{mots} mots seulement : la page paraîtra vide",
            correction="", defect="contenu_pauvre",
        )
    return Criterion("contenu", 100, f"{mots} mots de contenu réel")


#: Un terme entre guillemets dans une règle de marque est **vérifiable** :
#: le patron désigne exactement ce qu'il refuse de voir écrit.
_QUOTED = re.compile(r"[«\"']\s*([^»\"']{2,40}?)\s*[»\"']")


def banned_terms(rule: str) -> list[str]:
    """Termes qu'une règle de marque interdit **de façon décidable**.

    Une règle en français libre ne se lit pas mécaniquement. « ne pas écrire
    Chindini comme port de départ : c'est Ouroveni » cite deux noms propres,
    dont l'un est justement celui qu'il faut employer : extraire les majuscules
    au hasard signalerait le bon mot comme une faute. On s'en tient donc à ce
    qui est explicite — un terme entre guillemets — et le reste est déclaré
    non vérifiable plutôt que deviné. C'est la même règle que pour les devises
    inconnues : UNKNOWN vaut mieux qu'une supposition.
    """
    return [terme.strip() for terme in _QUOTED.findall(rule or "") if terme.strip()]


def _interdits(files: dict[str, str], forbidden: list[str]) -> Criterion:
    html = files.get("index.html", "")
    trouves: list[str] = []
    verifiees = 0
    indecidables: list[str] = []

    for regle in forbidden or []:
        decidable = False
        if "emoji" in regle.lower():
            decidable = True
            if _EMOJI.search(html):
                trouves.append("emojis présents alors que la marque les interdit")
        for terme in banned_terms(regle):
            decidable = True
            if re.search(rf"\b{re.escape(terme)}\b", html, re.I):
                trouves.append(f"« {terme} » apparaît alors que la marque l'interdit")
        verifiees += decidable
        if not decidable:
            indecidables.append(regle)

    if trouves:
        return Criterion(
            "interdits", 0, " ; ".join(trouves[:3]),
            correction="retirer l'élément interdit par la marque",
            defect="interdit_de_marque",
        )
    detail = f"{verifiees} règle(s) vérifiée(s)"
    if indecidables:
        detail += (
            f" · {len(indecidables)} non vérifiable(s) mécaniquement "
            f"(pour la rendre vérifiable, citer le terme entre guillemets) : "
            + " ; ".join(indecidables[:2])
        )
    return Criterion("interdits", 100, detail)


def _poids(files: dict[str, str]) -> Criterion:
    total = sum(len(contenu.encode("utf-8")) for contenu in files.values())
    if total <= MAX_TOTAL_BYTES:
        return Criterion("poids", 100, f"{total / 1024:.1f} Ko au total")
    return Criterion(
        "poids", 40, f"{total / 1024:.1f} Ko — au-delà de {MAX_TOTAL_BYTES / 1024:.0f} Ko",
        correction="alléger le contenu ou découper la page",
        defect="poids_excessif",
    )


def _installable(files: dict[str, str], page: _Page) -> Criterion:
    manifeste = files.get("manifest.webmanifest")
    if manifeste is None:
        return Criterion("installable", 100, "site simple : pas d'installation demandée")
    try:
        data = json.loads(manifeste)
    except json.JSONDecodeError as exc:
        return Criterion(
            "installable", 0, f"manifeste illisible : {exc}",
            correction="réécrire le manifeste", defect="manifeste_invalide",
        )
    manques = [cle for cle in ("name", "start_url", "display") if not data.get(cle)]
    if "sw.js" not in files:
        manques.append("service worker")
    elif "caches.open" not in files["sw.js"]:
        manques.append("mise en cache de la coquille")
    if manques:
        return Criterion(
            "installable", 30, "manifeste incomplet : " + ", ".join(manques),
            correction="compléter le manifeste et le service worker",
            defect="manifeste_invalide",
        )
    return Criterion("installable", 100, f"installable : « {data['name']} », hors ligne")


def critique(files: dict[str, str], *, forbidden: list[str] | None = None) -> Critique:
    """Mesure un site livré sous forme `{nom de fichier: contenu}`."""
    html = files.get("index.html", "")
    css = files.get("style.css", "")

    page = _Page()
    try:
        page.feed(html)
        page.close()
    except Exception:  # un HTML impossible à lire est un défaut, pas un plantage
        page.unclosed = ["<illisible>"]

    criteres = [
        _structure(page, html),
        _autonomie(files),
        _contraste(css),
        _mobile(page, css),
        _liens(page, files),
        _semantique(page),
        _contenu(page),
        _interdits(files, list(forbidden or [])),
        _poids(files),
        _installable(files, page),
    ]

    total = sum(WEIGHTS[c.key] * c.score for c in criteres) / sum(WEIGHTS.values())
    defauts = [c.defect for c in criteres if c.defect]
    return Critique(
        score=round(total),
        criteria=criteres,
        blocking=[DEFECTS[d] for d in defauts if d in BLOCKING],
        defects=defauts,
    )


__all__ = [
    "BLOCKING", "Criterion", "Critique", "DEFECTS", "MAX_TOTAL_BYTES",
    "WEIGHTS", "critique",
]
