"""Chargement et interrogation de la bible du studio (avatars, décors, grammaire, voix, marque)."""

import json
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_BIBLE = os.path.join(RACINE, "bible")


def _lire(nom):
    with open(os.path.join(DOSSIER_BIBLE, nom), encoding="utf-8") as f:
        return json.load(f)


class Bible:
    def __init__(self):
        self.avatars = {a["id"]: a for a in _lire("avatars.json")["avatars"]}
        d = _lire("decors.json")
        self.decors = {x["id"]: x for x in d["decors"]}
        g = _lire("grammaire.json")
        self.cameras = {c["id"]: c for c in g["cameras"]}
        self.actions = {a["id"]: a for a in g["actions"]}
        self.expressions = {e["id"]: e for e in g["expressions"]}
        self.ambiances = {a["id"]: a for a in g["ambiances"]}
        self.musiques = {m["id"]: m for m in g["musiques"]}
        self.voix = _lire("voix.json")
        self.marque = _lire("marque.json")
        self.formats = {f["id"]: f for f in self.marque["formats_export"]}

    # --- recherche ---------------------------------------------------------

    def avatar(self, ref):
        """Retrouve un avatar par identifiant, nom complet ou prénom."""
        if ref in self.avatars:
            return self.avatars[ref]
        r = ref.strip().lower()
        for a in self.avatars.values():
            if a["nom"].lower() == r or a["nom"].split()[0].lower() == r:
                return a
        raise KeyError("avatar inconnu : %s" % ref)

    def decor(self, ref):
        if ref in self.decors:
            return self.decors[ref]
        r = ref.strip().lower()
        for d in self.decors.values():
            if d["nom"].lower() == r:
                return d
        raise KeyError("décor inconnu : %s" % ref)

    def empreinte_vocale(self, avatar_id, langue="fr"):
        """(voix edge-tts, rate, pitch) d'un avatar, ou None s'il n'a pas de voix."""
        av = self.avatars[avatar_id]
        reglage = self.voix["empreintes"].get(avatar_id, {})
        if reglage.get("interdit"):
            return None
        voix = av.get("voix", {}).get(langue)
        if not voix:
            return None
        return voix, reglage.get("rate", "+0%"), reglage.get("pitch", "+0Hz")

    def narrateur(self, langue="fr", feminin=False):
        cle = "fr_feminin" if (langue == "fr" and feminin) else langue
        n = self.voix["narrateur"].get(cle) or self.voix["narrateur"]["fr"]
        return n["voix"], n.get("rate", "+0%"), n.get("pitch", "+0Hz")

    def photo_decor(self, decor_id, index=0):
        """Chemin absolu d'une photo réelle de référence pour ce décor, ou None."""
        refs = self.decors[decor_id].get("photo_ref") or []
        if not refs:
            return None
        chemin = os.path.normpath(os.path.join(RACINE, refs[index % len(refs)]))
        return chemin if os.path.exists(chemin) else None


class RefusDeProduction(Exception):
    """Le projet viole une règle de la charte : on refuse et on dit pourquoi."""


def controler(bible, scenario):
    """Applique les règles dures de marque.json. Renvoie la liste des avertissements,
    lève RefusDeProduction si une règle bloquante est violée."""
    fautes, avertissements = [], []
    regles_mineurs = bible.marque["regles_mineurs"]["regles"]

    for plan in scenario["plans"]:
        acteurs = plan.get("acteurs", [])
        ids = [a["avatar"] for a in acteurs]
        mineurs = [i for i in ids if bible.avatars[i].get("mineur")]
        if not mineurs:
            continue
        adultes = [i for i in ids if not bible.avatars[i].get("mineur")]
        noms = ", ".join(bible.avatars[i]["nom"] for i in mineurs)
        if not adultes:
            fautes.append(
                "Plan %s : %s est un mineur et se retrouve seul à l'image. Règle : %s"
                % (plan["n"], noms, regles_mineurs[0])
            )
        if plan.get("camera") == "gros-plan" and len(ids) == 1:
            fautes.append(
                "Plan %s : gros plan isolé sur le mineur %s. Règle : %s"
                % (plan["n"], noms, regles_mineurs[2])
            )
        dialogue = plan.get("dialogue")
        if dialogue and dialogue.get("avatar") in mineurs:
            fautes.append(
                "Plan %s : dialogue attribué au mineur %s. Règle : %s"
                % (plan["n"], noms, regles_mineurs[1])
            )

    # vérité publicitaire : un prix chiffré doit rester dans la fourchette connue
    import re

    for plan in scenario["plans"]:
        textes = []
        if plan.get("dialogue"):
            textes.append(plan["dialogue"]["texte"])
        if plan.get("voix_off"):
            textes.append(plan["voix_off"])
        if plan.get("incrustation"):
            textes.append(str(plan["incrustation"]))
        for t in textes:
            for m in re.finditer(r"(\d[\d\s ]{2,})\s*(?:FC|francs)", t, re.I):
                valeur = int(re.sub(r"[^\d]", "", m.group(1)))
                if not 15000 <= valeur <= 17500:
                    avertissements.append(
                        "Plan %s : le prix « %s FC » sort de la fourchette réelle connue "
                        "(15 000 – 17 500 FC). À confirmer sur les données de l'app avant diffusion."
                        % (plan["n"], valeur)
                    )

    if fautes:
        raise RefusDeProduction(
            "Production refusée — protection des mineurs :\n  - " + "\n  - ".join(fautes)
        )
    return avertissements
