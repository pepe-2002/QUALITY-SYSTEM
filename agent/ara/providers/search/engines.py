"""Moteurs de recherche gratuits, sans clé d'API.

* **DuckDuckGo** (point d'entrée HTML public) — couverture web générale.
* **Wikipédia** (API MediaWiki publique) — source de référence stable, utile
  pour croiser les faits.
* **SearXNG** — instance choisie par l'utilisateur, respecte la vie privée.

Aucun ne demande de compte. Un moteur qui échoue ne doit jamais faire tomber la
tâche : l'orchestrateur travaille avec ce qu'il obtient et le signale.
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse

from ...core import http
from ...core.errors import AraError, ProviderError
from ...core.html_text import strip_tags
from ...core.models import SearchResult
from ...core.urls import canonical
from .base import SearchProvider


def _unwrap_ddg(href: str) -> str:
    """DuckDuckGo enveloppe les liens dans /l/?uddg=<url encodée>."""
    if "uddg=" not in href:
        return href if href.startswith("http") else f"https:{href}" if href.startswith("//") else href
    query = urllib.parse.urlparse(href if href.startswith("http") else f"https:{href}").query
    target = urllib.parse.parse_qs(query).get("uddg", [""])[0]
    return target or href


class DuckDuckGoSearch(SearchProvider):
    name = "duckduckgo"

    HTML_URL = "https://html.duckduckgo.com/html/"
    LITE_URL = "https://lite.duckduckgo.com/lite/"

    _RESULT_RE = re.compile(
        r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE,
    )
    _SNIPPET_RE = re.compile(
        r'<a[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE,
    )
    _LITE_RE = re.compile(
        r'<a[^>]+class="[^"]*result-link[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        re.DOTALL | re.IGNORECASE,
    )

    def search(self, query: str, *, limit: int = 8) -> list[SearchResult]:
        html = self._fetch(self.HTML_URL, query)
        results = self._parse_html(html, limit)
        if not results:
            results = self._parse_lite(self._fetch(self.LITE_URL, query), limit)
        return results

    def _fetch(self, url: str, query: str) -> str:
        try:
            return http.post(url, {"q": query, "kl": "fr-fr"}).text()
        except AraError as exc:
            raise ProviderError(f"DuckDuckGo indisponible : {exc}") from exc

    def _parse_html(self, html: str, limit: int) -> list[SearchResult]:
        links = self._RESULT_RE.findall(html)
        snippets = self._SNIPPET_RE.findall(html)
        results: list[SearchResult] = []
        for rank, (href, title_html) in enumerate(links[:limit], start=1):
            url = _unwrap_ddg(href)
            if not url.startswith("http"):
                continue
            snippet = strip_tags(snippets[rank - 1]) if rank - 1 < len(snippets) else ""
            results.append(
                SearchResult(
                    title=strip_tags(title_html),
                    url=url,
                    snippet=snippet,
                    engine=self.name,
                    rank=rank,
                )
            )
        return results

    def _parse_lite(self, html: str, limit: int) -> list[SearchResult]:
        results: list[SearchResult] = []
        for rank, (href, title_html) in enumerate(self._LITE_RE.findall(html)[:limit], start=1):
            url = _unwrap_ddg(href)
            if not url.startswith("http"):
                continue
            results.append(
                SearchResult(
                    title=strip_tags(title_html), url=url, engine=self.name, rank=rank
                )
            )
        return results


class WikipediaSearch(SearchProvider):
    """API MediaWiki publique — source de recoupement fiable et citable."""

    name = "wikipedia"

    def __init__(self, lang: str | None = None) -> None:
        self.lang = (lang or os.environ.get("ARA_WIKIPEDIA_LANG", "fr")).strip() or "fr"

    def search(self, query: str, *, limit: int = 5) -> list[SearchResult]:
        params = urllib.parse.urlencode(
            {
                "action": "query",
                "list": "search",
                "srsearch": query,
                "srlimit": str(limit),
                "format": "json",
                "utf8": "1",
            }
        )
        url = f"https://{self.lang}.wikipedia.org/w/api.php?{params}"
        try:
            payload = json.loads(http.get(url).text())
        except (AraError, json.JSONDecodeError) as exc:
            raise ProviderError(f"Wikipédia indisponible : {exc}") from exc

        results: list[SearchResult] = []
        for rank, item in enumerate(payload.get("query", {}).get("search", []), start=1):
            title = item.get("title", "")
            slug = urllib.parse.quote(title.replace(" ", "_"))
            results.append(
                SearchResult(
                    title=title,
                    url=f"https://{self.lang}.wikipedia.org/wiki/{slug}",
                    snippet=strip_tags(item.get("snippet", "")),
                    engine=self.name,
                    rank=rank,
                )
            )
        return results


class SearxNGSearch(SearchProvider):
    """Méta-moteur auto-hébergeable — nécessite une instance fournie par l'utilisateur."""

    name = "searxng"
    requires_external = True

    def __init__(self) -> None:
        self.base_url = (os.environ.get("ARA_SEARXNG_URL", "") or "").rstrip("/")

    def available(self) -> tuple[bool, str]:
        if not self.base_url:
            return False, "ARA_SEARXNG_URL non défini (adresse de votre instance SearXNG)."
        return True, ""

    def search(self, query: str, *, limit: int = 8) -> list[SearchResult]:
        if not self.base_url:
            raise ProviderError("ARA_SEARXNG_URL non défini.")
        params = urllib.parse.urlencode({"q": query, "format": "json", "language": "fr"})
        try:
            payload = json.loads(http.get(f"{self.base_url}/search?{params}").text())
        except (AraError, json.JSONDecodeError) as exc:
            raise ProviderError(f"SearXNG indisponible : {exc}") from exc

        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                snippet=item.get("content", ""),
                engine=self.name,
                rank=rank,
            )
            for rank, item in enumerate(payload.get("results", [])[:limit], start=1)
            if item.get("url")
        ]


class MultiSearch(SearchProvider):
    """Interroge plusieurs moteurs et fusionne les résultats.

    C'est la configuration par défaut : consulter **plusieurs sources** est une
    exigence de la spec §2, pas une option.
    """

    name = "auto"

    def __init__(self, engines: list[SearchProvider] | None = None) -> None:
        self.engines = engines or [DuckDuckGoSearch(), WikipediaSearch()]
        self.failures: list[str] = []

    def available(self) -> tuple[bool, str]:
        return (True, "") if self.engines else (False, "Aucun moteur configuré.")

    def search(self, query: str, *, limit: int = 8) -> list[SearchResult]:
        merged: list[SearchResult] = []
        seen: set[str] = set()
        self.failures = []

        for engine in self.engines:
            ok, reason = engine.available()
            if not ok:
                self.failures.append(f"{engine.name} : {reason}")
                continue
            try:
                results = engine.search(query, limit=limit)
            except AraError as exc:
                self.failures.append(f"{engine.name} : {exc}")
                continue
            for result in results:
                key = canonical(result.url)
                if key in seen:
                    continue
                seen.add(key)
                merged.append(result)

        if not merged and self.failures:
            raise ProviderError("Aucun moteur n'a répondu — " + " ; ".join(self.failures))
        return merged[: limit * 2]
