"""L'ordonnanceur : ce qui réveille l'agent quand personne ne le regarde.

Un fil d'exécution unique, qui se réveille toutes les :data:`TICK_SECONDS`
secondes, demande au registre ce qui est dû, et lance. Le cœur de la décision
— :meth:`Scheduler.decide` — est une fonction **pure** : on lui donne l'heure
et l'état du téléphone, elle répond quoi lancer et ce qu'elle a écarté. C'est
ce qui rend l'automatisation testable sans attendre demain matin.

Ce que l'ordonnanceur ne fait pas, volontairement :

* il ne rattrape pas les exécutions manquées. Le téléphone était éteint à 7 h ?
  La routine ne se déclenche pas à 11 h en prétendant être à l'heure ; elle
  attend le lendemain. Un rattrapage aveugle produirait une rafale de tâches
  au premier démarrage de la journée.
* il ne lance jamais deux fois la même routine en parallèle.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from ..core.errors import AraError
from .routines import Routine, RoutineStore

#: Rythme du réveil. Une minute suffit : les routines se comptent en heures.
TICK_SECONDS = 60
#: Au-delà, la tâche d'une routine est considérée comme perdue et le verrou
#: est relâché, sinon une tâche bloquée gèlerait la routine pour toujours.
RUN_TIMEOUT_SECONDS = 1800


@dataclass
class Decision:
    """Ce que l'ordonnanceur a décidé à un instant donné."""

    to_run: list[Routine] = field(default_factory=list)
    skipped: list[tuple[Routine, str]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "to_run": [r.routine_id for r in self.to_run],
            "skipped": [{"id": r.routine_id, "reason": reason} for r, reason in self.skipped],
        }


class Scheduler:
    """Fait tourner les routines. Un par serveur."""

    def __init__(
        self,
        service: Any,
        store: RoutineStore,
        *,
        battery_reader: Callable[[], int | None] | None = None,
        tick_seconds: float = TICK_SECONDS,
    ) -> None:
        self.service = service
        self.store = store
        self.tick_seconds = tick_seconds
        self._battery_reader = battery_reader or _read_battery
        self._running: dict[str, float] = {}   # routine_id → début de l'exécution
        self._lock = threading.Lock()
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.last_error = ""

    # -- décision (pure, donc testable) ------------------------------------

    def decide(self, moment: float, *, battery: int | None = None) -> Decision:
        """Que lancer à cet instant, et pourquoi écarter le reste."""
        decision = Decision()
        for routine in self.store.list():
            if not routine.is_due(moment):
                continue
            reason = self._refuse(routine, moment, battery)
            if reason:
                decision.skipped.append((routine, reason))
            else:
                decision.to_run.append(routine)
        return decision

    def _refuse(self, routine: Routine, moment: float, battery: int | None) -> str:
        with self._lock:
            started = self._running.get(routine.routine_id)
        if started is not None and moment - started < RUN_TIMEOUT_SECONDS:
            return "l'exécution précédente n'est pas terminée"
        if routine.exceeded_today():
            return "plafond d'exécutions atteint pour aujourd'hui"
        if battery is not None and routine.min_battery and battery < routine.min_battery:
            return f"batterie à {battery} % (minimum {routine.min_battery} %)"
        return ""

    # -- exécution ---------------------------------------------------------

    def tick(self, moment: float | None = None) -> Decision:
        """Un réveil : décide, lance, replanifie. Retourne ce qui a été décidé."""
        moment = time.time() if moment is None else moment
        decision = self.decide(moment, battery=self._battery_reader())

        for routine, reason in decision.skipped:
            # Une exécution écartée est **reportée**, pas perdue : sans cela,
            # une batterie basse à 7 h bloquerait la routine indéfiniment.
            routine.reschedule(moment)
            routine.last_status = f"reportée : {reason}"
            self.store.save(routine)

        for routine in decision.to_run:
            self._launch(routine, moment)
        return decision

    def _launch(self, routine: Routine, moment: float) -> None:
        try:
            record = self.service.start(routine.prompt)
        except AraError as exc:
            routine.note_result(False, f"refus : {exc}")
            routine.reschedule(moment)
            self.store.save(routine)
            return

        with self._lock:
            self._running[routine.routine_id] = moment
        routine.note_start(moment, record.task_id)
        routine.reschedule(moment)
        self.store.save(routine)

        watcher = threading.Thread(
            target=self._watch,
            args=(routine.routine_id, record.task_id),
            name=f"ara-routine-{routine.routine_id}",
            daemon=True,
        )
        watcher.start()

    def _watch(self, routine_id: str, task_id: str) -> None:
        """Attend la fin de la tâche, met la routine à jour, prévient."""
        try:
            record = self.service.wait(task_id, timeout=RUN_TIMEOUT_SECONDS)
        finally:
            with self._lock:
                self._running.pop(routine_id, None)

        routine = self.store.get(routine_id)
        if routine is None:
            return
        if record is None:
            routine.note_result(False, "tâche introuvable")
        else:
            ok = record.status == "done"
            routine.note_result(ok, record.status)
        self.store.save(routine)

        if routine.notify and record is not None:
            self._notify(routine, record)

    def _notify(self, routine: Routine, record: Any) -> None:
        """Prévient sur le téléphone — sans jamais faire échouer la routine.

        La notification passe par la boîte à outils, donc par la liste blanche
        (spec §16) : `notify_phone` révoqué, aucune notification. Et elle reste
        un confort : sur un ordinateur, ou sans Termux:API, elle est impossible
        — ce n'est pas une erreur de la tâche.
        """
        from .notify import routine_toolbox  # import tardif : évite un cycle

        titre = routine.label or "Routine ARA"
        if record.status == "done":
            corps = record.answer[:200] if record.answer else "terminé"
        else:
            corps = "échec : " + (record.errors[0] if record.errors else record.status)
        try:
            toolbox = routine_toolbox(self.service.settings, self.service.permissions)
            toolbox.call(
                "notify_phone",
                title=titre,
                message=corps,
                notification_id=f"ara-{routine.routine_id}",
            )
        except Exception as exc:  # noqa: BLE001 — un confort ne casse rien
            self.last_error = f"notification impossible : {exc}"

    # -- fil d'exécution ---------------------------------------------------

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        if self.running:
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="ara-scheduler", daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 2.0) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout)

    def _loop(self) -> None:
        while not self._stop.is_set():
            try:
                self.tick()
            except Exception as exc:  # noqa: BLE001 — l'ordonnanceur ne doit jamais mourir
                self.last_error = f"{type(exc).__name__}: {exc}"
            self._stop.wait(self.tick_seconds)


def _read_battery() -> int | None:
    """Niveau de batterie, ou ``None`` si la machine n'en a pas.

    Une batterie inconnue ne bloque **rien** : sur un ordinateur, les routines
    tournent normalement.
    """
    from ..android.bridge import detect

    device = detect()
    if not device.has("termux-battery-status"):
        return None
    import json

    from ..android.bridge import run_termux

    try:
        data = json.loads(run_termux("termux-battery-status") or "{}")
        niveau = data.get("percentage")
        return int(niveau) if niveau is not None else None
    except (AraError, json.JSONDecodeError, TypeError, ValueError):
        return None


__all__ = ["Decision", "RUN_TIMEOUT_SECONDS", "TICK_SECONDS", "Scheduler"]
