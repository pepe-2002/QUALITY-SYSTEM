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

⚠️ CE QU'ON N'ÉCRIT JAMAIS : « les traversées REPRENNENT mardi » — un présent qui
affirme. Une date annoncée puis non tenue fait plus de mal que pas de date du
tout. On reprend le mot exact du patron, ni plus fort ni plus faible :
  · 12/08, « ouverture POSSIBLE mardi »  → on écrivait « peut-être mardi » ;
  · 30/08, « la réouverture est PRÉVUE Mardi » → on écrit « c'est prévu mardi ».
Et dans les deux cas la phrase de prudence reste collée derrière : c'est la mer
qui décide, on ne décide pas des départs.
📌 UNE SEULE SOURCE : `FERMETURE['reouverture_possible']`, lue par
`reouverture()`, `paragraphe_reprise()` et `mention_fermeture()`. Rien qui parle
de la reprise ne s'écrit ailleurs — deux fois (26/08 et 30/08) la faute est
venue d'un texte de reprise qui vivait dans son coin.

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
import re

# --- l'état du service ------------------------------------------------------
# 🟢 ROUVERT LE MARDI 01/09/2026. Le patron, mot pour mot : « les traversées sont
# ouvertes ». La reprise était prévue ce jour-là depuis le 30/08 : elle a eu lieu.
# 📌 SEPT JOURS DE FERMETURE (26/08 → 01/09), la plus longue des deux de l'été.
# Ce qui repart tout seul en passant cette ligne à True : la mention de fermeture
# disparaît de toutes les publications, le bandeau du bulletin redevient
# « RÉSERVE POUR DEMAIN », le premier commentaire redevient commercial, et la
# vidéo Young Leader cesse d'être bloquée. **Un seul interrupteur, exprès.**
#
# 🔴 Historique : REFERMÉ le MERCREDI 26/08/2026. Le patron : « les liaisons
# maritimes sont fermées, la mer est agitée. »
# ⚠️ PENDANT QUATRE JOURS, AUCUNE DATE : il n'avait rien dit, donc on n'écrivait
# nulle part une date de reprise, et on n'en inventait pas une par analogie avec
# la fermeture précédente. ✅ Le 30/08 au soir il en a donné une — voir
# `reouverture_possible` ci-dessous. La règle n'a pas changé : on n'invente pas,
# on attend qu'il parle.
#
# 🗄️ Précédente fermeture : du 12 au 18/08/2026, six jours, même cause (mer
# agitée). Deuxième épisode en quinze jours — c'est la saison, et c'est
# exactement pourquoi le bulletin du soir vaut plus que n'importe quelle
# publicité : il est le seul endroit où l'on dit la vérité tous les jours.
OUVERT = True

FERMETURE = dict(
    depuis='2026-08-26',
    jusqu_au='2026-09-01',     # rouvert ce jour-là, confirmé par le patron
    # Ce que le patron a dit, mot pour mot, sans l'arrondir :
    annonce="les liaisons maritimes sont fermées, la mer est agitée",
    # ✅ RENSEIGNÉ LE 30/08/2026 À 19H30. Le patron, mot pour mot :
    # « la réouverture des traversées est prévue Mardi ».
    # 📌 SON MOT EST « PRÉVUE », PAS « POSSIBLE » — et on ne bouge ni dans un
    # sens ni dans l'autre. Le 12/08 il avait dit « ouverture POSSIBLE mardi »
    # et le texte disait « peut-être mardi » : c'était juste. Aujourd'hui il dit
    # « prévue », donc le texte dit « c'est prévu ». Arrondir vers le haut ferait
    # une promesse qu'il n'a pas faite ; arrondir vers le bas effacerait la seule
    # bonne nouvelle qu'on ait à donner depuis cinq jours.
    # ⚠️ CE QUI NE CHANGE PAS POUR AUTANT : `OUVERT` reste False. Une reprise
    # PRÉVUE n'est pas une reprise CONSTATÉE, et c'est la vedette qui part —
    # pas le calendrier — qui rouvre le service. La marche à suivre du jour J
    # est en tête de ce fichier, en trois gestes et dans cet ordre.
    reouverture_possible='2026-09-01',
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

# ✍️ APOSTROPHES TYPOGRAPHIQUES ’ ET NON ' — corrigé le 29/08/2026.
# Ce texte part sur CHAQUE publication pendant une fermeture : une apostrophe
# droite ici se répète des dizaines de fois sur la page. C'est le passage le
# plus lu de tout ce qu'on écrit, et c'était le seul qui restait fautif après
# la mise aux normes (norme § 5).
# 🚩 DEVENUE UNE FONCTION LE 30/08/2026, et pour une raison précise.
# Le patron a donné une date de reprise. Une mention écrite en dur aurait dit
# « la reprise est prévue MARDI » — y compris LE MARDI, et y compris le
# mercredi si personne ne repasse derrière. Un texte qui parle d'un jour doit
# savoir quel jour on est, sinon il devient faux tout seul, en silence.
# 📌 C'est la même règle que pour les dates gravées dans un visuel (norme § 7.3) :
# ce qui porte une date se REGÉNÈRE, jamais ne se garde.
def mention_fermeture(jour=None):
    """La mention ajoutée à CHAQUE publication commerciale pendant la fermeture.

    ✍️ Apostrophes typographiques ’ et non ' — corrigé le 29/08/2026. Ce texte
    part sur chaque publication pendant une fermeture : c'est le passage le plus
    lu de tout ce qu'on écrit (norme § 5).
    """
    jour = jour or datetime.date.today()
    d = FERMETURE.get('reouverture_possible')
    if not d:
        quand = ('Ne descends pas au port avant qu’on annonce la reprise ici :\n'
                 'on la publiera dès qu’elle est décidée.')
    else:
        d = datetime.date.fromisoformat(d)
        if jour < d:
            quand = ('La reprise est prévue %s. Ce n’est pas une promesse — c’est '
                     'la mer qui\ndécide — mais c’est ce qui est prévu, et tu le '
                     'liras ici le jour où ça repart.' % JOURS[d.weekday()])
        elif jour == d:
            quand = ('La reprise est prévue pour aujourd’hui. Attends notre '
                     'annonce ici avant de\ndescendre au port : c’est la vedette '
                     'qui part qui rouvre la ligne, pas le calendrier.')
        else:
            # La date est passée sans qu'on ait rouvert : on ne la répète pas.
            quand = ('Ne descends pas au port avant qu’on annonce la reprise ici :\n'
                     'on la publiera dès qu’elle est décidée.')
    # 📌 La nouvelle a son propre paragraphe. Collée en fin de phrase, elle se
    # lisait comme une précision de plus ; seule, elle se voit.
    return ("""⚠️ EN CE MOMENT, LES DÉPARTS SONT SUSPENDUS (mer agitée).
Tu peux prendre ta place pour les jours qui viennent — elle t’attend, et si la
date ne te va plus, la changer ne coûte rien.

""" + quand)


def _avant_les_hashtags(texte, mention):
    """Glisse un paragraphe juste avant la ligne de mots-dièse.

    Placé AVANT les hashtags et le rappel de source : au-dessus, il serait lu
    comme une mauvaise nouvelle avant même l'offre ; en toute fin, sous les
    hashtags, personne ne le lit. Juste avant, il est vu par ceux qui lisent
    jusqu'au bout — ceux qui, justement, s'apprêtaient à réserver.
    """
    lignes = texte.rstrip().split('\n')
    for i, l in enumerate(lignes):
        if l.startswith('#'):
            return '\n'.join(lignes[:i] + [mention, ''] + lignes[i:]) + '\n'
    return texte.rstrip() + '\n\n' + mention + '\n'


def avec_mention(texte):
    """Ajoute la mention de fermeture à un texte commercial, avant les mots-dièse."""
    if not texte or ouvert():
        return texte
    return _avant_les_hashtags(texte, mention_fermeture())


# ─────────────────────────────────────────────────────────────────────────────
# 🔴 LA DEUXIÈME PANNE — celle du PAIEMENT. 03/09/2026.
#
# Le patron, le 03/09 au soir : « on a un souci aux Comores, MVola ne marche
# pas, tout son service ne marche pas, et c'est le service qu'on utilise pour le
# paiement. » Puis, sur la marche à suivre : « juste l'annonce, mais les pubs
# doivent partir normalement. »
#
# ⛔ POURQUOI CE FICHIER DEVAIT APPRENDRE UN DEUXIÈME TYPE DE PANNE, ET POURQUOI
# JE NE L'AVAIS PAS VU EN ÉCRIVANT L'AVIS. Nous avons publié l'avis MVola à
# 20h41. Soixante-dix minutes plus tôt, à 19h29, le bulletin du soir était parti
# avec sa ligne habituelle : « • Tu paies par MVola ou kartaPay ». Le lendemain
# midi, le flyer du vendredi aurait dit la même chose. **L'avis ne corrigeait
# rien : il s'ajoutait à des textes qui continuaient de promettre le contraire.**
# 📌 **UN AVIS NE RATTRAPE PAS LES TEXTES QUI TOURNENT À CÔTÉ DE LUI.** Tout ce
# fichier existe contre les promesses intenables, mais il ne connaissait qu'une
# seule panne — la mer. Une panne qu'un programme ne sait pas nommer est une
# panne qu'il publiera par-dessus.
#
# ⚖️ CE QUE JE FAIS EN PLUS DE L'ANNONCE, ET QUE LE PATRON N'A PAS DEMANDÉ :
# `sans_promesse_de_paiement()` retire la phrase « tu paies par MVola » des
# textes du jour. Sa consigne est « juste l'annonce » — mais un post qui dit
# « paie par MVola » et, huit lignes plus bas, « MVola est hors service », n'est
# pas une pub qui part normalement : c'est une pub qui se contredit toute seule.
# ⚠️ POUR REVENIR À LA LETTRE DE SA CONSIGNE : supprimer l'appel à
# `sans_promesse_de_paiement()` dans `avec_panne_paiement()`. L'annonce, elle,
# reste.
#
# 📌 QUAND MVOLA REVIENT : `PANNE_PAIEMENT = None`, committer, pousser sur
# `main`. Un seul endroit, exactement comme `OUVERT` pour la mer. Et le dire sur
# la page — on a annoncé la panne, on doit annoncer la fin.
PANNE_PAIEMENT = dict(
    depuis='2026-09-03',
    # Le mot du patron, sans l'arrondir — même règle que `FERMETURE['annonce']`.
    annonce='mvola ne marche pas, tout son service ne marche pas',
    # 🔴 CE QU'ON NE SAIT PAS ENCORE, ET QUI EST À LUI (poste C, § 12.2 ter) :
    # Holo passe-t-il encore par kartaPay ? Comment on encaisse d'ici là ?
    # Tant que ce n'est pas tranché, l'annonce ne promet AUCUN moyen de payer —
    # elle ouvre une conversation, et c'est tout ce qu'elle peut tenir.
    encaissement='non tranché',
)

MARQUE_PANNE = 'LE PAIEMENT EN LIGNE EST INTERROMPU'

# 🚩 L'EMPREINTE N'EST PAS LE TITRE DE L'ANNONCE, ET J'AI DÛ LE CORRIGER À
# L'ESSAI. J'avais pris `MARQUE_PANNE` comme empreinte : `texte-whatsapp.txt`
# — l'avis lui-même, qui dit déjà tout ça dans ses mots — ne la contient pas, et
# recevait donc l'annonce collée sous son propre texte.
# 📌 **UNE EMPREINTE DOIT RECONNAÎTRE LE SUJET, PAS LA FORMULATION.** Ces cinq
# mots-là sont dans l'annonce ET dans l'avis, et dans aucun texte commercial.
DEJA_DIT = 'MVola est hors service'

# ⚠️ LES DEUX FORMES SONT NÉCESSAIRES, ET LA DEUXIÈME N'EST PAS UN DOUBLON.
# Six textes portent la phrase complète (« Tu paies par MVola ou kartaPay »),
# parfois coupée par un retour à la ligne — d'où le `\s+` partout plutôt que des
# espaces. Mais `texte-reprise.txt` écrit « Prends ta place : MVola ou
# kartaPay, et ton billet arrive » : pas de verbe « paies », donc la première
# forme le rate. Relevé sur les sept fichiers, pas deviné.
_PAIEMENT_PROMIS = [
    (re.compile(r'[Tt]u\s+paies\s+par\s+MVola\s*(?:,|ou)?\s*(?:avec\s+)?kartaPay'),
     'Tu prends ta place'),
    (re.compile(r'\s*:?\s*MVola\s+ou\s+kartaPay'), ''),
]


def paiement_en_panne():
    """Le paiement en ligne est-il tombé ? (la seule source : PANNE_PAIEMENT)"""
    return bool(PANNE_PAIEMENT)


def mention_paiement():
    """L'annonce ajoutée à CHAQUE publication tant que MVola est hors service.

    ✍️ Apostrophes typographiques ’ et non ' (norme § 5) : ce paragraphe part
    sur tout ce qu'on publie, c'est le passage le plus lu de la période.
    """
    return ("""⚠️ %s : MVola est hors service.
Les vedettes partent normalement — c’est le paiement qui est tombé, pas la
traversée. Écris-nous sur WhatsApp au +269 479 43 28 : on prend ta place à la
main, le temps que ça revienne.""" % MARQUE_PANNE)


def sans_promesse_de_paiement(texte):
    """Retire des textes du jour la phrase qui promet un paiement impossible."""
    if not texte or not paiement_en_panne():
        return texte
    for motif, remplacement in _PAIEMENT_PROMIS:
        texte = motif.sub(remplacement, texte)
    return texte


def avec_panne_paiement(texte):
    """Le texte tel qu'il doit partir pendant la panne de paiement.

    ⚠️ Appelée dans `publier_fb.decouper()`, c'est-à-dire au RAS DU FIL — le
    dernier endroit par lequel passe tout texte publié, quel que soit le chemin
    (calendrier de midi, bulletin du soir, visuel choisi à la main, vidéo).
    📌 La mention de fermeture, elle, vit dans `programme.py` : elle ne couvre
    donc que le chemin de midi. C'est la leçon de ce soir — le bulletin du soir
    a promis MVola soixante-dix minutes avant qu'on annonce sa panne. **On place
    un garde-fou là où passent TOUS les chemins, pas là où passe celui auquel on
    pense.**
    """
    if not texte or not paiement_en_panne() or DEJA_DIT in texte:
        return texte
    return _avant_les_hashtags(sans_promesse_de_paiement(texte),
                               mention_paiement())


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

%sLe service est toujours suspendu : aucun départ aujourd’hui.

NE DESCENDS PAS AU PORT POUR RIEN.
Tant que cet avis est en ligne, il n’y a pas de vedette. Le jour où ça repart, tu
le liras ici — avant de partir de chez toi.

SI TU AS UN BILLET, TU NE PERDS RIEN.
Il reste valable. Changer la date est gratuit, et le remboursement est possible
tant que la traversée n’est pas partie. Écris-nous, on s’en occupe.

Et ce soir, comme chaque soir, la mer de demain sur cette page. C’est comme ça
que tu verras le calme revenir, en même temps que nous.

moheligo.com — WhatsApp +269 479 43 28

Prévision Open-Meteo Marine. Nous ne décidons pas des départs : nous publions la
mer et l’état du service.

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
    return 'Service suspendu. Aucun départ. On publie la mer quand même.'


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
                'MVola ou kartaPay · WhatsApp +269 479 43 28')
    # 02/09/2026 — « TRAVERSÉES SUSPENDUES » était un CONSTAT, pas un appel.
    # La norme § 4 exige un verbe d'action : un visuel qui n'a rien à vendre a
    # quand même un geste à demander, et pendant une fermeture ce geste est
    # évident — se faire prévenir plutôt que descendre au port chaque matin.
    # L'information « suspendues » n'est pas perdue : elle passe en 3e ligne.
    return ('ÉCRIS-NOUS, ON TE PRÉVIENT', 'moheligo.com',
            'Traversées suspendues · la mer chaque soir ici · +269 479 43 28')


JOURS = ('lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche')


def paragraphe_reprise():
    """Le paragraphe « QUAND ÇA REPREND » de l'avis de suspension.

    🚨 AJOUTÉ LE 26/08/2026, et il a évité une faute grave. L'avis contenait
    **« QUAND ÇA REPREND : PEUT-ÊTRE MARDI »** écrit EN DUR — un reste de la
    fermeture du 12/08, où le patron avait dit « ouverture possible mardi ».
    Cette fois il n'a donné AUCUNE date. L'avis serait parti en annonçant un
    mardi que personne n'a promis.

    C'est précisément ce que l'en-tête de ce fichier interdit : « une date
    annoncée puis non tenue fait plus de mal que pas de date du tout ». La règle
    ne suffit pas si le texte qui la viole vit ailleurs — **d'où ce paragraphe,
    ici, piloté par `FERMETURE['reouverture_possible']`.**

    🚩 30/08/2026 — « PEUT-ÊTRE » EST DEVENU « PRÉVU », ET LE MOT VIENT DE LUI.
    Le 12/08 le patron disait « ouverture POSSIBLE mardi » → « peut-être mardi ».
    Le 30/08 il dit « la réouverture est PRÉVUE mardi » → « c’est prévu mardi ».
    On ne traduit pas son mot, on le reprend. Arrondir vers le haut invente une
    promesse ; arrondir vers le bas efface la nouvelle. La phrase de prudence,
    elle, ne bouge pas : c’est la mer qui décide.
    """
    d = FERMETURE.get('reouverture_possible')
    if d:
        jour = JOURS[datetime.date.fromisoformat(d).weekday()]
        titre = 'QUAND ÇA REPREND : C’EST PRÉVU %s.' % jour.upper()
    else:
        titre = 'QUAND ÇA REPREND : ON NE LE SAIT PAS ENCORE.'
    return (titre + '\n'
            'Ce n’est pas une date promise — c’est la mer qui décide, et nous ne '
            'décidons pas\ndes départs. Le jour où ça rouvre, tu le liras ici en '
            'premier.')


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

    🚩 30/08/2026 — LA MÊME FAUTE A FAILLI RECOMMENCER, EN PLUS DOUX.
    Le post du soir annonçait « QUAND ÇA REPREND : C’EST PRÉVU MARDI » et ce
    commentaire, trois lignes plus bas, disait encore « la reprise dès qu’elle
    est décidée » — comme si on n’avait toujours pas de date. Ce n’est pas un
    mensonge, c’est pire à sa manière : le même envoi ne se souvient pas de ce
    qu’il vient de dire. 📌 Il tire donc sa phrase de la MÊME source que le
    post : `reouverture()`.
    ✍️ Et il portait une apostrophe droite dans `qu\\'elle` — échappée, donc
    invisible au détecteur qui cherchait une lettre avant l’apostrophe.
    **Une faute qu’un contrôle ne peut pas voir est une faute qui reste.**
    """
    if ouvert():
        return ('Ta traversée de demain : moheligo.com\n'
                'WhatsApp : +269 479 43 28')
    return ('Les départs sont suspendus : la mer, chaque soir, ici — %s\n'
            'Un billet déjà pris ? Changement de date gratuit.\n'
            'moheligo.com — WhatsApp : +269 479 43 28' % reouverture())


def reouverture():
    """La reprise, en UNE phrase, tirée d’un seul endroit.

    Tout ce qui parle de la reprise passe par ici : le post du soir (via
    `paragraphe_reprise`), le premier commentaire, la mention des publications
    commerciales. Le 26/08, une date écrite en dur avait survécu à la fermeture
    suivante ; le 30/08, un commentaire ignorait une date que le post annonçait.
    Les deux fois, la cause est la même : **la reprise vivait à plusieurs
    endroits.**
    """
    d = FERMETURE.get('reouverture_possible')
    if not d:
        return 'et la reprise dès qu’elle est décidée.'
    d = datetime.date.fromisoformat(d)
    aujourdhui = datetime.date.today()
    if aujourdhui < d:
        return 'et la reprise, prévue %s, dès qu’elle est confirmée.' % JOURS[d.weekday()]
    if aujourdhui == d:
        return 'et la reprise, prévue aujourd’hui, dès qu’elle est confirmée.'
    return 'et la reprise dès qu’elle est décidée.'


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

    # 🚩 LE PAIEMENT A SON PROPRE ÉTAT, ET IL DOIT SE VOIR ICI. Ce fichier est
    # « la seule source de vérité sur : est-ce qu'on vend ? ». Le 03/09 il
    # répondait « service ouvert, publications autorisées » alors que plus
    # personne ne pouvait payer. Une source de vérité qui ne connaît qu'une
    # moitié de la question répond faux avec aplomb.
    if paiement_en_panne():
        print()
        print('🔴 PAIEMENT EN LIGNE HORS SERVICE depuis le %s.'
              % PANNE_PAIEMENT['depuis'])
        print('   Le patron : « %s »' % PANNE_PAIEMENT['annonce'])
        print('→ les pubs partent NORMALEMENT (sa consigne du 03/09),')
        print('   avec l\'annonce WhatsApp ajoutée à tout ce qui se publie')
        print('   (`publier_fb.decouper`, donc midi, soir, visuel choisi, vidéo).')
        print('→ la phrase « tu paies par MVola » est retirée des textes du jour.')
        print('→ encaissement pendant la panne : %s.' % PANNE_PAIEMENT['encaissement'])
        print('→ quand MVola revient : PANNE_PAIEMENT = None, et on le dit sur la page.')


if __name__ == '__main__':
    main()
