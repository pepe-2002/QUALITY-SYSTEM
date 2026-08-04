/* ═══════════════════════════════════════════════════════════════════
   Kodo — niveaux 5 et 6 des quatre branches.
   Ce fichier ne crée pas de branche : il complète celles qui existent.
   ═══════════════════════════════════════════════════════════════════ */
(function () {
  const ajouter = (idBranche, lecons) => {
    const b = (window.KODO_COURS || []).find(x => x.id === idBranche);
    if (b) b.lecons.push.apply(b.lecons, lecons);
  };

/* ─────────────────────────── LE CODE ─────────────────────────── */
ajouter('code', [
  {
    id: 'code-5',
    titre: "Des tests qui te protègent",
    minutes: 7,
    but: "Corriger sans casser autre chose, et le savoir en une seconde.",
    contenu: [
      ['p', "Au début, tu vérifies à la main : tu ouvres l'application, tu cliques, tu regardes. À dix fonctions ça va. À cent, tu ne peux plus tout revérifier après chaque changement — alors tu ne vérifies plus rien, et tu casses en silence des choses qui marchaient."],
      ['h', "Un test, c'est une phrase"],
      ['code', `« Avec cette entrée connue, j'attends cette sortie. »

  total(15000, 3)   doit rendre   45000
  moyenne([])       doit rendre   0
  statut(0)         doit rendre   "complet"`],
      ['p', "Rien de plus. Un test n'est pas un outil compliqué : c'est un appel de ta fonction avec une réponse écrite d'avance. Ce qui change tout, c'est qu'une machine peut les rejouer tous en une seconde, à chaque modification."],
      ['h', "Écrire son premier test à la main"],
      ['code', `function verifier(nom, obtenu, attendu) {
  if (JSON.stringify(obtenu) === JSON.stringify(attendu)) {
    console.log("OK   " + nom);
  } else {
    console.log("RATÉ " + nom + " : attendu " + attendu +
                ", obtenu " + obtenu);
  }
}

verifier("total simple", total(15000, 3), 45000);
verifier("total à zéro", total(15000, 0), 0);`],
      ['note', "Tu viens d'écrire un mini-outil de test en six lignes. Les vrais outils (Jest, Vitest…) font la même chose en plus confortable — mais le principe est exactement celui-là. Ne les attends pas pour commencer."],
      ['h', "Que faut-il tester ? Trois cas, toujours"],
      ['code', `1. Le cas normal     total(15000, 3)
2. Le cas limite     total(15000, 0), moyenne([])
3. Le cas d'erreur   que se passe-t-il si on
                     envoie du texte, ou rien ?`],
      ['p', "Le cas normal est celui auquel tu penses tout seul, et c'est presque jamais celui qui casse. Les bugs vivent dans les deux autres."],
      ['h', "Le test de non-régression : le plus rentable de tous"],
      ['p', "Un client signale un bug. Avant de le corriger, écris un test qui <b>échoue</b> à cause de ce bug. Corrige ensuite : le test passe. Ce test reste dans ton projet pour toujours, et ce bug précis ne pourra plus jamais revenir sans que tu le saches."],
      ['code', `Bug signalé  →  test qui échoue  →  correction
             →  test qui passe  →  test gardé`],
      ['h', "Ce que les tests t'apportent vraiment"],
      ['p', "Le confort de <b>changer</b>. Sans tests, tu n'oses plus toucher au code qui marche, et le projet se fige. Avec des tests, tu peux réorganiser, simplifier, améliorer — et savoir en une seconde si tu as cassé quelque chose. C'est ce qui sépare un projet vivant d'un projet qu'on n'ose plus ouvrir."]
    ],
    exos: [
      { type: 'qcm',
        q: "Un client signale un bug. Quel est le premier bon réflexe ?",
        choix: ["Corriger tout de suite", "Écrire un test qui reproduit le bug, puis corriger", "Réécrire la fonction en entier", "Ajouter un try/catch autour"],
        bon: 1,
        expl: "Le test prouve que tu as bien compris le bug, puis prouve que ta correction marche, et empêche définitivement son retour." },
      { type: 'code',
        q: "Écris <code>reussis</code> : elle reçoit une liste de cas de test (objets avec <code>obtenu</code> et <code>attendu</code>) et rend le nombre de cas où les deux sont égaux.",
        nom: 'reussis',
        depart: `function reussis(cas) {

}`,
        tests: [
          {args:[[{obtenu:45000,attendu:45000},{obtenu:0,attendu:1}]], att:1},
          {args:[[{obtenu:'a',attendu:'a'},{obtenu:'b',attendu:'b'}]], att:2},
          {args:[[]], att:0}
        ],
        indice: "Un <code>filter</code> puis <code>.length</code> : <code>return cas.filter(c => c.obtenu === c.attendu).length;</code>",
        expl: "C'est le cœur de n'importe quel outil de test : comparer l'obtenu à l'attendu, et compter." },
      { type: 'ordre',
        q: "Remets le cycle « un bug est signalé » dans l'ordre.",
        items: [ "Reproduire le bug une fois à la main", "Écrire un test qui échoue à cause de lui", "Corriger le code", "Vérifier que le test passe maintenant", "Garder ce test pour toujours" ],
        expl: "Reproduire d'abord : si tu ne sais pas reproduire, tu ne sauras pas non plus si tu as corrigé." }
    ]
  },
  {
    id: 'code-6',
    titre: "Git : ne plus jamais perdre son travail",
    minutes: 7,
    but: "Garder l'histoire de ton projet, revenir en arrière, et travailler à plusieurs sans se marcher dessus.",
    contenu: [
      ['p', "Tu as un dossier <code>projet-final</code>, un <code>projet-final-2</code>, un <code>projet-final-vrai</code>, et tu ne sais plus lequel marche. <b>Git</b> règle ça définitivement : un seul dossier, et toute l'histoire des modifications dedans."],
      ['h', "Le commit : une photo du projet"],
      ['code', `git add .
git commit -m "Correction du tarif enfant"`],
      ['p', "Un <b>commit</b> enregistre l'état complet du projet à cet instant, avec un message qui dit pourquoi. Tu peux revenir à n'importe quelle photo, comparer deux moments, retrouver le jour où un bug est apparu. Rien n'est jamais perdu."],
      ['h', "Écrire un message utile"],
      ['code', `✗ « modif », « fix », « ça marche », « aaa »
✓ « Correction du tarif enfant : la moitié de prix
    ne s'appliquait pas entre 3 et 12 ans »`],
      ['note', "Le message s'écrit pour toi, dans six mois, quand tu chercheras ce qui a cassé. Dis <b>pourquoi</b>, pas <b>quoi</b> : le « quoi » est déjà visible dans le code, le « pourquoi » n'existe nulle part ailleurs."],
      ['h', "La branche : essayer sans risque"],
      ['code', `git switch -c tarifs-2027   # nouvelle branche
… tu travailles, tu commits …
git switch main             # retour à la version qui marche`],
      ['p', "Une <b>branche</b> est une ligne parallèle. Tu tentes une refonte, une idée risquée, une grosse fonctionnalité — pendant ce temps la version en production reste intacte sur <code>main</code>. Si l'idée est mauvaise, tu abandonnes la branche et il ne s'est rien passé. Si elle est bonne, tu la fusionnes."],
      ['h', "Le conflit : deux personnes, la même ligne"],
      ['p', "Quand deux personnes modifient la même ligne du même fichier, Git ne choisit pas à ta place : il te montre les deux versions et te demande de trancher. Ce n'est pas une panne, c'est une question. Tu gardes l'une, l'autre, ou tu écris la bonne fusion des deux."],
      ['h', "Pousser : la sauvegarde qui vit ailleurs"],
      ['code', `git push`],
      ['p', "Ton dépôt local est sur ton ordinateur ; <code>push</code> l'envoie sur un serveur (GitHub). À partir de là, ton disque peut brûler : tout est ailleurs, avec l'historique complet. C'est ta sauvegarde <b>et</b> ta machine à remonter le temps, dans la même commande."],
      ['h', "La dette technique"],
      ['p', "Chaque raccourci pris pour livrer plus vite est un emprunt : tu le rembourseras avec des intérêts, sous forme de temps perdu à chaque modification suivante. Emprunter est parfois la bonne décision — mais note-le, et rembourse avant que le projet devienne impossible à faire évoluer."]
    ],
    exos: [
      { type: 'qcm',
        q: "À quoi sert une branche ?",
        choix: ["À sauvegarder plus souvent", "À travailler sur une idée sans toucher à la version qui marche", "À accélérer le code", "À partager son mot de passe"],
        bon: 1,
        expl: "La branche isole ton chantier. <code>main</code> reste la version fiable, tant que tu n'as pas décidé de fusionner." },
      { type: 'qcm',
        q: "Git te signale un conflit. Que s'est-il passé ?",
        choix: ["Le dépôt est corrompu", "Deux modifications touchent la même ligne, Git te demande de trancher", "Tu n'as pas le droit de pousser", "Le réseau a coupé"],
        bon: 1,
        expl: "Un conflit n'est pas une erreur : c'est une décision que seule une personne peut prendre. Git refuse de deviner à ta place." },
      { type: 'ordre',
        q: "Remets une journée de travail avec Git dans l'ordre.",
        items: [ "Créer une branche pour la nouvelle fonctionnalité", "Modifier le code et vérifier que ça marche", "Enregistrer un commit avec un message clair", "Fusionner la branche dans main", "Pousser sur le serveur" ],
        expl: "On ne fusionne dans <code>main</code> que ce qu'on a vérifié — et on pousse pour que le travail survive à la machine." }
    ]
  }
]);

/* ─────────────────────────── LE WEB ─────────────────────────── */
ajouter('web', [
  {
    id: 'web-5',
    titre: "Formulaires : saisir sans se tromper",
    minutes: 6,
    but: "Récupérer des informations justes, et guider celui qui se trompe.",
    contenu: [
      ['p', "Le formulaire est l'endroit où ton visiteur devient client. C'est aussi l'endroit où il abandonne. Chaque champ inutile, chaque message d'erreur obscur coûte des réservations."],
      ['h', "Le bon type de champ fait la moitié du travail"],
      ['code', `&lt;label for="tel"&gt;Téléphone&lt;/label&gt;
&lt;input id="tel" type="tel" inputmode="numeric"
       autocomplete="tel" required&gt;`],
      ['p', "Sur un téléphone, <code>type=\"tel\"</code> ouvre le clavier numérique, <code>type=\"email\"</code> ajoute l'arobase, <code>type=\"date\"</code> affiche un calendrier. C'est gratuit, et ça évite la moitié des fautes de saisie."],
      ['note', "Le <code>&lt;label&gt;</code> relié par <code>for</code> n'est pas décoratif : il agrandit la zone cliquable, et c'est lui que lit un lecteur d'écran. Un champ sans label est inutilisable pour une personne aveugle."],
      ['h', "Valider deux fois, toujours"],
      ['code', `Dans le navigateur  →  pour AIDER l'utilisateur
                       (message immédiat, poli)

Sur le serveur      →  pour PROTÉGER tes données
                       (obligatoire, non contournable)`],
      ['p', "La validation du navigateur se contourne en dix secondes. Elle sert au confort, jamais à la sécurité. Toute donnée doit être revérifiée à l'arrivée, côté serveur — c'est la seule vérification qui compte."],
      ['h', "Des messages d'erreur qui servent"],
      ['code', `✗ « Erreur »
✗ « Champ invalide »
✗ « Format incorrect (code E-42) »
✓ « Le numéro doit commencer par +269 et
    contenir 7 chiffres. Exemple : +269 321 45 67 »`],
      ['p', "Un bon message dit <b>ce qui ne va pas</b> et <b>comment le réparer</b>, à côté du champ concerné, sans effacer ce que la personne avait déjà tapé. Effacer le formulaire après une erreur est la meilleure façon de perdre un client définitivement."],
      ['h', "Utilisable par tout le monde"],
      ['code', `• Zones tactiles d'au moins 44 pixels de côté
• Contraste suffisant entre le texte et le fond
• Naviguer au clavier : l'ordre doit être logique
  et l'élément actif toujours visible
• Ne jamais coder une information par la seule
  couleur (le rouge seul ne dit rien à un daltonien)`],
      ['p', "Ce ne sont pas des faveurs faites à une minorité : un contraste correct sert aussi celui qui regarde son écran en plein soleil, et une grande zone tactile sert tous ceux qui ont les mains prises."]
    ],
    exos: [
      { type: 'qcm',
        q: "Tu as mis <code>required</code> sur tes champs. Peux-tu te passer de vérifier côté serveur ?",
        choix: ["Oui, le navigateur bloque l'envoi", "Non : la validation du navigateur se contourne en dix secondes", "Oui si le site est en https", "Seulement pour les champs texte"],
        bon: 1,
        expl: "N'importe qui peut envoyer une requête sans passer par ton formulaire. Le navigateur aide l'utilisateur ; seul le serveur protège." },
      { type: 'code',
        q: "Écris <code>nettoyerTel</code> : elle reçoit un numéro saisi n'importe comment et rend uniquement ses chiffres (espaces, tirets et points enlevés).",
        nom: 'nettoyerTel',
        depart: `function nettoyerTel(saisi) {

}`,
        tests: [
          {args:['+269 321 45 67'], att:'2693214567'},
          {args:['321-45-67'], att:'3214567'},
          {args:['321.45.67'], att:'3214567'},
          {args:[''], att:''}
        ],
        indice: "Une expression régulière suffit : <code>return saisi.replace(/[^0-9]/g, '');</code>",
        expl: "On nettoie la saisie AVANT de la ranger : une base où le même numéro existe sous quatre formes est une base inutilisable." },
      { type: 'ordre',
        q: "Remets dans l'ordre le traitement d'un formulaire envoyé.",
        items: [ "Le navigateur vérifie les champs et aide l'utilisateur", "Les données partent vers le serveur", "Le serveur revérifie tout, sans rien croire", "Les données nettoyées sont enregistrées", "Une confirmation claire s'affiche" ],
        expl: "La revérification serveur est l'étape qu'on saute quand on est pressé — et c'est celle par laquelle les ennuis arrivent." }
    ]
  },
  {
    id: 'web-6',
    titre: "Ne jamais faire confiance au navigateur",
    minutes: 7,
    but: "Fermer les portes que tout site débutant laisse ouvertes.",
    contenu: [
      ['p', "Tout ce qui tourne dans le navigateur du visiteur appartient au visiteur. Il peut lire ton code, modifier tes variables, changer ce que ton formulaire envoie. Ce n'est pas du piratage avancé : c'est un clic droit et deux minutes."],
      ['h', "Faille 1 — le prix calculé côté client"],
      ['code', `❌ La page calcule le total et l'envoie au serveur
   { article: "billet", total: 15000 }
   → le visiteur remplace 15000 par 100. Tu encaisses 100.

✅ La page envoie ce que la personne a CHOISI
   { article: "billet", places: 2 }
   → le serveur va chercher le vrai prix dans sa base
     et calcule lui-même le total.`],
      ['p', "Règle générale : le navigateur envoie des <b>intentions</b>, jamais des <b>conclusions</b>. Tout ce qui a une valeur — prix, droits, identité, quantité disponible — se décide côté serveur."],
      ['h', "Faille 2 — le XSS : du code injecté dans ta page"],
      ['code', `❌ zone.innerHTML = messageDuVisiteur;
   → si le message contient du HTML, il s'exécute
     dans le navigateur de TOUS les autres visiteurs

✅ zone.textContent = messageDuVisiteur;
   → le texte s'affiche tel quel, rien ne s'exécute`],
      ['p', "C'est la faille la plus courante du web. Un visiteur écrit du code dans un champ « commentaire » ; ce code s'exécute ensuite chez tous ceux qui lisent la page, et peut voler leurs sessions. La parade tient en un mot : <code>textContent</code>."],
      ['note', "Si tu as vraiment besoin d'insérer du HTML, échappe d'abord les caractères <code>&lt;</code>, <code>&gt;</code> et <code>&amp;</code>. Mais dans 95 % des cas, <code>textContent</code> est la bonne réponse et tu n'as rien à échapper."],
      ['h', "Faille 3 — les secrets dans le code de la page"],
      ['p', "Clé d'API, mot de passe de base, jeton d'administration : rien de tout cela ne doit se trouver dans un fichier envoyé au navigateur. « Caché dans un fichier JavaScript » n'est pas caché — c'est publié."],
      ['h', "Faille 4 — vérifier les droits au bon endroit"],
      ['code', `❌ Masquer le bouton « Supprimer » aux non-admins
   → l'action reste appelable par qui sait comment

✅ Le serveur vérifie, à CHAQUE appel, que celui
   qui demande a bien le droit de le faire.`],
      ['p', "Cacher un bouton est du confort d'interface, pas de la sécurité. La question « as-tu le droit ? » se pose sur le serveur, à chaque requête, sans exception."],
      ['h', "Le minimum vital"],
      ['code', `• HTTPS partout, sans exception
• Rien de sensible en clair dans le navigateur
• textContent par défaut, innerHTML jamais
  sur du contenu venu d'un visiteur
• Vérifier les droits côté serveur, à chaque appel
• Mettre à jour ses dépendances`]
    ],
    exos: [
      { type: 'qcm',
        q: "Ton formulaire envoie <code>{ article: \"billet\", total: 15000 }</code>. Où est le problème ?",
        choix: ["Nulle part, c'est correct", "Le visiteur peut modifier le total avant l'envoi", "Le JSON est mal formé", "Il manque la date"],
        bon: 1,
        expl: "Le prix ne doit jamais venir du navigateur. Envoie le choix, laisse le serveur calculer le montant depuis sa propre base." },
      { type: 'qcm',
        q: "Un visiteur écrit du HTML dans un champ « commentaire » et tu l'affiches avec <code>innerHTML</code>. Que risques-tu ?",
        choix: ["Rien, le HTML est inoffensif", "Son code s'exécute chez tous les autres visiteurs (XSS)", "Le site ralentit", "Le commentaire est tronqué"],
        bon: 1,
        expl: "C'est une faille XSS : du code étranger s'exécute dans la page de tes visiteurs. <code>textContent</code> l'aurait affiché comme du simple texte." },
      { type: 'code',
        q: "Écris <code>echapper</code> : elle reçoit un texte et remplace <code>&amp;</code> par <code>&amp;amp;</code>, <code>&lt;</code> par <code>&amp;lt;</code> et <code>&gt;</code> par <code>&amp;gt;</code>.",
        nom: 'echapper',
        depart: `function echapper(texte) {

}`,
        tests: [
          {args:['<b>salut</b>'], att:'&lt;b&gt;salut&lt;/b&gt;'},
          {args:['a & b'], att:'a &amp; b'},
          {args:['rien'], att:'rien'}
        ],
        indice: "Remplace l'esperluette EN PREMIER, sinon tu ré-échappes ce que tu viens d'écrire : <code>.replace(/&/g,'&amp;amp;')</code> puis les chevrons.",
        expl: "L'ordre compte : si tu traites <code>&lt;</code> avant <code>&amp;</code>, le <code>&amp;</code> de <code>&amp;lt;</code> se fait réécrire à son tour. C'est le piège classique de cette fonction." }
    ]
  }
]);

/* ────────────────────────── LES SERVEURS ────────────────────────── */
ajouter('serveur', [
  {
    id: 'srv-5',
    titre: "Tenir en vie : surveiller et maintenir",
    minutes: 8,
    but: "Être prévenu avant tes clients, et savoir quoi faire quand ça casse.",
    contenu: [
      ['p', "Mettre en ligne n'est pas la fin du travail : c'est le début. Un service vit, se dégrade, tombe. La différence entre un amateur et un professionnel n'est pas que son service ne tombe jamais — c'est qu'il l'apprend avant ses clients, et qu'il sait quoi faire."],
      ['h', "1. Les journaux : la mémoire de ton service"],
      ['code', `À journaliser :
  • chaque erreur, avec ce qui l'a provoquée
  • les actions importantes (paiement, annulation)
  • les temps de réponse anormalement longs

À NE JAMAIS journaliser :
  • mots de passe, clés d'API, numéros de carte
  • données personnelles au-delà du nécessaire`],
      ['p', "Un journal sans date ni contexte ne sert à rien. Un journal qui contient des mots de passe est une fuite de données qui attend son heure."],
      ['h', "2. Les trois chiffres à connaître"],
      ['code', `Disponibilité    % du temps où le service répond
Temps de réponse la durée d'une demande, en moyenne
                 ET pour les 5 % les plus lents
Taux d'erreur    part des réponses en 4xx / 5xx`],
      ['note', "Regarde toujours les <b>plus lents</b>, pas seulement la moyenne. Une moyenne de 200 ms peut cacher 5 % d'utilisateurs à 8 secondes — et ces 5 %-là partent sans jamais se plaindre."],
      ['h', "3. Les alertes : être prévenu, pas noyé"],
      ['p', "Une alerte doit réveiller quelqu'un uniquement si une action est nécessaire tout de suite. Une alerte qui se déclenche dix fois par jour pour rien finit ignorée — et le jour où elle dit vrai, personne ne la lit. Peu d'alertes, mais des vraies."],
      ['h', "4. Les sauvegardes : la règle 3-2-1"],
      ['code', `3 copies des données
2 supports différents
1 copie hors du site principal

+ une RESTAURATION test, pour de vrai,
  au moins une fois par trimestre.`],
      ['p', "Une sauvegarde jamais restaurée n'est pas une sauvegarde : c'est une hypothèse. Beaucoup découvrent le jour du sinistre que le fichier était vide, corrompu, ou qu'il ne contenait pas la bonne base."],
      ['h', "5. Les mises à jour"],
      ['p', "Les dépendances de ton projet reçoivent des correctifs de sécurité. Ne pas mettre à jour, c'est laisser ouvertes des failles publiquement documentées. Mets à jour régulièrement et par petites touches : une année de retard se rattrape dix fois plus difficilement que douze mois d'entretien."],
      ['h', "6. La nuit où ça casse"],
      ['code', `1. Rétablir le service AVANT de comprendre
   (revenir à la version précédente, redémarrer)
2. Prévenir les clients, même sans solution :
   « nous avons un incident, on vous tient au courant »
3. Comprendre la cause, une fois le calme revenu
4. Écrire ce qui s'est passé et ce qui a changé
   pour que ça ne recommence pas`],
      ['p', "L'ordre est important. Chercher la cause pendant que le service est à terre, c'est doubler la panne. On rétablit, puis on enquête — et le retour en arrière doit être préparé <b>avant</b> d'en avoir besoin."],
      ['note', "Le compte-rendu d'incident ne cherche pas un coupable mais une cause. Une équipe qui punit les erreurs obtient des erreurs cachées, ce qui est bien pire."]
    ],
    exos: [
      { type: 'qcm',
        q: "Ton service est à terre à 21 h. Que fais-tu en premier ?",
        choix: ["Chercher la cause dans les journaux", "Rétablir le service (retour à la version précédente)", "Écrire le compte-rendu", "Attendre demain matin"],
        bon: 1,
        expl: "On rétablit d'abord, on enquête ensuite. Chercher la cause pendant la panne allonge la panne." },
      { type: 'code',
        q: "Écris <code>disponibilite</code> : elle reçoit le nombre de minutes d'arrêt dans le mois et rend le pourcentage de disponibilité, sur une base de 43 200 minutes par mois.",
        nom: 'disponibilite',
        depart: `function disponibilite(minutesArret) {

}`,
        tests: [ {args:[0], att:100}, {args:[43200], att:0}, {args:[21600], att:50}, {args:[432], att:99} ],
        indice: "Le temps en marche divisé par le temps total, multiplié par 100 : <code>(43200 - minutesArret) / 43200 * 100</code>",
        expl: "432 minutes d'arrêt — 7 heures — ne font tomber la disponibilité qu'à 99 %. Ce chiffre paraît rassurant : c'est pour ça qu'on regarde aussi le nombre de clients touchés." },
      { type: 'ordre',
        q: "Remets la gestion d'un incident dans le bon ordre.",
        items: [ "Rétablir le service au plus vite", "Prévenir les clients de l'incident", "Chercher la cause une fois le calme revenu", "Corriger la cause pour de bon", "Écrire ce qui s'est passé et ce qui a changé" ],
        expl: "Prévenir tôt coûte peu et sauve la confiance. Un client informé attend ; un client dans le noir s'en va." }
    ]
  },
  {
    id: 'srv-6',
    titre: "Comptes, mots de passe et droits",
    minutes: 7,
    but: "Protéger les comptes de tes clients — et ne pas être celui par qui la fuite arrive.",
    contenu: [
      ['p', "Le jour où ta base fuite — et des bases fuitent tous les jours — la seule question qui compte est : qu'est-ce que le voleur peut en faire ? Bien construite, la réponse est « presque rien »."],
      ['h', "1. Un mot de passe ne se range JAMAIS tel quel"],
      ['code', `❌ mot_de_passe : "amina2026"
   → la base fuite, tous les comptes sont ouverts,
     et comme les gens réutilisent leurs mots de passe,
     leurs autres comptes aussi.

✅ mot_de_passe : "$argon2id$v=19$m=65536,...$Xk9..."
   → une empreinte à sens unique. On peut vérifier
     un mot de passe, on ne peut pas le retrouver.`],
      ['p', "On appelle cela le <b>hachage</b>. À la connexion, on rehache ce que la personne tape et on compare les empreintes. Utilise un algorithme prévu pour ça — <b>argon2</b> ou <b>bcrypt</b> — jamais MD5 ni SHA-1, qui sont trop rapides et se cassent en masse."],
      ['note', "N'écris pas toi-même cette partie. Toute plateforme sérieuse fournit la gestion des comptes ; c'est un des rares endroits où réinventer est une faute, pas un apprentissage."],
      ['h', "2. Le sel : deux mots de passe identiques, deux empreintes différentes"],
      ['p', "Un <b>sel</b> est une valeur aléatoire ajoutée avant le hachage. Sans lui, deux clients ayant le même mot de passe ont la même empreinte, et un voleur casse mille comptes d'un coup. Les bons algorithmes salent automatiquement."],
      ['h', "3. La session : rester connecté sans renvoyer son mot de passe"],
      ['p', "Après la connexion, le serveur remet un <b>jeton</b> que le navigateur renvoie à chaque demande. Ce jeton doit avoir une durée de vie limitée, être révocable (bouton « déconnecter tous mes appareils ») et voyager uniquement en HTTPS."],
      ['h', "4. Le moindre privilège"],
      ['code', `Chaque compte, chaque clé, chaque service
n'a QUE les droits dont il a besoin, et rien de plus.

  Le service qui affiche les horaires
  n'a pas besoin de pouvoir supprimer des clients.`],
      ['p', "Ainsi, un compte compromis ne donne accès qu'à une petite partie. C'est la différence entre un incident et une catastrophe."],
      ['h', "5. Les secrets ne vivent pas dans le code"],
      ['code', `❌ const CLE = "sk-ant-...";   dans un fichier du dépôt
✅ La clé est lue dans une variable d'environnement,
   fournie par l'hébergeur, absente du dépôt.`],
      ['p', "Un secret poussé une fois sur un dépôt reste dans l'historique même après effacement. S'il t'échappe : révoque-le immédiatement, avant toute autre chose."],
      ['h', "6. La double authentification"],
      ['p', "Un deuxième facteur — un code à usage unique — rend un mot de passe volé presque inutile. Active-la au minimum sur tes propres comptes d'administration : ce sont eux qui ouvrent tout le reste."]
    ],
    exos: [
      { type: 'qcm',
        q: "Comment ranger le mot de passe d'un client dans ta base ?",
        choix: ["Tel quel, mais dans une table protégée", "Chiffré, avec la clé à côté", "Haché avec argon2 ou bcrypt", "Encodé en base64"],
        bon: 2,
        expl: "Le hachage est à sens unique : on vérifie sans pouvoir retrouver. Le base64 n'est pas du chiffrement, ça se décode en une seconde." },
      { type: 'qcm',
        q: "Le service qui affiche les horaires a le droit de supprimer des clients. Quel principe est violé ?",
        choix: ["Le moindre privilège", "Le chiffrement en transit", "La règle 3-2-1", "La double authentification"],
        bon: 0,
        expl: "Chaque service ne doit avoir que les droits nécessaires à son travail. Sinon une faille mineure devient une catastrophe." },
      { type: 'code',
        q: "Écris <code>motDePasseFort</code> : elle rend <code>true</code> si le mot de passe fait au moins 12 caractères ET contient au moins un chiffre.",
        nom: 'motDePasseFort',
        depart: `function motDePasseFort(mdp) {

}`,
        tests: [
          {args:['amina2026'], att:false},
          {args:['traverseeversmoheli'], att:false},
          {args:['traversee2026moheli'], att:true},
          {args:[''], att:false}
        ],
        indice: "Combine deux conditions : la longueur, et <code>/[0-9]/.test(mdp)</code> pour la présence d'un chiffre.",
        expl: "La longueur pèse plus lourd que les caractères bizarres : une phrase longue et facile à retenir bat un « P@ss1! » que personne ne mémorise." }
    ]
  }
]);

/* ─────────────────────────── API & IA ─────────────────────────── */
ajouter('ia', [
  {
    id: 'ia-5',
    titre: "Une IA en production sans se ruiner",
    minutes: 7,
    but: "Garder la facture et la latence sous contrôle quand de vrais clients l'utilisent.",
    contenu: [
      ['p', "Un assistant qui marche en démonstration peut coûter une fortune une fois ouvert au public. Le passage à l'échelle ne se règle pas après coup : il se prépare avant le premier client."],
      ['h', "1. Mesurer chaque appel, dès le premier jour"],
      ['code', `Pour chaque appel, enregistre :
  qui a appelé · quand · tokens d'entrée
  · tokens de sortie · modèle utilisé · durée

Sans ces lignes, tu découvriras le problème
sur la facture, un mois trop tard.`],
      ['p', "La réponse de l'API te donne le compte exact des tokens consommés. Enregistre-le. C'est ce qui te permettra de dire « ce sont les résumés qui coûtent, pas les réponses » plutôt que de deviner."],
      ['h', "2. Limiter par utilisateur"],
      ['code', `• X appels par personne et par heure
• Une longueur maximale acceptée en entrée
• Un plafond de dépense chez le fournisseur

Sans limite, un seul utilisateur — ou un robot —
peut vider ton budget du mois en une nuit.`],
      ['h', "3. Le cache : ne pas payer deux fois la même réponse"],
      ['p', "Beaucoup de questions reviennent à l'identique : les horaires, les tarifs, les conditions d'annulation. Range la réponse et ressers-la. C'est gratuit, instantané, et ça soulage aussi les jours de forte affluence."],
      ['h', "4. Choisir le bon modèle pour chaque tâche"],
      ['code', `Trier un message, détecter une langue,
extraire un numéro         → le modèle le plus rapide

Répondre à un client,
rédiger, résumer           → un modèle intermédiaire

Analyser un dossier complexe,
écrire du code             → le modèle le plus fort`],
      ['p', "Beaucoup d'applications font tout tourner sur le modèle le plus puissant par confort. Commence ainsi pour vérifier que ton idée marche, puis descends d'un cran là où la qualité tient : c'est souvent la moitié de la facture."],
      ['h', "5. Couper l'historique"],
      ['p', "Dans une conversation, tu renvoies tout l'historique à chaque message : le vingtième tour coûte bien plus cher que le premier. Garde les derniers échanges, résume les plus anciens, et repars à zéro quand le sujet change."],
      ['h', "6. Tomber proprement"],
      ['code', `L'API est lente, en panne, ou tu es limité (429).
Ton application doit :
  • réessayer une fois, après une courte pause
  • sinon afficher un message clair et une
    solution de repli (formulaire, WhatsApp)
  • jamais rester bloquée sur un écran qui tourne`],
      ['note', "Une fonctionnalité d'IA doit toujours avoir un plan B humain. Le jour où elle tombe, ton service doit continuer de fonctionner sans elle — dégradé, mais debout."]
    ],
    exos: [
      { type: 'qcm',
        q: "Quelle est la première chose à mettre en place avant d'ouvrir un assistant IA au public ?",
        choix: ["Un joli logo", "La mesure des tokens et un plafond de dépense", "Un modèle plus puissant", "Une base de données"],
        bon: 1,
        expl: "Sans mesure ni plafond, tu découvres le problème sur la facture. Les deux se mettent en place en une heure." },
      { type: 'code',
        q: "Écris <code>sousPlafond</code> : elle reçoit le nombre d'appels déjà faits par un utilisateur dans l'heure et le plafond autorisé, et rend <code>true</code> s'il a encore le droit d'appeler.",
        nom: 'sousPlafond',
        depart: `function sousPlafond(faits, plafond) {

}`,
        tests: [ {args:[0,20], att:true}, {args:[19,20], att:true}, {args:[20,20], att:false}, {args:[25,20], att:false} ],
        indice: "Attention à la limite exacte : au 20ᵉ appel sur un plafond de 20, il n'a plus le droit. <code>return faits &lt; plafond;</code>",
        expl: "Le piège est le <code>&lt;=</code> au lieu du <code>&lt;</code> : il accorde un appel de trop. Sur un plafond, cette erreur d'un cran se paie." },
      { type: 'ordre',
        q: "Remets dans l'ordre la mise en production d'une fonctionnalité d'IA.",
        items: [ "Mesurer les tokens et le coût sur quelques appels réels", "Poser un plafond de dépense et une limite par utilisateur", "Mettre en cache les questions qui reviennent", "Descendre au modèle le moins cher qui tient la qualité", "Prévoir ce qui se passe quand l'API tombe" ],
        expl: "On mesure avant d'optimiser : autrement on optimise ce qui ne coûte rien et on laisse passer ce qui coûte tout." }
    ]
  },
  {
    id: 'ia-6',
    titre: "Savoir si ton IA est bonne",
    minutes: 7,
    but: "Remplacer « ça a l'air de marcher » par un chiffre, et progresser pour de bon.",
    contenu: [
      ['p', "Tu changes une phrase de ton prompt, tu essaies deux exemples, ça semble mieux : tu gardes. Trois jours plus tard, un client se plaint d'un cas que tu réussissais avant. Sans mesure, tu ne progresses pas — tu déplaces le problème."],
      ['h', "1. Le jeu de test : ton unique boussole"],
      ['code', `Rassemble 30 à 50 cas RÉELS :
  la question posée  +  la bonne réponse

  « tarif enfant de 8 ans ? »      → 7 500 FC
  « bébé de 2 ans ? »              → gratuit
  « il y a un vol demain ? »       → hors sujet,
                                      doit le dire`],
      ['p', "Prends de vraies questions de vrais clients, y compris celles qui sont mal écrites, ambiguës ou hors sujet — ce sont elles qui cassent les assistants. Un jeu de test bâti sur des questions idéales ne mesure rien."],
      ['h', "2. Mesurer avant, puis après"],
      ['code', `Version A du prompt  →  41 / 50 réponses justes
Version B du prompt  →  46 / 50

Sans ces deux chiffres, « B est meilleur »
n'est qu'une impression.`],
      ['note', "Change <b>une seule chose</b> à la fois. Si tu modifies le prompt, le modèle et la température ensemble, tu ne sauras jamais lequel a produit le gain — ni lequel a produit la perte, la fois suivante."],
      ['h', "3. Ce qu'on mesure vraiment"],
      ['code', `Justesse    la réponse est-elle correcte ?
Prudence    dit-il « je ne sais pas » quand il
            faut, au lieu d'inventer ?
Format      respecte-t-il la forme demandée ?
Coût        combien de tokens par réponse ?
Vitesse     combien de secondes d'attente ?`],
      ['p', "Une réponse fausse mais confiante est bien pire qu'un « je ne trouve pas cette information ». Compte les deux séparément : un assistant qui invente une fois sur dix est inutilisable, même s'il est juste neuf fois sur dix."],
      ['h', "4. Boucler avec les vrais clients"],
      ['p', "Ajoute un pouce en haut / en bas sous chaque réponse. Les réponses mal notées deviennent de nouveaux cas de test, et ton jeu de test grandit avec ton service. C'est la boucle qui fait progresser un assistant sur la durée, bien plus que le choix du modèle."],
      ['h', "5. Quand ne PAS utiliser d'IA"],
      ['code', `Un calcul                → du code, toujours
Une règle fixe et connue → une condition, pas un modèle
Une décision à enjeu     → un humain décide,
  (remboursement, refus)   l'IA prépare le dossier
Une donnée exacte        → ta base de données`],
      ['p', "Le meilleur usage de l'IA est de <b>comprendre</b> une demande formulée en langage humain, puis de passer la main à du code fiable pour l'exécuter. La compréhension au modèle, la vérité à ta base, la décision à toi."]
    ],
    exos: [
      { type: 'qcm',
        q: "Tu modifies ton prompt et les deux exemples que tu testes sont meilleurs. Que conclure ?",
        choix: ["Le nouveau prompt est meilleur", "Rien : deux exemples ne mesurent rien", "Il faut changer de modèle", "Le prompt est trop long"],
        bon: 1,
        expl: "Deux exemples ne disent rien sur les quarante-huit autres cas. C'est exactement pour ça qu'on se constitue un jeu de test." },
      { type: 'code',
        q: "Écris <code>tauxReussite</code> : elle reçoit une liste de résultats (objets avec <code>juste</code> vrai ou faux) et rend le pourcentage de réussite, arrondi à l'entier.",
        nom: 'tauxReussite',
        depart: `function tauxReussite(resultats) {

}`,
        tests: [
          {args:[[{juste:true},{juste:true},{juste:false},{juste:true}]], att:75},
          {args:[[{juste:false}]], att:0},
          {args:[[]], att:0}
        ],
        indice: "Compte les justes, divise par le total, multiplie par 100, <code>Math.round</code> — et traite la liste vide en premier.",
        expl: "La liste vide doit rendre 0 et non <code>NaN</code> : le cas limite d'abord, comme toujours." },
      { type: 'qcm',
        q: "Un client demande le remboursement d'un billet. Quel est le bon rôle de l'IA ?",
        choix: ["Décider seule et rembourser", "Rassembler le dossier et proposer, un humain décide", "Refuser automatiquement", "Ne rien faire du tout"],
        bon: 1,
        expl: "L'IA comprend la demande et prépare le travail. Une décision qui engage de l'argent ou un client se prend par une personne." }
    ]
  }
]);

})();
