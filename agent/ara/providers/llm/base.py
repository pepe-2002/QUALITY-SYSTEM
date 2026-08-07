"""Interface commune des fournisseurs LLM.

La requête est **structurée** (`LLMRequest`) et non un simple texte : cela
permet au fournisseur hors-ligne d'exploiter directement la question et les
documents, tandis que les fournisseurs réseau utilisent `render_prompt()`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from ...core.models import SourceDoc

#: Tâches que l'orchestrateur sait demander à un LLM
TASKS = ("answer", "synthesis", "title", "queries")


@dataclass
class LLMRequest:
    task: str = "answer"
    question: str = ""
    instructions: str = ""
    documents: list[SourceDoc] = field(default_factory=list)
    max_tokens: int = 1200
    temperature: float = 0.2

    def render_prompt(self, *, max_doc_chars: int = 4000) -> str:
        """Construit le prompt texte pour un fournisseur réseau."""
        parts: list[str] = []
        if self.instructions:
            parts.append(self.instructions.strip())
        parts.append(f"DEMANDE DE L'UTILISATEUR :\n{self.question.strip()}")

        if self.documents:
            parts.append("SOURCES CONSULTÉES :")
            for index, doc in enumerate(self.documents, start=1):
                body = (doc.content or "").strip()
                if len(body) > max_doc_chars:
                    body = body[:max_doc_chars].rsplit(" ", 1)[0] + " […]"
                parts.append(
                    f"[S{index}] {doc.title or doc.domain}\nURL : {doc.url}\n{body}"
                )
            parts.append(
                "Appuie-toi uniquement sur ces sources. Cite-les sous la forme [S1], [S2]. "
                "Si une information manque ou si les sources se contredisent, dis-le "
                "explicitement au lieu d'inventer."
            )
        return "\n\n".join(parts)


@dataclass
class LLMResult:
    text: str
    provider: str
    model: str = ""
    usage: dict[str, Any] = field(default_factory=dict)
    #: True si la réponse vient d'un moteur dégradé (hors-ligne, extractif)
    degraded: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "usage": self.usage,
            "degraded": self.degraded,
        }


class LLMProvider(ABC):
    """Contrat minimal d'un fournisseur LLM."""

    #: identifiant utilisé dans ARA_LLM_PROVIDER
    name: str = "base"
    #: True si le fournisseur suppose une ressource externe (clé, service)
    requires_external: bool = False
    #: True si la qualité est structurellement inférieure à un vrai LLM
    degraded: bool = False

    @abstractmethod
    def complete(self, request: LLMRequest) -> LLMResult:
        """Produit une réponse. Doit lever `ProviderError` en cas d'échec."""

    def available(self) -> tuple[bool, str]:
        """Retourne `(disponible, raison)`.

        Un fournisseur indisponible n'est jamais activé automatiquement
        (spec §19) : l'orchestrateur bascule sur le moteur hors-ligne et
        prévient l'utilisateur.
        """
        return True, ""

    def describe(self) -> dict[str, Any]:
        ok, reason = self.available()
        return {
            "name": self.name,
            "available": ok,
            "reason": reason,
            "requires_external": self.requires_external,
            "degraded": self.degraded,
        }
