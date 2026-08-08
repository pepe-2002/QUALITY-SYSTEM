"""JEU 8 — jeu de test indépendant de CONTEXT-V3. Écrit avant son exécution.

Le jeu 7 a servi à développer V3 : elle y obtient 100 %, et ce chiffre ne vaut
rien — on ne s'examine pas sur ses propres brouillons. Celui-ci juge.

Univers neuf : une clinique vétérinaire, ses espèces, ses communes. Aucun mot
des sept jeux précédents.

Ce jeu est construit contre V3 autant que pour elle
----------------------------------------------------
V3 durcit trois règles : terme d'objet le plus **spécifique** exigé, objet
concurrent valant désaveu, et noms composés comparés tête et qualificatif.
Chacune peut **trop** rejeter. Le jeu contient donc :

* huit cas **corrects** — dont plusieurs conçus pour déclencher à tort les
  nouvelles règles : une phrase qui nomme autre chose en passant, un nom
  composé écrit sans son qualificatif, une page où tous les mots se
  ressemblent ;
* dix pièges, couvrant les neuf familles demandées.

Un jeu qui ne contiendrait que des pièges récompenserait le rejet aveugle.
C'est le faux rejet qui coûte le plus cher ici : une information correcte
écartée ne revient jamais.
"""

from __future__ import annotations

from .context_test import ContextCase, ContextScore

ANNEE = 2026

CASES: list[ContextCase] = [
    # === CORRECTS — à conserver ============================================
    ContextCase(
        "ok_simple",
        "Combien coûte la consultation d'un chat à la clinique de Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 42 euros à la clinique de Villeneuve-sur-Loire.",
        title="Clinique vétérinaire de Villeneuve-sur-Loire — tarifs",
        assertable=True, family="sujet",
    ),
    ContextCase(
        "ok_document",
        "Combien coûte la consultation d'un chat à la clinique de Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 42 euros.",
        title="Clinique vétérinaire de Villeneuve-sur-Loire",
        document="Clinique vétérinaire de Villeneuve-sur-Loire. La consultation "
                 "d'un chat coûte 42 euros. Le cabinet ouvre à 8 heures.",
        assertable=True, family="sujet",
        note="Le lieu est nommé dans la source, pas dans la phrase.",
    ),
    ContextCase(
        "ok_mot_en_passant",
        "Combien coûte la consultation d'un chat à la clinique de Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 42 euros, sur rendez-vous, vaccination "
        "comprise, à Villeneuve-sur-Loire.",
        title="Clinique de Villeneuve-sur-Loire",
        assertable=True, family="sur_rejet",
        note="Contre la règle « objet concurrent » : « rendez-vous » et "
             "« vaccination » sont là sans être le sujet. Elles ne doivent pas "
             "faire rejeter une phrase par ailleurs correcte.",
    ),
    ContextCase(
        "ok_nom_sans_qualificatif",
        "Combien coûte la consultation d'un chat à la clinique de Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 42 euros à la clinique de Villeneuve.",
        title="Clinique de Villeneuve",
        assertable=True, family="sur_rejet",
        note="Contre la règle des noms composés : la source abrège le nom. "
             "Abréger n'est pas contredire.",
    ),
    ContextCase(
        "ok_page_uniforme",
        "Combien coûte la consultation d'un chat à la clinique de Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 42 euros.",
        title="Clinique de Villeneuve-sur-Loire",
        document="Clinique de Villeneuve-sur-Loire. La consultation d'un chat "
                 "coûte 42 euros. La consultation d'un chat en urgence coûte "
                 "68 euros. La consultation d'un chat à domicile coûte 90 euros.",
        assertable=True, family="sur_rejet",
        note="Contre la pesée : « chat » est partout dans cette page, donc peu "
             "spécifique. Le repli ne doit pas désactiver le contrôle au point "
             "de rejeter la bonne phrase.",
    ),
    ContextCase(
        "ok_annee_courante",
        "Quel est le tarif actuel du vaccin pour chien à Villeneuve-sur-Loire ?",
        "Depuis 2026, le vaccin pour chien coûte 55 euros à Villeneuve-sur-Loire.",
        title="Tarifs en vigueur",
        assertable=True, family="archive",
    ),
    ContextCase(
        "ok_espece_precise",
        "Combien coûte la stérilisation d'une chienne à Villeneuve-sur-Loire ?",
        "La stérilisation d'une chienne est facturée 180 euros à Villeneuve-sur-Loire.",
        title="Chirurgie — clinique de Villeneuve-sur-Loire",
        assertable=True, family="sujet",
    ),
    ContextCase(
        "ok_sans_nom_propre",
        "Combien coûte le vaccin contre la rage pour un chien ?",
        "Le vaccin contre la rage pour un chien coûte 48 euros.",
        title="Tarifs de vaccination",
        assertable=True, family="sans_nom_propre",
        note="Question sans majuscule : le contrôle d'objet doit fonctionner "
             "quand même, et ne pas rejeter la bonne réponse.",
    ),

    # === PIÈGES — à rejeter ================================================
    ContextCase(
        "autre_pays",
        "Combien coûte la consultation d'un chat à la clinique de Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 38 francs suisses à notre cabinet de Sion.",
        title="Cabinet vétérinaire de Sion",
        assertable=False, family="autre_pays",
    ),
    ContextCase(
        "homonyme",
        "Combien coûte la consultation d'un chat à Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 29 euros à Villeneuve-les-Bains.",
        title="Clinique de Villeneuve-les-Bains",
        assertable=False, family="homonyme",
        note="Même tête, autre qualificatif : c'est le cas que V2 ne savait "
             "pas trancher.",
    ),
    ContextCase(
        "archive_declaree",
        "Quel est le tarif actuel de la consultation à Villeneuve-sur-Loire ?",
        "En 2019, la consultation coûtait 26 euros à Villeneuve-sur-Loire.",
        title="Tarifs 2019 — archive",
        assertable=False, family="archive",
    ),
    ContextCase(
        "passe_sans_mot_archive",
        "Quel est le tarif actuel de la consultation à Villeneuve-sur-Loire ?",
        "En 2018, la consultation valait 24 euros à Villeneuve-sur-Loire.",
        title="Évolution des tarifs",
        assertable=False, family="archive",
    ),
    ContextCase(
        "historique",
        "Combien coûte la consultation d'un chat à Villeneuve-sur-Loire ?",
        "En 1930, la visite du vétérinaire à Villeneuve-sur-Loire coûtait 3 francs.",
        title="Histoire de la clinique",
        assertable=False, family="historique",
    ),
    ContextCase(
        "autre_espece",
        "Combien coûte la consultation d'un chat à Villeneuve-sur-Loire ?",
        "La consultation d'un cheval coûte 95 euros à Villeneuve-sur-Loire.",
        title="Clinique de Villeneuve-sur-Loire — grands animaux",
        assertable=False, family="autre_objet",
        note="Bon lieu, bonne clinique, mauvaise espèce.",
    ),
    ContextCase(
        "service_voisin",
        "Combien coûte la consultation d'un chat à Villeneuve-sur-Loire ?",
        "Le toilettage d'un chat coûte 35 euros à Villeneuve-sur-Loire.",
        title="Clinique de Villeneuve-sur-Loire",
        assertable=False, family="services",
        note="Bonne espèce, bon lieu, autre prestation.",
    ),
    ContextCase(
        "multi_tarifs_mauvais",
        "Combien coûte la consultation d'un chat à Villeneuve-sur-Loire ?",
        "La pension pour chat revient à 22 euros la nuit.",
        title="Clinique de Villeneuve-sur-Loire — tarifs",
        document="Clinique de Villeneuve-sur-Loire — tarifs. La consultation "
                 "d'un chat coûte 42 euros. La pension pour chat revient à "
                 "22 euros la nuit.",
        assertable=False, family="multi_tarifs",
    ),
    ContextCase(
        "devise_autre",
        "Combien coûte la consultation d'un chat à Villeneuve-sur-Loire ?",
        "La consultation d'un chat est facturée 42 francs suisses à Lausanne.",
        title="Cabinet de Lausanne",
        assertable=False, family="devises",
        note="Le nombre est identique ; ni le lieu ni la devise ne le sont.",
    ),
    ContextCase(
        "commune_voisine",
        "Combien coûte la consultation d'un chat à Villeneuve-sur-Loire ?",
        "La consultation d'un chat coûte 37 euros à Bellegarde, commune voisine.",
        title="Clinique de Bellegarde",
        assertable=False, family="proche",
    ),
]


def evaluate(version: str, cases: list[ContextCase] | None = None) -> ContextScore:
    """Passe une version sur le jeu 8.

    ``baseline`` = aucun contrôle de contexte, l'état du système avant V2.
    """
    cases = cases or CASES
    note = ContextScore(version=version)

    if version == "v2":
        from ..analysis.context_v2 import assess_context
    elif version == "v3":
        from ..analysis.context_v3 import assess_context
    else:
        assess_context = None

    for case in cases:
        if assess_context is None:
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
    return {version: evaluate(version) for version in ("baseline", "v2", "v3")}


__all__ = ["ANNEE", "CASES", "compare", "evaluate"]
