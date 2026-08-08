"""Attribution d'une panne à une étape du pipeline.

Ces tests vérifient que chaque règle range bien l'échec là où l'information a
été perdue — et surtout qu'elle s'arrête à la **première** étape fautive.
Sans cet ordre, un même échec compterait plusieurs fois et le diagnostic ne
dirait plus où porter l'effort.
"""

from __future__ import annotations

from ara.core.models import SourceDoc
from ara.lab.dataset import Gold, Task
from ara.lab.failures import STAGES, diagnose, tally
from ara.lab.harness import Outcome
from ara.lab.metrics import Score, score


def _task(**kwargs) -> Task:
    base = dict(
        id="t", question="Combien coûte le billet ?",
        gold=[Gold("money", 15000, "15 000 FC")], family="facile",
    )
    base.update(kwargs)
    return Task(**base)


def _outcome(answer: str, *textes: str, contradictions=()) -> Outcome:
    return Outcome(
        strategy="test", task_id="t", answer=answer,
        sources=[
            SourceDoc(url=f"https://s{i}.test/a", title="s", text=texte)
            for i, texte in enumerate(textes, start=1)
        ],
        contradictions=list(contradictions),
    )


# --- Réussite ------------------------------------------------------------------


def test_une_bonne_reponse_n_est_pas_une_panne():
    task = _task()
    outcome = _outcome("Le billet coûte 15 000 francs comoriens.",
                       "Le billet coûte 15 000 francs comoriens.")
    verdict = diagnose(task, outcome, score(task, outcome))
    assert not verdict.failed and verdict.stage == "aucune"


# --- Les six étapes ------------------------------------------------------------


def test_recherche_quand_la_valeur_n_est_dans_aucune_source():
    task = _task()
    outcome = _outcome("Je n'ai rien trouvé.", "Les traversées sont fréquentes.")
    assert diagnose(task, outcome, score(task, outcome)).stage == "recherche"


def test_extraction_quand_la_valeur_est_ecrite_mais_mal_lue():
    """Le nombre est là, dans une unité que l'extracteur ne connaît pas."""
    task = _task()
    outcome = _outcome("Rien d'exploitable.", "Le billet coûte 15 000 balboas.")
    verdict = diagnose(task, outcome, score(task, outcome))
    assert verdict.stage == "extraction"
    assert "écrit dans une source" in verdict.reason


def test_contextualisation_quand_une_valeur_piege_est_avancee():
    """La bonne valeur était disponible ; c'est la mauvaise qui est servie."""
    task = _task(distractors=[Gold("money", 9000, "9 000 FC (archive)")])
    outcome = _outcome(
        "Le billet coûte 9 000 francs comoriens.",
        "Le billet coûte 15 000 francs comoriens.",
        "En 2019 le billet coûtait 9 000 francs comoriens.",
        contradictions=["15 000 ≠ 9 000"],
    )
    assert diagnose(task, outcome, score(task, outcome)).stage == "contextualisation"


def test_une_valeur_piege_sans_bonne_source_reste_une_panne_de_recherche():
    """Servir la mauvaise valeur faute d'avoir la bonne n'est pas un problème
    de contexte : la bonne n'était nulle part."""
    task = _task(distractors=[Gold("money", 9000, "9 000 FC (archive)")])
    outcome = _outcome(
        "Le billet coûte 9 000 francs comoriens.",
        "En 2019 le billet coûtait 9 000 francs comoriens.",
    )
    assert diagnose(task, outcome, score(task, outcome)).stage == "recherche"


def test_comparaison_quand_le_desaccord_n_est_pas_signale():
    """Les deux valeurs sont extraites, aucune contradiction annoncée."""
    task = _task(distractors=[Gold("money", 9000, "9 000 FC (archive)")])
    outcome = _outcome(
        "Les traversées sont fréquentes.",
        "Le billet coûte 15 000 francs comoriens.",
        "En 2019 le billet coûtait 9 000 francs comoriens.",
    )
    assert diagnose(task, outcome, score(task, outcome)).stage == "comparaison"


def test_raisonnement_quand_la_valeur_extraite_n_est_pas_retenue():
    task = _task()
    outcome = _outcome(
        "Les traversées ont lieu tous les jours.",
        "Le billet coûte 15 000 francs comoriens.",
    )
    assert diagnose(task, outcome, score(task, outcome)).stage == "raisonnement"


def test_limite_connue_la_generation_est_invisible_pour_la_metrique():
    """L'étape GÉNÉRATION existe dans le code mais ne peut pas être observée.

    L'exactitude est mesurée sur la réponse **entière**, bilan d'analyse
    compris. Une valeur qui n'apparaît que dans le bilan est donc comptée
    comme trouvée, et aucune panne n'est attribuée. Changer cela reviendrait à
    changer la métrique de H1 et H2 — donc à rendre leurs chiffres
    irreproductibles. La limite est documentée plutôt que contournée.
    """
    task = _task()
    outcome = _outcome(
        "Les traversées ont lieu tous les jours.\n\n"
        "## Déroulé de la recherche\n\nFait retenu : 15 000 francs comoriens.",
        "Le billet coûte 15 000 francs comoriens.",
    )
    assert diagnose(task, outcome, score(task, outcome)).stage == "aucune"


# --- Ordre du pipeline ---------------------------------------------------------


def test_une_valeur_jamais_trouvee_n_est_pas_imputee_a_l_extraction():
    """L'attribution s'arrête à la première étape fautive."""
    task = _task()
    outcome = _outcome("Rien.", "Aucun chiffre ici.")
    verdict = diagnose(task, outcome, score(task, outcome))
    assert verdict.stage == "recherche"


def test_le_bruit_prime_sur_le_raisonnement():
    """Avancer une valeur piège est une panne plus grave que ne rien dire."""
    task = _task(distractors=[Gold("money", 9000, "9 000 FC")])
    outcome = _outcome(
        "Le billet coûte 9 000 francs comoriens.",
        "Le billet coûte 15 000 francs comoriens. En 2019 : 9 000 francs comoriens.",
    )
    assert diagnose(task, outcome, score(task, outcome)).stage == "contextualisation"


# --- Reconnaissance des écritures de nombres -----------------------------------


def test_les_nombres_espaces_sont_reconnus_dans_le_texte_brut():
    """« 15 000 », « 15000 » : la même valeur, deux écritures."""
    task = _task()
    for ecriture in ("15 000", "15000", "15.000"):
        outcome = _outcome("Rien.", f"Le billet coûte {ecriture} balboas.")
        assert diagnose(task, outcome, score(task, outcome)).stage == "extraction", ecriture


def test_un_nombre_voisin_ne_compte_pas():
    task = _task()
    outcome = _outcome("Rien.", "Le billet coûte 150 000 balboas.")
    assert diagnose(task, outcome, score(task, outcome)).stage == "recherche"


# --- Comptage ------------------------------------------------------------------


def test_le_comptage_couvre_toutes_les_etapes():
    from ara.lab.failures import Diagnosis

    compte = tally([Diagnosis(stage, "") for stage in STAGES])
    assert set(compte) == set(STAGES)
    assert all(valeur == 1 for valeur in compte.values())


def test_les_six_etapes_sont_celles_demandees():
    assert STAGES == (
        "recherche", "extraction", "contextualisation",
        "comparaison", "raisonnement", "generation",
    )
