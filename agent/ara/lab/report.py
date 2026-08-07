"""Rapport d'expérience (spec §18).

Un rapport de laboratoire doit permettre à quelqu'un d'autre de **contredire**
la conclusion. Il donne donc, dans cet ordre : l'hypothèse pré-enregistrée et
ses conditions de réfutation, le protocole, les résultats bruts par tâche, puis
seulement le verdict — assorti de ce qu'il ne prouve pas.
"""

from __future__ import annotations

from . import strategies as arms
from .experiment import COST_HYPOTHESIS_NOTE, ExperimentResult


def render(result: ExperimentResult) -> str:
    hypothesis = result.hypothesis
    comparison = result.comparison
    verdict = result.verdict
    lines: list[str] = []

    lines += [
        "# RESEARCH LAB — raisonnement adaptatif",
        "",
        "## Hypothèse pré-enregistrée",
        "",
        f"> {hypothesis.statement}",
        "",
        "Conditions de réfutation, **écrites avant l'expérience** :",
        "",
        f"- gain d'exactitude nette < {hypothesis.min_gain:+.2f} → réfutée ;",
        f"- coût > {hypothesis.max_cost_ratio:.1f}× la référence → réfutée ;",
        "- dégradation sur les tâches pièges → réfutée ;",
        f"- p > {hypothesis.alpha} au test des signes → non concluant.",
        "",
        "### Seconde hypothèse, sur le coût",
        "",
        f"> {COST_HYPOTHESIS_NOTE}",
        "",
        "## Protocole",
        "",
        "- Corpus **figé**, identique pour toutes les stratégies et toutes les",
        "  exécutions. Les comparaisons sont appariées : même tâche, même web.",
        "- Seule la **décision de chercher** change d'une stratégie à l'autre ;",
        "  le moteur de synthèse est le même partout.",
        "- L'exactitude est mesurée par extraction de faits contre une vérité de",
        "  référence chiffrée — aucun jugement humain dans la boucle.",
        "- Le jeu contient des **tâches pièges**, conçues pour faire perdre la",
        "  stratégie adaptative.",
        "",
        "## Résultats par stratégie",
        "",
        "| Stratégie | Exactitude | Bruit | Nette | Qualité | Recherches | Pages | Jetons | Temps |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for strategy in arms.STRATEGIES:
        s = result.summary(strategy)
        if not s:
            continue
        lines.append(
            f"| {s['label']} | {s['accuracy']:.2f} | {s['noise']:.2f} | "
            f"**{s['net']:.2f}** | {s['quality']:.2f} | {s['searches']:.1f} | "
            f"{s['fetches']:.1f} | {s['tokens']} | {s['latency_ms']} ms |"
        )

    lines += [
        "",
        "*Bruit* : valeurs pièges présentées comme la réponse. *Nette* = "
        "exactitude − ½ bruit. *Jetons* : volume de texte traversé, en unités de "
        "4 caractères — un indicateur de calcul comparable, pas une facture.",
        "",
    ]

    if comparison:
        lines += [
            f"## Confrontation appariée — {arms.LABELS[comparison.challenger]} "
            f"contre {arms.LABELS[comparison.reference]}",
            "",
            f"- **{comparison.wins} victoires**, {comparison.losses} défaites, "
            f"{comparison.ties} égalités sur {comparison.wins + comparison.losses + comparison.ties} tâches",
            f"- Gain moyen d'exactitude nette : **{comparison.mean_gain:+.3f}** "
            f"(IC95 par ré-échantillonnage : [{comparison.ci[0]:+.3f}, {comparison.ci[1]:+.3f}])",
            f"- Test des signes (binomiale exacte) : **p = {comparison.p_value:.3f}**",
            f"- Coût relatif : **{comparison.cost_ratio:.2f}×**",
            f"- Sur les tâches pièges seules : {comparison.trap_gain:+.3f}",
            "",
        ]

    if result.cost_verdict:
        cv = result.cost_verdict
        lines += [
            f"## {cv.label}", "",
            f"- ADAPTIVE REASONING contre FIXED REASONING : {cv.reason}",
            f"- Écart d'exactitude nette : {cv.accuracy_delta:+.3f} · "
            f"recherches : {cv.search_ratio:.2f}× la référence",
            "",
        ]

    lines += ["## Résultats par tâche", "",
              "| Tâche | Famille | " + " | ".join(arms.LABELS[s] for s in arms.STRATEGIES) + " |",
              "|---|---|" + "---|" * len(arms.STRATEGIES)]

    par_tache: dict[str, dict] = {}
    familles: dict[str, str] = {}
    for row in result.rows:
        par_tache.setdefault(row.task.id, {})[row.outcome.strategy] = row
        familles[row.task.id] = row.task.family

    for task_id, rows in par_tache.items():
        cellules = []
        for strategy in arms.STRATEGIES:
            row = rows.get(strategy)
            if row is None:
                cellules.append("—")
                continue
            marque = "✓" if row.score.net >= 0.99 else ("~" if row.score.net > 0 else "✗")
            detail = f" ({row.outcome.searches}r)" if row.outcome.searches else ""
            cellules.append(f"{marque} {row.score.net:.2f}{detail}")
        lines.append(f"| `{task_id}` | {familles[task_id]} | " + " | ".join(cellules) + " |")

    lines += ["", "`r` = recherches lancées.", ""]

    if verdict:
        lines += [f"## {verdict.label}", ""]
        for reason in verdict.reasons:
            lines.append(f"- {reason}")
        if verdict.warnings:
            lines += ["", "**Réserves**", ""]
            for warning in verdict.warnings:
                lines.append(f"- {warning}")

    lines += [
        "",
        "## Ce que cette expérience ne prouve pas",
        "",
        "- Le corpus est petit et construit à la main. Il peut **réfuter** une",
        "  hypothèse ; il ne peut pas établir une loi générale.",
        "- La synthèse est extractive (moteur hors-ligne). Avec un vrai modèle,",
        "  l'écart entre stratégies peut se réduire — un bon modèle rattrape une",
        "  partie d'une recherche médiocre — ou se creuser.",
        "- Le coût est mesuré en volume de texte traversé, pas en facture réelle.",
        "- Les tâches sont chiffrées, donc vérifiables. Rien ici ne dit ce que",
        "  vaut la stratégie sur des questions ouvertes.",
    ]
    return "\n".join(lines)
