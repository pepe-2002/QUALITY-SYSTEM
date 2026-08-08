"""Les quatre stratégies comparées (spec §18).

    MODEL ONLY          — répondre sans rien chercher
    FIXED REASONING     — un nombre de recherches fixe, une seule passe
    ADAPTIVE REASONING  — budget alloué selon la complexité estimée, une passe
    ADAPTIVE RESEARCH   — la boucle complète : analyser, puis relancer si besoin

Elles ne diffèrent que par **la décision de chercher**, jamais par le moteur de
synthèse ni par le corpus. C'est la seule façon d'attribuer un écart de
résultat à la stratégie elle-même.
"""

from __future__ import annotations

from ..agents.gather import collect
from ..agents.planner import plan as build_plan
from ..agents.research import ResearchAgent
from ..core.complexity import Complexity
from ..core.config import Settings
from ..core.errors import AraError
from ..providers.llm.base import LLMRequest
from ..tools.registry import ToolBox
from .corpus import Corpus
from .dataset import Task
from .harness import LabSearch, Outcome, Timer, build_context, estimate_tokens, frozen_network

#: Nombre de recherches de la stratégie « fixe ». Choisi comme la moyenne des
#: budgets adaptatifs, pour que la comparaison ne soit pas truquée d'avance.
FIXED_STEPS = 3

STRATEGIES = ("model_only", "fixed", "adaptive_reasoning", "adaptive_research")

#: Bras de l'expérience V2 — trois stratégies, comme demandé.
V2_STRATEGIES = ("fixed", "adaptive_reasoning", "adaptive_v2")

LABELS = {
    "model_only": "MODEL ONLY",
    "fixed": "FIXED REASONING",
    "adaptive_reasoning": "ADAPTIVE-V1",
    "adaptive_research": "ADAPTIVE RESEARCH",
    "adaptive_v2": "ADAPTIVE-V2",
}

#: Version du contrôleur **épinglée** pour chaque bras.
#:
#: C'est ce qui permet de faire avancer le système sans rendre irreproductibles
#: les expériences déjà publiées : H1 et H2 continuent de jouer V1, quoi qu'il
#: arrive ensuite au contrôleur par défaut de l'application.
CONTROLLER_BY_STRATEGY = {
    "model_only": "v1",
    "fixed": "v1",
    "adaptive_reasoning": "v1",
    "adaptive_research": "v1",
    "adaptive_v2": "v2",
}


def _synthesize(ctx, docs) -> str:
    """Même synthèse pour toutes les stratégies : on ne compare qu'un choix."""
    try:
        return ctx.llm.complete(
            LLMRequest(
                task="synthesis" if docs else "answer",
                question=ctx.prompt,
                documents=docs,
                max_tokens=1200,
            )
        ).text
    except AraError as exc:
        return f"Synthèse impossible : {exc}"


def run(
    strategy: str, task: Task, settings: Settings, corpus: Corpus, *, seed: int = 0
) -> Outcome:
    """Exécute une stratégie sur une tâche, dans le corpus figé."""
    search = LabSearch(corpus)
    counters: dict[str, int] = {}
    outcome = Outcome(strategy=strategy, task_id=task.id, seed=seed)

    ctx = build_context(task.question, settings, search, f"lab-{strategy}-{task.id}")
    toolbox = ToolBox(ctx)
    plan = build_plan(
        task.question,
        max_search_steps=settings.max_research_steps,
        controller=CONTROLLER_BY_STRATEGY.get(strategy, "v1"),
    )
    plan.needs_research = strategy != "model_only"
    ctx.budget = plan.budget

    docs = []
    try:
        with frozen_network(corpus, counters), Timer() as timer:
            if strategy == "model_only":
                answer = _synthesize(ctx, [])

            elif strategy == "fixed":
                # Budget imposé, identique pour toutes les questions, et
                # jamais révisé : un témoin qui s'adapte ne mesure plus rien.
                plan.budget.complexity = Complexity.MEDIUM
                plan.budget.search_steps = min(FIXED_STEPS, settings.max_research_steps)
                plan.adaptive_budget = False
                docs = collect(ctx, plan, toolbox)
                answer = _synthesize(ctx, docs)

            elif strategy in {"adaptive_reasoning", "adaptive_v2"}:
                # Même code, deux contrôleurs. V1 décide une fois avant de
                # chercher et n'y revient pas ; V2 estime la difficulté puis
                # révise son budget sur preuve. C'est la seule différence entre
                # ces deux bras, et c'est exactement ce que l'expérience mesure.
                docs = collect(ctx, plan, toolbox)
                answer = _synthesize(ctx, docs)

            else:  # adaptive_research
                agent = ResearchAgent(ctx, toolbox, plan)
                docs, report = agent.run()
                answer = _synthesize(ctx, docs)
                answer = f"{answer}\n\n{report.sections()}"
                outcome.cycles = report.iterations
                outcome.gaps = [gap.label for gap in report.gaps]
                outcome.contradictions = [a.describe() for a in report.anomalies]
                outcome.stopped_because = report.stopped_because
                outcome.stop_code = report.stop_code

    except AraError as exc:
        outcome.error = str(exc)
        answer = ""

    outcome.answer = answer
    outcome.sources = docs
    outcome.searches = len(search.queries)
    outcome.fetches = counters.get("fetches", 0)
    outcome.tool_calls = len(toolbox.calls)
    outcome.llm_calls = getattr(ctx.llm, "calls", 0)
    outcome.latency_ms = timer.ms
    outcome.tokens = estimate_tokens(ctx, docs, answer)
    outcome.domains = len({doc.domain for doc in docs})
    if not outcome.cycles:
        outcome.cycles = 1 if strategy != "model_only" else 0
    outcome.controller = plan.budget.controller
    if not outcome.stop_code:
        outcome.stop_code = plan.budget.stop_code
    outcome.difficulty = plan.budget.difficulty
    outcome.revisions = [action for action, _motif in plan.budget.revisions]
    return outcome
