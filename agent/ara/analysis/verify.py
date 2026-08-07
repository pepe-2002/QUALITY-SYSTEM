"""Vérification de la réponse avant livraison (étape VÉRIFICATION de la spec §3).

La boucle de recherche peut être irréprochable et la réponse rester mauvaise :
un LLM invente parfois une citation, oublie de sourcer un chiffre, ou renvoie
vers une source qui n'existe pas. On contrôle donc la réponse **elle-même**,
avant de la présenter.

Ces contrôles ne réécrivent rien : ils signalent. Corriger automatiquement une
réponse mal sourcée reviendrait à masquer le problème.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..core.models import SourceDoc

_CITATION = re.compile(r"\[S(\d+)\]")
#: Un chiffre significatif : au moins deux caractères, pour ignorer les
#: numéros de liste et les « 1 » isolés.
_NUMERIC_CLAIM = re.compile(r"\b\d[\d\s  .,]{1,}\d\s*(?:%|€|\$|[A-Za-zÀ-ÿ]{1,20})")


@dataclass
class AnswerCheck:
    """Résultat du contrôle d'une réponse."""

    citations: set[int] = field(default_factory=set)
    problems: list[str] = field(default_factory=list)
    uncited_claims: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "citations": sorted(self.citations),
            "problems": self.problems,
            "uncited_claims": self.uncited_claims[:5],
        }


def verify_answer(answer: str, docs: list[SourceDoc]) -> AnswerCheck:
    """Contrôle la cohérence entre la réponse et les sources réellement lues.

    >>> from ara.core.models import SourceDoc
    >>> verify_answer("Le tarif est de 15 000 FC [S1].", [SourceDoc(url="https://a.test")]).ok
    True
    >>> verify_answer("Le tarif est de 15 000 FC [S9].", [SourceDoc(url="https://a.test")]).ok
    False
    """
    check = AnswerCheck()
    if not answer.strip():
        check.problems.append("La réponse est vide.")
        return check

    check.citations = {int(n) for n in _CITATION.findall(answer)}

    # 1. Une citation doit désigner une source existante.
    invalid = sorted(n for n in check.citations if n < 1 or n > len(docs))
    if invalid:
        check.problems.append(
            "Citations vers des sources inexistantes : "
            + ", ".join(f"[S{n}]" for n in invalid)
        )

    # 2. Des sources ont été lues, mais la réponse n'en cite aucune.
    if docs and not check.citations:
        check.problems.append(
            f"{len(docs)} source(s) consultée(s) mais aucune n'est citée dans la réponse."
        )

    # 3. Chiffres avancés sans citation sur la même ligne.
    if docs:
        for line in answer.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", ">", "|")):
                continue
            if _CITATION.search(stripped):
                continue
            for match in _NUMERIC_CLAIM.finditer(stripped):
                claim = match.group(0).strip()
                if claim not in check.uncited_claims:
                    check.uncited_claims.append(claim)

    return check


def summarize(check: AnswerCheck) -> str:
    """Phrase courte destinée à l'étape VÉRIFICATION de l'interface."""
    if check.ok and not check.uncited_claims:
        return f"réponse cohérente · {len(check.citations)} citation(s)"
    bits = []
    if check.problems:
        bits.append(f"{len(check.problems)} problème(s) de citation")
    if check.uncited_claims:
        bits.append(f"{len(check.uncited_claims)} chiffre(s) non sourcé(s)")
    return " · ".join(bits)
