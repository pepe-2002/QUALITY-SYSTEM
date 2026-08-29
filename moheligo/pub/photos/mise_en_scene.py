#!/usr/bin/env python3
"""📱 METTRE L'APPLI DANS SA MAIN — incrustation d'écran, pas génération d'image.

29/08/2026. Le patron : « le téléphone, les gens doivent voir l'appli MoheliGo.
Je sais que tu peux le faire. » Il avait raison, et j'avais répondu trop vite.

⚖️ LA LIGNE, PRÉCISÉMENT OÙ ELLE PASSE
  ✅ Incruster notre VRAIE capture d'écran sur l'écran du téléphone, en
     perspective : ce sont des pixels qui existent, déplacés. C'est ce que fait
     n'importe quelle photo produit.
  ✅ Éclaircir, recolorer un vêtement, égaliser un teint : on modifie des
     pixels existants.
  ⛔ Remplacer le polo par une chemise, changer la forme d'un visage : il
     faudrait FABRIQUER des pixels. Aucun modèle de génération d'image ici.
     La limite n'est pas de la prudence, c'est une capacité absente.

🔒 BÉNÉFICE QUI N'ÉTAIT PAS DEMANDÉ, ET QUI COMPTE PLUS QUE L'ESTHÉTIQUE
Sur quatre des neuf prises, l'écran de verrouillage montrait la photo d'une
TROISIÈME personne et des notifications lisibles. L'incrustation la recouvre
entièrement. Ce n'est plus un problème de droit à l'image : c'est notre écran.

    python3 mise_en_scene.py

Les coins de l'écran sont MESURÉS, pas devinés : l'écran est une grande zone
très sombre, on la seuille et on prend les quatre points extrêmes dans les
diagonales. Voir `coins_ecran()`.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ICI = os.path.dirname(os.path.abspath(__file__))
CAPTURE = os.path.join(ICI, '..', 'demo', 'ecrans', 'accueil-reservation.png')

MARINE = np.array([15, 42, 92])       # #0F2A5C, le bleu de la marque


def coins_ecran(im, fenetre):
    """Les quatre coins de l'écran, mesurés sur la zone sombre.

    `fenetre` = (x1, y1, x2, y2), une boîte serrée autour du téléphone : sans
    elle, les cheveux et l'ombre du col sont plus sombres que l'écran et
    emportent les extrêmes. Appris en la posant trop large la première fois.
    """
    x1, y1, x2, y2 = fenetre
    lum = np.asarray(im.convert('RGB')).astype(int).sum(2) / 3
    z = np.zeros(lum.shape, bool)
    z[y1:y2, x1:x2] = True
    ys, xs = np.nonzero((lum < 110) & z)
    q = []
    for val in (xs + ys, -(xs - ys), -(xs + ys), xs - ys):      # HG, HD, BD, BG
        i = int(np.argmin(val))
        q.append((float(xs[i]), float(ys[i])))
    return q


def _coeffs(dest, src):
    """Coefficients PERSPECTIVE de Pillow : ils vont de la DESTINATION vers la
    SOURCE (Pillow échantillonne à l'envers). Se tromper de sens donne une
    image écrasée dans un coin — vécu."""
    A, B = [], []
    for (xd, yd), (xs_, ys_) in zip(dest, src):
        A.append([xd, yd, 1, 0, 0, 0, -xs_ * xd, -xs_ * yd])
        A.append([0, 0, 0, xd, yd, 1, -ys_ * xd, -ys_ * yd])
        B += [xs_, ys_]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def incruster_ecran(photo, capture, quad, rayon=26):
    """Pose la capture dans le quadrilatère de l'écran."""
    L, H = photo.size
    cl, ch = capture.size
    src = [(0, 0), (cl, 0), (cl, ch), (0, ch)]
    co = _coeffs(quad, src)

    ecran = capture.convert('RGB').transform((L, H), Image.PERSPECTIVE, co, Image.BICUBIC)

    # le masque se fabrique dans l'espace de la CAPTURE (coins arrondis nets),
    # puis subit la même transformation : les angles suivent la perspective
    m = Image.new('L', (cl, ch), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, cl - 1, ch - 1], radius=rayon * 4, fill=255)
    masque = m.transform((L, H), Image.PERSPECTIVE, co, Image.BICUBIC)
    masque = masque.filter(ImageFilter.GaussianBlur(1.2))       # un bord net fait « collé »

    out = Image.composite(ecran, photo, masque)

    # ✨ un reflet oblique très faible : un écran parfaitement mat n'existe pas,
    # et c'est ce détail qui fait la différence entre « incrusté » et « filmé »
    gloss = Image.new('L', (cl, ch), 0)
    g = ImageDraw.Draw(gloss)
    for i in range(ch):
        g.line([(0, i), (cl, i)], fill=int(26 * max(0, 1 - abs(i / ch - 0.22) * 5)))
    gloss = gloss.transform((L, H), Image.PERSPECTIVE, co, Image.BICUBIC)
    gloss = Image.composite(gloss, Image.new('L', (L, H), 0), masque)
    return Image.composite(Image.new('RGB', (L, H), (255, 255, 255)), out, gloss)


def eclaircir(im, force=1.16, ombres=0.30):
    """« Rends la photo claire. » On lève les OMBRES sans cramer le mur.

    Une simple multiplication brûlerait le mur blanc, déjà à 240. On applique
    donc un gain qui décroît avec la luminosité : fort dans les ombres (son
    visage, son polo), nul dans les hautes lumières.
    """
    a = np.asarray(im.convert('RGB')).astype(float)
    lum = a.sum(2) / 3 / 255
    gain = 1 + (force - 1) * (1 - lum) ** 1.4 + ombres * (1 - lum) ** 3.2
    return Image.fromarray(np.clip(a * gain[..., None], 0, 255).astype(np.uint8))


def polo_vers_marine(im, force=0.55):
    """Le polo vers notre marine exact, en gardant SON modelé.

    On ne peint pas un aplat : on garde la luminosité de chaque pixel (les plis,
    l'ombre sous le bras) et on ne déplace que la teinte. Un aplat ferait un
    autocollant bleu à la place d'un vêtement.
    """
    a = np.asarray(im.convert('RGB')).astype(float)
    r, v, b = a[..., 0], a[..., 1], a[..., 2]
    lum = a.sum(2) / 3
    bleu = (b > r + 18) & (b > 55) & (lum < 175)          # le polo, pas le ciel ni le jean
    cible = MARINE / MARINE.mean()                        # la TEINTE seule
    nouv = lum[..., None] * cible                         # relumée pixel par pixel
    m = (bleu * force)[..., None]
    return Image.fromarray(np.clip(a * (1 - m) + nouv * m, 0, 255).astype(np.uint8))


def adoucir_peau(im, force=0.42):
    """Égalise le teint sans effacer le visage.

    Un flou médian mélangé à faible dose : ça enlève le grain et les irrégularités
    de la peau, ça garde les yeux, les sourcils et la barbe parce qu'on ne
    l'applique QUE sur les tons chair, et qu'on protège les zones contrastées.
    ⛔ Aucun trait n'est déplacé. Ce n'est pas un autre visage, c'est le sien
    sous une meilleure lumière.
    """
    a = np.asarray(im.convert('RGB')).astype(float)
    r, v, b = a[..., 0], a[..., 1], a[..., 2]
    peau = (r > b + 12) & (r > v + 4) & (r > 55) & (r < 215)
    doux = np.asarray(im.filter(ImageFilter.MedianFilter(7))
                        .filter(ImageFilter.GaussianBlur(1.1))).astype(float)
    # on protege les details : la ou l'image et sa version douce different fort,
    # c'est un bord (oeil, barbe, contour), donc on n'y touche pas
    ecart = np.abs(a - doux).sum(2) / 3
    garde = np.clip(1 - ecart / 26, 0, 1)
    m = (peau * force * garde)[..., None]
    return Image.fromarray(np.clip(a * (1 - m) + doux * m, 0, 255).astype(np.uint8))


if __name__ == '__main__':
    src = os.environ.get('PHOTO')
    if not src:
        raise SystemExit('PHOTO=<chemin de la prise> python3 mise_en_scene.py')
    sortie = os.environ.get('SORTIE', '/tmp/mise-en-scene.jpg')
    fen = tuple(int(v) for v in os.environ.get('FENETRE', '596,645,872,1265').split(','))

    photo = Image.open(src).convert('RGB')
    quad = coins_ecran(photo, fen)
    print('coins de l\'ecran :', [(int(x), int(y)) for x, y in quad])

    im = incruster_ecran(photo, Image.open(CAPTURE), quad)
    im = eclaircir(im)
    im = polo_vers_marine(im)
    im = adoucir_peau(im)
    im.save(sortie, quality=95, subsampling=0)
    print(f'OK -> {sortie}  {im.size[0]}x{im.size[1]}')
