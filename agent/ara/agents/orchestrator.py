"""Orchestrateur : décide quel agent et quels outils utiliser (spec §1).

Pipeline Phase 1, exactement celui que l'interface affiche (spec §14) :

    TÂCHE → RECHERCHE → ANALYSE → CRÉATION → VÉRIFICATION → RÉSULTAT

Chaque étape peut être **sautée** : une salutation ne déclenche ni recherche ni
document. C'est le raisonnement adaptatif du MVP — modeste, mais réel.

Toute erreur maîtrisée est capturée : une tâche rend toujours un résultat, même
partiel, et écrit toujours son journal.
"""

from __future__ import annotations

import time
import uuid

from ..core.complexity import Complexity
from ..core.config import Settings, get_settings
from ..core.context import TaskContext
from ..core.errors import AraError, ApprovalRequired, BudgetExceeded
from ..core.events import EventBus, Stage, Status
from ..core.journal import JournalStore, ResearchLog
from ..core.models import SourceDoc, TaskResult
from ..core.permissions import PermissionManager
from ..providers.llm import get_llm
from ..providers.llm.base import LLMRequest
from ..providers.search import get_search
from ..providers.storage import get_storage
from ..analysis.report import ResearchReport
from ..analysis.verify import summarize, verify_answer
from ..tools.registry import ToolBox
from . import document_agent
from .planner import Plan, plan as build_plan
from .research import run_research

def _headline(prompt: str) -> str:
    """Titre d'accroche tiré de la demande, sans les mots de fabrication."""
    from ..providers.llm.offline import subject

    import re as _re

    words: list[str] = []
    for word in subject(prompt).split():
        # On s'arrête au premier chiffre : un titre qui avale le prix donne
        # « Traversée Ouroveni vers Hoani à 15 000 », coupé en plein milieu.
        if _re.search(r"\d", word):
            break
        words.append(word)
    words = words[:8] or subject(prompt).split()[:6]
    # Un titre ne se termine pas sur une préposition en suspens (« … Hoani à »).
    orphelins = {"a", "à", "de", "du", "des", "en", "pour", "vers", "sur",
                 "et", "ou", "le", "la", "les", "un", "une", "dans"}
    while words and words[-1].lower() in orphelins:
        words.pop()
    titre = " ".join(words).strip(" ,.;:—-")
    return (titre[:1].upper() + titre[1:]) if titre else "Sans titre"


_SYNTHESIS_INSTRUCTIONS = (
    "Rédige une réponse structurée en Markdown : un court paragraphe de "
    "conclusion en tête, puis les détails en sections. Cite chaque affirmation "
    "importante avec [S1], [S2]… Termine par une section « Limites » indiquant "
    "ce que les sources ne permettent pas d'établir."
)


class Orchestrator:
    """Exécute une tâche de bout en bout."""

    def __init__(
        self,
        settings: Settings | None = None,
        *,
        permissions: PermissionManager | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self.permissions = permissions or PermissionManager(self.settings)

    # -- construction du contexte -----------------------------------------

    def _context(self, task_id: str, prompt: str, bus: EventBus) -> TaskContext:
        llm, llm_notice = get_llm(self.settings.llm_provider)
        search, search_notice = get_search(self.settings.search_provider)
        plan = build_plan(prompt, max_search_steps=self.settings.max_research_steps)

        ctx = TaskContext(
            task_id=task_id,
            prompt=prompt,
            settings=self.settings,
            bus=bus,
            journal=ResearchLog(task_id=task_id, task=prompt),
            permissions=self.permissions,
            storage=get_storage(self.settings.storage_provider),
            llm=llm,
            search=search,
            budget=plan.budget,
        )
        ctx._plan = plan  # type: ignore[attr-defined]
        for notice in (llm_notice, search_notice):
            if notice:
                ctx.notice(notice)
        return ctx

    # -- exécution ---------------------------------------------------------

    def run(self, prompt: str, *, task_id: str | None = None, bus: EventBus | None = None) -> TaskResult:
        task_id = task_id or uuid.uuid4().hex[:12]
        bus = bus or EventBus()
        started = time.monotonic()

        ctx = self._context(task_id, prompt, bus)
        plan: Plan = ctx._plan  # type: ignore[attr-defined]
        ctx.journal.complexity = plan.budget.complexity.value

        toolbox = ToolBox(ctx)
        result = TaskResult(
            task_id=task_id,
            prompt=prompt,
            complexity=plan.budget.complexity.value,
            degraded=ctx.llm.degraded,
        )
        sources: list[SourceDoc] = []

        try:
            # 1. TÂCHE — analyse de la demande et allocation du budget
            ctx.stage(
                Stage.TASK,
                Status.DONE,
                plan.describe(),
                plan=plan.to_dict(),
                llm=ctx.llm.name,
                search=ctx.search.name,
            )
            ctx.journal.add_summary(f"plan : {plan.describe()}")

            # 2. RECHERCHE + ANALYSE — boucle adaptative (spec §3)
            report: ResearchReport | None = None
            if plan.needs_research or plan.urls:
                sources, report = run_research(ctx, plan, toolbox)
                if not sources:
                    ctx.notice(
                        "Aucune source exploitable : réponse produite sans appui documentaire."
                    )
                self._announce(ctx, report)
            else:
                ctx.stage(Stage.RESEARCH, Status.SKIPPED, "Recherche non nécessaire")

            # 3. SYNTHÈSE
            result.answer = self._analyze(ctx, plan, sources)
            if report is not None:
                result.answer = f"{result.answer}\n\n{report.sections()}".strip()
                result.report = report.to_dict()

            # 4. CRÉATION — documents et/ou création graphique
            files = document_agent.produce(ctx, plan, toolbox, result.answer, sources)
            if plan.needs_design:
                design_files, design_report = self._design(ctx, plan, toolbox, report)
                files += design_files
                if design_report:
                    result.answer = f"{design_report}\n\n---\n\n{result.answer}".strip()

            # 5. VÉRIFICATION — la réponse d'abord, les fichiers ensuite
            ctx.stage(Stage.VERIFICATION, Status.RUNNING, "Vérification…")
            check = self._verify_answer(ctx, result, sources)
            result.files = document_agent.verify_all(ctx, files)
            self._verdict(ctx, check, files, result.files)

        except ApprovalRequired as exc:
            # L'interface doit présenter la demande de confirmation à l'utilisateur.
            ctx.stage(
                Stage.RESULT,
                Status.PENDING,
                str(exc),
                approval={"request_id": exc.request_id, "tool": exc.tool},
            )
            result.errors.append(str(exc))
        except BudgetExceeded as exc:
            ctx.notice(str(exc))
            result.errors.append(str(exc))
        except AraError as exc:
            ctx.journal.add_error(str(exc))
            result.errors.append(str(exc))
            ctx.stage(Stage.RESULT, Status.FAILED, str(exc))
        except Exception as exc:  # filet de sécurité : jamais de trace brute à l'écran
            message = f"Erreur inattendue : {type(exc).__name__}: {exc}"
            ctx.journal.add_error(message)
            result.errors.append(message)
            ctx.stage(Stage.RESULT, Status.FAILED, message)

        # 6. RÉSULTAT
        result.sources = sources
        result.notices = list(ctx.notices)
        if not result.answer and not result.errors:
            result.answer = "Aucun résultat produit."

        if not any(
            event.stage is Stage.RESULT for event in bus.history if event.type == "stage"
        ):
            ctx.stage(
                Stage.RESULT,
                Status.DONE,
                f"{len(result.files)} fichier(s) · {len(sources)} source(s)",
                result=result.to_dict(),
            )

        self._finish(ctx, result, started)
        bus.close()
        return result

    # -- étapes ------------------------------------------------------------

    def _analyze(self, ctx: TaskContext, plan: Plan, sources: list[SourceDoc]) -> str:
        ctx.stage(Stage.ANALYSIS, Status.RUNNING, "Analyse et synthèse…")
        ctx.check_deadline()

        instructions = _SYNTHESIS_INSTRUCTIONS if sources else ""
        try:
            completion = ctx.llm.complete(
                LLMRequest(
                    task="synthesis" if sources else "answer",
                    question=plan.prompt,
                    instructions=instructions,
                    documents=sources,
                    max_tokens=1600 if plan.budget.complexity is Complexity.HIGH else 1000,
                )
            )
        except AraError as exc:
            ctx.journal.add_error(f"analyse : {exc}")
            ctx.stage(Stage.ANALYSIS, Status.FAILED, str(exc))
            ctx.notice(f"Synthèse impossible avec « {ctx.llm.name} » : {exc}")
            return _fallback_answer(plan, sources)

        ctx.journal.add_summary(
            f"synthèse via {completion.provider} sur {len(sources)} source(s)"
        )
        ctx.stage(
            Stage.ANALYSIS,
            Status.DONE,
            f"Synthèse produite ({completion.provider})",
            provider=completion.provider,
            degraded=completion.degraded,
        )
        if completion.degraded and sources:
            ctx.notice(
                "Synthèse extractive (moteur hors-ligne) : les phrases sont copiées "
                "des sources. Configurez un LLM pour une rédaction complète."
            )
        elif completion.degraded:
            ctx.notice(
                "Moteur hors-ligne : il ne rédige pas de texte, il n'extrait que des "
                "phrases de sources. Configurez un LLM pour obtenir une réponse rédigée."
            )
        return completion.text

    def _design(self, ctx: TaskContext, plan: Plan, toolbox: ToolBox,
                report: ResearchReport | None):
        """Studio créatif : brief → concepts → critique → amélioration (spec §5-§7).

        La recherche déjà menée sert de matière : arguments confirmés par
        plusieurs sources, et sites concurrents rencontrés en chemin.
        """
        from ..design.brief import from_prompt

        ctx.stage(Stage.CREATION, Status.RUNNING, f"Studio créatif : {plan.design}")
        brief = from_prompt(plan.prompt)

        market: list[str] = []
        competitors: list[str] = []
        if report is not None:
            for cluster in report.confirmed[:3]:
                sources = ", ".join(f"S{s}" for s in sorted({f.source for f in cluster}))
                market.append(f"{cluster[0].describe()} (confirmé par {sources})")
            competitors = sorted(report.domains)[:5]

        try:
            info = toolbox.call(
                "create_flyer",
                title=brief.title or _headline(plan.prompt),
                subtitle=brief.subject,
                bullets=market,
                price=brief.price,
                contact=brief.contact,
                url=brief.url,
                format=plan.design,
                filename=plan.filename_hint,
                market=market,
                competitors=competitors,
                subject=brief.subject,
            )
        except AraError as exc:
            ctx.journal.add_error(f"création graphique : {exc}")
            ctx.notice(f"Création graphique impossible : {exc}")
            ctx.stage(Stage.CREATION, Status.FAILED, str(exc))
            return [], ""

        ctx.stage(
            Stage.CREATION, Status.DONE,
            f"{len(info['files'])} visuel(s) · note finale {info['score']}/100",
            files=info["files"], studio=info["studio"],
        )
        return info["files"], info["report"]

    @staticmethod
    def _announce(ctx: TaskContext, report: ResearchReport) -> None:
        """Remonte à l'utilisateur ce que la boucle a trouvé de notable."""
        for item in report.anomalies:
            ctx.notice(f"CONTRADICTION DÉTECTÉE — {item.describe()}")
        for gap in report.gaps[:3]:
            ctx.notice(f"Information manquante — {gap.label}")
        if report.iterations > 1:
            ctx.bus.log(
                f"{report.iterations} cycles de recherche · arrêt : {report.stopped_because}",
                kind="loop",
            )

    @staticmethod
    def _verify_answer(ctx: TaskContext, result: TaskResult, sources: list[SourceDoc]):
        """Contrôle la réponse elle-même avant de la livrer (spec §3)."""
        check = verify_answer(result.answer, sources)
        result.answer_check = check.to_dict()

        for problem in check.problems:
            ctx.notice(f"Vérification — {problem}")
        if check.uncited_claims:
            ctx.notice(
                "Vérification — chiffre(s) sans source dans la réponse : "
                + ", ".join(check.uncited_claims[:3])
            )
        ctx.journal.add_step("verify", summarize(check), ok=check.ok)
        return check

    @staticmethod
    def _verdict(ctx: TaskContext, check, produced: list, checked: list) -> None:
        """Un seul verdict de VÉRIFICATION, couvrant réponse et fichiers."""
        parts = [summarize(check)]
        if produced:
            parts.append(f"{len(checked)}/{len(produced)} fichier(s) ouvrable(s)")

        failed = bool(produced) and not checked
        ctx.stage(
            Stage.VERIFICATION,
            Status.FAILED if failed else Status.DONE,
            " · ".join(parts),
            answer=check.to_dict(),
            files=checked,
        )

    def _finish(self, ctx: TaskContext, result: TaskResult, started: float) -> None:
        ctx.journal.duration_ms = int((time.monotonic() - started) * 1000)
        ctx.journal.iterations = 1
        for doc in result.sources:
            ctx.journal.add_source(doc.url, doc.title, via=doc.engine)
        try:
            JournalStore(self.settings.journal_path()).append(ctx.journal)
        except OSError as exc:  # un disque plein ne doit pas perdre le résultat
            result.notices.append(f"Journal non écrit : {exc}")


def _fallback_answer(plan: Plan, sources: list[SourceDoc]) -> str:
    """Réponse minimale quand même l'analyse échoue — on ne rend jamais rien de vide."""
    lines = [
        "La synthèse automatique a échoué. Voici la matière brute collectée :",
        "",
    ]
    for index, doc in enumerate(sources, start=1):
        lines.append(f"- [S{index}] {doc.title or doc.domain} — {doc.url}")
        excerpt = " ".join((doc.content or "").split())[:300]
        if excerpt:
            lines.append(f"  {excerpt}…")
    if not sources:
        lines.append("- Aucune source n'a pu être consultée.")
    return "\n".join(lines)


def run_task(prompt: str, **kwargs) -> TaskResult:
    """Raccourci : exécute une tâche avec les réglages courants."""
    return Orchestrator().run(prompt, **kwargs)
