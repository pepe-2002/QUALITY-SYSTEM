"""Génération des prompts verrouillés à donner au moteur d'image/vidéo.

Règle d'or : l'identité d'un avatar et celle d'un décor sont copiées TELLES QUELLES,
en tête du prompt, avec leur seed. C'est ce qui fait que Nassim a le même visage
dans la pub de janvier et dans celle de juin.
"""

import json
import os

LUMIERE = {
    "aube": "soft dawn light, long shadows, pink and gold sky",
    "matin": "clear morning light, fresh colours",
    "midi": "harsh midday tropical sun, short shadows, high contrast",
    "dore": "golden hour, warm low sun, long shadows",
    "nuit": "night scene, moonlight and warm practical lights, deep blue shadows",
}

QUALITE = (
    "photorealistic, natural skin texture, realistic anatomy, documentary photography style, "
    "shot on a full-frame camera, high dynamic range"
)

NEGATIF = (
    "no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, "
    "no plastic skin, no cartoon, no stock-photo smile, no snow, no western city"
)


def prompt_plan(bible, plan, casting):
    """Renvoie le dict de prompt d'un plan."""
    tenues = {c["avatar"]: c for c in casting}
    morceaux = []
    seeds = []

    for acteur in plan.get("acteurs", []):
        av = bible.avatars[acteur["avatar"]]
        choix = tenues.get(acteur["avatar"], {})
        tenue = _trouver(av["tenues"], choix.get("tenue"))
        coiffure = _trouver(av["coiffures"], choix.get("coiffure"))
        action = bible.actions.get(acteur["action"], {}).get("prompt", acteur["action"])
        expression = bible.expressions.get(acteur["expression"], {}).get(
            "prompt", acteur["expression"]
        )
        morceaux.append(
            "%s, wearing %s, %s, %s, %s" % (av["identite"], tenue, coiffure, action, expression)
        )
        seeds.append(av["seed"])

    if plan.get("decor"):
        d = bible.decors[plan["decor"]]
        lieu = d["identite"]
        seeds.append(d["seed"])
    else:
        lieu = "plain brand background, no location"

    cam = bible.cameras.get(plan.get("camera"), {}).get("prompt", "")
    lum = LUMIERE.get(plan.get("heure"), "")

    if morceaux:
        texte = "%s. Location: %s. %s. %s. %s." % (" AND ".join(morceaux), lieu, lum, cam, QUALITE)
    else:
        texte = "%s. %s. %s. %s." % (lieu, lum, cam, QUALITE)

    return {
        "plan": plan["n"],
        "role": plan["role"],
        "duree": plan["duree"],
        "seed": seeds[0] if seeds else 0,
        "seeds_references": seeds,
        "prompt": texte,
        "negatif": NEGATIF,
        "image_reference": _photo_ref(bible, plan),
        "incrustation": plan.get("incrustation"),
        "note": _note(plan),
    }


def _trouver(liste, cle):
    for x in liste:
        if x["id"] == cle:
            return x["desc"]
    return liste[0]["desc"]


def _photo_ref(bible, plan):
    if not plan.get("decor"):
        return None
    chemin = bible.photo_decor(plan["decor"])
    if not chemin:
        return None
    return os.path.relpath(chemin, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _note(plan):
    incrustation = plan.get("incrustation") or ""
    if incrustation.startswith("app:"):
        return (
            "L'écran de l'application n'est PAS généré par le moteur : filmer l'app réelle "
            "(moheligo.com) puis incruster l'écran dans le téléphone au montage. "
            "Procédé documenté dans MEMOIRE.md (Playwright, viewport 540x960)."
        )
    if plan.get("carton"):
        return "Carton final composé par le studio (PIL/ffmpeg), pas par le moteur d'image."
    return None


def generer(bible, scenario, dossier):
    """Écrit prompts.json et prompts.md dans le dossier du projet."""
    casting = scenario["casting"]
    liste = [prompt_plan(bible, p, casting) for p in scenario["plans"]]

    os.makedirs(dossier, exist_ok=True)
    with open(os.path.join(dossier, "prompts.json"), "w", encoding="utf-8") as f:
        json.dump({"projet": scenario["projet"], "plans": liste}, f, ensure_ascii=False, indent=2)

    lignes = [
        "# Prompts de génération — %s" % scenario["titre"],
        "",
        "> À coller dans le moteur vidéo (Veo, Kling, Runway, Sora, Hailuo…) ou à envoyer",
        "> par API via `moteur/moteurs_video.py`. **Ne pas reformuler le début du prompt** :",
        "> c'est l'identité verrouillée de l'avatar et du décor, c'est elle qui garantit",
        "> qu'on retrouve le même visage et le même lieu d'une pub à l'autre.",
        "",
        "| Plan | Rôle | Durée | Seed |",
        "|---|---|---|---|",
    ]
    for p in liste:
        lignes.append("| %s | %s | %.1f s | `%s` |" % (p["plan"], p["role"], p["duree"], p["seed"]))
    lignes.append("")

    for p in liste:
        lignes += [
            "## Plan %s — %s (%.1f s)" % (p["plan"], p["role"], p["duree"]),
            "",
            "**Seed : `%s`**" % p["seed"],
            "",
            "```",
            p["prompt"],
            "```",
            "",
            "*À exclure :* `%s`" % p["negatif"],
            "",
        ]
        if p["image_reference"]:
            lignes += ["*Image de référence (image-to-video) :* `%s`" % p["image_reference"], ""]
        if p["note"]:
            lignes += ["> ⚠ %s" % p["note"], ""]

    with open(os.path.join(dossier, "prompts.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    return liste
