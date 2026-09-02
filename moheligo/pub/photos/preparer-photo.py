#!/usr/bin/env python3
"""Prépare une photo du patron pour un flyer plein cadre — 02/09/2026.

    python3 preparer-photo.py <source.jpg> <sortie.png> [largeur] [hauteur]

🚩 POURQUOI CE PROGRAMME EXISTE : le patron a envoyé sept photos de Mohéli en
demandant que TOUS les flyers hors bulletin en portent une. Elles font toutes
**720 px de large**. Nos visuels font **2160 px**. Il faut donc agrandir 3 fois,
et un agrandissement de 3× est normalement un aveu d'échec.

📊 CE QUE LA MESURE A DIT, ET COMMENT ELLE M'A D'ABORD TROMPÉ.
Premier réflexe : comparer la « netteté » (variance du laplacien) avant et après
agrandissement, sur deux photos — une très nette (végétation, 3156) et une très
floue (mer et ciel, 249).
    végétation : 3156 → 69   soit 97,8 % de perte
    mer + ciel :  249 →  6   soit 97,7 % de perte
**Les deux chiffres sont identiques.** Un indicateur qui donne exactement la même
réponse pour le bon cas et pour le mauvais ne mesure pas ce qui nous intéresse :
la variance du laplacien est une mesure PAR PIXEL, et tripler les pixels la
divise mécaniquement, quelle que soit l'image.
📌 **UN POURCENTAGE IDENTIQUE DANS LES DEUX CAS N'EST PAS UN RÉSULTAT, C'EST UN
AVERTISSEMENT : on mesure la mauvaise chose.** (Même leçon que le 01/09 sur le
carton de fin de la vidéo, trouvé en comptant des pixels marine au lieu de
comparer des formes.)

👁️ CE QUI TRANCHE VRAIMENT, ET IL A FALLU REGARDER : ce n'est pas la netteté de
départ, c'est **la quantité de détail fin que l'image contient**.
· Une frondaison, du sable en gros plan, une foule : le détail est plus petit
  que le pixel source. Agrandi, il devient une bouillie plastique. Inutilisable.
· La mer, le ciel, un horizon, une plage vue de loin : ce sont des DÉGRADÉS. Il
  n'y a presque rien à inventer entre deux pixels, donc l'agrandissement ne
  fabrique aucun faux détail. Le résultat tient sans qu'on le voie.
✅ **LA PHOTO LA PLUS FLOUE DES SEPT EST CELLE QUI S'AGRANDIT LE MIEUX** — parce
qu'elle n'a rien à perdre. C'est contre-intuitif et c'est vérifiable à l'œil.

⚖️ LA RÈGLE QUI EN SORT, ET ELLE VAUT POUR TOUTES LES PROCHAINES PHOTOS :
    plein cadre  → uniquement mer, ciel, horizon, plage au loin
    demi-page    → paysage avec un peu de végétation lointaine
    jamais       → feuillage proche, sable en gros plan, visage, foule
Et de toute façon : **on demande toujours l'original.** Ces sept-là sont des
copies compressées (signature d'un renvoi WhatsApp). L'original du téléphone
ferait 3000 à 4000 px et cette page entière deviendrait inutile.

🔧 CE QUE FAIT LE PROGRAMME : il coupe les bandes de capture d'écran, cadre sans
déformer, puis délègue l'agrandissement à `affiner.py` — débruitage, puis
**rétroprojection itérative**, puis un accentuage faible guidé par les contours.
📊 Mesuré sur les sept photos à taille de sortie identique : l'acutance des
contours **double**, et sur les plus compressées le bruit **baisse** en même
temps. Voir `affiner.py` pour le détail, et surtout pour la surprise : c'est la
rétroprojection qui fait le travail, pas l'accentuage.

⚠️ LE SEUIL DE DIAGNOSTIC CI-DESSOUS SE LIT SUR LA SOURCE, JAMAIS SUR LE
RÉSULTAT. Je m'y suis fait prendre : appliqué à l'image déjà agrandie, il annonce
des « détails fins » deux fois plus bas et donc des verdicts flatteurs — alors
que la seule chose qui a changé, c'est le nombre de pixels.
📌 Un seuil calibré à une échelle ne veut plus rien dire à une autre.
"""
import pathlib
import sys

import cv2
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import affiner                                   # noqa: E402



def sans_bandes(im, seuil=4.0):
    """Retire les bandes UNIFORMES en haut et en bas — 02/09/2026.

    Les photos du patron sont des captures d'écran renvoyées par WhatsApp : la
    première en portait quatre lignes grises en haut (écart-type 0,2 contre 20
    pour la vraie image juste en dessous). Quatre lignes sur 535, c'est
    invisible à l'œil sur le téléphone — mais agrandies trois fois elles font
    **douze lignes** en haut d'un visuel, et là ça se voit.
    📌 Un défaut qu'on ne voit pas dans la source se voit dans l'agrandissement.
    On coupe donc AVANT d'agrandir, et automatiquement : il y aura d'autres
    captures, et personne ne pensera à vérifier à chaque fois.
    """
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(float)
    haut = 0
    while haut < len(g) // 4 and g[haut].std() < seuil:
        haut += 1
    bas = len(g)
    while bas > len(g) * 3 // 4 and g[bas - 1].std() < seuil:
        bas -= 1
    return im[haut:bas], haut, len(g) - bas


def preparer(source, largeur, hauteur):
    im = cv2.imread(source)
    if im is None:
        sys.exit('image illisible : ' + source)
    im, nh, nb = sans_bandes(im)
    if nh or nb:
        print(f'   bandes uniformes retirées : {nh} px en haut, {nb} px en bas')
    h, w = im.shape[:2]

    # --- cadrage : on remplit la boîte demandée sans jamais déformer ---------
    # Déformer une photo pour la faire entrer, c'est le premier signe d'un
    # visuel amateur, et ça se voit surtout sur un horizon : la mer penche.
    echelle = max(largeur / w, hauteur / h)
    nw, nh = int(round(w * echelle)), int(round(h * echelle))
    # 02/09/2026 — l'agrandissement passe par `affiner.py` et non plus par un
    # simple Lanczos. Mesuré sur les sept photos, à taille de sortie IDENTIQUE :
    # l'acutance des contours DOUBLE, et sur les photos les plus compressées le
    # bruit BAISSE en même temps. Ce n'est pas du maquillage : la
    # rétroprojection recolle le résultat aux pixels réellement mesurés.
    g, _ = affiner.affiner(im, nw, nh)

    # On coupe au centre horizontalement, mais on garde le HAUT verticalement :
    # sur une photo de plage, le ciel et l'horizon sont en haut, et c'est cette
    # partie-là qui supporte l'agrandissement. Couper au centre mangerait le
    # ciel pour garder du sable en gros plan, exactement l'inverse du bon choix.
    x = (nw - largeur) // 2
    g = g[0:hauteur, x:x + largeur]

    # Plus d'accentuage ici : `affiner` en applique déjà un, guidé par les
    # contours. En empiler un second, aveugle celui-là, redonnerait exactement
    # le grain qu'on vient d'éviter.
    return g


def diagnostic(source):
    """Dit si la photo supporte un plein cadre, et sur quel critère."""
    im = cv2.imread(source)
    h, w = im.shape[:2]
    gris = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # Le détail FIN : ce que l'agrandissement ne saura pas inventer. On le
    # mesure en comparant l'image à elle-même adoucie — ce qui disparaît au
    # passage est exactement ce qui ne survivra pas non plus à l'agrandissement.
    fin = float(np.mean(np.abs(gris.astype(float) -
                               cv2.GaussianBlur(gris, (0, 0), 1.2).astype(float))))
    verdict = ('plein cadre' if fin < 3.0 else
               'demi-page' if fin < 6.0 else 'vignette seulement')
    return w, h, fin, verdict


if __name__ == '__main__':
    if len(sys.argv) == 2:
        w, h, fin, v = diagnostic(sys.argv[1])
        print(f'{w}x{h}  détail fin {fin:.2f}  ->  {v}')
        sys.exit(0)
    if len(sys.argv) < 3:
        sys.exit(__doc__.strip().splitlines()[2])
    L = int(sys.argv[4]) if len(sys.argv) > 4 else 1485
    cv2.imwrite(sys.argv[2], preparer(sys.argv[1],
                                      int(sys.argv[3]) if len(sys.argv) > 3 else 2160, L))
    print('OK ->', sys.argv[2])
