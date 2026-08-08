"""Planificateur : lit la demande et décide du chemin à suivre.

C'est ce qui distingue un agent d'un chatbot : avant de répondre, on décide
*quoi faire* — chercher ou non, produire quels fichiers, avec quel budget.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from ..core.complexity import DEFAULT_CONTROLLER, TaskBudget, assess_for
from ..providers.llm.offline import subject

#: Extensions demandables explicitement
_FORMAT_WORDS = {
    "pdf": "pdf",
    "docx": "docx",
    "word": "docx",
    "markdown": "md",
    "md": "md",
    "txt": "txt",
    "texte": "txt",
}

#: Mots qui impliquent un livrable écrit même sans extension nommée
_DOC_WORDS = {
    "rapport", "document", "dossier", "note", "fiche", "memo", "synthese",
    "compte rendu", "recapitulatif", "resume ecrit",
}

#: Mots qui déclenchent une recherche web
_SEARCH_WORDS = {
    "recherche", "cherche", "chercher", "trouve", "trouver", "renseigne",
    "actualite", "actualites", "horaire", "horaires", "prix", "tarif",
    "tarifs", "meteo", "qui est", "combien", "quand", "sources", "documente",
    "compare", "comparer", "verifie", "verifier", "search", "find", "news",
}

#: Mots interrogatifs : une question factuelle exige des sources, même courte.
#: Sans cette règle, « Qui a écrit Le Petit Prince ? » ne déclenchait aucune
#: recherche et l'agent répondait qu'il n'avait rien consulté.
_INTERROGATIVES = {
    "qui", "que", "quoi", "quel", "quelle", "quels", "quelles", "quand",
    "comment", "pourquoi", "combien", "ou", "est-ce", "lequel", "laquelle",
    "who", "what", "when", "where", "why", "how", "which",
}

#: Politesses et bavardage : aucune recherche à lancer.
_SMALL_TALK = {
    "bonjour", "salut", "coucou", "bonsoir", "merci", "hello", "hi", "ok",
    "ca va", "comment ca va", "comment vas tu", "comment allez vous",
    "qui es tu", "que sais tu faire", "aide", "help", "test",
}

#: Une demande de création graphique n'est pas une demande de document.
_DESIGN_WORDS = {
    "flyer": "flyer", "flyers": "flyer", "affiche": "affiche",
    "affiches": "affiche", "poster": "affiche", "visuel": "flyer",
    "publicite": "flyer", "pub": "flyer", "story": "story",
    "banniere": "banniere", "carre": "carre", "prospectus": "flyer",
    "depliant": "flyer",
}

_URL_RE = re.compile(r"https?://\S+")


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


@dataclass
class Plan:
    """Décision du planificateur pour une tâche."""

    prompt: str
    budget: TaskBudget
    needs_research: bool = False
    formats: list[str] = field(default_factory=list)
    urls: list[str] = field(default_factory=list)
    filename_hint: str = "resultat"
    #: format de création graphique demandé (flyer, affiche, story…)
    design: str = ""
    #: le budget peut-il être révisé d'après ce que la recherche ramène ?
    #: Faux pour ADAPTIVE-V1 (gelée) et pour le témoin FIXED du laboratoire,
    #: qui doit rester rigoureusement fixe pour servir de point de comparaison.
    adaptive_budget: bool = False

    @property
    def needs_documents(self) -> bool:
        return bool(self.formats)

    @property
    def needs_design(self) -> bool:
        return bool(self.design)

    def describe(self) -> str:
        bits = [f"complexité {self.budget.complexity.value}"]
        if self.design:
            bits.append(f"création : {self.design}")
        bits.append(
            f"{self.budget.search_steps} recherche(s)" if self.needs_research else "sans recherche"
        )
        if self.formats:
            bits.append("livrables : " + ", ".join(self.formats))
        return " · ".join(bits)

    def to_dict(self) -> dict:
        return {
            "needs_research": self.needs_research,
            "design": self.design,
            "formats": self.formats,
            "urls": self.urls,
            **self.budget.to_dict(),
        }


def _slug(prompt: str, max_words: int = 5) -> str:
    """Nom de fichier tiré du sujet, sans les verbes de consigne."""
    words = [w for w in _normalize(subject(prompt)).split() if len(w) > 2][:max_words]
    return "-".join(words) or "resultat"


def plan(
    prompt: str,
    *,
    max_search_steps: int = 10,
    controller: str = DEFAULT_CONTROLLER,
) -> Plan:
    """Construit le plan d'exécution d'une demande.

    `controller` choisit la version du contrôleur de difficulté. Le laboratoire
    l'épingle explicitement pour chaque bras : c'est ce qui permet de comparer
    V1 et V2 sans que l'une contamine les résultats déjà publiés de l'autre.

    >>> p = plan("Recherche les horaires des traversées et fais-moi un PDF")
    >>> p.needs_research, p.formats
    (True, ['pdf'])
    """
    text = _normalize(prompt)
    padded = f" {text} "
    budget = assess_for(controller, prompt, max_search_steps=max_search_steps)

    urls = _URL_RE.findall(prompt)

    design = ""
    for word, fmt in _DESIGN_WORDS.items():
        if f" {word} " in padded:
            design = fmt
            break

    formats: list[str] = []
    for word, fmt in _FORMAT_WORDS.items():
        if f" {word} " in padded and fmt not in formats:
            formats.append(fmt)
    if not formats and any(f" {word} " in padded for word in _DOC_WORDS):
        formats.append("pdf")

    small_talk = any(text == phrase or text.startswith(phrase + " ") for phrase in _SMALL_TALK)
    first_word = text.split()[0] if text.split() else ""
    is_question = not small_talk and (
        "?" in prompt or first_word in _INTERROGATIVES
    )

    needs_research = (
        bool(urls)
        or is_question
        or any(f" {word} " in padded for word in _SEARCH_WORDS)
    )
    # Un livrable documentaire sans matière : on cherche pour avoir du contenu.
    if formats and not needs_research and budget.complexity.value != "LOW":
        needs_research = True

    # Un flyer n'est pas un rapport : ne pas produire un PDF de texte en plus.
    if design:
        formats = [f for f in formats if f != "pdf"] if "pdf" not in text else formats

    return Plan(
        prompt=prompt,
        budget=budget,
        needs_research=needs_research,
        formats=formats,
        urls=urls,
        filename_hint=_slug(prompt),
        design=design,
        # V1 est gelée : elle décide une fois, avant de chercher, et ne revient
        # jamais dessus. Seule V2 révise son budget en cours de route.
        adaptive_budget=(controller == "v2"),
    )
