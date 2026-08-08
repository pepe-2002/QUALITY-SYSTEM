"""Serveur HTTP de l'agent — `python -m ara.api.server`.

Bâti sur `http.server` de la bibliothèque standard : aucune dépendance, donc
installable sur un téléphone (Termux) sans compilation. Le flux d'événements
utilise Server-Sent Events, ce que tout navigateur Android sait lire nativement.

Sécurité : si `ARA_TOKEN` est défini, toutes les routes `/api/` exigent ce
jeton (en-tête `X-ARA-Token` ou paramètre `?token=`). Sans jeton, le serveur
n'écoute que ce que l'utilisateur a décidé via `ARA_HOST`.
"""

from __future__ import annotations

import json
import mimetypes
import os
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from ..agents.engines import engine_name
from ..automation.routines import DEFAULT_MIN_BATTERY, build_routine
from ..core.complexity import DEFAULT_CONTROLLER
from ..core.config import Settings, get_settings
from ..core.errors import AraError
from ..core.events import STAGE_ORDER
from ..providers.llm import available_llms
from ..providers.search import available_engines
from ..service import TaskService
from ..tools.registry import REGISTRY

STATIC_DIR = Path(__file__).parent / "static"
MAX_PROMPT_CHARS = 4000


class AraHandler(BaseHTTPRequestHandler):
    """Routeur minimal. Une instance par requête."""

    protocol_version = "HTTP/1.1"
    server_version = "ARA/0.1"

    # -- utilitaires -------------------------------------------------------

    @property
    def service(self) -> TaskService:
        return self.server.service  # type: ignore[attr-defined]

    @property
    def settings(self) -> Settings:
        return self.server.settings  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: Any) -> None:  # moins bavard
        if os.environ.get("ARA_VERBOSE"):
            super().log_message(fmt, *args)

    def _send(self, status: int, body: bytes, content_type: str, extra: dict | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _json(self, payload: Any, status: int = 200) -> None:
        self._send(
            status,
            json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            "application/json; charset=utf-8",
        )

    def _error(self, status: int, message: str) -> None:
        self._json({"error": message}, status)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(min(length, 1_000_000))
        try:
            data = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
        return data if isinstance(data, dict) else {}

    def _authorized(self, query: dict[str, list[str]]) -> bool:
        token = Settings.secret("ARA_TOKEN")
        if not token:
            return True
        provided = self.headers.get("X-ARA-Token") or (query.get("token") or [""])[0]
        return provided == token

    # -- routage -----------------------------------------------------------

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path.startswith("/api/"):
            if not self._authorized(query):
                return self._error(401, "Jeton manquant ou invalide.")
            return self._api_get(path, query)

        return self._static(path)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        if not parsed.path.startswith("/api/"):
            return self._error(404, "Route inconnue.")
        if not self._authorized(query):
            return self._error(401, "Jeton manquant ou invalide.")
        return self._api_post(parsed.path)

    # -- API ---------------------------------------------------------------

    def _api_get(self, path: str, query: dict[str, list[str]]) -> None:
        if path == "/api/health":
            from .. import __phase__, __version__

            return self._json(
                {"status": "ok", "version": __version__, "phase": __phase__}
            )

        if path == "/api/config":
            return self._json(
                {
                    "stages": [stage.value for stage in STAGE_ORDER],
                    "llm": {
                        "selected": self.settings.llm_provider,
                        "providers": available_llms(),
                    },
                    "search": {
                        "selected": self.settings.search_provider,
                        "providers": available_engines(),
                    },
                    "versions": {
                        "controller": DEFAULT_CONTROLLER,
                        "research_engine": engine_name(),
                    },
                    "tools": [
                        {
                            **tool.to_dict(),
                            "allowed": self.service.permissions.is_allowed(name),
                        }
                        for name, tool in sorted(REGISTRY.items())
                    ],
                    "limits": {
                        "max_research_steps": self.settings.max_research_steps,
                        "max_design_iterations": self.settings.max_design_iterations,
                        "design_target_score": self.settings.design_target_score,
                        "max_task_seconds": self.settings.max_task_seconds,
                    },
                }
            )

        if path == "/api/tasks":
            limit = int((query.get("limit") or ["50"])[0] or 50)
            return self._json({"tasks": self.service.history(min(limit, 200))})

        if path == "/api/phone":
            from ..android.bridge import capabilities

            return self._json(capabilities())

        if path == "/api/routines":
            return self._json(
                {
                    "routines": [r.to_dict() for r in self.service.routines.list()],
                    "scheduler": {
                        "enabled": self.settings.automation_enabled,
                        "running": self.service.scheduler.running,
                        "last_error": self.service.scheduler.last_error,
                    },
                }
            )

        parts = [p for p in path.split("/") if p]
        # /api/tasks/<id>[/events|/files/<name>]
        if len(parts) >= 3 and parts[0] == "api" and parts[1] == "tasks":
            task_id = parts[2]
            if len(parts) == 3:
                record = self.service.get(task_id)
                if record is None:
                    return self._error(404, "Tâche inconnue.")
                return self._json(record.to_dict())
            if len(parts) == 4 and parts[3] == "events":
                return self._events(task_id)
            if len(parts) == 5 and parts[3] == "files":
                return self._file(task_id, urllib.parse.unquote(parts[4]))

        return self._error(404, "Route inconnue.")

    def _api_post(self, path: str) -> None:
        if path == "/api/tasks":
            data = self._body()
            prompt = str(data.get("prompt", "")).strip()
            if not prompt:
                return self._error(400, "Le champ « prompt » est requis.")
            if len(prompt) > MAX_PROMPT_CHARS:
                return self._error(400, f"Demande trop longue (max {MAX_PROMPT_CHARS} caractères).")
            record = self.service.start(prompt)
            return self._json(record.summary(), 201)

        if path == "/api/routines":
            return self._create_routine(self._body())

        parts = [p for p in path.split("/") if p]
        # /api/routines/<id>/<action>
        if len(parts) == 4 and parts[0] == "api" and parts[1] == "routines":
            return self._routine_action(parts[2], parts[3])

        # /api/approvals/<request_id> — confirmation humaine (spec §15)
        if len(parts) == 3 and parts[0] == "api" and parts[1] == "approvals":
            data = self._body()
            granted = bool(data.get("granted"))
            try:
                request = self.service.permissions.resolve(parts[2], granted)
            except AraError as exc:
                return self._error(404, str(exc))
            return self._json({"request_id": request.request_id, "granted": request.granted})

        return self._error(404, "Route inconnue.")

    # -- routines (Phase 5) ------------------------------------------------

    def _create_routine(self, data: dict) -> None:
        prompt = str(data.get("prompt", "")).strip()
        when = str(data.get("when", "")).strip()
        if not prompt:
            return self._error(400, "Le champ « prompt » est requis.")
        if len(prompt) > MAX_PROMPT_CHARS:
            return self._error(400, f"Demande trop longue (max {MAX_PROMPT_CHARS} caractères).")
        try:
            routine = build_routine(
                prompt,
                when,
                label=str(data.get("label", "")).strip(),
                min_battery=int(data.get("min_battery", DEFAULT_MIN_BATTERY)),
                notify=bool(data.get("notify", True)),
            )
            self.service.routines.add(routine)
        except (AraError, TypeError, ValueError) as exc:
            return self._error(400, str(exc))

        if self.settings.automation_enabled:
            self.service.scheduler.start()
        return self._json(routine.to_dict(), 201)

    def _routine_action(self, routine_id: str, action: str) -> None:
        routines = self.service.routines
        if action == "delete":
            if not routines.delete(routine_id):
                return self._error(404, "Routine inconnue.")
            return self._json({"deleted": routine_id})

        routine = routines.get(routine_id)
        if routine is None:
            return self._error(404, "Routine inconnue.")

        if action in {"enable", "disable"}:
            if action == "enable":
                routine.enabled = True
                routine.disabled_reason = ""
                routine.failures = 0
                routine.reschedule(time.time())
            else:
                routine.disable("désactivée à la main")
            routines.save(routine)
            return self._json(routine.to_dict())

        if action == "run":
            # Exécution immédiate, à la demande — elle ne décale pas l'horaire.
            record = self.service.start(routine.prompt)
            routine.last_task_id = record.task_id
            routine.last_status = "lancée à la main"
            routines.save(routine)
            return self._json({"task": record.summary(), "routine": routine.to_dict()})

        return self._error(400, f"Action inconnue : {action}")

    # -- flux d'événements (SSE) -------------------------------------------

    def _events(self, task_id: str) -> None:
        bus = self.service.bus(task_id)
        record = self.service.get(task_id)

        if bus is None:
            # Tâche déjà terminée (ou serveur redémarré) : on renvoie l'état final.
            if record is None:
                return self._error(404, "Tâche inconnue.")
            payload = f"data: {json.dumps({'type': 'final', 'task': record.to_dict()}, ensure_ascii=False)}\n\n"
            return self._send(200, payload.encode("utf-8"), "text/event-stream; charset=utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True

        try:
            for event in bus.subscribe():
                chunk = f"data: {json.dumps(event.to_dict(), ensure_ascii=False)}\n\n"
                self.wfile.write(chunk.encode("utf-8"))
                self.wfile.flush()
            final = self.service.get(task_id)
            if final:
                chunk = f"data: {json.dumps({'type': 'final', 'task': final.to_dict()}, ensure_ascii=False)}\n\n"
                self.wfile.write(chunk.encode("utf-8"))
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass  # le téléphone a fermé l'écran : normal

    # -- fichiers ----------------------------------------------------------

    def _file(self, task_id: str, filename: str) -> None:
        try:
            path = self.service.store.root / task_id / "files"
            target = (path / filename).resolve()
            if not str(target).startswith(str(path.resolve())) or not target.is_file():
                return self._error(404, "Fichier introuvable.")
            data = target.read_bytes()
        except (OSError, ValueError):
            return self._error(404, "Fichier introuvable.")

        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self._send(
            200,
            data,
            mime,
            {"Content-Disposition": f'inline; filename="{target.name}"'},
        )

    def _static(self, path: str) -> None:
        name = "index.html" if path in {"", "/"} else path.lstrip("/")
        target = (STATIC_DIR / name).resolve()
        if not str(target).startswith(str(STATIC_DIR.resolve())) or not target.is_file():
            return self._error(404, "Page inconnue.")
        mime = mimetypes.guess_type(target.name)[0] or "text/plain"
        charset = "; charset=utf-8" if mime.startswith("text/") or "json" in mime else ""
        self._send(200, target.read_bytes(), mime + charset, {"Cache-Control": "no-cache"})


def build_server(settings: Settings | None = None) -> ThreadingHTTPServer:
    settings = settings or get_settings()
    httpd = ThreadingHTTPServer((settings.host, settings.port), AraHandler)
    httpd.daemon_threads = True
    httpd.service = TaskService(settings)  # type: ignore[attr-defined]
    httpd.settings = settings  # type: ignore[attr-defined]
    return httpd


def main() -> None:
    settings = get_settings()
    settings.workspace.mkdir(parents=True, exist_ok=True)
    httpd = build_server(settings)

    token = Settings.secret("ARA_TOKEN")
    from .. import __phase__, __version__
    from ..android.bridge import detect

    device = detect()
    service: TaskService = httpd.service  # type: ignore[attr-defined]
    automation = service.start_scheduler()

    print(f"ARA v{__version__} (phase {__phase__}) — http://{settings.host}:{settings.port}")
    print(f"  LLM       : {settings.llm_provider}")
    print(f"  Recherche : {settings.search_provider}")
    print(f"  Espace    : {settings.workspace}")
    print(f"  Jeton     : {'activé' if token else 'désactivé (réseau local uniquement)'}")
    print(f"  Téléphone : {'Termux, ' + str(len(device.available)) + ' commandes' if device.usable else 'non (' + device.reason + ')'}")
    print(
        "  Routines  : "
        + (
            f"actives, {len(service.routines.list())} enregistrée(s)"
            if automation
            else "arrêtées (ARA_AUTOMATION=1 pour les activer)"
        )
    )
    print("Ctrl+C pour arrêter.")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt.")
    finally:
        service.stop_scheduler()
        httpd.server_close()


if __name__ == "__main__":
    main()
