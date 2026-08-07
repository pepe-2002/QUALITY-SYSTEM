"""Analyse des sources (spec §2, §3) — Phase 2.

Comparer des sources suppose d'avoir quelque chose de **comparable**. Du texte
brut ne se compare pas ; des faits chiffrés, si. Ce paquet extrait les
grandeurs mesurables des pages (prix, durées, distances, pourcentages, dates),
les confronte entre sources, et signale ce qui manque.

Tout y est déterministe et sans réseau : c'est ce qui rend la détection de
contradictions reproductible et testable, indépendamment du LLM configuré.
"""

from .compare import Contradiction, find_contradictions
from .coverage import Gap, detect_aspects, find_gaps
from .facts import Fact, extract_facts
from .verify import AnswerCheck, verify_answer
from .report import ResearchReport

__all__ = [
    "Fact",
    "extract_facts",
    "Contradiction",
    "find_contradictions",
    "Gap",
    "find_gaps",
    "detect_aspects",
    "ResearchReport",
    "AnswerCheck",
    "verify_answer",
]
