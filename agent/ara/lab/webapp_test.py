"""JEU 10 — jeu de test indépendant pour H3 (mémoire des défauts web).

Écrit **avant** toute exécution, comme les neuf précédents. Le développement du
studio web s'est fait sur trois briefs jetables (traversées, réservations,
location de barques) avec une marque volontairement terne ; aucun de ces
briefs ne figure ici.

Ce que ce jeu doit contenir pour être honnête
---------------------------------------------
* des marques **variées** : certaines bien contrastées, d'autres non. Si toutes
  étaient fautives, la mémoire n'aurait qu'une leçon à apprendre et le résultat
  serait truqué par construction ;
* des briefs **avec** matière et des briefs **sans** : le défaut de bouche-trou
  ne doit pas apparaître partout ;
* des types différents (vitrine, landing, app, portfolio) ;
* deux briefs sans aucun défaut attendu — s'ils en révèlent un, tant mieux :
  cela voudra dire que le critique mesure quelque chose que je n'avais pas vu.

Ce jeu ne juge qu'une fois. Après H3, il devient un jeu de développement.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..design.brand import BrandProfile


@dataclass
class WebCase:
    """Un brief, sa marque, sa matière."""

    id: str
    brief: str
    palette: list[str]
    material: list[str] = field(default_factory=list)
    avoid: list[str] = field(default_factory=list)
    kind: str = ""
    note: str = ""

    def brand(self) -> BrandProfile:
        return BrandProfile(name=self.id, palette=list(self.palette),
                            avoid=list(self.avoid))


#: Palettes nommées, pour lire le jeu sans compter les codes hexadécimaux.
#: L'ordre d'une palette est [dominante, secondaire, accent, papier, encre] ;
#: le site prend l'encre comme fond, le papier comme texte.
LISIBLE = ["#0a2550", "#1b6ca8", "#facc15", "#f7fafc", "#0b1220"]
TERNE = ["#3a3f4a", "#40454f", "#4a5060", "#5a6070", "#606878"]
PALOTE = ["#e9e4d8", "#dcd6c6", "#efe9dc", "#f6f3ec", "#eae5d9"]

CASES: list[WebCase] = [
    WebCase(
        "marche_couvert", "Crée un site vitrine pour le marché couvert de Fomboni",
        LISIBLE,
        material=[
            "Le marché ouvre du lundi au samedi, de 6 h à 13 h.",
            "Une trentaine d'étals proposent poisson, fruits et épices.",
            "Le stationnement est gratuit sur la place adjacente.",
        ],
        note="Cas propre : marque lisible, matière complète. Aucun défaut attendu.",
    ),
    WebCase(
        "atelier_couture", "Fais un site vitrine pour un atelier de couture",
        TERNE,
        material=["L'atelier réalise retouches et pièces sur mesure."],
        note="Contraste fautif + matière incomplète : deux défauts.",
    ),
    WebCase(
        "taxi_brousse", "Crée une landing page pour un service de taxi-brousse",
        TERNE,
        note="Contraste fautif, aucune matière.",
    ),
    WebCase(
        "photographe", "Fais un portfolio pour un photographe de mariage",
        LISIBLE,
        material=[
            "Reportages complets, de la préparation à la soirée.",
            "Les photos sont livrées retouchées sous trois semaines.",
        ],
        note="Marque lisible, matière pour deux sections sur trois.",
    ),
    WebCase(
        "carnet_peche", "Crée une application installable pour tenir un carnet de pêche",
        PALOTE,
        material=[
            "Chaque sortie enregistre la date, le lieu et les prises.",
            "Les données restent sur le téléphone, sans compte à créer.",
            "L'application fonctionne sans réseau, en mer comme au port.",
        ],
        note="Palette pâle : le contraste doit échouer sur presque tout.",
    ),
    WebCase(
        "boulangerie", "Fais un site vitrine pour une boulangerie 🥐 artisanale",
        LISIBLE,
        material=["Le pain est cuit deux fois par jour, au levain naturel."],
        avoid=["pas d'emojis dans les textes publiés"],
        note="Emoji dans le brief + interdit de marque décidable.",
    ),
    WebCase(
        "location_velos", "Crée une landing page pour la location de vélos",
        PALOTE,
        material=[
            "Vélos à assistance électrique, de 9 h à 19 h.",
            "Casque et antivol fournis avec chaque location.",
            "Réservation la veille conseillée en haute saison.",
        ],
        note="Palette pâle, matière complète : un seul défaut attendu.",
    ),
    WebCase(
        "cabinet_infirmier", "Fais un site vitrine pour un cabinet infirmier",
        LISIBLE,
        material=[
            "Soins à domicile sept jours sur sept, sur prescription.",
            "Le cabinet reçoit sans rendez-vous de 7 h à 9 h.",
            "Les déplacements couvrent la commune et ses hameaux.",
        ],
        avoid=["ne jamais écrire « urgences » : le cabinet n'en assure pas"],
        note="Deuxième cas propre, avec un interdit qui ne doit pas se déclencher.",
    ),
    WebCase(
        "ecole_voile", "Crée une application web pour les inscriptions à l'école de voile",
        TERNE,
        material=["Les stages durent cinq demi-journées, du lundi au vendredi."],
        note="Application installable + contraste fautif + matière partielle.",
    ),
    WebCase(
        "epicerie_ligne", "Fais un site vitrine pour une épicerie",
        PALOTE,
        material=[
            "Voir le catalogue complet sur https://exemple.test/catalogue",
            "Livraison le mardi et le vendredi dans le centre.",
        ],
        note="Une adresse dans la matière : le site doit rester autonome.",
    ),
]


__all__ = ["CASES", "LISIBLE", "PALOTE", "TERNE", "WebCase"]
