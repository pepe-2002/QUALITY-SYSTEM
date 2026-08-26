#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LES TROIS FILMS D'IDENTITÉ MoheliGo.

    python3 identite.py              # les trois
    python3 identite.py --film 2     # un seul

COMMANDE DU PATRON (26/08/2026)
===============================
« Crée une vidéo marketing, le but renforcer notre marque et identité. Fais
3 vidéos sur notre identité. » Puis, après une première version : « les photos
ne sont pas assez neutres, crée des flyers à nous pour les vidéos », et « bien
sûr tu vas mettre le logo et utiliser notre identité ».

🎯 CE QUI REND UNE MARQUE RECONNAISSABLE
========================================
Pas de belles images : **des gestes qui reviennent**. Quatre codes, répétés à
l'identique dans les trois films. C'est la répétition qui fabrique la marque,
jamais la variété.

  1. NOS CARTES, pas des photos. Une photo appartient à son sujet ; une carte
     dessinée n'appartient qu'à nous (`cartes.py`, même grille que les flyers).
  2. LE COIN BLANC avec l'emblème, en haut à gauche, sur chaque image.
  3. LA VAGUE DORÉE QUI BALAIE l'écran à chaque changement de carte. C'est LE
     geste signature — personne d'autre ne coupe comme ça.
  4. ARCHIVO 900 blanc, UNE LIGNE EN OR par carte : celle qui porte le sens.

⚠️ AUCUN FAIT INVENTÉ : pas de distance, pas de durée, pas d'horaire. Tout ce
qui est dit est vrai et vérifiable (manuel § 11).

🎙️ LA VOIX — CE QU'ON S'AUTORISE, ET CE QU'ON NE S'AUTORISE PAS
Le patron : « la voix doit être naturelle, tu peux utiliser la voix du Young
Leader. » ✅ **On utilise UNE PHRASE QU'IL A RÉELLEMENT DITE** : « avec MoheliGo,
c'est la mer qui décide, nous on te le dit avant » — extraite telle quelle de son
tournage, et posée sur la carte finale qui dit exactement la même chose.

🚫 **CE QU'ON NE FAIT PAS : lui faire dire des phrases qu'il n'a pas dites.**
Fabriquer sa voix pour lui faire prononcer un texte qu'il n'a jamais prononcé,
c'est mettre des mots dans la bouche de quelqu'un. On ne le ferait pas sans son
accord écrit — et on n'a même pas encore obtenu sa phrase de droit à l'image.
📌 **Pour une voix sur tout le film, il faut qu'il enregistre trois prises.** Le
script est dans `dossier/BRIEF-VIDEO-YOUNG-LEADER.md`.

🔇 Le reste du film est muet, et c'est tenable : sur Facebook la majorité regarde
sans le son. Le patron peut ajouter une musique au moment de publier.
"""
import argparse, os, subprocess
import numpy as np
from PIL import Image
import cartes

ICI = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
OR = (246, 188, 28)
BALAYAGE = 0.60                      # durée du coup de vague, en secondes
NUIT = "#0A1D42"                     # le marine grave, pour les cartes fortes

VOIX = os.path.join(ICI, "voix", "signature-young-leader.m4a")

FINALE = dict(lignes=["LA MER DÉCIDE.", "NOUS, ON TE LE", "DIT AVANT."],
              mot_or=["NOUS, ON TE LE", "DIT AVANT."],
              surtitre="LA PROMESSE MoheliGo",
              pied=("RÉSERVE TA TRAVERSÉE SUR", "moheligo.com"), duree=4.2)

FILMS = [
    dict(nom="1-la-mer-decide", titre="LA MER DÉCIDE",
         # LA PROMESSE : le film qui dit d'abord ce qu'on ne maîtrise PAS.
         # C'est ce renoncement qui rend croyable tout le reste.
         cartes=[
             dict(lignes=["ICI, LA MER", "NE SE NÉGOCIE PAS."],
                  surtitre="MOHÉLI ↔ NGAZIDJA", duree=3.2),
             dict(lignes=["ELLE NE PREND PAS", "DE RENDEZ-VOUS."], duree=3.0),
             dict(lignes=["ELLE", "DÉCIDE."], mot_or=["DÉCIDE."],
                  surtitre="LA MER", fond=NUIT, duree=2.8),
             dict(lignes=["NOUS,", "ON TE LE DIT", "AVANT."], mot_or=["AVANT."],
                  surtitre="ET C'EST TOUT CE QU'ON PROMET", duree=3.6),
         ]),
    dict(nom="2-deux-rives", titre="DEUX RIVES",
         # LA GÉOGRAPHIE racontée comme un lien entre des gens. On ne vend pas
         # un siège sur une vedette : on vend une retrouvaille.
         cartes=[
             dict(lignes=["DEUX ÎLES."], surtitre="NGAZIDJA · MOHÉLI", duree=2.6),
             dict(lignes=["UN BRAS DE MER", "ENTRE LES DEUX."], duree=3.0),
             dict(lignes=["ET, DE L'AUTRE CÔTÉ,", "QUELQU'UN", "QUI ATTEND."],
                  mot_or=["QUELQU'UN"], fond=NUIT, duree=3.6),
             dict(lignes=["ON NE TRAVERSE PAS", "POUR TRAVERSER."],
                  surtitre="C'EST POUR ÇA QU'ON FAIT ÇA", duree=3.4),
         ]),
    dict(nom="3-chaque-soir", titre="CHAQUE SOIR",
         # LA PREUVE : le seul film que personne d'autre ne peut tourner, parce
         # qu'il raconte un comportement et non une promesse. Et il est vrai —
         # vérifié les jours de fermeture, où le bulletin est parti quand même.
         cartes=[
             dict(lignes=["CHAQUE SOIR,", "ON PUBLIE LA MER", "DU LENDEMAIN."],
                  surtitre="19H30, SUR CETTE PAGE", duree=3.6),
             dict(lignes=["QU'ELLE SOIT BELLE"], duree=2.2),
             dict(lignes=["OU MAUVAISE."], mot_or=["OU MAUVAISE."],
                  fond=NUIT, duree=2.4),
             # ⚠️ 26/08/2026 — ici était écrit « MÊME LES JOURS OÙ ON NE VEND
             # RIEN ». Le patron l'a fait retirer, et c'est la MÊME règle que le
             # 12/08 avec « on te vend rien » : **nommer la vente la remet dans
             # la tête du lecteur**, et la phrase parle de NOUS au lieu de parler
             # de LUI. On écrit ce qu'il gagne, jamais ce dont on s'abstient
             # (manuel § 4 et § 11).
             dict(lignes=["TU LE SAIS AVANT", "DE PARTIR", "DE CHEZ TOI."],
                  mot_or=["DE CHEZ TOI."], surtitre="TOUS LES SOIRS, SANS EXCEPTION",
                  duree=3.8),
         ]),
]


def vague(a, b, avancee):
    """LE GESTE SIGNATURE : la vague dorée balaie l'écran de gauche à droite.

    Identique dans les trois films, et elle doit le rester : c'est ce coup de
    vague — pas le logo — qui doit faire dire « c'est eux » dans un fil.
    """
    amp = 74
    ys = np.arange(H).reshape(H, 1)
    bord = avancee * (W + 4 * amp) - 2 * amp + amp * np.sin(ys / H * 3.1 * np.pi)
    xs = np.arange(W).reshape(1, W)
    out = np.where((xs < bord)[:, :, None], b, a)
    crete = np.abs(xs - bord) < 24
    out = np.where(crete[:, :, None], np.array(OR, np.uint8), out)
    halo = (np.abs(xs - bord) < 70) & ~crete
    return np.where(halo[:, :, None],
                    (out.astype(np.float32) * .55 + np.array(OR, np.float32) * .45)
                    .astype(np.uint8), out)


def derive(grande, t):
    """Un glissement très lent (1,00 → 1,035). Assez pour que l'image vive,
    assez peu pour qu'on ne le remarque pas."""
    z = 1.0 + 0.035 * t
    gh, gw = grande.shape[:2]
    vw, vh = int(gw / z), int(gh / z)
    x0, y0 = (gw - vw) // 2, (gh - vh) // 2
    return np.asarray(Image.fromarray(grande[y0:y0 + vh, x0:x0 + vw])
                      .resize((W, H), Image.LANCZOS))


def fabriquer(film, sortie, travail):
    os.makedirs(travail, exist_ok=True)
    plans = film["cartes"] + [FINALE]
    images = []
    for i, c in enumerate(plans):
        f = os.path.join(travail, f"{film['nom']}-{i}.png")
        cartes.carte(f, c["lignes"], c.get("mot_or"), c.get("surtitre"),
                     c.get("note"), c.get("fond", "#0F2A5C"), c.get("pied"))
        im = Image.open(f).convert("RGB")
        # marge de sécurité pour le glissement
        images.append(np.asarray(im.resize((int(W * 1.05), int(H * 1.05)), Image.LANCZOS)))

    tube = subprocess.Popen(
        ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", sortie],
        stdin=subprocess.PIPE)

    precedent = np.zeros((H, W, 3), np.uint8)
    nb = int(BALAYAGE * FPS)
    for i, c in enumerate(plans):
        n = int(c["duree"] * FPS)
        for k in range(n):
            img = derive(images[i], k / max(1, n - 1))
            if k < nb:
                img = vague(precedent, img, k / nb)
            tube.stdin.write(img.astype(np.uint8).tobytes())
            if k == n - 1:
                precedent = img
    tube.stdin.close()
    tube.wait()

    # LA VOIX DU YOUNG LEADER sur la carte finale — sa vraie phrase, sur la
    # carte qui dit la même chose. Elle entre 0,5 s après le coup de vague,
    # le temps que l'image se pose.
    if os.path.exists(VOIX):
        debut = sum(c["duree"] for c in plans[:-1]) + 0.5
        muet = sortie.replace(".mp4", "-muet.mp4")
        os.replace(sortie, muet)
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", muet, "-i", VOIX,
             "-filter_complex",
             f"[1:a]adelay={int(debut*1000)}|{int(debut*1000)},apad[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac",
             "-b:a", "160k", "-shortest", "-movflags", "+faststart", sortie],
            check=True)
        os.unlink(muet)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--film", type=int)
    ap.add_argument("--travail", default="/tmp/identite-moheligo")
    a = ap.parse_args()
    for i, film in enumerate(FILMS, 1):
        if a.film and a.film != i:
            continue
        sortie = os.path.join(ICI, f"MoheliGo-identite-{film['nom']}.mp4")
        fabriquer(film, sortie, a.travail)
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", sortie],
                           capture_output=True, text=True).stdout.strip()
        print(f"✅ {film['titre']:16s} → {os.path.basename(sortie)}  {float(d):.1f} s")


if __name__ == "__main__":
    main()
