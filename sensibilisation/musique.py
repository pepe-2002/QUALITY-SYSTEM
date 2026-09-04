#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LA NAPPE DES FILMS ROYAL AIR — composée ici, à partir de rien.

    python3 musique.py --duree 240 --sortie nappe.wav

🚨 POURQUOI ON N'UTILISE PAS UNE MUSIQUE DU COMMERCE
Une musique trouvée sur internet appartient à quelqu'un. Un film interne qui
circule dans un groupe WhatsApp finit toujours par être réexpédié ailleurs, et
le jour où il l'est, la compagnie se retrouve à diffuser l'œuvre d'un tiers.
Une nappe écrite ici ne peut être réclamée par personne.

📌 CE QU'ELLE DOIT FAIRE, ET DONC COMMENT ELLE EST FAITE
Elle accompagne du texte à lire, pas une histoire à suivre. Donc :
  · aucune percussion — un rythme presse la lecture, et on lit tous à des
    vitesses différentes ;
  · aucune mélodie — une mélodie se retient et couvre ce qui est écrit ;
  · un creux entre 250 Hz et 4 kHz, la bande de la parole, gardée libre au cas
    où une voix off serait posée plus tard sans avoir à refaire la nappe ;
  · quatre accords qui tournent lentement, toujours les mêmes : on reconnaît un
    film Royal Air avant d'avoir lu le premier mot.

L'enchaînement est en FA MAJEUR : Fa − Do − Ré mineur − Si♭. Calme et posé, il
ne tire ni vers le triste ni vers le triomphal — c'est un film de travail, pas
une publicité.
"""
import argparse
import wave

import numpy as np

TE = 48000                     # taux d'échantillonnage
CYCLE = 24.0                   # secondes pour les quatre accords

ACCORDS = [
    [87.31, 174.61, 261.63, 349.23],    # Fa  majeur  (fa fa do fa)
    [65.41, 196.00, 261.63, 329.63],    # Do  majeur  (do sol do mi)
    [73.42, 174.61, 293.66, 349.23],    # Ré  mineur  (ré fa ré fa)
    [58.27, 174.61, 233.08, 349.23],    # Si♭ majeur  (si♭ fa si♭ fa)
]


def note(freq, n, desaccord=0.0):
    """Une note : trois partiels, pas plus. Au-delà, on entend un instrument,
    et un instrument attire l'oreille au lieu de la laisser lire."""
    t = np.arange(n) / TE
    f = freq * (1 + desaccord)
    return (np.sin(2 * np.pi * f * t)
            + 0.26 * np.sin(2 * np.pi * 2 * f * t + 0.7)
            + 0.09 * np.sin(2 * np.pi * 3 * f * t + 1.9))


def creux_de_parole(x):
    """Atténue la bande où vit la voix : −6 dB entre 250 Hz et 4 kHz, avec des
    bords adoucis pour qu'on n'entende pas le filtre lui-même. Fait dans le
    domaine des fréquences — c'est exact, et instantané même sur cinq minutes."""
    spectre = np.fft.rfft(x)
    f = np.fft.rfftfreq(x.size, 1.0 / TE)
    gain = np.ones_like(f)
    creux = (f > 180) & (f < 5200)
    # une cloche douce en échelle logarithmique, centrée sur 1 kHz
    lf = np.log10(np.clip(f, 1.0, None))
    gain[creux] = 1 - 0.5 * np.exp(-((lf[creux] - 3.0) ** 2) / (2 * 0.42 ** 2))
    return np.fft.irfft(spectre * gain, n=x.size)


def composer(duree, sortie):
    n_total = int(duree * TE)
    n_accord = int(CYCLE / 4 * TE)
    piste = np.zeros(n_total + n_accord)

    i = 0
    k = 0
    while i < n_total:
        freqs = ACCORDS[k % 4]
        n = n_accord
        env = np.ones(n)
        m = int(n * 0.45)                      # fondus longs : les accords se
        env[:m] = np.linspace(0, 1, m) ** 1.6  # recouvrent, on n'entend jamais
        env[-m:] = np.linspace(1, 0, m) ** 1.6 # une attaque
        acc = np.zeros(n)
        for j, f in enumerate(freqs):
            acc += note(f, n, desaccord=0.0018 * (j - 1.5)) * (0.9 - 0.12 * j)
        piste[i:i + n] += acc * env
        i += int(n * 0.62)                     # recouvrement de 38 %
        k += 1

    x = piste[:n_total]
    x = creux_de_parole(x)

    # respiration très lente : la nappe monte et redescend de 15 % en 40 s
    t = np.arange(n_total) / TE
    x *= 1 + 0.15 * np.sin(2 * np.pi * t / 40.0)

    x /= np.max(np.abs(x)) + 1e-9
    x *= 0.20                                   # discret : c'est un fond
    fondu = int(2.5 * TE)
    x[:fondu] *= np.linspace(0, 1, fondu)
    x[-fondu:] *= np.linspace(1, 0, fondu)

    stereo = np.stack([x, np.roll(x, 300)], axis=1)   # légère largeur
    data = (stereo * 32767).astype(np.int16)
    with wave.open(sortie, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(TE)
        w.writeframes(data.tobytes())
    return sortie


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--duree", type=float, required=True)
    p.add_argument("--sortie", required=True)
    a = p.parse_args()
    print(composer(a.duree, a.sortie))
