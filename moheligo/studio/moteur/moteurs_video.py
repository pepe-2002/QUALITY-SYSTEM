"""Branchement des moteurs d'image et de vidéo externes.

Le studio ne génère pas lui-même les visages photoréalistes : aucun modèle de ce
type ne tourne dans cet environnement. Il prépare TOUT le reste (identités
verrouillées, prompts, seeds, timeline, voix, sous-titres, montage, exports) et
délègue la génération à un moteur, dès qu'une clé d'API est fournie.

Comment brancher un moteur : poser la clé dans l'environnement, puis
    python3 studio.py generer <projet> --moteur fal

Aucune clé n'est stockée dans le dépôt. Le studio lit uniquement les variables
d'environnement listées ci-dessous.
"""

import json
import os
import subprocess
import urllib.request

CA = "/root/.ccr/ca-bundle.crt"

MOTEURS = {
    "fal": {
        "nom": "fal.ai",
        "variable": "FAL_KEY",
        "type": "image + vidéo",
        "modeles": {"image": "fal-ai/flux/dev", "video": "fal-ai/kling-video/v2/master/image-to-video"},
        "url": "https://fal.run/%s",
        "entete": lambda cle: {"Authorization": "Key %s" % cle, "Content-Type": "application/json"},
        "corps_image": lambda p: {"prompt": p["prompt"], "seed": p["seed"],
                                  "image_size": "portrait_16_9", "num_images": 1},
        "corps_video": lambda p, img: {"prompt": p["prompt"], "image_url": img,
                                       "duration": "5", "aspect_ratio": "9:16"},
    },
    "replicate": {
        "nom": "Replicate",
        "variable": "REPLICATE_API_TOKEN",
        "type": "image + vidéo",
        "modeles": {"image": "black-forest-labs/flux-dev", "video": "minimax/video-01"},
        "url": "https://api.replicate.com/v1/models/%s/predictions",
        "entete": lambda cle: {"Authorization": "Bearer %s" % cle, "Content-Type": "application/json"},
        "corps_image": lambda p: {"input": {"prompt": p["prompt"], "seed": p["seed"],
                                            "aspect_ratio": "9:16"}},
        "corps_video": lambda p, img: {"input": {"prompt": p["prompt"], "first_frame_image": img}},
    },
    "runway": {
        "nom": "Runway Gen-3",
        "variable": "RUNWAY_API_KEY",
        "type": "vidéo (image-to-video)",
        "modeles": {"video": "gen3a_turbo"},
        "url": "https://api.dev.runwayml.com/v1/image_to_video",
        "entete": lambda cle: {"Authorization": "Bearer %s" % cle, "Content-Type": "application/json",
                               "X-Runway-Version": "2024-11-06"},
        "corps_video": lambda p, img: {"promptImage": img, "promptText": p["prompt"],
                                       "model": "gen3a_turbo", "ratio": "768:1280"},
    },
    "heygen": {
        "nom": "HeyGen",
        "variable": "HEYGEN_API_KEY",
        "type": "avatar parlant (lip-sync)",
        "modeles": {"avatar": "photo_avatar"},
        "url": "https://api.heygen.com/v2/video/generate",
        "entete": lambda cle: {"X-Api-Key": cle, "Content-Type": "application/json"},
        "note": "à utiliser pour la synchronisation labiale des plans de dialogue, "
                "à partir du portrait figé de l'avatar + la piste voix du studio",
    },
}


def disponibles():
    """Moteurs pour lesquels une clé est présente dans l'environnement."""
    return [c for c, m in MOTEURS.items() if os.environ.get(m["variable"])]


def etat():
    lignes = []
    for cle, m in MOTEURS.items():
        presente = bool(os.environ.get(m["variable"]))
        lignes.append("%-11s %-22s %-26s %s" % (
            cle, m["nom"], m["type"],
            "clé présente" if presente else "clé absente (%s)" % m["variable"]))
    return "\n".join(lignes)


def _appel(url, entetes, corps):
    donnees = json.dumps(corps).encode()
    requete = urllib.request.Request(url, data=donnees, headers=entetes, method="POST")
    with urllib.request.urlopen(requete, timeout=300) as r:
        return json.loads(r.read().decode())


def generer_plans(prompts, dossier_sortie, moteur="fal", type_sortie="video"):
    """Envoie chaque prompt au moteur choisi et récupère les rushes.

    Renvoie la liste des fichiers écrits. Lève une erreur explicite si aucune clé
    n'est configurée — le studio ne fabrique jamais de résultat fictif.
    """
    if moteur not in MOTEURS:
        raise ValueError("moteur inconnu : %s (connus : %s)" % (moteur, ", ".join(MOTEURS)))
    conf = MOTEURS[moteur]
    cle = os.environ.get(conf["variable"])
    if not cle:
        raise RuntimeError(
            "Aucune clé pour %s. Poser %s dans l'environnement, puis relancer.\n"
            "État des moteurs :\n%s" % (conf["nom"], conf["variable"], etat()))

    os.makedirs(dossier_sortie, exist_ok=True)
    produits = []
    for p in prompts:
        corps = (conf["corps_video"](p, p.get("image_reference"))
                 if type_sortie == "video" and "corps_video" in conf
                 else conf["corps_image"](p))
        url = conf["url"]
        if "%s" in url:
            url = url % conf["modeles"].get(type_sortie, next(iter(conf["modeles"].values())))
        reponse = _appel(url, conf["entete"](cle), corps)
        lien = _extraire_lien(reponse)
        if not lien:
            raise RuntimeError("Réponse inattendue du moteur %s : %s" % (moteur, str(reponse)[:300]))
        ext = "mp4" if type_sortie == "video" else "png"
        chemin = os.path.join(dossier_sortie, "plan-%02d.%s" % (p["plan"], ext))
        _telecharger(lien, chemin)
        produits.append(chemin)
    return produits


def _extraire_lien(reponse):
    for cle in ("video", "image", "output"):
        v = reponse.get(cle)
        if isinstance(v, dict) and v.get("url"):
            return v["url"]
        if isinstance(v, str) and v.startswith("http"):
            return v
        if isinstance(v, list) and v and isinstance(v[0], str):
            return v[0]
    images = reponse.get("images")
    if isinstance(images, list) and images and isinstance(images[0], dict):
        return images[0].get("url")
    return None


def _telecharger(url, chemin):
    cmd = ["curl", "-sS", "-L", "-o", chemin, url]
    if os.path.exists(CA):
        cmd[1:1] = ["--cacert", CA]
    subprocess.run(cmd, check=True)
    return chemin
