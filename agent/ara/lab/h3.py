"""H3 — la mémoire des défauts réduit-elle le travail de correction ?

Protocole intégral dans `docs/H3-APPRENTISSAGE.md`, écrit et commité avant
cette exécution. Ce module ne fait qu'appliquer ce qui y est décrit : deux
bras, dix briefs du JEU 10, cinq permutations pour le bras `AVEC`, et les
critères de décision tels qu'ils ont été fixés.

Rien ici ne doit être ajusté après avoir vu les nombres.
"""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field

from ..webapp.builder import apply_brand, spec_from_brief
from ..webapp.lessons import Lessons
from ..webapp.studio import SiteStudio
from .experiment import sign_test
from .webapp_test import CASES, WebCase

#: Graine des permutations, annoncée dans le pré-enregistrement.
SEED = 20260809

#: Nombre de permutations du bras `AVEC`.
PERMUTATIONS = 5

#: Marge de non-infériorité sur la note finale, en points.
MARGIN = 1.0

#: Nombre minimal de briefs devant montrer une baisse (7/10 → p ≤ 0,055).
MIN_WINS = 7


@dataclass
class Run:
    """Une exécution du studio sur un brief."""

    case: str
    corrections: int
    first_score: int
    final_score: int
    defects: list[str] = field(default_factory=list)
    blocking: list[str] = field(default_factory=list)
    prevented: int = 0

    def to_dict(self) -> dict:
        return {
            "case": self.case, "corrections": self.corrections,
            "first_score": self.first_score, "final_score": self.final_score,
            "defects": self.defects, "blocking": self.blocking,
            "prevented": self.prevented,
        }


@dataclass
class Arm:
    name: str
    runs: list[Run] = field(default_factory=list)

    def by_case(self) -> dict[str, list[Run]]:
        groupes: dict[str, list[Run]] = {}
        for run in self.runs:
            groupes.setdefault(run.case, []).append(run)
        return groupes

    def mean(self, field_name: str) -> float:
        """Moyenne par **brief**, pas par exécution.

        L'unité statistique est le brief : moyenner les exécutions ferait
        peser cinq fois plus les briefs vus dans cinq permutations, ce qui
        est de la pseudo-réplication.
        """
        par_cas = [
            statistics.fmean(getattr(run, field_name) for run in runs)
            for runs in self.by_case().values()
        ]
        return statistics.fmean(par_cas) if par_cas else 0.0

    def per_case(self, field_name: str) -> dict[str, float]:
        return {
            nom: statistics.fmean(getattr(run, field_name) for run in runs)
            for nom, runs in self.by_case().items()
        }


@dataclass
class H3Result:
    without: Arm
    with_memory: Arm
    wins: int = 0
    losses: int = 0
    ties: int = 0
    p_value: float = 1.0
    verdict: str = ""
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "sans": [r.to_dict() for r in self.without.runs],
            "avec": [r.to_dict() for r in self.with_memory.runs],
            "wins": self.wins, "losses": self.losses, "ties": self.ties,
            "p_value": round(self.p_value, 4),
            "verdict": self.verdict, "reasons": self.reasons,
        }


def _run_case(case: WebCase, lessons: Lessons, *, learn: bool) -> Run:
    spec = spec_from_brief(case.brief, kind=case.kind, material=list(case.material))
    apply_brand(spec, case.brand())
    resultat = SiteStudio(lessons, learn=learn).run(spec, task=case.id)
    premiere = resultat.versions[0]
    return Run(
        case=case.id,
        corrections=len(resultat.versions) - 1,
        first_score=premiere.score,
        final_score=resultat.score,
        defects=list(premiere.critique.defects),
        blocking=list(resultat.final.critique.blocking) if resultat.final else [],
        prevented=len(resultat.prevented),
    )


def run_h3(cases: list[WebCase] | None = None) -> H3Result:
    """Exécute les deux bras et applique les critères pré-enregistrés."""
    cases = list(cases or CASES)

    # --- Bras SANS : mémoire vide à chaque fois, rien n'est retenu.
    sans = Arm("sans mémoire")
    for case in cases:
        sans.runs.append(_run_case(case, Lessons(), learn=False))

    # --- Bras AVEC : une mémoire par permutation, qui se remplit.
    avec = Arm("avec mémoire")
    rng = random.Random(SEED)
    for _ in range(PERMUTATIONS):
        ordre = cases[:]
        rng.shuffle(ordre)
        memoire = Lessons()
        for case in ordre:
            avec.runs.append(_run_case(case, memoire, learn=True))

    resultat = H3Result(without=sans, with_memory=avec)

    corrections_sans = sans.per_case("corrections")
    corrections_avec = avec.per_case("corrections")
    for nom, valeur in corrections_sans.items():
        autre = corrections_avec.get(nom, valeur)
        if autre < valeur:
            resultat.wins += 1
        elif autre > valeur:
            resultat.losses += 1
        else:
            resultat.ties += 1
    resultat.p_value = sign_test(resultat.wins, resultat.losses)

    moyenne_sans = sans.mean("corrections")
    moyenne_avec = avec.mean("corrections")
    note_sans = sans.mean("final_score")
    note_avec = avec.mean("final_score")

    baisse = moyenne_avec < moyenne_sans
    tient = resultat.wins >= MIN_WINS
    non_inferieure = note_avec >= note_sans - MARGIN

    if baisse and tient and non_inferieure:
        resultat.verdict = "H3 SOUTENUE"
    elif baisse and (note_avec >= note_sans - 3.0):
        resultat.verdict = "H3 PARTIELLEMENT SOUTENUE"
    else:
        resultat.verdict = "H3 RÉFUTÉE"

    resultat.reasons = [
        f"corrections moyennes : {moyenne_sans:.2f} sans mémoire → "
        f"{moyenne_avec:.2f} avec ({'baisse' if baisse else 'pas de baisse'})",
        f"briefs en baisse : {resultat.wins}/{len(cases)} "
        f"(seuil pré-enregistré : {MIN_WINS}) · p = {resultat.p_value:.4f}",
        f"note finale moyenne : {note_sans:.1f} → {note_avec:.1f} "
        f"({'non-infériorité respectée' if non_inferieure else 'marge dépassée'})",
    ]
    return resultat


__all__ = ["Arm", "H3Result", "MARGIN", "MIN_WINS", "PERMUTATIONS", "Run",
           "SEED", "run_h3"]
