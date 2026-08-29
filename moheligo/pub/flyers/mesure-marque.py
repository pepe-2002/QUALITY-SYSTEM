#!/usr/bin/env python3
"""📐 MESURER LA MARQUE — pas la juger, la mesurer.

29/08/2026. Une relecture extérieure a dit : « votre vague doit devenir un
élément officiel », « le jaune doit devenir une propriété », « votre symbole
doit être reconnaissable sans le mot ». Trois affirmations justes — mais dites
de l'extérieur, donc devinées.

📌 LA RÈGLE QU'ON S'EST DONNÉE LE 29/08 : quand un relecteur signale une
incohérence, on ne discute pas, ON MESURE. Ce fichier est l'instrument. Il
répond à trois questions, et il donne des CHIFFRES, pas des avis :

  1. LA VAGUE  — combien de formes différentes portent le même nom ?
                 Une signature qui a six dessins n'est pas une signature.
  2. L'OR      — quelle part de chaque visuel ? La règle proposée est 10 %.
                 Ce qui compte n'est pas la moyenne, c'est L'ÉCART : une marque
                 dont les visuels vont de 0,1 % à 19,8 % n'a pas de règle.
  3. L'EMBLÈME — tient-il à 32 px, taille d'une pastille d'application ?
                 C'est le test « cache le mot, reste-t-il reconnaissable ? ».

    python3 mesure-marque.py

⚠️ CE PROGRAMME NE CORRIGE RIEN, exprès. Il constate. La correction touche à
l'identité (le logo est celui du patron, la vague aussi) : elle se propose, elle
ne se décide pas ici. Manuel § 12.2, règle A / B / C — dans le doute, je propose.
"""
import glob
import os
import re
import sys
from collections import defaultdict

try:
    from PIL import Image
except ImportError:
    sys.exit("pillow manquant :  pip install pillow")

ICI = os.path.dirname(os.path.abspath(__file__))
OR_VISE = (8.0, 15.0)      # la bande qu'on se donne, voir plus bas
PETIT = 32                 # taille d'une pastille d'application


def _paths(texte):
    """Les tracés larges qui ferment vers le bas : les vagues, pas les icônes."""
    sortie = []
    for d in re.findall(r'<path[^>]*\sd="([^"]+)"', texte):
        if not re.match(r'^M\s*0[ ,]', d):
            continue
        nombres = [float(x) for x in re.findall(r'-?\d+\.?\d*', d)]
        if nombres and max(nombres) > 200:       # une icône tient dans 24 ou 40
            sortie.append(' '.join(d.split()))
    return sortie


def la_vague():
    formes = defaultdict(set)
    fichiers = sorted(glob.glob(os.path.join(ICI, 'flyer*.html')))
    sans = []
    for f in fichiers:
        trouves = _paths(open(f, encoding='utf-8').read())
        if trouves:
            for d in trouves:
                formes[d].add(os.path.basename(f))
        else:
            sans.append(os.path.basename(f))
    avec = len(fichiers) - len(sans)
    print(f"\n🌊 LA VAGUE")
    print(f"   {len(fichiers)} sources de visuels")
    print(f"   {avec} en portent une · {len(sans)} n'en portent AUCUNE")
    print(f"   {len(formes)} tracés différents pour un seul nom")
    for i, (d, fs) in enumerate(sorted(formes.items(), key=lambda k: -len(k[1])), 1):
        print(f"     {i:2}. {len(fs):2} visuel(s)  {d[:56]}…")
    if len(formes) > 1:
        print("   ⚠️  Une signature de marque a UN dessin. Ici elle en a "
              f"{len(formes)}, et {len(sans)} visuels s'en passent.")
    return len(formes), avec, len(sans)


def _classe(px):
    r, g, b = px
    if r > 200 and g > 200 and b > 200:
        return 'blanc'
    if r > 150 and g > 120 and b < 110 and r > b + 60:
        return 'or'
    if b > r + 25 and b > 60:
        return 'bleu'
    return 'autre'


def l_or():
    """La part d'or de chaque visuel publié.

    ⚠️ On échantillonne en 160 x 200 : on cherche une PROPORTION, pas un pixel.
    Mesurer en pleine résolution donnerait le même chiffre en 300 fois plus de
    temps.
    """
    lignes = []
    for f in sorted(glob.glob(os.path.join(ICI, 'flyer-*facebook.png'))):
        im = Image.open(f).convert('RGB').resize((160, 200))
        n = defaultdict(int)
        for px in im.getdata():
            n[_classe(px)] += 1
        t = sum(n.values())
        lignes.append((n['or'] / t * 100, n['bleu'] / t * 100,
                       os.path.basename(f)[6:-13]))
    if not lignes:
        print("\n🟡 L'OR — aucun visuel rendu, rien à mesurer.")
        return
    lignes.sort(reverse=True)
    moy = sum(l[0] for l in lignes) / len(lignes)
    hors = [l for l in lignes if not (OR_VISE[0] <= l[0] <= OR_VISE[1])]
    print(f"\n🟡 L'OR  ({len(lignes)} visuels publiés)")
    print(f"   moyenne {moy:.1f} %  ·  du plus sobre {lignes[-1][0]:.1f} % "
          f"au plus chargé {lignes[0][0]:.1f} %")
    print(f"   bande visée {OR_VISE[0]:.0f}–{OR_VISE[1]:.0f} % : "
          f"{len(lignes) - len(hors)} dedans, {len(hors)} dehors")
    print("   les cinq plus chargés  : " +
          ', '.join(f"{n} {o:.0f}%" for o, _, n in lignes[:5]))
    print("   les cinq plus pauvres  : " +
          ', '.join(f"{n} {o:.0f}%" for o, _, n in lignes[-5:]))
    print("   📌 Ce n'est pas la moyenne qui cloche — elle est bonne. C'est "
          "L'ÉCART :\n      un visuel à 0,1 % et un autre à 20 % ne viennent "
          "pas de la même marque.")


def l_embleme():
    f = os.path.join(ICI, 'logo-emblem.png')
    if not os.path.exists(f):
        print("\n🔵 L'EMBLÈME — logo-emblem.png introuvable.")
        return
    im = Image.open(f).convert('RGB')
    petit = im.resize((PETIT, PETIT), Image.LANCZOS)
    # Combien de couleurs distinctes survivent ? Un symbole fort en garde 2 ou 3
    # nettes ; une illustration se mélange en une bouillie de nuances.
    couleurs = len(set(petit.getdata()))
    n = defaultdict(int)
    for px in petit.getdata():
        n[_classe(px)] += 1
    t = sum(n.values())
    print(f"\n🔵 L'EMBLÈME  ({im.size[0]} x {im.size[1]})")
    print(f"   réduit à {PETIT} px : {couleurs} nuances distinctes")
    print(f"   dont bleu {n['bleu']/t*100:.0f} %  or {n['or']/t*100:.0f} %  "
          f"blanc {n['blanc']/t*100:.0f} %")
    if couleurs > 120:
        print("   ⚠️  À la taille d'une pastille d'application, le dessin se "
              "referme en tache.\n      C'est une ILLUSTRATION (un navire vu de "
              "trois quarts, avec ses ponts),\n      pas encore un SYMBOLE. Le "
              "test « cache le mot » n'est pas passé.")
    else:
        print("   ✅ Le dessin tient à la taille d'une pastille.")


if __name__ == '__main__':
    print("=" * 68)
    print(" MESURE DE LA MARQUE MoheliGo — des chiffres, pas des avis")
    print("=" * 68)
    la_vague()
    l_or()
    l_embleme()
    print("\n" + "=" * 68)
    print(" Ces trois mesures ne disent PAS quoi faire. Elles disent où on en")
    print(" est. Ce qui touche à l'identité se propose au patron — § 12.2.")
    print("=" * 68)
