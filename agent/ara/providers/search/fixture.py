"""Moteur de test : rejoue des résultats figés, sans réseau.

Indispensable pour que la suite de tests soit **déterministe et reproductible**
(exigence de la règle finale : fiabilité, reproductibilité) et pour que le
RESEARCH LAB puisse comparer des stratégies sur un corpus constant.
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from pathlib import Path

from ...core.models import SearchResult
from .base import SearchProvider


def _tokens(text: str) -> set[str]:
    """Mots normalisés, pluriel simple retiré (« tarifs » ≈ « tarif »)."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return {
        word[:-1] if len(word) > 4 and word.endswith("s") else word
        for word in re.findall(r"[a-z0-9]{3,}", text)
    }


class FixtureSearch(SearchProvider):
    name = "fixture"

    def __init__(self, data: dict[str, list[dict]] | None = None, path: Path | None = None) -> None:
        self.data = dict(data or {})
        # Permet de rejouer un corpus depuis l'environnement (tests, LAB).
        path = path or (
            Path(os.environ["ARA_SEARCH_FIXTURE"])
            if os.environ.get("ARA_SEARCH_FIXTURE")
            else None
        )
        if path and Path(path).is_file():
            self.data.update(json.loads(Path(path).read_text(encoding="utf-8")))
        self.queries: list[str] = []

    def search(self, query: str, *, limit: int = 8) -> list[SearchResult]:
        self.queries.append(query)
        items = self.data.get(query)
        if items is None:
            items = self._best_match(query)
        items = items or []
        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("snippet", ""),
                engine=self.name,
                rank=rank,
            )
            for rank, item in enumerate(items[:limit], start=1)
        ]

    # Les requêtes réelles varient (reformulations de l'agent) alors que les
    # clés du corpus sont fixes : on apparie sur le recouvrement des mots.
    def _best_match(self, query: str) -> list[dict] | None:
        asked = _tokens(query)
        if not asked:
            return None
        best: tuple[float, list[dict]] | None = None
        for key, value in self.data.items():
            keyed = _tokens(key)
            if not keyed:
                continue
            score = len(keyed & asked) / len(keyed)
            if score >= 0.5 and (best is None or score > best[0]):
                best = (score, value)
        return best[1] if best else None
