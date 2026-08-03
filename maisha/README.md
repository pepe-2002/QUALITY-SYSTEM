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
- **Entreprendre** : 5 types d'entreprises (boutique, restaurant,
  import-export, compagnie maritime, startup) — capital de départ, bénéfices
  liés à l'économie du pays, investissement, modernisation, revente… et
  faillite après 3 années de pertes.
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
  retrouve son parent survivant et ses frères et sœurs.

## Technique

- Un seul fichier : `index.html` (HTML + CSS + JS, zéro dépendance, hors-ligne).
- Compatible mobile (interface pensée téléphone d'abord).
- Thème clair et sombre automatiques.
- Sauvegarde automatique dans le navigateur (localStorage).

## Déployer

Le fichier peut être ouvert directement dans un navigateur, ou déposé tel quel
sur n'importe quel hébergeur statique (Netlify, GitHub Pages…).
