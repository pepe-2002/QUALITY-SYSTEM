"""RESEARCH AGENT — boucle de recherche adaptative (spec §2, §3, §4).

    QUESTION
      ↓
    PLAN DE RECHERCHE
      ↓
    RECHERCHE ──────────────┐
      ↓                     │
    ANALYSE                 │
      ↓                     │
    INFORMATIONS MANQUANTES ?
      ↓ OUI ────────────────┘  (relance ciblée, budget augmenté)
      ↓ NON
    VÉRIFICATION
      ↓
    RÉPONSE

Ce qui distingue cette boucle d'une simple répétition de recherches :

* **elle relance pour une raison précise** — un aspect non couvert, un mot-clé
  absent, une valeur non confirmée, ou deux sources qui se contredisent — et
  la requête de relance découle de cette raison ;
* **elle sait s'arrêter**, et dit pourquoi : plus rien ne manque, budget
  épuisé, plus aucune piste, ou plafond de cycles atteint ;
* **elle sait aussi réduire la voilure** : si le premier cycle répond à tout,
  le budget est ramené vers le bas au lieu d'être dépensé jusqu'au bout.

Aucune de ces décisions ne dépend du LLM : elles reposent sur des faits
extraits et comparés (`ara.analysis`), donc reproductibles et testables.
"""

from __future__ import annotations

import unicodedata

from ..analysis.compare import find_contradictions
from ..analysis.coverage import Gap, find_gaps
from ..analysis.facts import extract_facts
from ..analysis.report import ResearchReport
from ..analysis.validate import ContradictionValidator
from ..core.context import TaskContext
from ..core.events import Stage, Status
from ..core.models import SourceDoc
from ..providers.llm.offline import subject
from ..tools.registry import ToolBox
from .gather import SourceCollector, build_queries
from .planner import Plan

#: Plafond de cycles, indépendamment du budget de recherches.
#: Sans lui, une question mal posée pourrait relancer indéfiniment.
MAX_CYCLES = 4
#: Requêtes de relance générées par cycle
FOLLOWUP_PER_CYCLE = 2
#: Requêtes lancées au premier cycle.
#: Règle posée par le propriétaire du projet : **chercher uniquement lorsque
#: c'est nécessaire**. On part donc du minimum — une requête — et on ne dépense
#: davantage qu'après avoir constaté un manque. Le budget de complexité est un
#: plafond, jamais une consommation obligatoire : sinon une question simple
#: coûte aussi cher qu'une question difficile, et l'adaptatif ne sert à rien.
INITIAL_QUERIES = 1

#: Terme de relance selon la nature de la contradiction
_CONTRADICTION_HINT = {
    "money": "tarif officiel",
    "duration": "durée officielle",
    "distance": "distance exacte",
    "percent": "chiffres officiels",
    "weight": "limite officielle",
}


def _key(query: str) -> str:
    text = unicodedata.normalize("NFKD", query.lower())
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).split())


def followup_queries(
    topic: str,
    gaps: list[Gap],
    contradictions: list,
    used: set[str],
    *,
    chased: set[str] | None = None,
    limit: int = FOLLOWUP_PER_CYCLE,
) -> list[tuple[str, str]]:
    """Construit les requêtes de relance et la raison de chacune.

    Retourne des couples `(requête, raison)` : la raison est affichée à
    l'utilisateur et journalisée, pour qu'une relance ne soit jamais opaque.

    `used` est seulement **consulté** : c'est l'exécution de la requête qui
    l'y inscrit. Marquer ici reviendrait à interdire l'exécution de ce qu'on
    vient de proposer.
    """
    chased = chased if chased is not None else set()
    candidates: list[tuple[str, str]] = []

    # Une contradiction prime : c'est le défaut le plus grave d'une synthèse.
    # Mais on ne cherche à trancher un même désaccord qu'**une fois** : s'il
    # persiste après une recherche ciblée, chercher davantage ne le résoudra
    # pas — il faut le signaler et s'arrêter.
    for contradiction in contradictions:
        signature = f"{contradiction.kind}:{contradiction.unit}"
        if signature in chased:
            continue
        chased.add(signature)
        hint = _CONTRADICTION_HINT.get(contradiction.kind, "source officielle")
        sujet = " ".join(sorted(contradiction.shared)[:2])
        candidates.append(
            (
                f"{topic} {sujet} {hint}".strip(),
                f"contradiction sur {contradiction.unit} entre "
                + ", ".join(f"[S{s}]" for s in contradiction.sources),
            )
        )

    for gap in gaps:
        candidates.append((f"{topic} {gap.hint}".strip(), gap.label))

    out: list[tuple[str, str]] = []
    proposed: set[str] = set()
    for query, reason in candidates:
        query = " ".join(query.split())[:200]
        key = _key(query)
        if not query or key in used or key in proposed:
            continue
        proposed.add(key)
        out.append((query, reason))
        if len(out) >= limit:
            break
    return out


class ResearchAgent:
    """Conduit la boucle de recherche jusqu'à une réponse ou un arrêt motivé."""

    def __init__(self, ctx: TaskContext, toolbox: ToolBox, plan: Plan) -> None:
        self.ctx = ctx
        self.toolbox = toolbox
        self.plan = plan
        self.collector = SourceCollector(ctx, toolbox, plan)
        self.report = ResearchReport(question=plan.prompt)
        # Requête de relance = sujet **court** + piste. Reprendre la question
        # entière donnait des requêtes comme « hauteur de la tour Eiffel et en
        # année a-t-elle été construite ans tour durée officielle » : illisible
        # pour un moteur.
        self.topic = " ".join(subject(plan.prompt).split()[:8])
        self._used: set[str] = set()
        #: désaccords déjà cherchés (famille:unité) — on n'y revient pas
        self._chased: set[str] = set()
        #: requêtes initiales non consommées, gardées comme pistes de repli
        self._spare: list[str] = []

    # -- boucle ------------------------------------------------------------

    def run(self) -> tuple[list[SourceDoc], ResearchReport]:
        ctx, plan = self.ctx, self.plan
        ctx.stage(Stage.RESEARCH, Status.RUNNING, "Plan de recherche…")

        self.collector.fetch_urls(plan.urls)
        pending = self._initial_queries()

        for cycle in range(1, MAX_CYCLES + 1):
            self.report.iterations = cycle
            self._search(cycle, pending)
            self._analyze(cycle)

            stop = self._should_stop(cycle)
            if stop:
                self.report.stopped_because = stop
                break

            # Un manque justifie de dépenser plus : on augmente le budget
            # AVANT de constater qu'il est épuisé, sinon aucune relance
            # n'aurait jamais lieu.
            escalated = plan.budget.escalate("information manquante")
            if plan.budget.remaining_searches <= 0:
                self.report.stopped_because = (
                    f"budget de recherche épuisé ({plan.budget.used_searches} recherches, "
                    f"plafond {plan.budget.max_search_steps})"
                )
                break

            relances = followup_queries(
                self.topic,
                self.report.gaps,
                self.report.contradictions,
                self._used,
                chased=self._chased,
            )
            if not relances:
                # « Chercher uniquement lorsque c'est nécessaire » : sans manque
                # ni désaccord non tranché, il n'y a aucune raison de relancer.
                # Les requêtes de départ non explorées ne sont PAS une raison —
                # elles ne font que compléter une relance déjà justifiée.
                self.report.stopped_because = (
                    "aucun manque et aucun désaccord à trancher : "
                    "rien ne justifie une recherche de plus"
                )
                break

            relances += [
                (query, "piste de départ non explorée")
                for query in self._spare
                if _key(query) not in self._used
            ][: max(0, FOLLOWUP_PER_CYCLE - len(relances))]

            reasons = " · ".join(reason for _query, reason in relances)
            ctx.journal.add_step(
                "escalate",
                f"cycle {cycle + 1} : {reasons}",
                complexity=plan.budget.complexity.value,
                escalated=escalated,
            )
            ctx.stage(
                Stage.RESEARCH,
                Status.RUNNING,
                f"Relance (cycle {cycle + 1}) — {reasons}",
                cycle=cycle + 1,
                reasons=[reason for _q, reason in relances],
            )
            pending = [query for query, _reason in relances]
        else:
            self.report.stopped_because = f"plafond de {MAX_CYCLES} cycles atteint"

        self._finish()
        return self.collector.docs, self.report

    # -- étapes ------------------------------------------------------------

    def _initial_queries(self) -> list[str]:
        if not self.plan.needs_research:
            return []
        queries = build_queries(self.ctx, self.plan)
        first, self._spare = queries[:INITIAL_QUERIES], queries[INITIAL_QUERIES:]
        self.ctx.journal.add_summary(
            f"plan de recherche : {len(first)} requête(s) au départ, "
            f"{len(self._spare)} en réserve"
        )
        return first

    def _search(self, cycle: int, queries: list[str]) -> None:
        plan, ctx = self.plan, self.ctx
        for query in queries:
            if plan.budget.remaining_searches <= 0 or self.collector.saturated:
                break
            if _key(query) in self._used:
                continue
            self._used.add(_key(query))
            plan.budget.consume_search()
            self.report.queries.append(query)

            ctx.stage(
                Stage.RESEARCH,
                Status.RUNNING,
                f"Cycle {cycle} · recherche : {query}",
                query=query,
                cycle=cycle,
                step=plan.budget.used_searches,
                total=plan.budget.search_steps,
            )
            self.collector.run_query(query)

    def _analyze(self, cycle: int) -> None:
        """Extrait les faits, confronte les sources, recense les manques."""
        ctx = self.ctx
        ctx.check_deadline()
        ctx.stage(
            Stage.ANALYSIS, Status.RUNNING, f"Cycle {cycle} · comparaison des sources…"
        )

        docs = self.collector.docs
        facts = []
        for index, doc in enumerate(docs, start=1):
            facts.extend(extract_facts(doc.content, index))

        # Deux pages d'un même site ne sont pas deux sources indépendantes.
        domains = {index: doc.domain for index, doc in enumerate(docs, start=1)}

        self.report.docs = docs
        self.report.facts = facts
        self.report.domains_by_source = domains
        # Étage 1 : détection déterministe, réglée pour le rappel.
        candidates = find_contradictions(
            facts, focus=self.collector.keywords, domains=domains
        )
        # Étage 2 : agent contexte — « est-ce une vraie contradiction ? »
        validator = ContradictionValidator(ctx.llm, question=self.plan.prompt)
        self.report.anomalies = validator.validate(candidates, docs)
        self.report.dismissed = validator.rejected

        for anomaly, verdict in validator.rejected:
            ctx.journal.add_step(
                "dismiss", f"écart expliqué : {verdict.reason}", by=verdict.decided_by
            )
        self.report.gaps = find_gaps(
            self.plan.prompt,
            docs,
            facts,
            subject_keywords=self.collector.keywords,
            domains=domains,
        )

        ctx.journal.add_step(
            "analysis",
            f"cycle {cycle} : {len(facts)} fait(s), "
            f"{len(self.report.anomalies)} contradiction(s) validée(s), "
            f"{len(validator.rejected)} écart(s) expliqué(s), "
            f"{len(self.report.gaps)} manque(s)",
            sources=len(docs),
        )

        for item in self.report.anomalies:
            ctx.bus.log(
                f"CONTRADICTION DÉTECTÉE — {item.describe()}",
                kind="contradiction",
                contradiction=item.to_dict(),
            )

        ctx.stage(
            Stage.ANALYSIS,
            Status.DONE,
            f"Cycle {cycle} · {len(docs)} source(s), {len(facts)} fait(s) chiffré(s), "
            f"{len(self.report.anomalies)} contradiction(s), "
            f"{len(validator.rejected)} écart(s) expliqué(s), "
            f"{len(self.report.gaps)} manque(s)",
            cycle=cycle,
            contradictions=[item.to_dict() for item in self.report.anomalies],
            gaps=[g.to_dict() for g in self.report.gaps],
        )

    def _should_stop(self, cycle: int) -> str:
        """Retourne la raison d'arrêt, ou une chaîne vide pour continuer."""
        plan = self.plan
        report = self.report

        if not report.gaps and not report.contradictions:
            if report.docs:
                # Tâche plus simple que l'estimation : on rend le budget.
                if cycle == 1 and plan.budget.remaining_searches > 0:
                    plan.budget.de_escalate("réponse complète dès le premier cycle")
                    self.ctx.journal.add_step(
                        "de-escalate",
                        f"budget réduit à {plan.budget.complexity.value}",
                    )
                return "aucune information manquante, aucune contradiction"
            if not plan.needs_research:
                return "recherche non nécessaire"

        if not plan.needs_research:
            return "recherche non nécessaire"
        if self.collector.saturated:
            return "nombre maximal de sources atteint"
        if cycle >= MAX_CYCLES:
            return f"plafond de {MAX_CYCLES} cycles atteint"
        return ""

    def _finish(self) -> None:
        ctx, report = self.ctx, self.report
        ctx.journal.iterations = report.iterations
        ctx.journal.add_summary(
            f"recherche : {report.iterations} cycle(s), "
            f"{len(report.queries)} requête(s), arrêt — {report.stopped_because}"
        )

        ctx.stage(
            Stage.RESEARCH,
            Status.DONE if report.docs else Status.SKIPPED,
            f"{self.collector.summary()} · {report.iterations} cycle(s) · "
            f"arrêt : {report.stopped_because}",
            sources=[doc.to_dict() for doc in report.docs],
            rejected=self.collector.rejected,
            report=report.to_dict(),
        )


def run_research(
    ctx: TaskContext, plan: Plan, toolbox: ToolBox
) -> tuple[list[SourceDoc], ResearchReport]:
    """Raccourci : exécute la boucle de recherche adaptative."""
    return ResearchAgent(ctx, toolbox, plan).run()
