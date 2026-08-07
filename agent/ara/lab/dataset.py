"""Jeu de tâches du laboratoire, avec les réponses attendues (spec §18).

Chaque tâche porte une **vérité de référence** vérifiable par machine : une
grandeur chiffrée, avec son unité. C'est ce qui permet de mesurer une exactitude
sans jugement humain, donc de façon reproductible.

Trois familles, et la troisième est la plus importante :

* `facile` — la première recherche suffit. Chercher plus est du gaspillage :
  une stratégie adaptative qui s'acharne doit y **perdre**.
* `profond` — la réponse n'existe que sur une source précise, atteinte par une
  relance ciblée. Une stratégie à budget fixe doit y échouer.
* `piege` — chercher davantage ramène du bruit, une archive périmée ou une
  contradiction hors sujet. Ces tâches sont là **exprès**, pour donner à
  l'hypothèse une chance d'être réfutée.

⚠️ Ce jeu est petit et construit à la main. Il ne peut pas établir une loi
générale. Il peut en revanche **réfuter** : si la stratégie adaptative ne bat
pas la stratégie fixe ici, sur un terrain qu'on a soi-même préparé, alors
l'hypothèse est en mauvaise posture.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Gold:
    """Une valeur attendue dans la réponse."""

    kind: str        # money | duration | distance | weight | percent
    value: float     # valeur normalisée (minutes, km, kg…)
    label: str       # forme lisible, pour le rapport

    def to_dict(self) -> dict:
        return {"kind": self.kind, "value": self.value, "label": self.label}


@dataclass
class Task:
    """Une tâche du banc d'essai."""

    id: str
    question: str
    gold: list[Gold]
    family: str = "facile"        # facile | profond | piege
    note: str = ""
    #: valeurs qui NE doivent PAS être présentées comme la réponse
    distractors: list[Gold] = field(default_factory=list)
    #: reformulations de la même question, pour faire varier les exécutions
    #: d'une graine à l'autre. Les faits attendus, eux, ne changent jamais.
    paraphrases: list[str] = field(default_factory=list)

    def variants(self) -> list[str]:
        """Toutes les formulations possibles, l'originale en tête."""
        return [self.question, *self.paraphrases]

    def to_dict(self) -> dict:
        return {
            "id": self.id, "question": self.question, "family": self.family,
            "gold": [g.to_dict() for g in self.gold], "note": self.note,
            "variants": len(self.variants()),
        }


TASKS: list[Task] = [
    # --- famille « facile » : la première recherche suffit -------------------
    Task(
        id="tarif",
        question="Combien coûte le billet de la traversée entre Ouroveni et Hoani ?",
        gold=[Gold("money", 15000, "15 000 FC")],
        family="facile",
        note="Deux sources concordantes dès la première requête.",
        paraphrases=[
            "Quel est le tarif du billet pour la traversée Ouroveni – Hoani ?",
            "Combien faut-il payer pour aller d'Ouroveni à Hoani en vedette ?",
        ],
    ),
    Task(
        id="duree",
        question="Combien de temps dure la traversée entre Ouroveni et Hoani ?",
        gold=[Gold("duration", 180, "3 heures")],
        family="facile",
        note="Réponse présente sur les deux premières pages.",
        paraphrases=[
            "Quelle est la durée du trajet en vedette entre Ouroveni et Hoani ?",
            "Combien d'heures dure la traversée Ouroveni – Hoani ?",
        ],
    ),
    Task(
        id="distance",
        question="Quelle distance sépare la Grande Comore de Mohéli ?",
        gold=[Gold("distance", 70, "70 km")],
        family="facile",
        note="Deux sources indépendantes, aucune ambiguïté.",
        paraphrases=[
            "Combien de kilomètres y a-t-il entre la Grande Comore et Mohéli ?",
            "Quelle est la distance maritime Grande Comore – Mohéli ?",
        ],
    ),
    Task(
        id="hotel",
        question="Combien coûte une nuit d'hôtel aux Comores ?",
        gold=[Gold("money", 45000, "45 000 FC")],
        family="facile",
        note="Une seule page, mais elle répond directement.",
        paraphrases=[
            "Quel est le prix d'une nuit d'hôtel aux Comores ?",
            "Combien faut-il compter pour dormir une nuit à l'hôtel aux Comores ?",
        ],
    ),
    # --- famille « profond » : il faut relancer ------------------------------
    Task(
        id="horaire",
        question="À quelle heure part la vedette d'Ouroveni vers Hoani ?",
        gold=[Gold("time", 7, "7 h du matin")],
        family="profond",
        note="Blog et forum ne savent pas. Seule l'autorité maritime répond, "
             "et il faut une requête ciblée pour l'atteindre.",
        paraphrases=[
            "Quel est l'horaire de départ de la vedette Ouroveni vers Hoani ?",
            "À quelle heure la vedette quitte-t-elle Ouroveni pour Hoani ?",
        ],
    ),
    # --- famille « piège » : chercher plus peut nuire ------------------------
    Task(
        id="bagages",
        question="Quelle est la franchise bagages par passager ?",
        gold=[Gold("weight", 20, "20 kg")],
        family="piege",
        note="Une seule source la donne, et aucune autre ne la confirmera. "
             "Une stratégie qui relance pour confirmer dépense sans rien gagner.",
        paraphrases=[
            "Combien de kilos de bagages chaque passager peut-il emporter ?",
            "Quel poids de bagages est autorisé par passager à bord ?",
        ],
    ),
    Task(
        id="tarif_officiel",
        question="Quel est le prix officiel du billet de la traversée ?",
        gold=[Gold("money", 15000, "15 000 FC")],
        distractors=[Gold("money", 9000, "9 000 FC (archive 2019)"),
                     Gold("money", 25000, "25 000 FC (autre île)")],
        family="piege",
        note="Le mot « officiel » ramène une archive de 2019 et une autre "
             "liaison. Chercher plus expose à répondre faux.",
        paraphrases=[
            "Quel est le tarif officiel en vigueur pour le billet de la traversée ?",
            "Combien coûte officiellement le billet de la traversée aujourd'hui ?",
        ],
    ),
    Task(
        id="repas",
        question="Combien coûte un repas au restaurant du port ?",
        gold=[Gold("money", 6000, "6 000 FC")],
        family="piege",
        note="La page contient trois prix différents. Le risque est de "
             "retenir le mauvais.",
        paraphrases=[
            "Quel est le prix d'un repas au restaurant du port ?",
            "Combien faut-il payer pour manger au restaurant du port ?",
        ],
    ),
]


def by_family(family: str) -> list[Task]:
    return [task for task in TASKS if task.family == family]
