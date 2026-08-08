"""RESEARCH-V2 — nouvelle version du Research Agent, à côté de la baseline.

Pourquoi une version séparée plutôt qu'une correction
------------------------------------------------------
`research.py` est le moteur qui a produit H1 et H2. Le corriger rendrait ces
résultats irreproductibles : les chiffres publiés ne correspondraient plus au
code du dépôt. Il est donc **gelé définitivement**, et cette version-ci vit à
côté, avec son propre identifiant.

C'est la même discipline que pour le contrôleur (ADAPTIVE-V1 / V2). Elle coûte
un peu de duplication ; elle évite de réécrire l'histoire.

Ce que V2 corrige, et rien d'autre
----------------------------------
Trois défauts observés en conditions réelles, sur :

> « Quel est le tarif officiel de la traversée en vedette entre la Grande
> Comore et Mohéli ? »

1. **Requêtes malformées** — le sujet extrait finissait sur une préposition et
   le complément répétait ce qu'il contenait déjà : « …en vedette entre tarif
   officiel ». Corrigé par `compose_query`.
2. **Mots-clés orphelins** — un mot manquant devenait un complément de requête
   à lui seul : « …entre grande », « …entre comore ». Corrigé par `is_orphan`,
   et par le fait qu'une requête garde toujours le sujet nettoyé.
3. **Pertinence purement lexicale** — une page bretonne contenant
   « traversée », « vedette » et « tarif » passait le filtre. Corrigé par
   l'exigence d'au moins un **terme distinctif** de la question.

Aucune liste noire nulle part : ce sont les mécanismes qui changent.
"""

from __future__ import annotations

from ..core.context import TaskContext
from ..core.events import Stage, Status
from ..core.models import SourceDoc
from ..tools.registry import ToolBox
from .gather import SourceCollector
from .planner import Plan
from .queries import compose_query, is_on_topic, is_orphan
from .research import FOLLOWUP_PER_CYCLE, MAX_CYCLES, ResearchAgent, _key
from .research import ResearchReport

#: Identifiant de version, cité par les rapports d'expérience.
RESEARCH_VERSION = "RESEARCH-V2 (2026-08-08)"
#: Identifiant de la version gelée, pour mémoire.
BASELINE_VERSION = "RESEARCH-BASELINE (moteur de H1 et H2 — gelé)"


def followup_queries_v2(
    topic: str,
    gaps,
    contradictions,
    used: set[str],
    *,
    chased: set[str] | None = None,
    limit: int = FOLLOWUP_PER_CYCLE,
) -> list[tuple[str, str]]:
    """Relances propres : sujet nettoyé + complément qui apporte quelque chose.

    Même rôle que `research.followup_queries`, trois différences :

    * le sujet passe par `compose_query`, donc plus de fragment grammatical ;
    * un complément orphelin (mot générique isolé) est écarté au lieu de
      produire une requête ;
    * une requête qui, après nettoyage, ne garde pas assez de mots porteurs de
      sens n'est pas émise du tout.
    """
    chased = chased if chased is not None else set()
    candidats: list[tuple[str, str]] = []

    # 1. Les désaccords d'abord : c'est ce qui met une réponse en danger.
    for contradiction in contradictions:
        signature = f"{contradiction.kind}:{contradiction.unit}"
        if signature in chased:
            continue
        chased.add(signature)
        candidats.append(
            (
                compose_query(topic, "source officielle"),
                f"désaccord sur {contradiction.kind} à trancher",
            )
        )

    # 2. Puis les manques, du plus grave au plus discret.
    for gap in gaps:
        if is_orphan(gap.hint, topic):
            # Défaut 2 : « grande », « comore » — un mot générique isolé
            # n'oriente rien et fait dériver la recherche.
            continue
        candidats.append((compose_query(topic, gap.hint), gap.label))

    sortie: list[tuple[str, str]] = []
    proposees: set[str] = set()
    for query, reason in candidats:
        query = " ".join(query.split())
        cle = _key(query)
        if not query or cle in used or cle in proposees:
            continue
        proposees.add(cle)
        sortie.append((query, reason))
        if len(sortie) >= limit:
            break
    return sortie


class TopicRelevance:
    """Filtre de pertinence contextuelle, injecté dans le collecteur.

    La baseline juge la pertinence par recouvrement de mots-clés. V2 ajoute une
    condition : la page doit contenir au moins un **terme distinctif** de la
    question — un nom propre, ou à défaut un mot rare. Les mots qui décrivent
    un genre de chose (« traversée », « tarif ») ne suffisent plus à établir
    qu'on parle bien de *cette* chose-là.
    """

    def __init__(self, question: str) -> None:
        self.question = question

    def __call__(self, doc: SourceDoc, baseline_ok: bool) -> bool:
        if not baseline_ok:
            return False
        return is_on_topic(f"{doc.title} {doc.content}", self.question)


class ResearchAgentV2(ResearchAgent):
    """Le Research Agent corrigé. Même boucle, décisions plus propres."""

    version = RESEARCH_VERSION

    def __init__(self, ctx: TaskContext, toolbox: ToolBox, plan: Plan) -> None:
        super().__init__(ctx, toolbox, plan)
        # Le sujet sert de base à toutes les relances : on le nettoie une fois.
        self.topic = compose_query(self.topic) or self.topic
        self.collector = SourceCollector(
            ctx, toolbox, plan, relevance=TopicRelevance(plan.prompt)
        )
        #: sources écartées pour cause de hors-sujet contextuel
        self.off_topic = 0

    def run(self) -> tuple[list[SourceDoc], ResearchReport]:
        """Boucle identique à la baseline, relances construites autrement.

        La boucle n'est pas le sujet de cette version : elle est reprise telle
        quelle pour que la comparaison porte sur les trois corrections, et sur
        elles seules.
        """
        ctx, plan = self.ctx, self.plan
        ctx.stage(Stage.RESEARCH, Status.RUNNING, "Plan de recherche…")

        self.collector.fetch_urls(plan.urls)
        pending = self._initial_queries()

        for cycle in range(1, MAX_CYCLES + 1):
            self.report.iterations = cycle
            self._search(cycle, pending)
            self._analyze(cycle)

            stop, code = self._should_stop(cycle)
            if stop:
                self.report.stopped_because = stop
                self.report.stop_code = code
                break

            escalated = plan.budget.escalate("information manquante")
            if plan.budget.remaining_searches <= 0:
                self.report.stopped_because = (
                    f"budget de recherche épuisé ({plan.budget.used_searches} recherches, "
                    f"plafond {plan.budget.max_search_steps})"
                )
                self.report.stop_code = "limite_budget"
                break

            relances = followup_queries_v2(
                self.topic,
                self.report.gaps,
                self.report.contradictions,
                self._used,
                chased=self._chased,
            )
            if not relances:
                if self.report.gaps:
                    manques = ", ".join(gap.label for gap in self.report.gaps[:2])
                    self.report.stopped_because = (
                        f"il manque encore quelque chose ({manques}), mais aucune "
                        "relance exploitable : chercher plus ne servirait à rien"
                    )
                    self.report.stop_code = "manque_information"
                else:
                    self.report.stopped_because = (
                        "aucun manque et aucun désaccord à trancher : "
                        "rien ne justifie une recherche de plus"
                    )
                    self.report.stop_code = (
                        "contradiction_tranchee" if self._chased else "information_suffisante"
                    )
                break

            # Les pistes de départ non explorées complètent une relance déjà
            # justifiée — elles ne la déclenchent jamais.
            relances += [
                (query, "piste de départ non explorée")
                for query in self._spare
                if _key(query) not in self._used and query
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
            self.report.stop_code = "limite_budget"

        self._finish()
        return self.collector.docs, self.report


def run_research_v2(ctx: TaskContext, plan: Plan, toolbox: ToolBox):
    """Point d'entrée symétrique de `research.run_research`."""
    return ResearchAgentV2(ctx, toolbox, plan).run()


__all__ = [
    "BASELINE_VERSION",
    "RESEARCH_VERSION",
    "ResearchAgentV2",
    "TopicRelevance",
    "followup_queries_v2",
    "run_research_v2",
]
