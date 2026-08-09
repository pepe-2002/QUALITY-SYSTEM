"""Boucle de fabrication d'un site : construire → critiquer → corriger.

    SPEC → SITE V1 → CRITIQUE → CORRECTION → SITE V2 → … → LIVRAISON

Deux règles héritées du studio graphique, et qui valent ici mot pour mot :

* la première version n'est **jamais** réputée correcte — elle est notée ;
* une correction qui fait **baisser** la note est annulée, et la boucle
  s'arrête sur « version précédente meilleure ».

Ce que ce studio ajoute par rapport à celui des flyers, c'est la troisième
règle : ce qu'il apprend en corrigeant sort de la tâche. Les codes de défaut
dont la correction a marché sont écrits dans `workspace/lessons.json`, et
appliqués **avant** la première version de la tâche suivante. C'est là, et
seulement là, que l'agent « apprend de ses erreurs ».

Toutes les corrections agissent sur la `SiteSpec`, jamais sur les fichiers :
on régénère. Retoucher du HTML au marteau produirait des documents qu'aucun
gabarit ne sait plus reconstruire — et rendrait le retour arrière impossible.
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field

from ..design import color as colors
from .builder import PLACEHOLDER, SiteSpec, build_site
from .critic import Critique, banned_terms, critique
from .lessons import Lessons

#: Note visée. Au-delà, on arrête : chercher 100 sur un gabarit revient à
#: fabriquer des critères complaisants.
TARGET = 90

#: Nombre maximal de corrections. La boucle doit savoir s'arrêter.
MAX_ITERATIONS = 4

_EMOJI = re.compile("[\U0001f300-\U0001faff☀-➿⬀-⯿️]")
_URL = re.compile(r"(?:https?:)?//\S+")


@dataclass
class SiteVersion:
    """Un état du site et sa note."""

    number: int
    spec: SiteSpec
    files: dict[str, str]
    critique: Critique
    origin: str = ""
    applied: list[str] = field(default_factory=list)
    kept: bool = True

    @property
    def score(self) -> int:
        return self.critique.score

    def to_dict(self) -> dict:
        return {
            "version": self.number, "score": self.score, "origin": self.origin,
            "applied": self.applied, "kept": self.kept,
            "defects": self.critique.defects,
            "blocking": self.critique.blocking,
        }


@dataclass
class SiteResult:
    """Sortie complète de la boucle."""

    spec: SiteSpec
    versions: list[SiteVersion] = field(default_factory=list)
    final: SiteVersion | None = None
    stopped_because: str = ""
    prevented: list[str] = field(default_factory=list)
    learned: list[str] = field(default_factory=list)
    unfixable: list[str] = field(default_factory=list)

    @property
    def files(self) -> dict[str, str]:
        return self.final.files if self.final else {}

    @property
    def score(self) -> int:
        return self.final.score if self.final else 0

    def to_dict(self) -> dict:
        return {
            "site": self.spec.to_dict(),
            "versions": [v.to_dict() for v in self.versions],
            "final": self.final.to_dict() if self.final else None,
            "stopped_because": self.stopped_because,
            "prevented": self.prevented,
            "learned": self.learned,
            "unfixable": self.unfixable,
        }

    def report(self) -> str:
        lignes = [f"## Site — {self.spec.title}", ""]
        if self.prevented:
            lignes += [
                "**Défauts évités d'avance** (mémoire des tâches précédentes) :", "",
            ] + [f"- {item}" for item in self.prevented] + [""]

        lignes += ["### Versions", ""]
        for version in self.versions:
            verdict = (
                "conservée" if version.kept
                else "**annulée — version précédente meilleure**"
            )
            lignes.append(f"- V{version.number} : {version.score}/100 ({verdict})")
            for item in version.applied:
                lignes.append(f"  - {item}")

        if self.unfixable:
            lignes += ["", "### Défauts non corrigeables mécaniquement", ""]
            lignes += [f"- {item}" for item in self.unfixable]

        if self.learned:
            lignes += ["", "### Retenu pour la prochaine fois", ""]
            lignes += [f"- {item}" for item in self.learned]

        if self.final:
            lignes += ["", "### Version livrée", "", self.final.critique.report()]
        lignes += ["", f"*Arrêt : {self.stopped_because}*"]
        return "\n".join(lignes)


# --- Corrections mécaniques -----------------------------------------------------
#
# Chaque fonction reçoit la spec, la modifie sur place, et rend une phrase
# décrivant ce qu'elle a fait — ou `None` si elle n'avait rien à faire. Ce
# `None` est important : il dit au studio que ce défaut-là ne se corrige pas
# tout seul, ce qui vaut mieux qu'une boucle qui tourne à vide.


def _lisible(fond: str, candidats: tuple[str, ...]) -> str | None:
    for couleur in candidats:
        try:
            if colors.contrast(couleur, fond) >= colors.WCAG_AA_NORMAL:
                return couleur
        except ValueError:
            continue
    return None


def _fix_contraste(spec: SiteSpec) -> str | None:
    """Éclaircit ou assombrit jusqu'à repasser au-dessus de 4,5:1."""
    faits: list[str] = []

    # 1. le texte, sur le fond et sur les surfaces
    for arriere_nom in ("background", "surface"):
        arriere = getattr(spec, arriere_nom)
        try:
            if colors.contrast(spec.text, arriere) >= colors.WCAG_AA_NORMAL:
                continue
        except ValueError:
            pass
        candidats = tuple(
            colors.lighten(spec.text, part) for part in (0.2, 0.4, 0.6, 0.8)
        ) + tuple(colors.darken(spec.text, part) for part in (0.2, 0.4, 0.6, 0.8)) + (
            "#ffffff", "#0b1220",
        )
        choisi = _lisible(arriere, candidats)
        if choisi and choisi != spec.text:
            faits.append(f"couleur de texte portée à {choisi} sur {arriere_nom}")
            spec.text = choisi

    # 2. l'accent, qui porte l'accroche et le bouton
    try:
        insuffisant = colors.contrast(spec.accent, spec.background) < colors.WCAG_AA_NORMAL
    except ValueError:
        insuffisant = True
    if insuffisant:
        # On va jusqu'au blanc et au presque-noir : une marque terne peut
        # n'avoir aucune nuance intermédiaire lisible sur son propre fond.
        candidats = tuple(
            colors.lighten(spec.accent, part)
            for part in (0.2, 0.35, 0.5, 0.65, 0.8, 0.92)
        ) + tuple(
            colors.darken(spec.accent, part) for part in (0.2, 0.35, 0.5, 0.7, 0.9)
        ) + ("#ffffff", "#0b1220")
        choisi = _lisible(spec.background, candidats)
        if choisi:
            faits.append(f"accent ajusté à {choisi} pour atteindre 4,5:1")
            spec.accent = choisi

    # 3. la surface, si elle se confond avec le fond au point d'effacer le texte
    if not faits:
        return None
    return " ; ".join(faits)


def _fix_contenu(spec: SiteSpec) -> str | None:
    """Remplace le bouche-trou par de la matière réelle — ou retire la section.

    Rien n'est inventé. Si la demande et la recherche n'ont rien fourni pour
    une section, la section disparaît. Un site plus court et vrai vaut mieux
    qu'un site complet et faux : c'est la même règle que « CONTEXT_UNKNOWN ne
    devient pas une affirmation ».
    """
    reste = [
        phrase for phrase in spec.material
        if phrase and not any(phrase in s.body for s in spec.sections)
    ]
    remplies, retirees = [], []
    a_retirer = []

    for section in spec.sections:
        if PLACEHOLDER not in section.body and section.body.strip():
            continue
        if reste:
            section.body = reste.pop(0)
            remplies.append(section.title)
        else:
            a_retirer.append(section)

    # On garde toujours au moins une section, et c'est la **première** :
    # supprimer l'accueil pour ne laisser que « Contact » donnerait un site
    # techniquement propre et parfaitement inutile.
    survivantes = [s for s in spec.sections if s not in a_retirer]
    if not survivantes and a_retirer:
        garde = a_retirer.pop(0)
        garde.body = spec.tagline or spec.title
        remplies.append(garde.title)
    for section in a_retirer:
        spec.sections.remove(section)
        retirees.append(section.title)

    if not remplies and not retirees:
        return None

    # Les liens qui pointaient vers une section supprimée doivent suivre.
    _fix_liens(spec)

    morceaux = []
    if remplies:
        morceaux.append("sections remplies avec la matière disponible : " + ", ".join(remplies))
    if retirees:
        morceaux.append(
            "sections retirées faute de contenu fourni (rien n'a été inventé) : "
            + ", ".join(retirees)
        )
    return " ; ".join(morceaux)


def _fix_liens(spec: SiteSpec) -> str | None:
    ancres = {section.anchor for section in spec.sections}
    corriges = []
    for section in spec.sections:
        cible = section.cta_href
        if not section.cta:
            continue
        if not cible or (cible.startswith("#") and cible[1:] not in ancres):
            section.cta_href = f"#{spec.sections[-1].anchor}"
            corriges.append(section.title)
    return ("liens d'action redirigés : " + ", ".join(corriges)) if corriges else None


def _fix_titre(spec: SiteSpec) -> str | None:
    faits = []
    if not spec.title.strip():
        spec.title = spec.tagline.split(".")[0][:60].strip() or "Site"
        faits.append("titre reconstruit depuis l'accroche")
    if not spec.lang.strip():
        spec.lang = "fr"
        faits.append("langue déclarée (fr)")
    if not spec.tagline.strip():
        spec.tagline = spec.title
        faits.append("description reprise du titre")
    return " ; ".join(faits) if faits else None


def _fix_interdits(spec: SiteSpec) -> str | None:
    """Applique les interdits de la marque au texte du site."""
    interdits = " ".join(spec.forbidden).lower()
    faits = []

    if "emoji" in interdits:
        def sans_emoji(texte: str) -> str:
            return re.sub(r"\s{2,}", " ", _EMOJI.sub("", texte)).strip()

        avant = spec.tagline + "".join(s.body for s in spec.sections)
        spec.tagline = sans_emoji(spec.tagline)
        spec.title = sans_emoji(spec.title)
        for section in spec.sections:
            section.body = sans_emoji(section.body)
            section.bullets = [sans_emoji(b) for b in section.bullets]
        apres = spec.tagline + "".join(s.body for s in spec.sections)
        if avant != apres:
            faits.append("emojis retirés (interdits par la marque)")

    # Seuls les termes explicitement cités par la marque sont retirés — pas les
    # noms propres devinés dans la règle (voir `critic.banned_terms`).
    for regle in spec.forbidden:
        for terme in banned_terms(regle):
            motif = re.compile(rf"[^.!?]*\b{re.escape(terme)}\b[^.!?]*[.!?]?", re.I)
            touche = False
            for section in spec.sections:
                nouveau = motif.sub("", section.body).strip()
                if nouveau != section.body:
                    section.body = nouveau or spec.tagline
                    touche = True
            nettoyee = motif.sub("", spec.tagline).strip()
            if nettoyee != spec.tagline:
                spec.tagline, touche = nettoyee or spec.title, True
            if touche:
                faits.append(f"mention « {terme} » retirée : {regle}")

    return " ; ".join(faits) if faits else None


def _fix_externe(spec: SiteSpec) -> str | None:
    """Retire du texte tout ce qui ferait charger une ressource distante."""
    faits = 0
    for section in spec.sections:
        nouveau = _URL.sub("", section.body).strip()
        if nouveau != section.body:
            section.body, faits = nouveau, faits + 1
        section.bullets = [_URL.sub("", b).strip() for b in section.bullets]
        if section.cta_href and "//" in section.cta_href:
            section.cta_href = f"#{spec.sections[-1].anchor}"
            faits += 1
    nettoyee = _URL.sub("", spec.tagline).strip()
    if nettoyee != spec.tagline:
        spec.tagline, faits = nettoyee, faits + 1
    return f"{faits} référence(s) distante(s) retirée(s)" if faits else None


def _fix_poids(spec: SiteSpec) -> str | None:
    trop_longues = [s for s in spec.sections if len(s.body) > 1200]
    if not trop_longues:
        return None
    for section in trop_longues:
        section.body = section.body[:1200].rsplit(" ", 1)[0] + "…"
    return f"{len(trop_longues)} section(s) raccourcie(s)"


def _fix_installable(spec: SiteSpec) -> str | None:
    if not spec.installable:
        return None
    if spec.title.strip():
        return None
    spec.title = spec.tagline[:40] or "Application"
    return "nom d'application rétabli dans le manifeste"


#: code de défaut → correction. Un défaut absent de cette table est signalé
#: mais non corrigé : mieux vaut le dire que faire semblant.
FIXES = {
    "contraste_insuffisant": _fix_contraste,
    "texte_bouche_trou": _fix_contenu,
    "lien_mort": _fix_liens,
    "titre_manquant": _fix_titre,
    "interdit_de_marque": _fix_interdits,
    "ressource_externe": _fix_externe,
    "poids_excessif": _fix_poids,
    "manifeste_invalide": _fix_installable,
}


class SiteStudio:
    """Construit un site, le critique, le corrige — et retient ce qu'il apprend."""

    def __init__(
        self,
        lessons: Lessons | None = None,
        *,
        target: int = TARGET,
        max_iterations: int = MAX_ITERATIONS,
        learn: bool = True,
    ) -> None:
        self.lessons = lessons if lessons is not None else Lessons()
        self.target = target
        self.max_iterations = max_iterations
        self.learn = learn

    # -- mémoire -----------------------------------------------------------

    def _preflight(self, spec: SiteSpec) -> list[str]:
        """Applique d'avance les corrections dont l'effet est déjà établi."""
        appliquees: list[str] = []
        for code in self.lessons.preventive():
            correction = FIXES.get(code)
            if correction is None:
                continue
            fait = correction(spec)
            if fait:
                self.lessons.record_prevention(code)
                appliquees.append(f"{fait} — appris d'une tâche précédente")
        return appliquees

    # -- boucle ------------------------------------------------------------

    def run(self, spec: SiteSpec, *, task: str = "") -> SiteResult:
        spec = copy.deepcopy(spec)
        resultat = SiteResult(spec=spec)
        resultat.prevented = self._preflight(spec)

        version = self._build(spec, 1, origin="première version")
        resultat.versions.append(version)
        meilleur = version

        # Ce que produit la **première** version est ce que la mémoire doit
        # retenir : après correction, le défaut n'est plus représentatif.
        for code in version.critique.defects:
            self.lessons.record_defect(code, task=task, example=spec.title)

        epuises: set[str] = set()
        numero = 1
        # Un défaut bloquant se corrige **même si la note visée est atteinte** :
        # un site à 95/100 qui charge une police distante ne s'ouvre pas hors
        # ligne, et la note n'y change rien.
        while (
            meilleur.score < self.target or meilleur.critique.blocking
        ) and numero <= self.max_iterations:
            cible = self._next_defect(meilleur.critique, epuises)
            if cible is None:
                resultat.stopped_because = (
                    "plus aucun défaut corrigeable mécaniquement"
                    if meilleur.score < self.target or meilleur.critique.blocking
                    else "note visée atteinte"
                )
                break

            candidate = copy.deepcopy(meilleur.spec)
            fait = FIXES[cible](candidate)
            if not fait:
                epuises.add(cible)
                resultat.unfixable.append(
                    f"{cible} : aucune correction mécanique applicable"
                )
                continue

            numero += 1
            essai = self._build(candidate, numero, origin=f"correction de {cible}")
            essai.applied = [fait]
            resultat.versions.append(essai)

            if essai.score > meilleur.score:
                if self.learn:
                    self.lessons.record_fix(cible, worked=True)
                    resultat.learned.append(
                        f"{cible} : correction efficace "
                        f"({meilleur.score} → {essai.score}) — sera appliquée d'avance"
                    )
                meilleur = essai
                epuises.add(cible)
            else:
                essai.kept = False
                if self.learn:
                    self.lessons.record_fix(cible, worked=False)
                resultat.stopped_because = (
                    f"version précédente meilleure ({meilleur.score} ≥ {essai.score}) — "
                    f"correction de {cible} annulée"
                )
                break

        if not resultat.stopped_because:
            resultat.stopped_because = (
                "note visée atteinte"
                if meilleur.score >= self.target and not meilleur.critique.blocking
                else f"limite de {self.max_iterations} correction(s) atteinte"
            )
        if meilleur.critique.blocking:
            resultat.unfixable += [
                f"défaut bloquant persistant : {item}"
                for item in meilleur.critique.blocking
            ]

        resultat.final = meilleur
        resultat.spec = meilleur.spec
        if self.learn and self.lessons.path is not None:
            self.lessons.save()
        return resultat

    @staticmethod
    def _next_defect(verdict: Critique, epuises: set[str]) -> str | None:
        """Le défaut le plus coûteux qui sache encore être corrigé."""
        for critere in verdict.worst():
            if critere.defect in FIXES and critere.defect not in epuises:
                return critere.defect
        return None

    @staticmethod
    def _build(spec: SiteSpec, number: int, *, origin: str) -> SiteVersion:
        fichiers = build_site(spec)
        return SiteVersion(
            number=number, spec=spec, files=fichiers,
            critique=critique(fichiers, forbidden=spec.forbidden),
            origin=origin,
        )


__all__ = [
    "FIXES", "MAX_ITERATIONS", "SiteResult", "SiteStudio", "SiteVersion", "TARGET",
]
