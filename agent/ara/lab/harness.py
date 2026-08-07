"""Harnais du laboratoire : rejouer le corpus figé, mesurer, compter.

Pour comparer des stratégies, il faut qu'elles voient **exactement le même
web**. Le harnais substitue donc le réseau par le corpus figé, le temps d'une
mesure, et remet tout en place ensuite.

C'est assumé : un laboratoire *doit* contrôler son environnement. Ce qui serait
malhonnête, ce serait de mesurer contre l'Internet réel et de présenter le
résultat comme reproductible.
"""

from __future__ import annotations

import contextlib
import time
from dataclasses import dataclass, field

from ..core import http
from ..core.complexity import assess
from ..core.config import Settings
from ..core.context import TaskContext
from ..core.events import EventBus
from ..core.journal import ResearchLog
from ..core.models import SearchResult
from ..core.permissions import PermissionManager
from ..providers.llm import get_llm
from ..providers.search.base import SearchProvider
from ..providers.storage import LocalStorage
from .corpus import Corpus


class LabSearch(SearchProvider):
    """Moteur branché sur le corpus figé. Compte ce qu'on lui demande."""

    name = "laboratoire"

    def __init__(self, corpus: Corpus) -> None:
        self.corpus = corpus
        self.queries: list[str] = []

    def search(self, query: str, *, limit: int = 8) -> list[SearchResult]:
        self.queries.append(query)
        return [
            SearchResult(
                title=url.rsplit("/", 1)[-1], url=url, engine=self.name, rank=rank
            )
            for rank, url in enumerate(self.corpus.search(query, limit), start=1)
        ]


@contextlib.contextmanager
def frozen_network(corpus: Corpus, counters: dict[str, int]):
    """Remplace le réseau par le corpus, et compte les pages servies."""
    original_get = http.get

    def fetch(url: str, **kwargs):
        counters["fetches"] = counters.get("fetches", 0) + 1
        body = corpus.fetch(url)
        if body is None:
            raise http.ToolError(f"page absente du corpus : {url}")
        counters["chars"] = counters.get("chars", 0) + len(body)
        return http.HttpResponse(
            url=url, status=200, body=body.encode("utf-8"),
            content_type="text/html; charset=utf-8",
        )

    http.get = fetch
    try:
        yield
    finally:
        http.get = original_get


@dataclass
class Outcome:
    """Ce qu'une stratégie a produit et ce qu'elle a coûté."""

    strategy: str
    task_id: str
    answer: str = ""
    sources: list = field(default_factory=list)
    cycles: int = 0
    searches: int = 0
    fetches: int = 0
    tool_calls: int = 0
    tokens: int = 0
    latency_ms: int = 0
    domains: int = 0
    gaps: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    stopped_because: str = ""
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy, "task": self.task_id,
            "cycles": self.cycles, "searches": self.searches,
            "fetches": self.fetches, "tool_calls": self.tool_calls,
            "tokens": self.tokens, "latency_ms": self.latency_ms,
            "sources": len(self.sources), "domains": self.domains,
            "gaps": len(self.gaps), "contradictions": len(self.contradictions),
            "stopped_because": self.stopped_because, "error": self.error,
        }


def build_context(
    question: str, settings: Settings, search: SearchProvider, task_id: str
) -> TaskContext:
    llm, _notice = get_llm(settings.llm_provider)
    return TaskContext(
        task_id=task_id,
        prompt=question,
        settings=settings,
        bus=EventBus(),
        journal=ResearchLog(task_id=task_id, task=question),
        permissions=PermissionManager(settings),
        storage=LocalStorage(settings.tasks_dir()),
        llm=llm,
        search=search,
        budget=assess(question, max_search_steps=settings.max_research_steps),
    )


def estimate_tokens(ctx: TaskContext, docs, answer: str) -> int:
    """Estimation du calcul consommé, en « jetons » de 4 caractères.

    Ce n'est pas une facture : le moteur hors-ligne ne consomme rien chez un
    fournisseur. C'est une mesure **comparable** du volume de texte traversé,
    qui est ce qui coûte cher dès qu'un vrai LLM est branché. Le rapport le
    dit explicitement pour éviter toute confusion.
    """
    volume = len(ctx.prompt) + len(answer)
    for doc in docs:
        volume += len(doc.content or "")
    return round(volume / 4)


class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.ms = int((time.perf_counter() - self.start) * 1000)
        return False
