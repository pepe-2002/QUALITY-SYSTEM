"""RESEARCH LAB (spec §18) — mesurer, et surtout tenter de réfuter.

    « Le système doit chercher à réfuter l'hypothèse, pas à la confirmer. »

Le laboratoire compare quatre stratégies sur un corpus figé :

    MODEL ONLY          — répondre sans chercher
    FIXED REASONING     — même budget pour tout
    ADAPTIVE REASONING  — budget variable selon la difficulté
    ADAPTIVE RESEARCH   — chercher uniquement lorsque nécessaire

L'hypothèse et ses conditions de réfutation sont écrites dans le code avant
toute exécution, et le verdict ne dit jamais « confirmée ».
"""

from .corpus import Corpus
from .dataset import TASKS, Gold, Task
from .experiment import HYPOTHESIS, ExperimentResult, Hypothesis, run_experiment
from .metrics import Score, score
from .report import render

__all__ = [
    "Corpus", "TASKS", "Task", "Gold", "HYPOTHESIS", "Hypothesis",
    "ExperimentResult", "run_experiment", "Score", "score", "render",
]
