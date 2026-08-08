"""Autopsie des erreurs de contextualisation.

Avant de corriger, comprendre. Ce module rejoue le diagnostic, isole les
exécutions rangées en CONTEXTUALISATION, et pour chacune reconstitue :

* quelle valeur piège a été présentée comme la réponse ;
* d'où elle venait — quelle page, quelle nature de piège ;
* quelle était la bonne valeur, et si elle était disponible ;
* ce que le piège avait de trompeur, tel que le jeu le déclare.

Rien n'est corrigé ici. Un diagnostic qui propose déjà son remède n'est plus
un diagnostic : c'est une justification.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

from ..core.config import Settings, get_settings
from .diagnostic import JEUX, _run_once
from .failures import diagnose
from .metrics import _matches, score
from .seeds import SEEDS, corpus_for, task_for


@dataclass
class Autopsy:
    """Une erreur de contextualisation, ouverte."""

    jeu: str
    task_id: str
    seed: int
    question: str
    gold: str
    presented: list[str] = field(default_factory=list)
    gold_available: bool = False
    sources: list[str] = field(default_factory=list)
    cause: str = ""

    def to_dict(self) -> dict:
        return {
            "jeu": self.jeu, "task": self.task_id, "seed": self.seed,
            "gold": self.gold, "presented": self.presented,
            "gold_available": self.gold_available, "sources": self.sources,
            "cause": self.cause,
        }


#: Ce que l'étiquette d'un piège révèle de sa nature. Les jeux nomment leurs
#: pièges en clair — « archive 2019 », « autre île », « girofle, autre
#: produit » — et c'est cette déclaration qui sert de vérité de référence.
CAUSE_KEYWORDS = {
    "archive": "temps — page ancienne prise pour l'actuelle",
    "2019": "temps — page ancienne prise pour l'actuelle",
    "2018": "temps — page ancienne prise pour l'actuelle",
    "2017": "temps — page ancienne prise pour l'actuelle",
    "2014": "temps — page ancienne prise pour l'actuelle",
    "autre île": "géographie — autre lieu que celui demandé",
    "autre ile": "géographie — autre lieu que celui demandé",
    "autre pays": "géographie — autre lieu que celui demandé",
    "delta": "géographie — autre lieu que celui demandé",
    "nord": "géographie — lieu au nom voisin",
    "autre produit": "objet — autre bien que celui demandé",
    "girofle": "objet — autre bien que celui demandé",
    "vanille": "objet — autre bien que celui demandé",
    "clinique": "objet — autre service que celui demandé",
    "dispensaire": "objet — autre service que celui demandé",
    "autre structure": "objet — autre service que celui demandé",
    "autre liaison": "objet — autre service que celui demandé",
}


def _cause(labels: list[str]) -> str:
    for label in labels:
        minuscule = label.lower()
        for indice, cause in CAUSE_KEYWORDS.items():
            if indice in minuscule:
                return cause
    return "non étiqueté — cause à établir à la main"


def run_autopsy(
    *, settings: Settings | None = None, seeds: tuple[int, ...] = SEEDS
) -> list[Autopsy]:
    """Rejoue le diagnostic et ouvre chaque erreur de contextualisation."""
    settings = replace(settings or get_settings(), search_delay=0.0)
    cas: list[Autopsy] = []

    for nom, taches, fabrique in JEUX:
        base = fabrique()
        for seed in seeds:
            web = corpus_for(base, seed)
            for task in taches:
                pose = task_for(task, seed)
                outcome = _run_once(pose, settings, web, seed)
                note = score(task, outcome)
                if diagnose(task, outcome, note).stage != "contextualisation":
                    continue

                faits_sources = []
                for index, doc in enumerate(outcome.sources, start=1):
                    from ..analysis.facts import extract_facts

                    for fait in extract_facts(
                        f"{doc.title} {doc.content}", index, max_facts=120
                    ):
                        faits_sources.append((doc.url, fait))

                pieges = [d for d in task.distractors if d.label in note.traps]
                origines = sorted({
                    url for url, fait in faits_sources
                    if any(_matches(fait, piege) for piege in pieges)
                })

                cas.append(
                    Autopsy(
                        jeu=nom, task_id=task.id, seed=seed,
                        question=pose.question,
                        gold=", ".join(g.label for g in task.gold),
                        presented=list(note.traps),
                        gold_available=any(
                            _matches(fait, g) for _u, fait in faits_sources
                            for g in task.gold
                        ),
                        sources=origines,
                        cause=_cause(list(note.traps)),
                    )
                )
    return cas


def summarize(cas: list[Autopsy]) -> dict[str, int]:
    compte: dict[str, int] = {}
    for cas_unique in cas:
        compte[cas_unique.cause] = compte.get(cas_unique.cause, 0) + 1
    return compte


__all__ = ["Autopsy", "CAUSE_KEYWORDS", "run_autopsy", "summarize"]
