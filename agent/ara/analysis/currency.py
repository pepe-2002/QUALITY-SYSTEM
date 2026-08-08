"""EXTRACTION-V2 — identifier la devise d'un montant, ou avouer qu'on ne sait pas.

Le diagnostic avait montré qu'un montant écrit « 3 200 francs » n'était pas vu
du tout. Le réflexe serait de décréter que « francs » vaut la devise du projet
— ici KMF. Ce serait pire que l'aveuglement : un agent qui comparerait des
francs comoriens à des francs CFA produirait des contradictions imaginaires et
des réponses fausses avec l'aplomb de la certitude.

Trois niveaux de confiance, et un seul chemin vers l'affirmation :

``certaine``
    la devise est **écrite** — « francs comoriens », « FCFA », « KMF », « € ».

``probable``
    la devise n'est pas écrite auprès du montant, mais le document ne laisse
    qu'une seule possibilité : une autre devise y est nommée sans ambiguïté,
    ou le contexte géographique désigne un pays à devise unique.

``inconnue``
    tout le reste. Le montant est **conservé** — il compte, il se compare à
    d'autres montants de même unité — mais sa devise reste ``UNKNOWN``.

La règle de sécurité est explicite : en cas de doute, on garde le nombre et on
perd la devise. Jamais l'inverse.
"""

from __future__ import annotations

import re
import unicodedata

#: Devise provisoire d'un montant dont la devise n'est pas écrite.
UNKNOWN = "UNKNOWN"

CONFIDENCE_LEVELS = ("certaine", "probable", "inconnue")

#: Indices géographiques → devise. Volontairement court et explicite.
#:
#: Ce n'est pas un référentiel du monde : c'est la liste des pays dont le nom,
#: apparaissant dans un document, lève l'ambiguïté d'un « franc ». Chaque
#: entrée est une **zone à devise unique** ; un pays qui aurait changé de
#: devise récemment n'y a pas sa place.
GEOGRAPHIC_HINTS: dict[str, str] = {
    "comores": "KMF", "comorien": "KMF", "comorienne": "KMF",
    "moroni": "KMF", "moheli": "KMF", "anjouan": "KMF",
    "madagascar": "MGA", "malgache": "MGA", "antananarivo": "MGA",
    "suisse": "CHF", "geneve": "CHF", "zurich": "CHF", "lausanne": "CHF",
    "senegal": "XOF", "dakar": "XOF", "mali": "XOF", "bamako": "XOF",
    "burkina": "XOF", "ouagadougou": "XOF", "benin": "XOF", "cotonou": "XOF",
    "togo": "XOF", "lome": "XOF", "niger": "XOF", "niamey": "XOF",
    "ivoire": "XOF", "abidjan": "XOF",
    "cameroun": "XAF", "yaounde": "XAF", "douala": "XAF",
    "gabon": "XAF", "libreville": "XAF", "tchad": "XAF", "ndjamena": "XAF",
    "centrafrique": "XAF", "bangui": "XAF",
    "djibouti": "DJF", "burundi": "BIF", "bujumbura": "BIF",
    "rwanda": "RWF", "kigali": "RWF",
    "guinee": "GNF", "conakry": "GNF",
}

#: Devises écrites, telles qu'on les reconnaît dans un texte.
WRITTEN_CURRENCIES: dict[str, str] = {
    r"francs?\s+comoriens?|\bkmf\b|\bfc\b": "KMF",
    r"francs?\s+cfa|\bfcfa\b|\bxof\b": "XOF",
    r"\bxaf\b|francs?\s+cfa\s+d'afrique\s+centrale": "XAF",
    r"francs?\s+suisses?|\bchf\b": "CHF",
    r"francs?\s+djiboutiens?|\bdjf\b": "DJF",
    r"francs?\s+rwandais|\brwf\b": "RWF",
    r"francs?\s+burundais|\bbif\b": "BIF",
    r"francs?\s+guineens?|\bgnf\b": "GNF",
    r"euros?|\beur\b|€": "EUR",
    r"dollars?|\busd\b|\$": "USD",
    r"ariary|\bmga\b": "MGA",
    r"livres?\s+sterling|\bgbp\b|£": "GBP",
}

_COMPILED = {re.compile(motif, re.IGNORECASE): devise
             for motif, devise in WRITTEN_CURRENCIES.items()}

#: Marques d'une **conversion** : « 3 200 francs, soit environ 6,50 euros ».
#:
#: Dans une phrase pareille, la devise écrite appartient à l'autre montant.
#: L'hériter serait exactement l'erreur que ce module doit empêcher — et c'est
#: celle qu'il commettait avant ce garde-fou.
_CONVERSION = re.compile(
    r"\b(?:soit|c'est-a-dire|c'est-à-dire|equivalent|équivalent|equivaut"
    r"|équivaut|converti|conversion|contre|au\s+taux)\b|[≈~]",
    re.IGNORECASE,
)


def _fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def written_currencies(text: str) -> set[str]:
    """Devises **écrites** dans un texte."""
    return {devise for motif, devise in _COMPILED.items() if motif.search(text)}


def geographic_currencies(text: str) -> set[str]:
    """Devises suggérées par les lieux nommés dans un texte."""
    mots = set(re.findall(r"[a-z]{4,}", _fold(text)))
    return {
        devise for indice, devise in GEOGRAPHIC_HINTS.items() if indice in mots
    }


def resolve(sentence: str, document: str = "") -> tuple[str, str]:
    """Devise d'un montant non qualifié, et confiance associée.

    L'ordre est celui de la prudence : ce qui est écrit tout près d'abord, le
    document ensuite, la géographie en dernier — et le doute l'emporte sur
    tout le reste.

    >>> resolve("Le billet coûte 3 200 francs.", "Voyager aux Comores")
    ('KMF', 'probable')
    >>> resolve("Le billet coûte 3 200 francs.")
    ('UNKNOWN', 'inconnue')
    >>> resolve("3 200 francs, soit environ 6,50 euros.")
    ('UNKNOWN', 'inconnue')
    """
    # 1. Une devise écrite dans la phrase même.
    dans_la_phrase = written_currencies(sentence)
    if len(dans_la_phrase) == 1 and not _CONVERSION.search(sentence):
        return next(iter(dans_la_phrase)), "probable"
    if dans_la_phrase and _CONVERSION.search(sentence):
        # Conversion : la devise écrite est celle de l'**autre** montant.
        return UNKNOWN, "inconnue"
    if len(dans_la_phrase) > 1:
        # Deux devises dans une phrase : conversion, comparaison, énumération.
        # Attribuer l'une d'elles au montant nu serait un pari.
        return UNKNOWN, "inconnue"

    corpus = f"{document}"
    # 2. Une devise écrite ailleurs dans le document, et une seule.
    dans_le_document = written_currencies(corpus)
    if len(dans_le_document) == 1:
        return next(iter(dans_le_document)), "probable"
    if len(dans_le_document) > 1:
        return UNKNOWN, "inconnue"

    # 3. À défaut, le contexte géographique — s'il ne désigne qu'une zone.
    lieux = geographic_currencies(f"{sentence} {corpus}")
    if len(lieux) == 1:
        return next(iter(lieux)), "probable"

    # 4. Rien de concluant : on garde le montant, on perd la devise.
    return UNKNOWN, "inconnue"


__all__ = [
    "CONFIDENCE_LEVELS",
    "GEOGRAPHIC_HINTS",
    "UNKNOWN",
    "WRITTEN_CURRENCIES",
    "geographic_currencies",
    "resolve",
    "written_currencies",
]
