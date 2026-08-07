"""Registre d'outils : déclaration, permissions, exécution, journalisation.

Point de passage **unique**. Un agent n'appelle jamais la fonction d'un outil
directement : il passe par :class:`ToolBox`, qui vérifie l'autorisation (§16),
demande la confirmation humaine si l'outil est sensible (§15), enregistre
l'usage dans le journal (§17) et convertit toute exception en erreur maîtrisée.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

from ..core.context import TaskContext
from ..core.errors import AraError, ToolError, ToolNotFound


@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., Any]
    params: dict[str, str] = field(default_factory=dict)
    #: action sensible → confirmation humaine obligatoire
    sensitive: bool = False
    #: dépend d'une ressource externe (clé d'API, service payant)
    requires_external: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "params": self.params,
            "sensitive": self.sensitive,
            "requires_external": self.requires_external,
        }


#: Registre global des outils déclarés
REGISTRY: dict[str, Tool] = {}


def tool(
    name: str,
    description: str,
    *,
    params: dict[str, str] | None = None,
    sensitive: bool = False,
    requires_external: bool = False,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Déclare une fonction comme outil.

    La fonction décorée reçoit toujours le contexte en premier argument :

        @tool("web_search", "Cherche sur le web", params={"query": "texte"})
        def web_search(ctx, query: str, limit: int = 8): ...
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        REGISTRY[name] = Tool(
            name=name,
            description=description,
            func=func,
            params=params or {},
            sensitive=sensitive,
            requires_external=requires_external,
        )
        return func

    return decorator


@dataclass
class ToolCall:
    """Trace d'un appel d'outil (pour le journal et le LAB)."""

    name: str
    ok: bool
    duration_ms: int
    error: str = ""


class ToolBox:
    """Vue d'un contexte de tâche sur les outils autorisés."""

    def __init__(self, ctx: TaskContext) -> None:
        self.ctx = ctx
        self.calls: list[ToolCall] = []

    def available(self) -> list[dict[str, Any]]:
        """Outils réellement utilisables dans cette session."""
        return [
            tool.to_dict()
            for tool in REGISTRY.values()
            if self.ctx.permissions.is_allowed(tool.name)
        ]

    def has(self, name: str) -> bool:
        return name in REGISTRY and self.ctx.permissions.is_allowed(name)

    def call(self, name: str, **params: Any) -> Any:
        """Exécute un outil après tous les contrôles.

        Lève `ToolNotFound`, `PermissionDenied`, `ApprovalRequired` ou
        `ToolError` — jamais d'exception brute.
        """
        entry = REGISTRY.get(name)
        if entry is None:
            raise ToolNotFound(f"Outil inconnu : {name}")

        # 1. autorisation + confirmation humaine
        self.ctx.permissions.guard(name, params)
        # 2. garde-fou temporel
        self.ctx.check_deadline()

        started = time.monotonic()
        try:
            result = entry.func(self.ctx, **params)
        except AraError as exc:
            self._record(name, False, started, str(exc))
            raise
        except TypeError as exc:
            self._record(name, False, started, str(exc))
            raise ToolError(f"Paramètres invalides pour « {name} » : {exc}") from exc
        except Exception as exc:  # dernier filet : aucun bug d'outil ne tue la tâche
            self._record(name, False, started, str(exc))
            raise ToolError(f"Échec de l'outil « {name} » : {exc}") from exc

        self._record(name, True, started)
        return result

    def _record(self, name: str, ok: bool, started: float, error: str = "") -> None:
        duration = int((time.monotonic() - started) * 1000)
        self.calls.append(ToolCall(name=name, ok=ok, duration_ms=duration, error=error))
        self.ctx.journal.add_tool(name)
        if not ok:
            self.ctx.journal.add_error(f"{name}: {error}")
