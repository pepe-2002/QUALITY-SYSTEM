#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LA VOIX DU PATRON, CLONÉE — pour lui faire dire le texte de la voix off.

    python3 cloner.py --reference voix/reference-patron.wav

Le patron, 26/08/2026 : « clone ma voix ».

🔒 LA RÈGLE, ET ELLE N'EST PAS NÉGOCIABLE
================================================================================
**Ce modèle ne sert QUE pour la voix du patron, sur les textes de MoheliGo, à sa
demande.** C'est SA voix, SON entreprise, SA décision : il n'y a ni usurpation ni
tromperie, il se prête sa propre voix pour gagner du temps.

⛔ **CE QU'ON NE CLONERA JAMAIS AVEC CET OUTIL** :
  · la voix du Young Leader, ni celle d'aucun partenaire, même « juste pour
    essayer » — mettre des mots dans la bouche de quelqu'un d'autre, non ;
  · la voix d'un client, d'un commandant, d'un responsable ;
  · quoi que ce soit qui laisse croire qu'une personne a dit ce qu'elle n'a
    pas dit.
📌 Le jour où on s'autorise l'exception « c'est pour rendre service », la règle
ne vaut plus rien. Elle tient parce qu'elle est absolue.

⚠️ ET MÊME POUR LUI : la voix clonée sert à **gagner des prises**, pas à
remplacer sa parole. Une vidéo où il s'engage personnellement (un avis, une
excuse, une promesse) se dit avec sa vraie voix, enregistrée ce jour-là.

--------------------------------------------------------------------------------
COMMENT ÇA MARCHE
Modèle XTTS-v2 (Coqui), synthèse multilingue avec clonage à partir d'un court
extrait. On lui donne ~12 s de sa vraie voix, propre, et le texte à dire.

⚠️ LA QUALITÉ DE LA RÉFÉRENCE FAIT TOUT. Un extrait avec du souffle, de la
réverbération ou des coupures donne une voix synthétique qui « flotte ». On lui
donne donc de la parole CONTINUE, nettoyée, sans silences.
"""
import argparse, os, subprocess, sys

os.environ.setdefault("COQUI_TOS_AGREED", "1")
ICI = os.path.dirname(os.path.abspath(__file__))
MODELE = "tts_models/multilingual/multi-dataset/xtts_v2"

# Le texte de la voix off, repris de texte-voix-off.py — une entrée par phrase.
import minutage
PHRASES = [" ".join(lignes) for lignes, vu in minutage.TEXTE]

# ⚠️ ON NE DONNE PLUS DE SECONDE À LA VOIX. Le texte disait « phrase 2 : de
# 6,4 s à 12,6 s » et la voix débordait de 3,6 s. On la laisse dire sa phrase,
# on la mesure, et `minutage.py` en déduit le film. Voir sa docstring.


def fabriquer_reference(source, sortie, morceaux):
    """Colle bout à bout de la parole CONTINUE, sans les silences."""
    parts = []
    for i, (d, f) in enumerate(morceaux):
        p = f"/tmp/_ref{i}.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y",
                        "-ss", str(d), "-t", str(f - d), "-i", source, "-vn",
                        "-ar", "22050", "-ac", "1", p], check=True)
        parts.append(p)
    liste = "/tmp/_ref.txt"
    open(liste, "w").write("".join(f"file '{p}'\n" for p in parts))
    os.makedirs(os.path.dirname(sortie) or ".", exist_ok=True)
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-f", "concat",
                    "-safe", "0", "-i", liste,
                    "-af", "highpass=f=125,afftdn=nf=-24:nt=w,"
                           "equalizer=f=230:t=q:w=1.0:g=-5,"
                           "loudnorm=I=-18:TP=-2:LRA=11",
                    "-ar", "22050", "-ac", "1", sortie], check=True)
    for p in parts:
        os.unlink(p)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", sortie], capture_output=True, text=True).stdout.strip()
    print(f"référence : {sortie}  {float(d):.1f} s de parole continue")
    return sortie


def _reparer_torchaudio():
    """⚠️ torchaudio 2.11 délègue la lecture à `torchcodec`, dont la
    bibliothèque native ne se charge pas dans cette image. On remplace
    `load`/`save` par `soundfile`, qui fait le même travail sans code natif.
    Sans ça, XTTS ne peut pas lire l'extrait de référence."""
    import numpy as np, torch, torchaudio, soundfile as sf

    def load(chemin, *a, **k):
        d, te = sf.read(str(chemin), dtype="float32", always_2d=True)
        return torch.from_numpy(d.T.copy()), te

    def save(chemin, tenseur, te, *a, **k):
        d = tenseur.detach().cpu().numpy()
        sf.write(str(chemin), d.T if d.ndim > 1 else d, te)

    torchaudio.load, torchaudio.save = load, save


def cloner(reference, dossier):
    _reparer_torchaudio()
    from TTS.api import TTS
    print("chargement du modèle (le premier appel télécharge ~1,8 Go)…", flush=True)
    tts = TTS(MODELE, progress_bar=False)
    os.makedirs(dossier, exist_ok=True)
    for i, texte in enumerate(PHRASES):
        out = os.path.join(dossier, f"{i:02d}.wav")
        tts.tts_to_file(text=texte, speaker_wav=reference, language="fr",
                        file_path=out, split_sentences=True)
        print(f"  {i}  « {texte[:56]}… »", flush=True)
    return dossier


# XTTS respire là où un lecteur respirerait — mais il respire LARGE, et il laisse
# du blanc avant le premier mot et après le dernier. On enlève ce blanc-là, et on
# ramène les pauses internes à 0,34 s : c'est ce qui a fait tomber la phrase la
# plus longue de 9,83 s à 8,55 s sans toucher au débit.
SERRER = ("silenceremove=start_periods=1:start_silence=0.06:start_threshold=-45dB:"
          "stop_periods=-1:stop_silence=0.34:stop_threshold=-45dB,"
          "apad=pad_dur=0.12")


def serrer(dossier):
    """`NN.wav` → `NN-serre.wav`. C'est la version serrée que lit `minutage.py`."""
    for i in range(len(PHRASES)):
        brut = os.path.join(dossier, f"{i:02d}.wav")
        out = os.path.join(dossier, f"{i:02d}-serre.wav")
        subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", brut,
                        "-af", SERRER, out], check=True)
        print("  phrase %d : %5.2f s → %5.2f s"
              % (i, minutage.duree_fichier(brut), minutage.duree_fichier(out)))
    return dossier


def assembler(sortie):
    """Chaque phrase à la seconde que `minutage.py` lui donne.

    📌 C'est le seul endroit qui décide de l'heure des mots — et il ne décide
    rien : il applique le minutage, qui a été calculé sur les durées réelles."""
    creneaux, duree = minutage.calculer()
    if any(c[2] is None for c in creneaux):
        raise SystemExit("❌ les phrases ne sont pas là (voix/phrases/). Elles ne "
                         "sont PAS dans Git — dépôt public. Relancer sans --remonter.")
    entrees, filtres, etiquettes = [], [], []
    for i, (a, b, f, lignes, vu) in enumerate(creneaux):
        entrees += ["-i", f]
        filtres.append(f"[{i}:a]adelay={int(a*1000)}|{int(a*1000)},"
                       f"aresample=48000[a{i}]")
        etiquettes.append(f"[a{i}]")
    chaine = ";".join(filtres) + ";" + "".join(etiquettes) + \
        f"amix=inputs={len(creneaux)}:normalize=0,apad,atrim=0:{duree}," \
        "alimiter=limit=0.95,loudnorm=I=-17:TP=-1.5:LRA=13[out]"
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y"] + entrees +
                   ["-filter_complex", chaine, "-map", "[out]",
                    "-c:a", "aac", "-b:a", "192k", sortie], check=True)
    print(f"✅ {sortie}  {duree:.2f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="/root/.claude/uploads/dd65582f-da94-5ee8-ace1-6aec9514fe93/8df373c1-VID20260826210616.mp4")
    ap.add_argument("--reference", default=os.path.join(ICI, "voix", "reference-patron.wav"))
    ap.add_argument("--sortie", default=os.path.join(ICI, "voix", "voix-off-clonee.m4a"))
    ap.add_argument("--remonter", action="store_true",
                    help="réassemble sans relancer la synthèse")
    a = ap.parse_args()
    dossier = os.path.join(ICI, "voix", "phrases")
    if not a.remonter:
        # ses blocs de parole les plus longs, relevés sur sa bande son
        if not os.path.exists(a.reference):
            fabriquer_reference(a.source, a.reference,
                                [(4.60, 7.15), (10.50, 13.80), (16.50, 19.75), (23.50, 25.85)])
        cloner(a.reference, dossier)
        serrer(dossier)
    assembler(a.sortie)
