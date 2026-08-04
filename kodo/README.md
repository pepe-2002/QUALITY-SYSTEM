# KODO — l'école qui se joue

Un jeu de gestion où **apprendre est la seule façon de progresser**.

Tu diriges une startup tech depuis ta chambre. Un client propose un contrat ?
Il exige une compétence. Tu ne l'as pas → tu la passes : une leçon courte, des
exercices corrigés automatiquement, et la capacité est débloquée. Tu signes, tu
développes, tu livres, tu encaisses, tu achètes des serveurs, tu recrutes.

**La partie ne se termine jamais.** Une entreprise ne s'arrête pas à un
objectif : les contrats continuent d'arriver, de plus en plus gros, la
clientèle change d'échelle, l'équipe s'agrandit. Et si la caisse se vide, ce
n'est pas la fin — on se sépare de quelqu'un, on repart, on remonte.

Tout ce que tu apprends dans le jeu est vrai, utilisable dehors.

---

## Ouvrir le jeu

Rien à installer. Trois façons :

0. **En un seul fichier** — ouvrir `kodo-en-ligne.html` : tout est dedans,
   polices comprises. Pratique pour l'envoyer par WhatsApp ou le déposer
   sur n'importe quelle page. Régénéré par `python3 construire-page-unique.py`
   après chaque modification.
1. **En local** — depuis le dossier `kodo/` :
   ```
   python3 -m http.server 8080
   ```
   puis ouvrir `http://localhost:8080` dans le navigateur.
2. **En ligne** — déposer le dossier sur n'importe quel hébergement statique
   (Netlify, Cloudflare Pages, GitHub Pages). Il n'y a pas de serveur à gérer :
   c'est un site de fichiers.

Sur téléphone, « Ajouter à l'écran d'accueil » installe le jeu comme une
application. Il fonctionne ensuite **entièrement hors connexion** et la partie
est sauvegardée sur l'appareil.

---

## Le programme

4 branches, 6 niveaux chacune : **24 leçons, 74 exercices corrigés**.

| Niveau | Le code | Le web | Les serveurs | API & IA |
|---|---|---|---|---|
| 1 | Variables & fonctions | HTML / CSS | Client, serveur, DNS | Appeler une API |
| 2 | Décider (si/sinon) | Le JS dans la page | HTTP : verbes et codes | Modèles, tokens, coût |
| 3 | Listes & boucles | JSON & mémoire locale | Mise en ligne, HTTPS | Brancher une IA sans fuite de clé |
| 4 | Lire une erreur, déboguer | Rapide même en 3G | Bases de données (SQL) | L'IA sur tes propres données |
| 5 | Des tests qui te protègent | Formulaires & accessibilité | **Surveiller et maintenir** | Une IA en production sans se ruiner |
| 6 | Git & la dette technique | Ne jamais faire confiance au navigateur | Comptes, mots de passe, droits | Savoir si ton IA est bonne |

Les niveaux 1 à 3 apprennent à **construire**. Les niveaux 4 à 6 apprennent à
**garder en vie** : déboguer, tester, surveiller, sauvegarder, sécuriser,
maîtriser les coûts — c'est là que se joue la différence entre un projet
qui tient et un projet qu'on abandonne.

**On ne reste jamais bloqué.** Premier essai raté : l'indice s'ouvre tout seul.
Deuxième : le jeu propose de montrer la solution — la bonne réponse pour un QCM,
le bon ordre pour un enchaînement, et pour un exercice de code, la solution
écrite proprement, placée directement dans l'éditeur pour que tu puisses la
modifier et la relancer. La leçon se valide dans tous les cas ; le bilan indique
seulement ce que tu as réussi seul et ce que tu as fait avec la solution.

Trois types d'exercices, tous corrigés sur-le-champ avec une explication :

- **QCM** — on explique aussi pourquoi la mauvaise réponse est tentante ;
- **Code** — tu écris une vraie fonction, elle est **exécutée** contre une série
  de cas de test ; en cas d'échec on te montre l'entrée, le résultat attendu et
  ce que ton code a rendu ;
- **Remise en ordre** — pour les enchaînements où l'ordre est ce qui compte.

---

## Les règles du jeu

- **Énergie** : 5 actions par jour au début, **+1 à chaque palier franchi**
  (jusqu'à 10). Chaque leçon en coûte 1, chaque action aussi.
- **Développer** : avance les contrats. La vitesse dépend de tes niveaux en
  *code* et *web*, plus les développeurs de ton équipe.
- **Prospecter** : fait apparaître des offres. Une offre marquée en rouge exige
  une compétence que tu n'as pas encore.
- **Maintenance** : évite la panne du jour quand tes serveurs sont saturés.
- **Pub** : achète des clients ; le rendement dépend de ta réputation.
- **Fin de journée** : les clients paient, les serveurs et les salaires coûtent,
  et tes commerciaux ramènent des offres pendant que tu dors.

### L'équipe

| Métier | Ce qu'il apporte |
|---|---|
| **Développeur** | un point de développement de plus à chaque action |
| **Commercial** | ramène une offre par jour, sans dépenser ton énergie |
| **Technicien** | tient 500 clients de plus et réduit le risque de panne |

Chaque embauche coûte plus cher que la précédente, et tout le monde touche un
salaire quotidien : une équipe se nourrit de contrats.

### Les paliers

Chambre → Bureau → Agence → Studio → Groupe → Groupe régional → Multinationale
→ Licorne → Empire → Empire II, III… **et ça continue.** Passé le dernier palier
nommé, il faut 2,5 fois plus de clients pour monter d'un cran, sans limite.

Les contrats suivent : le catalogue écrit à la main sert de départ, puis le jeu
en fabrique à la taille de l'entreprise — missions plus lourdes, clientèle qui
passe du marché de Moroni aux groupes internationaux, montants à l'avenant.

---

## Ce qu'il y a dans le dossier

```
index.html          structure de l'application
kodo.css            design (sombre, mobile d'abord)
kodo.js             moteur de jeu, écrans, correcteur d'exercices
cours-bases.js      niveaux 1-4 : « Le code » et « Le web »
cours-tech.js       niveaux 1-4 : « Les serveurs » et « API & IA »
cours-avance.js     niveaux 5 et 6 des quatre branches
solutions.js        la solution de chaque exercice de code
construire-page-unique.py   assemble tout en un seul fichier HTML
kodo-en-ligne.html  le jeu en une seule page (produit par le script)
manifest.webmanifest, sw.js   installation + fonctionnement hors ligne
fonts.css, fonts/   polices embarquées (aucun appel extérieur)
icon-192.png, icon-512.png    icônes de l'application
```

Aucune dépendance, aucun compte, aucun serveur, aucune donnée qui sort de
l'appareil. La partie est dans le `localStorage` sous la clé `kodo_partie_v1`.

---

## Ajouter une leçon

Ouvrir `cours-bases.js` ou `cours-tech.js` (niveaux 1-4), ou `cours-avance.js`
(niveaux 5-6), et ajouter un objet dans le tableau `lecons` de la branche voulue :

```js
{
  id: 'code-4',                    // identifiant unique
  titre: 'Titre de la leçon',
  minutes: 5,
  but: "Ce que le joueur saura faire après.",
  contenu: [
    ['p', "Un paragraphe. Les balises <b>gras</b> et <code>code</code> marchent."],
    ['h', "Un sous-titre"],
    ['code', `du code affiché tel quel`],
    ['note', "Un encadré jaune pour un piège classique."]
  ],
  exos: [
    { type:'qcm',  q:"…", choix:['a','b'], bon:1, expl:"…" },
    { type:'code', q:"…", nom:'maFonction',
      depart:"function maFonction(x) {\n\n}",
      tests:[{args:[2], att:4}], indice:"…", expl:"…" },
    { type:'ordre', q:"…", items:["étape 1","étape 2"], expl:"…" }
  ]
}
```

Les leçons se débloquent dans l'ordre du tableau, et le niveau d'une branche
est simplement le nombre de leçons terminées — les contrats du catalogue
(`CONTRATS` dans `kodo.js`) s'ouvrent en conséquence.

---

*Fait pour Nayam (pepe-2002) — Comores, août 2026.*
