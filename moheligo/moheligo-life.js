/* ================================================================
   🎮 MoheliGo Life — v94 (REDESIGN façon BitLife, identité MoheliGo)
   LA VIE · LA FAMILLE · L'EMPIRE · LE MONDE
   Nouveautés v94 (UI seulement, logique de jeu INCHANGÉE) :
   · barre du HAUT sticky (nom + métier à gauche, ARGENT toujours visible)
   · écran principal = le JOURNAL DE VIE central scrollable
     (séparateurs d'âge « — 21 ans · 2027 — », lignes emoji)
   · bilan mensuel = lignes DANS le journal (plus de gros écran)
   · ÉVÉNEMENTS en POPUP (grand emoji + choix) au lieu d'un écran
   · navigation BAS 5 items : 💼 Carrière · 🏢 Empire · [🌙] ·
     👨‍👩‍👧 Famille · 🎉 Loisirs (+ menu ⋯ : villages, boutique,
     classement, inviter)
   · 4 STATS en mini-barres FIXES au-dessus de la nav
   Identité conservée : nuit tropicale glassmorphism + ciel + KMF.
   Sauvegarde : à CHAQUE action + cloud + migration v1/v2 → v3.
   ================================================================ */
(function(){
"use strict";
if(window.MGLife)return;

/* ---------------- RÉGLAGES (équilibrage central) ---------------- */
var CFG={
  argentDepart:25000, ageDepart:20,
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
  conjointCout:14000, enfantCout:9000, ecoleRentree:18000, etudesAn:60000,
  mariageSimple:200000, grandMariage:1200000, fiancailles:40000,
  demenagement:50000, salaireEmploye:45000, embauche:20000, pub:50000,
  ordinateur:180000, moto:800000,
  maison:{p:12000000,entretien:25000}, villa:{p:45000000,entretien:80000},
  partageGain:10000, partageMaxMois:3, loisirsMaxMois:3,
  pdgMin:200000, pdgPartActivite:0.25,        // salaire PDG max = 200 000 + 25 % du net mensuel
  bizCapMois:15000000,                        // plafond de production/mois par entreprise (sauf tech)
  inflationMois:0.002
};

/* ---------------- MÉTIERS ---------------- */
var METIERS=[
  {id:"capitaine",ic:"🚤",n:"Capitaine de vedette",type:"carriere",d:"Tu prends la mer entre Grande Comore et Mohéli. La météo décide de tes journées.",
   niveaux:[{t:"Matelot",sal:60000},{t:"Second",sal:80000},{t:"Capitaine",sal:100000},{t:"Capitaine principal",sal:250000}],debut:2,meteoSensible:true,tag:"mer"},
  {id:"tourisme",ic:"🌴",n:"Agent touristique",type:"carriere",d:"Tu fais découvrir Mohéli aux visiteurs : tortues, baleines, îlots.",
   niveaux:[{t:"Guide stagiaire",sal:70000},{t:"Agent touristique",sal:100000},{t:"Agent senior",sal:150000},{t:"Chef d'agence",sal:250000}],debut:1,saisonSensible:true,tag:"tourisme"},
  {id:"dev",ic:"💻",n:"Développeur",type:"carriere",d:"Pas de salaire fixe au début… mais aucun plafond pour les meilleurs.",
   niveaux:[{t:"Débutant",sal:0},{t:"Freelance",sal:0},{t:"Développeur confirmé",sal:0},{t:"Développeur expert",sal:0}],debut:0,freelance:true,tag:"ville"},
  {id:"pecheur",ic:"🎣",n:"Pêcheur",type:"metier",d:"La mer nourrit — quand elle le veut bien.",
   niveaux:[{t:"Pêcheur",sal:55000},{t:"Pêcheur expérimenté",sal:75000},{t:"Patron pêcheur",sal:110000}],debut:0,meteoSensible:true,tag:"mer"},
  {id:"enseignant",ic:"📚",n:"Enseignant",type:"metier",d:"Un salaire stable et le respect du village.",
   niveaux:[{t:"Instituteur",sal:85000},{t:"Professeur",sal:120000},{t:"Directeur d'école",sal:180000}],debut:0,stable:true,reputation:1,tag:"ville"},
  {id:"commercant",ic:"🏪",n:"Commerçant",type:"metier",d:"Ta boutique au marché : tout dépend des clients.",
   niveaux:[{t:"Vendeur",sal:50000},{t:"Commerçant",sal:90000},{t:"Grossiste",sal:160000}],debut:1,variable:true,tag:"commerce"},
  {id:"infirmier",ic:"🩺",n:"Infirmier",type:"metier",d:"À l'hôpital de Fomboni, on compte sur toi jour et nuit.",
   niveaux:[{t:"Aide-soignant",sal:70000},{t:"Infirmier",sal:110000},{t:"Infirmier chef",sal:170000}],debut:1,fatigue:1,reputation:1,tag:"ville"},
  {id:"chauffeur",ic:"🚕",n:"Chauffeur",type:"metier",d:"Taxi partagé sur la côtière.",
   niveaux:[{t:"Chauffeur",sal:65000},{t:"Chauffeur-propriétaire",sal:120000}],debut:0,variable:true,tag:"ville"},
  {id:"agriculteur",ic:"🌱",n:"Agriculteur",type:"metier",d:"Bananes, manioc, ylang-ylang — la terre est généreuse.",
   niveaux:[{t:"Ouvrier agricole",sal:45000},{t:"Agriculteur",sal:80000},{t:"Grand planteur",sal:140000}],debut:0,meteoSensible:true,tag:"terre"}
];

/* ---------------- VILLAGES ---------------- */
var VILLAGES=[
  {id:"fomboni",n:"Fomboni",ic:"🏙️",d:"La capitale : marché, port, hôpital.",bonus:{commerce:1.12,ville:1.08}},
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
var PRETENDANTES=["Anturia","Zalhata","Kamaria","Mistoihi","Raïssa","Andjiza"];    // épouses possibles (pour un homme)
var PRETENDANTS=["Soidiki","Ben Ali","Rastami","Fazul","Kassim","Madi"];           // époux possibles (pour une femme)
var AVATARS={h:["👨🏾","🧔🏾","👨🏾‍💼","👳🏾‍♂️"],f:["👩🏾","🧕🏾","👩🏾‍💼","👰🏾‍♀️"]};

/* ---------------- ÉVÉNEMENTS GÉNÉRAUX (inchangés v92) ---------------- */
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
  {id:"formation",p:4,ic:"🎓",t:"Une formation est proposée",d:"Un organisme forme à ton métier à Fomboni.",
   choix:[{t:"S'inscrire (30 000 KMF)",e:{argent:-30000,xp:6,energie:-4}},{t:"Pas les moyens",e:{}}]},
  {id:"visite_medecin",p:4,ic:"🩺",t:"Campagne de santé gratuite",d:"Des médecins consultent gratuitement à l'hôpital.",
   choix:[{t:"Faire le contrôle",e:{sante:8,energie:2}},{t:"Pas le temps",e:{}}]},
  {id:"mangues",p:4,ic:"🥭",t:"La saison des mangues !",d:"Les manguiers croulent. Les enfants du quartier en distribuent.",
   choix:[{t:"En profiter en famille",e:{bonheur:5,sante:3}}]},
  {id:"voleur_marche",p:3,ic:"👝",t:"Pickpocket au marché",d:"Ta poche est plus légère…",
   choix:[{t:"C'est perdu (−6 000 KMF)",e:{argent:-6000,bonheur:-4}}]},
  {id:"invite_djando",p:4,ic:"🥁",t:"Soirée twarab à Djando",d:"Un orchestre vient jouer. Toute la jeunesse y va.",
   choix:[{t:"Y aller (2 000 KMF)",e:{argent:-2000,bonheur:8,energie:-4}},{t:"Se coucher tôt",e:{energie:6}}]},
  {id:"client_impaye",p:4,ic:"🧾",t:"Un client ne paie pas",d:"Il promet « le mois prochain incha'Allah »…",
   choix:[{t:"Patienter avec le sourire",e:{argent:-8000,reput:2}},{t:"Insister fermement",e:{argent:-2000,reput:-2,bonheur:-2}}],pour:["commercant","chauffeur","dev","tourisme"]},
  {id:"contrat_dev",p:0,ic:"💻",t:"Un contrat de développement !",d:"Une boutique veut un site vitrine. C'est ta chance.",
   choix:[{t:"Accepter et bosser dur",e:{argent:45000,energie:-12,xp:5}},{t:"Trop compliqué pour l'instant",e:{bonheur:-2}}],pour:["dev"]},
  {id:"cyclone_annonce",p:2,ic:"🌀",t:"Alerte cyclonique",d:"La radio annonce un cyclone au large.",
   choix:[{t:"Protéger la maison (10 000 KMF)",e:{argent:-10000,sante:2}},{t:"Faire confiance au destin",e:{_risque:true}}]},
  {id:"naissance_voisin",p:4,ic:"👶",t:"Naissance chez les voisins",d:"Un petit garçon ! Le quartier célèbre.",
   choix:[{t:"Apporter un cadeau (4 000 KMF)",e:{argent:-4000,bonheur:4,reput:3}},{t:"Féliciter simplement",e:{bonheur:2}}]},
  {id:"deces_village",p:3,ic:"🕌",t:"Deuil au village",d:"Un ancien s'est éteint. Tout le monde participe.",
   choix:[{t:"Participer dignement (5 000 KMF)",e:{argent:-5000,spirit:6,reput:4,bonheur:-2}},{t:"Présenter ses condoléances",e:{spirit:2,reput:1,bonheur:-2}}]}
];

/* ---------------- ÉVÉNEMENTS FAMILLE (sexe respecté) ---------------- */
function pretendant(){return (L.sexe==="f"?PRETENDANTS:PRETENDANTES)[Math.floor(Math.random()*6)];}
function epx(){return L.sexe==="f"?"ton époux":"ton épouse";}
var FAM_EVENTS=[
  {id:"rencontre",ic:"💞",t:"Une belle rencontre…",cond:function(){return !L.conjoint&&!L.fiance&&L.age>=21&&L.bonheur>=35;},p:0.16,
   d:function(){L._pretendant=pretendant();return "Au mariage d'une cousine, ton regard croise celui de "+L._pretendant+". Les anciens ont remarqué…";},
   choix:[{t:"Se fiancer (40 000 KMF de cadeaux)",f:function(){if(L.argent<CFG.fiancailles){alert("Pas assez pour les cadeaux de fiançailles !");return false;}L.argent-=CFG.fiancailles;L.fiance=L._pretendant;bouge({bonheur:12,reput:3});hist("💞 Fiançailles avec "+L.fiance+" !");}},
          {t:"Pas encore prêt(e)",f:function(){bouge({bonheur:-2});}}]},
  {id:"mariage",ic:"💍",t:"Le grand jour approche",cond:function(){return L.fiance&&!L.conjoint;},p:0.5,
   d:function(){return "Les deux familles sont d'accord. Comment célébrer ton mariage avec "+L.fiance+" ?";},
   choix:[{t:"Mariage simple (200 000 KMF)",f:function(){if(L.argent<CFG.mariageSimple){alert("Pas assez d'argent pour le mariage — économise !");return false;}L.argent-=CFG.mariageSimple;L.conjoint={nom:L.fiance};L.fiance=null;bouge({bonheur:18,spirit:6,reput:5});hist("💍 Mariage avec "+L.conjoint.nom+" — que du bonheur !");}},
          {t:"Attendre d'avoir plus de moyens",f:function(){bouge({bonheur:-1});}}]},
  {id:"grand_mariage",ic:"👑",t:"Le GRAND MARIAGE (anda)",cond:function(){return L.conjoint&&!L.grandMariage&&L.argent>=CFG.grandMariage;},p:0.35,
   d:function(){return "Tu as les moyens d'organiser l'anda : des semaines de fêtes, le village entier, le statut de NOTABLE à vie. 1 200 000 KMF.";},
   choix:[{t:"Organiser l'anda ! (1 200 000 KMF)",f:function(){L.argent-=CFG.grandMariage;L.grandMariage=true;bouge({bonheur:20,spirit:10,reput:30});hist("👑 GRAND MARIAGE accompli — te voilà notable de Mohéli !");}},
          {t:"Plus tard",f:function(){}}]},
  {id:"naissance",ic:"👶",t:"Un heureux événement !",cond:function(){return L.conjoint&&L.enfants.length<6&&L.age<=50;},p:0.14,
   d:function(){return L.conjoint.nom+" et toi attendez un enfant. Le quartier prépare déjà les youyous…";},
   choix:[{t:"Accueillir le bébé (10 000 KMF de fête)",f:function(){var g=Math.random()<0.5;var nom=(g?PRENOMS_G:PRENOMS_F)[Math.floor(Math.random()*12)];L.argent-=10000;L.enfants.push({nom:nom,g:g?"g":"f",age:0,etudes:false,parti:false});bouge({bonheur:16,spirit:5,reput:3});hist("👶 Naissance de "+nom+" ! La famille s'agrandit.");}}]},
  {id:"enfant_malade",ic:"🤒",t:"Un enfant est malade",cond:function(){return L.enfants.some(function(e){return e.age<15&&!e.parti;});},p:0.08,
   d:function(){return "Fièvre depuis deux jours. Direction l'hôpital ?";},
   choix:[{t:"Hôpital tout de suite (10 000 KMF)",f:function(){L.argent-=10000;bouge({bonheur:3});hist("🤒 Petite frayeur — l'enfant va mieux.");}},
          {t:"Attendre que ça passe",f:function(){bouge({bonheur:-8});if(Math.random()<0.3){L.argent-=25000;hist("🚑 Ça a empiré : 25 000 KMF d'urgences.");}}}]},
  {id:"etudes_enfant",ic:"🎓",t:"L'université pour ton enfant ?",cond:function(){return L.enfants.some(function(e){return e.age>=18&&e.age<=19&&!e.etudes&&!e.parti&&!e.travaille;});},p:0.6,
   d:function(){var e=L.enfants.find(function(x){return x.age>=18&&x.age<=19&&!x.etudes&&!x.parti&&!x.travaille;});L._enfEtudes=e;return e.nom+" a fini le lycée avec de bons résultats. L'université à Moroni coûte 60 000 KMF/an pendant 4 ans.";},
   choix:[{t:"Payer les études (60 000/an)",f:function(){L._enfEtudes.etudes=true;bouge({bonheur:8,reput:4});hist("🎓 "+L._enfEtudes.nom+" part étudier à Moroni. Fierté !");}},
          {t:"Il/elle travaillera au village",f:function(){L._enfEtudes.travaille=true;bouge({bonheur:-3});hist("💼 "+L._enfEtudes.nom+" commence à travailler au village.");}}]},
  {id:"conjoint_projet",ic:"🧵",t:"Le projet du foyer",cond:function(){return !!L.conjoint&&!L.conjointBiz;},p:0.06,
   d:function(){return L.conjoint.nom+" veut lancer un petit commerce au marché : 60 000 KMF pour démarrer.";},
   choix:[{t:"Financer le projet (60 000 KMF)",f:function(){if(L.argent<60000){alert("Pas assez d'argent !");return false;}L.argent-=60000;L.conjointBiz=true;bouge({bonheur:8,reput:2});hist("🧵 "+L.conjoint.nom+" lance son petit commerce (+15 000 KMF/mois pour le foyer).");}},
          {t:"Pas maintenant",f:function(){bouge({bonheur:-4});}}]}
];

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

function nouveauJeu(nom,metierId,sexe,avatar){
  var m=byId(METIERS,metierId);
  return {v:3,nom:nom,sexe:sexe||"h",avatar:avatar||AVATARS[sexe||"h"][0],
    metier:metierId,niveau:m.debut||0,emploi:true,
    annee:2026,mois:6,age:CFG.ageDepart,moisJoues:0,generation:1,village:"fomboni",
    argent:CFG.argentDepart,patrimoine:[],entreprises:[],
    sante:90,energie:85,bonheur:70,spirit:60,reput:30,xp:0,
    tontine:0,internet:false,ordinateur:false,maison:false,villa:false,moto:false,
    conjoint:null,fiance:null,enfants:[],grandMariage:false,conjointBiz:false,
    confort:"normal",salairePDG:CFG.pdgMin,dernierNetBiz:0,
    loisirsMois:-1,loisirsFaits:0,loisirsUniques:[],
    eco:{tour:1,infl:0},partages:0,partMois:-1,pseudo:null,_recents:[],
    histoire:[{t:"🌅 "+nom+" commence sa vie à Mohéli comme "+m.niveaux[m.debut||0].t.toLowerCase()+", à Fomboni.",age:CFG.ageDepart,an:2026}],
    maj:Date.now()};
}
function migrer(s){
  if(s.v===3)return s;
  var n=nouveauJeu(s.nom,s.metier,s.sexe||"h",s.avatar);
  ["niveau","emploi","annee","mois","age","moisJoues","generation","village","argent","patrimoine","entreprises","sante","energie","bonheur","spirit","reput","xp","tontine","internet","ordinateur","maison","moto","conjoint","fiance","enfants","grandMariage","conjointBiz","eco","partages","partMois","pseudo","histoire"].forEach(function(k){if(s[k]!==undefined)n[k]=s[k];});
  (n.entreprises||[]).forEach(function(b){if(b.caisse===undefined)b.caisse=0;});
  n.v=3;n.maj=Date.now();
  if(s.v===1||s.v===2)n.histoire.unshift("✨ Ton monde évolue : profil, salaire de PDG, loisirs et vraie gestion d'entreprise sont arrivés !");
  return n;
}
function byId(arr,id){return arr.find(function(x){return x.id===id});}
function metierOf(){return byId(METIERS,L.metier);}
function villageOf(){return byId(VILLAGES,L.village)||VILLAGES[0];}
function bonusVillage(tag){var b=villageOf().bonus||{};return b[tag]||1;}

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
function chargerLocal(){try{var s=JSON.parse(localStorage.getItem("mg_life")||"null");if(s&&s.v>=1&&s.v<=3)return migrer(s);}catch(e){}return null;}
function cloudPull(cb){
  if(!cloudOK())return cb(null);
  try{
    (typeof sbUid==="function"?sbUid():Promise.resolve(null)).then(function(uid){
      if(!uid)return cb(null);
      sb.from("life_saves").select("save").eq("user_id",uid).maybeSingle().then(function(r){
        var s=r&&r.data&&r.data.save;cb(s&&s.v>=1&&s.v<=3?migrer(s):null);
      },function(){cb(null);});
    });
  }catch(e){cb(null);}
}

/* ---------------- OUTILS ---------------- */
function fmt(n){return (Math.round(n)||0).toLocaleString("fr-FR")+" KMF";}
function clamp(v){return Math.max(0,Math.min(100,Math.round(v)));}
function bouge(e){
  if(!e)return;
  if(e.argent)L.argent+=e.argent;
  if(e.sante)L.sante=clamp(L.sante+e.sante);
  if(e.energie)L.energie=clamp(L.energie+e.energie);
  if(e.bonheur)L.bonheur=clamp(L.bonheur+e.bonheur);
  if(e.spirit)L.spirit=clamp(L.spirit+e.spirit);
  if(e.reput)L.reput=clamp(L.reput+e.reput);
  if(e.xp)L.xp+=e.xp;
  if(e._tontine)L.tontine++;
  if(e._risque&&Math.random()<0.35){L.sante=clamp(L.sante-12);L.argent-=8000;L._msgRisque="⚠️ Le risque s'est retourné contre toi : −12 santé, −8 000 KMF.";}
}
/* Journal de vie : chaque entrée garde l'âge et l'année (les anciennes
   sauvegardes ont des textes simples — le rendu accepte les deux). */
function hist(t,k){L.histoire.unshift({t:t,age:L.age,an:L.annee,k:k||null});if(L.histoire.length>120)L.histoire.length=120;}
function ciel(mois){return (mois>=10||mois<=2)?"linear-gradient(160deg,#1a2f52 0%,#274a72 45%,#3b6d8f 100%)":"linear-gradient(160deg,#0e2240 0%,#14406b 45%,#1f6f95 100%)";}
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
  L.entreprises.forEach(function(b){var dd=byId(BIZ,b.type);t+=dd.prix+(b.niv-1)*dd.prix*0.5;});
  return Math.round(t);
}
function pdgMax(){return CFG.pdgMin+Math.round(Math.max(0,L.dernierNetBiz)*CFG.pdgPartActivite);}

/* ---------------- LE MOIS ---------------- */
function salaireDuMois(mer){
  if(!L.emploi)return{montant:0,note:""};
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
  return {montant:sal,note:note};
}
/* Les entreprises versent dans leur CAISSE ; le PDG se paie un SALAIRE (réglable). */
function revenusEntreprises(mer){
  var lignes=[],netTotal=0;
  L.entreprises.forEach(function(b){
    if(b.caisse===undefined)b.caisse=0;
    var t=byId(BIZ,b.type),brut;
    if(b.type==="startup"){
      // la tech BRÛLE au début, explose ensuite — sans plafond
      if(b.niv<3){brut=Math.random()<0.3?Math.round(80000*b.niv*Math.random()):0;}
      else{brut=Math.random()<0.22?Math.round(1000000*b.niv*(1+Math.random()*4)):Math.round(120000*b.niv*Math.random());}
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
    var charges=b.emp*CFG.salaireEmploye+Math.round(t.prix*0.008);
    var net=Math.round(Math.min(brut,CFG.bizCapMois)-charges);   // ⛔ plafond 15 M/mois (hors tech)
    b.caisse+=net;netTotal+=net;
    lignes.push({n:t.ic+" "+t.n+(b.emp?" ("+b.emp+" emp.)":""),v:net});
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
  if(L.conjointBiz){L.argent+=15000;lignes.push({n:"🧵 Commerce du foyer",v:15000,_direct:true});netTotal+=0;}
  L.dernierNetBiz=Math.max(0,netTotal);
  return {lignes:lignes,pdg:pdg};
}
function depensesDuMois(){
  var conf=CFG.confort[L.confort]||CFG.confort.normal;
  var inflation=(1+L.eco.infl)*conf.m,lignes=[],total=0;
  CFG.depenses.forEach(function(dd){var v=Math.round(dd.base*inflation);lignes.push({n:dd.n,v:v});total+=v;});
  if(!L.maison&&!L.villa){var lo=Math.round(CFG.loyer*(1+L.eco.infl));lignes.push({n:"🏠 Loyer",v:lo});total+=lo;}
  if(L.maison){lignes.push({n:"🏠 Entretien maison",v:CFG.maison.entretien});total+=CFG.maison.entretien;}
  if(L.villa){lignes.push({n:"🏖️ Entretien villa",v:CFG.villa.entretien});total+=CFG.villa.entretien;}
  if(L.internet){lignes.push({n:"🌐 Internet",v:CFG.internet});total+=CFG.internet;}
  if(L.conjoint){lignes.push({n:"💑 Foyer",v:CFG.conjointCout});total+=CFG.conjointCout;}
  var nKids=L.enfants.filter(function(e){return !e.parti&&!e.travaille;}).length;
  if(nKids){var ck=nKids*CFG.enfantCout;lignes.push({n:"👧 Enfants ×"+nKids,v:ck});total+=ck;}
  var etudiants=L.enfants.filter(function(e){return e.etudes&&e.age<=22;}).length;
  if(etudiants){var ce=Math.round(etudiants*CFG.etudesAn/12);lignes.push({n:"🎓 Études ×"+etudiants,v:ce});total+=ce;}
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
  if(!L.emploi)return null;
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

/* ---------------- CSS (v94 : layout façon BitLife, habillage MoheliGo) ---------------- */
var CSS=
"#mgl-root{position:fixed;inset:0;z-index:99990;background:#0b1830;color:#eef4ff;font-family:inherit;display:flex;flex-direction:column;overflow:hidden}"+
"#mgl-root *{box-sizing:border-box;margin:0;padding:0}"+
"#mgl-sky{position:absolute;inset:0;transition:background 1s}"+
"#mgl-waves{position:absolute;left:0;right:0;bottom:0;height:120px;background:radial-gradient(120% 70% at 50% 130%,rgba(46,155,214,.45),transparent 70%);pointer-events:none}"+
/* barre du HAUT sticky : identité à gauche, argent toujours visible */
"#mgl-top{position:relative;z-index:5;display:none;padding:9px 12px 8px;background:rgba(9,18,38,.72);border-bottom:1px solid rgba(255,255,255,.1);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}"+
".mgl-tprow{display:flex;align-items:center;gap:9px}"+
".mgl-tpav{font-size:27px;flex:none}"+
".mgl-tpid{flex:1;min-width:0}"+
".mgl-tpnom{font-weight:900;font-size:14.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"+
".mgl-tpsub{font-size:11px;opacity:.75;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"+
".mgl-tpargent{font-size:19px;font-weight:900;color:#F6BC1C;white-space:nowrap}"+
".mgl-wrap{position:relative;flex:1;overflow-y:auto;-webkit-overflow-scrolling:touch;padding:12px 14px 18px;max-width:520px;margin:0 auto;width:100%}"+
".mgl-glass{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:18px;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);padding:14px;margin-bottom:12px;box-shadow:0 10px 30px rgba(0,0,0,.25)}"+
".mgl-x{background:rgba(255,255,255,.12);border:none;color:#fff;width:32px;height:32px;border-radius:10px;font-size:15px;cursor:pointer;flex:none}"+
".mgl-title{font-weight:900;font-size:17px}"+
".mgl-sub{font-size:11.5px;opacity:.75}"+
".mgl-bar{height:7px;border-radius:99px;background:rgba(255,255,255,.12);overflow:hidden;margin-top:4px}"+
".mgl-bar>i{display:block;height:100%;border-radius:99px;transition:width .6s}"+
".mgl-stats{display:grid;grid-template-columns:1fr 1fr;gap:9px 14px;font-size:11.5px}"+
".mgl-btn{width:100%;border:none;border-radius:16px;padding:15px;font-size:15.5px;font-weight:900;cursor:pointer;color:#fff;background:linear-gradient(135deg,#129E63,#0E9BB5);box-shadow:0 8px 22px rgba(18,158,99,.35)}"+
".mgl-btn:active{transform:scale(.98)}"+
".mgl-btn.ghost{background:rgba(255,255,255,.1);box-shadow:none;font-weight:700;font-size:13px;padding:11px}"+
".mgl-choice{display:block;width:100%;text-align:left;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.07);color:#fff;border-radius:14px;padding:12px;font-size:13.5px;margin-top:8px;cursor:pointer}"+
".mgl-choice:active{background:rgba(255,255,255,.16)}"+
".mgl-job{display:flex;gap:11px;align-items:center;border:1px solid rgba(255,255,255,.15);background:rgba(255,255,255,.06);border-radius:16px;padding:12px;margin-bottom:9px;cursor:pointer}"+
".mgl-job:active{background:rgba(255,255,255,.14)}"+
".mgl-job .ic{font-size:26px}"+
".mgl-line{display:flex;justify-content:space-between;font-size:12.5px;padding:2.5px 0}"+
".mgl-badge{display:inline-block;background:rgba(246,188,28,.18);border:1px solid rgba(246,188,28,.4);color:#F6BC1C;border-radius:99px;padding:2px 10px;font-size:10.5px;font-weight:800;margin-left:6px}"+
".mgl-in{width:100%;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;border-radius:12px;padding:12px;font-size:14px;margin-top:8px}"+
".mgl-in::placeholder{color:rgba(255,255,255,.4)}"+
".mgl-av{display:inline-flex;width:52px;height:52px;border-radius:16px;background:rgba(255,255,255,.1);border:2px solid transparent;font-size:30px;align-items:center;justify-content:center;cursor:pointer;margin:4px 6px 0 0}"+
".mgl-av.on{border-color:#F6BC1C;background:rgba(246,188,28,.15)}"+
/* 📖 le JOURNAL DE VIE (écran central) */
".mgl-jsep{text-align:center;color:#F6BC1C;font-weight:900;font-size:12px;letter-spacing:1.5px;margin:14px 0 4px}"+
".mgl-jline{font-size:13px;line-height:1.5;padding:4px 0;border-bottom:1px dashed rgba(255,255,255,.07)}"+
".mgl-jline.mois{opacity:.62;font-size:11px;font-weight:800;letter-spacing:.4px;margin-top:7px;border-bottom:none;text-transform:uppercase}"+
/* ❤️⚡😊🕌 les 4 stats FIXES au-dessus de la nav */
"#mgl-stbar{position:relative;z-index:5;display:none;gap:10px;padding:7px 14px;background:rgba(9,18,38,.82);border-top:1px solid rgba(255,255,255,.08);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}"+
"#mgl-stbar .st{flex:1;display:flex;align-items:center;gap:5px;font-size:12px}"+
"#mgl-stbar .st .mgl-bar{flex:1;margin-top:0}"+
/* la NAVIGATION du bas (5 items, le bouton du mois au centre) */
"#mgl-nav{position:relative;z-index:5;display:none;align-items:stretch;background:rgba(7,14,30,.94);border-top:1px solid rgba(255,255,255,.08);padding:7px 4px calc(8px + env(safe-area-inset-bottom))}"+
"#mgl-nav button{flex:1;background:none;border:none;color:#9fb4d8;font-size:19px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:2px;padding:5px 0 3px;border-radius:12px}"+
"#mgl-nav button span{font-size:9.5px;font-weight:800;letter-spacing:.2px}"+
"#mgl-nav button.on{color:#F6BC1C;background:rgba(246,188,28,.08)}"+
"#mgl-navgap{width:86px;flex:none}"+
/* 🌙 LE BOUTON DU MOIS : ROND, au CENTRE de la nav */
"#mgl-fab{position:absolute;left:50%;transform:translateX(-50%);bottom:calc(14px + env(safe-area-inset-bottom));width:76px;height:76px;border-radius:50%;border:none;cursor:pointer;z-index:8;"+
 "background:linear-gradient(135deg,#129E63,#0E9BB5);color:#fff;box-shadow:0 10px 30px rgba(18,158,99,.5),0 0 0 6px rgba(255,255,255,.08);"+
 "display:none;flex-direction:column;align-items:center;justify-content:center;font-weight:900}"+
"#mgl-fab:active{transform:translateX(-50%) scale(.94)}"+
"#mgl-fab .lune{font-size:27px;line-height:1}"+
"#mgl-fab .lbl{font-size:9px;letter-spacing:.3px;margin-top:2px;opacity:.95}"+
"@keyframes mglpulse{0%,100%{box-shadow:0 10px 30px rgba(18,158,99,.5),0 0 0 6px rgba(255,255,255,.08)}50%{box-shadow:0 10px 34px rgba(18,158,99,.65),0 0 0 10px rgba(255,255,255,.05)}}"+
"#mgl-fab{animation:mglpulse 2.4s ease-in-out infinite}"+
/* 🎭 la POPUP d'événement (façon BitLife) */
"#mgl-modal{position:absolute;inset:0;z-index:20;display:none;align-items:flex-end;justify-content:center;background:rgba(3,8,20,.7);backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);padding:14px}"+
"#mgl-modal.on{display:flex}"+
"#mgl-mbox{width:100%;max-width:480px;background:rgba(18,32,60,.97);border:1px solid rgba(255,255,255,.16);border-radius:22px;padding:18px;margin-bottom:calc(10px + env(safe-area-inset-bottom));box-shadow:0 -10px 40px rgba(0,0,0,.5);max-height:80%;overflow-y:auto}"+
".mgl-mic{font-size:46px;text-align:center;line-height:1.1}"+
"@keyframes mglpop{from{transform:translateY(14px);opacity:0}to{transform:none;opacity:1}}"+
".mgl-pop{animation:mglpop .35s ease}";

/* ---------------- UI v94 (façon BitLife) ---------------- */
function esc2(s){var dv=document.createElement("div");dv.textContent=s==null?"":String(s);return dv.innerHTML;}
function barre(v,c){return '<div class="mgl-bar"><i style="width:'+clamp(v)+'%;background:'+c+'"></i></div>';}
function on(id,fn){var e=elRoot.querySelector("#"+id);if(e)e.onclick=fn;}
var jeuActif=false;

/* barre du HAUT : identité + ARGENT toujours visible */
function majTop(){
  if(!L)return;
  var m=metierOf(),v=villageOf();
  var titre=L.emploi?m.niveaux[L.niveau].t:"PDG"+(L.entreprises.length?" · "+L.entreprises.length+" entr.":"");
  elRoot.querySelector("#mgl-top").innerHTML=
   '<div class="mgl-tprow">'+
   '<span class="mgl-tpav">'+(L.avatar||"👤")+'</span>'+
   '<div class="mgl-tpid"><div class="mgl-tpnom">'+esc2(L.nom)+(L.grandMariage?' 👑':'')+(L.generation>1?' <span class="mgl-badge">'+L.generation+'ᵉ gén.</span>':'')+'</div>'+
   '<div class="mgl-tpsub">'+m.ic+' '+titre+' · '+L.age+' ans · '+v.ic+' '+v.n+'</div></div>'+
   '<button class="mgl-x" id="mgl-plus" title="Plus">⋯</button><button class="mgl-x" id="mgl-close2">✕</button></div>'+
   '<div class="mgl-tprow" style="margin-top:4px">'+
   '<div class="mgl-tpargent">'+fmt(L.argent)+'</div>'+
   '<div class="mgl-sub" style="flex:1;text-align:right;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">🏦 '+fmt(patrimoineTotal())+(L.entreprises.length?' · 🏢 '+fmt(caisseTotale()):'')+' · <span id="mgl-save">'+cloudEtat+'</span></div></div>';
  on("mgl-plus",menuPlus);on("mgl-close2",fermer);
}
/* les 4 stats FIXES (mini-barres toujours visibles) */
function majStats(){
  if(!L)return;
  elRoot.querySelector("#mgl-stbar").innerHTML=
   '<div class="st" title="Santé">❤️'+barre(L.sante,"#ef4444")+'</div>'+
   '<div class="st" title="Énergie">⚡'+barre(L.energie,"#f59e0b")+'</div>'+
   '<span style="width:64px;flex:none"></span>'+   // le bouton 🌙 dépasse ici, comme BitLife
   '<div class="st" title="Bonheur">😊'+barre(L.bonheur,"#22c55e")+'</div>'+
   '<div class="st" title="Spiritualité">🕌'+barre(L.spirit,"#38bdf8")+'</div>';
}
/* montre/cache l'habillage du jeu (haut + stats + nav + bouton mois) */
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
  var w=elRoot.querySelector(".mgl-wrap");w.innerHTML=html;w.scrollTop=0;
  elRoot.querySelector("#mgl-sky").style.background=ciel(L?L.mois:6);
  if(L&&jeuActif){majTop();majStats();}
}
/* popups (événements + menu ⋯) */
function modalOuvre(html){
  elRoot.querySelector("#mgl-mbox").innerHTML='<div class="mgl-pop">'+html+'</div>';
  elRoot.querySelector("#mgl-modal").className="on";
  elRoot.querySelector("#mgl-fab").style.display="none";
}
function modalFerme(){
  elRoot.querySelector("#mgl-modal").className="";
  elRoot.querySelector("#mgl-fab").style.display=jeuActif?"flex":"none";
}
/* menu ⋯ : villages, boutique, classement, inviter */
function menuPlus(){
  modalOuvre('<div class="mgl-mic">🏝️</div><b style="display:block;text-align:center;font-size:16px;margin:6px 0 8px">Mohéli & plus</b>'+
   '<button class="mgl-choice" id="mgl-m-vill">🗺️ Les villages de Mohéli</button>'+
   '<button class="mgl-choice" id="mgl-m-shop">🛒 Boutique & train de vie</button>'+
   '<button class="mgl-choice" id="mgl-m-class">🏆 Le classement</button>'+
   '<button class="mgl-choice" id="mgl-m-part">📣 Inviter des amis (+10 000 KMF)</button>'+
   '<button class="mgl-choice" id="mgl-m-x" style="text-align:center;opacity:.7">Fermer</button>');
  on("mgl-m-vill",function(){modalFerme();ecranVillages();});
  on("mgl-m-shop",function(){modalFerme();ecranBoutique();});
  on("mgl-m-class",function(){modalFerme();ecranClassement();});
  on("mgl-m-part",function(){modalFerme();partager();});
  on("mgl-m-x",modalFerme);
}
/* le JOURNAL DE VIE : oldest en haut, séparateurs d'âge, lignes emoji */
function journalHTML(){
  var arr=L.histoire.slice(0,120).reverse(),h="",age=null;
  arr.forEach(function(e){
    if(typeof e==="string"){h+='<div class="mgl-jline">'+esc2(e)+'</div>';return;}
    if(e.age!=null&&e.age!==age){age=e.age;h+='<div class="mgl-jsep">— '+age+' ans · '+e.an+' —</div>';}
    h+='<div class="mgl-jline'+(e.k==="mois"?" mois":"")+'">'+esc2(e.t)+'</div>';
  });
  return h||'<div class="mgl-sub">Ta vie commence…</div>';
}

/* — accueil / création (sexe + avatar + prénom + métier) — */
function ecranAccueil(){
  majChrome(false);
  var save=chargerLocal();
  var h='<div style="text-align:center;padding:22px 0 8px" class="mgl-pop">'+
   '<div style="font-size:52px">🏝️</div><div style="font-size:24px;font-weight:900;margin:6px 0 2px">MoheliGo Life</div>'+
   '<div class="mgl-sub">Vis ta vie à Mohéli — travaille, fonde ta famille, bâtis ton empire, transmets ton héritage</div></div>';
  if(save){
    var m=byId(METIERS,save.metier)||METIERS[0];
    h+='<div class="mgl-glass mgl-pop"><b>'+(save.avatar||m.ic)+' '+esc2(save.nom)+'</b><span class="mgl-badge">'+MOIS[save.mois]+' '+save.annee+'</span>'+(save.generation>1?'<span class="mgl-badge">'+save.generation+'ᵉ génération</span>':'')+
     '<div class="mgl-sub" style="margin:4px 0 10px">'+(save.emploi?m.niveaux[save.niveau].t:"PDG")+' · '+fmt(save.argent)+'</div>'+
     '<button class="mgl-btn" id="mgl-continuer">▶️ Continuer ma vie</button>'+
     '<button class="mgl-btn ghost" id="mgl-nouvelle" style="margin-top:8px">🔄 Recommencer une nouvelle vie</button></div>';
    ecran(h);
    on("mgl-continuer",function(){L=save;sauver();ecranJeu("Bon retour à Mohéli, "+esc2(L.nom)+" ! 🌺");});
    on("mgl-nouvelle",function(){if(confirm("Effacer cette vie et tout recommencer ? (la sauvegarde cloud sera effacée aussi)")){localStorage.removeItem("mg_life");cloudEffacer();L=null;ecranAccueil();}});
    return;
  }
  var sexe=window._mglSexe||"h";
  h+='<div class="mgl-glass mgl-pop"><b>1 · Qui es-tu ?</b>'+
   '<div style="display:flex;gap:8px;margin-top:8px">'+
   '<button class="mgl-btn'+(sexe==="h"?"":" ghost")+'" style="flex:1" id="mgl-sx-h">👨🏾 Homme</button>'+
   '<button class="mgl-btn'+(sexe==="f"?"":" ghost")+'" style="flex:1" id="mgl-sx-f">👩🏾 Femme</button></div>'+
   '<div style="margin-top:10px" id="mgl-avatars">'+AVATARS[sexe].map(function(a,i){return '<span class="mgl-av'+(i===(window._mglAv||0)?" on":"")+'" data-i="'+i+'">'+a+'</span>';}).join("")+'</div>'+
   '<input class="mgl-in" id="mgl-nom" maxlength="24" placeholder="Ton prénom…" value="'+esc2(window._mglNom||"")+'"></div>'+
   '<div class="mgl-glass mgl-pop"><b>2 · Choisis ta voie :</b><div id="mgl-jobs" style="margin-top:8px"></div></div>';
  ecran(h);
  on("mgl-sx-h",function(){window._mglSexe="h";window._mglAv=0;window._mglNom=elRoot.querySelector("#mgl-nom").value;ecranAccueil();});
  on("mgl-sx-f",function(){window._mglSexe="f";window._mglAv=0;window._mglNom=elRoot.querySelector("#mgl-nom").value;ecranAccueil();});
  elRoot.querySelectorAll(".mgl-av").forEach(function(a){a.onclick=function(){window._mglAv=+a.getAttribute("data-i");elRoot.querySelectorAll(".mgl-av").forEach(function(x){x.className="mgl-av";});a.className="mgl-av on";};});
  var jb=elRoot.querySelector("#mgl-jobs");
  METIERS.forEach(function(m){
    var sal=m.freelance?"revenus variables — le plus difficile":("~"+fmt(m.niveaux[m.debut||0].sal)+"/mois");
    var dv=document.createElement("div");dv.className="mgl-job mgl-pop";
    dv.innerHTML='<span class="ic">'+m.ic+'</span><div><b>'+m.n+'</b>'+(m.type==="carriere"?'<span class="mgl-badge">GRANDE CARRIÈRE</span>':'')+
      '<div class="mgl-sub">'+m.d+'</div><div class="mgl-sub" style="color:#F6BC1C">'+sal+'</div></div>';
    dv.onclick=function(){
      var nom=(elRoot.querySelector("#mgl-nom").value||"").trim();
      if(!nom){alert("Écris ton prénom d'abord 😊");return;}
      var sx=window._mglSexe||"h";
      L=nouveauJeu(nom,m.id,sx,AVATARS[sx][window._mglAv||0]);sauver();
      window._mglNom="";
      ecranJeu("🌅 Ta vie commence à Mohéli, "+esc2(nom)+". Fais les bons choix !");
    };
    jb.appendChild(dv);
  });
}

/* — écran principal : LE JOURNAL DE VIE — */
function ecranJeu(message){
  majChrome(true);navActive(null);
  var h="";
  if(message)h+='<div class="mgl-glass mgl-pop" style="border-color:rgba(246,188,28,.35)">'+message+'</div>';
  h+='<div class="mgl-glass" style="padding:14px 14px 10px"><b style="font-size:13px">📖 Le journal de ta vie</b>'+
     '<div style="margin-top:2px">'+journalHTML()+'</div>'+
     '<div class="mgl-sub" style="text-align:center;margin-top:10px;opacity:.55">Appuie sur 🌙 pour vivre le mois suivant</div></div>';
  ecran(h);
  var w=elRoot.querySelector(".mgl-wrap");w.scrollTop=w.scrollHeight;   // le plus récent en bas, comme un vrai journal
}

/* — vivre un mois (bilan = lignes du journal, événement = popup) — */
function jouerMois(){
  L.moisJoues++;L.mois++;
  if(L.mois>11){L.mois=0;L.annee++;}
  var anniv=L.moisJoues%12===0;
  if(anniv){L.age++;L.enfants.forEach(function(e){e.age++;});}
  hist("🗓️ "+MOIS[L.mois]+" "+L.annee+" · "+saison(L.mois),"mois");
  if(anniv)L.enfants.forEach(function(e){if(e.etudes&&e.age===23){e.etudes=false;e.travaille=true;hist("🎓 "+e.nom+" est diplômé(e) et trouve un bon travail !");bouge({bonheur:6,reput:3});}});
  L.eco.tour=Math.max(0.75,Math.min(1.35,L.eco.tour+(Math.random()-0.48)*0.08));
  L.eco.infl+=CFG.inflationMois;
  var mo=L.annee*12+L.mois;
  if(L.loisirsMois!==mo){L.loisirsMois=mo;L.loisirsFaits=0;}
  var mer=merReelle();
  var sal=salaireDuMois(mer);L.argent+=sal.montant;
  var biz=revenusEntreprises(mer);
  var dep=depensesDuMois();L.argent-=dep.total;
  var fatigueBiz=L.emploi?L.entreprises.length*4:Math.max(0,L.entreprises.length*2-2);
  L.energie=clamp(L.energie-6-fatigueBiz+(L.moto?2:0));
  L.bonheur=clamp(L.bonheur-2+(villageOf().bonus.bonheur||0)+(dep.conf.bonheur||0));
  if(dep.conf.sante)L.sante=clamp(L.sante+dep.conf.sante);
  if(L.energie<25)L.sante=clamp(L.sante-6);
  if(L.emploi)L.xp+=2;
  var m=metierOf();
  if(m.fatigue&&L.emploi)L.energie=clamp(L.energie-3);
  if(m.reputation&&L.emploi)L.reput=clamp(L.reput+1);
  if(L.age>=55)L.sante=clamp(L.sante-1);
  var fete=feteDuMois();if(fete)bouge(fete.e);
  /* le bilan du mois s'écrit DANS le journal */
  if(L.emploi&&sal.montant)hist("💵 Salaire"+sal.note+" : +"+fmt(sal.montant));
  var netBiz=0;
  biz.lignes.forEach(function(l){if(l._direct)hist(l.n+" : +"+fmt(l.v));else netBiz+=l.v;});
  if(L.entreprises.length)hist("🏢 Entreprises : "+(netBiz>=0?"+":"−")+fmt(Math.abs(netBiz))+" dans les caisses");
  if(biz.pdg)hist("👔 Ton salaire de PDG : +"+fmt(biz.pdg));
  hist("💸 Dépenses du mois : −"+fmt(dep.total)+" · reste "+fmt(L.argent)+" en poche");
  if(mer!=null)hist("🌊 La vraie mer de Mohéli : "+(mer===0?"calme":(mer===1?"modérée":"agitée"))+" (météo MoheliGo en direct)");
  if(fete)hist(fete.ic+" "+fete.t+" — "+fete.d);
  var promo=verifierPromotion();
  if(L.sante<=0){L.argent-=20000;L.sante=35;L.energie=40;hist("🏥 Hospitalisé d'épuisement : 20 000 KMF de soins. Lève le pied (les 🎉 Loisirs aident) !");}
  if(L.argent<0)hist("🕳️ Tu es endetté — la boutique fait crédit… mais pas longtemps. Trouve vite des revenus !");
  if(verifierMort()){sauver();return ecranHeritage();}
  sauver();
  var ev=tirerEvenement();
  L._recents=[ev.id].concat(L._recents||[]).slice(0,3);
  ecranJeu();
  modalEvenement(ev);
}

/* — l'événement du mois, en POPUP façon BitLife — */
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

/* — héritage — */
function ecranHeritage(){
  majChrome(false);
  var heritiers=L.enfants.filter(function(e){return e.age>=18;});
  var resume="⚰️ "+L.nom+" s'est éteint(e) paisiblement à "+L.age+" ans"+(L.grandMariage?", NOTABLE de Mohéli":"")+". Patrimoine : "+fmt(patrimoineTotal())+".";
  var h='<div style="text-align:center;padding:22px 0 6px" class="mgl-pop"><div style="font-size:46px">🕊️</div>'+
   '<div style="font-size:20px;font-weight:900;margin:6px 0">Une vie s\'achève…</div></div>'+
   '<div class="mgl-glass mgl-pop">'+esc2(resume)+'</div>';
  if(heritiers.length){
    h+='<div class="mgl-glass mgl-pop"><b>🎁 L\'héritage</b><div class="mgl-sub" style="margin:4px 0 8px">L\'héritage est partagé selon la tradition. Choisis l\'enfant qui continue l\'histoire :</div><div id="mgl-herit"></div></div>';
  }else{
    h+='<div class="mgl-glass mgl-pop"><b>🌪️ Fin de lignée</b><div class="mgl-sub" style="margin-top:4px">Aucun enfant adulte pour reprendre le flambeau. Mohéli n\'oubliera pas '+esc2(L.nom)+'.</div>'+
     '<button class="mgl-btn" id="mgl-renaitre" style="margin-top:10px">🌅 Commencer une nouvelle histoire</button></div>';
  }
  ecran(h);
  if(heritiers.length){
    var hb=elRoot.querySelector("#mgl-herit");
    heritiers.forEach(function(e){
      var dv=document.createElement("div");dv.className="mgl-job";
      dv.innerHTML='<span class="ic">'+(e.g==="g"?"👨🏾":"👩🏾")+'</span><div><b>'+esc2(e.nom)+'</b><div class="mgl-sub">'+e.age+' ans · '+(e.travaille?"travaille déjà":(e.etudes?"études supérieures":"au village"))+'</div></div>';
      dv.onclick=function(){herite(e);};
      hb.appendChild(dv);
    });
  }else on("mgl-renaitre",function(){localStorage.removeItem("mg_life");L=null;ecranAccueil();});
}
function herite(enfant){
  var part=Math.round((L.argent>0?L.argent:0)*0.6);
  var ancien=L.nom,gen=L.generation+1;
  var sx=enfant.g==="g"?"h":"f";
  var n=nouveauJeu(enfant.nom,L.metier,sx,AVATARS[sx][0]);
  n.generation=gen;n.age=enfant.age;n.argent=part+15000;
  n.annee=L.annee;n.mois=L.mois;   // l'histoire continue la même année (le journal affiche les années)
  n.village=L.village;n.maison=L.maison;n.villa=L.villa;n.moto=L.moto;n.ordinateur=L.ordinateur;n.internet=L.internet;
  n.entreprises=L.entreprises;n.patrimoine=L.patrimoine;
  n.niveau=enfant.etudes||enfant.travaille?1:0;n.emploi=true;
  n.reput=clamp(20+(L.grandMariage?15:0)+Math.round(L.reput*0.3));
  n.histoire=[{t:"🕊️ "+enfant.nom+" reprend le flambeau de "+ancien+" ("+gen+"ᵉ génération). Héritage : "+fmt(part)+(L.entreprises.length?" + les entreprises familiales":"")+".",age:n.age,an:n.annee}];
  L=n;sauver();
  ecranJeu("🕊️ Repose en paix, "+esc2(ancien)+". À toi d'écrire la suite, "+esc2(enfant.nom)+".");
}

/* — famille — */
function ecranFamille(){
  navActive("famille");
  var h='<div class="mgl-glass mgl-pop"><b>👨‍👩‍👧 Ma famille</b>';
  if(L.conjoint)h+='<div class="mgl-line"><span>💑 '+esc2(L.conjoint.nom)+(L.grandMariage?" 👑":"")+'</span><span>'+(L.conjointBiz?"commerce au marché":"au foyer")+'</span></div>';
  else if(L.fiance)h+='<div class="mgl-line"><span>💞 Fiancé(e) : '+esc2(L.fiance)+'</span><span>le mariage approche…</span></div>';
  else h+='<div class="mgl-sub">Célibataire — les rencontres arrivent avec le temps (et le bonheur 😊)</div>';
  if(L.enfants.length){
    h+='<div style="margin-top:8px;font-weight:800;font-size:13px">Enfants :</div>';
    L.enfants.forEach(function(e){
      h+='<div class="mgl-line"><span>'+(e.g==="g"?"👦🏾":"👧🏾")+' '+esc2(e.nom)+'</span><span>'+e.age+' an'+(e.age>1?"s":"")+' · '+(e.travaille?"travaille":(e.etudes?"🎓 études":(e.age>=5?"école":"bébé")))+'</span></div>';
    });
  }
  h+='</div><div class="mgl-glass mgl-pop mgl-sub">Les grands moments (fiançailles, mariage, anda, naissances, études) arrivent au fil des mois — selon ton âge, ton bonheur et ton argent. 🌺</div>'+
   '<button class="mgl-btn ghost" id="mgl-retour">← Retour au journal</button>';
  ecran(h);on("mgl-retour",function(){ecranJeu();});
}

/* — 💼 carrière : changer de travail / reprendre un emploi — */
function ecranCarriere(){
  navActive("carriere");
  var m=metierOf();
  var h='<div class="mgl-glass mgl-pop"><b>💼 Ma carrière</b>'+
   '<div class="mgl-stats" style="margin:8px 0 2px"><div>⭐ Réputation '+barre(L.reput,"#a78bfa")+'</div>'+
   '<div>📈 Expérience '+barre(L.emploi?L.xp*100/((L.niveau+1)*24):0,"#F6BC1C")+'</div></div>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">'+(L.emploi?("Aujourd'hui : "+m.ic+" "+m.niveaux[L.niveau].t):"Tu es PDG à plein temps (sans emploi salarié).")+'</div>'+
   (L.emploi?'<div class="mgl-sub">Changer de métier = repartir au premier niveau du nouveau métier (ton expérience du terrain compte : +1 niveau si tu as déjà été promu).</div>':'<div class="mgl-sub">Reprendre un emploi te redonne un salaire fixe — mais attention à la fatigue si tu gardes tes entreprises.</div>')+
   '</div><div class="mgl-glass mgl-pop"><b>'+(L.emploi?"Changer de métier :":"Reprendre un emploi :")+'</b><div id="mgl-metiers" style="margin-top:8px"></div></div>'+
   '<button class="mgl-btn ghost" id="mgl-retour">← Retour au journal</button>';
  ecran(h);
  var zm=elRoot.querySelector("#mgl-metiers");
  METIERS.forEach(function(mm){
    if(L.emploi&&mm.id===L.metier)return;
    var dv=document.createElement("div");dv.className="mgl-job";
    var sal=mm.freelance?"revenus variables":("~"+fmt(mm.niveaux[0].sal)+" → "+fmt(mm.niveaux[mm.niveaux.length-1].sal));
    dv.innerHTML='<span class="ic">'+mm.ic+'</span><div><b>'+mm.n+'</b><div class="mgl-sub">'+mm.d+'</div><div class="mgl-sub" style="color:#F6BC1C">'+sal+'</div></div>';
    dv.onclick=function(){
      if(!confirm((L.emploi?"Changer de métier pour":"Devenir")+" « "+mm.n+" » ?"))return;
      var bonusNiv=(L.niveau>0&&L.emploi)?1:0;
      L.metier=mm.id;L.niveau=Math.min(bonusNiv,mm.niveaux.length-1);L.xp=0;L.emploi=true;
      hist("💼 "+L.nom+" devient "+mm.niveaux[L.niveau].t+" ("+mm.n+").");bouge({bonheur:4,energie:-4});
      sauver();ecranJeu("💼 Nouveau départ : "+mm.ic+" "+mm.n+" — bonne chance !");
    };
    zm.appendChild(dv);
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* — 🎉 loisirs : dépenser pour le bonheur et la santé — */
function ecranLoisirs(){
  navActive("loisirs");
  var mo=L.annee*12+L.mois;
  if(L.loisirsMois!==mo){L.loisirsMois=mo;L.loisirsFaits=0;}
  var h='<div class="mgl-glass mgl-pop"><b>🎉 Loisirs & bien-être</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Dépenser pour soi, ce n\'est pas gaspiller : c\'est du bonheur et de la santé. '+(CFG.loisirsMaxMois-L.loisirsFaits)+' activité(s) restante(s) ce mois-ci.</div>'+
   '<div id="mgl-lz"></div></div>'+
   '<button class="mgl-btn ghost" id="mgl-retour">← Retour au journal</button>';
  ecran(h);
  var z=elRoot.querySelector("#mgl-lz");
  LOISIRS.forEach(function(a){
    if(a.unique&&(L.loisirsUniques||[]).indexOf(a.id)>=0)return;
    var dv=document.createElement("div");dv.className="mgl-job";
    var eff=Object.keys(a.e).map(function(k){var v=a.e[k];var ic={bonheur:"😊",sante:"❤️",energie:"⚡",spirit:"🕌",reput:"⭐"}[k]||k;return ic+(v>0?"+":"")+v;}).join(" ");
    dv.innerHTML='<span class="ic">'+a.ic+'</span><div style="flex:1"><b>'+a.n+'</b><div class="mgl-sub" style="color:#F6BC1C">'+fmt(a.p)+' · '+eff+'</div></div>';
    dv.onclick=function(){
      if(L.loisirsFaits>=CFG.loisirsMaxMois){alert("Assez de sorties pour ce mois — le travail t'attend 😄");return;}
      if(L.argent<a.p){alert("Pas assez d'argent pour ça !");return;}
      L.argent-=a.p;L.loisirsFaits++;bouge(a.e);
      if(a.unique)(L.loisirsUniques=L.loisirsUniques||[]).push(a.id);
      hist(a.ic+" "+a.n+" — ça fait du bien !");
      sauver();ecranLoisirs();
    };
    z.appendChild(dv);
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* — 🏢 entreprises (caisse + salaire PDG) — */
function ecranBiz(){
  navActive("biz");
  var h='<div class="mgl-glass mgl-pop"><b>👔 Salaire de PDG</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Tu te verses <b style="color:#F6BC1C">'+fmt(L.salairePDG||CFG.pdgMin)+'</b>/mois depuis les caisses de tes entreprises. Maximum autorisé selon ton activité : '+fmt(pdgMax())+' (200 000 + 25 % du net mensuel).</div>'+
   '<button class="mgl-btn ghost" id="mgl-pdg">⚙️ Régler mon salaire de PDG</button></div>'+
   '<div class="mgl-glass mgl-pop"><b>🏢 Mes entreprises</b>';
  if(!L.entreprises.length)h+='<div class="mgl-sub" style="margin-top:4px">Aucune pour l\'instant. Les bénéfices vont dans la CAISSE de chaque entreprise ; toi, tu touches ton salaire de PDG. ⚠️ Emploi + entreprises = fatigue (−4 énergie/mois par entreprise).</div>';
  L.entreprises.forEach(function(b,i){
    var t=byId(BIZ,b.type);
    h+='<div class="mgl-glass" style="margin:8px 0 0;padding:11px"><b>'+t.ic+' '+esc2(b.nom||t.n)+'</b><span class="mgl-badge">niv. '+b.niv+'</span>'+
     '<div class="mgl-sub">💰 Caisse : <b style="color:'+((b.caisse||0)>=0?"#4ade80":"#f87171")+'">'+fmt(b.caisse||0)+'</b> · '+b.emp+' employé(s) · pub : '+(b.pub||0)+' mois</div>'+
     '<div style="display:flex;gap:6px;flex-wrap:wrap;margin-top:8px">'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="emp" data-i="'+i+'">＋ Embaucher</button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="pub" data-i="'+i+'">📣 Pub</button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="niv" data-i="'+i+'">⬆️ Agrandir</button>'+
     '<button class="mgl-btn ghost" style="flex:1" data-a="vendre" data-i="'+i+'">💸 Vendre</button></div></div>';
  });
  h+='</div><div class="mgl-glass mgl-pop"><b>💼 Créer une entreprise</b><div class="mgl-sub">Les investissements (embauche, pub, agrandir) se paient depuis la CAISSE de l\'entreprise — la création depuis ta poche.</div><div id="mgl-achats" style="margin-top:6px"></div></div>';
  if(L.emploi&&L.entreprises.length)h+='<button class="mgl-btn ghost mgl-pop" id="mgl-quitter">🚪 Quitter mon emploi (PDG à 100 %)</button>';
  h+='<button class="mgl-btn ghost" id="mgl-retour" style="margin-top:8px">← Retour au journal</button>';
  ecran(h);
  on("mgl-pdg",function(){
    var v=prompt("Ton salaire de PDG mensuel (min "+CFG.pdgMin.toLocaleString("fr-FR")+", max "+pdgMax().toLocaleString("fr-FR")+") :",L.salairePDG||CFG.pdgMin);
    if(v==null)return;
    v=parseInt(String(v).replace(/[^\d]/g,""),10);
    if(!v||v<CFG.pdgMin){alert("Minimum : "+fmt(CFG.pdgMin));return;}
    if(v>pdgMax()){alert("Ton activité ne permet pas plus de "+fmt(pdgMax())+" pour l'instant — développe tes entreprises !");return;}
    L.salairePDG=v;hist("👔 Salaire de PDG fixé à "+fmt(v)+"/mois.");sauver();ecranBiz();
  });
  var za=elRoot.querySelector("#mgl-achats");
  BIZ.forEach(function(t){
    var bloque=t.cond==="dev3"&&!(L.metier==="dev"&&L.niveau>=3);
    var dv=document.createElement("div");dv.className="mgl-job";if(bloque)dv.style.opacity=.5;
    dv.innerHTML='<span class="ic">'+t.ic+'</span><div style="flex:1"><b>'+t.n+'</b><div class="mgl-sub">'+t.d+'</div>'+
      '<div class="mgl-sub" style="color:#F6BC1C">'+fmt(t.prix)+(t.rev?' · ~'+fmt(t.rev)+'/mois brut · plafond '+fmt(CFG.bizCapMois)+'/mois':' · SANS plafond, mais brûle de l\'argent au début')+'</div></div>';
    dv.onclick=function(){
      if(bloque){alert("Réservé aux développeurs experts (niveau 4 de la carrière dev).");return;}
      if(L.argent<t.prix){alert("Pas assez d'argent — il faut "+fmt(t.prix)+".");return;}
      if(!confirm("Créer « "+t.n+" » pour "+fmt(t.prix)+" ?"))return;
      L.argent-=t.prix;
      L.entreprises.push({type:t.id,niv:1,emp:0,pub:0,caisse:0,nom:null});
      hist("💼 "+L.nom+" crée : "+t.n+" !");bouge({reput:6,bonheur:5});
      sauver();ecranBiz();
    };
    za.appendChild(dv);
  });
  elRoot.querySelectorAll("[data-a]").forEach(function(b){
    b.onclick=function(){
      var i=+b.getAttribute("data-i"),a=b.getAttribute("data-a"),biz=L.entreprises[i],t=byId(BIZ,biz.type);
      function payeCaisse(cout,quoi){
        if((biz.caisse||0)>=cout){biz.caisse-=cout;return true;}
        if(L.argent>=cout){if(!confirm("La caisse est trop juste — payer "+fmt(cout)+" de ta poche ?"))return false;L.argent-=cout;return true;}
        alert("Ni la caisse ni ta poche ne suffisent ("+fmt(cout)+").");return false;
      }
      if(a==="emp"){if(biz.emp>=biz.niv*3){alert("Agrandis d'abord (max "+biz.niv*3+" employés).");return;}if(!payeCaisse(CFG.embauche))return;biz.emp++;hist("🤝 Embauche dans "+t.n+" ("+biz.emp+" employés).");}
      if(a==="pub"){if(!payeCaisse(CFG.pub))return;biz.pub=(biz.pub||0)+3;hist("📣 Pub pour "+t.n+" (3 mois boostés).");}
      if(a==="niv"){var c=Math.round(t.prix*0.6);if(!payeCaisse(c))return;biz.niv++;hist("⬆️ "+t.n+" passe au niveau "+biz.niv+" !");bouge({reput:3});}
      if(a==="vendre"){
        var val=Math.round(t.prix*0.6*biz.niv)+Math.max(0,biz.caisse||0);
        if(!confirm("Vendre "+t.n+" pour "+fmt(val)+" (60 % de la valeur + la caisse) ?"))return;
        L.argent+=val;L.entreprises.splice(i,1);hist("💸 "+t.n+" vendue pour "+fmt(val)+".");
      }
      sauver();ecranBiz();
    };
  });
  on("mgl-quitter",function(){
    if(!confirm("Quitter ton emploi pour te consacrer à tes entreprises ?"))return;
    L.emploi=false;hist("🚪 "+L.nom+" quitte son emploi : PDG à 100 % !");bouge({bonheur:5,energie:8});
    sauver();ecranBiz();
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* — villages — */
function ecranVillages(){
  navActive(null);
  var h='<div class="mgl-glass mgl-pop"><b>🗺️ Les villages de Mohéli</b><div class="mgl-sub" style="margin-bottom:6px">Chaque village a son économie — déménager coûte '+fmt(CFG.demenagement)+'.</div><div id="mgl-vill"></div></div>'+
   '<button class="mgl-btn ghost" id="mgl-retour">← Retour au journal</button>';
  ecran(h);
  var zv=elRoot.querySelector("#mgl-vill");
  VILLAGES.forEach(function(v){
    var ici=v.id===L.village;
    var bon=Object.keys(v.bonus).map(function(k){return k==="bonheur"?("😊 +"+v.bonus[k]):("+"+Math.round((v.bonus[k]-1)*100)+"% "+k);}).join(" · ");
    var dv=document.createElement("div");dv.className="mgl-job";if(ici)dv.style.borderColor="rgba(246,188,28,.6)";
    dv.innerHTML='<span class="ic">'+v.ic+'</span><div style="flex:1"><b>'+v.n+'</b>'+(ici?'<span class="mgl-badge">TU VIS ICI</span>':'')+'<div class="mgl-sub">'+v.d+'</div><div class="mgl-sub" style="color:#F6BC1C">'+bon+'</div></div>';
    dv.onclick=function(){
      if(ici)return;
      if(L.argent<CFG.demenagement){alert("Il faut "+fmt(CFG.demenagement)+" pour déménager.");return;}
      if(!confirm("Déménager à "+v.n+" pour "+fmt(CFG.demenagement)+" ?"))return;
      L.argent-=CFG.demenagement;L.village=v.id;
      hist("📦 Déménagement à "+v.n+" !");bouge({bonheur:4,energie:-6});
      sauver();ecranVillages();
    };
    zv.appendChild(dv);
  });
  on("mgl-retour",function(){ecranJeu();});
}

/* — classement — */
function ecranClassement(){
  navActive(null);
  var h='<div class="mgl-glass mgl-pop"><b>🏆 Les grandes familles de Mohéli</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Classées par patrimoine — publie ton score avec un pseudo (jamais ton vrai numéro).</div>'+
   '<button class="mgl-btn ghost" id="mgl-pub-score">📤 Publier mon score</button>'+
   '<div id="mgl-scores" style="margin-top:10px" class="mgl-sub">Chargement du classement…</div></div>'+
   '<button class="mgl-btn ghost" id="mgl-retour">← Retour au journal</button>';
  ecran(h);
  on("mgl-retour",function(){ecranJeu();});
  on("mgl-pub-score",function(){
    if(!cloudOK()){alert("Connecte-toi à internet pour publier ton score.");return;}
    var ps=L.pseudo||localStorage.getItem("mg_pseudo")||"";
    ps=prompt("Ton pseudo pour le classement :",ps)||"";ps=ps.trim().slice(0,24);
    if(!ps)return;
    L.pseudo=ps;
    (typeof ensureUid==="function"?ensureUid():Promise.resolve(null)).then(function(uid){
      if(!uid){alert("Impossible pour l'instant — réessaie.");return;}
      sb.from("life_scores").upsert({user_id:uid,pseudo:ps,patrimoine:patrimoineTotal(),fortune:Math.max(0,L.argent),generation:L.generation,reput:L.reput,maj:new Date().toISOString()},{onConflict:"user_id"})
        .then(function(r){if(r&&r.error){alert("Publication impossible : "+r.error.message);}else{sauver();chargerScores();}});
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

/* — partage récompensé — */
function partager(){
  var mo=L.annee*12+L.mois;
  if(L.partMois!==mo){L.partMois=mo;L.partages=0;}
  if(L.partages>=CFG.partageMaxMois){alert("Tu as déjà gagné tes 3 partages du mois — reviens le mois prochain ! 😉");return;}
  var texte="Je vis ma vie à Mohéli sur MoheliGo Life 🎮🏝️ — carrière, famille, entreprises… Viens jouer et réserver tes traversées sur https://moheligo.com !";
  var apres=function(){
    L.partages++;L.argent+=CFG.partageGain;
    hist("📣 Merci d'avoir fait connaître MoheliGo ! +"+fmt(CFG.partageGain)+" ("+L.partages+"/"+CFG.partageMaxMois+" ce mois).");
    sauver();ecranJeu("📣 +"+fmt(CFG.partageGain)+" pour ton partage — asante ! 🌺");
  };
  try{if(navigator.share){navigator.share({text:texte}).then(apres,function(){});return;}}catch(e){}
  window.open("https://wa.me/?text="+encodeURIComponent(texte),"_blank");
  setTimeout(apres,1500);
}

/* — boutique (train de vie + biens) — */
function ecranBoutique(){
  var conf=CFG.confort[L.confort]||CFG.confort.normal;
  var items=[
    {id:"ordinateur",n:"💻 Ordinateur portable",p:CFG.ordinateur,d:"Indispensable au développeur. Ouvre les vrais contrats.",cond:!L.ordinateur},
    {id:"internet",n:"🌐 Abonnement internet",p:0,d:"15 000 KMF/mois. Nécessaire pour les gros contrats.",cond:!L.internet,mensuel:true},
    {id:"moto",n:"🛵 Moto",p:CFG.moto,d:"Transport plus facile, énergie préservée.",cond:!L.moto},
    {id:"maison",n:"🏠 Maison familiale",p:CFG.maison.p,d:"Plus de loyer — mais 25 000 KMF/mois d'entretien. Un vrai patrimoine.",cond:!L.maison},
    {id:"villa",n:"🏖️ Villa au bord de mer",p:CFG.villa.p,d:"Le prestige absolu (+10 réputation) — 80 000 KMF/mois d'entretien.",cond:!L.villa&&L.maison}
  ];
  navActive(null);
  var h='<div class="mgl-glass mgl-pop"><b>🏠 Train de vie</b>'+
   '<div class="mgl-sub" style="margin:4px 0 8px">Actuellement : <b>'+conf.n+'</b>. L\'économe réduit les dépenses (mais pèse sur le moral) ; le confortable coûte cher (mais fait du bien).</div>'+
   '<div style="display:flex;gap:6px">'+
   ["econome","normal","large"].map(function(k){var c=CFG.confort[k];return '<button class="mgl-btn'+(L.confort===k?"":" ghost")+'" style="flex:1;font-size:12px;padding:10px" data-conf="'+k+'">'+c.n+'</button>';}).join("")+
   '</div></div>'+
   '<div class="mgl-glass mgl-pop"><b>🛒 Boutique & projets</b><div id="mgl-shop" style="margin-top:6px"></div></div>'+
   '<button class="mgl-btn ghost" id="mgl-retour">← Retour au journal</button>';
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
      if(!it.mensuel&&L.argent<it.p){alert("Pas assez d'argent — économise encore !");return;}
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
    elRoot.innerHTML='<div id="mgl-sky"></div><div id="mgl-waves"></div>'+
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
