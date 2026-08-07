"""Journal de recherche (spec §17).

Chaque tâche produit une entrée reproductible :

    timestamp, task, research_steps, sources, tools_used,
    reasoning_steps_summary, files_created, iterations, final_score, errors

⚠️ Règle stricte de la spec : **aucune chaîne de pensée privée n'est stockée**.
On n'enregistre que des *résumés opérationnels* — des étiquettes d'action du
type « recherche : horaires traversées » — et les résultats nécessaires à la
reproductibilité.
"""

from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

#: Longueur maximale d'un résumé opérationnel. Au-delà, on tronque : c'est un
#: garde-fou contre l'enregistrement accidentel d'un raisonnement complet.
MAX_SUMMARY_CHARS = 200


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class ResearchLog:
    """Journal d'une tâche, écrit en JSONL à la fin de l'exécution."""

    task_id: str
    task: str
    timestamp: str = field(default_factory=_now_iso)
    complexity: str = "LOW"
    research_steps: list[dict[str, Any]] = field(default_factory=list)
    sources: list[dict[str, str]] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    reasoning_steps_summary: list[str] = field(default_factory=list)
    files_created: list[str] = field(default_factory=list)
    iterations: int = 0
    final_score: int | None = None
    errors: list[str] = field(default_factory=list)
    duration_ms: int = 0

    # -- enregistrement ----------------------------------------------------

    def add_step(self, kind: str, detail: str, **data: Any) -> None:
        """Ajoute une étape de recherche (résumé opérationnel uniquement)."""
        self.research_steps.append(
            {"n": len(self.research_steps) + 1, "kind": kind, "detail": _trim(detail), **data}
        )

    def add_source(self, url: str, title: str = "", via: str = "") -> None:
        if not url:
            return
        if any(s["url"] == url for s in self.sources):
            return
        self.sources.append({"url": url, "title": _trim(title, 120), "via": via})

    def add_tool(self, name: str) -> None:
        self.tools_used.append(name)

    def add_summary(self, label: str) -> None:
        """Ajoute un résumé opérationnel — jamais un raisonnement détaillé."""
        self.reasoning_steps_summary.append(_trim(label))

    def add_file(self, path: str | Path) -> None:
        self.files_created.append(str(path))

    def add_error(self, message: str) -> None:
        self.errors.append(_trim(str(message), 300))

    # -- sérialisation -----------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "task_id": self.task_id,
            "task": _trim(self.task, 500),
            "complexity": self.complexity,
            "research_steps": self.research_steps,
            "sources": self.sources,
            "tools_used": self.tools_used,
            "reasoning_steps_summary": self.reasoning_steps_summary,
            "files_created": self.files_created,
            "iterations": self.iterations,
            "final_score": self.final_score,
            "errors": self.errors,
            "duration_ms": self.duration_ms,
        }


def _trim(text: str, limit: int = MAX_SUMMARY_CHARS) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


class JournalStore:
    """Écrit et relit les journaux (JSONL, une ligne par tâche)."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._lock = threading.Lock()

    def append(self, log: ResearchLog) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(log.to_dict(), ensure_ascii=False)
        with self._lock:
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(line + "\n")

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        entries: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return entries
