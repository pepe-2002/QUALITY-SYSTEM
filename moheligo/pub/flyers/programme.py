#!/usr/bin/env python3
"""Publie la publication du jour (celle de midi), d'après `calendrier.py`.

    python3 programme.py                 # répétition à blanc (midi)
    python3 programme.py --publier       # pour de vrai
    python3 programme.py --matin         # le créneau du matin (démonstration)
    python3 programme.py --jour 2026-08-14   # essayer un autre jour

Le bulletin du soir a son propre chemin (`bulletin.py` puis `publier_fb.py`) :
lui est daté et doit être fabriqué le jour même. Ici, les visuels existent déjà
dans le dépôt — donc aucun rendu à faire, la publication prend deux secondes.

Deux interrupteurs, dans cet ordre :
  PAUSE_FB = oui   → rien ne part, quoi qu'il arrive. Le frein d'urgence.
  PUBLIER_FB = oui → arme la publication automatique (côté workflow).

Et deux garde-fous, qui passent AVANT le calendrier :
  1. `service.py` — service fermé → aucun message commercial, l'avis à la place ;
  2. `mer.py`     — houle ≥ 2,50 m → l'avis de grosse mer à la place.
Dans les deux cas ce n'est pas une panne : c'est le travail. On ne vend pas une
traversée qu'on n'est pas sûr de faire.
"""
import argparse
import datetime
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import calendrier                              # noqa: E402
import mer                                     # noqa: E402
import page                                    # noqa: E402
import publier_fb                              # noqa: E402
import service                                 # noqa: E402

GROS_TEMPS = 'flyer-grostemps-facebook.png'

MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
        'août', 'septembre', 'octobre', 'novembre', 'décembre']


def avis_de_gros_temps(jour):
    """(visuel, texte) de l'avis de mer forte, avec les vrais chiffres du jour."""
    modele = next(f['texte'] for f in page.FLYERS if f['png'] == GROS_TEMPS)
    n, etat, houle = mer.niveau(jour)
    return GROS_TEMPS, modele.format(etat=etat.capitalize(),
                                     houle=('%.1f' % houle).replace('.', ','))


def avis_de_suspension():
    """(visuel, texte) de l'avis de service suspendu, daté depuis service.py."""
    modele = next(f['texte'] for f in page.FLYERS if f['png'] == service.VISUEL_AVIS)
    d = datetime.date.fromisoformat(service.FERMETURE['depuis'])
    return service.VISUEL_AVIS, modele.format(
        depuis='%d %s' % (d.day, MOIS[d.month - 1]),
        raison=service.FERMETURE.get('raison') or 'la mer')


def envoyer(visuel, texte, quoi, a):
    """Annonce ce qu'on publie, puis le confie à publier_fb."""
    print('Publication        :', quoi)
    print('Visuel             :', visuel)

    if texte.startswith('@'):                  # sécurité : jamais le bulletin ici
        sys.exit('Ce contenu est daté, il passe par bulletin.py — pas par programme.py.')

    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write(texte)
        chemin = fh.name
    try:
        publier_fb.publier(visuel, chemin, a.publier or a.essai, essai=a.essai)
    finally:
        os.unlink(chemin)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jour', help='AAAA-MM-JJ, par défaut aujourd\'hui')
    ap.add_argument('--publier', action='store_true')
    ap.add_argument('--essai', action='store_true')
    ap.add_argument('--matin', action='store_true',
                    help='publier le créneau du matin (démonstration) au lieu de midi')
    ap.add_argument('--avis', action='store_true',
                    help='forcer l\'avis de service suspendu (le robot ne le sort '
                         'de lui-même que le premier jour de la fermeture)')
    a = ap.parse_args()

    if os.environ.get('PAUSE_FB', '').strip().lower() == 'oui':
        print('PAUSE_FB = oui → publication suspendue, rien n\'a été envoyé.')
        return

    jour = datetime.date.fromisoformat(a.jour) if a.jour else datetime.date.today()

    # ---- LE SERVICE EST-IL OUVERT ? (avant tout le reste) ------------------
    # Le patron, 12/08/2026 : « les traversées sont fermées jusqu'à nouvel ordre
    # […] à cause de la mer agitée. » Fermé, aucun message commercial ne part :
    # « réserve ta place » un jour sans vedette, c'est le client qui descend au
    # port pour rien, et qui ne revient plus (§ 11 et § 14.2 du manuel).
    # Ça passe AVANT le garde-fou de la mer : la fermeture est déjà la
    # conséquence de la mer, et c'est la nouvelle la plus importante du jour.
    ouvert_service, etat_service = service.etat(jour)
    if not ouvert_service:
        print('⛔', etat_service)
        # L'avis part UNE fois, le premier jour — pas tous les jours à
        # l'identique : une page qui répète le même avis se fait masquer. Les
        # jours suivants, c'est le bulletin du soir qui porte la nouvelle (son
        # bandeau dit « TRAVERSÉES SUSPENDUES », voir service.cta_bulletin).
        # Règle sans mémoire : le robot ne garde aucun état entre deux
        # exécutions (le journal ne survit pas au serveur GitHub), donc on
        # compare la date, et `--avis` sert à le republier à la main.
        premier_jour = jour.isoformat() == service.FERMETURE.get('depuis')
        if not (a.avis or (premier_jour and not a.matin)):
            print('→ rien ne part : ni pub, ni avis (déjà annoncé le %s).'
                  % service.FERMETURE.get('depuis'))
            print('→ pour republier l\'avis : programme.py --avis --publier')
            return
        visuel, texte = avis_de_suspension()
        envoyer(visuel, texte,
                'AVIS DE SERVICE SUSPENDU — aucun message commercial', a)
        return

    if a.matin:
        prevu = calendrier.du_matin(jour)
        # Rien de prévu ce matin-là n'est PAS une erreur : le matin ne sort que
        # deux jours par semaine. Sortir en échec ferait clignoter le workflow
        # cinq matins sur sept, et un voyant rouge qu'on apprend à ignorer ne
        # sert plus à rien le jour où il compte vraiment.
        if prevu is None:
            print('Aucune démonstration prévue ce matin (%s) — rien à publier.'
                  % calendrier.JOURS[jour.weekday()])
            return
        visuel, texte, quoi = prevu
    else:
        visuel, texte, quoi = calendrier.du_jour(jour)

    # ---- le garde-fou de la mer -------------------------------------------
    # Le patron, 11/08/2026 : « en mauvais temps les vedettes ne partent pas ».
    # Donc les jours de mer forte, on ne publie pas de message commercial : on
    # publie l'avis de mer. Une pub qui invite à descendre au port un jour où la
    # vedette peut rester à quai est une promesse qu'on ne tient pas.
    gros = mer.gros_temps(jour)
    if gros is True:
        # Un avis suffit par jour. Le matin est le meilleur moment pour le
        # donner (c'est là qu'on décide de descendre au port), donc les jours
        # où un créneau du matin existe, midi se tait. Aucun état à conserver
        # entre les deux exécutions : le calendrier suffit à trancher — et le
        # journal des publications, lui, ne survit pas à la fin du travail
        # GitHub (voir MEMOIRE.md).
        if not a.matin and calendrier.du_matin(jour) is not None:
            print('Mer forte, et l\'avis est déjà parti ce matin (%s) :'
                  ' rien à midi, on ne se répète pas.'
                  % calendrier.JOURS[jour.weekday()])
            return
        visuel, texte = avis_de_gros_temps(jour)
        quoi = 'AVIS DE MER FORTE — aucun message commercial aujourd\'hui'
    elif gros is None:
        # On ne sait pas : on publie quand même. Nos textes ne promettent jamais
        # qu'une vedette partira, et se taire à chaque hoquet d'Open-Meteo
        # ferait des trous dans la régularité, qui est notre seul vrai actif.
        print('⚠️  État de la mer inconnu (Open-Meteo injoignable) :'
              ' publication normale, aucun message ne promet un départ.')

    envoyer(visuel, texte, quoi, a)


if __name__ == '__main__':
    main()
