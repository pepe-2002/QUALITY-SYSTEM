"""Routines et ordonnanceur (Phase 5).

L'automatisation agit quand personne ne regarde. Ces tests portent donc moins
sur « est-ce que ça marche » que sur « est-ce que ça refuse quand il faut » :
horaire mal compris, batterie basse, exécution déjà en cours, échecs répétés.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import pytest

from ara.automation.routines import (
    MAX_CONSECUTIVE_FAILURES,
    MAX_ROUTINES,
    Routine,
    RoutineError,
    RoutineStore,
    build_routine,
)
from ara.automation.schedule import Schedule, parse_schedule
from ara.automation.scheduler import Scheduler

# --- lecture d'un horaire --------------------------------------------------


@pytest.mark.parametrize(
    "phrase, attendu",
    [
        ("chaque matin", "tous les jours à 07:00"),
        ("tous les jours à 7h30", "tous les jours à 07:30"),
        ("tous les jours à 19:15", "tous les jours à 19:15"),
        ("chaque soir", "tous les jours à 19:00"),
        ("chaque lundi à 8h", "chaque lundi à 08:00"),
        ("tous les vendredis à 17h", "chaque vendredi à 17:00"),
        ("toutes les 6 heures", "toutes les 6 heures"),
        ("toutes les 30 minutes", "toutes les 30 minutes"),
    ],
)
def test_les_horaires_courants_sont_compris(phrase, attendu):
    plan = parse_schedule(phrase)
    assert plan is not None and plan.describe() == attendu


@pytest.mark.parametrize(
    "phrase",
    ["de temps en temps", "souvent", "quand tu peux", "", "à 7h", "demain"],
)
def test_un_horaire_flou_ne_produit_rien(phrase):
    """Refuser vaut mieux que deviner : personne ne veut d'exécutions surprises."""
    assert parse_schedule(phrase) is None


def test_un_intervalle_trop_court_est_releve_au_minimum():
    plan = parse_schedule("toutes les 2 minutes")
    assert plan.minutes == 15


def test_un_intervalle_delirant_est_refuse():
    assert parse_schedule("toutes les 900 heures") is None


# --- calcul de la prochaine exécution --------------------------------------


def _stamp(annee, mois, jour, heure, minute=0):
    return time.mktime((annee, mois, jour, heure, minute, 0, 0, 0, -1))


def test_quotidien_le_meme_jour_si_l_heure_n_est_pas_passee():
    plan = Schedule(kind="daily", hour=7)
    suivant = plan.next_after(_stamp(2026, 8, 7, 5, 0))
    assert time.localtime(suivant).tm_hour == 7
    assert time.localtime(suivant).tm_mday == 7


def test_quotidien_le_lendemain_si_l_heure_est_passee():
    plan = Schedule(kind="daily", hour=7)
    suivant = plan.next_after(_stamp(2026, 8, 7, 9, 0))
    assert time.localtime(suivant).tm_mday == 8


def test_hebdomadaire_tombe_sur_le_bon_jour():
    plan = Schedule(kind="weekly", hour=8, weekday=0)   # lundi
    suivant = plan.next_after(_stamp(2026, 8, 7, 9, 0))  # un vendredi
    assert time.localtime(suivant).tm_wday == 0
    assert suivant > _stamp(2026, 8, 7, 9, 0)


def test_intervalle_avance_de_la_duree_prevue():
    plan = Schedule(kind="interval", minutes=90)
    depart = _stamp(2026, 8, 7, 9, 0)
    assert plan.next_after(depart) == pytest.approx(depart + 90 * 60)


# --- création d'une routine ------------------------------------------------


def test_une_routine_naît_avec_sa_prochaine_echeance():
    routine = build_routine("Vérifie les tarifs des traversées", "chaque matin")
    assert routine.next_run > time.time()
    assert routine.enabled


def test_un_horaire_incompris_refuse_la_routine():
    with pytest.raises(RoutineError) as erreur:
        build_routine("Vérifie les tarifs", "quand tu veux")
    assert "chaque matin" in str(erreur.value)   # le message propose des exemples


def test_une_demande_vide_refuse_la_routine():
    with pytest.raises(RoutineError):
        build_routine("  ", "chaque matin")


# --- registre --------------------------------------------------------------


@pytest.fixture
def store(tmp_path):
    return RoutineStore(tmp_path / "routines.json")


def test_le_registre_survit_au_redemarrage(store, tmp_path):
    routine = store.add(build_routine("Veille tarifs traversées", "chaque matin"))
    relu = RoutineStore(tmp_path / "routines.json").get(routine.routine_id)
    assert relu is not None and relu.prompt == routine.prompt


def test_suppression(store):
    routine = store.add(build_routine("Veille tarifs traversées", "chaque matin"))
    assert store.delete(routine.routine_id)
    assert store.get(routine.routine_id) is None
    assert not store.delete(routine.routine_id)


def test_le_nombre_de_routines_est_plafonne(store):
    for index in range(MAX_ROUTINES):
        store.add(build_routine(f"Veille numéro {index} sur les tarifs", "chaque matin"))
    with pytest.raises(RoutineError):
        store.add(build_routine("Une de trop sur les tarifs", "chaque matin"))


def test_un_fichier_illisible_ne_fait_pas_tomber_le_registre(tmp_path):
    chemin = tmp_path / "routines.json"
    chemin.write_text("{ceci n'est pas du json", encoding="utf-8")
    assert RoutineStore(chemin).list() == []


# --- garde-fous de la routine ---------------------------------------------


def test_trois_echecs_consecutifs_suspendent_la_routine():
    routine = build_routine("Veille tarifs traversées", "chaque matin")
    for _ in range(MAX_CONSECUTIVE_FAILURES):
        routine.note_result(False, "error")
    assert not routine.enabled
    assert "échecs consécutifs" in routine.disabled_reason


def test_un_succes_remet_le_compteur_a_zero():
    routine = build_routine("Veille tarifs traversées", "chaque matin")
    routine.note_result(False, "error")
    routine.note_result(True, "done")
    assert routine.failures == 0 and routine.enabled


def test_une_routine_suspendue_dit_pourquoi():
    routine = build_routine("Veille tarifs traversées", "chaque matin")
    routine.disable("désactivée à la main")
    assert routine.disabled_reason and not routine.enabled


# --- ordonnanceur ----------------------------------------------------------


@dataclass
class FauxRecord:
    task_id: str = "t1"
    status: str = "done"
    answer: str = "réponse"
    errors: list = field(default_factory=list)

    def summary(self):
        return {"task_id": self.task_id, "status": self.status}


class FauxService:
    """Service minimal : compte les lancements, ne fait rien de coûteux."""

    def __init__(self, settings, statut: str = "done") -> None:
        self.settings = settings
        from ara.core.permissions import PermissionManager

        self.permissions = PermissionManager(settings)
        self.lancements: list[str] = []
        self.statut = statut

    def start(self, prompt: str) -> FauxRecord:
        self.lancements.append(prompt)
        return FauxRecord(task_id=f"t{len(self.lancements)}", status=self.statut)

    def wait(self, task_id: str, timeout: float = 0) -> FauxRecord:
        return FauxRecord(task_id=task_id, status=self.statut)


@pytest.fixture
def scheduler(store, isolated_settings):
    service = FauxService(isolated_settings)
    ordonnanceur = Scheduler(service, store, battery_reader=lambda: None)
    return ordonnanceur


def _due(store, **kwargs) -> Routine:
    routine = build_routine(kwargs.pop("prompt", "Veille tarifs traversées"), "chaque matin")
    for cle, valeur in kwargs.items():
        setattr(routine, cle, valeur)
    routine.next_run = time.time() - 60      # échue il y a une minute
    return store.add(routine)


def test_une_routine_echue_est_lancee(scheduler, store):
    _due(store)
    decision = scheduler.tick()
    assert len(decision.to_run) == 1
    assert scheduler.service.lancements == ["Veille tarifs traversées"]


def test_une_routine_non_echue_n_est_pas_lancee(scheduler, store):
    store.add(build_routine("Veille tarifs traversées", "chaque matin"))
    assert scheduler.tick().to_run == []
    assert scheduler.service.lancements == []


def test_apres_lancement_la_prochaine_echeance_est_dans_le_futur(scheduler, store):
    routine = _due(store)
    scheduler.tick()
    assert store.get(routine.routine_id).next_run > time.time()


def test_pas_de_rattrapage_en_rafale(scheduler, store):
    """Téléphone éteint toute la nuit : une seule exécution, pas dix."""
    routine = _due(store)
    routine.next_run = time.time() - 12 * 3600
    store.save(routine)
    scheduler.tick()
    scheduler.tick()
    assert len(scheduler.service.lancements) == 1


def test_une_batterie_basse_reporte_au_lieu_de_lancer(store, isolated_settings):
    service = FauxService(isolated_settings)
    ordonnanceur = Scheduler(service, store, battery_reader=lambda: 9)
    routine = _due(store, min_battery=20)
    decision = ordonnanceur.tick()
    assert decision.to_run == []
    assert "batterie" in decision.skipped[0][1]
    # …et la routine est reprogrammée, pas perdue
    assert store.get(routine.routine_id).next_run > time.time()


def test_une_batterie_inconnue_ne_bloque_rien(scheduler, store):
    _due(store, min_battery=90)
    assert len(scheduler.tick().to_run) == 1


def test_une_execution_en_cours_bloque_la_suivante(scheduler, store):
    routine = _due(store)
    scheduler._running[routine.routine_id] = time.time()
    routine.next_run = time.time() - 10
    store.save(routine)
    decision = scheduler.tick()
    assert decision.to_run == []
    assert "précédente" in decision.skipped[0][1]


def test_le_plafond_quotidien_est_respecte(scheduler, store):
    routine = _due(store)
    routine.day_stamp = time.strftime("%Y-%m-%d")
    routine.runs_today = 999
    store.save(routine)
    decision = scheduler.tick()
    assert decision.to_run == []
    assert "plafond" in decision.skipped[0][1]


def test_un_echec_de_tache_est_compte_par_la_routine(store, isolated_settings):
    service = FauxService(isolated_settings, statut="error")
    ordonnanceur = Scheduler(service, store, battery_reader=lambda: None)
    routine = _due(store)
    ordonnanceur.tick()
    time.sleep(0.2)                              # le suivi tourne dans un fil
    assert store.get(routine.routine_id).failures >= 1


def test_la_notification_passe_par_la_liste_blanche(store, isolated_settings):
    """Une routine n'obtient aucun droit qu'une demande manuelle n'aurait pas."""
    service = FauxService(isolated_settings)
    service.permissions.revoke("notify_phone")
    ordonnanceur = Scheduler(service, store, battery_reader=lambda: None)
    ordonnanceur._notify(build_routine("Veille tarifs traversées", "chaque matin"), FauxRecord())
    assert "notification impossible" in ordonnanceur.last_error
    assert "notify_phone" in ordonnanceur.last_error


def test_l_ordonnanceur_ne_demarre_pas_sans_autorisation(isolated_settings):
    from ara.service import TaskService

    service = TaskService(isolated_settings)
    assert service.settings.automation_enabled is False
    assert service.start_scheduler() is False
    assert not service.scheduler.running
