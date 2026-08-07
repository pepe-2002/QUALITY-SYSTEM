"""Prévenir le propriétaire — en passant par le registre, comme tout le reste.

Il aurait été plus court d'appeler `notify_phone()` directement depuis
l'ordonnanceur. Ce raccourci aurait créé exactement le trou que la spec §16
interdit : un chemin d'exécution où un outil s'exécute sans être autorisé.
Une routine qui tourne à 7 h du matin est justement le cas où personne ne
regarde — c'est là que la règle doit tenir, pas seulement dans les tests.

D'où ce module : il fabrique le contexte minimal nécessaire pour que la
notification passe par :class:`ToolBox`, donc par la liste blanche, le journal
et la gestion d'erreur habituels.
"""

from __future__ import annotations

from ..core.complexity import Complexity, TaskBudget
from ..core.config import Settings
from ..core.context import TaskContext
from ..core.events import EventBus
from ..core.journal import ResearchLog
from ..core.permissions import PermissionManager
from ..providers.llm import get_llm
from ..providers.search import get_search
from ..providers.storage import get_storage
from ..tools.registry import ToolBox


def routine_toolbox(
    settings: Settings,
    permissions: PermissionManager,
    *,
    task_id: str = "routine",
    prompt: str = "notification de routine",
) -> ToolBox:
    """Boîte à outils d'un contexte hors tâche (notification d'une routine).

    Le contexte est réel mais volontairement pauvre : budget nul, moteur
    hors-ligne, aucun accès réseau prévu. Il ne sert qu'à faire respecter les
    contrôles, pas à travailler.
    """
    llm, _ = get_llm("offline")
    search, _ = get_search(settings.search_provider)
    ctx = TaskContext(
        task_id=task_id,
        prompt=prompt,
        settings=settings,
        bus=EventBus(),
        journal=ResearchLog(task_id=task_id, task=prompt),
        permissions=permissions,
        storage=get_storage(settings.storage_provider),
        llm=llm,
        search=search,
        budget=TaskBudget(
            complexity=Complexity.LOW,
            search_steps=0,
            analysis_passes=0,
            signals={},
            max_search_steps=0,
        ),
    )
    return ToolBox(ctx)


__all__ = ["routine_toolbox"]
