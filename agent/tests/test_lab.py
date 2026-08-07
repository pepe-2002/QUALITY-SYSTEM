"""RESEARCH LAB (spec §18) — l'expérience, et sa capacité à dire non.

Le test le plus important de ce fichier n'est pas qu'une stratégie gagne :
c'est que la machinerie **sache réfuter**. Un laboratoire incapable de conclure
contre l'hypothèse de son auteur ne mesure rien.
"""

from __future__ import annotations

import json

import pytest

from ara.lab import experiment as lab
from ara.lab import strategies as arms
from ara.lab.corpus import Corpus
from ara.lab.dataset import TASKS, Gold, Task
from ara.lab.harness import Outcome
from ara.lab.metrics import Row, score
from ara.lab.report import render


@pytest.fixture
def corpus():
    return Corpus()


# --- Corpus figé ---------------------------------------------------------------


def test_le_corpus_repond_aux_requetes_proches(corpus):
    urls = corpus.search("tarif de la traversée Ouroveni Hoani")
    assert "https://compagnie-a.test/tarifs" in urls


def test_le_corpus_est_stable(corpus):
    """Deux exécutions doivent voir le même web, sinon rien n'est comparable."""
    assert corpus.search("distance Grande Comore Mohéli") == corpus.search(
        "distance Grande Comore Mohéli"
    )


def test_une_page_absente_nest_pas_inventee(corpus):
    assert corpus.fetch("https://inexistante.test/x") is None


# --- Stratégies ----------------------------------------------------------------


@pytest.mark.parametrize("strategy", arms.STRATEGIES)
def test_chaque_strategie_produit_un_resultat(strategy, corpus, isolated_settings):
    task = next(t for t in TASKS if t.id == "tarif")
    outcome = arms.run(strategy, task, isolated_settings, corpus)
    assert outcome.strategy == strategy
    assert outcome.latency_ms >= 0
    assert outcome.error == ""


def test_model_only_ne_cherche_jamais(corpus, isolated_settings):
    task = next(t for t in TASKS if t.id == "tarif")
    outcome = arms.run("model_only", task, isolated_settings, corpus)
    assert outcome.searches == 0 and outcome.fetches == 0


def test_fixed_depense_le_meme_budget_partout(corpus, isolated_settings):
    """C'est la définition même de la stratégie fixe."""
    budgets = {
        arms.run("fixed", task, isolated_settings, corpus).searches
        for task in TASKS[:4]
    }
    assert budgets == {arms.FIXED_STEPS}


def test_adaptive_reasoning_module_son_budget(corpus, isolated_settings):
    """Budget variable selon la difficulté : deux questions, deux budgets."""
    budgets = [
        arms.run("adaptive_reasoning", task, isolated_settings, corpus).searches
        for task in TASKS
    ]
    assert len(set(budgets)) > 1, "un budget constant n'est pas adaptatif"


def test_adaptive_research_ne_cherche_que_si_necessaire(corpus, isolated_settings):
    """Règle du propriétaire : pas de relance sans raison constatée."""
    facile = next(t for t in TASKS if t.id == "tarif")
    outcome = arms.run("adaptive_research", facile, isolated_settings, corpus)
    assert outcome.stopped_because
    assert outcome.searches <= arms.FIXED_STEPS


# --- Mesures -------------------------------------------------------------------


def test_la_bonne_valeur_est_reconnue():
    task = Task("t", "Combien ?", [Gold("money", 15000, "15 000 FC")])
    outcome = Outcome("x", "t", answer="Le billet coûte 15 000 francs comoriens [S1].")
    result = score(task, outcome)
    assert result.accuracy == 1.0 and result.noise == 0.0


def test_une_valeur_absente_est_comptee_comme_manquee():
    task = Task("t", "Combien ?", [Gold("money", 15000, "15 000 FC")])
    result = score(task, Outcome("x", "t", answer="Je ne sais pas."))
    assert result.accuracy == 0.0 and result.missed


def test_une_valeur_piege_est_penalisee():
    task = Task(
        "t", "Combien ?", [Gold("money", 15000, "15 000 FC")],
        distractors=[Gold("money", 9000, "9 000 FC")],
    )
    outcome = Outcome("x", "t", answer="Le billet coûte 15 000 FC, ou 9 000 FC [S1].")
    result = score(task, outcome)
    assert result.accuracy == 1.0 and result.noise == 1.0
    assert result.net < result.accuracy, "avancer une fausse valeur doit coûter"


def test_avouer_ce_qui_manque_vaut_mieux_que_se_taire():
    task = Task("t", "Combien ?", [Gold("money", 15000, "15 000 FC")])
    muet = score(task, Outcome("x", "t", answer="Rien trouvé."))
    honnete = score(task, Outcome("x", "t", answer="Rien trouvé.", gaps=["prix absent"]))
    assert honnete.quality > muet.quality


# --- Statistiques ---------------------------------------------------------------


def test_test_des_signes_sur_valeurs_connues():
    assert lab.sign_test(0, 0) == 1.0
    assert lab.sign_test(5, 0) == pytest.approx(2 / 32)
    assert lab.sign_test(3, 3) == 1.0


def test_le_hasard_est_reproductible():
    diffs = [0.1, -0.2, 0.3, 0.0, 0.5]
    assert lab.bootstrap_ci(diffs) == lab.bootstrap_ci(diffs)


def test_un_intervalle_vide_ne_casse_pas():
    assert lab.bootstrap_ci([]) == (0.0, 0.0)


# --- Le verdict doit pouvoir dire NON ------------------------------------------


def _resultat_bidon(gain: float, cost_ratio: float, trap: float = 0.0,
                    p: float = 0.01) -> lab.ExperimentResult:
    result = lab.ExperimentResult(hypothesis=lab.HYPOTHESIS)
    result.comparison = lab.Comparison(
        challenger="adaptive_research", reference="fixed",
        wins=8, losses=0, ties=0, mean_gain=gain, ci=(gain - 0.01, gain + 0.01),
        p_value=p, cost_ratio=cost_ratio, trap_gain=trap,
    )
    return result


def test_un_gain_insuffisant_refute():
    verdict = lab.judge(_resultat_bidon(gain=0.01, cost_ratio=1.0), lab.HYPOTHESIS)
    assert verdict.status == "refutee"
    assert "gain d'exactitude" in verdict.reasons[0]


def test_un_surcout_excessif_refute():
    verdict = lab.judge(_resultat_bidon(gain=0.5, cost_ratio=3.0), lab.HYPOTHESIS)
    assert verdict.status == "refutee"
    assert "coût" in verdict.reasons[0]


def test_une_degradation_sur_les_pieges_refute():
    """Nuire là où chercher plus est inutile suffit à réfuter."""
    verdict = lab.judge(
        _resultat_bidon(gain=0.5, cost_ratio=1.0, trap=-0.2), lab.HYPOTHESIS
    )
    assert verdict.status == "refutee"
    assert "pièges" in verdict.reasons[0]


def test_sans_signification_on_ne_conclut_pas():
    verdict = lab.judge(_resultat_bidon(gain=0.5, cost_ratio=1.0, p=0.9), lab.HYPOTHESIS)
    assert verdict.status == "non_concluante"


def test_le_verdict_ne_dit_jamais_confirmee():
    verdict = lab.judge(_resultat_bidon(gain=0.5, cost_ratio=1.0), lab.HYPOTHESIS)
    assert verdict.status == "non_refutee"
    assert "confirm" not in verdict.label.lower()
    assert verdict.warnings, "une non-réfutation doit s'accompagner de ses réserves"


# --- Expérience complète --------------------------------------------------------


@pytest.fixture
def experience(isolated_settings, corpus):
    import dataclasses

    settings = dataclasses.replace(isolated_settings, search_delay=0)
    return lab.run_experiment(settings=settings, corpus=corpus)


def test_lexperience_couvre_toutes_les_taches(experience):
    assert len(experience.rows) == len(TASKS) * len(arms.STRATEGIES)


def test_chercher_vaut_mieux_que_ne_pas_chercher(experience):
    """Le socle : si MODEL ONLY faisait aussi bien, tout le projet serait vain."""
    sans = experience.summary("model_only")["net"]
    avec = experience.summary("fixed")["net"]
    assert avec > sans


def test_lexperience_rend_un_verdict_motive(experience):
    assert experience.verdict is not None
    assert experience.verdict.reasons or experience.verdict.warnings
    assert experience.cost_verdict is not None


def test_lexperience_est_reproductible(isolated_settings, corpus):
    import dataclasses

    settings = dataclasses.replace(isolated_settings, search_delay=0)
    a = lab.run_experiment(settings=settings, corpus=Corpus())
    b = lab.run_experiment(settings=settings, corpus=Corpus())
    assert a.comparison.to_dict() == b.comparison.to_dict()
    assert a.verdict.status == b.verdict.status


def test_le_rapport_expose_lhypothese_avant_le_verdict(experience):
    rapport = render(experience)
    assert rapport.index("Hypothèse pré-enregistrée") < rapport.index("Résultats par stratégie")
    assert "Ce que cette expérience ne prouve pas" in rapport
    assert "Conditions de réfutation" in rapport


def test_le_resultat_est_serialisable(experience):
    json.dumps(experience.to_dict(), ensure_ascii=False)
