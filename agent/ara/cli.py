"""Ligne de commande — utile pour tester sans navigateur et pour les scripts.

    python -m ara.cli "Recherche X et fais-moi un PDF"
    python -m ara.cli --serve
"""

from __future__ import annotations

import argparse
import sys
import time

from .core.config import get_settings, load_dotenv
from .core.events import EventBus, Stage
from .core.models import TaskResult


def _print_events(bus: EventBus) -> None:
    for event in bus.history:
        if event.type == "stage":
            print(f"  [{event.stage.value:<12}] {event.status.value:<8} {event.message}")


def run_once(prompt: str) -> int:
    from .agents.orchestrator import Orchestrator

    bus = EventBus()
    print(f"» {prompt}\n")
    result: TaskResult = Orchestrator().run(prompt, bus=bus)
    _print_events(bus)

    print("\n" + "─" * 60)
    print(result.answer)
    if result.files:
        print("\nFichiers :")
        for info in result.files:
            print(f"  · {info.get('name')} ({info.get('size')} octets)")
    if result.notices:
        print("\nAvertissements :")
        for notice in result.notices:
            print(f"  ! {notice}")
    if result.errors:
        print("\nErreurs :")
        for error in result.errors:
            print(f"  ✕ {error}")
        return 1
    return 0


def run_lab() -> int:
    """Exécute l'expérience et écrit le rapport dans l'espace de travail."""
    from .lab import render, run_experiment

    settings = get_settings()
    result = run_experiment(settings=settings)
    rapport = render(result)
    print(rapport)

    settings.workspace.mkdir(parents=True, exist_ok=True)
    chemin = settings.workspace / "lab-report.md"
    chemin.write_text(rapport, encoding="utf-8")
    print(f"\nRapport écrit : {chemin}")

    # Une hypothèse réfutée n'est pas une erreur du programme : c'est un
    # résultat. Le code de sortie le distingue quand même, pour qu'un script
    # d'intégration puisse le remarquer.
    return 0 if result.verdict and result.verdict.status != "refutee" else 3


def run_h2_experiment() -> int:
    """Expérience H2 : le contrôleur adaptatif économise-t-il des recherches ?"""
    from .lab import run_h2
    from .lab.report_h2 import render as render_h2

    settings = get_settings()
    result = run_h2(settings=settings)
    rapport = render_h2(result)
    print(rapport)

    settings.workspace.mkdir(parents=True, exist_ok=True)
    chemin = settings.workspace / "h2-report.md"
    chemin.write_text(rapport, encoding="utf-8")
    print(f"\nRapport écrit : {chemin}")

    # Réfutée n'est pas une panne : c'est un résultat. Le code de sortie le
    # distingue quand même, pour qu'un script d'intégration le remarque.
    return 0 if result.verdict and result.verdict.status != "refutee" else 3


def run_v2_experiment_cli() -> int:
    """Expérience ADAPTIVE-V2 : le défaut identifié par H2 est-il corrigé ?"""
    from .lab import run_v2_experiment
    from .lab.report_v2 import render as render_v2

    settings = get_settings()
    result = run_v2_experiment(settings=settings)
    rapport = render_v2(result)
    print(rapport)

    settings.workspace.mkdir(parents=True, exist_ok=True)
    chemin = settings.workspace / "v2-report.md"
    chemin.write_text(rapport, encoding="utf-8")
    print(f"\nRapport écrit : {chemin}")

    return 0 if result.verdict and result.verdict.status != "non_corrige" else 3


def run_research_experiment_cli() -> int:
    """Expérience RESEARCH-BASELINE contre RESEARCH-V2, sur le jeu adversarial."""
    from .lab import run_research_experiment
    from .lab.report_research import render as render_research

    settings = get_settings()
    result = run_research_experiment(settings=settings)
    rapport = render_research(result)
    print(rapport)

    settings.workspace.mkdir(parents=True, exist_ok=True)
    chemin = settings.workspace / "research-report.md"
    chemin.write_text(rapport, encoding="utf-8")
    print(f"\nRapport écrit : {chemin}")
    return 0


def run_diagnostic_cli() -> int:
    """Diagnostic : à quelle étape du pipeline l'information se perd-elle ?"""
    from .lab import run_diagnostic
    from .lab.report_diagnostic import render as render_diagnostic

    settings = get_settings()
    result = run_diagnostic(settings=settings)
    rapport = render_diagnostic(result)
    print(rapport)

    settings.workspace.mkdir(parents=True, exist_ok=True)
    chemin = settings.workspace / "diagnostic-report.md"
    chemin.write_text(rapport, encoding="utf-8")
    print(f"\nRapport écrit : {chemin}")
    return 0


def run_phone() -> int:
    """Dit ce que cette machine sait faire côté téléphone, et ce qui manque."""
    from .android.bridge import SUPPORTED, capabilities

    infos = capabilities()
    print("Termux détecté : " + ("oui" if infos["on_termux"] else "non"))
    if infos["reason"]:
        print(f"  → {infos['reason']}")
    for name, usage in sorted(SUPPORTED.items()):
        etat = "✓" if name in infos["commands"] else "·"
        print(f"  {etat} {name:<28} {usage}")
    return 0 if infos["usable"] else 2


def run_routines(create: tuple[str, str] | None) -> int:
    """Liste les routines, ou en ajoute une."""
    from .automation import RoutineError, RoutineStore, build_routine

    settings = get_settings()
    store = RoutineStore(settings.routines_path())

    if create:
        prompt, when = create
        try:
            routine = build_routine(prompt, when)
            store.add(routine)
        except RoutineError as exc:
            print(f"✕ {exc}")
            return 1
        print(f"Routine créée : {routine.describe()} — « {routine.prompt} »")

    routines = store.list()
    if not routines:
        print("Aucune routine. Exemple :")
        print('  python -m ara.cli --add-routine "chaque matin" "Tarifs des traversées"')
        return 0

    print(f"{len(routines)} routine(s) :")
    for routine in routines:
        etat = "actif " if routine.enabled else "arrêté"
        prochaine = (
            time.strftime("%d/%m %H:%M", time.localtime(routine.next_run))
            if routine.next_run
            else "—"
        )
        print(f"  [{etat}] {routine.routine_id}  {routine.describe():<28} → {prochaine}")
        print(f"           « {routine.prompt[:70]} »")
        if routine.disabled_reason:
            print(f"           arrêtée : {routine.disabled_reason}")
    if not settings.automation_enabled:
        print("\n⚠ L'ordonnanceur est arrêté. ARA_AUTOMATION=1 pour qu'elles tournent.")
    return 0


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="ara", description="Agent de recherche et de création.")
    parser.add_argument("prompt", nargs="*", help="la demande à traiter")
    parser.add_argument("--serve", action="store_true", help="lance le serveur web/mobile")
    parser.add_argument(
        "--lab", action="store_true",
        help="lance le RESEARCH LAB : compare les stratégies et tente de réfuter l'hypothèse",
    )
    parser.add_argument(
        "--h2", action="store_true",
        help="lance l'expérience H2 : le contrôleur adaptatif économise-t-il des recherches ?",
    )
    parser.add_argument(
        "--v2", action="store_true",
        help="lance l'expérience ADAPTIVE-V2 : le défaut identifié est-il corrigé ?",
    )
    parser.add_argument(
        "--research", action="store_true",
        help="compare RESEARCH-BASELINE et RESEARCH-V2 sur le jeu adversarial",
    )
    parser.add_argument(
        "--diagnostic", action="store_true",
        help="range les échecs par étape du pipeline (recherche, extraction, …)",
    )
    parser.add_argument(
        "--phone", action="store_true",
        help="montre les capacités Android détectées (Termux)",
    )
    parser.add_argument(
        "--routines", action="store_true", help="liste les routines programmées",
    )
    parser.add_argument(
        "--add-routine", nargs=2, metavar=("QUAND", "DEMANDE"),
        help='ajoute une routine, ex. --add-routine "chaque matin" "Tarifs des traversées"',
    )
    args = parser.parse_args(argv)

    if args.lab:
        return run_lab()

    if args.h2:
        return run_h2_experiment()

    if args.v2:
        return run_v2_experiment_cli()

    if args.research:
        return run_research_experiment_cli()

    if args.diagnostic:
        return run_diagnostic_cli()

    if args.phone:
        return run_phone()

    if args.routines or args.add_routine:
        creation = (args.add_routine[1], args.add_routine[0]) if args.add_routine else None
        return run_routines(creation)

    if args.serve:
        from .api.server import main as serve

        serve()
        return 0

    if not args.prompt:
        settings = get_settings()
        print("Usage : python -m ara.cli \"votre demande\"  |  python -m ara.cli --serve")
        print(f"LLM={settings.llm_provider} recherche={settings.search_provider}")
        return 2

    return run_once(" ".join(args.prompt))


if __name__ == "__main__":
    sys.exit(main())
