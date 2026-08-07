"""Système d'outils (spec §13).

Chaque outil est **indépendant** : une fonction, des paramètres explicites, un
résultat sérialisable. Aucun outil ne s'exécute sans être passé par le registre,
qui vérifie systématiquement les permissions.
"""

from . import (  # noqa: F401  (l'import enregistre les outils)
    android,
    design,
    documents,
    files,
    media,
    web,
)
from .registry import REGISTRY, Tool, ToolBox, tool

__all__ = ["REGISTRY", "Tool", "ToolBox", "tool"]
