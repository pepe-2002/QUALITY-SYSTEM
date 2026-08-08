"""Diagnostic : où le système perd-il l'information, aujourd'hui ?

Passe la configuration **adoptée** (ADAPTIVE-V2 + RESEARCH-V2) sur les quatre
jeux, et range chaque échec à l'étape où l'information a été perdue. Ce n'est
pas une expérience comparative — aucune hypothèse, aucun verdict : c'est un
état des lieux, destiné à dire où porter l'effort suivant.

Il répond en particulier à la question laissée ouverte par le jeu 4 : de
meilleures sources n'avaient pas donné de meilleures réponses, et on ne savait
pas où l'information se perdait.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from ..agents.engines import engine_name
from ..agents.planner import plan as build_plan
from ..agents.research_v2 import ResearchAgentV2
from ..core.complexity import DEFAULT_CONTROLLER
from ..core.config import Settings, get_settings
from ..core.errors import AraError
from ..providers.llm.base import LLMRequest
from ..tools.registry import ToolBox
from .adversarial import TASKS as JEU4
from .adversarial import adversarial_corpus
from .corpus import Corpus
from .dataset import TASKS as JEU1
from .failures import Diagnosis, diagnose
from .harness import LabSearch, Outcome, Timer, build_context, estimate_tokens, frozen_network
from .heldout import TASKS as JEU2
from .heldout import held_out_corpus as corpus_jeu2
from .heldout2 import TASKS as JEU3
from .heldout2 import held_out_corpus as corpus_jeu3
from .metrics import score
from .seeds import SEEDS, corpus_for, task_for

JEUX = (
    ("jeu 1 — calibration", JEU1, Corpus),
    ("jeu 2 — validation", JEU2, corpus_jeu2),
    ("jeu 3 — contrôleur", JEU3, corpus_jeu3),
    ("jeu 4 — adversarial", JEU4, adversarial_corpus),
)


@dataclass
class DatasetDiagnosis:
    name: str
    stages: dict[str, int] = field(default_factory=dict)
    examples: dict[str, str] = field(default_factory=dict)
    runs: int = 0
    correct: int = 0

    def to_dict(self) -> dict:
        return {
            "name": self.name, "stages": self.stages, "runs": self.runs,
            "correct": self.correct, "examples": self.examples,
        }


@dataclass
class DiagnosticResult:
    controller: str = DEFAULT_CONTROLLER
    engine: str = ""
    seeds: tuple[int, ...] = SEEDS
    datasets: list[DatasetDiagnosis] = field(default_factory=list)

    @property
    def total(self) -> dict[str, int]:
        cumul: dict[str, int] = {}
        for jeu in self.datasets:
            for stage, compte in jeu.stages.items():
                cumul[stage] = cumul.get(stage, 0) + compte
        return cumul

    def to_dict(self) -> dict:
        return {
            "controller": self.controller, "engine": self.engine,
            "seeds": list(self.seeds), "total": self.total,
            "datasets": [d.to_dict() for d in self.datasets],
        }


def _run_once(task, settings: Settings, corpus, seed: int) -> Outcome:
    search = LabSearch(corpus)
    counters: dict[str, int] = {}
    outcome = Outcome(strategy="adopte", task_id=task.id, seed=seed)

    ctx = build_context(task.question, settings, search, f"diag-{task.id}-{seed}")
    toolbox = ToolBox(ctx)
    plan = build_plan(task.question, max_search_steps=settings.max_research_steps)
    plan.needs_research = True
    ctx.budget = plan.budget

    docs = []
    try:
        with frozen_network(corpus, counters), Timer() as timer:
            docs, report = ResearchAgentV2(ctx, toolbox, plan).run()
            try:
                answer = ctx.llm.complete(
                    LLMRequest(task="synthesis", question=ctx.prompt,
                               documents=docs, max_tokens=1200)
                ).text
            except AraError as exc:
                answer = f"Synthèse impossible : {exc}"
            answer = f"{answer}\n\n## Déroulé de la recherche\n\n{report.sections()}"
            outcome.contradictions = [a.describe() for a in report.anomalies]
            outcome.gaps = [gap.label for gap in report.gaps]
            outcome.stop_code = report.stop_code
    except AraError as exc:
        outcome.error = str(exc)
        answer = ""

    outcome.answer = answer
    outcome.sources = docs
    outcome.searches = len(search.queries)
    outcome.latency_ms = timer.ms
    outcome.tokens = estimate_tokens(ctx, docs, answer)
    return outcome


def run_diagnostic(
    *, settings: Settings | None = None, seeds: tuple[int, ...] = SEEDS
) -> DiagnosticResult:
    settings = replace(settings or get_settings(), search_delay=0.0)
    result = DiagnosticResult(engine=engine_name(), seeds=seeds)

    for nom, taches, fabrique in JEUX:
        jeu = DatasetDiagnosis(name=nom)
        base = fabrique()
        for seed in seeds:
            web = corpus_for(base, seed)
            for task in taches:
                pose = task_for(task, seed)
                outcome = _run_once(pose, settings, web, seed)
                note = score(task, outcome)
                verdict: Diagnosis = diagnose(task, outcome, note)
                jeu.runs += 1
                jeu.stages[verdict.stage] = jeu.stages.get(verdict.stage, 0) + 1
                if not verdict.failed:
                    jeu.correct += 1
                elif verdict.stage not in jeu.examples:
                    jeu.examples[verdict.stage] = f"{task.id} — {verdict.reason}"
        result.datasets.append(jeu)

    return result


__all__ = ["DatasetDiagnosis", "DiagnosticResult", "run_diagnostic"]
