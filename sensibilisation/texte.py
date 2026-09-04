#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LES TEXTES QUI ACCOMPAGNENT LES FILMS — fabriqués depuis le scénario.

    python3 texte.py        → réécrit voix-off-agence.md, voix-off-escale.md
                              et fiche-agence.md, fiche-escale.md

📌 POURQUOI C'EST UN PROGRAMME ET NON DEUX FICHIERS ÉCRITS À LA MAIN
Le jour où une phrase du film change, la voix off et la fiche papier doivent
changer avec elle. Écrits à la main, ils divergent en trois semaines et on se
retrouve avec un film qui dit une chose et une fiche qui en dit une autre —
c'est exactement le genre d'écart qu'un audit relève. Ici, il n'y a qu'une
source : `scenarios.py`. Ces fichiers en sont la sortie, jamais l'inverse.

CE QUE ÇA PRODUIT
  · `voix-off-*.md` — le texte à lire, minuté scène par scène, si le patron
    veut un jour poser sa voix sur le film. Le film n'aura pas à être refait :
    les durées sont déjà celles du montage.
  · `fiche-*.md` — la même chose en une page, à imprimer et à afficher au
    comptoir. Un film se regarde une fois ; une fiche punaisée se relit.
"""
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import scenarios  # noqa: E402


def duree_scene(sc):
    if sc["type"] in ("liste", "cloture"):
        n = len(sc["points"])
        return sc["par_point"] * n + sc.get("tenue", 1.6 if sc["type"] == "liste" else 2.4)
    if sc["type"] == "duo":
        return sc["par_point"] * len(sc["paires"]) + sc.get("tenue", 1.6)
    return sc["duree"]


def minutage(t):
    return "%d:%02d" % (int(t // 60), int(t % 60))


def voix_off(film):
    """Le texte à dire, avec le repère de temps de chaque scène.

    Il ne redit pas ce qui est écrit à l'écran — une voix qui lit les
    sous-titres endort. Elle enchaîne, elle nomme, elle laisse lire."""
    lignes = ["# Voix off — %s" % film["titre"], "",
              "Texte à lire si l'on veut poser une voix sur le film. Les repères de",
              "temps sont ceux du montage : à chaque scène, la voix a exactement la",
              "durée indiquée, silences compris.", "",
              "**Ton** : posé, sans emphase. C'est un collègue qui parle à des collègues,",
              "pas une publicité. On ne lit pas le texte affiché — on le prolonge.", "",
              "| Temps | Durée | À dire |", "|---|---|---|"]
    t = 0.0
    for sc in film["scenes"]:
        d = duree_scene(sc)
        dit = ""
        if sc["type"] == "ouverture":
            dit = "Royal Air, département qualité. %s." % sc["titre"]
        elif sc["type"] == "situation":
            dit = "%s … %s" % (sc["texte"], sc["question"])
        elif sc["type"] == "chapitre":
            dit = "%s." % sc["titre"]
        elif sc["type"] == "regle":
            dit = "%s %s" % (sc["texte"], sc.get("appui", ""))
        elif sc["type"] == "liste":
            dit = "%s *(laisser lire les %d points)*" % (sc["titre"], len(sc["points"]))
        elif sc["type"] == "duo":
            dit = "%s *(laisser lire)*" % sc["titre"]
        elif sc["type"] == "cloture":
            dit = "Cinq réflexes à garder. *(laisser lire)*"
        elif sc["type"] == "fin":
            dit = ("Ce film est interne. Il reste dans le groupe du personnel. "
                   "Merci de votre attention.")
        lignes.append("| %s | %.1f s | %s |" % (minutage(t), d, dit.strip().replace("\n", " ")))
        t += d
    lignes += ["", "**Durée totale : %s.**" % minutage(t), "",
               "Une fois enregistrée, la voix se nettoie et se mixe avec la nappe ;",
               "la nappe est déjà creusée dans la bande de la parole (`musique.py`),",
               "il n'y a donc rien à baisser au montage."]
    return "\n".join(lignes) + "\n"


def fiche(film):
    """La même chose en une page — ce qui se punaise au comptoir."""
    lignes = ["# %s — la fiche" % film["titre"], "",
              "Tout ce que dit le film, en une page. À imprimer et à afficher.",
              "Le film se regarde une fois ; ceci se relit.", ""]
    for sc in film["scenes"]:
        if sc["type"] == "chapitre":
            lignes += ["", "## %s. %s" % (sc["numero"], sc["titre"]), ""]
        elif sc["type"] == "situation":
            lignes += ["", "## %s" % sc["chapitre"], "",
                       "> %s **%s**" % (sc["texte"], sc["question"]), ""]
        elif sc["type"] == "liste":
            lignes.append("**%s**" % sc["titre"])
            lignes.append("")
            marque = "🚫" if sc.get("marqueur") == "interdit" else "•"
            for p in sc["points"]:
                lignes.append("%s %s" % (marque, p))
            lignes.append("")
        elif sc["type"] == "regle":
            lignes += ["> **%s** %s" % (sc["texte"], sc.get("appui", "")), ""]
        elif sc["type"] == "duo":
            lignes += ["**%s**" % sc["titre"], "",
                       "| Ne dites pas | Dites |", "|---|---|"]
            for mauvais, bon in sc["paires"]:
                lignes.append("| %s | %s |" % (mauvais, bon))
            lignes.append("")
        elif sc["type"] == "cloture":
            lignes += ["", "## %s" % sc["titre"], ""]
            lignes += ["%d. %s" % (i + 1, p) for i, p in enumerate(sc["points"])]
            lignes += ["", "*%s*" % sc.get("reference", ""), ""]
    lignes += ["---", "",
               "Document interne — Département Qualité Royal Air.",
               "Références : GOM · GRD-PROC-001 · QUA-PROC-002 · Manuel Qualité (ANACM).",
               "", "*Généré par `texte.py` depuis `scenarios.py` — ne pas corriger ici.*"]
    return "\n".join(lignes) + "\n"


if __name__ == "__main__":
    for nom, film in (("agence", scenarios.AGENCE), ("escale", scenarios.ESCALE)):
        for prefixe, fabrique in (("voix-off", voix_off), ("fiche", fiche)):
            chemin = os.path.join(ICI, "%s-%s.md" % (prefixe, nom))
            with open(chemin, "w") as f:
                f.write(fabrique(film))
            print("→", os.path.basename(chemin))
