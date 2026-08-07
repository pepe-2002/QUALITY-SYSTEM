"""Studio créatif (spec §5 à §12) — Phase 3.

    Brief marketing → recherche du marché → concepts → critique → amélioration
    → version finale

Trois principes, hérités des phases précédentes :

* **Zéro dépendance** — les créations sont du SVG produit avec la bibliothèque
  standard, et le QR code est encodé en Python pur.
* **Mesuré, pas ressenti** — le critique note douze critères sur la géométrie
  et les couleurs, donc de façon reproductible et testable.
* **Vérifié avant livraison** — un QR qui ne se relit pas n'est jamais posé,
  une correction qui dégrade la note est annulée.
"""

from .brand import BrandProfile
from .brief import Brief, from_prompt
from .canvas import Canvas, Element
from .concepts import propose
from .critic import Critique, critique
from .studio import Studio, StudioResult, Version

__all__ = [
    "BrandProfile", "Brief", "from_prompt", "Canvas", "Element",
    "propose", "critique", "Critique", "Studio", "StudioResult", "Version",
]
