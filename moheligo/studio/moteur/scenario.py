"""Construction du scénario : intentions → plans, dialogues, caméras, expressions.

Le scénario est le FORMAT PIVOT du studio (fichier scenario.json d'un projet).
Tout le reste — prompts moteur, voix, sous-titres, montage, exports — en découle.
"""

import json
import os
import unicodedata


def _cle(t):
    return "".join(
        c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn"
    )


# --- répliques types, par situation ----------------------------------------
# {prenom} = celui qui parle, {autre} = son interlocuteur.

REPLIQUES = {
    "accroche_question": [
        "Tu descends à Mohéli ce week-end ?",
        "Tu pars quand à Mohéli, toi ?",
        "Et pour Mohéli, tu fais comment ?",
    ],
    "objection": [
        "J'ai pas envie d'attendre pour rien.",
        "Et si la vedette est déjà pleine ?",
        "La dernière fois j'ai attendu toute la matinée.",
        "On ne sait jamais à quelle heure ça part.",
    ],
    "solution": [
        "Regarde. Tout est là : MoheliGo.",
        "Tiens, regarde. Je réserve depuis mon téléphone.",
        "Attends, je te montre.",
    ],
    "demonstration": [
        "Ton départ, ton horaire. C'est réservé.",
        "Les horaires du jour, la météo de la mer, et ton billet.",
        "Deux minutes, et t'as ta place.",
    ],
    "confirmation": [
        "Voilà. Billet réservé.",
        "C'est fait. J'ai mon billet sur le téléphone.",
        "Et voilà, c'est réservé.",
    ],
    "adhesion": [
        "Sérieux ? Envoie-moi le lien.",
        "Ah quand même. Je fais pareil alors.",
        "Bon. Tu me montres comment on fait ?",
    ],
    "embarquement": [
        "Elle part dans dix minutes.",
        "Allez, on monte.",
        "C'est nous. On embarque.",
    ],
    "securite": [
        "Gilets pour tout le monde. On part quand la mer le permet.",
        "On regarde la météo avant chaque départ.",
    ],
    "arrivee": [
        "Mohéli. On y est.",
        "Et voilà Mohéli.",
    ],
}

VOIX_OFF = {
    "notoriete": [
        "Entre la Grande Comore et Mohéli, il y a la mer.",
        "Et maintenant, il y a MoheliGo.",
    ],
    "conversion": [
        "Vos horaires, votre billet, votre place.",
        "Sur votre téléphone.",
    ],
    "confiance": [
        "La météo de la mer avant chaque départ.",
        "Votre billet, votre place, votre horaire.",
    ],
    "tourisme": [
        "Mohéli. Les tortues, les baleines, le lagon.",
        "La traversée se réserve en deux minutes.",
    ],
    "fret": [
        "Vos marchandises partent à l'heure.",
        "Les départs du jour, sur votre téléphone.",
    ],
}


def _tour(liste, i):
    return liste[i % len(liste)]


def construire(bible, intentions, nom_projet, titre=None):
    """intentions (langage.analyser) → scénario dict."""
    duree = intentions["duree"]
    langue = intentions["langue"]
    casting_ids = [i for i in intentions["casting"] if i in bible.avatars]
    decors_ids = [d for d in intentions["decors"] if d in bible.decors]
    heure = intentions["heure"]
    objectif = intentions["objectifs"][0]
    actions = intentions["actions"]

    principal = casting_ids[0]
    second = casting_ids[1] if len(casting_ids) > 1 else None
    p_nom = bible.avatars[principal]["nom"].split()[0]
    s_nom = bible.avatars[second]["nom"].split()[0] if second else None

    decor_principal = decors_ids[0]
    decor_mer = "DEC-11" if "DEC-11" not in decors_ids else "DEC-11"
    decor_bord = "DEC-10"

    montre_app = "montrer-app" in actions or "telephone" in actions
    reserve = "payer-mobile" in actions
    embarque = "monter-bord" in actions or "scanner-billet" in actions

    # --- séquence de « beats » --------------------------------------------
    beats = []

    beats.append(dict(
        role="accroche", decor=decor_principal, camera="drone", heure=heure,
        acteurs=[], voix_off=VOIX_OFF.get(objectif, VOIX_OFF["notoriete"])[0], poids=1.2))

    if second:
        beats.append(dict(
            role="situation", decor=decor_principal, camera="cinema", heure=heure,
            acteurs=[(second, "parler", "detendu"), (principal, "sourire", "detendu")],
            dialogue=(second, _tour(REPLIQUES["accroche_question"], 0)), poids=1.0))
        beats.append(dict(
            role="objection", decor=decor_principal, camera="cinema", heure=heure,
            acteurs=[(second, "parler", "inquiet"), (principal, "sourire", "detendu")],
            dialogue=(second, _tour(REPLIQUES["objection"], 0)), poids=1.0))
    else:
        beats.append(dict(
            role="situation", decor=decor_principal, camera="cinema", heure=heure,
            acteurs=[(principal, "regarder-mer", "inquiet")],
            voix_off=_tour(REPLIQUES["objection"], 0), poids=1.0))

    # la démonstration de l'app est le cœur de toute pub MoheliGo : elle est toujours là
    beats.append(dict(
        role="solution", decor=decor_principal, camera="cinema", heure=heure,
        acteurs=[(principal, "montrer-app", "enthousiaste")]
                + ([(second, "sourire", "etonne")] if second else []),
        dialogue=(principal, _tour(REPLIQUES["solution"], 0)), poids=1.0))
    beats.append(dict(
        role="demonstration", decor=decor_principal, camera="gros-plan", heure=heure,
        acteurs=[(principal, "telephone", "serieux")],
        incrustation="app:recherche",
        dialogue=(principal, _tour(REPLIQUES["demonstration"], 0)), poids=1.2))

    if reserve:
        beats.append(dict(
            role="confirmation", decor=decor_principal, camera="gros-plan", heure=heure,
            acteurs=[(principal, "payer-mobile", "heureux")],
            incrustation="app:billet-qr",
            dialogue=(principal, _tour(REPLIQUES["confirmation"], 0)), poids=1.0))

    if second:
        beats.append(dict(
            role="adhesion", decor=decor_principal, camera="cinema", heure=heure,
            acteurs=[(second, "parler", "enthousiaste"), (principal, "rire", "heureux")],
            dialogue=(second, _tour(REPLIQUES["adhesion"], 0)), poids=1.0))

    if embarque:
        beats.append(dict(
            role="embarquement", decor=decor_principal, camera="cinema", heure=heure,
            acteurs=[(principal, "monter-bord", "enthousiaste")]
                    + ([(second, "monter-bord", "heureux")] if second else []),
            dialogue=(principal, _tour(REPLIQUES["embarquement"], 0)), poids=1.1))
        beats.append(dict(
            role="traversee", decor=decor_mer, camera="drone", heure=heure,
            acteurs=[], voix_off=VOIX_OFF.get(objectif, VOIX_OFF["notoriete"])[1], poids=1.2))
    else:
        beats.append(dict(
            role="traversee", decor=decor_mer, camera="drone", heure=heure,
            acteurs=[], voix_off=VOIX_OFF.get(objectif, VOIX_OFF["notoriete"])[1], poids=1.4))

    # décors supplémentaires demandés mais pas encore utilisés
    utilises = {b["decor"] for b in beats}
    for d in decors_ids:
        if d not in utilises and d not in (decor_mer, decor_bord):
            beats.insert(len(beats) - 1, dict(
                role="illustration", decor=d, camera="cinema", heure=heure,
                acteurs=[], poids=0.9))

    beats.append(dict(role="chute", decor=None, camera="fixe", heure=heure,
                      acteurs=[], carton=True, poids=1.1))

    # --- répartition de la durée ------------------------------------------
    total_poids = sum(b["poids"] for b in beats)
    plans = []
    for i, b in enumerate(beats, 1):
        d = round(duree * b["poids"] / total_poids, 1)
        d = max(1.6, min(d, 8.0))
        acteurs = [
            {"avatar": av, "action": act, "expression": exp}
            for av, act, exp in b.get("acteurs", [])
        ]
        plan = {
            "n": i,
            "role": b["role"],
            "duree": d,
            "decor": b["decor"],
            "heure": b["heure"],
            "camera": b["camera"],
            "acteurs": acteurs,
            "dialogue": None,
            "voix_off": b.get("voix_off"),
            "incrustation": b.get("incrustation"),
            "carton": b.get("carton", False),
        }
        if b.get("dialogue"):
            av, texte = b["dialogue"]
            plan["dialogue"] = {"avatar": av, "texte": texte, "langue": langue}
        plans.append(plan)

    # ajustement final pour coller à la durée cible
    ecart = duree - sum(p["duree"] for p in plans)
    if plans:
        plans[-1]["duree"] = round(max(1.6, plans[-1]["duree"] + ecart), 1)

    scenario = {
        "projet": nom_projet,
        "titre": titre or _titre_auto(bible, decor_principal, objectif),
        "brief": intentions["brief"],
        "duree_cible": duree,
        "langue": langue,
        "formats": intentions["formats"],
        "sous_titres": intentions["sous_titres"],
        "objectif": objectif,
        "casting": [
            {
                "avatar": a,
                "nom": bible.avatars[a]["nom"],
                "tenue": bible.avatars[a]["tenues"][0]["id"],
                "coiffure": bible.avatars[a]["coiffures"][0]["id"],
            }
            for a in casting_ids
        ],
        "plans": plans,
        "carton_final": {
            "logo": "MoheliGo",
            "signature": bible.marque["marque"]["signature_sonore_finale"],
            "site": "moheligo.com",
            "mention_ia": bible.marque["mention_ia"]["texte_fr"],
        },
        "musique": "aucune",
        "ambiance": bible.decors[decor_principal].get("ambiance_sonore"),
    }
    return scenario


def _titre_auto(bible, decor_id, objectif):
    d = bible.decors[decor_id]["nom"]
    return {"notoriete": "MoheliGo — %s" % d,
            "conversion": "Réservez votre traversée — %s" % d,
            "confiance": "La mer, en confiance — %s" % d,
            "tourisme": "Destination Mohéli — %s" % d,
            "fret": "Vos marchandises à l'heure — %s" % d}.get(objectif, "MoheliGo — %s" % d)


def ecrire(scenario, dossier):
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, "scenario.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(scenario, f, ensure_ascii=False, indent=2)
    return chemin


def lire(dossier):
    with open(os.path.join(dossier, "scenario.json"), encoding="utf-8") as f:
        return json.load(f)
