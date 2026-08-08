"""Rapport de l'expérience ADAPTIVE-V2."""

from __future__ import annotations

from . import strategies as arms
from .stops import ERROR_LABELS, ERROR_ORDER, STOP_LABELS, STOP_ORDER
from .v2 import (
    DISCRIMINATION_MINIMALE,
    MARGE_EXACTITUDE,
    REDUCTION_MINIMALE,
    REGRESSION_TOLEREE,
    V2Result,
    V2Run,
)


def _table_arms(run: V2Run) -> list[str]:
    lignes = [
        "| Stratégie | Exactitude | Nette | Recherches | Appels LLM | Jetons | "
        "Latence | Coût est. | Rech./réponse juste |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for strategy in arms.V2_STRATEGIES:
        s = run.stats.get(strategy)
        if not s:
            continue
        rpc = (
            f"{s.searches_per_correct:.2f}"
            if s.searches_per_correct != float("inf") else "—"
        )
        lignes.append(
            f"| {s.label} | {s.accuracy:.2f} | **{s.net:.2f}** | {s.searches:.2f} | "
            f"{s.llm_calls:.2f} | {s.tokens:.0f} | {s.latency_ms:.0f} ms | "
            f"{s.cost:.6f} | {rpc} |"
        )
    return lignes


def _table_families(run: V2Run) -> list[str]:
    familles = ("facile", "profond", "piege")
    lignes = [
        "| Stratégie | " + " | ".join(
            f"{f} : rech. / exact." for f in familles
        ) + " | écart profond − facile |",
        "|---|" + "---|" * (len(familles) + 1),
    ]
    for strategy in arms.V2_STRATEGIES:
        par_famille = run.by_family.get(strategy, {})
        cellules = []
        for famille in familles:
            data = par_famille.get(famille)
            cellules.append(
                f"{data['searches']:.2f} / {data['net']:.2f}" if data else "—"
            )
        ecart = (
            par_famille.get("profond", {}).get("searches", 0)
            - par_famille.get("facile", {}).get("searches", 0)
        )
        lignes.append(
            f"| {arms.LABELS[strategy]} | " + " | ".join(cellules) + f" | {ecart:+.2f} |"
        )
    return lignes


def _table_errors(run: V2Run) -> list[str]:
    lignes = [
        "| Stratégie | " + " | ".join(ERROR_LABELS[e] for e in ERROR_ORDER)
        + " | recherches gaspillées |",
        "|---|" + "---|" * (len(ERROR_ORDER) + 1),
    ]
    for strategy in arms.V2_STRATEGIES:
        fautes = run.errors.get(strategy, {})
        lignes.append(
            f"| {arms.LABELS[strategy]} | "
            + " | ".join(str(fautes.get(e, 0)) for e in ERROR_ORDER)
            + f" | {run.wasted.get(strategy, 0)} |"
        )
    return lignes


def _table_stops(run: V2Run) -> list[str]:
    codes = [c for c in (*STOP_ORDER, "passe_unique")
             if any(c in run.stops.get(s, {}) for s in arms.V2_STRATEGIES)]
    if not codes:
        return []
    lignes = [
        "| Stratégie | " + " | ".join(STOP_LABELS[c] for c in codes) + " |",
        "|---|" + "---|" * len(codes),
    ]
    for strategy in arms.V2_STRATEGIES:
        compte = run.stops.get(strategy, {})
        lignes.append(
            f"| {arms.LABELS[strategy]} | "
            + " | ".join(str(compte.get(c, 0)) for c in codes) + " |"
        )
    return lignes


def render(result: V2Result) -> str:
    lignes: list[str] = [
        "# ADAPTIVE-V2 — correction d'un défaut identifié",
        "",
        "## Ce que ce rapport n'est pas",
        "",
        "- Ce n'est **pas** une preuve de H2. H2 reste *partiellement soutenue*,",
        "  H1 reste *non concluante*, et leurs résultats bruts sont conservés",
        "  tels quels (`lab-report.md`, `h2-report.md`).",
        "- ADAPTIVE-V1 est **gelée définitivement**. Elle reste la baseline des",
        "  deux expériences précédentes et n'a pas été modifiée d'une ligne.",
        "- Toute amélioration ultérieure de V2 devra faire l'objet d'une",
        "  nouvelle expérience, sur un jeu encore jamais utilisé.",
        "",
        f"**Version évaluée** : {result.controller_version}",
        f"**Baseline** : {result.baseline_version}",
        "",
        "## Le défaut à corriger",
        "",
        "> Le contrôleur ne distingue pas suffisamment les tâches faciles des",
        "> tâches profondes. Il réduit les recherches presque partout, ce qui",
        "> produit une économie réelle mais une perte d'exactitude sur les",
        "> tâches difficiles.",
        "",
        "## Critères de réussite, écrits avant le test",
        "",
        "| Critère | Condition |",
        "|---|---|",
        f"| **C1 — défaut corrigé** | exactitude nette de V2 sur les tâches profondes ≥ FIXED − {MARGE_EXACTITUDE:.2f}, **et** au moins {DISCRIMINATION_MINIMALE:.2f} recherche d'écart entre profond et facile |",
        f"| **C2 — économie conservée** | ≥ {REDUCTION_MINIMALE:.0%} de recherches en moins que FIXED |",
        f"| **C3 — pas de régression** | exactitude nette globale ≥ celle de V1 − {REGRESSION_TOLEREE:.2f} |",
        "",
        "| Verdict | Condition |",
        "|---|---|",
        "| **DÉFAUT CORRIGÉ** | C1 et C2 et C3 |",
        "| **CORRECTION PARTIELLE** | C1 vérifié, mais C2 ou C3 non |",
        "| **DÉFAUT NON CORRIGÉ** | C1 non vérifié |",
        "",
        "**Métriques relevées** : " + ", ".join(result.metrics) + ".",
        "",
        "## Protocole",
        "",
        "- **Trois jeux, trois rôles.** Jeu 1 : développement et calibration.",
        "  Jeu 2 : première validation, dont les résultats ont été observés et",
        "  ont servi à concevoir V2. Jeu 3 : **jamais utilisé auparavant**, il",
        "  porte seul le verdict.",
        f"- **{len(result.seeds)} graines** : la formulation des questions et",
        "  l'ordre des résultats varient ; les faits, jamais.",
        "- **Trois bras** : FIXED, ADAPTIVE-V1, ADAPTIVE-V2. Même moteur de",
        "  synthèse, même corpus ; seule la décision de chercher change.",
        "- **V2 n'a pas été modifiée** après la première exécution du jeu 3.",
        "",
    ]

    ordre = [
        (result.jeu3, "Jeu 3 — test final (verdict)"),
        (result.jeu2, "Jeu 2 — première validation (indicatif)"),
        (result.jeu1, "Jeu 1 — calibration (indicatif)"),
    ]
    for run, titre in ordre:
        if run is None:
            continue
        lignes += [f"## {titre}", "", *_table_arms(run), ""]
        lignes += ["### Par famille de tâches — recherches / exactitude nette", ""]
        lignes += _table_families(run)
        lignes += ["", "### Erreurs relevées après coup", "", *_table_errors(run), ""]
        arrets = _table_stops(run)
        if arrets:
            lignes += ["### Raisons d'arrêt", "", *arrets, ""]
        niveaux = run.difficulties.get("adaptive_v2")
        if niveaux:
            lignes += [
                "*Difficulté estimée par V2 avant recherche* : "
                + ", ".join(f"{k} × {v}" for k, v in sorted(niveaux.items())) + ".",
                "",
            ]

    if result.verdict:
        lignes += [f"## {result.verdict.label}", ""]
        lignes += [
            f"- C1 (défaut corrigé) : {'vérifié' if result.verdict.c1 else 'NON vérifié'}",
            f"- C2 (économie conservée) : {'vérifié' if result.verdict.c2 else 'NON vérifié'}",
            f"- C3 (pas de régression) : {'vérifié' if result.verdict.c3 else 'NON vérifié'}",
            "",
        ]
        for reason in result.verdict.reasons:
            lignes.append(f"- {reason}")
        if result.verdict.warnings:
            lignes += ["", "**Réserves**", ""]
            for warning in result.verdict.warnings:
                lignes.append(f"- {warning}")
        lignes.append("")

    if result.explanation:
        lignes += ["## Analyse", ""]
        for paragraphe in result.explanation:
            lignes += [paragraphe, ""]

    lignes += [
        "## Ce que cette expérience ne prouve pas",
        "",
        "- Les trois jeux sont écrits par l'auteur du système. Séparation",
        "  développement / validation / test, **pas** réplication indépendante.",
        "- L'estimateur de difficulté est lexical. Il lit la grandeur demandée",
        "  et quelques mots ; il ne comprend pas le sujet.",
        "- Le classement des grandeurs par difficulté (`ASPECT_DIFFICULTY`) a",
        "  été formé en lisant les jeux 1 et 2. Il ne dépend d'aucune valeur",
        "  d'or, mais il n'est pas tombé du ciel non plus.",
        "- Rien ici ne dit ce que valent ces contrôleurs sur des questions",
        "  ouvertes, ni sur le vrai web.",
    ]
    return "\n".join(lignes)


__all__ = ["render"]
