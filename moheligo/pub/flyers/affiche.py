#!/usr/bin/env python3
"""Étalonnage des photos d'affiche MoheliGo.

Consigne du patron (06/08/2026) : **aucune photo montrant une personne**
(droit à l'image). Les deux photos traitées ici sont des paysages, personne
dessus.

  A. ../photos-cc/nioumachoua-ilot-fatima.jpg — îlots de Nioumachoua depuis la
     plage, Fatima771, CC BY 3.0, Wikimedia Commons (plage vide).
     Photo voilée à l'origine → « dévoilage » par autocontrast puis couleur.
     -> nioumachoua-affiche.jpg
  B. ../photos/vedette-mer.jpg — notre photo : une vedette au large, pleine mer.
     Aucune licence à respecter. -> vedette-affiche.jpg

Le traitement rend la lumière que le voile a mangée : niveaux, contraste,
saturation, chaleur douce au ras de l'horizon, mer plus profonde, vignettage,
netteté. Rien n'est ajouté ni retiré de la scène.
"""
import sys
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageOps

JOBS = [
    dict(src='../photos-cc/nioumachoua-ilot-fatima.jpg', out='nioumachoua-affiche.jpg',
         horizon=0.545, devoile=(2, 8), contraste=1.14, couleur=1.45,
         halo=(0.16, (50, 32, 10)), bleu=1.10),
    dict(src='../photos/vedette-mer.jpg', out='vedette-affiche.jpg',
         horizon=0.135, devoile=None, contraste=1.14, couleur=1.30,
         halo=(0.18, (60, 40, 12)), bleu=1.10),
]


def etalonner(src, out, horizon, devoile, contraste, couleur, halo, bleu):
    im = Image.open(src).convert('RGB')
    W, H = im.size

    # 1) niveaux : on récupère les noirs et les blancs mangés par le voile
    if devoile:
        im = ImageOps.autocontrast(im, cutoff=devoile)
    im = ImageEnhance.Contrast(im).enhance(contraste)
    im = ImageEnhance.Color(im).enhance(couleur)

    # 2) chaleur douce au ras de l'horizon
    largeur, amp = halo
    glow = Image.new('RGB', (1, H))
    for y in range(H):
        d = abs(y / H - horizon)
        v = max(0.0, 1 - (d / largeur) ** 1.5)
        glow.putpixel((0, y), (int(amp[0] * v), int(amp[1] * v), int(amp[2] * v)))
    im = ImageChops.add(im, glow.resize((W, H)))

    # 3) mer plus profonde sous l'horizon
    r, g, b = im.split()
    mask = Image.new('L', (1, H))
    for y in range(H):
        t = y / H
        v = 0.0 if t < horizon else min(1.0, (t - horizon) / 0.12)
        mask.putpixel((0, y), int(140 * v))
    mask = mask.resize((W, H))
    b = Image.composite(b.point(lambda v: min(255, int(v * bleu + 5))), b, mask)
    r = Image.composite(r.point(lambda v: int(v * 0.93)), r, mask)
    im = Image.merge('RGB', (r, g, b))

    # 4) vignettage discret (masque calculé en petit puis agrandi)
    sw, sh = 180, 240
    vig = Image.new('L', (sw, sh))
    vp = vig.load()
    for y in range(sh):
        for x in range(sw):
            d = (((x - sw / 2) / (sw / 2)) ** 2 + ((y - sh * 0.46) / (sh * 0.62)) ** 2) ** 0.5
            vp[x, y] = int(255 * max(0.0, 1 - 0.32 * max(0.0, d - 0.62) / 0.70))
    vig = vig.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(W * 0.015))
    im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig)

    im = im.filter(ImageFilter.UnsharpMask(radius=2.4, percent=64, threshold=3))
    im.save(out, quality=94)
    print(out, im.size)


for job in JOBS:
    try:
        etalonner(**job)
    except FileNotFoundError:
        print('absent, ignoré :', job['src'], file=sys.stderr)
