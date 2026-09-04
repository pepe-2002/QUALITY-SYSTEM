#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LA VOIX OFF DES FILMS — écrite, prononcée, puis travaillée comme en studio.

    python3 voix.py --essai        → un extrait avec les trois voix, à comparer
    (sinon, `film.py` l'appelle tout seul)

CE QUE FAIT CE FICHIER, DANS L'ORDRE
  1. Il tire de `scenarios.py` le texte à DIRE — un texte par image du film,
     pas un texte par scène : la voix arrive donc exactement quand la ligne
     apparaît à l'écran, sans avoir à caler quoi que ce soit à la main.
  2. Il le réécrit pour la bouche (`prononcer`). C'est l'étape que tout le
     monde saute, et c'est celle qui trahit le travail bâclé : une synthèse à
     qui l'on donne « 5 h 30 », « 3 kg » ou « GRD-PROC-001 » dit « cinq h
     trente », « trois kg » et « gerdeproc zéro zéro un ».
  3. Il synthétise (Piper, modèle neuronal français, tourne hors ligne).
  4. Il POLIT — et c'est là que « synthèse vocale » devient « voix off » :
     coupe des graves, réduction de souffle, creux à 250 Hz, présence à
     3,2 kHz, dé-essage, compression, et normalisation à −16 LUFS.

📌 POURQUOI UNE VOIX DE SYNTHÈSE ET PAS UN COMÉDIEN
Un comédien français facturerait plus que le film entier, et pour deux films
qui seront corrigés à chaque révision du GOM, il faudrait le rappeler à chaque
fois. Ici, corriger une phrase du scénario et relancer le montage suffit : la
voix se refait toute seule, sur toute la ligne. Le jour où le patron veut sa
propre voix, elle se substitue sans rien changer d'autre — le montage cale déjà
chaque image sur la durée du fichier son qu'on lui donne.

⚠️ CE QUE ÇA N'EST PAS. Ce n'est pas une voix humaine et cela s'entend sur les
phrases longues. Le texte a donc été écrit court, en phrases simples : c'est
exactement ce qu'il faut pour une voix off de formation, et c'est ce qui rend
le résultat propre plutôt que « robotique ».
"""
import argparse
import os
import re
import subprocess

ICI = os.path.dirname(os.path.abspath(__file__))
MODELES = os.path.join(ICI, ".travail", "voix")

# 🗣️ LE CHOIX DU PATRON, 04/09/2026 : la deuxième voix de COMPARER-LES-VOIX.mp4,
# c'est-à-dire fr_FR-siwis. « voix numéro 2 mais c un peu trop rapide ».
# Ne pas changer sans le lui redemander : une voix, c'est la sienne, pas un
# réglage technique. L'ordre de l'extrait de comparaison ci-dessous est celui
# sur lequel il s'est prononcé — le modifier rendrait sa réponse illisible.
VOIX = "fr_FR-siwis-medium"
VOIX_COMPARAISON = ["fr_FR-tom-medium", "fr_FR-siwis-medium", "fr_FR-upmc-medium"]

# L'allure : plus le nombre est grand, plus la voix est posée.
#
# 🗣️ RÉGLÉE PAR L'OREILLE DU PATRON, 04/09/2026 : « un peu trop rapide ».
# Mesure faite après coup sur un vrai passage du film, en mots par minute :
#     0,90 → 165     ← ce qu'il a entendu
#     1,00 → 149
#     1,15 → 140     ← retenu
#     1,25 → 130
#     1,35 → 119     (là, ça traîne)
#
# ⚠️ ET LA LEÇON, QUI VAUT POUR LA PROCHAINE FOIS : l'allure n'est PAS une
# propriété du réglage, elle dépend de la voix. Le même 0,90 donnait 140 mots
# par minute avec la voix « tom » et 165 avec « siwis ». Changer de voix sans
# remesurer, c'est changer le débit sans s'en apercevoir. Toute nouvelle voix
# se recalibre sur un passage réel, jamais sur une phrase d'essai — les
# silences entre phrases comptent dans le rythme perçu.
#
# 📌 POURQUOI 140 ET NON LES 150 DE LA NORME
# Les 145-160 mots/minute sont l'allure d'une voix qui raconte à quelqu'un qui
# écoute. Ici la voix parle à quelqu'un qui LIT en même temps : chaque phrase
# double une ligne affichée. Il faut le temps de faire les deux, et c'est la
# lecture qui commande, pas la parole.
ALLURE = 1.15

# LE TON. Deux réglages du modèle, laissés à leur valeur d'origine.
#   SOUFFLE (noise_scale, 0.667) — la part d'aléa dans la voix. En baissant,
#     on obtient une voix plus lisse ; trop bas, elle devient plate et sonne
#     « machine ».
#   VARIATION (noise_w, 0.8) — la variabilité de la durée des sons, c'est-à-dire
#     le naturel du débit. En baissant, chaque syllabe dure pareil : très
#     régulier, et très artificiel.
# ⚠️ On ne les a PAS bougés. Le naturel qui manquait ne venait pas du timbre
# mais du phrasé — la voix ne respirait pas aux virgules. C'est corrigé par le
# découpage plus bas, à la source du problème. Toucher au timbre par-dessus,
# sans pouvoir écouter, ne ferait que remplacer un défaut par un autre.
SOUFFLE = 0.667
VARIATION = 0.8


# ════════════════════════════════════════════ 1. écrire ce qui doit être dit
def a_dire(scene, n):
    """Le texte de la n-ième image d'une scène (n commence à 1).

    La voix DIT ce qui est affiché, et rien de plus. C'est un choix : dans un
    film de formation, l'écart entre ce qu'on lit et ce qu'on entend fatigue —
    on finit par ne plus suivre ni l'un ni l'autre. La règle « la voix ne lit
    pas les sous-titres » vaut pour un documentaire, pas pour une consigne."""
    t = scene["type"]
    if t == "ouverture":
        return "Royal Air. Département Qualité. %s. %s" % (scene["titre"], scene["sous_titre"])
    if t == "situation":
        return "La situation. %s %s" % (scene["texte"], scene["question"])
    if t == "chapitre":
        return scene["titre"] + "."
    if t == "regle":
        return "%s %s" % (scene["texte"], scene.get("appui", ""))
    if t == "liste":
        p = scene["points"][n - 1]
        return (scene["titre"] + " " + p) if n == 1 else p
    if t == "duo":
        mauvais, bon = scene["paires"][n - 1]
        debut = (scene["titre"] + " ") if n == 1 else ""
        # ⚠️ le point après la mauvaise phrase n'est pas cosmétique : sans lui,
        # « ... jamais l'inverse Dites : ... » est lu d'un seul souffle.
        return "%sNe dites pas : %s Dites plutôt : %s" % (debut, mauvais.rstrip(". ") + ".",
                                                          bon)
    if t == "cloture":
        rang = ["Un.", "Deux.", "Trois.", "Quatre.", "Cinq.",
                "Six.", "Sept.", "Huit.", "Neuf.", "Dix."][n - 1]
        debut = (scene["titre"] + ". ") if n == 1 else ""
        return "%s%s %s" % (debut, rang, scene["points"][n - 1])
    if t == "fin":
        return ("Ce film est interne. Il reste dans le groupe du personnel Royal Air. "
                "Il ne se publie pas. Merci de votre attention.")
    return ""


# ═══════════════════════════════════════════════ 2. le réécrire pour la bouche
UNITES = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit",
          "neuf", "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize",
          "dix-sept", "dix-huit", "dix-neuf"]
DIZAINES = {20: "vingt", 30: "trente", 40: "quarante", 50: "cinquante",
            60: "soixante", 80: "quatre-vingt"}


def en_lettres(n):
    """Les nombres qu'on rencontre ici : heures, kilos, numéros de vol, années.
    Au-delà de 9999 on n'en a pas, et une fonction qui couvre tout serait dix
    fois plus longue pour rien."""
    n = int(n)
    if n < 20:
        return UNITES[n]
    if n < 100:
        for base in (80, 60, 40, 30, 20):
            if n >= base:
                reste = n - base
                if base == 60 and reste > 19:          # soixante-dix…
                    return "soixante-" + en_lettres(reste)
                if base == 80 and reste > 19:          # quatre-vingt-dix…
                    return "quatre-vingt-" + en_lettres(reste)
                if reste == 0:
                    return DIZAINES[base] + ("s" if base == 80 else "")
                if reste == 1 and base in (20, 30, 40, 50, 60):
                    return DIZAINES[base] + " et un"
                return DIZAINES[base] + "-" + en_lettres(reste)
    if n < 1000:
        c, r = divmod(n, 100)
        tete = "cent" if c == 1 else en_lettres(c) + " cent"
        if r == 0:
            return tete + ("" if c == 1 else "s")
        return tete + " " + en_lettres(r)
    m, r = divmod(n, 1000)
    tete = "mille" if m == 1 else en_lettres(m) + " mille"
    return tete if r == 0 else tete + " " + en_lettres(r)


# Les sigles maison. Certains se lisent lettre par lettre, d'autres se
# prononcent comme un mot — et deux se disent en clair parce qu'un agent qui
# entend « P M R » pour la première fois ne sait pas de quoi on parle.
SIGLES = {
    "ANACM": "A-N-A-C-M", "OACI": "O-A-C-I", "SGS": "S-G-S", "PMR": "P-M-R",
    "GOM": "G-O-M", "PIR": "P-I-R", "MANEX": "manex", "AOC": "A-O-C",
    "LET": "L-E-T", "HAH": "H-A-H", "AJN": "A-J-N", "NWA": "N-W-A",
    "UM": "U-M", "ISO": "isso", "WhatsApp": "watsapp", "MEL": "M-E-L",
}


def prononcer(txt):
    """Réécrit un texte affiché en un texte prononçable.

    Chaque règle ci-dessous vient d'une faute entendue à l'essai — rien n'est
    préventif. C'est trente lignes qui font toute la différence entre une
    synthèse d'amateur et une voix off qu'on écoute jusqu'au bout."""
    t = txt

    # la ponctuation d'écran n'a pas de son
    t = (t.replace("’", "'").replace(" ", " ")
           .replace("«", "").replace("»", "")
           .replace("—", ",").replace("·", ",").replace("…", "."))

    # les références de procédure : « GRD-PROC-001 » → « G-R-D proc zéro zéro un »
    def _proc(m):
        lettres = "-".join(m.group(1))
        chiffres = " ".join(en_lettres(c) for c in m.group(2))
        return "%s proc, %s" % (lettres, chiffres)
    t = re.sub(r"\b([A-Z]{3})-PROC-(\d{3})\b", _proc, t)

    # les heures : « 5 h 30 » → « cinq heures trente » ; « 7 h » → « sept heures »
    t = re.sub(r"\b(\d{1,2})\s*h\s*(\d{2})\b",
               lambda m: "%s heures %s" % (en_lettres(m.group(1)), en_lettres(m.group(2))), t)
    t = re.sub(r"\b(\d{1,2})\s*h\b(?!\w)",
               lambda m: "%s heures" % en_lettres(m.group(1)), t)

    # les unités
    t = re.sub(r"\b(\d+)\s*kg\b", lambda m: "%s kilos" % en_lettres(m.group(1)), t)
    t = re.sub(r"\b(\d+)\s*(km|m)\b", lambda m: "%s mètres" % en_lettres(m.group(1)), t)

    # « le vol du 12 » → « le vol du douze »
    t = re.sub(r"\b(\d{1,4})\b", lambda m: en_lettres(m.group(1)), t)

    # les sigles, une fois les nombres traités (sinon « LET 410 » se casse)
    for sigle, dit in SIGLES.items():
        t = re.sub(r"\b%s\b" % re.escape(sigle), dit, t)

    # ce qui reste en capitales n'est PAS un sigle : c'est une insistance
    # d'écriture (« ... AVANT que le passager ne le demande »). Laissée telle
    # quelle, la synthèse l'épelle. À l'oral, l'insistance passe par le sens,
    # pas par la casse — on remet donc en minuscules.
    t = re.sub(r"\b[A-ZÉÈÀÇÔÎÊÛ]{3,}\b", lambda m: m.group(0).lower(), t)

    # une virgule vaut une respiration : deux-points et points-virgules en font
    # de meilleures que leur signe d'origine, que la synthèse ignore
    # ⚠️ NE PAS transformer « : » et « ; » en virgules. C'était le cas au début,
    # quand la synthèse ignorait tout sauf le point et la virgule. Maintenant
    # que les silences sont posés à la main, le deux-points vaut une pause plus
    # longue que la virgule — et c'est lui qui annonce : « Ne dites pas : … ».
    # Le rabattre sur une virgule, c'est perdre exactement l'effet recherché.

    # ménage : les remplacements ci-dessus laissent des « , , » et des espaces
    # avant la ponctuation. La synthèse marque une pause à chaque virgule —
    # deux virgules d'affilée font un trou dans la phrase.
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"(,\s*){2,}", ", ", t)
    t = re.sub(r",\s*\.", ".", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


# ══════════════════════════════════ 3. découper la phrase sur sa ponctuation
# Les silences, en secondes, selon le signe qui ferme le morceau.
# Ce ne sont pas des valeurs de goût : elles remplacent ce que la synthèse ne
# fait pas d'elle-même. MESURE FAITE SUR NOTRE VOIX, le 04/09/2026 :
#   · un point ....... la synthèse marque 0,50 à 0,65 s. C'est bien, on garde.
#   · une virgule .... elle marque 0,08 s. Autant dire rien : la virgule est
#                      avalée, et c'est exactement ce que le patron entendait.
# D'où ce qui suit : on découpe la phrase à chaque signe, on synthétise les
# morceaux séparément, et on pose SOI-MÊME le silence.
SILENCE = {",": 0.26, ";": 0.32, ":": 0.38, ".": 0.50, "?": 0.58, "!": 0.52, "": 0.34}

# ⚠️ ET POURQUOI ÇA NE HACHE PAS LA PHRASE
# Découper une phrase et la recoller, c'est risquer que chaque morceau se
# termine comme une phrase — intonation qui retombe, lecture en escalier.
# On garde donc le signe de ponctuation À LA FIN du morceau qu'on synthétise.
# Vérifié à la mesure, sur le même fragment « Comptoir propre » :
#     fini par une virgule → la voix tient à 150 Hz  (la phrase continue)
#     fini par un point ... → la voix retombe à 138 Hz (la phrase est finie)
# Le morceau qui se termine par une virgule garde donc sa suspension. C'est ce
# qui permet de coller les morceaux sans que cela s'entende.
COUPURES = re.compile(r"[^,;:.!?]+[,;:.!?]?")


def decouper(txt):
    """Découpe un texte en morceaux prononçables, avec le silence qui suit."""
    morceaux = []
    for brut in COUPURES.findall(txt):
        m = brut.strip()
        if not m or not any(c.isalnum() for c in m):
            continue
        fin = m[-1] if m[-1] in SILENCE else ""
        morceaux.append((m, SILENCE[fin]))
    if morceaux:                       # rien à attendre après le dernier mot
        morceaux[-1] = (morceaux[-1][0], 0.0)
    return morceaux


def _serrer(x, te, seuil=0.015, marge=0.025):
    """Enlève le silence que la synthèse laisse en tête et en queue de chaque
    morceau. Sans ce serrage, le silence qu'on ajoute s'empile sur celui qui
    est déjà là et la pause dure le double de ce qu'on a demandé."""
    import numpy as np
    fort = np.abs(x) > seuil * (np.abs(x).max() + 1e-9)
    if not fort.any():
        return x
    i, j = np.argmax(fort), len(fort) - np.argmax(fort[::-1])
    m = int(marge * te)
    return x[max(0, i - m):min(x.size, j + m)]


# ═══════════════════════════════════════════════════ 4. synthétiser et polir
def modele(nom):
    return os.path.join(MODELES, nom + ".onnx")


_CHARGE = {}


def _moteur(nom):
    """Charge le modèle UNE FOIS et le garde.

    ⚠️ POURQUOI CE N'EST PAS UN DÉTAIL. La première version appelait la
    synthèse en ligne de commande, un processus par texte. C'était tenable tant
    qu'il y avait un texte par image (~90 par film). Depuis qu'on découpe à la
    ponctuation, il y a cinq à six morceaux par image, soit plus de cinq cents
    appels par film — et chacun rechargeait 63 Mo de modèle. Le montage serait
    passé de quarante minutes à plusieurs heures pour un résultat identique.
    Le modèle est donc chargé en mémoire, une fois, et réutilisé."""
    from piper import PiperVoice
    if nom not in _CHARGE:
        _CHARGE[nom] = PiperVoice.load(modele(nom))
    return _CHARGE[nom]


def dire(texte, sortie, voix=VOIX, allure=ALLURE):
    """Synthèse brute d'un texte, morceau par morceau.

    C'est ici que la ponctuation devient audible : chaque morceau est
    synthétisé seul, serré, puis posé sur une piste avec le silence que son
    signe de ponctuation commande. Le résultat n'est pas « une voix lue plus
    lentement » — c'est une voix qui respire aux bons endroits, ce qui n'est
    pas la même chose et s'entend tout de suite."""
    import numpy as np
    import wave

    morceaux = decouper(texte)
    if not morceaux:
        return None

    from piper import SynthesisConfig
    moteur = _moteur(voix)
    reglage = SynthesisConfig(length_scale=allure, noise_scale=SOUFFLE,
                              noise_w_scale=VARIATION, normalize_audio=True)

    pistes, te = [], None
    for m, pause in morceaux:
        bouts = []
        for bout in moteur.synthesize(m, syn_config=reglage):
            te = bout.sample_rate
            bouts.append(np.frombuffer(bout.audio_int16_bytes, dtype=np.int16))
        if not bouts:
            continue
        x = np.concatenate(bouts).astype(np.float32) / 32768
        pistes.append(_serrer(x, te))
        if pause:
            pistes.append(np.zeros(int(pause * te), dtype=np.float32))

    tout = np.concatenate(pistes)
    with wave.open(sortie, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(te)
        w.writeframes((tout * 32767).astype(np.int16).tobytes())
    return sortie


CHAINE_STUDIO = (
    # Chaque étage répond à un défaut mesuré, aucun n'est décoratif.
    "highpass=f=85,"                       # le grondement sous la voix : rien d'utile
    "afftdn=nr=10:nf=-32,"                 # le souffle de synthèse, mesuré puis soustrait
    "equalizer=f=260:t=q:w=1.1:g=-2.5,"    # enlève le côté « boîte »
    "equalizer=f=3200:t=q:w=1.3:g=3,"      # la bande de l'intelligibilité : ce qui fait
                                           # qu'on comprend dans un couloir
    "equalizer=f=9000:t=h:g=1.5,"          # un peu d'air, l'enregistrement respire
    "deesser=i=0.4,"                       # les « s » que le +3,2 kHz vient d'aggraver
    "acompressor=threshold=-19dB:ratio=3:attack=12:release=260,"  # resserre fort et faible
    "loudnorm=I=-16:TP=-1.5:LRA=11,"       # la norme de diffusion
    "aresample=48000"
)


def polir(entree, sortie):
    """Le traitement studio. C'est lui qui fait la différence à l'oreille."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", entree,
                    "-af", CHAINE_STUDIO, "-ac", "1", "-ar", "48000", sortie], check=True)
    return sortie


def duree(fichier):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of", "csv=p=0", fichier],
                                capture_output=True, text=True).stdout.strip())


def fabriquer(texte, sortie, voix=VOIX):
    """Le tout : écrit → prononçable → synthétisé → poli. Renvoie la durée."""
    if not texte.strip():
        return None, 0.0
    brut = sortie + ".brut.wav"
    dire(prononcer(texte), brut, voix)
    polir(brut, sortie)
    os.remove(brut)
    return sortie, duree(sortie)


# ══════════════════════════════════════════════════════ l'extrait de contrôle
def essai():
    """Un même passage dit par les trois voix, pour que le patron choisisse.

    Une voix ne se choisit pas sur une fiche technique : elle s'écoute. Le
    fichier produit annonce chaque voix par son nom avant de la faire parler."""
    import sys
    sys.path.insert(0, ICI)
    import scenarios
    sc = scenarios.ESCALE["scenes"]
    # un passage représentatif : une phrase de garde, une mise en situation avec
    # des heures et un nom d'escale, et une règle. De quoi juger le grain de la
    # voix, sa prononciation des chiffres, et son autorité.
    choisies = [sc[0], next(s for s in sc if s["type"] == "situation"),
                next(s for s in sc if s["type"] == "regle")]
    passage = " ".join(a_dire(s, 1) for s in choisies)
    dossier = os.path.join(ICI, ".travail", "essai-voix")
    os.makedirs(dossier, exist_ok=True)
    morceaux = []
    for v in VOIX_COMPARAISON:
        nom = v.split("-")[1]
        a, _ = fabriquer("Voix %s." % nom, os.path.join(dossier, "titre-%s.wav" % nom), v)
        b, d = fabriquer(passage, os.path.join(dossier, "extrait-%s.wav" % nom), v)
        morceaux += [a, b]
        print("   %-20s %5.1f s" % (v, d))
    liste = os.path.join(dossier, "liste.txt")
    with open(liste, "w") as f:
        for m in morceaux:
            f.write("file '%s'\n" % m)
    sortie = os.path.join(ICI, "COMPARER-LES-VOIX.mp4")
    silence = os.path.join(dossier, "tout.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                    "-i", liste, "-c", "copy", silence], check=True)
    # un son seul ne s'ouvre pas partout ; une vidéo, si — donc une carte fixe
    carte = os.path.join(dossier, "carte.png")
    import film
    film.c_regle("Quelle voix pour les films ?",
                 "Trois voix disent le même passage, dans l'ordre : Tom, Siwis, UPMC. "
                 "Dites-moi laquelle et je refais les deux films avec.",
                 "Choix de la voix").save(carte)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", carte,
                    "-i", silence, "-shortest", "-r", "25", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart",
                    sortie], check=True)
    print("→", os.path.basename(sortie))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--essai", action="store_true",
                   help="fabrique l'extrait de comparaison des trois voix")
    p.add_argument("--dire", help="prononce un texte et affiche sa version parlée")
    a = p.parse_args()
    if a.dire:
        print(prononcer(a.dire))
    elif a.essai:
        essai()
