"""Planches de casting : une fiche visuelle par avatar + une planche d'ensemble.

Tant qu'aucun moteur d'image n'est branché, ces fiches ne contiennent pas de
photo — elles contiennent l'identité verrouillée, les tenues, les coiffures, les
expressions et l'empreinte vocale. C'est le document qu'on présente pour valider
le casting AVANT de payer la génération des visages, et celui qu'on garde ensuite
comme référence (la photo générée viendra s'y coller).
"""

import os

from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICE_GRAS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
POLICE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BLEU = (10, 37, 80)
TURQUOISE = (20, 184, 166)
OR = (250, 204, 21)
BLANC = (255, 255, 255)
GRIS = (205, 220, 235)


def _f(p, t):
    return ImageFont.truetype(p, t)


def _envelopper(d, texte, police, largeur):
    mots, lignes, courante = texte.split(), [], ""
    for mot in mots:
        essai = (courante + " " + mot).strip()
        if d.textlength(essai, font=police) <= largeur:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def fiche(bible, avatar_id, W=1080, H=2400):
    """Fiche d'un avatar. La hauteur donnée est une réserve : l'image est recadrée
    à la fin sur le contenu réellement dessiné, pour qu'aucun bloc ne soit tronqué."""
    av = bible.avatars[avatar_id]
    img = Image.new("RGB", (W, H), BLEU)
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(10 + 8 * t), int(37 + 40 * t), int(80 + 30 * t)))

    marge = 64
    d.text((marge, 54), av["id"], font=_f(POLICE_GRAS, 34), fill=OR)
    d.text((marge, 100), av["nom"], font=_f(POLICE_GRAS, 74), fill=BLANC)
    p_sous = _f(POLICE, 34)
    sous = "%s · %s ans · %s" % (av["role"], av["age"], av["origine"])
    for i, ligne in enumerate(_envelopper(d, sous, p_sous, W - 2 * marge)):
        d.text((marge, 186 + i * 42), ligne, font=p_sous, fill=GRIS)

    # emplacement du portrait (à remplir quand un moteur d'image sera branché)
    cadre_h = 430
    portrait = os.path.join(RACINE, "casting", "portraits", "%s.png" % avatar_id)
    y = 290
    if os.path.exists(portrait):
        p = Image.open(portrait).convert("RGB")
        r = max((W - 2 * marge) / p.width, cadre_h / p.height)
        p = p.resize((int(p.width * r), int(p.height * r)), Image.LANCZOS)
        p = p.crop((0, 0, W - 2 * marge, cadre_h))
        img.paste(p, (marge, y))
    else:
        d.rounded_rectangle([marge, y, W - marge, y + cadre_h], radius=28,
                            fill=(255, 255, 255, 16), outline=(255, 255, 255, 60), width=2)
        d.text((marge + 34, y + 30), "PORTRAIT À GÉNÉRER", font=_f(POLICE_GRAS, 32), fill=OR)
        p_id = _f(POLICE, 26)
        for i, ligne in enumerate(_envelopper(d, av["identite"], p_id, W - 2 * marge - 68)):
            d.text((marge + 34, y + 86 + i * 36), ligne, font=p_id, fill=GRIS)
        d.text((marge + 34, y + cadre_h - 58), "seed %s — à réutiliser toujours" % av["seed"],
               font=_f(POLICE_GRAS, 28), fill=TURQUOISE)
    y += cadre_h + 46

    def bloc(titre, lignes, y):
        d.text((marge, y), titre, font=_f(POLICE_GRAS, 32), fill=TURQUOISE)
        y += 46
        p = _f(POLICE, 30)
        for ligne in lignes:
            for sous in _envelopper(d, ligne, p, W - 2 * marge - 30):
                d.text((marge + 16, y), sous, font=p, fill=BLANC)
                y += 40
        return y + 22

    y = bloc("TENUES", ["· %s — %s" % (t["id"], t["desc"]) for t in av["tenues"]], y)
    y = bloc("COIFFURES", ["· %s" % c["desc"] for c in av["coiffures"]], y)
    y = bloc("EXPRESSIONS",
             [", ".join(bible.expressions.get(e, {}).get("nom", e) for e in av["expressions"])], y)

    empreinte = bible.voix["empreintes"].get(avatar_id, {})
    if empreinte.get("interdit"):
        voix_txt = ["Aucune voix de synthèse (mineur) — voir les règles de protection"]
    else:
        voix_txt = ["%s : %s (débit %s, hauteur %s)" %
                    (lg.upper(), v, empreinte.get("rate", "+0%"), empreinte.get("pitch", "+0Hz"))
                    for lg, v in av.get("voix", {}).items() if not lg.startswith("_")]
    y = bloc("VOIX", voix_txt, y)
    y = bloc("EMPLOI", [av["emploi"]], y)
    if av.get("restrictions"):
        p_r = _f(POLICE, 24)
        lignes = _envelopper(d, ", ".join(av["restrictions"]).replace("_", " "), p_r,
                             W - 2 * marge - 48)
        hauteur = 74 + len(lignes) * 32
        d.rounded_rectangle([marge, y, W - marge, y + hauteur], radius=20,
                            fill=(250, 204, 21, 30), outline=OR, width=2)
        d.text((marge + 24, y + 20), "RESTRICTIONS (mineur)", font=_f(POLICE_GRAS, 28), fill=OR)
        for i, ligne in enumerate(lignes):
            d.text((marge + 24, y + 62 + i * 32), ligne, font=p_r, fill=BLANC)
        y += hauteur + 22

    d.text((marge, y + 24), "MoheliGo Studio IA — bibliothèque d'avatars permanents",
           font=_f(POLICE, 24), fill=GRIS)
    return img.crop((0, 0, W, min(H, y + 90)))


def planche(bible, W=2160, colonnes=4):
    """Planche d'ensemble : tout le casting sur une image."""
    ids = list(bible.avatars)
    case_l = W // colonnes
    case_h = int(case_l * 1.35)
    lignes = (len(ids) + colonnes - 1) // colonnes
    H = case_h * lignes + 220
    img = Image.new("RGB", (W, H), BLEU)
    d = ImageDraw.Draw(img, "RGBA")

    d.text((60, 56), "CASTING MOHELIGO", font=_f(POLICE_GRAS, 76), fill=BLANC)
    d.text((60, 146), "%d avatars permanents — visage et voix verrouillés" % len(ids),
           font=_f(POLICE, 34), fill=OR)

    for i, aid in enumerate(ids):
        av = bible.avatars[aid]
        cx = (i % colonnes) * case_l
        cy = 220 + (i // colonnes) * case_h
        d.rounded_rectangle([cx + 14, cy + 14, cx + case_l - 14, cy + case_h - 14], radius=22,
                            fill=(255, 255, 255, 16), outline=(255, 255, 255, 50), width=2)
        portrait = os.path.join(RACINE, "casting", "portraits", "%s.png" % aid)
        zone = (cx + 40, cy + 40, cx + case_l - 40, cy + int(case_h * 0.52))
        if os.path.exists(portrait):
            p = Image.open(portrait).convert("RGB").resize(
                (zone[2] - zone[0], zone[3] - zone[1]), Image.LANCZOS)
            img.paste(p, (zone[0], zone[1]))
        else:
            d.rounded_rectangle(list(zone), radius=16, fill=(20, 184, 166, 45))
            initiales = "".join(m[0] for m in av["nom"].split()[:2]).upper()
            f = _f(POLICE_GRAS, int(case_l * 0.22))
            b = d.textbbox((0, 0), initiales, font=f)
            d.text((zone[0] + (zone[2] - zone[0] - (b[2] - b[0])) // 2,
                    zone[1] + (zone[3] - zone[1] - (b[3] - b[1])) // 2 - 10),
                   initiales, font=f, fill=BLANC)
        ty = zone[3] + 24
        d.text((cx + 40, ty), av["nom"], font=_f(POLICE_GRAS, 32), fill=BLANC)
        d.text((cx + 40, ty + 42), av["id"], font=_f(POLICE, 24), fill=OR)
        p_r = _f(POLICE, 26)
        for j, ligne in enumerate(_envelopper(d, av["role"], p_r, case_l - 80)[:2]):
            d.text((cx + 40, ty + 78 + j * 32), ligne, font=p_r, fill=GRIS)
        if av.get("mineur"):
            d.text((cx + 40, cy + case_h - 60), "usage encadré (mineur)",
                   font=_f(POLICE_GRAS, 22), fill=OR)
    return img


def produire(bible, dossier):
    os.makedirs(os.path.join(dossier, "fiches"), exist_ok=True)
    os.makedirs(os.path.join(dossier, "portraits"), exist_ok=True)
    produits = []
    for aid in bible.avatars:
        chemin = os.path.join(dossier, "fiches", "%s.png" % aid)
        fiche(bible, aid).save(chemin)
        produits.append(chemin)
    p = os.path.join(dossier, "planche-casting.png")
    planche(bible).save(p)
    produits.append(p)
    return produits
