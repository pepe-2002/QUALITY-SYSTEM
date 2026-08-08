"""Choix du moteur de recherche : baseline gelée ou RESEARCH-V2.

Un seul endroit décide quelle version tourne. L'application prend la valeur
par défaut ; le laboratoire, lui, nomme explicitement le moteur de chaque bras
— c'est ce qui permet à H1 et H2 de rester reproductibles pendant que le
système avance.
"""

from __future__ import annotations

import os

from ..core.context import TaskContext
from ..tools.registry import ToolBox
from .planner import Plan
from .research import ResearchAgent
from .research_v2 import ResearchAgentV2

#: Moteurs disponibles. « baseline » est le moteur figé de H1 et H2 ; il n'est
#: pas retiré, il ne bouge plus.
ENGINES = {
    "baseline": ResearchAgent,
    "v2": ResearchAgentV2,
}

#: Moteur de l'application.
#:
#: Passé à « v2 » sur décision du propriétaire du projet, après l'expérience
#: du jeu 4 : V2 élimine deux formes de faux positifs sur trois mesurées, sans
#: perte d'exactitude ni surcoût. Deux limites subsistent et sont documentées
#: — noms de lieux voisins, sources hors période.
#:
#: `ARA_RESEARCH_ENGINE=baseline` permet de revenir au moteur gelé sans
#: modifier une ligne de code.
DEFAULT_ENGINE = "v2"


def engine_name() -> str:
    """Moteur effectif, éventuellement forcé par l'environnement."""
    choix = (os.environ.get("ARA_RESEARCH_ENGINE") or DEFAULT_ENGINE).strip().lower()
    return choix if choix in ENGINES else DEFAULT_ENGINE


def research_agent(ctx: TaskContext, plan: Plan, toolbox: ToolBox, *, engine: str | None = None):
    """Construit l'agent de recherche de la version demandée."""
    return ENGINES[engine or engine_name()](ctx, toolbox, plan)


def run_research(
    ctx: TaskContext, plan: Plan, toolbox: ToolBox, *, engine: str | None = None
):
    """Exécute la boucle de recherche avec le moteur choisi."""
    return research_agent(ctx, plan, toolbox, engine=engine).run()


__all__ = ["DEFAULT_ENGINE", "ENGINES", "engine_name", "research_agent", "run_research"]
