#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LA MUSIQUE MoheliGo — composée ici, à partir de rien.

    python3 musique.py --duree 42 --sortie musique/nappe-mer.wav

🚨 POURQUOI ON NE PREND PAS UNE MUSIQUE TOUTE FAITE
Facebook et Instagram reconnaissent les musiques du commerce et **coupent le son
de la publication**, parfois la retirent. Une page qui poste une vidéo muette
sans le savoir perd tout son travail. Une musique qu'on écrit nous-mêmes ne peut
être réclamée par personne — et elle devient, elle aussi, un code de la marque.

📌 CE QUE FAIT CETTE NAPPE, ET POURQUOI ELLE EST FAITE COMME ÇA
Elle doit passer SOUS une voix, pas à côté. Donc :
  · **aucune percussion** — un rythme oblige l'image à le suivre ;
  · **aucune mélodie** — une mélodie discute avec la voix, une nappe la porte ;
  · **un creux dans les médiums** (250 Hz → 4 kHz atténués) : c'est exactement
    la bande où vit la parole. On lui laisse la place au lieu de monter le
    volume de la voix ;
  · **une marche d'accords lente**, quatre accords, qui tourne. Le retour du
    même cycle fait le même travail que la vague dorée à l'image : on reconnaît
    sans savoir qu'on reconnaît.

L'enchaînement est en RÉ MAJEUR : Ré − Si mineur − Sol − La. Chaud, ouvert, il
ne tire ni vers le triste ni vers le triomphal. C'est une mer calme, pas une
victoire.
"""
import argparse, os
import numpy as np

TE = 48000                      # taux d'échantillonnage

# Ré, Si mineur, Sol, La — en fréquences, sur deux octaves
ACCORDS = [
    [146.83, 220.00, 293.66, 369.99],    # Ré  majeur  (ré la ré fa#)
    [123.47, 246.94, 293.66, 349.23],    # Si  mineur  (si si ré fa)
    [98.00,  196.00, 293.66, 392.00],    # Sol majeur  (sol sol ré sol)
    [110.00, 220.00, 277.18, 329.63],    # La  majeur  (la la do# mi)
]


def voix_sinus(freq, n, detune=0.0):
    """Une note. Trois partiels seulement : au-delà, ça devient un instrument
    qui se remarque, et une nappe ne doit pas se remarquer."""
    t = np.arange(n) / TE
    f = freq * (1 + detune)
    s = (np.sin(2 * np.pi * f * t)
         + 0.28 * np.sin(2 * np.pi * 2 * f * t + 0.7)
         + 0.10 * np.sin(2 * np.pi * 3 * f * t + 1.9))
    # un très léger flottement : sans lui, la nappe sonne électronique
    s *= 1 + 0.035 * np.sin(2 * np.pi * (0.17 + freq % 0.11) * t)
    return s


def enveloppe(n, montee, descente):
    """Attaque et chute longues : rien ne doit « démarrer »."""
    e = np.ones(n)
    m, d = int(montee * TE), int(descente * TE)
    e[:m] = np.sin(np.linspace(0, np.pi / 2, m)) ** 2
    e[-d:] = np.cos(np.linspace(0, np.pi / 2, d)) ** 2
    return e


def reverbe(x, duree=2.6, melange=0.34):
    """Une réverbération courte, faite d'un bruit qui décroît. Elle donne la
    salle — sans elle, la nappe est collée à l'oreille."""
    n = int(duree * TE)
    rng = np.random.default_rng(7)
    ri = rng.standard_normal(n) * np.exp(-np.linspace(0, 6.5, n))
    ri[:int(0.012 * TE)] = 0
    ri /= np.abs(ri).sum()
    humide = np.convolve(x, ri, mode="full")[:len(x)]
    return (1 - melange) * x + melange * humide


def passe_bas(x, coupure=2600):
    """Un seul pôle : doux, sans résonance. On veut retirer, pas colorer."""
    a = np.exp(-2 * np.pi * coupure / TE)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def creux_parole(x):
    """LE CREUX : on baisse 250 Hz → 4 kHz, la bande de la parole. C'est ce qui
    permet à la voix de passer devant sans monter le volume."""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / TE)
    gain = np.ones_like(f)
    bande = (f > 220) & (f < 4200)
    # un creux doux, −7 dB au centre, pour ne pas trouer la nappe
    centre = np.sqrt(220 * 4200)
    gain[bande] = 10 ** (-7 / 20 + (np.abs(np.log(f[bande] / centre)) / 3.0) * 0.35)
    return np.fft.irfft(X * np.minimum(gain, 1.0), len(x))


def composer(duree):
    par_accord = duree / 4 * 1.0
    cycles = max(1, int(np.ceil(duree / (par_accord * 4))))
    n_acc = int(par_accord * TE)
    piste = np.zeros(int(duree * TE) + n_acc)
    pos = 0
    for c in range(cycles * 4):
        notes = ACCORDS[c % 4]
        bloc = np.zeros(n_acc)
        for j, f in enumerate(notes):
            for det in (-0.0016, 0.0016):        # deux oscillateurs = de la largeur
                bloc += voix_sinus(f, n_acc, det) * (0.85 ** j)
        bloc *= enveloppe(n_acc, par_accord * 0.42, par_accord * 0.46)
        fin = min(len(piste), pos + n_acc)
        piste[pos:fin] += bloc[:fin - pos]
        pos += int(n_acc * 0.78)                 # les accords se chevauchent
    piste = piste[:int(duree * TE)]
    piste /= np.max(np.abs(piste)) + 1e-9
    piste = passe_bas(piste, 2600)
    piste = creux_parole(piste)
    piste = reverbe(piste)
    piste /= np.max(np.abs(piste)) + 1e-9
    # entrée et sortie en fondu : une nappe ne commence ni ne finit jamais net
    e = np.ones(len(piste))
    f_in, f_out = int(2.2 * TE), int(3.2 * TE)
    e[:f_in] = np.linspace(0, 1, f_in) ** 1.6
    e[-f_out:] = np.linspace(1, 0, f_out) ** 1.4
    return (piste * e * 0.82).astype(np.float32)


def ecrire_wav(x, chemin):
    import wave, struct
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    d = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    with wave.open(chemin, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(TE)
        w.writeframes(d.tobytes())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--duree", type=float, default=42.0)
    ap.add_argument("--sortie", default="musique/nappe-mer.wav")
    a = ap.parse_args()
    ecrire_wav(composer(a.duree), a.sortie)
    print(f"→ {a.sortie}  {a.duree:.0f} s  (Ré · Si m · Sol · La)")
