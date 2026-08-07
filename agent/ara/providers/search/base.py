"""Interface commune des moteurs de recherche."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ...core.models import SearchResult


class SearchProvider(ABC):
    """Contrat minimal d'un moteur de recherche."""

    name: str = "base"
    requires_external: bool = False

    @abstractmethod
    def search(self, query: str, *, limit: int = 8) -> list[SearchResult]:
        """Retourne des résultats. Lève `ProviderError` en cas d'échec dur."""

    def available(self) -> tuple[bool, str]:
        return True, ""

    def describe(self) -> dict[str, Any]:
        ok, reason = self.available()
        return {
            "name": self.name,
            "available": ok,
            "reason": reason,
            "requires_external": self.requires_external,
        }
