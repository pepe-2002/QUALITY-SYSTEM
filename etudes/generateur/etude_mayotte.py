# -*- coding: utf-8 -*-
"""
Générateur de l'étude de sécurité RA-SGS-ETU-26-01 (desserte de Mayotte / FMCZ).

La cotation, l'indice OACI, le score et la tolérabilité sont CALCULÉS ici avec
exactement les mêmes règles que le module Risk Management du RA-QDMS
(app.js : riskCalc) — matrice OACI 5x5, Doc 9859.

Sortie : etudes/RA-SGS-ETU-26-01-desserte-mayotte.html
"""
import os, datetime

PROBA = {1: "Extrêmement improbable", 2: "Improbable", 3: "Occasionnel", 4: "Probable", 5: "Fréquent"}
GRAV  = {5: "Catastrophique", 4: "Dangereux", 3: "Majeur", 2: "Mineur", 1: "Négligeable"}
LETTRE = {5: "A", 4: "B", 3: "C", 2: "D", 1: "E"}

def risk_calc(p, g):
    score = p * g
    index = f"{p}{LETTRE[g]}"
    if score >= 15 or (p >= 4 and g >= 4):
        return score, index, "Intolérable", "red"
    if score >= 6:
        return score, index, "Tolérable", "orange"
    return score, index, "Acceptable", "green"

# ---------------------------------------------------------------- registre
# (ref, famille, danger, conséquences, pi, gi, mesures d'atténuation, pr, gr, responsable, échéance)
R = [
 # ---- Famille 1 : conformité réglementaire et accès au marché
 ("RM-01","REG","Exploitation d'un vol commercial vers un aérodrome de l'Union européenne (Mayotte est dans le champ Part-TCO) sans autorisation TCO EASA en vigueur",
  "Vol illégal, refus d'entrée dans l'espace aérien de l'UE, sanctions, investissement perdu, discrédit du dossier auprès de l'ANACM",
  3,4,"Désignation d'un point focal TCO ; analyse d'écarts par rapport aux Annexes OACI 1, 6, 8 et 19 ; dépôt du formulaire FO.TCO.00160 au moins 12 mois avant la date visée ; aucune mise en vente de sièges avant notification écrite de l'autorisation par l'EASA ; vérification que les spécifications techniques annexées couvrent bien D6-RAA et l'aérodrome FMCZ",
  1,4,"Responsable Qualité (point focal)","T0 + 2 mois (dépôt)"),
 ("RM-02","REG","Droits de trafic non attribués ou désignation du transporteur non notifiée à la partie française (accord aérien France–Comores du 22/08/2014 : les droits sont fixés en consultations bilatérales, pas par l'accord)",
  "Impossibilité juridique d'ouvrir la ligne ; report de plusieurs saisons ; coûts engagés à fonds perdus",
  4,3,"Saisine formelle de l'ANACM pour demander l'ouverture de consultations bilatérales ANACM / DGAC-DTA ; dossier de désignation (établissement principal et contrôle effectif aux Comores) ; demande de capacité cohérente avec la flotte (2 à 4 fréquences hebdomadaires) ; calendrier aligné sur les saisons IATA",
  2,3,"Direction générale + Point focal","T0 + 3 mois"),
 ("RM-03","REG","Autorisation d'exploitation et programme d'exploitation non délivrés par la DGAC française (transporteur extracommunautaire)",
  "Vols non autorisés, annulation du programme publié, remboursements, atteinte à la réputation commerciale",
  3,3,"Dépôt du programme d'exploitation saisonnier auprès de la DGAC/DTA avec l'ensemble des pièces (AOC, OpSpecs, TCO, assurance, contrat d'assistance en escale) ; interlocuteur désigné à la DGAC ; délais d'instruction intégrés au rétroplanning",
  2,2,"Point focal certification","T0 + 9 mois"),
 ("RM-04","REG","Présentation au dossier TCO d'un aéronef hors périmètre de l'AOC ANACM (cas de 5Y-SYF, immatriculé au Kenya, affrété) ou d'une location avec équipage non approuvée",
  "Refus ou restriction de l'autorisation TCO, retrait de l'aéronef des spécifications, interruption de la desserte",
  3,3,"N'inscrire au dossier TCO que les aéronefs figurant aux OpSpecs ANACM ; régulariser la location (dry lease + inscription à l'AOC, ou accord article 83 bis) ; revue trimestrielle de la cohérence flotte / AOC / TCO par le Département Qualité",
  1,3,"Responsable Qualité + Maintenance","T0 + 4 mois"),
 ("RM-05","REG","Couverture d'assurance non conforme au règlement (CE) 785/2004 (250 000 DTS par passager, 1 288 DTS bagages, 22 DTS/kg fret, et 18 M DTS de RC tiers pour un aéronef de 6 600 kg de MTOM)",
  "Refus de l'autorisation, exploitation illégale, exposition financière non couverte en cas d'accident",
  2,4,"Avenant à la police RC couvrant les montants réglementaires et les risques de guerre et assimilés ; dépôt du certificat d'assurance auprès de l'autorité de l'État membre concerné avant le premier vol ; contrôle annuel de validité par alerte d'échéance RA-QDMS",
  1,4,"Direction générale + Qualité","T0 + 8 mois"),
 ("RM-06","REG","Dégradation de la supervision de l'État de l'exploitant (ANACM) conduisant à une inscription des transporteurs comoriens sur la liste de sécurité de l'UE en cours d'exploitation (les Comores n'y figurent pas au règlement d'exécution (UE) 2026/1317 du 08/06/2026)",
  "Perte immédiate du droit d'exploiter vers l'UE, arrêt de la ligne, impact majeur sur l'image et les recettes",
  2,5,"Contribution active de Royal Air au plan d'actions correctives USOAP de l'ANACM ; préparation permanente à un audit EASA sur site ; suivi trimestriel des indicateurs de supervision ; clause de continuité dans le plan d'affaires (arrêt planifié sans rupture de trésorerie)",
  2,5,"Direction générale","Revue trimestrielle"),
 ("RM-07","REG","Fret ou courrier embarqué à destination de Mayotte sans désignation ACC3 (règlement d'exécution (UE) 2015/1998 : une désignation par couple transporteur / aéroport de départ)",
  "Refus du fret à l'arrivée, immobilisation, sanctions, perte de recettes fret",
  3,3,"Aucun fret ni courrier au lancement : bagages accompagnés uniquement ; si le fret est ouvert, validation UE de sûreté aérienne par un validateur agréé pour chaque escale de départ (HAH, AJN, NWA) ; procédure d'acceptation verrouillée dans le manuel de sûreté",
  1,3,"Responsable Sûreté","Avant toute ouverture fret"),
 ("RM-08","REG","Obligations européennes envers les passagers non intégrées pour les vols au départ de Mayotte (règlement (CE) 261/2004 — indemnisation, assistance ; règlement (CE) 1107/2006 — personnes handicapées et à mobilité réduite)",
  "Réclamations, sanctions administratives françaises, provisions non budgétées, contentieux",
  4,2,"Procédure de gestion des perturbations (retard, annulation, refus d'embarquement) ; affichage et information des passagers ; contrat d'assistance PMR avec l'assistant en escale ; provision financière et suivi mensuel des réclamations",
  2,2,"Service client + Qualité","T0 + 10 mois"),
 # ---- Famille 2 : opérations et navigation aérienne
 ("RM-09","OPS","Absence de service de contrôle d'approche à Mayotte : intégration et départ dans un espace non contrôlé fréquenté par des aéronefs de transport public lourds, sans radar, avec séparation procédurale (situation reconnue par le ministère chargé des transports, réponse du 25/06/2024 ; transfert d'espaces à l'ASECNA/Antananarivo à l'étude)",
  "Abordage ou quasi-abordage (AIRPROX) en vue de l'aérodrome, perte de séparation avec un ATR 72 ou un long-courrier",
  3,5,"Briefing de route obligatoire et carte d'arrivée spécifique FMCZ ; écoute permanente de la fréquence de la tour et auto-information en anglais et en français ; transpondeur mode S opérationnel imposé en no-go MEL ; vérification de l'emport d'un ACAS II conformément à l'Annexe 6 (aéronef de plus de 5 700 kg) ; phares d'atterrissage allumés sous 10 000 ft ; horaires choisis hors des pointes de trafic long-courrier ; entraînement spécifique « espace non contrôlé à fort trafic »",
  2,5,"Directeur des opérations + Chef pilote","T0 + 11 mois"),
 ("RM-10","OPS","Coordination transfrontalière des services de la circulation aérienne (FIR d'Antananarivo, approche de Moroni, tour de Dzaoudzi) : clairances contradictoires, absence de couverture VHF en route",
  "Pénétration non coordonnée d'espace, perte de communication, déroutement, écart de niveau",
  3,3,"Procédure de panne de communication écrite au MANEX partie C ; points de compte rendu obligatoires publiés sur la route ; double équipement VHF vérifié avant départ ; préavis de vol transmis aux organismes concernés ; retour d'expérience après chacun des dix premiers vols",
  2,3,"Chef pilote","T0 + 11 mois"),
 ("RM-11","OPS","Aérodrome à piste unique (16/34, environ 1 930 m) sans aérodrome de dégagement à Mayotte : toute fermeture (accident, travaux, incendie, aéronef en panne sur la piste) impose un déroutement vers les Comores ou Madagascar",
  "Déroutement avec carburant limité, atterrissage sur un terrain non préparé, passagers bloqués",
  3,3,"Politique carburant : dégagement systématique sur Ouani (64 NM) avec réserve finale, jamais de vol sans carburant de dégagement ; contrôle NOTAM au dispatch et point de décision en route défini avant le départ ; aucune réduction de carburant pour charge marchande",
  2,2,"Dispatch + Commandant de bord","Permanent"),
 ("RM-12","OPS","Approbation PBN (RNP APCH) absente des OpSpecs ANACM ou équipement GNSS non certifié pour les procédures d'approche publiées à FMCZ",
  "Impossibilité d'approcher en conditions instrumentales, remises de gaz, déroutements récurrents, régularité dégradée",
  3,3,"Demande d'extension des OpSpecs (PBN, approches RNP APCH) auprès de l'ANACM ; vérification de la certification de l'équipement et de la mise à jour de la base de données de navigation à chaque cycle AIRAC ; formation et contrôle en simulateur ; à défaut, restriction d'exploitation aux conditions de vol à vue de jour inscrite au programme",
  2,2,"Directeur des opérations","T0 + 8 mois"),
 ("RM-13","OPS","Convection tropicale sévère sur le canal du Mozambique (saison des pluies du 1er novembre au 30 avril) avec un LET 410 non pressurisé volant dans la couche, et détection météo embarquée limitée",
  "Pénétration orageuse, turbulence sévère, grêle, givrage, perte de contrôle, blessures à bord",
  4,4,"Vérification et maintien en condition opérationnelle d'un radar météorologique ou d'un détecteur d'orages ; limites météorologiques explicites au MANEX partie A ; briefing renforcé (Météo-France Mayotte et prévisions de zone) ; interdiction formelle de pénétrer une cellule orageuse, contournement par 20 NM minimum ; carburant supplémentaire de contournement ; priorité aux créneaux matinaux en saison des pluies",
  2,4,"Chef pilote + Dispatch","T0 + 10 mois"),
 ("RM-14","OPS","Saison cyclonique de novembre à avril : cyclone tropical affectant Mayotte (précédent : Chido, 14 décembre 2024, tour de contrôle détruite et trafic civil suspendu ; 8 systèmes passés à moins de 200 km des côtes en 46 ans)",
  "Aéronef endommagé ou immobilisé sur place, fermeture prolongée de l'aérodrome, interruption de la desserte, équipage bloqué",
  3,4,"Procédure cyclone : sur alerte orange, évacuation de l'aéronef vers un terrain sûr au plus tard 24 h avant l'échéance ; aucun stationnement de nuit à Dzaoudzi en période d'alerte ; suivi quotidien des bulletins en saison ; couverture d'assurance des dommages au sol ; plan de continuité commerciale et politique de réacheminement",
  2,3,"Directeur des opérations","Avant chaque saison"),
 ("RM-15","OPS","Survol maritime prolongé, jusqu'à 140 NM sans terrain utilisable en route (Moroni – Dzaoudzi), au-delà de la distance de plané, avec un bimoteur dont la capacité de montée sur un moteur est limitée",
  "Amerrissage forcé, noyade, recherches et sauvetage tardifs",
  2,5,"Équipements de survie conformes à l'Annexe 6 : gilets à portée immédiate de chaque occupant, radeaux, ELT et balise de survie, trousse de premiers secours ; briefing passagers spécifique amerrissage ; entraînement périodique de l'équipage (exercice d'amerrissage et d'évacuation) ; comptes rendus de position réguliers et suivi de vol ; coordination préalable avec le centre de coordination de sauvetage compétent",
  1,5,"Chef pilote + Sûreté/Sécurité","T0 + 10 mois"),
 ("RM-16","OPS","Pression sur la charge marchande : l'emport du carburant de dégagement et de contournement météo réduit la charge payante, avec tentation de dépassement de masse ou d'approximation du centrage",
  "Décollage en surcharge, centrage hors limites, perte de contrôle au décollage",
  3,5,"Tableau de charge marchande maximale par étape (HAH, NWA, AJN vers DZA) intégré au manuel d'exploitation ; pesée systématique des bagages et du fret, masses forfaitaires validées ; double contrôle dispatch et commandant de bord sur le devis de masse approuvé ; interdiction absolue de dépassement, adossée à la politique de culture juste ; audit trimestriel des devis de masse",
  1,5,"Dispatch + Commandant de bord","Permanent"),
 ("RM-17","OPS","Péril animalier sur un aérodrome littoral (oiseaux marins, chauves-souris frugivores aux heures crépusculaires)",
  "Ingestion, dommage à une hélice ou au pare-brise, arrêt décollage",
  3,3,"Consultation des consignes locales publiées et coordination avec l'exploitant d'aérodrome ; vigilance accrue aux heures crépusculaires ; compte rendu systématique de toute collision ou quasi-collision animalière ; adaptation des horaires si la fréquence le justifie",
  2,3,"Chef pilote","T0 + 11 mois"),
 ("RM-18","OPS","Assistance en escale sous-traitée à Dzaoudzi sans maîtrise du prestataire (chargement, calage, tractage, propreté de l'aire, absence de compétence sur LET 410)",
  "Dommage à l'aéronef au sol, erreur de chargement, retard, blessure de personnel",
  3,3,"Contrat d'assistance avec annexe technique spécifique LET 410 ; audit du prestataire inscrit au plan d'audits avant le premier vol ; formation type-spécifique et checklists arrivée/départ signées ; procédure de compte rendu de dommage au sol ; supervision par un agent Royal Air pendant les trois premiers mois",
  2,2,"Responsable Ground Handling + Qualité","T0 + 11 mois"),
 ("RM-19","OPS","Avitaillement à Dzaoudzi : disponibilité, contrat, qualité du carburant, procédure locale méconnue",
  "Immobilisation faute de carburant, contamination du circuit, panne moteur",
  2,4,"Contrat d'avitaillement signé avant l'ouverture ; contrôle qualité à chaque plein (bulletin de livraison, contrôle d'eau) ; procédure d'avitaillement au MANEX ; politique d'emport aller-retour depuis les Comores lorsque la charge marchande le permet",
  1,4,"Maintenance + Opérations","T0 + 10 mois"),
 ("RM-20","OPS","Aéronef immobilisé à Dzaoudzi sans organisme de maintenance agréé sur LET 410 sur place, pièces et outillage à acheminer, formalités douanières",
  "Immobilisation prolongée hors base, annulations en cascade, coûts d'assistance, pression à voler en état dégradé",
  3,2,"Accord d'assistance technique avec un organisme de la région ; lot de pièces critiques embarqué ; procédure MEL et CDL appliquée sans dérogation, vol de convoyage soumis à l'accord de la Maintenance et de l'ANACM ; contact douane identifié pour l'importation temporaire de pièces",
  2,2,"Responsable Maintenance","T0 + 10 mois"),
 ("RM-21","OPS","Inspection au sol de type SAFA par l'autorité française à Dzaoudzi (contrôle des transporteurs de pays tiers)",
  "Constats de catégorie 2 ou 3, restriction ou immobilisation de l'aéronef, signalement à l'EASA et à la Commission, risque d'effet sur le statut TCO",
  4,3,"Programme interne de pré-inspection reprenant l'ensemble des points contrôlés, appliqué avant chaque départ vers Mayotte ; documentation de bord complète, à jour et disponible en anglais ; état extérieur et équipements de sécurité vérifiés (pneus, fuites, marquages, gilets, extincteurs) ; formation des équipages à l'inspection ; traitement documenté de tout constat sous 30 jours",
  2,3,"Responsable Qualité","Avant le 1er vol, puis permanent"),
 ("RM-22","OPS","Fatigue des équipages : effectif limité, rotations enchaînées sur des étapes courtes, aléas météo et retards en fin de journée",
  "Erreur de pilotage, décision dégradée, dépassement des limites de temps de vol",
  3,4,"Schéma de limitation des temps de vol approuvé et vérifié au dispatch ; équipage supplémentaire qualifié recruté avant l'ouverture ; réserve planifiée sur les jours d'exploitation ; déclaration de fatigue sans conséquence disciplinaire ; suivi mensuel des dépassements par la Qualité",
  2,4,"Directeur des opérations + Qualité","T0 + 9 mois"),
 ("RM-23","OPS","Environnement documentaire et linguistique français : phraséologie bilingue, cartes et NOTAM français, procédures locales publiées à l'AIP",
  "Mauvaise compréhension d'une clairance, non-respect d'une consigne locale, événement de sécurité, écart en inspection",
  3,3,"Vérification du niveau 4 OACI en français et en anglais pour les équipages affectés ; abonnement à la documentation aéronautique française et intégration au dossier de vol ; formation « opérations vers Mayotte » avec étude de la section AD 2 FMCZ, notamment les règlements de circulation locaux ; les premiers vols effectués avec un commandant de bord déjà expérimenté sur le terrain",
  1,3,"Chef pilote + Formation","T0 + 11 mois"),
 # ---- Famille 3 : sûreté et frontière
 ("RM-24","SUR","Fraude documentaire à l'embarquement : Mayotte applique un régime d'entrée propre et les titres valables ailleurs ne le sont pas nécessairement ; le transporteur encourt une amende de 10 000 € par passager débarqué sans document requis (CESEDA, art. L. 821-6) et le réacheminement à sa charge",
  "Amendes cumulées, frais de réacheminement et d'hébergement, passagers non admis, relation dégradée avec la police aux frontières",
  4,3,"Procédure de contrôle documentaire à double vérification (enregistrement puis porte) ; liste des documents acceptés établie avec la police aux frontières et affichée ; formation des agents à la détection de la fraude avec équipement adapté ; refus d'embarquement documenté et tracé ; information des passagers à la réservation ; provision budgétaire et suivi mensuel des cas",
  2,3,"Responsable Sûreté + Escale","T0 + 10 mois"),
 ("RM-25","SUR","Immigration irrégulière organisée : tentative de corruption du personnel, passager clandestin en soute ou dans les compartiments, substitution de passagers",
  "Poursuites pénales, retrait de l'autorisation, immobilisation de l'aéronef, atteinte grave à l'image",
  3,4,"Contrôle d'accès à l'aéronef et fouille de sûreté avant chaque départ, consignée sur checklist ; scellés sur les soutes ; politique anti-corruption signée, dispositif d'alerte interne et sanctions ; rotation des équipes d'escale ; signalement immédiat à l'ANACM et à la police aux frontières",
  2,4,"Responsable Sûreté","T0 + 10 mois"),
 ("RM-26","SUR","Mesures de sûreté à l'origine (escales comoriennes) non reconnues équivalentes aux exigences européennes",
  "Contrôles renforcés à l'arrivée, retards, restrictions d'exploitation, refus de correspondance",
  3,3,"Mise à niveau du programme de sûreté de la compagnie sur la base de l'Annexe 17 et du programme national ; coordination avec l'ANACM et les exploitants d'aérodrome sur l'inspection filtrage des passagers et des bagages ; audit interne de sûreté avant l'ouverture ; dossier tenu prêt pour une éventuelle validation européenne",
  2,3,"Responsable Sûreté","T0 + 9 mois"),
 ("RM-27","SUR","Marchandises dangereuses non déclarées dans les bagages ou le fret informel (batteries au lithium, bonbonnes, carburant, produits chimiques) — pratique fréquente sur les liaisons régionales",
  "Incendie en soute ou en cabine, perte de l'aéronef",
  4,4,"Politique « aucune marchandise dangereuse acceptée » au lancement ; formation marchandises dangereuses de tous les agents d'acceptation et des équipages ; affichage réglementaire et question posée à chaque enregistrement ; inspection visuelle de tout bagage hors gabarit, refus en cas de doute ; checklist de chargement signée ; compte rendu obligatoire de toute découverte",
  2,4,"Responsable Sûreté + Ground Handling","T0 + 9 mois"),
 ("RM-28","SUR","Sûreté de l'aéronef en escale ou en stationnement de nuit hors base",
  "Intrusion, sabotage, vol d'équipements, découverte d'objet suspect au départ",
  2,3,"Pas de stationnement de nuit à Dzaoudzi au lancement ; si nécessaire, gardiennage contractuel et fouille de sûreté complète avant le premier vol du jour ; portes et trappes verrouillées, scellés vérifiés",
  1,3,"Responsable Sûreté","T0 + 11 mois"),
 # ---- Famille 4 : économique, politique, réputation
 ("RM-29","ECO","Concurrence d'un opérateur établi sur l'axe (Ewa Air, filiale du groupe Air Austral, exploitant des ATR 72-600 depuis Dzaoudzi) et marché de taille limitée",
  "Remplissage insuffisant, recettes inférieures au point mort, retrait de la ligne après investissement",
  4,2,"Étude de marché préalable et seuil de remplissage d'arrêt défini par écrit ; positionnement horaire complémentaire plutôt que frontal ; ouverture progressive à deux fréquences ; recherche d'accords interlignes ; revue commerciale mensuelle avec décision de poursuite ou d'arrêt",
  3,2,"Direction générale","Revue mensuelle"),
 ("RM-30","ECO","Sous-estimation des coûts et des délais de mise en conformité (TCO, sûreté, assurance, documentation, formation) — un dossier complet demande de l'ordre de 12 à 18 mois",
  "Trésorerie sous tension, dossier interrompu en cours d'instruction, crédibilité entamée auprès des autorités",
  4,3,"Budget dédié et échéancier validés par la Direction avant le lancement du dossier ; jalons de décision à chaque phase ; aucun engagement commercial ni recrutement irréversible avant notification de l'autorisation TCO ; suivi budgétaire mensuel",
  2,3,"Direction générale","Revue mensuelle"),
 ("RM-31","ECO","Contexte politique : différend de souveraineté entre l'Union des Comores et la France sur Mayotte, décisions unilatérales de suspension de liaisons (précédent des vols d'Air Austral et d'Ewa Air suspendus aux Comores), tensions liées aux reconduites à la frontière",
  "Suspension brutale de la ligne, aéronef et équipage immobilisés, recettes perdues, exposition médiatique",
  3,4,"Veille diplomatique et institutionnelle avec l'ANACM et le ministère chargé des transports ; clauses de suspension dans les contrats d'escale et de distribution ; flexibilité de la flotte permettant un redéploiement immédiat sur le réseau intérieur ; plan de communication préparé ; aucun investissement fixe dédié à la ligne",
  3,3,"Direction générale","Revue trimestrielle"),
 ("RM-32","ECO","Crise sanitaire ou épidémique dans l'archipel (épisodes de choléra récents) entraînant des mesures sanitaires aux frontières",
  "Suspension de la desserte, mesures de désinfection, contrôles renforcés, baisse de la demande",
  3,2,"Procédures sanitaires conformes à l'Annexe 9 et au Règlement sanitaire international ; désinsectisation si exigée ; information des passagers ; plan de continuité et clause de force majeure dans les contrats",
  2,2,"Qualité + Opérations","Revue trimestrielle"),
 ("RM-33","ECO","Événement de sécurité majeur sur la nouvelle ligne, dans un environnement à forte visibilité médiatique française et européenne",
  "Enquête de sécurité, suspension de l'autorisation TCO, effet direct sur l'AOC et sur la supervision de l'État, perte de confiance durable",
  2,5,"Plan d'intervention d'urgence testé par un exercice avant l'ouverture de la ligne ; porte-parole désigné et messages préparés ; couverture d'assurance vérifiée ; procédure de coordination avec l'ANACM et l'autorité d'enquête conformément à l'Annexe 13 ; assistance aux familles",
  1,5,"Direction générale + SGS","Exercice avant ouverture"),
]

FAMILLES = {
 "REG": ("1. Conformité réglementaire et accès au marché", "Droit d'exploiter : autorisation européenne, droits de trafic, assurance, sûreté du fret, droits des passagers."),
 "OPS": ("2. Opérations aériennes et navigation", "Sécurité du vol : espace aérien, aérodrome, météorologie, survol maritime, performances, escale et maintenance."),
 "SUR": ("3. Sûreté de l'aviation civile et contrôle aux frontières", "Sûreté de l'aéronef, contrôle documentaire des passagers, marchandises dangereuses."),
 "ECO": ("4. Économie, contexte politique et réputation", "Viabilité de la ligne, environnement politique et sanitaire, conséquences d'un événement majeur."),
}

# ---------------------------------------------------------------- mise en page
CSS = """
:root{--navy:#0A2342;--blue:#0056D2;--acc:#2f7bff;--ink:#14213d;--mut:#5b6b82;--line:#d8e0ec;
      --green:#1f8a4c;--orange:#d97706;--red:#c0261f;--bg:#fff;}
*{box-sizing:border-box}
body{margin:0;background:#eef2f7;color:var(--ink);
     font-family:"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:13px;line-height:1.55}
.page{max-width:1000px;margin:0 auto;background:var(--bg);padding:0 0 60px}
header.bandeau{display:flex;align-items:center;gap:16px;padding:14px 28px;border-bottom:4px solid var(--blue);
     background:linear-gradient(90deg,#0A2342 0%,#123a6b 100%);color:#fff}
header.bandeau .txt .n{font-size:1.35rem;font-weight:800;letter-spacing:.11em}
header.bandeau .txt .s{font-size:.72rem;letter-spacing:.06em;opacity:.85;text-transform:uppercase}
header.bandeau .ref{margin-left:auto;text-align:right;font-size:.72rem;opacity:.9;line-height:1.5}
.corps{padding:26px 34px}
h1{font-size:1.5rem;margin:.2em 0 .1em;color:var(--navy);line-height:1.25}
h1+.st{color:var(--mut);font-size:.9rem;margin-bottom:18px}
h2{font-size:1.05rem;color:var(--navy);margin:30px 0 8px;padding-bottom:5px;border-bottom:2px solid var(--line)}
h3{font-size:.93rem;color:var(--blue);margin:18px 0 6px}
p{margin:.5em 0}
ul,ol{margin:.4em 0 .6em 1.1em;padding:0}li{margin:.22em 0}
table{width:100%;border-collapse:collapse;margin:10px 0;font-size:.8rem}
th,td{border:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}
th{background:#f2f6fb;color:var(--navy);font-weight:700}
td.c,th.c{text-align:center}
.ident{width:100%;font-size:.78rem;margin:0 0 14px}
.ident td:nth-child(odd){background:#f7fafd;font-weight:600;width:15%;color:var(--navy)}
.badge{display:inline-block;padding:2px 7px;border-radius:10px;color:#fff;font-weight:700;font-size:.72rem;white-space:nowrap}
.green{background:var(--green)}.orange{background:var(--orange)}.red{background:var(--red)}
.enc{border-left:4px solid var(--blue);background:#f4f8ff;padding:10px 14px;margin:12px 0;border-radius:0 6px 6px 0}
.enc.alerte{border-color:var(--red);background:#fdf3f2}
.enc.ok{border-color:var(--green);background:#f2faf5}
.enc .t{font-weight:700;color:var(--navy);margin-bottom:3px}
.mx td{text-align:center;font-weight:700;color:#fff;padding:9px 4px}
.mx th{text-align:center;font-size:.72rem}
.src{font-size:.76rem;color:var(--mut)}
.src li{margin:.3em 0;word-break:break-word}
.sign{display:flex;gap:12px;margin-top:18px;flex-wrap:wrap}
.sign div{flex:1;min-width:170px;border:1px solid var(--line);border-radius:6px;padding:8px 10px;font-size:.76rem}
.sign .r{color:var(--mut);text-transform:uppercase;font-size:.68rem;letter-spacing:.05em}
.sign .v{font-weight:700;margin:3px 0 20px}
footer{padding:14px 34px;border-top:2px solid var(--line);color:var(--mut);font-size:.74rem;
       display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
small.note{color:var(--mut)}
@media print{
  body{background:#fff;font-size:10.5pt}
  .page{max-width:none;padding:0}
  header.bandeau{padding:8px 12px}
  h2{page-break-after:avoid}table{page-break-inside:auto}tr{page-break-inside:avoid}
  @page{size:A4;margin:12mm 10mm 14mm}
}
@media(max-width:640px){.corps{padding:16px}table{font-size:.72rem}}
"""

LOGO = """<svg width="46" height="46" viewBox="0 0 64 64" aria-hidden="true">
  <rect width="64" height="64" rx="14" fill="#0A2342" stroke="#2f7bff" stroke-width="2"/>
  <path d="M12 44 L32 14 L52 44 L44 44 L32 26 L20 44 Z" fill="#2f7bff"/>
  <path d="M24 44 L32 32 L40 44 Z" fill="#fff"/>
  <rect x="14" y="48" width="36" height="3" rx="1.5" fill="#0056D2"/></svg>"""

REF   = "RA-SGS-ETU-26-01"
DATE  = "11 septembre 2026"
TITRE = "Étude de sécurité — Ouverture d'une desserte de Mayotte (FMCZ / DZA)"

def entete():
    return f"""<header class="bandeau">{LOGO}
  <div class="txt"><div class="n">ROYAL AIR</div>
    <div class="s">Union des Comores &middot; Département Qualité &amp; Système de gestion de la sécurité</div></div>
  <div class="ref">{REF}<br>Éd. 1 / Rév. 0 — {DATE}<br>Interne &middot; diffusion restreinte</div>
</header>"""

def bloc_identification():
    return f"""<table class="ident">
<tr><td>Référence</td><td>{REF}</td><td>Édition / Révision</td><td>Éd. 1 / Rév. 0</td></tr>
<tr><td>Titre</td><td colspan="3">{TITRE}</td></tr>
<tr><td>Objet</td><td colspan="3">Évaluation des risques préalable à la décision d'ouvrir une liaison régulière entre les Comores (HAH, NWA, AJN) et Mayotte (FMCZ), conformément au Doc 9859 de l'OACI et à la procédure SGS-PROC de Royal Air</td></tr>
<tr><td>Exploitant</td><td>Royal Air — AOC délivré par l'ANACM</td><td>Aéronef visé</td><td>LET 410 UVP-E20 (D6-RAA), 19 sièges, MTOM 6&nbsp;600&nbsp;kg</td></tr>
<tr><td>Rédacteur</td><td>Responsable Qualité, point focal certification</td><td>Date</td><td>{DATE}</td></tr>
<tr><td>Vérification</td><td>Directeur des opérations / Responsable SGS</td><td>Approbation</td><td>Dirigeant responsable</td></tr>
<tr><td>Statut</td><td>Projet soumis à approbation (DOC-PROC-001)</td><td>Prochaine revue</td><td>À la première des échéances : décision de la Direction ou 11 mars 2027</td></tr>
<tr><td>Diffusion</td><td colspan="3">Direction générale &middot; Opérations &middot; Maintenance &middot; Sûreté &middot; Escale &middot; ANACM (sur demande) &middot; DGAC et AESA (à l'appui du dossier d'autorisation)</td></tr>
</table>"""

def table_registre():
    out = []
    for code, (titre, sous) in FAMILLES.items():
        lignes = [r for r in R if r[1] == code]
        out.append(f"<h3>{titre}</h3><p class='src'>{sous}</p>")
        out.append("<table><thead><tr><th style='width:6%'>Réf.</th><th style='width:22%'>Danger identifié</th>"
                   "<th style='width:17%'>Conséquences redoutées</th><th class='c' style='width:9%'>Risque initial</th>"
                   "<th style='width:28%'>Mesures d'atténuation</th><th class='c' style='width:9%'>Risque résiduel</th>"
                   "<th style='width:9%'>Pilote / échéance</th></tr></thead><tbody>")
        for ref, _f, danger, cons, pi, gi, mit, pr, gr, resp, ech in lignes:
            si, ii, ti, ci = risk_calc(pi, gi)
            sr, ir, tr, cr = risk_calc(pr, gr)
            out.append(
                f"<tr><td><strong>{ref}</strong></td><td>{danger}</td><td>{cons}</td>"
                f"<td class='c'><span class='badge {ci}'>{ii}</span><br><small>P{pi}×G{gi}={si}</small><br><small>{ti}</small></td>"
                f"<td>{mit}</td>"
                f"<td class='c'><span class='badge {cr}'>{ir}</span><br><small>P{pr}×G{gr}={sr}</small><br><small>{tr}</small></td>"
                f"<td><small>{resp}<br>{ech}</small></td></tr>")
        out.append("</tbody></table>")
    return "\n".join(out)

def matrice(initial=True):
    cases = {}
    for ref, _f, _d, _c, pi, gi, _m, pr, gr, _r, _e in R:
        p, g = (pi, gi) if initial else (pr, gr)
        cases.setdefault((p, g), []).append(ref)
    couleur = {"green": "#1f8a4c", "orange": "#d97706", "red": "#c0261f"}
    h = ["<table class='mx'><thead><tr><th>P \\ G</th>"]
    for g in (5, 4, 3, 2, 1):
        h.append(f"<th>{g} — {GRAV[g]}</th>")
    h.append("</tr></thead><tbody>")
    for p in (5, 4, 3, 2, 1):
        h.append(f"<tr><th>{p} — {PROBA[p]}</th>")
        for g in (5, 4, 3, 2, 1):
            _s, idx, tol, cls = risk_calc(p, g)
            refs = cases.get((p, g), [])
            contenu = f"{idx}<br><small style='font-weight:400'>{'&nbsp;'.join(refs) if refs else '—'}</small>"
            h.append(f"<td style='background:{couleur[cls]}' title='{tol}'>{contenu}</td>")
        h.append("</tr>")
    h.append("</tbody></table>")
    return "".join(h)

def compte(initial=True):
    c = {"Acceptable": 0, "Tolérable": 0, "Intolérable": 0}
    for ref, _f, _d, _co, pi, gi, _m, pr, gr, _r, _e in R:
        p, g = (pi, gi) if initial else (pr, gr)
        c[risk_calc(p, g)[2]] += 1
    return c

# ---------------------------------------------------------------- corps
def corps():
    ci, cr = compte(True), compte(False)
    top_i = [r[0] for r in R if risk_calc(r[4], r[5])[2] == "Intolérable"]
    res_tol = sorted([r for r in R if risk_calc(r[7], r[8])[2] == "Tolérable"],
                     key=lambda r: -(r[7] * r[8]))[:3]
    res_tol = [r[0] for r in res_tol]
    return f"""
<h1>{TITRE}</h1>
<div class="st">Étude de sécurité préalable à l'ouverture de ligne — matrice OACI 5×5 (Doc 9859, 4<sup>e</sup> édition) —
{len(R)} dangers analysés</div>

{bloc_identification()}

<div class="enc"><div class="t">Synthèse pour la Direction</div>
La desserte de Mayotte est <strong>juridiquement accessible</strong> à Royal Air : les Comores ne figurent
ni à l'annexe A ni à l'annexe B de la liste de sécurité de l'Union européenne en vigueur (règlement
d'exécution (UE) 2026/1317 du 8 juin 2026), et un accord de services aériens lie la France et l'Union des
Comores depuis le 22 août 2014. Elle n'est cependant <strong>pas ouverte en l'état</strong> : Mayotte est un
territoire de l'Union européenne au sens du règlement (UE) 452/2014, ce qui impose une autorisation
<em>Part-TCO</em> délivrée par l'AESA avant tout vol commercial, en plus des droits de trafic et de
l'autorisation d'exploitation française.<br><br>
Sur {len(R)} dangers analysés, <strong>{ci['Intolérable']} présentent un risque initial intolérable</strong>
({', '.join(top_i)}) et {ci['Tolérable']} un risque tolérable. Après application des mesures d'atténuation
proposées, <strong>aucun risque résiduel intolérable ne subsiste</strong> : {cr['Acceptable']} risques
deviennent acceptables et {cr['Tolérable']} restent tolérables sous surveillance,
les plus élevés étant {', '.join(res_tol)}. L'ouverture est donc <strong>envisageable sous conditions</strong>, avec un délai
réaliste de 12 à 18 mois et six conditions bloquantes détaillées au § 8.</div>

<h2>1. Objet, périmètre et limites de l'étude</h2>
<p><strong>Objet.</strong> Identifier, coter et traiter les dangers associés à l'ouverture d'une liaison
régulière de transport public entre les escales comoriennes et l'aéroport de Mayotte, afin d'éclairer la
décision de la Direction générale et de constituer la pièce « analyse de risques » du dossier à présenter
à l'ANACM, à l'AESA (Part-TCO) et à la DGAC française.</p>
<p><strong>Périmètre.</strong> Exploitation en transport public de passagers, en LET 410 UVP-E20, au départ
de Moroni (HAH / FMCH), Mohéli (NWA / FMCV) et Anjouan (AJN / FMCI) vers Dzaoudzi-Pamandzi (DZA / FMCZ)
et retour, de jour, à raison de deux à quatre fréquences hebdomadaires en phase de lancement.</p>
<p><strong>Limites.</strong> L'étude porte sur la sécurité des vols, la sûreté, la conformité réglementaire
et les risques d'entreprise directement liés à cette ligne. Elle ne remplace ni l'étude de marché, ni le
dossier de certification lui-même, ni l'étude d'aérodrome de l'exploitant de FMCZ. Deux sources primaires
n'ont pas pu être consultées pendant la préparation de l'étude (serveurs indisponibles) : la section
<strong>AD 2 FMCZ de l'AIP France</strong>, en particulier le paragraphe <strong>AD 2.20 « Règlements de
circulation locaux »</strong>, et la fiche d'entrée à Mayotte du transporteur de référence. Les données
d'aérodrome utilisées proviennent donc de sources secondaires et sont signalées comme
<em>à confirmer sur l'AIP en vigueur</em> ; la vérification est inscrite au plan d'actions (§ 9, action A7)
et l'annexe B en donne la liste précise.</p>

<h2>2. Documents et textes de référence</h2>
<table>
<thead><tr><th style="width:32%">Référence</th><th>Portée pour la présente étude</th></tr></thead>
<tbody>
<tr><td>Règlement (UE) n° 452/2014 (Part-TCO) et Part-ART</td><td>Autorisation de sécurité exigée de tout exploitant de pays tiers assurant du transport aérien commercial vers l'Union ; Mayotte est expressément citée par l'AESA parmi les territoires couverts</td></tr>
<tr><td>Règlement d'exécution (UE) 2026/1317 du 8 juin 2026 (liste de sécurité de l'UE)</td><td>Les Comores ne figurent ni à l'annexe A, ni à l'annexe B — aucune interdiction ni restriction applicable à Royal Air à la date de l'étude</td></tr>
<tr><td>Accord France – Union des Comores relatif aux services de transport aérien, signé à Moroni le 22 août 2014</td><td>Cadre bilatéral ; les droits de trafic ne sont pas fixés par l'accord mais en consultations entre autorités aéronautiques</td></tr>
<tr><td>Règlement (CE) n° 785/2004</td><td>Montants minimaux d'assurance et obligation de preuve auprès de l'État membre de destination</td></tr>
<tr><td>Règlement d'exécution (UE) 2015/1998 (ACC3)</td><td>Sûreté du fret et du courrier à destination de l'Union, désignation par couple transporteur / aéroport de départ</td></tr>
<tr><td>Règlements (CE) n° 261/2004 et n° 1107/2006</td><td>Droits des passagers et assistance aux personnes handicapées et à mobilité réduite, applicables aux vols au départ de Mayotte</td></tr>
<tr><td>CESEDA, art. L. 821-6 et suivants</td><td>Amende de 10 000 € par passager débarqué sans document de voyage requis, et obligation de réacheminement</td></tr>
<tr><td>Annexes OACI 6 (partie I), 9, 13, 17, 19 et Doc 9859 (SGS)</td><td>Exigences d'exploitation, facilitation, enquêtes, sûreté, gestion de la sécurité et méthode d'évaluation des risques</td></tr>
<tr><td>AIP France, section AD 2 FMCZ (dont § AD 2.20) et NOTAM en vigueur</td><td>Caractéristiques de l'aérodrome, espace aérien, procédures et règlements de circulation locaux — <em>à extraire et annexer</em></td></tr>
<tr><td>Documentation interne : MANEX A/B/C/D, MEL, manuel de sûreté, manuel SGS, DOC-PROC-001, SGS-PROC, registre des risques RA-QDMS</td><td>Cadre d'intégration des mesures d'atténuation retenues</td></tr>
</tbody></table>

<h2>3. Description de l'exploitation projetée</h2>
<h3>3.1 Routes et distances</h3>
<table>
<thead><tr><th>Étape</th><th class="c">Distance orthodromique</th><th class="c">Route vraie</th><th class="c">Temps de vol estimé (160 kt sol)</th><th>Observations</th></tr></thead>
<tbody>
<tr><td>Moroni (FMCH) → Dzaoudzi (FMCZ)</td><td class="c">260 km / 140 NM</td><td class="c">123°</td><td class="c">≈ 53 min</td><td>Survol maritime intégral, aucun terrain utilisable en route</td></tr>
<tr><td>Mohéli (FMCV) → Dzaoudzi (FMCZ)</td><td class="c">174 km / 94 NM</td><td class="c">109°</td><td class="c">≈ 35 min</td><td>Survol maritime, dégagement possible sur Anjouan</td></tr>
<tr><td>Anjouan / Ouani (FMCI) → Dzaoudzi (FMCZ)</td><td class="c">119 km / 64 NM</td><td class="c">129°</td><td class="c">≈ 24 min</td><td>Étape la plus courte ; terrain de dégagement naturel de la ligne</td></tr>
</tbody></table>
<p class="src">Distances calculées par le générateur de la présente étude à partir des coordonnées publiées des
aérodromes (formule orthodromique, rayon terrestre moyen 6&nbsp;371 km) ; à confirmer sur la documentation de route.</p>
<h3>3.2 Aéronef et hypothèses d'exploitation</h3>
<ul>
<li>LET 410 UVP-E20, immatriculé D6-RAA, 19 sièges, masse maximale au décollage 6&nbsp;600 kg, non pressurisé,
exploité de jour, en règles de vol aux instruments dès que l'équipement et les approbations le permettent.</li>
<li>Deux à quatre fréquences hebdomadaires en phase de lancement, sans stationnement de nuit à Dzaoudzi.</li>
<li>Bagages accompagnés uniquement ; ni fret ni courrier tant que la désignation ACC3 n'est pas obtenue.</li>
<li>Assistance en escale sous-traitée à Dzaoudzi ; avitaillement sous contrat ; maintenance en base aux Comores.</li>
</ul>

<h2>4. Méthode d'évaluation</h2>
<p>La cotation applique la matrice OACI 5×5 du Doc 9859 telle qu'elle est paramétrée dans le module
« Risk Management » du RA-QDMS : probabilité de 1 (extrêmement improbable) à 5 (fréquent), gravité de 1
(négligeable) à 5 (catastrophique), indice composé du chiffre de probabilité et de la lettre de gravité
(5 = A catastrophique … 1 = E négligeable). Les valeurs de la présente étude sont calculées par programme,
avec les règles de tolérabilité en vigueur dans le système :</p>
<ul>
<li><span class="badge red">Intolérable</span> score ≥ 15, ou probabilité ≥ 4 associée à une gravité ≥ 4 :
exploitation interdite en l'état, atténuation obligatoire avant toute mise en œuvre ;</li>
<li><span class="badge orange">Tolérable</span> score compris entre 6 et 14 : acceptable sous réserve des
mesures d'atténuation, avec surveillance et revue périodique ;</li>
<li><span class="badge green">Acceptable</span> score ≤ 5 : acceptable en l'état, sous surveillance ordinaire.</li>
</ul>
<p>Chaque danger est coté avant atténuation (risque initial), puis après application des mesures
proposées (risque résiduel). Un risque résiduel supérieur au risque initial constituerait une erreur
d'évaluation ; le contrôle est automatique dans le RA-QDMS.</p>

<h2>5. Analyse du contexte</h2>

<h3>5.1 Cadre juridique d'accès — ce qui conditionne le droit de voler</h3>
<p>Mayotte est un département français et une région ultrapériphérique de l'Union européenne. Il en
résulte quatre obligations cumulatives, dont aucune ne se substitue aux autres :</p>
<ol>
<li><strong>Autorisation Part-TCO de l'AESA.</strong> Tout exploitant de pays tiers effectuant du transport
aérien commercial à destination du territoire de l'Union doit détenir une autorisation unique délivrée
par l'AESA ; Mayotte figure explicitement dans la liste des territoires couverts publiée par l'Agence.
La demande se fait par le formulaire FO.TCO.00160 via le portail de l'Agence ; l'accusé de réception
intervient sous 30 jours et l'évaluation, proportionnée au risque, peut se limiter à un examen
documentaire ou comporter une réunion technique, voire un <strong>audit sur site au siège de la
compagnie</strong>. L'autorisation est assortie de spécifications techniques précisant le périmètre
autorisé (aéronefs et aérodromes) et donne lieu à une surveillance continue.</li>
<li><strong>Droits de trafic.</strong> L'accord aérien franco-comorien du 22 août 2014 fixe le cadre, mais
les droits eux-mêmes sont attribués en consultations bilatérales entre l'ANACM et la DGAC. Le précédent
est établi : les consultations de 2014 ont pérennisé les liaisons Dzaoudzi–Moroni et Dzaoudzi–Anjouan.
Royal Air doit être désignée par l'ANACM et cette désignation notifiée à la partie française.</li>
<li><strong>Autorisation d'exploitation française</strong> et approbation du programme d'exploitation par
la DGAC, sur présentation de l'AOC, des OpSpecs, de l'autorisation TCO et de la preuve d'assurance.</li>
<li><strong>Assurance conforme au règlement (CE) 785/2004</strong> : 250 000 DTS par passager,
1 288 DTS par passager pour les bagages, 22 DTS par kilogramme pour le fret, et, pour un aéronef de
6 600 kg de masse maximale (catégorie « moins de 12 000 kg »), <strong>18 millions de DTS</strong> de
responsabilité civile envers les tiers. Le certificat doit être déposé auprès de l'autorité de l'État
membre de destination.</li>
</ol>
<div class="enc ok"><div class="t">Point favorable confirmé le 11 septembre 2026</div>
Les Comores ne figurent ni à l'annexe A (interdiction totale) ni à l'annexe B (restrictions) du règlement
d'exécution (UE) 2026/1317 du 8 juin 2026. Aucune interdiction européenne ne pèse donc sur les
transporteurs certifiés par l'ANACM, contrairement à quinze autres États africains, asiatiques et
sud-américains. Ce statut n'est pas acquis : il dépend de la qualité de la supervision exercée par
l'ANACM, ce que traduit le risque RM-06.</div>
<p>À ces quatre obligations s'ajoutent, dès l'ouverture commerciale, les <strong>droits des passagers de
l'Union</strong> (indemnisation et assistance en cas de retard, d'annulation ou de refus d'embarquement au
départ de Mayotte ; assistance aux personnes handicapées et à mobilité réduite) et, si du fret ou du
courrier est un jour embarqué, la <strong>désignation ACC3</strong> précédée d'une validation de sûreté
aérienne UE réalisée sur chaque aérodrome de départ.</p>

<h3>5.2 Environnement opérationnel de Dzaoudzi-Pamandzi</h3>
<p><strong>Aérodrome.</strong> Piste unique 16/34 d'environ 1 930 m sur 45 m, revêtue, sans autre plateforme
de dégagement sur l'île ; trafic de l'ordre de 424 000 passagers en 2024 et 461 000 en 2025, en croissance,
avec des ATR 72 et des appareils long-courriers. Le projet d'une piste longue de 2 600 m est ancien et
n'a pas été réalisé. Les longueurs disponibles sont largement suffisantes pour un LET 410 ; la contrainte
n'est pas la performance mais la <strong>cohabitation avec un trafic lourd sur une plateforme unique</strong>.</p>
<p><strong>Services de la circulation aérienne.</strong> Mayotte ne dispose que d'un service de contrôle
d'aérodrome : il n'existe pas de contrôle d'approche, ni de couverture radar, et les espaces supérieurs
relèvent d'organismes voisins. Répondant le 25 juin 2024 à une question écrite déposée en janvier 2023,
le ministère chargé des transports a confirmé cette situation et indiqué que la solution retenue consiste
à confier à l'ASECNA la gestion d'espaces contrôlés au-dessus de Mayotte, avec Antananarivo comme centre
gestionnaire, la France assurant l'installation et la maintenance des moyens techniques ainsi que les
procédures de vol — <strong>sans calendrier arrêté</strong>. C'est, du point de vue de la sécurité des vols,
le point le plus structurant de l'étude (risques RM-09 et RM-10).</p>
<p><strong>Météorologie.</strong> Saison des pluies du 1<sup>er</sup> novembre au 30 avril, cœur de mousson de
décembre à mars, plus d'un mètre de précipitations annuelles à Dzaoudzi dont environ 80 % pendant cette
période. La saison cyclonique couvre les mêmes mois : huit systèmes sont passés à moins de 200 km des
côtes au stade de cyclone entre 1979 et 2024, dont <strong>Chido le 14 décembre 2024</strong>, qui a détruit
la tour de contrôle et suspendu le trafic civil, rétabli environ deux mois plus tard. La convection
tropicale, avec un appareil non pressurisé volant dans la couche, constitue le second grand facteur de
risque opérationnel (RM-13 et RM-14).</p>
<p><strong>Survol maritime.</strong> L'étape Moroni–Dzaoudzi impose 140 NM au-dessus de la mer sans terrain
utilisable ; les équipements de survie, l'entraînement à l'amerrissage et la coordination du sauvetage
doivent être traités comme des prérequis, non comme des options (RM-15).</p>

<h3>5.3 Sûreté et contrôle aux frontières</h3>
<p>Mayotte applique un régime d'entrée spécifique : les titres de séjour et visas valables pour le reste
du territoire français ne permettent pas nécessairement d'y entrer, et le transporteur est le premier
contrôleur. La sanction est directe et connue : <strong>10 000 € d'amende par passager</strong> débarqué sans
le document de voyage, le visa ou l'autorisation exigés, appliquée autant de fois qu'il y a de passagers
concernés, sans préjudice des frais de réacheminement et d'hébergement. Sur un axe soumis à une forte
pression migratoire, le contrôle documentaire et la résistance à la fraude et à la corruption deviennent
des processus de sécurité à part entière (RM-24, RM-25, RM-26).</p>
<p>S'y ajoute le risque, classique mais majeur sur les lignes régionales, des marchandises dangereuses non
déclarées dans les bagages et le fret informel (RM-27), traité au lancement par une politique de refus
total et par la formation des agents d'acceptation.</p>

<h3>5.4 Contexte économique et politique</h3>
<p>L'axe est déjà desservi par un opérateur établi, Ewa Air, filiale du groupe Air Austral, qui exploite
des ATR 72-600 depuis Dzaoudzi. Le marché est réel mais étroit, et la relation entre les deux pays reste
sensible : des liaisons ont déjà été suspendues unilatéralement par le passé. L'étude en tire une règle de
prudence : aucun investissement irréversible dédié à cette ligne, une ouverture progressive et un seuil
d'arrêt défini avant le premier vol (RM-29 à RM-31).</p>

<h2>6. Registre des dangers et évaluation des risques</h2>
<p>{len(R)} dangers ont été identifiés et cotés. Les mesures d'atténuation sont rédigées de manière à
pouvoir être reprises telles quelles dans le registre des risques du RA-QDMS, dans le MANEX et dans les
procédures concernées.</p>
{table_registre()}

<h2>7. Synthèse et cartographie des risques</h2>
<table>
<thead><tr><th>Niveau de tolérabilité</th><th class="c">Avant atténuation</th><th class="c">Après atténuation</th></tr></thead>
<tbody>
<tr><td><span class="badge red">Intolérable</span></td><td class="c">{ci['Intolérable']}</td><td class="c">{cr['Intolérable']}</td></tr>
<tr><td><span class="badge orange">Tolérable</span></td><td class="c">{ci['Tolérable']}</td><td class="c">{cr['Tolérable']}</td></tr>
<tr><td><span class="badge green">Acceptable</span></td><td class="c">{ci['Acceptable']}</td><td class="c">{cr['Acceptable']}</td></tr>
<tr><td><strong>Total</strong></td><td class="c"><strong>{len(R)}</strong></td><td class="c"><strong>{len(R)}</strong></td></tr>
</tbody></table>
<h3>7.1 Matrice des risques initiaux</h3>
{matrice(True)}
<h3>7.2 Matrice des risques résiduels</h3>
{matrice(False)}
<div class="enc alerte"><div class="t">Les quatre risques initialement intolérables</div>
<strong>RM-09</strong> — intégration à Mayotte sans contrôle d'approche ni radar, au milieu d'un trafic
commercial lourd ; <strong>RM-13</strong> — convection tropicale avec un appareil non pressurisé et une
détection météo embarquée limitée ; <strong>RM-16</strong> — pression sur la charge marchande et risque de
surcharge ou d'erreur de centrage ; <strong>RM-27</strong> — marchandises dangereuses non déclarées.
Aucun de ces quatre risques ne peut être accepté au titre de la seule vigilance des équipages : chacun
appelle une mesure matérielle ou documentaire vérifiable, inscrite au plan d'actions du § 9.</div>
<p>Après atténuation, les risques résiduels les plus élevés restent <strong>RM-06</strong> (supervision de
l'État de l'exploitant) et <strong>RM-31</strong> (contexte politique) : ils échappent largement au contrôle
de la compagnie et sont traités par la préparation à l'arrêt plutôt que par la prévention, ainsi que
<strong>RM-09</strong>, qui restera tolérable tant que Mayotte ne disposera pas d'un service de contrôle
d'approche.</p>

<h2>8. Conditions bloquantes avant le premier vol commercial</h2>
<p>La Direction générale est invitée à retenir ces six conditions comme critères de décision : aucune
n'est négociable, et le non-respect de l'une d'elles interdit l'ouverture.</p>
<ol>
<li><strong>Autorisation Part-TCO notifiée par écrit par l'AESA</strong>, avec des spécifications techniques
couvrant l'aéronef effectivement exploité et l'aérodrome de Dzaoudzi-Pamandzi.</li>
<li><strong>Droits de trafic attribués</strong> à l'issue des consultations bilatérales, désignation notifiée
à la partie française et <strong>autorisation d'exploitation délivrée par la DGAC</strong>.</li>
<li><strong>Preuve d'assurance conforme au règlement (CE) 785/2004</strong> déposée auprès de l'autorité
compétente, y compris la couverture des risques de guerre et assimilés.</li>
<li><strong>OpSpecs ANACM étendues</strong> à la route, aux approches PBN le cas échéant, au survol maritime
prolongé et aux équipements associés (transpondeur mode S, ACAS le cas échéant, équipements de survie,
moyen de détection météorologique), avec une MEL à jour.</li>
<li><strong>Programme de sûreté et procédure de contrôle documentaire validés</strong>, agents formés,
aucun fret ni courrier accepté avant désignation ACC3.</li>
<li><strong>Audit interne d'ouverture de ligne</strong> réalisé par le Département Qualité et
<strong>vol de validation</strong> effectué sans constat majeur, précédés d'un exercice du plan
d'intervention d'urgence.</li>
</ol>

<h2>9. Plan d'actions et calendrier</h2>
<table>
<thead><tr><th class="c" style="width:7%">Action</th><th style="width:14%">Phase</th><th>Contenu</th><th style="width:17%">Pilote</th><th class="c" style="width:12%">Échéance</th></tr></thead>
<tbody>
<tr><td class="c">A1</td><td>Cadrage</td><td>Note de faisabilité à la Direction, budget dédié, décision de lancement du dossier</td><td>Direction générale</td><td class="c">T0</td></tr>
<tr><td class="c">A2</td><td>Droits de trafic</td><td>Saisine de l'ANACM pour l'ouverture de consultations bilatérales avec la DGAC et dossier de désignation</td><td>Point focal certification</td><td class="c">T0 + 3 mois</td></tr>
<tr><td class="c">A3</td><td>Part-TCO</td><td>Analyse d'écarts Annexes 1, 6, 8 et 19, constitution du dossier et dépôt du formulaire FO.TCO.00160</td><td>Responsable Qualité</td><td class="c">T0 + 2 à 4 mois</td></tr>
<tr><td class="c">A4</td><td>Part-TCO</td><td>Réponse aux demandes de l'AESA, préparation d'un éventuel audit sur site, clôture des écarts</td><td>Responsable Qualité</td><td class="c">T0 + 6 à 12 mois</td></tr>
<tr><td class="c">A5</td><td>Exploitation</td><td>Extension des OpSpecs, mise à jour MANEX et MEL, politique carburant et tableaux de charge marchande par étape</td><td>Directeur des opérations</td><td class="c">T0 + 8 mois</td></tr>
<tr><td class="c">A6</td><td>Équipements</td><td>Vérification et mise à niveau : détection météorologique, transpondeur mode S, ACAS selon Annexe 6, équipements de survie et radeaux</td><td>Maintenance</td><td class="c">T0 + 8 mois</td></tr>
<tr><td class="c">A7</td><td>Documentation</td><td>Extraction et annexion de la section AD 2 FMCZ de l'AIP en vigueur, notamment le § AD 2.20, et intégration au dossier de route et à la formation (annexe B)</td><td>Opérations + Qualité</td><td class="c">T0 + 5 mois</td></tr>
<tr><td class="c">A8</td><td>Sûreté et frontière</td><td>Procédure de contrôle documentaire établie avec la police aux frontières, formation des agents, politique marchandises dangereuses</td><td>Responsable Sûreté</td><td class="c">T0 + 9 mois</td></tr>
<tr><td class="c">A9</td><td>Escale</td><td>Contrats d'assistance, d'avitaillement et d'assistance technique ; audit des prestataires avant le premier vol</td><td>Ground Handling + Qualité</td><td class="c">T0 + 11 mois</td></tr>
<tr><td class="c">A10</td><td>Formation</td><td>Formation « opérations vers Mayotte », entraînement amerrissage, vérification des niveaux linguistiques, briefings de route</td><td>Chef pilote</td><td class="c">T0 + 11 mois</td></tr>
<tr><td class="c">A11</td><td>Validation</td><td>Exercice du plan d'intervention d'urgence, audit interne d'ouverture de ligne, vol de validation</td><td>Responsable Qualité</td><td class="c">T0 + 12 à 16 mois</td></tr>
<tr><td class="c">A12</td><td>Ouverture</td><td>Vérification des six conditions bloquantes, décision formelle de la Direction, ouverture commerciale</td><td>Dirigeant responsable</td><td class="c">T0 + 12 à 18 mois</td></tr>
</tbody></table>

<h2>10. Surveillance de la performance de sécurité</h2>
<p>Les indicateurs suivants sont suivis mensuellement par le Département Qualité et présentés en revue de
sécurité ; le dépassement d'un seuil d'alerte déclenche une réévaluation du risque concerné.</p>
<table>
<thead><tr><th style="width:38%">Indicateur</th><th style="width:22%">Objectif</th><th>Seuil d'alerte et réaction</th></tr></thead>
<tbody>
<tr><td>Constats en inspection au sol (SAFA) sur la ligne</td><td>Aucun constat de catégorie 2 ou 3</td><td>Un constat de catégorie 2 : audit interne sous 15 jours ; catégorie 3 : suspension de la ligne</td></tr>
<tr><td>Quasi-collisions ou pertes de séparation signalées à l'arrivée ou au départ de FMCZ</td><td>Zéro</td><td>Un événement : réévaluation de RM-09 et adaptation des créneaux</td></tr>
<tr><td>Passagers non admis et amendes frontière</td><td>Zéro</td><td>Un cas : revue immédiate de la procédure de contrôle documentaire</td></tr>
<tr><td>Taux de déroutement et de demi-tour pour cause météorologique</td><td>&lt; 2 % des vols</td><td>Au-delà : révision des créneaux horaires et de la politique carburant</td></tr>
<tr><td>Découvertes de marchandises dangereuses non déclarées</td><td>Zéro</td><td>Un cas : recyclage des agents d'acceptation sous 30 jours</td></tr>
<tr><td>Dépassements des limites de temps de vol</td><td>Zéro</td><td>Un cas : révision du planning et renfort d'équipage</td></tr>
<tr><td>Comptes rendus de sécurité déposés par les équipages sur la ligne</td><td>≥ 5 pour 1 000 vols</td><td>En deçà : signe d'une sous-déclaration, action sur la culture de sécurité</td></tr>
</tbody></table>

<h2>11. Conclusion et décision demandée</h2>
<p>L'ouverture d'une desserte de Mayotte est <strong>techniquement réalisable</strong> avec le LET 410 :
les distances, les longueurs de piste et les infrastructures ne posent pas de difficulté de performance.
Elle est <strong>juridiquement possible</strong>, les Comores n'étant frappées d'aucune interdiction
européenne et un accord bilatéral existant depuis 2014. Elle est en revanche
<strong>exigeante</strong> : elle suppose une autorisation européenne de sécurité délivrée après examen
approfondi de la compagnie, des droits de trafic à négocier entre États, et la maîtrise de deux risques
propres à cette ligne — l'intégration dans un espace aérien sans contrôle d'approche, et la météorologie
tropicale avec un appareil non pressurisé — auxquels s'ajoute une exposition frontalière financièrement
lourde.</p>
<p>Le Département Qualité recommande à la Direction générale :</p>
<ol>
<li>d'<strong>autoriser le lancement du dossier</strong> (actions A1 à A4) sans engagement commercial,
avec un budget et un échéancier arrêtés ;</li>
<li>de <strong>subordonner toute décision d'ouverture</strong> aux six conditions bloquantes du § 8 ;</li>
<li>de <strong>traiter en priorité les quatre risques intolérables</strong> RM-09, RM-13, RM-16 et RM-27,
dont le traitement conditionne l'ensemble ;</li>
<li>d'<strong>intégrer les {len(R)} risques</strong> de la présente étude au registre du RA-QDMS avec
leurs pilotes et leurs échéances, et de <strong>réviser cette étude</strong> à la décision de la Direction
ou au plus tard le 11 mars 2027.</li>
</ol>
<div class="sign">
  <div><div class="r">Rédigé par</div><div class="v">Responsable Qualité</div><div class="r">Date et signature</div></div>
  <div><div class="r">Vérifié par</div><div class="v">Directeur des opérations</div><div class="r">Date et signature</div></div>
  <div><div class="r">Approuvé par</div><div class="v">Dirigeant responsable</div><div class="r">Date et signature</div></div>
</div>

<h2>Annexe A — Sources consultées</h2>
<p class="src">Sources publiques consultées le 11 septembre 2026. Les références réglementaires doivent être
revérifiées dans leur version en vigueur au moment du dépôt du dossier.</p>
<ol class="src">
<li>AESA — <em>Third-Country Operators (TCO), Part-TCO</em>, champ d'application territorial (Mayotte citée), procédure et formulaire FO.TCO.00160 : https://www.easa.europa.eu/en/domains/air-operations/tco-third-country-operators</li>
<li>Règlement d'exécution (UE) 2026/1317 du 8 juin 2026 — liste de sécurité de l'UE, annexes A et B : https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=OJ:L_202601317</li>
<li>Commission européenne — mise à jour de la liste de sécurité aérienne du 9 juin 2026 : https://transport.ec.europa.eu/news-events/news/commission-updates-eu-air-safety-list-all-air-carriers-kyrgyzstan-removed-air-express-algeria-added-2026-06-09_en</li>
<li>Assemblée nationale — projet de loi et étude d'impact relatifs à l'accord de services aériens France / Union des Comores signé le 22 août 2014 : https://www.assemblee-nationale.fr/14/projets/pl3384-ei.asp</li>
<li>Assemblée nationale — question écrite n° 4934 sur la sécurité du transport aérien à Mayotte et réponse du ministère du 25 juin 2024 (absence de contrôle d'approche, transfert d'espaces à l'ASECNA) : https://questions.assemblee-nationale.fr/q16/16-4934QE.htm</li>
<li>Règlement (CE) n° 785/2004 consolidé — montants minimaux d'assurance : https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:02004R0785-20200730</li>
<li>Règlement d'exécution (UE) 2015/1998 et documentation ACC3 : https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX%3A02015R1998-20180206</li>
<li>CESEDA, art. L. 821-6 à L. 821-9 — amendes aux entreprises de transport : https://www.legifrance.gouv.fr/codes/id/LEGIARTI000049051088/2024-01-28</li>
<li>Météo-France Mayotte — climat mahorais et évolution de l'activité cyclonique : https://meteofrance.yt/fr/climat/evolution-de-lactivite-cyclonique</li>
<li>Infrastructures de Mayotte après le cyclone Chido (14 décembre 2024) : https://la1ere.franceinfo.fr/mayotte/aeroport-routes-barges-electricite-eau-le-point-sur-les-infrastructures-apres-le-passage-du-cyclone-chido-a-mayotte-1545745.html</li>
<li>Données de trafic et caractéristiques de l'aéroport de Dzaoudzi-Pamandzi : https://en.wikipedia.org/wiki/Dzaoudzi%E2%80%93Pamandzi_International_Airport</li>
<li>Service de l'information aéronautique — AIP France, section AD 2 FMCZ : https://www.sia.aviation-civile.gouv.fr/ <em>(serveur inaccessible le jour de la rédaction ; extraction à réaliser, action A7)</em></li>
</ol>

<h2>Annexe B — Éléments à extraire de l'AIP en vigueur (action A7)</h2>
<p>Les rubriques suivantes de la section AD 2 FMCZ doivent être extraites de l'AIP France en vigueur,
annexées à la présente étude et intégrées au dossier de route ; toute divergence avec les hypothèses
retenues ici impose une réévaluation des risques concernés.</p>
<table>
<thead><tr><th style="width:14%">Rubrique</th><th>Élément à relever</th><th style="width:18%">Risque concerné</th></tr></thead>
<tbody>
<tr><td>AD 2.3</td><td>Horaires de l'aérodrome et des services (douane, sûreté, assistance, avitaillement)</td><td>RM-18, RM-19</td></tr>
<tr><td>AD 2.6</td><td>Niveau de sauvetage et de lutte contre l'incendie, et horaires de disponibilité</td><td>RM-33</td></tr>
<tr><td>AD 2.12</td><td>Caractéristiques de piste : dimensions réelles, résistance, distances déclarées</td><td>RM-11, RM-16</td></tr>
<tr><td>AD 2.17 / 2.18</td><td>Espace aérien ATS, classification, limites verticales, fréquences</td><td>RM-09, RM-10</td></tr>
<tr><td>AD 2.19 / 2.22</td><td>Aides de radionavigation, procédures d'arrivée, de départ et d'attente, minima</td><td>RM-12</td></tr>
<tr><td><strong>AD 2.20</strong></td><td><strong>Règlements de circulation locaux</strong> : restrictions de roulage et de stationnement, consignes de nuit et par faible visibilité, procédures particulières applicables aux aéronefs légers</td><td>RM-09, RM-18, RM-23</td></tr>
<tr><td>AD 2.21 / 2.23</td><td>Procédures antibruit, péril animalier, consignes particulières, survol des zones habitées</td><td>RM-17, RM-23</td></tr>
<tr><td>NOTAM</td><td>Travaux en cours liés à la reconstruction post-Chido, indisponibilités temporaires</td><td>RM-11, RM-14</td></tr>
</tbody></table>
<p class="src">Nota : les valeurs d'aérodrome citées au § 5.2 proviennent de sources secondaires publiques et
sont données à titre indicatif. Seules les données de l'AIP en vigueur et les NOTAM font foi pour la
préparation des vols.</p>
"""

def main():
    html = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{REF} — {TITRE}</title>
<meta name="author" content="Royal Air — Département Qualité">
<style>{CSS}</style></head>
<body><div class="page">{entete()}
<main class="corps">{corps()}</main>
<footer><span>ROYAL AIR &middot; Département Qualité &amp; SGS &middot; {REF} &middot; Éd. 1 / Rév. 0</span>
<span>Document interne — toute copie imprimée est non contrôlée &middot; {DATE}</span></footer>
</div></body></html>"""
    dest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                        "RA-SGS-ETU-26-01-desserte-mayotte.html")
    dest = os.path.normpath(dest)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    c1, c2 = compte(True), compte(False)
    print(f"Écrit : {dest}")
    print(f"{len(R)} risques — initial {c1} / résiduel {c2}")

if __name__ == "__main__":
    main()
