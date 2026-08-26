#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NETTOYER UNE VOIX ENREGISTRÉE AU TÉLÉPHONE.

    python3 voix.py --source enregistrement.mp4 --sortie voix/patron-propre.m4a

Le patron, 26/08/2026 : « utilise ma voix mais améliore-la un peu 😂 ».

📌 CE QU'ON PEUT VRAIMENT FAIRE, ET CE QU'ON NE PEUT PAS
« Améliorer une voix » ne veut pas dire la changer. On ne rend pas une voix plus
grave ni plus belle : **on retire ce qui la gêne**. Ce qui suit est mesurable —
sur l'enregistrement du 26/08, le niveau moyen est passé de **−30,4 dB à
−17,2 dB**, à la norme des plateformes.

LA CHAÎNE, ÉTAGE PAR ÉTAGE (aucun n'est décoratif) :
  · highpass 85 Hz ....... coupe le grondement et les bruits de main sur le
                           téléphone. Rien d'utile dans une voix en dessous.
  · afftdn ............... retire le souffle de la pièce, mesuré puis soustrait.
                           Trop fort, il donne une voix « sous l'eau » : −26 dB.
  · −3 dB à 260 Hz ....... enlève le côté « boîte » d'une pièce fermée.
  · +3,5 dB à 3,2 kHz .... la bande de l'intelligibilité : c'est ce qui fait
                           qu'on comprend les mots sur un haut-parleur de
                           téléphone, dans la rue.
  · +2 dB au-dessus de 9 kHz ... rend l'air, l'enregistrement respire.
  · deesser .............. les « s » sifflants que le +3,5 kHz vient d'aggraver.
  · acompressor .......... resserre l'écart entre les mots forts et faibles :
                           on n'a plus à monter le son pour comprendre.
  · alimiter + loudnorm .. −16 LUFS, la norme Facebook / Instagram. En dessous,
                           la plateforme remonte elle-même et ramène le souffle.

📦 TROIS FORMATS, ET C'EST VOULU. Le patron n'arrivait pas à ouvrir le `.m4a` :
un fichier son ne se lit pas partout, une VIDÉO si. On livre donc toujours
`.m4a` (le montage), `.mp3` (n'importe quel téléphone) et un `.mp4` — une carte
MoheliGo fixe avec le son dessus. **Un livrable qui ne s'ouvre pas n'est pas
livré.**

🎚️ QUAND LE PATRON DIT « TROP GROS » — ON NE DEVINE PAS, ON FAIT ÉCOUTER.
Le 26/08 il a trouvé sa voix « trop grosse ». Une remarque de goût ne se règle
pas en tâtonnant : on fabrique **trois réglages sur le même extrait**, annoncés
à l'écran, et il rend un numéro. `voix/COMPARE-3-reglages.mp4`.

  1. LÉGÈRE ..... coupe à 125 Hz, −5 dB à 230 Hz, −2,5 dB à 420 Hz, compression
                  douce (2:1). C'est le réglage qui dégraisse une voix épaisse.
  2. NATURELLE .. souffle et niveau, RIEN d'autre. Aucune couleur ajoutée.
  3. la chaîne ci-dessus (celle qu'il a trouvée trop grosse).

📌 **Trois options valent mieux que dix questions.** Sur une question de goût,
l'oreille du patron tranche en douze secondes ce qu'un échange de messages ne
tranche pas en dix minutes.

⚠️ ON NE FABRIQUE JAMAIS UNE VOIX. Nettoyer l'enregistrement de quelqu'un qui
nous l'a donné, oui. Synthétiser sa voix pour lui faire dire ce qu'il n'a pas
dit, non — voir `identite.py`.
"""
import argparse, os, subprocess

CHAINE = ("highpass=f=85,"
          "afftdn=nf=-26:nt=w,"
          "equalizer=f=260:t=q:w=1.1:g=-3,"
          "equalizer=f=3200:t=q:w=1.4:g=3.5,"
          "equalizer=f=9000:t=h:g=2,"
          "deesser=i=0.35,"
          "acompressor=threshold=-20dB:ratio=3.2:attack=8:release=180:makeup=2,"
          "alimiter=limit=0.94,"
          "loudnorm=I=-16:TP=-1.5:LRA=11")


def niveau(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "volumedetect",
                        "-f", "null", "-"], capture_output=True, text=True).stderr
    return [l.split("] ")[-1] for l in r.splitlines() if "mean_volume" in l][0]


def nettoyer(source, sortie, debut=None, duree=None):
    os.makedirs(os.path.dirname(sortie) or ".", exist_ok=True)
    cmd = ["ffmpeg", "-hide_banner", "-v", "error", "-y"]
    if debut is not None:
        cmd += ["-ss", str(debut)]
    if duree is not None:
        cmd += ["-t", str(duree)]
    cmd += ["-i", source, "-vn", "-af", CHAINE, "-ar", "48000", "-ac", "1",
            "-c:a", "aac", "-b:a", "192k", sortie]
    subprocess.run(cmd, check=True)
    print(f"avant : {niveau(source)}\naprès : {niveau(sortie)}\n→ {sortie}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--sortie", default="voix/propre.m4a")
    ap.add_argument("--debut", type=float, help="secondes")
    ap.add_argument("--duree", type=float, help="secondes")
    a = ap.parse_args()
    nettoyer(a.source, a.sortie, a.debut, a.duree)
