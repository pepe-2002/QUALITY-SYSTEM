# ❤ « Nous » — votre messagerie privée

Une application **complètement à part**. Elle ne touche à rien : ni au code
de MoheliGo, ni à son adresse, ni à sa base de données. Son dossier est
`nous/`, à la racine du dépôt — on peut le copier, le déplacer ou le
supprimer sans que MoheliGo s'en aperçoive.

Elle est faite pour un problème précis : **vous n'avez pas toujours le
temps**. Les gens qui comptent, eux, attendent quand même.

---

## 1. L'essayer tout de suite (rien à installer)

Depuis le dossier `nous/` :

```
python3 -m http.server 8877
```

puis ouvrir **http://localhost:8877/** sur l'ordinateur. Ça marche déjà :
salon, messages, vocaux, photos, idées, rappels. Tout est gardé **dans le
navigateur** (base intégrée, IndexedDB). Rien ne sort de la machine.

> Le chiffrement exige une adresse en `https` ou `localhost` — c'est une
> règle des navigateurs, pas un choix de l'app. Ouvrir le fichier
> directement (`file://`) ne marchera pas.

## 2. La mettre sur le téléphone, et parler à deux

### a) Lui donner une adresse à elle

**Le plus simple : GitHub le fait, gratuitement, sans nouveau compte.**
Tout est préparé dans `.github/workflows/nous-pages.yml` — le robot
active Pages lui-même au premier passage, il n'y a aucun réglage à
toucher. Dès que le dossier `nous/` est sur la branche principale, le
site se publie tout seul sur :

```
https://pepe-2002.github.io/QUALITY-SYSTEM/
```

⚠️ Ce robot ne met en ligne **que le dossier `nous/`**. RA-QDMS et
MoheliGo ne partent pas là-dedans et ne bougent pas.

⚠️ GitHub n'accepte de publier Pages que depuis la **branche
principale** (`main`) : c'est sa règle, pas un choix de l'app. Le
dossier `nous/` doit donc y être fusionné pour que le lien existe.

*Autres options, si un jour vous préférez :* **Netlify Drop**
(`app.netlify.com/drop`, on glisse le dossier `nous/`, adresse `https` en
quinze secondes) ou **Cloudflare Pages** — dans ce cas, un projet et un
sous-domaine séparés, jamais la racine de moheligo.com.

Sur le téléphone, ouvrir l'adresse puis « Ajouter à l'écran d'accueil » :
ça devient une vraie application.

### b) Sa propre base de données (pour que deux téléphones se parlent)
Tant que vous êtes seul sur un appareil, il n'y a **rien à faire** : la
base est dans le téléphone. Pour que votre femme voie vos messages, il
faut un point de rendez-vous entre les deux appareils. On lui en crée un
**à elle, séparé** :

1. `supabase.com` → vous avez **déjà un compte** (celui de MoheliGo) :
   pas de compte à créer. → **New project** → nom : `nous`.
   ⚠️ Un **nouveau projet**. Pas celui de MoheliGo, jamais. Deux projets
   dans le même compte ne se voient pas : bases, clés et mots de passe
   sont séparés.
2. Dans ce projet : `SQL Editor` → coller tout `SQL-nous.sql` → **Run**.
3. `Settings` → `API` : copier **Project URL** et la clé **anon public**,
   les coller dans `nous-config.js` (les deux lignes du haut).
4. Redéployer le dossier.

C'est gratuit, et ça le reste à votre volume (deux personnes).

### c) Se relier
Créer le salon, choisir un code à 4 chiffres pour ouvrir l'app, puis
**envoyer le code du salon** (`nous-XXXX-XXXX-XXXX`) à la personne
concernée. Elle ouvre la même adresse, « Rejoindre le salon », colle le
code : vous êtes reliés.

Vous pouvez avoir **plusieurs salons** : « Nous deux », « Famille »,
« Maman ». Un code par salon.

---

## 3. Ce que ça fait

### 💬 Le fil
Messages, **vocaux**, **photos** (réduites automatiquement pour les
connexions comoriennes), et un bouton « Appelle-moi quand tu peux ».
Un appui sur un de vos messages pour l'effacer chez les deux.

### ⏳ Mon temps — le cœur du sujet
- **« Je suis occupé »** : une tape, et elle voit en haut de son écran
  « Nayam est pris jusqu'à 18 h ». Un mot part aussi dans le fil.
  Vous n'êtes plus quelqu'un qui ne répond pas : vous êtes quelqu'un
  d'occupé qui l'a dit.
- **Messages qui partiront plus tard** : écrivez cinq mots le dimanche
  soir, ils arrivent un par jour, à l'heure choisie. Elle ne voit rien
  avant — même en fouillant, la base ne les livre pas avant l'heure.
- **Mes rappels** : « 12 h 30 — écrire un mot à ma femme », « 21 h —
  bonne nuit ». Ça s'affiche quand l'application est ouverte, et en
  notification si vous les avez autorisées.

### ❤ Nous
- **L'idée du jour** : une activité à deux, différente chaque jour
  (60 idées : cinq minutes, une heure, une journée, à distance, des mots).
- **Proposer** : deux tapes, elle reçoit une carte « Oui, on le fait » /
  « Une autre fois ». Si elle dit oui, ça devient un **rendez-vous**.
- **Dates à ne jamais oublier** : anniversaires, mariage, votre
  rencontre — avec le nombre de jours qui restent.

### 👪 Famille
La liste des proches avec, pour chacun, **depuis combien de jours** ils
n'ont pas eu de vos nouvelles. Rouge = c'est trop long. Un bouton pour
appeler, un pour WhatsApp, un pour dire « c'est fait ». La pastille sur
l'onglet vous prévient sans vous harceler.

---

## 4. La confidentialité, concrètement

- Sans base configurée : **rien ne sort du téléphone**, point.
- Avec une base : tout est **chiffré sur le téléphone** avant d'être
  envoyé (AES-GCM 256). La clé est fabriquée à partir du code du salon,
  qui **ne quitte jamais l'appareil**.
- La base ne reçoit que : une empreinte du code (pour savoir dans quel
  salon ranger le message) et un bloc illisible. Même en l'ouvrant, on ne
  voit ni les mots, ni les photos, ni les prénoms.
- Les tables ne sont accessibles par aucune requête directe : uniquement
  par des fonctions qui exigent l'empreinte du salon.
- L'application se verrouille avec un code à 4 chiffres.

**⚠️ La contrepartie, et elle est réelle :** si vous perdez le code du
salon, personne ne peut retrouver la conversation. Gardez-le.

---

## 5. Ce que ça ne fait pas (à savoir)

- **Pas d'appels audio/vidéo en direct.** Il y a les vocaux et le bouton
  « Appelle-moi » ; pour la voix en direct, le téléphone ou WhatsApp.
- **Les notifications n'arrivent que si l'application a été ouverte** au
  moins une fois dans la journée. Une vraie notification « push » quand le
  téléphone dort demande un serveur d'envoi — à faire si vous le voulez.
- **Photos et vocaux limités** (photo réduite à 1280 px, vocal 2 minutes) :
  c'est volontaire, pour que ça passe sur le réseau d'ici.
- Un message effacé disparaît chez l'autre **à la synchronisation
  suivante** (moins d'une minute), pas à la seconde.
- La base dans le téléphone est liée **à ce navigateur** : si on vide les
  données du navigateur, l'historique local part. Le bouton « Sauvegarder
  la conversation » (Réglages) en sort une copie en texte.

---

## 6. Les fichiers

| Fichier | À quoi ça sert |
|---|---|
| `index.html` | L'application (écrans, structure) |
| `nous.css` | L'apparence |
| `nous.js` | Toute la logique : chiffrement, envoi, rattrapage, idées |
| `nous-config.js` | Vide par défaut. L'adresse de VOTRE base si vous en créez une |
| `SQL-nous.sql` | À coller dans votre projet Supabase à vous, une seule fois |
| `sw.js` | Fonctionnement hors ligne |
| `manifest.webmanifest`, `icon-*.png` | Installation sur l'écran d'accueil |

Aucune bibliothèque extérieure, aucun compte, aucun suivi.
