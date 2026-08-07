"""Outils média — frontière explicite entre gratuit et payant (spec §19).

La génération d'images par IA n'a pas d'équivalent gratuit fiable et local en
Phase 1. Plutôt que d'appeler silencieusement un service payant, l'outil est
déclaré, refuse de s'exécuter, et explique ce qui manque. C'est le
comportement exigé : « ne pas l'activer automatiquement ».

Les vrais outils créatifs (QR code, composition de flyers) arrivent en Phase 3.
"""

from __future__ import annotations

from ..core.context import TaskContext
from ..core.errors import ExternalResourceRequired
from .registry import tool


@tool(
    "generate_image",
    "Génère une image par IA. Nécessite un service externe — désactivé par défaut.",
    params={"prompt": "description de l'image", "size": "dimensions, ex. 1024x1024"},
    requires_external=True,
)
def generate_image(ctx: TaskContext, prompt: str, size: str = "1024x1024") -> dict:
    raise ExternalResourceRequired(
        "generate_image",
        "aucun générateur d'images gratuit n'est configuré. "
        "Options : Stable Diffusion en local (ARA_IMAGE_PROVIDER=local), "
        "ou une API d'images (clé requise). Phase 3 du projet.",
    )
