#!/usr/bin/env python3
"""📷 TRAITER UNE PHOTO — l'étalonnage maison, pas un filtre.

29/08/2026. Le patron envoie neuf photos de lui avec un téléphone et demande
« des photos très belles retouches, niveau Apple ».

⛔ CE QUE CE PROGRAMME NE FAIT PAS, ET NE FERA JAMAIS
Il ne change pas les vêtements, ne remodèle pas un visage, n'invente pas un
décor. Je n'ai aucun modèle de génération d'image dans cette session : je
travaille les pixels qui existent, je n'en fabrique pas de nouveaux. Dire le
contraire aurait été un mensonge coûteux — le patron aurait attendu une chemise
blanche qui ne serait jamais venue.

✅ CE QU'IL FAIT, ET QUI EST LE VRAI MÉTIER
Ce qu'un étalonneur fait sur une photo de campagne, dans l'ordre :
  1. BALANCE DES BLANCS — le mur crème et le carrelage orange renvoient leur
     couleur sur la peau et sur le polo. Mesuré : rouge +30 sur le bleu. On
     neutralise sur les hautes lumières (le mur EST blanc, il doit le redevenir).
  2. CADRAGE 4:5 — le format d'Instagram et de Facebook. Recadrer, ce n'est pas
     rogner : c'est décider où le regard entre.
  3. COURBE — noirs tenus, hautes lumières retenues. Une photo « à plat » n'est
     pas sous-exposée, elle manque de séparation.
  4. ÉTALONNAGE PARTAGÉ — ombres poussées vers notre marine (#0F2A5C). C'est ça
     qui fait qu'une photo « appartient » à une marque sans qu'on sache dire
     pourquoi. Apple fait exactement ça, en gris froid.
  5. VIGNETAGE + GRAIN — le vignetage ramène l'œil au sujet ; le grain empêche
     le dégradé de faire des bandes et enlève le côté « photo de téléphone ».

    python3 traiter.py <entrée.jpg> <sortie.jpg>

⚠️ CE PROGRAMME NE COMMITE RIEN. Les photos d'une personne ne rentrent pas dans
un dépôt PUBLIC avant que les droits soient écrits — c'est la règle qu'on
s'est donnée pour le neveu (voir CREDITS-FAMILLE.md).
"""
import sys

from PIL import Image, ImageEnhance, ImageFilter

FORMAT = (4, 5)                 # 4:5, le format des réseaux
MARINE = (15, 42, 92)           # #0F2A5C — les ombres vont vers lui
FORCE_OMBRES = 0.17             # au-delà, la peau vire au bleu


def balance_des_blancs(im):
    """Le mur EST blanc : on le force à le redevenir, la peau suit.

    On mesure sur le 5 % le plus clair (le mur, la lumière de la fenêtre) et
    non sur la moyenne : une moyenne inclut le carrelage orange, qui n'a
    aucune raison d'être neutre.
    """
    petite = im.resize((160, 213))
    px = list(petite.getdata())
    px.sort(key=lambda p: p[0] + p[1] + p[2], reverse=True)
    haut = px[:len(px) // 20]
    moy = [sum(c[i] for c in haut) / len(haut) for i in range(3)]
    cible = sum(moy) / 3
    tables = []
    for i in range(3):
        gain = cible / moy[i] if moy[i] else 1.0
        gain = max(0.82, min(1.18, gain))       # jamais violent : ça vire vite
        tables += [min(255, int(v * gain)) for v in range(256)]
    return im.point(tables)


def cadrer(im):
    """Recadre en 4:5 en gardant le HAUT : la tête ne se coupe jamais."""
    l, h = im.size
    vise = l * FORMAT[1] / FORMAT[0]
    if vise <= h:
        # on garde le haut et un peu d'air : le sujet est debout
        haut = int((h - vise) * 0.18)
        return im.crop((0, haut, l, haut + int(vise)))
    largeur = int(h * FORMAT[0] / FORMAT[1])
    g = (l - largeur) // 2
    return im.crop((g, 0, g + largeur, h))


def courbe(im):
    """Noirs tenus, hautes lumières retenues — une S douce, pas un contraste."""
    def f(v):
        x = v / 255
        # S de Hermite, atténuée : x*x*(3-2x) est trop dur sur les visages
        s = x * x * (3 - 2 * x)
        y = x * 0.42 + s * 0.58
        y = 0.035 + y * 0.945          # noirs légèrement levés : jamais bouchés
        return max(0, min(255, int(y * 255)))
    t = [f(v) for v in range(256)]
    return im.point(t * 3)


def etalonner(im):
    """Les ombres vers le marine de la marque. C'est la signature invisible."""
    lum = im.convert('L')
    ombre = Image.new('RGB', im.size, MARINE)
    # le masque : fort dans les ombres, nul dans les hautes lumières
    masque = lum.point(lambda v: int(FORCE_OMBRES * 255 * (1 - v / 255) ** 1.6))
    return Image.composite(Image.blend(im, ombre, 0.55), im, masque)


def vignetage(im, force=0.28):
    l, h = im.size
    # un dégradé radial fabriqué par redimensionnement : rapide et sans bandes
    petit = Image.new('L', (64, 80), 0)
    px = petit.load()
    for y in range(80):
        for x in range(64):
            dx, dy = (x - 31.5) / 31.5, (y - 39.5) / 39.5
            d = min(1.0, (dx * dx + dy * dy) ** 0.5 / 1.32)
            px[x, y] = int(255 * (d ** 2.4) * force)
    masque = petit.resize((l, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(l / 60))
    return Image.composite(Image.new('RGB', im.size, (0, 0, 0)), im, masque)


def grain(im, force=5):
    """Sans grain, l'étalonnage fait des bandes dans les dégradés du mur."""
    import random
    l, h = im.size
    bruit = Image.new('L', (l // 3, h // 3))
    bruit.putdata([128 + random.randint(-force, force) for _ in range(bruit.size[0] * bruit.size[1])])
    bruit = bruit.resize((l, h), Image.BICUBIC)
    return Image.blend(im, Image.merge('RGB', (bruit, bruit, bruit)), 0.055)


def traiter(entree, sortie):
    im = Image.open(entree).convert('RGB')
    im = balance_des_blancs(im)
    im = cadrer(im)
    im = courbe(im)
    im = etalonner(im)
    im = ImageEnhance.Color(im).enhance(0.90)      # −10 % : le carrelage criait
    im = vignetage(im)
    im = grain(im)
    im = im.filter(ImageFilter.UnsharpMask(radius=2.4, percent=58, threshold=3))
    im.save(sortie, quality=94, subsampling=0)
    print(f"OK -> {sortie}  {im.size[0]}x{im.size[1]}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    traiter(sys.argv[1], sys.argv[2])
