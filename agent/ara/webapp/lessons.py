"""Mémoire des défauts — ce qui fait qu'ARA « apprend de ses erreurs ».

Le studio corrige déjà ses fautes à l'intérieur d'une tâche : il construit,
mesure, corrige, recommence. Mais à la tâche suivante il repartait de zéro et
refaisait exactement les mêmes fautes. C'est cela que ce module supprime.

Le mécanisme, en trois lignes
-----------------------------
1. chaque défaut mesuré par le critique est enregistré sous son **code** ;
2. quand une correction fait **monter la note**, le code est marqué corrigible
   et la correction devient une règle ;
3. à la construction suivante, les règles sont appliquées **avant** la première
   version, si bien que le défaut n'apparaît plus.

Une règle prudente, et elle compte
----------------------------------
Un défaut n'entre dans les règles préventives que si sa correction a **déjà
fonctionné au moins une fois**, mesurée par une note qui monte. Une correction
tentée sans effet reste dans l'historique — pour ne pas la retenter en
aveugle — mais ne devient jamais une règle. Sans ce garde-fou, la mémoire
apprendrait aussi les mauvaises idées, et les appliquerait plus vite.

Le fichier vit dans `workspace/lessons.json`. Il est lisible : le patron doit
pouvoir voir ce que l'agent croit avoir appris, et l'effacer s'il se trompe.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ..core.config import get_settings
from .critic import DEFECTS


@dataclass
class Lesson:
    """Ce que l'agent retient d'un type de défaut."""

    code: str
    seen: int = 0            # rencontré à la première version d'un site
    fixed: int = 0           # correction appliquée, note en hausse
    failed: int = 0          # correction appliquée, note stable ou en baisse
    prevented: int = 0       # évité d'avance grâce à cette leçon
    last_task: str = ""
    examples: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return DEFECTS.get(self.code, self.code)

    @property
    def actionable(self) -> bool:
        """Vrai si la correction a déjà prouvé son effet au moins une fois."""
        return self.fixed > 0

    @property
    def reliability(self) -> float:
        essais = self.fixed + self.failed
        return self.fixed / essais if essais else 0.0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Lessons:
    """La collection, et son fichier."""

    items: dict[str, Lesson] = field(default_factory=dict)
    path: Path | None = None

    # -- écriture ----------------------------------------------------------

    def _entry(self, code: str) -> Lesson:
        return self.items.setdefault(code, Lesson(code=code))

    def record_defect(self, code: str, *, task: str = "", example: str = "") -> Lesson:
        lesson = self._entry(code)
        lesson.seen += 1
        if task:
            lesson.last_task = task
        if example and example not in lesson.examples:
            lesson.examples = (lesson.examples + [example])[-3:]
        return lesson

    def record_fix(self, code: str, *, worked: bool) -> Lesson:
        lesson = self._entry(code)
        if worked:
            lesson.fixed += 1
        else:
            lesson.failed += 1
        return lesson

    def record_prevention(self, code: str) -> Lesson:
        lesson = self._entry(code)
        lesson.prevented += 1
        return lesson

    # -- lecture -----------------------------------------------------------

    def preventive(self) -> list[str]:
        """Codes à corriger **d'avance**, les mieux établis en premier."""
        retenus = [l for l in self.items.values() if l.actionable]
        retenus.sort(key=lambda l: (l.fixed, l.seen), reverse=True)
        return [l.code for l in retenus]

    def known(self, code: str) -> bool:
        return code in self.items

    def constraints(self) -> list[str]:
        """Règles en français, telles qu'on peut les montrer au patron."""
        return [
            f"{DEFECTS.get(code, code)} — corrigé {self.items[code].fixed} fois, "
            f"appliqué d'avance"
            for code in self.preventive()
        ]

    def report(self) -> str:
        if not self.items:
            return "Aucune leçon retenue pour l'instant."
        lignes = ["| défaut | vu | corrigé | échoué | évité d'avance |",
                  "|---|---:|---:|---:|---:|"]
        for lesson in sorted(self.items.values(), key=lambda l: l.seen, reverse=True):
            lignes.append(
                f"| {lesson.label} | {lesson.seen} | {lesson.fixed} | "
                f"{lesson.failed} | {lesson.prevented} |"
            )
        return "\n".join(lignes)

    def to_dict(self) -> dict:
        return {"lessons": [l.to_dict() for l in self.items.values()]}

    # -- persistance -------------------------------------------------------

    @classmethod
    def from_dict(cls, data: dict, path: Path | None = None) -> "Lessons":
        items: dict[str, Lesson] = {}
        connus = set(Lesson.__dataclass_fields__)
        for brut in data.get("lessons", []):
            if not isinstance(brut, dict) or not brut.get("code"):
                continue
            lesson = Lesson(**{k: v for k, v in brut.items() if k in connus})
            items[lesson.code] = lesson
        return cls(items=items, path=path)

    @classmethod
    def load(cls, path: Path | None = None) -> "Lessons":
        """Charge la mémoire. Un fichier absent ou abîmé donne une mémoire vide.

        Perdre ses leçons est ennuyeux ; refuser de travailler à cause d'un
        fichier corrompu le serait beaucoup plus.
        """
        path = Path(path or get_settings().lessons_path())
        if not path.is_file():
            return cls(path=path)
        try:
            return cls.from_dict(json.loads(path.read_text(encoding="utf-8")), path)
        except (json.JSONDecodeError, TypeError, ValueError, OSError):
            return cls(path=path)

    def save(self, path: Path | None = None) -> Path:
        destination = Path(path or self.path or get_settings().lessons_path())
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self.path = destination
        return destination


__all__ = ["Lesson", "Lessons"]
