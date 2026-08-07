"""Normalisation d'URL pour le dédoublonnage des sources.

Constaté en conditions réelles : la même page revient sous deux adresses
(`…/page` et `…/page?lang=fr`) et compte pour deux sources, ce qui fausse la
diversité affichée à l'utilisateur.

On ne supprime que les paramètres **cosmétiques** (langue, suivi publicitaire,
ancre) : un paramètre qui change le contenu (`?id=`, `?page=`) est conservé,
sinon on fusionnerait des pages réellement différentes.
"""

from __future__ import annotations

import urllib.parse

#: Paramètres qui ne changent pas le contenu d'une page
COSMETIC_PARAMS = {
    "lang", "hl", "locale", "language", "l",
    "fbclid", "gclid", "msclkid", "igshid", "mc_cid", "mc_eid",
    "ref", "referrer", "source", "amp",
}
COSMETIC_PREFIXES = ("utm_",)


def _is_cosmetic(name: str) -> bool:
    name = name.lower()
    return name in COSMETIC_PARAMS or name.startswith(COSMETIC_PREFIXES)


def canonical(url: str) -> str:
    """Forme canonique d'une URL, utilisée comme clé de dédoublonnage.

    >>> canonical("https://Exemple.test/Page/?lang=fr&utm_source=x#bas")
    'https://exemple.test/Page'
    >>> canonical("https://exemple.test/page?id=7") != canonical("https://exemple.test/page")
    True
    """
    try:
        parsed = urllib.parse.urlsplit(url.strip())
    except ValueError:
        return url.strip().lower()

    if not parsed.netloc:
        return url.strip().lower()

    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.rstrip("/") or "/"

    kept = [
        (key, value)
        for key, value in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        if not _is_cosmetic(key)
    ]
    query = urllib.parse.urlencode(sorted(kept)) if kept else ""

    scheme = parsed.scheme.lower() or "https"
    return urllib.parse.urlunsplit((scheme, host, path, query, ""))
