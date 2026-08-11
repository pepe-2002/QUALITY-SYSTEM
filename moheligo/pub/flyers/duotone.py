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

# rampe SOMBRE : ombres marine -> bleu -> or -> crème (points d'arrêt = la charte)
RAMPE = [(0.00, (5, 14, 34)), (0.28, (14, 45, 100)), (0.52, (28, 79, 168)),
         (0.74, (246, 188, 28)), (0.90, (255, 226, 150)), (1.00, (255, 247, 224))]

# rampe CLAIRE (« lumineuse ») : on ne descend jamais dans le noir. Les ombres
# restent un marine doux, les tons moyens passent par l'aigue-marine, et les
# hautes lumières montent jusqu'au crème presque blanc. C'est ce qui donne une
# affiche qui semble éclairée de l'intérieur au lieu d'être assombrie.
RAMPE_CLAIRE = [(0.00, (14, 40, 84)), (0.20, (32, 88, 140)), (0.40, (96, 162, 190)),
                (0.58, (170, 210, 214)), (0.74, (250, 214, 122)), (0.88, (255, 238, 196)),
                (1.00, (255, 252, 242))]
CIBLE = (2160, 2700)          # plein cadre 4:5 pour Facebook


def rampe_255(rampe=None):
    """Interpole une rampe en une table de 256 couleurs."""
    rampe = rampe or RAMPE
    table = []
    for i in range(256):
        t = i / 255
        for (t0, c0), (t1, c1) in zip(rampe, rampe[1:]):
            if t0 <= t <= t1:
                k = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                table.append(tuple(int(a + (b - a) * k) for a, b in zip(c0, c1)))
                break
        else:
            table.append(rampe[-1][1])
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


def duotone(src, out, contraste=1.18, grain=9, rampe=None, clair=False):
    im = cadrer(Image.open(src).convert('RGB'), CIBLE)
    W, H = im.size

    lum = im.convert('L')
    if clair:                                # on remonte les basses lumières
        lum = lum.point(lambda v: int(255 * (v / 255) ** 0.88))
    lum = ImageEnhance.Contrast(lum).enhance(contraste)
    table = rampe_255(rampe)
    plat = [c for coul in table for c in coul]          # palette à plat
    duo = lum.convert('P')
    duo.putpalette(plat)
    im = duo.convert('RGB').filter(ImageFilter.SMOOTH)

    # grain monochrome : le détail qui enlève le côté « fait à l'ordinateur »
    random.seed(5)
    bruit = Image.effect_noise((W // 2, H // 2), 26).resize((W, H), Image.BILINEAR)
    bruit = bruit.point(lambda v: 128 + int((v - 128) * grain / 100))
    im = ImageChops.overlay(im, Image.merge('RGB', (bruit, bruit, bruit)))

    if clair:
        return terminer_clair(im, out)

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


def terminer_clair(im, out):
    """Version claire : halo blanc sur les bords au lieu d'un vignettage sombre,
    et bloom généreux — l'image doit paraître éclairée, pas encadrée."""
    W, H = im.size
    lum = im.convert('L')
    hautes = lum.point(lambda v: 0 if v < 170 else min(255, int((v - 170) * 3)))
    bloom = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), hautes)
    bloom = bloom.filter(ImageFilter.GaussianBlur(W * 0.022))
    im = ImageChops.screen(im, ImageChops.multiply(bloom, Image.new('RGB', (W, H), (92, 92, 92))))

    # voile clair sur les bords (l'inverse du vignettage)
    sw, sh = 160, 200
    voile = Image.new('L', (sw, sh)); vp = voile.load()
    for y in range(sh):
        for x in range(sw):
            d = (((x - sw / 2) / (sw / 2)) ** 2 + ((y - sh / 2) / (sh / 2)) ** 2) ** 0.5
            vp[x, y] = int(140 * max(0.0, (d - 0.66) / 0.70) ** 1.5)
    voile = voile.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(W * 0.03))
    im = Image.composite(Image.new('RGB', (W, H), (255, 252, 242)), im, voile)
    im.save(out, quality=94)
    print(out, im.size, '(clair)')


if __name__ == '__main__':
    duotone('../photos-cc/nioumachoua-ilot-fatima.jpg', 'duo-ilots.jpg', contraste=1.30)
    duotone('../photos/mer-bateau.jpg', 'duo-vedette.jpg', contraste=1.14)
    duotone('../photos-cc/nioumachoua-ilot-fatima.jpg', 'duo-ilots-clair.jpg',
            contraste=1.22, grain=6, rampe=RAMPE_CLAIRE, clair=True)
