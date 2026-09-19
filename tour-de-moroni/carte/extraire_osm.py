#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extraction des données de Moroni depuis OpenStreetMap (et des altitudes SRTM).

À relancer seulement pour rafraîchir le fond de carte — pas à chaque carte.
Écrit dans `donnees/` :

  routes_moroni.json    les rues de Moroni (nom, catégorie, tracé)
  contexte_moroni.json  le trait de côte et les repères nommés
  altitudes.json        l'altitude SRTM 30 m de chaque point de rue

    python3 extraire_osm.py

Sources : Overpass API (données OpenStreetMap, licence ODbL — l'attribution
« © les contributeurs OpenStreetMap » doit rester sur toute carte publiée) et
api.opentopodata.org pour le modèle de terrain SRTM 30 m.

Attention : les altitudes SRTM ont environ ±5 m d'incertitude verticale. Elles
suffisent à dire que le parcours est plat ; elles ne remplacent pas un relevé de
terrain pour valider les pentes vues par un fauteuil roulant.
"""

import json
import os
import ssl
import time
import urllib.parse
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
DONNEES = os.path.join(ICI, "donnees")

# Cadre de travail : Moroni, d'Iconi au sud à Salimani-Itsandra au nord.
BBOX = (-11.7320, -11.6770, 43.2380, 43.2680)          # latmin latmax lonmin lonmax
BBOX_LARGE = (-11.76, -11.64, 43.22, 43.30)            # pour le réseau routier

MIROIRS = ["https://overpass-api.de/api/interpreter",
           "https://overpass.kumi.systems/api/interpreter",
           "https://overpass.private.coffee/api/interpreter"]

CATEGORIES = ("motorway|trunk|primary|secondary|tertiary|unclassified|"
              "residential|living_street|pedestrian")


def _ouvreur():
    """Un ouvreur d'URL qui passe par le proxy de session quand il y en a un."""
    ca = "/root/.ccr/ca-bundle.crt"
    ctx = ssl.create_default_context(cafile=ca) if os.path.exists(ca) else None
    handlers = []
    proxy = os.environ.get("HTTPS_PROXY")
    if proxy:
        handlers.append(urllib.request.ProxyHandler({"https": proxy}))
    if ctx:
        handlers.append(urllib.request.HTTPSHandler(context=ctx))
    return urllib.request.build_opener(*handlers)


OUVREUR = _ouvreur()


def overpass(requete):
    """Interroge Overpass, en changeant de miroir si l'un ne répond pas."""
    for url in MIROIRS:
        for essai in range(3):
            try:
                r = OUVREUR.open(urllib.request.Request(
                    url, data=requete.encode(),
                    headers={"User-Agent": "tour-de-moroni/1.0"}), timeout=180)
                return json.loads(r.read())
            except Exception as e:                       # miroir saturé, on patiente
                print(f"   {url.split('/')[2]} : {type(e).__name__}, nouvel essai")
                time.sleep(5)
    raise SystemExit("Overpass injoignable — réessayer plus tard.")


def extraire_routes():
    la0, la1, lo0, lo1 = BBOX_LARGE
    q = (f"[out:json][timeout:120];(way[\"highway\"~\"^({CATEGORIES})$\"]"
         f"({la0},{lo0},{la1},{lo1}););out body geom;")
    d = overpass(q)
    la0, la1, lo0, lo1 = BBOX
    out = []
    for e in d["elements"]:
        if e["type"] != "way" or "geometry" not in e:
            continue
        g = [(round(p["lat"], 5), round(p["lon"], 5)) for p in e["geometry"]]
        if not any(la0 <= la <= la1 and lo0 <= lo <= lo1 for la, lo in g):
            continue
        out.append({"h": e["tags"].get("highway"), "n": e["tags"].get("name"), "g": g})
    ecrire("routes_moroni.json", out)
    return out


def extraire_contexte():
    la0, la1, lo0, lo1 = BBOX
    q = ("[out:json][timeout:120];("
         f"way[\"natural\"=\"coastline\"]({la0 - 0.03},{lo0 - 0.02},{la1 + 0.03},{lo1 + 0.02});"
         f"nwr[\"place\"~\"suburb|neighbourhood|quarter|town\"]({la0},{lo0},{la1},{lo1});"
         f"nwr[\"amenity\"~\"hospital|marketplace|university|townhall|place_of_worship|police|college\"]({la0},{lo0},{la1},{lo1});"
         f"nwr[\"leisure\"~\"stadium|sports_centre|pitch\"]({la0},{lo0},{la1},{lo1});"
         f"nwr[\"office\"=\"government\"]({la0},{lo0},{la1},{lo1});"
         f"nwr[\"historic\"]({la0},{lo0},{la1},{lo1});"
         ");out center geom tags;")
    d = overpass(q)
    coast, reperes = [], []
    for e in d["elements"]:
        t = e.get("tags", {})
        if t.get("natural") == "coastline" and "geometry" in e:
            coast.append([(round(p["lat"], 5), round(p["lon"], 5)) for p in e["geometry"]])
            continue
        nom = t.get("name") or t.get("name:fr")
        la = e.get("lat") or e.get("center", {}).get("lat")
        lo = e.get("lon") or e.get("center", {}).get("lon")
        if not nom or la is None:
            continue
        if not (la0 <= la <= la1 and lo0 <= lo <= lo1):
            continue
        genre = (t.get("place") or t.get("amenity") or t.get("leisure")
                 or t.get("natural") or t.get("office") or t.get("historic"))
        reperes.append({"n": nom, "k": genre, "la": round(la, 5), "lo": round(lo, 5)})
    ecrire("contexte_moroni.json", {"coast": coast, "reperes": reperes})


def extraire_altitudes(routes):
    """Altitude SRTM de chaque point de rue, par paquets de 100 (limite du service)."""
    chemin = os.path.join(DONNEES, "altitudes.json")
    connues = {}
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            connues = json.load(f)
    points = []
    for r in routes:
        for la, lo in r["g"]:
            cle = f"{la:.5f},{lo:.5f}"
            if cle not in connues:
                points.append((cle, la, lo))
    points = list(dict(((p[0], p) for p in points)).values())
    print(f"   {len(points)} points sans altitude")
    for i in range(0, len(points), 100):
        paquet = points[i:i + 100]
        locs = "|".join(f"{la:.6f},{lo:.6f}" for _, la, lo in paquet)
        for essai in range(4):
            try:
                r = OUVREUR.open(urllib.request.Request(
                    "https://api.opentopodata.org/v1/srtm30m",
                    data=urllib.parse.urlencode({"locations": locs}).encode(),
                    headers={"User-Agent": "tour-de-moroni/1.0"}), timeout=90)
                for (cle, _, _), res in zip(paquet, json.loads(r.read())["results"]):
                    connues[cle] = res["elevation"]
                break
            except Exception as e:
                print(f"   altitudes : {type(e).__name__}, nouvel essai")
                time.sleep(4)
        time.sleep(1.1)                                  # 1 requête/seconde : la règle du service
    ecrire("altitudes.json", connues)


def ecrire(nom, obj):
    os.makedirs(DONNEES, exist_ok=True)
    with open(os.path.join(DONNEES, nom), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
    print(f"   écrit : donnees/{nom}")


if __name__ == "__main__":
    print("1/3 réseau routier…")
    routes = extraire_routes()
    print("2/3 trait de côte et repères…")
    extraire_contexte()
    print("3/3 altitudes…")
    extraire_altitudes(routes)
    print("Fait. Relancer ensuite : python3 calculer_parcours.py puis python3 carte.py")
