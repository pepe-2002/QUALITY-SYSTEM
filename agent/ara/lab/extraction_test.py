"""JEU 6 — jeu de test indépendant d'EXTRACTION-V2. Jamais utilisé auparavant.

Le jeu 5 (`extraction.py`) a servi à développer : ses cas ont été relus,
ajustés, rejoués. Il ne peut donc plus juger. Celui-ci est écrit **avant** la
première exécution de la version corrigée dessus, dans un autre univers
lexical — pas de traversées, pas de Comores — et il n'a servi à calibrer
aucun seuil.

Ce qu'il mesure, et que le jeu 5 ne mesurait pas : la **devise** attendue et
la **confiance** attendue. Extraire 3 200 est une chose ; savoir si c'est un
franc CFA, un franc suisse ou une devise indéterminée en est une autre, et
c'est là que se joue la correction demandée.

Six familles de cas :

* ``ecrite`` — la devise est écrite : confiance certaine exigée ;
* ``deduite`` — elle se déduit du contexte : confiance probable exigée ;
* ``indeterminee`` — rien ne permet de trancher : ``UNKNOWN`` exigé ;
* ``conversion`` — deux montants, deux devises : ne pas mélanger ;
* ``multi`` — plusieurs devises dans le document ;
* ``piege`` — nombres qui ne sont pas des montants.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..analysis.currency import UNKNOWN
from ..analysis.facts import extract_facts, extractor


@dataclass
class CurrencyCase:
    """Un texte, et ce que l'extracteur doit en tirer — devise comprise."""

    id: str
    text: str
    #: (valeur, devise attendue, confiance attendue)
    expected: list[tuple[float, str, str]] = field(default_factory=list)
    #: valeurs qui ne doivent pas être relevées comme montants
    forbidden: list[float] = field(default_factory=list)
    family: str = "ecrite"
    note: str = ""


CASES: list[CurrencyCase] = [
    # --- devise écrite → certaine -------------------------------------------
    CurrencyCase("ecrite_xof", "L'inscription au club coûte 25 000 francs CFA.",
                 [(25000, "XOF", "certaine")]),
    CurrencyCase("ecrite_chf", "La licence annuelle vaut 240 francs suisses.",
                 [(240, "CHF", "certaine")]),
    CurrencyCase("ecrite_eur", "Le maillot est vendu 55 euros.",
                 [(55, "EUR", "certaine")]),
    CurrencyCase("ecrite_usd", "Le stage revient à 320 dollars.",
                 [(320, "USD", "certaine")]),
    CurrencyCase("ecrite_gbp", "L'abonnement coûte 30 livres sterling.",
                 [(30, "GBP", "certaine")]),
    CurrencyCase("ecrite_mga", "Le transport coûte 18 000 ariary.",
                 [(18000, "MGA", "certaine")]),

    # --- devise déduite → probable ------------------------------------------
    CurrencyCase("deduite_lieu_xof",
                 "À Dakar, la cotisation du club s'élève à 25 000 francs.",
                 [(25000, "XOF", "probable")], family="deduite",
                 note="Le lieu ne laisse qu'une zone monétaire possible."),
    CurrencyCase("deduite_lieu_chf",
                 "À Lausanne, la licence coûte 240 francs.",
                 [(240, "CHF", "probable")], family="deduite"),
    CurrencyCase("deduite_phrase",
                 "La licence vaut 240 francs suisses et le maillot 60 francs.",
                 [(240, "CHF", "certaine"), (60, "CHF", "probable")],
                 family="deduite",
                 note="La devise du premier montant éclaire le second."),
    CurrencyCase("deduite_adjectif",
                 "La cotisation malgache est de 18 000 francs.",
                 [(18000, "MGA", "probable")], family="deduite"),

    # --- rien pour trancher → UNKNOWN ---------------------------------------
    CurrencyCase("indetermine_nu", "La cotisation s'élève à 25 000 francs.",
                 [(25000, UNKNOWN, "inconnue")], family="indeterminee",
                 note="Le cas le plus important : ne pas deviner."),
    CurrencyCase("indetermine_court", "Prix : 900 francs.",
                 [(900, UNKNOWN, "inconnue")], family="indeterminee"),

    # --- conversions : ne pas mélanger --------------------------------------
    CurrencyCase("conversion_soit",
                 "La licence coûte 240 francs, soit environ 250 euros.",
                 [(250, "EUR", "certaine"), (240, UNKNOWN, "inconnue")],
                 family="conversion",
                 note="La devise écrite appartient à l'autre montant."),
    CurrencyCase("conversion_contre",
                 "Le stage revient à 25 000 francs, contre 40 dollars ailleurs.",
                 [(40, "USD", "certaine"), (25000, UNKNOWN, "inconnue")],
                 family="conversion"),

    # --- plusieurs devises dans le document ---------------------------------
    CurrencyCase("multi_devises",
                 "Tarifs du tournoi. L'inscription est de 55 euros en France. "
                 "Le stage coûte 320 dollars au Canada. La cotisation locale "
                 "s'élève à 25 000 francs.",
                 [(55, "EUR", "certaine"), (320, "USD", "certaine"),
                  (25000, UNKNOWN, "inconnue")],
                 family="multi",
                 note="Deux devises nommées : le montant nu reste indéterminé."),

    # --- pièges : ce qui n'est pas un montant --------------------------------
    CurrencyCase("piege_membres", "Le club compte 25 000 membres.",
                 [], [25000], family="piege"),
    CurrencyCase("piege_annee", "Le club a été fondé en 1932.",
                 [], [1932], family="piege"),
    CurrencyCase("piege_livres", "La bibliothèque du club contient 900 livres.",
                 [], [900], family="piege"),
    CurrencyCase("piege_poids", "Le matériel pèse 240 kilogrammes.",
                 [], [240], family="piege"),
]


TOLERANCE = 0.02


@dataclass
class CurrencyScore:
    """Ce qu'une version d'extracteur réussit et rate sur le jeu 6."""

    version: str
    amounts_expected: int = 0
    amounts_found: int = 0
    currencies_correct: int = 0
    currencies_wrong: int = 0
    confidence_correct: int = 0
    false_positives: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def amount_recall(self) -> float:
        return self.amounts_found / self.amounts_expected if self.amounts_expected else 0.0

    @property
    def currency_accuracy(self) -> float:
        return self.currencies_correct / self.amounts_found if self.amounts_found else 0.0

    @property
    def confidence_accuracy(self) -> float:
        return self.confidence_correct / self.amounts_found if self.amounts_found else 0.0

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "amounts_expected": self.amounts_expected,
            "amounts_found": self.amounts_found,
            "amount_recall": round(self.amount_recall, 3),
            "currencies_correct": self.currencies_correct,
            "currencies_wrong": self.currencies_wrong,
            "currency_accuracy": round(self.currency_accuracy, 3),
            "confidence_accuracy": round(self.confidence_accuracy, 3),
            "false_positives": self.false_positives,
            "failures": self.failures,
        }


def evaluate(version: str, cases: list[CurrencyCase] | None = None) -> CurrencyScore:
    """Passe une version de l'extracteur sur le jeu 6."""
    cases = cases or CASES
    note = CurrencyScore(version=version)

    with extractor(version):
        for case in cases:
            faits = [f for f in extract_facts(case.text, 1, max_facts=50)
                     if f.kind == "money"]

            for valeur, devise, confiance in case.expected:
                note.amounts_expected += 1
                marge = abs(valeur) * TOLERANCE
                trouve = next(
                    (f for f in faits if (f.low - marge) <= valeur <= (f.high + marge)),
                    None,
                )
                if trouve is None:
                    note.failures.append(f"{case.id} : {valeur:g} non extrait")
                    continue
                note.amounts_found += 1
                if trouve.unit == devise:
                    note.currencies_correct += 1
                else:
                    note.currencies_wrong += 1
                    note.failures.append(
                        f"{case.id} : {valeur:g} → {trouve.unit} au lieu de {devise}"
                    )
                if getattr(trouve, "confidence", "certaine") == confiance:
                    note.confidence_correct += 1
                else:
                    note.failures.append(
                        f"{case.id} : {valeur:g} confiance "
                        f"{getattr(trouve, 'confidence', '?')} au lieu de {confiance}"
                    )

            for valeur in case.forbidden:
                marge = abs(valeur) * TOLERANCE
                if any((f.low - marge) <= valeur <= (f.high + marge) for f in faits):
                    note.false_positives += 1
                    note.failures.append(f"{case.id} : {valeur:g} pris pour un montant")

    return note


def compare() -> dict[str, CurrencyScore]:
    return {version: evaluate(version) for version in ("baseline", "v2")}


def by_family(family: str) -> list[CurrencyCase]:
    return [case for case in CASES if case.family == family]


__all__ = ["CASES", "CurrencyCase", "CurrencyScore", "by_family", "compare", "evaluate"]
