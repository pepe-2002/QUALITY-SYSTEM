"""JEU DE TEST TENU À L'ÉCART — à n'utiliser qu'une fois, à la fin.

Le jeu de la Phase 4 (`corpus.py` + `dataset.py`) est **brûlé** : le système a
été corrigé après avoir vu ses résultats. Il ne peut plus servir qu'à
calibrer, jamais à conclure — mesurer sur ce qui a servi à régler, c'est
mesurer son propre réglage.

D'où ce second jeu :

* **autre domaine** — une coopérative agricole, pas des traversées maritimes.
  Aucune page, aucun chiffre, aucun mot-clé en commun avec le jeu de
  calibration ;
* **écrit avant** d'avoir lancé la moindre stratégie dessus, et versionné dans
  un commit antérieur à celui des résultats : l'ordre est vérifiable dans
  l'historique Git, ce n'est pas une promesse sur l'honneur ;
* **mêmes familles** — facile / profond / piège — pour que la comparaison
  porte sur la stratégie et non sur la difficulté du terrain.

⚠️ Ce que ce jeu ne corrige pas : il est écrit par l'auteur du système. C'est
une séparation **calibration / test**, pas une réplication indépendante. Un
tiers écrivant son propre corpus reste le seul vrai contrôle, et le rapport
le dit.
"""

from __future__ import annotations

from .corpus import Corpus, page
from .dataset import Gold, Task

# --- Le web figé du jeu de test ------------------------------------------------

PAGES: dict[str, str] = {
    # -- prix d'achat : deux sources concordantes, première recherche ---------
    "https://cooperative-nord.test/prix-achat": page(
        "Prix d'achat aux planteurs",
        "La coopérative achète la vanille verte 4 500 francs comoriens le kilogramme "
        "aux planteurs adhérents.",
        "Le paiement intervient sous 15 jours après la livraison au centre.",
    ),
    "https://chambre-agriculture.test/filiere-vanille": page(
        "La filière vanille en 2026",
        "Le prix d'achat de la vanille verte au planteur s'établit à "
        "4 500 francs comoriens le kilogramme cette campagne.",
        "La filière fait vivre plusieurs milliers de familles.",
    ),
    # -- séchage : durée donnée par deux pages -------------------------------
    "https://cooperative-nord.test/sechage": page(
        "Le séchage des gousses",
        "Le séchage complet des gousses demande 90 jours après l'échaudage.",
        "Les gousses sont étalées au soleil le matin puis remisées en malle.",
    ),
    "https://guide-planteur.test/preparation": page(
        "Préparer sa récolte",
        "Comptez 90 jours de séchage avant le conditionnement des gousses.",
        "Un séchage bâclé fait perdre tout l'arôme.",
    ),
    # -- distance : deux sources indépendantes -------------------------------
    "https://transport-rural.test/collecte": page(
        "Tournée de collecte",
        "Le centre de collecte se trouve à 12 kilomètres du village de plantation.",
    ),
    "https://annuaire-villages.test/plateau": page(
        "Le plateau agricole",
        "La distance entre le village et le centre de collecte est de 12 kilomètres.",
    ),
    # -- rendement : information isolée, jamais confirmée --------------------
    "https://institut-agronomique.test/rendement": page(
        "Rendement au séchage",
        "Le rendement au séchage est de 20 pour cent : cinq kilogrammes de "
        "vanille verte donnent un kilogramme de vanille préparée.",
    ),
    # -- horaire d'ouverture : SEULE la page officielle le donne --------------
    "https://blog-agricole.test/coop": page(
        "Visite à la coopérative",
        "Le centre ouvre tôt, mais les horaires changent souvent selon la "
        "saison et l'affluence des planteurs.",
        "Mieux vaut appeler avant de se déplacer avec sa récolte.",
    ),
    "https://forum-planteurs.test/coop": page(
        "Forum : livrer sa récolte",
        "Personne ne sait dire l'heure exacte d'ouverture du centre.",
        "Un planteur dit y aller le matin, sans plus de précision.",
    ),
    "https://cooperative-nord.test/reglement": page(
        "Règlement intérieur du centre de collecte",
        "Le centre de collecte ouvre officiellement à 6 heures du matin.",
        "La pesée des lots s'arrête 2 heures avant la fermeture.",
    ),
    # -- PIÈGE : archive périmée sur le même sujet ---------------------------
    "https://archives-filiere.test/2018": page(
        "Campagne 2018 — archive",
        "En 2018, la coopérative achetait la vanille verte 1 800 francs "
        "comoriens le kilogramme aux planteurs.",
    ),
    # -- PIÈGE : autre produit, chiffre franchement différent -----------------
    "https://cooperative-sud.test/girofle": page(
        "Achat du clou de girofle",
        "Le clou de girofle est acheté 8 200 francs comoriens le kilogramme aux planteurs.",
    ),
    # -- PIÈGE : page bavarde, plusieurs chiffres sans rapport ---------------
    "https://magazine-rural.test/vie-du-village": page(
        "La vie du village",
        "Le sac d'engrais coûte 32 000 francs comoriens à la boutique du bourg.",
        "La journée d'un ouvrier agricole est payée 3 000 francs comoriens.",
        "Le transport d'un lot jusqu'au port revient à 7 500 francs comoriens.",
    ),
    # -- cotisation : une seule source, information ferme ---------------------
    "https://cooperative-nord.test/adhesion": page(
        "Adhérer à la coopérative",
        "La cotisation annuelle d'un planteur adhérent est de 5 000 francs comoriens.",
    ),
}


INDEX: dict[str, list[str]] = {
    "prix achat vanille verte planteur": [
        "https://cooperative-nord.test/prix-achat",
        "https://chambre-agriculture.test/filiere-vanille",
        "https://magazine-rural.test/vie-du-village",
    ],
    "prix officiel vanille campagne": [
        "https://cooperative-nord.test/prix-achat",
        "https://archives-filiere.test/2018",
        "https://cooperative-sud.test/girofle",
    ],
    "duree sechage gousses": [
        "https://cooperative-nord.test/sechage",
        "https://guide-planteur.test/preparation",
    ],
    "distance village centre collecte": [
        "https://transport-rural.test/collecte",
        "https://annuaire-villages.test/plateau",
    ],
    "rendement sechage pourcentage": [
        "https://institut-agronomique.test/rendement",
    ],
    "horaire ouverture centre collecte": [
        "https://blog-agricole.test/coop",
        "https://forum-planteurs.test/coop",
    ],
    "reglement officiel centre collecte": [
        "https://cooperative-nord.test/reglement",
        "https://blog-agricole.test/coop",
    ],
    "cotisation annuelle adherent cooperative": [
        "https://cooperative-nord.test/adhesion",
    ],
    "transport lot port cout": [
        "https://magazine-rural.test/vie-du-village",
    ],
    "clou girofle prix achat": [
        "https://cooperative-sud.test/girofle",
    ],
}


def held_out_corpus() -> Corpus:
    return Corpus(pages=dict(PAGES), index=dict(INDEX))


# --- Les tâches ----------------------------------------------------------------

TASKS: list[Task] = [
    # --- facile : la première recherche suffit ------------------------------
    Task(
        id="prix_vanille",
        question="Combien la coopérative achète-t-elle le kilo de vanille verte ?",
        gold=[Gold("money", 4500, "4 500 FC le kilo")],
        family="facile",
        note="Deux sources concordantes dès la première requête.",
        paraphrases=[
            "Quel est le prix d'achat du kilo de vanille verte au planteur ?",
            "À combien est payé le kilogramme de vanille verte aux planteurs ?",
        ],
    ),
    Task(
        id="sechage",
        question="Combien de temps dure le séchage des gousses ?",
        gold=[Gold("duration", 129600, "90 jours")],
        family="facile",
        note="Durée donnée par deux pages différentes.",
        paraphrases=[
            "Quelle est la durée de séchage des gousses de vanille ?",
            "Combien de jours faut-il pour sécher les gousses ?",
        ],
    ),
    Task(
        id="distance_collecte",
        question="Quelle distance sépare le village du centre de collecte ?",
        gold=[Gold("distance", 12, "12 km")],
        family="facile",
        note="Deux sources indépendantes, aucune ambiguïté.",
        paraphrases=[
            "Combien de kilomètres y a-t-il entre le village et le centre de collecte ?",
            "À quelle distance du village se trouve le centre de collecte ?",
        ],
    ),
    Task(
        id="cotisation",
        question="Combien coûte la cotisation annuelle d'un planteur adhérent ?",
        gold=[Gold("money", 5000, "5 000 FC")],
        family="facile",
        note="Une seule page, mais elle répond directement.",
        paraphrases=[
            "Quel est le montant de la cotisation annuelle à la coopérative ?",
            "Combien un planteur paie-t-il de cotisation chaque année ?",
        ],
    ),
    # --- profond : il faut une relance ciblée -------------------------------
    Task(
        id="ouverture",
        question="À quelle heure ouvre le centre de collecte ?",
        gold=[Gold("time", 6, "6 h du matin")],
        family="profond",
        note="Blog et forum l'ignorent. Seul le règlement intérieur répond, "
             "et il faut une requête ciblée pour l'atteindre.",
        paraphrases=[
            "Quel est l'horaire d'ouverture du centre de collecte ?",
            "Le centre de collecte ouvre à quelle heure le matin ?",
        ],
    ),
    Task(
        id="rendement",
        question="Quel est le rendement au séchage de la vanille, en pourcentage ?",
        gold=[Gold("percent", 20, "20 %")],
        family="profond",
        note="Un seul institut le publie ; la requête générale ne le ramène pas.",
        paraphrases=[
            "Quel pourcentage de vanille préparée obtient-on au séchage ?",
            "Quel est le taux de rendement au séchage des gousses ?",
        ],
    ),
    # --- piège : chercher plus peut nuire -----------------------------------
    Task(
        id="prix_officiel_vanille",
        question="Quel est le prix d'achat officiel de la vanille cette campagne ?",
        gold=[Gold("money", 4500, "4 500 FC le kilo")],
        distractors=[Gold("money", 1800, "1 800 FC (archive 2018)"),
                     Gold("money", 8200, "8 200 FC (girofle, autre produit)")],
        family="piege",
        note="Le mot « officiel » ramène une archive de 2018 et un autre "
             "produit. Chercher plus expose à répondre faux.",
        paraphrases=[
            "Quel est le tarif officiel d'achat de la vanille pour cette campagne ?",
            "Combien vaut officiellement le kilo de vanille cette année ?",
        ],
    ),
    Task(
        id="transport",
        question="Combien coûte le transport d'un lot jusqu'au port ?",
        gold=[Gold("money", 7500, "7 500 FC")],
        family="piege",
        note="La page contient trois montants sans rapport. Le risque est de "
             "retenir le mauvais.",
        paraphrases=[
            "Quel est le prix du transport d'un lot jusqu'au port ?",
            "Combien faut-il payer pour acheminer un lot au port ?",
        ],
    ),
    Task(
        id="girofle",
        question="À quel prix le clou de girofle est-il acheté au planteur ?",
        gold=[Gold("money", 8200, "8 200 FC le kilo")],
        distractors=[Gold("money", 4500, "4 500 FC (vanille, autre produit)")],
        family="piege",
        note="Sujet voisin du prix de la vanille : une stratégie qui élargit "
             "sa recherche ramène le mauvais produit.",
        paraphrases=[
            "Combien est payé le kilo de clou de girofle aux planteurs ?",
            "Quel est le prix d'achat du girofle au planteur ?",
        ],
    ),
    Task(
        id="engrais",
        question="Combien coûte le sac d'engrais à la boutique du bourg ?",
        gold=[Gold("money", 32000, "32 000 FC")],
        family="piege",
        note="Même page que le transport et la journée d'ouvrier : trois "
             "montants, un seul est demandé.",
        paraphrases=[
            "Quel est le prix d'un sac d'engrais à la boutique du bourg ?",
            "À combien revient le sac d'engrais au bourg ?",
        ],
    ),
]


def by_family(family: str) -> list[Task]:
    return [task for task in TASKS if task.family == family]
