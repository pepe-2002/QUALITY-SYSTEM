"""Stockage des fichiers produits — abstraction remplaçable (spec §19).

Une seule implémentation en Phase 1 : le disque local. L'interface reste
volontairement étroite (`write_bytes`, `read_bytes`, `list`, `path_for`) pour
qu'un stockage objet puisse la remplacer sans toucher aux agents.

Sécurité : tout est confiné dans `workspace/tasks/<task_id>/` et les noms de
fichiers sont assainis — aucune remontée de répertoire possible.
"""

from __future__ import annotations

import re
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..core.config import get_settings
from ..core.errors import ToolError

_SAFE_NAME = re.compile(r"[^A-Za-z0-9._-]+")


def safe_filename(name: str, *, default: str = "fichier", max_len: int = 80) -> str:
    """Assainit un nom de fichier (accents retirés, séparateurs supprimés).

    >>> safe_filename("Rapport été/2026.pdf")
    'Rapport_ete_2026.pdf'
    >>> safe_filename("../../etc/passwd")
    'etc_passwd'
    """
    name = unicodedata.normalize("NFKD", name)
    name = "".join(ch for ch in name if not unicodedata.combining(ch))
    name = name.replace("/", "_").replace("\\", "_")
    name = _SAFE_NAME.sub("_", name).strip("._-")
    name = re.sub(r"_+", "_", name)
    if not name:
        name = default
    if len(name) > max_len:
        stem, dot, suffix = name.rpartition(".")
        if dot and len(suffix) <= 5:
            name = stem[: max_len - len(suffix) - 1] + "." + suffix
        else:
            name = name[:max_len]
    return name


@dataclass
class StoredFile:
    name: str
    path: Path
    size: int
    kind: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "size": self.size,
            "kind": self.kind or self.path.suffix.lstrip("."),
        }


class Storage(ABC):
    name = "base"

    @abstractmethod
    def path_for(self, task_id: str, filename: str) -> Path: ...

    @abstractmethod
    def write_bytes(self, task_id: str, filename: str, data: bytes) -> StoredFile: ...

    @abstractmethod
    def read_bytes(self, task_id: str, filename: str) -> bytes: ...

    @abstractmethod
    def list(self, task_id: str) -> list[StoredFile]: ...

    def write_text(self, task_id: str, filename: str, text: str) -> StoredFile:
        return self.write_bytes(task_id, filename, text.encode("utf-8"))


class LocalStorage(Storage):
    """Fichiers sur disque, un dossier par tâche."""

    name = "local"

    def __init__(self, root: Path | None = None) -> None:
        self.root = Path(root or get_settings().tasks_dir())

    def task_dir(self, task_id: str) -> Path:
        directory = self.root / safe_filename(task_id, default="task") / "files"
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def path_for(self, task_id: str, filename: str) -> Path:
        directory = self.task_dir(task_id)
        target = (directory / safe_filename(filename)).resolve()
        # Ceinture et bretelles : le chemin final doit rester sous le dossier.
        if not str(target).startswith(str(directory.resolve())):
            raise ToolError(f"Chemin de fichier refusé : {filename}")
        return target

    def write_bytes(self, task_id: str, filename: str, data: bytes) -> StoredFile:
        target = self.path_for(task_id, filename)
        target.write_bytes(data)
        return StoredFile(name=target.name, path=target, size=len(data))

    def read_bytes(self, task_id: str, filename: str) -> bytes:
        target = self.path_for(task_id, filename)
        if not target.is_file():
            raise ToolError(f"Fichier introuvable : {filename}")
        return target.read_bytes()

    def list(self, task_id: str) -> list[StoredFile]:
        directory = self.task_dir(task_id)
        return [
            StoredFile(name=p.name, path=p, size=p.stat().st_size)
            for p in sorted(directory.iterdir())
            if p.is_file()
        ]


def get_storage(name: str | None = None) -> Storage:
    name = (name or get_settings().storage_provider).strip().lower()
    if name == "local":
        return LocalStorage()
    # Un stockage inconnu ne doit pas faire perdre le travail de l'utilisateur.
    return LocalStorage()
