"""Rapport de diagnostic : où l'information se perd."""

from __future__ import annotations

from .diagnostic import DiagnosticResult
from .failures import STAGE_LABELS, STAGE_MEANING, STAGES


def render(result: DiagnosticResult) -> str:
    total = result.total
    executions = sum(total.values()) or 1
    reussites = total.get("aucune", 0)

    lignes: list[str] = [
        "# Diagnostic — où l'agent perd l'information",
        "",
        "Ce document n'est pas une expérience : aucune hypothèse, aucun verdict,",
        "rien à réfuter. C'est un **état des lieux** de la configuration adoptée,",
        "destiné à dire où porter l'effort suivant.",
        "",
        f"**Contrôleur** : {result.controller} · **Moteur de recherche** : "
        f"{result.engine} · **{len(result.seeds)} graines**",
        "",
        "## Les six étapes",
        "",
        "| Étape | Ce qu'elle signifie |",
        "|---|---|",
    ]
    for stage in STAGES:
        lignes.append(f"| **{STAGE_LABELS[stage]}** | {STAGE_MEANING[stage]} |")

    lignes += [
        "",
        "L'attribution suit l'ordre du pipeline et s'arrête à la **première**",
        "étape fautive : une information jamais trouvée ne peut pas être mal",
        "extraite. Chaque règle est mécanique — on compare des ensembles de",
        "faits, jamais la qualité perçue d'une réponse.",
        "",
        "## Vue d'ensemble",
        "",
        f"{reussites} réponses correctes sur {executions} exécutions "
        f"({reussites / executions:.0%}).",
        "",
        "| Étape | Pannes | Part des pannes |",
        "|---|---|---|",
    ]

    pannes = executions - reussites
    for stage in STAGES:
        compte = total.get(stage, 0)
        if not compte:
            continue
        lignes.append(
            f"| {STAGE_LABELS[stage]} | {compte} | "
            f"{compte / pannes:.0%} |" if pannes else f"| {STAGE_LABELS[stage]} | {compte} | — |"
        )

    lignes += ["", "## Par jeu", "",
               "| Jeu | Exécutions | Correctes | "
               + " | ".join(STAGE_LABELS[s] for s in STAGES) + " |",
               "|---|---|---|" + "---|" * len(STAGES)]
    for jeu in result.datasets:
        lignes.append(
            f"| {jeu.name} | {jeu.runs} | {jeu.correct} | "
            + " | ".join(str(jeu.stages.get(s, 0)) for s in STAGES) + " |"
        )

    lignes += ["", "## Un exemple par panne", ""]
    vus: set[str] = set()
    for jeu in result.datasets:
        for stage, exemple in jeu.examples.items():
            if stage in vus:
                continue
            vus.add(stage)
            lignes.append(f"- **{STAGE_LABELS[stage]}** — {jeu.name} : {exemple}")
    lignes.append("")

    # Lecture : quelle étape domine ?
    if pannes:
        dominante = max(
            (s for s in STAGES if total.get(s)), key=lambda s: total[s], default=None
        )
        if dominante:
            part = total[dominante] / pannes
            lignes += [
                "## Lecture",
                "",
                f"La panne dominante est **{STAGE_LABELS[dominante]}** — "
                f"{STAGE_MEANING[dominante]} — avec {part:.0%} des échecs.",
                "",
            ]
            if dominante in {"raisonnement", "generation"}:
                lignes.append(
                    "C'est en aval de la recherche. Améliorer encore le moteur de "
                    "recherche ne changerait donc pas grand-chose : l'information "
                    "arrive, elle se perd au moment de rédiger. Avec le moteur "
                    "hors-ligne, la « rédaction » est une sélection de phrases — "
                    "c'est là qu'un vrai modèle de langage aurait le plus d'effet."
                )
            elif dominante == "recherche":
                lignes.append(
                    "L'information n'entre pas dans le pipeline. C'est le moteur "
                    "de recherche et la formulation des requêtes qu'il faut "
                    "travailler, pas la rédaction."
                )
            elif dominante == "extraction":
                lignes.append(
                    "L'information est là, écrite noir sur blanc, et l'extracteur "
                    "de faits ne la voit pas. C'est le module le moins coûteux à "
                    "améliorer : il est purement déterministe."
                )
            elif dominante == "contextualisation":
                lignes.append(
                    "Les valeurs trouvées viennent du mauvais lieu, de la mauvaise "
                    "date ou du mauvais contexte. C'est l'agent contexte qu'il "
                    "faut renforcer."
                )
            elif dominante == "comparaison":
                lignes.append(
                    "Les bonnes sources sont là mais ne sont pas confrontées : "
                    "c'est la détection de désaccords qui laisse passer."
                )

    lignes += [
        "",
        "## Ce que ce diagnostic ne dit pas",
        "",
        "- Il porte sur quatre corpus figés, écrits par l'auteur du système.",
        "  Une panne rare ici peut être fréquente sur le vrai web.",
        "- L'attribution est mécanique, donc parfois grossière : entre",
        "  RAISONNEMENT et GÉNÉRATION, la frontière tient à ce que la valeur",
        "  apparaisse ou non dans le bilan d'analyse.",
        "- Aucun verdict, aucune hypothèse : ce document ne remplace aucune des",
        "  expériences, et n'en révise aucune.",
    ]
    return "\n".join(lignes)


__all__ = ["render"]
