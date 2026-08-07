"""Moteur hors-ligne extractif — le fournisseur par défaut (coût zéro).

Ce n'est **pas** un modèle de langage : il n'invente rien et ne reformule rien.
Il sélectionne les phrases des sources les plus proches de la question et les
restitue avec leurs citations. C'est ce qui permet au système de fonctionner
sans aucune clé d'API (spec §19) et de rester testable de façon déterministe.

Il est marqué `degraded = True` : l'interface prévient l'utilisateur que la
synthèse est extractive et qu'un vrai LLM donnerait mieux.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date

from ...core.models import SourceDoc
from .base import LLMProvider, LLMRequest, LLMResult

#: Mots vides français + anglais (liste courte, suffisante pour la pondération)
_STOPWORDS = {
    "a", "au", "aux", "avec", "ce", "ces", "cet", "cette", "dans", "de", "des",
    "du", "elle", "en", "est", "et", "eux", "il", "je", "la", "le", "les",
    "leur", "lui", "ma", "mais", "me", "meme", "mes", "moi", "mon", "ne",
    "nos", "notre", "nous", "on", "ou", "par", "pas", "pour", "qu", "que",
    "qui", "sa", "se", "ses", "son", "sur", "ta", "te", "tes", "toi", "ton",
    "tu", "un", "une", "vos", "votre", "vous", "c", "d", "j", "l", "m", "n",
    "s", "t", "y", "ete", "etee", "etes", "etant", "suis", "es", "sommes",
    "sont", "sera", "the", "of", "and", "to", "in", "is", "it", "for", "on",
    "with", "as", "at", "by", "an", "be", "are", "this", "that", "from",
    "fais", "faire", "moi", "quel", "quelle", "quels", "quelles",
    # Mots outils fréquents : présents partout, ils ne discriminent rien.
    # Sans eux dans cette liste, une page sans rapport passe pour pertinente
    # au seul motif qu'elle contient « entre » et « dans ».
    "entre", "vers", "dans", "sous", "chez", "plus", "moins", "tout", "tous",
    "toute", "toutes", "aussi", "comme", "tres", "bien", "peut", "peuvent",
    "doit", "doivent", "avoir", "etre", "cela", "celui", "celle", "ceux",
    "donc", "alors", "apres", "avant", "depuis", "pendant", "selon", "sans",
    "contre", "leurs", "notre", "votre", "autre", "autres", "encore", "deja",
    "ici", "quand", "comment", "pourquoi", "faut", "font", "ainsi", "chaque",
    "about", "into", "over", "between", "their", "there", "which", "when",
    "where", "what", "your", "our", "more", "most", "also", "than", "then",
}

#: Verbes d'instruction et noms de livrables — à retirer AVANT d'interroger un
#: moteur de recherche : ce sont des consignes pour l'agent, pas le sujet.
_INSTRUCTION_WORDS = {
    "recherche", "recherches", "cherche", "chercher", "trouve", "trouver",
    "fais", "faire", "fait", "faites", "cree", "creer", "genere", "generer",
    "prepare", "preparer", "donne", "donner", "ecris", "ecrire", "redige",
    "rediger", "montre", "montrer", "dis", "dire", "explique", "expliquer",
    "moi", "nous", "stp", "svp", "merci", "peux", "pourrais", "voudrais",
    "pdf", "docx", "doc", "word", "markdown", "txt", "fichier", "fichiers",
    "document", "documents", "rapport", "note", "fiche", "dossier",
    "s'il", "plait", "please", "make", "create", "write", "give",
}

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?…])\s+|\n+")


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def _keywords(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]{3,}", _normalize(text))
    return {w for w in words if w not in _STOPWORDS}


def _is_instruction(word: str) -> bool:
    """Vrai si le mot est une consigne (« fais-moi », « pdf »…) et non le sujet.

    Les composés sont découpés : « fais-moi » est une consigne, « Saint-Denis »
    reste un nom propre.
    """
    parts = [p for p in re.split(r"['-]", _normalize(word)) if p]
    return bool(parts) and all(part in _INSTRUCTION_WORDS for part in parts)


def _trim_stopwords(words: list[str]) -> list[str]:
    """Retire les mots vides en tête et en queue (« … et un » → « … »)."""
    start, end = 0, len(words)
    while start < end and _normalize(words[start]) in _STOPWORDS:
        start += 1
    while end > start and _normalize(words[end - 1]) in _STOPWORDS:
        end -= 1
    return words[start:end]


def subject(question: str) -> str:
    """Ne garde que le sujet de la demande, sans les consignes.

    « Recherche les tarifs des traversées et fais-moi un PDF »
    → « tarifs des traversées »

    Utilisé pour construire les requêtes ET pour juger de la pertinence d'une
    page : sans cela, un article encyclopédique quelconque passe pour pertinent
    parce qu'il contient « recherche » et « PDF » dans son menu.
    """
    words = re.findall(r"[\w'-]+", " ".join(question.split()))
    useful = _trim_stopwords([w for w in words if not _is_instruction(w)])
    return " ".join(useful).strip(" ,.;:!?-")


def _sentences(text: str) -> list[str]:
    out: list[str] = []
    for raw in _SENTENCE_SPLIT.split(text or ""):
        sentence = " ".join(raw.split())
        # Rejette les fragments de navigation et les pavés illisibles.
        if 40 <= len(sentence) <= 400:
            out.append(sentence)
    return out


def _score(sentence: str, keywords: set[str], position: int) -> float:
    words = _keywords(sentence)
    if not words:
        return 0.0
    overlap = len(words & keywords)
    if overlap == 0:
        return 0.0
    # Densité de mots-clés + petit bonus aux premières phrases de la page.
    density = overlap / (len(words) ** 0.5)
    position_bonus = 1.0 / (1.0 + position * 0.15)
    return density * (1.0 + 0.3 * position_bonus)


class OfflineLLM(LLMProvider):
    name = "offline"
    requires_external = False
    degraded = True

    #: nombre de phrases retenues par source
    per_doc = 3
    #: nombre total de phrases dans la synthèse
    total = 10

    def complete(self, request: LLMRequest) -> LLMResult:
        if request.task == "queries":
            text = "\n".join(self._queries(request.question))
        elif request.task == "title":
            text = self._title(request.question)
        elif request.documents:
            text = self._synthesize(request.question, request.documents)
        else:
            text = self._no_source_answer(request.question)

        return LLMResult(
            text=text,
            provider=self.name,
            model="extractif-v1",
            usage={"documents": len(request.documents)},
            degraded=True,
        )

    # -- génération de requêtes de recherche --------------------------------

    def _queries(self, question: str) -> list[str]:
        """Décline la question en quelques requêtes complémentaires.

        Les verbes d'instruction et les noms de livrables sont retirés : envoyer
        « fais-moi un PDF » à un moteur de recherche ramène des convertisseurs
        de fichiers, pas la réponse. C'est une erreur observée en conditions
        réelles lors de la mise au point.
        """
        topic = subject(question)
        keywords = [
            w for w in topic.split() if _normalize(w) not in _STOPWORDS and len(w) > 2
        ]
        core = " ".join(keywords[:8])

        queries = [topic[:200] or " ".join(question.split())[:200]]
        if core and core.lower() != topic.lower():
            queries.append(core)
        if len(keywords) >= 2:
            queries.append(f"{core or topic} {date.today().year}")
            queries.append(f"{core or topic} site officiel")

        seen: set[str] = set()
        return [q for q in queries if q and not (q.lower() in seen or seen.add(q.lower()))]

    def _title(self, question: str) -> str:
        words = " ".join(question.split())
        return (words[:70].rsplit(" ", 1)[0] if len(words) > 70 else words) or "Tâche"

    # -- synthèse extractive ------------------------------------------------

    def _synthesize(self, question: str, documents: list[SourceDoc]) -> str:
        keywords = _keywords(question)
        picked: list[tuple[float, int, str]] = []

        for index, doc in enumerate(documents, start=1):
            scored = [
                (_score(sentence, keywords, position), index, sentence)
                for position, sentence in enumerate(_sentences(doc.content))
            ]
            scored = [item for item in scored if item[0] > 0]
            scored.sort(key=lambda item: item[0], reverse=True)
            picked.extend(scored[: self.per_doc])

        picked.sort(key=lambda item: item[0], reverse=True)
        picked = self._dedupe(picked)[: self.total]

        lines = [
            "**Synthèse extractive** (moteur hors-ligne, sans reformulation) :",
            "",
        ]
        if picked:
            for _, source_index, sentence in picked:
                lines.append(f"- {sentence} [S{source_index}]")
        else:
            lines.append(
                "- Aucune phrase des sources ne recoupe suffisamment la demande. "
                "Les sources ci-dessous sont fournies telles quelles."
            )

        lines += ["", "**Sources :**"]
        for index, doc in enumerate(documents, start=1):
            label = doc.title or doc.domain or doc.url
            lines.append(f"- [S{index}] {label} — {doc.url}")

        covered = {index for _, index, _ in picked}
        missing = [i for i in range(1, len(documents) + 1) if i not in covered]
        if missing:
            lines += [
                "",
                "**Informations manquantes** : les sources "
                + ", ".join(f"[S{i}]" for i in missing)
                + " n'ont rien apporté d'exploitable sur cette question.",
            ]

        lines += [
            "",
            "> ⚠️ Moteur hors-ligne : ces phrases sont **copiées** des sources, pas "
            "rédigées. Configurez `ARA_LLM_PROVIDER` (ollama en local, ou une API) "
            "pour obtenir une vraie synthèse rédigée.",
        ]
        return "\n".join(lines)

    @staticmethod
    def _dedupe(items: list[tuple[float, int, str]]) -> list[tuple[float, int, str]]:
        kept: list[tuple[float, int, str]] = []
        seen: list[set[str]] = []
        for score, index, sentence in items:
            words = _keywords(sentence)
            if any(words and len(words & other) / len(words) > 0.7 for other in seen):
                continue
            kept.append((score, index, sentence))
            seen.append(words)
        return kept

    def _no_source_answer(self, question: str) -> str:
        return (
            "**Moteur hors-ligne** — aucune source n'a été consultée pour cette "
            "demande, et ce moteur ne génère pas de texte : il ne fait qu'extraire "
            "des phrases de documents.\n\n"
            f"Demande reçue : « {' '.join(question.split())[:300]} »\n\n"
            "> Pour une réponse rédigée, configurez un LLM : `ARA_LLM_PROVIDER=ollama` "
            "(gratuit, en local) ou un fournisseur d'API. Voir le README."
        )
