"""Rapport de recherche : ce que l'agent a établi, ce qui cloche, ce qui manque.

Ces sections sont produites **de façon déterministe**, indépendamment du LLM
configuré. Un modèle peut rédiger une belle synthèse ; il ne doit pas être le
seul garant du constat « ces deux sources se contredisent ».
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..core.models import SourceDoc
from .compare import Contradiction, agreements
from .coverage import Gap
from .facts import Fact


@dataclass
class ResearchReport:
    """Bilan d'une boucle de recherche."""

    question: str
    docs: list[SourceDoc] = field(default_factory=list)
    facts: list[Fact] = field(default_factory=list)
    contradictions: list[Contradiction] = field(default_factory=list)
    gaps: list[Gap] = field(default_factory=list)
    iterations: int = 0
    queries: list[str] = field(default_factory=list)
    stopped_because: str = ""
    #: source → domaine, pour ne recouper que des sites distincts
    domains_by_source: dict[int, str] = field(default_factory=dict)

    @property
    def domains(self) -> set[str]:
        return {doc.domain for doc in self.docs}

    @property
    def confirmed(self) -> list[list[Fact]]:
        return agreements(self.facts, domains=self.domains_by_source)

    # -- rendu ------------------------------------------------------------

    def sections(self) -> str:
        """Sections Markdown à ajouter sous la synthèse."""
        blocks: list[str] = []

        confirmed = self.confirmed
        if confirmed:
            lines = ["## Recoupements", ""]
            for cluster in confirmed[:6]:
                sources = ", ".join(f"[S{s}]" for s in sorted({f.source for f in cluster}))
                lines.append(f"- **{cluster[0].describe()}** — confirmé par {sources}")
            blocks.append("\n".join(lines))

        if self.contradictions:
            lines = ["## CONTRADICTION DÉTECTÉE", ""]
            for contradiction in self.contradictions[:6]:
                lines.append(f"- {contradiction.describe()}")
                for fact in contradiction.facts[:3]:
                    extrait = fact.sentence
                    if len(extrait) > 180:
                        extrait = extrait[:180].rsplit(" ", 1)[0] + "…"
                    lines.append(f"  - [S{fact.source}] « {extrait} »")
            lines += [
                "",
                "> Ces valeurs ne peuvent pas être vraies ensemble. "
                "À trancher sur une source officielle avant toute décision.",
            ]
            blocks.append("\n".join(lines))

        if self.gaps:
            lines = ["## Informations manquantes", ""]
            for gap in self.gaps[:6]:
                lines.append(f"- {gap.label}")
            blocks.append("\n".join(lines))

        lines = ["## Déroulé de la recherche", ""]
        lines.append(
            f"- {self.iterations} cycle(s) · {len(self.queries)} requête(s) · "
            f"{len(self.docs)} source(s) sur {len(self.domains)} domaine(s)"
        )
        if self.stopped_because:
            lines.append(f"- Arrêt : {self.stopped_because}")
        blocks.append("\n".join(lines))

        return "\n\n".join(blocks)

    def to_dict(self) -> dict:
        return {
            "iterations": self.iterations,
            "queries": self.queries,
            "sources": len(self.docs),
            "domains": sorted(self.domains),
            "facts": len(self.facts),
            "contradictions": [c.to_dict() for c in self.contradictions],
            "gaps": [g.to_dict() for g in self.gaps],
            "stopped_because": self.stopped_because,
        }
