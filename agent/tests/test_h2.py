"""H2 : pré-enregistrement, graines, taxonomies, verdict.

Ces tests ne rejouent pas l'expérience complète — elle est lente et ce n'est
pas leur rôle. Ils vérifient ce qui doit rester vrai quel que soit le
résultat : que les critères sont ceux qui ont été annoncés, que le verdict les
applique sans indulgence, que les graines ne changent pas les faits, et que H1
n'est pas retouchée.
"""

from __future__ import annotations

import re

import pytest

from ara.analysis.report import STOP_CODES
from ara.lab import h2
from ara.lab.corpus import Corpus
from ara.lab.dataset import TASKS as CALIBRATION
from ara.lab.harness import Outcome
from ara.lab.heldout import PAGES, TASKS as HELDOUT, held_out_corpus
from ara.lab.metrics import Row, Score
from ara.lab.seeds import SEEDS, ShuffledCorpus, question_for, task_for
from ara.lab.stops import classify_errors, stop_reason

# --- Pré-enregistrement --------------------------------------------------------


def test_l_enonce_de_h2_est_celui_qui_a_ete_fixe():
    assert h2.H2_STATEMENT == (
        "H2 — À exactitude comparable, ADAPTIVE REASONING réduit significativement "
        "le nombre de recherches nécessaires par rapport à FIXED."
    )


def test_les_seuils_sont_ceux_annonces():
    """Un seuil déplacé après coup, c'est une hypothèse qu'on ne peut plus perdre."""
    assert h2.MARGE_EXACTITUDE == 0.05
    assert h2.REDUCTION_MINIMALE == 0.20
    assert h2.ALPHA == 0.05


def test_h1_n_est_pas_touchee():
    from ara.lab.experiment import HYPOTHESIS

    assert HYPOTHESIS.min_gain == 0.05
    assert HYPOTHESIS.max_cost_ratio == 1.5
    assert HYPOTHESIS.challenger == "adaptive_research"


# --- Jeux de données -----------------------------------------------------------


def test_les_deux_jeux_ne_partagent_aucune_tache():
    assert {t.id for t in CALIBRATION} & {t.id for t in HELDOUT} == set()


def test_les_deux_jeux_ne_partagent_aucune_page():
    calibration = set(Corpus().pages)
    assert calibration & set(PAGES) == set()


def test_le_jeu_de_test_contient_les_trois_familles():
    familles = {t.family for t in HELDOUT}
    assert familles == {"facile", "profond", "piege"}


def test_chaque_valeur_attendue_existe_dans_le_corpus_de_test():
    """Une vérité de référence introuvable rendrait la tâche impossible — donc
    la mesure ininterprétable."""
    from ara.analysis.facts import extract_facts
    from ara.lab.metrics import _matches

    corpus = held_out_corpus()
    textes = [re.sub(r"<[^>]+>", " ", html) for html in corpus.pages.values()]
    faits = [f for texte in textes for f in extract_facts(texte, 1, max_facts=200)]
    for task in HELDOUT:
        for gold in task.gold:
            assert any(_matches(f, gold) for f in faits), f"{task.id} : {gold.label} introuvable"


def test_chaque_tache_a_des_reformulations():
    for task in (*CALIBRATION, *HELDOUT):
        assert len(task.variants()) >= 3, task.id


# --- Graines -------------------------------------------------------------------


def test_une_graine_change_la_formulation_pas_la_verite():
    task = HELDOUT[0]
    autre = task_for(task, 1)
    assert autre.question != task.question or len(task.variants()) == 1
    assert [g.value for g in autre.gold] == [g.value for g in task.gold]


def test_la_meme_graine_donne_la_meme_question():
    task = CALIBRATION[0]
    assert question_for(task, 4) == question_for(task, 4)


def test_le_melange_conserve_l_ensemble_des_pages():
    """Une graine ne doit rendre aucune tâche plus facile ni plus difficile."""
    base = Corpus()
    requete = "tarif traversée Ouroveni Hoani"
    attendu = sorted(base.search(requete))
    for seed in SEEDS:
        assert sorted(ShuffledCorpus(base, seed).search(requete)) == attendu


def test_le_melange_est_reproductible():
    base = Corpus()
    requete = "tarif traversée Ouroveni Hoani"
    assert (
        ShuffledCorpus(base, 3).search(requete)
        == ShuffledCorpus(base, 3).search(requete)
    )


# --- Raisons d'arrêt -----------------------------------------------------------


def test_une_passe_unique_n_est_pas_une_limite_de_budget():
    """Sinon la case « limite de budget » se remplirait de stratégies qui ne
    décident rien."""
    assert stop_reason(Outcome(strategy="fixed", task_id="x")) == "passe_unique"


def test_une_erreur_est_imputee_au_controleur():
    outcome = Outcome(strategy="adaptive_research", task_id="x", error="boum")
    assert stop_reason(outcome) == "erreur_controleur"


def test_les_codes_d_arret_sont_ceux_du_systeme():
    outcome = Outcome(strategy="adaptive_research", task_id="x",
                      stop_code="manque_information")
    assert stop_reason(outcome) in STOP_CODES


# --- Taxonomie des erreurs -----------------------------------------------------


def _row(**kwargs) -> Outcome:
    return Outcome(strategy="fixed", task_id="t", **kwargs)


def test_arret_trop_tot_quand_une_autre_strategie_a_trouve():
    tally = classify_errors(
        HELDOUT[0], _row(searches=1), Score(accuracy=0.0),
        best_searches=2, someone_found=True,
    )
    assert "arret_trop_tot" in tally.kinds


def test_pas_d_arret_trop_tot_si_personne_n_a_trouve():
    """La réponse était peut-être absente du corpus : ce n'est pas la faute
    de la stratégie."""
    tally = classify_errors(
        HELDOUT[0], _row(searches=1), Score(accuracy=0.0),
        best_searches=None, someone_found=False,
    )
    assert "arret_trop_tot" not in tally.kinds


def test_recherche_inutile_compte_les_recherches_en_trop():
    tally = classify_errors(
        HELDOUT[0], _row(searches=5), Score(accuracy=1.0),
        best_searches=2, someone_found=True,
    )
    assert "recherche_inutile" in tally.kinds
    assert tally.wasted_searches == 3


def test_mauvaise_detection_de_suffisance():
    outcome = _row(searches=1, stop_code="information_suffisante")
    tally = classify_errors(
        HELDOUT[0], outcome, Score(accuracy=0.0),
        best_searches=2, someone_found=True,
    )
    assert "mauvaise_detection_suffisance" in tally.kinds


def test_fausse_contradiction_sur_une_tache_sans_piege():
    sans_piege = next(t for t in HELDOUT if not t.distractors)
    tally = classify_errors(
        sans_piege, _row(searches=2, contradictions=["a ≠ b"]), Score(accuracy=1.0),
        best_searches=2, someone_found=True,
    )
    assert "fausse_contradiction" in tally.kinds


def test_contradiction_manquee_quand_une_valeur_piege_est_avancee():
    avec_piege = next(t for t in HELDOUT if t.distractors)
    tally = classify_errors(
        avec_piege, _row(searches=2), Score(accuracy=1.0, noise=1.0),
        best_searches=2, someone_found=True,
    )
    assert "contradiction_manquee" in tally.kinds


# --- Comparaison appariée ------------------------------------------------------


def _paire(task_id, seed, strategy, searches, net):
    task = next(t for t in HELDOUT if t.id == task_id)
    return Row(
        task=task,
        outcome=Outcome(strategy=strategy, task_id=task_id, seed=seed, searches=searches),
        score=Score(accuracy=net),
    )


def test_les_graines_sont_moyennees_avant_comparaison():
    """Cinq graines d'une même tâche ne font pas cinq observations."""
    rows = []
    for seed in (1, 2):
        rows.append(_paire("prix_vanille", seed, "adaptive_reasoning", 1, 1.0))
        rows.append(_paire("prix_vanille", seed, "fixed", 3, 1.0))
    resultat = h2.paired(rows, "adaptive_reasoning", "fixed")
    assert resultat.n == 1                      # une tâche, pas deux
    assert resultat.search_delta == pytest.approx(-2.0)


def test_la_reduction_est_calculee_sur_les_totaux():
    rows = [
        _paire("prix_vanille", 1, "adaptive_reasoning", 1, 1.0),
        _paire("prix_vanille", 1, "fixed", 4, 1.0),
    ]
    resultat = h2.paired(rows, "adaptive_reasoning", "fixed")
    assert resultat.reduction == pytest.approx(0.75)


# --- Verdict -------------------------------------------------------------------


def _resultat(reduction, p_value, ci_bas, n=10, wins=9, losses=0):
    return h2.PairedResult(
        challenger="adaptive_reasoning", reference="fixed", unit="tâche", n=n,
        accuracy_delta=(ci_bas + 0.02), accuracy_ci=(ci_bas, ci_bas + 0.1),
        search_delta=-1.5, search_ci=(-2.0, -1.0),
        search_ratio=1 - reduction, reduction=reduction,
        wins=wins, losses=losses, ties=n - wins - losses, p_value=p_value,
    )


def test_h2_soutenue_quand_les_deux_criteres_tiennent():
    verdict = h2.judge_h2(_resultat(0.5, 0.01, -0.01), _resultat(0.5, 0.01, -0.01))
    assert verdict.status == "soutenue"
    assert verdict.criterion_a and verdict.criterion_b


def test_h2_refutee_si_la_reduction_est_trop_faible():
    verdict = h2.judge_h2(_resultat(0.05, 0.01, 0.0), _resultat(0.05, 0.5, 0.0))
    assert verdict.status == "refutee"


def test_h2_refutee_si_l_ecart_n_est_pas_significatif():
    verdict = h2.judge_h2(_resultat(0.5, 0.40, 0.0), _resultat(0.5, 0.40, 0.0))
    assert verdict.status == "refutee"


def test_h2_partielle_si_l_economie_se_paie_en_exactitude():
    verdict = h2.judge_h2(_resultat(0.5, 0.01, -0.30), _resultat(0.5, 0.01, -0.30))
    assert verdict.status == "partielle"
    assert verdict.criterion_b and not verdict.criterion_a


def test_h2_partielle_si_seule_la_calibration_montre_l_effet():
    verdict = h2.judge_h2(_resultat(0.05, 0.5, 0.0), _resultat(0.5, 0.01, 0.0))
    assert verdict.status == "partielle"


def test_le_verdict_previent_quand_les_deux_jeux_divergent():
    verdict = h2.judge_h2(_resultat(0.05, 0.5, 0.0), _resultat(0.5, 0.01, 0.0))
    assert any("ne disent pas la même chose" in w for w in verdict.warnings)


def test_le_verdict_ne_dit_jamais_prouvee():
    for status in ("soutenue", "partielle", "refutee"):
        libelle = h2.H2Verdict(status=status).label
        assert "PROUVÉE" not in libelle and "DÉMONTRÉE" not in libelle


# --- Coût ----------------------------------------------------------------------


def test_le_cout_estime_est_proportionnel_aux_jetons():
    assert h2._cost(1_000_000) == pytest.approx(h2.PRIX_PAR_MILLION_JETONS)
    assert h2._cost(0) == 0


def test_recherches_par_reponse_juste_est_indefini_sans_reponse_juste():
    rows = [_paire("prix_vanille", 1, "fixed", 3, 0.0)]
    stats = h2.summarize(rows, "fixed")
    assert stats.searches_per_correct == float("inf")
    assert stats.to_dict()["searches_per_correct"] is None
