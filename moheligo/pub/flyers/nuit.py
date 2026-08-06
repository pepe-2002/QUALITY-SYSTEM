#!/usr/bin/env python3
"""Traitement nocturne d'une photo de jour (pour le flyer « nuit »).

horizon.jpg (plage de jour) -> horizon-nuit.jpg : bascule bleu nuit, îles en
silhouette, étoiles discrètes au-dessus de l'horizon, lune et son reflet sur
l'eau. Aucune photo de nuit n'était disponible ; c'est un étalonnage, pas un
faux document.
"""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

SRC, OUT = '../photos/horizon.jpg', 'horizon-nuit.jpg'
random.seed(7)  # rendu reproductible

im = Image.open(SRC).convert('RGB')
W, H = im.size
HORIZON = 0.52          # ligne d'horizon (fraction de la hauteur)
MOON = (0.80, 0.16)     # position de la lune

# 1) bascule nuit : canaux séparés, le bleu domine, les hautes lumières tombent
r, g, b = im.split()
r = r.point(lambda v: int((v / 255) ** 1.35 * 255 * 0.30))
g = g.point(lambda v: int((v / 255) ** 1.28 * 255 * 0.40))
b = b.point(lambda v: int((v / 255) ** 1.10 * 255 * 0.55) + 8)
night = Image.merge('RGB', (r, g, b))
night = ImageEnhance.Contrast(night).enhance(1.18)

# 2) le ciel s'assombrit vers le haut, la plage vers le bas
grad = Image.new('L', (1, H))
for y in range(H):
    t = y / H
    if t < HORIZON:                        # ciel : sombre en haut
        v = int(178 * (1 - t / HORIZON) ** 1.25)
    else:                                  # premier plan : sombre en bas
        v = int(120 * ((t - HORIZON) / (1 - HORIZON)) ** 1.6)
    grad.putpixel((0, y), v)
night = Image.composite(Image.new('RGB', (W, H), (4, 10, 28)),
                        night, grad.resize((W, H)))

d = ImageDraw.Draw(night, 'RGBA')

# 3) étoiles (uniquement au-dessus de l'horizon, densité modérée)
sky = int(H * HORIZON * 0.92)
for _ in range(260):
    x, y = random.randrange(W), random.randrange(int(H * 0.02), sky)
    fade = 1 - (y / sky) ** 1.6           # moins d'étoiles près de l'horizon
    a = int(random.uniform(60, 210) * fade)
    if a < 25:
        continue
    rr = 1.6 if a > 165 else 1.0
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 253, 240, a))

# 4) lune + halo
mx, my = int(W * MOON[0]), int(H * MOON[1])
halo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
for rad, a in ((int(W * .085), 26), (int(W * .055), 34), (int(W * .032), 52)):
    hd.ellipse([mx - rad, my - rad, mx + rad, my + rad], fill=(198, 216, 255, a))
halo = halo.filter(ImageFilter.GaussianBlur(W * 0.02))
night = Image.alpha_composite(night.convert('RGBA'), halo).convert('RGB')
d = ImageDraw.Draw(night, 'RGBA')
mr = int(W * 0.0165)
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(246, 248, 255, 255))

# 5) reflet de lune sur l'eau : traits horizontaux qui s'élargissent
refl = Image.new('RGBA', (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(refl)
y0, y1 = int(H * HORIZON), int(H * 0.645)
for y in range(y0, y1, 3):
    t = (y - y0) / (y1 - y0)
    half = int(W * (0.012 + 0.075 * t))
    a = int(70 * (1 - t) ** 1.3)
    if a <= 2:
        continue
    jitter = random.randint(-int(W * .012), int(W * .012))
    rd.line([mx - half + jitter, y, mx + half + jitter, y],
            fill=(190, 214, 255, a), width=2)
refl = refl.filter(ImageFilter.GaussianBlur(3))
night = Image.alpha_composite(night.convert('RGBA'), refl).convert('RGB')

night.filter(ImageFilter.SMOOTH).save(OUT, quality=93)
print(OUT, night.size)
