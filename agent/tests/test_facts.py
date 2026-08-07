"""Extraction de faits chiffrés (spec §2 — comparer suppose du comparable)."""

from __future__ import annotations

import pytest

from ara.analysis.facts import extract_facts, parse_number


# --- Nombres ------------------------------------------------------------------


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("15 000", 15000.0),
        ("15 000", 15000.0),      # espace insécable
        ("17,5", 17.5),
        ("1.234", 1234.0),             # séparateur de milliers
        ("12.5", 12.5),                # décimale anglo-saxonne
        ("trois", 3.0),
        ("quinze", 15.0),
        ("42", 42.0),
    ],
)
def test_lecture_des_nombres(raw, expected):
    assert parse_number(raw) == expected


def test_un_texte_non_numerique_ne_donne_rien():
    assert parse_number("beaucoup") is None


# --- Unités -------------------------------------------------------------------


@pytest.mark.parametrize(
    "phrase, kind, unit, valeur",
    [
        ("Le billet coûte 15 000 francs comoriens par personne.", "money", "KMF", 15000),
        ("Le billet coûte 15 000 FC par personne.", "money", "KMF", 15000),
        ("Le trajet revient à 42 euros pour un adulte.", "money", "EUR", 42),
        ("La traversée dure environ trois heures selon la mer.", "duration", "min", 180),
        ("La traversée dure 90 minutes en moyenne cette saison.", "duration", "min", 90),
        ("Les deux îles sont distantes de 70 kilomètres environ.", "distance", "km", 70),
        ("Le taux de remplissage atteint 85 % en haute saison.", "percent", "%", 85),
        ("La franchise bagages est de 20 kg par passager.", "weight", "kg", 20),
    ],
)
def test_reconnaissance_des_unites(phrase, kind, unit, valeur):
    facts = [f for f in extract_facts(phrase, 1) if f.kind == kind]
    assert facts, f"aucun fait « {kind} » relevé dans : {phrase}"
    assert facts[0].unit == unit
    assert facts[0].low == pytest.approx(valeur)


def test_les_durees_sont_ramenees_aux_minutes():
    """Comparer 3 heures et 90 minutes exige une unité commune."""
    heures = extract_facts("Le trajet dure trois heures au total.", 1)[0]
    minutes = extract_facts("Le trajet dure 90 minutes au total.", 2)[0]
    assert heures.unit == minutes.unit == "min"
    assert heures.low == 180 and minutes.low == 90


# --- Fourchettes --------------------------------------------------------------


def test_une_fourchette_est_un_seul_fait():
    """« entre 15 000 et 17 500 » est une fourchette, pas deux valeurs."""
    facts = extract_facts(
        "Les tarifs vont de 15 000 à 17 500 francs comoriens selon la compagnie.", 1
    )
    money = [f for f in facts if f.kind == "money"]
    assert len(money) == 1
    assert money[0].is_range
    assert (money[0].low, money[0].high) == (15000, 17500)


def test_fourchette_avec_entre_et():
    facts = extract_facts("Comptez entre 40 et 60 euros par personne.", 1)
    money = [f for f in facts if f.kind == "money"]
    assert len(money) == 1
    assert (money[0].low, money[0].high) == (40, 60)


# --- Contexte et divers -------------------------------------------------------


def test_le_contexte_de_la_phrase_est_conserve():
    """Sans contexte, impossible de savoir de quoi parle un chiffre."""
    fact = extract_facts("Le billet adulte coûte 15 000 francs comoriens.", 1)[0]
    assert "billet" in fact.context
    assert "adulte" in fact.context
    assert "les" not in fact.context, "les mots outils ne sont pas du contexte"


def test_lannee_est_relevee_sans_separateur():
    facts = [f for f in extract_facts("Tarifs applicables depuis 2026.", 1) if f.kind == "year"]
    assert facts and facts[0].describe() == "2026"


def test_la_source_est_tracee():
    for fact in extract_facts("Le billet coûte 15 000 FC.", 7):
        assert fact.source == 7


def test_un_texte_vide_ne_leve_pas():
    assert extract_facts("", 1) == []
    assert extract_facts("Aucun chiffre ici, seulement du texte.", 1) == []


def test_le_nombre_de_faits_est_borne():
    texte = " ".join(f"Le tarif numéro {i} est de {i}00 francs comoriens." for i in range(1, 200))
    assert len(extract_facts(texte, 1, max_facts=10)) <= 10


# --- Lisibilité ---------------------------------------------------------------


@pytest.mark.parametrize(
    "phrase, attendu",
    [
        ("Le trajet dure 45 minutes au total.", "45 min"),
        ("Le trajet dure trois heures au total.", "3 h"),
        ("La formation dure deux jours complets.", "2 j"),
    ],
)
def test_les_durees_saffichent_dans_une_unite_lisible(phrase, attendu):
    """Stockées en minutes pour être comparables, affichées pour être lues."""
    fact = [f for f in extract_facts(phrase, 1) if f.kind == "duration"][0]
    assert fact.describe() == attendu
    assert fact.unit == "min", "l'unité de comparaison reste la minute"
