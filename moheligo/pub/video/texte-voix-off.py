#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LE TEXTE DE LA VOIX OFF — et le souffleur pour l'enregistrer en rythme.

    python3 texte-voix-off.py            # fabrique SOUFFLEUR.mp4

Le patron, 26/08/2026 : « change ce que je dis, et fais-en une voix qui décrit
les services et qui va avec les images. »

📌 CE QUE JE NE PEUX PAS FAIRE, ET POURQUOI ON PASSE PAR LÀ
Je ne peux pas modifier ce qu'il a dit : synthétiser sa voix pour lui faire
prononcer un autre texte, c'est fabriquer une parole qu'il n'a jamais tenue. Je
ne le fais pas, même pour lui, même sur sa propre voix.
➡️ Donc : **j'écris le texte, il l'enregistre.** Et pour que ça tombe juste du
premier coup, on ne lui envoie pas une feuille — on lui envoie **un souffleur** :
une vidéo qui affiche la phrase à dire, à la seconde où il faut la dire. Il la
lance, il lit, il enregistre. Le fichier tombe ensuite au montage sans le
moindre recalage.

⚠️ AUCUN FAIT INVENTÉ. Pas de durée de traversée, pas d'horaire de vedette, pas
de prix — rien qui ne soit vérifié. Ce qui est dit ici est vrai aujourd'hui :
la réservation depuis le téléphone, MVola, le billet à code QR qui reste dans le
téléphone, le bulletin mer du soir, le changement de date gratuit.
"""
import os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
MARINE = (15, 42, 92)
NUIT = (10, 29, 66)
OR = (246, 188, 28)
DUREE = 42.0

ARCH = os.path.join(ICI, "polices", "Archivo-900.ttf")
INTER = os.path.join(ICI, "polices", "Inter-700.ttf")
INTER5 = os.path.join(ICI, "polices", "Inter-500.ttf")

# (début, fin, les lignes à lire, ce qu'on voit à l'écran à ce moment-là)
TEXTE = [
    (3.0,  5.6,  ["Mohéli."], "l'île vue du ciel"),
    (6.4, 12.6,  ["Avant, pour y aller,", "il fallait descendre au port.",
                  "Demander. Attendre."], "la plage, l'horizon"),
    (13.4, 19.4, ["Aujourd'hui, tu réserves", "ta traversée depuis", "ton téléphone."],
                 "les pirogues sous les cocotiers"),
    (20.2, 22.8, ["Tu paies par MVola."], "les tortues"),
    (23.6, 29.4, ["Ton billet arrive", "avec son code QR.", "Il reste dans ton téléphone,",
                  "même sans réseau."], "la mer, la vedette au loin"),
    (30.2, 34.4, ["Et chaque soir, on publie", "la mer du lendemain."], "le dauphin"),
    (35.0, 37.4, ["Tu sais avant de partir", "de chez toi."], "l'îlot au couchant"),
    (38.2, 41.6, ["MoheliGo.", "La mer décide,", "nous on te le dit avant."], "la carte finale"),
]


def image(t):
    im = Image.new("RGB", (W, H), MARINE if int(t) % 2 == 0 else MARINE)
    d = ImageDraw.Draw(im)
    for i in range(H):
        k = (i / H) ** 1.25
        d.line([(0, i), (W, i)], fill=tuple(
            int(MARINE[c] * (1 - k * .5) + NUIT[c] * (k * .5)) for c in range(3)))

    # le compte à rebours du départ
    if t < 3.0:
        n = 3 - int(t)
        f = ImageFont.truetype(ARCH, 300)
        s = str(max(1, n))
        lg = d.textlength(s, font=f)
        d.text(((W - lg) / 2, H * 0.36), s, font=f, fill=OR)
        f2 = ImageFont.truetype(INTER, 34)
        s2 = "PRÉPARE-TOI"
        lg = d.textlength(s2, font=f2)
        d.text(((W - lg) / 2, H * 0.30), s2, font=f2, fill=(147, 197, 253))

    courant = suivant = None
    for i, (a, b, lignes, vu) in enumerate(TEXTE):
        if a <= t < b:
            courant = (a, b, lignes, vu)
        if t < a and suivant is None:
            suivant = (a, lignes)

    if courant:
        a, b, lignes, vu = courant
        f = ImageFont.truetype(ARCH, 78 if max(len(l) for l in lignes) <= 26 else 62)
        y = int(H * 0.40) - int(f.size * 1.16 * len(lignes)) // 2
        for l in lignes:
            lg = d.textlength(l, font=f)
            d.text(((W - lg) / 2, y), l, font=f, fill=(255, 255, 255))
            y += int(f.size * 1.16)
        # la jauge : on voit combien de temps il reste pour dire la phrase
        av = (t - a) / (b - a)
        d.rectangle([120, int(H * 0.60), W - 120, int(H * 0.60) + 12], fill=(255, 255, 255, 40))
        d.rectangle([120, int(H * 0.60), 120 + int((W - 240) * av), int(H * 0.60) + 12],
                    fill=OR)
        f3 = ImageFont.truetype(INTER5, 30)
        s = "À L'IMAGE : " + vu.upper()
        lg = d.textlength(s, font=f3)
        d.text(((W - lg) / 2, int(H * 0.645)), s, font=f3, fill=(147, 197, 253))
    elif suivant and t > 2.9:
        a, lignes = suivant
        f = ImageFont.truetype(INTER, 40)
        s = "dans %.0f…" % max(0, a - t)
        lg = d.textlength(s, font=f)
        d.text(((W - lg) / 2, H * 0.40), s, font=f, fill=(120, 150, 200))
        f2 = ImageFont.truetype(INTER5, 34)
        apercu = " ".join(lignes)
        if len(apercu) > 44:
            apercu = apercu[:42] + "…"
        lg = d.textlength(apercu, font=f2)
        d.text(((W - lg) / 2, H * 0.46), apercu, font=f2, fill=(90, 120, 165))

    # le temps qui passe, en bas
    f4 = ImageFont.truetype(INTER, 28)
    d.text((60, H - 90), "%04.1f s" % t, font=f4, fill=(110, 140, 190))
    d.rectangle([0, H - 14, int(W * t / DUREE), H], fill=OR)
    return np.asarray(im)


def fabriquer(sortie):
    tube = subprocess.Popen(
        ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", sortie],
        stdin=subprocess.PIPE)
    for k in range(int(DUREE * FPS)):
        tube.stdin.write(image(k / FPS).astype(np.uint8).tobytes())
    tube.stdin.close()
    tube.wait()


def feuille():
    out = ["LE TEXTE À LIRE — MoheliGo, film de présentation", ""]
    for a, b, lignes, vu in TEXTE:
        out.append("%5.1f s  %s" % (a, " ".join(lignes)))
    return "\n".join(out)


if __name__ == "__main__":
    fabriquer(os.path.join(ICI, "SOUFFLEUR.mp4"))
    open(os.path.join(ICI, "texte-voix-off.txt"), "w", encoding="utf-8").write(feuille())
    print(feuille())
    print("\n✅ SOUFFLEUR.mp4")
