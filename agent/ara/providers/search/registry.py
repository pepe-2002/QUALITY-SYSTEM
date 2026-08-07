"""Sélection du moteur de recherche."""

from __future__ import annotations

from typing import Callable

from ...core.config import get_settings
from .base import SearchProvider
from .engines import DuckDuckGoSearch, MultiSearch, SearxNGSearch, WikipediaSearch
from .fixture import FixtureSearch

_FACTORIES: dict[str, Callable[[], SearchProvider]] = {
    "auto": MultiSearch,
    "duckduckgo": DuckDuckGoSearch,
    "wikipedia": WikipediaSearch,
    "searxng": SearxNGSearch,
    "fixture": FixtureSearch,
}


def get_search(name: str | None = None) -> tuple[SearchProvider, str]:
    """Retourne `(moteur, avertissement)`."""
    name = (name or get_settings().search_provider).strip().lower()
    factory = _FACTORIES.get(name)

    if factory is None:
        return MultiSearch(), (
            f"Moteur de recherche inconnu « {name} » — mode auto utilisé. "
            f"Choix possibles : {', '.join(sorted(_FACTORIES))}."
        )

    provider = factory()
    ok, reason = provider.available()
    if ok:
        return provider, ""
    return MultiSearch(), (
        f"Cette fonction nécessite une ressource externe. Moteur « {name} » : {reason} "
        "— repli sur le mode auto (DuckDuckGo + Wikipédia)."
    )


def available_engines() -> list[dict]:
    out = []
    for name, factory in _FACTORIES.items():
        try:
            out.append(factory().describe())
        except Exception as exc:
            out.append({"name": name, "available": False, "reason": str(exc)})
    return out
