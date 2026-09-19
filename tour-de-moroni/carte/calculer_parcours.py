#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calcul du parcours — TOUR DE MORONI, 10 km, départ place de l'Indépendance.

Le parcours n'est pas dessiné à la main : il est calculé sur le vrai réseau de
rues de Moroni (OpenStreetMap), avec un coût qui pénalise trois choses, dans cet
ordre : la pente (une course inclusive se juge à ses montées), les petites rues
(on veut des axes larges, fermables et éclairés), et la longueur.

Forme retenue : un **huit** autour de la place de l'Indépendance.
  · Boucle Sud  (6,03 km) — front de mer, Itsambuni, Palais du Peuple, Karthala
  · Boucle Nord (3,97 km) — Hankunu, Union Africaine, Corniche
Les deux boucles se referment sur la place : un seul village, un seul poste de
commandement, et le public voit les coureurs trois fois.

    python3 calculer_parcours.py      # écrit parcours.geojson + donnees/*.json

Entrées : donnees/routes_moroni.json et donnees/altitudes.json (voir
extraire_osm.py). Aucune dépendance extérieure.
"""

import heapq
import json
import math
import os

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, "donnees")

# Les trois points qui fixent la forme du huit (relevés sur le terrain OSM).
DEPART = (-11.70146, 43.25269)          # place de l'Indépendance
PIVOT_SUD = (-11.71925, 43.24565)       # Palais du Peuple / entrée de Hamramba
PIVOT_NORD = (-11.68866, 43.25524)      # Oasis / Alliance Française

# Coût : un mètre de rue vaut ce facteur, un mètre de montée vaut 18 m de plat,
# et au-delà de 5 % de pente la note explose (limite d'un fauteuil accompagné).
FACTEUR = {"primary": 1.0, "secondary": 1.05, "tertiary": 1.3,
           "unclassified": 2.0, "residential": 2.0, "living_street": 2.4,
           "pedestrian": 2.6}
COUT_MONTEE = 18.0
PENTE_MAX = 0.05

# Postes du dispositif, posés à un kilométrage donné du parcours.
POSTES = [
    ("Ravitaillement R1 — km 2,5", "ravito", 2500),
    ("Ravitaillement R2 — km 5", "ravito", 5000),
    ("Ravitaillement R3 — km 7,5", "ravito", 7500),
    ("Brumisation B1 — km 3,8", "brume", 3800),
    ("Brumisation B2 — km 8,8", "brume", 8800),
    ("Poste de secours PS2 — km 2,4 (Palais du Peuple)", "secours", 2400),
    ("Poste de secours PS3 — km 7,6 (Alliance Française)", "secours", 7600),
    ("Relais PMR / joëlettes — km 5,0", "pmr", 5000),
]


def distance(a, b):
    """Distance en mètres entre deux couples (lat, lon)."""
    r = 6371000.0
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    return 2 * r * math.asin(math.sqrt(
        math.sin((la2 - la1) / 2) ** 2
        + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))


class Reseau:
    """Le réseau de rues, sommets repérés par leurs coordonnées arrondies."""

    def __init__(self):
        with open(os.path.join(DONNEES, "routes_moroni.json"), encoding="utf-8") as f:
            routes = json.load(f)
        with open(os.path.join(DONNEES, "altitudes.json"), encoding="utf-8") as f:
            self.alt = json.load(f)
        self.voisins = {}
        for r in routes:
            if r["h"] not in FACTEUR:
                continue
            pts = [tuple(p) for p in r["g"]]
            for a, b in zip(pts, pts[1:]):
                d = distance(a, b)
                nom = r["n"] or f"voie sans nom ({r['h']})"
                self.voisins.setdefault(a, []).append((b, d, nom, r["h"]))
                self.voisins.setdefault(b, []).append((a, d, nom, r["h"]))

    def altitude(self, p):
        return self.alt.get(f"{p[0]:.5f},{p[1]:.5f}")

    def plus_proche(self, lat, lon):
        return min(self.voisins, key=lambda p: distance(p, (lat, lon)))

    def chemin(self, depart, arrivee, interdits=frozenset()):
        """Dijkstra sur le coût « plat, large, court », arêtes interdites exclues."""
        cout = {depart: 0.0}
        precedent = {}
        file = [(0.0, depart)]
        while file:
            c, u = heapq.heappop(file)
            if c > cout.get(u, math.inf):
                continue
            if u == arrivee:
                break
            zu = self.altitude(u)
            for v, d, _, cat in self.voisins[u]:
                if (min(u, v), max(u, v)) in interdits:
                    continue
                zv = self.altitude(v)
                if zu is None or zv is None:
                    continue
                dz = zv - zu
                pente = abs(dz) / max(d, 1.0)
                penalite = COUT_MONTEE * max(dz, 0.0)
                if pente > PENTE_MAX:
                    penalite += 400 * d * (pente - PENTE_MAX)
                nouveau = c + d * FACTEUR[cat] + penalite
                if nouveau < cout.get(v, math.inf):
                    cout[v] = nouveau
                    precedent[v] = u
                    heapq.heappush(file, (nouveau, v))
        if arrivee not in precedent and arrivee != depart:
            raise SystemExit("Pas de chemin — les données de rues sont-elles à jour ?")
        chemin = [arrivee]
        while chemin[-1] != depart:
            chemin.append(precedent[chemin[-1]])
        return chemin[::-1]

    def boucle(self, depart, pivot):
        """Aller par le plus court/plat, retour par un autre chemin : une vraie boucle."""
        aller = self.chemin(depart, pivot)
        interdits = frozenset((min(a, b), max(a, b)) for a, b in zip(aller, aller[1:]))
        retour = self.chemin(pivot, depart, interdits)
        return aller + retour[1:]


def longueur(pts):
    return sum(distance(a, b) for a, b in zip(pts, pts[1:]))


def cumul(pts):
    c = [0.0]
    for a, b in zip(pts, pts[1:]):
        c.append(c[-1] + distance(a, b))
    return c


def point_au_km(pts, cum, metres):
    for i in range(len(cum) - 1):
        if cum[i] <= metres <= cum[i + 1]:
            t = (metres - cum[i]) / max(cum[i + 1] - cum[i], 1e-9)
            return [round(pts[i][1] + t * (pts[i + 1][1] - pts[i][1]), 6),
                    round(pts[i][0] + t * (pts[i + 1][0] - pts[i][0]), 6)]
    return [round(pts[-1][1], 6), round(pts[-1][0], 6)]


def feuille_de_route(reseau, pts):
    """Le road-book : rue par rue, avec le kilométrage d'entrée."""
    lignes = []
    courante, acc, depuis, total = None, 0.0, 0.0, 0.0
    for a, b in zip(pts, pts[1:]):
        nom = next((n for v, d, n, c in reseau.voisins[a] if v == b), "?")
        if nom != courante:
            if courante is not None:
                lignes.append({"rue": courante, "m": round(acc),
                               "depuis_km": round(depuis / 1000, 2)})
            courante, acc, depuis = nom, 0.0, total
        d = distance(a, b)
        acc += d
        total += d
    lignes.append({"rue": courante, "m": round(acc), "depuis_km": round(depuis / 1000, 2)})
    return [l for l in lignes if l["m"] >= 50]


def points_de_blocage(reseau, pts, cum):
    """Chaque rue qui débouche sur le parcours est un point à tenir le jour J.
    On les liste avec leur kilométrage : c'est la base du plan de fermeture."""
    sur = set(pts)
    lignes, dernier = [], -999.0
    for p, d in zip(pts, cum):
        laterales = [(v, n) for v, _, n, _ in reseau.voisins[p] if v not in sur]
        if not laterales or d - dernier < 80:
            continue
        noms = sorted({n for _, n in laterales if not n.startswith("voie sans nom")})
        lignes.append({"km": round(d / 1000, 2), "lat": p[0], "lon": p[1],
                       "voies": len(laterales), "debouche_sur": " / ".join(noms)})
        dernier = d
    return lignes


def denivele(reseau, pts):
    monte = descend = 0.0
    alts = [reseau.altitude(p) for p in pts]
    for a, b in zip(alts, alts[1:]):
        if a is None or b is None:
            continue
        monte += max(b - a, 0.0)
        descend += max(a - b, 0.0)
    return monte, descend, [a for a in alts if a is not None]


def main():
    reseau = Reseau()
    depart = reseau.plus_proche(*DEPART)
    sud = reseau.boucle(depart, reseau.plus_proche(*PIVOT_SUD))
    nord = reseau.boucle(depart, reseau.plus_proche(*PIVOT_NORD))
    complet = sud + nord[1:]
    cum = cumul(complet)
    monte, descend, alts = denivele(reseau, complet)

    print(f"Boucle Sud  : {longueur(sud) / 1000:5.2f} km")
    print(f"Boucle Nord : {longueur(nord) / 1000:5.2f} km")
    print(f"TOTAL       : {cum[-1] / 1000:5.2f} km — D+ {monte:.0f} m, "
          f"altitude {min(alts):.0f} à {max(alts):.0f} m")

    bornes = [{"km": k, "coord": point_au_km(complet, cum, k * 1000)}
              for k in range(1, 10)]
    postes = [{"nom": "Départ / Arrivée — Place de l'Indépendance", "type": "depart",
               "coord": [round(complet[0][1], 6), round(complet[0][0], 6)]}]
    postes += [{"nom": n, "type": t, "coord": point_au_km(complet, cum, m)}
               for n, t, m in POSTES]

    coords = lambda pts: [[round(p[1], 6), round(p[0], 6)] for p in pts]
    with open(os.path.join(DONNEES, "parcours_calcule.json"), "w", encoding="utf-8") as f:
        json.dump({"sud": coords(sud), "nord": coords(nord),
                   "cum": [round(c, 1) for c in cum],
                   "elev": [reseau.altitude(p) for p in complet],
                   "km": bornes, "points": postes}, f, ensure_ascii=False)
    with open(os.path.join(DONNEES, "roadbook.json"), "w", encoding="utf-8") as f:
        json.dump(feuille_de_route(reseau, complet), f, ensure_ascii=False, indent=1)
    blocages = points_de_blocage(reseau, complet, cum)
    with open(os.path.join(DONNEES, "points_blocage.csv"), "w", encoding="utf-8") as f:
        f.write("km;latitude;longitude;voies_laterales;debouche_sur\n")
        for b in blocages:
            f.write(f"{b['km']:.2f};{b['lat']:.5f};{b['lon']:.5f};"
                    f"{b['voies']};{b['debouche_sur']}\n")
    print(f"{len(blocages)} points de blocage listés dans donnees/points_blocage.csv")

    traits = [{"type": "Feature",
               "properties": {"nom": "Boucle Sud (km 0 - 6,03)", "type": "parcours"},
               "geometry": {"type": "LineString", "coordinates": coords(sud)}},
              {"type": "Feature",
               "properties": {"nom": "Boucle Nord (km 6,03 - 10,00)", "type": "parcours"},
               "geometry": {"type": "LineString", "coordinates": coords(nord)}}]
    for b in bornes:
        traits.append({"type": "Feature", "properties": {"nom": f"km {b['km']}", "type": "borne"},
                       "geometry": {"type": "Point", "coordinates": b["coord"]}})
    for p in postes:
        traits.append({"type": "Feature", "properties": {"nom": p["nom"], "type": p["type"]},
                       "geometry": {"type": "Point", "coordinates": p["coord"]}})
    with open(os.path.join(ICI, "parcours.geojson"), "w", encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "name": "Tour de Moroni — parcours 10 km",
                   "features": traits}, f, ensure_ascii=False, indent=1)

    print("\nFeuille de route :")
    for l in feuille_de_route(reseau, complet):
        print(f"  km {l['depuis_km']:5.2f}  {l['m']:5d} m  {l['rue']}")


if __name__ == "__main__":
    main()
