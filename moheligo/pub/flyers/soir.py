#!/usr/bin/env python3
"""Étalonnage « fin de journée » de notre photo de vedette, pour le flyer du soir.

../photos/vedette-mer.jpg (pleine mer, aucune personne) -> vedette-soir.jpg

Méthode d'étalonneur, pas de filtre :
  1. base : saturation, contraste, exposition ;
  2. le CIEL est remplacé par un dégradé de crépuscule (indigo -> ambre) fondu
     à 82 % sur le ciel d'origine — c'est ce qui fait la fin de journée ;
  3. l'EAU reste froide (bleu renforcé, rouge atténué), mais les crêtes (les
     hautes lumières uniquement) reçoivent de l'ambre : c'est le reflet du
     soleil couchant, et c'est ce détail qui rend la scène crédible ;
  4. soleil bas : disque + halo atmosphérique ;
  5. chemin de lumière sur l'eau ;
  6. bloom léger (hautes lumières floutées reposées en écran) ;
  7. vignettage et netteté.
⚠️ Le bloom à forte dose lave l'image et tue le split-toning : rester sous 0.35.
"""
import random
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

SRC, OUT = '../photos/vedette-mer.jpg', 'vedette-soir.jpg'
HORIZON = 0.135
SUN = (0.520, 0.112)

im = Image.open(SRC).convert('RGB')
W, H = im.size
random.seed(11)

# 1) base
im = ImageEnhance.Color(im).enhance(1.22)
im = ImageEnhance.Contrast(im).enhance(1.10)
im = ImageEnhance.Brightness(im).enhance(0.96)

# 2) ciel de crépuscule
hy = int(H * HORIZON)
sky = Image.new('RGB', (1, hy))
for y in range(hy):
    t = y / max(1, hy - 1)                      # 0 en haut, 1 à l'horizon
    c = (int(38 + (232 - 38) * t ** 1.7),
         int(58 + (146 - 58) * t ** 1.5),
         int(116 + (86 - 116) * t ** 1.2))
    sky.putpixel((0, y), c)
sky = sky.resize((W, hy))
band = im.crop((0, 0, W, hy))
im.paste(Image.blend(band, sky, 0.82), (0, 0))
# raccord doux juste sous l'horizon
soft = Image.new('RGB', (1, H))
for y in range(H):
    t = y / H
    v = max(0.0, 1 - abs(t - HORIZON) / 0.085)
    soft.putpixel((0, y), (int(72 * v), int(38 * v), int(6 * v)))
im = ImageChops.add(im, soft.resize((W, H)))

# 3) eau froide, crêtes ambrées
r, g, b = im.split()
water = Image.new('L', (1, H))
for y in range(H):
    water.putpixel((0, y), int(150 * min(1.0, max(0.0, (y / H - HORIZON) / 0.10))))
water = water.resize((W, H))
b = Image.composite(b.point(lambda v: min(255, int(v * 1.12 + 6))), b, water)
r = Image.composite(r.point(lambda v: int(v * 0.82)), r, water)
im = Image.merge('RGB', (r, g, b))
# ambre uniquement sur les hautes lumières (les crêtes)
lum = im.convert('L')
crests = lum.point(lambda v: 0 if v < 150 else min(255, int((v - 150) * 2.6)))
crests = Image.composite(crests, Image.new('L', (W, H), 0), water)
im = ImageChops.add(im, Image.merge('RGB', (
    crests.point(lambda v: int(v * .30)),
    crests.point(lambda v: int(v * .15)),
    crests.point(lambda v: 0))))

# 4) soleil + halo
sx, sy = int(W * SUN[0]), int(H * SUN[1])
halo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(halo)
for rad, col in ((int(W * .215), (255, 168, 72, 20)),
                 (int(W * .115), (255, 186, 96, 28)),
                 (int(W * .052), (255, 214, 140, 44)),
                 (int(W * .024), (255, 240, 200, 78))):
    hd.ellipse([sx - rad, sy - rad, sx + rad, sy + rad], fill=col)
halo = halo.filter(ImageFilter.GaussianBlur(W * 0.022))
im = Image.alpha_composite(im.convert('RGBA'), halo).convert('RGB')
d = ImageDraw.Draw(im, 'RGBA')
sr = int(W * 0.0062)
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 244, 214, 210))

# 5) chemin de lumière
path = Image.new('RGBA', (W, H), (0, 0, 0, 0))
pd = ImageDraw.Draw(path)
y0, y1 = int(H * (HORIZON + .008)), int(H * 0.88)
for y in range(y0, y1, 3):
    t = (y - y0) / (y1 - y0)
    half = int(W * (0.009 + 0.10 * t))
    a = int(88 * (1 - t) ** 1.25)
    if a <= 2:
        continue
    j = random.randint(-int(W * .013), int(W * .013))
    pd.line([sx - half + j, y, sx + half + j, y], fill=(255, 206, 128, a), width=2)
im = Image.alpha_composite(im.convert('RGBA'),
                           path.filter(ImageFilter.GaussianBlur(4))).convert('RGB')

# 6) bloom léger
lum = im.convert('L')
mask_hi = lum.point(lambda v: 0 if v < 192 else min(255, int((v - 192) * 3.0)))
bloom = Image.composite(im, Image.new('RGB', (W, H), (0, 0, 0)), mask_hi)
bloom = bloom.filter(ImageFilter.GaussianBlur(W * 0.016))
im = ImageChops.screen(im, ImageChops.multiply(bloom, Image.new('RGB', (W, H), (78, 78, 78))))

# 7) vignettage + netteté
sw, sh = 180, 135
vig = Image.new('L', (sw, sh)); vp = vig.load()
for y in range(sh):
    for x in range(sw):
        dd = (((x - sw / 2) / (sw / 2)) ** 2 + ((y - sh * 0.44) / (sh * 0.66)) ** 2) ** 0.5
        vp[x, y] = int(255 * max(0.0, 1 - 0.40 * max(0.0, dd - 0.56) / 0.72))
vig = vig.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(W * 0.015))
im = Image.composite(im, Image.new('RGB', (W, H), (3, 8, 22)), vig)
im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=58, threshold=3))
im.save(OUT, quality=94)
print(OUT, im.size)
