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

📌 CE QUI PART PENDANT LA FERMETURE — révisé le 13/08/2026 sur décision du
patron (« les pubs continuent même si c'est fermé jusqu'à mardi ») :
  · **midi** publie la publication normale de la semaine, **plus la mention de
    fermeture** ajoutée automatiquement (`avec_mention`) : on peut réserver pour
    les jours à venir, on ne descend pas au port avant l'annonce de la reprise ;
  · **le soir**, le bulletin continue, et son bandeau reste « TRAVERSÉES
    SUSPENDUES » — lui parle de la mer de DEMAIN, donc « réserve pour demain »
    y serait faux, mention ou pas ;
  · **le matin** reste muet : la démonstration explique comment réserver un
    départ, geste qui n'aboutit pas aujourd'hui.
  · `texte_du_point()` reste écrit et utilisable (`programme.py --point`) : il
    resservira à la prochaine fermeture si on décide de couper les pubs.

📌 QUAND ÇA ROUVRE, TROIS GESTES ET DANS CET ORDRE :
  1. le patron publie **à la main** le visuel de reprise
     (`flyer-reprise-facebook.png`, son texte est dans `page.py`). À la main, et
     pas par le robot : une reprise ne se décide pas à 12h07, elle se décide
     quand la vedette part vraiment. Le patron, 12/08/2026 : « ne le donne pas
     au robot, donne-le-moi, je le publierai. »
  2. remettre `OUVERT = True` ici, committer, pousser sur `main` — et la semaine
     normale repart toute seule dès le lendemain midi.
  3. 🎬 **PUIS LA VIDÉO YOUNG LEADER** : case `video_young_leader` du workflow.
     Décision du patron du 26/08/2026 : « on la garde pour le jour de la
     réouverture, comme ça ça fait le boom. » Son texte
     (`pub/video/texte-publication.txt`) est DÉJÀ écrit pour ce jour-là — il
     commence par « LES TRAVERSÉES REPRENNENT ». ⚠️ Elle ne peut pas partir
     avant : `publier_video()` refuse tant que `OUVERT` est False.
Faire le 2 sans le 1, c'est reprendre la vente sans avoir annoncé la reprise :
personne ne sait que c'est reparti.
"""

import argparse
import datetime

# --- l'état du service ------------------------------------------------------
# 🔴 REFERMÉ le MERCREDI 26/08/2026. Le patron : « les liaisons maritimes sont
# fermées, la mer est agitée. »
# ⚠️ AUCUNE DATE CETTE FOIS. Le 12/08 il avait dit « ouverture possible mardi » ;
# ici il n'a rien dit de tel, donc on n'écrit NULLE PART une date de reprise,
# et on n'en invente pas une par analogie avec la fermeture précédente.
#
# 🗄️ Précédente fermeture : du 12 au 18/08/2026, six jours, même cause (mer
# agitée). Deuxième épisode en quinze jours — c'est la saison, et c'est
# exactement pourquoi le bulletin du soir vaut plus que n'importe quelle
# publicité : il est le seul endroit où l'on dit la vérité tous les jours.
OUVERT = False

FERMETURE = dict(
    depuis='2026-08-26',
    jusqu_au=None,             # inconnue — et on ne la devine pas
    # Ce que le patron a dit, mot pour mot, sans l'arrondir :
    annonce="les liaisons maritimes sont fermées, la mer est agitée",
    # Pas de date annoncée par le patron → rien à afficher, rien à revérifier
    # à une date précise. On redemande, on n'extrapole pas.
    reouverture_possible=None,
    # Une fermeture expliquée rassure (« ils savent ce qu'ils font »), une
    # fermeture muette inquiète (« ils ont un problème »). Et c'est vérifiable
    # par n'importe qui depuis la plage — donc c'est un bon argument.
    raison='mer agitée',
)

# Le visuel de l'avis public, et son texte, vivent avec les autres (page.py).
# Ici on ne garde que l'ÉTAT : un seul endroit à changer quand ça rouvre.
VISUEL_AVIS = 'flyer-suspension-facebook.png'

# --- DÉCISION DU PATRON, 13/08/2026 -----------------------------------------
# « Les pubs continuent même si c'est fermé jusqu'à mardi. »
#
# J'avais recommandé l'inverse et je l'ai dit clairement ; il a tranché, et c'est
# son entreprise (règle A/B/C, § 12.2 ter : la direction générale décide). Donc
# les pubs repartent.
#
# CE QUI EST VRAI DANS SA DÉCISION, ET QUE J'AVAIS SOUS-ESTIMÉ : on ne vend pas
# une traversée « pour demain », on vend une place sur un départ à venir. Réserver
# aujourd'hui pour la semaine prochaine n'a jamais été un mensonge. Et six jours
# de page commercialement muette coûtent une habitude qu'on met des mois à bâtir.
#
# CE QUE JE NE PEUX PAS LAISSER TOMBER, ET QUI NE COÛTE RIEN : que personne ne
# descende au port pour rien. D'où UNE mention ajoutée à chaque publication
# commerciale tant que le service est fermé. Elle dit la vérité, autorise la
# réservation à l'avance, et ne promet aucune date.
#
# ⚠️ Pour couper les pubs à nouveau : `PUB_PENDANT_FERMETURE = False`.
PUB_PENDANT_FERMETURE = True   # sans effet tant que OUVERT vaut True

MENTION_FERMETURE = """⚠️ EN CE MOMENT, LES DÉPARTS SONT SUSPENDUS (mer agitée).
Tu peux prendre ta place pour les jours qui viennent — elle t'attend, et si la
date ne te va plus, la changer ne coûte rien. Mais ne descends pas au port avant
qu'on annonce la reprise ici : on la publiera dès qu'elle est décidée."""


def avec_mention(texte):
    """Ajoute la mention de fermeture à un texte commercial, avant les mots-dièse.

    Placée AVANT les hashtags et le rappel de source : au-dessus, elle serait lue
    comme une mauvaise nouvelle avant même l'offre ; en toute fin, sous les
    hashtags, personne ne la lit. Juste avant, elle est vue par ceux qui lisent
    jusqu'au bout — ceux qui, justement, s'apprêtaient à réserver.
    """
    if not texte or ouvert():
        return texte
    lignes = texte.rstrip().split('\n')
    for i, l in enumerate(lignes):
        if l.startswith('#'):
            return '\n'.join(lignes[:i] + [MENTION_FERMETURE, ''] + lignes[i:]) + '\n'
    return texte.rstrip() + '\n\n' + MENTION_FERMETURE + '\n'


def jour_de_fermeture(jour=None):
    """Le nombre de jours de fermeture, 1 le premier jour."""
    jour = jour or datetime.date.today()
    debut = datetime.date.fromisoformat(FERMETURE['depuis'])
    return (jour - debut).days + 1


def texte_du_point(jour=None, etat=None, houle=None):
    """Le texte du POINT DE MIDI pendant une fermeture.

    🚨 POURQUOI IL EXISTE (13/08/2026). Le patron : « le flyer de 12 n'est pas
    parti. » Il n'était pas parti parce que le service est fermé — le garde-fou
    a fonctionné. Mais se taire six jours d'affilée est une erreur en soi : la
    page perd l'habitude qu'elle est en train de construire, et les gens qui ne
    voient rien concluent tout seuls (« ils ont coulé »). Or il y a une chose
    vraie à dire chaque jour, qui ne vend rien : **où en est la mer, et où en est
    le service.**

    C'est du même bois que notre seul avantage : on informe même quand on ne
    gagne rien. Un opérateur de transport qui donne un état quotidien pendant une
    interruption est cru la fois suivante.

    ⚠️ Il ne remplace pas le bulletin du soir et ne le répète pas : le bulletin
    parle de la mer de DEMAIN, ce point parle du service D'AUJOURD'HUI.
    ⚠️ Zéro appel commercial : pas de « réserve », pas de prix.
    ⚠️ Aucune date de reprise annoncée.
    """
    n = jour_de_fermeture(jour)
    mer = ''
    if etat and houle is not None:
        mer = ('Ce matin entre nos ports : %s — houle de %s m.\n\n'
               % (etat.lower(), ('%.1f' % houle).replace('.', ',')))
    return """OÙ EN EST LE SERVICE — JOUR %d.

%sLe service est toujours suspendu : aucun départ aujourd'hui.

NE DESCENDS PAS AU PORT POUR RIEN.
Tant que cet avis est en ligne, il n'y a pas de vedette. Le jour où ça repart, tu
le liras ici — avant de partir de chez toi.

SI TU AS UN BILLET, TU NE PERDS RIEN.
Il reste valable. Changer la date est gratuit, et le remboursement est possible
tant que la traversée n'est pas partie. Écris-nous, on s'en occupe.

Et ce soir, comme chaque soir, la mer de demain sur cette page. C'est comme ça
que tu verras le calme revenir, en même temps que nous.

moheligo.com — WhatsApp +269 479 43 28

Prévision Open-Meteo Marine. Nous ne décidons pas des départs : nous publions la
mer et l'état du service.

#MoheliGo #Comores #Mohéli #AvisAuxVoyageurs #MétéoMer""" % (n, mer)


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


def commentaire_bulletin():
    """Le PREMIER COMMENTAIRE du bulletin du soir.

    🚨 AJOUTÉ LE 26/08/2026, deuxième jour de fermeture de l'été. Le texte du
    bulletin disait correctement « on ne prend pas de réservation pour demain »
    — et le premier commentaire, lui, était écrit en dur : « Ta traversée de
    demain : moheligo.com ». Le même envoi se contredisait à deux lignes
    d'écart, et la contradiction tombait sur la seule phrase qu'on ne doit
    jamais dire pendant une fermeture.

    Il vit ici, avec l'état du service, pour la même raison que `cta_bulletin` :
    **on ne peut pas changer l'un en oubliant l'autre.** Tout ce qui promet une
    traversée doit être dans ce fichier, jamais écrit en dur ailleurs.
    """
    if ouvert():
        return ('Ta traversée de demain : moheligo.com\n'
                'WhatsApp : +269 479 43 28')
    return ('Les départs sont suspendus : la mer, chaque soir, ici — et la '
            'reprise dès qu\'elle est décidée.\n'
            'Un billet déjà pris ? Changement de date gratuit.\n'
            'moheligo.com — WhatsApp : +269 479 43 28')


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
    elif PUB_PENDANT_FERMETURE:
        # ⚠️ Ce diagnostic DOIT suivre PUB_PENDANT_FERMETURE. Il a déjà menti une
        # fois (il annonçait le silence pendant que les pubs partaient) : un
        # indicateur faux est pire que pas d'indicateur, on prend des décisions
        # dessus. Décision du patron, 13/08/2026 : « les pubs continuent. »
        print('→ les publications de midi CONTINUENT (décision du patron du 13/08),')
        print('   avec la mention de fermeture ajoutée automatiquement.')
        print('→ le bulletin du soir continue, bandeau « TRAVERSÉES SUSPENDUES ».')
        print('→ le matin reste muet : la démonstration explique un geste')
        print('   qui n\'aboutit pas aujourd\'hui.')
        print('→ l\'avis de suspension se publie à la main : case « avis_de_suspension ».')
    else:
        print('→ AUCUN message commercial ne part.')
        print('→ à la place : l\'avis de service suspendu (une fois par jour).')
        print('→ le bulletin mer continue : informer n\'est pas vendre,')
        print('   mais son appel « réserve » est remplacé par l\'avis.')


if __name__ == '__main__':
    main()
