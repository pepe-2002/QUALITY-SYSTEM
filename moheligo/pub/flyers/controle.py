#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE CONTRÔLE AVANT DE DIRE « C'EST BON » — jour par jour, sans rien publier.

    python3 controle.py                      # d'aujourd'hui à dans 7 jours
    python3 controle.py --jusqu-au 2026-08-18
    python3 controle.py --ouvert             # simule la réouverture

Le patron, 12/08/2026 : « y'a pas d'erreur ? vérifie jusqu'à mardi. » Répondre
« c'est bon » sans avoir déroulé les jours, c'est deviner. Ce script déroule.

CE QU'IL VÉRIFIE, POUR CHAQUE JOUR ET CHAQUE CRÉNEAU (matin, midi, soir) :
  1. le visuel prévu EXISTE, au bon format (1080 × 1350 en 2×, sous 4 Mo) ;
  2. le texte existe, n'est pas vide, et ne contient plus AUCUN trou `{...}`
     non rempli — c'est l'erreur qui se voit le plus sur une page publique ;
  3. pendant une fermeture, aucun mot commercial ne sort : ni « réserve »,
     ni un prix, ni « ta place » (la liste est dans MOTS_QUI_VENDENT) ;
  4. le bulletin du soir ne promet pas de départ pendant une fermeture ;
  5. l'avis de fermeture ne promet pas de date de reprise (« reprennent
     mardi »), et n'écrit pas « on ne te vend rien » (deux interdits du patron).

⚠️ Ce script ne publie RIEN et ne touche à rien. Il lit, il déroule, il compte.
⚠️ Il ne remplace pas l'œil du patron : il dit qu'un visuel n'est pas cassé,
   pas qu'il est beau.
"""
import argparse
import datetime
import pathlib
import re
import sys

from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import calendrier                              # noqa: E402
import page                                    # noqa: E402
import programme                                # noqa: E402
import publier_fb                               # noqa: E402
import service                                 # noqa: E402

ICI = pathlib.Path(__file__).parent
JOURS = calendrier.JOURS

# Ce qui n'a RIEN à faire dans une publication pendant une fermeture.
MOTS_QUI_VENDENT = [
    'réserve ta place', 'réserve pour demain', 'ta place se prend',
    'ta place pour demain', 'réserve maintenant', 'embarque tranquille',
    'francs comoriens', '15 000 fc', 'prix', 'paie par', 'paiement mvola',
]
# Ce qu'on n'écrit jamais, fermé ou ouvert (§ 11 du manuel).
INTERDITS = [
    ('reprennent mardi', 'annonce une date de reprise comme une promesse'),
    ('reprise mardi', 'annonce une date de reprise comme une promesse'),
    ('on ne te vend rien', 'formule refusée par le patron le 12/08/2026'),
    ('on te vend rien', 'formule refusée par le patron le 12/08/2026'),
    ('les vedettes ne partent pas', 'affirme un seuil d\'annulation qu\'on ignore'),
]

ennuis = []
remarques = []


def pb(quoi):
    ennuis.append(quoi)


def visuel_ok(nom, ou):
    """Le fichier existe, fait la bonne taille, et passera bien chez Facebook.

    ⚠️ Un PNG lourd n'est PAS un problème : `publier_fb.preparer()` repasse en
    JPEG 92 au-delà de 3,5 Mo, et Facebook recompresse de toute façon. Le vrai
    contrôle est donc de faire tourner cet allègement et de vérifier qu'il passe
    sous la limite — pas de crier au loup parce qu'un fichier est gros.
    """
    f = ICI / nom
    if not f.is_file():
        return pb('%s : le visuel « %s » N\'EXISTE PAS' % (ou, nom))
    if f.stat().st_size > publier_fb.LIMITE:
        envoye, tmp = publier_fb.preparer(f)
        ko = envoye.stat().st_size / 1024
        if envoye.stat().st_size > publier_fb.LIMITE:
            pb('%s : « %s » fait encore %d ko après allègement — Facebook refusera'
               % (ou, nom, ko))
        else:
            remarques.append('« %s » est lourd mais l\'allègement automatique le'
                             ' ramène à %d ko' % (nom, ko))
        if tmp:
            tmp.unlink(missing_ok=True)
    with Image.open(f) as im:
        if im.size != (2160, 2700):
            pb('%s : « %s » fait %dx%d au lieu de 2160x2700 (rendu en 2x)'
               % (ou, nom, im.size[0], im.size[1]))


def texte_ok(texte, ou, ferme):
    if not texte or not texte.strip():
        return pb('%s : le texte est VIDE' % ou)
    trous = re.findall(r'\{[a-z_]+\}', texte)
    if trous:
        pb('%s : trou(s) non rempli(s) dans le texte : %s' % (ou, ', '.join(trous)))
    bas = texte.lower()
    for mot, pourquoi in INTERDITS:
        if mot in bas:
            pb('%s : contient « %s » — %s' % (ou, mot, pourquoi))
    if ferme:
        for mot in MOTS_QUI_VENDENT:
            if mot in bas:
                pb('%s : SERVICE FERMÉ et le texte dit « %s »' % (ou, mot))


def creneau(jour, matin, ferme):
    """Déroule un créneau comme le fera le robot, sans rien envoyer."""
    quand = '%s %s %s' % (JOURS[jour.weekday()], jour.isoformat(),
                          'matin' if matin else 'midi')
    if ferme:
        premier = jour.isoformat() == service.FERMETURE.get('depuis')
        if not (premier and not matin):
            return '%-28s rien (fermé, avis déjà annoncé)' % quand
        visuel, texte = programme.avis_de_suspension()
        visuel_ok(visuel, quand)
        texte_ok(texte, quand, ferme)
        return '%-28s AVIS DE FERMETURE — %s' % (quand, visuel)

    prevu = calendrier.du_matin(jour) if matin else calendrier.du_jour(jour)
    if prevu is None:
        return '%-28s rien de prévu (normal : le matin sort 2 jours sur 7)' % quand
    visuel, texte, quoi = prevu
    visuel_ok(visuel, quand)
    texte_ok(texte, quand, ferme)
    return '%-28s %-42s %s' % (quand, visuel, quoi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jusqu-au', help='AAAA-MM-JJ (par défaut : dans 7 jours)')
    ap.add_argument('--ouvert', action='store_true',
                    help='simuler le service RÉOUVERT, pour vérifier la reprise')
    a = ap.parse_args()

    if a.ouvert:
        service.OUVERT = True                  # simulation, rien n'est écrit
    ferme = not service.ouvert()

    debut = datetime.date.today()
    fin = (datetime.date.fromisoformat(a.jusqu_au) if a.jusqu_au
           else debut + datetime.timedelta(days=7))

    print('CONTRÔLE du %s au %s — service %s\n'
          % (debut, fin, 'FERMÉ' if ferme else 'OUVERT (simulé)' if a.ouvert
             else 'OUVERT'))

    jour = debut
    while jour <= fin:
        print(' ', creneau(jour, True, ferme))
        print(' ', creneau(jour, False, ferme))
        jour += datetime.timedelta(days=1)

    # --- le bulletin du soir : il part TOUS les soirs, ouvert ou fermé -------
    print('\nLe bulletin du soir (tous les soirs, fabriqué le jour même) :')
    titre, adr, wa = service.cta_bulletin()
    print('  bandeau d\'or      :', titre, '·', adr, '·', wa)
    print('  conseil de mer    :', service.conseil_bulletin(
        'Ça bouge : prévoyez, et suivez les consignes du commandant.'))
    if ferme:
        if 'réserve' in titre.lower():
            pb('bulletin du soir : le bandeau dit encore « réserve » alors que'
               ' le service est fermé')
        if 'commandant' in service.conseil_bulletin('x suivez les consignes du commandant'):
            pb('bulletin du soir : le conseil suppose encore un départ')
    gabarit = (ICI / 'flyer8-soir-fb.template.html').read_text()
    fait = (ICI / 'flyer8-soir-fb.html').read_text()
    manquants = set(re.findall(r'\{\{([A-Z_]+)\}\}', gabarit))
    restants = set(re.findall(r'\{\{([A-Z_]+)\}\}', fait))
    if restants:
        pb('bulletin du soir : %d valeur(s) non remplacée(s) dans le fichier'
           ' fabriqué : %s' % (len(restants), ', '.join(sorted(restants))))
    else:
        remarques.append('les %d valeurs du gabarit du soir sont toutes remplies'
                         % len(manquants))

    # --- la bibliothèque de la page du patron -------------------------------
    print('\nLa bibliothèque (%d visuels sur la page du patron) :' % len(page.FLYERS))
    for f in page.FLYERS:
        visuel_ok(f['png'], 'bibliothèque')
        # les textes à trous sont normaux ICI (remplis à la publication) :
        # on vérifie seulement qu'ils ne sont pas vides et n'ont pas d'interdit
        if not f['texte'].strip():
            pb('bibliothèque : « %s » n\'a pas de texte' % f['png'])
        bas = f['texte'].lower()
        for mot, pourquoi in INTERDITS:
            if mot in bas:
                pb('bibliothèque : « %s » contient « %s » — %s'
                   % (f['png'], mot, pourquoi))
    print('  tous les fichiers et tous les textes ont été examinés.')

    print()
    for r in remarques:
        print('·', r)
    if ennuis:
        print('\n⛔ %d PROBLÈME(S) :' % len(ennuis))
        for e in ennuis:
            print('  ⛔', e)
        sys.exit(1)
    if ferme:
        print('\n✅ RIEN À SIGNALER. Aucun message commercial ne peut partir tant'
              ' que\n   service.py dit fermé, et tous les visuels prévus existent.')
    else:
        print('\n✅ RIEN À SIGNALER. Chaque jour a son visuel, chaque visuel existe'
              '\n   au bon format, et aucun texte ne contient de trou ni d\'interdit.')


if __name__ == '__main__':
    main()
