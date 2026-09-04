#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LES QUESTIONS DES DEUX ÉVALUATIONS — la source, et rien d'autre.

`examen.py` ne fait que les mettre en page. Corriger une question ICI, puis
relancer : les trois PDF (les deux sujets et le corrigé) se refont ensemble et
ne peuvent donc pas se contredire.

📌 CE QU'UNE QUESTION DOIT ÊTRE, ET CE QU'ELLE NE DOIT PAS ÊTRE
On n'évalue pas la mémoire, on évalue le réflexe. Chaque question est donc une
SITUATION avec une décision à prendre, pas une définition à réciter. « Que dit
le GOM sur l'assistance PMR ? » ne prouve rien ; « une assistance PMR n'a pas
été annoncée à la réservation, que fait l'escale ? » prouve qu'on saura quoi
faire mardi matin.

Les mauvaises réponses ne sont pas des remplissages : chacune est une erreur
qu'on voit réellement au comptoir ou en salle. Un agent qui coche B à la
question 4 de l'escale ne s'est pas trompé au hasard — il a un problème précis,
et le corrigé le nomme.

Chaque question porte son RENVOI : le chapitre du film et la procédure. Une
mauvaise réponse doit toujours pouvoir se rattraper en revoyant trente
secondes de film, pas le film entier.

BARÈME : 1 point par question, seuil d'acquisition à 8/10. Ce seuil est haut
volontairement — les deux tiers des questions portent sur des règles où il n'y
a pas de demi-mesure (sûreté, données passager, traçabilité).
"""

SEUIL = 8          # sur 10, en dessous : à revoir avec le chef d'escale ou d'agence


# ═══════════════════════════════════════════════════════ ÉVALUATION 1 — AGENCE
AGENCE = {
    "titre": "L'accueil en agence",
    "film": "RoyalAir-accueil-agence.mp4",
    "reference": "QUA-EVAL-001",
    "pour": "Personnel des comptoirs de vente et de la réservation",
    "questions": [
        {"q": "Un passager entre dans l'agence pendant que vous êtes au téléphone. "
              "Que faites-vous ?",
         "options": [
             "Vous terminez l'appel avant de vous occuper de lui : c'est plus efficace.",
             "Vous lui faites un signe de la main et vous croisez son regard.",
             "Vous lui demandez à voix haute de patienter, sans interrompre l'appel.",
             "Vous lui montrez la chaise sans lever les yeux."],
         "bonne": 1,
         "pourquoi": "Il faut qu'il sache qu'il existe. Un regard et un signe coûtent "
                     "une seconde et suppriment toute l'attente ressentie.",
         "renvoi": "Film 1 · Premiers instants"},

        {"q": "Vous ne pouvez pas servir un passager tout de suite. "
              "Qu'est-ce qui compte le plus ?",
         "options": [
             "Le servir en moins de deux minutes.",
             "Lui proposer de repasser plus tard.",
             "Lui annoncer combien de temps il va attendre.",
             "Ne rien dire pour ne pas le déranger."],
         "bonne": 2,
         "pourquoi": "Deux minutes annoncées passent mieux que trente secondes de "
                     "silence. Ce n'est pas la durée qui fâche, c'est de ne pas savoir.",
         "renvoi": "Film 1 · Premiers instants"},

        {"q": "Un passager pose une question dont vous n'avez pas la réponse. "
              "Que dites-vous ?",
         "options": [
             "« Je ne sais pas. »",
             "« Ce n'est pas mon service. »",
             "« C'est le système, je n'y peux rien. »",
             "« Je vérifie et je vous donne la réponse avant midi. »"],
         "bonne": 3,
         "pourquoi": "Les trois autres ferment la porte. La bonne réponse engage un "
                     "délai — et un délai annoncé se tient.",
         "renvoi": "Film 1 · Écouter"},

        {"q": "Un passager demande un tarif que vous n'avez pas vérifié au système. "
              "Vous :",
         "options": [
             "Annoncez le tarif habituel : il change rarement.",
             "Donnez une fourchette pour ne pas le faire attendre.",
             "Vérifiez avant d'annoncer quoi que ce soit.",
             "Le renvoyez vers l'escale le jour du vol."],
         "bonne": 2,
         "pourquoi": "Un tarif annoncé engage Royal Air. Une fourchette aussi : "
                     "le passager retiendra le bas de la fourchette.",
         "renvoi": "Film 1 · Information · QUA-PROC-002"},

        {"q": "Le vol d'un passager est reporté à demain et il hausse le ton. Quelle "
              "est la seule technique qui fonctionne à tous les coups ?",
         "options": [
             "Lui rappeler les conditions de transport.",
             "Baisser la voix d'un ton.",
             "Appeler un responsable tout de suite.",
             "Lui expliquer que ce n'est pas la faute de l'agence."],
         "bonne": 1,
         "pourquoi": "L'autre baisse la sienne pour vous entendre. Les trois autres "
                     "réponses font monter le ton d'un cran.",
         "renvoi": "Film 1 · Irrégularités"},

        {"q": "Pendant une irrégularité, qu'est-ce qui ne se fait jamais devant "
              "le passager ?",
         "options": [
             "Reconnaître qu'on n'a pas encore l'information.",
             "Donner l'heure de la prochaine information.",
             "Mettre la faute sur un collègue ou sur l'escale.",
             "Noter par écrit ce qui lui a été dit."],
         "bonne": 2,
         "pourquoi": "Devant le passager, la compagnie parle d'une seule voix. "
                     "Désigner un coupable interne détruit la confiance dans le tout.",
         "renvoi": "Film 1 · Irrégularités"},

        {"q": "Un homme demande si son frère est bien sur le vol de demain. Il donne "
              "le nom, la date, il connaît tout le dossier. Vous :",
         "options": [
             "Confirmez : il connaît manifestement le dossier.",
             "Confirmez le vol, mais pas le numéro de place.",
             "Demandez l'accord de votre chef, puis confirmez.",
             "Ne communiquez rien."],
         "bonne": 3,
         "pourquoi": "Les données du passager ne sortent pas de l'agence — ni à la "
                     "famille, ni au téléphone, ni sur WhatsApp. Connaître le dossier "
                     "n'est pas une autorisation.",
         "renvoi": "Film 1 · Le comptoir"},

        {"q": "Une passagère âgée entre avec ses bagages. L'assistance :",
         "options": [
             "Se propose sans attendre qu'elle la demande.",
             "Se déclenche uniquement à sa demande.",
             "Se traite à l'aéroport, pas en agence.",
             "Est réservée aux passagers déclarés PMR."],
         "bonne": 0,
         "pourquoi": "L'assistance se propose, elle ne se mendie pas. Attendre la "
                     "demande, c'est obliger quelqu'un à se déclarer diminué.",
         "renvoi": "Film 1 · Accompagner"},

        {"q": "Que fait-on de la réclamation d'un passager mécontent ?",
         "options": [
             "On la règle sur place et on n'en parle plus.",
             "On la note et on la remonte au Département Qualité le jour même.",
             "On la transmet oralement au chef d'agence.",
             "On la note seulement si le passager insiste."],
         "bonne": 1,
         "pourquoi": "Une réclamation est une information gratuite sur ce qui ne "
                     "marche pas. Réglée sans être remontée, elle se reproduira.",
         "renvoi": "Film 1 · La trace · QUA-PROC-002"},

        {"q": "Lors d'un audit ANACM, qu'est-ce qui est examiné ?",
         "options": [
             "La qualité de l'accueil constatée sur place le jour de l'audit.",
             "Le témoignage des agents en poste.",
             "L'absence de réclamation sur la période.",
             "Ce qui est écrit et tracé."],
         "bonne": 3,
         "pourquoi": "L'audit lit les traces, pas les intentions. Ce qui n'est pas "
                     "écrit n'existe pas — même si cela a été fait.",
         "renvoi": "Film 1 · La trace · QUA-PROC-002"},
    ],
}


# ═══════════════════════════════════════════════════════ ÉVALUATION 2 — ESCALE
ESCALE = {
    "titre": "L'accueil en escale",
    "film": "RoyalAir-accueil-escale.mp4",
    "reference": "QUA-EVAL-002",
    "pour": "Agents d'escale — Moroni (HAH), Ouani (AJN), Mohéli (NWA)",
    "questions": [
        {"q": "Le comptoir ouvre dans dix minutes, vingt personnes attendent déjà "
              "devant la porte. Qu'est-ce qui doit être prêt ?",
         "options": [
             "Ouvrir en avance pour désengorger l'entrée.",
             "L'état du vol, connu avant que le premier passager ne le demande.",
             "L'appel au chef d'escale pour renfort.",
             "Le passage prioritaire des PMR."],
         "bonne": 1,
         "pourquoi": "Le vol commence quand le comptoir ouvre. Un agent qui découvre "
                     "le retard en même temps que le passager a déjà perdu la salle.",
         "renvoi": "Film 2 · Avant le vol · GOM"},

        {"q": "Un bagage dépasse la franchise de 3 kg. Comment l'annoncez-vous ?",
         "options": [
             "« Votre bagage est trop lourd. »",
             "« C'est le règlement, c'est comme ça. »",
             "« Nous sommes à 3 kg au-dessus. Voici vos deux options. »",
             "Vous laissez passer : 3 kg, ce n'est rien."],
         "bonne": 2,
         "pourquoi": "On annonce un chiffre et une solution, pas un jugement. Et sur "
                     "le LET 410, laisser passer n'est pas un service rendu : chaque "
                     "kilo compte pour la sécurité du vol.",
         "renvoi": "Film 2 · Enregistrement"},

        {"q": "À quel moment annonce-t-on la franchise bagages ?",
         "options": [
             "Après la pesée, pour ne pas inquiéter inutilement.",
             "Avant de poser le bagage sur la balance.",
             "Seulement si le passager pose la question.",
             "À l'embarquement, si le bagage pose problème."],
         "bonne": 1,
         "pourquoi": "Annoncée après, la règle ressemble à une sanction. Annoncée "
                     "avant, c'est une information — et la discussion n'a pas lieu.",
         "renvoi": "Film 2 · Enregistrement"},

        {"q": "Un collègue vous demande d'enregistrer le bagage de son cousin, qui "
              "arrive juste après. Il vous dit : « je le connais ». Vous :",
         "options": [
             "Acceptez : il se porte garant.",
             "Acceptez si le cousin se présente avant la fermeture du vol.",
             "Demandez au chef d'escale de trancher, et suivez sa décision.",
             "Refusez, et signalez la demande."],
         "bonne": 3,
         "pourquoi": "Aucun bagage ne part sans son passager à bord — connaître "
                     "quelqu'un n'y change rien. Et une pression pour contourner une "
                     "règle de sûreté se signale : elle ne se gère pas seul, et elle "
                     "ne se délègue pas non plus.",
         "renvoi": "Film 2 · Sûreté · GRD-PROC-001"},

        {"q": "Le vol devait partir à 11 h. Il est 12 h 20, personne n'a rien dit "
              "depuis une heure et la salle se lève. Quelle est la faute ?",
         "options": [
             "Le retard lui-même.",
             "L'absence d'information.",
             "Le manque de personnel au comptoir.",
             "L'absence de prise en charge repas."],
         "bonne": 1,
         "pourquoi": "Ce qui fâche un passager n'est presque jamais le retard, c'est "
                     "de ne pas savoir. Une salle informée attend ; une salle ignorée "
                     "s'énerve.",
         "renvoi": "Film 2 · Salle d'attente"},

        {"q": "En cas de retard, à quel rythme informe-t-on la salle ?",
         "options": [
             "Dès qu'on a une information nouvelle.",
             "Toutes les vingt minutes, même sans rien de nouveau.",
             "Toutes les heures.",
             "Une seule fois, à l'annonce du retard."],
         "bonne": 1,
         "pourquoi": "« Nous n'avons pas encore d'information » est une information. "
                     "Le silence, non. Attendre d'avoir du neuf, c'est laisser la "
                     "salle inventer ses propres explications.",
         "renvoi": "Film 2 · Salle d'attente"},

        {"q": "Qui embarque en premier ?",
         "options": [
             "Les passagers enregistrés depuis le plus longtemps.",
             "Les passagers des rangs arrière.",
             "Les PMR, les familles avec enfants et les personnes âgées.",
             "Les passagers au plein tarif."],
         "bonne": 2,
         "pourquoi": "Ceux qui ont besoin de temps embarquent quand il y en a. "
                     "Les faire passer en dernier, c'est les faire monter sous le "
                     "regard de tout l'avion.",
         "renvoi": "Film 2 · Embarquement"},

        {"q": "Une assistance PMR n'a pas été annoncée à la réservation. "
              "Que fait l'escale ?",
         "options": [
             "Elle refuse : l'assistance se demande à l'avance.",
             "Elle assiste d'abord, et régularise ensuite.",
             "Elle attend la confirmation de l'agence.",
             "Elle assiste si le temps le permet."],
         "bonne": 1,
         "pourquoi": "L'assistance est due dans les deux cas. La régularisation est "
                     "un problème de dossier, pas un préalable à l'aide.",
         "renvoi": "Film 2 · Accompagner"},

        {"q": "Un bagage arrive manquant. Quand remplit-on le constat ?",
         "options": [
             "Après le départ du passager, au calme.",
             "Le lendemain, avec le dossier complet.",
             "Sur place, avec le passager.",
             "Seulement si le passager le réclame."],
         "bonne": 2,
         "pourquoi": "Rempli sans lui, le constat est incomplet et invérifiable. "
                     "Et un passager qui repart sans réponse revient en réclamation "
                     "écrite.",
         "renvoi": "Film 2 · L'arrivée"},

        {"q": "Un événement d'escale touche la sécurité. À qui remonte-t-il ?",
         "options": [
             "Au chef d'escale, qui décide de la suite.",
             "Au SGS, en plus du chef d'escale.",
             "À l'agence de Moroni.",
             "Directement à l'ANACM."],
         "bonne": 1,
         "pourquoi": "Ce qui touche la sécurité part au SGS. S'arrêter au chef "
                     "d'escale, c'est laisser l'information mourir à l'échelon où "
                     "elle est née. Un signalement n'est jamais reproché ; une "
                     "omission, si.",
         "renvoi": "Film 2 · La trace · GOM · GRD-PROC-001"},
    ],
}
