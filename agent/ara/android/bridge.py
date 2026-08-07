"""Exécution des commandes Termux, sous liste blanche stricte.

Un agent qui peut lancer une commande arbitraire sur le téléphone de son
propriétaire n'est pas un agent, c'est un risque. Ce module est donc écrit à
l'envers de la facilité :

* **liste blanche fermée** — seules les commandes de :data:`SUPPORTED` peuvent
  être lancées ; un nom absent est refusé même s'il existe sur le téléphone ;
* **jamais de shell** — les arguments passent en liste à `subprocess`, donc
  aucun `;`, `&&` ou `$(…)` glissé dans un paramètre ne peut s'exécuter ;
* **arguments contrôlés** — refus de tout ce qui n'est pas une chaîne simple ;
* **délai maximal** sur chaque appel, sortie tronquée.

Sur une machine qui n'est pas un téléphone, :func:`detect` le dit et les outils
lèvent `ExternalResourceRequired` avec le motif exact. Rien ne s'installe tout
seul (spec §19).
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from typing import Callable, Sequence

from ..core.errors import ExternalResourceRequired, ToolError

#: Commandes autorisées → ce à quoi elles servent.
#: Tout ce qui n'est pas ici est refusé. En particulier `termux-sms-send`
#: n'y figure **pas** : voir la note en bas de module.
SUPPORTED: dict[str, str] = {
    "termux-notification": "afficher une notification",
    "termux-share": "ouvrir le sélecteur de partage d'Android",
    "termux-clipboard-set": "écrire dans le presse-papier",
    "termux-clipboard-get": "lire le presse-papier",
    "termux-tts-speak": "lire un texte à voix haute",
    "termux-battery-status": "état de la batterie",
    "termux-wifi-connectioninfo": "état du Wi-Fi",
    "termux-vibrate": "faire vibrer le téléphone",
}

#: Ces commandes viennent du paquet Termux:API, installé séparément.
_NEEDS_API = set(SUPPORTED) - {"termux-share"}

MAX_OUTPUT_CHARS = 20_000
DEFAULT_TIMEOUT = 15

#: Type d'un lanceur de commande — remplaçable dans les tests, ce qui permet
#: de vérifier le pont sans téléphone.
Runner = Callable[[Sequence[str], float, str | None], "CommandResult"]


@dataclass(frozen=True)
class CommandResult:
    code: int
    stdout: str = ""
    stderr: str = ""

    @property
    def ok(self) -> bool:
        return self.code == 0


@dataclass(frozen=True)
class Device:
    """Ce que la machine sait faire, tel que constaté — pas tel qu'espéré."""

    on_termux: bool = False
    #: commandes de :data:`SUPPORTED` réellement présentes
    available: tuple[str, ...] = ()
    reason: str = ""

    @property
    def usable(self) -> bool:
        return self.on_termux and bool(self.available)

    def has(self, command: str) -> bool:
        return command in self.available

    def to_dict(self) -> dict:
        return {
            "on_termux": self.on_termux,
            "usable": self.usable,
            "available": list(self.available),
            "reason": self.reason,
        }


def _default_runner(args: Sequence[str], timeout: float, stdin: str | None) -> CommandResult:
    try:
        proc = subprocess.run(  # noqa: S603 — liste d'arguments, jamais de shell
            list(args),
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except FileNotFoundError:
        return CommandResult(127, stderr="commande absente")
    except subprocess.TimeoutExpired:
        return CommandResult(124, stderr=f"délai dépassé ({timeout}s)")
    except OSError as exc:  # permission, exécutable illisible…
        return CommandResult(126, stderr=str(exc))
    return CommandResult(
        proc.returncode,
        (proc.stdout or "")[:MAX_OUTPUT_CHARS],
        (proc.stderr or "")[:MAX_OUTPUT_CHARS],
    )


_runner: Runner = _default_runner
_cache: Device | None = None


def set_runner(runner: Runner | None) -> None:
    """Remplace le lanceur de commandes (tests, simulation d'un téléphone)."""
    global _runner, _cache
    _runner = runner or _default_runner
    _cache = None


def _on_termux() -> bool:
    """Vrai si l'on tourne bien dans Termux.

    Deux indices, pas un seul : la variable `PREFIX` d'un côté, la présence du
    dossier d'installation de l'autre. `TERMUX_VERSION` suffit quand elle est
    là, mais elle manque dans certaines sessions non interactives.
    """
    if os.environ.get("TERMUX_VERSION"):
        return True
    prefix = os.environ.get("PREFIX", "")
    return prefix.startswith("/data/data/com.termux") or os.path.isdir(
        "/data/data/com.termux/files/usr"
    )


def detect(*, refresh: bool = False) -> Device:
    """Constate ce que la machine sait faire, et le retient."""
    global _cache
    if _cache is not None and not refresh:
        return _cache

    if not _on_termux():
        _cache = Device(
            on_termux=False,
            reason=(
                "cette machine n'est pas un téléphone sous Termux : "
                "les fonctions Android (notification, partage, batterie) "
                "n'y existent pas"
            ),
        )
        return _cache

    present = tuple(name for name in sorted(SUPPORTED) if shutil.which(name))
    if not present:
        _cache = Device(
            on_termux=True,
            reason=(
                "Termux est là mais Termux:API manque. "
                "Installez l'application « Termux:API » depuis F-Droid, "
                "puis « pkg install termux-api »"
            ),
        )
        return _cache

    manquantes = sorted(_NEEDS_API - set(present))
    _cache = Device(
        on_termux=True,
        available=present,
        reason=(
            f"{len(manquantes)} commande(s) absente(s) : {', '.join(manquantes)}"
            if manquantes
            else ""
        ),
    )
    return _cache


def capabilities() -> dict:
    """Vue lisible par l'interface — utile pour ne pas proposer l'impossible."""
    device = detect()
    return {
        **device.to_dict(),
        "commands": {name: SUPPORTED[name] for name in device.available},
    }


def require(command: str) -> Device:
    """Vérifie qu'une commande est utilisable, sinon explique ce qui manque."""
    if command not in SUPPORTED:
        raise ToolError(f"Commande Termux non autorisée : {command}")
    device = detect()
    if not device.has(command):
        raise ExternalResourceRequired(
            command,
            device.reason or f"« {command} » n'est pas installée sur ce téléphone",
        )
    return device


def _clean(args: Sequence[str]) -> list[str]:
    """Refuse tout argument qui n'est pas une chaîne simple.

    Sans shell, une injection classique n'a pas de prise ; on écarte quand même
    les caractères de contrôle, qui n'ont aucune raison d'être dans un titre de
    notification et brouillent les journaux.
    """
    propres: list[str] = []
    for arg in args:
        if not isinstance(arg, str):
            raise ToolError("Argument Termux invalide : une chaîne était attendue.")
        if any(ord(ch) < 32 and ch not in "\t\n" for ch in arg):
            raise ToolError("Argument Termux invalide : caractère de contrôle.")
        propres.append(arg)
    return propres


def run_termux(
    command: str,
    args: Sequence[str] = (),
    *,
    stdin: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> str:
    """Lance une commande Termux autorisée et retourne sa sortie.

    Lève `ExternalResourceRequired` si la machine ne peut pas, `ToolError` si
    la commande échoue.
    """
    require(command)
    result = _runner([command, *_clean(args)], timeout, stdin)
    if not result.ok:
        detail = (result.stderr or result.stdout or "").strip()
        raise ToolError(
            f"« {command} » a échoué (code {result.code})"
            + (f" : {detail[:200]}" if detail else "")
        )
    return result.stdout


# --------------------------------------------------------------------------
# Note de conception — pourquoi pas `termux-sms-send`
#
# Envoyer un SMS est la seule capacité de cette liste qui engage le
# propriétaire auprès d'un tiers sans qu'il voie ce qui part. Une confirmation
# dans l'interface de l'agent ne suffit pas : elle porte sur un texte, pas sur
# le geste d'envoi. `termux-share` fait au contraire passer par le sélecteur
# d'applications d'Android — le destinataire est choisi par l'humain, dans son
# application, hors de portée de l'agent. C'est ce chemin qui est retenu.
# --------------------------------------------------------------------------

__all__ = [
    "CommandResult",
    "Device",
    "SUPPORTED",
    "capabilities",
    "detect",
    "require",
    "run_termux",
    "set_runner",
]
