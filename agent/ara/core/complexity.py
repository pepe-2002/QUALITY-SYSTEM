"""Contrôleur TASK_COMPLEXITY (spec §4).

L'agent ne doit pas dépenser la même quantité de calcul pour « quelle heure
est-il ? » et pour « compare les horaires de trois compagnies et fais-moi un
PDF ». Ce module estime la complexité **avant** d'engager des ressources, puis
alloue un budget d'étapes.

Statut scientifique — à lire avant d'en tirer des conclusions
------------------------------------------------------------
Cette V0 est une **heuristique lexicale**, pas un modèle appris. Elle est
volontairement simple, déterministe et lisible pour servir de *baseline* au
RESEARCH LAB (spec §18), dont le rôle sera de tenter de la **réfuter** :

* si `ADAPTIVE REASONING` ne bat pas `FIXED REASONING` en qualité à coût égal,
  l'hypothèse est fausse et ce contrôleur doit être jeté, pas ajusté ;
* les seuils ci-dessous n'ont **aucune** validation empirique à ce jour.

Le budget peut être révisé **en cours de tâche** (`escalate` / `de_escalate`) :
la spec exige que le système sache augmenter ou diminuer le nombre d'étapes.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from enum import Enum


class Complexity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


#: Budgets par niveau : (étapes de recherche, passes d'analyse)
BUDGETS: dict[Complexity, tuple[int, int]] = {
    Complexity.LOW: (1, 1),
    Complexity.MEDIUM: (3, 2),
    Complexity.HIGH: (6, 3),
}

# --- Signaux lexicaux (français + anglais, sans accents après normalisation) ---

_RESEARCH_WORDS = {
    "recherche", "cherche", "chercher", "trouve", "trouver", "actualite",
    "actualites", "horaire", "horaires", "prix", "tarif", "tarifs", "meteo",
    "source", "sources", "qui est", "combien", "quand", "ou est", "search",
    "find", "latest", "news", "documente", "documenter", "verifie", "verifier",
}

_COMPARE_WORDS = {
    "compare", "comparer", "comparaison", "versus", "vs", "difference",
    "differences", "meilleur", "meilleure", "avantages", "inconvenients",
    "pour et contre", "analyse", "analyser", "evalue", "evaluer", "synthese",
    "benchmark", "compare",
}

_DELIVERABLE_WORDS = {
    "pdf", "docx", "word", "document", "rapport", "dossier", "flyer",
    "affiche", "presentation", "note", "memo", "fiche", "tableau", "md",
    "markdown", "txt", "fichier",
}

_TRIVIAL_WORDS = {
    "bonjour", "salut", "merci", "ok", "test", "coucou", "hello", "hi",
    "ca va", "comment vas tu",
}


def _normalize(text: str) -> str:
    """Minuscule, sans accents, ponctuation réduite à des espaces."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _count_hits(haystack: str, needles: set[str]) -> int:
    """Nombre de termes du lexique présents (mots entiers ou expressions)."""
    padded = f" {haystack} "
    return sum(1 for needle in needles if f" {needle} " in padded)


@dataclass
class TaskBudget:
    """Décision du contrôleur pour une tâche donnée."""

    complexity: Complexity
    search_steps: int
    analysis_passes: int
    signals: dict[str, int]
    max_search_steps: int = 10

    #: nombre de recherches réellement consommées
    used_searches: int = 0

    @property
    def remaining_searches(self) -> int:
        return max(0, min(self.search_steps, self.max_search_steps) - self.used_searches)

    def consume_search(self) -> None:
        self.used_searches += 1

    def escalate(self, reason: str = "") -> bool:
        """Augmente le budget d'un cran. Retourne False si déjà au maximum.

        Appelé quand l'analyse détecte un manque d'information ou une
        contradiction (spec §3).
        """
        if self.complexity is Complexity.HIGH:
            # déjà au maximum : on peut encore élargir jusqu'au plafond dur
            if self.search_steps >= self.max_search_steps:
                return False
            self.search_steps = min(self.search_steps + 1, self.max_search_steps)
            return True
        order = [Complexity.LOW, Complexity.MEDIUM, Complexity.HIGH]
        self.complexity = order[order.index(self.complexity) + 1]
        steps, passes = BUDGETS[self.complexity]
        self.search_steps = min(max(self.search_steps, steps), self.max_search_steps)
        self.analysis_passes = max(self.analysis_passes, passes)
        return True

    def de_escalate(self, reason: str = "") -> bool:
        """Réduit le budget d'un cran (tâche plus simple que prévu)."""
        order = [Complexity.LOW, Complexity.MEDIUM, Complexity.HIGH]
        index = order.index(self.complexity)
        if index == 0:
            return False
        self.complexity = order[index - 1]
        steps, passes = BUDGETS[self.complexity]
        self.search_steps = max(self.used_searches, min(self.search_steps, steps))
        self.analysis_passes = min(self.analysis_passes, passes)
        return True

    def to_dict(self) -> dict[str, object]:
        return {
            "complexity": self.complexity.value,
            "search_steps": self.search_steps,
            "analysis_passes": self.analysis_passes,
            "used_searches": self.used_searches,
            "signals": self.signals,
        }


def assess(prompt: str, *, max_search_steps: int = 10) -> TaskBudget:
    """Estime la complexité d'une tâche et alloue son budget.

    >>> assess("bonjour").complexity
    <Complexity.LOW: 'LOW'>
    >>> assess("compare les horaires des 3 compagnies et fais un PDF").complexity
    <Complexity.HIGH: 'HIGH'>
    """
    text = _normalize(prompt)
    words = text.split()

    signals = {
        "length": len(words),
        "research": _count_hits(text, _RESEARCH_WORDS),
        "compare": _count_hits(text, _COMPARE_WORDS),
        "deliverable": _count_hits(text, _DELIVERABLE_WORDS),
        "questions": prompt.count("?"),
        "conjunctions": len(re.findall(r"\b(et|puis|ensuite|and|then)\b", text)),
    }

    # Salutation seule → toujours LOW, quel que soit le reste du score.
    if len(words) <= 4 and _count_hits(text, _TRIVIAL_WORDS):
        score = 0
    else:
        score = (
            signals["research"] * 2
            + signals["compare"] * 3
            + signals["deliverable"] * 2
            + min(signals["conjunctions"], 3)
            + (2 if signals["length"] > 25 else 1 if signals["length"] > 12 else 0)
        )

    if score >= 7:
        complexity = Complexity.HIGH
    elif score >= 3:
        complexity = Complexity.MEDIUM
    else:
        complexity = Complexity.LOW

    steps, passes = BUDGETS[complexity]
    signals["score"] = score
    return TaskBudget(
        complexity=complexity,
        search_steps=min(steps, max_search_steps),
        analysis_passes=passes,
        signals=signals,
        max_search_steps=max_search_steps,
    )
