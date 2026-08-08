"""JEU 4 — corpus adversarial pour RESEARCH-V2. Jamais utilisé auparavant.

Les jeux 1 à 3 mesuraient la *décision de chercher*. Celui-ci mesure la
**pertinence de ce qu'on retient** : ses pièges ne sont pas des chiffres
trompeurs, ce sont des pages qui *ressemblent* à la bonne réponse.

Six formes de faux positifs, chacune tirée d'un mode d'échec réel :

1. **même vocabulaire, autre lieu** — le piège exact rencontré en conditions
   réelles : des traversées en vedette, avec tarifs et horaires, dans un autre
   pays ;
2. **noms voisins** — deux endroits qui partagent un nom ;
3. **termes génériques** — une page qui n'emploie que le vocabulaire du genre,
   sans jamais nommer le sujet ;
4. **hors période** — la bonne chose, la mauvaise année ;
5. **même objet, autre contexte** — le sujet est bien nommé, mais on parle
   d'autre chose à son propos ;
6. **bonne réponse** — sinon le banc ne mesurerait que le rejet.

⚠️ Aucun résultat de H1 ou H2 n'a servi à calibrer ce jeu, et il n'est pas
dérivé des trois autres. Même réserve que d'habitude, et elle ne s'efface
pas : il reste écrit par l'auteur du système.
"""

from __future__ import annotations

from .corpus import Corpus, page
from .dataset import Gold, Task

#: Nature de chaque page, pour mesurer les faux positifs par catégorie.
#: sujet · autre_lieu · nom_voisin · generique · perime · autre_contexte
LABELS: dict[str, str] = {}


def _page(url: str, label: str, title: str, *paragraphes: str) -> tuple[str, str]:
    LABELS[url] = label
    return url, page(title, *paragraphes)


PAGES: dict[str, str] = dict(
    [
        # === Sujet : traversée fluviale de Bandiagara (pays A) ==============
        _page(
            "https://compagnie-bandiagara.test/tarifs",
            "sujet",
            "Traversée du fleuve à Bandiagara — tarifs",
            "La traversée en pirogue motorisée entre Bandiagara et Songho coûte "
            "3 200 francs par passager.",
            "Les départs ont lieu toute la journée selon l'affluence.",
        ),
        _page(
            "https://office-tourisme-bandiagara.test/pirogues",
            "sujet",
            "Se déplacer autour de Bandiagara",
            "Comptez 3 200 francs pour la traversée Bandiagara – Songho en "
            "pirogue motorisée.",
            "La traversée dure environ 40 minutes.",
        ),
        # === Piège 1 : même vocabulaire, autre pays =========================
        _page(
            "https://vedettes-lacustres.test/tarifs",
            "autre_lieu",
            "Vedettes lacustres — nos tarifs de traversée",
            "La traversée en vedette coûte 9 500 francs par passager, tarif "
            "officiel affiché à l'embarcadère.",
            "Horaires, billets et traversées toute l'année.",
        ),
        _page(
            "https://traversees-du-delta.test/billets",
            "autre_lieu",
            "Billets et tarifs des traversées du delta",
            "Le tarif officiel de la traversée en pirogue est de 1 400 francs "
            "par personne.",
            "Nos vedettes assurent la liaison plusieurs fois par jour.",
        ),
        # === Piège 2 : nom voisin ==========================================
        _page(
            "https://bandiagara-nord.test/bac",
            "nom_voisin",
            "Bac de Bandiagara-Nord",
            "La traversée du bac de Bandiagara-Nord, dans la province voisine, "
            "coûte 700 francs par véhicule.",
            "Ce bac n'a aucun lien avec la liaison vers Songho.",
        ),
        # === Piège 3 : termes génériques, sujet jamais nommé ================
        _page(
            "https://guide-transport.test/pirogues",
            "generique",
            "Voyager en pirogue : ce qu'il faut savoir",
            "Le prix d'une traversée en pirogue varie de 500 à 12 000 francs "
            "selon la distance et la saison.",
            "Vérifiez toujours le tarif officiel auprès du batelier.",
        ),
        # === Piège 4 : bon sujet, mauvaise période ==========================
        _page(
            "https://archives-transport.test/bandiagara-2014",
            "perime",
            "Bandiagara — tarifs 2014 (archive)",
            "En 2014, la traversée entre Bandiagara et Songho coûtait "
            "900 francs par passager.",
        ),
        # === Piège 5 : bon sujet, autre contexte ============================
        _page(
            "https://patrimoine-bandiagara.test/histoire",
            "autre_contexte",
            "Bandiagara — histoire du site",
            "Bandiagara est connue pour ses falaises classées depuis 1989.",
            "L'entrée du musée de Bandiagara coûte 2 000 francs.",
        ),
        # === Sujet : horaire, une seule source =============================
        _page(
            "https://autorite-fluviale.test/horaires-bandiagara",
            "sujet",
            "Autorité fluviale — horaires officiels Bandiagara",
            "Le départ officiel de la pirogue de Bandiagara vers Songho est "
            "fixé à 6 heures du matin.",
        ),
        _page(
            "https://blog-voyage-sahel.test/bandiagara",
            "sujet",
            "Carnet de route : Bandiagara",
            "Les pirogues partent tôt, mais l'heure exacte change selon la "
            "saison et le niveau du fleuve.",
        ),
        # === Sujet : distance ==============================================
        _page(
            "https://geo-fleuve.test/bandiagara-songho",
            "sujet",
            "Le fleuve entre Bandiagara et Songho",
            "Bandiagara est séparée de Songho par 18 kilomètres de fleuve.",
        ),
        _page(
            "https://annuaire-fluvial.test/liaisons",
            "sujet",
            "Liaisons fluviales de la région",
            "La liaison Bandiagara – Songho couvre 18 kilomètres.",
        ),
    ]
)


INDEX: dict[str, list[str]] = {
    # Une requête générique ramène le bon et le mauvais, mélangés : c'est tout
    # l'intérêt du jeu.
    "tarif traversee pirogue": [
        "https://compagnie-bandiagara.test/tarifs",
        "https://vedettes-lacustres.test/tarifs",
        "https://guide-transport.test/pirogues",
        "https://traversees-du-delta.test/billets",
    ],
    "tarif officiel traversee vedette": [
        "https://vedettes-lacustres.test/tarifs",
        "https://traversees-du-delta.test/billets",
        "https://guide-transport.test/pirogues",
    ],
    "tarif traversee bandiagara songho": [
        "https://compagnie-bandiagara.test/tarifs",
        "https://office-tourisme-bandiagara.test/pirogues",
        "https://bandiagara-nord.test/bac",
    ],
    "tarif officiel bandiagara": [
        "https://compagnie-bandiagara.test/tarifs",
        "https://archives-transport.test/bandiagara-2014",
        "https://bandiagara-nord.test/bac",
    ],
    "horaire depart pirogue": [
        "https://blog-voyage-sahel.test/bandiagara",
        "https://guide-transport.test/pirogues",
        "https://vedettes-lacustres.test/tarifs",
    ],
    "horaire officiel autorite fluviale bandiagara": [
        "https://autorite-fluviale.test/horaires-bandiagara",
        "https://blog-voyage-sahel.test/bandiagara",
    ],
    "distance bandiagara songho": [
        "https://geo-fleuve.test/bandiagara-songho",
        "https://annuaire-fluvial.test/liaisons",
    ],
    "bandiagara histoire patrimoine": [
        "https://patrimoine-bandiagara.test/histoire",
    ],
}


def adversarial_corpus() -> Corpus:
    return Corpus(pages=dict(PAGES), index=dict(INDEX))


def label_of(url: str) -> str:
    return LABELS.get(url, "inconnu")


def is_on_topic_page(url: str) -> bool:
    return label_of(url) == "sujet"


TASKS: list[Task] = [
    Task(
        id="tarif_bandiagara",
        question="Combien coûte la traversée en pirogue entre Bandiagara et Songho ?",
        gold=[Gold("money", 3200, "3 200 francs")],
        distractors=[Gold("money", 9500, "9 500 francs (autre pays)"),
                     Gold("money", 1400, "1 400 francs (delta, autre liaison)"),
                     Gold("money", 900, "900 francs (archive 2014)")],
        family="piege",
        note="Le vocabulaire — traversée, pirogue, tarif — est partagé par des "
             "pages d'autres régions. Seul le nom du lieu distingue.",
        paraphrases=[
            "Quel est le prix de la traversée en pirogue de Bandiagara à Songho ?",
            "Combien faut-il payer pour traverser de Bandiagara vers Songho ?",
        ],
    ),
    Task(
        id="tarif_officiel_bandiagara",
        question="Quel est le tarif officiel de la traversée en pirogue entre Bandiagara et Songho ?",
        gold=[Gold("money", 3200, "3 200 francs")],
        distractors=[Gold("money", 9500, "9 500 francs (autre pays)"),
                     Gold("money", 900, "900 francs (archive 2014)"),
                     Gold("money", 700, "700 francs (Bandiagara-Nord)")],
        family="piege",
        note="Reproduit exactement la question qui a fait dérailler la "
             "baseline en conditions réelles : « tarif officiel » + deux noms "
             "de lieux + un vocabulaire très partagé.",
        paraphrases=[
            "Quel est le prix officiel de la traversée Bandiagara – Songho en pirogue ?",
            "Combien coûte officiellement la traversée en pirogue vers Songho ?",
        ],
    ),
    Task(
        id="horaire_bandiagara",
        question="À quelle heure part la pirogue de Bandiagara vers Songho ?",
        gold=[Gold("time", 6, "6 h du matin")],
        family="profond",
        note="Seule l'autorité fluviale répond ; blog et pages génériques "
             "parlent d'horaires sans jamais en donner.",
        paraphrases=[
            "Quel est l'horaire de départ de la pirogue de Bandiagara vers Songho ?",
            "La pirogue quitte Bandiagara à quelle heure pour Songho ?",
        ],
    ),
    Task(
        id="distance_bandiagara",
        question="Quelle distance sépare Bandiagara de Songho ?",
        gold=[Gold("distance", 18, "18 km")],
        family="facile",
        note="Deux sources concordantes, aucun piège — le banc doit aussi "
             "mesurer qu'on ne rejette pas tout.",
        paraphrases=[
            "Combien de kilomètres séparent Bandiagara de Songho ?",
            "Quelle est la distance entre Bandiagara et Songho ?",
        ],
    ),
]


__all__ = [
    "LABELS", "PAGES", "INDEX", "TASKS",
    "adversarial_corpus", "is_on_topic_page", "label_of",
]
