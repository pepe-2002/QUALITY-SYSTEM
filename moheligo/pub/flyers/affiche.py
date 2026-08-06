#!/usr/bin/env python3
"""Étalonnage de la photo de l'îlot de Nioumachoua pour l'affiche MoheliGo.

Source : Wikimedia Commons, « Vue de l'îlot principale de nioumachoua.jpg »,
Eldalil05, CC BY-SA 4.0 (crédit obligatoire, porté sur l'affiche et dans
pub/photos-cc/CREDITS.md).

La photo d'origine est belle mais grise (ciel couvert). On lui rend de la
lumière : chaleur douce au ras de l'horizon, mer plus profonde, contraste et
saturation relevés, léger vignettage. Rien n'est ajouté ni retiré de la scène.
"""
from PIL import Image, ImageChops, ImageEnhance, ImageFilter

SRC = '../photos-cc/nioumachoua-ilot.jpg'
OUT = 'nioumachoua-affiche.jpg'
HORIZON = 0.515          # ligne de mer (fraction de la hauteur)

im = Image.open(SRC).convert('RGB')
W, H = im.size

# 1) base : contraste, couleur, exposition
im = ImageEnhance.Contrast(im).enhance(1.16)
im = ImageEnhance.Color(im).enhance(1.30)
im = ImageEnhance.Brightness(im).enhance(1.04)

# 2) lumière chaude au ras de l'horizon (fin de journée)
glow = Image.new('RGB', (1, H))
for y in range(H):
    d = abs(y / H - HORIZON)
    v = max(0.0, 1 - (d / 0.30) ** 1.5)
    glow.putpixel((0, y), (int(92 * v), int(62 * v), int(22 * v)))
im = ImageChops.add(im, glow.resize((W, H)))

# 3) mer plus profonde : bleu renforcé, rouge atténué sous l'horizon
r, g, b = im.split()
mask = Image.new('L', (1, H))
for y in range(H):
    t = y / H
    v = 0.0 if t < HORIZON else min(1.0, (t - HORIZON) / 0.12)
    mask.putpixel((0, y), int(150 * v))
mask = mask.resize((W, H))
b = Image.composite(b.point(lambda v: min(255, int(v * 1.14 + 6))), b, mask)
r = Image.composite(r.point(lambda v: int(v * 0.94)), r, mask)
im = Image.merge('RGB', (r, g, b))

# 4) vignettage discret (masque calculé en petit puis agrandi)
sw, sh = 180, 240
vig = Image.new('L', (sw, sh))
vp = vig.load()
for y in range(sh):
    for x in range(sw):
        d = (((x - sw / 2) / (sw / 2)) ** 2 + ((y - sh * 0.46) / (sh * 0.62)) ** 2) ** 0.5
        vp[x, y] = int(255 * max(0.0, 1 - 0.36 * max(0.0, d - 0.60) / 0.70))
vig = vig.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(W * 0.015))
im = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), vig)

im = im.filter(ImageFilter.UnsharpMask(radius=2.4, percent=58, threshold=3))
im.save(OUT, quality=94)
print(OUT, im.size)
