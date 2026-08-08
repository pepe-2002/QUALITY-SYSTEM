"""EXPÉRIENCE ADAPTIVE-V2 — corriger un défaut, pas fabriquer un résultat.

Ce que cette expérience est, et n'est pas
----------------------------------------
Elle **ne prouve rien sur H2**. H1 reste non concluante, H2 partiellement
soutenue, et leurs résultats bruts ne bougent pas. Ici on ne teste pas une
hypothèse sur le raisonnement adaptatif en général : on vérifie qu'un **défaut
précis**, identifié par H2, est corrigé.

Le défaut, tel que constaté sur le jeu 2
----------------------------------------
ADAPTIVE-V1 réduit les recherches presque partout — y compris là où il ne
faudrait pas. Sur les tâches profondes du jeu 2, elle dépensait 1,00 recherche
contre 3,00 pour FIXED, et obtenait 0,80 d'exactitude nette contre 1,00. Elle
ne distingue donc pas une question facile d'une question profonde : elle
rationne uniformément.

La logique de V2, documentée avant le test
------------------------------------------
1. **Estimer la difficulté AVANT de chercher** (`estimate_difficulty`), sur
   des caractéristiques de la seule question :

   * la **grandeur demandée** — un horaire officiel ou un taux statistique est
     publié à un seul endroit ; un prix courant est répété partout ;
   * l'**exigence d'autorité** — « officiel », « exact », « règlement » ;
   * l'**ampleur** — comparaison, plusieurs grandeurs, propositions enchaînées ;
   * la **longueur**, qui ne compte qu'un peu : c'est précisément l'erreur de
     V1 d'avoir cru qu'une question courte est une question facile.

2. **Trois niveaux, trois budgets** : simple → 1 recherche, intermédiaire → 3,
   profonde → 6 (toujours plafonné par `max_search_steps`).

3. **Réviser en cours de route** sur des signaux explicites :

   * la grandeur demandée est introuvable dans les sources → *difficile* → le
     budget monte ;
   * elle y est → *information suffisante* → arrêt anticipé, budget rendu ;
   * on ne sait pas trancher → on ne touche à rien.

Garde-fous exigés, et où ils sont
---------------------------------
* **arrêt prématuré sur tâche difficile** — l'arrêt anticipé n'est possible que
  si la grandeur demandée a été *trouvée* (`judge_difficulty`) ;
* **recherche inutile sur tâche facile** — dès que c'est trouvé, on s'arrête ;
* **dépassement du budget maximal** — `min(..., max_search_steps)` à chaque
  allocation et à chaque montée ;
* **boucle infinie** — `MAX_REVISIONS` révisions au plus, et une seule requête
  de repli fabriquée par tâche.

Ce qui ne doit pas arriver
--------------------------
V2 ne doit pas allouer un gros budget aux questions dont on connaît déjà la
réponse : l'estimateur ne voit jamais le corpus, jamais la vérité de référence,
jamais un résultat de recherche. Il ne lit que la question. Un test le vérifie.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field, replace

from ..analysis.facts import extractor
from ..core.complexity import MAX_REVISIONS
from ..core.config import Settings, get_settings
from . import strategies as arms
from .corpus import Corpus
from .dataset import TASKS as JEU1_TASKS
from .dataset import Task
from .experiment import bootstrap_ci, sign_test
from .h2 import ArmStats, _cost, paired, summarize
from .heldout import TASKS as JEU2_TASKS
from .heldout import held_out_corpus as jeu2_corpus
from .heldout2 import TASKS as JEU3_TASKS
from .heldout2 import held_out_corpus as jeu3_corpus
from .metrics import Row, score
from .seeds import SEEDS, corpus_for, task_for
from .stops import classify_errors, stop_reason

#: Version évaluée. Enregistrée avant le test, citée dans le rapport.
CONTROLLER_VERSION = "ADAPTIVE-V2 (2026-08-08)"

#: Baseline immuable.
BASELINE_VERSION = "ADAPTIVE-V1 (gelée — baseline de H1 et H2)"

#: Marge de non-infériorité en exactitude nette.
MARGE_EXACTITUDE = 0.05
#: Réduction de recherches à conserver face à FIXED.
REDUCTION_MINIMALE = 0.20
#: Écart minimal de budget entre tâches profondes et faciles pour que l'on
#: puisse dire que le contrôleur **discrimine** au lieu de rationner.
DISCRIMINATION_MINIMALE = 0.50
#: Régression tolérée face à V1 sur l'exactitude globale.
REGRESSION_TOLEREE = 0.02

CRITERES = {
    "C1_defaut_corrige": (
        "sur les tâches profondes, exactitude nette de V2 ≥ FIXED − "
        f"{MARGE_EXACTITUDE:.2f} ET V2 alloue au moins "
        f"{DISCRIMINATION_MINIMALE:.2f} recherche de plus aux tâches profondes "
        "qu'aux faciles"
    ),
    "C2_economie_conservee": (
        f"réduction globale des recherches face à FIXED ≥ {REDUCTION_MINIMALE:.0%}"
    ),
    "C3_pas_de_regression": (
        f"exactitude nette globale de V2 ≥ celle de V1 − {REGRESSION_TOLEREE:.2f}"
    ),
    "verdict_corrige": "C1 et C2 et C3",
    "verdict_partiel": "C1 vérifié, mais C2 ou C3 non",
    "verdict_non_corrige": "C1 non vérifié",
}

#: Métriques relevées, fixées avant le test.
METRIQUES = (
    "exactitude", "recherches", "appels LLM", "jetons", "latence",
    "coût estimé", "recherches par réponse correcte",
    "arrêts prématurés", "recherches inutiles",
)


@dataclass
class V2Verdict:
    status: str          # corrige | partiel | non_corrige
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    c1: bool = False
    c2: bool = False
    c3: bool = False

    @property
    def label(self) -> str:
        return {
            "corrige": "DÉFAUT CORRIGÉ",
            "partiel": "CORRECTION PARTIELLE",
            "non_corrige": "DÉFAUT NON CORRIGÉ",
        }[self.status]

    def to_dict(self) -> dict:
        return {
            "status": self.status, "label": self.label,
            "c1": self.c1, "c2": self.c2, "c3": self.c3,
            "reasons": self.reasons, "warnings": self.warnings,
        }


@dataclass
class V2Run:
    """Résultats sur un jeu de tâches, pour les trois bras comparés."""

    name: str
    rows: list[Row] = field(default_factory=list)
    stats: dict[str, ArmStats] = field(default_factory=dict)
    stops: dict[str, dict[str, int]] = field(default_factory=dict)
    errors: dict[str, dict[str, int]] = field(default_factory=dict)
    wasted: dict[str, int] = field(default_factory=dict)
    by_family: dict[str, dict[str, dict[str, float]]] = field(default_factory=dict)
    difficulties: dict[str, dict[str, int]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "stats": {k: v.to_dict() for k, v in self.stats.items()},
            "stops": self.stops, "errors": self.errors, "wasted": self.wasted,
            "by_family": self.by_family, "difficulties": self.difficulties,
            "rows": [r.to_dict() for r in self.rows],
        }


@dataclass
class V2Result:
    controller_version: str = CONTROLLER_VERSION
    baseline_version: str = BASELINE_VERSION
    criteria: dict = field(default_factory=lambda: dict(CRITERES))
    metrics: tuple = METRIQUES
    seeds: tuple[int, ...] = SEEDS
    jeu1: V2Run | None = None
    jeu2: V2Run | None = None
    jeu3: V2Run | None = None
    verdict: V2Verdict | None = None
    explanation: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "controller_version": self.controller_version,
            "baseline_version": self.baseline_version,
            "criteria": self.criteria, "metrics": list(self.metrics),
            "seeds": list(self.seeds),
            "jeu1": self.jeu1.to_dict() if self.jeu1 else None,
            "jeu2": self.jeu2.to_dict() if self.jeu2 else None,
            "jeu3": self.jeu3.to_dict() if self.jeu3 else None,
            "verdict": self.verdict.to_dict() if self.verdict else None,
            "explanation": self.explanation,
        }


# --- Exécution -----------------------------------------------------------------


def run_v2_dataset(*args, **kwargs) -> V2Run:
    """Joue un jeu avec l'extracteur qui a produit les chiffres publiés."""
    with extractor("baseline"):
        return _run_v2_dataset(*args, **kwargs)


def _run_v2_dataset(
    name: str,
    tasks: list[Task],
    corpus: Corpus,
    settings: Settings,
    *,
    seeds: tuple[int, ...] = SEEDS,
) -> V2Run:
    """Joue FIXED, ADAPTIVE-V1 et ADAPTIVE-V2 sur un jeu de tâches."""
    run = V2Run(name=name)
    settings = replace(settings, search_delay=0.0)

    for seed in seeds:
        web = corpus_for(corpus, seed)
        for task in tasks:
            pose = task_for(task, seed)
            lignes: list[Row] = []
            for strategy in arms.V2_STRATEGIES:
                outcome = arms.run(strategy, pose, settings, web, seed=seed)
                outcome.task_id = task.id
                lignes.append(Row(task=task, outcome=outcome, score=score(task, outcome)))

            justes = [r for r in lignes if r.score.accuracy >= 0.999]
            meilleur = min((r.outcome.searches for r in justes), default=None)
            for row in lignes:
                row.errors = classify_errors(
                    row.task, row.outcome, row.score,
                    best_searches=meilleur, someone_found=bool(justes),
                )
            run.rows.extend(lignes)

    for strategy in arms.V2_STRATEGIES:
        selection = [r for r in run.rows if r.outcome.strategy == strategy]
        run.stats[strategy] = summarize(run.rows, strategy)

        arrets: dict[str, int] = {}
        fautes: dict[str, int] = {}
        niveaux: dict[str, int] = {}
        gaspille = 0
        for row in selection:
            code = stop_reason(row.outcome)
            arrets[code] = arrets.get(code, 0) + 1
            if row.outcome.difficulty:
                niveaux[row.outcome.difficulty] = niveaux.get(row.outcome.difficulty, 0) + 1
            if row.errors is None:
                continue
            for kind in row.errors.kinds:
                fautes[kind] = fautes.get(kind, 0) + 1
            gaspille += row.errors.wasted_searches
        run.stops[strategy] = arrets
        run.errors[strategy] = fautes
        run.wasted[strategy] = gaspille
        run.difficulties[strategy] = niveaux

        familles: dict[str, dict[str, float]] = {}
        for famille in ("facile", "profond", "piege"):
            lignes = [r for r in selection if r.task.family == famille]
            if lignes:
                familles[famille] = {
                    "searches": statistics.fmean(r.outcome.searches for r in lignes),
                    "net": statistics.fmean(r.score.net for r in lignes),
                    "accuracy": statistics.fmean(r.score.accuracy for r in lignes),
                }
        run.by_family[strategy] = familles

    return run


# --- Verdict -------------------------------------------------------------------


def judge_v2(run: V2Run) -> V2Verdict:
    """Applique les trois critères, tels qu'écrits avant le test."""
    reasons: list[str] = []
    warnings: list[str] = []

    v2 = run.stats.get("adaptive_v2")
    v1 = run.stats.get("adaptive_reasoning")
    fixe = run.stats.get("fixed")
    if not (v2 and v1 and fixe):
        return V2Verdict("non_corrige", ["mesures manquantes"])

    familles_v2 = run.by_family.get("adaptive_v2", {})
    familles_fixe = run.by_family.get("fixed", {})
    profond_v2 = familles_v2.get("profond", {})
    profond_fixe = familles_fixe.get("profond", {})
    facile_v2 = familles_v2.get("facile", {})

    # C1 — le défaut visé est-il corrigé ?
    exact_ok = profond_v2.get("net", 0.0) >= profond_fixe.get("net", 0.0) - MARGE_EXACTITUDE
    ecart = profond_v2.get("searches", 0.0) - facile_v2.get("searches", 0.0)
    discrimine = ecart >= DISCRIMINATION_MINIMALE
    c1 = exact_ok and discrimine

    reasons.append(
        f"Tâches profondes : V2 obtient {profond_v2.get('net', 0):.2f} d'exactitude "
        f"nette contre {profond_fixe.get('net', 0):.2f} pour FIXED "
        f"({'dans' if exact_ok else 'hors'} la marge de {MARGE_EXACTITUDE:.2f})."
    )
    reasons.append(
        f"Discrimination : V2 alloue {profond_v2.get('searches', 0):.2f} recherches "
        f"aux tâches profondes contre {facile_v2.get('searches', 0):.2f} aux faciles, "
        f"soit {ecart:+.2f} (seuil : {DISCRIMINATION_MINIMALE:+.2f}) — "
        f"{'elle distingue' if discrimine else 'elle ne distingue pas'} les deux."
    )

    # C2 — l'économie face à FIXED est-elle conservée ?
    ratio = v2.searches / fixe.searches if fixe.searches else 1.0
    reduction = 1 - ratio
    c2 = reduction >= REDUCTION_MINIMALE
    reasons.append(
        f"Économie : {reduction:.0%} de recherches en moins que FIXED "
        f"(seuil : {REDUCTION_MINIMALE:.0%})."
    )

    # C3 — pas de régression face à V1.
    c3 = v2.net >= v1.net - REGRESSION_TOLEREE
    reasons.append(
        f"Face à la baseline gelée : V2 {v2.net:.2f} contre V1 {v1.net:.2f} "
        f"d'exactitude nette ({v2.net - v1.net:+.2f})."
    )

    premature_v2 = run.errors.get("adaptive_v2", {}).get("arret_trop_tot", 0)
    premature_v1 = run.errors.get("adaptive_reasoning", {}).get("arret_trop_tot", 0)
    reasons.append(
        f"Arrêts prématurés : {premature_v2} pour V2 contre {premature_v1} pour V1. "
        f"Recherches inutiles : {run.wasted.get('adaptive_v2', 0)} contre "
        f"{run.wasted.get('adaptive_reasoning', 0)}."
    )

    if v2.searches > fixe.searches:
        warnings.append(
            "V2 cherche davantage que FIXED : elle corrige peut-être le défaut, "
            "mais elle n'est plus une économie."
        )
    if not run.rows:
        warnings.append("aucune mesure")
    n_taches = len({r.outcome.task_id for r in run.rows})
    if n_taches < 10:
        warnings.append(
            f"n = {n_taches} tâches : un effet mesuré sur si peu demande une réplication."
        )

    status = "corrige" if (c1 and c2 and c3) else ("partiel" if c1 else "non_corrige")
    return V2Verdict(status=status, reasons=reasons, warnings=warnings, c1=c1, c2=c2, c3=c3)


def explain_v2(result: V2Result) -> list[str]:
    """Pourquoi V2 fait mieux — ou pourquoi elle ne fait pas mieux."""
    lignes: list[str] = []
    run = result.jeu3
    if run is None or not run.stats:
        return lignes

    v2 = run.stats["adaptive_v2"]
    v1 = run.stats["adaptive_reasoning"]
    fixe = run.stats["fixed"]
    fam_v2 = run.by_family.get("adaptive_v2", {})
    fam_v1 = run.by_family.get("adaptive_reasoning", {})

    ecart_v2 = (fam_v2.get("profond", {}).get("searches", 0)
                - fam_v2.get("facile", {}).get("searches", 0))
    ecart_v1 = (fam_v1.get("profond", {}).get("searches", 0)
                - fam_v1.get("facile", {}).get("searches", 0))

    if ecart_v2 > ecart_v1 + 1e-9:
        lignes.append(
            f"**Ce qui a changé.** V1 allouait {ecart_v1:+.2f} recherche d'écart "
            f"entre une tâche profonde et une tâche facile ; V2 en alloue "
            f"{ecart_v2:+.2f}. C'est le défaut visé : V1 rationnait uniformément, "
            "V2 dépense là où c'est nécessaire."
        )
    else:
        lignes.append(
            f"**Le défaut persiste.** V2 alloue {ecart_v2:+.2f} recherche d'écart "
            f"entre profond et facile, contre {ecart_v1:+.2f} pour V1 : "
            "l'estimateur ne discrimine pas davantage."
        )

    lignes.append(
        f"**D'où vient la différence.** L'estimateur de V2 lit la *grandeur "
        f"demandée* : un horaire ou un taux officiel est publié à un seul "
        f"endroit, un prix courant partout. V1 ne lisait que la forme de la "
        f"demande — longueur, comparaison, livrable — et une question courte lui "
        f"paraissait facile. La révision en cours de route fait le reste : quand "
        f"la grandeur demandée n'apparaît dans aucune source, le budget monte au "
        f"lieu de rester bloqué sur l'estimation de départ."
    )

    lignes.append(
        f"**Le prix.** V2 dépense {v2.searches:.2f} recherches en moyenne contre "
        f"{v1.searches:.2f} pour V1 et {fixe.searches:.2f} pour FIXED, pour "
        f"{v2.searches_per_correct:.2f} recherches par réponse correcte contre "
        f"{v1.searches_per_correct:.2f} et {fixe.searches_per_correct:.2f}."
    )

    lignes.append(
        "**Ce que cela ne dit pas.** V2 n'est pas une preuve de H2, et ce jeu de "
        "test ne dit rien de son comportement hors de ce corpus. La prochaine "
        "amélioration devra passer par une nouvelle expérience, sur un jeu "
        "encore jamais utilisé."
    )
    return lignes


def run_v2_experiment(
    *,
    settings: Settings | None = None,
    seeds: tuple[int, ...] = SEEDS,
    include_calibration: bool = True,
) -> V2Result:
    """Expérience complète. Le verdict ne porte que sur le **jeu 3**."""
    settings = settings or get_settings()
    result = V2Result(seeds=seeds)

    if include_calibration:
        result.jeu1 = run_v2_dataset("jeu 1 — calibration", JEU1_TASKS, Corpus(), settings, seeds=seeds)
        result.jeu2 = run_v2_dataset("jeu 2 — première validation", JEU2_TASKS, jeu2_corpus(), settings, seeds=seeds)
    result.jeu3 = run_v2_dataset("jeu 3 — test final", JEU3_TASKS, jeu3_corpus(), settings, seeds=seeds)

    result.verdict = judge_v2(result.jeu3)
    result.explanation = explain_v2(result)
    return result


__all__ = [
    "BASELINE_VERSION",
    "CONTROLLER_VERSION",
    "CRITERES",
    "DISCRIMINATION_MINIMALE",
    "MARGE_EXACTITUDE",
    "METRIQUES",
    "REDUCTION_MINIMALE",
    "REGRESSION_TOLEREE",
    "V2Result",
    "V2Run",
    "V2Verdict",
    "explain_v2",
    "judge_v2",
    "run_v2_dataset",
    "run_v2_experiment",
]
