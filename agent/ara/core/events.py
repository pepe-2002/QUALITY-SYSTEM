"""Événements de progression — c'est ce que le téléphone affiche en direct.

La spec §14 impose d'afficher le pipeline :

    TÂCHE → RECHERCHE → ANALYSE → CRÉATION → VÉRIFICATION → RÉSULTAT

Chaque étape émet des événements ; l'interface les consomme en SSE.
"""

from __future__ import annotations

import queue
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Iterator


class Stage(str, Enum):
    """Les six étapes visibles par l'utilisateur."""

    TASK = "TACHE"
    RESEARCH = "RECHERCHE"
    ANALYSIS = "ANALYSE"
    CREATION = "CREATION"
    VERIFICATION = "VERIFICATION"
    RESULT = "RESULTAT"


#: Ordre d'affichage dans l'interface
STAGE_ORDER: tuple[Stage, ...] = (
    Stage.TASK,
    Stage.RESEARCH,
    Stage.ANALYSIS,
    Stage.CREATION,
    Stage.VERIFICATION,
    Stage.RESULT,
)


class Status(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    SKIPPED = "skipped"
    FAILED = "failed"


@dataclass
class Event:
    """Un événement de progression, sérialisable en JSON."""

    type: str
    stage: Stage | None = None
    status: Status | None = None
    message: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    ts: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"type": self.type, "ts": self.ts}
        if self.stage is not None:
            payload["stage"] = self.stage.value
        if self.status is not None:
            payload["status"] = self.status.value
        if self.message:
            payload["message"] = self.message
        if self.data:
            payload["data"] = self.data
        return payload


class EventBus:
    """File d'événements multi-abonnés, sans dépendance externe.

    Les événements sont conservés (`history`) pour qu'un téléphone qui se
    reconnecte — cas courant en 3G — retrouve tout le déroulé.
    """

    _SENTINEL = object()

    def __init__(self) -> None:
        self.history: list[Event] = []
        self._subscribers: list[queue.Queue] = []
        self._closed = False

    def emit(self, event: Event) -> Event:
        if self._closed:
            return event
        self.history.append(event)
        for sub in list(self._subscribers):
            sub.put(event)
        return event

    def stage(
        self,
        stage: Stage,
        status: Status,
        message: str = "",
        **data: Any,
    ) -> Event:
        return self.emit(Event("stage", stage=stage, status=status, message=message, data=data))

    def log(self, message: str, **data: Any) -> Event:
        return self.emit(Event("log", message=message, data=data))

    def close(self) -> None:
        self._closed = True
        for sub in list(self._subscribers):
            sub.put(self._SENTINEL)

    @property
    def closed(self) -> bool:
        return self._closed

    def subscribe(self, *, replay: bool = True) -> Iterator[Event]:
        """Itère sur les événements ; rejoue l'historique par défaut."""
        sub: queue.Queue = queue.Queue()
        self._subscribers.append(sub)
        try:
            if replay:
                for event in list(self.history):
                    yield event
            if self._closed:
                return
            while True:
                item = sub.get()
                if item is self._SENTINEL:
                    return
                yield item
        finally:
            if sub in self._subscribers:
                self._subscribers.remove(sub)


#: Signature d'un observateur d'événements
EventSink = Callable[[Event], Any]
