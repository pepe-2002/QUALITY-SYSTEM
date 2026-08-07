"""Horaires de routine : comprendre « chaque matin » sans rien deviner.

Règle de conception : **une phrase non comprise ne produit pas d'horaire**.
Un agent qui devine « tous les jours à 9 h » parce qu'il n'a pas su lire est
pire qu'un agent qui refuse : le propriétaire découvrirait des exécutions
qu'il n'a pas demandées. :func:`parse_schedule` retourne donc ``None`` quand
elle ne sait pas, et l'appelant refuse de créer la routine.

Tout est calculé en heure **locale** du téléphone, puisque c'est ce que veut
dire « chaque matin » pour son propriétaire.
"""

from __future__ import annotations

import re
import time
import unicodedata
from dataclasses import dataclass

#: Une routine ne peut pas tourner plus souvent que cela. En dessous, on ne
#: rend pas service : on vide la batterie.
MIN_INTERVAL_MINUTES = 15

#: Moments de la journée nommés, avec l'heure qu'ils désignent.
MOMENTS: dict[str, tuple[int, int]] = {
    "matin": (7, 0),
    "midi": (12, 0),
    "apres-midi": (15, 0),
    "soir": (19, 0),
    "nuit": (22, 0),
}

JOURS: dict[str, int] = {
    "lundi": 0, "mardi": 1, "mercredi": 2, "jeudi": 3,
    "vendredi": 4, "samedi": 5, "dimanche": 6,
}

JOURS_LISIBLES = {value: key for key, value in JOURS.items()}

_JOUR = 24 * 3600


def _fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9:h\s-]", " ", text)


@dataclass(frozen=True)
class Schedule:
    """Quand une routine doit tourner."""

    kind: str            # daily | weekly | interval
    hour: int = 0
    minute: int = 0
    weekday: int = 0     # 0 = lundi (kind == weekly)
    minutes: int = 60    # kind == interval
    label: str = ""

    def to_dict(self) -> dict:
        return {
            "kind": self.kind, "hour": self.hour, "minute": self.minute,
            "weekday": self.weekday, "minutes": self.minutes, "label": self.label,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Schedule":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in (data or {}).items() if k in known})

    def describe(self) -> str:
        if self.kind == "daily":
            return f"tous les jours à {self.hour:02d}:{self.minute:02d}"
        if self.kind == "weekly":
            jour = JOURS_LISIBLES.get(self.weekday, "lundi")
            return f"chaque {jour} à {self.hour:02d}:{self.minute:02d}"
        if self.minutes % 60 == 0:
            heures = self.minutes // 60
            return f"toutes les {heures} heure{'s' if heures > 1 else ''}"
        return f"toutes les {self.minutes} minutes"

    # -- calcul de la prochaine échéance -----------------------------------

    def next_after(self, moment: float) -> float:
        """Premier instant d'exécution **strictement** après ``moment``."""
        if self.kind == "interval":
            return moment + max(MIN_INTERVAL_MINUTES, self.minutes) * 60

        candidat = self._at(time.localtime(moment))
        if candidat <= moment:
            candidat = self._at(time.localtime(moment + _JOUR))

        if self.kind == "weekly":
            # tm_wday : 0 = lundi, comme JOURS
            for _ in range(8):
                if time.localtime(candidat).tm_wday == self.weekday and candidat > moment:
                    break
                candidat = self._at(time.localtime(candidat + _JOUR))
        return candidat

    def _at(self, local: time.struct_time) -> float:
        """Horodatage de l'heure voulue, le jour de ``local``.

        On repasse par `mktime` avec ``tm_isdst = -1`` pour que le passage à
        l'heure d'été ne décale pas les routines d'une heure.
        """
        return time.mktime(
            (local.tm_year, local.tm_mon, local.tm_mday,
             self.hour, self.minute, 0, 0, 0, -1)
        )


# -- lecture d'une phrase ---------------------------------------------------

_HEURE = re.compile(
    r"(?:a|vers|des)\s+(\d{1,2})\s*(?:h|:)\s*(\d{2})?"   # à 7h30, à 7:30, à 7h
    r"|\b(\d{1,2})\s*h\s*(\d{2})\b"                       # 7h30
    r"|\b(\d{1,2})\s*h\b"                                 # 7h
)

_INTERVALLE = re.compile(
    r"\b(?:toutes?|tous)\s+les\s+(\d{1,3})\s*(minutes?|min|heures?|h)\b"
)

_QUOTIDIEN = re.compile(r"\b(?:chaque|tous\s+les)\s+jours?\b|\bquotidien\w*\b|\bchaque\s+matin\b")


def _lire_heure(texte: str) -> tuple[int, int] | None:
    match = _HEURE.search(texte)
    if not match:
        return None
    groupes = [g for g in match.groups()]
    if groupes[0] is not None:
        heure, minute = int(groupes[0]), int(groupes[1] or 0)
    elif groupes[2] is not None:
        heure, minute = int(groupes[2]), int(groupes[3] or 0)
    else:
        heure, minute = int(groupes[4]), 0
    if not (0 <= heure <= 23 and 0 <= minute <= 59):
        return None
    return heure, minute


def parse_schedule(text: str) -> Schedule | None:
    """Traduit une phrase en :class:`Schedule`, ou ``None`` si elle est floue.

    >>> parse_schedule("chaque matin").describe()
    'tous les jours à 07:00'
    >>> parse_schedule("chaque lundi à 8h").describe()
    'chaque lundi à 08:00'
    >>> parse_schedule("toutes les 6 heures").describe()
    'toutes les 6 heures'
    >>> parse_schedule("de temps en temps") is None
    True
    """
    brut = str(text or "")
    texte = _fold(brut)
    if not texte.strip():
        return None

    # 1. « toutes les N heures / minutes »
    match = _INTERVALLE.search(texte)
    if match:
        quantite = int(match.group(1))
        unite = match.group(2)
        minutes = quantite * 60 if unite.startswith("h") else quantite
        if minutes < MIN_INTERVAL_MINUTES:
            minutes = MIN_INTERVAL_MINUTES
        if minutes > 7 * 24 * 60:
            return None
        return Schedule(kind="interval", minutes=minutes, label=brut.strip())

    # 2. heure explicite, ou moment nommé
    heure = _lire_heure(texte)
    if heure is None:
        for nom, valeur in MOMENTS.items():
            if re.search(rf"\b{nom}\b", texte):
                heure = valeur
                break
    if heure is None:
        return None

    # 3. jour de la semaine → hebdomadaire
    for nom, index in JOURS.items():
        if re.search(rf"\b{nom}s?\b", texte):
            return Schedule(
                kind="weekly", hour=heure[0], minute=heure[1],
                weekday=index, label=brut.strip(),
            )

    # 4. quotidien — mais seulement si la phrase le dit. « à 7h » tout seul
    #    n'est pas une récurrence : c'est une heure. On refuse plutôt que
    #    d'inventer une répétition que personne n'a demandée.
    if _QUOTIDIEN.search(texte) or any(
        re.search(rf"\b(?:chaque|tous\s+les)\s+{nom}\b", texte) for nom in MOMENTS
    ) or re.search(r"\b(?:le|au)\s+(?:matin|soir|midi)\b", texte):
        return Schedule(kind="daily", hour=heure[0], minute=heure[1], label=brut.strip())

    return None


__all__ = [
    "JOURS",
    "MIN_INTERVAL_MINUTES",
    "MOMENTS",
    "Schedule",
    "parse_schedule",
]
