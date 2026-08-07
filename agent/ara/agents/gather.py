"""Collecte de sources — version Phase 1.

Périmètre volontairement limité : plusieurs requêtes, plusieurs moteurs,
récupération des meilleures pages. **Pas encore** de boucle adaptative, de
détection de contradictions ni de relance automatique : c'est le RESEARCH AGENT
de la Phase 2, et la spec §21 interdit de le construire avant que le MVP tourne.

Ce que cette étape garantit déjà :

* jamais une seule source — on vise la diversité de domaines ;
* les URL données par l'utilisateur sont consultées en priorité ;
* un échec de récupération n'interrompt pas la tâche.
"""

from __future__ import annotations

import math
import time

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
MAX_FETCH = 8
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
    """Décline la demande en requêtes de recherche."""
    if plan.budget.search_steps <= 1:
        return [plan.prompt.strip()[:200]]

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


def collect(ctx: TaskContext, plan: Plan, toolbox: ToolBox) -> list[SourceDoc]:
    """Cherche, télécharge et retourne les sources exploitables."""
    ctx.stage(Stage.RESEARCH, Status.RUNNING, "Préparation des recherches…")

    docs: list[SourceDoc] = []
    seen: set[str] = set()
    # Pertinence jugée sur le sujet seul : « pdf », « recherche »… sont des
    # consignes, et les retenir ferait passer n'importe quelle page pour bonne.
    keywords = _stems(subject(plan.prompt))
    rejected = 0

    # 1. Les URL fournies par l'utilisateur passent en premier.
    for url in plan.urls[:MAX_FETCH]:
        payload = toolbox.call("fetch_page", url=url)
        doc = _to_doc(payload)
        if doc.content:
            docs.append(doc)
            seen.add(canonical(doc.url))

    if plan.needs_research:
        queries = build_queries(ctx, plan)
        ctx.journal.add_summary(f"plan de recherche : {len(queries)} requête(s)")

        for index, query in enumerate(queries):
            if plan.budget.remaining_searches <= 0 or len(docs) >= MAX_FETCH:
                break
            ctx.check_deadline()
            # Politesse : enchaîner les requêtes sans pause fait répondre 429
            # aux moteurs publics (constaté sur l'API Wikipédia).
            if index and ctx.settings.search_delay > 0:
                time.sleep(ctx.settings.search_delay)
            plan.budget.consume_search()
            ctx.stage(
                Stage.RESEARCH,
                Status.RUNNING,
                f"Recherche : {query}",
                query=query,
                step=plan.budget.used_searches,
                total=plan.budget.search_steps,
            )

            try:
                results = toolbox.call("web_search", query=query, limit=6)
            except AraError as exc:
                ctx.notice(f"Recherche impossible ({query}) : {exc}")
                continue

            fetched = 0
            for result in results:
                if fetched >= FETCH_PER_QUERY or len(docs) >= MAX_FETCH:
                    break
                url = result.get("url", "")
                key = canonical(url)
                if not url or key in seen:
                    continue
                seen.add(key)

                payload = toolbox.call("fetch_page", url=url)
                doc = _to_doc(payload, snippet=result.get("snippet", ""),
                              engine=result.get("engine", ""))
                if not doc.content:
                    continue
                if not _is_relevant(doc, keywords):
                    rejected += 1
                    ctx.journal.add_step("reject", f"hors sujet : {doc.domain}", url=url)
                    continue
                docs.append(doc)
                fetched += 1
                ctx.bus.log(f"Source retenue : {doc.domain}", url=url)

    message = f"{len(docs)} source(s) retenue(s)"
    if docs:
        message += f" sur {len({d.domain for d in docs})} domaine(s)"
    if rejected:
        message += f" · {rejected} écartée(s) hors sujet"

    ctx.stage(
        Stage.RESEARCH,
        Status.DONE if docs else Status.SKIPPED,
        message,
        sources=[doc.to_dict() for doc in docs],
        rejected=rejected,
    )
    return docs


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
