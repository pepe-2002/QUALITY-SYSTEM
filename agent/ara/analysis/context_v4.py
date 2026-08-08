"""CONTEXT-V4 — ne bloquer que sur preuve, jamais sur silence.

Ce que la mesure de bout en bout a montré
------------------------------------------
V2 et V3 sont figées, mesurées, et **inadoptables** :

=========  ===============  ==============================
version    pièges bloqués   bonnes valeurs bloquées à tort
=========  ===============  ==============================
V2         10/22 (46 %)     12/125 (10 %)
V3         15/22 (68 %)     31/125 (25 %)
=========  ===============  ==============================

V3 obtenait pourtant 94 % sur son propre jeu. L'écart vient d'un biais des
jeux écrits à la main : leurs phrases sont **autoportantes**, elles nomment le
lieu, l'objet et la période. Les vraies pages ne le font pas.

    « La franchise bagages est fixée à 20 kilogrammes par passager. »

Ni lieu, ni service répétés — et V3 y voyait un défaut d'ancrage.

Le principe de V4, en une phrase
---------------------------------
**Le silence n'est pas une preuve.** Une information n'est écartée que si
quelque chose, dans la phrase, la rattache *positivement* à un autre contexte.
Ne pas répéter le sujet n'est pas en changer.

Trois conséquences, chacune contre une règle de V3 :

1. **Objet** — un objet concurrent nommé dans la phrase fait rejeter ; son
   simple silence, non. V3 exigeait la présence du terme spécifique ; V4
   exige l'absence de contradiction.
2. **Géographie** — un lieu concurrent nommé fait rejeter ; l'absence de tout
   lieu, non, dès lors que la source est du bon sujet.
3. **Noms composés** — deux qualificatifs qui **diffèrent** font rejeter
   (« Villeneuve-les-Bains » contre « Villeneuve-sur-Loire ») ; un
   qualificatif **absent** ne fait rien. Abréger n'est pas contredire — c'est
   le faux rejet que le jeu 8 avait attrapé sur V3.

Le contrôle du temps ne change pas : c'était le seul des trois à ne produire
aucun faux rejet, sur les deux jeux comme en bout de chaîne.

Ce que V4 accepte de perdre
----------------------------
Un piège dont la phrase ne dit rien de compromettant passera. C'est assumé :
sur ce système, une bonne réponse bloquée coûte plus cher qu'une mauvaise
laissée passer, puisque la seconde reste soumise au reste de la chaîne —
recoupement, détection de contradictions, agent contexte.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..agents.queries import COMMON_MODIFIERS, content_words
from .context_v2 import (
    ASSERTABLE,
    CONTEXT_UNKNOWN,
    MATCH,
    MISMATCH,
    PROBABLE_MATCH,
    STALE_YEARS,
    STATES,
    ContextVerdict,
    _MEASURE_WORDS,
    _mentions,
    _time_check,
)
from .context_v3 import _head_and_qualifiers, most_specific, proper_names

#: Longueur minimale d'un mot pour être considéré comme un objet concurrent.
#: En dessous, le risque de bruit dépasse le service rendu.
MIN_COMPETITOR_LENGTH = 5


@dataclass
class ContextV4Verdict(ContextVerdict):
    """Même contrat, avec la preuve qui a fait rejeter — s'il y en a une."""

    evidence: str = ""

    def to_dict(self) -> dict:
        return {**super().to_dict(), "evidence": self.evidence}


def object_terms(question: str) -> set[str]:
    """Ce dont la question parle, lieux et mots de mesure retirés."""
    lieux = {mot for nom in proper_names(question) for mot in nom.split()}
    return {
        mot for mot in content_words(question)
        if len(mot) >= 4
        and mot not in _MEASURE_WORDS
        and mot not in COMMON_MODIFIERS
        and mot not in lieux
    }


def conflicting_place(question: str, sentence: str, document: str = "") -> str:
    """Un lieu **concurrent** est-il nommé, alors que celui demandé est absent ?

    Deux formes de conflit, et seulement deux :

    * un nom composé partageant sa tête avec celui de la question mais portant
      un **autre qualificatif** — « Villeneuve-les-Bains » contre
      « Villeneuve-sur-Loire ». Un qualificatif *manquant* ne compte pas :
      abréger n'est pas contredire ;
    * un nom propre étranger à la question, là où aucun de ses lieux n'est
      nommé — ni dans la phrase, ni dans la source.
    """
    lieux_question = proper_names(question)
    if not lieux_question:
        return ""

    racines = {mot for nom in lieux_question for mot in nom.split() if len(mot) >= 4}
    presents = _mentions(sentence, racines) or _mentions(document, racines)

    # 1. Même tête, qualificatifs tous deux présents et différents.
    for nom_q in lieux_question:
        tete_q, qual_q = _head_and_qualifiers(nom_q)
        if not tete_q or not qual_q:
            continue
        for nom_s in proper_names(f"{sentence} {document}"):
            tete_s, qual_s = _head_and_qualifiers(nom_s)
            if tete_s == tete_q and qual_s and qual_s != qual_q:
                return f"« {nom_s} » n'est pas « {nom_q} »"

    # 2. Un lieu étranger, et aucun lieu de la question nulle part.
    if not presents:
        etrangers = {
            nom for nom in proper_names(sentence)
            if not any(mot in racines for mot in nom.split())
        }
        if etrangers:
            return (
                f"la source parle de {', '.join(sorted(etrangers))} et jamais "
                "du lieu demandé"
            )
    return ""


def conflicting_object(question: str, sentence: str, document: str = "") -> str:
    """Un objet **concurrent** est-il nommé là où celui demandé manque ?

    C'est le cœur de V4. La question n'est plus « le bon objet est-il là ? »
    — les vraies pages ne le répètent pas — mais « un autre objet a-t-il pris
    sa place ? ».
    """
    attendus = object_terms(question)
    if not attendus:
        return ""

    source = document or sentence
    specifiques = most_specific(attendus, source)
    if _mentions(sentence, specifiques):
        return ""   # le bon objet est nommé : rien à redire

    lieux = {mot for nom in proper_names(question) for mot in nom.split()}
    candidats = {
        mot for mot in content_words(sentence)
        if len(mot) >= MIN_COMPETITOR_LENGTH
        and mot not in _MEASURE_WORDS
        and mot not in COMMON_MODIFIERS
        and mot not in attendus
        and mot not in lieux
    }
    # Un mot n'est concurrent que s'il occupe la place de l'objet : on exige
    # qu'il soit, dans la source, au moins aussi spécifique que ce qu'on
    # cherchait. Sinon c'est du vocabulaire de circonstance.
    if not candidats:
        return ""
    concurrents = most_specific(candidats | specifiques, source) & candidats
    if concurrents:
        return f"la phrase parle de {', '.join(sorted(concurrents))}"
    return ""


def assess_context(
    *,
    question: str,
    sentence: str,
    document: str = "",
    title: str = "",
    now: int | None = None,
) -> ContextV4Verdict:
    """Rattache une information au contexte, en ne bloquant que sur preuve."""
    corpus = f"{title} {document}".strip()
    checks: dict[str, str] = {}

    # 1. TEMPS — inchangé : aucun faux rejet ne lui est imputable.
    temps_ok, motif = _time_check(sentence, corpus, now=now)
    checks["temps"] = "ok" if temps_ok else motif
    if not temps_ok:
        return ContextV4Verdict(MISMATCH, f"période : {motif}", checks, motif)

    # 2. LIEU — un lieu concurrent, pas un lieu absent.
    conflit_lieu = conflicting_place(question, sentence, corpus)
    checks["lieu"] = conflit_lieu or "aucun lieu concurrent"
    if conflit_lieu:
        return ContextV4Verdict(
            MISMATCH, f"lieu : {conflit_lieu}", checks, conflit_lieu
        )

    # 3. OBJET — un objet concurrent, pas un objet absent.
    conflit_objet = conflicting_object(question, sentence, corpus)
    checks["objet"] = conflit_objet or "aucun objet concurrent"
    if conflit_objet:
        return ContextV4Verdict(
            MISMATCH, f"objet : {conflit_objet}", checks, conflit_objet
        )

    # 4. Rien ne s'y oppose. Reste à dire avec quelle assurance.
    attendus = object_terms(question)
    specifiques = most_specific(attendus, corpus or sentence) if attendus else set()
    lieux = {mot for nom in proper_names(question) for mot in nom.split()
             if len(mot) >= 4}

    ancre_phrase = bool(_mentions(sentence, specifiques)) or bool(
        _mentions(sentence, lieux)
    )
    if ancre_phrase:
        return ContextV4Verdict(MATCH, "rien ne contredit le contexte demandé", checks)

    ancre_source = bool(_mentions(corpus, specifiques)) or bool(_mentions(corpus, lieux))
    if ancre_source or not (specifiques or lieux):
        return ContextV4Verdict(
            PROBABLE_MATCH,
            "la phrase ne répète pas le contexte, mais rien ne le contredit "
            "et la source est du bon sujet",
            checks,
        )

    checks["ancrage"] = "ni la phrase ni la source ne nomment le sujet"
    return ContextV4Verdict(
        CONTEXT_UNKNOWN,
        "rien ne rattache cette information au sujet, ni pour ni contre",
        checks,
    )


def filter_facts(facts, *, question: str, documents: dict[str, str] | None = None,
                 now: int | None = None):
    """Sépare l'affirmable du reste. Rien n'est jeté."""
    documents = documents or {}
    affirmables, bloques = [], []
    for fact in facts:
        verdict = assess_context(
            question=question, sentence=fact.sentence,
            document=documents.get(fact.source, ""), now=now,
        )
        (affirmables if verdict.assertable else bloques).append((fact, verdict))
    return affirmables, bloques


__all__ = [
    "ASSERTABLE", "CONTEXT_UNKNOWN", "ContextV4Verdict", "MATCH", "MISMATCH",
    "MIN_COMPETITOR_LENGTH", "PROBABLE_MATCH", "STALE_YEARS", "STATES",
    "assess_context", "conflicting_object", "conflicting_place",
    "filter_facts", "object_terms",
]
