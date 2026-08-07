"""Automatisation : routines programmées et ordonnanceur (Phase 5).

C'est la partie du système qui agit **sans demande immédiate**. Elle n'accorde
aucun droit nouveau : une routine emprunte le même orchestrateur, la même liste
blanche d'outils et les mêmes confirmations humaines qu'une demande tapée à la
main.
"""

from .routines import Routine, RoutineError, RoutineStore, build_routine
from .schedule import Schedule, parse_schedule
from .scheduler import Scheduler

__all__ = [
    "Routine",
    "RoutineError",
    "RoutineStore",
    "Schedule",
    "Scheduler",
    "build_routine",
    "parse_schedule",
]
