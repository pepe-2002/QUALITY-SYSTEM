"""Extraction de faits chiffrés depuis le texte d'une source.

On ne cherche pas à « comprendre » la page : on isole les grandeurs qui ont un
sens comparable — un prix, une durée, une distance, un pourcentage, une année —
avec leur contexte immédiat. C'est le seul matériau sur lequel une machine peut
constater objectivement que deux sources se contredisent.

Les fourchettes sont reconnues (« entre 15 000 et 17 500 FC ») : sans cela, un
prix ponctuel compris dans une fourchette passerait pour une contradiction,
alors que les deux sources disent la même chose.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# --- Normalisation ------------------------------------------------------------

#: Espaces utilisés comme séparateurs de milliers en français
_THIN_SPACES = "    "

_STOP = {
    "de", "des", "du", "la", "le", "les", "un", "une", "et", "ou", "a", "au",
    "aux", "en", "par", "pour", "sur", "dans", "avec", "est", "sont", "que",
    "qui", "ce", "cette", "ces", "son", "sa", "ses", "leur", "leurs", "plus",
    "moins", "entre", "environ", "selon", "soit", "the", "of", "and", "to",
    "in", "is", "for", "on", "with", "at", "by", "from", "about",
}

#: Mots d'unité : ils décrivent la grandeur, jamais le sujet dont on parle.
_UNIT_WORDS = {
    "franc", "francs", "comorien", "comoriens", "euro", "euros", "eur",
    "dollar", "dollars", "usd", "kmf", "ariary", "mga", "devise",
    "heure", "heures", "minute", "minutes", "jour", "jours", "journee",
    "journees", "semaine", "semaines", "mois", "annee", "annees",
    "kilometre", "kilometres", "metre", "metres", "mille", "milles",
    "nautique", "nautiques", "pourcent", "cent", "kilogramme", "kilogrammes",
    "environ", "moyenne", "total", "totale",
}

#: Nombres écrits en toutes lettres (fréquents pour les durées)
_WORD_NUMBERS = {
    "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
    "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10, "onze": 11,
    "douze": 12, "treize": 13, "quatorze": 14, "quinze": 15, "seize": 16,
    "vingt": 20, "trente": 30, "quarante": 40, "cinquante": 50,
    "soixante": 60, "cent": 100, "mille": 1000, "demi": 0.5,
}

#: Familles d'unités : motif → (famille, unité canonique, facteur)
_UNITS: list[tuple[str, str, str, float]] = [
    # --- monnaie (jamais convertie : on ne compare que devise identique) ---
    (r"(?:francs?\s+comoriens?|fc|kmf)", "money", "KMF", 1),
    (r"(?:euros?|eur|€)", "money", "EUR", 1),
    (r"(?:dollars?\s*(?:us)?|usd|\$)", "money", "USD", 1),
    (r"(?:ariary|mga)", "money", "MGA", 1),
    # --- durée (normalisée en minutes) ---
    (r"(?:heures?|hrs?|\bh\b)", "duration", "min", 60),
    (r"(?:minutes?|mins?|\bmn\b)", "duration", "min", 1),
    (r"(?:jours?|journées?)", "duration", "min", 1440),
    (r"(?:semaines?)", "duration", "min", 10080),
    # --- distance (normalisée en km) ---
    (r"(?:kilom[eè]tres?|\bkms?\b)", "distance", "km", 1),
    (r"(?:m[eè]tres?)", "distance", "km", 0.001),
    (r"(?:milles?\s+nautiques?|nm)", "distance", "km", 1.852),
    # --- divers ---
    (r"(?:pour\s*cent|%)", "percent", "%", 1),
    (r"(?:kilogrammes?|\bkgs?\b)", "weight", "kg", 1),
]

_NUMBER = r"\d{1,3}(?:[\s" + _THIN_SPACES + r"\.]\d{3})*(?:[,.]\d+)?|\d+(?:[,.]\d+)?"
_WORD_NUM = "|".join(sorted(_WORD_NUMBERS, key=len, reverse=True))

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])\s+|\n+")
_YEAR = re.compile(r"\b(19|20)\d{2}\b")


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def parse_number(raw: str) -> float | None:
    """Convertit « 15 000 », « 17,5 » ou « trois » en nombre.

    >>> parse_number("15 000")
    15000.0
    >>> parse_number("17,5")
    17.5
    >>> parse_number("trois")
    3.0
    """
    raw = raw.strip()
    word = _WORD_NUMBERS.get(_normalize(raw))
    if word is not None:
        return float(word)

    cleaned = raw
    for space in _THIN_SPACES + " ":
        cleaned = cleaned.replace(space, "")
    # « 1.234,56 » → séparateur de milliers puis décimale ; « 12.5 » → décimale
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif cleaned.count(".") == 1 and len(cleaned.split(".")[1]) == 3:
        cleaned = cleaned.replace(".", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


#: Nombre de mots retenus de part et d'autre du chiffre pour le décrire
CONTEXT_RADIUS = 6


def window_words(sentence: str, start: int, end: int, radius: int = CONTEXT_RADIUS) -> set[str]:
    """Mots entourant immédiatement un chiffre — ce qu'il mesure vraiment.

    Prendre la phrase entière comme contexte était trop grossier : sur un
    article encyclopédique, « 312 mètres » (hauteur d'origine), « 125 mètres »
    (côté de la base) et « 57 mètres » (premier étage) partagent tous « tour »
    et « hauteur », et passaient pour des contradictions. Le voisinage
    immédiat, lui, les distingue.
    """
    before = re.findall(r"[a-z]{3,}", _normalize(sentence[:start]))[-radius:]
    after = re.findall(r"[a-z]{3,}", _normalize(sentence[end:]))[:radius]
    return {w for w in before + after if w not in _STOP and w not in _UNIT_WORDS}


def context_words(sentence: str) -> set[str]:
    """Mots porteurs de sens d'une phrase — sert à savoir si deux faits
    parlent bien de la même chose.

    Les mots d'unité en sont exclus : sans cela, « 15 000 francs comoriens »
    (un billet) et « 45 000 francs comoriens » (une nuit d'hôtel) partagent
    « francs » et « comoriens » et passent pour une contradiction. L'unité est
    déjà comparée à part ; ici, on ne veut que le **sujet**.
    """
    words = re.findall(r"[a-z]{3,}", _normalize(sentence))
    return {w for w in words if w not in _STOP and w not in _UNIT_WORDS}


@dataclass
class Fact:
    """Une grandeur relevée dans une source."""

    kind: str          # money | duration | distance | percent | weight | year
    unit: str          # KMF, EUR, min, km, %, kg, an
    low: float
    high: float
    text: str          # expression telle qu'elle apparaît
    sentence: str
    source: int        # index de la source (1 = [S1])
    context: set[str] = field(default_factory=set)

    @property
    def is_range(self) -> bool:
        return self.high > self.low

    def describe(self) -> str:
        if self.kind == "year":
            # Une année ne prend pas de séparateur de milliers.
            return str(int(self.low))
        if self.kind == "duration":
            # Les durées sont stockées en minutes pour être comparables ;
            # « 1 440 min » ne se lit pas, « 1 jour » si.
            if self.is_range:
                return f"{_duration(self.low)}–{_duration(self.high)}"
            return _duration(self.low)
        if self.is_range:
            return f"{_fmt(self.low)}–{_fmt(self.high)} {self.unit}"
        return f"{_fmt(self.low)} {self.unit}"

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "unit": self.unit,
            "low": self.low,
            "high": self.high,
            "text": self.text,
            "source": self.source,
            "describe": self.describe(),
        }


def _duration(minutes: float) -> str:
    """Rend une durée dans l'unité où on l'exprime naturellement."""
    if minutes >= 1440:
        return f"{_fmt(minutes / 1440)} j"
    if minutes >= 60:
        return f"{_fmt(minutes / 60)} h"
    return f"{_fmt(minutes)} min"


def _fmt(value: float) -> str:
    if value == int(value):
        return f"{int(value):,}".replace(",", " ")
    return f"{value:g}"


def _sentences(text: str) -> list[str]:
    out = []
    for raw in _SENTENCE_SPLIT.split(text or ""):
        sentence = " ".join(raw.split())
        if 15 <= len(sentence) <= 500:
            out.append(sentence)
    return out


# Motifs compilés une fois : (famille, unité, facteur, regex simple, regex fourchette)
def _build_patterns() -> list[tuple[str, str, float, re.Pattern, re.Pattern]]:
    patterns = []
    for unit_re, kind, unit, factor in _UNITS:
        number = f"(?:{_NUMBER}|{_WORD_NUM})"
        simple = re.compile(
            rf"(?:({number})\s*(?:{unit_re})(?!\w))|(?:(?:{unit_re})\s*({number}))",
            re.IGNORECASE,
        )
        spread = re.compile(
            rf"(?:entre|de)\s+({number})\s*(?:{unit_re})?\s*(?:et|a|à|au?)\s+"
            rf"({number})\s*(?:{unit_re})(?!\w)",
            re.IGNORECASE,
        )
        patterns.append((kind, unit, factor, simple, spread))
    return patterns


_PATTERNS = _build_patterns()


def extract_facts(text: str, source: int, *, max_facts: int = 40) -> list[Fact]:
    """Relève les grandeurs mesurables d'un texte.

    >>> facts = extract_facts("Le tarif est de 15 000 francs comoriens.", 1)
    >>> facts[0].kind, facts[0].low, facts[0].unit
    ('money', 15000.0, 'KMF')
    """
    facts: list[Fact] = []

    for sentence in _sentences(text):
        for kind, unit, factor, simple, spread in _PATTERNS:
            # Les fourchettes d'abord : « entre 15 000 et 17 500 FC » est un
            # seul fait, pas deux valeurs qui se contredisent.
            consumed: list[tuple[int, int]] = []
            for match in spread.finditer(sentence):
                low = parse_number(match.group(1))
                high = parse_number(match.group(2))
                if low is None or high is None:
                    continue
                low, high = sorted((low * factor, high * factor))
                facts.append(
                    Fact(
                        kind, unit, low, high, match.group(0).strip(), sentence, source,
                        window_words(sentence, match.start(), match.end()),
                    )
                )
                consumed.append(match.span())

            for match in simple.finditer(sentence):
                if any(start <= match.start() < end for start, end in consumed):
                    continue
                raw = match.group(1) or match.group(2)
                value = parse_number(raw) if raw else None
                if value is None:
                    continue
                value *= factor
                facts.append(
                    Fact(
                        kind, unit, value, value, match.group(0).strip(), sentence, source,
                        window_words(sentence, match.start(), match.end()),
                    )
                )

        for match in _YEAR.finditer(sentence):
            year = float(match.group(0))
            facts.append(
                Fact(
                    "year", "an", year, year, match.group(0), sentence, source,
                    window_words(sentence, match.start(), match.end()),
                )
            )

        if len(facts) >= max_facts:
            break

    return facts[:max_facts]
