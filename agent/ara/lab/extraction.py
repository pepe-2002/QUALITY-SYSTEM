"""JEU 5 — banc d'essai de l'extracteur de faits, et son expérience.

Les jeux 1 à 4 mesuraient le comportement de l'agent. Celui-ci mesure une
brique : l'extracteur de grandeurs. Il est donc fait de phrases, pas de
tâches, et chaque phrase dit ce qu'il faut y trouver **et ce qu'il ne faut pas
y trouver**.

Ce second point est l'essentiel. Élargir la reconnaissance des devises est
facile ; le faire sans se mettre à voir de l'argent partout l'est moins. Un
extracteur qui prendrait « 42 000 habitants » pour une somme serait pire que
celui qu'on remplace.

Trois familles de cas :

* **devises** — celles que la version gelée connaissait, celles qu'elle
  ignorait, et les formes ambiguës ;
* **pièges** — nombres qui ne sont pas des montants, mots qui ressemblent à
  des devises sans en être, doubles comptages possibles ;
* **régressions** — phrases des jeux 1 à 4, dont le résultat ne doit pas
  changer d'un iota.

⚠️ Jeu écrit avant d'exécuter la version corrigée dessus. Même réserve que
partout : il est écrit par l'auteur du système.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..analysis.facts import extract_facts, extractor


@dataclass
class Case:
    """Une phrase, ce qu'il faut y lire, ce qu'il ne faut pas y lire."""

    id: str
    text: str
    #: (famille, valeur) attendus
    expected: list[tuple[str, float]] = field(default_factory=list)
    #: (famille, valeur) qui ne doivent PAS être produits
    forbidden: list[tuple[str, float]] = field(default_factory=list)
    family: str = "devise"      # devise | piege | regression
    note: str = ""


CASES: list[Case] = [
    # --- devises déjà connues de la version gelée ---------------------------
    Case("kmf", "Le billet coûte 15 000 francs comoriens.",
         [("money", 15000)], family="regression",
         note="Doit rester identique : c'est la devise des jeux 1 à 3."),
    Case("eur", "L'entrée est à 12 euros par personne.", [("money", 12)]),
    Case("usd", "Le transfert revient à 45 dollars US.", [("money", 45)]),
    Case("mga", "Le trajet coûte 8 000 ariary.", [("money", 8000)]),

    # --- devises que la version gelée ignorait ------------------------------
    Case("franc_nu", "La traversée en pirogue coûte 3 200 francs.",
         [("money", 3200)],
         note="Le cas exact trouvé par le diagnostic : dix pannes sur dix."),
    Case("cfa", "Le sac de riz vaut 12 500 francs CFA.", [("money", 12500)]),
    Case("fcfa", "Le transport coûte 7 000 FCFA.", [("money", 7000)]),
    Case("chf", "La nuit d'hôtel est à 180 francs suisses.", [("money", 180)]),
    Case("gbp", "Le billet coûte 40 livres sterling.", [("money", 40)]),
    Case("shilling", "La course revient à 2 500 shillings.", [("money", 2500)]),
    Case("rand", "L'entrée du parc coûte 350 rands.", [("money", 350)]),
    Case("dirham", "La chambre est à 600 dirhams la nuit.", [("money", 600)]),
    Case("naira", "Le sac coûte 4 500 nairas.", [("money", 4500)]),
    Case("roupie", "Le trajet en train vaut 900 roupies.", [("money", 900)]),
    Case("symbole_livre", "Le supplément est de 15 £.", [("money", 15)]),

    # --- pièges : ne pas voir de l'argent partout ---------------------------
    Case("habitants", "L'île compte 42 000 habitants.", [],
         [("money", 42000)], family="piege",
         note="Un grand nombre n'est pas un montant."),
    Case("annee", "La liaison existe depuis 1974.", [],
         [("money", 1974)], family="piege",
         note="Une année reste une année."),
    Case("livre_objet", "La bibliothèque contient 3 000 livres.", [],
         [("money", 3000)], family="piege",
         note="« livre » sans « sterling » désigne un ouvrage ou une masse."),
    Case("kilos", "Le colis pèse 25 kilogrammes.", [("weight", 25)],
         [("money", 25)], family="piege"),
    Case("pourcentage", "Le rendement atteint 20 pour cent.", [("percent", 20)],
         [("money", 20)], family="piege"),
    Case("sans_unite", "Il y a 17 sièges à bord.", [],
         [("money", 17)], family="piege"),

    # --- pièges de double comptage -----------------------------------------
    Case("pas_de_double_kmf", "Le billet coûte 15 000 francs comoriens.",
         [("money", 15000)], family="piege",
         note="« francs » générique ne doit pas recompter un franc déjà "
              "qualifié : sinon la même somme apparaîtrait deux fois."),
    Case("pas_de_double_cfa", "Le sac vaut 12 500 francs CFA.",
         [("money", 12500)], family="piege"),

    # --- régressions : phrases des jeux existants ---------------------------
    Case("regression_duree", "La traversée dure environ 3 heures.",
         [("duration", 180)], family="regression"),
    Case("regression_distance", "L'île est à 70 kilomètres de la côte.",
         [("distance", 70)], family="regression"),
    Case("regression_heure", "Le départ est fixé à 7 heures du matin.",
         [("time", 7)], family="regression"),
    Case("regression_fourchette",
         "Comptez entre 15 000 et 17 500 francs comoriens.",
         [("money", 15000)], family="regression",
         note="Une fourchette reste un seul fait, pas deux valeurs opposées."),
]


TOLERANCE = 0.02


def _found(facts, kind: str, value: float) -> bool:
    marge = abs(value) * TOLERANCE
    return any(
        f.kind == kind and (f.low - marge) <= value <= (f.high + marge)
        for f in facts
    )


@dataclass
class VersionScore:
    version: str
    found: int = 0
    expected: int = 0
    false_positives: int = 0
    duplicates: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def recall(self) -> float:
        return self.found / self.expected if self.expected else 0.0

    def to_dict(self) -> dict:
        return {
            "version": self.version, "found": self.found,
            "expected": self.expected, "recall": round(self.recall, 3),
            "false_positives": self.false_positives,
            "duplicates": self.duplicates, "failures": self.failures,
        }


def evaluate(version: str, cases: list[Case] | None = None) -> VersionScore:
    """Passe une version de l'extracteur sur le jeu 5."""
    cases = cases or CASES
    note = VersionScore(version=version)

    with extractor(version):
        for case in cases:
            facts = extract_facts(case.text, 1, max_facts=50)

            for kind, value in case.expected:
                note.expected += 1
                if _found(facts, kind, value):
                    note.found += 1
                else:
                    note.failures.append(f"{case.id} : {kind} {value:g} non trouvé")

            for kind, value in case.forbidden:
                if _found(facts, kind, value):
                    note.false_positives += 1
                    note.failures.append(
                        f"{case.id} : {kind} {value:g} trouvé à tort"
                    )

            # Double comptage : la même valeur relevée deux fois dans la même
            # phrase, sous deux unités différentes.
            for kind, value in case.expected:
                doublons = [
                    f for f in facts
                    if f.kind == kind and abs(f.low - value) <= abs(value) * TOLERANCE
                ]
                if len(doublons) > 1:
                    note.duplicates += len(doublons) - 1
                    note.failures.append(
                        f"{case.id} : {value:g} compté {len(doublons)} fois "
                        f"({', '.join(sorted({f.unit for f in doublons}))})"
                    )
    return note


def compare_versions() -> dict[str, VersionScore]:
    return {version: evaluate(version) for version in ("baseline", "v2")}


def by_family(family: str) -> list[Case]:
    return [case for case in CASES if case.family == family]


__all__ = ["CASES", "Case", "VersionScore", "by_family", "compare_versions", "evaluate"]
