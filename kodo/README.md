# KODO — l'école qui se joue

Un jeu de gestion où **apprendre est la seule façon de progresser**.

Tu diriges une startup tech depuis ta chambre. Un client propose un contrat ?
Il exige une compétence. Tu ne l'as pas → tu la passes : une leçon courte, des
exercices corrigés automatiquement, et la capacité est débloquée. Tu signes, tu
développes, tu livres, tu encaisses, tu achètes des serveurs, tu embauches.
Objectif : 25 000 clients.

Tout ce que tu apprends dans le jeu est vrai, utilisable dehors.

---

## Ouvrir le jeu

Rien à installer. Deux façons :

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

4 branches, 16 leçons, 50 exercices corrigés.

| Branche | Leçons |
|---|---|
| **Le code** | Variables & fonctions · Décider (si/sinon) · Listes & boucles · Lire une erreur et déboguer |
| **Le web** | HTML/CSS · Le JS dans la page (DOM, événements) · JSON & mémoire locale · Rapide même en 3G |
| **Les serveurs** | Client/serveur, DNS, ports · HTTP, verbes & codes · Mise en ligne, HTTPS, sauvegardes · Bases de données (SQL, index, injection) |
| **API & IA** | Appeler une API (fetch, JSON) · Modèles, tokens, coût · Brancher une IA sans faire fuiter sa clé · Faire travailler l'IA sur tes données |

Trois types d'exercices, tous corrigés sur-le-champ avec une explication :

- **QCM** — on explique aussi pourquoi la mauvaise réponse est tentante ;
- **Code** — tu écris une vraie fonction, elle est **exécutée** contre une série
  de cas de test ; en cas d'échec on te montre l'entrée, le résultat attendu et
  ce que ton code a rendu ;
- **Remise en ordre** — pour les enchaînements où l'ordre est ce qui compte.

---

## Les règles du jeu

- **Énergie** : 5 actions par jour. Chaque leçon en coûte 1, chaque action aussi.
- **Développer** : avance les contrats. La vitesse dépend de tes niveaux en
  *code* et *web*, plus les développeurs embauchés.
- **Prospecter** : fait apparaître des offres. Une offre marquée en rouge exige
  une compétence que tu n'as pas encore.
- **Maintenance** : évite la panne du jour quand tes serveurs sont saturés.
- **Pub** : achète des clients ; le rendement dépend de ta réputation.
- **Fin de journée** : les clients paient, les serveurs et les salaires coûtent.
  Si la caisse passe sous zéro, la partie est perdue.

Paliers : Chambre → Bureau → Agence → Studio → **Groupe** (25 000 clients = victoire).

---

## Ce qu'il y a dans le dossier

```
index.html          structure de l'application
kodo.css            design (sombre, mobile d'abord)
kodo.js             moteur de jeu, écrans, correcteur d'exercices
cours-bases.js      branches « Le code » et « Le web »
cours-tech.js       branches « Les serveurs » et « API & IA »
manifest.webmanifest, sw.js   installation + fonctionnement hors ligne
fonts.css, fonts/   polices embarquées (aucun appel extérieur)
icon-192.png, icon-512.png    icônes de l'application
```

Aucune dépendance, aucun compte, aucun serveur, aucune donnée qui sort de
l'appareil. La partie est dans le `localStorage` sous la clé `kodo_partie_v1`.

---

## Ajouter une leçon

Ouvrir `cours-bases.js` ou `cours-tech.js` et ajouter un objet dans le tableau
`lecons` de la branche voulue :

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
