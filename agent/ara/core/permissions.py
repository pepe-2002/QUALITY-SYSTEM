"""Système de permissions des outils (spec §16) et validation humaine (spec §15).

Deux verrous distincts :

1. **Autorisation** — un outil doit figurer dans la liste blanche, sinon il est
   refusé. Le fait qu'une fonction existe dans le code ne donne aucun droit.
2. **Confirmation** — un outil marqué sensible exige un accord humain explicite
   avant chaque exécution (publication, suppression, envoi, achat…).
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any

from .config import Settings, get_settings
from .errors import ApprovalRequired, PermissionDenied


@dataclass
class ApprovalRequest:
    """Demande de confirmation en attente d'une réponse humaine."""

    request_id: str
    tool: str
    reason: str
    params: dict[str, Any] = field(default_factory=dict)
    decided: bool = False
    granted: bool = False


class PermissionManager:
    """Gardien des outils : autorise, refuse, demande confirmation.

    Thread-safe : le serveur exécute les tâches dans des threads séparés.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._allowed = set(self.settings.allowed_tools)
        self._sensitive = set(self.settings.sensitive_tools)
        self._pending: dict[str, ApprovalRequest] = {}
        self._lock = threading.Lock()

    # -- autorisation ------------------------------------------------------

    def is_allowed(self, tool: str) -> bool:
        return tool in self._allowed

    def is_sensitive(self, tool: str) -> bool:
        return tool in self._sensitive

    def allow(self, tool: str) -> None:
        """Autorise explicitement un outil (usage : tests, session avancée)."""
        self._allowed.add(tool)

    def revoke(self, tool: str) -> None:
        self._allowed.discard(tool)

    def check(self, tool: str) -> None:
        """Lève :class:`PermissionDenied` si l'outil n'est pas autorisé."""
        if not self.is_allowed(tool):
            raise PermissionDenied(
                f"Outil « {tool} » non autorisé. "
                "Ajoutez-le à ARA_ALLOWED_TOOLS pour l'activer."
            )

    # -- confirmation humaine ---------------------------------------------

    def request_approval(
        self, tool: str, reason: str, params: dict[str, Any] | None = None
    ) -> ApprovalRequest:
        request = ApprovalRequest(
            request_id=uuid.uuid4().hex[:12],
            tool=tool,
            reason=reason,
            params=dict(params or {}),
        )
        with self._lock:
            self._pending[request.request_id] = request
        return request

    def resolve(self, request_id: str, granted: bool) -> ApprovalRequest:
        with self._lock:
            request = self._pending.get(request_id)
            if request is None:
                raise PermissionDenied(f"Demande de confirmation inconnue : {request_id}")
            request.decided = True
            request.granted = granted
        return request

    def pending(self) -> list[ApprovalRequest]:
        with self._lock:
            return [r for r in self._pending.values() if not r.decided]

    def guard(self, tool: str, params: dict[str, Any] | None = None) -> None:
        """Vérifie autorisation + confirmation avant l'exécution d'un outil.

        Lève :class:`PermissionDenied` ou :class:`ApprovalRequired`.
        """
        self.check(tool)
        if not self.is_sensitive(tool) or not self.settings.require_approval:
            return
        request = self.request_approval(
            tool, reason=f"Action sensible : {tool}", params=params
        )
        raise ApprovalRequired(
            f"L'action « {tool} » nécessite votre confirmation.",
            tool=tool,
            request_id=request.request_id,
        )
