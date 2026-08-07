"""RESEARCH LAB (spec §18) — mesurer, et surtout tenter de réfuter.

    « Le système doit chercher à réfuter l'hypothèse, pas à la confirmer. »

Le laboratoire compare quatre stratégies sur un corpus figé :

    MODEL ONLY          — répondre sans chercher
    FIXED REASONING     — même budget pour tout
    ADAPTIVE REASONING  — budget variable selon la difficulté
    ADAPTIVE RESEARCH   — chercher uniquement lorsque nécessaire

L'hypothèse et ses conditions de réfutation sont écrites dans le code avant
toute exécution, et le verdict ne dit jamais « confirmée ».

La seconde hypothèse, H2, porte sur le **coût** plutôt que sur l'exactitude ;
elle a son jeu de test tenu à l'écart, ses graines et son propre rapport
(`h2.py`, `report_h2.py`). H1 n'est pas révisée pour autant.
"""

from .corpus import Corpus
from .dataset import TASKS, Gold, Task
from .experiment import HYPOTHESIS, ExperimentResult, Hypothesis, run_experiment
from .h2 import H2_STATEMENT, H2Result, run_h2
from .metrics import Score, score
from .report import render
from .report_h2 import render as render_h2

__all__ = [
    "Corpus", "TASKS", "Task", "Gold", "HYPOTHESIS", "Hypothesis",
    "ExperimentResult", "run_experiment", "Score", "score", "render",
    "H2_STATEMENT", "H2Result", "run_h2", "render_h2",
]
