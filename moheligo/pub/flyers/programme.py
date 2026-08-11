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
"""
import argparse
import datetime
import os
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import calendrier                              # noqa: E402
import publier_fb                              # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jour', help='AAAA-MM-JJ, par défaut aujourd\'hui')
    ap.add_argument('--publier', action='store_true')
    ap.add_argument('--essai', action='store_true')
    ap.add_argument('--matin', action='store_true',
                    help='publier le créneau du matin (démonstration) au lieu de midi')
    a = ap.parse_args()

    if os.environ.get('PAUSE_FB', '').strip().lower() == 'oui':
        print('PAUSE_FB = oui → publication suspendue, rien n\'a été envoyé.')
        return

    jour = datetime.date.fromisoformat(a.jour) if a.jour else datetime.date.today()

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


if __name__ == '__main__':
    main()
