/* ================================================================
   🎮 MoheliGo Life — v100 « LA DYNASTIE »
   LES ÉTUDES · LE TRAVAIL · L'EMPIRE · LES FOYERS · L'HÉRITAGE

   Ce que la v100 ajoute par rapport à la v94 :
   · 🎓 LES ÉTUDES sont un vrai parcours : lycée → licence → master →
     doctorat (+ formation pro). Mérite mensuel, mentions, bourses,
     redoublement, petits boulots. Le diplôme OUVRE des métiers.
   · 💼 On commence sa vie par un choix : étudier ou travailler.
   · 🏢 Quitter son emploi pour l'entreprise donne un VRAI bonus de
     dirigeant à plein temps (+25 %). Un enfant adulte peut être nommé
     GÉRANT d'une entreprise.
   · 💍 POLYGAMIE : jusqu'à deux épouses (pour un homme). Équité entre
     les foyers, jalousie, divorce. Chaque enfant a sa mère.
   · 📜 TESTAMENT : on lègue chaque entreprise, la maison et l'argent à
     l'enfant de son choix, de son vivant.
   · 🕊️ SUCCESSION : à la mort, l'enfant qui reprend l'histoire choisit
     — ACCEPTER L'HÉRITAGE, ou PARTIR DE ZÉRO (plus dur, mais la fierté
     du self-made et un bonus permanent).
   · 📖 CHRONIQUES : toutes les générations passées sont conservées.
   · 🎨 Design refondu : ciel étoilé animé, cartes à accent, navigation.

   Identité conservée : nuit tropicale glassmorphism + KMF + Mohéli.
   Sauvegarde : à CHAQUE action + cloud + migration v1/v2/v3 → v4.
   ================================================================ */
(function(){
"use strict";
if(window.MGLife)return;

/* ---------------- RÉGLAGES (équilibrage central) ---------------- */
var CFG={
  argentDepart:25000, ageDepart:18,
  depenses:[
    {id:"nourriture",n:"🍚 Nourriture",base:32000},
    {id:"eau",n:"💧 Eau",base:5000},
    {id:"elec",n:"💡 Électricité",base:11000},
    {id:"transport",n:"🛺 Transport",base:12000},
    {id:"telephone",n:"📱 Crédit téléphone",base:7000},
    {id:"divers",n:"🧺 Divers & habits",base:10000}],
  loyer:18000, internet:15000,
  trainDeVie:0.02, trainDeVieMax:150000,      // la richesse coûte cher
  confort:{econome:{m:0.8,bonheur:-2,n:"🌱 Économe"},normal:{m:1,bonheur:0,n:"⚖️ Normal"},large:{m:1.45,bonheur:2,sante:1,n:"✨ Confortable"}},
  foyerCout:14000, enfantCout:9000, ecoleRentree:18000,
  mariageSimple:200000, grandMariage:1200000, fiancailles:40000,
  secondMariage:450000,                       // épouser une deuxième femme coûte plus cher
  equiteCadeau:35000,                         // le cadeau qui rétablit l'équité entre foyers
  demenagement:50000, salaireEmploye:45000, embauche:20000, pub:50000,
  ordinateur:180000, moto:800000,
  maison:{p:12000000,entretien:25000}, villa:{p:45000000,entretien:80000},
  partageGain:10000, partageMaxMois:3, loisirsMaxMois:3,
  pdgMin:200000, pdgPartActivite:0.25,        // salaire PDG max = 200 000 + 25 % du net mensuel
  pdgPleinTemps:1.25,                         // 🏢 quitter son emploi = +25 % sur les entreprises
  gerantBonus:1.15,                           // un enfant gérant fait tourner la boîte
  bizCapMois:15000000,                        // plafond de production/mois par entreprise (sauf tech)
  inflationMois:0.002,
  bourse:22000, petitBoulot:11000,            // pendant les études
  diplomeSalaire:0.15,                        // +15 % de salaire par niveau de diplôme
  selfMadeBonus:1.15                          // celui qui refuse l'héritage gagne mieux sa vie
};

/* ---------------- 🎓 LES ÉTUDES ---------------- */
var DIPLOMES=["sans diplôme","Baccalauréat","Licence","Master","Doctorat"];
var DIPLOME_IC=["📄","📗","📘","📕","🎓"];
var CURSUS=[
  {id:"bac",ic:"📗",n:"Lycée → Baccalauréat",req:0,don:1,mois:24,cout:9000,ageMin:15,ageMax:30,
   d:"Le lycée de Fomboni. La base de tout : sans le bac, beaucoup de portes restent fermées."},
  {id:"pro",ic:"🛠️",n:"Formation professionnelle",req:0,don:null,bonusNiv:1,mois:12,cout:16000,ageMin:16,ageMax:60,
   d:"Courte et concrète : tu montes d'un niveau dans ton métier, sans diplôme d'État."},
  {id:"licence",ic:"📘",n:"Licence — Université de Moroni",req:1,don:2,mois:36,cout:26000,ageMin:17,ageMax:45,
   d:"Trois ans en Grande Comore. Ça coûte, ça éloigne de la famille — et ça change une vie."},
  {id:"master",ic:"📕",n:"Master",req:2,don:3,mois:24,cout:48000,ageMin:19,ageMax:55,
   d:"Deux ans de plus. C'est le diplôme des cadres, des ingénieurs et des grandes administrations."},
  {id:"doctorat",ic:"🎓",n:"Doctorat",req:3,don:4,mois:36,cout:65000,ageMin:22,ageMax:60,
   d:"Le sommet. Long, cher, exigeant — et il ouvre absolument tout."}
];
function mention(m){
  if(m>=85)return{t:"mention Très Bien",b:3};
  if(m>=70)return{t:"mention Bien",b:2};
  if(m>=55)return{t:"mention Assez Bien",b:1};
  return{t:"sans mention",b:0};
}

/* ---------------- MÉTIERS ---------------- */
/* reqDip = diplôme minimum exigé (0 = aucun) */
var METIERS=[
  {id:"sans",ic:"🧍",n:"Sans emploi",cache:true,reqDip:0,tag:"ville",d:"",
   niveaux:[{t:"Sans emploi",sal:0}],debut:0},
  {id:"capitaine",ic:"🚤",n:"Capitaine de vedette",type:"carriere",reqDip:0,d:"Tu prends la mer entre Grande Comore et Mohéli. La météo décide de tes journées.",
   niveaux:[{t:"Matelot",sal:60000},{t:"Second",sal:80000},{t:"Capitaine",sal:100000},{t:"Capitaine principal",sal:250000}],debut:2,meteoSensible:true,tag:"mer"},
  {id:"tourisme",ic:"🌴",n:"Agent touristique",type:"carriere",reqDip:0,d:"Tu fais découvrir Mohéli aux visiteurs : tortues, baleines, îlots.",
   niveaux:[{t:"Guide stagiaire",sal:70000},{t:"Agent touristique",sal:100000},{t:"Agent senior",sal:150000},{t:"Chef d'agence",sal:250000}],debut:1,saisonSensible:true,tag:"tourisme"},
  {id:"dev",ic:"💻",n:"Développeur",type:"carriere",reqDip:0,d:"Pas de salaire fixe au début… mais aucun plafond pour les meilleurs. Le seul grand métier qui s'apprend seul.",
   niveaux:[{t:"Débutant",sal:0},{t:"Freelance",sal:0},{t:"Développeur confirmé",sal:0},{t:"Développeur expert",sal:0}],debut:0,freelance:true,tag:"ville"},
  {id:"pecheur",ic:"🎣",n:"Pêcheur",type:"metier",reqDip:0,d:"La mer nourrit — quand elle le veut bien.",
   niveaux:[{t:"Pêcheur",sal:55000},{t:"Pêcheur expérimenté",sal:75000},{t:"Patron pêcheur",sal:110000}],debut:0,meteoSensible:true,tag:"mer"},
  {id:"commercant",ic:"🏪",n:"Commerçant",type:"metier",reqDip:0,d:"Ta boutique au marché : tout dépend des clients.",
   niveaux:[{t:"Vendeur",sal:50000},{t:"Commerçant",sal:90000},{t:"Grossiste",sal:160000}],debut:1,variable:true,tag:"commerce"},
  {id:"chauffeur",ic:"🚕",n:"Chauffeur",type:"metier",reqDip:0,d:"Taxi partagé sur la côtière.",
   niveaux:[{t:"Chauffeur",sal:65000},{t:"Chauffeur-propriétaire",sal:120000}],debut:0,variable:true,tag:"ville"},
  {id:"agriculteur",ic:"🌱",n:"Agriculteur",type:"metier",reqDip:0,d:"Bananes, manioc, ylang-ylang — la terre est généreuse.",
   niveaux:[{t:"Ouvrier agricole",sal:45000},{t:"Agriculteur",sal:80000},{t:"Grand planteur",sal:140000}],debut:0,meteoSensible:true,tag:"terre"},
  {id:"enseignant",ic:"📚",n:"Enseignant",type:"metier",reqDip:1,d:"Un salaire stable et le respect du village. Il faut le bac.",
   niveaux:[{t:"Instituteur",sal:85000},{t:"Professeur",sal:120000},{t:"Directeur d'école",sal:180000}],debut:0,stable:true,reputation:1,retraite:true,tag:"ville"},
  {id:"infirmier",ic:"🩺",n:"Infirmier",type:"metier",reqDip:1,d:"À l'hôpital de Fomboni, on compte sur toi jour et nuit. Il faut le bac.",
   niveaux:[{t:"Aide-soignant",sal:70000},{t:"Infirmier",sal:110000},{t:"Infirmier chef",sal:170000}],debut:1,fatigue:1,reputation:1,retraite:true,tag:"ville"},
  {id:"fonctionnaire",ic:"🏛️",n:"Fonctionnaire",type:"carriere",reqDip:2,d:"L'administration : ni riche ni pauvre, mais une retraite et une signature qui compte. Licence exigée.",
   niveaux:[{t:"Agent",sal:95000},{t:"Chef de bureau",sal:150000},{t:"Directeur de service",sal:240000},{t:"Secrétaire général",sal:400000}],debut:0,stable:true,reputation:2,retraite:true,tag:"ville"},
  {id:"gestionnaire",ic:"📊",n:"Gestionnaire",type:"carriere",reqDip:2,d:"Comptes, banque, projets financés. Le métier qui apprend à faire tourner l'argent des autres — puis le sien. Licence exigée.",
   niveaux:[{t:"Comptable",sal:110000},{t:"Contrôleur de gestion",sal:180000},{t:"Directeur financier",sal:320000},{t:"Banquier d'affaires",sal:550000}],debut:0,bizSavvy:true,tag:"commerce"},
  {id:"ingenieur",ic:"⚙️",n:"Ingénieur",type:"carriere",reqDip:3,d:"Routes, ports, énergie, réseaux. On te fait venir pour les grands chantiers. Master exigé.",
   niveaux:[{t:"Ingénieur junior",sal:180000},{t:"Ingénieur",sal:300000},{t:"Chef de projet",sal:480000},{t:"Directeur technique",sal:750000}],debut:0,reputation:1,tag:"ville"},
  {id:"avocat",ic:"⚖️",n:"Avocat",type:"carriere",reqDip:3,d:"Le droit, les contrats, les successions. Rien ne protège mieux un patrimoine. Master exigé.",
   niveaux:[{t:"Avocat stagiaire",sal:150000},{t:"Avocat",sal:320000},{t:"Avocat d'affaires",sal:600000},{t:"Bâtonnier",sal:900000}],debut:0,reputation:3,tag:"ville"},
  {id:"medecin",ic:"🧑🏾‍⚕️",n:"Médecin",type:"carriere",reqDip:4,d:"Le respect absolu, et des journées sans fin. Doctorat exigé.",
   niveaux:[{t:"Médecin généraliste",sal:350000},{t:"Spécialiste",sal:600000},{t:"Chef de service",sal:900000},{t:"Directeur de l'hôpital",sal:1400000}],debut:0,fatigue:2,reputation:4,retraite:true,tag:"ville"}
];
function metiersVisibles(){return METIERS.filter(function(m){return !m.cache;});}

/* ---------------- VILLAGES ---------------- */
var VILLAGES=[
  {id:"fomboni",n:"Fomboni",ic:"🏙️",d:"La capitale : marché, port, hôpital, lycée.",bonus:{commerce:1.12,ville:1.08},etudes:1.15},
  {id:"hoani",n:"Hoani",ic:"⚓",d:"Port du nord, face à la Grande Comore.",bonus:{mer:1.1}},
  {id:"nioumachoua",n:"Nioumachoua",ic:"🏝️",d:"Les îlots, le parc marin, les lodges.",bonus:{tourisme:1.18,mer:1.05}},
  {id:"ouallah",n:"Ouallah",ic:"🎣",d:"Village de pêcheurs, porte du parc.",bonus:{mer:1.12,terre:1.05}},
  {id:"wanani",n:"Wanani",ic:"⛰️",d:"Sur les hauteurs, entre plantations.",bonus:{terre:1.12}},
  {id:"djando",n:"Djando",ic:"🥁",d:"Le village des fêtes et du twarab.",bonus:{bonheur:2}},
  {id:"itsamia",n:"Itsamia",ic:"🐢",d:"Les tortues, l'écotourisme pionnier.",bonus:{tourisme:1.15}},
  {id:"miringoni",n:"Miringoni",ic:"🌾",d:"Plages sauvages et grandes cultures.",bonus:{terre:1.15}},
  {id:"hamavouna",n:"Hamavouna",ic:"🌊",d:"Petit village tranquille du littoral.",bonus:{mer:1.06,bonheur:1}},
  {id:"mbatse",n:"Mbatsé",ic:"🌴",d:"Entre cocotiers et lagon.",bonus:{tourisme:1.06,terre:1.06}},
  {id:"ouroveni",n:"Ourovéni",ic:"🚤",d:"Escale des vedettes du sud.",bonus:{mer:1.08,commerce:1.05}}
];

/* ---------------- ENTREPRISES ---------------- */
var BIZ=[
  {id:"commerce",ic:"🏪",n:"Commerce",prix:600000,rev:90000,tag:"commerce",d:"Une boutique bien placée au marché."},
  {id:"ferme",ic:"🌾",n:"Ferme",prix:400000,rev:65000,tag:"terre",d:"Bananes, manioc, ylang — la terre paie patiemment."},
  {id:"restaurant",ic:"🍽️",n:"Restaurant",prix:900000,rev:130000,tag:"tourisme",d:"Poisson grillé et poulet coco face à la mer."},
  {id:"agence",ic:"🌴",n:"Agence touristique",prix:1500000,rev:200000,tag:"tourisme",d:"Excursions : tortues, baleines, îlots."},
  {id:"vedette",ic:"🚤",n:"Compagnie maritime",prix:3000000,rev:380000,tag:"mer",d:"Ta propre vedette sur la ligne Mohéli ↔ Grande Comore."},
  {id:"cabinet",ic:"⚖️",n:"Cabinet de conseil",prix:2000000,rev:290000,tag:"ville",cond:"dip3",d:"Droit, comptabilité, montage de dossiers. (Master exigé)"},
  {id:"clinique",ic:"🏥",n:"Clinique privée",prix:9000000,rev:1100000,tag:"ville",cond:"dip4",d:"La santé privée à Fomboni. (Doctorat exigé)"},
  {id:"startup",ic:"💻",n:"Entreprise technologique",prix:2500000,rev:0,tag:"ville",cond:"dev3",d:"Elle BRÛLE de l'argent au début (salaires, serveurs)… mais aucun plafond pour qui tient bon. (Réservé aux développeurs experts)"},
  {id:"hotel",ic:"🏨",n:"Hôtel",prix:12000000,rev:1400000,tag:"tourisme",d:"Le grand rêve : ton hôtel face aux îlots."}
];

/* ---------------- LOISIRS (dépenser pour vivre mieux) ---------------- */
var LOISIRS=[
  {id:"plage",ic:"🏖️",n:"Journée plage en famille",p:3000,e:{bonheur:6,energie:3}},
  {id:"foot",ic:"⚽",n:"Sport avec les jeunes",p:1000,e:{sante:5,energie:2,bonheur:2}},
  {id:"resto",ic:"🍽️",n:"Restaurant à Fomboni",p:9000,e:{bonheur:8}},
  {id:"soin",ic:"💆🏾",n:"Massage & soins traditionnels",p:12000,e:{sante:8,energie:5}},
  {id:"pirogue",ic:"🛶",n:"Sortie aux îlots en pirogue",p:18000,e:{bonheur:12,sante:4}},
  {id:"gcomore",ic:"✈️",n:"Week-end en Grande Comore",p:70000,e:{bonheur:15,sante:4,energie:-3}},
  {id:"cadeaux",ic:"🎁",n:"Gâter la famille",p:25000,e:{bonheur:7,reput:5,spirit:3}},
  {id:"omra",ic:"🕋",n:"Le pèlerinage (Omra)",p:1800000,e:{spirit:35,bonheur:18,reput:12},unique:true}
];

/* ---------------- PRÉNOMS & PRÉTENDANTS ---------------- */
var PRENOMS_G=["Ahmed","Said","Ibrahim","Ali","Moussa","Youssouf","Anli","Fahad","Nassur","Chamsoudine","Zaki","Abdou"];
var PRENOMS_F=["Fatima","Zainaba","Echat","Rahma","Moinaécha","Salima","Nadjati","Anfia","Halima","Mariama","Zalia","Nourou"];
var NOMS_FAMILLE=["Mohamed","Abdallah","Said","Ahmed","Soilihi","Mmadi","Attoumane","Halifa","Bacar","Chanfi"];
var PRETENDANTES=["Anturia","Zalhata","Kamaria","Mistoihi","Raïssa","Andjiza","Naila","Chamina"];
var PRETENDANTS=["Soidiki","Ben Ali","Rastami","Fazul","Kassim","Madi","Ahamada","Toiheir"];
var AVATARS={h:["👨🏾","🧔🏾","👨🏾‍💼","👳🏾‍♂️"],f:["👩🏾","🧕🏾","👩🏾‍💼","👰🏾‍♀️"]};

/* ---------------- ÉVÉNEMENTS GÉNÉRAUX ---------------- */
var EVENTS=[
  {id:"mariage_cousin",p:7,ic:"💒",t:"Mariage d'un cousin à Wanani",d:"Toute la famille y sera. Il faut participer, c'est l'honneur.",
   choix:[{t:"Donner 15 000 KMF",e:{argent:-15000,bonheur:6,reput:4}},{t:"Donner 5 000 KMF",e:{argent:-5000,bonheur:2,reput:1}},{t:"Ne pas y aller",e:{bonheur:-4,reput:-6}}]},
  {id:"paludisme",p:6,ic:"🦟",t:"Fièvre — sûrement le paludisme",d:"Tu trembles depuis deux jours. Il faut se soigner.",
   choix:[{t:"Hôpital de Fomboni (12 000 KMF)",e:{argent:-12000,sante:14,energie:-5}},{t:"Remèdes traditionnels (2 000 KMF)",e:{argent:-2000,sante:4,energie:-10}},{t:"Ignorer et travailler",e:{sante:-16,energie:-12,bonheur:-5}}]},
  {id:"tontine",p:7,ic:"🤝",t:"La tontine du quartier",d:"Le groupe d'épargne t'invite : chacun cotise, chacun reçoit son tour.",
   choix:[{t:"Cotiser 10 000 KMF",e:{argent:-10000,reput:3,_tontine:true}},{t:"Pas ce mois-ci",e:{reput:-1}}]},
  {id:"tontine_gain",p:0,ic:"💰",t:"C'est TON tour de tontine !",d:"Le groupe te remet la cagnotte. La solidarité, ça paie.",
   choix:[{t:"Alhamdulillah ! (+60 000 KMF)",e:{argent:60000,bonheur:8}}]},
  {id:"tel_casse",p:4,ic:"📱",t:"Ton téléphone est tombé dans l'eau",d:"Au port, en aidant à décharger… plouf.",
   choix:[{t:"Racheter (35 000 KMF)",e:{argent:-35000,bonheur:-2}},{t:"Réparer (8 000 KMF)",e:{argent:-8000}},{t:"Vivre sans",e:{bonheur:-6,reput:-2}}]},
  {id:"touriste_genereux",p:5,ic:"🧳",t:"Un touriste ravi te récompense",d:"Tu l'as aidé et raconté l'histoire de Djoumbé Fatima.",
   choix:[{t:"Accepter avec le sourire (+8 000 KMF)",e:{argent:8000,bonheur:4,reput:2}}],pour:["tourisme","capitaine","chauffeur"]},
  {id:"mer_dangereuse",p:6,ic:"🌊",t:"Mer très agitée cette semaine",d:"Les anciens disent de ne pas sortir. Le travail attend pourtant.",
   choix:[{t:"Rester à quai (sage)",e:{argent:-8000,sante:2,reput:2}},{t:"Sortir quand même",e:{argent:12000,sante:-10,energie:-12,_risque:true}}],pour:["capitaine","pecheur"]},
  {id:"belle_saison",p:5,ic:"🐋",t:"Les baleines sont arrivées !",d:"Les touristes affluent — tout le monde travaille double.",
   choix:[{t:"Travailler double (+20 000 KMF)",e:{argent:20000,energie:-14,xp:2}},{t:"Rythme normal",e:{bonheur:2}}],pour:["tourisme","capitaine","commercant"]},
  {id:"panne_moteur",p:4,ic:"🔧",t:"Panne de moteur",d:"Le moteur tousse, puis plus rien.",
   choix:[{t:"Réparation complète (25 000 KMF)",e:{argent:-25000}},{t:"Bricolage (7 000 KMF)",e:{argent:-7000,_risque:true}}],pour:["capitaine","pecheur","chauffeur"]},
  {id:"coupure_elec",p:5,ic:"💡",t:"Coupures d'électricité toute la semaine",d:"Le quartier est dans le noir.",
   choix:[{t:"Lampe solaire (9 000 KMF)",e:{argent:-9000,bonheur:2}},{t:"Patienter à la bougie",e:{bonheur:-3,energie:-3}}]},
  {id:"aide_parents",p:6,ic:"👵",t:"Tes parents ont besoin d'aide",d:"Le toit de la maison familiale fuit avec les pluies.",
   choix:[{t:"Payer la réparation (20 000 KMF)",e:{argent:-20000,bonheur:6,spirit:4,reput:4}},{t:"Donner un peu (7 000 KMF)",e:{argent:-7000,bonheur:2,reput:1}},{t:"Je ne peux vraiment pas",e:{bonheur:-6,spirit:-3,reput:-4}}]},
  {id:"match_foot",p:5,ic:"⚽",t:"Grand match du village",d:"Ton équipe joue contre le village voisin.",
   choix:[{t:"Y aller et cotiser (3 000 KMF)",e:{argent:-3000,bonheur:7,reput:2,energie:3}},{t:"Rester travailler",e:{argent:5000,bonheur:-3,xp:1}}]},
  {id:"visite_medecin",p:4,ic:"🩺",t:"Campagne de santé gratuite",d:"Des médecins consultent gratuitement à l'hôpital.",
   choix:[{t:"Faire le contrôle",e:{sante:8,energie:2}},{t:"Pas le temps",e:{}}]},
  {id:"mangues",p:4,ic:"🥭",t:"La saison des mangues !",d:"Les manguiers croulent. Les enfants du quartier en distribuent.",
   choix:[{t:"En profiter en famille",e:{bonheur:5,sante:3}}]},
  {id:"voleur_marche",p:3,ic:"👝",t:"Pickpocket au marché",d:"Ta poche est plus légère…",
   choix:[{t:"C'est perdu (−6 000 KMF)",e:{argent:-6000,bonheur:-4}}]},
  {id:"invite_djando",p:4,ic:"🥁",t:"Soirée twarab à Djando",d:"Un orchestre vient jouer. Toute la jeunesse y va.",
   choix:[{t:"Y aller (2 000 KMF)",e:{argent:-2000,bonheur:8,energie:-4}},{t:"Se coucher tôt",e:{energie:6}}]},
  {id:"client_impaye",p:4,ic:"🧾",t:"Un client ne paie pas",d:"Il promet « le mois prochain incha'Allah »…",
   choix:[{t:"Patienter avec le sourire",e:{argent:-8000,reput:2}},{t:"Insister fermement",e:{argent:-2000,reput:-2,bonheur:-2}}],pour:["commercant","chauffeur","dev","tourisme","gestionnaire"]},
  {id:"contrat_dev",p:0,ic:"💻",t:"Un contrat de développement !",d:"Une boutique veut un site vitrine. C'est ta chance.",
   choix:[{t:"Accepter et bosser dur",e:{argent:45000,energie:-12,xp:5}},{t:"Trop compliqué pour l'instant",e:{bonheur:-2}}],pour:["dev"]},
  {id:"cyclone_annonce",p:2,ic:"🌀",t:"Alerte cyclonique",d:"La radio annonce un cyclone au large.",
   choix:[{t:"Protéger la maison (10 000 KMF)",e:{argent:-10000,sante:2}},{t:"Faire confiance au destin",e:{_risque:true}}]},
  {id:"naissance_voisin",p:4,ic:"👶",t:"Naissance chez les voisins",d:"Un petit garçon ! Le quartier célèbre.",
   choix:[{t:"Apporter un cadeau (4 000 KMF)",e:{argent:-4000,bonheur:4,reput:3}},{t:"Féliciter simplement",e:{bonheur:2}}]},
  {id:"deces_village",p:3,ic:"🕌",t:"Deuil au village",d:"Un ancien s'est éteint. Tout le monde participe.",
   choix:[{t:"Participer dignement (5 000 KMF)",e:{argent:-5000,spirit:6,reput:4,bonheur:-2}},{t:"Présenter ses condoléances",e:{spirit:2,reput:1,bonheur:-2}}]},
  /* — événements liés aux ÉTUDES — */
  {id:"exam_blanc",p:0,ic:"📝",t:"Examens blancs",d:"La semaine des partiels. Tu peux réviser à fond… ou sortir un peu.",
   choix:[{t:"Réviser jour et nuit",e:{merite:9,energie:-14,bonheur:-4}},{t:"Réviser normalement",e:{merite:3,energie:-5}},{t:"Sortir avec les autres",e:{merite:-6,bonheur:8,energie:3}}]},
  {id:"prof_remarque",p:0,ic:"👨🏾‍🏫",t:"Un professeur te remarque",d:"Il te propose du tutorat payé pour les plus jeunes.",
   choix:[{t:"Accepter (+14 000 KMF/mois de plus ce mois-ci)",e:{argent:14000,merite:4,energie:-6}},{t:"Refuser, je dois réviser",e:{merite:5}}]},
  {id:"greve_fac",p:0,ic:"✊🏾",t:"Grève à l'université",d:"Les cours sont bloqués depuis trois semaines.",
   choix:[{t:"Réviser seul à la maison",e:{merite:4,bonheur:-3}},{t:"Rentrer à Mohéli en attendant",e:{merite:-5,bonheur:6,argent:-12000}}]}
];

/* ---------------- ÉVÉNEMENTS FAMILLE (unions, polygamie) ---------------- */
function pretendantNom(){
  var l=(L.sexe==="f"?PRETENDANTS:PRETENDANTES).filter(function(n){
    return !L.unions.some(function(u){return u.nom===n;});
  });
  return l[Math.floor(Math.random()*l.length)]||"Anturia";
}
function motEpoux(){return L.sexe==="f"?"ton époux":"ton épouse";}
function maxUnions(){return L.sexe==="f"?1:2;}   /* aux Comores, un homme peut avoir plusieurs épouses */
function unionsActives(){return L.unions.filter(function(u){return !u.divorce;});}

var FAM_EVENTS=[
  {id:"rencontre",ic:"💞",t:"Une belle rencontre…",p:0.16,
   cond:function(){return !unionsActives().length&&!L.fiance&&L.age>=20&&L.bonheur>=35&&!L.etude;},
   d:function(){L._pretendant=pretendantNom();return "Au mariage d'une cousine, ton regard croise celui de "+L._pretendant+". Les anciens ont remarqué…";},
   choix:[{t:"Se fiancer (40 000 KMF de cadeaux)",f:function(){
       if(L.argent<CFG.fiancailles){alerte("Pas assez pour les cadeaux de fiançailles !");return false;}
       L.argent-=CFG.fiancailles;L.fiance=L._pretendant;bouge({bonheur:12,reput:3});
       hist("💞 Fiançailles avec "+L.fiance+" !");}},
     {t:"Pas encore prêt(e)",f:function(){bouge({bonheur:-2});}}]},

  {id:"mariage",ic:"💍",t:"Le grand jour approche",p:0.5,
   cond:function(){return L.fiance&&!unionsActives().length;},
   d:function(){return "Les deux familles sont d'accord. Comment célébrer ton mariage avec "+L.fiance+" ?";},
   choix:[{t:"Mariage simple (200 000 KMF)",f:function(){
       if(L.argent<CFG.mariageSimple){alerte("Pas assez d'argent pour le mariage — économise !");return false;}
       L.argent-=CFG.mariageSimple;ajouterUnion(L.fiance,"simple");L.fiance=null;
       bouge({bonheur:18,spirit:6,reput:5});}},
     {t:"Attendre d'avoir plus de moyens",f:function(){bouge({bonheur:-1});}}]},

  /* 💍💍 LA DEUXIÈME ÉPOUSE — seulement pour un homme, et ça ne se fait pas à la légère */
  {id:"seconde",ic:"💍",t:"On te parle d'un second mariage",p:0.10,
   cond:function(){return L.sexe==="h"&&unionsActives().length===1&&unionsActives().length<maxUnions()
     &&L.age>=28&&L.reput>=55&&L.argent>=CFG.secondMariage&&!L.etude;},
   d:function(){
     var u=unionsActives()[0];L._pretendant=pretendantNom();
     return "Ta situation est connue au village, et ta famille évoque "+L._pretendant+". La loi te l'autorise, mais l'islam demande l'ÉQUITÉ ABSOLUE entre les foyers — deux maisons, deux budgets, deux familles. "+(u?u.nom:"Ton épouse")+" le sait déjà, et elle attend ta décision.";},
   choix:[{t:"Épouser une seconde épouse (450 000 KMF)",f:function(){
       var prem=unionsActives()[0];
       if(!prem)return false;
       if(L.argent<CFG.secondMariage){alerte("Il faut "+fmt(CFG.secondMariage)+" pour faire les choses dignement.");return false;}
       L.argent-=CFG.secondMariage;
       ajouterUnion(L._pretendant,"simple");
       prem.bonheur=clamp(prem.bonheur-28);
       bouge({bonheur:8,reput:6,energie:-6});
       hist("⚖️ "+prem.nom+" accuse le coup. À toi de tenir l'équité entre les deux foyers, mois après mois.");}},
     {t:"Refuser — un seul foyer me suffit",f:function(){
       var u=unionsActives()[0];
       if(u)u.bonheur=clamp(u.bonheur+15);
       bouge({bonheur:5,spirit:4});
       hist("🤍 Tu refuses le second mariage. "+(u?u.nom:"Ton épouse")+" ne l'oubliera pas.");}}]},

  {id:"equite",ic:"⚖️",t:"L'équité entre les foyers",p:0.30,
   cond:function(){return unionsActives().length>=2&&unionsActives().some(function(u){return u.bonheur<55;});},
   d:function(){
     L._lesee=unionsActives().slice().sort(function(a,b){return a.bonheur-b.bonheur;})[0]||null;
     if(!L._lesee)return "Tout va bien dans les foyers.";
     return L._lesee.nom+" se sent délaissée : « tu passes tout ton temps là-bas ». L'équité entre les épouses n'est pas un détail — c'est une obligation.";},
   choix:[{t:"Rétablir l'équité (35 000 KMF de cadeaux et de temps)",f:function(){
       if(!L._lesee)return false;
       if(L.argent<CFG.equiteCadeau){alerte("Il faut "+fmt(CFG.equiteCadeau)+" pour bien faire.");return false;}
       L.argent-=CFG.equiteCadeau;L._lesee.bonheur=clamp(L._lesee.bonheur+30);
       bouge({spirit:6,energie:-4});
       hist("⚖️ Équité rétablie avec "+L._lesee.nom+".");}},
     {t:"Elle comprendra, je travaille pour tout le monde",f:function(){
       if(!L._lesee)return false;
       L._lesee.bonheur=clamp(L._lesee.bonheur-18);bouge({bonheur:-6,spirit:-5});
       hist("😔 "+L._lesee.nom+" s'éloigne un peu plus.");}}]},

  {id:"divorce",ic:"💔",t:"Le foyer se brise",p:0.45,
   cond:function(){return unionsActives().some(function(u){return u.bonheur<12;});},
   d:function(){
     L._partante=unionsActives().filter(function(u){return u.bonheur<12;})[0]||null;
     if(!L._partante)return "Le foyer tient bon.";
     return L._partante.nom+" demande la séparation devant le cadi. Les enfants resteront avec elle jusqu'à leur majorité.";},
   choix:[{t:"Tenter une dernière réconciliation (120 000 KMF)",f:function(){
       if(!L._partante)return false;
       if(L.argent<120000){alerte("Il faut 120 000 KMF — et ce n'est même pas garanti.");return false;}
       L.argent-=120000;
       if(Math.random()<0.55){L._partante.bonheur=clamp(L._partante.bonheur+40);bouge({bonheur:8,spirit:5});hist("🤍 Réconciliation avec "+L._partante.nom+". Le foyer tient.");}
       else{divorcer(L._partante);bouge({bonheur:-14,spirit:-4});}}},
     {t:"Accepter la séparation",f:function(){
       if(!L._partante)return false;
       divorcer(L._partante);bouge({bonheur:-12,reput:-4});}}]},

  {id:"grand_mariage",ic:"👑",t:"Le GRAND MARIAGE (anda)",p:0.35,
   cond:function(){return unionsActives().length&&!L.grandMariage&&L.argent>=CFG.grandMariage;},
   d:function(){return "Tu as les moyens d'organiser l'anda : des semaines de fêtes, le village entier, le statut de NOTABLE à vie. 1 200 000 KMF.";},
   choix:[{t:"Organiser l'anda ! (1 200 000 KMF)",f:function(){
       L.argent-=CFG.grandMariage;L.grandMariage=true;
       unionsActives().forEach(function(u){u.bonheur=clamp(u.bonheur+20);});
       bouge({bonheur:20,spirit:10,reput:30});
       hist("👑 GRAND MARIAGE accompli — te voilà notable de Mohéli !");}},
     {t:"Plus tard",f:function(){}}]},

  {id:"naissance",ic:"👶",t:"Un heureux événement !",p:0.14,
   cond:function(){return unionsActives().length&&L.enfants.length<8&&L.age<=52;},
   d:function(){
     var us=unionsActives();L._mere=us[Math.floor(Math.random()*us.length)]||null;
     if(!L._mere)return "Un heureux événement se prépare…";
     return L._mere.nom+" et toi attendez un enfant. Le quartier prépare déjà les youyous…";},
   choix:[{t:"Accueillir le bébé (10 000 KMF de fête)",f:function(){
       if(!L._mere)return false;
       var g=Math.random()<0.5,nom=(g?PRENOMS_G:PRENOMS_F)[Math.floor(Math.random()*12)];
       L.argent-=10000;
       L.enfants.push({nom:nom,g:g?"g":"f",age:0,mere:L._mere.nom,etudes:false,diplome:0,
         travaille:false,parti:false,talent:25+Math.floor(Math.random()*60)});
       L._mere.bonheur=clamp(L._mere.bonheur+12);
       bouge({bonheur:16,spirit:5,reput:3});
       hist("👶 Naissance de "+nom+", de "+L._mere.nom+" ! La famille s'agrandit.");}}]},

  {id:"enfant_malade",ic:"🤒",t:"Un enfant est malade",p:0.08,
   cond:function(){return L.enfants.some(function(e){return e.age<15&&!e.parti;});},
   d:function(){return "Fièvre depuis deux jours. Direction l'hôpital ?";},
   choix:[{t:"Hôpital tout de suite (10 000 KMF)",f:function(){L.argent-=10000;bouge({bonheur:3});hist("🤒 Petite frayeur — l'enfant va mieux.");}},
     {t:"Attendre que ça passe",f:function(){bouge({bonheur:-8});if(Math.random()<0.3){L.argent-=25000;hist("🚑 Ça a empiré : 25 000 KMF d'urgences.");}}}]},

  {id:"etudes_enfant",ic:"🎓",t:"L'université pour ton enfant ?",p:0.6,
   cond:function(){return L.enfants.some(function(e){return e.age>=18&&e.age<=19&&!e.etudes&&!e.parti&&!e.travaille&&!e.gerant;});},
   d:function(){
     var e=L.enfants.filter(function(x){return x.age>=18&&x.age<=19&&!x.etudes&&!x.parti&&!x.travaille&&!x.gerant;})[0]||null;
     L._enfEtudes=e;
     if(!e)return "Un de tes enfants termine le lycée…";
     return e.nom+" a fini le lycée"+(e.talent>=65?" avec d'excellents résultats":"")+". L'université à Moroni coûte 60 000 KMF/an pendant 4 ans. Un enfant diplômé fait un bien meilleur héritier — et un bien meilleur gérant.";},
   choix:[{t:"Payer les études (60 000/an)",f:function(){
       if(!L._enfEtudes)return false;
       L._enfEtudes.etudes=true;bouge({bonheur:8,reput:4});
       hist("🎓 "+L._enfEtudes.nom+" part étudier à Moroni. Fierté !");}},
     {t:"Il/elle travaillera au village",f:function(){
       if(!L._enfEtudes)return false;
       L._enfEtudes.travaille=true;bouge({bonheur:-3});
       hist("💼 "+L._enfEtudes.nom+" commence à travailler au village.");}}]},

  {id:"conjoint_projet",ic:"🧵",t:"Le projet du foyer",p:0.06,
   cond:function(){return unionsActives().some(function(u){return !u.biz;});},
   d:function(){
     L._porteuse=unionsActives().filter(function(u){return !u.biz;})[0]||null;
     if(!L._porteuse)return "Un projet se prépare à la maison…";
     return L._porteuse.nom+" veut lancer un petit commerce au marché : 60 000 KMF pour démarrer.";},
   choix:[{t:"Financer le projet (60 000 KMF)",f:function(){
       if(!L._porteuse)return false;
       if(L.argent<60000){alerte("Pas assez d'argent !");return false;}
       L.argent-=60000;L._porteuse.biz=true;L._porteuse.bonheur=clamp(L._porteuse.bonheur+14);
       bouge({bonheur:8,reput:2});
       hist("🧵 "+L._porteuse.nom+" lance son commerce (+15 000 KMF/mois pour le foyer).");}},
     {t:"Pas maintenant",f:function(){
       if(L._porteuse)L._porteuse.bonheur=clamp(L._porteuse.bonheur-8);
       bouge({bonheur:-4});}}]}
];

function ajouterUnion(nom,type){
  L.unions.push({nom:nom,type:type||"simple",bonheur:80,biz:false,divorce:false,depuisAn:L.annee});
  var rang=unionsActives().length;
  hist("💍 Mariage avec "+nom+(rang>1?" — ta "+rang+"ᵉ épouse":"")+" — que du bonheur !");
}
function divorcer(u){
  u.divorce=true;
  var part=Math.round(Math.max(0,L.argent)*0.25);
  L.argent-=part;
  hist("💔 Séparation d'avec "+u.nom+" : elle part avec "+fmt(part)+" et les jeunes enfants.");
  L.enfants.forEach(function(e){if(e.mere===u.nom&&e.age<18)e.parti=true;});
}

/* ---------------- FÊTES ---------------- */
var FETES={
  ramadan:{ic:"🌙",t:"Le mois de Ramadan",d:"Le jeûne, les prières, les grandes tables du soir. L'âme se repose, le budget nourriture monte.",e:{argent:-14000,spirit:14,bonheur:5,energie:-8}},
  aidFitr:{ic:"🌺",t:"Aïd el-Fitr !",d:"Habits neufs pour tout le monde, gâteaux, visites dans tout Mohéli.",e:{argent:-22000,bonheur:14,spirit:8,reput:3}},
  aidKebir:{ic:"🐑",t:"Aïd el-Kébir",d:"Le sacrifice et le partage : famille, voisins, et les plus pauvres.",e:{argent:-40000,bonheur:10,spirit:12,reput:6}},
  fete_nat:{ic:"🇰🇲",t:"Fête de l'indépendance",d:"Défilés, drapeaux et twarab dans tout le pays.",e:{bonheur:6,reput:1}}
};

/* ---------------- ÉTAT ---------------- */
var L=null,elRoot=null;
var MOIS=["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"];

function nouveauJeu(nom,metierId,sexe,avatar,famille){
  var m=byId(METIERS,metierId||"sans");
  return {v:4,nom:nom,famille:famille||NOMS_FAMILLE[Math.floor(Math.random()*NOMS_FAMILLE.length)],
    sexe:sexe||"h",avatar:avatar||AVATARS[sexe||"h"][0],
    metier:m.id,niveau:m.debut||0,emploi:m.id!=="sans",
    diplome:0,etude:null,merite:55,redoublements:0,retraite:false,
    annee:2026,mois:6,age:CFG.ageDepart,moisJoues:0,generation:1,village:"fomboni",
    argent:CFG.argentDepart,patrimoine:[],entreprises:[],
    sante:92,energie:88,bonheur:72,spirit:60,reput:25,xp:0,
    tontine:0,internet:false,ordinateur:false,maison:false,villa:false,moto:false,
    unions:[],fiance:null,enfants:[],grandMariage:false,
    confort:"normal",salairePDG:CFG.pdgMin,dernierNetBiz:0,
    loisirsMois:-1,loisirsFaits:0,loisirsUniques:[],
    eco:{tour:1,infl:0},partages:0,partMois:-1,pseudo:null,_recents:[],
    testament:{biz:{},maison:null,argent:"egal"},
    selfMade:false,lignee:[],
    histoire:[{t:"🌅 "+nom+" "+ (famille||"") +" a "+CFG.ageDepart+" ans et commence sa vie à Fomboni.",age:CFG.ageDepart,an:2026}],
    maj:Date.now()};
}

function migrer(s){
  if(s.v===4)return s;
  var n=nouveauJeu(s.nom,s.metier&&byId(METIERS,s.metier)?s.metier:"sans",s.sexe||"h",s.avatar);
  ["niveau","emploi","annee","mois","age","moisJoues","generation","village","argent","patrimoine",
   "entreprises","sante","energie","bonheur","spirit","reput","xp","tontine","internet","ordinateur",
   "maison","villa","moto","fiance","enfants","grandMariage","eco","partages","partMois","pseudo",
   "histoire","confort","salairePDG","dernierNetBiz","loisirsUniques"]
    .forEach(function(k){if(s[k]!==undefined)n[k]=s[k];});
  /* conjoint unique (v1→v3) → tableau d'unions */
  n.unions=[];
  if(s.conjoint&&s.conjoint.nom)n.unions.push({nom:s.conjoint.nom,type:s.grandMariage?"anda":"simple",
    bonheur:80,biz:!!s.conjointBiz,divorce:false,depuisAn:s.annee||2026});
  /* les enfants n'avaient pas de mère ni de talent */
  (n.enfants||[]).forEach(function(e){
    if(e.mere===undefined)e.mere=n.unions.length?n.unions[0].nom:"—";
    if(e.talent===undefined)e.talent=25+Math.floor(Math.random()*60);
    if(e.diplome===undefined)e.diplome=e.etudes?2:0;
  });
  (n.entreprises||[]).forEach(function(b){if(b.caisse===undefined)b.caisse=0;if(b.gerant===undefined)b.gerant=null;});
  n.testament={biz:{},maison:null,argent:"egal"};
  n.v=4;n.maj=Date.now();
  n.histoire.unshift({t:"✨ Ton monde s'agrandit : LES ÉTUDES, les foyers multiples, les gérants et LE TESTAMENT sont arrivés. Va voir 🎓 Études et 📜 Testament.",age:n.age,an:n.annee});
  return n;
}
function byId(arr,id){return arr.find(function(x){return x.id===id});}
function metierOf(){return byId(METIERS,L.metier)||METIERS[0];}
function villageOf(){return byId(VILLAGES,L.village)||VILLAGES[0];}
function bonusVillage(tag){var b=villageOf().bonus||{};return b[tag]||1;}
function cursusOf(id){return byId(CURSUS,id);}

/* ---------------- SAUVEGARDE ---------------- */
var cloudEtat="⏳";
function cloudOK(){try{return typeof sb!=="undefined"&&sb&&typeof CLOUD!=="undefined"&&CLOUD;}catch(e){return false;}}
function sauver(){
  if(!L)return;
  L.maj=Date.now();
  try{localStorage.setItem("mg_life",JSON.stringify(L));}catch(e){}
  majSaveBadge("💾 sauvegardé");
  cloudPush();
}
var _cloudTmr=null;
function cloudPush(){
  clearTimeout(_cloudTmr);
  _cloudTmr=setTimeout(function(){
    if(!cloudOK()){cloudEtat="📴 hors ligne";majSaveBadge();return;}
    try{
      (typeof ensureUid==="function"?ensureUid():Promise.resolve(null)).then(function(uid){
        if(!uid){cloudEtat="📴 local";majSaveBadge();return;}
        sb.from("life_saves").upsert({user_id:uid,save:L,maj:new Date().toISOString()},{onConflict:"user_id"})
          .then(function(r){cloudEtat=r&&r.error?"⚠️ cloud":"☁️ cloud ✓";majSaveBadge();},function(){cloudEtat="⚠️ cloud";majSaveBadge();});
      });
    }catch(e){cloudEtat="⚠️ cloud";majSaveBadge();}
  },1200);
}
function majSaveBadge(){var b=elRoot&&elRoot.querySelector("#mgl-save");if(b)b.textContent=cloudEtat;}
function cloudEffacer(){   // « Recommencer » efface AUSSI le cloud (sinon l'ancienne vie ressusciterait)
  if(!cloudOK())return;
  try{
    (typeof sbUid==="function"?sbUid():Promise.resolve(null)).then(function(uid){
      if(uid)sb.from("life_saves").delete().eq("user_id",uid).then(function(){},function(){});
    });
  }catch(e){}
}
function chargerLocal(){try{var s=JSON.parse(localStorage.getItem("mg_life")||"null");if(s&&s.v>=1&&s.v<=4)return migrer(s);}catch(e){}return null;}
function cloudPull(cb){
  if(!cloudOK())return cb(null);
  try{
    (typeof sbUid==="function"?sbUid():Promise.resolve(null)).then(function(uid){
      if(!uid)return cb(null);
      sb.from("life_saves").select("save").eq("user_id",uid).maybeSingle().then(function(r){
        var s=r&&r.data&&r.data.save;cb(s&&s.v>=1&&s.v<=4?migrer(s):null);
      },function(){cb(null);});
    });
  }catch(e){cb(null);}
}

/* ---------------- OUTILS ---------------- */
function fmt(n){return (Math.round(n)||0).toLocaleString("fr-FR")+" KMF";}
function clamp(v){return Math.max(0,Math.min(100,Math.round(v)));}
function alerte(m){try{alert(m);}catch(e){}}
function bouge(e){
  if(!e)return;
  if(e.argent)L.argent+=e.argent;
  if(e.sante)L.sante=clamp(L.sante+e.sante);
  if(e.energie)L.energie=clamp(L.energie+e.energie);
  if(e.bonheur)L.bonheur=clamp(L.bonheur+e.bonheur);
  if(e.spirit)L.spirit=clamp(L.spirit+e.spirit);
  if(e.reput)L.reput=clamp(L.reput+e.reput);
  if(e.merite)L.merite=clamp(L.merite+e.merite);
  if(e.xp)L.xp+=e.xp;
  if(e._tontine)L.tontine++;
  if(e._risque&&Math.random()<0.35){L.sante=clamp(L.sante-12);L.argent-=8000;L._msgRisque="⚠️ Le risque s'est retourné contre toi : −12 santé, −8 000 KMF.";}
}
/* Journal de vie : chaque entrée garde l'âge et l'année */
function hist(t,k){L.histoire.unshift({t:t,age:L.age,an:L.annee,k:k||null});if(L.histoire.length>140)L.histoire.length=140;}
function ciel(mois){return (mois>=10||mois<=2)?"linear-gradient(160deg,#16294a 0%,#24456b 45%,#376a8c 100%)":"linear-gradient(160deg,#0c1f3c 0%,#123c66 45%,#1d6a91 100%)";}
function saison(mois){return (mois>=10||mois<=2)?"🌧️ saison des pluies":"☀️ saison sèche";}
function moisRamadan(annee){var base=2,dec=Math.floor((annee-2026)/3);return ((base-dec)%12+12)%12;}
function feteDuMois(){
  var r=moisRamadan(L.annee);
  if(L.mois===r)return FETES.ramadan;
  if(L.mois===(r+1)%12)return FETES.aidFitr;
  if(L.mois===(r+3)%12)return FETES.aidKebir;
  if(L.mois===6)return FETES.fete_nat;
  return null;
}
function merReelle(){
  try{if(typeof seaForDate==="function"&&typeof d==="function"){var s=seaForDate(d(0));if(s&&s.level>=0)return s.level;}}catch(e){}
  return null;
}
function caisseTotale(){return L.entreprises.reduce(function(s,b){return s+(b.caisse||0)},0);}
function patrimoineTotal(){
  var t=L.argent+caisseTotale();
  if(L.maison)t+=CFG.maison.p;if(L.villa)t+=CFG.villa.p;if(L.moto)t+=500000;if(L.ordinateur)t+=100000;
  L.entreprises.forEach(function(b){var dd=byId(BIZ,b.type);if(dd)t+=dd.prix+(b.niv-1)*dd.prix*0.5;});
  return Math.round(t);
}
function pdgMax(){return CFG.pdgMin+Math.round(Math.max(0,L.dernierNetBiz)*CFG.pdgPartActivite);}
/* Agrandir coûte de plus en plus cher : chaque niveau rapporte autant que le
   précédent, mais coûte davantage. Sans ça, réinvestir la caisse suffit à
   faire exploser l'empire à l'infini. */
function coutAgrandir(t,niv){return Math.round(t.prix*0.6*niv*(1+L.eco.infl));}
function enfantsVivants(){return L.enfants.filter(function(e){return !e.parti;});}
function heritiersPossibles(){return enfantsVivants().filter(function(e){return e.age>=16;});}

/* ---------------- 🎓 LES ÉTUDES ---------------- */
function cursusDispo(){
  return CURSUS.filter(function(c){
    if(L.diplome<c.req)return false;
    if(c.don!==null&&L.diplome>=c.don)return false;      // déjà obtenu
    if(L.age<c.ageMin||L.age>c.ageMax)return false;
    return true;
  });
}
function inscrire(c){
  L.etude={id:c.id,reste:c.mois,total:c.mois};
  L.merite=Math.max(40,Math.min(70,L.merite));
  L.emploi=false;
  hist("🎓 Inscription : "+c.n+" ("+c.mois+" mois, "+fmt(c.cout)+"/mois).");
  bouge({bonheur:6,energie:-4});
}
function moisEtudes(){
  if(!L.etude)return;
  var c=cursusOf(L.etude.id);if(!c){L.etude=null;return;}
  var cout=Math.round(c.cout*(1+L.eco.infl));
  L.argent-=cout;
  L.etude.reste--;
  /* le mérite dépend de la forme, du moral, du matériel et du village */
  var dm=0;
  dm+=L.energie>55?2:(L.energie<30?-3:0);
  dm+=L.bonheur>55?1:(L.bonheur<30?-2:0);
  if(L.ordinateur)dm+=1;
  if(L.internet)dm+=1;
  dm+=Math.round((villageOf().etudes||1)-1);
  dm+=Math.random()<0.5?1:-1;
  L.merite=clamp(L.merite+dm);
  L.energie=clamp(L.energie-5);
  /* bourse au mérite, sinon petits boulots */
  if(L.merite>=75){L.argent+=CFG.bourse;hist("🏅 Bourse au mérite : +"+fmt(CFG.bourse));}
  else{L.argent+=CFG.petitBoulot;}
  hist("📚 "+c.n+" — "+L.etude.reste+" mois restants · mérite "+L.merite+"/100 · −"+fmt(cout));
  if(L.etude.reste<=0)diplomer(c);
}
function diplomer(c){
  if(L.merite<30){
    L.redoublements++;
    if(L.redoublements>=3){
      hist("😞 Trois échecs de suite : tu abandonnes "+c.n+". Il faudra gagner sa vie autrement.");
      L.etude=null;L.redoublements=0;bouge({bonheur:-14,reput:-4});
      return;
    }
    L.etude.reste=8;
    hist("📕 Échec aux examens — tu redoubles (8 mois de plus). Repose-toi et remonte ton mérite.");
    bouge({bonheur:-10});
    return;
  }
  var mn=mention(L.merite);
  L.etude=null;L.redoublements=0;
  if(c.don!==null){
    L.diplome=Math.max(L.diplome,c.don);
    hist("🎓 DIPLÔMÉ ! "+DIPLOMES[L.diplome]+" obtenu, "+mn.t+". De nouveaux métiers s'ouvrent à toi.");
    bouge({bonheur:22,reput:6+mn.b*3,spirit:4});
  }else{
    L.niveau=Math.min(L.niveau+(c.bonusNiv||1),metierOf().niveaux.length-1);
    hist("🛠️ Formation terminée ("+mn.t+") — tu montes d'un niveau dans ton métier.");
    bouge({bonheur:12,reput:3});
  }
  L._diplomeFrais=true;
}
/* niveau de départ offert par le diplôme quand on prend un métier */
function niveauDepart(m){
  var n=m.debut||0;
  if(L.diplome>=m.reqDip+1)n+=1;
  if(L.diplome>=m.reqDip+2)n+=1;
  return Math.min(n,m.niveaux.length-1);
}

/* ---------------- LE MOIS ---------------- */
function salaireDuMois(mer){
  if(!L.emploi||L.etude)return{montant:0,note:""};
  var m=metierOf(),sal=m.niveaux[L.niveau].sal,note="";
  if(m.freelance){
    var base=L.ordinateur?(L.internet?40000:20000):6000;
    sal=Math.round(base*(1+L.niveau*0.9)*(0.5+Math.random()));
    note=L.ordinateur?(L.internet?"":" (sans internet, dur de trouver des contrats)"):" (sans ordinateur, presque impossible)";
  }else if(m.variable){sal=Math.round(sal*(0.7+Math.random()*0.6));}
  else if(m.meteoSensible){
    if(mer!=null){if(mer>=2){sal=Math.round(sal*0.7);note=" (mer agitée — la VRAIE mer de Mohéli 🌊)";}else if(mer===0){sal=Math.round(sal*1.15);note=" (mer calme — la VRAIE mer de Mohéli 🌊)";}}
    else{var r=Math.random();if(r<0.2){sal=Math.round(sal*0.6);note=" (mer difficile)";}else if(r>0.85){sal=Math.round(sal*1.25);note=" (mer magnifique !)";}}
  }
  if(m.saisonSensible){if(L.mois>=6&&L.mois<=9){sal=Math.round(sal*1.3);note=" (haute saison 🐋)";}else if(L.mois<=2){sal=Math.round(sal*0.75);note=" (basse saison)";}}
  sal=Math.round(sal*bonusVillage(m.tag)*L.eco.tour);
  /* les salaires suivent le coût de la vie — sinon 40 ans d'inflation ruinent
     mécaniquement tous ceux qui vivent d'un salaire */
  sal=Math.round(sal*(1+L.eco.infl));
  if(L.diplome>0){sal=Math.round(sal*(1+CFG.diplomeSalaire*L.diplome));note+=" ("+DIPLOME_IC[L.diplome]+" "+DIPLOMES[L.diplome]+")";}
  if(L.selfMade)sal=Math.round(sal*CFG.selfMadeBonus);
  return {montant:sal,note:note};
}
/* Les entreprises versent dans leur CAISSE ; le PDG se paie un SALAIRE (réglable). */
function revenusEntreprises(mer){
  var lignes=[],netTotal=0;
  /* 🏢 se consacrer à 100 % à l'entreprise, ça se voit dans les comptes */
  var focus=(!L.emploi&&!L.etude&&!L.retraite)?CFG.pdgPleinTemps:1;
  L.entreprises.forEach(function(b){
    if(b.caisse===undefined)b.caisse=0;
    var t=byId(BIZ,b.type);if(!t)return;
    var ger=b.gerant?L.enfants.filter(function(e){return e.nom===b.gerant&&!e.parti;})[0]:null;
    var mGer=ger?(CFG.gerantBonus+(ger.talent/500)+(ger.diplome*0.04)):1;
    var brut;
    if(b.type==="startup"){
      // la tech BRÛLE au début, explose ensuite — sans plafond
      if(b.niv<3){brut=Math.random()<0.3?Math.round(80000*b.niv*Math.random()):0;}
      else{brut=Math.random()<0.22?Math.round(1000000*b.niv*(1+Math.random()*4)):Math.round(120000*b.niv*Math.random());}
      brut=Math.round(brut*focus*mGer);
      var chS=250000*b.niv+b.emp*CFG.salaireEmploye;   // serveurs + ingénieurs : ça coûte
      var netS=Math.round(brut-chS);
      b.caisse+=netS;netTotal+=netS;
      lignes.push({n:t.ic+" "+t.n+" (niv."+b.niv+")",v:netS});
      return;
    }
    brut=t.rev*b.niv*(1+0.25*b.emp)*bonusVillage(t.tag);
    if(t.tag==="tourisme")brut*=L.eco.tour*(L.mois>=6&&L.mois<=9?1.3:(L.mois<=2?0.75:1));
    if(t.tag==="mer"&&mer!=null)brut*=(mer>=2?0.65:(mer===0?1.15:1));
    if(t.tag==="terre")brut*=(L.mois>=10||L.mois<=2)?1.15:1;
    if(b.pub>0){brut*=1.5;b.pub--;}
    brut*=focus*mGer*(1+L.eco.infl);                // les prix de vente suivent le coût de la vie
    if(metierOf().bizSavvy&&L.emploi)brut*=1.08;    // 📊 le gestionnaire sait tenir des comptes
    var charges=Math.round((b.emp*CFG.salaireEmploye+Math.round(t.prix*0.008))*(1+L.eco.infl));
    var net=Math.round(Math.min(brut,CFG.bizCapMois)-charges);   // ⛔ plafond 15 M/mois (hors tech)
    b.caisse+=net;netTotal+=net;
    lignes.push({n:t.ic+" "+t.n+(b.emp?" ("+b.emp+" emp.)":"")+(ger?" · 🧑🏾‍💼 "+ger.nom:""),v:net});
  });
  // salaire du PDG : prélevé sur les caisses positives
  var pdg=0;
  if(L.entreprises.length){
    var souhait=Math.min(L.salairePDG||CFG.pdgMin,pdgMax());
    var dispo=L.entreprises.reduce(function(s,b){return s+Math.max(0,b.caisse)},0);
    pdg=Math.min(souhait,dispo);
    var reste=pdg;
    L.entreprises.forEach(function(b){if(reste<=0)return;var take=Math.min(Math.max(0,b.caisse),reste);b.caisse-=take;reste-=take;});
    L.argent+=pdg;
  }
  unionsActives().forEach(function(u){
    if(u.biz){L.argent+=15000;lignes.push({n:"🧵 Commerce de "+u.nom,v:15000,_direct:true});}
  });
  L.dernierNetBiz=Math.max(0,netTotal);
  return {lignes:lignes,pdg:pdg,focus:focus>1};
}
function depensesDuMois(){
  var conf=CFG.confort[L.confort]||CFG.confort.normal;
  var inflation=(1+L.eco.infl)*conf.m,lignes=[],total=0;
  CFG.depenses.forEach(function(dd){var v=Math.round(dd.base*inflation);lignes.push({n:dd.n,v:v});total+=v;});
  if(!L.maison&&!L.villa){var lo=Math.round(CFG.loyer*(1+L.eco.infl));lignes.push({n:"🏠 Loyer",v:lo});total+=lo;}
  if(L.maison){lignes.push({n:"🏠 Entretien maison",v:CFG.maison.entretien});total+=CFG.maison.entretien;}
  if(L.villa){lignes.push({n:"🏖️ Entretien villa",v:CFG.villa.entretien});total+=CFG.villa.entretien;}
  if(L.internet){lignes.push({n:"🌐 Internet",v:CFG.internet});total+=CFG.internet;}
  var nu=unionsActives().length;
  if(nu){var cf=nu*CFG.foyerCout;lignes.push({n:(nu>1?"💑 Deux foyers":"💑 Foyer"),v:cf});total+=cf;}
  var nKids=L.enfants.filter(function(e){return !e.parti&&!e.travaille&&!e.gerant;}).length;
  if(nKids){var ck=nKids*CFG.enfantCout;lignes.push({n:"👧 Enfants ×"+nKids,v:ck});total+=ck;}
  var etudiants=L.enfants.filter(function(e){return e.etudes&&e.age<=22&&!e.parti;}).length;
  if(etudiants){var ce=Math.round(etudiants*60000/12);lignes.push({n:"🎓 Études des enfants ×"+etudiants,v:ce});total+=ce;}
  if(L.mois===8){var scolaires=L.enfants.filter(function(e){return e.age>=5&&e.age<18&&!e.parti;}).length;
    if(scolaires){var cs=scolaires*CFG.ecoleRentree;lignes.push({n:"🎒 Rentrée scolaire ×"+scolaires,v:cs});total+=cs;}}
  var tdv=Math.min(Math.round((L.argent>0?L.argent:0)*CFG.trainDeVie),CFG.trainDeVieMax);
  if(tdv>2000){lignes.push({n:"✨ Train de vie ("+conf.n+")",v:tdv});total+=tdv;}
  return {lignes:lignes,total:total,conf:conf};
}
function tirerEvenement(){
  for(var i=0;i<FAM_EVENTS.length;i++){
    var f=FAM_EVENTS[i];
    try{if(f.cond()&&Math.random()<f.p&&(L._recents||[]).indexOf(f.id)<0)return f;}catch(e){}
  }
  if(L.tontine>=6){L.tontine=0;return byId(EVENTS,"tontine_gain");}
  if(L.etude&&Math.random()<0.45){
    var ecole=["exam_blanc","prof_remarque","greve_fac"];
    return byId(EVENTS,ecole[Math.floor(Math.random()*ecole.length)]);
  }
  if(L.metier==="dev"&&L.emploi&&L.ordinateur&&Math.random()<0.35)return byId(EVENTS,"contrat_dev");
  var recents=L._recents||[];
  var pool=EVENTS.filter(function(e){
    if(!e.p)return false;
    if(e.pour&&(e.pour.indexOf(L.metier)<0||!L.emploi))return false;
    if(recents.indexOf(e.id)>=0)return false;
    return true;
  });
  if(!pool.length)pool=EVENTS.filter(function(e){return e.p>0;});
  var tot=pool.reduce(function(s,e){return s+e.p},0),r=Math.random()*tot,ev=pool[0];
  for(var j=0;j<pool.length;j++){r-=pool[j].p;if(r<=0){ev=pool[j];break;}}
  return ev;
}
function verifierPromotion(){
  if(!L.emploi||L.etude)return null;
  var m=metierOf(),seuil=(L.niveau+1)*24;
  if(L.niveau<m.niveaux.length-1&&L.xp>=seuil){L.niveau++;L.xp=0;var t=m.niveaux[L.niveau].t;hist("🎉 PROMOTION : te voilà "+t+" !");return t;}
  return null;
}
function verifierMort(){
  var p=0;
  if(L.age>=62)p+=(L.age-60)*0.008;
  if(L.sante<15&&L.age>45)p+=0.02;
  return Math.random()<p;
}
/* les enfants grandissent : diplômes, départs, autonomie */
function grandirEnfants(){
  L.enfants.forEach(function(e){
    if(e.parti)return;
    if(e.etudes&&e.age===23){e.etudes=false;e.travaille=true;e.diplome=2+(e.talent>=70?1:0);
      hist("🎓 "+e.nom+" est diplômé(e) ("+DIPLOMES[e.diplome]+") et trouve un bon travail !");bouge({bonheur:6,reput:3});}
    if(e.age===26&&!e.gerant&&!e.travaille&&!e.etudes&&Math.random()<0.4){
      e.parti=true;hist("🚪 "+e.nom+" quitte Mohéli pour tenter sa chance ailleurs.");bouge({bonheur:-6});}
  });
}

/* ---------------- CSS (v100 : design refondu) ---------------- */
var CSS=
"#mgl-root{position:fixed;inset:0;z-index:99990;background:#081326;color:#eef4ff;font-family:inherit;display:flex;flex-direction:column;overflow:hidden;-webkit-tap-highlight-color:transparent}"+
"#mgl-root *{box-sizing:border-box;margin:0;padding:0}"+
"#mgl-sky{position:absolute;inset:0;transition:background 1.2s ease}"+
/* ✨ ciel étoilé animé — la nuit tropicale */
"#mgl-stars{position:absolute;inset:0;pointer-events:none;opacity:.55;"+
 "background-image:radial-gradient(1.4px 1.4px at 12% 18%,#fff,transparent),radial-gradient(1.2px 1.2px at 34% 9%,#fff,transparent),"+
 "radial-gradient(1.6px 1.6px at 58% 22%,#fff,transparent),radial-gradient(1.1px 1.1px at 78% 12%,#fff,transparent),"+
 "radial-gradient(1.3px 1.3px at 88% 30%,#fff,transparent),radial-gradient(1.2px 1.2px at 22% 38%,#fff,transparent),"+
 "radial-gradient(1.5px 1.5px at 68% 42%,#fff,transparent);animation:mgltwinkle 5.5s ease-in-out infinite}"+
"@keyframes mgltwinkle{0%,100%{opacity:.28}50%{opacity:.7}}"+
"#mgl-waves{position:absolute;left:0;right:0;bottom:0;height:150px;pointer-events:none;"+
 "background:radial-gradient(130% 80% at 50% 135%,rgba(46,155,214,.5),transparent 70%)}"+
/* barre du HAUT sticky : identité à gauche, argent toujours visible */
"#mgl-top{position:relative;z-index:5;display:none;padding:9px 12px 8px;background:rgba(7,15,32,.8);border-bottom:1px solid rgba(255,255,255,.09);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px)}"+
".mgl-tprow{display:flex;align-items:center;gap:9px}"+
".mgl-tpav{font-size:27px;flex:none;filter:drop-shadow(0 2px 6px rgba(0,0,0,.4))}"+
".mgl-tpid{flex:1;min-width:0}"+
".mgl-tpnom{font-weight:900;font-size:14.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;letter-spacing:.2px}"+
".mgl-tpsub{font-size:11px;opacity:.72;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"+
".mgl-tpargent{font-size:19.5px;font-weight:900;color:#F6BC1C;white-space:nowrap;text-shadow:0 2px 10px rgba(246,188,28,.28)}"+
".mgl-wrap{position:relative;flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:12px 14px 20px;max-width:540px;margin:0 auto;width:100%}"+
/* cartes en verre, avec un filet lumineux en haut */
".mgl-glass{position:relative;background:linear-gradient(180deg,rgba(255,255,255,.085),rgba(255,255,255,.05));"+
 "border:1px solid rgba(255,255,255,.13);border-radius:20px;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);"+
 "padding:15px;margin-bottom:12px;box-shadow:0 12px 34px rgba(0,0,0,.28)}"+
".mgl-glass::before{content:'';position:absolute;top:0;left:16px;right:16px;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.32),transparent)}"+
".mgl-glass.or{border-color:rgba(246,188,28,.34)}"+
".mgl-x{background:rgba(255,255,255,.12);border:none;color:#fff;width:32px;height:32px;border-radius:11px;font-size:15px;cursor:pointer;flex:none}"+
".mgl-title{font-weight:900;font-size:17px}"+
".mgl-sub{font-size:11.5px;opacity:.75;line-height:1.5}"+
".mgl-h{font-weight:900;font-size:14px;letter-spacing:.2px;display:block;margin-bottom:2px}"+
".mgl-bar{height:7px;border-radius:99px;background:rgba(255,255,255,.12);overflow:hidden;margin-top:4px}"+
".mgl-bar>i{display:block;height:100%;border-radius:99px;transition:width .7s cubic-bezier(.3,1,.4,1)}"+
".mgl-stats{display:grid;grid-template-columns:1fr 1fr;gap:9px 14px;font-size:11.5px}"+
".mgl-btn{width:100%;border:none;border-radius:16px;padding:15px;font-size:15.5px;font-weight:900;cursor:pointer;color:#fff;"+
 "background:linear-gradient(135deg,#12A468,#0E9BB5);box-shadow:0 8px 24px rgba(18,158,99,.36);transition:transform .12s}"+
".mgl-btn:active{transform:scale(.975)}"+
".mgl-btn.ghost{background:rgba(255,255,255,.1);box-shadow:none;font-weight:700;font-size:13px;padding:11px}"+
".mgl-btn.or{background:linear-gradient(135deg,#F6BC1C,#E08A16);box-shadow:0 8px 24px rgba(246,188,28,.32);color:#20160a}"+
".mgl-btn.danger{background:linear-gradient(135deg,#b0413a,#8d2f2f);box-shadow:none}"+
".mgl-choice{display:block;width:100%;text-align:left;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.07);color:#fff;"+
 "border-radius:14px;padding:13px;font-size:13.5px;margin-top:8px;cursor:pointer;transition:background .15s,transform .12s}"+
".mgl-choice:active{background:rgba(255,255,255,.18);transform:scale(.99)}"+
".mgl-job{display:flex;gap:11px;align-items:center;border:1px solid rgba(255,255,255,.14);background:rgba(255,255,255,.06);"+
 "border-radius:16px;padding:12px;margin-bottom:9px;cursor:pointer;transition:background .15s}"+
".mgl-job:active{background:rgba(255,255,255,.15)}"+
".mgl-job.off{opacity:.42}"+
".mgl-job .ic{font-size:26px;flex:none}"+
".mgl-line{display:flex;justify-content:space-between;gap:10px;font-size:12.5px;padding:3px 0}"+
".mgl-badge{display:inline-block;background:rgba(246,188,28,.18);border:1px solid rgba(246,188,28,.4);color:#F6BC1C;border-radius:99px;padding:2px 10px;font-size:10.5px;font-weight:800;margin-left:6px;vertical-align:middle}"+
".mgl-badge.v{background:rgba(74,222,128,.15);border-color:rgba(74,222,128,.4);color:#4ade80}"+
".mgl-badge.b{background:rgba(56,189,248,.15);border-color:rgba(56,189,248,.4);color:#38bdf8}"+
".mgl-in{width:100%;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;border-radius:12px;padding:12px;font-size:14px;margin-top:8px}"+
".mgl-in::placeholder{color:rgba(255,255,255,.4)}"+
"select.mgl-in{appearance:none;-webkit-appearance:none}"+
"select.mgl-in option{background:#12203c;color:#fff}"+
".mgl-av{display:inline-flex;width:52px;height:52px;border-radius:16px;background:rgba(255,255,255,.1);border:2px solid transparent;font-size:30px;align-items:center;justify-content:center;cursor:pointer;margin:4px 6px 0 0}"+
".mgl-av.on{border-color:#F6BC1C;background:rgba(246,188,28,.15)}"+
/* 📖 le JOURNAL DE VIE */
".mgl-jsep{text-align:center;color:#F6BC1C;font-weight:900;font-size:12px;letter-spacing:1.6px;margin:15px 0 4px;position:relative}"+
".mgl-jline{font-size:13px;line-height:1.55;padding:4px 0;border-bottom:1px dashed rgba(255,255,255,.07)}"+
".mgl-jline.mois{opacity:.6;font-size:11px;font-weight:800;letter-spacing:.4px;margin-top:8px;border-bottom:none;text-transform:uppercase}"+
/* ❤️⚡😊🕌 les 4 stats FIXES au-dessus de la nav */
"#mgl-stbar{position:relative;z-index:5;display:none;gap:10px;padding:7px 14px;background:rgba(7,15,32,.86);border-top:1px solid rgba(255,255,255,.07);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}"+
"#mgl-stbar .st{flex:1;display:flex;align-items:center;gap:5px;font-size:12px}"+
"#mgl-stbar .st .mgl-bar{flex:1;margin-top:0}"+
/* la NAVIGATION du bas */
"#mgl-nav{position:relative;z-index:5;display:none;align-items:stretch;background:rgba(5,11,24,.96);border-top:1px solid rgba(255,255,255,.07);padding:7px 4px calc(8px + env(safe-area-inset-bottom))}"+
"#mgl-nav button{flex:1;background:none;border:none;color:#9fb4d8;font-size:19px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:2px;padding:5px 0 3px;border-radius:12px;transition:color .15s,background .15s}"+
"#mgl-nav button span{font-size:9.5px;font-weight:800;letter-spacing:.2px}"+
"#mgl-nav button.on{color:#F6BC1C;background:rgba(246,188,28,.09)}"+
"#mgl-navgap{width:86px;flex:none}"+
/* 🌙 LE BOUTON DU MOIS */
"#mgl-fab{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(14px + env(safe-area-inset-bottom));width:76px;height:76px;border-radius:50%;border:none;cursor:pointer;z-index:8;"+
 "background:linear-gradient(135deg,#12A468,#0E9BB5);color:#fff;box-shadow:0 10px 30px rgba(18,158,99,.5),0 0 0 6px rgba(255,255,255,.07);"+
 "display:none;flex-direction:column;align-items:center;justify-content:center;font-weight:900}"+
"#mgl-fab:active{transform:translateX(-50%) scale(.94)}"+
"#mgl-fab .lune{font-size:27px;line-height:1}"+
"#mgl-fab .lbl{font-size:9px;letter-spacing:.3px;margin-top:2px;opacity:.95}"+
"@keyframes mglpulse{0%,100%{box-shadow:0 10px 30px rgba(18,158,99,.5),0 0 0 6px rgba(255,255,255,.07)}50%{box-shadow:0 10px 34px rgba(18,158,99,.66),0 0 0 11px rgba(255,255,255,.045)}}"+
"#mgl-fab{animation:mglpulse 2.4s ease-in-out infinite}"+
/* 🎭 la POPUP d'événement */
"#mgl-modal{position:absolute;inset:0;z-index:20;display:none;align-items:flex-end;justify-content:center;background:rgba(3,8,20,.72);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);padding:14px}"+
"#mgl-modal.on{display:flex}"+
"#mgl-mbox{width:100%;max-width:480px;background:linear-gradient(180deg,rgba(22,38,68,.98),rgba(14,26,50,.98));border:1px solid rgba(255,255,255,.16);"+
 "border-radius:24px;padding:19px;margin-bottom:calc(10px + env(safe-area-inset-bottom));box-shadow:0 -12px 46px rgba(0,0,0,.55);max-height:82%;overflow-y:auto}"+
".mgl-mic{font-size:48px;text-align:center;line-height:1.1;filter:drop-shadow(0 4px 12px rgba(0,0,0,.4))}"+
"@keyframes mglpop{from{transform:translateY(16px);opacity:0}to{transform:none;opacity:1}}"+
".mgl-pop{animation:mglpop .34s cubic-bezier(.2,.9,.3,1)}"+
"@keyframes mglfade{from{opacity:0}to{opacity:1}}"+
".mgl-fade{animation:mglfade .4s ease}";

/* ---------------- UI ---------------- */
function esc2(s){var dv=document.createElement("div");dv.textContent=s==null?"":String(s);return dv.innerHTML;}
function barre(v,c){return '<div class="mgl-bar"><i style="width:'+clamp(v)+'%;background:'+c+'"></i></div>';}
function on(id,fn){var e=elRoot.querySelector("#"+id);if(e)e.onclick=fn;}
var jeuActif=false;

function titreActuel(){
  if(L.etude){var c=cursusOf(L.etude.id);return c?("🎓 "+c.n.split("→").pop().trim()):"🎓 Étudiant(e)";}
  if(L.retraite)return "🌅 Retraité(e)";
  if(!L.emploi)return "PDG"+(L.entreprises.length?" · "+L.entreprises.length+" entr.":" sans activité");
  return metierOf().niveaux[L.niveau].t;
}
function majTop(){
  if(!L)return;
  var m=metierOf(),v=villageOf();
  elRoot.querySelector("#mgl-top").innerHTML=
   '<div class="mgl-tprow">'+
   '<span class="mgl-tpav">'+(L.avatar||"👤")+'</span>'+
   '<div class="mgl-tpid"><div class="mgl-tpnom">'+esc2(L.nom)+' '+esc2(L.famille||"")+
     (L.grandMariage?' 👑':'')+(L.selfMade?' 💪':'')+
     (L.generation>1?' <span class="mgl-badge">'+L.generation+'ᵉ gén.</span>':'')+'</div>'+
   '<div class="mgl-tpsub">'+(L.etude?"🎓":m.ic)+' '+titreActuel()+' · '+L.age+' ans · '+v.ic+' '+v.n+
     (L.diplome>0?' · '+DIPLOME_IC[L.diplome]+' '+DIPLOMES[L.diplome]:'')+'</div></div>'+
   '<button class="mgl-x" id="mgl-plus" title="Plus">⋯</button><button class="mgl-x" id="mgl-close2">✕</button></div>'+
   '<div class="mgl-tprow" style="margin-top:4px">'+
   '<div class="mgl-tpargent">'+fmt(L.argent)+'</div>'+
   '<div class="mgl-sub" style="flex:1;text-align:right;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">🏦 '+fmt(patrimoineTotal())+(L.entreprises.length?' · 🏢 '+fmt(caisseTotale()):'')+' · <span id="mgl-save">'+cloudEtat+'</span></div></div>';
  on("mgl-plus",menuPlus);on("mgl-close2",fermer);
}
function majStats(){
  if(!L)return;
  elRoot.querySelector("#mgl-stbar").innerHTML=
   '<div class="st" title="Santé">❤️'+barre(L.sante,"#ef4444")+'</div>'+
   '<div class="st" title="Énergie">⚡'+barre(L.energie,"#f59e0b")+'</div>'+
   '<span style="width:64px;flex:none"></span>'+
   '<div class="st" title="Bonheur">😊'+barre(L.bonheur,"#22c55e")+'</div>'+
   '<div class="st" title="'+(L.etude?"Mérite scolaire":"Spiritualité")+'">'+(L.etude?"📚":"🕌")+barre(L.etude?L.merite:L.spirit,L.etude?"#a78bfa":"#38bdf8")+'</div>';
}
function majChrome(on){
  jeuActif=!!on;
  elRoot.querySelector("#mgl-top").style.display=on?"block":"none";
  elRoot.querySelector("#mgl-stbar").style.display=on?"flex":"none";
  elRoot.querySelector("#mgl-nav").style.display=on?"flex":"none";
  elRoot.querySelector("#mgl-fab").style.display=on?"flex":"none";
  elRoot.querySelector("#mgl-close").style.display=on?"none":"block";
}
function navActive(id){
  elRoot.querySelectorAll("#mgl-nav button").forEach(function(b){b.className=b.getAttribute("data-nav")===id?"on":"";});
}
function ecran(html){
  var w=elRoot.querySelector(".mgl-wrap");w.innerHTML=html;w.scrollTop=0;w.className="mgl-wrap mgl-fade";
  elRoot.querySelector("#mgl-sky").style.background=ciel(L?L.mois:6);
  if(L&&jeuActif){majTop();majStats();}
}
function modalOuvre(html){
  elRoot.querySelector("#mgl-mbox").innerHTML='<div class="mgl-pop">'+html+'</div>';
  elRoot.querySelector("#mgl-modal").className="on";
  elRoot.querySelector("#mgl-fab").style.display="none";
}
function modalFerme(){
  elRoot.querySelector("#mgl-modal").className="";
  elRoot.querySelector("#mgl-fab").style.display=jeuActif?"flex":"none";
}
function retour(){return '<button class="mgl-btn ghost" id="mgl-retour" style="margin-top:4px">← Retour au journal</button>';}

/* menu ⋯ */
function menuPlus(){
  modalOuvre('<div class="mgl-mic">🏝️</div><b style="display:block;text-align:center;font-size:16px;margin:6px 0 8px">Mohéli & plus</b>'+
   '<button class="mgl-choice" id="mgl-m-etu">🎓 Les études</button>'+
   '<button class="mgl-choice" id="mgl-m-test">📜 Mon testament</button>'+
   '<button class="mgl-choice" id="mgl-m-chro">📖 Les chroniques de la famille</button>'+
   '<button class="mgl-choice" id="mgl-m-vill">🗺️ Les villages de Mohéli</button>'+
   '<button class="mgl-choice" id="mgl-m-shop">🛒 Boutique & train de vie</button>'+
   '<button class="mgl-choice" id="mgl-m-class">🏆 Le classement</button>'+
   '<button class="mgl-choice" id="mgl-m-part">📣 Inviter des amis (+10 000 KMF)</button>'+
   '<button class="mgl-choice" id="mgl-m-x" style="text-align:center;opacity:.7">Fermer</button>');
  on("mgl-m-etu",function(){modalFerme();ecranEtudes();});
  on("mgl-m-test",function(){modalFerme();ecranTestament();});
  on("mgl-m-chro",function(){modalFerme();ecranChroniques();});
  on("mgl-m-vill",function(){modalFerme();ecranVillages();});
  on("mgl-m-shop",function(){modalFerme();ecranBoutique();});
  on("mgl-m-class",function(){modalFerme();ecranClassement();});
  on("mgl-m-part",function(){modalFerme();partager();});
  on("mgl-m-x",modalFerme);
}
function journalHTML(){
  var arr=L.histoire.slice(0,140).reverse(),h="",age=null;
  arr.forEach(function(e){
    if(typeof e==="string"){h+='<div class="mgl-jline">'+esc2(e)+'</div>';return;}
    if(e.age!=null&&e.age!==age){age=e.age;h+='<div class="mgl-jsep">— '+age+' ans · '+e.an+' —</div>';}
    h+='<div class="mgl-jline'+(e.k==="mois"?" mois":"")+'">'+esc2(e.t)+'</div>';
  });
  return h||'<div class="mgl-sub">Ta vie commence…</div>';
}

/* — accueil / création — */
function ecranAccueil(){
  majChrome(false);
  var save=chargerLocal();
  var h='<div style="text-align:center;padding:24px 0 8px" class="mgl-pop">'+
   '<div style="font-size:54px">🏝️</div><div style="font-size:25px;font-weight:900;margin:6px 0 2px">MoheliGo Life</div>'+
   '<div class="mgl-sub">Étudie, travaille, bâtis ton empire, fonde tes foyers —<br>et transmets tout à ceux qui viennent après toi.</div></div>';
  if(save){
    var m=byId(METIERS,save.metier)||METIERS[0];
    h+='<div class="mgl-glass or mgl-pop"><b>'+(save.avatar||m.ic)+' '+esc2(save.nom)+' '+esc2(save.famille||"")+'</b>'+
     '<span class="mgl-badge">'+MOIS[save.mois]+' '+save.annee+'</span>'+
     (save.generation>1?'<span class="mgl-badge">'+save.generation+'ᵉ génération</span>':'')+
     '<div class="mgl-sub" style="margin:6px 0 10px">'+save.age+' ans · '+fmt(save.argent)+
       (save.diplome>0?' · '+DIPLOME_IC[save.diplome]+' '+DIPLOMES[save.diplome]:'')+'</div>'+
     '<button class="mgl-btn" id="mgl-continuer">▶️ Continuer ma vie</button>'+
     '<button class="mgl-btn ghost" id="mgl-nouvelle" style="margin-top:8px">🔄 Recommencer une nouvelle vie</button></div>';
    ecran(h);
    on("mgl-continuer",function(){L=save;sauver();ecranJeu("Bon retour à Mohéli, "+esc2(L.nom)+" ! 🌺");});
    on("mgl-nouvelle",function(){if(confirm("Effacer cette vie et tout recommencer ? (la sauvegarde cloud sera effacée aussi)")){localStorage.removeItem("mg_life");cloudEffacer();L=null;ecranAccueil();}});
    return;
  }
  var sexe=window._mglSexe||"h";
  h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">1 · Qui es-tu ?</b>'+
   '<div style="display:flex;gap:8px;margin-top:8px">'+
   '<button class="mgl-btn'+(sexe==="h"?"":" ghost")+'" style="flex:1" id="mgl-sx-h">👨🏾 Homme</button>'+
   '<button class="mgl-btn'+(sexe==="f"?"":" ghost")+'" style="flex:1" id="mgl-sx-f">👩🏾 Femme</button></div>'+
   '<div style="margin-top:10px" id="mgl-avatars">'+AVATARS[sexe].map(function(a,i){return '<span class="mgl-av'+(i===(window._mglAv||0)?" on":"")+'" data-i="'+i+'">'+a+'</span>';}).join("")+'</div>'+
   '<input class="mgl-in" id="mgl-nom" maxlength="20" placeholder="Ton prénom…" value="'+esc2(window._mglNom||"")+'">'+
   '<input class="mgl-in" id="mgl-fam" maxlength="20" placeholder="Le nom de ta famille (facultatif)…" value="'+esc2(window._mglFam||"")+'">'+
   '<div class="mgl-sub" style="margin-top:6px">Ce nom traversera les générations : tes enfants et petits-enfants le porteront.</div></div>'+
   '<div class="mgl-glass mgl-pop"><b class="mgl-h">2 · Tu as 18 ans. Que fais-tu ?</b>'+
   '<div class="mgl-sub" style="margin-bottom:8px">C\'est LE choix qui décide de tout le reste : le diplôme ouvre les grands métiers, mais il coûte des années et de l\'argent.</div>'+
   '<button class="mgl-choice" id="mgl-voie-etu"><b>🎓 Continuer mes études</b><div class="mgl-sub">Lycée → bac (24 mois, 9 000 KMF/mois). Pas de salaire, des petits boulots, une bourse si tu travailles bien. Puis licence, master, doctorat.</div></button>'+
   '<button class="mgl-choice" id="mgl-voie-job"><b>💼 Travailler tout de suite</b><div class="mgl-sub">Un salaire dès le premier mois. Tu pourras reprendre les études plus tard — ça coûtera juste plus cher.</div></button>'+
   '</div>';
  ecran(h);
  function memo(){
    var a=elRoot.querySelector("#mgl-nom"),b=elRoot.querySelector("#mgl-fam");
    window._mglNom=a?a.value:"";window._mglFam=b?b.value:"";
  }
  on("mgl-sx-h",function(){memo();window._mglSexe="h";window._mglAv=0;ecranAccueil();});
  on("mgl-sx-f",function(){memo();window._mglSexe="f";window._mglAv=0;ecranAccueil();});
  elRoot.querySelectorAll(".mgl-av").forEach(function(a){a.onclick=function(){
    window._mglAv=+a.getAttribute("data-i");
    elRoot.querySelectorAll(".mgl-av").forEach(function(x){x.className="mgl-av";});a.className="mgl-av on";};});
  function creer(voie){
    memo();
    var nom=(window._mglNom||"").trim();
    if(!nom){alerte("Écris ton prénom d'abord 😊");return null;}
    var sx=window._mglSexe||"h";
    L=nouveauJeu(nom,"sans",sx,AVATARS[sx][window._mglAv||0],(window._mglFam||"").trim());
    window._mglNom="";window._mglFam="";
    return L;
  }
  on("mgl-voie-etu",function(){
    if(!creer())return;
    inscrire(cursusOf("bac"));sauver();
    ecranJeu("🎓 Te voilà au lycée de Fomboni. Travaille bien : le mérite décide de ta mention, et la mention ouvre les portes.");
  });
  on("mgl-voie-job",function(){
    if(!creer())return;
    sauver();ecranChoixMetier(true);
  });
}

/* — choix du métier (au départ, ou plus tard) — */
function ecranChoixMetier(premier){
  majChrome(!premier);
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">💼 '+(premier?"Choisis ta voie":"Choisir un métier")+'</b>'+
   '<div class="mgl-sub">Tu as '+DIPLOME_IC[L.diplome]+' <b>'+DIPLOMES[L.diplome]+'</b>. Les métiers grisés demandent un diplôme que tu n\'as pas encore — les études restent ouvertes à tout âge.</div></div>'+
   '<div id="mgl-jobs"></div>'+(premier?'':retour());
  ecran(h);
  var jb=elRoot.querySelector("#mgl-jobs");
  metiersVisibles().forEach(function(m){
    if(!premier&&L.emploi&&m.id===L.metier)return;
    var bloque=L.diplome<m.reqDip;
    var sal=m.freelance?"revenus variables — le plus difficile":("~"+fmt(m.niveaux[0].sal)+" → "+fmt(m.niveaux[m.niveaux.length-1].sal));
    var dv=document.createElement("div");dv.className="mgl-job mgl-pop"+(bloque?" off":"");
    dv.innerHTML='<span class="ic">'+m.ic+'</span><div style="flex:1"><b>'+m.n+'</b>'+
      (m.type==="carriere"?'<span class="mgl-badge">GRANDE CARRIÈRE</span>':'')+
      (m.reqDip>0?'<span class="mgl-badge b">'+DIPLOMES[m.reqDip]+'</span>':'')+
      '<div class="mgl-sub">'+m.d+'</div><div class="mgl-sub" style="color:#F6BC1C">'+sal+'</div></div>';
    dv.onclick=function(){
      if(bloque){alerte("Il faut le "+DIPLOMES[m.reqDip]+" pour ce métier.\n\nVa dans ⋯ → 🎓 Les études.");return;}
      if(!premier&&!confirm((L.emploi?"Changer de métier pour":"Devenir")+" « "+m.n+" » ?"))return;
      var bonusNiv=(!premier&&L.niveau>0&&L.emploi)?1:0;
      L.metier=m.id;L.niveau=Math.max(niveauDepart(m),Math.min(bonusNiv,m.niveaux.length-1));
      L.xp=0;L.emploi=true;L.retraite=false;
      hist("💼 "+L.nom+" devient "+m.niveaux[L.niveau].t+" ("+m.n+").");
      bouge({bonheur:4,energie:-4});
      sauver();ecranJeu("💼 "+m.ic+" "+m.n+" — "+m.niveaux[L.niveau].t+". Bonne chance !");
    };
    jb.appendChild(dv);
  });
  if(!premier)on("mgl-retour",function(){ecranJeu();});
}

/* — écran principal : LE JOURNAL DE VIE — */
function ecranJeu(message){
  majChrome(true);navActive(null);
  var h="";
  if(message)h+='<div class="mgl-glass or mgl-pop">'+message+'</div>';
  if(L.etude){
    var c=cursusOf(L.etude.id),prog=Math.round((L.etude.total-L.etude.reste)*100/L.etude.total);
    h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">'+c.ic+' '+c.n+'</b>'+
      '<div class="mgl-sub">'+L.etude.reste+' mois restants · mérite '+L.merite+'/100 ('+mention(L.merite).t+')</div>'+
      barre(prog,"#a78bfa")+'</div>';
  }
  h+='<div class="mgl-glass" style="padding:15px 15px 10px"><b class="mgl-h">📖 Le journal de ta vie</b>'+
     '<div style="margin-top:2px">'+journalHTML()+'</div>'+
     '<div class="mgl-sub" style="text-align:center;margin-top:10px;opacity:.55">Appuie sur 🌙 pour vivre le mois suivant</div></div>';
  ecran(h);
  var w=elRoot.querySelector(".mgl-wrap");w.scrollTop=w.scrollHeight;
}

/* — vivre un mois — */
function jouerMois(){
  L.moisJoues++;L.mois++;
  if(L.mois>11){L.mois=0;L.annee++;}
  var anniv=L.moisJoues%12===0;
  if(anniv){L.age++;L.enfants.forEach(function(e){e.age++;});}
  hist("🗓️ "+MOIS[L.mois]+" "+L.annee+" · "+saison(L.mois),"mois");
  if(anniv)grandirEnfants();
  L.eco.tour=Math.max(0.75,Math.min(1.35,L.eco.tour+(Math.random()-0.48)*0.08));
  L.eco.infl+=CFG.inflationMois;
  var mo=L.annee*12+L.mois;
  if(L.loisirsMois!==mo){L.loisirsMois=mo;L.loisirsFaits=0;}
  var mer=merReelle();

  moisEtudes();                                    // 🎓 d'abord l'école
  var sal=salaireDuMois(mer);L.argent+=sal.montant;
  var biz=revenusEntreprises(mer);
  var dep=depensesDuMois();L.argent-=dep.total;

  var fatigueBiz=L.emploi?L.entreprises.length*4:Math.max(0,L.entreprises.length*2-2);
  L.entreprises.forEach(function(b){if(b.gerant)fatigueBiz=Math.max(0,fatigueBiz-2);});
  L.energie=clamp(L.energie-6-fatigueBiz+(L.moto?2:0)+(L.retraite?6:0));
  L.bonheur=clamp(L.bonheur-2+(villageOf().bonus.bonheur||0)+(dep.conf.bonheur||0));
  if(dep.conf.sante)L.sante=clamp(L.sante+dep.conf.sante);
  if(L.energie<25)L.sante=clamp(L.sante-6);
  if(L.emploi&&!L.etude)L.xp+=2;
  var m=metierOf();
  if(m.fatigue&&L.emploi)L.energie=clamp(L.energie-3*m.fatigue);
  if(m.reputation&&L.emploi)L.reput=clamp(L.reput+m.reputation);
  if(L.age>=55)L.sante=clamp(L.sante-1);
  /* l'équité entre foyers s'érode toute seule si on ne fait rien */
  if(unionsActives().length>=2)unionsActives().forEach(function(u,i){u.bonheur=clamp(u.bonheur-(i===0?1:2));});
  else if(unionsActives().length===1)unionsActives()[0].bonheur=clamp(unionsActives()[0].bonheur+1);
  var fete=feteDuMois();if(fete)bouge(fete.e);

  /* le bilan du mois s'écrit DANS le journal */
  if(sal.montant)hist("💵 Salaire"+sal.note+" : +"+fmt(sal.montant));
  var netBiz=0;
  biz.lignes.forEach(function(l){if(l._direct)hist(l.n+" : +"+fmt(l.v));else netBiz+=l.v;});
  if(L.entreprises.length)hist("🏢 Entreprises"+(biz.focus?" (PDG à plein temps +25 %)":"")+" : "+(netBiz>=0?"+":"−")+fmt(Math.abs(netBiz))+" dans les caisses");
  if(biz.pdg)hist("👔 Ton salaire de PDG : +"+fmt(biz.pdg));
  hist("💸 Dépenses du mois : −"+fmt(dep.total)+" · reste "+fmt(L.argent)+" en poche");
  if(mer!=null)hist("🌊 La vraie mer de Mohéli : "+(mer===0?"calme":(mer===1?"modérée":"agitée"))+" (météo MoheliGo en direct)");
  if(fete)hist(fete.ic+" "+fete.t+" — "+fete.d);
  verifierPromotion();
  /* la retraite, pour ceux qui ont un métier qui en donne une */
  if(!L.retraite&&L.emploi&&L.age>=62&&m.retraite){
    L.retraite=true;L.emploi=false;
    hist("🌅 Départ à la retraite après une carrière de "+m.n.toLowerCase()+". Pension : "+fmt(Math.round(m.niveaux[L.niveau].sal*0.55))+"/mois.");
    bouge({bonheur:8,energie:10});
  }
  if(L.retraite)L.argent+=Math.round(m.niveaux[L.niveau].sal*0.55*(1+L.eco.infl));
  if(L.sante<=0){L.argent-=20000;L.sante=35;L.energie=40;hist("🏥 Hospitalisé d'épuisement : 20 000 KMF de soins. Lève le pied (les 🎉 Loisirs aident) !");}
  if(L.argent<0)hist("🕳️ Tu es endetté — la boutique fait crédit… mais pas longtemps. Trouve vite des revenus !");

  if(verifierMort()){sauver();return ecranHeritage();}
  sauver();

  /* juste diplômé : on propose tout de suite le métier */
  if(L._diplomeFrais){
    L._diplomeFrais=false;
    ecranJeu();
    modalOuvre('<div class="mgl-mic">'+DIPLOME_IC[L.diplome]+'</div>'+
      '<b style="display:block;text-align:center;font-size:17px;margin:7px 0 3px">'+DIPLOMES[L.diplome]+' en poche !</b>'+
      '<div class="mgl-sub" style="text-align:center;margin-bottom:6px">De nouveaux métiers te sont ouverts. Tu peux aussi enchaîner sur le diplôme supérieur.</div>'+
      '<button class="mgl-choice" id="mgl-d-job">💼 Chercher un métier maintenant</button>'+
      '<button class="mgl-choice" id="mgl-d-etu">🎓 Continuer les études</button>'+
      '<button class="mgl-choice" id="mgl-d-x" style="text-align:center;opacity:.7">Plus tard</button>');
    on("mgl-d-job",function(){modalFerme();ecranChoixMetier(false);});
    on("mgl-d-etu",function(){modalFerme();ecranEtudes();});
    on("mgl-d-x",function(){modalFerme();ecranJeu();});
    return;
  }
  var ev=tirerEvenement();
  L._recents=[ev.id].concat(L._recents||[]).slice(0,3);
  ecranJeu();
  modalEvenement(ev);
}

/* — l'événement du mois, en POPUP — */
function modalEvenement(ev){
  var desc=typeof ev.d==="function"?ev.d():ev.d;
  modalOuvre('<div class="mgl-mic">'+ev.ic+'</div>'+
   '<b style="display:block;text-align:center;font-size:17px;margin:7px 0 3px">'+ev.t+'</b>'+
   '<div class="mgl-sub" style="text-align:center;margin-bottom:6px">'+desc+'</div><div id="mgl-choix"></div>');
  var cx=elRoot.querySelector("#mgl-choix");
  ev.choix.forEach(function(c){
    var b=document.createElement("button");b.className="mgl-choice";b.textContent=c.t;
    b.onclick=function(){
      var ok=true;
      if(c.f)ok=c.f();else bouge(c.e);
      if(ok===false)return;
      if(c.e)hist(ev.ic+" "+ev.t+" — "+c.t+".");
      if(L._msgRisque){hist(L._msgRisque);L._msgRisque=null;}
      sauver();modalFerme();ecranJeu();
    };
    cx.appendChild(b);
  });
}

/* ---------------- 🎓 ÉCRAN DES ÉTUDES ---------------- */
function ecranEtudes(){
  navActive(null);
  var h="";
  if(L.etude){
    var c=cursusOf(L.etude.id),prog=Math.round((L.etude.total-L.etude.reste)*100/L.etude.total);
    h+='<div class="mgl-glass or mgl-pop"><b class="mgl-h">'+c.ic+' '+c.n+'</b>'+
      '<div class="mgl-sub" style="margin:4px 0 6px">'+c.d+'</div>'+
      '<div class="mgl-line"><span>Avancement</span><b>'+(L.etude.total-L.etude.reste)+' / '+L.etude.total+' mois</b></div>'+barre(prog,"#a78bfa")+
      '<div class="mgl-line" style="margin-top:8px"><span>Mérite</span><b>'+L.merite+'/100 — '+mention(L.merite).t+'</b></div>'+barre(L.merite,"#F6BC1C")+
      '<div class="mgl-sub" style="margin-top:8px">Coût : '+fmt(c.cout)+'/mois. En dessous de 30 de mérite à la fin, tu redoubles. Au-dessus de 75, tu touches une bourse de '+fmt(CFG.bourse)+'/mois au lieu des petits boulots.</div>'+
      '<div class="mgl-sub" style="margin-top:6px">Ce qui fait monter le mérite : l\'énergie ⚡, le moral 😊, un ordinateur 💻, internet 🌐, et vivre à Fomboni 🏙️.</div>'+
      '<button class="mgl-btn danger" id="mgl-abandon" style="margin-top:10px">✋ Abandonner mes études</button></div>';
  }else{
    h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">🎓 Ton parcours</b>'+
      '<div class="mgl-line"><span>Diplôme actuel</span><b>'+DIPLOME_IC[L.diplome]+' '+DIPLOMES[L.diplome]+'</b></div>'+
      '<div class="mgl-sub" style="margin-top:6px">Chaque diplôme ajoute +'+Math.round(CFG.diplomeSalaire*100)+' % de salaire, ouvre de nouveaux métiers, et te fait démarrer plus haut dans la hiérarchie.</div></div>';
    var dispo=cursusDispo();
    h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">📚 S\'inscrire</b>'+
      (dispo.length?'':'<div class="mgl-sub">Rien de disponible pour toi en ce moment — soit tu as déjà tout obtenu, soit c\'est une question d\'âge.</div>')+
      '<div id="mgl-cursus" style="margin-top:6px"></div></div>';
  }
  h+=retour();
  ecran(h);
  if(L.etude){
    on("mgl-abandon",function(){
      if(!confirm("Abandonner "+cursusOf(L.etude.id).n+" ? Tout l'argent déjà dépensé est perdu."))return;
      hist("✋ Abandon des études — retour à la vie active.");
      L.etude=null;bouge({bonheur:-8,reput:-3});
      sauver();ecranChoixMetier(false);
    });
  }else{
    var z=elRoot.querySelector("#mgl-cursus");
    cursusDispo().forEach(function(c){
      var dv=document.createElement("div");dv.className="mgl-job";
      dv.innerHTML='<span class="ic">'+c.ic+'</span><div style="flex:1"><b>'+c.n+'</b>'+
        (c.don!==null?'<span class="mgl-badge b">'+DIPLOMES[c.don]+'</span>':'<span class="mgl-badge v">+1 niveau</span>')+
        '<div class="mgl-sub">'+c.d+'</div>'+
        '<div class="mgl-sub" style="color:#F6BC1C">'+c.mois+' mois · '+fmt(c.cout)+'/mois · total ~'+fmt(c.cout*c.mois)+'</div></div>';
      dv.onclick=function(){
        if(L.argent<c.cout*3){alerte("Il te faut au moins trois mois d'avance ("+fmt(c.cout*3)+") pour t'inscrire sereinement.");return;}
        if(!confirm("S'inscrire en « "+c.n+" » ?\n\n"+c.mois+" mois sans salaire, "+fmt(c.cout)+"/mois."))return;
        inscrire(c);sauver();ecranJeu("🎓 Inscription faite : "+c.n+". Garde ton énergie et ton moral, c'est ça qui fait le mérite.");
      };
      z.appendChild(dv);
    });
  }
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- 👨‍👩‍👧 FAMILLE ---------------- */
function ecranFamille(){
  navActive("famille");
  var us=unionsActives();
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">💑 '+(us.length>1?"Mes foyers":"Mon foyer")+'</b>';
  if(us.length){
    us.forEach(function(u,i){
      var etat=u.bonheur>=70?"😊 heureuse":(u.bonheur>=45?"🙂 ça va":(u.bonheur>=20?"😕 elle souffre":"💔 au bord de la rupture"));
      h+='<div style="margin-top:9px"><div class="mgl-line"><span><b>'+esc2(u.nom)+'</b>'+
        (us.length>1?'<span class="mgl-badge">'+(i+1)+(i===0?"ʳᵉ":"ᵉ")+' épouse</span>':'')+
        (u.biz?'<span class="mgl-badge v">commerce</span>':'')+'</span><span class="mgl-sub">'+etat+'</span></div>'+
        barre(u.bonheur,u.bonheur>=45?"#22c55e":"#ef4444")+'</div>';
    });
    if(us.length>1)h+='<div class="mgl-sub" style="margin-top:9px">⚖️ Deux foyers, c\'est deux fois le budget et l\'obligation d\'équité. Si l\'une tombe trop bas, elle demandera la séparation devant le cadi.</div>';
    h+='<button class="mgl-btn ghost" id="mgl-cadeau" style="margin-top:10px">🎁 Faire un cadeau au foyer le plus fragile ('+fmt(CFG.equiteCadeau)+')</button>';
  }
  else if(L.fiance)h+='<div class="mgl-sub">💞 Fiancé(e) à '+esc2(L.fiance)+' — le mariage approche…</div>';
  else h+='<div class="mgl-sub">Célibataire — les rencontres arrivent avec le temps, le bonheur 😊 et un peu d\'argent de côté.</div>';
  h+='</div>';

  var vivants=enfantsVivants();
  h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">👨‍👩‍👧 Mes enfants ('+vivants.length+')</b>';
  if(!vivants.length)h+='<div class="mgl-sub">Aucun enfant pour l\'instant. Ce sont eux qui reprendront l\'histoire après toi.</div>';
  vivants.forEach(function(e){
    var quoi=e.gerant?("🧑🏾‍💼 gère "+e.gerant):(e.travaille?"💼 travaille":(e.etudes?"🎓 études à Moroni":(e.age>=5?"🎒 école":"👶 bébé")));
    h+='<div style="margin-top:9px"><div class="mgl-line"><span>'+(e.g==="g"?"👦🏾":"👧🏾")+' <b>'+esc2(e.nom)+'</b>'+
      (e.diplome>0?'<span class="mgl-badge b">'+DIPLOMES[e.diplome]+'</span>':'')+'</span>'+
      '<span class="mgl-sub">'+e.age+' an'+(e.age>1?"s":"")+' · '+quoi+'</span></div>'+
      '<div class="mgl-sub">mère : '+esc2(e.mere||"—")+' · talent '+e.talent+'/100</div>'+
      barre(e.talent,"#38bdf8")+'</div>';
  });
  h+='<div class="mgl-sub" style="margin-top:10px">Le <b>talent</b> décide de ce que l\'enfant fera de ton héritage : un enfant doué et diplômé fait fructifier une entreprise, un autre la laisse s\'éteindre.</div></div>'+
   '<button class="mgl-btn or" id="mgl-test">📜 Écrire mon testament</button>'+retour();
  ecran(h);
  on("mgl-test",function(){ecranTestament();});
  on("mgl-cadeau",function(){
    var us2=unionsActives();
    if(!us2.length)return;
    if(L.argent<CFG.equiteCadeau){alerte("Il faut "+fmt(CFG.equiteCadeau)+".");return;}
    var f=us2.slice().sort(function(a,b){return a.bonheur-b.bonheur;})[0];
    L.argent-=CFG.equiteCadeau;f.bonheur=clamp(f.bonheur+26);
    bouge({bonheur:4,spirit:3});
    hist("🎁 Cadeau et temps passé avec "+f.nom+" — le foyer respire.");
    sauver();ecranFamille();
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- 📜 LE TESTAMENT ---------------- */
function ecranTestament(){
  navActive(null);
  if(!L.testament)L.testament={biz:{},maison:null,argent:"egal"};
  var her=heritiersPossibles();
  var h='<div class="mgl-glass or mgl-pop"><b class="mgl-h">📜 Mon testament</b>'+
   '<div class="mgl-sub">De ton vivant, tu décides qui reçoit quoi. À ta mort, le testament sera exécuté à la lettre — et l\'enfant qui reprend l\'histoire pourra <b>accepter ce qu\'il reçoit</b>… ou <b>tout refuser pour partir de zéro</b>.</div></div>';
  if(!her.length){
    h+='<div class="mgl-glass mgl-pop"><div class="mgl-sub">Aucun héritier de 16 ans ou plus pour l\'instant. Reviens quand tes enfants auront grandi.</div></div>'+retour();
    ecran(h);on("mgl-retour",function(){ecranJeu();});return;
  }
  var opts=function(sel){
    return '<option value=""'+(!sel?" selected":"")+'>— personne (vendu et partagé) —</option>'+
      her.map(function(e){return '<option value="'+esc2(e.nom)+'"'+(sel===e.nom?" selected":"")+'>'+esc2(e.nom)+' ('+e.age+" ans, talent "+e.talent+')</option>';}).join("");
  };
  h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">🏢 Les entreprises</b>';
  if(!L.entreprises.length)h+='<div class="mgl-sub">Tu n\'as pas encore d\'entreprise à léguer.</div>';
  L.entreprises.forEach(function(b,i){
    var t=byId(BIZ,b.type);if(!t)return;
    h+='<div style="margin-top:10px"><div class="mgl-line"><span>'+t.ic+' <b>'+esc2(b.nom||t.n)+'</b> <span class="mgl-badge">niv. '+b.niv+'</span></span></div>'+
      '<select class="mgl-in" data-leg="'+i+'">'+opts(L.testament.biz[i]||"")+'</select></div>';
  });
  h+='</div>';
  if(L.maison||L.villa){
    h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">🏠 La maison de famille</b>'+
      '<select class="mgl-in" id="mgl-leg-maison">'+opts(L.testament.maison||"")+'</select>'+
      '<div class="mgl-sub" style="margin-top:6px">Celui qui reçoit la maison n\'aura plus de loyer à payer — c\'est souvent le plus beau cadeau.</div></div>';
  }
  h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">💰 L\'argent</b>'+
   '<select class="mgl-in" id="mgl-leg-argent">'+
   '<option value="egal"'+(L.testament.argent==="egal"?" selected":"")+'>Partage égal entre tous les enfants</option>'+
   '<option value="aine"'+(L.testament.argent==="aine"?" selected":"")+'>Tout à l\'aîné</option>'+
   her.map(function(e){return '<option value="n:'+esc2(e.nom)+'"'+(L.testament.argent==="n:"+e.nom?" selected":"")+'>Tout à '+esc2(e.nom)+'</option>';}).join("")+
   '</select>'+
   '<div class="mgl-sub" style="margin-top:6px">Une part de 40 % revient toujours aux frais funéraires et aux obligations familiales — c\'est la coutume.</div></div>'+
   '<button class="mgl-btn or" id="mgl-test-ok">✅ Enregistrer mon testament</button>'+retour();
  ecran(h);
  on("mgl-test-ok",function(){
    elRoot.querySelectorAll("[data-leg]").forEach(function(s){
      var i=s.getAttribute("data-leg");
      if(s.value)L.testament.biz[i]=s.value;else delete L.testament.biz[i];
    });
    var mm=elRoot.querySelector("#mgl-leg-maison");
    L.testament.maison=mm?(mm.value||null):null;
    var aa=elRoot.querySelector("#mgl-leg-argent");
    L.testament.argent=aa?aa.value:"egal";
    hist("📜 Testament mis à jour devant témoins.");
    bouge({spirit:5});
    sauver();ecranJeu("📜 Ton testament est enregistré. Tes enfants savent désormais à quoi s'attendre.");
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- 🕊️ LA SUCCESSION ---------------- */
function partArgent(e,her){
  var dispo=Math.round(Math.max(0,L.argent)*0.6);   // 40 % : funérailles et obligations
  var t=L.testament||{argent:"egal"};
  if(t.argent==="egal")return Math.round(dispo/Math.max(1,her.length));
  if(t.argent==="aine"){
    var aine=her.slice().sort(function(a,b){return b.age-a.age;})[0];
    return aine&&aine.nom===e.nom?dispo:0;
  }
  if(t.argent&&t.argent.indexOf("n:")===0)return t.argent.slice(2)===e.nom?dispo:0;
  return Math.round(dispo/Math.max(1,her.length));
}
function bizPour(e){
  var t=(L.testament&&L.testament.biz)||{},out=[];
  L.entreprises.forEach(function(b,i){if(t[i]===e.nom)out.push(b);});
  return out;
}
/* Inscrire la génération qui s'achève dans les chroniques. Appelé à la fois par
   l'écran d'héritage et par herite() : le livre de famille ne doit jamais
   dépendre du fait qu'un écran ait été affiché ou non. */
function archiverGeneration(){
  if(L._archive)return;
  L._archive=true;
  L.lignee=L.lignee||[];
  L.lignee.push({nom:L.nom,famille:L.famille,gen:L.generation,age:L.age,annee:L.annee,
    patrimoine:patrimoineTotal(),metier:metierOf().n,diplome:L.diplome,
    enfants:L.enfants.length,anda:!!L.grandMariage,selfMade:!!L.selfMade});
}
function ecranHeritage(){
  majChrome(false);
  var her=heritiersPossibles();
  archiverGeneration();
  var resume="⚰️ "+L.nom+" "+(L.famille||"")+" s'est éteint(e) à "+L.age+" ans"+
    (L.grandMariage?", NOTABLE de Mohéli":"")+
    (L.diplome>0?", "+DIPLOMES[L.diplome]:"")+
    ". Patrimoine laissé : "+fmt(patrimoineTotal())+".";
  var h='<div style="text-align:center;padding:24px 0 6px" class="mgl-pop"><div style="font-size:48px">🕊️</div>'+
   '<div style="font-size:21px;font-weight:900;margin:6px 0">Une vie s\'achève…</div></div>'+
   '<div class="mgl-glass mgl-pop">'+esc2(resume)+'</div>';
  if(her.length){
    h+='<div class="mgl-glass or mgl-pop"><b class="mgl-h">📜 Lecture du testament</b>'+
      '<div class="mgl-sub" style="margin-bottom:8px">Voici ce que chacun reçoit. Choisis l\'enfant dont tu veux vivre l\'histoire :</div><div id="mgl-herit"></div></div>';
  }else{
    h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">🌪️ Fin de lignée</b>'+
     '<div class="mgl-sub" style="margin-top:4px">Aucun enfant de 16 ans ou plus pour reprendre le flambeau. Mohéli n\'oubliera pas '+esc2(L.nom)+'.</div>'+
     '<button class="mgl-btn" id="mgl-renaitre" style="margin-top:10px">🌅 Commencer une nouvelle histoire</button></div>';
  }
  h+='<button class="mgl-btn ghost" id="mgl-chro">📖 Voir les chroniques de la famille</button>';
  ecran(h);
  on("mgl-chro",ecranChroniques);
  if(her.length){
    var hb=elRoot.querySelector("#mgl-herit");
    her.forEach(function(e){
      var arg=partArgent(e,her),bz=bizPour(e);
      var maison=(L.testament&&L.testament.maison===e.nom&&(L.maison||L.villa));
      var recu=[];
      if(arg>0)recu.push(fmt(arg));
      if(bz.length)recu.push(bz.length+" entreprise"+(bz.length>1?"s":""));
      if(maison)recu.push("la maison");
      var dv=document.createElement("div");dv.className="mgl-job";
      dv.innerHTML='<span class="ic">'+(e.g==="g"?"👨🏾":"👩🏾")+'</span><div style="flex:1"><b>'+esc2(e.nom)+'</b>'+
        (e.diplome>0?'<span class="mgl-badge b">'+DIPLOMES[e.diplome]+'</span>':'')+
        '<div class="mgl-sub">'+e.age+' ans · mère : '+esc2(e.mere||"—")+' · talent '+e.talent+'/100</div>'+
        '<div class="mgl-sub" style="color:#F6BC1C">reçoit : '+(recu.length?recu.join(" · "):"rien du tout")+'</div></div>';
      dv.onclick=function(){choixSuccession(e,her);};
      hb.appendChild(dv);
    });
  }else on("mgl-renaitre",function(){var lg=L.lignee;localStorage.removeItem("mg_life");L=null;window._mglLignee=lg;ecranAccueil();});
}
/* LE choix : accepter l'héritage, ou tout refuser et partir de zéro */
function choixSuccession(enfant,her){
  var arg=partArgent(enfant,her),bz=bizPour(enfant);
  var maison=!!(L.testament&&L.testament.maison===enfant.nom&&(L.maison||L.villa));
  var recu=[];
  if(arg>0)recu.push("💰 "+fmt(arg));
  bz.forEach(function(b){var t=byId(BIZ,b.type);if(t)recu.push(t.ic+" "+(b.nom||t.n));});
  if(maison)recu.push("🏠 la maison de famille");
  modalOuvre('<div class="mgl-mic">'+(enfant.g==="g"?"👨🏾":"👩🏾")+'</div>'+
   '<b style="display:block;text-align:center;font-size:17px;margin:7px 0 3px">'+esc2(enfant.nom)+' reprend l\'histoire</b>'+
   '<div class="mgl-sub" style="text-align:center;margin-bottom:10px">Le testament lui laisse :<br><b style="color:#F6BC1C">'+(recu.length?recu.join(" · "):"rien du tout")+'</b></div>'+
   '<button class="mgl-choice" id="mgl-h-oui"><b>🎁 Accepter l\'héritage</b><div class="mgl-sub">Tu démarres avec tout ce que ton parent t\'a laissé, et la réputation du nom. Mais on attendra beaucoup de toi.</div></button>'+
   '<button class="mgl-choice" id="mgl-h-non"><b>💪 Refuser et partir de zéro</b><div class="mgl-sub">Tu ne prends rien : '+fmt(CFG.argentDepart)+' en poche, comme n\'importe qui. En échange, la fierté du self-made — et <b>+'+Math.round((CFG.selfMadeBonus-1)*100)+' % de revenus à vie</b>.</div></button>');
  on("mgl-h-oui",function(){modalFerme();herite(enfant,her,false);});
  on("mgl-h-non",function(){modalFerme();herite(enfant,her,true);});
}
function herite(enfant,her,zero){
  archiverGeneration();
  var ancien=L.nom,gen=L.generation+1,lignee=L.lignee||[],famille=L.famille;
  var arg=zero?CFG.argentDepart:partArgent(enfant,her)+15000;
  var bz=zero?[]:bizPour(enfant);
  var maison=zero?false:!!(L.testament&&L.testament.maison===enfant.nom&&L.maison);
  var villa=zero?false:!!(L.testament&&L.testament.maison===enfant.nom&&L.villa);
  var reputParent=L.reput,anda=L.grandMariage,vill=L.village,an=L.annee,mo=L.mois;

  var sx=enfant.g==="g"?"h":"f";
  var n=nouveauJeu(enfant.nom,"sans",sx,AVATARS[sx][0],famille);
  n.generation=gen;n.age=Math.max(16,enfant.age);n.argent=arg;
  n.annee=an;n.mois=mo;n.village=vill;n.lignee=lignee;
  n.diplome=enfant.diplome||0;
  n.entreprises=bz;
  n.maison=maison;n.villa=villa;
  n.selfMade=!!zero;
  n.bonheur=clamp(70+(zero?12:0));
  n.reput=clamp(zero?18:(20+(anda?15:0)+Math.round(reputParent*0.3)));
  /* le talent de l'enfant devient son avance de départ */
  n.xp=Math.round((enfant.talent||40)/8);
  n.entreprises.forEach(function(b){b.gerant=null;});

  var recap=zero
    ? "💪 "+enfant.nom+" REFUSE l'héritage de "+ancien+" et repart de zéro, avec "+fmt(arg)+" et ses seules mains. « Ce que je bâtirai sera à moi. »"
    : "🕊️ "+enfant.nom+" reprend le flambeau de "+ancien+" ("+gen+"ᵉ génération). Héritage : "+fmt(arg)+
      (bz.length?" + "+bz.length+" entreprise"+(bz.length>1?"s":""):"")+(maison||villa?" + la maison de famille":"")+".";
  n.histoire=[{t:recap,age:n.age,an:n.annee}];
  if(n.diplome>0)n.histoire.unshift({t:DIPLOME_IC[n.diplome]+" "+enfant.nom+" a déjà son "+DIPLOMES[n.diplome]+" — les grands métiers lui sont ouverts.",age:n.age,an:n.annee});
  L=n;sauver();
  if(zero)ecranChoixMetier(false);
  else ecranJeu("🕊️ Repose en paix, "+esc2(ancien)+". À toi d'écrire la suite, "+esc2(enfant.nom)+". Va choisir ta voie : 💼 Carrière ou 🎓 Études.");
}

/* ---------------- 📖 CHRONIQUES DE LA FAMILLE ---------------- */
function ecranChroniques(){
  navActive(null);
  var lg=(L?L.lignee:window._mglLignee)||[];
  var h='<div class="mgl-glass or mgl-pop"><b class="mgl-h">📖 Les chroniques de la famille</b>'+
   '<div class="mgl-sub">Toutes les générations qui t\'ont précédé. C\'est ça, une dynastie : pas une vie réussie, mais une suite de vies qui se passent le relais.</div></div>';
  if(!lg.length){
    h+='<div class="mgl-glass mgl-pop"><div class="mgl-sub">Tu es la première génération. Ton nom ouvrira le livre.</div></div>';
  }else{
    lg.slice().reverse().forEach(function(g){
      h+='<div class="mgl-glass mgl-pop"><b>'+g.gen+'ᵉ génération — '+esc2(g.nom)+' '+esc2(g.famille||"")+'</b>'+
        (g.anda?'<span class="mgl-badge">👑 anda</span>':'')+(g.selfMade?'<span class="mgl-badge v">💪 self-made</span>':'')+
        '<div class="mgl-sub" style="margin-top:4px">'+g.metier+(g.diplome?' · '+DIPLOMES[g.diplome]:'')+' · '+g.enfants+' enfant(s)</div>'+
        '<div class="mgl-line"><span>Mort à '+g.age+' ans, en '+g.annee+'</span><b style="color:#F6BC1C">'+fmt(g.patrimoine)+'</b></div></div>';
    });
  }
  h+=(L?retour():'<button class="mgl-btn" id="mgl-retour2">← Retour</button>');
  ecran(h);
  on("mgl-retour",function(){ecranJeu();});
  on("mgl-retour2",function(){ecranHeritage();});
}

/* ---------------- 💼 CARRIÈRE ---------------- */
function ecranCarriere(){
  navActive("carriere");
  var m=metierOf();
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">💼 Ma carrière</b>'+
   '<div class="mgl-stats" style="margin:8px 0 2px"><div>⭐ Réputation '+barre(L.reput,"#a78bfa")+'</div>'+
   '<div>📈 Expérience '+barre(L.emploi&&!L.etude?L.xp*100/((L.niveau+1)*24):0,"#F6BC1C")+'</div></div>'+
   '<div class="mgl-sub" style="margin:8px 0 0">Aujourd\'hui : <b>'+titreActuel()+'</b>'+
     (L.emploi&&!L.etude?' — '+fmt(m.niveaux[L.niveau].sal)+'/mois de base':'')+'</div>'+
   (L.diplome>0?'<div class="mgl-sub">'+DIPLOME_IC[L.diplome]+' '+DIPLOMES[L.diplome]+' : +'+Math.round(CFG.diplomeSalaire*L.diplome*100)+' % sur ton salaire.</div>':
     '<div class="mgl-sub">Sans diplôme, les grands métiers (ingénieur, avocat, médecin) restent fermés.</div>')+
   (L.selfMade?'<div class="mgl-sub" style="color:#4ade80">💪 Self-made : +'+Math.round((CFG.selfMadeBonus-1)*100)+' % de revenus, parce que tu n\'as rien pris à personne.</div>':'')+
   '</div>'+
   '<button class="mgl-btn or" id="mgl-etudes">🎓 Les études — '+(L.etude?"suivre mon parcours":"reprendre des études")+'</button>'+
   '<div style="height:10px"></div>'+
   (L.etude?'<div class="mgl-glass mgl-pop"><div class="mgl-sub">Tu es en études : pas de métier tant que tu n\'as pas fini (ou abandonné).</div></div>':
     '<div class="mgl-glass mgl-pop"><b class="mgl-h">'+(L.emploi?"Changer de métier":"Prendre un emploi")+'</b>'+
      '<div class="mgl-sub">'+(L.emploi?"Changer = repartir bas dans le nouveau métier (ton diplôme et ton expérience amortissent la chute).":"Reprendre un emploi te redonne un salaire fixe — mais attention à la fatigue si tu gardes tes entreprises.")+'</div>'+
      '<div id="mgl-metiers" style="margin-top:8px"></div></div>')+
   retour();
  ecran(h);
  on("mgl-etudes",function(){ecranEtudes();});
  if(!L.etude){
    var zm=elRoot.querySelector("#mgl-metiers");
    metiersVisibles().forEach(function(mm){
      if(L.emploi&&mm.id===L.metier)return;
      var bloque=L.diplome<mm.reqDip;
      var dv=document.createElement("div");dv.className="mgl-job"+(bloque?" off":"");
      var sal=mm.freelance?"revenus variables":("~"+fmt(mm.niveaux[0].sal)+" → "+fmt(mm.niveaux[mm.niveaux.length-1].sal));
      dv.innerHTML='<span class="ic">'+mm.ic+'</span><div style="flex:1"><b>'+mm.n+'</b>'+
        (mm.reqDip>0?'<span class="mgl-badge b">'+DIPLOMES[mm.reqDip]+'</span>':'')+
        '<div class="mgl-sub">'+mm.d+'</div><div class="mgl-sub" style="color:#F6BC1C">'+sal+'</div></div>';
      dv.onclick=function(){
        if(bloque){alerte("Il faut le "+DIPLOMES[mm.reqDip]+" pour devenir "+mm.n.toLowerCase()+".\n\nVa dans 🎓 Les études.");return;}
        if(!confirm((L.emploi?"Changer de métier pour":"Devenir")+" « "+mm.n+" » ?"))return;
        var bonusNiv=(L.niveau>0&&L.emploi)?1:0;
        L.metier=mm.id;L.niveau=Math.max(niveauDepart(mm),Math.min(bonusNiv,mm.niveaux.length-1));
        L.xp=0;L.emploi=true;L.retraite=false;
        hist("💼 "+L.nom+" devient "+mm.niveaux[L.niveau].t+" ("+mm.n+").");
        bouge({bonheur:4,energie:-4});
        sauver();ecranJeu("💼 Nouveau départ : "+mm.ic+" "+mm.n+" — bonne chance !");
      };
      zm.appendChild(dv);
    });
  }
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- 🎉 LOISIRS ---------------- */
function ecranLoisirs(){
  navActive("loisirs");
  var mo=L.annee*12+L.mois;
  if(L.loisirsMois!==mo){L.loisirsMois=mo;L.loisirsFaits=0;}
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">🎉 Loisirs & bien-être</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Dépenser pour soi, ce n\'est pas gaspiller : c\'est du bonheur, de la santé — et pendant les études, du mérite. '+(CFG.loisirsMaxMois-L.loisirsFaits)+' activité(s) restante(s) ce mois-ci.</div>'+
   '<div id="mgl-lz"></div></div>'+retour();
  ecran(h);
  var z=elRoot.querySelector("#mgl-lz");
  LOISIRS.forEach(function(a){
    if(a.unique&&(L.loisirsUniques||[]).indexOf(a.id)>=0)return;
    var dv=document.createElement("div");dv.className="mgl-job";
    var eff=Object.keys(a.e).map(function(k){var v=a.e[k];var ic={bonheur:"😊",sante:"❤️",energie:"⚡",spirit:"🕌",reput:"⭐"}[k]||k;return ic+(v>0?"+":"")+v;}).join(" ");
    dv.innerHTML='<span class="ic">'+a.ic+'</span><div style="flex:1"><b>'+a.n+'</b><div class="mgl-sub" style="color:#F6BC1C">'+fmt(a.p)+' · '+eff+'</div></div>';
    dv.onclick=function(){
      if(L.loisirsFaits>=CFG.loisirsMaxMois){alerte("Assez de sorties pour ce mois — le travail t'attend 😄");return;}
      if(L.argent<a.p){alerte("Pas assez d'argent pour ça !");return;}
      L.argent-=a.p;L.loisirsFaits++;bouge(a.e);
      if(a.unique)(L.loisirsUniques=L.loisirsUniques||[]).push(a.id);
      unionsActives().forEach(function(u){u.bonheur=clamp(u.bonheur+2);});
      hist(a.ic+" "+a.n+" — ça fait du bien !");
      sauver();ecranLoisirs();
    };
    z.appendChild(dv);
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- 🏢 L'EMPIRE ---------------- */
function ecranBiz(){
  navActive("biz");
  var focus=(!L.emploi&&!L.etude&&!L.retraite);
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">👔 Salaire de PDG</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Tu te verses <b style="color:#F6BC1C">'+fmt(L.salairePDG||CFG.pdgMin)+'</b>/mois depuis les caisses. Maximum selon ton activité : '+fmt(pdgMax())+' (200 000 + 25 % du net mensuel).</div>'+
   '<button class="mgl-btn ghost" id="mgl-pdg">⚙️ Régler mon salaire de PDG</button></div>';
  h+='<div class="mgl-glass mgl-pop'+(focus?' or':'')+'"><b class="mgl-h">'+(focus?"🔥 PDG à plein temps":"⏳ PDG à temps partiel")+'</b>'+
   '<div class="mgl-sub">'+(focus
     ? "Tu ne dépends plus d'un patron : tes entreprises produisent <b>+"+Math.round((CFG.pdgPleinTemps-1)*100)+" %</b>, et la fatigue est bien moindre."
     : "Tant que tu as un emploi salarié, tes entreprises tournent au ralenti et te fatiguent (−4 énergie/mois chacune). Quitter ton travail leur donnerait <b>+"+Math.round((CFG.pdgPleinTemps-1)*100)+" %</b>.")+'</div>'+
   (L.emploi&&L.entreprises.length?'<button class="mgl-btn or" id="mgl-quitter" style="margin-top:10px">🚪 Quitter mon emploi et me consacrer à l\'entreprise</button>':'')+
   '</div>';
  h+='<div class="mgl-glass mgl-pop"><b class="mgl-h">🏢 Mes entreprises</b>';
  if(!L.entreprises.length)h+='<div class="mgl-sub" style="margin-top:4px">Aucune pour l\'instant. Les bénéfices vont dans la CAISSE de chaque entreprise ; toi, tu touches ton salaire de PDG.</div>';
  var adultes=enfantsVivants().filter(function(e){return e.age>=18;});
  L.entreprises.forEach(function(b,i){
    var t=byId(BIZ,b.type);if(!t)return;
    var ger=b.gerant?adultes.filter(function(e){return e.nom===b.gerant;})[0]:null;
    h+='<div class="mgl-glass" style="margin:9px 0 0;padding:12px"><b>'+t.ic+' '+esc2(b.nom||t.n)+'</b><span class="mgl-badge">niv. '+b.niv+'</span>'+
     (ger?'<span class="mgl-badge v">🧑🏾‍💼 '+esc2(ger.nom)+'</span>':'')+
     '<div class="mgl-sub">💰 Caisse : <b style="color:'+((b.caisse||0)>=0?"#4ade80":"#f87171")+'">'+fmt(b.caisse||0)+'</b> · '+b.emp+' employé(s) · pub : '+(b.pub||0)+' mois</div>'+
     (L.testament&&L.testament.biz&&L.testament.biz[i]?'<div class="mgl-sub">📜 léguée à <b>'+esc2(L.testament.biz[i])+'</b></div>':'')+
     '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="emp" data-i="'+i+'">＋ Embaucher</button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="pub" data-i="'+i+'">📣 Pub</button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="niv" data-i="'+i+'">⬆️ Agrandir<br><span style="font-weight:600;opacity:.75;font-size:10px">'+fmt(coutAgrandir(t,b.niv))+'</span></button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="ger" data-i="'+i+'">🧑🏾‍💼 Gérant</button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="nom" data-i="'+i+'">✏️ Nommer</button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="vendre" data-i="'+i+'">💸 Vendre</button></div></div>';
  });
  h+='</div><div class="mgl-glass mgl-pop"><b class="mgl-h">💼 Créer une entreprise</b>'+
   '<div class="mgl-sub">Les investissements (embauche, pub, agrandir) se paient depuis la CAISSE de l\'entreprise — la création depuis ta poche.</div>'+
   '<div id="mgl-achats" style="margin-top:6px"></div></div>'+
   '<button class="mgl-btn or" id="mgl-test2">📜 Léguer tout ça (testament)</button><div style="height:10px"></div>'+retour();
  ecran(h);
  on("mgl-test2",function(){ecranTestament();});
  on("mgl-pdg",function(){
    var v=prompt("Ton salaire de PDG mensuel (min "+CFG.pdgMin.toLocaleString("fr-FR")+", max "+pdgMax().toLocaleString("fr-FR")+") :",L.salairePDG||CFG.pdgMin);
    if(v==null)return;
    v=parseInt(String(v).replace(/[^\d]/g,""),10);
    if(!v||v<CFG.pdgMin){alerte("Minimum : "+fmt(CFG.pdgMin));return;}
    if(v>pdgMax()){alerte("Ton activité ne permet pas plus de "+fmt(pdgMax())+" pour l'instant — développe tes entreprises !");return;}
    L.salairePDG=v;hist("👔 Salaire de PDG fixé à "+fmt(v)+"/mois.");sauver();ecranBiz();
  });
  var za=elRoot.querySelector("#mgl-achats");
  BIZ.forEach(function(t){
    var bloque=false,pourquoi="";
    if(t.cond==="dev3"&&!(L.metier==="dev"&&L.niveau>=3)){bloque=true;pourquoi="Réservé aux développeurs experts (niveau 4 de la carrière dev).";}
    if(t.cond==="dip3"&&L.diplome<3){bloque=true;pourquoi="Il faut un Master.";}
    if(t.cond==="dip4"&&L.diplome<4){bloque=true;pourquoi="Il faut un Doctorat.";}
    var dv=document.createElement("div");dv.className="mgl-job"+(bloque?" off":"");
    dv.innerHTML='<span class="ic">'+t.ic+'</span><div style="flex:1"><b>'+t.n+'</b><div class="mgl-sub">'+t.d+'</div>'+
      '<div class="mgl-sub" style="color:#F6BC1C">'+fmt(t.prix)+(t.rev?' · ~'+fmt(t.rev)+'/mois brut · plafond '+fmt(CFG.bizCapMois)+'/mois':' · SANS plafond, mais brûle de l\'argent au début')+'</div></div>';
    dv.onclick=function(){
      if(bloque){alerte(pourquoi);return;}
      if(L.argent<t.prix){alerte("Pas assez d'argent — il faut "+fmt(t.prix)+".");return;}
      if(!confirm("Créer « "+t.n+" » pour "+fmt(t.prix)+" ?"))return;
      L.argent-=t.prix;
      L.entreprises.push({type:t.id,niv:1,emp:0,pub:0,caisse:0,nom:null,gerant:null});
      hist("💼 "+L.nom+" crée : "+t.n+" !");bouge({reput:6,bonheur:5});
      sauver();ecranBiz();
    };
    za.appendChild(dv);
  });
  elRoot.querySelectorAll("[data-a]").forEach(function(b){
    b.onclick=function(){
      var i=+b.getAttribute("data-i"),a=b.getAttribute("data-a"),biz=L.entreprises[i],t=byId(BIZ,biz.type);
      function payeCaisse(cout){
        if((biz.caisse||0)>=cout){biz.caisse-=cout;return true;}
        if(L.argent>=cout){if(!confirm("La caisse est trop juste — payer "+fmt(cout)+" de ta poche ?"))return false;L.argent-=cout;return true;}
        alerte("Ni la caisse ni ta poche ne suffisent ("+fmt(cout)+").");return false;
      }
      if(a==="emp"){if(biz.emp>=biz.niv*3){alerte("Agrandis d'abord (max "+biz.niv*3+" employés).");return;}if(!payeCaisse(CFG.embauche))return;biz.emp++;hist("🤝 Embauche dans "+t.n+" ("+biz.emp+" employés).");}
      if(a==="pub"){if(!payeCaisse(CFG.pub))return;biz.pub=(biz.pub||0)+3;hist("📣 Pub pour "+t.n+" (3 mois boostés).");}
      if(a==="niv"){var c=coutAgrandir(t,biz.niv);if(!payeCaisse(c))return;biz.niv++;hist("⬆️ "+(biz.nom||t.n)+" passe au niveau "+biz.niv+" ("+fmt(c)+") !");bouge({reput:3});}
      if(a==="nom"){
        var nn=prompt("Le nom de cette entreprise :",biz.nom||t.n);
        if(nn==null)return;
        biz.nom=String(nn).trim().slice(0,28)||null;
        hist("✏️ L'entreprise s'appelle désormais « "+(biz.nom||t.n)+" ».");
      }
      if(a==="ger"){
        var ad=enfantsVivants().filter(function(e){return e.age>=18&&(!e.gerant||e.gerant===(biz.nom||t.n));});
        if(!ad.length){alerte("Aucun enfant de 18 ans ou plus pour gérer cette entreprise.");return;}
        var liste=ad.map(function(e,k){return (k+1)+" — "+e.nom+" (talent "+e.talent+", "+DIPLOMES[e.diplome||0]+")";}).join("\n");
        var rep=prompt("Qui gère « "+(biz.nom||t.n)+" » ?\n\n"+liste+"\n\n0 — personne\n\nTon choix :","1");
        if(rep==null)return;
        var k=parseInt(rep,10);
        if(k===0){
          if(biz.gerant){L.enfants.forEach(function(e){if(e.nom===biz.gerant)e.gerant=null;});}
          biz.gerant=null;hist("🧑🏾‍💼 Plus de gérant pour "+(biz.nom||t.n)+".");
        }else if(k>=1&&k<=ad.length){
          var e2=ad[k-1];
          if(biz.gerant){L.enfants.forEach(function(x){if(x.nom===biz.gerant)x.gerant=null;});}
          biz.gerant=e2.nom;e2.gerant=biz.nom||t.n;e2.travaille=true;
          hist("🧑🏾‍💼 "+e2.nom+" prend la gérance de "+(biz.nom||t.n)+" — l'entreprise tourne mieux et te fatigue moins.");
          bouge({bonheur:6,reput:3});
        }else return;
      }
      if(a==="vendre"){
        var val=Math.round(t.prix*0.6*biz.niv)+Math.max(0,biz.caisse||0);
        if(!confirm("Vendre "+(biz.nom||t.n)+" pour "+fmt(val)+" (60 % de la valeur + la caisse) ?"))return;
        if(biz.gerant)L.enfants.forEach(function(e){if(e.nom===biz.gerant)e.gerant=null;});
        L.argent+=val;L.entreprises.splice(i,1);
        if(L.testament&&L.testament.biz)delete L.testament.biz[i];
        hist("💸 "+(biz.nom||t.n)+" vendue pour "+fmt(val)+".");
      }
      sauver();ecranBiz();
    };
  });
  on("mgl-quitter",function(){
    if(!confirm("Quitter ton emploi pour te consacrer à tes entreprises ?\n\n+"+Math.round((CFG.pdgPleinTemps-1)*100)+" % de production, moins de fatigue — mais plus aucun salaire fixe."))return;
    L.emploi=false;
    hist("🚪 "+L.nom+" quitte son emploi : PDG à 100 % ! Les entreprises tournent à plein régime.");
    bouge({bonheur:8,energie:10});
    sauver();ecranBiz();
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- VILLAGES ---------------- */
function ecranVillages(){
  navActive(null);
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">🗺️ Les villages de Mohéli</b>'+
   '<div class="mgl-sub" style="margin-bottom:6px">Chaque village a son économie — déménager coûte '+fmt(CFG.demenagement)+'. Fomboni aide aussi les études.</div>'+
   '<div id="mgl-vill"></div></div>'+retour();
  ecran(h);
  var zv=elRoot.querySelector("#mgl-vill");
  VILLAGES.forEach(function(v){
    var ici=v.id===L.village;
    var bon=Object.keys(v.bonus).map(function(k){return k==="bonheur"?("😊 +"+v.bonus[k]):("+"+Math.round((v.bonus[k]-1)*100)+"% "+k);}).join(" · ");
    if(v.etudes)bon+=" · 🎓 +"+Math.round((v.etudes-1)*100)+"% études";
    var dv=document.createElement("div");dv.className="mgl-job";if(ici)dv.style.borderColor="rgba(246,188,28,.6)";
    dv.innerHTML='<span class="ic">'+v.ic+'</span><div style="flex:1"><b>'+v.n+'</b>'+(ici?'<span class="mgl-badge">TU VIS ICI</span>':'')+'<div class="mgl-sub">'+v.d+'</div><div class="mgl-sub" style="color:#F6BC1C">'+bon+'</div></div>';
    dv.onclick=function(){
      if(ici)return;
      if(L.argent<CFG.demenagement){alerte("Il faut "+fmt(CFG.demenagement)+" pour déménager.");return;}
      if(!confirm("Déménager à "+v.n+" pour "+fmt(CFG.demenagement)+" ?"))return;
      L.argent-=CFG.demenagement;L.village=v.id;
      hist("📦 Déménagement à "+v.n+" !");bouge({bonheur:4,energie:-6});
      sauver();ecranVillages();
    };
    zv.appendChild(dv);
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- CLASSEMENT ---------------- */
function ecranClassement(){
  navActive(null);
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">🏆 Les grandes familles de Mohéli</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Classées par patrimoine — publie ton score avec un pseudo (jamais ton vrai numéro).</div>'+
   '<button class="mgl-btn ghost" id="mgl-pub-score">📤 Publier mon score</button>'+
   '<div id="mgl-scores" style="margin-top:10px" class="mgl-sub">Chargement du classement…</div></div>'+retour();
  ecran(h);
  on("mgl-retour",function(){ecranJeu();});
  on("mgl-pub-score",function(){
    if(!cloudOK()){alerte("Connecte-toi à internet pour publier ton score.");return;}
    var ps=L.pseudo||localStorage.getItem("mg_pseudo")||"";
    ps=prompt("Ton pseudo pour le classement :",ps)||"";ps=ps.trim().slice(0,24);
    if(!ps)return;
    L.pseudo=ps;
    (typeof ensureUid==="function"?ensureUid():Promise.resolve(null)).then(function(uid){
      if(!uid){alerte("Impossible pour l'instant — réessaie.");return;}
      sb.from("life_scores").upsert({user_id:uid,pseudo:ps,patrimoine:patrimoineTotal(),fortune:Math.max(0,L.argent),generation:L.generation,reput:L.reput,maj:new Date().toISOString()},{onConflict:"user_id"})
        .then(function(r){if(r&&r.error){alerte("Publication impossible : "+r.error.message);}else{sauver();chargerScores();}});
    });
  });
  chargerScores();
}
function chargerScores(){
  var z=elRoot.querySelector("#mgl-scores");if(!z)return;
  if(!cloudOK()){z.textContent="📴 Hors ligne — le classement s'affiche avec internet.";return;}
  sb.from("life_scores").select("pseudo,patrimoine,generation").order("patrimoine",{ascending:false}).limit(10)
    .then(function(r){
      if(r.error||!r.data){z.textContent="Classement indisponible.";return;}
      if(!r.data.length){z.textContent="Sois le premier à publier ton score ! 🏆";return;}
      z.innerHTML=r.data.map(function(s,i){
        var med=["🥇","🥈","🥉"][i]||("#"+(i+1));
        return '<div class="mgl-line"><span>'+med+' '+esc2(s.pseudo)+(s.generation>1?' <span class="mgl-badge">'+s.generation+'ᵉ gén.</span>':'')+'</span><b style="color:#F6BC1C">'+fmt(s.patrimoine)+'</b></div>';
      }).join("");
    },function(){z.textContent="Classement indisponible.";});
}

/* ---------------- PARTAGE ---------------- */
function partager(){
  var mo=L.annee*12+L.mois;
  if(L.partMois!==mo){L.partMois=mo;L.partages=0;}
  if(L.partages>=CFG.partageMaxMois){alerte("Tu as déjà gagné tes 3 partages du mois — reviens le mois prochain ! 😉");return;}
  var texte="Je vis ma vie à Mohéli sur MoheliGo Life 🎮🏝️ — études, carrière, famille, entreprises, héritage… Viens jouer et réserver tes traversées sur https://moheligo.com !";
  var apres=function(){
    L.partages++;L.argent+=CFG.partageGain;
    hist("📣 Merci d'avoir fait connaître MoheliGo ! +"+fmt(CFG.partageGain)+" ("+L.partages+"/"+CFG.partageMaxMois+" ce mois).");
    sauver();ecranJeu("📣 +"+fmt(CFG.partageGain)+" pour ton partage — asante ! 🌺");
  };
  try{if(navigator.share){navigator.share({text:texte}).then(apres,function(){});return;}}catch(e){}
  window.open("https://wa.me/?text="+encodeURIComponent(texte),"_blank");
  setTimeout(apres,1500);
}

/* ---------------- BOUTIQUE ---------------- */
function ecranBoutique(){
  var conf=CFG.confort[L.confort]||CFG.confort.normal;
  var items=[
    {id:"ordinateur",n:"💻 Ordinateur portable",p:CFG.ordinateur,d:"Indispensable au développeur. Ouvre les vrais contrats — et fait monter le mérite pendant les études.",cond:!L.ordinateur},
    {id:"internet",n:"🌐 Abonnement internet",p:0,d:"15 000 KMF/mois. Nécessaire pour les gros contrats, utile pour réviser.",cond:!L.internet,mensuel:true},
    {id:"moto",n:"🛵 Moto",p:CFG.moto,d:"Transport plus facile, énergie préservée.",cond:!L.moto},
    {id:"maison",n:"🏠 Maison familiale",p:CFG.maison.p,d:"Plus de loyer — mais 25 000 KMF/mois d'entretien. Un vrai patrimoine, et le plus beau des legs.",cond:!L.maison},
    {id:"villa",n:"🏖️ Villa au bord de mer",p:CFG.villa.p,d:"Le prestige absolu (+10 réputation) — 80 000 KMF/mois d'entretien.",cond:!L.villa&&L.maison}
  ];
  navActive(null);
  var h='<div class="mgl-glass mgl-pop"><b class="mgl-h">🏠 Train de vie</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Actuellement : <b>'+conf.n+'</b>. L\'économe réduit les dépenses (mais pèse sur le moral) ; le confortable coûte cher (mais fait du bien).</div>'+
   '<div style="display:flex;gap:6px">'+
   ["econome","normal","large"].map(function(k){var c=CFG.confort[k];return '<button class="mgl-btn'+(L.confort===k?"":" ghost")+'" style="flex:1;font-size:12px;padding:10px" data-conf="'+k+'">'+c.n+'</button>';}).join("")+
   '</div></div>'+
   '<div class="mgl-glass mgl-pop"><b class="mgl-h">🛒 Boutique & projets</b><div id="mgl-shop" style="margin-top:6px"></div></div>'+retour();
  ecran(h);
  elRoot.querySelectorAll("[data-conf]").forEach(function(b){
    b.onclick=function(){L.confort=b.getAttribute("data-conf");hist("🏠 Train de vie : "+CFG.confort[L.confort].n+".");sauver();ecranBoutique();};
  });
  var shop=elRoot.querySelector("#mgl-shop");
  items.forEach(function(it){
    if(!it.cond)return;
    var dv=document.createElement("div");dv.className="mgl-job";
    dv.innerHTML='<div style="flex:1"><b>'+it.n+'</b><div class="mgl-sub">'+it.d+'</div><div class="mgl-sub" style="color:#F6BC1C">'+(it.mensuel?"15 000 KMF/mois":fmt(it.p))+'</div></div>';
    dv.onclick=function(){
      if(!it.mensuel&&L.argent<it.p){alerte("Pas assez d'argent — économise encore !");return;}
      if(!it.mensuel&&!confirm("Acheter "+it.n+" pour "+fmt(it.p)+" ?"))return;
      if(!it.mensuel)L.argent-=it.p;
      L[it.id]=true;
      if(it.id==="villa")bouge({reput:10,bonheur:8});
      if(!it.mensuel)L.patrimoine.push(it.n);
      hist((it.mensuel?"🌐 Abonnement internet pris.":"🛍️ Achat : "+it.n+"."));
      sauver();ecranBoutique();
    };
    shop.appendChild(dv);
  });
  if(!shop.children.length)shop.innerHTML='<div class="mgl-sub">Tout est acheté ici — pense aux entreprises 🏢 et aux loisirs 🎉 !</div>';
  on("mgl-retour",function(){ecranJeu();});
}

/* ---------------- OUVERTURE ---------------- */
function ouvrir(){
  if(!elRoot){
    var st=document.createElement("style");st.textContent=CSS;document.head.appendChild(st);
    elRoot=document.createElement("div");elRoot.id="mgl-root";
    elRoot.innerHTML='<div id="mgl-sky"></div><div id="mgl-stars"></div><div id="mgl-waves"></div>'+
      '<div id="mgl-top"></div><div class="mgl-wrap"></div>'+
      '<div id="mgl-stbar"></div>'+
      '<div id="mgl-nav">'+
       '<button data-nav="carriere">💼<span>Carrière</span></button>'+
       '<button data-nav="biz">🏢<span>Empire</span></button>'+
       '<span id="mgl-navgap"></span>'+
       '<button data-nav="famille">👨‍👩‍👧<span>Famille</span></button>'+
       '<button data-nav="loisirs">🎉<span>Loisirs</span></button></div>'+
      '<button id="mgl-fab"><span class="lune">🌙</span><span class="lbl">MOIS<br>SUIVANT</span></button>'+
      '<button class="mgl-x" style="position:absolute;top:12px;right:12px;z-index:6" id="mgl-close">✕</button>'+
      '<div id="mgl-modal"><div id="mgl-mbox"></div></div>';
    document.body.appendChild(elRoot);
    elRoot.querySelector("#mgl-close").onclick=fermer;
    elRoot.querySelector("#mgl-fab").onclick=function(){jouerMois();};
    elRoot.querySelectorAll("#mgl-nav button").forEach(function(b){
      b.onclick=function(){
        var id=b.getAttribute("data-nav");
        if(id==="carriere")ecranCarriere();else if(id==="biz")ecranBiz();
        else if(id==="famille")ecranFamille();else if(id==="loisirs")ecranLoisirs();
      };
    });
  }
  elRoot.style.display="flex";
  ecranAccueil();
  cloudPull(function(cloud){
    var locale=chargerLocal();
    if(cloud&&(!locale||cloud.maj>locale.maj)){
      try{localStorage.setItem("mg_life",JSON.stringify(cloud));}catch(e){}
      if(!L)ecranAccueil();
    }
  });
}
function fermer(){if(L)sauver();if(elRoot)elRoot.style.display="none";}

window.MGLife={open:ouvrir,close:fermer,_dbg:function(){return L;}};
if(window._mglAutoOpen){window._mglAutoOpen=false;ouvrir();}
})();
