"""Erreurs du système.

Toutes les erreurs de l'agent héritent de :class:`AraError` afin que
l'orchestrateur puisse les distinguer d'un bug Python réel.
"""

from __future__ import annotations


class AraError(Exception):
    """Erreur maîtrisée de l'agent (affichable à l'utilisateur)."""

    #: code court, stable, utilisable par l'interface
    code = "ara_error"


class ConfigError(AraError):
    """Configuration invalide ou incomplète."""

    code = "config_error"


class ToolError(AraError):
    """Un outil a échoué de façon récupérable."""

    code = "tool_error"


class ToolNotFound(ToolError):
    """L'outil demandé n'existe pas dans le registre."""

    code = "tool_not_found"


class PermissionDenied(AraError):
    """L'outil existe mais n'est pas explicitement autorisé.

    Règle de la spec §16 : « L'agent ne doit jamais avoir accès à une fonction
    uniquement parce qu'elle existe. »
    """

    code = "permission_denied"


class ApprovalRequired(AraError):
    """Action sensible : l'humain doit confirmer avant exécution (spec §15)."""

    code = "approval_required"

    def __init__(self, message: str, *, tool: str, request_id: str) -> None:
        super().__init__(message)
        self.tool = tool
        self.request_id = request_id


class ExternalResourceRequired(AraError):
    """La fonction demandée exige une ressource externe (souvent payante).

    Spec §19 : ne jamais activer automatiquement, afficher un message clair.
    """

    code = "external_resource_required"

    def __init__(self, feature: str, hint: str = "") -> None:
        message = "Cette fonction nécessite une ressource externe."
        if hint:
            message = f"{message} ({feature} : {hint})"
        else:
            message = f"{message} ({feature})"
        super().__init__(message)
        self.feature = feature
        self.hint = hint


class ProviderError(AraError):
    """Un fournisseur (LLM, recherche, stockage) a échoué."""

    code = "provider_error"


class BudgetExceeded(AraError):
    """Une limite d'arrêt a été atteinte (étapes, itérations, temps).

    Le système DOIT savoir s'arrêter (règle finale de la spec).
    """

    code = "budget_exceeded"
