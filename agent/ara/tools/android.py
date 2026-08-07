"""Outils du téléphone (spec §13) — notification, partage, presse-papier, voix.

Chacun est un outil **indépendant**, déclaré au registre, soumis à la liste
blanche. `share_file` est en plus marqué sensible : un fichier qui sort de
l'appareil est une action que l'humain doit confirmer (spec §15).

Sur une machine qui n'est pas un téléphone, ces outils ne plantent pas : ils
lèvent `ExternalResourceRequired`, dont le message dit exactement ce qui
manque et comment l'installer.
"""

from __future__ import annotations

import json
from typing import Any

from ..android.bridge import capabilities, run_termux
from ..core.context import TaskContext
from ..core.errors import ToolError
from .registry import tool

#: Une notification trop longue est tronquée par Android ; on le fait avant lui.
MAX_TITLE = 100
MAX_MESSAGE = 500


def _short(text: str, limit: int) -> str:
    text = " ".join(str(text or "").split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


@tool(
    "phone_status",
    "État du téléphone : batterie, charge, réseau. Sert aussi aux routines.",
)
def phone_status(ctx: TaskContext) -> dict[str, Any]:
    infos = capabilities()
    etat: dict[str, Any] = {"device": infos}
    if not infos["usable"]:
        return etat

    if "termux-battery-status" in infos["commands"]:
        try:
            data = json.loads(run_termux("termux-battery-status") or "{}")
            etat["battery"] = {
                "percentage": data.get("percentage"),
                "status": data.get("status"),
                "plugged": data.get("plugged"),
            }
        except (ToolError, json.JSONDecodeError, ValueError):
            etat["battery"] = None

    if "termux-wifi-connectioninfo" in infos["commands"]:
        try:
            data = json.loads(run_termux("termux-wifi-connectioninfo") or "{}")
            etat["wifi"] = {
                "connected": bool(data.get("supplicant_state") == "COMPLETED"),
                "ssid": data.get("ssid"),
            }
        except (ToolError, json.JSONDecodeError, ValueError):
            etat["wifi"] = None

    return etat


@tool(
    "notify_phone",
    "Affiche une notification sur le téléphone (fin de tâche, routine).",
    params={"title": "titre", "message": "texte", "notification_id": "identifiant (optionnel)"},
)
def notify_phone(
    ctx: TaskContext,
    title: str,
    message: str = "",
    notification_id: str = "",
) -> dict[str, Any]:
    args = ["--title", _short(title, MAX_TITLE), "--content", _short(message, MAX_MESSAGE)]
    if notification_id:
        # Un identifiant stable remplace la notification précédente au lieu
        # d'en empiler une nouvelle à chaque exécution d'une routine.
        args += ["--id", _short(notification_id, 40)]
    run_termux("termux-notification", args)
    return {"notified": True, "title": _short(title, MAX_TITLE)}


@tool(
    "copy_to_clipboard",
    "Copie un texte dans le presse-papier du téléphone.",
    params={"text": "texte à copier"},
)
def copy_to_clipboard(ctx: TaskContext, text: str) -> dict[str, Any]:
    contenu = str(text or "")
    if not contenu.strip():
        raise ToolError("Rien à copier : le texte est vide.")
    run_termux("termux-clipboard-set", stdin=contenu)
    return {"copied": len(contenu)}


@tool(
    "speak_text",
    "Lit un texte à voix haute (utile en conduisant).",
    params={"text": "texte à lire"},
)
def speak_text(ctx: TaskContext, text: str) -> dict[str, Any]:
    contenu = _short(text, 1000)
    if not contenu:
        raise ToolError("Rien à lire : le texte est vide.")
    run_termux("termux-tts-speak", stdin=contenu, timeout=60)
    return {"spoken": len(contenu)}


@tool(
    "share_file",
    "Ouvre le partage Android pour un fichier produit par la tâche. "
    "Le destinataire est choisi par vous, dans l'application de votre choix.",
    params={"filename": "nom du fichier de la tâche"},
    sensitive=True,
)
def share_file(ctx: TaskContext, filename: str) -> dict[str, Any]:
    path = ctx.storage.path_for(ctx.task_id, filename)
    if not path.is_file():
        raise ToolError(f"Fichier introuvable : {filename}")
    # --action send ouvre le sélecteur : c'est l'humain qui désigne
    # l'application et le destinataire, jamais l'agent.
    run_termux("termux-share", ["--action", "send", str(path)], timeout=30)
    return {"shared": path.name, "size": path.stat().st_size}


__all__ = [
    "copy_to_clipboard",
    "notify_phone",
    "phone_status",
    "share_file",
    "speak_text",
]
