#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LE MOTEUR DES FILMS DE SENSIBILISATION ROYAL AIR.

    python3 film.py agence      → RoyalAir-accueil-agence.mp4  (+ version légère)
    python3 film.py escale      → RoyalAir-accueil-escale.mp4  (+ version légère)
    python3 film.py tout
    python3 film.py agence --muet     → la même chose sans voix off

Ce fichier ne contient AUCUN texte du film : tout le contenu est dans
`scenarios.py`. Ici, il n'y a que la fabrication de l'image et le montage.
Corriger une phrase = corriger `scenarios.py`, jamais le .mp4.

📌 POURQUOI DES CARTES DESSINÉES ET PAS DES IMAGES D'ARCHIVE
Une vidéo de sensibilisation trouvée sur internet montre l'aéroport de
quelqu'un d'autre, avec ses règles et son logo. On ne peut ni y coller le nôtre
(c'est l'œuvre d'un tiers), ni faire dire à un film étranger ce que disent
notre GOM et nos procédures. Des cartes fabriquées ici n'appartiennent qu'à
Royal Air : elles citent nos références, nos escales, notre flotte.

📌 UNE VOIX OFF, ET TOUT ÉCRIT QUAND MÊME
Le film est destiné au groupe WhatsApp, où une vidéo démarre SANS LE SON : une
partie des agents la regardera muette, dans un couloir ou dans un bus. Tout ce
qui compte est donc écrit en grand à l'écran — et dit par la voix off pour les
autres. Le film doit fonctionner entièrement dans les deux cas ; aucune
information n'existe seulement à l'oreille, aucune seulement à l'œil.
La voix est fabriquée par `voix.py`, et c'est ELLE qui commande la durée des
images : chacune dure au moins le temps de sa phrase. On n'accélère jamais une
voix pour la faire rentrer dans un montage — cela s'entend toujours.

FORMAT : 1080 × 1920 (vertical plein écran de téléphone), 25 im/s, H.264.
Deux fichiers par film — le complet, et un allégé sous la limite WhatsApp.
"""
import os
import subprocess
import sys
import textwrap as _tw

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
POLICES = os.path.join(ICI, "polices")
TRAVAIL = os.path.join(ICI, ".travail")          # images intermédiaires, jetables

# ---------------------------------------------------------------- l'identité
# 🎨 LES COULEURS SONT CELLES DU VRAI LOGO ROYAL AIR, relevées au pixel sur
# l'en-tête officielle de la compagnie (courrier « Demande de clearance
# positionnement F100 5Y-MMX » du 31/08/2026, fourni par le patron) :
#   · le bleu de la bande d'en-tête ......... #004AAD
#   · le bleu du mot ROYAL AIR .............. #1237A1
#   · le rouge de la sphère ................. #EC313A
#   · le jaune de l'orbite .................. #FDC20C
# Rien n'est inventé ni « approché » : un film aux couleurs approximatives se
# reconnaît immédiatement comme un travail fait à côté de la marque.
BLEU_MARQUE = (0, 74, 173)       # #004AAD  le bleu officiel de l'en-tête
BLEU_LOGO   = (18, 55, 161)      # #1237A1  le bleu du mot ROYAL AIR
ROUGE       = (236, 49, 58)      # #EC313A  le rouge de la sphère
OR          = (253, 194, 12)     # #FDC20C  le jaune de l'orbite

NAVY       = (5, 32, 78)         # le fond : le bleu de marque, assombri
NAVY_FONCE = (3, 21, 54)         # fond des cartes graves
ROYAL      = BLEU_MARQUE
CIEL       = (74, 141, 240)      # le bleu éclairci, lisible sur fond sombre
BLANC      = (255, 255, 255)
CRAIE      = (222, 232, 248)     # le blanc du corps de texte, moins agressif
BLEU_PALE  = (135, 175, 235)     # les surtitres
VERT       = (46, 190, 108)      # le vert du « dites » — hors marque, mais un
                                 # bon/mauvais sans vert ni rouge ne se lit pas
LOGO_FICHIER = os.path.join(ICI, "marque", "royal-air-logo.png")
_LOGO = None

L, H = 1080, 1920
MARGE = 84
IPS = 25

# Le silence qui suit chaque phrase de la voix off.
#
# 🗣️ PORTÉ DE 0,45 À 1,0 s LE 04/09/2026 : « si tu passes de 1 à 2, laisse la
# voix souffler […] même si la vidéo fait 10 min, si la voix paraît naturelle
# et calme et que les gens ont envie d'écouter, c'est ce qui gagne. »
#
# C'est le temps entre la fin d'un point et l'apparition du suivant. À 0,45 s
# le point suivant tombait pendant qu'on digérait encore le précédent. À 1 s,
# on a le temps de faire le lien entre ce qu'on vient d'entendre et ce qu'on
# vient de lire — et c'est tout l'intérêt d'un film de sensibilisation.
# La durée du film n'est plus une contrainte : elle a été explicitement
# déclassée au profit du calme.
RESPIRATION = 1.0


def police(nom, taille):
    return ImageFont.truetype(os.path.join(POLICES, nom + ".ttf"), taille)


# ------------------------------------------------------------------ le texte
def beau(txt):
    """La typographie française : apostrophe courbe, points de suspension d'un
    seul signe, espace insécable avant les deux-points et les guillemets. Une
    apostrophe droite dans un film d'entreprise se voit tout de suite."""
    return (txt.replace("'", "\u2019").replace("...", "\u2026")
               .replace(" :", "\u202f:").replace(" ;", "\u202f;")
               .replace("\u00ab ", "\u00ab\u202f").replace(" \u00bb", "\u202f\u00bb"))


def largeur(d, txt, ft, espacement=0):
    if not txt:
        return 0
    n = d.textlength(txt, font=ft)
    return n + espacement * max(0, len(txt) - 1)


def ecrire(d, xy, txt, ft, couleur, espacement=0, ancre="la"):
    """Écrit un texte, avec interlettrage optionnel (les capitales espacées de
    la marque). PIL ne sait pas espacer : on pose les lettres une par une."""
    txt = beau(txt)
    x, y = xy
    if espacement == 0:
        d.text((x, y), txt, font=ft, fill=couleur, anchor=ancre)
        return
    if ancre[0] == "m":
        x -= largeur(d, txt, ft, espacement) / 2
    elif ancre[0] == "r":
        x -= largeur(d, txt, ft, espacement)
    for c in txt:
        d.text((x, y), c, font=ft, fill=couleur, anchor="l" + ancre[1])
        x += d.textlength(c, font=ft) + espacement


def couper(d, txt, ft, largeur_max):
    """Découpe un paragraphe en lignes qui tiennent dans la largeur donnée."""
    lignes, courante = [], ""
    for mot in beau(txt).split():
        essai = (courante + " " + mot).strip()
        if d.textlength(essai, font=ft) <= largeur_max or not courante:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def bloc(d, x, y, txt, ft, couleur, largeur_max, interligne, ancre="la"):
    """Pose un paragraphe et renvoie le y d'après."""
    for ligne in couper(d, txt, ft, largeur_max):
        d.text((x, y), ligne, font=ft, fill=couleur, anchor=ancre)
        y += interligne
    return y


# ------------------------------------------------------------------- le logo
def logo(img, d, x, y, hauteur):
    """LE VRAI LOGO, posé tel quel sur une plaque blanche.

    📌 POURQUOI UNE PLAQUE BLANCHE ET NON LE LOGO « DÉTOURÉ »
    Le logo Royal Air écrit son nom en bleu foncé. Détouré sur un fond marine,
    ce bleu disparaît : le mot ROYAL AIR devient illisible et on se retrouve à
    « corriger » le logo — c'est-à-dire à le déformer. La règle de toutes les
    compagnies est la même : sur fond sombre, le logo va dans une réserve
    blanche. Il reste exactement lui-même, et il reste lisible."""
    global _LOGO
    if _LOGO is None:
        _LOGO = Image.open(LOGO_FICHIER).convert("RGB")
    lg = int(hauteur * _LOGO.width / _LOGO.height)
    marge = int(hauteur * 0.16)
    d.rounded_rectangle([x, y, x + lg + 2 * marge, y + hauteur + 2 * marge],
                        radius=int(hauteur * 0.20), fill=BLANC)
    img.paste(_LOGO.resize((lg, hauteur), Image.LANCZOS), (x + marge, y + marge))
    return lg + 2 * marge


# ------------------------------------------------------------------ la carte
def fond(grave=False):
    """Le fond de toutes les cartes : marine, avec une lueur en haut à droite
    (le ciel du chevron) et une trame de chevrons très basse, pour que l'image
    ne soit jamais un aplat mort à la compression."""
    base = NAVY_FONCE if grave else NAVY
    img = Image.new("RGB", (L, H), base)
    lueur = Image.new("RGB", (L, H), base)
    dl = ImageDraw.Draw(lueur)
    cx, cy = L * 0.78, H * 0.16
    for i in range(46, 0, -1):
        r = i * 26
        k = (46 - i) / 46.0
        c = tuple(int(base[j] + (ROYAL[j] - base[j]) * 0.16 * (1 - k) ** 2) for j in range(3))
        dl.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
    img = Image.blend(img, lueur, 0.9)
    d = ImageDraw.Draw(img)
    for i in range(-2, 14):                       # la trame de chevrons
        y = i * 190 + 60
        d.line([(-60, y + 260), (L * 0.5, y), (L + 60, y + 260)],
               fill=tuple(int(base[j] + 12) for j in range(3)), width=3)
    return img


def entete(img, d, chapitre, avancement=None):
    """Le bandeau du haut : l'emblème, le nom, et le chapitre en cours.
    Il est sur TOUTES les cartes — sur WhatsApp une vidéo est souvent reprise
    en capture d'écran, chaque image doit dire d'où elle vient."""
    lg = logo(img, d, MARGE, 70, 62)
    ecrire(d, (MARGE + lg + 26, 82), "ROYAL AIR", police("Inter-700", 34), BLANC, espacement=5)
    ecrire(d, (MARGE + lg + 26, 124), "DÉPARTEMENT QUALITÉ", police("Inter-500", 21),
           BLEU_PALE, espacement=3)
    if chapitre:
        ft = police("Inter-700", 22)
        lg = largeur(d, chapitre.upper(), ft, 3)
        x2 = L - MARGE
        d.rounded_rectangle([x2 - lg - 34, 82, x2, 128], radius=23,
                            fill=(20, 52, 94), outline=(44, 84, 140), width=2)
        ecrire(d, (x2 - lg / 2 - 17, 95), chapitre.upper(), ft, CIEL,
               espacement=3, ancre="ma")
    d.line([(MARGE, 176), (L - MARGE, 176)], fill=(30, 62, 116), width=2)
    if avancement:
        # 📌 Un film de cinq minutes sur un téléphone, sans savoir combien il en
        # reste, se ferme au bout de deux. La barre dit « tu es aux trois quarts ».
        d.rectangle([MARGE, 174, MARGE + int((L - 2 * MARGE) * avancement), 180], fill=OR)


def pied(d, mention="Usage interne · groupe WhatsApp Royal Air · ne pas diffuser à l'extérieur"):
    d.line([(MARGE, H - 132), (L - MARGE, H - 132)], fill=(31, 62, 102), width=2)
    d.rectangle([MARGE, H - 132, MARGE + 120, H - 128], fill=ROYAL)
    ecrire(d, (MARGE, H - 108), mention, police("Inter-500", 21), (110, 142, 190))


# ------------------------------------------------- le centrage du contenu
# La zone utile : sous le bandeau, au-dessus du pied.
HAUT, BAS = 236, H - 210
_BROUILLON = ImageDraw.Draw(Image.new("RGB", (L, H)))


def centrer(corps):
    """Mesure le bloc COMPLET (tous les points visibles), puis le pose une
    fois pour toutes à la bonne hauteur.

    📌 POURQUOI MESURER LE BLOC COMPLET ET NON CELUI QU'ON AFFICHE
    Les points apparaissent un par un. Si on centrait ce qui est visible, le
    texte déjà lu remonterait à chaque nouveau point : l'œil recommencerait la
    ligne. On réserve donc la place finale dès la première image — ce qui est
    écrit ne bouge plus jamais.
    Le bloc est posé à 40 % de l'espace libre et non à 50 % : au centre exact,
    une page de texte paraît basse. C'est le centre optique."""
    hauteur = corps(_BROUILLON, 0, 99)
    return HAUT + max(0, (BAS - HAUT - hauteur) * 0.34)


def bande_officielle(d, y):
    """La bande bleue et rouge du papier à en-tête Royal Air, redessinée au
    vecteur d'après `marque/bande-entete.png` : le trait rouge fin, puis le
    massif bleu qui se relève à droite. C'est la signature graphique qui figure
    en bas de tous les courriers de la compagnie — le film porte la même."""
    def profil(haut, bas):
        """Le même profil pour les deux traits : horizontal, puis une montée en
        biais aux deux tiers. C'est ce biais qui fait reconnaître le papier."""
        return [(0, haut), (L * 0.70, haut), (L * 0.79, haut - 52),
                (L, haut - 52), (L, bas - 52), (L * 0.79, bas - 52),
                (L * 0.70, bas), (0, bas)]
    d.polygon(profil(y, y + 9), fill=ROUGE)
    d.polygon(profil(y + 30, y + 84), fill=BLEU_MARQUE)


# ------------------------------------------------------- les types de cartes
def c_ouverture(titre, sous_titre, mention, avancement=0.0):
    img = fond()
    d = ImageDraw.Draw(img)
    entete(img, d, None, avancement)
    hl = 300
    lg = int(hl * 300 / 228) + int(hl * 0.32)
    logo(img, d, (L - lg) // 2, 430, hl)
    y = 880
    for ligne in couper(d, titre.upper(), police("Archivo-900", 104), L - 2 * MARGE):
        d.text((L // 2, y), ligne, font=police("Archivo-900", 104), fill=BLANC, anchor="ma")
        y += 122
    d.rectangle([L // 2 - 70, y + 34, L // 2 + 70, y + 42], fill=OR)
    y += 96
    y = bloc(d, L // 2, y, sous_titre, police("Inter-500", 40), CRAIE,
             L - 2 * MARGE - 60, 56, ancre="ma")
    ecrire(d, (L // 2, y + 66), mention.upper(), police("Inter-700", 26), CIEL,
           espacement=4, ancre="ma")
    bande_officielle(d, H - 300)
    pied(d)
    return img


def c_chapitre(numero, titre, chapitre, avancement=0.0):
    img = fond()
    d = ImageDraw.Draw(img)
    entete(img, d, chapitre, avancement)
    ecrire(d, (MARGE, 560), numero, police("Archivo-900", 300), (18, 52, 112))
    y = 900
    for ligne in couper(d, titre.upper(), police("Archivo-900", 96), L - 2 * MARGE):
        d.text((MARGE, y), ligne, font=police("Archivo-900", 96), fill=BLANC)
        y += 114
    d.rectangle([MARGE, y + 40, MARGE + 150, y + 48], fill=OR)
    pied(d)
    return img


def c_liste(titre, points, chapitre, visibles, marqueur="carre", avancement=0.0):
    """La carte de fond du film : un titre, puis des points qui apparaissent un
    par un (`visibles` dit combien sont déjà là). Les points à venir ne sont pas
    dessinés — on ne montre jamais la réponse avant la question."""
    img = fond()
    d = ImageDraw.Draw(img)
    entete(img, d, chapitre, avancement)
    ft_t = police("Archivo-900", 74)
    ft_p = police("Inter-500", 43)

    def corps(dd, y, n):
        ecrire(dd, (MARGE, y), chapitre.upper() if chapitre else "ROYAL AIR",
               police("Inter-700", 25), BLEU_PALE, espacement=4)
        y += 68
        for ligne in couper(dd, titre, ft_t, L - 2 * MARGE):
            dd.text((MARGE, y), ligne, font=ft_t, fill=BLANC)
            y += 88
        dd.rectangle([MARGE, y + 30, MARGE + 110, y + 38], fill=OR)
        y += 116
        for i, p in enumerate(points[:n]):
            neuf = (i == n - 1)
            coul_txt = BLANC if neuf else CRAIE
            if marqueur == "interdit":
                dd.line([(MARGE + 4, y + 16), (MARGE + 26, y + 38)], fill=ROUGE, width=6)
                dd.line([(MARGE + 26, y + 16), (MARGE + 4, y + 38)], fill=ROUGE, width=6)
            elif marqueur == "reflexe":
                dd.line([(MARGE + 3, y + 28), (MARGE + 14, y + 40)], fill=VERT, width=6)
                dd.line([(MARGE + 14, y + 40), (MARGE + 30, y + 14)], fill=VERT, width=6)
            else:
                dd.rounded_rectangle([MARGE + 4, y + 18, MARGE + 26, y + 40], radius=5,
                                     fill=CIEL if neuf else ROYAL)
            y = bloc(dd, MARGE + 56, y, p, ft_p, coul_txt, L - 2 * MARGE - 56, 57)
            y += 40
        return y

    corps(d, centrer(corps), visibles)
    pied(d)
    return img


def c_situation(texte, question, chapitre, avancement=0.0):
    """LA MISE EN SITUATION — une scène réelle, avant la règle.

    📌 POURQUOI ELLE EXISTE
    Une règle énoncée seule s'oublie ; la même règle attachée à une scène qu'on
    a déjà vécue reste. Les films de formation qui marchent posent tous une
    situation concrète AVANT la consigne, et laissent une seconde de silence
    sur la question — le temps que l'agent réponde dans sa tête. C'est ce
    temps-là qui fait la différence entre regarder et apprendre.
    Les scènes écrites ici sont nos escales et nos horaires, pas des exemples
    de manuel : Moroni un vendredi matin, Ouani un jour de pluie."""
    img = fond(grave=True)
    d = ImageDraw.Draw(img)
    entete(img, d, chapitre, avancement)
    ft = police("Inter-500", 52)

    def corps(dd, y, n):
        ecrire(dd, (MARGE + 34, y), "LA SITUATION", police("Inter-700", 26),
               OR, espacement=5)
        y += 76
        y0 = y
        for ligne in couper(dd, texte, ft, L - 2 * MARGE - 40):
            dd.text((MARGE + 34, y), ligne, font=ft, fill=BLANC)
            y += 70
        dd.rectangle([MARGE, y0 - 8, MARGE + 8, y - 14], fill=ROUGE)
        y += 50
        y = bloc(dd, MARGE + 34, y, question, police("Archivo-900", 60), OR,
                 L - 2 * MARGE - 40, 74)
        return y

    corps(d, centrer(corps), 1)
    pied(d)
    return img


def c_regle(texte, appui, chapitre, avancement=0.0):
    """La carte grave : une seule phrase, celle qu'on doit retenir. Fond plus
    sombre et guillemets — le film change de voix, l'œil le voit tout de suite."""
    img = fond(grave=True)
    d = ImageDraw.Draw(img)
    entete(img, d, chapitre, avancement)
    ft = police("Archivo-900", 82)

    def corps(dd, y, n):
        ecrire(dd, (MARGE, y), "«", police("Archivo-900", 190), (36, 74, 128))
        y += 172
        for ligne in couper(dd, texte, ft, L - 2 * MARGE):
            dd.text((MARGE, y), ligne, font=ft, fill=BLANC)
            y += 100
        dd.rectangle([MARGE, y + 44, MARGE + 150, y + 52], fill=OR)
        if appui:
            y = bloc(dd, MARGE, y + 110, appui, police("Inter-500", 40), CRAIE,
                     L - 2 * MARGE, 56)
        return y

    corps(d, centrer(corps), 1)
    pied(d)
    return img


def c_duo(titre, paires, chapitre, visibles, avancement=0.0):
    """« Ne dites pas / Dites » — la seule forme qui change vraiment une
    habitude de langage : on donne la phrase de remplacement, pas un principe."""
    img = fond()
    d = ImageDraw.Draw(img)
    entete(img, d, chapitre, avancement)
    ft_t = police("Archivo-900", 74)
    ft_e = police("Inter-700", 24)
    ft_p = police("Inter-500", 40)

    def corps(dd, y, n):
        ecrire(dd, (MARGE, y), chapitre.upper(), police("Inter-700", 25),
               BLEU_PALE, espacement=4)
        y += 68
        for ligne in couper(dd, titre, ft_t, L - 2 * MARGE):
            dd.text((MARGE, y), ligne, font=ft_t, fill=BLANC)
            y += 88
        y += 60
        for mauvais, bon in paires[:n]:
            y0 = y
            dd.rounded_rectangle([MARGE, y, L - MARGE, y + 4], radius=2, fill=(31, 62, 102))
            y += 30
            ecrire(dd, (MARGE, y), "NE DITES PAS", ft_e, ROUGE, espacement=3)
            y = bloc(dd, MARGE, y + 40, "« " + mauvais + " »", ft_p, (245, 195, 196),
                     L - 2 * MARGE, 52) + 26
            ecrire(dd, (MARGE, y), "DITES", ft_e, VERT, espacement=3)
            y = bloc(dd, MARGE, y + 40, "« " + bon + " »", ft_p, BLANC,
                     L - 2 * MARGE, 52) + 44
            dd.rectangle([MARGE - 22, y0 + 26, MARGE - 14, y - 24], fill=(20, 52, 94))
        return y

    corps(d, centrer(corps), visibles)
    pied(d)
    return img


def c_cloture(titre, points, reference, visibles, avancement=0.0):
    img = fond(grave=True)
    d = ImageDraw.Draw(img)
    entete(img, d, "À retenir", avancement)
    ft_t = police("Archivo-900", 84)
    ft_p = police("Inter-700", 48)

    def corps(dd, y, n):
        for ligne in couper(dd, titre.upper(), ft_t, L - 2 * MARGE):
            dd.text((MARGE, y), ligne, font=ft_t, fill=BLANC)
            y += 100
        dd.rectangle([MARGE, y + 34, MARGE + 150, y + 42], fill=OR)
        y += 120
        for i, p in enumerate(points[:n]):
            c = BLANC if i == n - 1 else CRAIE
            dd.line([(MARGE + 3, y + 30), (MARGE + 16, y + 44)], fill=VERT, width=7)
            dd.line([(MARGE + 16, y + 44), (MARGE + 34, y + 16)], fill=VERT, width=7)
            y = bloc(dd, MARGE + 62, y, p, ft_p, c, L - 2 * MARGE - 62, 62) + 44
        return y

    corps(d, centrer(corps), visibles)
    if reference:
        bloc(d, MARGE, H - 372, reference, police("Inter-500", 32), BLEU_PALE,
             L - 2 * MARGE, 46)
    pied(d)
    return img


def c_fin(lignes, avancement=1.0):
    img = fond()
    d = ImageDraw.Draw(img)
    entete(img, d, None, avancement)
    hl = 230
    lg = int(hl * 300 / 228) + int(hl * 0.32)
    logo(img, d, (L - lg) // 2, 480, hl)
    ecrire(d, (L // 2, 820), "DÉPARTEMENT QUALITÉ", police("Inter-700", 30),
           BLANC, espacement=6, ancre="ma")
    d.rectangle([L // 2 - 70, 892, L // 2 + 70, 900], fill=OR)
    y = 960
    for ligne in lignes:
        y = bloc(d, L // 2, y, ligne, police("Inter-500", 36), CRAIE,
                 L - 2 * MARGE - 40, 52, ancre="ma") + 34
    bande_officielle(d, H - 300)
    pied(d)
    return img


# ---------------------------------------------------------------- le montage
def images_de(scene, dossier, index, avancement):
    """Fabrique les images d'une scène et renvoie [(fichier, durée)].
    Une scène à points multiples devient plusieurs images : c'est ainsi que les
    points apparaissent un par un, sans animation à calculer."""
    t = scene["type"]
    sorties = []

    def poser(img, duree, n=0):
        f = os.path.join(dossier, "s%03d_%02d.png" % (index, n))
        img.save(f)
        # le rang de l'image dans sa scène sert à retrouver la phrase à dire
        sorties.append((f, duree, max(1, n)))

    if t == "ouverture":
        poser(c_ouverture(scene["titre"], scene["sous_titre"], scene["mention"], avancement),
              scene["duree"])
    elif t == "chapitre":
        poser(c_chapitre(scene["numero"], scene["titre"], scene["chapitre"], avancement),
              scene["duree"])
    elif t == "regle":
        poser(c_regle(scene["texte"], scene.get("appui", ""), scene["chapitre"], avancement),
              scene["duree"])
    elif t == "situation":
        poser(c_situation(scene["texte"], scene["question"], scene["chapitre"], avancement),
              scene["duree"])
    elif t == "fin":
        poser(c_fin(scene["lignes"], avancement), scene["duree"])
    elif t == "liste":
        pts, m = scene["points"], scene.get("marqueur", "carre")
        for i in range(1, len(pts) + 1):
            poser(c_liste(scene["titre"], pts, scene["chapitre"], i, m, avancement),
                  scene["par_point"], i)
        sorties[-1] = (sorties[-1][0], sorties[-1][1] + scene.get("tenue", 1.6), sorties[-1][2])
    elif t == "duo":
        pr = scene["paires"]
        for i in range(1, len(pr) + 1):
            poser(c_duo(scene["titre"], pr, scene["chapitre"], i, avancement),
                  scene["par_point"], i)
        sorties[-1] = (sorties[-1][0], sorties[-1][1] + scene.get("tenue", 1.6), sorties[-1][2])
    elif t == "cloture":
        pts = scene["points"]
        for i in range(1, len(pts) + 1):
            poser(c_cloture(scene["titre"], pts, scene.get("reference", ""), i, avancement),
                  scene["par_point"], i)
        sorties[-1] = (sorties[-1][0], sorties[-1][1] + scene.get("tenue", 2.4), sorties[-1][2])
    else:
        raise ValueError("type de scène inconnu : " + t)
    return sorties


def caler_sur_la_voix(scene, images, dossier, index, avec_voix):
    """Rend à chaque image la durée qu'il lui faut : celle qui laisse LIRE, ou
    celle qui laisse DIRE si la phrase est plus longue.

    📌 C'EST LA VOIX QUI COMMANDE, PAS L'INVERSE
    L'erreur classique est d'enregistrer une voix puis de la faire rentrer au
    chausse-pied dans un montage déjà fait : on accélère, on coupe des
    respirations, et cela s'entend. Ici c'est le montage qui s'adapte. Une
    image dure au moins le temps de sa phrase, plus une demi-seconde de
    silence — sans ce silence, la phrase suivante commence sur la fin de la
    précédente et tout devient précipité.
    Conséquence assumée : le film s'allonge. C'est le prix d'une voix qui
    respire, et il vaut mieux que six minutes bien dites."""
    if not avec_voix:
        return [(f, d) for f, d, _ in images], {}

    import voix as vx
    sons, ajustees = {}, []
    for f, d, n in images:
        texte = vx.a_dire(scene, n)
        wav = os.path.join(dossier, "v%03d_%02d.wav" % (index, n))
        _, dv = vx.fabriquer(texte, wav)
        if dv:
            d = max(d, dv + RESPIRATION)
            sons[len(ajustees)] = (wav, dv)
        ajustees.append((f, d))
    return ajustees, sons


def scene_en_video(images, sortie):
    """Une scène = un petit mp4, fabriqué IMAGE PAR IMAGE.

    ⚠️ POURQUOI PAS LE DÉMULTIPLEXEUR `concat` SUR LES PNG
    C'est la méthode courte, et elle ment sur les durées : la dernière image
    d'une liste n'était pas tenue le temps demandé, et le fondu de sortie
    tombait à côté. Sur le premier montage, le film annoncé à 4 min 51 durait
    5 min 31, dont quarante secondes d'écran vide. Ici, chaque image devient un
    clip `-loop 1 -t <durée>` : la durée est celle qu'on a écrite, à la frame
    près, et on peut le vérifier.

    Le fondu d'ouverture est sur la première image, le fondu de fermeture sur
    la dernière, tous deux SUR LE MARINE du fond et non sur du noir : à l'écran
    le texte apparaît et s'efface, le fond ne clignote jamais.
    """
    couleur = "0x%02X%02X%02X" % NAVY
    clips = []
    for n, (chemin, duree) in enumerate(images):
        vf = ["format=yuv420p"]
        if n == 0:
            vf.insert(0, "fade=t=in:st=0:d=0.45:color=%s" % couleur)
        if n == len(images) - 1:
            vf.insert(0, "fade=t=out:st=%.3f:d=0.40:color=%s" % (max(0.05, duree - 0.40),
                                                                couleur))
        clip = "%s.%02d.mp4" % (sortie, n)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", chemin,
                        "-t", "%.3f" % duree, "-r", str(IPS), "-vf", ",".join(vf),
                        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-pix_fmt", "yuv420p", clip], check=True)
        clips.append(clip)

    liste = sortie + ".txt"
    with open(liste, "w") as f:
        for c in clips:
            f.write("file '%s'\n" % c)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", liste, "-c", "copy", sortie], check=True)
    return sum(d for _, d in images)


def monter(scenario, nom, avec_voix=True):
    dossier = os.path.join(TRAVAIL, nom)
    os.makedirs(dossier, exist_ok=True)
    for f in os.listdir(dossier):
        os.remove(os.path.join(dossier, f))

    scenes, total = [], 0.0
    n_scenes = len(scenario["scenes"])
    paroles = []                       # (instant de départ, fichier wav)
    for i, sc in enumerate(scenario["scenes"]):
        brutes = images_de(sc, dossier, i, (i + 1) / n_scenes)
        imgs, sons = caler_sur_la_voix(sc, brutes, dossier, i, avec_voix)
        # l'instant où chaque phrase commence, dans le film entier
        t = total
        for k, (_, d) in enumerate(imgs):
            if k in sons:
                # ▸ la voix ne démarre pas avec l'image : elle attend la fin du
                #   fondu d'entrée. Sinon le premier mot tombe sur un écran noir.
                # un temps après l'apparition de l'image avant que la voix
                # parte : à l'ouverture d'une scène, le fondu d'entrée ; à
                # l'intérieur, le temps de poser l'œil sur la ligne nouvelle.
                paroles.append((t + (0.60 if k == 0 else 0.25), sons[k][0]))
            t += d
        mp4 = os.path.join(dossier, "scene%03d.mp4" % i)
        total += scene_en_video(imgs, mp4)
        scenes.append(mp4)
        print("   scène %2d/%2d  %-10s %5.1f s%s" % (i + 1, len(scenario["scenes"]),
                                                     sc["type"], sum(d for _, d in imgs),
                                                     "  (%d dites)" % len(sons) if sons else ""))

    liste = os.path.join(dossier, "montage.txt")
    with open(liste, "w") as f:
        for s in scenes:
            f.write("file '%s'\n" % s)
    muet = os.path.join(dossier, "muet.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", liste, "-c", "copy", muet], check=True)

    import musique
    nappe = os.path.join(dossier, "nappe.wav")
    musique.composer(total + 1.0, nappe)
    son = melanger(nappe, paroles, total, dossier) if paroles else nappe

    complet = os.path.join(ICI, scenario["fichier"] + ".mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", muet, "-i", son,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
                    "-movflags", "+faststart", complet], check=True)

    # La version qui passe partout : WhatsApp refuse les vidéos trop lourdes et
    # recompresse tout le reste. Mieux vaut livrer nous-mêmes un fichier léger
    # bien encodé qu'une bouillie faite par l'application.
    leger = os.path.join(ICI, scenario["fichier"] + "-whatsapp.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", complet,
                    "-vf", "scale=720:1280:flags=lanczos", "-r", str(IPS),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "28",
                    "-maxrate", "700k", "-bufsize", "1400k", "-profile:v", "main",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "64k",
                    "-movflags", "+faststart", leger], check=True)

    for f in (complet, leger):
        print("   → %-52s %6.1f Mo" % (os.path.basename(f), os.path.getsize(f) / 1e6))
    # 🔎 On ne croit pas le montage sur parole : on relit la durée du fichier
    # livré et on la compare à celle du scénario. Un écart, c'est un défaut.
    reel = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of", "csv=p=0", complet],
                                capture_output=True, text=True).stdout.strip())
    print("   durée : %d min %02d s  (scénario %d min %02d s, écart %+.2f s)"
          % (int(reel // 60), int(reel % 60), int(total // 60), int(total % 60),
             reel - total))
    if abs(reel - total) > 1.0:
        raise SystemExit("⛔ la durée livrée ne correspond pas au scénario")
    return complet, leger


def melanger(nappe, paroles, total, dossier):
    """Pose chaque phrase à son instant sur la nappe, et baisse la nappe pendant
    qu'on parle.

    📌 POURQUOI ON BAISSE LA MUSIQUE ALORS QU'ELLE EST DÉJÀ CREUSÉE
    `musique.py` retire déjà 6 dB dans la bande de la parole, ce qui suffit à
    ne pas masquer la voix. Mais ne pas masquer n'est pas assez : une musique
    au même niveau pendant toute la phrase fatigue, parce que l'oreille doit
    faire le tri en continu. On la descend donc encore de 7 dB pendant qu'on
    parle, et on la laisse remonter après — c'est ce mouvement, et non le
    niveau moyen, qui donne à un film son air « fini ».
    L'abaissement suit un lissage de 0,3 s : sans lui, on entendrait la musique
    sauter à chaque phrase.
    """
    import numpy as np
    import wave

    def lire(f):
        with wave.open(f, "rb") as w:
            n, larg, canaux = w.getnframes(), w.getsampwidth(), w.getnchannels()
            x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
            te = w.getframerate()
        if canaux == 2:
            x = x.reshape(-1, 2).mean(axis=1)
        return x, te

    fond_son, te = lire(nappe)
    n = int(total * te) + te
    if fond_son.size < n:
        fond_son = np.pad(fond_son, (0, n - fond_son.size))
    fond_son = fond_son[:n]

    voix_piste = np.zeros(n, dtype=np.float32)
    for depart, wav in paroles:
        x, te_v = lire(wav)
        assert te_v == te, "la voix et la nappe doivent être au même taux"
        i = int(depart * te)
        j = min(n, i + x.size)
        voix_piste[i:j] += x[:j - i]

    # l'enveloppe de la parole : où ça parle, et à quel point
    env = np.abs(voix_piste)
    # ⚠️ Moyenne glissante par somme cumulée, PAS par convolution : sur six
    # minutes à 48 kHz, une convolution avec une fenêtre de 0,3 s fait 2,6·10¹¹
    # multiplications — plusieurs heures. La somme cumulée fait le même calcul
    # en une seule passe.
    fenetre = int(0.30 * te)
    cum = np.concatenate(([0.0], np.cumsum(env, dtype=np.float64)))
    demi = fenetre // 2
    debut = np.clip(np.arange(env.size) - demi, 0, env.size)
    fin_f = np.clip(np.arange(env.size) + demi, 0, env.size)
    env = ((cum[fin_f] - cum[debut]) / np.maximum(1, fin_f - debut)).astype(np.float32)
    env = np.clip(env / (np.percentile(env[env > 0], 70) + 1e-9), 0, 1) if env.any() else env
    abaissement = 1 - 0.55 * env            # −7 dB au plus fort de la parole

    melange = fond_son * abaissement * 0.85 + voix_piste * 0.92
    crete = np.max(np.abs(melange))
    if crete > 0.97:
        melange *= 0.97 / crete

    sortie = os.path.join(dossier, "melange.wav")
    stereo = np.stack([melange, melange], axis=1)
    with wave.open(sortie, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(te)
        w.writeframes((stereo * 32767).astype(np.int16).tobytes())
    return sortie


def main():
    sys.path.insert(0, ICI)
    import scenarios
    args = [a.lower() for a in sys.argv[1:]]
    avec_voix = "--muet" not in args
    quoi = next((a for a in args if not a.startswith("--")), "tout")
    choix = {"agence": [scenarios.AGENCE], "escale": [scenarios.ESCALE],
             "tout": [scenarios.AGENCE, scenarios.ESCALE]}[quoi]
    os.makedirs(TRAVAIL, exist_ok=True)
    for sc in choix:
        print("\n▶ %s%s" % (sc["titre"], "" if avec_voix else "  (sans voix off)"))
        monter(sc, sc["fichier"], avec_voix)


if __name__ == "__main__":
    main()
