"""Expérience RESEARCH-BASELINE contre RESEARCH-V2.

Ce qu'elle compare : deux moteurs de recherche, sur le **jeu 4**, adversarial
et jamais utilisé. Rien d'autre ne change — même contrôleur, même corpus,
mêmes graines, même moteur de synthèse.

Ce qu'elle ne fait pas : elle ne touche ni à H1, ni à H2, ni à l'expérience
V2 du contrôleur. La baseline reste gelée et continue de produire exactement
les mêmes chiffres qu'avant.

Mesures demandées, toutes relevées ici : exactitude, pertinence des sources,
faux positifs, mauvaises géolocalisations, nombre de recherches, temps, jetons.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field, replace

from ..agents.planner import plan as build_plan
from ..agents.research import ResearchAgent
from ..agents.research_v2 import BASELINE_VERSION, RESEARCH_VERSION, ResearchAgentV2
from ..analysis.facts import extractor
from ..core.config import Settings, get_settings
from ..core.errors import AraError
from ..providers.llm.base import LLMRequest
from ..tools.registry import ToolBox
from .adversarial import TASKS as JEU4_TASKS
from .adversarial import adversarial_corpus, label_of
from .harness import LabSearch, Outcome, Timer, build_context, estimate_tokens, frozen_network
from .metrics import Row, score
from .seeds import SEEDS, corpus_for, task_for

ENGINES = ("baseline", "v2")
ENGINE_LABELS = {"baseline": "RESEARCH-BASELINE", "v2": "RESEARCH-V2"}

#: Catégories de pages du jeu 4 qui constituent un faux positif si retenues.
FAUX_POSITIFS = ("autre_lieu", "nom_voisin", "generique", "perime", "autre_contexte")
#: Sous-ensemble qui relève d'une erreur **géographique**.
MAUVAIS_LIEUX = ("autre_lieu", "nom_voisin")


@dataclass
class EngineStats:
    engine: str
    accuracy: float = 0.0
    net: float = 0.0
    noise: float = 0.0
    precision: float = 0.0          # part des sources retenues qui sont du sujet
    false_positives: float = 0.0    # nombre moyen de sources hors sujet retenues
    wrong_place: float = 0.0        # dont erreurs géographiques
    by_trap: dict = field(default_factory=dict)
    searches: float = 0.0
    latency_ms: float = 0.0
    tokens: float = 0.0
    rejected: float = 0.0
    runs: int = 0

    @property
    def label(self) -> str:
        return ENGINE_LABELS.get(self.engine, self.engine)

    def to_dict(self) -> dict:
        return {
            "engine": self.engine, "label": self.label,
            "accuracy": round(self.accuracy, 3), "net": round(self.net, 3),
            "noise": round(self.noise, 3), "precision": round(self.precision, 3),
            "false_positives": round(self.false_positives, 2),
            "wrong_place": round(self.wrong_place, 2),
            "by_trap": self.by_trap,
            "searches": round(self.searches, 2),
            "latency_ms": round(self.latency_ms), "tokens": round(self.tokens),
            "rejected": round(self.rejected, 2), "runs": self.runs,
        }


@dataclass
class ResearchResult:
    baseline_version: str = BASELINE_VERSION
    v2_version: str = RESEARCH_VERSION
    seeds: tuple[int, ...] = SEEDS
    rows: list[Row] = field(default_factory=list)
    stats: dict[str, EngineStats] = field(default_factory=dict)
    queries: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "baseline_version": self.baseline_version,
            "v2_version": self.v2_version,
            "seeds": list(self.seeds),
            "stats": {k: v.to_dict() for k, v in self.stats.items()},
            "queries": self.queries,
            "rows": [r.to_dict() for r in self.rows],
        }


def _synthesize(ctx, docs) -> str:
    try:
        return ctx.llm.complete(
            LLMRequest(
                task="synthesis" if docs else "answer",
                question=ctx.prompt, documents=docs, max_tokens=1200,
            )
        ).text
    except AraError as exc:
        return f"Synthèse impossible : {exc}"


def run_engine(engine: str, task, settings: Settings, corpus, *, seed: int = 0) -> Outcome:
    """Joue un moteur de recherche sur une tâche du jeu adversarial."""
    search = LabSearch(corpus)
    counters: dict[str, int] = {}
    outcome = Outcome(strategy=engine, task_id=task.id, seed=seed)

    ctx = build_context(task.question, settings, search, f"rech-{engine}-{task.id}")
    toolbox = ToolBox(ctx)
    # Contrôleur identique pour les deux moteurs : on ne compare qu'une chose.
    plan = build_plan(task.question, max_search_steps=settings.max_research_steps,
                      controller="v2")
    plan.needs_research = True
    ctx.budget = plan.budget

    docs = []
    try:
        with frozen_network(corpus, counters), Timer() as timer:
            agent = (ResearchAgent if engine == "baseline" else ResearchAgentV2)(
                ctx, toolbox, plan
            )
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
    outcome.revisions = list(search.queries)   # requêtes réellement envoyées
    return outcome


def _source_quality(outcome: Outcome) -> tuple[float, int, int, dict]:
    """(précision, faux positifs, mauvais lieux, détail par piège)."""
    labels = [label_of(doc.url) for doc in outcome.sources]
    if not labels:
        return (0.0, 0, 0, {})
    sujets = sum(1 for label in labels if label == "sujet")
    faux = sum(1 for label in labels if label in FAUX_POSITIFS)
    lieux = sum(1 for label in labels if label in MAUVAIS_LIEUX)
    detail = {}
    for piege in FAUX_POSITIFS:
        compte = sum(1 for label in labels if label == piege)
        if compte:
            detail[piege] = compte
    return (sujets / len(labels), faux, lieux, detail)


def run_research_experiment(*args, **kwargs) -> ResearchResult:
    """Compare les deux moteurs avec l'extracteur qui a produit ces chiffres."""
    with extractor("baseline"):
        return _run_research_experiment(*args, **kwargs)


def _run_research_experiment(
    *, settings: Settings | None = None, seeds: tuple[int, ...] = SEEDS
) -> ResearchResult:
    settings = replace(settings or get_settings(), search_delay=0.0)
    result = ResearchResult(seeds=seeds)
    corpus = adversarial_corpus()

    for seed in seeds:
        web = corpus_for(corpus, seed)
        for task in JEU4_TASKS:
            pose = task_for(task, seed)
            for engine in ENGINES:
                outcome = run_engine(engine, pose, settings, web, seed=seed)
                outcome.task_id = task.id
                result.rows.append(
                    Row(task=task, outcome=outcome, score=score(task, outcome))
                )

    for engine in ENGINES:
        selection = [r for r in result.rows if r.outcome.strategy == engine]
        stats = EngineStats(engine=engine, runs=len(selection))
        if not selection:
            result.stats[engine] = stats
            continue

        qualites = [_source_quality(r.outcome) for r in selection]
        detail: dict[str, int] = {}
        for _p, _f, _l, par_piege in qualites:
            for piege, compte in par_piege.items():
                detail[piege] = detail.get(piege, 0) + compte

        stats.accuracy = statistics.fmean(r.score.accuracy for r in selection)
        stats.net = statistics.fmean(r.score.net for r in selection)
        stats.noise = statistics.fmean(r.score.noise for r in selection)
        stats.precision = statistics.fmean(q[0] for q in qualites)
        stats.false_positives = statistics.fmean(q[1] for q in qualites)
        stats.wrong_place = statistics.fmean(q[2] for q in qualites)
        stats.by_trap = detail
        stats.searches = statistics.fmean(r.outcome.searches for r in selection)
        stats.latency_ms = statistics.fmean(r.outcome.latency_ms for r in selection)
        stats.tokens = statistics.fmean(r.outcome.tokens for r in selection)
        result.stats[engine] = stats

        # Quelques requêtes réellement émises, pour montrer la différence de
        # forme — c'est le défaut le plus visible à l'œil nu.
        vues: list[str] = []
        for row in selection:
            for query in row.outcome.revisions:
                if query not in vues:
                    vues.append(query)
        result.queries[engine] = vues[:12]

    return result


__all__ = [
    "ENGINES", "ENGINE_LABELS", "EngineStats", "ResearchResult",
    "run_engine", "run_research_experiment",
]
