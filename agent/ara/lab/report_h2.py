"""Rapport de l'expérience H2.

Ordre imposé : l'hypothèse et ses critères d'abord, les mesures ensuite, le
verdict en dernier. Un rapport qui commence par sa conclusion invite à lire
les chiffres comme des illustrations ; ici, ils doivent pouvoir la contredire.
"""

from __future__ import annotations

from . import strategies as arms
from .h2 import (
    ALPHA,
    H2_STATEMENT,
    MARGE_EXACTITUDE,
    PRIX_PAR_MILLION_JETONS,
    REDUCTION_MINIMALE,
    DatasetRun,
    H2Result,
    PairedResult,
)
from .stops import ERROR_LABELS, ERROR_ORDER, STOP_LABELS, STOP_ORDER


def _table_arms(run: DatasetRun) -> list[str]:
    lignes = [
        "| Stratégie | Exactitude | Bruit | Nette | Recherches | Pages | Appels LLM | Jetons | Latence | Coût est. | Rech./réponse juste |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for strategy in arms.STRATEGIES:
        s = run.stats.get(strategy)
        if not s:
            continue
        rpc = (
            f"{s.searches_per_correct:.2f}"
            if s.searches_per_correct != float("inf") else "—"
        )
        lignes.append(
            f"| {s.label} | {s.accuracy:.2f} | {s.noise:.2f} | **{s.net:.2f}** | "
            f"{s.searches:.2f} | {s.fetches:.2f} | {s.llm_calls:.2f} | "
            f"{s.tokens:.0f} | {s.latency_ms:.0f} ms | {s.cost:.6f} | {rpc} |"
        )
    return lignes


def _table_stops(run: DatasetRun) -> list[str]:
    codes = [c for c in (*STOP_ORDER, "passe_unique")
             if any(c in run.stops.get(s, {}) for s in arms.STRATEGIES)]
    lignes = [
        "| Stratégie | " + " | ".join(STOP_LABELS[c] for c in codes) + " |",
        "|---|" + "---|" * len(codes),
    ]
    for strategy in arms.STRATEGIES:
        compte = run.stops.get(strategy, {})
        lignes.append(
            f"| {arms.LABELS[strategy]} | "
            + " | ".join(str(compte.get(c, 0)) for c in codes) + " |"
        )
    return lignes


def _table_errors(run: DatasetRun) -> list[str]:
    lignes = [
        "| Stratégie | " + " | ".join(ERROR_LABELS[e] for e in ERROR_ORDER)
        + " | recherches gaspillées |",
        "|---|" + "---|" * (len(ERROR_ORDER) + 1),
    ]
    for strategy in arms.STRATEGIES:
        fautes = run.errors.get(strategy, {})
        lignes.append(
            f"| {arms.LABELS[strategy]} | "
            + " | ".join(str(fautes.get(e, 0)) for e in ERROR_ORDER)
            + f" | {run.wasted.get(strategy, 0)} |"
        )
    return lignes


def _paired_block(comparison: PairedResult, titre: str) -> list[str]:
    return [
        f"**{titre}** (unité : {comparison.unit}, n = {comparison.n})",
        "",
        f"- Recherches : **{'−' if comparison.reduction >= 0 else '+'}"
        f"{abs(comparison.reduction):.0%}** "
        f"({comparison.search_ratio:.2f}× la référence, écart moyen "
        f"{comparison.search_delta:+.2f} par tâche, IC95 "
        f"[{comparison.search_ci[0]:+.2f}, {comparison.search_ci[1]:+.2f}])",
        f"- Exactitude nette : écart {comparison.accuracy_delta:+.3f} "
        f"(IC95 [{comparison.accuracy_ci[0]:+.3f}, {comparison.accuracy_ci[1]:+.3f}])",
        f"- Test des signes : {comparison.wins} tâches moins chères, "
        f"{comparison.losses} plus chères, {comparison.ties} égales — "
        f"**p = {comparison.p_value:.3f}**",
        "",
    ]


def render(result: H2Result) -> str:
    lignes: list[str] = [
        "# H2 — le contrôleur adaptatif économise-t-il des recherches ?",
        "",
        "## Ce que ce rapport ne fait pas",
        "",
        "H1 reste **NON CONCLUANTE**. Rien ici ne la révise, ne la reformule ni",
        "ne la transforme en succès : ses résultats bruts sont conservés tels",
        "quels dans `lab-report.md`. H2 est une hypothèse **différente**, portant",
        "sur le coût et non sur l'exactitude.",
        "",
        "## Hypothèse pré-enregistrée",
        "",
        f"> {H2_STATEMENT}",
        "",
        "### Critères de succès et d'échec, écrits avant l'expérience",
        "",
        f"- **Critère A — exactitude comparable** : borne basse de l'IC95 de "
        f"l'écart d'exactitude nette ≥ −{MARGE_EXACTITUDE:.2f} (test de "
        "non-infériorité).",
        f"- **Critère B — réduction significative** : réduction moyenne des "
        f"recherches ≥ {REDUCTION_MINIMALE:.0%} **et** p < {ALPHA} au test des "
        "signes apparié.",
        "",
        "| Verdict | Condition |",
        "|---|---|",
        "| **H2 SOUTENUE** | A et B vérifiés sur le jeu de test tenu à l'écart |",
        "| **H2 PARTIELLEMENT SOUTENUE** | B vérifié sans A, ou B vérifié sur la calibration seulement |",
        "| **H2 RÉFUTÉE** | B non vérifié : pas de réduction, sous le seuil, ou non significative |",
        "",
        "## Protocole",
        "",
        "- **Deux jeux séparés.** Le jeu de la Phase 4 sert de *calibration* — il",
        "  est brûlé, le système ayant été corrigé après l'avoir vu. Un second",
        "  jeu, d'un autre domaine (coopérative agricole), sert de **test** et",
        "  n'a servi à aucun réglage.",
        f"- **{len(result.seeds)} graines** ({', '.join(str(s) for s in result.seeds)}).",
        "  Une graine change la **formulation** de la question et l'**ordre** des",
        "  résultats de recherche. Elle ne change jamais les pages, les chiffres",
        "  ni la vérité de référence.",
        "- **Unité statistique : la tâche.** Les graines d'une même tâche sont",
        "  moyennées avant comparaison — les compter séparément gonflerait",
        "  l'effectif sans ajouter de preuve (pseudo-réplication). L'analyse par",
        "  couple tâche×graine est donnée à part, à titre indicatif.",
        "- **Contrôleur gelé** avant la première exécution sur le jeu de test, et",
        "  non retouché ensuite.",
        f"- **Coût estimé** à {PRIX_PAR_MILLION_JETONS:.2f} par million de jetons —",
        "  ordre de grandeur d'un modèle payant courant. Le coût réel de cette",
        "  expérience est **nul** : le moteur est hors-ligne.",
        "",
    ]

    for run in (result.test, result.calibration):
        if run is None:
            continue
        titre = "Jeu de test tenu à l'écart" if run.name.startswith("test") else "Jeu de calibration"
        lignes += [f"## {titre}", "", *_table_arms(run), ""]
        if run.paired_task:
            lignes += _paired_block(
                run.paired_task, "ADAPTIVE REASONING contre FIXED REASONING"
            )
        if run.paired_seed:
            lignes += [
                f"*Analyse secondaire par couple tâche×graine (n = "
                f"{run.paired_seed.n}, pseudo-réplication)* : "
                f"{abs(run.paired_seed.reduction):.0%} de recherches "
                f"{'en moins' if run.paired_seed.reduction >= 0 else 'en plus'}, "
                f"p = {run.paired_seed.p_value:.3f}.",
                "",
            ]
        lignes += ["### Raisons d'arrêt", "", *_table_stops(run), ""]
        lignes += ["### Erreurs relevées après coup", "", *_table_errors(run), ""]

    if result.verdict:
        lignes += [f"## {result.verdict.label}", ""]
        lignes += [
            f"- Critère A (exactitude comparable) : "
            f"{'vérifié' if result.verdict.criterion_a else 'NON vérifié'}",
            f"- Critère B (réduction significative) : "
            f"{'vérifié' if result.verdict.criterion_b else 'NON vérifié'}",
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
        lignes += ["## Pourquoi ADAPTIVE cherche moins", ""]
        for paragraphe in result.explanation:
            lignes += [paragraphe, ""]

    lignes += [
        "## Ce que cette expérience ne prouve pas",
        "",
        "- Le jeu de test est écrit par l'auteur du système. C'est une",
        "  séparation calibration / test, **pas** une réplication indépendante.",
        "- Les graines font varier la formulation et le classement, pas le",
        "  contenu du web. La robustesse mesurée est donc étroite.",
        "- L'exactitude est mesurée sur des grandeurs chiffrées. Rien ici ne dit",
        "  ce que valent ces stratégies sur des questions ouvertes.",
        "- Le coût est estimé en jetons traversés. Avec un vrai modèle, le",
        "  rapport entre stratégies peut changer.",
        "- Une réduction de recherches n'est un gain que si les recherches",
        "  coûtent. Sur un moteur gratuit et rapide, l'économie est théorique.",
    ]
    return "\n".join(lignes)


__all__ = ["render"]
