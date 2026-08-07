"""Sélection du fournisseur LLM.

Règle de repli (spec §19) : si le fournisseur demandé n'est pas disponible,
on **ne l'active pas de force** et on ne fait pas échouer la tâche — on bascule
sur le moteur hors-ligne en signalant clairement la dégradation.
"""

from __future__ import annotations

from typing import Callable

from ...core.config import get_settings
from .base import LLMProvider
from .network import AnthropicLLM, OllamaLLM, OpenAICompatLLM
from .offline import OfflineLLM

_FACTORIES: dict[str, Callable[[], LLMProvider]] = {
    "offline": OfflineLLM,
    "ollama": OllamaLLM,
    "openai_compat": OpenAICompatLLM,
    "anthropic": AnthropicLLM,
}


def get_llm(name: str | None = None) -> tuple[LLMProvider, str]:
    """Retourne `(fournisseur, avertissement)`.

    L'avertissement est vide si tout va bien ; sinon il explique pourquoi on
    est retombé sur le moteur hors-ligne.
    """
    name = (name or get_settings().llm_provider).strip().lower()
    factory = _FACTORIES.get(name)

    if factory is None:
        return OfflineLLM(), (
            f"Fournisseur LLM inconnu « {name} » — moteur hors-ligne utilisé. "
            f"Choix possibles : {', '.join(sorted(_FACTORIES))}."
        )

    provider = factory()
    ok, reason = provider.available()
    if ok:
        return provider, ""

    notice = f"Cette fonction nécessite une ressource externe. LLM « {name} » : {reason}"
    return OfflineLLM(), notice


def available_llms() -> list[dict]:
    """État de tous les fournisseurs, pour l'écran de réglages."""
    out = []
    for name, factory in _FACTORIES.items():
        try:
            out.append(factory().describe())
        except Exception as exc:  # un fournisseur cassé ne doit rien bloquer
            out.append({"name": name, "available": False, "reason": str(exc)})
    return out
