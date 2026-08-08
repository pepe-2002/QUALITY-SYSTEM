"""FINAL_ANSWER_ACCURACY — ne compter que ce que l'utilisateur lit.

Ces tests portent sur les trois pannes que la métrique historique laissait
passer : une valeur cachée dans les traces, un aveu d'échec alors que la
réponse était connue, et une valeur fausse affichée pendant que la bonne
dormait dans les journaux.
"""

from __future__ import annotations

from ara.core.models import SourceDoc
from ara.lab.dataset import Gold, Task
from ara.lab.final_answer import final_answer_accuracy, user_facing
from ara.lab.harness import Outcome
from ara.lab.metrics import score

TACHE = Task(
    id="t", question="Combien coûte le billet ?",
    gold=[Gold("money", 15000, "15 000 FC")],
    distractors=[Gold("money", 9000, "9 000 FC (archive)")],
)

SOURCE = SourceDoc(
    url="https://s.test/a", title="Tarifs",
    text="Le billet coûte 15 000 francs comoriens.",
)


def _outcome(answer: str) -> Outcome:
    return Outcome(strategy="test", task_id="t", answer=answer, sources=[SOURCE])


# --- Découpage ------------------------------------------------------------------


def test_le_bilan_est_retire_de_la_partie_visible():
    texte = user_facing(
        "Le billet coûte 15 000 francs comoriens.\n\n"
        "## Déroulé de la recherche\n\n2 cycles, 3 sources."
    )
    assert "Déroulé" not in texte and "15 000" in texte


def test_les_sources_ne_sont_pas_la_reponse():
    assert "moheligo" not in user_facing(
        "Je n'ai pas trouvé.\n\n**Sources :**\n- moheligo.com"
    )


# --- Panne 1 : information cachée dans les traces -------------------------------


def test_une_valeur_cachee_dans_le_bilan_ne_compte_pas():
    """Le cœur de la nouvelle métrique."""
    outcome = _outcome(
        "Les traversées sont quotidiennes.\n\n"
        "## Déroulé de la recherche\n\nFait retenu : 15 000 francs comoriens."
    )
    note = final_answer_accuracy(TACHE, outcome)
    assert note.accuracy == 0.0
    assert note.hidden == ["15 000 FC"]


def test_la_metrique_historique_comptait_cette_valeur():
    """La différence entre les deux métriques, rendue explicite.

    Ce test échouerait si quelqu'un « corrigeait » la métrique historique —
    ce qui réécrirait H1 et H2.
    """
    outcome = _outcome(
        "Les traversées sont quotidiennes.\n\n"
        "## Déroulé de la recherche\n\nFait retenu : 15 000 francs comoriens."
    )
    assert score(TACHE, outcome).accuracy == 1.0
    assert final_answer_accuracy(TACHE, outcome).accuracy == 0.0


# --- Panne 2 : « je n'ai pas trouvé » alors qu'il savait ------------------------


def test_un_aveu_d_echec_alors_que_la_valeur_etait_connue():
    outcome = _outcome(
        "Je n'ai pas trouvé le tarif.\n\n"
        "## Déroulé de la recherche\n\n15 000 francs comoriens relevés."
    )
    note = final_answer_accuracy(TACHE, outcome)
    assert note.admits_failure
    assert note.silent_success, "le système savait et s'est tu"


def test_un_aveu_d_echec_sincere_n_est_pas_un_silence_coupable():
    outcome = Outcome(
        strategy="test", task_id="t",
        answer="Je n'ai pas trouvé le tarif.",
        sources=[SourceDoc(url="https://s.test/b", title="x", text="Rien d'utile.")],
    )
    note = final_answer_accuracy(TACHE, outcome)
    assert note.admits_failure and not note.silent_success


# --- Panne 3 : valeur fausse affichée, bonne valeur dans les traces -------------


def test_une_valeur_fausse_affichee_malgre_la_bonne_dans_les_traces():
    outcome = _outcome(
        "Le billet coûte 9 000 francs comoriens.\n\n"
        "## Déroulé de la recherche\n\nAutre valeur relevée : 15 000 francs comoriens."
    )
    note = final_answer_accuracy(TACHE, outcome)
    assert note.wrong == ["9 000 FC (archive)"]
    assert note.confidently_wrong


# --- Réussite -------------------------------------------------------------------


def test_une_valeur_affichee_compte():
    outcome = _outcome("Le billet coûte 15 000 francs comoriens.")
    note = final_answer_accuracy(TACHE, outcome)
    assert note.accuracy == 1.0
    assert not note.hidden and not note.wrong
    assert not note.silent_success and not note.confidently_wrong


def test_la_metrique_est_serialisable():
    note = final_answer_accuracy(TACHE, _outcome("15 000 francs comoriens."))
    donnees = note.to_dict()
    assert donnees["final_answer_accuracy"] == 1.0
    assert set(donnees) >= {"silent_success", "confidently_wrong", "hidden"}


# --- Séparation d'avec l'historique ---------------------------------------------


def test_la_metrique_historique_reste_intacte():
    """Elle n'est ni modifiée ni remplacée : H1 et H2 gardent la leur."""
    from ara.lab import metrics

    assert hasattr(metrics, "score")
    outcome = _outcome("Le billet coûte 15 000 francs comoriens.")
    assert metrics.score(TACHE, outcome).accuracy == 1.0
