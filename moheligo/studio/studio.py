#!/usr/bin/env python3
"""MoheliGo Studio IA — ligne de commande.

    python3 studio.py casting
        Fabrique les fiches de casting et la planche d'ensemble.

    python3 studio.py brief "Fais une pub de 30 secondes où deux amis discutent
        au port de Hoani. L'un montre MoheliGo sur son téléphone. Ils réservent
        leur traversée puis montent dans la vedette. Voix française, sous-titres."
        --nom demo-hoani
        Analyse la demande et écrit le scénario + le storyboard + les prompts.

    python3 studio.py produire demo-hoani [--formats tiktok,facebook,youtube]
        Synthétise les voix, cale la timeline, fabrique l'animatique et exporte.

    python3 studio.py generer demo-hoani --moteur fal
        Envoie les prompts au moteur vidéo externe (nécessite une clé d'API).

    python3 studio.py monter demo-hoani
        Remonte le film avec les rushes générés (projets/<nom>/rushes/plan-XX.mp4).

    python3 studio.py lister avatars|decors|cameras|actions|expressions|moteurs
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from moteur import bible as mod_bible
from moteur import casting as mod_casting
from moteur import langage, montage, prompts, scenario as mod_scenario, voix

RACINE = os.path.dirname(os.path.abspath(__file__))
PROJETS = os.path.join(RACINE, "projets")


def _dossier_projet(nom):
    return os.path.join(PROJETS, nom)


def cmd_casting(args):
    b = mod_bible.Bible()
    produits = mod_casting.produire(b, os.path.join(RACINE, "casting"))
    print("%d fiches de casting écrites dans studio/casting/" % (len(produits) - 1))
    print("Planche d'ensemble : %s" % os.path.relpath(produits[-1], RACINE))


def cmd_brief(args):
    b = mod_bible.Bible()
    intentions = langage.analyser(args.texte)
    if args.duree:
        intentions["duree"] = args.duree
    if args.langue:
        intentions["langue"] = args.langue
    if args.formats:
        intentions["formats"] = args.formats.split(",")

    nom = args.nom or "projet"
    dossier = _dossier_projet(nom)
    sc = mod_scenario.construire(b, intentions, nom, titre=args.titre)
    avertissements = mod_bible.controler(b, sc)
    mod_scenario.ecrire(sc, dossier)
    prompts.generer(b, sc, dossier)
    _storyboard(b, sc, dossier)

    print("Projet « %s » — %s" % (nom, sc["titre"]))
    print("  décors  : %s" % ", ".join(
        b.decors[d]["nom"] for d in dict.fromkeys(p["decor"] for p in sc["plans"] if p["decor"])))
    print("  casting : %s" % ", ".join(c["nom"] for c in sc["casting"]))
    print("  %d plans, %.1f s visés, langue %s, formats %s"
          % (len(sc["plans"]), sum(p["duree"] for p in sc["plans"]), sc["langue"],
             ", ".join(sc["formats"])))
    for a in avertissements:
        print("  ⚠ %s" % a)
    print("  écrit : scenario.json, storyboard.md, prompts.md, prompts.json")
    print("  suite : python3 studio.py produire %s" % nom)


def _storyboard(b, sc, dossier):
    L = ["# Storyboard — %s" % sc["titre"], "",
         "**Brief :** %s" % sc["brief"], "",
         "**Durée visée :** %s s · **Langue :** %s · **Formats :** %s · **Objectif :** %s"
         % (sc["duree_cible"], sc["langue"], ", ".join(sc["formats"]), sc["objectif"]), "",
         "## Casting", ""]
    for c in sc["casting"]:
        av = b.avatars[c["avatar"]]
        L.append("- **%s** (`%s`, seed %s) — %s · tenue *%s* · coiffure *%s*"
                 % (av["nom"], av["id"], av["seed"], av["role"], c["tenue"], c["coiffure"]))
    L += ["", "## Plans", "",
          "| # | Rôle | Durée | Décor | Caméra | À l'image | Réplique |",
          "|---|---|---|---|---|---|---|"]
    for p in sc["plans"]:
        acteurs = " / ".join(
            "%s (%s, %s)" % (b.avatars[a["avatar"]]["nom"].split()[0],
                             b.actions.get(a["action"], {}).get("nom", a["action"]),
                             b.expressions.get(a["expression"], {}).get("nom", a["expression"]))
            for a in p["acteurs"]) or "—"
        replique = ""
        if p.get("dialogue"):
            replique = "**%s** : « %s »" % (
                b.avatars[p["dialogue"]["avatar"]]["nom"].split()[0], p["dialogue"]["texte"])
        elif p.get("voix_off"):
            replique = "*voix off* : « %s »" % p["voix_off"]
        L.append("| %s | %s | %.1f s | %s | %s | %s | %s |" % (
            p["n"], p["role"], p["duree"],
            b.decors[p["decor"]]["nom"] if p["decor"] else "carton",
            b.cameras.get(p["camera"], {}).get("nom", p["camera"]), acteurs, replique))
    L += ["", "## Carton final", "",
          "%s — %s" % (sc["carton_final"]["signature"], sc["carton_final"]["site"]),
          "", "_%s_" % sc["carton_final"]["mention_ia"], ""]
    with open(os.path.join(dossier, "storyboard.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))


def _produire(nom, formats, mode):
    b = mod_bible.Bible()
    dossier = _dossier_projet(nom)
    sc = mod_scenario.lire(dossier)
    mod_bible.controler(b, sc)

    print("Voix (%s)…" % sc["langue"])
    pistes = voix.produire(b, sc, dossier)
    sc, pistes = voix.caler(sc, pistes)
    mod_scenario.ecrire(sc, dossier)
    with open(os.path.join(dossier, "pistes.json"), "w", encoding="utf-8") as f:
        json.dump(pistes, f, ensure_ascii=False, indent=2)
    chemin_srt = voix.srt(pistes, os.path.join(dossier, "%s.srt" % nom))
    print("  %d répliques, %.1f s de film, sous-titres : %s"
          % (len(pistes), sc["duree_reelle"], os.path.basename(chemin_srt)))
    if sc["duree_reelle"] > sc["duree_cible"] * 1.1:
        print("  ⚠ %.1f s au lieu des %s s visées : les répliques ne tiennent pas dans "
              "la durée. Raccourcir les textes du scenario.json (le studio ne coupe "
              "jamais une phrase au milieu), ou viser une durée plus longue."
              % (sc["duree_reelle"], sc["duree_cible"]))

    formats = formats or sc["formats"]
    for fid in formats:
        if fid not in b.formats:
            print("  format inconnu ignoré : %s" % fid)
            continue
        print("Rendu %s (%s)…" % (fid, mode))
        fichier = montage.rendre(b, sc, pistes, dossier, fid, mode=mode)
        leger = montage.alleger(fichier, 1280 if b.formats[fid]["w"] > b.formats[fid]["h"] else 720)
        print("  %s (%s) · diffusion : %s (%s)" % (
            os.path.basename(fichier), montage.poids(fichier),
            os.path.basename(leger), montage.poids(leger)))


def cmd_produire(args):
    _produire(args.nom, args.formats.split(",") if args.formats else None, "animatique")


def cmd_monter(args):
    dossier = os.path.join(_dossier_projet(args.nom), "rushes")
    if not os.path.isdir(dossier) or not os.listdir(dossier):
        print("Aucun rush dans %s — lancer d'abord « generer », ou y déposer les mp4 "
              "produits par le moteur vidéo (plan-01.mp4, plan-02.mp4, …)." % dossier)
        return 1
    _produire(args.nom, args.formats.split(",") if args.formats else None, "final")


def cmd_generer(args):
    from moteur import moteurs_video
    dossier = _dossier_projet(args.nom)
    with open(os.path.join(dossier, "prompts.json"), encoding="utf-8") as f:
        p = json.load(f)["plans"]
    fichiers = moteurs_video.generer_plans(
        p, os.path.join(dossier, "rushes"), moteur=args.moteur, type_sortie=args.type)
    print("%d fichiers reçus dans %s" % (len(fichiers), os.path.join(dossier, "rushes")))


def cmd_lister(args):
    b = mod_bible.Bible()
    quoi = args.quoi
    if quoi == "avatars":
        for a in b.avatars.values():
            marque = "  (mineur — usage encadré)" if a.get("mineur") else ""
            print("%-9s %-26s %-32s seed %s%s" % (a["id"], a["nom"], a["role"], a["seed"], marque))
    elif quoi == "decors":
        for d in b.decors.values():
            print("%-8s %-34s %-16s photo: %s" % (
                d["id"], d["nom"], d["ile"], "oui" if d.get("photo_ref") else "non"))
    elif quoi == "cameras":
        for c in b.cameras.values():
            print("%-11s %-26s %s" % (c["id"], c["nom"], c["usage"]))
    elif quoi == "actions":
        for a in b.actions.values():
            print("%-18s %s" % (a["id"], a["nom"]))
    elif quoi == "expressions":
        for e in b.expressions.values():
            print("%-12s %s" % (e["id"], e["nom"]))
    elif quoi == "moteurs":
        from moteur import moteurs_video
        print(moteurs_video.etat())
    else:
        print("inconnu : %s" % quoi)
        return 1


def main():
    p = argparse.ArgumentParser(description="MoheliGo Studio IA v1.0")
    sp = p.add_subparsers(dest="commande", required=True)

    c = sp.add_parser("casting", help="fabriquer les fiches de casting")
    c.set_defaults(f=cmd_casting)

    c = sp.add_parser("brief", help="analyser une demande en français")
    c.add_argument("texte")
    c.add_argument("--nom", help="nom du projet")
    c.add_argument("--titre")
    c.add_argument("--duree", type=int)
    c.add_argument("--langue")
    c.add_argument("--formats")
    c.set_defaults(f=cmd_brief)

    c = sp.add_parser("produire", help="voix + animatique + exports")
    c.add_argument("nom")
    c.add_argument("--formats")
    c.set_defaults(f=cmd_produire)

    c = sp.add_parser("generer", help="envoyer les prompts au moteur vidéo externe")
    c.add_argument("nom")
    c.add_argument("--moteur", default="fal")
    c.add_argument("--type", default="video", choices=["video", "image"])
    c.set_defaults(f=cmd_generer)

    c = sp.add_parser("monter", help="monter le film avec les rushes générés")
    c.add_argument("nom")
    c.add_argument("--formats")
    c.set_defaults(f=cmd_monter)

    c = sp.add_parser("lister", help="explorer la bibliothèque")
    c.add_argument("quoi", choices=["avatars", "decors", "cameras", "actions",
                                    "expressions", "moteurs"])
    c.set_defaults(f=cmd_lister)

    args = p.parse_args()
    try:
        return args.f(args) or 0
    except mod_bible.RefusDeProduction as e:
        print("\n%s\n" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
