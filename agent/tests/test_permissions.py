"""Permissions, confirmation humaine et sécurité (spec §15, §16)."""

from __future__ import annotations

import pytest

from ara.core.errors import (
    ApprovalRequired,
    ExternalResourceRequired,
    PermissionDenied,
    ToolError,
    ToolNotFound,
)
from ara.core.permissions import PermissionManager


def test_un_outil_non_autorise_est_refuse_meme_sil_existe(toolbox, ctx):
    """Règle §16 : exister ne donne aucun droit."""
    ctx.permissions.revoke("web_search")
    with pytest.raises(PermissionDenied):
        toolbox.call("web_search", query="test")


def test_outil_inconnu(toolbox):
    with pytest.raises(ToolNotFound):
        toolbox.call("outil_qui_nexiste_pas")


def test_action_sensible_demande_confirmation(toolbox, ctx):
    ctx.permissions.allow("delete_file")
    toolbox.call("save_file", filename="note.txt", content="contenu")

    with pytest.raises(ApprovalRequired) as exc:
        toolbox.call("delete_file", filename="note.txt")

    assert exc.value.tool == "delete_file"
    assert exc.value.request_id
    # Le fichier est toujours là : rien n'a été exécuté.
    assert [f["name"] for f in toolbox.call("list_files")] == ["note.txt"]


def test_confirmation_accordee_puis_execution(toolbox, ctx):
    ctx.permissions.allow("delete_file")
    toolbox.call("save_file", filename="note.txt", content="contenu")

    with pytest.raises(ApprovalRequired) as exc:
        toolbox.call("delete_file", filename="note.txt")

    ctx.permissions.resolve(exc.value.request_id, True)
    ctx.permissions.settings = ctx.settings
    # Une fois l'accord donné, l'appel est rejoué explicitement par l'appelant.
    from ara.tools.files import delete_file

    assert delete_file(ctx, filename="note.txt") == {"deleted": "note.txt"}


def test_les_demandes_en_attente_sont_listees(isolated_settings):
    manager = PermissionManager(isolated_settings)
    request = manager.request_approval("publish", "publication")
    assert [r.request_id for r in manager.pending()] == [request.request_id]

    manager.resolve(request.request_id, False)
    assert manager.pending() == []


def test_confirmation_inconnue_refusee(isolated_settings):
    manager = PermissionManager(isolated_settings)
    with pytest.raises(PermissionDenied):
        manager.resolve("identifiant-bidon", True)


# --- Ressources externes (spec §19) -------------------------------------------


def test_une_fonction_payante_ne_sactive_pas_toute_seule(toolbox, ctx):
    ctx.permissions.allow("generate_image")
    with pytest.raises(ExternalResourceRequired) as exc:
        toolbox.call("generate_image", prompt="un flyer")
    assert "ressource externe" in str(exc.value).lower()


def test_aucun_secret_dans_les_reglages(isolated_settings):
    """Les clés ne doivent jamais transiter par l'objet de configuration."""
    import dataclasses

    for field in dataclasses.fields(isolated_settings):
        assert not any(
            mot in field.name.lower() for mot in ("key", "token", "secret", "password")
        ), f"champ suspect dans Settings : {field.name}"

    values = " ".join(
        str(getattr(isolated_settings, f.name))
        for f in dataclasses.fields(isolated_settings)
        if f.name != "workspace"  # chemin temporaire, dépend du nom du test
    ).lower()
    for forbidden in ("api_key", "bearer ", "sk-"):
        assert forbidden not in values


def test_les_secrets_sont_lus_dans_lenvironnement(monkeypatch):
    from ara.core.config import Settings

    assert Settings.secret("ARA_TEST_KEY") is None
    monkeypatch.setenv("ARA_TEST_KEY", "valeur")
    assert Settings.secret("ARA_TEST_KEY") == "valeur"


# --- Confinement des fichiers -------------------------------------------------


def test_impossible_de_sortir_de_lespace_de_travail(ctx):
    stored = ctx.storage.write_text(ctx.task_id, "../../evasion.txt", "charge")
    assert ".." not in str(stored.path)
    assert str(ctx.settings.tasks_dir()) in str(stored.path)


def test_lecture_dun_fichier_absent(toolbox):
    with pytest.raises(ToolError):
        toolbox.call("read_file", filename="inexistant.txt")


def test_les_adresses_privees_sont_bloquees(monkeypatch):
    """Garde-fou SSRF : l'agent ne doit pas sonder le réseau local."""
    import ara.core.http as http_module

    monkeypatch.undo()  # retire le faux réseau de la fixture
    with pytest.raises(ToolError):
        http_module.request("http://127.0.0.1:8080/admin")
