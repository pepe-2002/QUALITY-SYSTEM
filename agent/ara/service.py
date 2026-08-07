"""Service de tâches : exécution en arrière-plan et historique persistant.

L'interface téléphone lance une tâche, ferme l'écran, revient plus tard : le
résultat doit être là. Les tâches tournent donc dans un thread et sont écrites
sur disque (`workspace/tasks/<id>/task.json`) — l'historique survit au
redémarrage du serveur (spec §21, « historique »).
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .agents.orchestrator import Orchestrator
from .core.config import Settings, get_settings
from .core.events import EventBus
from .core.permissions import PermissionManager
from .providers.storage import safe_filename


@dataclass
class TaskRecord:
    """Fiche d'une tâche, telle que l'historique la conserve."""

    task_id: str
    prompt: str
    status: str = "pending"  # pending | running | done | error
    created_at: float = field(default_factory=time.time)
    finished_at: float | None = None
    complexity: str = ""
    answer: str = ""
    files: list[dict[str, Any]] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)
    notices: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def summary(self) -> dict[str, Any]:
        """Vue courte pour la liste d'historique (économise la 3G)."""
        return {
            "task_id": self.task_id,
            "prompt": self.prompt[:160],
            "status": self.status,
            "created_at": self.created_at,
            "finished_at": self.finished_at,
            "complexity": self.complexity,
            "files": len(self.files),
            "sources": len(self.sources),
            "has_errors": bool(self.errors),
        }

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TaskStore:
    """Persistance des fiches de tâches."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root or get_settings().tasks_dir())
        self._lock = threading.Lock()

    def _path(self, task_id: str) -> Path:
        return self.root / safe_filename(task_id, default="task") / "task.json"

    def save(self, record: TaskRecord) -> None:
        path = self._path(record.task_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(record.to_dict(), ensure_ascii=False, indent=1)
        with self._lock:
            # Écriture atomique : pas de fiche à moitié écrite si on coupe.
            tmp = path.with_suffix(".tmp")
            tmp.write_text(payload, encoding="utf-8")
            tmp.replace(path)

    def get(self, task_id: str) -> TaskRecord | None:
        path = self._path(task_id)
        if not path.is_file():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
        known = {f for f in TaskRecord.__dataclass_fields__}
        return TaskRecord(**{k: v for k, v in data.items() if k in known})

    def list(self, limit: int = 50) -> list[TaskRecord]:
        if not self.root.is_dir():
            return []
        records: list[TaskRecord] = []
        for directory in self.root.iterdir():
            if not directory.is_dir():
                continue
            record = self.get(directory.name)
            if record:
                records.append(record)
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records[:limit]


class TaskService:
    """Lance les tâches, expose leurs événements, conserve l'historique."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.store = TaskStore(self.settings.tasks_dir())
        self.permissions = PermissionManager(self.settings)
        self._buses: dict[str, EventBus] = {}
        self._threads: dict[str, threading.Thread] = {}
        self._lock = threading.Lock()

    # -- lancement ---------------------------------------------------------

    def start(self, prompt: str) -> TaskRecord:
        task_id = uuid.uuid4().hex[:12]
        record = TaskRecord(task_id=task_id, prompt=prompt, status="running")
        self.store.save(record)

        bus = EventBus()
        with self._lock:
            self._buses[task_id] = bus

        thread = threading.Thread(
            target=self._run, args=(record, bus), name=f"ara-task-{task_id}", daemon=True
        )
        with self._lock:
            self._threads[task_id] = thread
        thread.start()
        return record

    def _run(self, record: TaskRecord, bus: EventBus) -> None:
        orchestrator = Orchestrator(self.settings, permissions=self.permissions)
        try:
            result = orchestrator.run(record.prompt, task_id=record.task_id, bus=bus)
            record.answer = result.answer
            record.files = result.files
            record.sources = [source.to_dict() for source in result.sources]
            record.notices = result.notices
            record.errors = result.errors
            record.complexity = result.complexity
            record.status = "error" if result.errors and not result.answer else "done"
        except Exception as exc:  # ne doit jamais arriver : l'orchestrateur capture
            record.status = "error"
            record.errors.append(f"{type(exc).__name__}: {exc}")
        finally:
            record.finished_at = time.time()
            self.store.save(record)
            if not bus.closed:
                bus.close()

    # -- consultation ------------------------------------------------------

    def bus(self, task_id: str) -> EventBus | None:
        with self._lock:
            return self._buses.get(task_id)

    def get(self, task_id: str) -> TaskRecord | None:
        return self.store.get(task_id)

    def history(self, limit: int = 50) -> list[dict[str, Any]]:
        return [record.summary() for record in self.store.list(limit)]

    def wait(self, task_id: str, timeout: float = 60) -> TaskRecord | None:
        """Attend la fin d'une tâche (utilisé par les tests et le mode CLI)."""
        with self._lock:
            thread = self._threads.get(task_id)
        if thread:
            thread.join(timeout)
        return self.get(task_id)
