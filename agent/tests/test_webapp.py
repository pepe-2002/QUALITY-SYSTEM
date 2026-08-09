"""Fabrique de sites : générateur, critique, mémoire des défauts, studio."""

from __future__ import annotations

import json

import pytest

from ara.agents.planner import plan
from ara.design.brand import BrandProfile
from ara.design.color import contrast
from ara.webapp.builder import (
    MIN_TAP_TARGET, PLACEHOLDER, Section, SiteSpec, apply_brand, build_site,
    spec_from_brief,
)
from ara.webapp.critic import DEFECTS, banned_terms, critique
from ara.webapp.lessons import Lesson, Lessons
from ara.webapp.studio import FIXES, SiteStudio


# --- Générateur ---------------------------------------------------------------


def test_le_site_ne_reference_aucune_ressource_distante():
    """La contrainte fondatrice : ça doit s'ouvrir hors ligne."""
    fichiers = build_site(spec_from_brief("Crée un site vitrine pour un port"))
    assemble = "\n".join(fichiers.values())
    assert "http://" not in assemble
    assert "https://" not in assemble
    assert "//cdn" not in assemble


def test_une_application_installable_recoit_manifeste_et_service_worker():
    spec = spec_from_brief("Crée une application installable pour un carnet")
    fichiers = build_site(spec)
    assert spec.installable
    assert set(fichiers) == {
        "index.html", "style.css", "app.js", "manifest.webmanifest", "sw.js",
    }
    manifeste = json.loads(fichiers["manifest.webmanifest"])
    assert manifeste["display"] == "standalone"


def test_le_generateur_n_ecrit_rien_sur_disque(tmp_path):
    build_site(spec_from_brief("Crée un site vitrine"))
    assert not list(tmp_path.iterdir())


def test_la_matiere_fournie_remplit_les_sections_dans_l_ordre():
    spec = spec_from_brief(
        "Crée un site vitrine pour un marché",
        material=["Ouvert du lundi au samedi.", "Trente étals."],
    )
    assert spec.sections[0].body == "Ouvert du lundi au samedi."
    assert spec.sections[1].body == "Trente étals."
    # La troisième n'a rien reçu : elle garde le bouche-trou, qui sera mesuré.
    assert PLACEHOLDER in spec.sections[2].body


# --- Critique -----------------------------------------------------------------


def test_le_critique_repere_une_ressource_distante():
    fichiers = build_site(spec_from_brief("Crée un site vitrine"))
    fichiers["index.html"] = fichiers["index.html"].replace(
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="https://cdn.example.test/joli.css">',
    )
    verdict = critique(fichiers)
    assert "ressource_externe" in verdict.defects
    assert not verdict.deliverable


def test_le_critique_repere_un_lien_mort():
    spec = spec_from_brief("Crée un site vitrine")
    spec.sections[0].cta_href = "#section-inexistante"
    verdict = critique(build_site(spec))
    assert "lien_mort" in verdict.defects


def test_le_critique_mesure_le_contraste_et_le_refuse_sous_le_seuil():
    spec = SiteSpec(
        title="Test", tagline="ligne", background="#606878", surface="#5f6776",
        text="#5a6070", accent="#4a5060",
        sections=[Section(title="Accueil", body="Un texte suffisamment long " * 5)],
    )
    verdict = critique(build_site(spec))
    assert "contraste_insuffisant" in verdict.defects
    assert not verdict.deliverable


def test_un_site_correct_n_a_aucun_defaut_bloquant():
    spec = spec_from_brief(
        "Crée un site vitrine pour un marché couvert",
        material=[
            "Le marché ouvre du lundi au samedi, de six heures à treize heures.",
            "Une trentaine d'étals proposent du poisson, des fruits et des épices.",
            "Le stationnement reste gratuit sur la place adjacente au bâtiment.",
        ],
    )
    verdict = critique(build_site(spec))
    assert verdict.deliverable, verdict.report()
    assert verdict.score >= 90


def test_les_cibles_tactiles_font_au_moins_44_pixels():
    css = build_site(spec_from_brief("Crée un site vitrine"))["style.css"]
    assert f"min-height: {MIN_TAP_TARGET}px" in css


def test_la_couleur_du_bouton_est_calculee_pour_etre_lisible():
    spec = spec_from_brief("Crée un site vitrine")
    spec.accent = "#facc15"
    css = build_site(spec)["style.css"]
    bouton = css.split("--bouton:")[1].split(";")[0].strip()
    assert contrast(bouton, spec.accent) >= 4.5


# --- Interdits de marque : décidable ou déclaré indécidable --------------------


def test_une_regle_de_marque_sans_guillemets_n_est_pas_devinee():
    """Le piège que le projet connaît bien : ne pas inventer une interdiction.

    « ne pas écrire Chindini … : c'est Ouroveni » cite le mot juste **et** le
    mot faux. Extraire les majuscules au hasard signalerait Ouroveni comme une
    faute. On préfère déclarer la règle non vérifiable.
    """
    assert banned_terms("ne pas écrire Chindini comme port : c'est Ouroveni") == []


def test_une_regle_entre_guillemets_est_verifiee():
    assert banned_terms("ne jamais écrire « Chindini »") == ["Chindini"]
    spec = spec_from_brief(
        "Crée un site vitrine", material=["Départ de Chindini chaque samedi."]
    )
    spec.forbidden = ["ne jamais écrire « Chindini »"]
    verdict = critique(build_site(spec), forbidden=spec.forbidden)
    assert "interdit_de_marque" in verdict.defects


def test_les_emojis_sont_reperes_quand_la_marque_les_interdit():
    spec = spec_from_brief("Crée un site vitrine", material=["Nos croissants 🥐 du jour."])
    spec.forbidden = ["pas d'emojis"]
    assert "interdit_de_marque" in critique(
        build_site(spec), forbidden=spec.forbidden
    ).defects


# --- Studio : corriger, et savoir revenir en arrière ---------------------------


def _marque_terne() -> BrandProfile:
    return BrandProfile(
        name="Terne",
        palette=["#3a3f4a", "#40454f", "#4a5060", "#5a6070", "#606878"],
    )


def test_le_studio_corrige_le_contraste_et_ameliore_la_note():
    spec = spec_from_brief("Crée un site vitrine pour un atelier")
    apply_brand(spec, _marque_terne())
    resultat = SiteStudio().run(spec)
    assert resultat.score > resultat.versions[0].score
    assert "contraste_insuffisant" not in resultat.final.critique.defects


def test_le_studio_retire_une_section_vide_plutot_que_d_inventer():
    """Règle de fond : rien n'est fabriqué pour combler un vide."""
    spec = spec_from_brief("Crée un site vitrine pour une épicerie")
    resultat = SiteStudio().run(spec)
    assert PLACEHOLDER not in resultat.files["index.html"]
    assert len(resultat.spec.sections) < 3


def test_le_studio_garde_la_premiere_section_pas_la_derniere():
    resultat = SiteStudio().run(spec_from_brief("Crée un site vitrine pour un port"))
    assert resultat.spec.sections[0].title == "Accueil"


def test_le_studio_s_arrete_et_ne_boucle_pas():
    resultat = SiteStudio(max_iterations=2).run(
        spec_from_brief("Crée un site vitrine pour un atelier")
    )
    assert len(resultat.versions) <= 3
    assert resultat.stopped_because


def test_une_correction_qui_degrade_est_annulee(monkeypatch):
    """Le studio doit savoir dire « version précédente meilleure »."""

    def saboteur(spec):
        spec.text = spec.background  # contraste nul : la note doit chuter
        return "correction volontairement mauvaise"

    monkeypatch.setitem(FIXES, "texte_bouche_trou", saboteur)
    resultat = SiteStudio().run(spec_from_brief("Crée un site vitrine pour un port"))

    assert any(not version.kept for version in resultat.versions)
    assert "version précédente meilleure" in resultat.stopped_because
    assert resultat.final is resultat.versions[0]


def test_un_defaut_bloquant_est_corrige_meme_au_dessus_de_la_note_visee():
    spec = spec_from_brief(
        "Crée un site vitrine pour un marché",
        material=["Le marché ouvre du lundi au samedi de six heures à treize heures. " * 3],
    )
    spec.sections[0].cta_href = "#nulle-part"
    resultat = SiteStudio().run(spec)
    assert not resultat.final.critique.blocking


# --- Mémoire des leçons -------------------------------------------------------


def test_une_correction_sans_effet_ne_devient_pas_une_regle():
    """Garde-fou central : on n'apprend que ce qui a marché."""
    memoire = Lessons()
    memoire.record_defect("contraste_insuffisant")
    memoire.record_fix("contraste_insuffisant", worked=False)
    assert memoire.preventive() == []

    memoire.record_fix("contraste_insuffisant", worked=True)
    assert memoire.preventive() == ["contraste_insuffisant"]


def test_la_memoire_evite_le_defaut_a_la_tache_suivante():
    """Le cœur de la phase 6 : la deuxième tâche part déjà corrigée."""
    memoire = Lessons()
    marque = _marque_terne()

    premier = spec_from_brief("Crée un site vitrine pour un atelier de couture")
    apply_brand(premier, marque)
    tache1 = SiteStudio(memoire).run(premier, task="t1")
    assert tache1.learned

    second = spec_from_brief("Crée un site vitrine pour une école de voile")
    apply_brand(second, marque)
    tache2 = SiteStudio(memoire).run(second, task="t2")

    assert tache2.prevented
    assert tache2.versions[0].score > tache1.versions[0].score
    assert len(tache2.versions) < len(tache1.versions)


def test_la_memoire_survit_a_un_aller_retour_sur_disque(tmp_path):
    chemin = tmp_path / "lessons.json"
    memoire = Lessons(path=chemin)
    memoire.record_defect("lien_mort", task="t1", example="Port")
    memoire.record_fix("lien_mort", worked=True)
    memoire.save()

    relue = Lessons.load(chemin)
    assert relue.items["lien_mort"].fixed == 1
    assert relue.preventive() == ["lien_mort"]


def test_un_fichier_de_lecons_abime_ne_bloque_pas_le_travail(tmp_path):
    chemin = tmp_path / "lessons.json"
    chemin.write_text("{ ceci n'est pas du JSON", encoding="utf-8")
    assert Lessons.load(chemin).items == {}


def test_chaque_code_de_defaut_est_documente():
    """Un code sans libellé serait illisible dans `lessons.json`."""
    for code in FIXES:
        assert code in DEFECTS
    assert Lesson(code="lien_mort").label == DEFECTS["lien_mort"]


# --- Planification ------------------------------------------------------------


@pytest.mark.parametrize(
    "prompt,attendu",
    [
        ("Crée un site vitrine pour la traversée", "vitrine"),
        ("Fais une landing page pour la location", "landing"),
        ("Développe une application web pour les inscriptions", "app"),
        ("Fais-moi un portfolio de photos", "portfolio"),
    ],
)
def test_le_planificateur_reconnait_une_demande_de_site(prompt, attendu):
    assert plan(prompt).site == attendu


@pytest.mark.parametrize(
    "prompt",
    [
        "Quel est le site officiel de la compagnie ?",
        "Trouve les horaires sur le site de la mairie",
        "Cette application coûte combien ?",
    ],
)
def test_une_question_qui_parle_de_site_ne_declenche_pas_une_fabrication(prompt):
    """Sans verbe de fabrication, « site » reste un mot ordinaire."""
    assert plan(prompt).site == ""
