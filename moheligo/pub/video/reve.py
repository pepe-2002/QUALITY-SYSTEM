#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LE FILM QUI FAIT RÊVER — Mohéli, la voix du patron, nos services.

    python3 reve.py

Le patron, 26/08/2026 : « la 1, et mets une petite musique à la vidéo, et utilise
ma voix pour les voix off. Fais une vidéo qui fait rêver, ça sera bien de
présenter nos services en fait. »

📌 POURQUOI DES PHOTOS ICI, ALORS QU'ON LES A REFUSÉES POUR LES FILMS D'IDENTITÉ
Ce n'est pas le même film. Un film d'identité doit faire reconnaître la MARQUE :
une photo y tire l'œil vers son sujet et dilue le propos — d'où les cartes.
Ici, le sujet EST Mohéli. **On ne fait pas rêver avec une carte marine.** Les
photos reprennent donc la première place, et la marque tient par le décor : le
coin blanc, la vague dorée qui coupe, la carte finale.

🎬 AUCUNE SECONDE N'EST ÉCRITE DANS CE FICHIER
Les plans, les bandeaux, la durée du film : tout vient de `minutage.py`, qui
mesure la voix telle qu'elle sort et en déduit le montage. J'avais d'abord fait
l'inverse — des créneaux fixes, à charge pour la voix d'y rentrer — et trois
phrases débordaient. **La voix mène, l'image suit.**
📌 Une coupe tombe donc toujours au début d'une phrase, jamais au milieu d'un
mot, et la respiration qui suit une phrase reste sur l'image de cette phrase :
couper dans le silence donne l'impression d'avoir coupé trop tôt.

🔊 TROIS COUCHES DE SON
  · sa voix, réglage « 1 · LÉGÈRE », devant ;
  · la nappe (`musique.py`), **écrite ici**, 14 dB en dessous — une musique du
    commerce ferait couper le son de la publication par Facebook ;
  · rien d'autre. Pas d'effet, pas de « whoosh » sur les transitions : la vague
    dorée se voit, elle n'a pas besoin de s'entendre.

🗣️ LA VOIX EST SA VOIX, CLONÉE (`cloner.py`), sur un texte que j'ai écrit et
qu'il a demandé. Les règles de `cloner.py` s'appliquent : c'est un gain de
prises, pas un remplacement de sa parole. **Il écoute et valide avant toute
publication** — je n'entends pas le résultat, lui seul peut dire si c'est lui.
"""
import argparse, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cartes, minutage

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", ".."))
W, H, FPS = 1080, 1920, 30
OR = (246, 188, 28)
MARINE = (15, 42, 92)
BALAYAGE = 0.55

VOIX = os.path.join(ICI, "voix", "voix-off-clonee.m4a")
NAPPE = os.path.join(ICI, "musique", "nappe-mer.wav")


def p(x):
    return os.path.join(RACINE, x)


# (photo, fin du plan, recadrage) · la seconde de la carte · la durée du film
_plans, CARTE, DUREE = minutage.plans()
PLANS = [(p(ph), fin, zone) for ph, fin, zone in _plans]
BANDEAUX = minutage.bandeaux()


def charger(chemin, zone=None):
    im = Image.open(chemin).convert("RGB")
    if zone:
        x0, y0, x1, y1 = zone
        im = im.crop((int(x0 * im.width), int(y0 * im.height),
                      int(x1 * im.width), int(y1 * im.height)))
    ar = W / H
    if im.width / im.height > ar:
        nw, nh = int(im.height * ar), im.height
    else:
        nw, nh = im.width, int(im.width / ar)
    im = im.crop(((im.width - nw) // 2, (im.height - nh) // 2,
                  (im.width - nw) // 2 + nw, (im.height - nh) // 2 + nh))
    return np.asarray(im.resize((int(W * 1.16), int(H * 1.16)), Image.LANCZOS))


def plan(grande, t, sens):
    """Zoom lent, alternativement vers l'intérieur et vers l'extérieur : deux
    plans qui zooment dans le même sens donnent une impression de tapis roulant."""
    z = (1.14 - 0.12 * t) if sens else (1.02 + 0.12 * t)
    gh, gw = grande.shape[:2]
    vw, vh = min(gw, int(gw / z)), min(gh, int(gh / z))
    x0, y0 = (gw - vw) // 2, (gh - vh) // 2
    im = Image.fromarray(grande[y0:y0 + vh, x0:x0 + vw]).resize((W, H), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32)
    # ÉTALONNAGE LÉGER — ici la photo doit rester belle : on ne la repeint pas,
    # on la réchauffe un peu et on assombrit le haut et le bas pour que le coin
    # blanc et les bandeaux tiennent.
    a[:, :, 0] *= 1.035
    a[:, :, 2] *= 0.985
    a = (a - 128) * 1.06 + 128
    y = np.linspace(0, 1, H).reshape(H, 1, 1)
    haut = np.clip((0.16 - y) / 0.16, 0, 1) ** 1.4
    bas = np.clip((y - 0.70) / 0.30, 0, 1) ** 1.3
    for m, force in ((haut, 0.34), (bas, 0.46)):
        a = a * (1 - force * m) + np.array(MARINE, np.float32) * (force * m)
    return np.clip(a, 0, 255).astype(np.uint8)


def coin(img, emblem):
    """Le coin blanc en biais, sur chaque image du film — comme sur les flyers."""
    im = Image.fromarray(img).convert("RGBA")
    lw, lh = 430, 150
    tuile = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    d = ImageDraw.Draw(tuile)
    d.polygon([(0, 0), (lw, 0), (int(lw * .78), lh), (0, lh)], fill=(255, 255, 255, 244))
    e = emblem.resize((66, int(66 * emblem.height / emblem.width)), Image.LANCZOS)
    tuile.alpha_composite(e, (34, (lh - e.height) // 2 - 6))
    f1 = ImageFont.truetype(os.path.join(ICI, "polices", "Archivo-900.ttf"), 30)
    f2 = ImageFont.truetype(os.path.join(ICI, "polices", "Inter-700.ttf"), 11)
    d.text((116, 46), "Moheli", font=f1, fill=(15, 42, 92, 255))
    lg = d.textlength("Moheli", font=f1)
    d.text((116 + lg, 46), "Go", font=f1, fill=OR + (255,))
    d.text((117, 84), "T R A V E R S É E S   M A R I T I M E S", font=f2,
           fill=(92, 110, 139, 255))
    im.alpha_composite(tuile, (0, 0))
    return np.asarray(im.convert("RGB"))


def bandeau(img, petit, grand, ouverture):
    """Un bandeau de service : la barre dorée, le mot en or, la phrase en blanc.
    Il s'ouvre depuis la gauche, comme la vague."""
    im = Image.fromarray(img).convert("RGBA")
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)
    f1 = ImageFont.truetype(os.path.join(ICI, "polices", "Inter-700.ttf"), 30)
    f2 = ImageFont.truetype(os.path.join(ICI, "polices", "Archivo-900.ttf"), 62)
    y = int(H * 0.735)
    larg = int((max(d.textlength(grand, font=f2),
                    d.textlength(petit, font=f1) + 40) + 150) * min(1.0, ouverture * 1.6))
    d.rectangle([0, y - 34, larg, y + 118], fill=(15, 42, 92, 232))
    d.rectangle([0, y - 34, 13, y + 118], fill=OR + (255,))
    if ouverture > 0.55:
        o = int(255 * min(1.0, (ouverture - 0.55) * 3.4))
        d.text((52, y - 22), petit, font=f1, fill=OR + (o,))
        d.text((52, y + 22), grand, font=f2, fill=(255, 255, 255, o))
    im.alpha_composite(calque)
    return np.asarray(im.convert("RGB"))


def vague(a, b, avancee):
    """LE GESTE SIGNATURE, identique aux films d'identité."""
    amp = 74
    ys = np.arange(H).reshape(H, 1)
    bord = avancee * (W + 4 * amp) - 2 * amp + amp * np.sin(ys / H * 3.1 * np.pi)
    xs = np.arange(W).reshape(1, W)
    out = np.where((xs < bord)[:, :, None], b, a)
    crete = np.abs(xs - bord) < 22
    out = np.where(crete[:, :, None], np.array(OR, np.uint8), out)
    halo = (np.abs(xs - bord) < 66) & ~crete
    return np.where(halo[:, :, None],
                    (out.astype(np.float32) * .55 + np.array(OR, np.float32) * .45)
                    .astype(np.uint8), out)


def fabriquer(sortie, travail="/tmp/reve-moheligo"):
    os.makedirs(travail, exist_ok=True)
    emblem = Image.open(os.path.join(RACINE, "pub", "flyers", "logo-emblem.png")).convert("RGBA")
    photos = [charger(c, z) for c, _, z in PLANS]
    fin_carte = os.path.join(travail, "finale.png")
    cartes.carte(fin_carte, ["LA MER DÉCIDE.", "NOUS, ON TE LE", "DIT AVANT."],
                 mot_or=["NOUS, ON TE LE", "DIT AVANT."],
                 surtitre="MOHÉLI ↔ NGAZIDJA",
                 pied=("RÉSERVE TA TRAVERSÉE SUR", "moheligo.com"))
    finale = np.asarray(Image.open(fin_carte).convert("RGB"))

    muet = sortie.replace(".mp4", "-muet.mp4")
    tube = subprocess.Popen(
        ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "19",
         "-pix_fmt", "yuv420p", muet], stdin=subprocess.PIPE)

    debuts = [0.0] + [f for _, f, _ in PLANS]
    precedent = np.zeros((H, W, 3), np.uint8)
    nb = int(BALAYAGE * FPS)
    for k in range(int(DUREE * FPS)):
        t = k / FPS
        if t < CARTE:
            i = next(j for j, (_, f, _) in enumerate(PLANS) if t < f)
            d0, d1 = debuts[i], debuts[i + 1]
            img = plan(photos[i], (t - d0) / max(0.4, d1 - d0), i % 2 == 0)
            img = coin(img, emblem)
            for b0, b1, pt, gr in BANDEAUX:
                if b0 <= t < b1:
                    img = bandeau(img, pt, gr, min(1.0, (t - b0) / 0.55))
            depuis = t - d0
        else:
            img = finale
            depuis = t - CARTE
        if depuis < BALAYAGE:
            img = vague(precedent, img, depuis / BALAYAGE)
        tube.stdin.write(img.astype(np.uint8).tobytes())
        precedent = img
    tube.stdin.close()
    tube.wait()

    # LE SON : sa voix devant, la nappe qui s'efface dessous et remonte dans les
    # blancs. 🚨 LE DÉFAUT SIGNALÉ PAR LE PATRON — « parfois tu n'entends rien ».
    # Avant, la nappe était à volume fixe : sous une phrase un peu faible elle
    # passait devant, et dans les silences il ne restait presque rien. Maintenant
    # c'est un ABAISSEMENT AUTOMATIQUE (`sidechaincompress`) : la voix commande
    # la musique. Elle parle → la nappe recule ; elle se tait → la nappe revient.
    # 📌 Deux effets d'un coup : la voix n'est jamais couverte, et les respirations
    # ne sont plus des trous — c'est la musique qui les tient.
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", muet,
         "-i", VOIX, "-i", NAPPE, "-filter_complex",
         "[1:a]adelay=0|0,volume=1.0,asplit=2[v][cle];"
         f"[2:a]volume=0.30,afade=t=out:st={DUREE - 3.0:.2f}:d=3[m];"
         # attaque courte (elle doit reculer dès la première syllabe), retour
         # lent (400 ms) : un retour rapide s'entend comme une pompe
         "[m][cle]sidechaincompress=threshold=0.03:ratio=8:attack=15:release=400"
         ":makeup=1[md];"
         "[v][md]amix=inputs=2:duration=first:dropout_transition=0,"
         f"apad,atrim=0:{DUREE},loudnorm=I=-15:TP=-1.5:LRA=12[a]",
         "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", sortie], check=True)
    os.unlink(muet)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default=os.path.join(ICI, "MoheliGo-Moheli-le-reve.mp4"))
    a = ap.parse_args()
    fabriquer(a.sortie)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", a.sortie], capture_output=True, text=True).stdout.strip()
    print(f"✅ {os.path.basename(a.sortie)}  {float(d):.1f} s")
