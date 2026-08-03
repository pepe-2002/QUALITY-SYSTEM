# Maisha 🌺 — simulateur de vie et de dynastie

Jeu de simulation de vie inspiré de BitLife, entièrement en français, avec une
touche comorienne (prénoms, villes, événements locaux).

## Principe

Tu choisis ton personnage (fille ou garçon, prénom, lieu de naissance) puis
chaque pression sur **+ Âge** fait passer un an, jusqu'à la mort… et au-delà :
la succession est partagée entre tes enfants et tu continues la dynastie avec
l'un d'eux (génération 2, 3, 4…).

## Monde 3D 🌍

En haut de l'écran, **ton île en 3D temps réel** (WebGL écrit à la main, sans
aucune bibliothèque externe) : mer animée, plage, palmiers, et surtout **tes
constructions qui poussent au fil de ta vie** — la case familiale, l'école, tes
maisons achetées (studio → villa avec piscine → manoir à colonnes), tes
entreprises dont le bâtiment grandit avec leur taille (échoppe → immeuble →
tour de multinationale), la mairie, le palais présidentiel, le **palais royal
doré** si tu es couronné, l'hôpital et l'université quand ton pays se
développe, et tes véhicules (voiture, barque, yacht, **jet privé sur sa
piste**). Ta famille se promène dans le décor.

- **Fais glisser** pour tourner la caméra, molette pour zoomer.
- **Touche un bâtiment** pour ouvrir l'écran correspondant (une entreprise
  ouvre sa gestion, le palais ouvre le gouvernement, la maison les relations).
- La lumière change avec l'âge : aube dans l'enfance, plein jour à la force de
  l'âge, couchant à la vieillesse.
- Bouton **▾** pour replier la vue si tu préfères lire le journal.

## Interface

Six onglets : **Travail** (emploi, entreprises, recrutement), **Actifs**
(patrimoine, immobilier, véhicules), **Pays** (état de la nation, classement
régional, construire pour son pays, politique & royaume), **+ Âge**,
**Relations** et **Vie** (quotidien, formations, carrière de star, risques).

## Modes de difficulté

Choisis à la création : **🌴 Facile** (5 000 € au départ, vie moins chère,
embauche facile), **⚖️ Normal**, **🔥 Difficile** (vie chère, maladies
fréquentes, embauche dure, marges faibles, 20 % de frais de succession) ou
**💀 Survie** (santé fragile, presque rien ne t'est donné, 30 % de frais).
La difficulté agit sur le coût de la vie, le risque de maladie, les chances
d'embauche, les marges des entreprises et l'héritage.

## Systèmes du jeu

- **Stats** : Santé, Bonheur, Intelligence, Apparence, Célébrité et
  **Compétence pro** (0–100) — la compétence pro monte avec l'expérience,
  le travail acharné et les **formations** (cours du soir, formation
  professionnelle, bootcamp numérique & IA, MBA) et améliore embauches,
  augmentations et gestion d'entreprise. Les **employés** gagnent aussi de
  l'expérience chaque année et peuvent être envoyés en formation (2 000 €).
- **Le pays vit vraiment** : 5 stats par pays (Développement, Économie,
  Éducation, Moral du peuple, Corruption), **classement régional** des pays,
  et tu peux **construire pour ton pays** avec ta fortune (école, dispensaire,
  centre numérique & IA). Président ou monarque, tes budgets annuels incluent
  universités & recherche et **plan national IA & numérique**.
- **Économie réaliste** : impôts selon le pays, coût de la vie, loyer si tu
  n'es pas propriétaire, frais d'université, coût des enfants, agios en cas de
  découvert, saisie par huissier si les dettes explosent. Pas d'argent facile :
  les grosses actions rémunératrices sont limitées à une fois par an.
- **Carrière** : petits boulots dès 15 ans, 11 métiers salariés, promotions,
  augmentations.
- **Vrai jeu de gestion d'entreprise** : 7 types d'entreprises (boutique,
  restaurant, import-export, compagnie maritime, startup tech, BTP, banque
  d'affaires), jusqu'à **3 en même temps**. On **entre dans son entreprise**
  via un écran dédié avec tableau de bord (trésorerie, valorisation, dette,
  CA, masse salariale, résultat) et jauges de **stock, qualité, réputation** :
  - **5 stratégies** (prix bas, équilibrée, premium, expansion, innovation)
    qui changent chiffre d'affaires, marges, qualité et réputation ;
  - **approvisionnement** : sans stock, l'activité tombe à 35 % ;
  - **marketing** (pub locale / nationale / internationale), **lancement de
    produits** et **développement d'applications** qui peuvent rapporter gros ;
  - **finance** : salaire de dirigeant, dividendes taxés, renflouement,
    emprunt bancaire à 8 % ;
  - **croissance** PME → Société → Groupe → **Multinationale**, sous
    conditions de valorisation et d'effectif ;
  - **réseau d'affaires** : déjeuners avec les patrons de la place (contrats,
    partenariats, conseils… et parfois une rencontre amoureuse), rachat de
    concurrents. À la mort, les entreprises ne
  sont pas vendues : elles sont **transmises à l'héritier choisi** (qui en
  devient le patron, employés compris). L'entreprise a sa **caisse** :
  chiffre d'affaires + production des employés − masse salariale = résultat.
  Tu fixes **ton salaire de dirigeant**, tu récupères des **dividendes**
  (taxés 15 %), tu renfloues, investis, modernises, revends… Faillite après
  3 années de caisse dans le rouge.
- **Recruter la famille et les amis** : femme, enfants (dès 16 ans), frères,
  sœurs et amis ont chacun une **compétence** (0–100). Tu choisis leur poste
  (directeur adjoint, comptable, commercial, vendeur, manutentionnaire,
  gardien — chaque poste a son niveau requis et son rendement) et leur
  **salaire selon le budget**. Incompétent pour le poste → production divisée
  par deux ; sous-payé → il finit par démissionner ; tu peux augmenter,
  baisser, muter ou licencier (au risque de fâcher la famille).
- **Candidatures externes** : chaque année, des inconnus envoient leur CV
  (âge, compétence, prétention salariale). Tu peux accepter leur prétention
  ou négocier −20 % — au risque qu'ils partent à la concurrence.
- **Immobilier** : 5 biens achetables, à habiter ou **mettre en location**
  (~5 %/an de rendement, vacance locative possible, entretien 1 %/an, valeur
  qui suit l'économie).
- **Star** : chanter aux mariages, poster des clips, single, tournée
  régionale, contrats pub — la célébrité monte, retombe, et attire paparazzi
  et bad buzz.
- **Politique et gouvernement** : adhère à un parti puis gravis les échelons —
  maire, député, ministre, **président**. Une fois élu, un **écran
  Gouvernement** permet de diriger réellement le pays : répartition du
  **budget national** entre éducation, santé, infrastructures, **IA &
  numérique**, sécurité et fonction publique ; **salaire minimum** ; **salaires
  des ministres** (les réduire nourrit la corruption, les augmenter indigne le
  peuple) ; **pression fiscale** (que tu paies aussi) ; **grands projets**
  (port en eau profonde, université nationale, institut d'IA, centrale
  solaire, hôpital central) ; et le détournement de fonds, au risque de la
  destitution et de la prison.
- **Monarchie exigeante** : proclamer la monarchie demande 75 de popularité,
  15 ans de carrière politique, un peuple acquis et 500 000 € ; acheter une
  île souveraine demande 2 M€ de liquidités, 1 M€ de patrimoine, 40 de
  célébrité et de diriger au moins un Groupe.
- **Éducation des enfants** : école publique, école privée (2 500 €/an) ou
  études à l'étranger (9 000 €/an), plus des cours de soutien — ce que tu
  paies détermine leur compétence, donc leur réussite d'adulte.
- **Le pays vit** : chaque pays a ses stats (Développement, Économie,
  Corruption) qui évoluent, affichées avec badges « Pays développé »,
  « Très corrompu »… Crises, cyclones, booms touristiques ; le taux d'impôt
  dépend du développement.
- **Héritage** : à la mort, succession (moins 10 % de frais) partagée à parts
  égales entre les enfants ; on continue avec l'héritier de son choix, qui
  retrouve son parent survivant, ses frères et sœurs, son métier et ses
  économies personnelles.
- **Les enfants vivent leur vie sans te demander ton avis** : université ou
  recherche d'emploi, diplôme, embauche, licenciement, **création de leur
  propre entreprise**, voyages d'affaires, fortune personnelle (ils peuvent
  devenir **riches avant l'héritage**), **carrière politique** jusqu'à la
  présidence, mariage et petits-enfants décidés par eux… ou la chute : refus
  en série, précarité et **rue** s'ils échouent. Ils te rendent ce que tu leur
  as donné : envois d'argent, voyage offert à leurs parents, maison bâtie au
  village. Tu peux les aider (don, financer leur entreprise, les sortir de la
  rue) — leur situation complète est visible dans l'onglet Relations.
- **La famille élargie compte** : frères, sœurs et amis mènent leur carrière,
  certains font fortune. Un proche riche et proche de toi t'aide ou te **lègue
  la moitié de sa fortune** à sa mort ; un proche riche mais distant ne te
  laisse rien. Tous les 5 ans, une **réunion de famille** : tout payer et
  souder le clan, partager les frais, ou ne pas venir (et être jugé).
- **Royaumes 👑** : proclame la monarchie en tant que président populaire
  (coup risqué !) ou achète une île (400 000 €) pour fonder ton royaume.
  Sujets, trésor royal, prestige, liste civile annuelle, décisions royales
  (bâtir, festoyer, pressurer le peuple, clémence fiscale), largesses,
  ponctions dans le trésor, abdication… et révolution si le prestige
  s'effondre. Le trône se transmet aux héritiers, avec régence avant 18 ans.
- **Vraie vie** : retraite à 65 ans avec pension, maladies réelles (paludisme,
  typhoïde, dengue…) à soigner à l'hôpital sous peine de perdre sa santé
  chaque année, salaire du conjoint qui contribue au ménage.

## Technique

- Un seul fichier : `index.html` (HTML + CSS + JS, zéro dépendance, hors-ligne).
- Compatible mobile (interface pensée téléphone d'abord).
- Thème clair et sombre automatiques.
- Sauvegarde automatique dans le navigateur (localStorage).

## Déployer

Le fichier peut être ouvert directement dans un navigateur, ou déposé tel quel
sur n'importe quel hébergeur statique (Netlify, GitHub Pages…).
