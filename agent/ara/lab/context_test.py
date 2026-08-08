"""JEU 7 — jeu de test indépendant de CONTEXT-V2. Écrit avant son exécution.

Ni les quatre jeux d'agent, ni le jeu 5, ni le jeu 6 ne servent ici : ce
mécanisme-ci juge le **rattachement d'une information à un contexte**, et
demande donc ses propres cas.

Univers volontairement neuf — une école de musique, des instruments, des
villes homonymes — pour qu'aucun mot des jeux précédents ne puisse porter le
résultat.

Les neuf familles demandées, chacune tirée d'un mode d'erreur réel :

===========================  =======================================
même produit, autre pays      un prix juste, ailleurs
même nom, autre lieu          deux villes homonymes
ancien prix / prix actuel     l'archive contre l'édition courante
plusieurs tarifs sur la page  choisir parmi trois montants
plusieurs devises             le montant est bon, la devise autre
services similaires           cours collectif contre cours individuel
autre objet                   bon vendeur, mauvais instrument
information historique        vraie, mais d'un autre siècle
géographiquement proche       la commune voisine
===========================  =======================================

Chaque cas déclare ce qui devrait être **affirmable** — et non l'état exact
attendu. Exiger l'état exact reviendrait à noter la mécanique interne plutôt
que ce qui compte : cette information a-t-elle le droit de devenir la réponse ?
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..analysis.context_v2 import assess_context

ANNEE = 2026


@dataclass
class ContextCase:
    id: str
    question: str
    sentence: str
    title: str = ""
    document: str = ""
    #: cette information a-t-elle le droit de devenir la réponse ?
    assertable: bool = True
    family: str = "sujet"
    note: str = ""

    @property
    def text(self) -> str:
        return self.document or self.sentence


CASES: list[ContextCase] = [
    # --- informations correctes, à conserver --------------------------------
    ContextCase(
        "juste_simple",
        "Combien coûte une guitare classique à l'école de Vaudreuil ?",
        "La guitare classique est vendue 240 euros à l'école de Vaudreuil.",
        title="École de musique de Vaudreuil — tarifs",
        assertable=True, family="sujet",
    ),
    ContextCase(
        "juste_document",
        "Combien coûte une guitare classique à l'école de Vaudreuil ?",
        "La guitare classique est vendue 240 euros.",
        title="École de musique de Vaudreuil",
        document="École de musique de Vaudreuil — catalogue des instruments. "
                 "La guitare classique est vendue 240 euros.",
        assertable=True, family="sujet",
        note="Le lieu est nommé dans le document, pas dans la phrase.",
    ),
    ContextCase(
        "juste_edition_courante",
        "Quel est le tarif actuel du cours de piano à Vaudreuil ?",
        "Le cours de piano coûte 45 euros la séance à Vaudreuil.",
        title="Tarifs 2026 — école de Vaudreuil",
        assertable=True, family="sujet",
    ),

    # --- même produit, autre pays -------------------------------------------
    ContextCase(
        "autre_pays",
        "Combien coûte une guitare classique à l'école de Vaudreuil ?",
        "La guitare classique est vendue 180 euros dans nos ateliers de Berlin.",
        title="Atelier de lutherie de Berlin",
        assertable=False, family="autre_pays",
    ),

    # --- même nom, autre lieu ------------------------------------------------
    ContextCase(
        "homonyme",
        "Quel est le tarif du cours de piano à Vaudreuil-sur-Mer ?",
        "Le cours de piano coûte 30 euros à Vaudreuil-les-Bois.",
        title="École municipale de Vaudreuil-les-Bois",
        assertable=False, family="homonyme",
        note="Deux communes qui partagent un nom : le cas le plus difficile, "
             "et celui que RESEARCH-V2 ne résout pas non plus.",
    ),

    # --- ancien prix / prix actuel -------------------------------------------
    ContextCase(
        "archive_declaree",
        "Quel est le tarif actuel du cours de piano à Vaudreuil ?",
        "En 2018, le cours de piano coûtait 28 euros la séance à Vaudreuil.",
        title="Tarifs 2018 — archive",
        assertable=False, family="archive",
    ),
    ContextCase(
        "passe_sans_mot_archive",
        "Quel est le tarif actuel du cours de piano à Vaudreuil ?",
        "En 2017, la séance de piano valait 25 euros à Vaudreuil.",
        title="Rétrospective des tarifs",
        assertable=False, family="archive",
        note="Aucun mot « archive » : c'est le temps du verbe et l'année qui "
             "doivent suffire.",
    ),
    ContextCase(
        "annee_courante_ok",
        "Quel est le tarif actuel du cours de piano à Vaudreuil ?",
        "Depuis 2026, le cours de piano coûte 45 euros la séance à Vaudreuil.",
        title="Tarifs en vigueur — Vaudreuil",
        assertable=True, family="archive",
        note="Une année récente ne doit pas déclencher le rejet.",
    ),

    # --- plusieurs tarifs sur une même page ----------------------------------
    ContextCase(
        "page_multi_tarifs_bon",
        "Combien coûte le cours de piano à Vaudreuil ?",
        "Le cours de piano coûte 45 euros la séance.",
        title="École de Vaudreuil — grille tarifaire",
        document="École de Vaudreuil — grille tarifaire. Le cours de piano "
                 "coûte 45 euros la séance. La location de salle est de "
                 "120 euros. L'adhésion annuelle vaut 60 euros.",
        assertable=True, family="multi_tarifs",
    ),
    ContextCase(
        "page_multi_tarifs_mauvais",
        "Combien coûte le cours de piano à Vaudreuil ?",
        "La location de salle est de 120 euros.",
        title="École de Vaudreuil — grille tarifaire",
        document="École de Vaudreuil — grille tarifaire. Le cours de piano "
                 "coûte 45 euros la séance. La location de salle est de "
                 "120 euros.",
        assertable=False, family="multi_tarifs",
        note="Même page, bon lieu, mauvais objet.",
    ),

    # --- plusieurs devises ---------------------------------------------------
    ContextCase(
        "devise_autre",
        "Combien coûte une guitare classique à l'école de Vaudreuil ?",
        "La guitare classique est vendue 240 francs suisses à Lausanne.",
        title="Lutherie de Lausanne",
        assertable=False, family="devises",
        note="Le nombre est le même ; ni le lieu ni la devise ne le sont.",
    ),

    # --- services similaires -------------------------------------------------
    ContextCase(
        "service_voisin",
        "Combien coûte le cours individuel de piano à Vaudreuil ?",
        "Le cours collectif de solfège coûte 18 euros à Vaudreuil.",
        title="École de Vaudreuil",
        assertable=False, family="services",
    ),

    # --- autre objet ---------------------------------------------------------
    ContextCase(
        "autre_instrument",
        "Combien coûte une guitare classique à l'école de Vaudreuil ?",
        "Le violon d'étude est vendu 310 euros à l'école de Vaudreuil.",
        title="École de Vaudreuil — catalogue",
        assertable=False, family="autre_objet",
        note="Bon vendeur, bon lieu, mauvais instrument.",
    ),

    # --- information historique ---------------------------------------------
    ContextCase(
        "historique",
        "Combien coûte une guitare classique à l'école de Vaudreuil ?",
        "En 1908, une guitare d'atelier valait 40 francs à Vaudreuil.",
        title="Histoire de la lutherie à Vaudreuil",
        assertable=False, family="historique",
    ),

    # --- géographiquement proche mais incorrect ------------------------------
    ContextCase(
        "commune_voisine",
        "Combien coûte le cours de piano à Vaudreuil ?",
        "Le cours de piano coûte 38 euros à Sainte-Colombe, commune voisine.",
        title="École intercommunale de Sainte-Colombe",
        assertable=False, family="proche",
    ),
]


@dataclass
class ContextScore:
    """Ce qu'une version conserve, rejette, et rejette à tort."""

    version: str
    kept_good: int = 0
    rejected_bad: int = 0
    false_rejects: int = 0
    missed_bad: int = 0
    by_family: dict[str, int] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    @property
    def total_good(self) -> int:
        return self.kept_good + self.false_rejects

    @property
    def total_bad(self) -> int:
        return self.rejected_bad + self.missed_bad

    @property
    def recall_good(self) -> float:
        return self.kept_good / self.total_good if self.total_good else 0.0

    @property
    def rejection_rate(self) -> float:
        return self.rejected_bad / self.total_bad if self.total_bad else 0.0

    @property
    def accuracy(self) -> float:
        total = self.total_good + self.total_bad
        return (self.kept_good + self.rejected_bad) / total if total else 0.0

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "kept_good": self.kept_good, "false_rejects": self.false_rejects,
            "rejected_bad": self.rejected_bad, "missed_bad": self.missed_bad,
            "recall_good": round(self.recall_good, 3),
            "rejection_rate": round(self.rejection_rate, 3),
            "accuracy": round(self.accuracy, 3),
            "by_family": self.by_family, "failures": self.failures,
        }


def evaluate(version: str, cases: list[ContextCase] | None = None) -> ContextScore:
    """Passe une version sur le jeu 7.

    ``baseline`` n'est pas un mécanisme : c'est l'absence de mécanisme. Le
    système actuel n'examine pas le contexte d'un fait avant de l'utiliser —
    tout est donc affirmable. C'est exactement ce que l'autopsie a mesuré.
    """
    cases = cases or CASES
    note = ContextScore(version=version)

    for case in cases:
        if version == "baseline":
            affirmable = True
        else:
            affirmable = assess_context(
                question=case.question, sentence=case.sentence,
                document=case.text, title=case.title, now=ANNEE,
            ).assertable

        if case.assertable and affirmable:
            note.kept_good += 1
        elif case.assertable and not affirmable:
            note.false_rejects += 1
            note.failures.append(f"{case.id} : bonne information rejetée")
            note.by_family[case.family] = note.by_family.get(case.family, 0) + 1
        elif not case.assertable and not affirmable:
            note.rejected_bad += 1
        else:
            note.missed_bad += 1
            note.failures.append(f"{case.id} : mauvaise information conservée")
            note.by_family[case.family] = note.by_family.get(case.family, 0) + 1

    return note


def compare() -> dict[str, ContextScore]:
    return {version: evaluate(version) for version in ("baseline", "v2")}


__all__ = ["ANNEE", "CASES", "ContextCase", "ContextScore", "compare", "evaluate"]
