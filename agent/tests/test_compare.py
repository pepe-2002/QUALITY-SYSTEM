"""Confrontation des sources : contradictions et recoupements (spec §2)."""

from __future__ import annotations

from ara.analysis.compare import agreements, find_contradictions
from ara.analysis.facts import extract_facts


def _facts(*textes: str):
    facts = []
    for index, texte in enumerate(textes, start=1):
        facts.extend(extract_facts(texte, index))
    return facts


# --- Contradictions -----------------------------------------------------------


def test_deux_prix_incompatibles_sont_une_contradiction():
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens par adulte.",
        "Le billet de la traversée coûte 45 000 francs comoriens par adulte.",
    )
    contradictions = find_contradictions(facts)
    assert len(contradictions) == 1
    assert contradictions[0].kind == "money"
    assert contradictions[0].sources == [1, 2]
    assert "15 000" in contradictions[0].describe()
    assert "45 000" in contradictions[0].describe()


def test_deux_durees_incompatibles_sont_detectees_malgre_les_unites():
    """Trois heures contre 90 minutes : il faut normaliser pour voir le conflit."""
    facts = _facts(
        "La traversée en vedette dure trois heures depuis le port.",
        "La traversée en vedette dure 90 minutes depuis le port.",
    )
    contradictions = find_contradictions(facts)
    assert len(contradictions) == 1
    assert contradictions[0].unit == "min"


def test_un_prix_dans_une_fourchette_ne_contredit_pas():
    """Le piège classique : 15 000 est compris dans « 15 000 à 17 500 »."""
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens par adulte.",
        "Le billet de la traversée coûte entre 15 000 et 17 500 francs comoriens par adulte.",
    )
    assert find_contradictions(facts) == []


def test_un_petit_ecart_est_tolere():
    """Arrondis et taxes : 15 000 et 15 500 ne sont pas un désaccord."""
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 15 500 francs comoriens.",
    )
    assert find_contradictions(facts) == []


def test_des_devises_differentes_ne_se_comparent_pas():
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 30 euros.",
    )
    assert find_contradictions(facts) == []


def test_deux_sujets_differents_ne_se_contredisent_pas():
    """Le prix d'un billet et celui d'une nuit d'hôtel n'ont rien à voir."""
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "La nuit d'hôtel revient à 45 000 francs comoriens petit-déjeuner inclus.",
    )
    assert find_contradictions(facts) == []


def test_une_source_ne_se_contredit_pas_elle_meme():
    """Deux chiffres d'une même page relèvent du contexte, pas du désaccord."""
    facts = extract_facts(
        "Le billet adulte de la traversée coûte 15 000 francs comoriens. "
        "Le billet adulte de la traversée en haute saison coûte 45 000 francs comoriens.",
        1,
    )
    assert find_contradictions(facts) == []


def test_les_annees_ne_declenchent_pas_de_contradiction():
    """Deux pages datées différemment, ce n'est pas un désaccord factuel."""
    facts = _facts(
        "Les tarifs des traversées sont applicables depuis 2019.",
        "Les tarifs des traversées sont applicables depuis 2026.",
    )
    assert find_contradictions(facts) == []


def test_trois_sources_en_desaccord_donnent_une_seule_alerte():
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 45 000 francs comoriens.",
        "Le billet de la traversée coûte 90 000 francs comoriens.",
    )
    contradictions = find_contradictions(facts)
    assert len(contradictions) == 1, "un seul problème réel, une seule alerte"
    assert contradictions[0].sources == [1, 2, 3]


# --- Recoupements -------------------------------------------------------------


def test_deux_sources_concordantes_sont_recoupees():
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 15 000 francs comoriens également.",
    )
    clusters = agreements(facts)
    assert len(clusters) == 1
    assert {f.source for f in clusters[0]} == {1, 2}


def test_une_valeur_isolee_nest_pas_un_recoupement():
    facts = extract_facts("Le billet de la traversée coûte 15 000 francs comoriens.", 1)
    assert agreements(facts) == []


def test_une_valeur_dans_une_fourchette_compte_comme_recoupement():
    facts = _facts(
        "Le billet de la traversée coûte 16 000 francs comoriens.",
        "Le billet de la traversée coûte entre 15 000 et 17 500 francs comoriens.",
    )
    assert len(agreements(facts)) == 1


# --- Recentrage sur le sujet demandé ------------------------------------------


def test_le_focus_ecarte_les_desaccords_hors_sujet():
    """Constaté en réel : une page de voyage produisait 29 fausses alertes."""
    facts = _facts(
        "Le repas au restaurant du port coûte 15 000 francs comoriens.",
        "Le repas au restaurant du port coûte 45 000 francs comoriens.",
    )
    assert find_contradictions(facts), "sans focus, le désaccord est bien vu"
    assert find_contradictions(facts, focus={"traversee", "billet"}) == [], (
        "avec un focus sur la traversée, un désaccord sur les repas est écarté"
    )


def test_le_focus_conserve_les_desaccords_sur_le_sujet():
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 45 000 francs comoriens.",
    )
    assert find_contradictions(facts, focus={"traversee"})


def test_les_desaccords_les_mieux_etayes_arrivent_en_premier():
    facts = _facts(
        "Le billet adulte de la traversée en vedette rapide coûte 15 000 francs comoriens.",
        "Le billet adulte de la traversée en vedette rapide coûte 45 000 francs comoriens.",
        "Le parking coûte 500 francs comoriens la journée au port.",
        "Le parking coûte 5 000 francs comoriens la journée au port.",
    )
    contradictions = find_contradictions(facts)
    assert len(contradictions[0].shared) >= len(contradictions[-1].shared)


# --- Indépendance des sources -------------------------------------------------


def test_deux_pages_du_meme_site_ne_se_contredisent_pas():
    """Constaté en réel : 14 fausses alertes entre pages d'une même encyclopédie."""
    facts = _facts(
        "La hauteur de la tour est de 300 mètres depuis sa construction.",
        "La hauteur de la tour est de 500 mètres depuis sa construction.",
    )
    domaines = {1: "fr.wikipedia.org", 2: "fr.wikipedia.org"}

    assert find_contradictions(facts), "deux sites différents : désaccord réel"
    assert find_contradictions(facts, domains=domaines) == [], (
        "un même site n'est pas deux sources indépendantes"
    )


def test_deux_pages_du_meme_site_ne_confirment_rien():
    facts = _facts(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 15 000 francs comoriens.",
    )
    domaines = {1: "exemple.test", 2: "exemple.test"}

    assert agreements(facts), "sites distincts : recoupement valable"
    assert agreements(facts, domains=domaines) == [], (
        "se citer soi-même n'est pas une confirmation"
    )
