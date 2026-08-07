"""Ligne de commande — utile pour tester sans navigateur et pour les scripts.

    python -m ara.cli "Recherche X et fais-moi un PDF"
    python -m ara.cli --serve
"""

from __future__ import annotations

import argparse
import sys

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


def main(argv: list[str] | None = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="ara", description="Agent de recherche et de création.")
    parser.add_argument("prompt", nargs="*", help="la demande à traiter")
    parser.add_argument("--serve", action="store_true", help="lance le serveur web/mobile")
    args = parser.parse_args(argv)

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
