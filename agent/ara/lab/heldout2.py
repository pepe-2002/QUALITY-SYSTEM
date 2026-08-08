"""SECOND JEU DE TEST TENU À L'ÉCART — pour évaluer le contrôleur corrigé.

Pourquoi un troisième jeu. Le contrôleur a été corrigé *après* l'expérience
H2, donc en connaissant les tâches sur lesquelles il perdait. Le jeu
`heldout.py` ne peut plus servir de preuve : rejouer dessus mesurerait en
partie ma mémoire de ses résultats. Il reste utile — comme indice, pas comme
verdict.

Ce jeu-ci est écrit **avant** d'avoir lancé le contrôleur corrigé dessus, dans
un troisième domaine, et versionné dans un commit antérieur à celui des
résultats. Il est fait pour être joué **une seule fois**.

Construction volontairement parallèle aux deux autres — mêmes familles, mêmes
formes de pièges — pour que la comparaison porte sur la stratégie et non sur
la difficulté du terrain. Ce qui change : le domaine, les entités, les
chiffres, les formulations.

⚠️ Même réserve que pour `heldout.py`, et elle ne s'efface pas : ce jeu est
écrit par l'auteur du système. Séparation calibration / test, pas réplication
indépendante.
"""

from __future__ import annotations

from .corpus import Corpus, page
from .dataset import Gold, Task

# --- Le web figé ---------------------------------------------------------------

PAGES: dict[str, str] = {
    # -- consultation : deux sources concordantes, première recherche --------
    "https://centre-sante.test/tarifs": page(
        "Tarifs des consultations",
        "La consultation générale au dispensaire coûte 2 500 francs comoriens "
        "par patient.",
        "Le carnet de santé est délivré lors de la première visite.",
    ),
    "https://ministere-sante.test/grille": page(
        "Grille tarifaire des dispensaires",
        "Le tarif d'une consultation générale en dispensaire est fixé à "
        "2 500 francs comoriens.",
        "Les femmes enceintes bénéficient d'un suivi dédié.",
    ),
    # -- durée de la formation des agents : deux pages ------------------------
    "https://centre-sante.test/formation": page(
        "Formation des agents communautaires",
        "La formation initiale des agents de santé communautaire dure 6 semaines.",
        "Elle alterne théorie et stage en dispensaire.",
    ),
    "https://ecole-infirmiers.test/programme": page(
        "Programme de formation",
        "Comptez 6 semaines de formation initiale avant l'affectation en poste.",
        "Un module de vaccination clôt le cursus.",
    ),
    # -- distance jusqu'à l'hôpital de référence ------------------------------
    "https://carte-sanitaire.test/reseau": page(
        "Réseau sanitaire du district",
        "Le dispensaire se situe à 35 kilomètres de l'hôpital de référence.",
    ),
    "https://annuaire-sante.test/district": page(
        "Annuaire des structures",
        "La distance entre le dispensaire et l'hôpital de référence est de "
        "35 kilomètres.",
    ),
    # -- stock : information isolée, jamais confirmée -------------------------
    "https://pharmacie-centrale.test/dotation": page(
        "Dotation en médicaments",
        "Chaque dispensaire reçoit une dotation trimestrielle de 40 kilogrammes "
        "de médicaments essentiels.",
    ),
    # -- couverture vaccinale : SEUL l'institut la publie ---------------------
    "https://blog-sante.test/terrain": page(
        "Carnet de terrain",
        "La couverture vaccinale progresse, mais les chiffres varient beaucoup "
        "d'un district à l'autre selon les campagnes.",
        "Les équipes mobiles font la différence dans les villages isolés.",
    ),
    "https://forum-soignants.test/vaccination": page(
        "Forum : campagnes de vaccination",
        "Personne ici n'a le taux exact, cela dépend des années.",
        "Un collègue parle d'une nette amélioration, sans chiffre.",
    ),
    "https://institut-statistique.test/couverture": page(
        "Institut de statistique — couverture vaccinale",
        "Le taux de couverture vaccinale du district s'établit à 72 pour cent.",
    ),
    # -- horaire d'ouverture : SEUL le règlement le donne ---------------------
    "https://blog-sante.test/visite": page(
        "Une visite au dispensaire",
        "Le dispensaire ouvre tôt le matin, mais l'heure change selon les jours "
        "et l'affluence.",
        "Mieux vaut demander au village avant de s'y rendre.",
    ),
    "https://centre-sante.test/reglement": page(
        "Règlement intérieur du dispensaire",
        "L'accueil des patients ouvre officiellement à 8 heures du matin.",
        "Les consultations s'arrêtent 1 heure avant la fermeture.",
    ),
    # -- PIÈGE : archive périmée sur le même sujet ---------------------------
    "https://archives-sante.test/2017": page(
        "Tarifs 2017 — archive",
        "En 2017, la consultation générale au dispensaire coûtait 900 francs "
        "comoriens.",
    ),
    # -- PIÈGE : autre structure, tarif franchement différent ----------------
    "https://clinique-privee.test/tarifs": page(
        "Tarifs de la clinique privée",
        "La consultation en clinique privée est facturée 12 000 francs comoriens.",
    ),
    # -- PIÈGE : page bavarde, plusieurs chiffres sans rapport ---------------
    "https://magazine-district.test/vie-locale": page(
        "La vie du district",
        "Le transport en taxi-brousse jusqu'au chef-lieu coûte 1 200 francs comoriens.",
        "Une nuit à la maison de passage revient à 8 000 francs comoriens.",
        "Le repas à la cantine du centre est facturé 900 francs comoriens.",
    ),
    # -- carnet : une seule source, information ferme -------------------------
    "https://centre-sante.test/carnet": page(
        "Le carnet de santé",
        "La délivrance du carnet de santé coûte 500 francs comoriens.",
    ),
}


INDEX: dict[str, list[str]] = {
    "tarif consultation dispensaire": [
        "https://centre-sante.test/tarifs",
        "https://ministere-sante.test/grille",
        "https://magazine-district.test/vie-locale",
    ],
    "tarif officiel consultation": [
        "https://centre-sante.test/tarifs",
        "https://archives-sante.test/2017",
        "https://clinique-privee.test/tarifs",
    ],
    "duree formation agents sante": [
        "https://centre-sante.test/formation",
        "https://ecole-infirmiers.test/programme",
    ],
    "distance dispensaire hopital reference": [
        "https://carte-sanitaire.test/reseau",
        "https://annuaire-sante.test/district",
    ],
    "dotation medicaments trimestrielle": [
        "https://pharmacie-centrale.test/dotation",
    ],
    "couverture vaccinale district": [
        "https://blog-sante.test/terrain",
        "https://forum-soignants.test/vaccination",
    ],
    "couverture vaccinale institut statistique officiel": [
        "https://institut-statistique.test/couverture",
        "https://blog-sante.test/terrain",
    ],
    "horaire ouverture dispensaire": [
        "https://blog-sante.test/visite",
        "https://forum-soignants.test/vaccination",
    ],
    "reglement officiel dispensaire accueil": [
        "https://centre-sante.test/reglement",
        "https://blog-sante.test/visite",
    ],
    "carnet sante delivrance prix": [
        "https://centre-sante.test/carnet",
    ],
    "transport taxi brousse chef lieu": [
        "https://magazine-district.test/vie-locale",
    ],
    "consultation clinique privee tarif": [
        "https://clinique-privee.test/tarifs",
    ],
}


def held_out_corpus() -> Corpus:
    return Corpus(pages=dict(PAGES), index=dict(INDEX))


# --- Les tâches ----------------------------------------------------------------

TASKS: list[Task] = [
    # --- facile -------------------------------------------------------------
    Task(
        id="consultation",
        question="Combien coûte une consultation au dispensaire ?",
        gold=[Gold("money", 2500, "2 500 FC")],
        family="facile",
        note="Deux sources concordantes dès la première requête.",
        paraphrases=[
            "Quel est le prix d'une consultation au dispensaire ?",
            "Combien faut-il payer pour une consultation au dispensaire ?",
        ],
    ),
    Task(
        id="formation",
        question="Combien de temps dure la formation des agents de santé ?",
        gold=[Gold("duration", 60480, "6 semaines")],
        family="facile",
        note="Durée donnée par deux pages différentes.",
        paraphrases=[
            "Quelle est la durée de la formation des agents de santé ?",
            "Combien de semaines dure la formation initiale des agents ?",
        ],
    ),
    Task(
        id="distance_hopital",
        question="Quelle distance sépare le dispensaire de l'hôpital de référence ?",
        gold=[Gold("distance", 35, "35 km")],
        family="facile",
        note="Deux sources indépendantes, aucune ambiguïté.",
        paraphrases=[
            "Combien de kilomètres séparent le dispensaire de l'hôpital de référence ?",
            "À quelle distance de l'hôpital de référence se trouve le dispensaire ?",
        ],
    ),
    Task(
        id="carnet",
        question="Combien coûte la délivrance du carnet de santé ?",
        gold=[Gold("money", 500, "500 FC")],
        family="facile",
        note="Une seule page, mais elle répond directement.",
        paraphrases=[
            "Quel est le prix du carnet de santé ?",
            "Combien faut-il payer pour obtenir le carnet de santé ?",
        ],
    ),
    # --- profond ------------------------------------------------------------
    Task(
        id="ouverture_dispensaire",
        question="À quelle heure ouvre l'accueil du dispensaire ?",
        gold=[Gold("time", 8, "8 h du matin")],
        family="profond",
        note="Blog et forum l'ignorent. Seul le règlement intérieur répond.",
        paraphrases=[
            "Quel est l'horaire d'ouverture de l'accueil du dispensaire ?",
            "Le dispensaire ouvre à quelle heure le matin ?",
        ],
    ),
    Task(
        id="couverture",
        question="Quel est le taux de couverture vaccinale du district, en pourcentage ?",
        gold=[Gold("percent", 72, "72 %")],
        family="profond",
        note="Seul l'institut de statistique le publie ; la requête générale "
             "ne ramène que blog et forum.",
        paraphrases=[
            "Quel pourcentage de couverture vaccinale atteint le district ?",
            "À combien s'élève le taux de vaccination du district ?",
        ],
    ),
    Task(
        id="dotation",
        question="Quel poids de médicaments le dispensaire reçoit-il par trimestre ?",
        gold=[Gold("weight", 40, "40 kg")],
        family="profond",
        note="Une seule source la donne, et aucune autre ne la confirmera.",
        paraphrases=[
            "Combien de kilogrammes de médicaments sont livrés chaque trimestre ?",
            "Quelle est la dotation trimestrielle en médicaments, en kilos ?",
        ],
    ),
    # --- piège --------------------------------------------------------------
    Task(
        id="tarif_officiel_consultation",
        question="Quel est le tarif officiel d'une consultation ?",
        gold=[Gold("money", 2500, "2 500 FC")],
        distractors=[Gold("money", 900, "900 FC (archive 2017)"),
                     Gold("money", 12000, "12 000 FC (clinique privée)")],
        family="piege",
        note="Le mot « officiel » ramène une archive de 2017 et une clinique "
             "privée. Chercher plus expose à répondre faux.",
        paraphrases=[
            "Quel est le tarif officiel en vigueur pour une consultation ?",
            "Combien coûte officiellement une consultation aujourd'hui ?",
        ],
    ),
    Task(
        id="taxi",
        question="Combien coûte le taxi-brousse jusqu'au chef-lieu ?",
        gold=[Gold("money", 1200, "1 200 FC")],
        family="piege",
        note="Même page que la maison de passage et la cantine : trois "
             "montants, un seul est demandé.",
        paraphrases=[
            "Quel est le prix du taxi-brousse jusqu'au chef-lieu ?",
            "Combien faut-il payer le taxi-brousse pour aller au chef-lieu ?",
        ],
    ),
    Task(
        id="clinique",
        question="Combien coûte une consultation en clinique privée ?",
        gold=[Gold("money", 12000, "12 000 FC")],
        distractors=[Gold("money", 2500, "2 500 FC (dispensaire, autre structure)")],
        family="piege",
        note="Sujet voisin du tarif du dispensaire : une recherche trop large "
             "ramène la mauvaise structure.",
        paraphrases=[
            "Quel est le prix d'une consultation dans une clinique privée ?",
            "À combien est facturée la consultation en clinique privée ?",
        ],
    ),
]


def by_family(family: str) -> list[Task]:
    return [task for task in TASKS if task.family == family]
