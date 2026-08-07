"""Répétitions : faire varier l'expérience sans changer les faits.

Une expérience jouée une seule fois ne dit rien de sa propre stabilité. Mais
sur un corpus figé, tout est déterministe : rejouer donne exactement le même
chiffre. Il faut donc introduire une variation **contrôlée**, et dire
précisément ce qu'elle touche.

Ce qu'une graine fait varier :

1. **la formulation de la question** — chaque tâche a plusieurs reformulations
   équivalentes ; la graine en choisit une ;
2. **l'ordre des résultats de recherche** — un vrai moteur ne classe pas deux
   fois pareil ; les pages retournées sont les mêmes, leur ordre change.

Ce qu'une graine ne touche **jamais** : les pages, les chiffres, la vérité de
référence. Une graine ne rend donc pas une tâche plus facile ou plus difficile
— elle mesure la sensibilité d'une stratégie à des détails qui ne devraient
pas compter.
"""

from __future__ import annotations

import random
from dataclasses import replace

from .corpus import Corpus
from .dataset import Task

#: Graines de l'expérience. Fixées ici, donc rejouables à l'identique.
SEEDS: tuple[int, ...] = (1, 2, 3, 4, 5)


def question_for(task: Task, seed: int) -> str:
    """Formulation de la tâche pour cette graine."""
    variantes = task.variants()
    return variantes[seed % len(variantes)]


def task_for(task: Task, seed: int) -> Task:
    """La même tâche, posée autrement. Vérité de référence inchangée."""
    return replace(task, question=question_for(task, seed))


class ShuffledCorpus(Corpus):
    """Le même web, dont les résultats de recherche arrivent dans un autre ordre.

    Le mélange est **borné** : on ne fait que permuter les résultats d'une même
    requête. Aucune page n'apparaît ni ne disparaît — sinon la graine changerait
    la difficulté de la tâche, et l'on ne mesurerait plus la stratégie.
    """

    def __init__(self, base: Corpus, seed: int) -> None:
        super().__init__(pages=dict(base.pages), index=dict(base.index))
        self.seed = seed

    def search(self, query: str, limit: int = 6) -> list[str]:
        urls = super().search(query, limit)
        if self.seed == 0 or len(urls) < 2:
            return urls
        # La graine et la requête déterminent la permutation : deux stratégies
        # qui posent la même question voient le même classement. C'est ce qui
        # garde la comparaison appariée.
        rng = random.Random(f"{self.seed}:{query}")
        melange = list(urls)
        rng.shuffle(melange)
        return melange


def corpus_for(base: Corpus, seed: int) -> Corpus:
    return ShuffledCorpus(base, seed)


__all__ = ["SEEDS", "ShuffledCorpus", "corpus_for", "question_for", "task_for"]
