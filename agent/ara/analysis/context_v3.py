"""CONTEXT-V3 — peser les termes au lieu de les compter.

CONTEXT-V2 est figée : elle reste consultable, elle a sa mesure (73 % sur le
jeu 7), et rien ici ne la modifie. Cette version-ci s'attaque aux quatre cas
qu'elle laissait passer, dont **trois avaient la même cause** : le contrôle
d'objet se contentait d'un terme partagé, sans le peser. « École » suffisait à
rattacher un violon à une question sur une guitare.

Trois changements, tous généraux
---------------------------------
1. **Le terme d'objet le plus spécifique fait foi.** Les mots de la question
   sont classés par rareté dans la source : celui qui apparaît partout
   (« école », « cours ») ne distingue rien ; celui qui apparaît peu
   (« guitare », « girofle ») désigne. C'est ce dernier qu'on exige.

2. **Un objet concurrent vaut désaveu.** Si la phrase nomme un objet que la
   question ne mentionne pas, là où le terme spécifique attendu est absent,
   ce n'est plus une incertitude : c'est un autre sujet. ``MISMATCH``, pas
   ``CONTEXT_UNKNOWN``.

3. **Même tête, autre qualificatif = autre entité.** « Vaudreuil-sur-Mer » et
   « Vaudreuil-les-Bois » partagent leur tête et diffèrent par leur
   qualificatif : ce sont deux lieux. La règle ne connaît aucun nom
   particulier — elle compare des formes composées, et vaut donc pour
   « Bandiagara » contre « Bandiagara-Nord » comme pour n'importe quelle
   paire du même moule.

Ce que V3 récupère au passage
------------------------------
La faille « question sans nom propre » que V2 documentait sans la corriger.
La correction avait été rejetée en V2 parce qu'elle dégradait le cas
girofle/vanille : « planteur » devenait un terme d'objet recevable. Avec la
règle du terme **le plus spécifique**, « planteur » ne l'emporte plus sur
« girofle » — la correction redevient donc sûre. Elle n'est reprise que pour
cette raison, et le jeu 8 dira si elle tient.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from ..agents.queries import COMMON_MODIFIERS, content_words, fold
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

#: Un mot présent dans cette proportion des phrases d'une source ne distingue
#: rien : c'est le vocabulaire de la page, pas l'objet de la question.
GENERIC_RATIO = 0.5

#: Noms propres : capitalisés hors début de phrase, tirets conservés pour que
#: « Vaudreuil-sur-Mer » reste d'un seul tenant.
_PROPER = re.compile(r"(?<!^)(?<![.!?…]\s)\b([A-ZÀ-Þ][\wÀ-ÿ'’]*(?:-[\wÀ-ÿ'’]+)*)")

#: Mots de liaison internes aux noms composés — ils ne portent pas l'identité.
_LINKERS = {"sur", "sous", "les", "le", "la", "de", "du", "des", "en", "aux",
            "lez", "and", "of"}


@dataclass
class ContextV3Verdict(ContextVerdict):
    """Même contrat que V2, avec le détail de la pesée."""

    weights: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {**super().to_dict(), "weights": self.weights}


def _sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?…])\s+|\n+", text or "") if s.strip()]


def proper_names(text: str) -> set[str]:
    """Noms propres composés d'un texte, forme repliée."""
    trouves = set()
    for match in _PROPER.finditer(text):
        nom = fold(match.group(1)).strip()
        if nom and nom not in COMMON_MODIFIERS:
            trouves.add(nom)
    return trouves


def _head_and_qualifiers(nom: str) -> tuple[str, set[str]]:
    """Tête d'un nom composé, et ce qui le qualifie.

    « vaudreuil sur mer » → ``('vaudreuil', {'mer'})``. Les mots de liaison
    sont écartés : ce qui distingue deux communes, c'est « mer » contre
    « bois », pas « sur » contre « les ».
    """
    morceaux = [m for m in nom.replace("-", " ").split() if m]
    if not morceaux:
        return "", set()
    tete = morceaux[0]
    qualifiants = {m for m in morceaux[1:] if m not in _LINKERS}
    return tete, qualifiants


def qualified_mismatch(question: str, source: str) -> str:
    """Détecte deux entités qui partagent leur tête mais pas leur qualificatif.

    Retourne une explication, ou une chaîne vide si rien ne s'y oppose.

    >>> qualified_mismatch("cours à Vaudreuil-sur-Mer ?", "École de Vaudreuil-les-Bois")
    'Vaudreuil-les-Bois n'est pas Vaudreuil-sur-Mer'
    """
    for nom_question in proper_names(question):
        tete_q, qual_q = _head_and_qualifiers(nom_question)
        if not tete_q:
            continue
        for nom_source in proper_names(source):
            tete_s, qual_s = _head_and_qualifiers(nom_source)
            if tete_s != tete_q:
                continue
            if not qual_q and not qual_s:
                continue
            if qual_q != qual_s and (qual_q or qual_s):
                # Même tête, qualificatifs différents : deux entités.
                return (
                    f"« {nom_source} » n'est pas « {nom_question} » : "
                    "même nom, autre lieu"
                )
    return ""


def object_terms(question: str) -> set[str]:
    """Ce dont la question parle, lieux et mots de mesure retirés.

    Contrairement à V2, les lieux sont ici les **noms propres seuls** : sans
    cela, une question sans majuscule perdait tous ses termes d'objet.
    """
    lieux = {mot for nom in proper_names(question) for mot in nom.split()}
    return {
        mot for mot in content_words(question)
        if len(mot) >= 4
        and mot not in _MEASURE_WORDS
        and mot not in COMMON_MODIFIERS
        and mot not in lieux
    }


def weigh_terms(terms: set[str], document: str) -> dict[str, float]:
    """Spécificité de chaque terme dans une source : 1 = rare, 0 = partout.

    Une simple fréquence de phrases suffit. Un vrai IDF demanderait un corpus ;
    ici la source elle-même dit ce qui, en son sein, distingue.
    """
    phrases = _sentences(document) or [document]
    poids: dict[str, float] = {}
    for terme in terms:
        presences = sum(1 for phrase in phrases if _mentions(phrase, {terme}))
        poids[terme] = 1.0 - (presences / len(phrases)) if phrases else 1.0
    return poids


def most_specific(terms: set[str], document: str) -> set[str]:
    """Termes qui portent réellement l'identité de l'objet demandé.

    On garde ceux dont la spécificité dépasse le seuil ; s'il n'en reste
    aucun — tous les mots sont banals dans cette source — on garde les plus
    longs, faute de mieux, plutôt que de renoncer au contrôle.
    """
    if not terms:
        return set()
    poids = weigh_terms(terms, document)
    retenus = {t for t, p in poids.items() if p >= GENERIC_RATIO}
    if retenus:
        return retenus
    longueur_max = max(len(t) for t in terms)
    return {t for t in terms if len(t) == longueur_max}


def competing_objects(sentence: str, question: str) -> set[str]:
    """Objets nommés dans la phrase que la question ne demande pas."""
    attendus = object_terms(question) | {
        mot for nom in proper_names(question) for mot in nom.split()
    }
    candidats = {
        mot for mot in content_words(sentence)
        if len(mot) >= 5
        and mot not in _MEASURE_WORDS
        and mot not in COMMON_MODIFIERS
    }
    return candidats - attendus


def assess_context(
    *,
    question: str,
    sentence: str,
    document: str = "",
    title: str = "",
    now: int | None = None,
) -> ContextV3Verdict:
    """Rattache — ou non — une information au contexte de la question."""
    corpus_doc = f"{title} {document}".strip()
    checks: dict[str, str] = {}
    poids: dict[str, float] = {}

    # 1. TEMPS — inchangé depuis V2 : il fonctionnait.
    temps_ok, motif = _time_check(sentence, corpus_doc, now=now)
    checks["temps"] = "ok" if temps_ok else motif
    if not temps_ok:
        return ContextV3Verdict(MISMATCH, f"période : {motif}", checks, poids)

    # 2. IDENTITÉ — même tête, autre qualificatif : deux entités.
    desaveu = qualified_mismatch(question, f"{corpus_doc} {sentence}")
    if desaveu:
        checks["identite"] = desaveu
        return ContextV3Verdict(MISMATCH, f"identité : {desaveu}", checks, poids)

    # 3. GÉOGRAPHIE — le sujet nommé est-il présent ?
    lieux = proper_names(question)
    if lieux:
        racines = {mot for nom in lieux for mot in nom.split()
                   if mot not in _LINKERS and len(mot) >= 4}
        dans_phrase = _mentions(sentence, racines)
        dans_document = _mentions(corpus_doc, racines)
        if not dans_phrase and not dans_document:
            checks["geographie"] = "aucun terme du sujet dans la source"
            return ContextV3Verdict(
                MISMATCH, "identité : la source ne nomme pas le sujet demandé",
                checks, poids,
            )
        checks["geographie"] = (
            "nommé dans la phrase" if dans_phrase else "nommé dans le document"
        )
    else:
        checks["geographie"] = "aucun nom propre à vérifier"
        dans_phrase = True

    # 4. OBJET — le terme le plus spécifique fait foi.
    objets = object_terms(question)
    if objets:
        source = corpus_doc or sentence
        poids = weigh_terms(objets, source)
        specifiques = most_specific(objets, source)
        checks["objet_specifique"] = ", ".join(sorted(specifiques))

        dans_phrase_obj = _mentions(sentence, specifiques)
        dans_document_obj = _mentions(source, specifiques)
        concurrents = competing_objects(sentence, question)

        if not dans_phrase_obj:
            if concurrents:
                checks["objet"] = f"objet concurrent : {', '.join(sorted(concurrents))}"
                return ContextV3Verdict(
                    MISMATCH,
                    "objet : la phrase parle d'autre chose que ce qui est demandé",
                    checks, poids,
                )
            if not dans_document_obj:
                checks["objet"] = "aucun terme spécifique retrouvé"
                return ContextV3Verdict(
                    CONTEXT_UNKNOWN,
                    "objet : rien ne rattache cette valeur à ce qui est demandé",
                    checks, poids,
                )
            checks["objet"] = "objet nommé ailleurs dans la source, pas ici"
            return ContextV3Verdict(
                PROBABLE_MATCH,
                "objet : la source parle du bon sujet, mais pas cette phrase-ci",
                checks, poids,
            )
        checks["objet"] = f"spécifique présent ({', '.join(sorted(dans_phrase_obj))})"
    else:
        checks["objet"] = "aucun terme d'objet à vérifier"

    if checks.get("geographie") == "nommé dans le document":
        return ContextV3Verdict(
            PROBABLE_MATCH,
            "le sujet est nommé dans la source, pas dans la phrase même",
            checks, poids,
        )
    return ContextV3Verdict(MATCH, "objet, lieu et période concordent", checks, poids)


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
    "ASSERTABLE", "CONTEXT_UNKNOWN", "ContextV3Verdict", "GENERIC_RATIO",
    "MATCH", "MISMATCH", "PROBABLE_MATCH", "STALE_YEARS", "STATES",
    "assess_context", "competing_objects", "filter_facts", "most_specific",
    "object_terms", "proper_names", "qualified_mismatch", "weigh_terms",
]
