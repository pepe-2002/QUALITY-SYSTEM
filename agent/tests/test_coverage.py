"""Détection des informations manquantes (spec §3) et contrôle de la réponse."""

from __future__ import annotations

import pytest

from ara.analysis.coverage import coverage_ratio, detect_aspects, find_gaps
from ara.analysis.facts import extract_facts
from ara.analysis.verify import summarize, verify_answer
from ara.core.models import SourceDoc


def _doc(url: str, titre: str, texte: str) -> SourceDoc:
    return SourceDoc(url=url, title=titre, text=texte, fetched=True)


# --- Aspects demandés ---------------------------------------------------------


@pytest.mark.parametrize(
    "question, attendu",
    [
        ("Combien coûte la traversée ?", {"prix"}),
        ("Quel est le tarif du billet ?", {"prix"}),
        ("Combien de temps dure la traversée ?", {"prix", "duree"}),
        ("Quelle distance sépare les deux îles ?", {"distance"}),
        ("Quand partent les vedettes ?", {"date"}),
        ("Parle-moi de Mohéli", set()),
    ],
)
def test_detection_des_aspects_demandes(question, attendu):
    assert detect_aspects(question) == attendu


# --- Manques ------------------------------------------------------------------


def test_un_aspect_sans_donnee_chiffree_est_un_manque():
    docs = [_doc("https://a.test/x", "Mohéli", "L'île de Mohéli est la plus sauvage des Comores.")]
    gaps = find_gaps("Combien coûte la traversée pour Mohéli ?", docs, [])
    assert any(gap.kind == "aspect" and "prix" in gap.label for gap in gaps)


def test_un_aspect_couvert_nest_pas_un_manque():
    texte = "Le billet de la traversée coûte 15 000 francs comoriens."
    docs = [_doc("https://a.test/x", "Tarifs", texte), _doc("https://b.test/x", "Tarifs bis", texte)]
    facts = extract_facts(texte, 1) + extract_facts(texte, 2)
    gaps = find_gaps("Combien coûte la traversée ?", docs, facts)
    assert not any(gap.kind == "aspect" for gap in gaps)


def test_un_mot_cle_absent_des_sources_est_un_manque():
    docs = [_doc("https://a.test/x", "Grande Comore", "La Grande Comore accueille Moroni.")]
    gaps = find_gaps(
        "traversées vers Mohéli", docs, [], subject_keywords={"traversee", "moheli"}
    )
    assert any(gap.kind == "keyword" and "moheli" in gap.label for gap in gaps)


def test_une_valeur_non_confirmee_est_un_manque():
    """Une information donnée par une seule source n'est pas vérifiée."""
    texte = "Le billet de la traversée coûte 15 000 francs comoriens."
    docs = [_doc("https://a.test/x", "Tarifs", texte)]
    gaps = find_gaps("Combien coûte la traversée ?", docs, extract_facts(texte, 1))
    assert any(gap.kind == "confirmation" for gap in gaps)


def test_les_manques_sont_ordonnes_par_urgence():
    docs = [_doc("https://a.test/x", "Mohéli", "L'île de Mohéli est sauvage.")]
    gaps = find_gaps(
        "Combien coûte la traversée vers Anjouan ?",
        docs,
        [],
        subject_keywords={"traversee", "anjouan"},
    )
    assert gaps[0].kind == "aspect", "un aspect manquant prime sur un mot-clé absent"


def test_chaque_manque_porte_de_quoi_relancer():
    docs = [_doc("https://a.test/x", "Mohéli", "L'île est sauvage.")]
    for gap in find_gaps("Combien coûte la traversée ?", docs, []):
        assert gap.hint, "un manque sans piste de relance est inexploitable"


def test_taux_de_couverture():
    docs = [_doc("https://a.test/x", "Traversées", "Les traversées vers Mohéli sont fréquentes.")]
    assert coverage_ratio("traversées Mohéli", docs) == 1.0
    assert coverage_ratio("traversées Anjouan", docs) == 0.5


# --- Vérification de la réponse -----------------------------------------------


def test_une_reponse_bien_sourcee_passe():
    docs = [_doc("https://a.test/x", "A", "texte"), _doc("https://b.test/x", "B", "texte")]
    check = verify_answer("Le tarif est de 15 000 FC [S1], confirmé par [S2].", docs)
    assert check.ok
    assert check.citations == {1, 2}


def test_une_citation_inexistante_est_signalee():
    """Un LLM invente parfois une source : il faut le voir."""
    docs = [_doc("https://a.test/x", "A", "texte")]
    check = verify_answer("Le tarif est de 15 000 FC [S4].", docs)
    assert not check.ok
    assert "inexistantes" in check.problems[0]


def test_des_sources_lues_mais_jamais_citees_sont_signalees():
    docs = [_doc("https://a.test/x", "A", "texte")]
    check = verify_answer("Le tarif est d'environ 15 000 francs.", docs)
    assert not check.ok
    assert "aucune n'est citée" in check.problems[0]


def test_un_chiffre_sans_citation_est_releve():
    docs = [_doc("https://a.test/x", "A", "texte")]
    answer = "Le tarif officiel est [S1].\nLe supplément bagages atteint 5 000 FC."
    check = verify_answer(answer, docs)
    assert check.uncited_claims


def test_une_reponse_vide_est_refusee():
    check = verify_answer("   ", [])
    assert not check.ok


def test_sans_source_une_reponse_sans_citation_est_acceptable():
    """On ne reproche pas l'absence de citation quand rien n'a été lu."""
    assert verify_answer("Bonjour, comment puis-je aider ?", []).ok


def test_resume_lisible():
    docs = [_doc("https://a.test/x", "A", "texte")]
    assert "citation" in summarize(verify_answer("Tarif [S1].", docs))


# --- Diversité des sources ----------------------------------------------------


def test_un_seul_domaine_est_un_manque():
    """Spec §2 : trois pages d'un même site ne font pas trois sources."""
    docs = [
        _doc("https://exemple.test/a", "A", "Les traversées coûtent 15 000 FC."),
        _doc("https://exemple.test/b", "B", "Les traversées coûtent 15 000 FC."),
    ]
    gaps = find_gaps("Combien coûte la traversée ?", docs, [])
    assert any(gap.kind == "diversity" for gap in gaps)


def test_deux_domaines_distincts_ne_sont_pas_un_manque():
    docs = [
        _doc("https://exemple.test/a", "A", "Les traversées coûtent 15 000 FC."),
        _doc("https://autre.test/b", "B", "Les traversées coûtent 15 000 FC."),
    ]
    gaps = find_gaps("Combien coûte la traversée ?", docs, [])
    assert not any(gap.kind == "diversity" for gap in gaps)


def test_sans_source_la_diversite_nest_pas_reprochee():
    gaps = find_gaps("Combien coûte la traversée ?", [], [])
    assert not any(gap.kind == "diversity" for gap in gaps)
