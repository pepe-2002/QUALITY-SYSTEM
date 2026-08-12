#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'ÉTAT DU SERVICE — la seule source de vérité sur « est-ce qu'on vend ? »

    python3 service.py          # dit l'état du jour et ce que ça change

Le patron, 12/08/2026 : « les traversées sont fermées jusqu'à nouvel ordre,
ouverture possible mardi », « à cause de la mer agitée ».

🚨 POURQUOI CE FICHIER EXISTE, ET POURQUOI IL PASSE AVANT TOUT LE RESTE :
pendant une fermeture, chaque publication qui dit « réserve ta place » est une
promesse qu'on ne peut pas tenir. Quelqu'un descend au port, il n'y a pas de
vedette, et on a perdu ce client pour de bon. Dans un pays où tout le monde se
connaît, ça coûte plus cher que six mois de publicité (manuel § 11 et § 14.2).

Donc : `programme.py` et `bulletin.py` consultent CE fichier avant de publier.
Fermé → aucun message commercial ne part. Rien d'autre à penser, rien à
désactiver à la main, aucun interrupteur à oublier.

⚠️ CE QU'ON N'ÉCRIT JAMAIS : « les traversées reprennent mardi ». Le patron a dit
« ouverture POSSIBLE mardi ». Une date annoncée puis non tenue fait plus de mal
que pas de date du tout. On écrit « peut-être mardi », et on renvoie vers le
WhatsApp pour la réponse du jour.

📌 QUAND ÇA ROUVRE : remettre `OUVERT = True` et vider `FERMETURE`, puis
committer et pousser sur `main`. Une seule ligne à changer.
"""

import argparse
import datetime

# --- l'état du service ------------------------------------------------------
OUVERT = False

FERMETURE = dict(
    depuis='2026-08-12',
    # Ce que le patron a dit, mot pour mot, sans l'arrondir :
    annonce="fermées jusqu'à nouvel ordre, ouverture possible mardi",
    # La date n'est PAS une promesse : elle sert seulement à savoir quand
    # revérifier auprès du patron. Elle ne s'affiche jamais comme une garantie.
    reouverture_possible='2026-08-18',
    # Le patron, 12/08/2026 : « à cause de la mer agitée. » On le dit : une
    # fermeture expliquée rassure (« ils savent ce qu'ils font »), une fermeture
    # muette inquiète (« ils ont un problème »). Et c'est vérifiable par
    # n'importe qui depuis la plage — donc c'est un bon argument.
    raison='mer agitée',
)

# Le visuel de l'avis public, et son texte, vivent avec les autres (page.py).
# Ici on ne garde que l'ÉTAT : un seul endroit à changer quand ça rouvre.
VISUEL_AVIS = 'flyer-suspension-facebook.png'


def ouvert(jour=None):
    """True si on peut vendre une traversée ce jour-là."""
    if OUVERT:
        return True
    return False


def conseil_bulletin(conseil_normal):
    """La phrase sous le verdict de mer, dans le bulletin du soir.

    Les conseils de l'échelle de Douglas (« suivez les consignes du commandant »,
    « vérifiez le maintien des départs ») supposent tous qu'une vedette part.
    Pendant une fermeture, ils font croire à un départ : on les remplace.
    """
    if ouvert():
        return conseil_normal
    return 'Service suspendu : aucun départ prévu. On publie la mer quand même.'


def cta_bulletin():
    """Les trois lignes du bandeau d'or du bulletin du soir.

    Le bulletin continue de partir pendant la fermeture — informer n'est pas
    vendre, et c'est justement les jours sans traversée qu'un bulletin gratuit
    se remarque. Mais son appel « RÉSERVE POUR DEMAIN » deviendrait un mensonge :
    il est remplacé ici, dans le même fichier que l'état, pour qu'on ne puisse
    pas oublier l'un en changeant l'autre.
    """
    if ouvert():
        return ('RÉSERVE POUR DEMAIN', 'moheligo.com',
                'MVola ou KartaPay · WhatsApp +269 479 43 28')
    return ('TRAVERSÉES SUSPENDUES', 'moheligo.com',
            'La mer chaque soir sur cette page · WhatsApp +269 479 43 28')


def etat(jour=None):
    """(ouvert, description courte) — pour les journaux et les rapports."""
    jour = jour or datetime.date.today()
    if ouvert(jour):
        return True, 'service ouvert'
    d = FERMETURE
    txt = 'SERVICE SUSPENDU depuis le %s — %s' % (d['depuis'], d['annonce'])
    if d.get('raison'):
        txt += ' (%s)' % d['raison']
    if d.get('reouverture_possible'):
        txt += ' (à revérifier le %s)' % d['reouverture_possible']
    return False, txt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jour', help='AAAA-MM-JJ')
    a = ap.parse_args()
    jour = datetime.date.fromisoformat(a.jour) if a.jour else datetime.date.today()
    ok, txt = etat(jour)
    print(txt)
    print()
    if ok:
        print('→ publications commerciales AUTORISÉES.')
    else:
        print('→ AUCUN message commercial ne part.')
        print('→ à la place : l\'avis de service suspendu (une fois par jour).')
        print('→ le bulletin mer continue : informer n\'est pas vendre,')
        print('   mais son appel « réserve » est remplacé par l\'avis.')


if __name__ == '__main__':
    main()
