"""Modèles de données partagés entre agents, outils et fournisseurs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SearchResult:
    """Un résultat de moteur de recherche."""

    title: str
    url: str
    snippet: str = ""
    engine: str = ""
    rank: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "engine": self.engine,
            "rank": self.rank,
        }


@dataclass
class SourceDoc:
    """Une source consultée : page récupérée et convertie en texte."""

    url: str
    title: str = ""
    text: str = ""
    snippet: str = ""
    engine: str = ""
    fetched: bool = False
    error: str = ""

    @property
    def domain(self) -> str:
        from urllib.parse import urlparse

        return urlparse(self.url).netloc.removeprefix("www.")

    @property
    def content(self) -> str:
        """Texte exploitable : le corps de page, sinon l'extrait du moteur."""
        return self.text or self.snippet

    def to_dict(self, *, with_text: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "url": self.url,
            "title": self.title,
            "domain": self.domain,
            "snippet": self.snippet,
            "engine": self.engine,
            "fetched": self.fetched,
        }
        if self.error:
            payload["error"] = self.error
        if with_text:
            payload["text"] = self.text
        return payload


@dataclass
class TaskResult:
    """Résultat final d'une tâche, tel que l'interface l'affiche."""

    task_id: str
    prompt: str
    answer: str = ""
    sources: list[SourceDoc] = field(default_factory=list)
    files: list[dict[str, Any]] = field(default_factory=list)
    complexity: str = "LOW"
    degraded: bool = False
    notices: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "prompt": self.prompt,
            "answer": self.answer,
            "sources": [s.to_dict() for s in self.sources],
            "files": self.files,
            "complexity": self.complexity,
            "degraded": self.degraded,
            "notices": self.notices,
            "errors": self.errors,
        }
