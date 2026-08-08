"""Effet de bout en bout : que se passerait-il si le contrôle était branché ?

Les jeux 7 et 8 mesurent le mécanisme sur des phrases écrites pour lui. Cette
mesure-ci est différente et complète les autres : elle prend les **vraies**
exécutions de l'agent sur les jeux 1 à 4, et pose deux questions simples.

1. Sur les seize erreurs de contextualisation, combien de valeurs pièges
   auraient été **bloquées** avant d'être affirmées ?
2. Sur les réponses **correctes**, combien de bonnes valeurs auraient été
   bloquées à tort ?

La seconde question est la plus importante. Un filtre qui bloque tout obtient
un score parfait à la première et détruit le système.

⚠️ Biais à connaître, et il est sérieux : l'autopsie qui a guidé CONTEXT-V2 et
V3 a été faite **sur ces exécutions-là**. Les pièges des jeux 1 à 4 ont donc
servi au développement. Ce que cette mesure établit, c'est un ordre de
grandeur de l'effet en production — pas une validation. Les jeux 7 et 8, eux,
étaient indépendants.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from ..analysis.facts import extract_facts
from ..core.config import Settings, get_settings
from .diagnostic import JEUX, _run_once
from .failures import diagnose
from .metrics import _matches, score
from .seeds import SEEDS, corpus_for, task_for

VERSIONS = ("v2", "v3")


@dataclass
class Impact:
    version: str
    traps_blocked: int = 0
    traps_seen: int = 0
    good_blocked: int = 0
    good_seen: int = 0
    details: list[str] = field(default_factory=list)

    @property
    def trap_block_rate(self) -> float:
        return self.traps_blocked / self.traps_seen if self.traps_seen else 0.0

    @property
    def false_block_rate(self) -> float:
        return self.good_blocked / self.good_seen if self.good_seen else 0.0

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "traps_blocked": self.traps_blocked, "traps_seen": self.traps_seen,
            "trap_block_rate": round(self.trap_block_rate, 3),
            "good_blocked": self.good_blocked, "good_seen": self.good_seen,
            "false_block_rate": round(self.false_block_rate, 3),
            "details": self.details,
        }


def _checker(version: str):
    if version == "v2":
        from ..analysis.context_v2 import assess_context
    else:
        from ..analysis.context_v3 import assess_context
    return assess_context


def _facts_with_sources(outcome):
    """(fait, titre, texte de la source) pour chaque fait des sources retenues."""
    sortie = []
    for index, doc in enumerate(outcome.sources, start=1):
        texte = f"{doc.title} {doc.content}"
        for fait in extract_facts(texte, index, max_facts=120):
            sortie.append((fait, doc.title, texte))
    return sortie


def run_impact(
    *, settings: Settings | None = None, seeds: tuple[int, ...] = SEEDS
) -> dict[str, Impact]:
    """Rejoue les jeux 1 à 4 et confronte chaque version au réel."""
    settings = replace(settings or get_settings(), search_delay=0.0)
    resultats = {version: Impact(version=version) for version in VERSIONS}

    for _nom, taches, fabrique in JEUX:
        base = fabrique()
        for seed in seeds:
            web = corpus_for(base, seed)
            for task in taches:
                pose = task_for(task, seed)
                outcome = _run_once(pose, settings, web, seed)
                note = score(task, outcome)
                etape = diagnose(task, outcome, note).stage
                faits = _facts_with_sources(outcome)

                # Les valeurs pièges effectivement présentées comme réponse.
                pieges = [d for d in task.distractors if d.label in note.traps]
                # Les bonnes valeurs effectivement trouvées et affichées.
                bonnes = [g for g in task.gold if g.label in note.found]

                for version in VERSIONS:
                    verifie = _checker(version)
                    impact = resultats[version]

                    if etape == "contextualisation":
                        for piege in pieges:
                            porteurs = [
                                (f, t, d) for f, t, d in faits if _matches(f, piege)
                            ]
                            if not porteurs:
                                continue
                            impact.traps_seen += 1
                            bloque = all(
                                not verifie(
                                    question=pose.question, sentence=f.sentence,
                                    document=d, title=t,
                                ).assertable
                                for f, t, d in porteurs
                            )
                            if bloque:
                                impact.traps_blocked += 1
                            else:
                                impact.details.append(
                                    f"{task.id}/{seed} : piège « {piege.label} » "
                                    "resterait affirmable"
                                )

                    for bonne in bonnes:
                        porteurs = [
                            (f, t, d) for f, t, d in faits if _matches(f, bonne)
                        ]
                        if not porteurs:
                            continue
                        impact.good_seen += 1
                        passe = any(
                            verifie(
                                question=pose.question, sentence=f.sentence,
                                document=d, title=t,
                            ).assertable
                            for f, t, d in porteurs
                        )
                        if not passe:
                            impact.good_blocked += 1
                            impact.details.append(
                                f"{task.id}/{seed} : bonne valeur "
                                f"« {bonne.label} » serait bloquée"
                            )

    return resultats


__all__ = ["Impact", "VERSIONS", "run_impact"]
