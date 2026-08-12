#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nettoie et agrandit les photos reçues, pour qu'elles tiennent sur un visuel.

    python3 agrandir.py                 # traite tous les .jpg du dossier
    python3 agrandir.py --facteur 2.5

⚠️ LE MOT JUSTE : on ne « décompresse » pas une photo. Ce que le JPEG a jeté est
**définitivement perdu** — aucun programme ne le retrouve. Ce qu'on peut faire,
et qui change vraiment le rendu :

  1. **effacer les artefacts** de compression (les petits carrés autour des
     contrastes, très visibles sur ces photos passées par les réseaux) ;
  2. **agrandir proprement** avec un rééchantillonnage Lanczos, qui invente des
     pixels intermédiaires doux au lieu de dupliquer les gros pixels ;
  3. **remonter la netteté locale** avec un masque flou, pour compenser le
     lissage des deux étapes précédentes.

Le résultat est **plus propre**, jamais **plus détaillé**. Un visage flou au
départ reste flou : c'est pour ça qu'on demande les fichiers d'origine.

Mesures relevées le 12/08/2026 sur les trois photos reçues (netteté = variance du
laplacien, artefacts = écart au filtre médian) :
    ocean-indien   1280x1280  netteté 1896  artefacts 5,13  → la plus abîmée
    podium         1080x856   netteté 1255  artefacts 2,91
    2e-challenger   854x1280  netteté  176  artefacts 0,67  → nette mais douce
"""

import argparse
import glob
import os

import cv2
import numpy as np


def traiter(chemin, facteur=2.0, force_debruitage=None):
    im = cv2.imread(chemin)
    if im is None:
        raise SystemExit('illisible : ' + chemin)
    h, w = im.shape[:2]

    gris = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    artefacts = float(np.mean(np.abs(gris.astype(float)
                                    - cv2.medianBlur(gris, 3).astype(float))))
    # Le débruitage est dosé selon les artefacts MESURÉS, pas au hasard : trop
    # fort, il lisse la peau et les tissus et donne un rendu « plastique ».
    h_lum = force_debruitage if force_debruitage is not None else \
        (5 if artefacts > 4 else 3 if artefacts > 1.5 else 0)
    if h_lum:
        im = cv2.fastNlMeansDenoisingColored(im, None, h_lum, h_lum, 7, 21)

    grand = cv2.resize(im, (int(w * facteur), int(h * facteur)),
                       interpolation=cv2.INTER_LANCZOS4)

    # masque flou : on soustrait une version floutée pour rehausser les bords
    flou = cv2.GaussianBlur(grand, (0, 0), 1.6)
    net = cv2.addWeighted(grand, 1.35, flou, -0.35, 0)

    return net, artefacts, h_lum


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--facteur', type=float, default=2.0)
    ap.add_argument('--qualite', type=int, default=95)
    a = ap.parse_args()

    for f in sorted(glob.glob('*.jpg')):
        if f.endswith('-net.jpg'):
            continue
        net, artefacts, h_lum = traiter(f, a.facteur)
        sortie = f.replace('.jpg', '-net.jpg')
        cv2.imwrite(sortie, net, [cv2.IMWRITE_JPEG_QUALITY, a.qualite])
        print('%-52s → %-56s %sx%s  (artefacts %.2f, débruitage %d)'
              % (f, sortie, net.shape[1], net.shape[0], artefacts, h_lum))
        print('   %s ko → %s ko' % (round(os.path.getsize(f) / 1024),
                                    round(os.path.getsize(sortie) / 1024)))


if __name__ == '__main__':
    main()
