"""Collecte de sources : recherche, téléchargement, filtrage de pertinence.

Ce module ne décide de rien — il exécute. C'est le RESEARCH AGENT
(`research.py`) qui choisit quoi chercher, quand relancer et quand s'arrêter.

Ce que la collecte garantit :

* jamais une seule source — on vise la diversité de domaines ;
* les URL données par l'utilisateur sont consultées en priorité ;
* les pages hors sujet sont écartées avant de polluer l'analyse ;
* un échec de récupération n'interrompt jamais la tâche.
"""

from __future__ import annotations

import math
import time
from collections import Counter

from ..core.context import TaskContext
from ..core.errors import AraError
from ..core.events import Stage, Status
from ..core.models import SourceDoc
from ..core.urls import canonical
from ..providers.llm.base import LLMRequest
from ..providers.llm.offline import _keywords, subject
from ..tools.registry import ToolBox
from .planner import Plan

#: Nombre de pages effectivement téléchargées par requête
FETCH_PER_QUERY = 3
#: Plafond de pages téléchargées pour une tâche
MAX_FETCH = 10
#: Pages retenues par domaine. Dix pages d'un même site ne font pas dix
#: sources : constaté en réel avec 10 sources pour 1 seul domaine.
MAX_PER_DOMAIN = 3
#: Nombre minimal de mots-clés de la question qu'une page doit contenir
MIN_KEYWORD_HITS = 2
#: …et au moins cette proportion des mots-clés, pour les questions détaillées
MIN_KEYWORD_RATIO = 0.34


def _stems(text: str) -> set[str]:
    """Mots-clés avec pluriel simple retiré (« tarifs » ≈ « tarif »).

    Sans cette normalisation, une page qui écrit « tarif » au singulier passe
    pour hors sujet face à une question qui dit « tarifs ».
    """
    return {
        word[:-1] if len(word) > 4 and word.endswith("s") else word
        for word in _keywords(text)
    }


def _is_relevant(doc: SourceDoc, keywords: set[str]) -> bool:
    """Écarte les pages hors sujet ramenées par les moteurs.

    Sans ce filtre, une requête contenant « Grande Comore » remonte des pages
    sur la « grande » n'importe quoi : constaté en conditions réelles avec un
    article encyclopédique sans rapport. Le filtre ne s'applique que si la
    question fournit assez de mots-clés distinctifs pour être discriminante.

    Plus la question est précise, plus on exige de recouvrement : deux mots
    communs à une question de dix mots-clés ne prouvent rien.
    """
    if len(keywords) < 3:
        return True
    needed = max(MIN_KEYWORD_HITS, math.ceil(MIN_KEYWORD_RATIO * len(keywords)))
    return len(keywords & _stems(f"{doc.title} {doc.content}")) >= needed


def build_queries(ctx: TaskContext, plan: Plan) -> list[str]:
    """Décline la demande en requêtes de recherche initiales."""
    if plan.budget.search_steps <= 1:
        return [subject(plan.prompt)[:200] or plan.prompt.strip()[:200]]

    try:
        result = ctx.llm.complete(
            LLMRequest(
                task="queries",
                question=plan.prompt,
                instructions=(
                    "Propose des requêtes de recherche web, une par ligne, sans "
                    "numérotation ni commentaire. Elles doivent couvrir des angles "
                    "différents de la demande."
                ),
                max_tokens=200,
            )
        )
        queries = [
            line.strip(" -•\t").strip()
            for line in result.text.splitlines()
            if 3 < len(line.strip()) < 200
        ]
    except AraError as exc:
        ctx.journal.add_error(f"génération de requêtes : {exc}")
        queries = []

    if not queries:
        queries = [plan.prompt.strip()[:200]]
    return queries[: plan.budget.search_steps]


class SourceCollector:
    """Accumule des sources au fil des cycles de recherche.

    L'état (`seen`) est conservé entre les cycles : une relance ne doit pas
    retélécharger ce qui a déjà été lu, sinon la boucle tourne sur elle-même.
    """

    def __init__(
        self,
        ctx: TaskContext,
        toolbox: ToolBox,
        plan: Plan,
        *,
        relevance=None,
    ) -> None:
        self.ctx = ctx
        self.toolbox = toolbox
        self.plan = plan
        #: Filtre de pertinence additionnel, injecté par RESEARCH-V2.
        #: `None` = comportement de la baseline, inchangé au bit près : c'est
        #: ce qui permet à H1 et H2 de rester reproductibles.
        self.relevance = relevance
        # Pertinence jugée sur le sujet seul : « pdf », « recherche »… sont des
        # consignes, et les retenir ferait passer n'importe quelle page pour bonne.
        self.keywords = _stems(subject(plan.prompt))
        self.docs: list[SourceDoc] = []
        self.seen: set[str] = set()
        self.per_domain: Counter[str] = Counter()
        self.rejected = 0
        self.searches = 0

    @property
    def saturated(self) -> bool:
        return len(self.docs) >= MAX_FETCH

    def fetch_urls(self, urls: list[str]) -> list[SourceDoc]:
        """Consulte les adresses fournies par l'utilisateur, sans filtrage.

        S'il donne une URL, il la veut : on ne lui oppose pas notre score de
        pertinence.
        """
        new: list[SourceDoc] = []
        for url in urls[:MAX_FETCH]:
            if self.saturated:
                break
            key = canonical(url)
            if key in self.seen:
                continue
            self.seen.add(key)
            doc = _to_doc(self.toolbox.call("fetch_page", url=url))
            if doc.content:
                self.per_domain[doc.domain] += 1
                self.docs.append(doc)
                new.append(doc)
        return new

    def run_query(self, query: str, *, limit: int = 6) -> list[SourceDoc]:
        """Exécute une requête et retourne les nouvelles sources retenues."""
        self.ctx.check_deadline()
        # Politesse : enchaîner les requêtes sans pause fait répondre 429
        # aux moteurs publics (constaté sur l'API Wikipédia).
        if self.searches and self.ctx.settings.search_delay > 0:
            time.sleep(self.ctx.settings.search_delay)
        self.searches += 1

        try:
            results = self.toolbox.call("web_search", query=query, limit=limit)
        except AraError as exc:
            self.ctx.notice(f"Recherche impossible ({query}) : {exc}")
            return []

        new: list[SourceDoc] = []
        for result in results:
            if len(new) >= FETCH_PER_QUERY or self.saturated:
                break
            url = result.get("url", "")
            key = canonical(url)
            if not url or key in self.seen:
                continue
            self.seen.add(key)

            doc = _to_doc(
                self.toolbox.call("fetch_page", url=url),
                snippet=result.get("snippet", ""),
                engine=result.get("engine", ""),
            )
            if not doc.content:
                continue
            pertinent = _is_relevant(doc, self.keywords)
            if self.relevance is not None:
                pertinent = self.relevance(doc, pertinent)
            if not pertinent:
                self.rejected += 1
                self.ctx.journal.add_step("reject", f"hors sujet : {doc.domain}", url=url)
                continue
            if self.per_domain[doc.domain] >= MAX_PER_DOMAIN:
                self.ctx.journal.add_step(
                    "reject", f"quota de domaine atteint : {doc.domain}", url=url
                )
                continue

            self.per_domain[doc.domain] += 1
            self.docs.append(doc)
            new.append(doc)
            self.ctx.bus.log(f"Source retenue : {doc.domain}", url=url)
        return new

    def summary(self) -> str:
        message = f"{len(self.docs)} source(s) retenue(s)"
        if self.docs:
            message += f" sur {len({d.domain for d in self.docs})} domaine(s)"
        if self.rejected:
            message += f" · {self.rejected} écartée(s) hors sujet"
        return message


def judge_difficulty(question: str, docs: list[SourceDoc]) -> tuple[str, str]:
    """Constate la difficulté d'après ce que la recherche a ramené.

    Retourne ``(verdict, motif)`` avec un verdict parmi ``difficile``,
    ``suffisant`` et ``indetermine``.

    Le principe est simple et vérifiable : la question réclame une grandeur
    d'un certain type — un prix, une durée, une heure, un pourcentage. Soit
    une source la donne, soit aucune ne la donne. Dans le second cas, la
    question était plus difficile que sa formulation ne le laissait croire, et
    le budget doit monter.

    Volontairement conservateur : sans aspect chiffré identifiable dans la
    question, on répond ``indetermine`` plutôt que d'inventer un verdict. Un
    contrôleur qui tranche au hasard est pire qu'un budget fixe.
    """
    from ..analysis.coverage import ASPECTS, detect_aspects
    from ..analysis.facts import extract_facts

    aspects = detect_aspects(question)
    if not aspects:
        return "indetermine", "la question ne réclame aucune grandeur identifiable"
    if not docs:
        return "difficile", "aucune source exploitable"

    attendus = {ASPECTS[aspect][0] for aspect in aspects}
    trouves: set[str] = set()
    for index, doc in enumerate(docs, start=1):
        for fact in extract_facts(f"{doc.title} {doc.content}", index, max_facts=120):
            trouves.add(fact.kind)

    manquants = sorted(attendus - trouves)
    if not manquants:
        return "suffisant", "toutes les grandeurs demandées figurent dans les sources"
    if len(manquants) == len(attendus):
        return (
            "difficile",
            "aucune source ne donne " + ", ".join(manquants) + " : "
            "la réponse n'est pas là où l'on cherchait",
        )
    return "difficile", "il manque encore : " + ", ".join(manquants)


def collect(ctx: TaskContext, plan: Plan, toolbox: ToolBox) -> list[SourceDoc]:
    """Collecte en une passe, avec révision du budget **sur preuve**.

    Deux comportements dans une seule fonction, selon `plan.adaptive_budget` :

    * à ``False``, le budget est dépensé tel quel, sans jamais être révisé.
      C'est la stratégie **FIXED** du laboratoire, et c'est ce qui en fait un
      témoin honnête : un témoin qui s'adapte ne mesure plus rien.
    * à ``True`` (défaut), le contrôleur regarde après chaque recherche si ce
      qui est demandé a été trouvé, puis monte ou s'arrête. C'est la
      correction apportée après H2, qui avait montré un contrôleur incapable
      de distinguer une question facile d'une question profonde.
    """
    ctx.stage(Stage.RESEARCH, Status.RUNNING, "Préparation des recherches…")
    collector = SourceCollector(ctx, toolbox, plan)
    collector.fetch_urls(plan.urls)

    if plan.needs_research:
        queries = build_queries(ctx, plan)
        ctx.journal.add_summary(f"plan de recherche : {len(queries)} requête(s)")
        index = 0
        while index < len(queries):
            if plan.budget.remaining_searches <= 0 or collector.saturated:
                break
            query = queries[index]
            index += 1
            plan.budget.consume_search()
            ctx.stage(
                Stage.RESEARCH,
                Status.RUNNING,
                f"Recherche : {query}",
                query=query,
                step=plan.budget.used_searches,
                total=plan.budget.search_steps,
            )
            collector.run_query(query)

            if not plan.adaptive_budget:
                continue

            verdict, motif = judge_difficulty(plan.prompt, collector.docs)
            action = plan.budget.revise(verdict, motif)
            if action != "aucune":
                ctx.journal.add_step(
                    "revise",
                    f"{action} — {motif}",
                    complexity=plan.budget.complexity.value,
                    searches=plan.budget.search_steps,
                )
            if verdict == "suffisant":
                # « INFORMATION SUFFISANTE → arrêt » : le reste du budget n'est
                # pas un dû, c'est un plafond.
                plan.budget.stop_code = "information_suffisante"
                break
            if verdict == "difficile" and index >= len(queries):
                # Le budget vient de monter mais il n'y a plus de requête à
                # jouer : on en fabrique une, ciblée sur ce qui manque.
                relance = f"{subject(plan.prompt)[:120]} officiel".strip()
                if relance and relance not in queries:
                    queries.append(relance)

        if plan.adaptive_budget and not plan.budget.stop_code:
            # La collecte s'est arrêtée sans avoir trouvé : dire lequel des
            # deux murs a été touché, plutôt que de laisser croire à une
            # décision qui n'a pas eu lieu.
            plan.budget.stop_code = (
                "limite_budget"
                if plan.budget.remaining_searches <= 0 or collector.saturated
                else "manque_information"
            )

    ctx.stage(
        Stage.RESEARCH,
        Status.DONE if collector.docs else Status.SKIPPED,
        collector.summary(),
        sources=[doc.to_dict() for doc in collector.docs],
        rejected=collector.rejected,
    )
    return collector.docs


def _to_doc(payload: dict, *, snippet: str = "", engine: str = "") -> SourceDoc:
    return SourceDoc(
        url=payload.get("url", ""),
        title=payload.get("title", ""),
        text=payload.get("text", ""),
        snippet=payload.get("snippet") or snippet,
        engine=payload.get("engine") or engine,
        fetched=bool(payload.get("fetched")),
        error=payload.get("error", ""),
    )
