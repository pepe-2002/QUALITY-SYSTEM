"""Fournisseurs LLM par réseau : Ollama (local, gratuit), OpenAI-compatible, Anthropic.

Aucun n'est activé par défaut. Chacun déclare ce qu'il exige (`available()`), et
l'orchestrateur refuse de l'activer tout seul si la ressource manque (spec §19).
Les clés sont lues à l'exécution depuis l'environnement et ne sont jamais
stockées en attribut, ni journalisées.
"""

from __future__ import annotations

import os

from ...core import http
from ...core.config import Settings
from ...core.errors import AraError, ProviderError
from .base import LLMProvider, LLMRequest, LLMResult

_SYSTEM = (
    "Tu es un agent de recherche rigoureux. Tu réponds en français, de façon "
    "structurée et concise. Tu ne présentes jamais une information comme certaine "
    "si les sources ne l'établissent pas, et tu signales explicitement les "
    "informations manquantes ainsi que les contradictions entre sources."
)


class OllamaLLM(LLMProvider):
    """Modèle local via Ollama — gratuit, aucune donnée ne sort de la machine."""

    name = "ollama"
    requires_external = False

    def __init__(self) -> None:
        self.base_url = os.environ.get("ARA_OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/")
        self.model = os.environ.get("ARA_OLLAMA_MODEL", "llama3.2")

    def available(self) -> tuple[bool, str]:
        try:
            http.get(f"{self.base_url}/api/tags", timeout=3, allow_private=True)
        except AraError as exc:
            return False, f"Ollama injoignable sur {self.base_url} ({exc})"
        return True, ""

    def complete(self, request: LLMRequest) -> LLMResult:
        payload = {
            "model": self.model,
            "prompt": request.render_prompt(),
            "system": _SYSTEM,
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        }
        try:
            data = http.post_json(
                f"{self.base_url}/api/generate",
                payload,
                timeout=120,
                allow_private=True,
            )
        except AraError as exc:
            raise ProviderError(f"Ollama : {exc}") from exc

        text = (data.get("response") or "").strip()
        if not text:
            raise ProviderError("Ollama a renvoyé une réponse vide.")
        return LLMResult(
            text=text,
            provider=self.name,
            model=self.model,
            usage={
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
            },
        )


class OpenAICompatLLM(LLMProvider):
    """Tout service exposant l'API `/chat/completions` (local ou hébergé).

    Couvre llama.cpp, vLLM, LM Studio, et les offres gratuites compatibles.
    """

    name = "openai_compat"
    requires_external = True

    def __init__(self) -> None:
        self.base_url = os.environ.get(
            "ARA_OPENAI_BASE_URL", "https://api.openai.com/v1"
        ).rstrip("/")
        self.model = os.environ.get("ARA_OPENAI_MODEL", "gpt-4o-mini")

    @property
    def _key(self) -> str | None:
        return Settings.secret("ARA_OPENAI_API_KEY")

    def available(self) -> tuple[bool, str]:
        if not self._key:
            return False, "ARA_OPENAI_API_KEY absent de l'environnement."
        return True, ""

    def complete(self, request: LLMRequest) -> LLMResult:
        key = self._key
        if not key:
            raise ProviderError("ARA_OPENAI_API_KEY absent de l'environnement.")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": request.render_prompt()},
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }
        try:
            data = http.post_json(
                f"{self.base_url}/chat/completions",
                payload,
                headers={"Authorization": f"Bearer {key}"},
                timeout=120,
            )
        except AraError as exc:
            raise ProviderError(f"{self.name} : {exc}") from exc

        try:
            text = data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, AttributeError) as exc:
            raise ProviderError(f"{self.name} : réponse inattendue.") from exc
        return LLMResult(
            text=text, provider=self.name, model=self.model, usage=data.get("usage", {})
        )


class AnthropicLLM(LLMProvider):
    """API Claude — activée uniquement si `ARA_ANTHROPIC_API_KEY` est présente."""

    name = "anthropic"
    requires_external = True

    API_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def __init__(self) -> None:
        self.model = os.environ.get("ARA_ANTHROPIC_MODEL", "claude-sonnet-4-5")

    @property
    def _key(self) -> str | None:
        return Settings.secret("ARA_ANTHROPIC_API_KEY")

    def available(self) -> tuple[bool, str]:
        if not self._key:
            return False, "ARA_ANTHROPIC_API_KEY absent de l'environnement."
        return True, ""

    def complete(self, request: LLMRequest) -> LLMResult:
        key = self._key
        if not key:
            raise ProviderError("ARA_ANTHROPIC_API_KEY absent de l'environnement.")
        payload = {
            "model": self.model,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "system": _SYSTEM,
            "messages": [{"role": "user", "content": request.render_prompt()}],
        }
        try:
            data = http.post_json(
                self.API_URL,
                payload,
                headers={
                    "x-api-key": key,
                    "anthropic-version": self.API_VERSION,
                },
                timeout=120,
            )
        except AraError as exc:
            raise ProviderError(f"Anthropic : {exc}") from exc

        blocks = data.get("content") or []
        text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text").strip()
        if not text:
            raise ProviderError("Anthropic : réponse vide.")
        return LLMResult(
            text=text, provider=self.name, model=self.model, usage=data.get("usage", {})
        )
