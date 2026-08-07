"""H2 — le contrôleur adaptatif économise-t-il vraiment des recherches ?

H1 (Phase 4) reste ce qu'elle est : **non concluante**. Rien ici ne la
transforme en succès, et ses résultats bruts ne sont pas retouchés.

H2 porte sur une affirmation différente, plus modeste et plus mesurable : non
pas « l'adaptation répond mieux », mais « l'adaptation coûte moins, sans
répondre moins bien ». Elle a l'avantage d'être réfutable pour de bon : il
suffit que la réduction de recherches soit absente, ou qu'elle se paie en
exactitude.

Le protocole, écrit **avant** la première exécution sur le jeu de test :

1. deux jeux séparés — `dataset` (calibration, déjà brûlé par la Phase 4) et
   `heldout` (test, jamais vu) ;
2. cinq graines, qui font varier la formulation des questions et l'ordre des
   résultats de recherche — jamais les faits ;
3. l'unité statistique est la **tâche**, pas le couple (tâche, graine) : cinq
   graines d'une même tâche ne sont pas cinq observations indépendantes ;
4. le contrôleur est **gelé** avant la première exécution sur le jeu de test,
   et n'est pas retouché ensuite, quel que soit le résultat.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field, replace

from ..core.config import Settings, get_settings
from . import strategies as arms
from .corpus import Corpus
from .dataset import TASKS as CALIBRATION_TASKS
from .dataset import Task
from .experiment import bootstrap_ci, sign_test
from .heldout import TASKS as HELDOUT_TASKS
from .heldout import held_out_corpus
from .metrics import Row, score
from .seeds import SEEDS, corpus_for, task_for
from .stops import ERROR_ORDER, classify_errors, stop_reason

# --- Pré-enregistrement --------------------------------------------------------

#: Énoncé exact de H2, tel que fixé par le propriétaire du projet.
H2_STATEMENT = (
    "H2 — À exactitude comparable, ADAPTIVE REASONING réduit significativement "
    "le nombre de recherches nécessaires par rapport à FIXED."
)

#: Marge de non-infériorité : au-delà, l'exactitude n'est plus « comparable ».
#: 0,05 point d'exactitude nette, soit une demi-réponse sur dix tâches.
MARGE_EXACTITUDE = 0.05

#: Réduction minimale de recherches pour parler de « significativement moins ».
REDUCTION_MINIMALE = 0.20

#: Seuil de signification du test des signes.
ALPHA = 0.05

#: Prix de référence pour l'estimation de coût, en unités monétaires par
#: million de jetons. C'est un ordre de grandeur public de modèle courant, pas
#: une facture : le moteur hors-ligne ne coûte rien du tout.
PRIX_PAR_MILLION_JETONS = 3.0

CRITERES = {
    "A_exactitude_comparable": (
        f"borne basse de l'IC95 de l'écart d'exactitude nette ≥ −{MARGE_EXACTITUDE:.2f}"
    ),
    "B_reduction_significative": (
        f"réduction moyenne des recherches ≥ {REDUCTION_MINIMALE:.0%} "
        f"ET p < {ALPHA} au test des signes apparié"
    ),
    "verdict_soutenue": "A et B vérifiés sur le jeu de test tenu à l'écart",
    "verdict_partielle": (
        "B vérifié mais A non (moins de recherches au prix de l'exactitude), "
        "ou B vérifié sur la calibration seulement"
    ),
    "verdict_refutee": (
        "B non vérifié : pas de réduction, réduction sous le seuil, "
        "ou écart non significatif"
    ),
}


# --- Mesures agrégées ----------------------------------------------------------


@dataclass
class ArmStats:
    """Ce qu'une stratégie a coûté et rapporté sur un jeu de tâches."""

    strategy: str
    accuracy: float = 0.0
    net: float = 0.0
    noise: float = 0.0
    searches: float = 0.0
    fetches: float = 0.0
    tokens: float = 0.0
    llm_calls: float = 0.0
    latency_ms: float = 0.0
    cost: float = 0.0
    searches_per_correct: float = float("inf")
    correct: int = 0
    runs: int = 0

    @property
    def label(self) -> str:
        return arms.LABELS.get(self.strategy, self.strategy)

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy, "label": self.label,
            "accuracy": round(self.accuracy, 3), "net": round(self.net, 3),
            "noise": round(self.noise, 3), "searches": round(self.searches, 2),
            "fetches": round(self.fetches, 2), "tokens": round(self.tokens),
            "llm_calls": round(self.llm_calls, 2),
            "latency_ms": round(self.latency_ms),
            "cost": round(self.cost, 6),
            "searches_per_correct": (
                round(self.searches_per_correct, 2)
                if self.searches_per_correct != float("inf") else None
            ),
            "correct": self.correct, "runs": self.runs,
        }


def _cost(tokens: float) -> float:
    return tokens / 1_000_000 * PRIX_PAR_MILLION_JETONS


def summarize(rows: list[Row], strategy: str) -> ArmStats:
    selection = [row for row in rows if row.outcome.strategy == strategy]
    stats = ArmStats(strategy=strategy, runs=len(selection))
    if not selection:
        return stats

    stats.accuracy = statistics.fmean(r.score.accuracy for r in selection)
    stats.net = statistics.fmean(r.score.net for r in selection)
    stats.noise = statistics.fmean(r.score.noise for r in selection)
    stats.searches = statistics.fmean(r.outcome.searches for r in selection)
    stats.fetches = statistics.fmean(r.outcome.fetches for r in selection)
    stats.tokens = statistics.fmean(r.outcome.tokens for r in selection)
    stats.llm_calls = statistics.fmean(r.outcome.llm_calls for r in selection)
    stats.latency_ms = statistics.fmean(r.outcome.latency_ms for r in selection)
    stats.cost = _cost(stats.tokens)

    stats.correct = sum(1 for r in selection if r.score.accuracy >= 0.999)
    total_recherches = sum(r.outcome.searches for r in selection)
    # « Recherches par réponse correcte » : le rapport qualité/prix de la
    # stratégie. Une stratégie qui cherche peu mais se trompe toujours n'y
    # gagne rien — la division la punit.
    stats.searches_per_correct = (
        total_recherches / stats.correct if stats.correct else float("inf")
    )
    return stats


# --- Comparaison appariée ------------------------------------------------------


@dataclass
class PairedResult:
    """Confrontation appariée de deux stratégies sur un jeu de tâches."""

    challenger: str
    reference: str
    unit: str                       # "tâche" ou "tâche×graine"
    n: int = 0
    accuracy_delta: float = 0.0
    accuracy_ci: tuple[float, float] = (0.0, 0.0)
    search_delta: float = 0.0
    search_ci: tuple[float, float] = (0.0, 0.0)
    search_ratio: float = 1.0
    reduction: float = 0.0
    wins: int = 0                   # moins de recherches
    losses: int = 0                 # plus de recherches
    ties: int = 0
    p_value: float = 1.0

    def to_dict(self) -> dict:
        return {
            "challenger": self.challenger, "reference": self.reference,
            "unit": self.unit, "n": self.n,
            "accuracy_delta": round(self.accuracy_delta, 4),
            "accuracy_ci95": [round(v, 4) for v in self.accuracy_ci],
            "search_delta": round(self.search_delta, 3),
            "search_ci95": [round(v, 3) for v in self.search_ci],
            "search_ratio": round(self.search_ratio, 3),
            "reduction": round(self.reduction, 4),
            "wins": self.wins, "losses": self.losses, "ties": self.ties,
            "p_value": round(self.p_value, 4),
        }


def _grouped(rows: list[Row], by_seed: bool) -> dict:
    """Regroupe les lignes par tâche (ou par couple tâche×graine)."""
    groupes: dict = {}
    for row in rows:
        cle = (row.outcome.task_id, row.outcome.seed) if by_seed else row.outcome.task_id
        groupes.setdefault(cle, {}).setdefault(row.outcome.strategy, []).append(row)
    return groupes


def paired(
    rows: list[Row], challenger: str, reference: str, *, by_seed: bool = False
) -> PairedResult:
    """Compare deux stratégies, unité par unité.

    Par défaut l'unité est la **tâche** : les graines d'une même tâche sont
    moyennées avant comparaison. Les compter comme des observations séparées
    multiplierait artificiellement l'effectif — c'est de la pseudo-réplication,
    et cela ferait baisser la p-valeur sans rien apporter comme preuve.
    """
    result = PairedResult(
        challenger=challenger, reference=reference,
        unit="tâche×graine" if by_seed else "tâche",
    )
    ecarts_exactitude: list[float] = []
    ecarts_recherches: list[float] = []
    total_a = total_b = 0.0

    for _cle, par_strategie in sorted(_grouped(rows, by_seed).items()):
        a, b = par_strategie.get(challenger), par_strategie.get(reference)
        if not a or not b:
            continue
        exact_a = statistics.fmean(r.score.net for r in a)
        exact_b = statistics.fmean(r.score.net for r in b)
        cherche_a = statistics.fmean(r.outcome.searches for r in a)
        cherche_b = statistics.fmean(r.outcome.searches for r in b)

        ecarts_exactitude.append(exact_a - exact_b)
        ecarts_recherches.append(cherche_a - cherche_b)
        total_a += cherche_a
        total_b += cherche_b

        if cherche_a < cherche_b - 1e-9:
            result.wins += 1
        elif cherche_a > cherche_b + 1e-9:
            result.losses += 1
        else:
            result.ties += 1

    result.n = len(ecarts_recherches)
    if not result.n:
        return result

    result.accuracy_delta = statistics.fmean(ecarts_exactitude)
    result.accuracy_ci = bootstrap_ci(ecarts_exactitude)
    result.search_delta = statistics.fmean(ecarts_recherches)
    result.search_ci = bootstrap_ci(ecarts_recherches)
    result.search_ratio = total_a / total_b if total_b else 1.0
    result.reduction = 1 - result.search_ratio
    result.p_value = sign_test(result.wins, result.losses)
    return result


# --- Verdict -------------------------------------------------------------------


@dataclass
class H2Verdict:
    status: str                     # soutenue | partielle | refutee
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    criterion_a: bool = False
    criterion_b: bool = False

    @property
    def label(self) -> str:
        return {
            "soutenue": "H2 SOUTENUE",
            "partielle": "H2 PARTIELLEMENT SOUTENUE",
            "refutee": "H2 RÉFUTÉE",
        }[self.status]

    def to_dict(self) -> dict:
        return {
            "status": self.status, "label": self.label,
            "criterion_a": self.criterion_a, "criterion_b": self.criterion_b,
            "reasons": self.reasons, "warnings": self.warnings,
        }


def judge_h2(test: PairedResult, calibration: PairedResult) -> H2Verdict:
    """Applique les critères pré-enregistrés. Aucun n'est ajusté après coup."""
    reasons: list[str] = []
    warnings: list[str] = []

    # Critère A — l'exactitude reste comparable (test de non-infériorité).
    a_ok = test.accuracy_ci[0] >= -MARGE_EXACTITUDE
    if a_ok:
        reasons.append(
            f"A vérifié : écart d'exactitude nette {test.accuracy_delta:+.3f} "
            f"(IC95 [{test.accuracy_ci[0]:+.3f}, {test.accuracy_ci[1]:+.3f}]), "
            f"borne basse au-dessus de la marge de −{MARGE_EXACTITUDE:.2f}."
        )
    else:
        reasons.append(
            f"A non vérifié : la borne basse de l'IC95 de l'écart d'exactitude "
            f"({test.accuracy_ci[0]:+.3f}) descend sous la marge de "
            f"−{MARGE_EXACTITUDE:.2f} : l'exactitude n'est plus comparable."
        )

    # Critère B — la réduction existe, atteint le seuil, et est significative.
    assez = test.reduction >= REDUCTION_MINIMALE
    significatif = test.p_value < ALPHA
    b_ok = assez and significatif
    if not assez:
        reasons.append(
            f"B non vérifié : les recherches ne baissent que de "
            f"{test.reduction:.0%} (seuil pré-enregistré : {REDUCTION_MINIMALE:.0%})."
        )
    if not significatif:
        reasons.append(
            f"B non vérifié : p = {test.p_value:.3f} ≥ {ALPHA} au test des signes "
            f"({test.wins} tâches moins chères, {test.losses} plus chères, "
            f"{test.ties} égales sur n = {test.n})."
        )
    if b_ok:
        reasons.append(
            f"B vérifié : {test.reduction:.0%} de recherches en moins "
            f"(écart moyen {test.search_delta:+.2f} par tâche, IC95 "
            f"[{test.search_ci[0]:+.2f}, {test.search_ci[1]:+.2f}]), p = "
            f"{test.p_value:.3f}."
        )

    if test.search_ci[0] <= 0 <= test.search_ci[1]:
        warnings.append(
            f"L'IC95 de l'écart de recherches [{test.search_ci[0]:+.2f}, "
            f"{test.search_ci[1]:+.2f}] contient zéro : l'absence de réduction "
            "reste plausible."
        )
    if calibration.n and (calibration.reduction >= REDUCTION_MINIMALE) != assez:
        warnings.append(
            f"Les deux jeux ne disent pas la même chose : réduction de "
            f"{calibration.reduction:.0%} en calibration contre "
            f"{test.reduction:.0%} en test. L'effet dépend du terrain."
        )
    if test.n < 10:
        warnings.append(
            f"n = {test.n} tâches : même significatif, un effet mesuré sur si "
            "peu de tâches demande une réplication."
        )

    if b_ok and a_ok:
        status = "soutenue"
    elif b_ok or (calibration.reduction >= REDUCTION_MINIMALE and calibration.p_value < ALPHA):
        status = "partielle"
    else:
        status = "refutee"

    return H2Verdict(
        status=status, reasons=reasons, warnings=warnings,
        criterion_a=a_ok, criterion_b=b_ok,
    )


# --- Exécution -----------------------------------------------------------------


@dataclass
class DatasetRun:
    """Résultats sur un jeu de tâches."""

    name: str
    rows: list[Row] = field(default_factory=list)
    stats: dict[str, ArmStats] = field(default_factory=dict)
    stops: dict[str, dict[str, int]] = field(default_factory=dict)
    errors: dict[str, dict[str, int]] = field(default_factory=dict)
    wasted: dict[str, int] = field(default_factory=dict)
    paired_task: PairedResult | None = None
    paired_seed: PairedResult | None = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "stats": {k: v.to_dict() for k, v in self.stats.items()},
            "stops": self.stops, "errors": self.errors, "wasted": self.wasted,
            "paired_task": self.paired_task.to_dict() if self.paired_task else None,
            "paired_seed": self.paired_seed.to_dict() if self.paired_seed else None,
            "rows": [r.to_dict() for r in self.rows],
        }


@dataclass
class H2Result:
    statement: str = H2_STATEMENT
    criteria: dict = field(default_factory=lambda: dict(CRITERES))
    seeds: tuple[int, ...] = SEEDS
    calibration: DatasetRun | None = None
    test: DatasetRun | None = None
    verdict: H2Verdict | None = None
    explanation: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "statement": self.statement, "criteria": self.criteria,
            "seeds": list(self.seeds),
            "calibration": self.calibration.to_dict() if self.calibration else None,
            "test": self.test.to_dict() if self.test else None,
            "verdict": self.verdict.to_dict() if self.verdict else None,
            "explanation": self.explanation,
        }


def run_dataset(
    name: str,
    tasks: list[Task],
    corpus: Corpus,
    settings: Settings,
    *,
    seeds: tuple[int, ...] = SEEDS,
) -> DatasetRun:
    """Joue toutes les stratégies, sur toutes les tâches, pour chaque graine."""
    run = DatasetRun(name=name)
    # La temporisation entre requêtes existe pour ne pas se faire limiter par
    # un vrai moteur. Ici le web est figé : la garder ne mesurerait qu'un
    # `sleep`, et la latence rapportée ne voudrait plus rien dire.
    settings = replace(settings, search_delay=0.0)

    for seed in seeds:
        web = corpus_for(corpus, seed)
        for task in tasks:
            pose = task_for(task, seed)
            lignes: list[Row] = []
            for strategy in arms.STRATEGIES:
                outcome = arms.run(strategy, pose, settings, web, seed=seed)
                # L'identifiant reste celui de la tâche d'origine : c'est lui
                # qui apparie les stratégies entre elles.
                outcome.task_id = task.id
                lignes.append(Row(task=task, outcome=outcome, score=score(task, outcome)))

            # Les erreurs se jugent en comparant les stratégies **sur la même
            # tâche et la même graine** : c'est là qu'on sait si une réponse
            # manquée était atteignable, et à quel prix.
            justes = [r for r in lignes if r.score.accuracy >= 0.999]
            meilleur = min((r.outcome.searches for r in justes), default=None)
            for row in lignes:
                row.errors = classify_errors(
                    row.task, row.outcome, row.score,
                    best_searches=meilleur, someone_found=bool(justes),
                )
            run.rows.extend(lignes)

    for strategy in arms.STRATEGIES:
        selection = [r for r in run.rows if r.outcome.strategy == strategy]
        run.stats[strategy] = summarize(run.rows, strategy)
        arrets: dict[str, int] = {}
        fautes: dict[str, int] = {}
        gaspille = 0
        for row in selection:
            code = stop_reason(row.outcome)
            arrets[code] = arrets.get(code, 0) + 1
            if row.errors is None:
                continue
            for kind in row.errors.kinds:
                fautes[kind] = fautes.get(kind, 0) + 1
            gaspille += row.errors.wasted_searches
        run.stops[strategy] = arrets
        run.errors[strategy] = fautes
        run.wasted[strategy] = gaspille

    # Garde-fou de harnais : une stratégie qui cherche et ne ramène jamais rien
    # signale une panne du banc, pas une contre-performance. Le premier essai
    # de cette expérience est tombé exactement là-dessus — une exception avalée
    # dans le moteur simulé — et les chiffres avaient l'air simplement mauvais.
    for strategy in arms.STRATEGIES:
        selection = [r for r in run.rows if r.outcome.strategy == strategy]
        if strategy != "model_only" and selection:
            cherche = sum(r.outcome.searches for r in selection)
            trouve = sum(len(r.outcome.sources) for r in selection)
            if cherche and not trouve:
                raise RuntimeError(
                    f"harnais en panne : « {strategy} » a lancé {cherche} "
                    f"recherche(s) sur « {name} » sans jamais ramener une page."
                )

    run.paired_task = paired(run.rows, "adaptive_reasoning", "fixed")
    run.paired_seed = paired(run.rows, "adaptive_reasoning", "fixed", by_seed=True)
    return run


def explain(result: H2Result) -> list[str]:
    """Pourquoi ADAPTIVE cherche moins — analyse *après* le verdict.

    Cette section n'a de sens que si l'effet est là. Elle est donc calculée à
    partir des mesures, pas rédigée d'avance : ce sont les raisons d'arrêt et
    les budgets alloués qui parlent.
    """
    lignes: list[str] = []
    test = result.test
    if test is None or test.paired_task is None:
        return lignes

    adaptatif = test.stats["adaptive_reasoning"]
    fixe = test.stats["fixed"]
    if test.paired_task.reduction <= 0:
        lignes.append(
            "Aucun effet à expliquer : sur le jeu de test, ADAPTIVE REASONING "
            "ne cherche pas moins que FIXED."
        )
        return lignes

    lignes.append(
        f"Le contrôleur alloue un budget **avant** de chercher, à partir de la "
        f"seule formulation de la question. FIXED dépense {fixe.searches:.2f} "
        f"recherches quelle que soit la question ; ADAPTIVE en dépense "
        f"{adaptatif.searches:.2f} en moyenne. L'écart ne vient pas d'un arrêt "
        "anticipé en cours de route — ces deux stratégies ne relancent jamais — "
        "mais d'une allocation plus basse dès le départ sur les questions "
        "jugées simples."
    )

    faciles = [r for r in test.rows if r.task.family == "facile"]
    if faciles:
        a_facile = statistics.fmean(
            r.outcome.searches for r in faciles if r.outcome.strategy == "adaptive_reasoning"
        )
        f_facile = statistics.fmean(
            r.outcome.searches for r in faciles if r.outcome.strategy == "fixed"
        )
        lignes.append(
            f"Sur les tâches **faciles**, l'écart est de {f_facile - a_facile:+.2f} "
            f"recherche par tâche ({a_facile:.2f} contre {f_facile:.2f}) : c'est "
            "là que l'économie se fait, exactement là où elle ne coûte rien."
        )

    profondes = [r for r in test.rows if r.task.family == "profond"]
    if profondes:
        a_profond = statistics.fmean(
            r.outcome.searches for r in profondes if r.outcome.strategy == "adaptive_reasoning"
        )
        f_profond = statistics.fmean(
            r.outcome.searches for r in profondes if r.outcome.strategy == "fixed"
        )
        lignes.append(
            f"Sur les tâches **profondes**, l'écart tombe à "
            f"{f_profond - a_profond:+.2f} ({a_profond:.2f} contre "
            f"{f_profond:.2f}) : le contrôleur y maintient le budget. Une "
            "économie uniforme aurait été suspecte — elle aurait signifié que "
            "le contrôleur coupe partout, sans lire la question."
        )

    perdues = test.wasted.get("fixed", 0)
    if perdues:
        lignes.append(
            f"Vu autrement : sur ce jeu, FIXED dépense {perdues} recherche(s) "
            "au-delà du minimum qui suffisait à trouver la bonne réponse. "
            "L'économie d'ADAPTIVE consiste largement à ne pas les faire."
        )

    lignes.append(
        "Limite de cette explication : elle décrit un mécanisme observé sur ce "
        "corpus, pas une loi. Le contrôleur est lexical — il compte des mots de "
        "la question. Sur un terrain où la difficulté ne se lit pas dans la "
        "formulation, rien ne garantit qu'il alloue mieux qu'un budget fixe."
    )
    return lignes


def run_h2(
    *,
    settings: Settings | None = None,
    seeds: tuple[int, ...] = SEEDS,
) -> H2Result:
    """Expérience H2 complète : calibration, puis jeu de test tenu à l'écart."""
    settings = settings or get_settings()
    result = H2Result(seeds=seeds)

    result.calibration = run_dataset(
        "calibration", CALIBRATION_TASKS, Corpus(), settings, seeds=seeds
    )
    result.test = run_dataset(
        "test tenu à l'écart", HELDOUT_TASKS, held_out_corpus(), settings, seeds=seeds
    )
    result.verdict = judge_h2(result.test.paired_task, result.calibration.paired_task)
    result.explanation = explain(result)
    return result


__all__ = [
    "ALPHA",
    "CRITERES",
    "H2_STATEMENT",
    "H2Result",
    "H2Verdict",
    "MARGE_EXACTITUDE",
    "PRIX_PAR_MILLION_JETONS",
    "REDUCTION_MINIMALE",
    "ArmStats",
    "DatasetRun",
    "PairedResult",
    "ERROR_ORDER",
    "explain",
    "judge_h2",
    "paired",
    "run_dataset",
    "run_h2",
    "summarize",
]
