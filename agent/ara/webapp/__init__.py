"""Fabrique de sites et d'applications web (Phase 6).

Quatre pièces, dans cet ordre de dépendance :

* :mod:`builder` — produit les fichiers à partir d'une `SiteSpec` ;
* :mod:`critic` — les mesure et nomme chaque défaut par un **code stable** ;
* :mod:`lessons` — retient ces codes d'une tâche à l'autre, sur disque ;
* :mod:`studio` — enchaîne construire → critiquer → corriger, avec retour
  arrière si une correction dégrade la note.

La pièce qui fait « apprendre » est la troisième, et c'est la seule dont
l'effet se mesure : voir `ara/lab/webapp_test.py` (JEU 10) et l'hypothèse H3
pré-enregistrée dans `docs/H3-APPRENTISSAGE.md`.
"""

from __future__ import annotations

from .builder import Section, SiteSpec, build_site, spec_from_brief
from .critic import Critique, critique
from .lessons import Lesson, Lessons
from .studio import SiteResult, SiteStudio

__all__ = [
    "Critique", "Lesson", "Lessons", "Section", "SiteResult", "SiteSpec",
    "SiteStudio", "build_site", "critique", "spec_from_brief",
]
