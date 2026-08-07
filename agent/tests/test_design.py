"""Studio créatif : marque, concepts, critique, boucle d'itération (spec §5-§12)."""

from __future__ import annotations

import json

import pytest

from ara.design import color as colors
from ara.design.brand import BrandProfile, moheligo_profile
from ara.design.brief import Brief, from_prompt
from ara.design.canvas import Canvas, Element, estimate_width, wrap
from ara.design.concepts import propose
from ara.design.critic import critique
from ara.design.studio import Studio, improve


@pytest.fixture
def brand():
    return moheligo_profile()


@pytest.fixture
def brief(brand):
    return Brief(
        subject="Traversée en vedette Ouroveni vers Hoani",
        title="Traversée Ouroveni vers Hoani",
        subtitle="Vedettes rapides entre Grande Comore et Mohéli, tous les jours",
        bullets=["Départ quotidien à 7h", "Billet avec QR code", "Météo mer à 7 jours"],
        price="15 000 FC", contact="WhatsApp +269 000 00 00",
        url="https://moheligo.com", audience="touriste", objective="conversion",
        brand=brand,
    )


# --- Couleurs -----------------------------------------------------------------


def test_contraste_wcag():
    assert round(colors.contrast("#ffffff", "#000000"), 1) == 21.0
    assert colors.contrast("#ffffff", "#ffffff") == 1.0


def test_choix_de_la_couleur_de_texte_la_plus_lisible():
    assert colors.readable_on("#0a2550") == "#ffffff"
    assert colors.readable_on("#f7fafc") == "#0b1220"


def test_les_gris_ne_comptent_pas_comme_des_teintes():
    assert colors.distinct_hues(["#ffffff", "#000000", "#888888"]) == 0
    assert colors.distinct_hues(["#ff0000", "#00ff00", "#0000ff"]) == 3


# --- Mémoire de marque (spec §10) ---------------------------------------------


def test_la_marque_se_sauvegarde_et_se_relit(tmp_path, brand):
    path = tmp_path / "brand_profile.json"
    brand.save(path)
    relu = BrandProfile.load(path)
    assert relu.name == "MoheliGo"
    assert relu.palette == brand.palette
    assert relu.avoid == brand.avoid


def test_un_profil_absent_donne_un_profil_neutre(tmp_path):
    assert BrandProfile.load(tmp_path / "absent.json").name == "Sans marque"


def test_un_profil_corrompu_ne_bloque_pas(tmp_path):
    path = tmp_path / "brand_profile.json"
    path.write_text("{ceci n'est pas du json}")
    assert BrandProfile.load(path).name == "Sans marque"


def test_les_interdits_de_la_marque_sont_consultables(brand):
    assert brand.forbids("emoji")
    assert not brand.forbids("photo")


def test_la_memoire_senrichit_sans_ecraser(brand):
    brand.remember(avoid=["ne jamais recadrer le logo"], slogans=[])
    assert len(brand.avoid) == 5
    assert brand.name == "MoheliGo", "un champ non fourni ne doit pas être écrasé"


# --- Brief ---------------------------------------------------------------------


def test_le_brief_extrait_prix_et_lien():
    b = from_prompt("Fais un flyer pour la traversée à 15 000 FC — https://moheligo.com")
    assert b.price.startswith("15 000")
    assert b.url == "https://moheligo.com"
    assert b.format == "flyer"


def test_le_format_demande_est_reconnu():
    assert from_prompt("fais-moi une story pour Instagram").format == "story"
    assert from_prompt("une affiche pour le port").format == "affiche"


def test_le_public_et_lobjectif_sont_deduits():
    b = from_prompt("flyer pour les touristes, objectif : faire réserver en ligne")
    assert b.audience == "touriste"
    assert b.objective == "conversion"


# --- Composition ---------------------------------------------------------------


def test_le_texte_se_coupe_pour_tenir_dans_la_largeur():
    texte = "Vedettes rapides entre la Grande Comore et Mohéli tous les jours de la semaine"
    coupe = wrap(texte, 40, 600, "sans", max_lines=4)
    for ligne in coupe.split("\n"):
        assert estimate_width(ligne, 40, "sans") <= 600 * 1.02


def test_le_svg_produit_est_bien_forme(brief):
    from xml.etree import ElementTree

    for canvas in propose(brief):
        svg = canvas.to_svg()
        assert svg.startswith("<svg")
        ElementTree.fromstring(svg)  # lève si le XML est cassé


def test_les_caracteres_speciaux_sont_echappes():
    canvas = Canvas(100, 100)
    canvas.add(Element("text", "titre", 0, 0, 100, 20, text='Tarifs & <balises> "x"', size=10))
    svg = canvas.to_svg()
    assert "&amp;" in svg and "&lt;" in svg


# --- Concepts (spec §5) --------------------------------------------------------


def test_au_moins_trois_concepts_sont_proposes(brief):
    """La spec l'exige : proposer et confronter, pas un seul jet."""
    concepts = propose(brief)
    assert len(concepts) >= 3
    assert len({c.name for c in concepts}) == len(concepts)


def test_chaque_concept_porte_lessentiel(brief):
    for canvas in propose(brief):
        roles = {e.role for e in canvas.elements}
        assert {"titre", "prix", "cta", "qr", "logo"} <= roles, (
            f"{canvas.name} : rôles manquants {({'titre','prix','cta','qr','logo'}) - roles}"
        )


def test_aucun_concept_ne_deborde_du_cadre(brief):
    for canvas in propose(brief):
        assert canvas.overflows(margin=1) == [], f"{canvas.name} déborde"


def test_le_qr_est_toujours_sombre_sur_clair(brief):
    """Un QR inversé n'est pas scanné par la plupart des lecteurs."""
    for canvas in propose(brief):
        for element in canvas.by_role("qr"):
            assert colors.luminance(element.fill) < colors.luminance(element.on)
            assert element.contrast() >= 7


def test_le_qr_pointe_vers_la_bonne_adresse(brief):
    from ara.design import qr as qrcode

    canvas = propose(brief)[0]
    code = canvas.by_role("qr")[0]
    assert code.text == "https://moheligo.com"
    assert qrcode.decode(qrcode.encode(code.text, "H").matrix) == "https://moheligo.com"


def test_les_interdits_de_marque_sont_respectes(brief):
    """Le patron a dit « pas de Embarquez » : l'agent doit s'en souvenir."""
    for canvas in propose(brief):
        for element in canvas.text_elements():
            assert "embarquez" not in element.text.lower()


def test_sans_lien_aucun_qr_nest_pose(brand):
    brief = Brief(subject="Traversée", price="15 000 FC", url="", brand=brand)
    for canvas in propose(brief):
        assert canvas.by_role("qr") == []


# --- Critique (spec §6) --------------------------------------------------------


def test_les_douze_criteres_sont_notes(brief):
    verdict = critique(propose(brief)[0], brief.brand)
    assert len(verdict.criteria) == 12
    assert all(0 <= c.score <= 100 for c in verdict.criteria)
    assert 0 <= verdict.score <= 100


def test_le_rapport_donne_forts_faibles_et_corrections(brief):
    verdict = critique(propose(brief)[0], brief.brand)
    rapport = verdict.report()
    assert "Note :" in rapport
    assert verdict.strengths or verdict.weaknesses


def test_un_contraste_insuffisant_est_puni():
    canvas = Canvas(1000, 1000, background="#ffffff")
    canvas.add(Element("text", "titre", 50, 50, 900, 100, text="Presque invisible",
                       size=90, fill="#f2f2f2", on="#ffffff"))
    verdict = critique(canvas)
    assert verdict.get("contraste").score < 30
    assert "WCAG" in verdict.get("contraste").correction


def test_une_seule_taille_de_texte_casse_la_hierarchie():
    canvas = Canvas(1000, 1000)
    for i in range(3):
        canvas.add(Element("text", "corps", 50, 100 + i * 100, 900, 40,
                           text=f"Ligne {i}", size=40, fill="#000000", on="#ffffff"))
    assert critique(canvas).get("hierarchie").score < 40


def test_un_debordement_est_bloquant(brief):
    canvas = propose(brief)[0]
    canvas.elements[-1].x = canvas.width + 200
    verdict = critique(canvas, brief.brand)
    assert verdict.blocking
    assert verdict.score <= 55, "un défaut bloquant doit plafonner la note"


def test_un_qr_inverse_est_bloquant():
    canvas = Canvas(1000, 1000, background="#0a2550")
    canvas.add(Element("qr", "qr", 100, 100, 200, 200, fill="#ffffff",
                       on="#0a2550", path="M0 0h1v1z"))
    verdict = critique(canvas)
    assert any("QR" in item for item in verdict.blocking)


def test_un_emoji_est_bloquant_si_la_marque_linterdit(brand):
    canvas = Canvas(1000, 1000)
    canvas.add(Element("text", "titre", 50, 50, 900, 100, text="Traversée 🚤 rapide",
                       size=80, fill="#000000", on="#ffffff"))
    assert any("emoji" in item for item in critique(canvas, brand).blocking)


def test_une_fleche_typographique_nest_pas_un_emoji(brand):
    """« → » est un signe de ponctuation : faux positif constaté en réel."""
    canvas = Canvas(1000, 1000)
    canvas.add(Element("text", "titre", 50, 50, 900, 100, text="Ouroveni → Hoani",
                       size=80, fill="#000000", on="#ffffff"))
    assert not any("emoji" in item for item in critique(canvas, brand).blocking)


# --- Boucle d'itération (spec §7 et §11) --------------------------------------


def test_la_boucle_note_chaque_concept_et_retient_le_meilleur(brief):
    result = Studio(brief.brand, target=95).run(brief)
    assert len(result.concepts) >= 3
    assert result.final is not None
    assert result.final.score == max(v.score for v in result.concepts + result.iterations)


def test_la_premiere_production_nest_jamais_supposee_correcte(brief):
    """Spec §11 : tout est noté, y compris le premier jet."""
    result = Studio(brief.brand, target=100).run(brief)
    assert all(v.critique.criteria for v in result.concepts)
    assert result.stopped_because


def test_le_nombre_diterations_est_borne(brief):
    result = Studio(brief.brand, max_iterations=2, target=100).run(brief)
    assert len(result.iterations) <= 4


def test_une_correction_qui_degrade_est_annulee(brand):
    """Spec §11 : « version précédente meilleure » et retour arrière."""
    from ara.design.critic import Critique, Criterion
    from ara.design import studio as studio_module

    def sabotage(canvas, verdict, brand):
        pire = studio_module._clone(canvas)
        for element in pire.text_elements():
            element.fill = element.on          # contraste nul
        return pire, ["dégradation volontaire"]

    brief = Brief(subject="Traversée", title="Traversée", price="15 000 FC",
                  url="https://moheligo.com", brand=brand)
    original = studio_module.improve
    studio_module.improve = sabotage
    try:
        result = Studio(brand, max_iterations=3, target=100).run(brief)
    finally:
        studio_module.improve = original

    annulees = [v for v in result.iterations if not v.kept]
    assert annulees, "la version dégradée doit être annulée"
    assert "précédente meilleure" in result.stopped_because
    assert result.final.score > annulees[0].score


def test_les_corrections_sont_mecaniques_pas_des_commentaires(brand):
    """Un critique qui ne fait que commenter laisse la boucle tourner à vide."""
    canvas = Canvas(2000, 2500, background="#ffffff")
    canvas.add(Element("text", "titre", 100, 100, 1800, 200, text="Titre principal",
                       size=180, font="serif", fill="#eeeeee", on="#ffffff"))
    canvas.add(Element("text", "corps", 100, 400, 1800, 60, text="Un argument",
                       size=50, font="sans", fill="#333333", on="#ffffff"))
    verdict = critique(canvas, brand)
    ameliore, applied = improve(canvas, verdict, brand)

    assert applied, "au moins une correction doit être appliquée"
    assert critique(ameliore, brand).score > verdict.score


def test_le_rapport_final_est_lisible(brief):
    result = Studio(brief.brand, target=95).run(brief)
    rapport = result.report()
    assert "Concepts proposés" in rapport
    assert "Version finale" in rapport
    assert "Arrêt :" in rapport


def test_le_resultat_est_serialisable(brief):
    result = Studio(brief.brand, target=95).run(brief)
    json.dumps(result.to_dict(), ensure_ascii=False)
