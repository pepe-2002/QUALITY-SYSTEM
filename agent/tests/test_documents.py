"""Génération et vérification des documents (spec §8, §20)."""

from __future__ import annotations

import zipfile

import pytest

from ara.documents.model import from_markdown
from ara.documents.render import VerificationError, document_from_markdown, generate, verify

MARKDOWN = """
# Traversées maritimes

Un **paragraphe** d'introduction avec du `code` et une citation [S1].

## Tarifs

| Trajet | Prix |
| --- | --- |
| Ouroveni → Hoani | 15 000 FC |
| Hoani → Ouroveni | 17 500 FC |

- Premier point de la liste
- Deuxième point de la liste

> Une remarque importante.

### Limites

1. Les sources datent de 2026.
"""

SOURCES = [
    {"title": "Traversées Grande Comore – Mohéli", "url": "https://exemple.test/traversees"},
    {"title": "Tarifs des vedettes", "url": "https://autre.test/tarifs"},
]


@pytest.fixture
def document():
    return document_from_markdown(
        "Rapport traversées", MARKDOWN, subtitle="Test automatisé", sources=SOURCES
    )


# --- Analyse Markdown ---------------------------------------------------------


def test_le_markdown_est_converti_en_blocs():
    kinds = [block.kind for block in from_markdown(MARKDOWN)]
    assert "h1" in kinds and "h2" in kinds and "h3" in kinds
    assert "table" in kinds
    assert kinds.count("bullet") == 2
    assert "quote" in kinds
    assert "numbered" in kinds


def test_le_tableau_conserve_ses_cellules():
    table = next(b for b in from_markdown(MARKDOWN) if b.kind == "table")
    assert table.rows[0] == ["Trajet", "Prix"]
    assert table.rows[1] == ["Ouroveni → Hoani", "15 000 FC"]


def test_le_gras_est_reconnu():
    block = from_markdown("Un **mot** en gras")[0]
    assert any(run.bold for run in block.runs)


# --- Génération ---------------------------------------------------------------


@pytest.mark.parametrize("fmt", ["pdf", "docx", "md", "txt"])
def test_generation_et_verification(document, tmp_path, fmt):
    info = generate(document, tmp_path / f"rapport.{fmt}", fmt)
    assert info["size"] > 0
    assert info["format"] == fmt


def test_le_pdf_est_pagine_et_ouvrable(document, tmp_path):
    path = tmp_path / "rapport.pdf"
    info = generate(document, path, "pdf")
    raw = path.read_bytes()
    assert raw.startswith(b"%PDF-")
    assert b"%%EOF" in raw[-2048:]
    assert info["pages"] >= 1


def test_le_docx_est_une_archive_valide(document, tmp_path):
    path = tmp_path / "rapport.docx"
    generate(document, path, "docx")
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        assert {"[Content_Types].xml", "word/document.xml", "word/styles.xml"} <= names
        body = archive.read("word/document.xml").decode("utf-8")
    assert "Traversées maritimes" in body
    assert "15 000 FC" in body


def test_le_markdown_contient_les_sources(document, tmp_path):
    path = tmp_path / "rapport.md"
    generate(document, path, "md")
    text = path.read_text(encoding="utf-8")
    assert "## Sources" in text
    assert "https://exemple.test/traversees" in text


def test_le_pdf_de_repli_fonctionne_sans_reportlab(document, tmp_path, monkeypatch):
    """Un téléphone sans ReportLab doit quand même produire un PDF lisible."""
    from ara.documents import pdf as pdf_engine

    monkeypatch.setattr(pdf_engine, "REPORTLAB", False)
    path, warning = pdf_engine.render(document, tmp_path / "repli.pdf")

    assert "ReportLab" in warning
    info = verify(path)
    assert info["pages"] >= 1


def test_les_caracteres_speciaux_ne_cassent_pas_le_rendu(tmp_path):
    doc = document_from_markdown("Test & <balises>", "Prix : 15 000 € — « guillemets » & <b>")
    for fmt in ("pdf", "docx", "md", "txt"):
        assert generate(doc, tmp_path / f"special.{fmt}", fmt)["size"] > 0


# --- Vérification -------------------------------------------------------------


def test_un_pdf_tronque_est_refuse(document, tmp_path):
    path = tmp_path / "casse.pdf"
    generate(document, path, "pdf")
    path.write_bytes(path.read_bytes()[: len(path.read_bytes()) // 2])
    with pytest.raises(VerificationError):
        verify(path)


def test_un_docx_corrompu_est_refuse(tmp_path):
    path = tmp_path / "casse.docx"
    path.write_bytes(b"ceci n'est pas un zip")
    with pytest.raises(VerificationError):
        verify(path)


def test_un_fichier_vide_est_refuse(tmp_path):
    path = tmp_path / "vide.md"
    path.write_text("")
    with pytest.raises(VerificationError):
        verify(path)


def test_format_inconnu_refuse(document, tmp_path):
    with pytest.raises(VerificationError):
        generate(document, tmp_path / "rapport.xyz", "xyz")


# --- Outils -------------------------------------------------------------------


def test_les_outils_documentaires_livrent_un_fichier_verifie(toolbox):
    info = toolbox.call(
        "create_pdf",
        filename="rapport",
        title="Rapport de test",
        markdown=MARKDOWN,
        sources=SOURCES,
    )
    assert info["name"] == "rapport.pdf"
    assert info["pages"] >= 1


def test_un_document_invalide_nest_pas_livre(toolbox, monkeypatch):
    """Si la vérification échoue, aucun fichier ne doit rester ni être annoncé."""
    from ara.core.errors import ToolError
    from ara.documents import render as render_module

    monkeypatch.setattr(
        render_module, "verify",
        lambda path: (_ for _ in ()).throw(VerificationError("illisible")),
    )

    with pytest.raises(ToolError):
        toolbox.call("create_pdf", filename="rapport", title="T", markdown="corps")

    assert toolbox.call("list_files") == []
