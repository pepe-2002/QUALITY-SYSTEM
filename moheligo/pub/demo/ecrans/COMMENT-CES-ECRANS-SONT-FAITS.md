# 📱 Les écrans de l'application — pris automatiquement, plus à la main

> 28/08/2026. Ce dossier a attendu des semaines des captures d'écran que le
> patron devait envoyer. **Il n'en a plus besoin :** l'application est dans le
> dépôt, on la fait tourner et on la photographie nous-mêmes.

## Comment refaire les captures

```
cd moheligo/pub/demo/ecrans
npm install --no-save playwright@1.56.1     # une fois
node capture.js
```

> 29/08/2026 — **le script est maintenant DANS le dépôt** (`capture.js`). Il n'a
> longtemps vécu que dans `/tmp` : la marche à suivre était écrite, l'outil avait
> disparu avec la session. Une procédure qu'on ne peut pas rejouer n'est pas une
> procédure, c'est un souvenir.

Il ouvre `moheligo/index.html` dans Chromium au format d'un téléphone
(440 × 892, densité 3 → 1320 px de large), passe l'écran d'accueil, coupe le
bandeau de rappels, masque les bulles flottantes, remplit la date, et
photographie.

⛔ **NE PAS essayer de photographier https://moheligo.com** : le navigateur de
ma session n'a aucun accès réseau (`ERR_CONNECTION_RESET`, revérifié le
28/08/2026). C'est le code local qu'on rend — c'est le même.

## Les pièges rencontrés, pour ne pas les repayer

| Ce qui abîmait la capture | Ce qu'on fait |
|---|---|
| Le bandeau « Reçois tes rappels » couvre le formulaire | on pose `mg_push_asked` dans le `localStorage` **avant** le chargement : il ne s'affiche jamais. Plus fiable que courir après sa croix |
| Les bulles flottantes (micro, chat) passent devant | on masque tout élément `position:fixed` de moins de 200 px de large |
| À 390 px, « MoheliGo » et « Commandants » sont tronqués (`Mohel…`) | viewport à **440 px** : plus rien n'est coupé |
| Le champ date affiche `mm/dd/yyyy`, ça fait inachevé | on lui donne une date **calculée** : aujourd'hui + 7 jours |
| Le premier écran est l'accueil (« Bienvenue »), pas la réservation | on clique « Passer » |
| 🚩 **La date sortait en `09/05/2026`** | voir ci-dessous — c'est le piège le plus coûteux du lot |

### 🚩 La date affichée à l'envers — le défaut qui ne se voit pas

La capture du 28/08 portait `09/05/2026` dans le champ Date. Lu par un client
comorien, ça veut dire **9 mai** : une réservation pour une date passée, donc un
service mort. En réalité c'était le **5 septembre**, écrit à l'américaine.

Le calendrier natif d'un `<input type=date>` suit **la langue de l'interface du
navigateur**, pas l'`Accept-Language` de la page. `locale: 'fr-FR'` sur le
contexte Playwright ne suffit pas — mesuré, la date restait en MM/JJ. Il faut
lancer le navigateur avec `--lang=fr-FR`.

**La leçon, plus large que ce script :** une capture d'écran fausse ne fait
lever aucune erreur. Le rendu réussit, le fichier fait le bon poids, le contrôle
automatique dit ✅. Il n'y a que l'œil pour l'attraper — donc **on regarde le
champ date après chaque capture**, avant de construire un visuel dessus.

## Ce qu'on a

| Fichier | Ce qu'on y voit |
|---|---|
| `accueil-reservation.png` | l'accueil complet : en-tête, « L'océan vous attend, embarquez en 2 minutes », les quatre raccourcis, la recherche, et le formulaire de réservation Chindini → Hoani avec sa date |

📌 **Ce fichier est la SEULE copie.** Les flyers 39 et 40 le pointent en
`../demo/ecrans/accueil-reservation.png`. Il en existait un double dans
`pub/flyers/ecran-appli.png` : supprimé le 29/08, parce qu'un double se corrige
d'un côté et pas de l'autre — c'est exactement comme ça qu'un visuel se retrouve
en retard sur sa source (déjà arrivé à quatre visuels le 29/08).

⚠️ **Aucune donnée personnelle** n'apparaît : l'application n'est pas connectée,
donc ni nom, ni numéro, ni référence de billet. C'est ce qui rend ces captures
publiables telles quelles, alors qu'une capture prise sur le téléphone du patron
demanderait un masquage.
