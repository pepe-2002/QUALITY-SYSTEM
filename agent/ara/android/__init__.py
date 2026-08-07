"""Pont Android — accès aux capacités du téléphone via Termux (spec §13, §16).

Rien ici n'est requis pour faire tourner l'agent : sur un ordinateur, le pont
se déclare simplement indisponible et explique pourquoi. C'est la règle §19
appliquée au matériel — une ressource absente n'échoue pas en silence.
"""

from .bridge import Device, capabilities, detect, run_termux

__all__ = ["Device", "capabilities", "detect", "run_termux"]
