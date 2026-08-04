/* Kodo — programme : branches « Le code » et « Le web ».
   Chaque leçon = une explication courte + des exercices corrigés tout seuls. */
window.KODO_COURS = window.KODO_COURS || [];

window.KODO_COURS.push({
  id: 'code',
  nom: 'Le code',
  sigle: '{ }',
  couleur: '#F6BC1C',
  pitch: 'Donner des ordres à la machine.',
  lecons: [
    {
      id: 'code-1',
      titre: 'Ranger une valeur, fabriquer une machine',
      minutes: 5,
      but: 'Les variables et les fonctions : les deux briques de tout le reste.',
      contenu: [
        ['p', "Un programme, c'est une suite d'ordres écrits. La machine ne devine rien : elle exécute, ligne après ligne, exactement ce que tu écris."],
        ['h', "1. La variable : une étiquette sur une valeur"],
        ['p', "Une variable, c'est un nom que tu colles sur une valeur pour pouvoir la réutiliser. On écrit <code>const</code> quand la valeur ne changera plus, et <code>let</code> quand elle peut changer."],
        ['code', `const prix = 15000;        // un nombre
const port = "Ouroveni";   // du texte (entre guillemets)
let places = 12;           // pourra changer
places = places - 1;       // il en reste 11`],
        ['note', "Le point-virgule termine l'ordre. Ce qui suit <code>//</code> est un commentaire : la machine l'ignore, c'est pour toi."],
        ['h', "2. La fonction : une machine à réponses"],
        ['p', "Une fonction prend des choses en entrée, fait un travail, et rend un résultat avec <code>return</code>. Tu l'écris une fois, tu t'en sers mille fois."],
        ['code', `function total(prix, nombre) {
  return prix * nombre;
}

total(15000, 3);   // rend 45000`],
        ['p', "Entre les parenthèses, ce sont les <b>paramètres</b> : les cases d'entrée. <code>return</code> est la sortie. Sans <code>return</code>, la fonction ne rend rien du tout."],
        ['h', "3. Les opérations"],
        ['code', `2 + 3      // 5   addition
10 - 4     // 6   soustraction
5 * 4      // 20  multiplication
20 / 4     // 5   division
"Port " + port   // "Port Ouroveni"  (le + colle les textes)`],
        ['note', "Erreur classique du débutant : <code>\"2\" + 3</code> donne <code>\"23\"</code>, pas 5. Un chiffre entre guillemets est du texte, pas un nombre."]
      ],
      exos: [
        { type: 'qcm',
          q: "Que vaut <code>places</code> à la fin ?<pre>let places = 10;\nplaces = places - 3;\nplaces = places + 1;</pre>",
          choix: ['10', '8', '7', 'Erreur'],
          bon: 1,
          expl: "On lit ligne par ligne : 10, puis 10 − 3 = 7, puis 7 + 1 = 8. La dernière valeur écrite gagne." },
        { type: 'code',
          q: "Écris la fonction <code>total</code> : elle reçoit un prix et un nombre de billets, et rend le montant à payer.",
          nom: 'total',
          depart: `function total(prix, nombre) {
  // écris le return ici
}`,
          tests: [ {args:[15000,3], att:45000}, {args:[17500,2], att:35000}, {args:[15000,0], att:0} ],
          indice: "Il faut multiplier : <code>return prix * nombre;</code>",
          expl: "<code>return prix * nombre;</code> — la fonction rend le produit des deux entrées." },
        { type: 'code',
          q: "Écris la fonction <code>bienvenue</code> : elle reçoit un nom et rend le texte <code>Bonjour Amina</code> (avec le nom reçu).",
          nom: 'bienvenue',
          depart: `function bienvenue(nom) {

}`,
          tests: [ {args:['Amina'], att:'Bonjour Amina'}, {args:['Nayam'], att:'Bonjour Nayam'} ],
          indice: "Colle deux textes avec le <code>+</code>, sans oublier l'espace : <code>\"Bonjour \" + nom</code>",
          expl: "<code>return \"Bonjour \" + nom;</code> — attention à l'espace après « Bonjour »." }
      ]
    },
    {
      id: 'code-2',
      titre: 'Décider : si… sinon',
      minutes: 5,
      but: "Faire prendre des décisions au programme au lieu de tout faire à la main.",
      contenu: [
        ['p', "Un programme utile doit choisir : accepter ou refuser une réservation, appliquer une réduction, afficher une alerte. C'est le rôle de <code>if</code> (si) et <code>else</code> (sinon)."],
        ['code', `function peutEmbarquer(places) {
  if (places > 0) {
    return "Bienvenue à bord";
  } else {
    return "Vedette complète";
  }
}`],
        ['h', "Les comparaisons"],
        ['code', `a > b     // plus grand que
a < b     // plus petit que
a >= b    // plus grand ou égal
a === b   // exactement égal
a !== b   // différent de`],
        ['note', "Trois signes égal pour comparer (<code>===</code>), un seul pour ranger une valeur (<code>=</code>). Confondre les deux est l'erreur la plus fréquente au monde."],
        ['h', "Plusieurs cas à la suite"],
        ['code', `function tarif(age) {
  if (age < 3) {
    return 0;           // bébé : gratuit
  } else if (age < 12) {
    return 7500;        // enfant : moitié prix
  } else {
    return 15000;       // adulte
  }
}`],
        ['p', "La machine descend et s'arrête au <b>premier</b> <code>if</code> vrai. L'ordre compte donc énormément : du cas le plus précis au plus général."],
        ['h', "Et / ou"],
        ['code', `if (places > 0 && meteo === "bonne") { }   // && = ET (les deux)
if (jour === "samedi" || jour === "dimanche") { }  // || = OU (au moins un)`]
      ],
      exos: [
        { type: 'qcm',
          q: "Avec la fonction <code>tarif</code> ci-dessus, que rend <code>tarif(2)</code> ?",
          choix: ['0', '7500', '15000', 'Rien'],
          bon: 0,
          expl: "2 est plus petit que 3 : le premier <code>if</code> est vrai, la fonction rend 0 et s'arrête là." },
        { type: 'code',
          q: "Écris <code>statut</code> : elle reçoit le nombre de places restantes et rend <code>\"complet\"</code> s'il n'en reste aucune, <code>\"presque complet\"</code> s'il en reste moins de 5, sinon <code>\"disponible\"</code>.",
          nom: 'statut',
          depart: `function statut(places) {

}`,
          tests: [ {args:[0], att:'complet'}, {args:[3], att:'presque complet'}, {args:[4], att:'presque complet'}, {args:[5], att:'disponible'}, {args:[20], att:'disponible'} ],
          indice: "Commence par le cas le plus précis : <code>if (places === 0)</code>, puis <code>else if (places < 5)</code>, puis <code>else</code>.",
          expl: "L'ordre est la clé : 0 doit être testé avant « moins de 5 », sinon 0 tomberait dans « presque complet »." },
        { type: 'ordre',
          q: "Remets les tests dans le bon ordre pour une fonction qui donne le tarif selon l'âge.",
          items: [ "if (age < 3) return 0;", "else if (age < 12) return 7500;", "else return 15000;" ],
          expl: "Du plus précis au plus général. Si tu testes <code>age &lt; 12</code> en premier, un bébé de 2 ans paierait 7500." }
      ]
    },
    {
      id: 'code-3',
      titre: 'Répéter : listes et boucles',
      minutes: 6,
      but: "Traiter 10 000 lignes avec le même effort que 3.",
      contenu: [
        ['p', "Un <b>tableau</b> est une liste ordonnée de valeurs. On l'écrit entre crochets, et on compte les places à partir de <b>zéro</b>."],
        ['code', `const ports = ["Ouroveni", "Chindini", "Hoani", "Fomboni"];

ports[0];        // "Ouroveni"  (le premier !)
ports[2];        // "Hoani"
ports.length;    // 4  (combien d'éléments)`],
        ['h', "La boucle : refaire la même chose"],
        ['code', `const prix = [15000, 17500, 15000];
let somme = 0;

for (let i = 0; i < prix.length; i = i + 1) {
  somme = somme + prix[i];
}
// somme vaut 47500`],
        ['p', "Le <code>for</code> se lit en trois temps : je pars de <code>i = 0</code> ; je continue tant que <code>i</code> est plus petit que la longueur ; à chaque tour j'ajoute 1 à <code>i</code>."],
        ['note', "Puisqu'on compte à partir de 0, le dernier élément est à la place <code>length - 1</code>. Écrire <code>i &lt;= prix.length</code> fait sortir du tableau : bug garanti."],
        ['h', "Les raccourcis qui font gagner du temps"],
        ['code', `const t = [5, 12, 8];

t.filter(n => n > 6);      // [12, 8]   garder ce qui passe le test
t.map(n => n * 2);         // [10,24,16] transformer chacun
t.find(n => n > 6);        // 12        le premier qui passe
t.includes(8);             // true      est-ce dedans ?
t.push(3);                 // ajoute 3 à la fin`],
        ['p', "<code>n => n > 6</code> est une mini-fonction : « donne-moi un <code>n</code>, je te dis s'il est plus grand que 6 ». C'est la même chose qu'un <code>function</code>, en plus court."]
      ],
      exos: [
        { type: 'qcm',
          q: "Avec <code>const ports = [\"Ouroveni\", \"Chindini\", \"Hoani\"];</code>, que vaut <code>ports[1]</code> ?",
          choix: ['"Ouroveni"', '"Chindini"', '"Hoani"', 'undefined'],
          bon: 1,
          expl: "On compte à partir de 0 : place 0 = Ouroveni, place 1 = Chindini." },
        { type: 'code',
          q: "Écris <code>recette</code> : elle reçoit un tableau de prix et rend la somme totale.",
          nom: 'recette',
          depart: `function recette(prix) {
  let somme = 0;
  // parcours le tableau
  return somme;
}`,
          tests: [ {args:[[15000,17500,15000]], att:47500}, {args:[[]], att:0}, {args:[[100]], att:100} ],
          indice: "<code>for (let i = 0; i &lt; prix.length; i++) { somme = somme + prix[i]; }</code>",
          expl: "On part de 0 et on ajoute chaque case. Un tableau vide rend bien 0, sans cas particulier à écrire." },
        { type: 'code',
          q: "Écris <code>disponibles</code> : elle reçoit un tableau de nombres de places et rend seulement celles qui sont au-dessus de 0.",
          nom: 'disponibles',
          depart: `function disponibles(places) {

}`,
          tests: [ {args:[[3,0,12,0,5]], att:[3,12,5]}, {args:[[0,0]], att:[]} ],
          indice: "Une seule ligne suffit : <code>return places.filter(n => n > 0);</code>",
          expl: "<code>filter</code> garde les éléments qui passent le test et rend un nouveau tableau." }
      ]
    }
  ]
});

window.KODO_COURS.push({
  id: 'web',
  nom: 'Le web',
  sigle: '</>',
  couleur: '#2E9BD6',
  pitch: 'Fabriquer une page que le monde entier peut ouvrir.',
  lecons: [
    {
      id: 'web-1',
      titre: 'La page : structure et habillage',
      minutes: 5,
      but: "Comprendre le duo HTML / CSS, la base de tout site.",
      contenu: [
        ['p', "Un site web tient en deux langages complémentaires. <b>HTML</b> dit ce qu'il y a (un titre, un bouton, une image). <b>CSS</b> dit à quoi ça ressemble (couleur, taille, position). Le squelette et les habits."],
        ['h', "HTML : des balises qui s'ouvrent et se ferment"],
        ['code', `&lt;h1&gt;MoheliGo&lt;/h1&gt;
&lt;p&gt;Réservez votre traversée.&lt;/p&gt;
&lt;button id="reserver"&gt;Réserver&lt;/button&gt;
&lt;img src="vedette.jpg" alt="Une vedette"&gt;`],
        ['p', "<code>&lt;h1&gt;</code> ouvre, <code>&lt;/h1&gt;</code> ferme. Ce qu'il y a entre les deux, c'est le contenu. Une balise peut porter des attributs : <code>id</code> (son nom unique), <code>class</code> (sa catégorie), <code>src</code> (le fichier à charger)."],
        ['h', "CSS : viser un élément, lui donner un style"],
        ['code', `h1 { color: #0F2A5C; font-size: 32px; }   /* toutes les balises h1 */
#reserver { background: #F6BC1C; }        /* l'élément dont l'id = reserver */
.carte { border-radius: 16px; padding: 20px; }  /* tous ceux de classe carte */`],
        ['note', "Le dièse <code>#</code> vise un <code>id</code> (unique dans la page). Le point <code>.</code> vise une <code>class</code> (autant d'éléments que tu veux). C'est la distinction que tout le monde confond au début."],
        ['h', "La page minimale complète"],
        ['code', `&lt;!doctype html&gt;
&lt;html lang="fr"&gt;
&lt;head&gt;
  &lt;meta charset="utf-8"&gt;
  &lt;title&gt;Mon site&lt;/title&gt;
  &lt;link rel="stylesheet" href="style.css"&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Bonjour&lt;/h1&gt;
  &lt;script src="app.js"&gt;&lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;`],
        ['p', "<code>head</code> = les informations pour le navigateur (titre, encodage, feuille de style). <code>body</code> = ce que le visiteur voit. Le <code>script</code> se met en bas, pour que le JavaScript trouve la page déjà construite."]
      ],
      exos: [
        { type: 'qcm',
          q: "En CSS, comment vise-t-on <code>&lt;button class=\"cta\"&gt;</code> ?",
          choix: ['#cta { }', '.cta { }', 'cta { }', 'button#cta { }'],
          bon: 1,
          expl: "Une <code>class</code> se vise avec un point. Le dièse est réservé aux <code>id</code>." },
        { type: 'qcm',
          q: "Où placer le contenu que le visiteur doit voir ?",
          choix: ['Dans le head', 'Dans le body', 'Dans le title', "N'importe où"],
          bon: 1,
          expl: "<code>head</code> contient les réglages invisibles, <code>body</code> le contenu visible." },
        { type: 'ordre',
          q: "Remets une page HTML dans l'ordre.",
          items: [ "&lt;!doctype html&gt;", "&lt;head&gt; … titre et style …&lt;/head&gt;", "&lt;body&gt; … le contenu visible …&lt;/body&gt;", "&lt;/html&gt;" ],
          expl: "Le doctype annonce le type de document, puis head (réglages), puis body (contenu), et on referme." }
      ]
    },
    {
      id: 'web-2',
      titre: 'Rendre la page vivante',
      minutes: 6,
      but: "Réagir au clic et modifier la page : c'est là que ça devient une application.",
      contenu: [
        ['p', "Le JavaScript s'exécute dans le navigateur du visiteur. Il peut lire la page, la modifier, réagir aux clics. La page vue par le navigateur s'appelle le <b>DOM</b>."],
        ['h', "1. Attraper un élément"],
        ['code', `const bouton = document.querySelector("#reserver");
const titre  = document.querySelector("h1");
const cartes = document.querySelectorAll(".carte");  // tous`],
        ['h', "2. Le modifier"],
        ['code', `titre.textContent = "Places limitées";   // changer le texte
bouton.disabled = true;                  // griser le bouton
bouton.classList.add("complet");         // lui coller une classe CSS`],
        ['note', "Utilise <code>textContent</code> pour du texte. <code>innerHTML</code> injecte du HTML : pratique, mais dangereux si le texte vient d'un visiteur — c'est la porte d'entrée classique des attaques."],
        ['h', "3. Réagir à un clic"],
        ['code', `bouton.addEventListener("click", function () {
  places = places - 1;
  titre.textContent = "Il reste " + places + " places";
});`],
        ['p', "On dit : « quand cet élément reçoit un clic, exécute cette fonction ». La fonction ne part pas tout de suite : elle attend l'événement. C'est ça, programmer une interface."],
        ['h', "Les événements utiles"],
        ['code', `"click"   // clic ou tape sur le téléphone
"input"   // à chaque frappe dans un champ
"change"  // quand un choix est validé
"submit"  // envoi d'un formulaire`]
      ],
      exos: [
        { type: 'qcm',
          q: "Quelle ligne attrape l'élément <code>&lt;div id=\"prix\"&gt;</code> ?",
          choix: ['document.querySelector(".prix")', 'document.querySelector("#prix")', 'document.get("prix")', 'document.prix'],
          bon: 1,
          expl: "Même syntaxe qu'en CSS : dièse pour un id, point pour une classe." },
        { type: 'qcm',
          q: "Le texte vient d'un visiteur. Que vaut-il mieux utiliser ?",
          choix: ['innerHTML, plus puissant', 'textContent, plus sûr', "Aucun des deux", "Peu importe"],
          bon: 1,
          expl: "<code>textContent</code> affiche le texte tel quel. <code>innerHTML</code> exécuterait du HTML — et donc du code — envoyé par un inconnu." },
        { type: 'ordre',
          q: "Remets dans l'ordre les étapes pour qu'un clic change un titre.",
          items: [ "Attraper le bouton avec querySelector", "Appeler addEventListener sur ce bouton", "Dans la fonction, modifier titre.textContent", "L'utilisateur clique : la fonction s'exécute" ],
          expl: "On attrape, on met l'écouteur en place, et ensuite seulement le clic déclenche le travail." }
      ]
    },
    {
      id: 'web-3',
      titre: 'Garder les données : JSON et mémoire locale',
      minutes: 5,
      but: "Ne plus tout perdre quand la page se recharge.",
      contenu: [
        ['p', "Une variable disparaît dès que la page se ferme. Pour garder une information, il faut l'écrire quelque part. Le plus simple : la mémoire du navigateur, le <b>localStorage</b>."],
        ['h', "L'objet : plusieurs informations en un seul paquet"],
        ['code', `const billet = {
  nom: "Amina",
  port: "Ouroveni",
  places: 2,
  prix: 15000
};

billet.nom;        // "Amina"
billet.prix * billet.places;   // 30000`],
        ['h', "JSON : l'objet transformé en texte"],
        ['code', `const texte = JSON.stringify(billet);   // objet  → texte
const objet = JSON.parse(texte);        // texte  → objet`],
        ['p', "Le localStorage ne sait ranger que du <b>texte</b>. C'est pour ça qu'on passe toujours par JSON, dans un sens puis dans l'autre. C'est aussi le format qu'utilisent les serveurs pour se parler — tu le retrouveras partout."],
        ['h', "Écrire et relire"],
        ['code', `localStorage.setItem("billet", JSON.stringify(billet));

const brut = localStorage.getItem("billet");
const relu = brut ? JSON.parse(brut) : null;   // attention au vide !`],
        ['note', "La première fois, il n'y a rien : <code>getItem</code> rend <code>null</code>, et <code>JSON.parse(null)</code> plante. Toujours vérifier avant de relire — c'est la moitié des bugs de démarrage d'une application."],
        ['h', "Ce que le localStorage n'est pas"],
        ['p', "Il est propre à <b>un</b> téléphone et à <b>un</b> navigateur. Rien n'est partagé entre deux appareils, et l'utilisateur peut tout effacer. Pour des données partagées ou sérieuses, il faut un serveur — c'est la branche suivante."]
      ],
      exos: [
        { type: 'qcm',
          q: "Que rend <code>JSON.stringify({a: 1})</code> ?",
          choix: ['un objet', 'le texte {"a":1}', 'le nombre 1', 'une erreur'],
          bon: 1,
          expl: "<code>stringify</code> fabrique du texte. <code>parse</code> fait le chemin inverse." },
        { type: 'code',
          q: "Écris <code>montant</code> : elle reçoit un billet (un objet avec <code>prix</code> et <code>places</code>) et rend le total à payer.",
          nom: 'montant',
          depart: `function montant(billet) {

}`,
          tests: [ {args:[{prix:15000, places:2}], att:30000}, {args:[{prix:17500, places:1}], att:17500} ],
          indice: "On lit une propriété avec un point : <code>billet.prix</code>.",
          expl: "<code>return billet.prix * billet.places;</code> — on accède aux champs de l'objet avec le point." },
        { type: 'qcm',
          q: "Ton client change de téléphone. Que devient ce qui était dans le localStorage ?",
          choix: ['Ça le suit', 'Ça reste sur l’ancien téléphone', 'Ça part sur le serveur', 'Ça se synchronise'],
          bon: 1,
          expl: "Le localStorage est local, point. Pour suivre l'utilisateur partout, il faut un compte et un serveur." }
      ]
    }
  ]
});
