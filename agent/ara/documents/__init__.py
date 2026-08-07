"""Générateur de documents (spec §8) : PDF, DOCX, TXT, MD.

Un modèle unique (:class:`Document`) est rendu vers plusieurs formats. Chaque
générateur **vérifie** son fichier après écriture : la spec exige que le
document puisse être ouvert avant d'être présenté à l'utilisateur.
"""

from .model import Block, Document, Run, from_markdown
from .render import VerificationError, generate, verify

__all__ = [
    "Block",
    "Document",
    "Run",
    "from_markdown",
    "generate",
    "verify",
    "VerificationError",
]
