# Maisha 🌺 — simulateur de vie et de dynastie

Jeu de simulation de vie inspiré de BitLife, entièrement en français, avec une
touche comorienne (prénoms, villes, événements locaux).

## Principe

Tu choisis ton personnage (fille ou garçon, prénom, lieu de naissance) puis
chaque pression sur **+ Âge** fait passer un an, jusqu'à la mort… et au-delà :
la succession est partagée entre tes enfants et tu continues la dynastie avec
l'un d'eux (génération 2, 3, 4…).

## Systèmes du jeu

- **Stats** : Santé, Bonheur, Intelligence, Apparence, Célébrité (0–100).
- **Économie réaliste** : impôts selon le pays, coût de la vie, loyer si tu
  n'es pas propriétaire, frais d'université, coût des enfants, agios en cas de
  découvert, saisie par huissier si les dettes explosent. Pas d'argent facile :
  les grosses actions rémunératrices sont limitées à une fois par an.
- **Carrière** : petits boulots dès 15 ans, 11 métiers salariés, promotions,
  augmentations.
- **Entreprendre et gérer** : 5 types d'entreprises (boutique, restaurant,
  import-export, compagnie maritime, startup), et jusqu'à **3 entreprises en
  même temps**, chacune avec sa gestion propre. À la mort, les entreprises ne
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
- **Politique** : adhère à un parti puis gravis les échelons — maire, député,
  ministre, **président**. Campagnes payantes, popularité à entretenir. Une
  fois au pouvoir : budget annuel (éducation, infrastructures, anticorruption…
  ou détournement de fonds, au risque de la destitution et de la prison).
- **Le pays vit** : chaque pays a ses stats (Développement, Économie,
  Corruption) qui évoluent, affichées avec badges « Pays développé »,
  « Très corrompu »… Crises, cyclones, booms touristiques ; le taux d'impôt
  dépend du développement.
- **Héritage** : à la mort, succession (moins 10 % de frais) partagée à parts
  égales entre les enfants ; on continue avec l'héritier de son choix, qui
  retrouve son parent survivant, ses frères et sœurs, son métier et ses
  économies personnelles.
- **Les enfants vivent leur vie** : université ou recherche d'emploi à 18 ans,
  diplôme, embauche, salaire, épargne, mariage, petits-enfants — leur fortune
  et leur situation sont visibles dans l'onglet Relations, et on peut leur
  donner de l'argent.
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
