"""Agents. En Phase 1 : planificateur, collecte de sources, agent documentaire.

Les agents RESEARCH (boucle adaptative), CREATIVE, CRITIC et LAB arrivent aux
phases suivantes — la spec §21 interdit de les construire avant que le MVP
fonctionne.
"""

from .orchestrator import Orchestrator, run_task

__all__ = ["Orchestrator", "run_task"]
