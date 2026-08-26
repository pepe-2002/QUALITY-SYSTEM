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


# ─────────────────────────────────────────────────────────────────────────────
# 🚨 LE DÉFAUT QUI A FAIT REFAIRE LA VOIX (patron, 26/08 : « il y a des parties
# dont la voix est accélérée, ça fait pas beau, et parfois tu n'entends rien »)
#
# XTTS ne tient PAS un débit constant d'une phrase à l'autre. Mesuré sur la
# première fournée : **de 8,6 à 27,1 caractères par seconde**, du simple au
# triple. À l'oreille, une phrase sur deux est lâchée à toute vitesse.
# ➡️ On ne subit plus : on **vise un débit**, on mesure ce qui sort, et on
# relance avec la vitesse corrigée jusqu'à tomber dans la bande. Cinq essais
# suffisent toujours ; on garde le meilleur si aucun ne tombe pile.
#
# 📌 LE DÉBIT N'EST PAS LE MÊME PARTOUT, ET C'EST VOULU. Un film qui fait rêver
# n'a pas un métronome : le souvenir se dit lentement, le service se dit net, la
# signature se pose. D'où une cible par phrase, écrite à la main.
DEBIT = [
     8.0,   # « Mohéli. » — un seul mot, posé lentement : c'est le titre du film
    11.0,   # le souvenir du port : lent exprès, c'est l'avant
    13.5,   # « tu réserves depuis ton téléphone » : net, c'est une information
    13.0,   # « tu paies par MVola »
    13.5,   # le billet, le code QR, même sans réseau
    13.0,   # « chaque soir, la mer de demain »
    12.5,   # « tu sais avant de partir » : on ralentit, on arrive à la fin
    12.0,   # la signature : la phrase la plus lente du film
]
BANDE = 0.06        # ±6 % autour de la cible, c'est inaudible
ESSAIS = 6
# ⚠️ Température basse = prosodie plus stable d'un essai à l'autre. Par défaut
# XTTS est à 0,75 et repart dans tous les sens ; on n'a pas besoin de sa
# fantaisie, on a besoin qu'il lise deux fois pareil.
TEMPERATURE = 0.65

# 🔎 COMMENT ON CHERCHE LA BONNE VITESSE — et pourquoi pas « à la règle de trois »
# Premier réflexe : mesurer l'écart et corriger proportionnellement. Mesuré :
# **vitesse 1,00 → 8,1 car/s ; vitesse 1,30 → 23,5 car/s.** Le réglage n'est pas
# linéaire du tout, et la règle de trois dépasse la cible à chaque coup.
# ➡️ On fait donc une **dichotomie** : trop lent, on monte la borne basse ; trop
# rapide, on descend la borne haute ; on essaie au milieu. Six essais réduisent
# l'intervalle à 1 %, quelle que soit la forme de la courbe.
VITESSE_MIN, VITESSE_MAX = 0.70, 1.35

# Puis un rattrapage fin au montage, qui **conserve la hauteur de la voix**
# (`atempo` étire le temps, pas le timbre). On s'interdit d'aller au-delà :
# au-delà de ±18 %, ça s'entend, et une voix qui « sonne trafiquée » est pire
# qu'une voix un peu rapide.
RATTRAPAGE = (0.84, 1.18)

# 🐛 LE BAVARDAGE DE XTTS. Sur un énoncé très court, le modèle ne s'arrête pas :
# pour « Mohéli. » (7 lettres) il a produit **3,6 s de contenu audible** — ce
# n'est pas du souffle, aucun seuil de silence ne l'enlève. Un débit très en
# dessous de la cible est la signature de ce défaut : on jette la prise et on
# relance, sans toucher aux bornes (le réglage n'y est pour rien).
BAVARDAGE = 0.55        # en dessous de 55 % de la cible, la prise est jetée


def parole(chemin):
    """Le temps RÉELLEMENT parlé : total moins les silences. C'est là-dessus
    qu'on mesure un débit — sinon une phrase pleine de blancs passe pour lente."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "info", "-i", chemin,
                        "-af", "silencedetect=n=-45dB:d=0.12", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    total, mute, debut = minutage.duree_fichier(chemin), 0.0, None
    for l in r.splitlines():
        if "silence_start" in l:
            debut = float(l.split("silence_start:")[1])
        elif "silence_end" in l and debut is not None:
            mute += float(l.split("silence_end:")[1].split("|")[0]) - debut
            debut = None
    if debut is not None:
        mute += total - debut
    return max(0.05, total - mute)


def cloner(reference, dossier):
    _reparer_torchaudio()
    from TTS.api import TTS
    print("chargement du modèle (le premier appel télécharge ~1,8 Go)…", flush=True)
    tts = TTS(MODELE, progress_bar=False)
    os.makedirs(dossier, exist_ok=True)
    for i, texte in enumerate(PHRASES):
        final = os.path.join(dossier, f"{i:02d}.wav")
        brut = os.path.join(dossier, f"_essai{i:02d}.wav")
        cible = DEBIT[i]
        lo, hi, vitesse = VITESSE_MIN, VITESSE_MAX, 1.0
        meilleur, jetees = None, 0
        for essai in range(ESSAIS):
            tts.tts_to_file(text=texte, speaker_wav=reference, language="fr",
                            file_path=brut, split_sentences=True,
                            speed=vitesse, temperature=TEMPERATURE)
            serrer_un(brut, final)
            d = len(texte) / parole(final)
            if d < cible * BAVARDAGE and jetees < 3:
                # le modèle a bavardé après la phrase : prise jetée, on relance
                # à la MÊME vitesse — les bornes ne sont pas en cause
                jetees += 1
                print("    essai %d  vitesse %.2f → %.1f car/s  ⛔ bavardage, prise jetée"
                      % (essai + 1, vitesse, d), flush=True)
                continue
            ecart = abs(d / cible - 1)
            print("    essai %d  vitesse %.2f → %.1f car/s  (cible %.1f)"
                  % (essai + 1, vitesse, d, cible), flush=True)
            if meilleur is None or ecart < meilleur[0]:
                meilleur = (ecart, d, open(final, "rb").read())
            if ecart <= BANDE:
                break
            if d > cible:            # trop rapide → la bonne vitesse est plus basse
                hi = vitesse
            else:                    # trop lent → elle est plus haute
                lo = vitesse
            vitesse = (lo + hi) / 2
        open(final, "wb").write(meilleur[2])
        d = meilleur[1]
        # rattrapage fin, à hauteur de voix conservée
        k = d / cible
        if abs(k - 1) > BANDE and RATTRAPAGE[0] <= 1 / k <= RATTRAPAGE[1]:
            subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", final,
                            "-af", "atempo=%.4f" % (1 / k), final + ".t.wav"], check=True)
            os.replace(final + ".t.wav", final)
            print("    rattrapage ×%.3f  → %.1f car/s" % (1 / k, cible), flush=True)
        elif abs(k - 1) > BANDE:
            print("    ⚠️ resté à %.1f car/s (cible %.1f) — hors de portée du "
                  "rattrapage, on garde la meilleure prise" % (d, cible), flush=True)
        if os.path.exists(brut):
            os.unlink(brut)
        print("  %d  %5.2f s  « %s… »" % (i, minutage.duree_fichier(final), texte[:48]),
              flush=True)
    egaliser(dossier)
    return dossier


# XTTS laisse du blanc avant le premier mot et après le dernier, et respire
# large au milieu. On enlève le blanc des bords et on plafonne les pauses
# internes — sans descendre trop bas en seuil, sinon on mange les consonnes
# douces et c'est ÇA qui donne l'impression d'une voix hachée.
SERRER = ("silenceremove=start_periods=1:start_silence=0.06:start_threshold=-48dB:"
          "stop_periods=-1:stop_silence=0.30:stop_threshold=-48dB,"
          "apad=pad_dur=0.10")


def serrer_un(entree, sortie):
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", entree,
                    "-af", SERRER, sortie], check=True)


def egaliser(dossier):
    """MÊME VOLUME POUR TOUTES LES PHRASES — l'autre moitié du défaut.

    Les phrases sortaient entre −19,9 et −15,0 LUFS : 5 dB d'écart, et sous la
    musique les plus faibles disparaissaient (« parfois tu n'entends rien »).
    Un `loudnorm` sur le mélange final ne répare pas ça : il règle la moyenne,
    pas l'écart entre les phrases. On les met donc toutes au même niveau ICI.
    📌 Et on redescend les crêtes à −3 dB : XTTS sort à 0,0 dBFS, collé au
    plafond, et ça s'entend comme une voix dure."""
    for i in range(len(PHRASES)):
        f = os.path.join(dossier, f"{i:02d}.wav")
        tmp = f + ".tmp.wav"
        subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", f,
                        "-af", "loudnorm=I=-18:TP=-3:LRA=9", "-ar", "24000", tmp],
                       check=True)
        os.replace(tmp, f)
    print("  volumes égalisés : toutes les phrases à −18 LUFS, crêtes à −3 dB")


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
        "alimiter=limit=0.95,loudnorm=I=-17:TP=-2:LRA=7[out]"
    # ⚠️ LRA=7 et pas 13. Une plage large laisse revenir l'écart de volume entre
    # les phrases — celui-là même qui faisait qu'on n'entendait plus certaines.
    # Les phrases sont déjà égalisées une par une par `egaliser()` : ici on
    # règle le niveau, on ne redistribue plus la dynamique.
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
    assembler(a.sortie)
