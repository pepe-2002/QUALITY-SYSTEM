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


def profondeur(im, centre, rayon, force=14):
    """Simule une faible profondeur de champ : net sur le téléphone, flou ailleurs.

    C'est LE geste qui sépare une photo de téléphone d'une photo de campagne.
    Un capteur de téléphone a tout net du premier plan à l'arrière-plan ; l'œil
    lit ça comme « amateur » sans savoir pourquoi. On refabrique la mise au
    point : net dans le disque du sujet, flou croissant au-delà.
    ⚠️ Le dégradé du masque doit être LONG (ici 1,9 × le rayon). Une transition
    courte fait une auréole nette autour du sujet — le défaut classique.
    """
    from PIL import ImageDraw
    L, H = im.size
    cx, cy = centre
    flou = im.filter(ImageFilter.GaussianBlur(force))
    # ⚠️ ON PEINT DU PLUS GRAND AU PLUS PETIT, et le fond part à 0 (tout flou).
    # Fait dans l'autre sens la première fois : chaque grand disque, plus sombre,
    # recouvrait le petit disque net déjà posé — et TOUTE l'image sortait floue,
    # y compris le téléphone. Un dégradé se peint de l'extérieur vers le centre.
    m = Image.new('L', (L // 4, H // 4), 0)
    d = ImageDraw.Draw(m)
    etapes = 44
    for i in reversed(range(etapes)):
        r = (rayon * (1 + 1.9 * i / etapes)) / 4
        d.ellipse([cx / 4 - r, cy / 4 - r, cx / 4 + r, cy / 4 + r],
                  fill=int(255 * (1 - i / etapes) ** 1.3))
    m = m.resize((L, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(L / 40))
    return Image.composite(im, flou, m)


def remplacer_mur(im, couleur=(15, 42, 92), lum_bas=155, lum_haut=200,
                  sat_bas=0.10, sat_haut=0.24, adoucir=2.6):
    """Remplace le mur par une couleur de marque, sans détourage manuel.

    29/08/2026. Le patron : « on utilise toujours nos couleurs, on cherche la
    solution sur le mur. » Le mur est le dernier défaut de la prise — taché,
    gris, sans intérêt. On ne peut pas le nettoyer ; on peut le SUPPRIMER.

    📐 CE QUI REND LA SÉPARATION POSSIBLE, ET C'EST MESURÉ :
        mur   luminosité 210-238   saturation 0,02-0,11
        peau  luminosité 170       saturation 0,30
        polo  luminosité  83       saturation 0,76
    La peau est à trois fois la saturation maximale du mur : la marge est
    confortable. On combine donc DEUX critères — clair ET désaturé — parce que
    la luminosité seule prendrait les doigts éclairés, et la saturation seule
    prendrait les ombres neutres du châssis.

    ⚠️ ON NE GARDE QUE LES ZONES TOUCHANT UN BORD DE L'IMAGE. Sans ça, le blanc
    des cartes de l'appli (clair et désaturé lui aussi) serait pris pour du mur
    et l'écran se remplirait de marine.

    ⚠️ ET ON ADOUCIT LE MASQUE : le mur est flou (profondeur de champ), donc le
    contour du sujet est progressif. Un masque net y découperait une silhouette
    en carton.
    """
    from scipy import ndimage
    a = np.asarray(im.convert('RGB')).astype(float)
    mx, mn = a.max(2), a.min(2)
    sat = (mx - mn) / np.maximum(mx, 1)
    lum = a.sum(2) / 3

    f = np.clip((lum - lum_bas) / (lum_haut - lum_bas), 0, 1)
    g = np.clip((sat_haut - sat) / (sat_haut - sat_bas), 0, 1)
    score = f * g

    lab, n = ndimage.label(score > 0.5)
    bords = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    bords.discard(0)
    relie = np.isin(lab, list(bords))
    score = score * ndimage.binary_dilation(relie, np.ones((9, 9)))

    # ⚠️ ON DURCIT LE SCORE. Sans ça, le mur n'est remplacé qu'À MOITIÉ là où il
    # est un peu plus sombre (ombre, vignetage) : le fond sort à R≈36 au lieu de
    # R=15, et cet écart se voit comme un TRAIT CLAIR au bord de la photo dès
    # qu'elle est posée sur la page. Signalé par le patron le 29/08.
    # 📌 Un fond « presque » de la bonne couleur est pire qu'un fond franchement
    # différent : l'œil ne voit pas une nuance, il voit une frontière.
    score = np.clip(score * 1.7, 0, 1)

    m = Image.fromarray((score * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(adoucir))
    fond = Image.new('RGB', im.size, tuple(couleur))
    return Image.composite(fond, im.convert('RGB'), m)


def telephone_propre(capture, larg=930, haut=1995, chassis=(8, 19, 44), arrondi=0.132):
    """Dessine le châssis propre des flyers 39/40, avec la capture dedans.

    29/08/2026. Le patron : « utilise la photo de téléphone d'hier, couvre mon
    téléphone en entier. » Sa coque est transparente, jaunie et fendue ; la
    recouvrir en entier vaut mieux que d'incruster seulement l'écran.
    Le châssis reprend exactement celui des flyers 39 et 40 : marine très
    sombre, coins très arrondis, encoche centrée.
    """
    tel = Image.new('RGBA', (larg, haut), (0, 0, 0, 0))
    d = ImageDraw.Draw(tel)
    # ⚠️ `arrondi` un peu MOINS rond que le vrai téléphone (0,132 au lieu de
    # 0,155) : la coque du patron a des renforts d'angle qui débordent, et un
    # châssis trop arrondi les laissait affleurer en doré dans les coins.
    d.rounded_rectangle([0, 0, larg - 1, haut - 1], radius=int(larg * arrondi),
                        fill=chassis + (255,))
    b = int(larg * 0.039)                                  # la tranche du châssis
    ecran = capture.convert('RGB').resize((larg - 2 * b, haut - 2 * b), Image.LANCZOS)
    m = Image.new('L', ecran.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, ecran.size[0] - 1, ecran.size[1] - 1],
                                        radius=int(larg * 0.125), fill=255)
    tel.paste(ecran, (b, b), m)
    d.rounded_rectangle([larg // 2 - int(larg * .19), int(haut * .011),
                         larg // 2 + int(larg * .19), int(haut * .011) + int(haut * .019)],
                        radius=int(haut * .010), fill=chassis + (255,))
    return tel


def couvrir_telephone(photo, tel, quad, doigts=(), adoucir=1.4):
    """Pose le châssis propre sur le corps entier du téléphone, en perspective.

    `doigts` : les zones à REMETTRE PAR-DESSUS, en (x, y, rayon). Ici seul le
    pouce mord le bord droit de la coque — les quatre autres doigts passent
    DERRIÈRE le téléphone, donc ils ne sont jamais recouverts.
    ⚠️ On ne peut pas les retrouver par la couleur : la coque est transparente et
    laisse voir la peau à travers. Mesuré — coque : lum 140, sat 0,43 ; pouce :
    lum 146, sat 0,45. Deux valeurs identiques. D'où le repérage à la main.
    """
    L, H = photo.size
    tl, th = tel.size
    co = _coeffs(quad, [(0, 0), (tl, 0), (tl, th), (0, th)])
    corps = tel.convert('RGB').transform((L, H), Image.PERSPECTIVE, co, Image.BICUBIC)
    m = tel.split()[3].transform((L, H), Image.PERSPECTIVE, co, Image.BICUBIC)
    m = m.filter(ImageFilter.GaussianBlur(adoucir))
    out = Image.composite(corps, photo.convert('RGB'), m)

    if doigts:
        md = Image.new('L', (L, H), 0)
        dd = ImageDraw.Draw(md)
        for x, y, r in doigts:
            dd.ellipse([x - r, y - r, x + r, y + r], fill=255)
        md = md.filter(ImageFilter.GaussianBlur(r * 0.28))
        out = Image.composite(photo.convert('RGB'), out, md)
    return out
