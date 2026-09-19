#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Carte du parcours — TOUR DE MORONI, cross inclusif de 10 km.

Fabrique `carte-tour-de-moroni.svg` (format A3 paysage, imprimable) à partir de
trois fichiers de données qui vivent dans `donnees/` :

  routes_moroni.json    le réseau routier de Moroni (OpenStreetMap, © contributeurs)
  contexte_moroni.json  le trait de côte et les repères (quartiers, mairie, marchés…)
  parcours_calcule.json le parcours retenu, ses bornes kilométriques et ses postes

Ces trois fichiers sont produits par `extraire_osm.py` (à relancer seulement si
le parcours change ou si l'on veut rafraîchir les données OSM).

    python3 carte.py            # écrit carte-tour-de-moroni.svg

Pas de dépendance : bibliothèque standard uniquement. Le SVG s'ouvre dans
n'importe quel navigateur et s'imprime en A3 (ou en A0 pour le panneau du
village départ : le format vectoriel ne perd rien à l'agrandissement).
"""

import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, "donnees")
SORTIE = os.path.join(ICI, "carte-tour-de-moroni.svg")

# --- Format et couleurs ------------------------------------------------------
W, H = 1680, 1188                      # A3 paysage (ratio 1,414)
MARGE = 28

MER = "#CBE0EC"
TERRE = "#F8F5EF"
ROUTE_BORD = "#E2DCD0"
ROUTE = "#FFFFFF"
TRAIT = "#3A3632"
GRIS = "#8C857B"
SUD = "#D9481F"                        # boucle sud
NORD = "#14607F"                       # boucle nord
EAU = "#1F86C8"                        # ravitaillements
SECOURS = "#C62828"
STAND = "#2E7D32"
PMR = "#6A3FA0"

POLICE = "'Helvetica Neue', Helvetica, Arial, sans-serif"


def charger():
    with open(os.path.join(DONNEES, "routes_moroni.json"), encoding="utf-8") as f:
        routes = json.load(f)
    with open(os.path.join(DONNEES, "contexte_moroni.json"), encoding="utf-8") as f:
        ctx = json.load(f)
    with open(os.path.join(DONNEES, "parcours_calcule.json"), encoding="utf-8") as f:
        parcours = json.load(f)
    return routes, ctx, parcours


# --- Projection --------------------------------------------------------------
class Projection:
    """Équirectangulaire centrée sur Moroni : à cette latitude l'erreur est nulle
    à l'échelle d'une ville, et la carte reste lisible à la règle."""

    def __init__(self, bbox, larg, haut, ox, oy):
        latmin, latmax, lonmin, lonmax = bbox
        self.lat0 = (latmin + latmax) / 2
        self.k = math.cos(math.radians(self.lat0))
        x0, x1 = lonmin * self.k, lonmax * self.k
        y0, y1 = latmin, latmax
        sx = larg / (x1 - x0)
        sy = haut / (y1 - y0)
        self.s = min(sx, sy)
        self.ox = ox + (larg - (x1 - x0) * self.s) / 2
        self.oy = oy + (haut - (y1 - y0) * self.s) / 2
        self.x0, self.y1 = x0, y1
        self.haut = (y1 - y0) * self.s

    def __call__(self, lat, lon):
        return (self.ox + (lon * self.k - self.x0) * self.s,
                self.oy + (self.y1 - lat) * self.s)

    def metres(self, m):
        """Longueur en pixels d'une distance donnée en mètres."""
        return m / 111320.0 * self.s


def bbox_parcours(parcours, marge=0.0030):
    """Cadre du parcours, élargi jusqu'au format de la feuille pour que la
    carte remplisse la page au lieu de flotter au milieu."""
    lats = [c[1] for c in parcours["sud"] + parcours["nord"]]
    lons = [c[0] for c in parcours["sud"] + parcours["nord"]]
    latmin, latmax = min(lats) - marge, max(lats) + marge
    lonmin, lonmax = min(lons) - marge, max(lons) + marge
    k = math.cos(math.radians((latmin + latmax) / 2))
    ratio = (W - 2 * MARGE) / (H - 2 * MARGE)
    dlat = latmax - latmin
    dlon_voulu = dlat * ratio / k
    manque = dlon_voulu - (lonmax - lonmin)
    if manque > 0:                      # on ouvre vers l'ouest (la mer) et l'est
        lonmin -= manque * 0.45
        lonmax += manque * 0.55
    return (latmin, latmax, lonmin, lonmax)


def esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def poly(points, **attrs):
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    a = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    return f'<polyline points="{d}" {a}/>'


def texte(x, y, t, taille=13, couleur=TRAIT, ancre="start", poids="400",
          espace="0", halo=None):
    """Un texte. `halo` pose un liseré de la couleur du fond : une étiquette
    posée sur une rue reste lisible sans masquer la rue."""
    h = (f'paint-order="stroke" stroke="{halo}" stroke-width="3.2" '
         f'stroke-linejoin="round"') if halo else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{POLICE}" '
            f'font-size="{taille}" fill="{couleur}" text-anchor="{ancre}" '
            f'font-weight="{poids}" letter-spacing="{espace}" {h}>{esc(t)}</text>')


# --- Fond de carte -----------------------------------------------------------
LARGEURS = {                     # (casing, remplissage)
    "primary": (9.0, 6.0),
    "secondary": (7.5, 5.0),
    "tertiary": (6.0, 3.8),
    "unclassified": (4.2, 2.6),
    "residential": (4.2, 2.6),
    "living_street": (3.4, 2.0),
    "pedestrian": (3.0, 1.8),
}


def dessiner_fond(p, routes, ctx, bbox):
    out = []
    latmin, latmax, lonmin, lonmax = bbox
    x1 = W
    out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{MER}"/>')

    # La terre : le trait de côte OSM est orienté « terre à gauche ». On ferme
    # chaque tronçon sur le bord est du cadre pour obtenir une surface.
    for ligne in ctx["coast"]:
        pts = [p(la, lo) for la, lo in ligne
               if latmin - 0.02 < la < latmax + 0.02]
        if len(pts) < 2:
            continue
        pts = [(x1, pts[0][1])] + pts + [(x1, pts[-1][1])]
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        out.append(f'<polygon points="{d}" fill="{TERRE}"/>')

    for couche in (0, 1):
        for r in routes:
            w = LARGEURS.get(r["h"])
            if not w:
                continue
            pts = [p(la, lo) for la, lo in r["g"]]
            out.append(poly(pts, fill="none",
                            stroke=ROUTE_BORD if couche == 0 else ROUTE,
                            stroke_width=f"{w[couche]:.1f}",
                            stroke_linecap="round", stroke_linejoin="round"))
    return out


QUARTIERS_UTILES = {
    "Magudju ماجودجو": "Magudju", "Mbuweni مبوني": "Mbuweni",
    "Irungudjani إيرونجودجاني": "Irungudjani", "Kaltex كالتكس": "Caltex",
    "Djivani جيفاني": "Djivani", "Zilimadju زيليمادجو": "Zilimadju",
    "Hamramba هامرامبا": "Hamramba", "Djomani جوماني": "Djomani",
    "Ribatwi رباطوي": "Ribatwi", "Mangani مانقاني": "Mangani",
    "Hankunu هانكونو": "Hankunu", "Hadudja هادوجا": "Hadudja",
    "Oasis الواحة": "Oasis", "Coulee de Lave تدفق الحمم": "Coulée de lave",
    "Porini بوريني": "Porini", "Basha باشا": "Basha",
    "Buzini بوزيني": "Buzini", "Mdjivurize مدجيفوريز": "Mdjivurize",
    "Mtsizambe متسيزامبي": "Mtsizambe",
}

REPERES_MANUELS = [          # ce que l'OSM ne nomme pas et qui compte pour la course
    ("Palais du Peuple", -11.71812, 43.24632, 8, 4),
    ("Place de l'Indépendance", -11.70146, 43.25269, 26, -22),
]

REPERES_UTILES = {
    "Hôtel de ville de Moroni": "Hôtel de ville",
    "Ancien marché de Moroni": "Ancien marché",
    "Le Grand Marché Couvert Volovolo": "Marché de Volo Volo",
    "Cour suprême المحكمة العليا": "Cour suprême",
    "Mosquée de Chadhuli": "Mosquée de Chadhuli",
    "Alliance Française Moroni": "Alliance Française",
    "Stade Omni Sport": "Stade omnisports",
    "Cour suprême المحكمة العليا": "Cour suprême",
    "Tennis Club de Moroni": "Tennis Club",
    "INJS": "INJS",
}

DECALAGES = {                # étiquettes à déplacer : elles tombaient sur un poste
    "Alliance Française": (-10, -12),
    "Marché de Volo Volo": (10, 20),
    "Tennis Club": (-8, -6),
    "Mosquée de Chadhuli": (-8, 14),
    "Hôtel de ville": (-9, -6),
}


def dessiner_reperes(p, ctx):
    out = []
    for r in ctx["reperes"]:
        nom = QUARTIERS_UTILES.get(r["n"])
        if nom:
            x, y = p(r["la"], r["lo"])
            out.append(texte(x, y, nom.upper(), 10.5, GRIS, "middle", "500", "1.4",
                             halo=TERRE))
    marques = [(REPERES_UTILES[r["n"]], r["la"], r["lo"])
               for r in ctx["reperes"] if r["n"] in REPERES_UTILES]
    for nom, la, lo, dx, dy in REPERES_MANUELS:
        marques.append((nom, la, lo))
        DECALAGES.setdefault(nom, (dx, dy))
    for nom, la, lo in marques:
        x, y = p(la, lo)
        dx, dy = DECALAGES.get(nom, (6, 3.5))
        ancre = "end" if dx < 0 else "start"
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{GRIS}"/>')
        out.append(texte(x + dx, y + dy, nom, 11, "#5E574E", ancre, "600",
                         halo="#FFFFFF"))
    return out


# --- Parcours ----------------------------------------------------------------
def fleches(p, coords, tous_les=9):
    """Chevrons de sens de course, posés régulièrement le long du tracé."""
    out = []
    for i in range(tous_les, len(coords) - 1, tous_les):
        x1, y1 = p(coords[i - 1][1], coords[i - 1][0])
        x2, y2 = p(coords[i + 1][1], coords[i + 1][0])
        a = math.degrees(math.atan2(y2 - y1, x2 - x1))
        x, y = p(coords[i][1], coords[i][0])
        out.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({a:.1f})">'
                   f'<path d="M -3.2 -3.4 L 2.6 0 L -3.2 3.4" fill="none" '
                   f'stroke="#FFFFFF" stroke-width="1.9" stroke-linecap="round" '
                   f'stroke-linejoin="round" opacity="0.95"/></g>')
    return out


def dessiner_parcours(p, parcours):
    out = []
    for coords, couleur in ((parcours["sud"], SUD), (parcours["nord"], NORD)):
        pts = [p(la, lo) for lo, la in coords]
        out.append(poly(pts, fill="none", stroke="#FFFFFF", stroke_width="13",
                        stroke_linecap="round", stroke_linejoin="round",
                        opacity="0.9"))
    for coords, couleur in ((parcours["sud"], SUD), (parcours["nord"], NORD)):
        pts = [p(la, lo) for lo, la in coords]
        out.append(poly(pts, fill="none", stroke=couleur, stroke_width="8",
                        stroke_linecap="round", stroke_linejoin="round"))
        out += fleches(p, coords)
    return out


def dessiner_bornes(p, parcours):
    out = []
    for b in parcours["km"]:
        x, y = p(b["coord"][1], b["coord"][0])
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#FFFFFF" '
                   f'stroke="{TRAIT}" stroke-width="1.6"/>')
        out.append(texte(x, y + 4, str(b["km"]), 12.5, TRAIT, "middle", "700"))
    return out


def symbole(x, y, type_, etiquette):
    """Pastille d'un poste sur le parcours + son étiquette."""
    out = []
    if type_ == "depart":
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="{TRAIT}"/>')
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="22" fill="none" '
                   f'stroke="{TRAIT}" stroke-width="2"/>')
        out.append(texte(x, y + 5, "D/A", 12.5, "#FFFFFF", "middle", "700"))
        return out
    couleurs = {"ravito": EAU, "brume": "#4FA8D8", "secours": SECOURS,
                "pmr": PMR, "stand": STAND}
    c = couleurs.get(type_, GRIS)
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="12.5" fill="{c}" '
               f'stroke="#FFFFFF" stroke-width="2.4"/>')
    out.append(texte(x, y + 4.2, etiquette, 11, "#FFFFFF", "middle", "700"))
    return out


ETIQUETTES = {
    "Ravitaillement R1 — km 2,5": ("ravito", "R1", 0, -26),
    "Ravitaillement R2 — km 5": ("ravito", "R2", 26, 0),
    "Ravitaillement R3 — km 7,5": ("ravito", "R3", 26, 0),
    "Brumisation B1 — km 3,8": ("brume", "B1", 24, 0),
    "Brumisation B2 — km 8,8": ("brume", "B2", -24, 0),
    "Poste de secours PS2 — km 2,4 (Palais du Peuple)": ("secours", "PS2", -26, 0),
    "Poste de secours PS3 — km 7,6 (Alliance Française)": ("secours", "PS3", 0, -26),
    "Relais PMR / joëlettes — km 5,0": ("pmr", "PMR", 0, 26),
}


def dessiner_postes(p, parcours):
    out = []
    for pt in parcours["points"]:
        x, y = p(pt["coord"][1], pt["coord"][0])
        if pt["type"] == "depart":
            out += symbole(x, y, "depart", "")
            continue
        info = ETIQUETTES.get(pt["nom"])
        if not info:
            continue
        _, et, dx, dy = info
        out += symbole(x + dx, y + dy, pt["type"], et)
    return out


# --- Habillage ---------------------------------------------------------------
def cartouche(x, y):
    out = [f'<rect x="{x}" y="{y}" width="452" height="146" rx="6" '
           f'fill="#FFFFFF" opacity="0.93"/>']
    out.append(texte(x + 22, y + 46, "TOUR DE MORONI", 36, TRAIT, "start", "800", "1"))
    out.append(texte(x + 22, y + 74, "Cross inclusif de 10 km — départ et arrivée "
                     "place de l'Indépendance", 14, "#5E574E"))
    out.append(texte(x + 22, y + 100, "1re édition : dimanche 6 décembre 2026, "
                     "6 h 30", 14.5, SUD, "start", "700"))
    out.append(texte(x + 22, y + 124, "Puis chaque année le 1er dimanche de "
                     "décembre", 12.5, GRIS))
    return out


def legende(x, y):
    lignes = [
        (SUD, "Boucle Sud — km 0 à 6,0 (front de mer, Itsambuni, Palais du Peuple, Karthala)"),
        (NORD, "Boucle Nord — km 6,0 à 10,0 (Hankunu, Union Africaine, Corniche)"),
        (EAU, "Ravitaillement : eau, jus locaux, fruits (R1 km 2,5 · R2 km 5 · R3 km 7,5)"),
        ("#4FA8D8", "Point de brumisation (B1 km 3,8 · B2 km 8,8)"),
        (SECOURS, "Poste de secours (PS1 au village, PS2 km 2,4, PS3 km 7,6)"),
        (PMR, "Relais PMR / joëlettes — relève des équipes d'accompagnement"),
        (TRAIT, "Village du Tour : départ, arrivée, stands, podium, PS1"),
    ]
    out = [f'<rect x="{x}" y="{y}" width="452" height="{30 + 26 * len(lignes)}" '
           f'rx="6" fill="#FFFFFF" opacity="0.93"/>']
    out.append(texte(x + 22, y + 26, "LÉGENDE", 12, GRIS, "start", "700", "1.6"))
    for i, (c, t) in enumerate(lignes):
        yy = y + 50 + 26 * i
        out.append(f'<circle cx="{x + 29}" cy="{yy - 4}" r="7" fill="{c}"/>')
        out.append(texte(x + 45, yy, t, 12, "#4A443C"))
    return out


def echelle(p, x, y):
    px = p.metres(1000)
    out = [f'<rect x="{x}" y="{y - 16}" width="{px:.0f}" height="6" fill="{TRAIT}"/>',
           f'<rect x="{x + px / 2:.0f}" y="{y - 16}" width="{px / 2:.0f}" height="6" fill="#FFFFFF" '
           f'stroke="{TRAIT}" stroke-width="1"/>',
           texte(x, y + 12, "0", 11, TRAIT, "middle"),
           texte(x + px, y + 12, "1 km", 11, TRAIT, "middle")]
    return out


def rose_des_vents(x, y):
    return [f'<g transform="translate({x},{y})">'
            f'<path d="M 0 -26 L 7 6 L 0 1 L -7 6 Z" fill="{TRAIT}"/>'
            f'<text x="0" y="24" font-family="{POLICE}" font-size="13" '
            f'font-weight="700" fill="{TRAIT}" text-anchor="middle">N</text></g>']


def profil(x, y, larg, haut, parcours):
    """Profil altimétrique (SRTM 30 m) — 10 km, 145 m de dénivelé positif."""
    cum, elev = parcours["cum"], parcours["elev"]
    pts = [(x + larg * c / cum[-1], y + haut - haut * (e - 0) / 60.0)
           for c, e in zip(cum, elev) if e is not None]
    out = [f'<rect x="{x - 16}" y="{y - 40}" width="{larg + 32}" height="{haut + 74}" '
           f'rx="6" fill="#FFFFFF" opacity="0.93"/>']
    out.append(texte(x - 2, y - 18, "PROFIL — 10 km, D+ 145 m, altitude 5 à 38 m",
                     12, GRIS, "start", "700", "1.2"))
    d = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    out.append(f'<polygon points="{x:.1f},{y + haut:.1f} {d} {x + larg:.1f},{y + haut:.1f}" '
               f'fill="{SUD}" opacity="0.16"/>')
    out.append(poly(pts, fill="none", stroke=SUD, stroke_width="2.2",
                    stroke_linejoin="round"))
    for k in range(0, 11, 2):
        px = x + larg * k / 10.0
        out.append(f'<line x1="{px:.1f}" y1="{y + haut:.1f}" x2="{px:.1f}" '
                   f'y2="{y + haut + 5:.1f}" stroke="{GRIS}" stroke-width="1"/>')
        out.append(texte(px, y + haut + 18, f"{k}", 10.5, GRIS, "middle"))
    out.append(texte(x + larg, y + haut + 18, "km", 10.5, GRIS, "start"))
    return out


def main():
    routes, ctx, parcours = charger()
    bbox = bbox_parcours(parcours)
    p = Projection(bbox, W - 2 * MARGE, H - 2 * MARGE, MARGE, MARGE)

    s = [f'<?xml version="1.0" encoding="UTF-8"?>',
         f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" '
         f'viewBox="0 0 {W} {H}">',
         f'<rect width="{W}" height="{H}" fill="{TERRE}"/>']
    s += dessiner_fond(p, routes, ctx, bbox)
    s += dessiner_reperes(p, ctx)
    s += dessiner_parcours(p, parcours)
    s += dessiner_bornes(p, parcours)
    s += dessiner_postes(p, parcours)
    s += cartouche(MARGE + 14, MARGE + 14)
    s += legende(MARGE + 14, H - MARGE - 232)
    s += echelle(p, W - MARGE - 330, H - MARGE - 46)
    s += rose_des_vents(W - MARGE - 60, MARGE + 60)
    s += profil(W - MARGE - 470, MARGE + 130, 420, 96, parcours)
    s.append(texte(MARGE + 14, H - MARGE - 8,
                   "Fond de carte : OpenStreetMap (ODbL) · altitudes SRTM 30 m · "
                   "parcours mesuré sur le réseau réel, à confirmer à la roue avant homologation",
                   11, GRIS))
    s.append("</svg>")

    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write("\n".join(s))
    print(f"écrit : {SORTIE}")


if __name__ == "__main__":
    main()
