"""Pont Android : détection, liste blanche, outils du téléphone (Phase 5).

Aucun téléphone n'est nécessaire pour ces tests : le lanceur de commandes est
remplacé, ce qui permet de vérifier **ce qui est envoyé** à Termux — donc les
garde-fous — sans dépendre du matériel.
"""

from __future__ import annotations

import json

import pytest

from ara.android import bridge
from ara.core.errors import (
    ApprovalRequired,
    ExternalResourceRequired,
    PermissionDenied,
    ToolError,
)


class FakeTermux:
    """Un téléphone simulé : retient les appels, répond ce qu'on lui dit."""

    def __init__(self, responses: dict | None = None, code: int = 0) -> None:
        self.calls: list[tuple[list[str], float, str | None]] = []
        self.responses = responses or {}
        self.code = code

    def __call__(self, args, timeout, stdin):
        self.calls.append((list(args), timeout, stdin))
        return bridge.CommandResult(self.code, self.responses.get(args[0], ""))

    @property
    def commands(self) -> list[str]:
        return [call[0][0] for call in self.calls]


@pytest.fixture
def phone(monkeypatch):
    """Simule Termux avec toutes les commandes présentes."""
    fake = FakeTermux()
    monkeypatch.setenv("TERMUX_VERSION", "0.118")
    monkeypatch.setattr(bridge.shutil, "which", lambda name: f"/usr/bin/{name}")
    bridge.set_runner(fake)
    return fake


# --- détection -------------------------------------------------------------


def test_hors_telephone_le_pont_se_declare_inutilisable():
    device = bridge.detect(refresh=True)
    assert not device.usable
    assert "termux" in device.reason.lower()


def test_sur_telephone_le_pont_liste_ses_commandes(phone):
    device = bridge.detect(refresh=True)
    assert device.usable
    assert "termux-notification" in device.available


def test_termux_sans_l_api_explique_ce_qu_il_faut_installer(monkeypatch):
    monkeypatch.setenv("TERMUX_VERSION", "0.118")
    monkeypatch.setattr(bridge.shutil, "which", lambda name: None)
    device = bridge.detect(refresh=True)
    assert device.on_termux and not device.usable
    assert "Termux:API" in device.reason


def test_la_detection_est_retenue_puis_rafraichie(phone):
    premier = bridge.detect(refresh=True)
    assert bridge.detect() is premier          # mise en cache
    assert bridge.detect(refresh=True) is not premier


# --- liste blanche et garde-fous ------------------------------------------


def test_une_commande_hors_liste_blanche_est_refusee(phone):
    with pytest.raises(ToolError):
        bridge.run_termux("termux-sms-send", ["--help"])
    assert phone.calls == []                   # rien n'a été lancé


def test_sms_send_n_est_pas_dans_la_liste_blanche():
    """Décision de conception, pas un oubli : voir la note de `bridge`."""
    assert "termux-sms-send" not in bridge.SUPPORTED


def test_les_arguments_partent_en_liste_jamais_dans_un_shell(phone):
    bridge.run_termux("termux-notification", ["--title", "a; rm -rf /"])
    args, _timeout, _stdin = phone.calls[0]
    assert args == ["termux-notification", "--title", "a; rm -rf /"]


def test_un_caractere_de_controle_est_refuse(phone):
    with pytest.raises(ToolError):
        bridge.run_termux("termux-notification", ["--title", "salut\x00malin"])
    assert phone.calls == []


def test_un_echec_de_commande_devient_une_erreur_maitrisee(monkeypatch, phone):
    bridge.set_runner(FakeTermux(code=3))
    with pytest.raises(ToolError) as erreur:
        bridge.run_termux("termux-vibrate")
    assert "code 3" in str(erreur.value)


def test_hors_telephone_l_outil_dit_ce_qui_manque():
    with pytest.raises(ExternalResourceRequired) as erreur:
        bridge.run_termux("termux-notification", ["--title", "test"])
    assert str(erreur.value).startswith("Cette fonction nécessite une ressource externe.")


# --- outils ----------------------------------------------------------------


def test_notification_par_la_boite_a_outils(toolbox, phone):
    resultat = toolbox.call("notify_phone", title="Routine", message="terminé")
    assert resultat["notified"]
    assert phone.commands == ["termux-notification"]


def test_un_titre_trop_long_est_tronque_avant_android(toolbox, phone):
    toolbox.call("notify_phone", title="x" * 400, message="")
    args = phone.calls[0][0]
    titre = args[args.index("--title") + 1]
    assert len(titre) <= 100 and titre.endswith("…")


def test_le_presse_papier_passe_par_l_entree_standard(toolbox, phone):
    """Un texte en argument se retrouverait dans la liste des processus."""
    toolbox.call("copy_to_clipboard", text="secret de campagne")
    args, _timeout, stdin = phone.calls[0]
    assert stdin == "secret de campagne"
    assert "secret de campagne" not in " ".join(args)


def test_copier_le_vide_est_refuse(toolbox, phone):
    with pytest.raises(ToolError):
        toolbox.call("copy_to_clipboard", text="   ")


def test_l_etat_du_telephone_reste_lisible_sans_telephone(toolbox):
    etat = toolbox.call("phone_status")
    assert etat["device"]["usable"] is False
    assert "battery" not in etat


def test_l_etat_du_telephone_lit_la_batterie(toolbox, monkeypatch, phone):
    bridge.set_runner(
        FakeTermux(
            {
                "termux-battery-status": json.dumps({"percentage": 42, "status": "DISCHARGING"}),
                "termux-wifi-connectioninfo": json.dumps({"supplicant_state": "COMPLETED", "ssid": "maison"}),
            }
        )
    )
    etat = toolbox.call("phone_status")
    assert etat["battery"]["percentage"] == 42
    assert etat["wifi"]["connected"] is True


def test_une_batterie_illisible_ne_casse_pas_l_etat(toolbox, monkeypatch, phone):
    bridge.set_runner(FakeTermux({"termux-battery-status": "pas du json"}))
    etat = toolbox.call("phone_status")
    assert etat["battery"] is None


# --- sécurité du partage ---------------------------------------------------


def test_le_partage_n_est_pas_autorise_par_defaut(ctx, phone):
    from ara.core.config import DEFAULT_ALLOWED_TOOLS

    assert "share_file" not in DEFAULT_ALLOWED_TOOLS


def test_le_partage_exige_une_confirmation_humaine(toolbox, ctx, phone):
    ctx.permissions.allow("share_file")
    with pytest.raises(ApprovalRequired):
        toolbox.call("share_file", filename="rapport.md")
    assert phone.calls == []                   # rien n'est parti sans accord


def test_le_partage_refuse_sans_autorisation(toolbox, phone):
    with pytest.raises(PermissionDenied):
        toolbox.call("share_file", filename="rapport.md")


def test_le_partage_passe_par_le_selecteur_android(ctx, phone):
    """L'humain choisit l'application et le destinataire, jamais l'agent."""
    from ara.tools.android import share_file

    ctx.storage.write_text(ctx.task_id, "note.md", "contenu")
    share_file(ctx, filename="note.md")
    args = phone.calls[0][0]
    assert args[:3] == ["termux-share", "--action", "send"]
