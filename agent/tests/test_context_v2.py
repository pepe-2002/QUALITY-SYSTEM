"""CONTEXT-V2 : rattachement d'une information au contexte demandé.

Les tests suivent l'autopsie : le temps d'abord, puisqu'il causait neuf des
seize erreurs, la géographie ensuite, l'objet en dernier. Quatre tests figent
des **limites non résolues** — mieux vaut les voir que les oublier.
"""

from __future__ import annotations

import pytest

from ara.analysis.context_v2 import (
    ASSERTABLE,
    CONTEXT_UNKNOWN,
    MATCH,
    MISMATCH,
    PROBABLE_MATCH,
    STATES,
    assess_context,
    filter_facts,
    object_terms,
)

ANNEE = 2026
Q_TRAVERSEE = "Quel est le tarif officiel de la traversée entre Ouroveni et Hoani ?"


def _etat(sentence, title="", document="", question=Q_TRAVERSEE):
    return assess_context(
        question=question, sentence=sentence, title=title,
        document=document or sentence, now=ANNEE,
    )


# --- Les quatre états -----------------------------------------------------------


def test_les_quatre_etats_sont_ceux_demandes():
    assert STATES == (MATCH, PROBABLE_MATCH, CONTEXT_UNKNOWN, MISMATCH)


def test_seuls_deux_etats_autorisent_l_affirmation():
    """Règle de sécurité : CONTEXT_UNKNOWN et MISMATCH ne s'affirment pas."""
    assert set(ASSERTABLE) == {MATCH, PROBABLE_MATCH}
    for etat in (CONTEXT_UNKNOWN, MISMATCH):
        assert etat not in ASSERTABLE


# --- TEMPS et ARCHIVE — neuf erreurs sur seize ---------------------------------


def test_une_archive_declaree_est_rejetee():
    verdict = _etat(
        "En 2019, le billet de la traversée entre Ouroveni et Hoani coûtait "
        "9 000 francs comoriens.",
        title="Tarifs 2019 — archive",
    )
    assert verdict.state == MISMATCH and not verdict.assertable


def test_un_prix_au_passe_est_rejete_sans_le_mot_archive():
    """C'est le temps du verbe et l'année qui doivent suffire."""
    verdict = _etat(
        "En 2017, le billet de la traversée Ouroveni – Hoani valait 8 000 "
        "francs comoriens.",
        title="Rétrospective",
    )
    assert verdict.state == MISMATCH


def test_une_annee_recente_ne_declenche_pas_le_rejet():
    verdict = _etat(
        "Depuis 2026, le billet de la traversée entre Ouroveni et Hoani coûte "
        "15 000 francs comoriens.",
        title="Tarifs en vigueur",
    )
    assert verdict.assertable


def test_une_information_historique_est_rejetee():
    verdict = _etat(
        "En 1908, la traversée entre Ouroveni et Hoani coûtait 30 centimes.",
        title="Histoire de la liaison",
    )
    assert verdict.state == MISMATCH


# --- GÉOGRAPHIE et IDENTITÉ ----------------------------------------------------


def test_un_autre_lieu_est_rejete():
    verdict = _etat(
        "Le billet de la traversée vers Anjouan coûte 25 000 francs comoriens.",
        title="Traversées vers Anjouan",
    )
    assert verdict.state == MISMATCH


def test_le_bon_lieu_passe():
    verdict = _etat(
        "Le billet de la traversée entre Ouroveni et Hoani coûte 15 000 francs "
        "comoriens.",
        title="Tarifs des traversées",
    )
    assert verdict.state == MATCH


def test_le_sujet_nomme_ailleurs_dans_la_source_donne_probable():
    verdict = assess_context(
        question=Q_TRAVERSEE,
        sentence="Le billet coûte 15 000 francs comoriens.",
        title="Traversées Ouroveni – Hoani",
        document="Traversées Ouroveni – Hoani. Le billet coûte 15 000 francs "
                 "comoriens. La traversée dure trois heures.",
        now=ANNEE,
    )
    assert verdict.state in ASSERTABLE


# --- OBJET ----------------------------------------------------------------------


def test_un_autre_produit_n_est_pas_affirmable():
    question = "À quel prix le clou de girofle est-il acheté au planteur ?"
    verdict = assess_context(
        question=question,
        sentence="Le prix d'achat de la vanille verte au planteur s'établit à "
                 "4 500 francs comoriens le kilogramme.",
        title="La filière vanille",
        document="La filière vanille en 2026.",
        now=ANNEE,
    )
    assert not verdict.assertable


def test_le_bon_produit_passe():
    question = "À quel prix le clou de girofle est-il acheté au planteur ?"
    verdict = assess_context(
        question=question,
        sentence="Le clou de girofle est acheté 8 200 francs comoriens le "
                 "kilogramme aux planteurs.",
        title="Achat du clou de girofle",
        now=ANNEE,
    )
    assert verdict.state == MATCH


def test_les_mots_de_mesure_ne_sont_pas_des_objets():
    """« prix », « tarif », « combien » décrivent la mesure, pas la chose."""
    termes = object_terms("Combien coûte la guitare à Vaudreuil ?")
    assert "guitare" in termes
    assert not {"prix", "tarif", "combien", "officiel"} & termes


def test_limite_connue_une_question_sans_nom_propre_desactive_le_controle_objet():
    """Faille figée, non corrigée.

    Sans majuscule dans la question, tous les mots longs sont traités comme
    des termes identifiants, et il ne reste plus d'objet à vérifier. Aucune
    question du jeu 7 n'est dans ce cas ; la faille n'en est pas moins réelle,
    et la corriger demandera une version suivante.
    """
    assert object_terms("Combien coûte le tarif officiel du billet de guitare ?") == set()


def test_les_lieux_ne_sont_pas_des_objets():
    termes = object_terms("Combien coûte la guitare à Vaudreuil ?")
    assert "guitare" in termes and "vaudreuil" not in termes


# --- Filtrage -------------------------------------------------------------------


def test_le_filtre_separe_sans_rien_jeter():
    from ara.analysis.facts import extract_facts

    faits = extract_facts(
        "Le billet de la traversée entre Ouroveni et Hoani coûte 15 000 francs "
        "comoriens. En 2019, il coûtait 9 000 francs comoriens.",
        1,
    )
    affirmables, bloques = filter_facts(faits, question=Q_TRAVERSEE, now=ANNEE)
    assert affirmables, "la valeur actuelle doit rester affirmable"
    assert bloques, "la valeur de 2019 doit être bloquée"
    # Rien n'est perdu : chaque fait est dans l'un des deux paniers.
    assert len(affirmables) + len(bloques) == len(faits)


def test_chaque_blocage_porte_sa_raison():
    from ara.analysis.facts import extract_facts

    faits = extract_facts("En 2018, la traversée coûtait 9 000 francs comoriens.", 1)
    _ok, bloques = filter_facts(faits, question=Q_TRAVERSEE, now=ANNEE)
    assert bloques and all(verdict.reason for _f, verdict in bloques)


# --- Limites figées, non résolues -----------------------------------------------


@pytest.mark.parametrize(
    "identifiant",
    ["homonyme", "page_multi_tarifs_mauvais", "service_voisin", "autre_instrument"],
)
def test_limites_connues_du_jeu_7(identifiant):
    """Quatre cas que CONTEXT-V2 ne résout pas, figés pour rester visibles.

    Les corriger demanderait une version suivante et un jeu de test neuf :
    ajuster le mécanisme sur ces cas-ci reviendrait à s'entraîner sur son
    propre examen. Si l'un de ces tests se met à échouer, c'est que quelqu'un
    a progressé — et le rapport doit être mis à jour.
    """
    from ara.lab.context_test import CASES

    case = next(c for c in CASES if c.id == identifiant)
    verdict = assess_context(
        question=case.question, sentence=case.sentence,
        document=case.text, title=case.title, now=2026,
    )
    assert verdict.assertable, "limite connue : ce cas passe encore"
    assert not case.assertable, "et il ne devrait pas"


# --- Le jeu 7 -------------------------------------------------------------------


def test_le_jeu_7_couvre_les_familles_demandees():
    from ara.lab.context_test import CASES

    familles = {c.family for c in CASES}
    assert {"autre_pays", "homonyme", "archive", "multi_tarifs", "devises",
            "services", "autre_objet", "historique", "proche"} <= familles


def test_le_jeu_7_contient_des_cas_a_conserver():
    """Un jeu qui ne contiendrait que des pièges récompenserait le rejet
    systématique."""
    from ara.lab.context_test import CASES

    assert sum(1 for c in CASES if c.assertable) >= 3


def test_context_v2_ne_rejette_aucune_bonne_information():
    from ara.lab.context_test import evaluate

    assert evaluate("v2").false_rejects == 0
