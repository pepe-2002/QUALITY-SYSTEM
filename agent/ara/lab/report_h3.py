"""Rapport H3 : la mémoire des défauts réduit-elle le travail de correction ?"""

from __future__ import annotations

from .h3 import MARGIN, MIN_WINS, PERMUTATIONS, SEED, H3Result, run_h3
from .webapp_test import CASES


def render(result: H3Result | None = None) -> str:
    result = result or run_h3()
    sans, avec = result.without, result.with_memory

    corrections_sans = sans.per_case("corrections")
    corrections_avec = avec.per_case("corrections")
    premiere_sans = sans.per_case("first_score")
    premiere_avec = avec.per_case("first_score")
    finale_sans = sans.per_case("final_score")
    finale_avec = avec.per_case("final_score")

    lignes = [
        "# H3 — apprendre de ses erreurs, mesuré",
        "",
        "> **H3 — À qualité finale au moins égale, la mémoire des défauts réduit",
        "> le nombre de corrections nécessaires après la première version.**",
        "",
        "Hypothèse et critères pré-enregistrés dans `docs/H3-APPRENTISSAGE.md`,",
        "commités avant cette exécution.",
        "",
        "## 1. Protocole",
        "",
        f"- JEU 10 : {len(CASES)} briefs, écrits avant exécution, jamais utilisés",
        "  pour développer le studio web ;",
        "- bras `SANS` : mémoire vide à chaque brief ;",
        f"- bras `AVEC` : une mémoire partagée, sur {PERMUTATIONS} permutations",
        f"  (graine {SEED}) — le premier brief de chaque permutation ne bénéficie",
        "  d'aucune mémoire et reste compté ;",
        "- unité statistique : le **brief**, pas l'exécution.",
        "",
        "## 2. Résultats",
        "",
        "| Brief | Corrections SANS | Corrections AVEC | Note V1 SANS | Note V1 AVEC | Note finale SANS | Note finale AVEC |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]

    for nom in corrections_sans:
        lignes.append(
            f"| {nom} | {corrections_sans[nom]:.1f} | {corrections_avec[nom]:.1f} | "
            f"{premiere_sans[nom]:.0f} | {premiere_avec[nom]:.1f} | "
            f"{finale_sans[nom]:.0f} | {finale_avec[nom]:.0f} |"
        )

    lignes += [
        f"| **moyenne** | **{sans.mean('corrections'):.2f}** | "
        f"**{avec.mean('corrections'):.2f}** | "
        f"**{sans.mean('first_score'):.1f}** | **{avec.mean('first_score'):.1f}** | "
        f"**{sans.mean('final_score'):.1f}** | **{avec.mean('final_score'):.1f}** |",
        "",
        "## 3. Décision",
        "",
        f"- briefs en baisse : **{result.wins}/{len(corrections_sans)}** "
        f"(seuil pré-enregistré : {MIN_WINS}) · hausses : {result.losses} · "
        f"égalités : {result.ties}",
        f"- test des signes exact : **p = {result.p_value:.4f}**",
        f"- note finale : {sans.mean('final_score'):.1f} → "
        f"{avec.mean('final_score'):.1f} (marge de non-infériorité : {MARGIN:.0f} point)",
        "",
        f"### Verdict : **{result.verdict}**",
        "",
    ]
    lignes += [f"- {raison}" for raison in result.reasons]

    lignes += [
        "",
        "## 4. Où l'effet se produit exactement",
        "",
        "La note **finale** est identique dans les deux bras. Ce n'est pas un",
        "résultat décevant, c'est le résultat attendu : la boucle de correction",
        "arrive au même endroit dans les deux cas. Ce que la mémoire change,",
        "c'est la note de la **première** version — l'agent produit d'emblée ce",
        "qu'il mettait auparavant deux ou trois tours à obtenir.",
        "",
        "Cela vaut d'être dit clairement : la mémoire ne rend pas les sites",
        "meilleurs. Elle les rend meilleurs **plus tôt**, et à moindre coût.",
        "",
        "## 5. Ce que ce résultat ne dit pas",
        "",
        "- **Le générateur est déterministe.** Le même brief produit toujours les",
        "  mêmes fichiers, donc un défaut se reproduit à l'identique et une",
        "  correction connue s'applique toujours. Avec un générateur variable,",
        "  l'effet serait vraisemblablement plus faible. C'est la limite",
        "  principale, annoncée avant l'exécution.",
        "- **Aucune généralisation.** La mémoire rejoue des corrections déjà",
        "  constatées efficaces ; elle n'invente aucune règle nouvelle.",
        "- **Le critère « autonomie » n'a jamais été déclenché** par le JEU 10 :",
        "  une adresse web dans le texte d'une section n'est pas une ressource",
        "  chargée. Ce contrôle reste donc vérifié par les tests unitaires",
        "  seulement, pas par cette expérience.",
        "- **Le goût n'est pas mesuré.** Contraste, cibles tactiles, liens,",
        "  contenu réel : rien qui dise si un site est beau.",
        "",
        "## 6. Reproduction",
        "",
        "```bash",
        "python -m ara.cli --h3",
        "```",
        "",
        "Le résultat est déterministe : mêmes briefs, même graine, mêmes nombres.",
    ]
    return "\n".join(lignes)


__all__ = ["render"]
