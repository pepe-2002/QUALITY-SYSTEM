#!/usr/bin/env python3
"""Duotone marine/or + grain : le traitement d'affiche de voyage.

Pourquoi ce traitement (recherche du 08/08/2026 sur ce qui fait une belle
affiche) : réduire une photo à deux couleurs force la clarté graphique — les
formes et les contrastes deviennent lisibles et mémorables, là où la couleur
complète disperse le regard. Le couple marine + or est le registre « sophistiqué »
du duotone, et c'est exactement notre charte. Le grain, lui, enlève le côté
« fait à l'ordinateur ».

Méthode : mappage de dégradé (gradient map). La luminance de chaque pixel sert
d'index dans une rampe de 256 couleurs allant du marine profond au crème doré.
Puis grain monochrome léger, et vignettage.

    python3 duotone.py            # traite les deux photos candidates
"""
import random
from PIL import Image, ImageChops, ImageEnhance, ImageFilter

# rampe : ombres marine -> bleu -> or -> crème (les points d'arrêt sont la charte)
RAMPE = [(0.00, (5, 14, 34)), (0.28, (14, 45, 100)), (0.52, (28, 79, 168)),
         (0.74, (246, 188, 28)), (0.90, (255, 226, 150)), (1.00, (255, 247, 224))]
CIBLE = (2160, 2700)          # plein cadre 4:5 pour Facebook


def rampe_255():
    """Interpole la rampe en une table de 256 couleurs."""
    table = []
    for i in range(256):
        t = i / 255
        for (t0, c0), (t1, c1) in zip(RAMPE, RAMPE[1:]):
            if t0 <= t <= t1:
                k = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                table.append(tuple(int(a + (b - a) * k) for a, b in zip(c0, c1)))
                break
        else:
            table.append(RAMPE[-1][1])
    return table


def cadrer(im, cible):
    """Recadre en couvrant, puis met à la taille cible."""
    cw, ch = cible
    r_src, r_cible = im.width / im.height, cw / ch
    if r_src > r_cible:                      # trop large : on coupe les côtés
        w = int(im.height * r_cible)
        im = im.crop(((im.width - w) // 2, 0, (im.width + w) // 2, im.height))
    else:                                    # trop haute : on coupe en hauteur
        h = int(im.width / r_cible)
        haut = int((im.height - h) * 0.34)    # un peu plus de ciel que de sable
        im = im.crop((0, haut, im.width, haut + h))
    return im.resize(cible, Image.LANCZOS)


def duotone(src, out, contraste=1.18, grain=9):
    im = cadrer(Image.open(src).convert('RGB'), CIBLE)
    W, H = im.size

    lum = ImageEnhance.Contrast(im.convert('L')).enhance(contraste)
    table = rampe_255()
    plat = [c for coul in table for c in coul]          # palette à plat
    duo = lum.convert('P')
    duo.putpalette(plat)
    im = duo.convert('RGB').filter(ImageFilter.SMOOTH)

    # grain monochrome : le détail qui enlève le côté « fait à l'ordinateur »
    random.seed(5)
    bruit = Image.effect_noise((W // 2, H // 2), 26).resize((W, H), Image.BILINEAR)
    bruit = bruit.point(lambda v: 128 + int((v - 128) * grain / 100))
    im = ImageChops.overlay(im, Image.merge('RGB', (bruit, bruit, bruit)))

    # vignettage doux : le regard reste au centre
    sw, sh = 160, 200
    vig = Image.new('L', (sw, sh)); vp = vig.load()
    for y in range(sh):
        for x in range(sw):
            d = (((x - sw / 2) / (sw / 2)) ** 2 + ((y - sh / 2) / (sh / 2)) ** 2) ** 0.5
            vp[x, y] = int(255 * max(0.0, 1 - 0.34 * max(0.0, d - 0.55) / 0.75))
    vig = vig.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(W * 0.02))
    im = Image.composite(im, Image.new('RGB', (W, H), (4, 11, 28)), vig)

    im.save(out, quality=94)
    print(out, im.size)


if __name__ == '__main__':
    duotone('../photos-cc/nioumachoua-ilot-fatima.jpg', 'duo-ilots.jpg', contraste=1.30)
    duotone('../photos/mer-bateau.jpg', 'duo-vedette.jpg', contraste=1.14)
