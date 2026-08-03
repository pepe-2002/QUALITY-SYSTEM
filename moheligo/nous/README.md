# ❤ « Nous » — votre messagerie privée

Une petite application à part, rien à voir avec le site public MoheliGo.
Elle vit dans `moheligo/nous/` et s'ouvre sur **https://moheligo.com/nous/**
(aucun lien depuis le site : personne ne tombe dessus par hasard, et les
moteurs de recherche ont l'interdiction de l'indexer).

Elle est faite pour un problème précis : **vous n'avez pas toujours le temps**.
Les gens qui comptent, eux, attendent quand même.

---

## 1. Mettre en route (une seule fois, 5 minutes)

1. **La base de données.** Ouvrir Supabase (le même projet que MoheliGo) →
   `SQL Editor` → coller tout le contenu de `SQL-nous.sql` → `Run`.
   Sans cette étape l'application fonctionne quand même, mais **seule sur
   votre téléphone** : rien n'est envoyé, l'autre personne ne voit rien.
2. **Déployer** comme d'habitude (le dossier part avec le reste du site).
3. **Ouvrir** https://moheligo.com/nous/ sur votre téléphone, puis
   « Ajouter à l'écran d'accueil » : ça devient une vraie application.
4. **Créer le salon**, choisir un code à 4 chiffres pour ouvrir l'app, puis
   **envoyer le code du salon** (`nous-XXXX-XXXX-XXXX`) à la personne
   concernée. Elle ouvre la même adresse, clique « Rejoindre le salon »,
   colle le code : vous êtes reliés.

Vous pouvez avoir **plusieurs salons** : « Nous deux », « Famille », « Maman ».
Un code par salon.

---

## 2. Ce que ça fait

### 💬 Le fil
Messages, **vocaux**, **photos** (réduites automatiquement pour les
connexions comoriennes), et un bouton « Appelle-moi quand tu peux ».
Appui long — en fait, un simple appui — sur un de vos messages pour
l'effacer chez les deux.

### ⏳ Mon temps — le cœur du sujet
- **« Je suis occupé »** : une tape, et elle voit en haut de son écran
  « Nayam est pris jusqu'à 18 h ». Un mot part aussi dans le fil.
  Vous n'êtes plus quelqu'un qui ne répond pas : vous êtes quelqu'un
  d'occupé qui l'a dit.
- **Messages qui partiront plus tard** : écrivez cinq mots le dimanche soir,
  ils arrivent un par jour, à l'heure choisie. Elle ne voit rien avant —
  même en fouillant, le serveur ne les livre pas avant l'heure.
- **Mes rappels** : « 12 h 30 — écrire un mot à ma femme », « 21 h — bonne
  nuit ». Ça s'affiche quand l'application est ouverte, et en notification
  si vous les avez autorisées.

### ❤ Nous
- **L'idée du jour** : une activité à deux, différente chaque jour
  (60 idées : cinq minutes, une heure, une journée, à distance, des mots).
- **Proposer** : deux tapes, elle reçoit une carte « Oui, on le fait » /
  « Une autre fois ». Si elle dit oui, ça devient un **rendez-vous**.
- **Dates à ne jamais oublier** : anniversaires, mariage, votre rencontre —
  avec le nombre de jours qui restent.

### 👪 Famille
La liste des proches avec, pour chacun, **depuis combien de jours** ils
n'ont pas eu de vos nouvelles. Rouge = c'est trop long. Un bouton pour
appeler, un pour WhatsApp, un pour dire « c'est fait ». La pastille sur
l'onglet vous prévient sans vous harceler.

---

## 3. La confidentialité, concrètement

- Tout est **chiffré sur le téléphone** avant d'être envoyé (AES-GCM 256).
  La clé est fabriquée à partir du code du salon, qui **ne quitte jamais
  l'appareil**.
- Le serveur ne reçoit que : une empreinte du code (pour savoir dans quel
  salon ranger le message) et un bloc illisible. Même en ouvrant la base
  Supabase, on ne voit ni les mots, ni les photos, ni les prénoms.
- Les tables ne sont accessibles par aucune requête directe : uniquement
  par des fonctions qui exigent l'empreinte du salon.
- L'application se verrouille avec un code à 4 chiffres.

**⚠️ La contrepartie, et elle est réelle :** si vous perdez le code du
salon, personne — ni moi, ni Supabase — ne peut retrouver la conversation.
Gardez-le quelque part.

---

## 4. Ce que ça ne fait pas (à savoir)

- **Pas d'appels audio/vidéo en direct.** Il y a les vocaux et le bouton
  « Appelle-moi » ; pour la voix en direct, le téléphone ou WhatsApp.
- **Les notifications n'arrivent que si l'application a été ouverte** au
  moins une fois dans la journée. Une vraie notification « push » quand le
  téléphone dort demande un serveur d'envoi — à faire si vous le voulez.
- **Les photos et vocaux sont limités** (photo réduite à 1280 px, vocal
  2 minutes) : c'est volontaire, pour que ça passe sur le réseau d'ici.
- Un message effacé disparaît chez l'autre **à la synchronisation
  suivante** (moins d'une minute), pas à la seconde.

---

## 5. Les fichiers

| Fichier | À quoi ça sert |
|---|---|
| `index.html` | L'application (écrans, structure) |
| `nous.css` | L'apparence |
| `nous.js` | Toute la logique : chiffrement, envoi, rattrapage, idées |
| `nous-config.js` | Adresse de la base + réglages (taille photo, cadence) |
| `SQL-nous.sql` | À coller dans Supabase, une seule fois |
| `sw.js` | Fonctionnement hors ligne |
| `manifest.webmanifest`, `icon-*.png` | Installation sur l'écran d'accueil |

Pour tester en local : `python3 -m http.server 8877` depuis `moheligo/`,
puis ouvrir `http://localhost:8877/nous/` (le chiffrement exige `https` ou
`localhost`).
