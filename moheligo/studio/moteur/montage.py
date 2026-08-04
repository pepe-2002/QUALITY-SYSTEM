"""Rendu et montage.

Deux modes :

1. ANIMATIQUE (fonctionne ici, sans moteur externe) — chaque plan devient une carte
   composée : photo réelle du décor quand elle existe, sinon fond de marque ; par-dessus,
   les personnages du plan, l'action, la caméra, et le dialogue en sous-titre incrusté.
   Avec la vraie voix off calée. C'est la maquette qu'on fait valider AVANT de dépenser
   en génération vidéo.

2. MONTAGE FINAL — quand les rushes générés (un mp4 par plan) sont déposés dans
   projets/<nom>/rushes/plan-01.mp4, etc., le studio les assemble à la place des cartes.
   Même timeline, même audio, mêmes exports.
"""

import json
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageFilter

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POLICE_GRAS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
POLICE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

BLEU = (10, 37, 80)
TURQUOISE = (20, 184, 166)
OR = (250, 204, 21)
BLANC = (255, 255, 255)


def _f(chemin, taille):
    return ImageFont.truetype(chemin, taille)


def _texte_centre(d, y, texte, police, couleur, largeur, contour=0):
    b = d.textbbox((0, 0), texte, font=police)
    x = (largeur - (b[2] - b[0])) // 2
    if contour:
        d.text((x, y), texte, font=police, fill=(0, 0, 0), stroke_width=contour,
               stroke_fill=(0, 0, 0))
    d.text((x, y), texte, font=police, fill=couleur)
    return b[3] - b[1]


def _envelopper(d, texte, police, largeur_max):
    mots, lignes, courante = texte.split(), [], ""
    for mot in mots:
        essai = (courante + " " + mot).strip()
        if d.textlength(essai, font=police) <= largeur_max:
            courante = essai
        else:
            if courante:
                lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


def _fond(plan, bible, W, H):
    """Photo réelle du décor en Ken Burns statique, sinon dégradé de marque."""
    photo = bible.photo_decor(plan["decor"]) if plan.get("decor") else None
    if photo:
        img = Image.open(photo).convert("RGB")
        r = max(W / img.width, H / img.height) * 1.06
        img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
        gauche = (img.width - W) // 2
        haut = (img.height - H) // 2
        img = img.crop((gauche, haut, gauche + W, haut + H))
        voile = Image.new("RGB", (W, H), BLEU)
        img = Image.blend(img, voile, 0.42)
        return img
    img = Image.new("RGB", (W, H), BLEU)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(
            int(BLEU[0] + (TURQUOISE[0] - BLEU[0]) * t * 0.55),
            int(BLEU[1] + (TURQUOISE[1] - BLEU[1]) * t * 0.55),
            int(BLEU[2] + (TURQUOISE[2] - BLEU[2]) * t * 0.55)))
    return img


def carte_plan(bible, scenario, plan, W, H, securite=0.0):
    """Compose l'image d'un plan (animatique).

    `securite` est la fraction de l'image que le recadrage animé peut manger sur
    chaque bord : tout le texte est composé à l'intérieur de cette zone sûre, sinon
    le bandeau du haut et la mention IA se retrouvent coupés au montage.
    """
    img = _fond(plan, bible, W, H)
    d = ImageDraw.Draw(img, "RGBA")
    ox, oy = int(W * securite), int(H * securite)
    Wu, Hu = W - 2 * ox, H - 2 * oy
    ech = Hu / 1920.0

    p_petit = _f(POLICE, int(34 * ech))
    p_moyen = _f(POLICE, int(44 * ech))
    p_gras = _f(POLICE_GRAS, int(56 * ech))
    p_titre = _f(POLICE_GRAS, int(72 * ech))

    marge = ox + int(70 * ech)

    # bandeau haut : n° de plan, caméra, décor
    d.rectangle([0, 0, W, oy + int(190 * ech)], fill=(10, 37, 80, 200))
    cam = bible.cameras.get(plan["camera"], {}).get("nom", plan["camera"])
    lieu = bible.decors[plan["decor"]]["nom"] if plan.get("decor") else "Carton de marque"
    d.text((marge, oy + int(46 * ech)), "PLAN %02d · %s" % (plan["n"], plan["role"].upper()),
           font=_f(POLICE_GRAS, int(38 * ech)), fill=OR)
    d.text((marge, oy + int(104 * ech)), "%s — %s" % (lieu, cam), font=p_petit, fill=BLANC)
    duree = "%.1f s" % plan["duree"]
    d.text((W - marge - d.textlength(duree, font=p_moyen), oy + int(70 * ech)), duree,
           font=p_moyen, fill=TURQUOISE)

    # personnages présents
    y = oy + int(280 * ech)
    for acteur in plan.get("acteurs", []):
        av = bible.avatars[acteur["avatar"]]
        action = bible.actions.get(acteur["action"], {}).get("nom", acteur["action"])
        expr = bible.expressions.get(acteur["expression"], {}).get("nom", acteur["expression"])
        h_pastille = int(120 * ech)
        d.rounded_rectangle([marge, y, W - marge, y + h_pastille], radius=int(24 * ech),
                            fill=(255, 255, 255, 28), outline=(255, 255, 255, 70), width=2)
        initiales = "".join(m[0] for m in av["nom"].split()[:2]).upper()
        d.ellipse([marge + int(18 * ech), y + int(18 * ech),
                   marge + int(18 * ech) + int(84 * ech), y + int(18 * ech) + int(84 * ech)],
                  fill=TURQUOISE)
        d.text((marge + int(42 * ech), y + int(38 * ech)), initiales,
               font=_f(POLICE_GRAS, int(40 * ech)), fill=BLEU)
        d.text((marge + int(130 * ech), y + int(24 * ech)), av["nom"],
               font=_f(POLICE_GRAS, int(40 * ech)), fill=BLANC)
        d.text((marge + int(130 * ech), y + int(72 * ech)), "%s · %s" % (action, expr),
               font=p_petit, fill=(220, 235, 245))
        y += h_pastille + int(22 * ech)

    # incrustation d'écran d'app
    if plan.get("incrustation"):
        d.rounded_rectangle([marge, y, marge + int(430 * ech), y + int(120 * ech)],
                            radius=int(20 * ech), fill=(250, 204, 21, 40),
                            outline=OR, width=3)
        d.text((marge + int(26 * ech), y + int(26 * ech)), "ÉCRAN APP",
               font=_f(POLICE_GRAS, int(34 * ech)), fill=OR)
        d.text((marge + int(26 * ech), y + int(70 * ech)), str(plan["incrustation"]),
               font=p_petit, fill=BLANC)
        y += int(160 * ech)

    # carton final
    if plan.get("carton"):
        cf = scenario["carton_final"]
        logo = os.path.join(RACINE, "..", "MoheliGo-logo.png")
        cy = oy + int(Hu * 0.30)
        if os.path.exists(logo):
            l = Image.open(logo).convert("RGBA")
            cote = int(Wu * 0.34)
            l = l.resize((cote, int(l.height * cote / l.width)), Image.LANCZOS)
            masque = Image.new("L", l.size, 0)
            ImageDraw.Draw(masque).rounded_rectangle([0, 0, l.size[0], l.size[1]],
                                                     radius=int(cote * 0.22), fill=255)
            # ombre portée (icône d'app), puis le logo aux coins arrondis
            ombre = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ombre.paste((0, 0, 0, 140), ((W - cote) // 2 + int(10 * ech), cy + int(14 * ech)),
                        masque)
            ombre = ombre.filter(ImageFilter.GaussianBlur(int(16 * ech)))
            img.paste(Image.alpha_composite(img.convert("RGBA"), ombre).convert("RGB"), (0, 0))
            img.paste(l, ((W - cote) // 2, cy), masque)
            d = ImageDraw.Draw(img, "RGBA")
            cy += l.size[1] + int(60 * ech)
        _texte_centre(d, cy, cf["signature"], p_titre, BLANC, W)
        cy += int(110 * ech)
        _texte_centre(d, cy, cf["site"], _f(POLICE_GRAS, int(52 * ech)), OR, W)

    # sous-titre incrusté (dialogue ou voix off)
    texte = None
    if plan.get("dialogue"):
        prenom = bible.avatars[plan["dialogue"]["avatar"]]["nom"].split()[0]
        texte = "%s — « %s »" % (prenom, plan["dialogue"]["texte"])
    elif plan.get("voix_off"):
        texte = plan["voix_off"]
    if texte:
        lignes = _envelopper(d, texte, p_gras, W - 2 * marge)
        bas = oy + int(Hu * 0.80) - len(lignes) * int(72 * ech)
        d.rectangle([0, bas - int(40 * ech), W, bas + len(lignes) * int(72 * ech) + int(30 * ech)],
                    fill=(0, 0, 0, 130))
        for i, ligne in enumerate(lignes):
            b = d.textbbox((0, 0), ligne, font=p_gras)
            x = (W - (b[2] - b[0])) // 2
            d.text((x, bas + i * int(72 * ech)), ligne, font=p_gras, fill=BLANC,
                   stroke_width=max(2, int(5 * ech)), stroke_fill=(0, 0, 0))

    # mention IA, toujours
    mention = bible.marque["mention_ia"]["texte_fr"]
    p_mention = _f(POLICE, max(14, int(Hu * 0.022)))
    d.text((marge, oy + Hu - int(72 * ech)), mention, font=p_mention, fill=(200, 215, 230))
    return img


MARGE_MOUVEMENT = 1.08  # la carte est composée un peu plus grande que le cadre final


def _segment(image_png, duree, sortie, W, H, zoom=True):
    """Une image → un segment vidéo avec un léger mouvement.

    Le mouvement est un travelling obtenu par recadrage animé sur une image déjà
    composée plus grande que le cadre. On évite ainsi le filtre zoompan, qui
    ré-échantillonne l'image à chaque trame et met plus d'une minute par plan en 1080p.
    """
    if zoom:
        vf = ("crop=%d:%d:x='(iw-ow)*(0.35+0.30*t/%.2f)':y='(ih-oh)*(0.55-0.25*t/%.2f)',"
              "format=yuv420p" % (W, H, max(duree, 0.1), max(duree, 0.1)))
    else:
        vf = "crop=%d:%d:x=(iw-ow)/2:y=(ih-oh)/2,format=yuv420p" % (W, H)
    vf += ",fade=t=in:st=0:d=0.25,fade=t=out:st=%.2f:d=0.25" % max(0.1, duree - 0.25)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "30",
         "-t", "%.2f" % duree, "-i", image_png, "-vf", vf,
         "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p", sortie],
        check=True)
    return sortie


def _piste_audio(pistes, dossier, duree_totale, sortie):
    """Mixe toutes les voix aux bons instants sur une base silencieuse."""
    if not pistes:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
                        "-i", "anullsrc=r=48000:cl=mono", "-t", "%.2f" % duree_totale,
                        "-c:a", "aac", "-b:a", "80k", sortie], check=True)
        return sortie
    entrees, filtres, etiquettes = [], [], []
    for i, p in enumerate(pistes):
        entrees += ["-i", os.path.join(dossier, p["fichier"])]
        filtres.append("[%d:a]adelay=%d|%d,volume=5dB[a%d]" %
                       (i, int(p["debut"] * 1000), int(p["debut"] * 1000), i))
        etiquettes.append("[a%d]" % i)
    filtre = ";".join(filtres) + ";" + "".join(etiquettes) + \
        "amix=inputs=%d:normalize=0,alimiter=limit=0.95,apad[out]" % len(pistes)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + entrees +
                   ["-filter_complex", filtre, "-map", "[out]", "-t", "%.2f" % duree_totale,
                    "-c:a", "aac", "-b:a", "128k", "-ar", "48000", sortie], check=True)
    return sortie


def rendre(bible, scenario, pistes, dossier, format_id="tiktok", mode="animatique"):
    """Produit la vidéo du projet dans un format. Renvoie le chemin du fichier."""
    fmt = bible.formats[format_id]
    W, H = fmt["w"], fmt["h"]
    travail = os.path.join(dossier, "travail", format_id)
    os.makedirs(travail, exist_ok=True)

    rushes = os.path.join(dossier, "rushes")
    segments = []
    for plan in scenario["plans"]:
        rush = os.path.join(rushes, "plan-%02d.mp4" % plan["n"])
        seg = os.path.join(travail, "seg-%02d.mp4" % plan["n"])
        if mode == "final" and os.path.exists(rush):
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", rush, "-t", "%.2f" % plan["duree"],
                 "-vf", "scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,fps=30,"
                        "format=yuv420p" % (W, H, W, H),
                 "-an", "-c:v", "libx264", "-crf", "19", "-preset", "medium", seg], check=True)
        else:
            png = os.path.join(travail, "plan-%02d.png" % plan["n"])
            gW, gH = int(W * MARGE_MOUVEMENT), int(H * MARGE_MOUVEMENT)
            carte_plan(bible, scenario, plan, gW, gH,
                       securite=(MARGE_MOUVEMENT - 1) / 2).save(png)
            _segment(png, plan["duree"], seg, W, H, zoom=not plan.get("carton"))
        segments.append(seg)

    liste = os.path.join(travail, "liste.txt")
    with open(liste, "w") as f:
        for s in segments:
            f.write("file '%s'\n" % os.path.abspath(s))
    muet = os.path.join(travail, "muet.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", liste, "-c", "copy", muet], check=True)

    duree = sum(p["duree"] for p in scenario["plans"])
    audio = _piste_audio(pistes, dossier, duree, os.path.join(travail, "audio.m4a"))

    sortie = os.path.join(dossier, "%s-%s.mp4" % (scenario["projet"], format_id))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", muet, "-i", audio,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
                    "-movflags", "+faststart", sortie], check=True)
    return sortie


def alleger(source, largeur=None):
    """Version diffusion (réglage validé pour les connexions comoriennes).

    720 px de large en vertical, 1280 px en horizontal : réduire un 16:9 à 720 px
    donnerait un 720×405 illisible sur un écran d'ordinateur.
    """
    sortie = source.replace(".mp4", "-leger.mp4")
    if largeur is None:
        largeur = 720
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", source,
                    "-vf", "scale=%d:-2" % largeur,
                    "-c:v", "libx264", "-crf", "26", "-preset", "slow",
                    "-c:a", "aac", "-b:a", "80k", "-ac", "1",
                    "-movflags", "+faststart", sortie], check=True)
    return sortie


def poids(chemin):
    return "%.1f Mo" % (os.path.getsize(chemin) / 1e6)
