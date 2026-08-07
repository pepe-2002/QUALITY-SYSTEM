"""Extraction de texte lisible depuis du HTML — sans dépendance externe."""

from __future__ import annotations

import re
from html.parser import HTMLParser

#: Balises dont le contenu n'est jamais du texte utile
_DROP = {"script", "style", "noscript", "template", "svg", "canvas", "iframe"}

#: Balises qui provoquent un saut de ligne
_BLOCK = {
    "p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6",
    "section", "article", "header", "footer", "table", "ul", "ol", "blockquote",
}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title: str = ""
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in _DROP:
            self._skip_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag in _BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _DROP and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag == "title":
            self._in_title = False
        elif tag in _BLOCK:
            self.parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._in_title:
            self.title += data
            return
        if data.strip():
            # Les retours à la ligne du code source HTML ne sont pas des
            # fins de phrase : les garder coupait « … coûte\n15 000 FC » en
            # deux, et l'analyse perdait le sujet du chiffre.
            self.parts.append(re.sub(r"\s+", " ", data))


def extract(html: str, *, max_chars: int = 20_000) -> tuple[str, str]:
    """Retourne `(titre, texte)` nettoyés depuis du HTML.

    >>> extract("<title>Salut</title><p>Bonjour <b>monde</b></p>")[0]
    'Salut'
    """
    parser = _TextExtractor()
    try:
        parser.feed(html)
        parser.close()
    except Exception:  # HTML cassé : on garde ce qui a été parsé
        pass

    text = "".join(parser.parts)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n\s*", "\n\n", text)
    text = "\n".join(line.strip() for line in text.split("\n")).strip()

    if len(text) > max_chars:
        text = text[:max_chars].rsplit(" ", 1)[0] + " […]"

    return " ".join(parser.title.split()), text


def strip_tags(html: str) -> str:
    """Retire les balises d'un fragment court (titre, extrait de résultat)."""
    return " ".join(re.sub(r"<[^>]+>", " ", html).split())
