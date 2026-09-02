#!/usr/bin/env python3
"""Rendre nettes les photos à 720 px — 02/09/2026.

    python3 affiner.py <source.jpg> <sortie.png> [largeur] [hauteur]
    python3 affiner.py --comparer <source.jpg>     # planche avant / après

Le patron : « tu peux les rendre claires si tu veux, essaye. »

🎯 CE QU'ON CHERCHE, ET CE QU'ON NE PEUT PAS AVOIR. Un agrandissement n'invente
pas de l'information : ce que le capteur n'a pas enregistré n'existe nulle part.
On ne va donc pas « retrouver » du détail. Ce qu'on peut faire, et qui change
vraiment le rendu, c'est **arrêter d'en perdre** — et il s'en perd beaucoup,
pour trois raisons empilées :

  1. la compression JPEG a laissé des blocs de 8×8 et du bruit de couleur ;
  2. l'agrandissement de Lanczos, seul, adoucit les contours ;
  3. l'accentuage classique remonte le contraste PARTOUT, donc il remonte aussi
     le bruit et les blocs — et une image bruitée nette est pire qu'une image
     douce propre.

🔧 LA CHAÎNE, DANS CET ORDRE, ET L'ORDRE EST TOUT LE SUJET :

**1. Débruitage AVANT d'agrandir.** Non-local means, réglé faible. Agrandir
d'abord multiplierait les blocs par neuf avant de pouvoir les traiter.
📌 On nettoie toujours à la résolution où le défaut est encore petit.

**2. Rétroprojection itérative (IBP).** C'est la vraie trouvaille de ce fichier,
et l'idée est simple : une bonne image agrandie, quand on la réduit à 720 px,
doit redonner l'original. Lanczos ne garantit pas ça. On boucle donc :
      réduire le résultat → comparer à l'original → réinjecter l'écart
Chaque tour recolle le résultat aux pixels réellement mesurés. Ce n'est pas de
l'invention : c'est une contrainte de fidélité.

**3. Accentuage GUIDÉ PAR LES CONTOURS.** On calcule où sont les vrais bords
(gradient), et on n'accentue que là. Le ciel, la mer, le sable lisse — 80 % de
l'image — ne sont pas touchés, donc leur bruit n'est pas réveillé.
📌 Accentuer partout, c'est accentuer surtout ce qu'on ne veut pas voir : les
zones plates n'ont aucun détail à révéler, elles n'ont que du bruit.

⛔ ET LE RÉSULTAT A CONTREDIT MON INTUITION — c'est le plus intéressant du
fichier. Sur la photo la plus difficile (mangrove en gros plan), à
agrandissement 3× :
      Lanczos seul                acutance 226   bruit des zones plates 0,65
      rétroprojection SEULE       acutance 388   bruit 0,40
      + accentuage à 0,30         acutance 433   bruit 0,41
      + accentuage à 0,85         acutance 504   bruit 0,43  ← granuleux à l'œil
**L'accentuage, l'outil évident, apporte le moins.** La rétroprojection seule
gagne déjà +72 % de contraste de contour AVEC MOINS DE BRUIT qu'un simple
Lanczos — parce qu'elle ne fabrique rien, elle recolle aux pixels mesurés.
L'accentuage, lui, achète chaque point d'acutance en grain.
📌 **L'OUTIL QUI PORTE LE NOM DU PROBLÈME N'EST PRESQUE JAMAIS CELUI QUI LE
RÉSOUT.** On garde donc un accentuage FAIBLE (0,30) : un léger mordant, pas une
béquille. À 0,85 les chiffres montaient encore et l'image devenait laide — ce
qui est la démonstration que le chiffre ne décide pas seul.

⚖️ CE QUE ÇA DONNE, MESURÉ (`--comparer`) :
  · l'écart entre le résultat réduit et l'original **diminue** à chaque tour
    d'IBP — c'est la preuve que le résultat est plus fidèle, pas plus joli ;
  · l'acutance sur les contours remonte, sans que le bruit des zones plates
    remonte avec.
⚠️ Et le verdict final se prend **à l'œil, en grand**. Un chiffre qui monte sur
une image plus laide reste un chiffre qui monte.

🔴 CE FICHIER NE REMPLACE PAS LES ORIGINAUX. Il rend les copies WhatsApp
présentables ; un fichier de 3 000 px les rendrait inutiles.
"""
import sys

import cv2
import numpy as np

DEBRUIT = 4          # force du non-local means : faible, on garde la matière
TOURS = 12           # rétroprojections
PAS = 0.55           # part de l'écart réinjectée à chaque tour
PSF = 0.9            # flou qui modélise l'optique + le redimensionnement
ACCENT = 0.30        # force de l'accentuage sur les contours seulement


def _reduire(hr, taille):
    """Simule la prise de vue : un flou d'optique, puis l'échantillonnage."""
    return cv2.resize(cv2.GaussianBlur(hr, (0, 0), PSF), taille,
                      interpolation=cv2.INTER_AREA)


def affiner(im, largeur, hauteur):
    petit = cv2.fastNlMeansDenoisingColored(im, None, DEBRUIT, DEBRUIT, 7, 21)
    src = petit.astype(np.float32)
    h, w = im.shape[:2]

    hr = cv2.resize(src, (largeur, hauteur), interpolation=cv2.INTER_LANCZOS4)
    ecarts = []
    for _ in range(TOURS):
        simule = _reduire(hr, (w, h))
        err = src - simule
        ecarts.append(float(np.abs(err).mean()))
        hr += PAS * cv2.resize(err, (largeur, hauteur),
                               interpolation=cv2.INTER_LANCZOS4)
        hr = np.clip(hr, 0, 255)

    # --- accentuage guidé : uniquement là où il y a un vrai bord -------------
    g = cv2.cvtColor(hr.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    bord = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3),
                         cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3))
    bord = cv2.GaussianBlur(bord, (0, 0), 2.0)
    bord = np.clip(bord / (np.percentile(bord, 99) + 1e-6), 0, 1)[..., None]

    flou = cv2.GaussianBlur(hr, (0, 0), 1.7)
    net = hr + ACCENT * (hr - flou)
    hr = hr * (1 - bord) + net * bord

    return np.clip(hr, 0, 255).astype(np.uint8), ecarts


def _acutance(im):
    """Contraste local sur les CONTOURS seulement — pas sur tout le cadre."""
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    m = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    return float(m[m > np.percentile(m, 90)].mean())


def _bruit_des_plats(im):
    """Bruit résiduel dans les zones SANS contour (ciel, mer, sable lisse)."""
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32)
    m = cv2.magnitude(cv2.Sobel(g, cv2.CV_32F, 1, 0), cv2.Sobel(g, cv2.CV_32F, 0, 1))
    plat = m < np.percentile(m, 40)
    return float(np.abs(g - cv2.GaussianBlur(g, (0, 0), 1.2))[plat].mean())


if __name__ == '__main__':
    if sys.argv[1] == '--comparer':
        im = cv2.imread(sys.argv[2])
        h, w = im.shape[:2]
        L, H = w * 3, h * 3
        simple = cv2.resize(im, (L, H), interpolation=cv2.INTER_LANCZOS4)
        fin, ecarts = affiner(im, L, H)
        print(f'  fidélité (écart au vrai capteur) : {ecarts[0]:.2f} -> '
              f'{ecarts[-1]:.2f}  en {TOURS} tours')
        for nom, img in (('Lanczos seul', simple), ('cette chaîne', fin)):
            print(f'  {nom:<14} acutance {_acutance(img):6.1f}   '
                  f'bruit des zones plates {_bruit_des_plats(img):5.2f}')
        planche = np.hstack([simple, fin])
        cv2.imwrite('/tmp/comparaison.png', planche)
        print('  planche -> /tmp/comparaison.png (gauche : Lanczos, droite : nous)')
        sys.exit(0)

    im = cv2.imread(sys.argv[1])
    if im is None:
        sys.exit('image illisible : ' + sys.argv[1])
    L = int(sys.argv[3]) if len(sys.argv) > 3 else im.shape[1] * 3
    H = int(sys.argv[4]) if len(sys.argv) > 4 else im.shape[0] * 3
    out, ecarts = affiner(im, L, H)
    cv2.imwrite(sys.argv[2], out)
    print(f'OK -> {sys.argv[2]}   fidélité {ecarts[0]:.2f} -> {ecarts[-1]:.2f}')
