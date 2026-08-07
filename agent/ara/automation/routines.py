"""Routines : des tâches que l'agent relance tout seul.

C'est le seul endroit du système où l'agent agit **sans que personne ne le
demande sur le moment**. Le reste du projet part du principe qu'un humain
appuie sur un bouton ; ici, non. Toute la conception en découle :

* une routine ne naît **que** d'un horaire compris (`parse_schedule`), jamais
  d'une supposition ;
* elle porte des **garde-fous** — nombre d'exécutions par jour, échecs
  consécutifs, batterie minimale — et s'éteint d'elle-même en disant pourquoi ;
* elle n'obtient **aucun droit supplémentaire** : ses tâches passent par le
  même orchestrateur, la même liste blanche d'outils, les mêmes confirmations.
  Une routine ne peut donc pas publier ou supprimer quoi que ce soit sans
  qu'un humain valide, et une action sensible programmée à 3 h du matin
  échoue proprement au lieu de s'exécuter en douce (spec §15, §16).
"""

from __future__ import annotations

import json
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from ..core.errors import AraError
from .schedule import Schedule, parse_schedule

#: Au-delà, on considère que la routine s'emballe et on l'arrête.
MAX_RUNS_PER_DAY = 24
#: Trois échecs d'affilée : ce n'est plus un incident, c'est une routine cassée.
MAX_CONSECUTIVE_FAILURES = 3
#: En dessous de ce niveau de batterie, on reporte plutôt que de vider le
#: téléphone de quelqu'un pendant la nuit.
DEFAULT_MIN_BATTERY = 20
MAX_ROUTINES = 20


class RoutineError(AraError):
    """Routine invalide ou refusée."""

    code = "routine_error"


@dataclass
class Routine:
    """Une demande répétée, et la trace de ce qu'elle a donné."""

    routine_id: str
    prompt: str
    schedule: dict[str, Any]
    label: str = ""
    enabled: bool = True
    created_at: float = field(default_factory=time.time)
    next_run: float = 0.0
    last_run: float | None = None
    last_task_id: str = ""
    last_status: str = ""
    runs: int = 0
    failures: int = 0            # échecs consécutifs
    runs_today: int = 0
    day_stamp: str = ""
    disabled_reason: str = ""
    min_battery: int = DEFAULT_MIN_BATTERY
    notify: bool = True

    # -- lecture -----------------------------------------------------------

    def plan(self) -> Schedule:
        return Schedule.from_dict(self.schedule)

    def describe(self) -> str:
        return self.plan().describe()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["describe"] = self.describe()
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Routine":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in data.items() if k in known})

    # -- vie de la routine -------------------------------------------------

    def is_due(self, moment: float) -> bool:
        return self.enabled and 0 < self.next_run <= moment

    def reschedule(self, moment: float) -> None:
        self.next_run = self.plan().next_after(moment)

    def disable(self, reason: str) -> None:
        """Éteint la routine **en disant pourquoi** : jamais de mort silencieuse."""
        self.enabled = False
        self.disabled_reason = reason

    def note_start(self, moment: float, task_id: str) -> None:
        jour = time.strftime("%Y-%m-%d", time.localtime(moment))
        if jour != self.day_stamp:
            self.day_stamp = jour
            self.runs_today = 0
        self.runs_today += 1
        self.runs += 1
        self.last_run = moment
        self.last_task_id = task_id
        self.last_status = "running"

    def note_result(self, ok: bool, status: str) -> None:
        self.last_status = status
        if ok:
            self.failures = 0
            return
        self.failures += 1
        if self.failures >= MAX_CONSECUTIVE_FAILURES:
            self.disable(
                f"{self.failures} échecs consécutifs — routine suspendue. "
                "Corrigez la demande puis réactivez-la."
            )

    def exceeded_today(self) -> bool:
        jour = time.strftime("%Y-%m-%d", time.localtime())
        return self.day_stamp == jour and self.runs_today >= MAX_RUNS_PER_DAY


def build_routine(
    prompt: str,
    when: str,
    *,
    label: str = "",
    min_battery: int = DEFAULT_MIN_BATTERY,
    notify: bool = True,
    now: float | None = None,
) -> Routine:
    """Crée une routine, ou refuse en expliquant.

    Refuse plutôt que de deviner : un horaire mal compris ferait tourner
    l'agent quand personne ne l'attend.
    """
    demande = " ".join(str(prompt or "").split())
    if len(demande) < 5:
        raise RoutineError("La demande de la routine est vide ou trop courte.")
    if len(demande) > 2000:
        raise RoutineError("Demande trop longue pour une routine (2000 caractères).")

    plan = parse_schedule(when)
    if plan is None:
        raise RoutineError(
            f"Je n'ai pas compris « {when} ». Exemples acceptés : "
            "« chaque matin », « tous les jours à 7h30 », « chaque lundi à 8h », "
            "« toutes les 6 heures »."
        )

    moment = time.time() if now is None else now
    routine = Routine(
        routine_id=uuid.uuid4().hex[:12],
        prompt=demande,
        schedule=plan.to_dict(),
        label=(label or demande)[:80],
        min_battery=max(0, min(100, int(min_battery))),
        notify=bool(notify),
    )
    routine.reschedule(moment)
    return routine


class RoutineStore:
    """Persistance des routines — un seul fichier JSON, écrit atomiquement."""

    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self._lock = threading.RLock()

    def _load(self) -> dict[str, Routine]:
        if not self.path.is_file():
            return {}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
        routines: dict[str, Routine] = {}
        for item in data.get("routines", []):
            try:
                routine = Routine.from_dict(item)
            except TypeError:
                continue
            routines[routine.routine_id] = routine
        return routines

    def _write(self, routines: dict[str, Routine]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            {"routines": [asdict(r) for r in routines.values()]},
            ensure_ascii=False,
            indent=1,
        )
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(payload, encoding="utf-8")
        tmp.replace(self.path)

    # -- opérations --------------------------------------------------------

    def list(self) -> list[Routine]:
        with self._lock:
            routines = list(self._load().values())
        routines.sort(key=lambda r: (not r.enabled, r.next_run or 0))
        return routines

    def get(self, routine_id: str) -> Routine | None:
        with self._lock:
            return self._load().get(routine_id)

    def add(self, routine: Routine) -> Routine:
        with self._lock:
            routines = self._load()
            if len(routines) >= MAX_ROUTINES:
                raise RoutineError(
                    f"Trop de routines ({MAX_ROUTINES} maximum). "
                    "Supprimez-en une avant d'en ajouter."
                )
            routines[routine.routine_id] = routine
            self._write(routines)
        return routine

    def save(self, routine: Routine) -> Routine:
        with self._lock:
            routines = self._load()
            routines[routine.routine_id] = routine
            self._write(routines)
        return routine

    def delete(self, routine_id: str) -> bool:
        with self._lock:
            routines = self._load()
            if routine_id not in routines:
                return False
            del routines[routine_id]
            self._write(routines)
        return True

    def due(self, moment: float | None = None) -> list[Routine]:
        moment = time.time() if moment is None else moment
        return [routine for routine in self.list() if routine.is_due(moment)]


__all__ = [
    "DEFAULT_MIN_BATTERY",
    "MAX_CONSECUTIVE_FAILURES",
    "MAX_ROUTINES",
    "MAX_RUNS_PER_DAY",
    "Routine",
    "RoutineError",
    "RoutineStore",
    "build_routine",
]
