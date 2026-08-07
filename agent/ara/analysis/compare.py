"""Confrontation des sources — détection de contradictions (spec §2).

Deux sources se contredisent quand elles avancent, **sur le même sujet**, deux
valeurs de même nature qui ne peuvent pas être vraies ensemble.

Trois précautions, sans lesquelles l'agent crierait à la contradiction en
permanence :

1. **Même unité, même devise.** 15 000 KMF et 30 EUR ne se comparent pas.
2. **Même sujet.** Les deux phrases doivent partager assez de mots porteurs de
   sens ; sinon on compare le prix d'un billet avec celui d'un hôtel.
3. **Tolérance et fourchettes.** Un écart de quelques pour cent est du bruit
   (arrondis, taxes) ; et une valeur ponctuelle incluse dans une fourchette
   confirme la fourchette, elle ne la contredit pas.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

from .facts import Fact

#: Écart relatif en deçà duquel deux valeurs sont considérées comme d'accord
TOLERANCE = 0.10
#: Mots porteurs de sens communs exigés pour juger que deux faits parlent
#: bien de la même chose
MIN_SHARED_CONTEXT = 2
#: Familles comparables. Les années en sont exclues : deux dates différentes
#: dans deux pages ne sont presque jamais une contradiction.
COMPARABLE = frozenset({"money", "duration", "distance", "percent", "weight"})
#: Nombre maximal de désaccords remontés pour une tâche
MAX_REPORTED = 5
#: Au-delà de ce rapport entre deux valeurs, elles ne mesurent pas la même
#: chose. « 6 m » (une antenne) et « 330 m » (la tour qui la porte) ne se
#: contredisent pas : elles parlent d'objets différents.
MAX_RATIO = 5.0


@dataclass
class Contradiction:
    """Un désaccord constaté entre deux sources."""

    kind: str
    unit: str
    facts: list[Fact] = field(default_factory=list)
    shared: set[str] = field(default_factory=set)

    @property
    def sources(self) -> list[int]:
        return sorted({fact.source for fact in self.facts})

    def describe(self) -> str:
        parts = " ≠ ".join(
            f"{fact.describe()} [S{fact.source}]" for fact in self.facts
        )
        sujet = ", ".join(sorted(self.shared)[:4])
        return f"{parts} (à propos de : {sujet})"

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "unit": self.unit,
            "sources": self.sources,
            "describe": self.describe(),
            "subject": sorted(self.shared)[:6],
            "facts": [fact.to_dict() for fact in self.facts],
            "sentences": [fact.sentence for fact in self.facts],
        }


def _independent(a: Fact, b: Fact, domains: dict[int, str] | None) -> bool:
    """Deux faits proviennent-ils de sources réellement indépendantes ?"""
    if a.source == b.source:
        return False
    if domains is None:
        return True
    left, right = domains.get(a.source), domains.get(b.source)
    return not (left and right and left == right)


def _same_order(a: Fact, b: Fact, max_ratio: float = MAX_RATIO) -> bool:
    """Les deux valeurs sont-elles du même ordre de grandeur ?

    Se contredire suppose de parler de la même chose. Deux valeurs séparées
    d'un facteur 50 décrivent presque toujours deux objets distincts.
    """
    left = max(abs(a.low), abs(a.high))
    right = max(abs(b.low), abs(b.high))
    if left == 0 or right == 0:
        return left == right
    return max(left, right) / min(left, right) <= max_ratio


def _overlap(a: Fact, b: Fact, tolerance: float) -> bool:
    """Les deux intervalles se recouvrent-ils, tolérance comprise ?"""
    low_a, high_a = a.low * (1 - tolerance), a.high * (1 + tolerance)
    low_b, high_b = b.low * (1 - tolerance), b.high * (1 + tolerance)
    return low_a <= high_b and low_b <= high_a


def find_contradictions(
    facts: list[Fact],
    *,
    tolerance: float = TOLERANCE,
    min_shared: int = MIN_SHARED_CONTEXT,
    focus: set[str] | None = None,
    domains: dict[int, str] | None = None,
) -> list[Contradiction]:
    """Retourne les désaccords entre sources différentes.

    `focus` porte les mots-clés de la question. Quand il est fourni, seuls les
    désaccords **portant sur le sujet demandé** sont retenus. Sans ce filtre,
    une page de voyage généraliste produit des dizaines de fausses alertes :
    prix d'un hôtel contre prix d'un repas, tous « à propos des Comores ».
    Constaté en conditions réelles — 29 alertes pour un seul désaccord utile.

    `domains` associe chaque source à son domaine. Deux pages du **même site**
    ne sont pas des sources indépendantes : leurs écarts relèvent du contexte
    (époques, variantes), pas du désaccord. Constaté aussi en réel — 14 fausses
    alertes entre pages d'un même encyclopédie.

    >>> from .facts import extract_facts
    >>> a = extract_facts("Le billet coûte 15 000 francs comoriens.", 1)
    >>> b = extract_facts("Le billet coûte 40 000 francs comoriens.", 2)
    >>> len(find_contradictions(a + b))
    1
    """
    groups: dict[tuple[str, str], list[Fact]] = {}
    for fact in facts:
        if fact.kind not in COMPARABLE:
            continue
        groups.setdefault((fact.kind, fact.unit), []).append(fact)

    found: list[Contradiction] = []
    for (kind, unit), group in groups.items():
        for a, b in combinations(group, 2):
            if not _independent(a, b, domains):
                continue
            shared = a.context & b.context
            if len(shared) < min_shared:
                continue
            if focus and not (shared & focus):
                continue
            if _overlap(a, b, tolerance):
                continue
            if not _same_order(a, b):
                continue
            found.append(Contradiction(kind=kind, unit=unit, facts=[a, b], shared=shared))

    # Les désaccords les mieux étayés (contexte le plus riche) d'abord, puis
    # on s'arrête : au-delà d'une poignée, on noie l'utilisateur et la boucle
    # de recherche part chasser du bruit.
    found.sort(key=lambda c: len(c.shared), reverse=True)
    return _merge(found)[:MAX_REPORTED]


def _merge(items: list[Contradiction]) -> list[Contradiction]:
    """Fusionne les désaccords portant sur le même sujet et la même unité.

    Sans cela, trois sources en désaccord produiraient trois alertes pour un
    seul problème réel.
    """
    merged: list[Contradiction] = []
    for item in items:
        for existing in merged:
            if existing.kind != item.kind or existing.unit != item.unit:
                continue
            if len(existing.shared & item.shared) < MIN_SHARED_CONTEXT:
                continue
            for fact in item.facts:
                if not any(
                    other.source == fact.source and other.low == fact.low
                    for other in existing.facts
                ):
                    existing.facts.append(fact)
            existing.shared &= item.shared or existing.shared
            break
        else:
            merged.append(item)
    return merged


def agreements(
    facts: list[Fact],
    *,
    tolerance: float = TOLERANCE,
    domains: dict[int, str] | None = None,
) -> list[list[Fact]]:
    """Faits concordants confirmés par au moins deux sources indépendantes.

    Une valeur que plusieurs sources donnent est bien plus solide qu'une valeur
    isolée — à condition que les sources soient réellement distinctes. Deux
    pages du même site qui se répètent ne confirment rien.
    """
    groups: dict[tuple[str, str], list[Fact]] = {}
    for fact in facts:
        if fact.kind in COMPARABLE:
            groups.setdefault((fact.kind, fact.unit), []).append(fact)

    confirmed: list[list[Fact]] = []
    for group in groups.values():
        for a, b in combinations(group, 2):
            if not _independent(a, b, domains):
                continue
            if len(a.context & b.context) < MIN_SHARED_CONTEXT:
                continue
            if not _overlap(a, b, tolerance):
                continue
            for cluster in confirmed:
                if any(_overlap(a, other, tolerance) for other in cluster):
                    if a not in cluster:
                        cluster.append(a)
                    if b not in cluster:
                        cluster.append(b)
                    break
            else:
                confirmed.append([a, b])

    return [c for c in confirmed if len({f.source for f in c}) >= 2]
