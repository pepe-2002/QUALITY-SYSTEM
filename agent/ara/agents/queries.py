"""Hygiène des requêtes et pertinence contextuelle — briques de RESEARCH-V2.

Module **nouveau** : la baseline (`research.py`, `gather.py`) n'en dépend pas
et n'est pas modifiée. Ce qui est ici corrige trois défauts constatés en
conditions réelles, sur une question posée au vrai web :

> « Quel est le tarif officiel de la traversée en vedette entre la Grande
> Comore et Mohéli ? »

L'agent avait produit les requêtes « …en vedette **entre** tarif officiel »,
« …entre **grande** » et « …entre **comore** », puis retenu comme sources les
*Vedettes de Bréhat* et les *Vedettes de l'Odet* — des traversées bretonnes.

Les trois corrections sont **générales**. Aucune liste noire : ni « Bréhat »,
ni « Odet », ni aucun nom propre particulier n'apparaît dans ce fichier. Ce
qui est corrigé, ce sont les mécanismes — sinon on ne ferait que déplacer le
problème au prochain domaine.
"""

from __future__ import annotations

import re
import unicodedata

#: Mots grammaticaux : ils ne portent pas de sens à eux seuls. Une requête qui
#: se termine par l'un d'eux est un fragment, pas une requête.
FUNCTION_WORDS: set[str] = {
    # prépositions et articles
    "a", "au", "aux", "de", "du", "des", "d", "le", "la", "les", "l", "un",
    "une", "en", "dans", "sur", "sous", "vers", "par", "pour", "avec", "sans",
    "entre", "chez", "depuis", "jusqu", "jusque", "apres", "avant", "pres",
    "loin", "contre", "selon", "malgre",
    # conjonctions et liaisons
    "et", "ou", "ni", "mais", "donc", "or", "car", "que", "qui", "quoi",
    "dont", "si", "comme", "puis", "ensuite",
    # verbes et interrogatifs vides dans une requête
    "est", "sont", "etre", "avoir", "fait", "faire", "quel", "quelle",
    "quels", "quelles", "combien", "comment", "pourquoi", "quand",
    # anglais
    "the", "of", "in", "on", "at", "to", "for", "and", "or", "is", "are",
    "with", "from", "by", "between",
}

#: Mots courants qui apparaissent **dans** les noms propres sans les
#: identifier : « Grande » Comore, « Saint »-Denis, « Nouvelle »-Calédonie,
#: « Nord »-Pas-de-Calais. Pris isolément, ils ne désignent rien.
#:
#: Ce n'est pas une liste de lieux — c'est une liste de qualificatifs
#: génériques. Elle reste valable dans n'importe quel domaine.
COMMON_MODIFIERS: set[str] = {
    "grand", "grande", "grands", "grandes", "petit", "petite", "petits",
    "petites", "haut", "haute", "bas", "basse", "nouveau", "nouvelle",
    "vieux", "vieille", "saint", "sainte", "saints", "saintes", "nord",
    "sud", "est", "ouest", "centre", "ville", "villes", "ile", "iles",
    "region", "regions", "pays", "port", "ports", "mont", "monts", "val",
    "new", "old", "north", "south", "east", "west", "city", "island",
    "upper", "lower", "great",
}

#: Une requête doit garder au moins ce nombre de mots porteurs de sens.
MIN_CONTENT_WORDS = 2
#: Longueur minimale d'un mot pour qu'il puisse à lui seul orienter une requête.
MIN_KEYWORD_LENGTH = 4
#: Longueur maximale d'une requête envoyée à un moteur.
MAX_QUERY_CHARS = 160

#: Part des termes distinctifs de la question qu'une source doit contenir.
#: À 1 terme distinctif, il faut ce terme. À 3, il en faut au moins 1.
MIN_DISTINCTIVE_RATIO = 0.34


def fold(text: str) -> str:
    """Minuscules, sans accents, ponctuation en espaces."""
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def content_words(text: str) -> list[str]:
    """Mots porteurs de sens, dans l'ordre."""
    return [w for w in fold(text).split() if w and w not in FUNCTION_WORDS]


# --- 1. Hygiène des fragments ---------------------------------------------------


def clean_fragment(text: str) -> str:
    """Retire les mots grammaticaux **en bord** de fragment.

    C'est le premier défaut constaté : le sujet extrait se terminait par une
    préposition (« …en vedette entre »), et lui recoller un complément donnait
    une requête que personne n'écrirait.

    >>> clean_fragment("tarif officiel de la traversée en vedette entre")
    'tarif officiel de la traversée en vedette'
    >>> clean_fragment("de la")
    ''
    """
    mots = fold(text).split()
    while mots and mots[0] in FUNCTION_WORDS:
        mots.pop(0)
    while mots and mots[-1] in FUNCTION_WORDS:
        mots.pop()
    return " ".join(mots)


def compose_query(topic: str, hint: str = "") -> str:
    """Assemble sujet + complément en une requête utilisable, ou rend « ».

    Trois garanties, chacune correspondant à un défaut observé :

    1. plus aucun fragment grammatical en bord (défaut 1) ;
    2. le complément n'est ajouté que s'il apporte des mots **nouveaux** —
       « tarif officiel » collé à un sujet qui dit déjà « tarif officiel »
       produisait la requête absurde constatée ;
    3. le résultat garde assez de mots porteurs de sens, sinon il est rejeté
       (défaut 2 : « entre grande » n'est pas une requête).

    >>> compose_query("tarif officiel de la traversée en vedette entre", "tarif officiel")
    'tarif officiel de la traversee en vedette'
    >>> compose_query("tarif de la traversée", "horaire officiel")
    'tarif de la traversee horaire officiel'
    >>> compose_query("entre", "grande")
    ''
    """
    sujet = clean_fragment(topic)
    complement = clean_fragment(hint)

    deja = set(sujet.split())
    nouveaux = [mot for mot in complement.split() if mot not in deja]

    requete = " ".join([sujet, *nouveaux]).strip()
    if len(content_words(requete)) < MIN_CONTENT_WORDS:
        return ""
    return requete[:MAX_QUERY_CHARS]


def is_orphan(hint: str, topic: str) -> bool:
    """Un complément qui ne peut pas porter une recherche à lui seul.

    Deuxième défaut : un mot-clé manquant devenait une requête indépendante.
    « comore » ou « grande », seuls, envoient l'agent n'importe où.
    """
    mots = content_words(hint)
    if not mots:
        return True
    if len(mots) == 1 and (
        len(mots[0]) < MIN_KEYWORD_LENGTH or mots[0] in COMMON_MODIFIERS
    ):
        return True
    # Un complément entièrement contenu dans le sujet n'ajoute rien : le
    # relancer ne ferait que rejouer la même recherche.
    return set(mots) <= set(content_words(topic))


# --- 2. Termes distinctifs et pertinence contextuelle --------------------------


_SENTENCE_START = re.compile(r"(?:^|[.!?…]\s+|«\s*)")


def distinctive_terms(question: str) -> set[str]:
    """Termes qui **identifient** le sujet, par opposition à ceux qui le décrivent.

    Troisième défaut : une page bretonne contenant « traversée », « vedette »
    et « tarif » passait le filtre d'une question sur les Comores. Ces trois
    mots décrivent un genre de chose ; ils n'en désignent aucune en
    particulier.

    Deux sources de distinction, aucune liste de noms :

    1. les **noms propres** — mots capitalisés ailleurs qu'en début de phrase,
       les suites de capitales étant recollées (« Grande Comore ») ;
    2. à défaut, les mots longs et rares de la question, qui restent le
       meilleur indice disponible sans corpus de fréquences.

    >>> sorted(distinctive_terms("Quel est le tarif de la traversée entre la Grande Comore et Mohéli ?"))
    ['comore', 'grande comore', 'moheli']
    """
    trouves: set[str] = set()

    # Position des débuts de phrase, pour ne pas prendre « Quel » pour un nom.
    debuts = {m.end() for m in _SENTENCE_START.finditer(question)}
    tokens = list(re.finditer(r"[A-Za-zÀ-ÖØ-öø-ÿ][\wÀ-ÖØ-öø-ÿ'’-]*", question))

    groupe: list[str] = []
    for index, token in enumerate(tokens):
        mot = token.group(0)
        capitalise = mot[:1].isupper() and token.start() not in debuts
        if capitalise:
            groupe.append(mot)
            suivant = tokens[index + 1] if index + 1 < len(tokens) else None
            if suivant and suivant.group(0)[:1].isupper() and suivant.start() not in debuts:
                continue
        if groupe:
            # Le groupe entier (« grande comore ») **et** chacun de ses mots :
            # une source qui ne cite que « Comores » reste pertinente.
            entier = clean_fragment(" ".join(groupe))
            if entier:
                trouves.add(entier)
                for mot_simple in entier.split():
                    # « Grande » seul ne désigne rien ; « Comore » si.
                    if (
                        len(mot_simple) >= MIN_KEYWORD_LENGTH
                        and mot_simple not in COMMON_MODIFIERS
                    ):
                        trouves.add(mot_simple)
            groupe = []

    if trouves:
        return trouves

    # Aucune majuscule exploitable : on retombe sur les mots longs, qui sont
    # les plus susceptibles d'être spécifiques.
    return {
        mot for mot in content_words(question)
        if len(mot) >= 6 and mot not in COMMON_MODIFIERS
    }


def _variants(term: str) -> set[str]:
    """Formes acceptées d'un terme : singulier/pluriel simple."""
    formes = {term}
    if term.endswith("s") and len(term) > 4:
        formes.add(term[:-1])
    else:
        formes.add(term + "s")
    return formes


def found_terms(text: str, terms: set[str]) -> set[str]:
    """Termes effectivement présents dans un texte."""
    corpus = f" {fold(text)} "
    presents = set()
    for term in terms:
        if any(f" {forme} " in corpus for forme in _variants(term)):
            presents.add(term)
    return presents


def distinctive_coverage(text: str, question: str) -> float:
    """Part des termes distinctifs de la question présents dans le texte."""
    terms = distinctive_terms(question)
    if not terms:
        return 1.0
    # Un groupe et ses mots comptent pour une seule exigence : sans cela,
    # « Grande Comore » pèserait trois fois plus que « Mohéli ».
    racines = {t for t in terms if " " not in t}
    if not racines:
        racines = terms
    return len(found_terms(text, racines)) / len(racines)


def is_on_topic(text: str, question: str, *, minimum: float = MIN_DISTINCTIVE_RATIO) -> bool:
    """Le texte parle-t-il bien du sujet de la question ?

    Exige au moins un terme distinctif. Une question sans terme distinctif
    (« combien coûte un timbre ? ») ne déclenche aucune exigence : il vaut
    mieux ne rien filtrer que filtrer au hasard.
    """
    terms = distinctive_terms(question)
    if not terms:
        return True
    return distinctive_coverage(text, question) >= minimum


__all__ = [
    "COMMON_MODIFIERS",
    "FUNCTION_WORDS",
    "MIN_CONTENT_WORDS",
    "MIN_DISTINCTIVE_RATIO",
    "MIN_KEYWORD_LENGTH",
    "clean_fragment",
    "compose_query",
    "content_words",
    "distinctive_coverage",
    "distinctive_terms",
    "fold",
    "found_terms",
    "is_on_topic",
    "is_orphan",
]
