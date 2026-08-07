"""Contexte d'exécution d'une tâche : tout ce qu'un agent ou un outil reçoit.

Regrouper ces objets évite les variables globales et rend chaque tâche
isolable — condition nécessaire pour que le RESEARCH LAB (spec §18) puisse
rejouer une tâche avec d'autres réglages.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from ..providers.llm.base import LLMProvider
from ..providers.search.base import SearchProvider
from ..providers.storage import Storage
from .complexity import TaskBudget
from .config import Settings
from .errors import BudgetExceeded
from .events import EventBus, Stage, Status
from .journal import ResearchLog
from .permissions import PermissionManager


@dataclass
class TaskContext:
    task_id: str
    prompt: str
    settings: Settings
    bus: EventBus
    journal: ResearchLog
    permissions: PermissionManager
    storage: Storage
    llm: LLMProvider
    search: SearchProvider
    budget: TaskBudget
    started_at: float = field(default_factory=time.monotonic)
    notices: list[str] = field(default_factory=list)

    # -- garde-fous d'arrêt ------------------------------------------------

    def elapsed(self) -> float:
        return time.monotonic() - self.started_at

    def check_deadline(self) -> None:
        """Le système doit savoir s'arrêter (règle finale de la spec)."""
        if self.elapsed() > self.settings.max_task_seconds:
            raise BudgetExceeded(
                f"Temps maximal atteint ({self.settings.max_task_seconds}s). "
                "Résultat partiel conservé."
            )

    # -- raccourcis --------------------------------------------------------

    def notice(self, message: str) -> None:
        """Message informatif destiné à l'utilisateur (dégradation, repli…)."""
        if message and message not in self.notices:
            self.notices.append(message)
            self.bus.log(message, kind="notice")

    def stage(self, stage: Stage, status: Status, message: str = "", **data: Any) -> None:
        self.bus.stage(stage, status, message, **data)
