#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Montage de la publicité Young Leader → MoheliGo.

    python3 monter.py --source VID....mp4 --sortie MoheliGo-YoungLeader.mp4

CE QUE FAIT CE SCRIPT, ET POURQUOI
==================================
La vidéo reçue du Young Leader le 26/08/2026 durait 52,5 s, ne montrait aucune
adresse, portait cinq fautes de français incrustées et écrivait notre nom de
deux façons. L'analyse complète est dans `dossier/VIDEO-YOUNG-LEADER-RECUE.md`.

On ne pouvait pas refilmer. Tout ce qui suit se règle au montage :

1. COUPE — on garde trois blocs de parole et on jette le reste :
     A 2,10 → 7,30   la salutation (« aux quatre coins du monde » : la diaspora)
     B 11,40 → 23,58 le message
     C 24,80 → 42,85 le nom, l'appel, et la signature
   Sont retirés : les 2 s de générique d'un autre organisme en ouverture, la
   présentation de 3 s non sous-titrée, « pour des informations quelconques »
   (tournure fautive), et les 10 s de fin sans appel à l'action.

2. RECADRAGE — on coupe 150 px en bas puis on rezoome. C'est ce qui fait
   disparaître **les anciens sous-titres fautifs** et le bandeau du nom. Le
   recadrage est calé à gauche (`crop=...:0:0`) exprès : centré, il rognait le
   logo MoheliGo incrusté dans la vidéo d'origine.

3. SOUS-TITRES — refaits à zéro dans `sous-titres.ass`, fautes corrigées et
   **MoheliGo écrit correctement partout**. ⚠️ Les temps viennent du **relevé
   exact des sous-titres d'origine** (masque du jaune, pas de 0,1 s), PAS des
   silences : les silences disent seulement « il parle / il ne parle pas ».
   La police est `polices/Inter-700.ttf`, convertie depuis **`Inter-700-latin`** :
   le sous-ensemble `latin-ext` **ne contient pas la lettre A**.

4. IMAGES — quatre photos réelles couvrent la voix aux moments qu'elles
   illustrent, chacune entrant **0,5 s avant sa phrase**. La plus importante est
   **le port de Hoani** (envoyée par le patron le 26/08) exactement sur « sans
   que vous ayez à vous rendre au port ». Les quatre racontent un voyage :
   la mer → les deux îles → le port → l'arrivée.

5. LE LIEN — une vidéo ne peut pas contenir de lien cliquable. On affiche donc
   la pastille `bande-lien.png` (**moheligo.com**) pile quand il en parle ; le
   lien sur lequel on appuie est dans le texte de la publication, écrit dans
   `dossier/TEXTES-PUBLICATIONS.md`.

6. CARTE FINALE — `../flyers/carte-fin-video.html`, rendue par l'atelier des
   flyers pour rester aux couleurs de la marque : la signature exacte du manuel,
   **moheligo.com**, et le crédit du Young Leader **avec le logo de son Comité**
   (`../photos-partenaires/young-leader-logo.png`, détouré depuis leur propre
   générique). Un partenaire se cite avec son logo, pas seulement son nom.

⚠️ Le fichier reçu est une version compressée par WhatsApp (576×1024). Avec
l'original, ne rien changer d'autre que `--source`.
"""
import argparse, os, subprocess, sys
import cv2, numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", ".."))
W, H = 576, 1024
PW, PH = 576, 730                     # la photo, en 4:5, occupe 71 % de la hauteur

# (début, durée) des blocs de parole gardés, en secondes de la vidéo d'origine.
# ⚠️ Ces bornes ne sont PAS estimées : elles viennent du relevé exact des
# sous-titres d'origine (masque du jaune, pas de 0,1 s). Les sous-titres du
# tournage sont la seule vérité disponible sur QUI dit QUOI et QUAND — ils ont
# été écrits par quelqu'un qui entendait la bande son. Ma première version les
# avait devinés à partir des silences, et trois phrases tombaient à côté.
SEGMENTS = [(2.10, 5.20), (11.40, 12.18), (24.80, 18.05)]
BAS_COUPE = 150                       # px retirés en bas : anciens sous-titres + bandeau

# (photo, début, fin) dans le montage — cale sur la phrase qu'elles illustrent
# ⚠️ Chaque plan démarre ~0,5 s AVANT la phrase qu'il illustre. Le patron a vu le
# défaut : « il parle avant et l'image vient après ». On coupe sur l'idée qui
# entre, jamais après elle.
PLANS = [
    ("pub/photos/vedette-mer.jpg",     10.60, 13.05),  # « nos voyages maritimes »
    ("pub/photos/ilot.jpg",            13.05, 15.05),  # « entre Mohéli et Ngazidja »
    ("PORT_HOANI",                     15.05, 17.36),  # « sans vous rendre au port »
    # 4ᵉ champ facultatif : la ZONE de la photo à utiliser (x0, y0, x1, y1 en
    # fractions), avant le cadrage 4:5. Ici on jette les 22 % du bas — il y a une
    # voiture au premier plan, et une voiture n'a rien à faire dans une image
    # qui doit donner envie de traverser.
    ("pub/photos/plage-vedettes.jpg",  27.00, 30.20, (0.0, 0.0, 1.0, 0.78)),
]

# La pastille moheligo.com, pile quand il dit « cliquez sur le lien ». Une vidéo
# ne peut pas contenir de lien cliquable : le cliquable va dans le texte de la
# publication Facebook, l'adresse à l'écran sert à ce qu'on la retienne.
BANDE_LIEN = (25.58, 31.28)


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ÉCHEC : " + cmd + "\n" + r.stderr[-1500:])
    return r.stdout.strip()


def fabriquer_plan(src, dest, zone=None):
    """Photo en 4:5 sur un fond flouté tiré d'elle-même, voile sombre en bas
    pour que les sous-titres restent lisibles.

    `zone` = (x0, y0, x1, y1) en fractions : la partie de la photo à garder
    avant le cadrage 4:5. Sert à écarter ce qui traîne au premier plan."""
    im = cv2.imread(src)
    if im is None:
        sys.exit("photo introuvable : " + src)
    if zone:
        H0, W0 = im.shape[:2]
        x0, y0, x1, y1 = zone
        im = im[int(y0 * H0):int(y1 * H0), int(x0 * W0):int(x1 * W0)]
    h, w = im.shape[:2]
    s = max(W / w, H / h) * 1.3
    bg = cv2.resize(im, (int(w * s), int(h * s)))
    bg = bg[(bg.shape[0] - H) // 2:(bg.shape[0] - H) // 2 + H,
            (bg.shape[1] - W) // 2:(bg.shape[1] - W) // 2 + W].copy()
    bg = cv2.GaussianBlur(bg, (0, 0), 30)
    bg = np.clip(bg.astype(np.float32) * 0.62 + 18, 0, 255).astype(np.uint8)

    ar = PW / PH
    nw, nh = (int(h * ar), h) if w / h > ar else (w, int(w / ar))
    ph = cv2.resize(im[(h - nh) // 2:(h - nh) // 2 + nh,
                       (w - nw) // 2:(w - nw) // 2 + nw],
                    (PW, PH), interpolation=cv2.INTER_CUBIC)
    if max(w, h) < 1200:                       # photo déjà compressée : on la raffermit
        ph = cv2.detailEnhance(ph, sigma_s=5, sigma_r=0.13)
    yy = int((H - PH) * 0.38)
    bg[yy:yy + PH, 0:PW] = ph

    y0 = int(H * 0.68); n = H - y0
    g = np.linspace(0, 1, n).reshape(n, 1, 1)
    bg[y0:] = (bg[y0:].astype(np.float32) * (1 - 0.62 * g)).astype(np.uint8)
    cv2.imwrite(dest, bg)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True, help="la vidéo reçue du Young Leader")
    p.add_argument("--port-hoani", default=os.path.join(ICI, "port-hoani.jpg"),
                   help="photo du port de Hoani (patron, 26/08/2026)")
    p.add_argument("--sortie", default=os.path.join(ICI, "MoheliGo-YoungLeader.mp4"))
    p.add_argument("--travail", default="/tmp/montage-moheligo")
    a = p.parse_args()
    T = a.travail
    os.makedirs(T, exist_ok=True)

    # 1. les trois blocs de parole, puis on les recolle
    liste = os.path.join(T, "liste.txt")
    with open(liste, "w") as f:
        for i, (deb, dur) in enumerate(SEGMENTS):
            seg = os.path.join(T, f"seg{i}.mp4")
            sh(f'ffmpeg -hide_banner -v error -y -ss {deb} -t {dur} -i "{a.source}" '
               f'-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 '
               f'-c:a aac -b:a 128k -ar 44100 -ac 2 '
               f'-af "afade=t=in:st=0:d=0.05,afade=t=out:st={dur-0.05:.2f}:d=0.05" "{seg}"')
            f.write(f"file '{seg}'\n")
    base = os.path.join(T, "base.mp4")
    sh(f'ffmpeg -hide_banner -v error -y -f concat -safe 0 -i "{liste}" -c copy "{base}"')

    # 2. les plans de coupe et le filigrane
    for i, pl in enumerate(PLANS):
        rel = pl[0]
        zone = pl[3] if len(pl) > 3 else None
        src = a.port_hoani if rel == "PORT_HOANI" else os.path.join(RACINE, rel)
        fabriquer_plan(src, os.path.join(T, f"plan{i}.png"), zone)
    lg = cv2.imread(os.path.join(RACINE, "MoheliGo-logo.png"), cv2.IMREAD_UNCHANGED)
    lw = 185
    cv2.imwrite(os.path.join(T, "logo.png"),
                cv2.resize(lg, (lw, int(lg.shape[0] * lw / lg.shape[1])),
                           interpolation=cv2.INTER_AREA))

    # 3. la carte finale, par l'atelier des flyers (mêmes polices, mêmes couleurs)
    carte = os.path.join(T, "carte-fin.png")
    flyers = os.path.join(RACINE, "pub", "flyers")
    sh(f'cd "{flyers}" && node render.js carte-fin-video.html "{carte}" 1080 1920 1')

    # 4. recadrage (efface les anciens sous-titres), plans, filigrane, sous-titres
    entrees = f'-i "{base}" -loop 1 -i {T}/logo.png ' + \
              " ".join(f'-loop 1 -i {T}/plan{i}.png' for i in range(len(PLANS))) + \
              f' -loop 1 -i "{ICI}/bande-lien.png"'
    ch = ("[0:v]crop=576:%d:0:0,scale=-2:1024:flags=lanczos,crop=576:1024:0:0,"
          "eq=saturation=1.06:contrast=1.03[z];" % (H - BAS_COUPE))
    prec = "z"
    for i, pl in enumerate(PLANS):
        d, fin = pl[1], pl[2]
        ch += f"[{prec}][{i+2}:v]overlay=0:0:enable='between(t,{d},{fin})'[p{i}];"
        prec = f"p{i}"
    # la pastille du lien, par-dessus les plans de coupe
    ch += (f"[{prec}][{len(PLANS)+2}:v]overlay=0:0:"
           f"enable='between(t,{BANDE_LIEN[0]},{BANDE_LIEN[1]})'[lien];")
    # le filigrane s'arrête quand le logo incrusté d'origine apparaît (19,4 s)
    ch += "[lien][1:v]overlay=24:26:enable='lt(t,19.4)'[e];"
    ch += f"[e]subtitles={ICI}/sous-titres.ass:fontsdir={ICI}/polices[v]"
    corps = os.path.join(T, "corps.mp4")
    sh(f'ffmpeg -hide_banner -v error -y {entrees} -filter_complex "{ch}" '
       f'-map "[v]" -map 0:a -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p '
       f'-c:a aac -b:a 128k -shortest "{corps}"')

    # 5. la carte finale en vidéo, puis on recolle
    cartemp4 = os.path.join(T, "carte.mp4")
    sh(f'ffmpeg -hide_banner -v error -y -loop 1 -t 4.0 -i "{carte}" '
       f'-f lavfi -t 4.0 -i anullsrc=r=44100:cl=stereo '
       f'-vf "scale=576:1024:flags=lanczos,fade=t=in:st=0:d=0.35,format=yuv420p" -r 30 '
       f'-c:v libx264 -preset medium -crf 19 -c:a aac -b:a 128k "{cartemp4}"')
    fin = os.path.join(T, "final.txt")
    open(fin, "w").write(f"file '{corps}'\nfile '{cartemp4}'\n")
    sh(f'ffmpeg -hide_banner -v error -y -f concat -safe 0 -i "{fin}" -c copy "{a.sortie}"')

    d = sh(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{a.sortie}"')
    print(f"✅ {a.sortie}  —  {float(d):.1f} s, {W}x{H}")


if __name__ == "__main__":
    main()
