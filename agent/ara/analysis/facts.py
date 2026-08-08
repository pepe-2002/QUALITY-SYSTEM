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

import contextlib
import re
import unicodedata
from dataclasses import dataclass, field

from .currency import UNKNOWN as _UNKNOWN_CURRENCY
from .currency import resolve as _resolve

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

#: Devises reconnues par la version **gelée** de l'extracteur.
#:
#: C'est celle qui a produit H1, H2 et les expériences ADAPTIVE-V2 et
#: RESEARCH-V2. Elle ne bouge plus : ces résultats doivent rester
#: reproductibles.
_CURRENCIES_BASELINE: list[tuple[str, str, str, float]] = [
    (r"(?:francs?\s+comoriens?|fc|kmf)", "money", "KMF", 1),
    (r"(?:euros?|eur|€)", "money", "EUR", 1),
    (r"(?:dollars?\s*(?:us)?|usd|\$)", "money", "USD", 1),
    (r"(?:ariary|mga)", "money", "MGA", 1),
]

#: Qualificatifs qui transforment « franc » en une devise précise. Un franc
#: suivi de l'un d'eux est déjà reconnu ; le motif générique doit donc
#: l'ignorer, sinon la même somme serait comptée deux fois.
_FRANC_QUALIFIERS = (
    r"comoriens?|cfa|suisses?|pacifique|belges?|congolais|djiboutiens?"
    r"|guineens?|guinéens?|rwandais|burundais"
)

#: EXTRACT-V2 — devises ajoutées après le diagnostic.
#:
#: Le diagnostic avait montré que dix pannes sur dix venaient d'un même
#: aveuglement : une somme écrite en « francs », sans devise précisée, n'était
#: pas vue du tout. La correction ne vise pas ce cas particulier — elle
#: élargit la reconnaissance aux devises qu'un agent francophone rencontre
#: réellement.
#:
#: Deux prudences volontaires :
#:
#: * « livre » n'est reconnu qu'accompagné de « sterling » : seul, le mot
#:   désigne aussi un ouvrage et une unité de masse ;
#: * un franc non qualifié reçoit l'unité générique ``FRANC``, jamais ``KMF`` :
#:   deux francs de pays différents ne doivent pas être comparés entre eux.
_CURRENCIES_V2: list[tuple[str, str, str, float]] = _CURRENCIES_BASELINE + [
    (r"(?:francs?\s+cfa|fcfa|xof|xaf)", "money", "XOF", 1),
    (r"(?:francs?\s+suisses?|chf)", "money", "CHF", 1),
    # Un franc sans qualificatif n'est **pas** une devise : c'est un montant
    # dont la devise reste à établir. L'unité est provisoire (`UNKNOWN`) et
    # sera résolue par le contexte — ou restera inconnue.
    (rf"(?:francs?(?!\s+(?:{_FRANC_QUALIFIERS})))", "money", "UNKNOWN", 1),
    (r"(?:livres?\s+sterling|gbp|£)", "money", "GBP", 1),
    (r"(?:yens?|jpy|¥)", "money", "JPY", 1),
    (r"(?:yuans?|renminbi|cny)", "money", "CNY", 1),
    (r"(?:roupies?|inr|₹)", "money", "INR", 1),
    (r"(?:dirhams?|aed|mad)", "money", "DIRHAM", 1),
    (r"(?:shillings?|kes|tzs|ugx)", "money", "SHILLING", 1),
    (r"(?:rands?|zar)", "money", "ZAR", 1),
    (r"(?:pesos?|mxn|ars|clp)", "money", "PESO", 1),
    (r"(?:roubles?|rub|₽)", "money", "RUB", 1),
    (r"(?:couronnes?|sek|nok|dkk)", "money", "COURONNE", 1),
    (r"(?:nairas?|ngn)", "money", "NGN", 1),
    (r"(?:dinars?|dzd|tnd|mad̸)", "money", "DINAR", 1),
    (r"(?:riyals?|rials?|sar)", "money", "RIAL", 1),
    (r"(?:wons?|krw|₩)", "money", "KRW", 1),
    (r"(?:birrs?|etb)", "money", "ETB", 1),
    (r"(?:cedis?|ghs)", "money", "GHS", 1),
    (r"(?:shekels?|ils|₪)", "money", "ILS", 1),
    (r"(?:zlotys?|pln)", "money", "PLN", 1),
    (r"(?:bahts?|thb|฿)", "money", "THB", 1),
    (r"(?:ringgits?|myr)", "money", "MYR", 1),
]

#: Unités non monétaires — communes aux deux versions.
_MEASURES: list[tuple[str, str, str, float]] = [
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

#: Jeux d'unités par version d'extracteur.
UNITS_BY_VERSION: dict[str, list] = {
    "baseline": _CURRENCIES_BASELINE + _MEASURES,
    "v2": _CURRENCIES_V2 + _MEASURES,
}

#: Compatibilité : le jeu d'unités de la version gelée.
_UNITS = UNITS_BY_VERSION["baseline"]

_NUMBER = r"\d{1,3}(?:[\s" + _THIN_SPACES + r"\.]\d{3})*(?:[,.]\d+)?|\d+(?:[,.]\d+)?"
_WORD_NUM = "|".join(sorted(_WORD_NUMBERS, key=len, reverse=True))

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])\s+|\n+")
_YEAR = re.compile(r"\b(19|20)\d{2}\b")

#: Heure du jour — à ne pas confondre avec une durée.
#: « La traversée dure 3 heures » et « le départ est à 7 heures » sont deux
#: grandeurs différentes ; les mélanger faisait croire à l'agent qu'il avait
#: l'horaire alors qu'il n'avait qu'une durée. Défaut trouvé par le laboratoire.
_TIME = re.compile(
    r"(?:(?:a|à|vers|des|dès|jusqu'a|jusqu'à)\s+(\d{1,2})\s*(?:h\b|heures?\b))"
    r"|(?:\b(\d{1,2})\s*h\s*(\d{2})\b)"
    r"|(?:\b(\d{1,2})\s*(?:h\b|heures?\b)\s*(?:du|le)\s+(?:matin|soir|midi))",
    re.IGNORECASE,
)


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
    #: Confiance dans l'**identification de la devise** (montants seulement) :
    #: « certaine » quand la devise est écrite, « probable » quand elle est
    #: déduite du contexte, « inconnue » quand rien ne permet de trancher.
    #: Les grandeurs non monétaires sont toujours « certaine » : un kilomètre
    #: est un kilomètre.
    confidence: str = "certaine"

    @property
    def is_range(self) -> bool:
        return self.high > self.low

    def describe(self) -> str:
        if self.kind == "year":
            # Une année ne prend pas de séparateur de milliers.
            return str(int(self.low))
        if self.kind == "time":
            entier = int(self.low)
            minutes = round((self.low - entier) * 60)
            return f"{entier} h" if not minutes else f"{entier} h {minutes:02d}"
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
def _build_patterns(units=None) -> list[tuple[str, str, float, re.Pattern, re.Pattern]]:
    patterns = []
    for unit_re, kind, unit, factor in (units if units is not None else _UNITS):
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


_PATTERNS_BY_VERSION = {
    version: _build_patterns(units) for version, units in UNITS_BY_VERSION.items()
}

#: Version active de l'extracteur.
#:
#: « v2 » depuis la correction des devises. Les expériences déjà publiées
#: épinglent explicitement « baseline » le temps de leur exécution : c'est ce
#: qui garde leurs chiffres reproductibles pendant que le système avance.
EXTRACTOR_VERSION = "v2"

_active_version = EXTRACTOR_VERSION


def set_extractor(version: str) -> str:
    """Change la version active. Retourne la précédente."""
    global _active_version
    if version not in _PATTERNS_BY_VERSION:
        raise ValueError(f"version d'extracteur inconnue : {version}")
    ancienne, _active_version = _active_version, version
    return ancienne


@contextlib.contextmanager
def extractor(version: str):
    """Épingle une version d'extracteur le temps d'un bloc.

    Utilisé par le laboratoire pour rejouer une expérience avec l'extracteur
    qui l'a produite. Sans cela, corriger l'extracteur réécrirait des
    résultats publiés.
    """
    ancienne = set_extractor(version)
    try:
        yield version
    finally:
        set_extractor(ancienne)


#: Compatibilité : motifs de la version gelée.
_PATTERNS = _PATTERNS_BY_VERSION["baseline"]


def _resolve_currency(unit: str, sentence: str, document: str) -> tuple[str, str]:
    """Devise effective d'une unité provisoire, et confiance associée.

    Seuls les montants sans devise écrite passent par la résolution : un
    « franc comorien » reste un franc comorien, avec la confiance maximale.
    """
    if unit != _UNKNOWN_CURRENCY:
        return unit, "certaine"
    return _resolve(sentence, document)


def extract_facts(text: str, source: int, *, max_facts: int = 40) -> list[Fact]:
    """Relève les grandeurs mesurables d'un texte.

    >>> facts = extract_facts("Le tarif est de 15 000 francs comoriens.", 1)
    >>> facts[0].kind, facts[0].low, facts[0].unit
    ('money', 15000.0, 'KMF')
    """
    facts: list[Fact] = []
    patterns = _PATTERNS_BY_VERSION[_active_version]
    # EXTRACTION-V2 : le document entier sert de contexte pour identifier la
    # devise d'un montant écrit sans elle. Calculé une fois, pas par phrase.
    document = text if _active_version != "baseline" else ""

    for sentence in _sentences(text):
        # Les heures du jour d'abord : elles consomment leur empan pour que la
        # même expression ne soit pas relue comme une durée.
        heures: list[tuple[int, int]] = []
        for match in _TIME.finditer(sentence):
            groupes = [g for g in match.groups() if g is not None]
            if not groupes:
                continue
            heure = parse_number(groupes[0])
            if heure is None or not 0 <= heure <= 24:
                continue
            minutes = parse_number(groupes[1]) if len(groupes) > 1 else 0
            valeur = heure + (minutes or 0) / 60
            facts.append(
                Fact(
                    "time", "h", valeur, valeur, match.group(0).strip(), sentence,
                    source, window_words(sentence, match.start(), match.end()),
                )
            )
            heures.append(match.span())

        for kind, unit, factor, simple, spread in patterns:
            # Les fourchettes d'abord : « entre 15 000 et 17 500 FC » est un
            # seul fait, pas deux valeurs qui se contredisent.
            consumed: list[tuple[int, int]] = []
            for match in spread.finditer(sentence):
                low = parse_number(match.group(1))
                high = parse_number(match.group(2))
                if low is None or high is None:
                    continue
                low, high = sorted((low * factor, high * factor))
                devise, confiance = _resolve_currency(unit, sentence, document)
                facts.append(
                    Fact(
                        kind, devise, low, high, match.group(0).strip(), sentence,
                        source, window_words(sentence, match.start(), match.end()),
                        confidence=confiance,
                    )
                )
                consumed.append(match.span())

            for match in simple.finditer(sentence):
                if any(start <= match.start() < end for start, end in consumed):
                    continue
                if any(start <= match.start() < end for start, end in heures):
                    continue
                raw = match.group(1) or match.group(2)
                value = parse_number(raw) if raw else None
                if value is None:
                    continue
                value *= factor
                devise, confiance = _resolve_currency(unit, sentence, document)
                facts.append(
                    Fact(
                        kind, devise, value, value, match.group(0).strip(), sentence,
                        source, window_words(sentence, match.start(), match.end()),
                        confidence=confiance,
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
