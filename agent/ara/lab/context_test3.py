"""JEU 9 — jeu de test indépendant de CONTEXT-V4. Écrit avant son exécution.

Les jeux 7 et 8 avaient un défaut commun, découvert seulement en mesurant
l'effet de bout en bout : **leurs phrases étaient autoportantes**. Elles
nommaient le lieu, l'objet et la période, ce que les vraies pages ne font
pas. V3 y obtenait 94 % et bloquait un quart des bonnes réponses en
production.

Le jeu 9 corrige ce biais dans sa construction même. Sur ses dix cas
corrects, **sept sont des phrases avares** — elles ne répètent ni le lieu, ni
l'objet, ni les deux, exactement comme une vraie page de tarifs. C'est le
seul moyen de mesurer si V4 tient sa promesse : ne bloquer que sur preuve.

Univers neuf : un port de plaisance, ses services, ses communes. Aucun mot des
huit jeux précédents.

Les pièges, eux, portent tous une **preuve positive** de contexte étranger :
un autre lieu nommé, un autre objet nommé, une date révolue. Un piège muet —
qui ne dirait rien de compromettant — passerait, et c'est assumé : V4 le
laisse au reste de la chaîne.
"""

from __future__ import annotations

from .context_test import ContextCase, ContextScore

ANNEE = 2026

CASES: list[ContextCase] = [
    # === CORRECTS — phrases avares, comme les vraies pages ==================
    ContextCase(
        "avare_sans_lieu",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un voilier est facturée 320 euros par mois.",
        title="Port de Kerlouan — tarifs",
        document="Port de Kerlouan — tarifs. La place pour un voilier est "
                 "facturée 320 euros par mois.",
        assertable=True, family="avare",
        note="Le lieu n'est que dans le titre. C'est le cas « franchise "
             "bagages » qui faisait échouer V3 en production.",
    ),
    ContextCase(
        "avare_sans_objet",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "Le tarif mensuel s'élève à 320 euros à Kerlouan.",
        title="Port de Kerlouan — voiliers",
        document="Port de Kerlouan — voiliers. Le tarif mensuel s'élève à "
                 "320 euros à Kerlouan.",
        assertable=True, family="avare",
    ),
    ContextCase(
        "avare_ni_lieu_ni_objet",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "Comptez 320 euros par mois.",
        title="Port de Kerlouan — tarifs des voiliers",
        document="Port de Kerlouan — tarifs des voiliers. Comptez 320 euros "
                 "par mois. Le règlement est affiché à la capitainerie.",
        assertable=True, family="avare",
        note="Le cas extrême : la phrase ne dit rien du contexte. La source, si.",
    ),
    ContextCase(
        "avare_pronom",
        "Combien coûte le carénage au port de Kerlouan ?",
        "Il revient à 145 euros pour une coque de moins de huit mètres.",
        title="Port de Kerlouan — carénage",
        document="Port de Kerlouan — carénage. Il revient à 145 euros pour une "
                 "coque de moins de huit mètres.",
        assertable=True, family="avare",
        note="Un pronom à la place de l'objet : fréquent, et illisible pour un "
             "contrôle qui exige la répétition.",
    ),
    ContextCase(
        "avare_abreviation",
        "Combien coûte une place au port de Kerlouan-sur-Mer pour un voilier ?",
        "La place pour un voilier coûte 320 euros par mois à Kerlouan.",
        title="Port de Kerlouan",
        assertable=True, family="avare",
        note="La source abrège le nom composé. C'est le faux rejet que le jeu 8 "
             "avait attrapé sur V3.",
    ),
    ContextCase(
        "avare_vocabulaire_voisin",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un voilier est à 320 euros par mois, ponton compris, "
        "électricité et eau incluses.",
        title="Port de Kerlouan",
        assertable=True, family="avare",
        note="« ponton », « électricité », « eau » ne sont pas des objets "
             "concurrents : ce sont des circonstances.",
    ),
    ContextCase(
        "avare_annee_courante",
        "Quel est le tarif actuel de la place au port de Kerlouan ?",
        "Depuis 2026, la place revient à 320 euros par mois.",
        title="Port de Kerlouan — tarifs en vigueur",
        assertable=True, family="avare",
    ),
    ContextCase(
        "explicite_complet",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un voilier au port de Kerlouan coûte 320 euros par mois.",
        title="Port de Kerlouan — tarifs",
        assertable=True, family="sujet",
    ),
    ContextCase(
        "sans_nom_propre",
        "Combien coûte le carénage d'un voilier ?",
        "Le carénage d'un voilier revient à 145 euros.",
        title="Tarifs des services portuaires",
        assertable=True, family="sans_nom_propre",
    ),
    ContextCase(
        "question_avec_deux_objets",
        "Combien coûtent la place et le carénage au port de Kerlouan ?",
        "La place revient à 320 euros par mois au port de Kerlouan.",
        title="Port de Kerlouan — tarifs",
        assertable=True, family="sujet",
        note="Deux objets demandés, un seul nommé : ce n'est pas une "
             "contradiction.",
    ),

    # === PIÈGES — chacun porte une preuve positive =========================
    ContextCase(
        "lieu_concurrent",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un voilier coûte 260 euros par mois au port de Plouescat.",
        title="Port de Plouescat — tarifs",
        assertable=False, family="autre_lieu",
    ),
    ContextCase(
        "homonyme_qualifie",
        "Combien coûte une place au port de Kerlouan-sur-Mer ?",
        "La place coûte 210 euros par mois à Kerlouan-en-Terre.",
        title="Port de Kerlouan-en-Terre",
        assertable=False, family="homonyme",
        note="Deux qualificatifs présents et différents : c'est un conflit, "
             "pas une abréviation.",
    ),
    ContextCase(
        "objet_concurrent",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un chalutier coûte 780 euros par mois au port de Kerlouan.",
        title="Port de Kerlouan — pêche professionnelle",
        assertable=False, family="autre_objet",
    ),
    ContextCase(
        "service_concurrent",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "Le gardiennage à terre revient à 95 euros par mois au port de Kerlouan.",
        title="Port de Kerlouan — services",
        assertable=False, family="services",
    ),
    ContextCase(
        "archive_declaree",
        "Quel est le tarif actuel de la place au port de Kerlouan ?",
        "En 2019, la place coûtait 240 euros par mois au port de Kerlouan.",
        title="Tarifs 2019 — archive",
        assertable=False, family="archive",
    ),
    ContextCase(
        "passe_sans_mot_archive",
        "Quel est le tarif actuel de la place au port de Kerlouan ?",
        "En 2018, la place valait 230 euros par mois.",
        title="Évolution des tarifs du port de Kerlouan",
        assertable=False, family="archive",
    ),
    ContextCase(
        "historique",
        "Combien coûte une place au port de Kerlouan ?",
        "En 1954, l'amarrage au port de Kerlouan coûtait 12 francs.",
        title="Histoire du port de Kerlouan",
        assertable=False, family="historique",
    ),
    ContextCase(
        "multi_tarifs_mauvais",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un chalutier coûte 780 euros par mois.",
        title="Port de Kerlouan — tarifs",
        document="Port de Kerlouan — tarifs. La place pour un voilier coûte "
                 "320 euros par mois. La place pour un chalutier coûte "
                 "780 euros par mois.",
        assertable=False, family="multi_tarifs",
    ),
    ContextCase(
        "devise_et_lieu_autres",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un voilier coûte 320 francs suisses au port de Morges.",
        title="Port de Morges",
        assertable=False, family="devises",
    ),
    ContextCase(
        "commune_voisine",
        "Combien coûte une place au port de Kerlouan pour un voilier ?",
        "La place pour un voilier coûte 290 euros par mois à Guissény, commune "
        "voisine.",
        title="Port de Guissény",
        assertable=False, family="proche",
    ),
]


def evaluate(version: str, cases: list[ContextCase] | None = None) -> ContextScore:
    """Passe une version sur le jeu 9."""
    cases = cases or CASES
    note = ContextScore(version=version)

    modules = {
        "v2": "context_v2", "v3": "context_v3", "v4": "context_v4",
    }
    assess = None
    if version in modules:
        import importlib

        assess = importlib.import_module(
            f"ara.analysis.{modules[version]}"
        ).assess_context

    for case in cases:
        affirmable = True if assess is None else assess(
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
    return {v: evaluate(v) for v in ("baseline", "v2", "v3", "v4")}


__all__ = ["ANNEE", "CASES", "compare", "evaluate"]
