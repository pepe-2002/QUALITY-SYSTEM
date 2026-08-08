"""RESEARCH LAB — l'expérience et son verdict (spec §18).

    « Le système doit chercher à réfuter l'hypothèse, pas à la confirmer. »

Cette phrase de la spécification commande tout le module. Concrètement :

1. L'hypothèse et ses **conditions de réfutation** sont écrites ici, dans le
   code, **avant** toute exécution. On ne choisit pas le critère après avoir vu
   le résultat — c'est ainsi qu'on se ment à soi-même.
2. Le jeu d'essai contient des **pièges** conçus pour faire perdre la stratégie
   adaptative. Un banc d'essai qui ne peut que donner raison ne prouve rien.
3. Le verdict ne dit jamais « confirmée ». Au mieux « non réfutée » : une
   expérience ne démontre pas une loi, elle échoue à l'abattre.
4. Les comparaisons sont **appariées** (même tâche, même corpus) et assorties
   d'un test de signe exact. Avec huit tâches, une moyenne seule ne veut rien
   dire.
"""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field
from math import comb

from ..analysis.facts import extractor
from ..core.config import Settings, get_settings
from . import strategies as arms
from .corpus import Corpus
from .dataset import TASKS, Task
from .metrics import Row, cost, score

#: Graine fixe : deux exécutions doivent donner le même rapport.
SEED = 20260807


@dataclass(frozen=True)
class Hypothesis:
    """Hypothèse pré-enregistrée, avec ses conditions de réfutation."""

    statement: str
    reference: str          # stratégie de comparaison
    challenger: str         # stratégie testée
    min_gain: float         # gain d'exactitude minimal exigé
    max_cost_ratio: float   # surcoût maximal toléré
    alpha: float            # seuil de signification

    def to_dict(self) -> dict:
        return {
            "statement": self.statement,
            "reference": self.reference, "challenger": self.challenger,
            "min_gain": self.min_gain, "max_cost_ratio": self.max_cost_ratio,
            "alpha": self.alpha,
        }


#: Seconde hypothèse, sur le coût. Elle porte sur le contrôleur de complexité
#: seul (sans boucle de relance) : à exactitude égale, allouer un budget selon
#: la difficulté doit coûter moins cher qu'un budget uniforme.
COST_HYPOTHESIS_NOTE = (
    "À exactitude au moins égale, ADAPTIVE REASONING doit consommer moins de "
    "recherches que FIXED REASONING. Réfutée si l'exactitude baisse, ou si le "
    "nombre de recherches ne diminue pas d'au moins 20 %."
)


#: L'hypothèse du projet, énoncée avant toute mesure.
HYPOTHESIS = Hypothesis(
    statement=(
        "À corpus identique, la recherche adaptative (analyser, puis relancer "
        "seulement si une information manque) obtient une exactitude nette "
        "supérieure à une recherche à budget fixe, sans dépenser plus de 50 % "
        "de calcul supplémentaire — et sans se dégrader sur les tâches pièges."
    ),
    reference="fixed",
    challenger="adaptive_research",
    min_gain=0.05,
    max_cost_ratio=1.5,
    alpha=0.05,
)


# --- Statistiques (sans dépendance) -------------------------------------------


def sign_test(wins: int, losses: int) -> float:
    """p-valeur bilatérale du test des signes (binomiale exacte).

    Les égalités sont écartées, comme le veut le test. Avec peu de tâches,
    c'est le test honnête : il ne suppose ni normalité ni variance connue.
    """
    n = wins + losses
    if n == 0:
        return 1.0
    extreme = max(wins, losses)
    queue = sum(comb(n, k) for k in range(extreme, n + 1)) / (2**n)
    return min(1.0, 2 * queue)


def bootstrap_ci(
    differences: list[float], *, draws: int = 5000, level: float = 0.95
) -> tuple[float, float]:
    """Intervalle de confiance de la différence moyenne, par ré-échantillonnage."""
    if not differences:
        return (0.0, 0.0)
    rng = random.Random(SEED)
    size = len(differences)
    means = sorted(
        statistics.fmean(rng.choice(differences) for _ in range(size))
        for _ in range(draws)
    )
    low = means[int((1 - level) / 2 * draws)]
    high = means[min(draws - 1, int((1 + level) / 2 * draws))]
    return (round(low, 4), round(high, 4))


# --- Résultats -----------------------------------------------------------------


@dataclass
class Comparison:
    """Confrontation appariée de deux stratégies."""

    challenger: str
    reference: str
    wins: int = 0
    losses: int = 0
    ties: int = 0
    mean_gain: float = 0.0
    ci: tuple[float, float] = (0.0, 0.0)
    p_value: float = 1.0
    cost_ratio: float = 1.0
    trap_gain: float = 0.0

    def to_dict(self) -> dict:
        return {
            "challenger": self.challenger, "reference": self.reference,
            "wins": self.wins, "losses": self.losses, "ties": self.ties,
            "mean_gain": round(self.mean_gain, 4), "ci95": list(self.ci),
            "p_value": round(self.p_value, 4),
            "cost_ratio": round(self.cost_ratio, 3),
            "trap_gain": round(self.trap_gain, 4),
        }


@dataclass
class Verdict:
    """Conclusion de l'expérience. Ne dit jamais « confirmée »."""

    status: str                     # refutee | non_concluante | non_refutee
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return {
            "refutee": "HYPOTHÈSE RÉFUTÉE",
            "non_concluante": "RÉSULTAT NON CONCLUANT",
            "non_refutee": "HYPOTHÈSE NON RÉFUTÉE",
        }[self.status]

    def to_dict(self) -> dict:
        return {"status": self.status, "label": self.label,
                "reasons": self.reasons, "warnings": self.warnings}


@dataclass
class CostVerdict:
    """Verdict de la seconde hypothèse : moins chercher, sans perdre."""

    status: str
    accuracy_delta: float
    search_ratio: float
    reason: str

    @property
    def label(self) -> str:
        return {
            "refutee": "SECONDE HYPOTHÈSE RÉFUTÉE",
            "non_refutee": "SECONDE HYPOTHÈSE NON RÉFUTÉE",
        }[self.status]

    def to_dict(self) -> dict:
        return {
            "status": self.status, "label": self.label,
            "accuracy_delta": round(self.accuracy_delta, 4),
            "search_ratio": round(self.search_ratio, 3),
            "reason": self.reason,
        }


@dataclass
class ExperimentResult:
    hypothesis: Hypothesis
    rows: list[Row] = field(default_factory=list)
    comparison: Comparison | None = None
    verdict: Verdict | None = None
    cost_verdict: CostVerdict | None = None

    def by_strategy(self, strategy: str) -> list[Row]:
        return [r for r in self.rows if r.outcome.strategy == strategy]

    def summary(self, strategy: str) -> dict:
        rows = self.by_strategy(strategy)
        if not rows:
            return {}
        return {
            "strategy": strategy,
            "label": arms.LABELS.get(strategy, strategy),
            "accuracy": round(statistics.fmean(r.score.accuracy for r in rows), 3),
            "net": round(statistics.fmean(r.score.net for r in rows), 3),
            "noise": round(statistics.fmean(r.score.noise for r in rows), 3),
            "quality": round(statistics.fmean(r.score.quality for r in rows), 3),
            "searches": round(statistics.fmean(r.outcome.searches for r in rows), 2),
            "fetches": round(statistics.fmean(r.outcome.fetches for r in rows), 2),
            "tool_calls": round(statistics.fmean(r.outcome.tool_calls for r in rows), 2),
            "tokens": round(statistics.fmean(r.outcome.tokens for r in rows)),
            "latency_ms": round(statistics.fmean(r.outcome.latency_ms for r in rows)),
            "cost": round(statistics.fmean(cost(r.outcome) for r in rows), 6),
        }

    def to_dict(self) -> dict:
        return {
            "hypothesis": self.hypothesis.to_dict(),
            "strategies": [self.summary(s) for s in arms.STRATEGIES],
            "comparison": self.comparison.to_dict() if self.comparison else None,
            "verdict": self.verdict.to_dict() if self.verdict else None,
            "cost_hypothesis": COST_HYPOTHESIS_NOTE,
            "cost_verdict": self.cost_verdict.to_dict() if self.cost_verdict else None,
            "rows": [r.to_dict() for r in self.rows],
        }


# --- Exécution ------------------------------------------------------------------


def run_experiment(
    tasks: list[Task] | None = None,
    *,
    settings: Settings | None = None,
    corpus: Corpus | None = None,
    hypothesis: Hypothesis = HYPOTHESIS,
) -> ExperimentResult:
    """Joue toutes les stratégies sur toutes les tâches, puis conclut."""
    tasks = tasks or TASKS
    settings = settings or get_settings()
    corpus = corpus or Corpus()
    result = ExperimentResult(hypothesis=hypothesis)

    # L'extracteur de faits est épinglé à la version qui a produit ces
    # chiffres. Le corriger ailleurs ne doit pas réécrire ce résultat.
    with extractor("baseline"):
        for task in tasks:
            for strategy in arms.STRATEGIES:
                outcome = arms.run(strategy, task, settings, corpus)
                result.rows.append(
                    Row(task=task, outcome=outcome, score=score(task, outcome))
                )

    result.comparison = compare(result, hypothesis.challenger, hypothesis.reference)
    result.verdict = judge(result, hypothesis)
    result.cost_verdict = judge_cost(result)
    return result


def judge_cost(result: ExperimentResult) -> CostVerdict:
    """Seconde hypothèse : allouer selon la difficulté doit coûter moins cher."""
    adaptatif = result.summary("adaptive_reasoning")
    fixe = result.summary("fixed")
    if not adaptatif or not fixe:
        return CostVerdict("refutee", 0.0, 1.0, "mesures manquantes")

    ecart = adaptatif["net"] - fixe["net"]
    ratio = adaptatif["searches"] / fixe["searches"] if fixe["searches"] else 1.0

    if ecart < -1e-9:
        return CostVerdict(
            "refutee", ecart, ratio,
            f"l'exactitude nette baisse de {ecart:+.3f} : économiser des "
            "recherches se paie en qualité de réponse.",
        )
    if ratio > 0.8:
        return CostVerdict(
            "refutee", ecart, ratio,
            f"les recherches ne baissent que de {(1 - ratio) * 100:.0f}% "
            "(seuil : 20 %) : le contrôleur de complexité n'économise pas grand-chose.",
        )
    return CostVerdict(
        "non_refutee", ecart, ratio,
        f"exactitude nette {ecart:+.3f} pour {(1 - ratio) * 100:.0f}% de "
        "recherches en moins.",
    )


def compare(result: ExperimentResult, challenger: str, reference: str) -> Comparison:
    """Confrontation appariée, tâche par tâche."""
    comparison = Comparison(challenger=challenger, reference=reference)
    differences: list[float] = []
    trap_diffs: list[float] = []

    par_tache = {}
    for row in result.rows:
        par_tache.setdefault(row.task.id, {})[row.outcome.strategy] = row

    for task_id, rows in par_tache.items():
        a, b = rows.get(challenger), rows.get(reference)
        if a is None or b is None:
            continue
        ecart = a.score.net - b.score.net
        differences.append(ecart)
        if a.task.family == "piege":
            trap_diffs.append(ecart)
        if ecart > 1e-9:
            comparison.wins += 1
        elif ecart < -1e-9:
            comparison.losses += 1
        else:
            comparison.ties += 1

    comparison.mean_gain = statistics.fmean(differences) if differences else 0.0
    comparison.ci = bootstrap_ci(differences)
    comparison.p_value = sign_test(comparison.wins, comparison.losses)
    comparison.trap_gain = statistics.fmean(trap_diffs) if trap_diffs else 0.0

    jetons_a = [r.outcome.tokens for r in result.by_strategy(challenger)]
    jetons_b = [r.outcome.tokens for r in result.by_strategy(reference)]
    moyenne_b = statistics.fmean(jetons_b) if jetons_b else 0
    comparison.cost_ratio = (
        statistics.fmean(jetons_a) / moyenne_b if moyenne_b else 1.0
    )
    return comparison


def judge(result: ExperimentResult, hypothesis: Hypothesis) -> Verdict:
    """Applique les conditions de réfutation, écrites avant l'expérience."""
    c = result.comparison
    assert c is not None
    reasons: list[str] = []
    warnings: list[str] = []

    # R1 — le gain d'exactitude doit exister et dépasser le seuil annoncé.
    if c.mean_gain < hypothesis.min_gain:
        reasons.append(
            f"Le gain d'exactitude nette est de {c.mean_gain:+.3f}, en deçà du "
            f"seuil de {hypothesis.min_gain:+.3f} annoncé avant l'expérience."
        )

    # R2 — le surcoût doit rester dans la limite annoncée.
    if c.cost_ratio > hypothesis.max_cost_ratio:
        reasons.append(
            f"Le coût est {c.cost_ratio:.2f}× celui de la référence, au-delà de "
            f"la limite de {hypothesis.max_cost_ratio:.2f}× annoncée."
        )

    # R3 — la stratégie ne doit pas nuire là où elle devrait s'abstenir.
    if c.trap_gain < -1e-9:
        reasons.append(
            f"Sur les tâches pièges, la stratégie adaptative fait {c.trap_gain:+.3f} "
            "d'exactitude : elle nuit précisément là où chercher plus est inutile."
        )

    # R4 — sans signification statistique, on ne conclut pas.
    if c.p_value > hypothesis.alpha:
        warnings.append(
            f"p = {c.p_value:.3f} > {hypothesis.alpha} : l'écart observé "
            f"({c.wins} victoires, {c.losses} défaites, {c.ties} égalités) peut "
            "venir du hasard. Le jeu d'essai est trop petit pour trancher."
        )
    if c.ci[0] <= 0 <= c.ci[1]:
        warnings.append(
            f"L'intervalle de confiance à 95 % du gain, [{c.ci[0]:+.3f}, "
            f"{c.ci[1]:+.3f}], contient zéro : l'absence de gain reste plausible."
        )

    if reasons:
        return Verdict("refutee", reasons, warnings)
    if warnings:
        return Verdict(
            "non_concluante",
            ["Aucune condition de réfutation n'est remplie, mais la preuve manque."],
            warnings,
        )
    return Verdict(
        "non_refutee",
        [
            f"Gain d'exactitude nette {c.mean_gain:+.3f} (IC95 "
            f"[{c.ci[0]:+.3f}, {c.ci[1]:+.3f}]), coût {c.cost_ratio:.2f}×, "
            f"p = {c.p_value:.3f}."
        ],
        ["Non réfutée ne veut pas dire démontrée : le jeu d'essai est petit "
         "et construit à la main."],
    )
