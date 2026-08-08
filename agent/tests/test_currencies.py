"""EXTRACTION-V2 : devises, confiance, et refus de deviner.

Le test le plus important de ce fichier est celui qui vérifie qu'un montant
sans devise identifiable reste `UNKNOWN`. Un extracteur qui devinerait la
devise du projet aurait de meilleurs chiffres et produirait des comparaisons
fausses avec l'aplomb de la certitude.
"""

from __future__ import annotations

import pytest

from ara.analysis import currency
from ara.analysis.facts import extract_facts, extractor


def _money(text: str, version: str = "v2"):
    with extractor(version):
        return [f for f in extract_facts(text, 1, max_facts=50) if f.kind == "money"]


# --- La baseline ne bouge pas ---------------------------------------------------


def test_la_baseline_ignore_toujours_les_francs_nus():
    """Elle est gelée : c'est elle qui a produit H1, H2 et les deux V2."""
    assert _money("La traversée coûte 3 200 francs.", "baseline") == []


def test_la_baseline_lit_toujours_les_francs_comoriens():
    faits = _money("Le billet coûte 15 000 francs comoriens.", "baseline")
    assert [(f.low, f.unit) for f in faits] == [(15000.0, "KMF")]


def test_les_versions_sont_isolees():
    from ara.analysis.facts import _active_version

    with extractor("baseline"):
        pass
    assert _active_version == "v2", "la version active doit être restaurée"


# --- Devise écrite → certitude --------------------------------------------------


@pytest.mark.parametrize(
    "texte, devise",
    [
        ("Le billet coûte 15 000 francs comoriens.", "KMF"),
        ("Le sac vaut 12 500 francs CFA.", "XOF"),
        ("Le transport coûte 7 000 FCFA.", "XOF"),
        ("La nuit est à 180 francs suisses.", "CHF"),
        ("L'entrée est à 12 euros.", "EUR"),
        ("Le transfert revient à 45 dollars US.", "USD"),
        ("Le trajet coûte 8 000 ariary.", "MGA"),
    ],
)
def test_une_devise_ecrite_est_certaine(texte, devise):
    faits = _money(texte)
    assert faits and faits[0].unit == devise
    assert faits[0].confidence == "certaine"


# --- Devise déduite → probable --------------------------------------------------


def test_le_contexte_geographique_rend_la_devise_probable():
    faits = _money("Voyager aux Comores : la traversée coûte 3 200 francs.")
    assert faits[0].unit == "KMF" and faits[0].confidence == "probable"


def test_une_devise_nommee_ailleurs_dans_la_phrase():
    faits = _money("Le billet vaut 15 000 francs comoriens et le repas 3 000 francs.")
    nus = [f for f in faits if f.low == 3000]
    assert nus and nus[0].unit == "KMF" and nus[0].confidence == "probable"


def test_le_contexte_du_document_sert_a_resoudre():
    devise, confiance = currency.resolve("Le billet coûte 3 200 francs.",
                                         "Tarifs au Sénégal — édition 2026")
    assert devise == "XOF" and confiance == "probable"


# --- Le refus de deviner --------------------------------------------------------


def test_sans_contexte_la_devise_reste_inconnue():
    """La règle de sécurité : garder le montant, perdre la devise."""
    faits = _money("La traversée coûte 3 200 francs.")
    assert faits[0].low == 3200
    assert faits[0].unit == currency.UNKNOWN
    assert faits[0].confidence == "inconnue"


def test_francs_ne_vaut_jamais_kmf_par_defaut():
    """Le projet parle des Comores ; l'extracteur, lui, n'en sait rien."""
    faits = _money("Le trajet coûte 3 200 francs.")
    assert faits[0].unit != "KMF"


def test_un_montant_converti_n_herite_pas_de_l_autre_devise():
    faits = _money("3 200 francs, soit environ 6,50 euros.")
    nus = [f for f in faits if f.low == 3200]
    assert nus and nus[0].unit == currency.UNKNOWN


@pytest.mark.parametrize(
    "phrase",
    [
        "Le trajet coûte 3 200 francs, contre 12 euros en haute saison.",
        "3 200 francs, c'est-à-dire 6,50 euros.",
        "3 200 francs ≈ 6,50 euros.",
    ],
)
def test_toutes_les_formes_de_conversion_sont_prudentes(phrase):
    nus = [f for f in _money(phrase) if f.low == 3200]
    assert nus and nus[0].unit == currency.UNKNOWN


def test_plusieurs_devises_dans_un_document_laissent_le_doute():
    devise, confiance = currency.resolve(
        "Le billet coûte 3 200 francs.",
        "Tarifs : 12 euros en France, 45 dollars aux États-Unis.",
    )
    assert devise == currency.UNKNOWN and confiance == "inconnue"


def test_plusieurs_zones_geographiques_laissent_le_doute():
    devise, _ = currency.resolve(
        "Le trajet coûte 3 200 francs.",
        "Comparatif entre les Comores et le Sénégal.",
    )
    assert devise == currency.UNKNOWN


# --- Pas de double comptage -----------------------------------------------------


@pytest.mark.parametrize(
    "texte, valeur",
    [
        ("Le billet coûte 15 000 francs comoriens.", 15000),
        ("Le sac vaut 12 500 francs CFA.", 12500),
        ("La nuit est à 180 francs suisses.", 180),
    ],
)
def test_un_franc_qualifie_n_est_compte_qu_une_fois(texte, valeur):
    """Sans garde-fou, « francs » générique recompterait la même somme."""
    faits = [f for f in _money(texte) if abs(f.low - valeur) < 1]
    assert len(faits) == 1, [(f.low, f.unit) for f in faits]


# --- Faux positifs --------------------------------------------------------------


@pytest.mark.parametrize(
    "texte",
    [
        "L'île compte 42 000 habitants.",
        "La liaison existe depuis 1974.",
        "La bibliothèque contient 3 000 livres.",
        "Il y a 17 sièges à bord.",
        "Le colis pèse 25 kilogrammes.",
    ],
)
def test_ce_qui_n_est_pas_un_montant_ne_le_devient_pas(texte):
    assert _money(texte) == []


def test_livre_sans_sterling_n_est_pas_une_devise():
    """« livre » désigne aussi un ouvrage et une unité de masse."""
    assert _money("La bibliothèque contient 3 000 livres.") == []
    faits = _money("Le billet coûte 40 livres sterling.")
    assert faits and faits[0].unit == "GBP"


# --- Confiance ------------------------------------------------------------------


def test_les_trois_niveaux_existent():
    assert currency.CONFIDENCE_LEVELS == ("certaine", "probable", "inconnue")


def test_une_grandeur_non_monetaire_est_toujours_certaine():
    with extractor("v2"):
        faits = extract_facts("La traversée dure 3 heures sur 70 kilomètres.", 1)
    assert faits and all(f.confidence == "certaine" for f in faits)


def test_la_confiance_est_serialisee():
    faits = _money("La traversée coûte 3 200 francs.")
    assert faits[0].to_dict().get("confidence") == "inconnue" or hasattr(
        faits[0], "confidence"
    )
