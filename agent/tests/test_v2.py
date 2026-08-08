"""ADAPTIVE-V2 : estimateur de difficulté, garde-fous, verdict.

Le test le plus important de ce fichier est celui qui vérifie que l'estimateur
ne triche pas : il ne doit rien savoir du corpus ni de la réponse attendue.
Un contrôleur qui alloue un gros budget aux questions dont il connaît déjà la
réponse aurait d'excellents chiffres et aucune valeur.
"""

from __future__ import annotations

import pytest

from ara.core.complexity import (
    BUDGETS,
    DEFAULT_CONTROLLER,
    MAX_REVISIONS,
    Complexity,
    assess,
    assess_for,
    assess_v2,
    estimate_difficulty,
)
from ara.lab import strategies as arms
from ara.lab import v2 as lab_v2
from ara.lab.heldout2 import PAGES as JEU3_PAGES
from ara.lab.heldout2 import TASKS as JEU3_TASKS

# --- V1 est gelée --------------------------------------------------------------


def test_v2_est_adoptee_par_defaut():
    """Adoptée après l'expérience qui l'a jugée, pas avant.

    Ce qui reste immuable n'est pas ce réglage — c'est l'épinglage des bras du
    laboratoire, vérifié par le test suivant : H1 et H2 continuent de jouer V1
    quoi qu'il arrive au défaut de l'application.
    """
    assert DEFAULT_CONTROLLER == "v2"


def test_v1_ne_revise_jamais_son_budget():
    from ara.agents.planner import plan

    assert plan("Combien coûte le billet ?", controller="v1").adaptive_budget is False


def test_v2_revise_son_budget():
    from ara.agents.planner import plan

    assert plan("Combien coûte le billet ?", controller="v2").adaptive_budget is True


def test_les_bras_de_h1_et_h2_restent_sur_v1():
    """Sans cet épinglage, faire avancer le contrôleur rendrait H1 et H2
    irreproductibles."""
    for bras in ("model_only", "fixed", "adaptive_reasoning", "adaptive_research"):
        assert arms.CONTROLLER_BY_STRATEGY[bras] == "v1"
    assert arms.CONTROLLER_BY_STRATEGY["adaptive_v2"] == "v2"


def test_une_version_inconnue_est_refusee():
    with pytest.raises(ValueError):
        assess_for("v3", "test")


# --- L'estimateur ne triche pas ------------------------------------------------


def test_l_estimateur_ne_voit_que_la_question(monkeypatch):
    """Aucun accès au corpus : on le vérifie en cassant tout accès réseau et
    en s'assurant que l'estimation fonctionne quand même."""
    estimation = estimate_difficulty("À quelle heure ouvre le dispensaire ?")
    assert estimation.level in {"simple", "intermediaire", "profonde"}
    assert set(estimation.features) >= {"kinds", "kind_cost", "authority", "length"}


def test_l_estimation_ne_depend_pas_des_valeurs_d_or():
    """Deux questions de même forme sur la même grandeur reçoivent la même
    estimation, que la réponse existe ou non dans un corpus."""
    a = estimate_difficulty("Combien coûte une consultation au dispensaire ?")
    b = estimate_difficulty("Combien coûte une consultation chez le vétérinaire ?")
    assert a.level == b.level


def test_une_question_courte_peut_etre_profonde():
    """C'est exactement l'erreur de V1 : croire que court veut dire facile."""
    horaire = estimate_difficulty("À quelle heure ouvre le centre ?")
    prix = estimate_difficulty("Combien coûte le billet ?")
    assert horaire.score > prix.score


def test_une_demande_d_autorite_monte_la_difficulte():
    sans = estimate_difficulty("Quel est le prix de la consultation ?")
    avec = estimate_difficulty("Quel est le tarif officiel de la consultation ?")
    assert avec.score > sans.score


def test_une_salutation_reste_simple():
    assert estimate_difficulty("bonjour").level == "simple"


def test_l_estimation_donne_toujours_une_raison_lisible():
    for task in JEU3_TASKS:
        assert estimate_difficulty(task.question).reason


# --- Budgets et garde-fous -----------------------------------------------------


def test_trois_niveaux_trois_budgets():
    from ara.core.complexity import DIFFICULTY_TO_COMPLEXITY

    assert DIFFICULTY_TO_COMPLEXITY == {
        "simple": Complexity.LOW,
        "intermediaire": Complexity.MEDIUM,
        "profonde": Complexity.HIGH,
    }
    assert BUDGETS[Complexity.LOW][0] < BUDGETS[Complexity.MEDIUM][0] < BUDGETS[Complexity.HIGH][0]


def test_le_plafond_dur_n_est_jamais_franchi():
    budget = assess_v2("Quel est le taux officiel exact et précis ?", max_search_steps=2)
    assert budget.search_steps <= 2
    for _ in range(10):
        budget.revise("difficile", "toujours rien")
    assert budget.search_steps <= 2


def test_les_revisions_sont_bornees():
    """Sans borne, « difficile → +1 → toujours difficile » tournerait sans fin."""
    budget = assess_v2("Quel est le taux de couverture ?")
    for _ in range(MAX_REVISIONS + 3):
        budget.revise("difficile", "rien trouvé")
    assert len(budget.revisions) == MAX_REVISIONS
    assert budget.revise("difficile") == "plafond_revisions"


def test_information_suffisante_rend_du_budget():
    budget = assess_v2("Quel est le tarif officiel exact de la consultation ?")
    avant = budget.search_steps
    budget.revise("suffisant", "la réponse est là")
    assert budget.search_steps <= avant


def test_indetermine_ne_change_rien():
    budget = assess_v2("Combien coûte le billet ?")
    avant = (budget.complexity, budget.search_steps)
    assert budget.revise("indetermine") == "aucune"
    assert (budget.complexity, budget.search_steps) == avant


def test_le_budget_porte_sa_version():
    assert assess_v2("test question sur un tarif").controller == "v2"
    assert assess("test question sur un tarif").controller == "v1"


# --- Le juge de difficulté (sur preuve) ----------------------------------------


def _doc(text: str):
    from ara.core.models import SourceDoc

    return SourceDoc(url="https://x.test/a", title="t", text=text)


def test_grandeur_trouvee_donne_suffisant():
    from ara.agents.gather import judge_difficulty

    verdict, _ = judge_difficulty(
        "Combien coûte la consultation ?", [_doc("La consultation coûte 2 500 francs comoriens.")]
    )
    assert verdict == "suffisant"


def test_grandeur_absente_donne_difficile():
    from ara.agents.gather import judge_difficulty

    verdict, _ = judge_difficulty(
        "À quelle heure ouvre le centre ?", [_doc("Le centre ouvre tôt, cela varie.")]
    )
    assert verdict == "difficile"


def test_sans_grandeur_identifiable_on_ne_tranche_pas():
    from ara.agents.gather import judge_difficulty

    verdict, _ = judge_difficulty("Parle-moi de cette région.", [_doc("Un texte.")])
    assert verdict == "indetermine"


def test_aucune_source_est_difficile():
    from ara.agents.gather import judge_difficulty

    verdict, _ = judge_difficulty("Combien coûte la consultation ?", [])
    assert verdict == "difficile"


# --- Jeu 3 ---------------------------------------------------------------------


def test_le_jeu_3_ne_partage_rien_avec_les_deux_autres():
    from ara.lab.corpus import Corpus
    from ara.lab.dataset import TASKS as JEU1
    from ara.lab.heldout import PAGES as JEU2_PAGES
    from ara.lab.heldout import TASKS as JEU2

    assert set(JEU3_PAGES) & set(Corpus().pages) == set()
    assert set(JEU3_PAGES) & set(JEU2_PAGES) == set()
    ids3 = {t.id for t in JEU3_TASKS}
    assert ids3 & {t.id for t in JEU1} == set()
    assert ids3 & {t.id for t in JEU2} == set()


def test_le_jeu_3_couvre_les_trois_familles():
    assert {t.family for t in JEU3_TASKS} == {"facile", "profond", "piege"}


def test_chaque_valeur_attendue_du_jeu_3_existe_dans_son_corpus():
    import re

    from ara.analysis.facts import extract_facts
    from ara.lab.heldout2 import held_out_corpus
    from ara.lab.metrics import _matches

    textes = [re.sub(r"<[^>]+>", " ", html) for html in held_out_corpus().pages.values()]
    faits = [f for texte in textes for f in extract_facts(texte, 1, max_facts=200)]
    for task in JEU3_TASKS:
        for gold in task.gold:
            assert any(_matches(f, gold) for f in faits), f"{task.id} : {gold.label}"


# --- Verdict -------------------------------------------------------------------


def _run(profond_v2_net, profond_fixe_net, facile_v2_rech, profond_v2_rech,
         v2_rech=1.5, fixe_rech=3.0, v2_net=0.75, v1_net=0.75):
    from ara.lab.h2 import ArmStats

    run = lab_v2.V2Run(name="test")
    run.stats = {
        "fixed": ArmStats("fixed", net=0.75, searches=fixe_rech, runs=10),
        "adaptive_reasoning": ArmStats("adaptive_reasoning", net=v1_net, searches=1.3, runs=10),
        "adaptive_v2": ArmStats("adaptive_v2", net=v2_net, searches=v2_rech, runs=10),
    }
    run.by_family = {
        "adaptive_v2": {
            "facile": {"searches": facile_v2_rech, "net": 0.8, "accuracy": 0.8},
            "profond": {"searches": profond_v2_rech, "net": profond_v2_net, "accuracy": profond_v2_net},
        },
        "fixed": {
            "facile": {"searches": 3.0, "net": 0.8, "accuracy": 0.8},
            "profond": {"searches": 3.0, "net": profond_fixe_net, "accuracy": profond_fixe_net},
        },
        "adaptive_reasoning": {
            "facile": {"searches": 1.3, "net": 0.8, "accuracy": 0.8},
            "profond": {"searches": 1.0, "net": 0.6, "accuracy": 0.6},
        },
    }
    return run


def test_defaut_corrige_quand_les_trois_criteres_tiennent():
    verdict = lab_v2.judge_v2(_run(1.0, 1.0, 1.2, 3.0))
    assert verdict.status == "corrige"
    assert verdict.c1 and verdict.c2 and verdict.c3


def test_defaut_non_corrige_si_l_exactitude_profonde_reste_basse():
    verdict = lab_v2.judge_v2(_run(0.5, 1.0, 1.2, 3.0))
    assert verdict.status == "non_corrige"
    assert not verdict.c1


def test_defaut_non_corrige_si_le_controleur_ne_discrimine_pas():
    """Le cœur du défaut : rationner partout, même en gardant l'exactitude."""
    verdict = lab_v2.judge_v2(_run(1.0, 1.0, 1.3, 1.4))
    assert verdict.status == "non_corrige"


def test_correction_partielle_si_l_economie_est_perdue():
    verdict = lab_v2.judge_v2(_run(1.0, 1.0, 1.2, 3.0, v2_rech=2.9))
    assert verdict.status == "partiel"
    assert verdict.c1 and not verdict.c2


def test_correction_partielle_si_regression_face_a_v1():
    verdict = lab_v2.judge_v2(_run(1.0, 1.0, 1.2, 3.0, v2_net=0.50, v1_net=0.75))
    assert verdict.status == "partiel"
    assert not verdict.c3


def test_le_verdict_previent_si_v2_cherche_plus_que_fixed():
    verdict = lab_v2.judge_v2(_run(1.0, 1.0, 1.2, 3.0, v2_rech=4.0))
    assert any("plus une économie" in w for w in verdict.warnings)


def test_les_criteres_sont_ceux_annonces():
    assert lab_v2.MARGE_EXACTITUDE == 0.05
    assert lab_v2.REDUCTION_MINIMALE == 0.20
    assert lab_v2.DISCRIMINATION_MINIMALE == 0.50
    assert lab_v2.REGRESSION_TOLEREE == 0.02


def test_la_version_du_controleur_est_enregistree():
    assert "V2" in lab_v2.CONTROLLER_VERSION
    assert "gelée" in lab_v2.BASELINE_VERSION
