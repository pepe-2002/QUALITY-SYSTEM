"""CONTEXT-V2 — une information appartient-elle vraiment au contexte demandé ?

Ce que l'autopsie a montré
--------------------------
Les seize erreurs de contextualisation ont un point commun qui change tout :
**dans les seize cas, la bonne valeur était disponible**. Le système ne
manquait pas d'information — il en avait trop, et il a servi la mauvaise.

Leurs causes, telles que relevées :

===  ==========================================================
  9  temps — une page ancienne prise pour l'actuelle
  3  objet — un autre bien ou service que celui demandé
  2  géographie — un autre lieu
  2  géographie — un lieu au nom voisin
===  ==========================================================

Le temps domine, et de loin. C'est donc par là que ce module commence.

Quatre états, et un seul autorise l'affirmation
-----------------------------------------------
``MATCH``
    l'information est ancrée dans le contexte demandé : bon objet, bon lieu,
    période compatible.

``PROBABLE_MATCH``
    l'ancrage est partiel — le document parle du bon sujet, la phrase ne le
    répète pas. Utilisable avec réserve.

``CONTEXT_UNKNOWN``
    rien ne permet de rattacher l'information au sujet. Ni preuve pour, ni
    preuve contre.

``MISMATCH``
    l'information appartient démontrablement à un autre contexte : autre
    période, autre lieu.

Règle de sécurité : ``CONTEXT_UNKNOWN`` et ``MISMATCH`` ne doivent **jamais**
devenir une affirmation factuelle. Le montant peut être mentionné, daté,
attribué — jamais présenté comme la réponse.

Faiblesse principale, mesurée et non corrigée
----------------------------------------------
Le contrôle d'objet se contente d'**un** terme partagé. « Le violon d'étude
est vendu 310 euros à l'école de Vaudreuil » répond donc à une question sur
une guitare, parce que « école » suffit. Quatre des dix pièges du jeu 7
passent pour cette raison.

Le corriger exigerait de peser les termes — savoir que « violon » et
« guitare » s'excluent, que « école » ne distingue rien — et donc une version
suivante avec son propre jeu de test. Ajuster ce mécanisme-ci sur les cas du
jeu 7 reviendrait à s'entraîner sur son propre examen.

Second effet, du même ordre : une question sans nom propre voit tous ses mots
longs traités comme des lieux, ce qui désactive le contrôle d'objet. Aucune
question du jeu 7 n'est dans ce cas, mais la faille est réelle.
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field

from ..agents.queries import COMMON_MODIFIERS, content_words, distinctive_terms, fold

MATCH = "MATCH"
PROBABLE_MATCH = "PROBABLE_MATCH"
CONTEXT_UNKNOWN = "CONTEXT_UNKNOWN"
MISMATCH = "MISMATCH"

STATES = (MATCH, PROBABLE_MATCH, CONTEXT_UNKNOWN, MISMATCH)

#: États dont une réponse peut faire une affirmation.
ASSERTABLE = (MATCH, PROBABLE_MATCH)

#: Un écart d'au moins deux ans rend une valeur suspecte pour une question
#: posée au présent. Un an d'écart peut n'être qu'un millésime de publication.
STALE_YEARS = 2

#: Mots qui signalent explicitement une page d'archive.
_ARCHIVE_WORDS = re.compile(
    r"\b(?:archive|archives|archiv[ée]e?s?|historique|ancien|anciens|ancienne"
    r"|anciennes|autrefois|[àa]\s+l'[ée]poque|p[ée]rim[ée]e?s?|obsol[èe]te)\b",
    re.IGNORECASE,
)

#: Formes verbales du passé qui accompagnent un prix révolu.
_PAST_TENSE = re.compile(
    r"\b(?:co[uû]tait|valait|[ée]tait|s'[ée]levait|atteignait|se\s+vendait"
    r"|pratiquait|achetait|facturait)\b",
    re.IGNORECASE,
)

_YEAR = re.compile(r"\b(19|20)\d{2}\b")

#: Mots qui décrivent la **mesure** demandée, pas son objet. Les garder comme
#: termes d'objet ferait passer n'importe quel prix pour le bon prix.
_MEASURE_WORDS = {
    "prix", "tarif", "tarifs", "cout", "couts", "coute", "montant", "somme",
    "combien", "payer", "budget", "cher", "valeur", "vaut", "duree", "dure",
    "temps", "distance", "heure", "heures", "horaire", "horaires", "poids",
    "taux", "pourcentage", "franc", "francs", "euro", "euros", "officiel",
    "officielle", "exact", "exacte", "actuel", "actuelle", "aujourd", "hui",
    "annee", "annees", "kilo", "kilos", "kilogramme", "kilogrammes",
    "kilometre", "kilometres", "personne", "passager", "passagers",
}


@dataclass
class ContextVerdict:
    """Ce qu'on peut dire du rattachement d'une information au sujet."""

    state: str
    reason: str
    checks: dict = field(default_factory=dict)

    @property
    def assertable(self) -> bool:
        """Cette information peut-elle être affirmée comme la réponse ?"""
        return self.state in ASSERTABLE

    def to_dict(self) -> dict:
        return {
            "state": self.state, "reason": self.reason,
            "assertable": self.assertable, "checks": self.checks,
        }


def object_terms(question: str) -> set[str]:
    """Ce dont la question parle, une fois retirés le lieu et la mesure.

    « Combien coûte le clou de girofle à Bandiagara ? » → ``{clou, girofle}``.
    C'est ce qui permet de refuser un prix de vanille à une question sur le
    girofle — le troisième motif d'erreur de l'autopsie.
    """
    lieux = {mot for terme in distinctive_terms(question) for mot in terme.split()}
    return {
        mot for mot in content_words(question)
        if len(mot) >= 4
        and mot not in _MEASURE_WORDS
        and mot not in COMMON_MODIFIERS
        and mot not in lieux
    }


def _mentions(text: str, terms: set[str]) -> set[str]:
    corpus = f" {fold(text)} "
    trouves = set()
    for terme in terms:
        formes = {terme, terme + "s", terme[:-1] if terme.endswith("s") else terme}
        if any(f" {forme} " in corpus for forme in formes):
            trouves.add(terme)
    return trouves


def _time_check(sentence: str, document: str, *, now: int | None = None) -> tuple[bool, str]:
    """(compatible, motif). Faux = l'information est datée."""
    annee_courante = now or time.localtime().tm_year

    # Un marqueur d'archive dans le document suffit : c'est une déclaration.
    if _ARCHIVE_WORDS.search(document) or _ARCHIVE_WORDS.search(sentence):
        annees = [int(a.group(0)) for a in _YEAR.finditer(f"{sentence} {document}")]
        anciennes = [a for a in annees if annee_courante - a >= STALE_YEARS]
        if anciennes or not annees:
            return False, (
                f"page déclarée d'archive{f' ({min(anciennes)})' if anciennes else ''}"
            )

    # Un prix au passé, accompagné d'une année révolue, dans la phrase même.
    annees_phrase = [int(a.group(0)) for a in _YEAR.finditer(sentence)]
    revolues = [a for a in annees_phrase if annee_courante - a >= STALE_YEARS]
    if revolues and _PAST_TENSE.search(sentence):
        return False, f"valeur donnée au passé pour {min(revolues)}"
    if revolues:
        return False, f"valeur rattachée à {min(revolues)}, révolue"

    return True, ""


def assess_context(
    *,
    question: str,
    sentence: str,
    document: str = "",
    title: str = "",
    now: int | None = None,
) -> ContextVerdict:
    """Rattache — ou non — une information au contexte de la question.

    L'ordre des contrôles suit l'autopsie : le temps d'abord, puisqu'il cause
    plus de la moitié des erreurs, la géographie ensuite, l'objet en dernier.

    >>> assess_context(question="Quel est le tarif de la traversée vers Mohéli ?",
    ...                sentence="En 2019, la traversée coûtait 9 000 francs comoriens.",
    ...                title="Tarifs 2019 — archive", now=2026).state
    'MISMATCH'
    """
    corpus_doc = f"{title} {document}"
    checks: dict[str, str] = {}

    # 1. TEMPS et ARCHIVE — la cause dominante.
    temps_ok, motif_temps = _time_check(sentence, corpus_doc, now=now)
    checks["temps"] = "ok" if temps_ok else motif_temps
    if not temps_ok:
        return ContextVerdict(MISMATCH, f"période : {motif_temps}", checks)

    # 2. IDENTITÉ et GÉOGRAPHIE — le sujet nommé est-il là ?
    lieux = distinctive_terms(question)
    racines = {t for t in lieux if " " not in t} or lieux
    if racines:
        dans_la_phrase = _mentions(sentence, racines)
        dans_le_document = _mentions(corpus_doc, racines)
        if not dans_le_document and not dans_la_phrase:
            checks["geographie"] = "aucun terme du sujet dans la source"
            return ContextVerdict(
                MISMATCH,
                "identité : la source ne nomme aucun des termes distinctifs "
                "de la question",
                checks,
            )
        checks["geographie"] = (
            "nommé dans la phrase" if dans_la_phrase else "nommé dans le document"
        )
    else:
        checks["geographie"] = "aucun terme distinctif à vérifier"

    # 3. OBJET — parle-t-on bien de la même chose ?
    objets = object_terms(question)
    if objets:
        dans_la_phrase = _mentions(sentence, objets)
        dans_le_document = _mentions(corpus_doc, objets)
        if not dans_la_phrase and not dans_le_document:
            checks["objet"] = "aucun terme d'objet retrouvé"
            return ContextVerdict(
                CONTEXT_UNKNOWN,
                "objet : rien ne rattache cette valeur à ce qui est demandé",
                checks,
            )
        if not dans_la_phrase:
            checks["objet"] = "objet nommé ailleurs dans la source, pas ici"
            return ContextVerdict(
                PROBABLE_MATCH,
                "objet : la source parle du bon sujet, mais pas cette phrase-ci",
                checks,
            )
        checks["objet"] = f"nommé dans la phrase ({', '.join(sorted(dans_la_phrase))})"
    else:
        checks["objet"] = "aucun terme d'objet à vérifier"

    if checks.get("geographie") == "nommé dans le document":
        return ContextVerdict(
            PROBABLE_MATCH,
            "le sujet est nommé dans la source, pas dans la phrase même",
            checks,
        )
    return ContextVerdict(MATCH, "objet, lieu et période concordent", checks)


def filter_facts(facts, *, question: str, documents: dict[str, str] | None = None,
                 now: int | None = None):
    """Sépare ce qui peut être affirmé de ce qui ne le peut pas.

    Retourne ``(affirmables, bloques)``, chaque élément étant un couple
    ``(fait, verdict)``. Rien n'est jeté : ce qui est bloqué reste
    consultable, avec la raison de son blocage.
    """
    documents = documents or {}
    affirmables, bloques = [], []
    for fact in facts:
        document = documents.get(fact.source, "")
        verdict = assess_context(
            question=question, sentence=fact.sentence, document=document, now=now
        )
        (affirmables if verdict.assertable else bloques).append((fact, verdict))
    return affirmables, bloques


__all__ = [
    "ASSERTABLE",
    "CONTEXT_UNKNOWN",
    "ContextVerdict",
    "MATCH",
    "MISMATCH",
    "PROBABLE_MATCH",
    "STALE_YEARS",
    "STATES",
    "assess_context",
    "filter_facts",
    "object_terms",
]
