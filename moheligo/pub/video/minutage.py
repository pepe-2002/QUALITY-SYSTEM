#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LE MINUTAGE DU FILM — calculé sur la voix, jamais l'inverse.

    python3 minutage.py          # affiche le minutage réel

🎬 LA LEÇON QUI A COÛTÉ UN MONTAGE
J'avais écrit le texte avec des créneaux fixes (« phrase 2 : de 6,4 s à 12,6 s »)
et j'attendais de la voix qu'elle rentre dedans. Elle n'est pas rentrée : trois
phrases débordaient, dont une de 3,6 s. On peut serrer les silences, on ne peut
pas faire parler quelqu'un plus vite sans que ça s'entende.

➡️ **La voix mène, l'image suit.** On mesure chaque phrase telle qu'elle sort,
on ajoute une respiration derrière, et c'est ÇA le minutage. Les plans et les
bandeaux se calent dessus. Aucune seconde n'est écrite à la main dans ce film.

📌 LES RESPIRATIONS NE SONT PAS TOUTES ÉGALES
Une pause n'est pas un vide, c'est de la ponctuation. Après « Mohéli. » il faut
1,5 s — le nom doit rester seul en l'air. Entre deux annonces de service, 0,8 s
suffit, sinon le film traîne. Elles sont donc écrites une par une.
"""
import importlib.util, json, os, subprocess

ICI = os.path.dirname(os.path.abspath(__file__))
PHRASES_DIR = os.path.join(ICI, "voix", "phrases")

# ⚠️ LES .wav DE SA VOIX NE SONT PAS DANS GIT — le dépôt est PUBLIC, et
# `voix/reference-patron.wav` est exactement ce qu'il faut à n'importe qui pour
# cloner sa voix. On n'offre pas ça. Mais le montage doit rester refabricable
# dans une session neuve : on garde donc **les durées mesurées**, et rien
# d'autre. Quelques nombres suffisent à retrouver le film à la milliseconde.
MESURES = os.path.join(ICI, "voix", "durees.json")

# la respiration APRÈS chaque phrase (la dernière n'en a pas : c'est la queue)
# ⚠️ RACCOURCIES le 26/08 au soir. Le patron : « parfois tu n'entends rien ».
# Avec des phrases lâchées à toute vitesse, les blancs prenaient toute la place :
# entre 0 et 5,4 s il n'y avait que 0,8 s de voix. Maintenant que le débit est
# tenu, les phrases occupent le temps et les respirations peuvent être courtes.
RESPIRATION = [1.20, 0.85, 0.85, 0.75, 0.85, 0.70, 0.95, 0.00]
DEBUT = 1.60        # avant le premier mot : l'image s'installe, sans traîner
QUEUE = 2.80        # après le dernier mot : la carte finale respire


def _texte():
    spec = importlib.util.spec_from_file_location(
        "tvo", os.path.join(ICI, "texte-voix-off.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return [(lignes, vu) for a, b, lignes, vu in m.TEXTE]


TEXTE = _texte()


def duree_fichier(chemin):
    s = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", chemin],
                       capture_output=True, text=True).stdout.strip()
    return float(s)


def fichier(i):
    """La phrase telle que `cloner.py` la laisse : déjà serrée et mise au bon
    volume. `None` si elle n'est pas là — la voix n'est pas dans le dépôt, on
    retombera sur `durees.json`."""
    c = os.path.join(PHRASES_DIR, "%02d.wav" % i)
    return c if os.path.exists(c) else None


def durees():
    """Les durées réelles des phrases — mesurées si les .wav sont là, relues
    dans `durees.json` sinon. Et on réécrit le cache dès qu'on mesure."""
    fichiers = [fichier(i) for i in range(len(TEXTE))]
    if all(fichiers):
        d = [duree_fichier(f) for f in fichiers]
        cache = {"phrases": [round(x, 4) for x in d],
                 "note": "durées de la voix clonée, phrases serrées. "
                         "Les .wav restent hors de Git : dépôt public."}
        os.makedirs(os.path.dirname(MESURES), exist_ok=True)
        if not os.path.exists(MESURES) or \
                json.load(open(MESURES))["phrases"] != cache["phrases"]:
            json.dump(cache, open(MESURES, "w"), ensure_ascii=False, indent=2)
        return d, fichiers
    if not os.path.exists(MESURES):
        raise SystemExit(
            "❌ ni les phrases (voix/phrases/NN-serre.wav) ni leurs mesures "
            "(voix/durees.json). Relancer `python3 cloner.py`.")
    return json.load(open(MESURES))["phrases"], fichiers


def calculer():
    """→ [(début, fin, fichier, lignes, ce qu'on voit)], durée totale du film."""
    mesures, fichiers = durees()
    creneaux, t = [], DEBUT
    for i, (lignes, vu) in enumerate(TEXTE):
        creneaux.append((t, t + mesures[i], fichiers[i], lignes, vu))
        t += mesures[i] + RESPIRATION[i]
    return creneaux, round(creneaux[-1][1] + QUEUE, 2)


# ─────────────────────────────────────────────────────────────────────────────
# CE QU'ON VOIT PENDANT CHAQUE PHRASE
# Une phrase = un bloc d'image, qui va du début de la phrase au début de la
# suivante (la respiration reste sur l'image en cours : couper dans le silence
# qui suit une phrase donne l'impression que l'image a été coupée trop tôt).
# Plusieurs photos dans un bloc se partagent le bloc à parts égales.
# ⚠️ La dernière phrase n'a pas de photo : c'est la carte de marque.
PHOTOS = [
    ["pub/photos-cc/ile-aerienne.jpg"],
    ["pub/photos/plage-vedettes.jpg", "pub/photos/horizon.jpg",
     "pub/photos-cc/moheli-beach.jpg"],
    ["pub/photos-cc/plage-pirogues.jpg"],
    ["pub/photos-cc/tortues.jpg"],
    ["pub/photos/vedette-mer.jpg", "pub/photos-cc/nioumachoua-ilot-fatima.jpg"],
    ["pub/photos-cc/dauphin.jpg"],
    ["pub/photos/ilot.jpg"],
    [],
]

# recadrages : la voiture rouge en bas de plage-vedettes n'a rien à faire là
RECADRAGE = {"pub/photos/plage-vedettes.jpg": (0.0, 0.0, 1.0, 0.78)}

# LE BANDEAU DE SERVICE, accroché à LA PHRASE qui le dit — plus à une seconde.
# Avant, ils étaient posés « dans ses silences » parce que j'ignorais ce qu'il
# disait. Ici c'est moi qui écris le texte : le bandeau montre le mot au moment
# exact où il est prononcé, et disparaît avec la phrase.
BANDEAUX = {
    2: ("RÉSERVE", "DEPUIS TON TÉLÉPHONE"),
    3: ("PAIE", "PAR MVOLA"),
    4: ("TON BILLET", "AVEC SON CODE QR"),
    5: ("CHAQUE SOIR", "LA MER DE DEMAIN"),
}
RETARD_BANDEAU = 0.35      # il arrive juste après l'attaque de la phrase
REPOS_BANDEAU = 0.15       # il repart avant la phrase suivante, jamais deux à la fois


def plans():
    """→ [(chemin photo, fin du plan, recadrage)] + la seconde où la carte arrive."""
    creneaux, duree = calculer()
    debuts = [c[0] for c in creneaux]
    sortie = []
    for i, photos in enumerate(PHOTOS):
        if not photos:
            continue
        a = debuts[i]
        b = debuts[i + 1] if i + 1 < len(debuts) else duree
        pas = (b - a) / len(photos)
        for j, ph in enumerate(photos):
            sortie.append((ph, round(a + pas * (j + 1), 3), RECADRAGE.get(ph)))
    carte = debuts[next(i for i, p in enumerate(PHOTOS) if not p)]
    return sortie, carte, duree


def bandeaux():
    """→ [(début, fin, petit, grand)] calés sur la parole.

    Le bandeau tient tout le bloc d'image de sa phrase, pas seulement la durée
    des mots : « Tu paies par MVola » dure 1,7 s, et un bandeau qui s'ouvre puis
    se referme en 1,7 s ne se lit pas — il clignote."""
    creneaux, duree = calculer()
    debuts = [c[0] for c in creneaux] + [duree]
    return [(round(creneaux[i][0] + RETARD_BANDEAU, 3),
             round(debuts[i + 1] - REPOS_BANDEAU, 3), pt, gr)
            for i, (pt, gr) in sorted(BANDEAUX.items())]


if __name__ == "__main__":
    creneaux, duree = calculer()
    print("MINUTAGE RÉEL — mesuré sur la voix\n")
    for i, (a, b, f, lignes, vu) in enumerate(creneaux):
        print("  %d  %5.2f → %5.2f  (%4.2f s)  %s"
              % (i, a, b, b - a, " ".join(lignes)))
        print("      %s%s" % (" " * 26, "à l'image : " + vu))
    print("\n  film : %.2f s" % duree)
    print("\nPLANS")
    ps, carte, _ = plans()
    for ph, fin, z in ps:
        print("  jusqu'à %5.2f  %s%s" % (fin, os.path.basename(ph),
                                         "   (recadré)" if z else ""))
    print("  carte de marque à %5.2f s" % carte)
    print("\nBANDEAUX")
    for a, b, pt, gr in bandeaux():
        print("  %5.2f → %5.2f  %s / %s" % (a, b, pt, gr))
