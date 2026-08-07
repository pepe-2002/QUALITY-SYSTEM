"""Configuration du système — 100 % variables d'environnement (spec §16).

Aucun secret n'est écrit dans le code ni dans le dépôt. Le fichier `.env`
(non versionné) est lu au démarrage s'il existe ; `.env.example` documente
les clés sans jamais contenir de valeur réelle.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from .errors import ConfigError

#: Répertoire racine du projet (agent/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

#: Outils autorisés par défaut en Phase 1.
#: Un outil absent de cette liste est refusé même s'il existe (spec §16).
DEFAULT_ALLOWED_TOOLS = (
    "web_search",
    "fetch_page",
    "extract_text",
    "save_file",
    "list_files",
    "read_file",
    "create_pdf",
    "create_docx",
    "create_markdown",
    "create_txt",
    "create_flyer",
    "create_qr",
    "remember_brand",
    # Phase 5 — capacités du téléphone. `share_file` en est volontairement
    # absent : un fichier qui sort de l'appareil exige une autorisation
    # explicite en plus de la confirmation humaine (double verrou, comme
    # `delete_file`).
    "notify_phone",
    "phone_status",
    "copy_to_clipboard",
    "speak_text",
)

#: Outils considérés comme sensibles : confirmation humaine obligatoire (spec §15).
DEFAULT_SENSITIVE_TOOLS = (
    "delete_file",
    "publish",
    "send_message",
    "purchase",
    "share_file",
)

_TRUE = {"1", "true", "yes", "on", "oui"}


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in _TRUE


def _env_int(name: str, default: int, *, minimum: int = 0) -> int:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw.strip())
    except ValueError as exc:
        raise ConfigError(f"{name} doit être un entier (reçu : {raw!r})") from exc
    if value < minimum:
        raise ConfigError(f"{name} doit être >= {minimum} (reçu : {value})")
    return value


def _env_list(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw = os.environ.get(name)
    if raw is None or raw.strip() == "":
        return tuple(default)
    return tuple(item.strip() for item in raw.split(",") if item.strip())


def load_dotenv(path: Path | None = None, *, override: bool = False) -> dict[str, str]:
    """Charge un fichier `.env` minimal (KEY=VALUE) dans l'environnement.

    Volontairement sans dépendance externe : le prototype doit tourner sur un
    téléphone (Termux) sans chaîne de compilation.
    """
    path = path or (PROJECT_ROOT / ".env")
    loaded: dict[str, str] = {}
    if not path.is_file():
        return loaded
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            continue
        if override or key not in os.environ:
            os.environ[key] = value
        loaded[key] = value
    return loaded


@dataclass(frozen=True)
class Settings:
    """Réglages effectifs de la session."""

    # --- Fournisseurs (abstraction, spec §19) ---
    llm_provider: str = "offline"
    search_provider: str = "auto"
    storage_provider: str = "local"

    # --- Budgets d'arrêt (spec §3, §7) ---
    max_research_steps: int = 10
    max_design_iterations: int = 5
    design_target_score: int = 85
    max_task_seconds: int = 300

    # --- Réseau ---
    http_timeout: int = 20
    #: pause entre deux recherches, pour ne pas se faire limiter
    search_delay: float = 1.0
    http_max_bytes: int = 2_000_000
    user_agent: str = "ARA/0.1 (+agent de recherche personnel)"

    # --- Stockage ---
    workspace: Path = field(default_factory=lambda: PROJECT_ROOT / "workspace")

    # --- Sécurité (spec §16) ---
    allowed_tools: tuple[str, ...] = DEFAULT_ALLOWED_TOOLS
    sensitive_tools: tuple[str, ...] = DEFAULT_SENSITIVE_TOOLS
    require_approval: bool = True

    # --- Automatisation (Phase 5) ---
    #: l'ordonnanceur ne démarre que si on le demande : rien ne tourne tout
    #: seul sur la machine de quelqu'un sans qu'il l'ait décidé
    automation_enabled: bool = False

    # --- Serveur ---
    host: str = "0.0.0.0"
    port: int = 8800

    @classmethod
    def from_env(cls) -> "Settings":
        """Construit les réglages à partir de l'environnement."""
        workspace = Path(
            os.environ.get("ARA_WORKSPACE") or (PROJECT_ROOT / "workspace")
        ).expanduser()

        return cls(
            llm_provider=os.environ.get("ARA_LLM_PROVIDER", "offline").strip() or "offline",
            search_provider=os.environ.get("ARA_SEARCH_PROVIDER", "auto").strip() or "auto",
            storage_provider=os.environ.get("ARA_STORAGE_PROVIDER", "local").strip() or "local",
            max_research_steps=_env_int("ARA_MAX_RESEARCH_STEPS", 10, minimum=1),
            max_design_iterations=_env_int("ARA_MAX_DESIGN_ITERATIONS", 5, minimum=1),
            design_target_score=_env_int("ARA_DESIGN_TARGET_SCORE", 85, minimum=0),
            max_task_seconds=_env_int("ARA_MAX_TASK_SECONDS", 300, minimum=5),
            http_timeout=_env_int("ARA_HTTP_TIMEOUT", 20, minimum=1),
            search_delay=float(os.environ.get("ARA_SEARCH_DELAY") or 1.0),
            http_max_bytes=_env_int("ARA_HTTP_MAX_BYTES", 2_000_000, minimum=1024),
            user_agent=os.environ.get("ARA_USER_AGENT", cls.user_agent),
            workspace=workspace,
            allowed_tools=_env_list("ARA_ALLOWED_TOOLS", DEFAULT_ALLOWED_TOOLS),
            sensitive_tools=_env_list("ARA_SENSITIVE_TOOLS", DEFAULT_SENSITIVE_TOOLS),
            require_approval=_env_bool("ARA_REQUIRE_APPROVAL", True),
            automation_enabled=_env_bool("ARA_AUTOMATION", False),
            host=os.environ.get("ARA_HOST", "0.0.0.0"),
            port=_env_int("ARA_PORT", 8800, minimum=1),
        )

    # -- secrets : lus à la demande, jamais stockés dans l'objet ------------

    @staticmethod
    def secret(name: str) -> str | None:
        """Lit un secret depuis l'environnement.

        Les secrets ne sont jamais placés dans :class:`Settings` pour qu'ils
        n'apparaissent ni dans les logs, ni dans les réponses JSON, ni dans
        une trace d'exception.
        """
        value = os.environ.get(name)
        return value.strip() if value and value.strip() else None

    def tasks_dir(self) -> Path:
        return self.workspace / "tasks"

    def journal_path(self) -> Path:
        return self.workspace / "journal.jsonl"

    def brand_profile_path(self) -> Path:
        return self.workspace / "brand_profile.json"

    def routines_path(self) -> Path:
        return self.workspace / "routines.json"


_settings: Settings | None = None


def get_settings(*, reload: bool = False) -> Settings:
    """Retourne les réglages (singleton paresseux)."""
    global _settings
    if _settings is None or reload:
        load_dotenv()
        _settings = Settings.from_env()
    return _settings


def set_settings(settings: Settings) -> None:
    """Force des réglages (utilisé par les tests)."""
    global _settings
    _settings = settings
