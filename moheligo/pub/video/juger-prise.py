#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LE JUGE DE PRISE DE SON — « est-ce que mon enregistrement est bon ? »

    python3 juger-prise.py ma-voix.m4a

Le patron, 27/08/2026 : « donne un truc pour bien mettre ma voix. »

📌 POURQUOI UN PROGRAMME ET PAS SEULEMENT DES CONSEILS
Les conseils, il les applique une fois et il oublie. Et surtout : **il ne peut
pas savoir si sa prise est bonne en l'écoutant.** L'oreille s'habitue en trois
secondes à un écho ou à un souffle ; elle ne les entend plus. Un chiffre, lui,
ne s'habitue pas.
➡️ Il enregistre 15 secondes, il me les envoie, je réponds en une ligne :
« refais-la, tu es trop loin du micro » ou « c'est bon, envoie la suite ».
Ça évite de découvrir le problème après vingt minutes d'enregistrement.

🎯 CE QU'ON MESURE, ET POURQUOI CHAQUE SEUIL EST LÀ
  · **le niveau** — sa première prise était à −30,4 dB, soit 13 dB trop faible.
    Monter le volume après coup monte AUSSI le souffle : c'est un défaut qu'on
    ne rattrape jamais complètement.
  · **l'écart parole / silence** — c'est la vraie mesure de la propreté. Une
    voix à −18 dB sur un fond à −60 dB est propre ; la même voix sur un fond à
    −35 dB est dans une pièce bruyante, et aucun filtre n'y changera rien sans
    abîmer la voix.
  · **la saturation** — au-delà de 0 dB le son est écrêté, définitivement. Il
    n'y a rien à réparer : l'information n'a jamais été enregistrée.
  · **la traîne** — combien de temps le son met à s'éteindre quand il arrête de
    parler. C'est l'écho de la pièce, et **c'est le seul défaut vraiment
    irréparable**. D'où le conseil de la couverture.
  · **le plus long bloc de parole continue** — pour cloner sa voix il faut de la
    parole SANS coupure ; une prise hachée donne une voix qui flotte.

⚠️ À LANCER SUR LE FICHIER BRUT, PAS SUR UNE VERSION NETTOYÉE. Vérifié sur ses
deux fichiers : la prise brute annonce 6,1 s de parole continue, la même prise
nettoyée n'en annonce plus que 3,8 s — le débruiteur creuse les micro-silences
et le juge les compte comme des coupures. Sur un fichier déjà traité, le niveau
et l'écart sont ceux du traitement, pas ceux de la prise : ils ne disent plus
rien de ce qu'il faut corriger au micro.
"""
import argparse, os, subprocess, sys
import numpy as np

CIBLE = dict(niveau=(-24.0, -12.0), ecart=35.0, traine=0.35, continu=10.0)


def lire(chemin):
    """N'importe quel fichier (m4a, mp3, mp4, wav) → un tableau mono 48 kHz."""
    brut = subprocess.run(
        ["ffmpeg", "-hide_banner", "-v", "error", "-i", chemin, "-vn",
         "-ac", "1", "-ar", "48000", "-f", "f32le", "-"],
        capture_output=True)
    if brut.returncode or not brut.stdout:
        sys.exit("❌ impossible de lire %s\n%s" % (chemin, brut.stderr.decode()[:400]))
    return np.frombuffer(brut.stdout, dtype=np.float32), 48000


def enveloppe(x, te, fenetre=0.02):
    """Le niveau en dB, fenêtre par fenêtre. Tout se déduit de ça."""
    n = int(fenetre * te)
    trames = x[:len(x) // n * n].reshape(-1, n)
    return 20 * np.log10(np.sqrt((trames.astype(np.float64) ** 2).mean(1)) + 1e-12), n / te


def juger(chemin):
    x, te = lire(chemin)
    duree = len(x) / te
    env, pas = enveloppe(x, te)

    # le fond sonore = les 10 % de fenêtres les plus calmes ; la parole = les 20 %
    # les plus fortes. On ne prend pas le minimum ni le maximum : un claquement
    # ou un blanc parfait fausserait tout.
    calme = float(np.percentile(env, 10))
    fort = float(np.percentile(env, 80))
    ecart = fort - calme
    seuil = calme + max(8.0, ecart * 0.35)      # au-dessus = on parle
    parle = env > seuil

    crete = 20 * np.log10(np.max(np.abs(x)) + 1e-12)
    satures = int(np.sum(np.abs(x) > 0.999))

    # LA TRAÎNE : après chaque fin de phrase, combien de temps pour retomber de
    # 20 dB ? C'est l'écho de la pièce.
    traines = []
    for i in range(1, len(parle) - 1):
        if parle[i] and not parle[i + 1]:
            depart = env[i]
            for j in range(i + 1, min(i + int(1.2 / pas), len(env))):
                if env[j] <= depart - 20:
                    traines.append((j - i) * pas)
                    break
    traine = float(np.median(traines)) if traines else 0.0

    # le plus long bloc de parole d'affilée (une coupure = 0,25 s de silence)
    trou = int(0.25 / pas)
    blocs, debut, vide = [], None, 0
    for i, p in enumerate(parle):
        if p:
            if debut is None:
                debut = i
            vide = 0
        elif debut is not None:
            vide += 1
            if vide >= trou:
                blocs.append((i - vide - debut) * pas)
                debut = None
    if debut is not None:
        blocs.append((len(parle) - debut) * pas)
    continu = max(blocs) if blocs else 0.0

    return dict(duree=duree, niveau=fort, fond=calme, ecart=ecart, crete=crete,
                satures=satures, traine=traine, continu=continu,
                parle=float(parle.mean() * duree))


def verdict(m):
    """Une ligne par défaut, et le geste qui le corrige. Jamais un chiffre nu."""
    fautes = []
    bas, haut = CIBLE['niveau']
    if m['niveau'] < bas:
        fautes.append(("TU ES TROP LOIN, OU TU PARLES TROP DOUCEMENT",
                       "%.0f dB, il en faut %.0f. Rapproche-toi à 15–20 cm et "
                       "parle comme à quelqu'un assis en face."
                       % (m['niveau'], bas), True))
    elif m['niveau'] > haut:
        fautes.append(("TU ES TROP PRÈS",
                       "%.0f dB, c'est trop fort. Éloigne-toi un peu."
                       % m['niveau'], False))
    if m['satures'] > 20 or m['crete'] > -0.5:
        fautes.append(("LE SON EST ÉCRÊTÉ — irréparable",
                       "%d échantillons collés au plafond. Baisse le volume "
                       "d'entrée ou éloigne le téléphone, et REFAIS la prise : "
                       "ce qui est écrêté n'a jamais été enregistré."
                       % m['satures'], True))
    if m['ecart'] < CIBLE['ecart']:
        fautes.append(("LA PIÈCE EST BRUYANTE",
                       "seulement %.0f dB entre ta voix et le fond (il en faut "
                       "%.0f). Coupe le ventilateur, ferme la fenêtre, mets le "
                       "téléphone en mode avion."
                       % (m['ecart'], CIBLE['ecart']), True))
    if m['traine'] > CIBLE['traine']:
        fautes.append(("ÇA RÉSONNE — le défaut qu'on ne répare pas",
                       "le son met %.2f s à s'éteindre (max %.2f). La couverture "
                       "sur la tête et le téléphone, ou parle dans l'armoire "
                       "au milieu des habits."
                       % (m['traine'], CIBLE['traine']), True))
    if m['continu'] < CIBLE['continu']:
        fautes.append(("PAS ASSEZ DE PAROLE D'AFFILÉE",
                       "%.1f s au mieux, il en faut %.0f pour cloner. Ne coupe "
                       "pas entre les phrases, enchaîne."
                       % (m['continu'], CIBLE['continu']), False))
    return fautes


def afficher(chemin, m, fautes):
    print("\n%s  —  %.1f s dont %.1f s de parole" % (os.path.basename(chemin),
                                                     m['duree'], m['parle']))
    print("─" * 66)
    print("  niveau de la voix       %7.1f dB      (visé %.0f à %.0f)"
          % (m['niveau'], *CIBLE['niveau']))
    print("  fond sonore             %7.1f dB" % m['fond'])
    print("  écart voix / fond       %7.1f dB      (au moins %.0f)"
          % (m['ecart'], CIBLE['ecart']))
    print("  crête                   %7.1f dB      (sous 0, sinon écrêté)" % m['crete'])
    print("  traîne de la pièce      %7.2f s       (sous %.2f)"
          % (m['traine'], CIBLE['traine']))
    print("  plus long bloc continu  %7.1f s       (au moins %.0f pour cloner)"
          % (m['continu'], CIBLE['continu']))
    print("─" * 66)
    if not fautes:
        print("✅ PRISE BONNE. Envoie la suite dans les mêmes conditions —\n"
              "   même pièce, même distance, même volume.")
        return 0
    graves = [f for f in fautes if f[2]]
    for titre, quoi, grave in fautes:
        print("%s %s\n   → %s" % ("🔴" if grave else "🟠", titre, quoi))
    if graves:
        print("\n❌ À REFAIRE. Corrige le(s) point(s) rouge(s) et renvoie 15 s d'essai.")
    else:
        print("\n🟠 UTILISABLE, mais on peut faire mieux en corrigeant ci-dessus.")
    return 1 if graves else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Dit si un enregistrement de voix est bon, et ce qu'il faut corriger.")
    ap.add_argument("fichier", nargs="+")
    a = ap.parse_args()
    pire = 0
    for f in a.fichier:
        m = juger(f)
        pire = max(pire, afficher(f, m, verdict(m)))
    sys.exit(pire)
