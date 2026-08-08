"""RESEARCH-V2 : tests adversariaux.

Chaque test correspond à un mode d'échec réel. Deux d'entre eux documentent
une **limite non résolue** plutôt qu'un succès : les noms voisins et le
hors-période. Les écrire ainsi est le seul moyen de ne pas se raconter que le
problème est réglé.
"""

from __future__ import annotations

import pathlib

import pytest

from ara.agents import queries as q
from ara.agents.research_v2 import (
    BASELINE_VERSION,
    RESEARCH_VERSION,
    ResearchAgentV2,
    TopicRelevance,
    followup_queries_v2,
)
from ara.core.models import SourceDoc

QUESTION = "Quel est le tarif officiel de la traversée en vedette entre la Grande Comore et Mohéli ?"


def _doc(title: str, text: str = "", url: str = "https://x.test/a") -> SourceDoc:
    return SourceDoc(url=url, title=title, text=text)


def _relevant(doc: SourceDoc, question: str = QUESTION) -> bool:
    return TopicRelevance(question)(doc, True)


# --- Défaut 1 : requêtes avec prépositions et fragments -----------------------


@pytest.mark.parametrize(
    "fragment",
    [
        "tarif officiel de la traversée en vedette entre",
        "prix du billet pour",
        "distance entre la ville et",
        "horaire de départ vers",
    ],
)
def test_une_requete_ne_finit_jamais_sur_une_preposition(fragment):
    nettoye = q.clean_fragment(fragment)
    assert nettoye.split()[-1] not in q.FUNCTION_WORDS


def test_le_cas_exact_observe_en_reel():
    """« …en vedette entre tarif officiel » ne doit plus pouvoir se produire."""
    requete = q.compose_query(
        "tarif officiel de la traversée en vedette entre", "tarif officiel"
    )
    assert "entre tarif" not in requete
    assert requete == "tarif officiel de la traversee en vedette"


def test_un_complement_deja_present_n_est_pas_recolle():
    requete = q.compose_query("horaire officiel du départ", "horaire officiel")
    assert requete.count("horaire") == 1
    assert requete.count("officiel") == 1


def test_un_fragment_entierement_grammatical_ne_produit_rien():
    assert q.clean_fragment("de la vers le") == ""
    assert q.compose_query("de la", "vers le") == ""


# --- Défaut 2 : mots-clés orphelins -------------------------------------------


@pytest.mark.parametrize("orphelin", ["grande", "nord", "ile", "de", "le", "a"])
def test_un_mot_generique_isole_ne_devient_pas_une_relance(orphelin):
    assert q.is_orphan(orphelin, "tarif de la traversée")


@pytest.mark.parametrize("utile", ["horaire officiel", "moheli", "reglement interieur"])
def test_un_complement_porteur_est_conserve(utile):
    assert not q.is_orphan(utile, "tarif de la traversée")


def test_une_relance_garde_toujours_le_sujet():
    """« entre grande » n'est pas une requête : il manque le sujet."""
    from ara.analysis.coverage import Gap

    gaps = [Gap(kind="keyword", label="« moheli » absent", hint="moheli")]
    relances = followup_queries_v2("tarif de la traversée", gaps, [], set())
    assert relances
    for requete, _raison in relances:
        assert "tarif" in requete and "traversee" in requete


def test_un_gap_orphelin_ne_produit_aucune_relance():
    from ara.analysis.coverage import Gap

    gaps = [Gap(kind="keyword", label="« grande » absent", hint="grande")]
    assert followup_queries_v2("tarif de la traversée", gaps, [], set()) == []


# --- Défaut 3 : pertinence contextuelle ---------------------------------------


def test_pays_different_meme_vocabulaire():
    """Le faux positif exact rencontré en réel."""
    page = _doc(
        "Nos tarifs 2026 — Vedettes de Bréhat",
        "Traversée en vedette vers l'île, tarifs et horaires officiels.",
    )
    assert not _relevant(page)


def test_termes_generiques_seuls_ne_suffisent_pas():
    page = _doc("Voyager en bateau", "Le tarif d'une traversée en vedette varie.")
    assert not _relevant(page)


def test_une_source_du_bon_sujet_passe():
    page = _doc("MoheliGo", "Traversées en vedette entre la Grande Comore et Mohéli.")
    assert _relevant(page)


def test_un_seul_terme_distinctif_suffit():
    """Une source qui ne cite que « Mohéli » reste pertinente."""
    page = _doc("Mohéli pratique", "Le billet coûte 15 000 francs comoriens.")
    assert _relevant(page)


def test_le_qualificatif_seul_ne_rend_pas_pertinent():
    """« Grande » est un qualificatif, pas une identité."""
    page = _doc("La grande traversée", "Une grande traversée en vedette.")
    assert not _relevant(page)


def test_lexicalement_proche_mais_geographiquement_faux():
    page = _doc(
        "Traversées du delta — billets",
        "Le tarif officiel de la traversée en pirogue est de 1 400 francs.",
    )
    assert not _relevant(
        page, "Combien coûte la traversée en pirogue entre Bandiagara et Songho ?"
    )


def test_meme_objet_autre_contexte():
    """Le sujet est bien nommé, mais on parle d'autre chose à son propos.

    Le filtre de pertinence **laisse passer** : la page parle bien du lieu
    demandé. C'est à l'analyse de constater qu'elle ne répond pas — un filtre
    qui rejetterait ici écarterait aussi des sources utiles.
    """
    page = _doc(
        "Bandiagara — histoire du site",
        "Bandiagara est connue pour ses falaises classées depuis 1989.",
    )
    assert _relevant(
        page, "Combien coûte la traversée en pirogue entre Bandiagara et Songho ?"
    )


def test_sans_terme_distinctif_le_filtre_ne_s_applique_pas():
    """Mieux vaut ne rien filtrer que filtrer au hasard."""
    page = _doc("Le prix des timbres", "Un timbre coûte 1,29 euro.")
    assert _relevant(page, "combien coûte un timbre ?")


# --- Limites documentées, pas résolues ----------------------------------------


def test_limite_connue_les_noms_voisins_passent_encore():
    """Deux lieux qui partagent un nom ne sont pas distingués.

    Le séparer demanderait un référentiel géographique, que ce système n'a
    pas. Ce test fige le comportement actuel pour que la limite reste visible
    au lieu d'être oubliée — s'il se met à échouer, c'est que quelqu'un a
    résolu le problème et doit mettre le rapport à jour.
    """
    page = _doc(
        "Bac de Bandiagara-Nord",
        "La traversée du bac de Bandiagara-Nord coûte 700 francs.",
    )
    assert _relevant(
        page, "Combien coûte la traversée en pirogue entre Bandiagara et Songho ?"
    )


def test_limite_connue_une_archive_reste_pertinente():
    """Le hors-période n'est pas l'affaire du filtre de pertinence.

    Une archive parle bien du sujet ; c'est sa **date** qui doit être lue, et
    c'est le travail de l'agent contexte (`analysis/validate.py`).
    """
    page = _doc(
        "Bandiagara — tarifs 2014 (archive)",
        "En 2014, la traversée entre Bandiagara et Songho coûtait 900 francs.",
    )
    assert _relevant(
        page, "Combien coûte la traversée en pirogue entre Bandiagara et Songho ?"
    )


# --- Aucune liste noire --------------------------------------------------------


def test_le_code_ne_contient_aucun_nom_propre_de_piege():
    """La consigne était de corriger le mécanisme, pas d'interdire des sites.

    On inspecte les **données** du module — littéraux et identifiants — et non
    sa prose : les noms des sites fautifs ont toute leur place dans la
    documentation qui explique le défaut, aucune dans le code qui le corrige.
    """
    import ast

    arbre = ast.parse(pathlib.Path(q.__file__).read_text(encoding="utf-8"))
    docstrings = {
        noeud.body[0].value
        for noeud in ast.walk(arbre)
        if isinstance(noeud, (ast.Module, ast.FunctionDef, ast.ClassDef))
        and noeud.body
        and isinstance(noeud.body[0], ast.Expr)
        and isinstance(noeud.body[0].value, ast.Constant)
    }
    donnees = " ".join(
        [
            *(
                str(noeud.value).lower()
                for noeud in ast.walk(arbre)
                if isinstance(noeud, ast.Constant) and noeud not in docstrings
            ),
            *(
                noeud.id.lower()
                for noeud in ast.walk(arbre)
                if isinstance(noeud, ast.Name)
            ),
        ]
    )
    for nom in ("brehat", "bréhat", "odet", "moheli", "mohéli", "comore",
                "bandiagara", "songho"):
        assert nom not in donnees, nom


# --- La baseline reste gelée ---------------------------------------------------


def test_les_deux_versions_sont_identifiees():
    assert "V2" in RESEARCH_VERSION
    assert "gel" in BASELINE_VERSION.lower()


def test_la_baseline_n_utilise_pas_le_nouveau_filtre():
    from ara.agents.gather import SourceCollector
    import inspect

    signature = inspect.signature(SourceCollector.__init__)
    assert signature.parameters["relevance"].default is None, (
        "sans valeur par défaut nulle, la baseline changerait de comportement"
    )


def test_v2_installe_son_filtre():
    from ara.agents.planner import plan
    from ara.core.context import TaskContext  # noqa: F401  (documentation)

    assert issubclass(ResearchAgentV2, __import__(
        "ara.agents.research", fromlist=["ResearchAgent"]
    ).ResearchAgent)


# --- Jeu 4 ---------------------------------------------------------------------


def test_le_jeu_4_est_separe_des_trois_autres():
    from ara.lab.adversarial import PAGES as JEU4, TASKS
    from ara.lab.corpus import Corpus
    from ara.lab.heldout import PAGES as JEU2
    from ara.lab.heldout2 import PAGES as JEU3

    assert set(JEU4) & set(Corpus().pages) == set()
    assert set(JEU4) & set(JEU2) == set()
    assert set(JEU4) & set(JEU3) == set()
    assert len(TASKS) >= 4


def test_le_jeu_4_etiquette_chaque_page():
    from ara.lab.adversarial import PAGES, label_of

    for url in PAGES:
        assert label_of(url) != "inconnu", url


def test_le_jeu_4_contient_les_cinq_formes_de_piege():
    from ara.lab.adversarial import LABELS

    assert {"autre_lieu", "nom_voisin", "generique", "perime", "autre_contexte"} <= set(
        LABELS.values()
    )


# --- Adoption ------------------------------------------------------------------


def test_v2_est_le_moteur_par_defaut_de_l_application():
    """Adopté après l'expérience du jeu 4, pas avant."""
    from ara.agents.engines import DEFAULT_ENGINE

    assert DEFAULT_ENGINE == "v2"


def test_la_baseline_reste_joignable():
    """Elle n'est pas supprimée : elle reste le moteur gelé de H1 et H2."""
    from ara.agents.engines import ENGINES
    from ara.agents.research import ResearchAgent

    assert ENGINES["baseline"] is ResearchAgent


def test_le_moteur_peut_etre_force_par_l_environnement(monkeypatch):
    from ara.agents import engines

    monkeypatch.setenv("ARA_RESEARCH_ENGINE", "baseline")
    assert engines.engine_name() == "baseline"
    monkeypatch.setenv("ARA_RESEARCH_ENGINE", "n-importe-quoi")
    assert engines.engine_name() == engines.DEFAULT_ENGINE


def test_le_laboratoire_n_utilise_jamais_le_moteur_par_defaut():
    """Sinon changer le défaut rendrait H1 et H2 irreproductibles."""
    import inspect

    from ara.lab import research_exp, strategies

    for module in (strategies, research_exp):
        source = inspect.getsource(module)
        assert "engines" not in source, module.__name__
