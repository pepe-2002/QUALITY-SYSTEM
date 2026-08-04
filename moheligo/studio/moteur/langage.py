"""Analyse d'un brief en français : « Fais une pub de 30 secondes où deux amis
discutent au port de Hoani… » → intentions structurées (durée, décors, casting,
actions, langue, formats).

C'est un analyseur déterministe par mots-clés : il tourne sans connexion et sans
modèle de langage. Quand Claude est dans la boucle, il peut écrire directement le
scénario JSON (plus fin) — voir README, section « les deux voies ».
"""

import re
import unicodedata


def _sansaccent(t):
    return "".join(
        c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn"
    )


# --- vocabulaires -----------------------------------------------------------

DECORS_MOTS = {
    "DEC-01": ["hoani", "port de hoani"],
    "DEC-02": ["ouroveni", "port d'ouroveni", "depart grande comore"],
    "DEC-03": ["chindini"],
    "DEC-04": ["fomboni", "port de fomboni"],
    "DEC-05": ["nioumachoua", "plage", "lagon", "ilots", "dauphin"],
    "DEC-06": ["itsamia", "tortue", "tortues", "ponte"],
    "DEC-07": ["hotel", "lodge", "bungalow", "hebergement"],
    "DEC-08": ["restaurant", "repas", "diner", "table"],
    "DEC-09": ["aeroport", "avion", "vol"],
    "DEC-10": ["a bord", "dans la vedette", "interieur de la vedette", "cabine"],
    "DEC-11": ["pleine mer", "traversee", "en mer", "large", "horizon"],
    "DEC-12": ["marche", "marchande", "legumes", "etal"],
    "DEC-13": ["route", "taxi", "minibus", "trajet"],
    "DEC-14": ["bureau", "agence", "guichet", "service client"],
}

# rôles génériques → avatar par défaut
ROLES_MOTS = {
    "AVA-001": ["amina", "voyageuse", "heroine"],
    "AVA-002": ["nassim", "jeune homme", "ami", "amis", "copain"],
    "AVA-003": ["toiwilou", "deuxieme ami", "sceptique"],
    "AVA-004": ["said", "pere de famille", "papa", "pere"],
    "AVA-005": ["hadidja", "mere de famille", "maman", "mere"],
    "AVA-006": ["anfane", "etudiant"],
    "AVA-007": ["chamsia", "etudiante", "influenceuse"],
    "AVA-008": ["camille", "touriste europeenne", "touriste francaise"],
    "AVA-009": ["lukas", "touriste europeen", "plongeur"],
    "AVA-010": ["kwame", "touriste africain"],
    "AVA-011": ["aisha", "touriste africaine"],
    "AVA-012": ["baco", "capitaine", "commandant"],
    "AVA-013": ["momo", "matelot", "second de bord", "equipage"],
    "AVA-014": ["fatima", "hoteliere"],
    "AVA-015": ["youssouf", "hotelier", "gerant"],
    "AVA-016": ["moinaecha", "commercante", "marchande"],
    "AVA-017": ["ibrahim", "commercant", "poissonnier"],
    "AVA-018": ["nadjat", "guide", "guide touristique"],
    "AVA-019": ["ali", "pecheur", "guide baleines", "baleine"],
    "AVA-020": ["zainaba", "agent moheligo", "receptionniste"],
    "AVA-021": ["abdou", "agent du quai", "billettiste", "controleur"],
    "AVA-022": ["farida", "grand-mere", "grand mere", "ainee", "vieille dame"],
    "AVA-023": ["djoumoi", "chauffeur"],
    "AVA-024": ["roukia", "cadre", "femme d'affaires", "professionnelle"],
    "AVA-025": ["salim", "garcon", "enfant"],
    "AVA-026": ["nailat", "fillette", "petite fille"],
}

ACTIONS_MOTS = {
    "montrer-app": ["montre l'application", "montre moheligo", "montre son telephone",
                    "montre l'appli", "lui montre", "presente l'application"],
    "telephone": ["telephone", "smartphone", "ecran", "portable"],
    "payer-mobile": ["reserve", "reservent", "reservation", "paie", "paient", "paiement", "mvola", "kartapay"],
    "monter-bord": ["monte", "montent", "embarque", "embarquent", "a bord", "embarquement"],
    "scanner-billet": ["scanne", "qr", "billet", "controle"],
    "selfie": ["selfie", "photo d'eux", "se prennent en photo"],
    "marcher": ["marche", "marchent", "avance", "se dirige"],
    "courir": ["court", "courent", "se depeche"],
    "rire": ["rient", "rit", "eclat de rire"],
    "sourire": ["sourit", "sourient", "sourire"],
    "serrer-main": ["serrent la main", "poignee de main", "se saluent"],
    "saluer": ["salue", "saluent", "fait signe", "au revoir", "bonjour"],
    "embrasser-famille": ["retrouvailles", "embrasse", "serre dans ses bras", "accueille sa famille"],
    "regarder-mer": ["regarde la mer", "contemple", "horizon"],
    "parler": ["discutent", "discute", "parlent", "parle", "conversation", "dialogue", "explique"],
    "porter-bagage": ["bagage", "valise", "sac", "panier", "marchandise"],
}

CAMERAS_MOTS = {
    "drone": ["drone", "vue du ciel", "aerien"],
    "aerien": ["vue aerienne", "vue satellite", "plongee verticale"],
    "selfie": ["selfie", "camera frontale"],
    "ralenti": ["ralenti", "slow motion"],
    "timelapse": ["timelapse", "accelere"],
    "fixe": ["camera fixe", "plan fixe", "tripied"],
    "cinema": ["cinematographique", "cinema", "travelling"],
    "gros-plan": ["gros plan", "gros-plan", "plan serre"],
}

LANGUES_MOTS = {
    "fr": ["en francais", "voix francaise", "francais"],
    "en": ["en anglais", "anglais", "english"],
    "ar": ["en arabe", "arabe"],
    "shikomori": ["shikomori", "comorien", "shimwali", "shingazidja"],
}

FORMATS_MOTS = {
    "tiktok": ["tiktok", "reels", "shorts", "9:16", "vertical"],
    "facebook": ["facebook", "fb", "4:5"],
    "carre": ["carre", "1:1", "instagram feed"],
    "youtube": ["youtube", "16:9", "horizontal"],
    "youtube4k": ["4k"],
    "statut": ["statut", "whatsapp", "status"],
}

HEURES_MOTS = {
    "aube": ["aube", "lever du soleil", "tot le matin", "petit matin"],
    "matin": ["matin", "matinee"],
    "midi": ["midi", "plein soleil", "milieu de journee"],
    "dore": ["coucher de soleil", "heure doree", "fin de journee", "soir"],
    "nuit": ["nuit", "nocturne", "etoiles"],
}

OBJECTIFS_MOTS = {
    "notoriete": ["faire connaitre", "notoriete", "presenter", "decouvrir"],
    "conversion": ["reserver", "reservation", "telecharger", "inscrire", "vendre"],
    "confiance": ["rassurer", "securite", "fiable", "confiance", "temoignage"],
    "tourisme": ["tourisme", "touriste", "vacances", "destination", "sejour"],
    "fret": ["marchandise", "fret", "commerce", "colis"],
}


def _trouve(texte, table, multiple=True):
    trouves = []
    for cle, mots in table.items():
        for m in mots:
            if re.search(r"\b%s" % re.escape(_sansaccent(m)), texte):
                trouves.append(cle)
                break
    if multiple:
        return trouves
    return trouves[0] if trouves else None


def _duree(texte):
    m = re.search(r"(\d+)\s*(?:secondes?|s\b|sec)", texte)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+)\s*(?:minutes?|min)", texte)
    if m:
        return int(m.group(1)) * 60
    if "une minute" in texte:
        return 60
    return 30


def _nombre_personnes(texte):
    for mot, n in [("deux", 2), ("trois", 3), ("quatre", 4), ("2 ", 2), ("3 ", 3)]:
        if mot in texte:
            return n
    return 1


def analyser(brief):
    """brief (str) → dict d'intentions."""
    t = _sansaccent(brief)

    decors = _trouve(t, DECORS_MOTS)
    casting = _trouve(t, ROLES_MOTS)
    actions = _trouve(t, ACTIONS_MOTS)
    cameras = _trouve(t, CAMERAS_MOTS)
    formats = _trouve(t, FORMATS_MOTS)
    langues = _trouve(t, LANGUES_MOTS)
    heures = _trouve(t, HEURES_MOTS)
    objectifs = _trouve(t, OBJECTIFS_MOTS)

    # « deux amis » : compléter le duo Nassim + Toiwilou
    n = _nombre_personnes(t)
    if "AVA-002" in casting and n >= 2 and "AVA-003" not in casting:
        casting.append("AVA-003")

    if not decors:
        decors = ["DEC-02", "DEC-11", "DEC-01"]  # départ, traversée, arrivée
    if not casting:
        casting = ["AVA-001"]

    return {
        "brief": brief.strip(),
        "duree": _duree(t),
        "decors": decors,
        "casting": casting,
        "actions": actions,
        "cameras": cameras,
        "heure": heures[0] if heures else "dore",
        "langue": langues[0] if langues else "fr",
        "langues_demandees": langues or ["fr"],
        "formats": formats or ["tiktok"],
        "sous_titres": ("sous-titre" in t or "sous titre" in t or True),
        "objectifs": objectifs or ["notoriete"],
        "nb_personnes": n,
    }
