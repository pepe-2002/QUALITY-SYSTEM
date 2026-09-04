#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LE TEXTE DES DEUX FILMS DE SENSIBILISATION — la source, et rien d'autre.

Tout ce qui se lit à l'écran est ici. `film.py` ne fait que le mettre en image.
Pour corriger une phrase : la corriger ICI, puis relancer `python3 film.py`.
Ne jamais retoucher un .mp4 — on corrigerait la copie au lieu de la source.

D'OÙ VIENT LE CONTENU
Rien n'est repris d'un film étranger. Les règles écrites ici sont celles de nos
propres documents (GOM, GRD-PROC-001 Sécurité en piste, QUA-PROC-002 Gestion des
non-conformités), appliquées à nos escales (Moroni HAH, Ouani AJN, Mohéli NWA)
et à notre flotte (LET 410). C'est ce qui rend ces films opposables en audit :
un agent formé sur eux est formé sur nos procédures.

RÈGLE D'ÉCRITURE — chaque point doit être VÉRIFIABLE. « Être aimable » ne se
constate pas. « Saluer le premier » se constate. On n'écrit que des choses qu'un
chef d'escale peut voir faire ou ne pas faire.

📌 LA FORME VIENT D'UNE COMPARAISON DES FILMS DE FORMATION QUI MARCHENT
Trois choses reviennent dans tous, et sont reprises ici :
  1. UNE SITUATION AVANT LA RÈGLE. On ne commence pas par la consigne, on
     commence par une scène que l'agent a déjà vécue, et une question restée
     en suspens. La règle qui suit répond à une question qu'il s'est posée.
  2. LE CÔTE À CÔTE « ne dites pas / dites ». Une phrase de remplacement
     change une habitude ; un principe général ne la change pas.
  3. UNE SEULE IDÉE PAR ÉCRAN, et un écran par point. Les points arrivent un
     par un : on lit ce qui apparaît, jamais un mur de texte.
Ajouté pour notre cas : une BARRE D'AVANCEMENT en haut. Un film de cinq minutes
sur un téléphone, sans savoir où il en est, se referme au bout de deux.
"""

# Durées, en secondes. Un point de liste = le temps de le lire à voix haute,
# une fois et demie : sur WhatsApp on regarde en marchant.
PAR_POINT = 4.0
CHAPITRE = 3.6
REGLE = 6.6
SITUATION = 7.5

PIED_FINAL = [
    "Film interne de sensibilisation — Département Qualité.",
    "Diffusion réservée au groupe WhatsApp du personnel Royal Air. "
    "Ne pas publier sur Facebook ni sur aucun réseau public.",
    "Références : GOM · GRD-PROC-001 · QUA-PROC-002 · Manuel Qualité — ANACM.",
]


# ═══════════════════════════════════════════════════════ FILM 1 — EN AGENCE
AGENCE = {
    "titre": "Film 1 — L'accueil des passagers en agence",
    "fichier": "RoyalAir-accueil-agence",
    "scenes": [
        {"type": "ouverture", "duree": 6.4,
         "titre": "L'accueil en agence",
         "sous_titre": "Ce que le passager retient de nous, "
                       "il le décide avant même de voir l'avion.",
         "mention": "Film de sensibilisation · Département Qualité"},

        {"type": "regle", "chapitre": "Pourquoi", "duree": 7.6,
         "texte": "L'agence, c'est la compagnie.",
         "appui": "Le passager ne fait pas la différence entre l'agent qui le reçoit et "
                  "Royal Air. Un vol parfait ne rattrape pas un mauvais comptoir. "
                  "Un bon comptoir, lui, fait pardonner beaucoup."},

        {"type": "situation", "chapitre": "Premiers instants", "duree": SITUATION,
         "texte": "Il est 9 h 10 à l'agence. Vous comptez la caisse de la veille. "
                  "Un homme entre, s'arrête devant le comptoir, et attend.",
         "question": "Qu'est-ce qu'il voit de vous ?"},
        {"type": "liste", "chapitre": "Premiers instants",
         "titre": "Il vous a déjà jugé avant de parler.",
         "par_point": PAR_POINT, "points": [
             "Lever les yeux dès qu'il entre. Même occupé, surtout occupé.",
             "Saluer le premier. Bonjour, Salam aleikoum — jamais l'inverse.",
             "Se redresser, poser le stylo. Le corps parle avant la bouche.",
             "Au téléphone : un regard, un signe de la main. Il sait qu'il existe.",
         ]},
        {"type": "regle", "chapitre": "Premiers instants", "duree": REGLE,
         "texte": "Personne n'attend sans savoir combien de temps.",
         "appui": "Deux minutes annoncées passent mieux que trente secondes de silence."},

        {"type": "chapitre", "numero": "1", "chapitre": "Écouter",
         "titre": "Écouter avant de répondre", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Écouter",
         "titre": "La moitié des réclamations naissent d'une phrase coupée.",
         "par_point": PAR_POINT, "points": [
             "Le laisser finir sa phrase. Toujours, même si vous avez compris.",
             "Reformuler : « Si je comprends bien, vous voulez… »",
             "Une question pour vérifier, pas dix pour l'interroger.",
             "Ne jamais répondre en regardant l'écran. On répond en regardant la personne.",
         ]},

        {"type": "duo", "chapitre": "Écouter", "par_point": 6.8,
         "titre": "Trois phrases à changer dès demain.", "paires": [
             ("Je ne sais pas.",
              "Je vérifie et je vous donne la réponse avant midi."),
             ("Ce n'est pas mon service.",
              "Je vous mets en relation avec la personne qui gère cela."),
             ("C'est le système, je n'y peux rien.",
              "Voici ce que je peux faire pour vous aujourd'hui."),
         ]},

        {"type": "chapitre", "numero": "2", "chapitre": "Information",
         "titre": "L'information juste", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Information",
         "titre": "Ce que vous annoncez engage la compagnie.",
         "par_point": PAR_POINT, "points": [
             "Un tarif annoncé engage Royal Air. Vérifier avant de le dire.",
             "Franchise bagages, horaires, escales : l'exact, jamais l'approximatif.",
             "Ne jamais confirmer une place qui n'est pas confirmée au système.",
             "Écrire ce qui est important et le remettre. La mémoire n'est pas une preuve.",
         ]},
        {"type": "regle", "chapitre": "Information", "duree": REGLE,
         "texte": "Une promesse tenue vaut dix promesses données.",
         "appui": "Mieux vaut annoncer un délai large et le tenir, "
                  "que promettre court et rappeler pour s'excuser."},

        {"type": "situation", "chapitre": "Irrégularités", "duree": SITUATION,
         "texte": "Le vol de 7 h pour Anjouan est reporté à demain. Le passager devant "
                  "vous devait être à un mariage ce soir. Il hausse le ton.",
         "question": "Vous répondez quoi, exactement ?"},
        {"type": "liste", "chapitre": "Irrégularités",
         "titre": "C'est là qu'on reconnaît une vraie compagnie.",
         "par_point": PAR_POINT, "points": [
             "Dire la vérité connue, même incomplète, plutôt que rien.",
             "Donner l'heure de la prochaine information — et la respecter.",
             "Ne jamais mettre la faute sur un collègue ou sur l'escale devant le passager.",
             "Le passager en colère n'est pas en colère contre vous. Ne le prenez pas pour vous.",
         ]},
        {"type": "duo", "chapitre": "Irrégularités", "par_point": 6.8,
         "titre": "Deux phrases qui décident de la suite.", "paires": [
             ("Le vol est annulé, je n'ai pas d'information.",
              "Le vol du 12 est annulé. Je vous rappelle avant 16 h avec le report."),
             ("Il fallait venir plus tôt.",
              "Voici ce qui reste possible aujourd'hui, et ce que je peux faire pour demain."),
         ]},

        {"type": "regle", "chapitre": "Irrégularités", "duree": REGLE,
         "texte": "Baisser la voix d'un ton.",
         "appui": "C'est la seule technique qui fonctionne à tous les coups : "
                  "l'autre baisse la sienne pour vous entendre."},

        {"type": "chapitre", "numero": "3", "chapitre": "Accompagner",
         "titre": "Les passagers qu'on accompagne", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Accompagner",
         "titre": "L'assistance se propose. Elle ne se mendie pas.",
         "par_point": PAR_POINT, "points": [
             "Personne âgée, femme enceinte, mobilité réduite : proposer sans attendre "
             "qu'on demande.",
             "Assistance PMR : elle se note à la réservation et s'annonce à l'escale. "
             "Pas le jour du vol.",
             "Enfant non accompagné : dossier complet vérifié au comptoir, pas à l'aéroport.",
             "Passager qui ne lit pas : lire pour lui, à voix basse, sans le mettre mal à l'aise.",
         ]},

        {"type": "situation", "chapitre": "Le comptoir", "duree": SITUATION,
         "texte": "Un homme demande si son frère est bien sur le vol de demain. "
                  "Il donne le nom, la date, il connaît tout le dossier.",
         "question": "Vous confirmez ?"},
        {"type": "liste", "chapitre": "Le comptoir",
         "titre": "Tout est visible depuis l'autre côté.",
         "par_point": PAR_POINT, "points": [
             "Tenue propre, badge visible : c'est la première preuve de sérieux.",
             "Comptoir dégagé. Pas de tasse, pas de téléphone personnel posé devant lui.",
             "Une conversation privée derrière le comptoir s'entend de l'autre côté.",
             "On ne mange pas devant un passager. On s'absente.",
         ]},
        {"type": "regle", "chapitre": "Le comptoir", "duree": 7.4,
         "texte": "Les données du passager ne sortent pas de l'agence.",
         "appui": "Numéro de téléphone, pièce d'identité, itinéraire, motif du voyage : "
                  "à personne. Ni à la famille, ni au téléphone, ni sur WhatsApp."},

        {"type": "chapitre", "numero": "4", "chapitre": "Les interdits",
         "titre": "Les cinq interdits", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Les interdits", "marqueur": "interdit",
         "titre": "Cinq choses qu'on ne fait jamais.",
         "par_point": PAR_POINT, "points": [
             "Confirmer une place ou un tarif qui ne l'est pas.",
             "Encaisser sans remettre immédiatement le justificatif.",
             "Parler du dossier d'un passager devant un autre passager.",
             "Répondre à une réclamation par une réclamation.",
             "Laisser repartir un passager mécontent sans aucune trace écrite.",
         ]},

        {"type": "chapitre", "numero": "5", "chapitre": "La trace",
         "titre": "Ce qui n'est pas écrit n'existe pas", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "La trace",
         "titre": "Une réclamation est une information gratuite.",
         "par_point": PAR_POINT, "points": [
             "Toute réclamation se note et remonte au Département Qualité le jour même.",
             "Signaler n'est jamais reproché. Ne pas signaler, si.",
             "Ce qui n'est pas écrit n'existe pas pour l'audit ANACM.",
             "Référence : QUA-PROC-002 — non-conformités et actions correctives.",
         ]},

        {"type": "cloture", "par_point": 3.7,
         "titre": "Cinq réflexes à garder",
         "points": [
             "Saluer le premier.",
             "Écouter jusqu'au bout.",
             "Ne dire que ce qui est vérifié.",
             "Donner un délai, et le tenir.",
             "Écrire ce qui compte.",
         ],
         "reference": "Ces cinq réflexes sont ceux que le Département Qualité vérifie "
                      "lors des visites d'agence."},

        {"type": "fin", "duree": 7.2, "lignes": PIED_FINAL},
    ],
}


# ═══════════════════════════════════════════════════════ FILM 2 — EN ESCALE
ESCALE = {
    "titre": "Film 2 — L'accueil des passagers en escale",
    "fichier": "RoyalAir-accueil-escale",
    "scenes": [
        {"type": "ouverture", "duree": 6.4,
         "titre": "L'accueil en escale",
         "sous_titre": "Moroni, Ouani, Mohéli : à l'escale, il n'y a plus d'écran "
                       "entre le passager et nous.",
         "mention": "Film de sensibilisation · Département Qualité"},

        {"type": "regle", "chapitre": "Pourquoi", "duree": 7.6,
         "texte": "À l'escale, la compagnie a un visage.",
         "appui": "C'est le vôtre. Le passager ne verra jamais le commandant de bord "
                  "ni le mécanicien. Il vous verra, vous, pendant deux heures."},

        {"type": "situation", "chapitre": "Avant le vol", "duree": SITUATION,
         "texte": "5 h 30 à Moroni. Le comptoir ouvre dans dix minutes. "
                  "Vingt personnes attendent déjà devant la porte.",
         "question": "Qu'est-ce qui doit être prêt maintenant ?"},
        {"type": "liste", "chapitre": "Avant le vol",
         "titre": "Le vol commence quand le comptoir ouvre.",
         "par_point": PAR_POINT, "points": [
             "Briefing station : nombre de passagers, PMR, enfants non accompagnés, "
             "bagages hors format.",
             "Tenue correcte, badge aéroportuaire porté et visible.",
             "Comptoir propre, affichage à jour, heure réelle affichée — pas l'heure d'hier.",
             "Connaître l'état du vol AVANT que le premier passager ne le demande.",
         ]},

        {"type": "chapitre", "numero": "1", "chapitre": "Enregistrement",
         "titre": "L'enregistrement", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Enregistrement",
         "titre": "Le document vient après la personne.",
         "par_point": PAR_POINT, "points": [
             "Saluer et regarder d'abord. Prendre la pièce d'identité ensuite.",
             "Nom, destination, numéro : à voix mesurée. Le comptoir voisin entend tout.",
             "Annoncer la franchise avant de poser le bagage sur la balance, pas après.",
             "Excédent : montrer le poids, expliquer le calcul, rester calme sur le tarif.",
         ]},

        {"type": "duo", "chapitre": "Enregistrement", "par_point": 6.8,
         "titre": "Deux phrases qui déclenchent tout.", "paires": [
             ("Votre bagage est trop lourd.",
              "Nous sommes à 3 kg au-dessus. Voici vos deux options."),
             ("C'est le règlement, c'est comme ça.",
              "Sur le LET 410, chaque kilo compte pour la sécurité du vol."),
         ]},

        {"type": "situation", "chapitre": "Sûreté", "duree": SITUATION,
         "texte": "Un collègue vous demande d'enregistrer le bagage de son cousin, "
                  "qui arrive juste après. Il vous dit : « je le connais ».",
         "question": "Vous faites quoi ?"},
        {"type": "liste", "chapitre": "Sûreté",
         "titre": "Ferme, jamais sec.",
         "par_point": PAR_POINT, "points": [
             "Identité passager–bagage : aucun bagage ne part sans son passager à bord.",
             "Les questions de sûreté se posent à chacun. Y compris à ceux qu'on connaît.",
             "Un refus poli reste un refus. La politesse n'est pas une ouverture à négocier.",
             "Une pression pour contourner une règle se signale — elle ne se gère pas seul.",
         ]},
        {"type": "regle", "chapitre": "Sûreté", "duree": 7.4,
         "texte": "Personne ne peut vous demander de sauter une règle de sûreté.",
         "appui": "Ni un passager, ni un collègue, ni un responsable, ni une connaissance. "
                  "Référence : GRD-PROC-001 — Sécurité en piste."},

        {"type": "situation", "chapitre": "Salle d'attente", "duree": SITUATION,
         "texte": "Le vol pour Mohéli devait partir à 11 h. Il est 12 h 20. "
                  "Personne n'a rien dit depuis une heure. La salle se lève.",
         "question": "Qu'est-ce qui a échoué ici ?"},
        {"type": "liste", "chapitre": "Salle d'attente",
         "titre": "Le silence est ce qui fâche, pas le retard.",
         "par_point": PAR_POINT, "points": [
             "Annonce claire, en français et en comorien, deux fois, sans crier.",
             "En cas de retard : une information toutes les vingt minutes, même sans nouveauté.",
             "« Nous n'avons pas encore d'information » est une information. Le silence, non.",
             "Ne jamais annoncer une heure qu'on n'est pas sûr de tenir.",
             "Ne jamais commenter une cause non confirmée. Une prise en charge annoncée "
             "est une prise en charge tenue.",
         ]},
        {"type": "duo", "chapitre": "Salle d'attente", "par_point": 6.8,
         "titre": "Deux phrases qui calment une salle.", "paires": [
             ("On ne sait pas, attendez.",
              "L'avion est encore à Ouani. Je reviens vers vous à 12 h 45, "
              "avec ou sans nouvelle."),
             ("Ce n'est pas nous, c'est la météo.",
              "Le vol est retardé pour raison météo. Voici ce qui est prévu pour vous."),
         ]},

        {"type": "regle", "chapitre": "Salle d'attente", "duree": REGLE,
         "texte": "Une salle informée attend. Une salle ignorée s'énerve.",
         "appui": "Et une seule voix pour informer : deux versions différentes "
                  "dans la même salle, c'est un incident qui commence."},

        {"type": "chapitre", "numero": "2", "chapitre": "Embarquement",
         "titre": "L'embarquement", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Embarquement",
         "titre": "Trente mètres de piste, et tout se voit.",
         "par_point": PAR_POINT, "points": [
             "Appeler d'abord les PMR, les familles avec enfants, les personnes âgées.",
             "Marches du LET 410 : une main tendue, pas un regard qui attend.",
             "Bagage cabine trop grand : repris en soute, étiqueté, expliqué — pas arraché.",
             "Compter, recompter, et signaler tout écart immédiatement.",
         ]},

        {"type": "chapitre", "numero": "3", "chapitre": "Accompagner",
         "titre": "Les passagers qu'on accompagne", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Accompagner",
         "titre": "On assiste d'abord. On régularise ensuite.",
         "par_point": PAR_POINT, "points": [
             "PMR annoncée ou non : l'assistance est due dans les deux cas.",
             "Enfant non accompagné : jamais seul, transmission de main à main, signature.",
             "Passager médical : ce qui a été accepté à la réservation doit être connu "
             "de l'escale.",
             "Accompagner jusqu'à l'avion, pas jusqu'à la porte de la salle.",
         ]},

        {"type": "chapitre", "numero": "4", "chapitre": "L'arrivée",
         "titre": "L'accueil ne s'arrête pas à la porte", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "L'arrivée",
         "titre": "Le dernier passager mérite le ton du premier.",
         "par_point": PAR_POINT, "points": [
             "Bagage manquant ou abîmé : constat rempli sur place, avec le passager.",
             "Ne jamais renvoyer quelqu'un sans un nom et un numéro à rappeler.",
             "Un passager qui repart sans réponse revient en réclamation écrite.",
             "Saluer à l'arrivée aussi. C'est la dernière image qu'il emporte.",
         ]},

        {"type": "chapitre", "numero": "5", "chapitre": "Les interdits",
         "titre": "Les cinq interdits", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "Les interdits", "marqueur": "interdit",
         "titre": "Cinq choses qu'on ne fait jamais.",
         "par_point": PAR_POINT, "points": [
             "Sauter une question de sûreté parce qu'on connaît le passager.",
             "Laisser partir un bagage sans son passager à bord.",
             "Annoncer une heure inventée pour faire taire la salle.",
             "Se disputer entre agents devant les passagers.",
             "Fermer le comptoir sans avoir traité le dernier cas.",
         ]},

        {"type": "chapitre", "numero": "6", "chapitre": "La trace",
         "titre": "Ce qui n'est pas écrit n'existe pas", "duree": CHAPITRE},
        {"type": "liste", "chapitre": "La trace",
         "titre": "L'audit lit les traces, pas les intentions.",
         "par_point": PAR_POINT, "points": [
             "Tout événement d'escale se note : heure, vol, passagers concernés.",
             "Ce qui touche la sécurité part au SGS, pas seulement au chef d'escale.",
             "Un signalement n'est jamais reproché. Une omission, si.",
             "Références : GOM · GRD-PROC-001 · QUA-PROC-002.",
         ]},

        {"type": "cloture", "par_point": 3.7,
         "titre": "Cinq réflexes à garder",
         "points": [
             "Informer avant qu'on demande.",
             "Expliquer plutôt qu'imposer.",
             "Assister d'abord.",
             "Ne jamais céder sur la sûreté.",
             "Écrire ce qui s'est passé.",
         ],
         "reference": "Ces cinq réflexes sont ceux que le Département Qualité vérifie "
                      "lors des audits de station (Moroni, Ouani, Mohéli)."},

        {"type": "fin", "duree": 7.2, "lignes": PIED_FINAL},
    ],
}
