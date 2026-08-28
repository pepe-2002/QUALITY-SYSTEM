# 📱 Les écrans de l'application — pris automatiquement, plus à la main

> 28/08/2026. Ce dossier a attendu des semaines des captures d'écran que le
> patron devait envoyer. **Il n'en a plus besoin :** l'application est dans le
> dépôt, on la fait tourner et on la photographie nous-mêmes.

## Comment refaire les captures

```
cd /tmp && npm install --no-save playwright@1.56.1
node /tmp/ecran.js          # ou le script ci-dessous
```

Le script ouvre `moheligo/index.html` dans Chromium au format d'un téléphone
(412 × 892, densité 3 → 1320 × 2700 pixels réels), passe l'écran d'accueil,
ferme les bandeaux, masque les bulles flottantes, remplit la date, et
photographie.

⛔ **NE PAS essayer de photographier https://moheligo.com** : le navigateur de
ma session n'a aucun accès réseau (`ERR_CONNECTION_RESET`, revérifié le
28/08/2026). C'est le code local qu'on rend — c'est le même.

## Les pièges rencontrés, pour ne pas les repayer

| Ce qui abîmait la capture | Ce qu'on fait |
|---|---|
| Le bandeau « Reçois tes rappels » couvre le formulaire | on clique sa croix avant de photographier |
| Les bulles flottantes (micro, chat) passent devant | on masque tout élément `position:fixed` étroit et bas |
| À 390 px, « MoheliGo » et « Commandants » sont tronqués (`Mohel…`) | viewport à **440 px** : plus rien n'est coupé |
| Le champ date affiche `mm/dd/yyyy`, ça fait inachevé | on lui donne une vraie date avant la photo |
| Le premier écran est l'accueil (« Bienvenue »), pas la réservation | on clique « Passer » |

## Ce qu'on a

| Fichier | Ce qu'on y voit |
|---|---|
| `accueil-reservation.png` | l'accueil complet : en-tête, « L'océan vous attend, embarquez en 2 minutes », les quatre raccourcis, la recherche, et le formulaire de réservation Chindini → Hoani avec sa date |

⚠️ **Aucune donnée personnelle** n'apparaît : l'application n'est pas connectée,
donc ni nom, ni numéro, ni référence de billet. C'est ce qui rend ces captures
publiables telles quelles, alors qu'une capture prise sur le téléphone du patron
demanderait un masquage.
