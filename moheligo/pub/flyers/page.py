#!/usr/bin/env python3
"""Construit la page web que le patron ouvre pour récupérer ses flyers.

    python3 page.py                    # écrit page-flyers.html
    python3 page.py --sortie /tmp/x.html

Pourquoi ce script existe : les pièces jointes ne s'affichent pas chez le
patron. Le seul canal qui marche est une page web publiée (artifact), toujours
à la même adresse. Elle était retouchée à la main à chaque fois — et une
retouche a fini par effacer deux blocs. Désormais la page est REGÉNÉRÉE
entièrement, jamais rapiécée.

Elle contient : la météo de demain (Open-Meteo, terre + mer), puis chaque flyer
en grand avec son texte de publication et un bouton pour le copier.
Tout est embarqué en base64 : aucune requête réseau à l'ouverture.
"""
import argparse
import base64
import json
import os
import pathlib
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone

from PIL import Image

LAT_MER, LON_MER = -12.08, 43.54        # couloir Ouroveni – Hoani
LAT_TERRE, LON_TERRE = -12.28, 43.74    # Fomboni
# Le proxy de session impose son propre certificat ; sur GitHub ce fichier
# n'existe pas et curl refuse de démarrer (erreur 77). D'où le test d'existence.
CACERT = '/root/.ccr/ca-bundle.crt'
TZ = 'Indian%2FComoro'
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
        'août', 'septembre', 'octobre', 'novembre', 'décembre']
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
CIEL = {0: 'Ciel dégagé', 1: 'Peu nuageux', 2: 'Partiellement nuageux', 3: 'Couvert',
        45: 'Brouillard', 51: 'Pluie fine', 53: 'Pluie fine', 55: 'Pluie fine dense',
        61: 'Pluie faible', 63: 'Pluie modérée', 65: 'Forte pluie',
        80: 'Averses', 81: 'Averses', 82: 'Fortes averses', 95: 'Orage'}

# Les flyers de la page, dans l'ordre d'affichage.
# (fichier PNG, titre, note, fichier texte ou None si le texte est ici)
FLYERS = [
    dict(png='flyer-affiche-vraie-facebook.png', titre="L'affiche MOHÉLI",
         note='Sans date<br>publiable quand vous voulez', texte="""MOHÉLI, À UNE TRAVERSÉE.

Les îlots de Nioumachoua, vus de la plage, un matin sans vent.

Pour y être, il suffit de traverser. Et la traversée se réserve depuis votre
téléphone, en deux minutes :

• Ouroveni ou Chindini au départ, Hoani ou Fomboni à l'arrivée.
• Paiement MVola ou KartaPay, billet QR immédiat.
• L'état de la mer sur 7 jours, consulté avant de partir.

moheligo.com

Photo : Fatima771 (CC BY 3.0, Wikimedia Commons)

#MoheliGo #Mohéli #Nioumachoua #Comores #VisitComoros #Traversée"""),
    dict(png='flyer-abonner-facebook.png', titre='⭐ JEUDI — S\'ABONNER',
         note="Sans date · publie le jeudi<br>la seule demande de la semaine<br>qui n'est pas « réserve »<br>l'objet : les sept soirs",
         texte="""CHAQUE SOIR, LA MER DE DEMAIN. SUR CETTE PAGE, À 19H30.

Gratuitement, et sans rien demander en échange.

CE QUE TU REÇOIS, SEPT SOIRS SUR SEPT :
• L'état de la mer — belle, peu agitée, agitée, forte : le mot et le chiffre.
• La houle du matin, en mètres, entre 5h et 13h.
• Le vent : sa force et sa direction, pour la fenêtre du matin.

Appuie une fois sur « S'abonner ». Tu sauras chaque soir, avant de quitter la
maison. Rien à payer, rien à installer, rien à donner — et tu peux te
désabonner quand tu veux.

Personne d'autre ne publie ça. Nous le faisons parce que partir sans savoir,
c'est se lever à 4 heures pour rien.

Prévision Open-Meteo Marine. Le bulletin officiel affiché à l'embarquement
fait foi.

#MoheliGo #Comores #Mohéli #MétéoMer #Traversée"""),
    dict(png='flyer-diaspora-v2-facebook.png', titre='⭐ VENDREDI — LA DIASPORA',
         note="Sans date · publie le vendredi<br>jour de paie en Europe<br>l'angle le plus fort du manuel<br>l'objet : les deux côtés de la mer",
         texte="""TU PAIES D'ICI. ELLE EMBARQUE LÀ-BAS.

Tu es à Marseille, à Mayotte, à Dubaï. Elle n'a rien à avancer, ni à comprendre.

TOI, DE L'AUTRE CÔTÉ :
• Tu choisis le départ et la date sur moheligo.com.
• Tu paies avec MVola ou KartaPay, depuis là où tu es.
• Tu mets SON nom et SON numéro à elle, pas le tien.

ELLE, AUX COMORES :
• Le billet arrive dans son téléphone, avec son code.
• Il y reste même sans réseau : c'est lui qu'on scanne à l'embarquement.
• Elle n'avance rien, et n'a rien à installer.

Un rendez-vous chez le médecin, un enterrement, une rentrée scolaire : elle n'a
plus à trouver l'argent le matin même.

Réserve pour elle : moheligo.com
Une question avant de payer ? WhatsApp +269 479 43 28

#MoheliGo #Comores #Mohéli #Diaspora #MVola"""),
    dict(png='flyer-destination-facebook.png', titre='⭐ SAMEDI — LA DESTINATION',
         note="Sans date · publie le samedi<br>photo tenue dans la carte claire<br>crédit imprimé sur le visuel<br>CC BY 3.0 — ne jamais l'enlever",
         texte="""MOHÉLI, À UNE TRAVERSÉE.

Les îlots de Nioumachoua, un matin sans vent. Pour y être, il suffit de traverser.

• Quatre ports : Ouroveni et Chindini au départ, Hoani et Fomboni à l'arrivée.
• La mer sur 7 jours, publiée chaque soir sur cette page — avant que tu descendes.
• Ta place prise d'avance, depuis le téléphone, sans aller la chercher au port.

Scanne le code ou va sur moheligo.com
Paiement MVola ou KartaPay · WhatsApp +269 479 43 28

Photo : Fatima771 — îlots de Nioumachoua, Mohéli (CC BY 3.0, Wikimedia Commons).

#MoheliGo #Mohéli #Nioumachoua #Comores #VisitComoros #Traversée"""),
    dict(png='flyer-institutionnel-facebook.png', titre='⭐ DIMANCHE — INSTITUTIONNEL',
         note="Sans date · publie le dimanche<br>registre partenaires, VOUVOIEMENT<br>aucun horaire annoncé (non vérifié)<br>l'objet : le tableau des liaisons",
         texte="""QUATRE PORTS. UNE LIAISON QUI SE PRÉPARE.

Entre deux îles, il y a une mer. Et, depuis peu, un service qu'on peut consulter,
réserver et payer à l'avance.

Ouroveni (Grande Comore) → Hoani (Mohéli)
Chindini (Grande Comore) → Fomboni (Mohéli)

• Billetterie en ligne : paiement MVola ou KartaPay, billet à code délivré
  immédiatement.
• État de la mer publié chaque soir pour le lendemain, source citée.
• Assistance : un numéro WhatsApp tenu par une personne, pas un répondeur.

HÔTELIERS, AGENCES, COMMERÇANTS : nous cherchons des points de vente assistés.
Vous réservez pour vos clients qui n'achètent pas en ligne. Écrivez-nous, nous
nous déplaçons.

moheligo.com — WhatsApp +269 479 43 28

Nous ne décidons pas des départs : nous publions la mer et délivrons les billets.

#MoheliGo #Comores #Mohéli #Traversée"""),
    dict(png='flyer-rien-installer-facebook.png', titre='⭐ LUNDI — RIEN À INSTALLER',
         note="Sans date · publie le lundi<br>répond à l'objection « mon<br>téléphone est plein »<br>l'objet : la barre d'adresse",
         texte="""RIEN À INSTALLER. C'EST JUSTE UNE PAGE.

Pas d'application à télécharger, pas de place à faire dans le téléphone. Tu écris
moheligo.com et c'est ouvert — comme n'importe quel site.

• Aucune place prise : rien ne s'installe, rien ne reste dans ton téléphone.
• Ton billet, lui, reste : une fois payé, il est dans le téléphone, même sans
  réseau.
• Rien à donner d'abord : tu regardes les traversées et les prix avant de te
  connecter.

Ta place est bloquée 15 minutes le temps de payer, avec MVola ou KartaPay.

Besoin d'aide ? On est là. Première réservation ? Un proche ou un commerçant peut
t'accompagner.

moheligo.com — WhatsApp +269 479 43 28

#MoheliGo #Comores #Mohéli #Traversée #MVola"""),
    dict(png='flyer-grostemps-facebook.png', titre='⛈️ LES JOURS DE GROSSE MER',
         note="Sans date<br>publié tout seul quand la houle<br>dépasse 2,50 m au matin<br>{etat} et {houle} sont remplacés<br>par les vrais chiffres du jour<br>ZÉRO appel commercial",
         texte="""AUJOURD'HUI, LA MER EST FORTE. ALORS ON NE TE VEND RIEN.

{etat} ce matin entre nos ports : houle de {houle} m.

PAR CETTE MER, LES VEDETTES PEUVENT NE PAS PARTIR.
Nous ne décidons pas des départs — nous publions la mer. Avant de descendre au
port, appelle ou écris : on te dit ce qui est maintenu, et ce qui n'est pas
encore décidé.

SI TU AS DÉJÀ UN BILLET.
Changer la date ne coûte rien, sur la même liaison. Et tant que la traversée
n'est pas partie, tu peux annuler et être remboursé.

CE QUI DÉCIDE, C'EST LA MER ET LE COMMANDANT.
Le bulletin officiel affiché à l'embarquement fait toujours foi.

Chaque soir à 19h30, on publie la mer du lendemain sur cette page. Gratuitement,
qu'elle soit belle ou mauvaise. C'est les jours comme aujourd'hui que ça compte.

moheligo.com — WhatsApp +269 479 43 28

Prévision Open-Meteo Marine.

#MoheliGo #Comores #Mohéli #MétéoMer #Sécurité"""),
    dict(png='flyer-modedemploi-v2-facebook.png', titre="⭐ MODE D'EMPLOI — V2",
         note="Sans date · celui qui publie<br>QR vérifié vers moheligo.com<br>lisible en 3 secondes :<br>promesse, 1-2-3, QR, adresse<br>les six corrections du patron",
         texte="""EN TROIS GESTES, TA PLACE EST RÉSERVÉE.

Depuis ton téléphone, sans passer au port pour chercher une place.

1. TU CHOISIS
Départ, arrivée, date. Tu vois les horaires et les prix sans rien donner.

2. TU RÉSERVES
Ton nom et ton numéro. Ça prend 30 secondes.

3. TU PAIES, TU EMBARQUES
MVola ou KartaPay, depuis ton téléphone. Ton billet arrive avec son code, et il
reste dans le téléphone même sans réseau.

Besoin d'aide ? On est là. Première réservation ? Un proche ou un commerçant
peut t'accompagner — la deuxième fois, tu le feras seul.

Scanne le code ou va sur moheligo.com
WhatsApp +269 479 43 28 — quelqu'un répond.

#MoheliGo #Comores #Mohéli #Traversée #MVola"""),
    dict(png='flyer-modedemploi-facebook.png', titre="Mode d'emploi — V1 (test terrain)",
         note="Sans date · gardée pour l'impression<br>notée 8,7/10 par le patron<br>remplacée par la V2 pour publier<br>textes plus longs, pas de QR",
         texte="""EN TROIS GESTES, TA PLACE EST PRISE.

Si tu n'as jamais réservé sur un site, lis ça une fois. Après, tu sauras.

1. TU CHOISIS.
Départ, arrivée, date — Ouroveni, Chindini, Hoani, Fomboni. Tu vois les
traversées, les places et les prix sans rien donner. Ni nom, ni numéro.

2. TU RÉSERVES.
C'est seulement ici qu'on te demande ton nom et ton numéro : trente secondes.
Ta place est bloquée quinze minutes, le temps de payer tranquillement.
Personne ne te la prend pendant ce temps-là.

3. TU PAIES, TU EMBARQUES.
MVola ou KartaPay, depuis ton téléphone — ce que tu utilises déjà. Ton billet
arrive avec son code, et il reste dans le téléphone même sans réseau. C'est lui
que le commandant scanne.

Rien à installer : ça s'ouvre comme une page.

Et la première fois, tu n'es pas obligé de le faire seul. Demande à un proche,
à un boutiquier, à ton hôtelier. Il n'y a aucune honte à ça — la deuxième fois,
tu le feras seul en trois minutes.

moheligo.com — une question avant de commencer ? WhatsApp +269 479 43 28,
quelqu'un répond, et peut le faire avec toi.

#MoheliGo #Comores #Mohéli #Traversée #MVola"""),
    dict(png='flyer-prix-facebook.png', titre='⭐ MERCREDI — LES PRIX',
         note="Sans date<br>publiable tous les mercredis<br>le billet est l'objet qu'on regarde<br>tous les chiffres viennent du site",
         texte="""LE PRIX, TU LE CONNAIS AVANT DE PAYER.

Adulte : environ 14 500 FC pour une personne, un trajet. Enfant : −30 à −50 %.
Le prix exact de chaque départ est écrit dans l'application, en direct, AVANT que
tu paies. Pas de négociation, pas de surprise au port.

Ce qui est déjà compris dans ce prix :

• Ta place est bloquée 15 minutes, le temps de payer tranquillement. Personne ne
  te la prend pendant ce temps-là.
• Changer la date de ton billet ne coûte rien, sur la même liaison.
• Tu annules avant le départ : ton argent revient, moins les frais de transaction.

Tu paies avec MVola ou KartaPay, depuis ton téléphone. Rien de nouveau à
apprendre. Et si quelqu'un de ta famille est à l'étranger, il peut payer pour toi
depuis là-bas : tu reçois ton billet ici, tu n'avances rien.

Regarde le prix de ton départ : moheligo.com
Une question avant de payer ? WhatsApp +269 479 43 28

#MoheliGo #Comores #Mohéli #Traversée #MVola"""),
    dict(png='flyer-signature-facebook.png', titre='⭐ LE MODÈLE DE SIGNATURE',
         note='Les quatre influences réunies<br>le logo Royal Air, la couleur et<br>l\'émotion Coca-Cola, le vide<br>d\'Apple, la brillance de Yas',
         texte="""On se voit de l'autre côté.

MoheliGo — traversées maritimes des Comores.
Ouroveni · Chindini · Hoani · Fomboni

Réservation en deux minutes : moheligo.com"""),
    dict(png='flyer-chiffre-facebook.png', titre='⭐ CARTE BLANCHE — le chiffre',
         note='Mon manuel appliqué à la lettre<br>aplat franc, un fait, zéro décor<br>DATÉ : à regénérer chaque jour',
         texte="""DEMAIN MATIN, LA MER SERA À 0,9 M.

Mer peu agitée entre Ouroveni et Hoani. Traversée normale, un peu de mouvement.
Vent 17 km/h de sud-est, période de houle 9,0 secondes.

Personne d'autre ne publie ce chiffre. Nous le faisons chaque soir, gratuitement,
parce que partir sans savoir, c'est se lever à 4 heures pour rien.

La mer des 7 prochains jours — et votre place — sur moheligo.com

Prévision Open-Meteo Marine. Le bulletin officiel affiché dans l'application
fait foi avant l'embarquement.

#MoheliGo #Comores #Mohéli #MétéoMer #Traversée"""),
    dict(png='flyer-couleur-facebook.png', titre='Le « Coca-Cola »',
         note='Sans date<br>une couleur, une émotion', texte="""On se voit de l'autre côté.

MoheliGo — traversées maritimes des Comores.
moheligo.com"""),
    dict(png='flyer-conglomerat-facebook.png', titre='Le « grand conglomérat »',
         note='Sans date<br>registre Apple / institutionnel', texte="""Entre deux îles, il y a une mer. Et un service.

MoheliGo — traversées maritimes des Comores.
moheligo.com"""),
    dict(png='flyer-aerien-facebook.png', titre='Le flyer « composition »',
         note='Sans date<br>le plus moderne', texte="""TRAVERSEZ VERS MOHÉLI, SEREINEMENT.

Votre place est prise avant même d'arriver au port, et votre billet est déjà
dans votre poche.

1. Vous choisissez votre départ sur moheligo.com
2. Vous payez par MVola ou KartaPay
3. Vous embarquez, billet QR en main

À partir de 15 000 FC la traversée.
Ouroveni et Chindini vers Hoani et Fomboni.

Et avant de partir, l'état de la mer et les places restantes sont sur le site :
on ne prend plus la mer à l'aveugle.

moheligo.com
WhatsApp +269 479 43 28

#MoheliGo #Mohéli #Comores #Traversée #BilletQR"""),
    dict(png='flyer-soir-facebook.png', titre='Le bulletin du soir',
         note='Annonce demain matin<br>bon pour ce soir seulement', texte='@texte-du-jour.txt'),
    dict(png='flyer-diaspora-facebook.png', titre='Pour la diaspora',
         note='Sans date<br>plutôt le week-end', texte="""TU PAIES ICI. IL EMBARQUE.

Tu es en France, à Mayotte ou dans le Golfe, et ta famille doit traverser
vers Mohéli ?

Depuis ton téléphone, sur moheligo.com :

• Tu choisis le port, la date et la place.
• Tu paies par MVola ou KartaPay.
• Ton proche reçoit son billet QR sur son téléphone. Il n'avance rien.

À partir de 15 000 FC la traversée.

moheligo.com — la place est prise avant même que tu raccroches.

#MoheliGo #DiasporaComorienne #Comores #Mohéli #Mayotte"""),
    dict(png='flyer-promo-brillant-facebook.png', titre='Le promo',
         note='Sans date<br>le plus accrocheur', texte="""TA TRAVERSÉE EN 2 MINUTES.

Plus besoin d'aller au port pour savoir s'il y a une place.
Tu ouvres moheligo.com, tu choisis ton départ, tu paies par MVola.
Ton billet QR arrive tout de suite dans ton téléphone.

À partir de 15 000 FC le trajet.
Ouroveni et Chindini vers Hoani et Fomboni.

Réserve maintenant : moheligo.com
Une question ? WhatsApp +269 479 43 28

#MoheliGo #Mohéli #Comores #Traversée"""),
]


# Textes sans image : à copier tels quels dans une publication Facebook.
TEXTES = [
    dict(titre="Faire s'abonner — version manuel", texte="CHAQUE SOIR, LA MER DE DEMAIN. GRATUITEMENT.\n\nCe soir, sur cette page : houle 0,9 m, vent 17 km/h de sud-est, mer peu agitée\ndemain matin entre Ouroveni et Hoani.\n\nDemain soir, les chiffres du jour suivant. Et le soir d'après aussi.\n\nPersonne d'autre ne le publie. Nous le faisons parce que traverser sans savoir,\nc'est se lever à 4 heures pour rien — et ça, ça suffit.\n\nTu n'as rien à payer, rien à installer, rien à donner.\nAppuie sur « S'abonner », et tu sauras avant de quitter la maison.\n\nMoheliGo — moheligo.com\n\n#MoheliGo #Comores #Mohéli #MétéoMer #Traversée"),
    dict(titre='Faire créer un compte — version manuel', texte="LA PREMIÈRE FOIS PREND TROIS MINUTES. LES SUIVANTES, TRENTE SECONDES.\n\nQuand tu crées ton compte sur moheligo.com :\n\n• Tes billets restent dedans. Tu les retrouves même sans connexion.\n• Ton nom et ton numéro sont déjà remplis la fois d'après.\n• Tu vois l'historique de tes traversées, et celles de ta famille si tu paies\n  pour elle.\n\nC'est tout. Pas de carte à donner, pas d'abonnement, pas de frais.\n\nUn compte, c'est une place prise en trente secondes le jour où tu es pressé.\n\nmoheligo.com — crée ton compte maintenant, tu remercieras ton téléphone\nla prochaine fois.\n\n#MoheliGo #Comores #Mohéli #BilletQR"),
    dict(titre="⭐ Convaincre celui qui n'a jamais acheté en ligne", texte="« ET SI JE PAIE ET QU'IL N'Y A PAS DE PLACE ? »\n\nC'est la question qu'on nous pose le plus. Voici les réponses, sans détour.\n\nTU PAIES AVEC CE QUE TU CONNAIS DÉJÀ.\nMVola ou KartaPay, depuis ton téléphone. Pas de carte bancaire, rien de\nnouveau à apprendre.\n\nTU REÇOIS UN BILLET, PAS UNE PROMESSE.\nDès le paiement, un billet avec un code QR arrive dans ton téléphone. Il y\nreste, même sans réseau. C'est lui que le commandant scanne à l'embarquement.\n\nQUELQU'UN RÉPOND, TOUJOURS.\nWhatsApp +269 479 43 28. Un vrai numéro, une vraie personne. Avant, pendant,\naprès.\n\nTU PEUX LE FAIRE ACCOMPAGNÉ.\nLa première fois, demande à un boutiquier, à un hôtelier, ou à un proche à\nl'étranger de le faire avec toi. Il n'y a aucune honte à ça : la deuxième fois,\ntu le feras seul en trois minutes.\n\nET SI QUELQU'UN PAIE POUR TOI.\nTon frère à Marseille, ta sœur à Mayotte : ils réservent et paient depuis\nlà-bas, tu reçois ton billet ici. Tu n'avances rien.\n\nTraverser sans savoir si on embarque, c'était normal. Ça ne l'est plus.\n\nmoheligo.com — WhatsApp +269 479 43 28\n\n#MoheliGo #Comores #Mohéli #Traversée #MVola"),
    dict(titre='Texte institutionnel — « grand conglomérat »', texte="""ENTRE DEUX ÎLES, IL Y A UN SERVICE.

Pendant longtemps, traverser vers Mohéli voulait dire se lever avant le jour,
descendre au port, et attendre de savoir.

MoheliGo a été construit pour supprimer cette attente.

Une plateforme. Quatre ports. Une réservation de deux minutes.
Un billet qui existe avant que vous arriviez au quai.
Un paiement qui part de votre téléphone — ou de celui d'un proche, à dix mille
kilomètres de là.
Un état de la mer consulté la veille, au lieu d'être découvert le matin.

Nous ne vendons pas des places de vedette. Nous rendons une liaison prévisible.

C'est le travail d'une infrastructure : retirer l'incertitude, puis se faire
oublier.

moheligo.com
Grande Comore et Mohéli — Union des Comores"""),

    dict(titre='Version très courte, même registre', texte="""Quatre ports. Deux îles. Une liaison prévisible.

Réservation, billet QR, paiement mobile et état de la mer : moheligo.com

MoheliGo — Union des Comores"""),

    dict(titre="Pour faire s'abonner à la page", texte="""POURQUOI S'ABONNER À CETTE PAGE ?

Parce qu'ici, chaque soir, vous trouverez la mer du lendemain matin sur le
trajet Grande Comore – Mohéli : hauteur de houle, vent, et un verdict clair —
mer belle, peu agitée, agitée.

Vous y trouverez aussi :
• les départs et les places qui restent ;
• les alertes quand la mer tourne mal, publiées la veille et pas le matin
  au port ;
• Mohéli comme elle est : les îlots, les tortues d'Itsamia, les baleines
  en saison.

Ce n'est pas une page de publicité. C'est le bulletin de la traversée.

Appuyez sur « S'abonner », et vous ne partirez plus à l'aveugle.

moheligo.com — réservation, billet QR, météo mer 7 jours.

#MoheliGo #Comores #Mohéli #MétéoMer #Traversée"""),

    dict(titre="Pour faire utiliser l'application", texte="""VOUS N'AVEZ RIEN À INSTALLER.

MoheliGo s'ouvre dans le navigateur de votre téléphone. Pas de boutique
d'applications, pas de mise à jour, pas de mémoire prise pour rien.

La première fois, ça prend deux minutes :

1. Ouvrez moheligo.com.
2. Choisissez votre port de départ, la date, le nombre de places.
3. Payez par MVola ou KartaPay.
4. Votre billet QR arrive aussitôt — et il reste dans votre téléphone, même
   sans connexion.

Une fois à l'intérieur, vous avez aussi la météo mer sur 7 jours, le suivi de
la vedette en direct pendant la traversée, le guide de l'île, et l'assistance
WhatsApp si quelque chose bloque.

Un conseil : ajoutez moheligo.com à l'écran d'accueil de votre téléphone.
Ça devient une icône, exactement comme une application.

moheligo.com — et la prochaine fois, votre place est prise avant d'arriver
au port.

#MoheliGo #Comores #Mohéli #BilletQR #MVola"""),

    dict(titre="Variante courte pour l'affiche", texte="""Un matin, la mer est plate. L'île est en face.
Il ne manque qu'une place.

moheligo.com — deux minutes, billet QR, paiement MVola.

#MoheliGo #Mohéli #Comores"""),
]


# ---------------------------------------------------------------------------
# Le plan publicitaire (demande du patron du 11/08/2026). La version longue est
# dans `dossier/PLAN-PUBLICITAIRE.md` ; ici c'est la version qu'on lit sur un
# téléphone : un chapitre = un volet dépliable, pas de tableau qui déborde.
# ---------------------------------------------------------------------------
PLAN_INTRO = ("On a déjà tout le matériel : 5 vidéos, une dizaine de flyers, le "
              "bulletin mer. Ce qui manque, ce n'est pas du matériel — c'est du "
              "<b>rythme</b>, du <b>terrain</b> et une <b>mesure</b>.")

SEMAINE = [
    ('Tous les soirs', 'Le bulletin mer', "19h30-21h · c'est le rendez-vous, il ne saute jamais"),
    ('Lundi', 'Comment ça marche', 'la vidéo démo de l\'app'),
    ('Mardi', "L'île", "l'affiche MOHÉLI, registre émotion"),
    ('Mercredi', 'Les prix', 'le flyer promo + les quatre ports'),
    ('Jeudi', 'La preuve', 'un vrai billet QR, un vrai client'),
    ('Vendredi', 'La diaspora', "jour de paie en Europe — le meilleur jour"),
    ('Samedi', 'La destination', 'la vidéo tourisme'),
    ('Dimanche', "L'institutionnel", 'le texte « Entre deux îles »'),
]

PALIERS = [
    ('Palier 0', '0 FC', 'Le rythme seul + tournée des ports. Croissance lente mais réelle.'),
    ('Palier 1', '≈ 25 000 FC / mois',
     '50 affiches couleur + 2 mises en avant par semaine. <b>Ma recommandation.</b>'),
    ('Palier 2', '≈ 100 000 FC / mois',
     'Palier 1 + campagne diaspora continue + reciblage des paniers abandonnés.'),
]

JOURS7 = [
    ('J1', 'Publier le film Amina', 'lien en premier commentaire · bulletin le soir'),
    ('J2', 'Ouvrir le tableau des 5 chiffres', 'noter les valeurs de départ'),
    ('J3', 'Imprimer 20 affiches A4', 'les fichiers 300 dpi sont prêts'),
    ('J4', 'Tournée Ouroveni + Chindini', 'affiches, et parler aux commandants'),
    ('J5', 'Publication diaspora', 'vendredi soir, jour de paie en Europe'),
    ('J6', 'Demander 3 témoignages', 'un mot + une photo de billet'),
    ('J7', 'Relever les 5 chiffres', 'et décider du palier de budget'),
]


def lignes_html(rangs):
    return ''.join(f'<div class="ligne"><span class="q">{q}</span>'
                   f'<span class="v">{v}</span><span class="d">{d}</span></div>'
                   for q, v, d in rangs)


PLAN = [
    ('1. Le diagnostic', """
<p>Notre problème n'est pas que les gens n'aiment pas le service. C'est que
<b>la plupart ne sait pas qu'on existe</b>, et que ceux qui savent hésitent à
payer en ligne un bateau qu'ils ont toujours payé en espèces au port.</p>
<p>Donc trois chantiers, dans cet ordre :</p>
<ul>
  <li><b>La notoriété</b> — « MoheliGo, c'est quoi ? » → présence quotidienne
      et affiches au port.</li>
  <li><b>La confiance</b> — « Si je paie, j'embarque vraiment ? » → des preuves :
      vrais billets, vrais clients, bulletin mer.</li>
  <li><b>La friction</b> — « Comment je paie, moi ? » → MVola et KartaPay
      expliqués en trois images, et un WhatsApp qui répond vite.</li>
</ul>
<p class="attention">Ne jamais payer de la publicité pour envoyer des gens dans
un tunnel qui fuit. Avant de dépenser un franc : vérifier que réserver et payer
prend moins de trois minutes sur un téléphone bas de gamme en 3G.</p>"""),

    ('2. Les quatre cibles, par valeur', """
<ul>
  <li><b>1. La diaspora payeuse</b> (France, Mayotte, Golfe) — carte bancaire,
      revenus en euros, famille à faire voyager. Elle ne prend pas le bateau :
      <b>elle paie le bateau des autres.</b> La plus rentable.</li>
  <li><b>2. Les habitués</b> — Mohéliens installés à Grande Comore, commerçants,
      fonctionnaires. Un client gagné = dix traversées. C'est le volume.</li>
  <li><b>3. Les grands moments</b> — mariages, deuils, rentrée scolaire. Voyage
      décidé en urgence : celui qui est visible à ce moment-là gagne.</li>
  <li><b>4. Les touristes et les lodges</b> — petit volume, gros panier,
      excellent pour l'image.</li>
</ul>"""),

    ('3. Notre arme, celle que personne n\'a', """
<p><b>Le bulletin mer quotidien.</b> Personne aux Comores ne publie chaque soir,
en chiffres, l'état de la mer du lendemain matin sur le couloir
Ouroveni – Hoani.</p>
<p>C'est le cœur du plan, pour une raison de fond : <b>on ne s'abonne pas à une
page qui vend, on s'abonne à une page qui sert.</b> Le bulletin est le service
gratuit ; la réservation est ce qu'on vend derrière.</p>
<p>Autrement dit : MoheliGo doit devenir <b>le média de la mer entre les deux
îles</b>. Celui qui vérifie la mer chez nous chaque soir réservera chez nous le
jour où il traverse — sans qu'on ait besoin de le convaincre.</p>
<p class="attention">Le prix à payer : c'est un engagement <b>tous les soirs</b>.
Un bulletin un soir sur trois ne crée aucune habitude. Soit on tient sept soirs
sur sept, soit on annonce « du lundi au vendredi » et on s'y tient.</p>"""),

    ('4. Étage 1 — le rythme (0 FC)', """
<p>C'est la base. Rien de payant ne marche sans ça. La semaine type, aux heures
de pointe comoriennes (12h-14h et 19h-22h) :</p>
{semaine}
<p style="margin-top:13px">Quatre règles d'exécution :</p>
<ul>
  <li>Le <b>lien va dans le premier commentaire</b>, pas dans le post.</li>
  <li><b>Statut WhatsApp chaque soir</b> avec le bulletin. Aux Comores, WhatsApp
      touche plus de monde que le fil Facebook — et c'est notre canal le plus
      sous-exploité. Gratuit.</li>
  <li><b>Répondre en moins de 10 minutes</b> entre 12h-14h et 19h-22h. Un message
      sans réponse le soir, c'est une réservation perdue. C'est le levier de
      conversion le moins cher de tout ce plan.</li>
  <li>Une seule idée par publication. Jamais deux appels à l'action.</li>
</ul>"""),

    ('5. Étage 2 — le terrain (coût : impression)', """
<p>Aux Comores, l'affiche physique bat le ciblage publicitaire, parce qu'elle est
là <b>au moment exact</b> où la personne pense au voyage. Par ordre
d'efficacité :</p>
<ul>
  <li><b>Les ports</b> — Chindini, Ouroveni, Hoani, Fomboni. Celui qui attend la
      vedette s'ennuie : il scanne.</li>
  <li><b>Les boutiques et cabines</b> autour des embarcadères et des gares
      routières.</li>
  <li><b>Les hôtels et lodges de Mohéli</b> — « vos clients réservent leur retour
      depuis votre réception, en trois minutes ».</li>
  <li><b>Les commandants et les équipages</b> — ce sont eux qu'on croit. Un
      commandant qui dit « réserve sur MoheliGo » vaut dix publications.</li>
  <li><b>Les taxis</b> de la route Moroni – Chindini.</li>
</ul>
<p>Les affiches A4 300 dpi sont déjà prêtes dans le dépôt, QR compris.</p>
<p><b>Le code partenaire, sans une ligne de code :</b> chaque partenaire reçoit un
mot à faire dire sur WhatsApp. On compte les mots reçus, on sait qui travaille,
on récompense. À mettre en place tout de suite, ça ne coûte rien.</p>"""),

    ('6. Étage 3 — le payant, après les deux autres', """
<ul>
  <li><b>La diaspora d'abord</b> — France (Marseille, Dunkerque, Paris), Mayotte,
      puis le Golfe. C'est la seule cible qui paie en euros : le coût par
      réservation y sera le meilleur.</li>
  <li><b>Mettre en avant le bulletin</b> auprès du public comorien, avec pour
      objectif les abonnés et pas les ventes. On achète l'audience une fois,
      elle revient gratuitement chaque soir.</li>
  <li><b>Le reciblage</b> de ceux qui ont commencé à payer sans finir. Demande
      d'installer le pixel Meta sur le site.</li>
</ul>
<p class="attention">À vérifier avant de rien promettre : Meta se paie par carte
bancaire ou PayPal — <b>MVola ne paie pas Facebook</b>. Sans carte utilisable,
l'étage 3 n'existe pas, et le plan tient très bien sur les étages 1 et 2.</p>"""),

    ('7. Le budget — trois paliers', """
<p>Rappel de change : le franc comorien est arrimé à l'euro,
<b>1 € = 492 FC</b>.</p>
{paliers}
<p style="margin-top:13px"><b>Palier 1 pendant un mois, en mesurant.</b> On ne
passe au palier 2 que si le premier mois prouve un coût par réservation
acceptable. Dépenser plus avant d'avoir mesuré, c'est acheter du bruit.</p>"""),

    ('8. Cinq chiffres, relevés chaque dimanche', """
<ul>
  <li><b>Abonnés de la page</b> — le stock qu'on construit.</li>
  <li><b>Visites sur moheligo.com</b> — l'intérêt qu'on génère.</li>
  <li><b>Réservations payées</b> — la seule qui compte vraiment.</li>
  <li><b>Abandon au paiement</b> — combien commencent, combien finissent.</li>
  <li><b>Coût par réservation</b> — dépensé ÷ réservations payées.</li>
</ul>
<p class="attention">Si l'abandon au paiement est mauvais : on arrête la
publicité et on répare le site d'abord. Et le seuil de décision est simple — le
coût par réservation doit rester nettement sous la marge gagnée sur une
traversée.</p>"""),

    ('9. Ce que j\'attends de toi, patron', """
<ul>
  <li><b>La marge que tu gagnes par réservation.</b> Sans ce chiffre, aucune
      publicité n'est jugeable. C'est la donnée la plus importante du plan.</li>
  <li><b>Une carte pour payer Meta</b>, si on veut l'étage 3.</li>
  <li><b>Trois témoignages de vrais clients</b> + une photo de billet QR. C'est le
      contenu qui convertit le mieux, et le seul que je ne peux pas fabriquer :
      inventer un témoignage, ça se retourne contre nous.</li>
  <li><b>Le budget d'impression</b>, et qui fait la tournée des ports.</li>
  <li><b>Tu ou vous ?</b> Ma recommandation : tutoyer partout, sauf
      l'institutionnel et le A4 destiné aux partenaires.</li>
</ul>"""),

    ('10. Les sept premiers jours', """
{jours7}
<p style="margin-top:13px">Le seul engagement qui compte dans cette liste :
<b>le bulletin, tous les soirs.</b> Le reste peut glisser d'un jour. Pas lui.</p>"""),
]


def api(url, essais=4):
    dernier = ''
    for n in range(essais):
        cmd = ['curl', '-sS', '--max-time', '25']
        if os.path.isfile(CACERT):
            cmd += ['--cacert', CACERT]
        out = subprocess.run(cmd + [url], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip():
            try:
                return json.loads(out.stdout)
            except json.JSONDecodeError as e:
                dernier = str(e)
        else:
            dernier = out.stderr.strip() or 'réponse vide'
        time.sleep(2 * (n + 1))
    sys.exit('Open-Meteo injoignable : ' + dernier)


def virgule(x, n=1):
    return f'{x:.{n}f}'.replace('.', ',')


def meteo_demain(cible):
    """Quatre lignes lisibles : la mer, le matin, l'après-midi, le soir."""
    jour = cible.isoformat()
    mer = api(f'https://marine-api.open-meteo.com/v1/marine?latitude={LAT_MER}&longitude={LON_MER}'
              f'&hourly=wave_height&timezone={TZ}&forecast_days=2')
    ter = api(f'https://api.open-meteo.com/v1/forecast?latitude={LAT_TERRE}&longitude={LON_TERRE}'
              f'&hourly=temperature_2m,precipitation_probability,weather_code'
              f'&daily=weather_code&timezone={TZ}&forecast_days=2')
    hi = {h: i for i, h in enumerate(ter['hourly']['time'])}
    hm = {h: i for i, h in enumerate(mer['hourly']['time'])}

    def t(h):  return ter['hourly']['temperature_2m'][hi[f'{jour}T{h:02d}:00']]
    def pl(h): return ter['hourly']['precipitation_probability'][hi[f'{jour}T{h:02d}:00']]
    def co(h): return CIEL.get(ter['hourly']['weather_code'][hi[f'{jour}T{h:02d}:00']], '—')

    houle = [mer['hourly']['wave_height'][hm[f'{jour}T{h:02d}:00']] for h in range(6, 11)]
    h_moy = sum(houle) / len(houle)
    etat = ('Belle' if h_moy < .5 else 'Peu agitée' if h_moy < 1.25
            else 'Agitée' if h_moy < 2.5 else 'Forte')
    apm = max(range(12, 18), key=pl)
    return [
        ('Mer', etat, f'houle {virgule(h_moy)} m au petit matin'),
        ('Matin', co(6), f'{t(6):.0f} °C à 6h, {t(9):.0f} °C à 9h'),
        ('Après-midi', co(15), f'risque de pluie {pl(apm)} % vers {apm}h · {t(12):.0f} °C'),
        ('Soir', co(18), f'{t(18):.0f} °C à 18h, {t(21):.0f} °C à 21h'),
    ]


def b64(chemin):
    return base64.b64encode(pathlib.Path(chemin).read_bytes()).decode()


def jpeg_leger(png, largeur=1080):
    """Le patron est sur un téléphone : on embarque du JPEG, pas du PNG de 2,6 Mo."""
    tmp = pathlib.Path('/tmp') / (pathlib.Path(png).stem + '-page.jpg')
    im = Image.open(png).convert('RGB')
    im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    im.save(tmp, quality=88, optimize=True)
    return b64(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sortie', default='page-flyers.html')
    args = ap.parse_args()

    maintenant = datetime.now(timezone(timedelta(hours=3)))
    demain = maintenant.date() + timedelta(days=1)
    fr = lambda d: f'{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}'

    lignes = ''.join(
        f'<div class="ligne"><span class="q">{q}</span><span class="v">{v}</span>'
        f'<span class="d">{d}</span></div>' for q, v, d in meteo_demain(demain))

    chapitres = ''
    for titre, corps in PLAN:
        corps = corps.format(semaine=lignes_html(SEMAINE), paliers=lignes_html(PALIERS),
                             jours7=lignes_html(JOURS7))
        chapitres += (f'<details><summary>{titre}</summary>'
                      f'<div class="plan">{corps}</div></details>')

    blocs = ''
    for i, f in enumerate(FLYERS, start=1):
        texte = (pathlib.Path(f['texte'][1:]).read_text().split('--- premier commentaire ---')[0].strip()
                 if f['texte'].startswith('@') else f['texte'])
        blocs += f'''
  <section class="bloc">
    <div class="tete"><b>{f['titre']}</b><span>{f['note']}</span></div>
    <img class="shot" src="data:image/jpeg;base64,{jpeg_leger(f['png'])}" alt="{f['titre']} MoheliGo">
    <p class="howto"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 11l5 5 5-5M4 20h16"/></svg>
      Appui long sur l'image, puis « Enregistrer » ou « Ajouter aux photos ».</p>
    <details><summary>Le texte du post</summary>
      <pre>{texte}</pre>
      <button class="copie" data-cible="t{i}">Copier le texte</button>
      <textarea id="t{i}" hidden>{texte}</textarea>
    </details>
  </section>
'''

    n = len(FLYERS)
    for j, t in enumerate(TEXTES, start=n + 1):
        blocs += f'''
  <section class="bloc">
    <div class="tete"><b>{t['titre']}</b><span>Texte seul<br>sans image</span></div>
    <details open><summary>Le texte</summary>
      <pre>{t['texte']}</pre>
      <button class="copie" data-cible="t{j}">Copier le texte</button>
      <textarea id="t{j}" hidden>{t['texte']}</textarea>
    </details>
  </section>
'''

    html = GABARIT.format(
        arch=b64('fonts/Archivo-800-latin.woff2'),
        in5=b64('fonts/Inter-500-latin.woff2'),
        in7=b64('fonts/Inter-700-latin.woff2'),
        embleme=b64('logo-emblem.png'),
        titre_jour=f'Demain, {fr(demain)}',
        releve=f"Relevé {fr(maintenant.date())} à {maintenant.strftime('%Hh%M')}, heure des Comores",
        lignes=lignes, plan_intro=PLAN_INTRO, chapitres=chapitres, blocs=blocs)
    pathlib.Path(args.sortie).write_text(html)
    print(args.sortie, round(len(html) / 1024), 'ko —', len(FLYERS), 'flyers,',
          len(TEXTES), 'textes,', len(PLAN), 'chapitres de plan')


GABARIT = '''<title>MoheliGo — la météo de demain et les flyers</title>
<style>
@font-face {{ font-family:'Archivo'; font-weight:800; font-display:swap;
  src:url(data:font/woff2;base64,{arch}) format('woff2'); }}
@font-face {{ font-family:'Inter'; font-weight:500; font-display:swap;
  src:url(data:font/woff2;base64,{in5}) format('woff2'); }}
@font-face {{ font-family:'Inter'; font-weight:700; font-display:swap;
  src:url(data:font/woff2;base64,{in7}) format('woff2'); }}

:root {{
  --ground:#F4F7FC; --card:#FFFFFF; --ink:#0F2A5C; --ink-soft:#5C6E8B;
  --line:#DCE4F1; --gold:#F6BC1C; --gold-ink:#5B4508; --btn:#0F2A5C;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#071630; --card:#0E2145; --ink:#EAF1FD; --ink-soft:#9FB6D8;
    --line:#1E3766; --gold:#F6BC1C; --gold-ink:#3A2B03; --btn:#1B4A8E;
  }}
}}
:root[data-theme="dark"] {{
  --ground:#071630; --card:#0E2145; --ink:#EAF1FD; --ink-soft:#9FB6D8;
  --line:#1E3766; --gold:#F6BC1C; --gold-ink:#3A2B03; --btn:#1B4A8E;
}}

* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--ground); color:var(--ink);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; font-weight:500;
  line-height:1.55; -webkit-font-smoothing:antialiased; }}
.wrap {{ max-width:560px; margin:0 auto; padding:26px 18px 56px; display:flex;
  flex-direction:column; gap:30px; }}
header {{ display:flex; align-items:center; gap:14px; }}
header img {{ width:50px; height:auto; display:block; }}
header b {{ font-family:'Archivo',sans-serif; font-weight:800; font-size:20px; letter-spacing:-.4px;
  display:block; line-height:1.15; }}
header span {{ display:block; font-size:13.5px; color:var(--ink-soft); }}

.bloc {{ background:var(--card); border:1px solid var(--line); border-radius:16px; overflow:hidden; }}
.tete {{ display:flex; align-items:baseline; justify-content:space-between; gap:12px;
  padding:16px 18px 14px; border-bottom:1px solid var(--line); }}
.tete b {{ font-family:'Archivo',sans-serif; font-weight:800; font-size:17px; letter-spacing:-.2px; }}
.tete span {{ font-size:13px; color:var(--ink-soft); text-align:right; }}

.ligne {{ display:grid; grid-template-columns:92px 1fr; gap:2px 12px; padding:13px 18px;
  border-bottom:1px solid var(--line); }}
.ligne:last-child {{ border-bottom:0; }}
.ligne .q {{ grid-row:span 2; font-size:12.5px; font-weight:700; letter-spacing:.6px;
  text-transform:uppercase; color:var(--ink-soft); padding-top:3px; }}
.ligne .v {{ font-family:'Archivo',sans-serif; font-weight:800; font-size:18px; }}
.ligne .d {{ font-size:14px; color:var(--ink-soft); }}

img.shot {{ width:100%; height:auto; display:block; }}
.howto {{ display:flex; gap:11px; align-items:flex-start; margin:0; padding:15px 18px;
  background:var(--gold); color:var(--gold-ink); font-size:14.5px; font-weight:700; }}
.howto svg {{ flex:none; margin-top:1px; }}

details {{ border-top:1px solid var(--line); }}
details[open] summary {{ border-bottom:1px solid var(--line); margin-bottom:14px; }}
summary {{ padding:15px 18px; font-size:15px; font-weight:700; cursor:pointer; list-style:none;
  display:flex; justify-content:space-between; align-items:center; gap:10px; }}
summary::-webkit-details-marker {{ display:none; }}
summary::after {{ content:'+'; font-family:'Archivo',sans-serif; font-size:20px; color:var(--ink-soft); }}
details[open] summary::after {{ content:'\\2013'; }}
summary:focus-visible {{ outline:3px solid var(--gold); outline-offset:-3px; }}
pre {{ margin:0; padding:0 18px 18px; white-space:pre-wrap; word-wrap:break-word;
  font-family:inherit; font-size:14.5px; line-height:1.6; }}
.copie {{ margin:0 18px 18px; padding:13px 18px; width:calc(100% - 36px);
  font-family:'Archivo',sans-serif; font-weight:800; font-size:15px; color:#fff;
  background:var(--btn); border:0; border-radius:999px; cursor:pointer; }}
.copie:focus-visible {{ outline:3px solid var(--gold); outline-offset:2px; }}
footer {{ font-size:14px; color:var(--ink-soft); border-top:1px solid var(--line); padding-top:20px; }}
footer b {{ color:var(--ink); }}

/* le plan publicitaire */
.intro {{ margin:0; padding:15px 18px; font-size:14.5px; color:var(--ink-soft); }}
.intro b {{ color:var(--ink); }}
.plan {{ padding:0 18px 6px; font-size:14.5px; }}
.plan p {{ margin:0 0 12px; }}
.plan ul {{ margin:0 0 12px; padding-left:19px; }}
.plan li {{ margin-bottom:8px; }}
.plan .ligne {{ padding:11px 0; grid-template-columns:108px 1fr; }}
.plan .ligne .v {{ font-size:16px; }}
.plan .attention {{ background:var(--gold); color:var(--gold-ink); font-weight:700;
  border-radius:12px; padding:13px 15px; margin-bottom:12px; }}
.plan details {{ border:0; }}
</style>

<div class="wrap">
  <header>
    <img src="data:image/png;base64,{embleme}" alt="">
    <div><b>{titre_jour}</b><span>{releve}</span></div>
  </header>

  <section class="bloc">
    <div class="tete"><b>La météo de demain</b><span>Mohéli et le couloir<br>Ouroveni – Hoani</span></div>
    {lignes}
  </section>

  <section class="bloc">
    <div class="tete"><b>Le plan publicitaire</b><span>Pour avoir<br>plus d'utilisateurs</span></div>
    <p class="intro">{plan_intro}</p>
    {chapitres}
  </section>
{blocs}
  <footer>Le bulletin du soir annonce <b>demain matin</b> : bon pour ce soir seulement.
    Les autres flyers n'ont pas de date, gardez-les. Les derniers blocs sont des
    <b>textes seuls</b>, à publier sans image ou avec une de vos photos.
    Le plan complet est aussi dans le dépôt : <b>moheligo/dossier/PLAN-PUBLICITAIRE.md</b>.</footer>
</div>

<script>
document.querySelectorAll('.copie').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var t = document.getElementById(b.dataset.cible), fini = function () {{
      var a = b.textContent; b.textContent = 'Texte copié';
      setTimeout(function () {{ b.textContent = a; }}, 2200);
    }};
    if (navigator.clipboard) {{ navigator.clipboard.writeText(t.value).then(fini, function () {{ manuel(t, fini); }}); }}
    else {{ manuel(t, fini); }}
  }});
}});
function manuel(t, fini) {{
  t.hidden = false; t.select(); t.setSelectionRange(0, 99999);
  try {{ document.execCommand('copy'); fini(); }} catch (e) {{}}
  t.hidden = true;
}}
</script>
'''

if __name__ == '__main__':
    main()
