/* Kodo — programme : branches « Les serveurs » et « API & IA ». */
window.KODO_COURS = window.KODO_COURS || [];

window.KODO_COURS.push({
  id: 'serveur',
  nom: 'Les serveurs',
  sigle: '[ ]',
  couleur: '#129E63',
  pitch: "Comprendre la machine qui répond, à l'autre bout.",
  lecons: [
    {
      id: 'srv-1',
      titre: "C'est quoi un serveur",
      minutes: 5,
      but: "Savoir ce qui se passe entre le doigt du client et la page qui s'affiche.",
      contenu: [
        ['p', "Un <b>serveur</b> n'est pas une machine magique : c'est un ordinateur allumé en permanence, branché à Internet, qui attend des demandes et y répond. Ton téléphone est le <b>client</b> : il demande. Le serveur répond."],
        ['h', "Le trajet complet, en 5 étapes"],
        ['code', `1. Tu tapes    moheligo.com
2. Le DNS traduit ce nom en adresse : 172.67.1.42
3. Ton téléphone ouvre une connexion vers cette adresse, port 443
4. Il envoie une demande : « donne-moi la page d'accueil »
5. Le serveur renvoie du HTML, du CSS, du JavaScript`],
        ['p', "Le <b>DNS</b> est l'annuaire d'Internet : il transforme un nom facile à retenir en adresse IP, le vrai numéro de la machine. Le <b>port</b> est la porte d'entrée : 80 pour http, <b>443 pour https</b> (le chiffré, le seul acceptable aujourd'hui)."],
        ['h', "Statique ou dynamique"],
        ['p', "Un serveur peut se contenter de renvoyer des fichiers déjà écrits (<b>statique</b> — rapide, pas cher, très solide), ou fabriquer la réponse au moment de la demande, en lisant une base de données (<b>dynamique</b>)."],
        ['note', "MoheliGo est un site statique + une base de données en ligne. C'est pour ça qu'il tient debout sans serveur à surveiller : les fichiers sont posés sur un réseau mondial, et les réservations vont dans une base séparée."],
        ['h', "Le vocabulaire qui revient tout le temps"],
        ['code', `Serveur     la machine qui répond
Client      celui qui demande (navigateur, application)
IP          l'adresse numérique d'une machine
DNS         l'annuaire nom → adresse
Port        la porte d'entrée (443 = https)
Hébergeur   l'entreprise chez qui tourne ton serveur
Latence     le temps d'aller-retour de la demande`]
      ],
      exos: [
        { type: 'qcm',
          q: "Le DNS sert à quoi ?",
          choix: ["À chiffrer les données", "À traduire un nom de site en adresse IP", "À stocker les fichiers", "À accélérer le site"],
          bon: 1,
          expl: "C'est l'annuaire : <code>moheligo.com</code> devient une adresse numérique que la machine sait joindre." },
        { type: 'qcm',
          q: "Quel port utilise une connexion sécurisée sur le web ?",
          choix: ['80', '443', '8080', '22'],
          bon: 1,
          expl: "443 = https (chiffré). 80 = http (en clair, à éviter). 22 = SSH, pour administrer un serveur." },
        { type: 'ordre',
          q: "Remets le trajet d'une demande dans l'ordre.",
          items: [ "Le visiteur tape l'adresse du site", "Le DNS traduit le nom en adresse IP", "Le navigateur ouvre une connexion vers cette adresse", "Le serveur renvoie la page", "Le navigateur affiche la page" ],
          expl: "Rien ne peut partir avant que le nom soit traduit en adresse : le DNS est toujours la première étape invisible." }
      ]
    },
    {
      id: 'srv-2',
      titre: "HTTP : demander et répondre",
      minutes: 6,
      but: "Lire une erreur au lieu de la subir.",
      contenu: [
        ['p', "<b>HTTP</b> est la langue que parlent le client et le serveur. Chaque échange a la même forme : une demande, une réponse. La demande dit ce qu'on veut faire (le <b>verbe</b>) et sur quoi (le <b>chemin</b>)."],
        ['h', "Les verbes"],
        ['code', `GET     lire        (afficher la liste des traversées)
POST    créer       (enregistrer une réservation)
PUT     remplacer   (modifier une fiche entière)
PATCH   corriger    (changer juste le nombre de places)
DELETE  supprimer   (annuler une réservation)`],
        ['note', "Règle d'or : <code>GET</code> ne doit JAMAIS modifier quoi que ce soit. Un lien qu'on clique ne supprime rien. Sinon le premier robot qui visite ton site efface ta base."],
        ['h', "Les codes de réponse : le serveur te dit ce qui s'est passé"],
        ['code', `2xx  ça a marché
  200  OK
  201  créé (après un POST)
3xx  va voir ailleurs
  301  déménagé pour toujours
4xx  TA demande a un problème
  400  demande mal écrite
  401  pas connecté
  403  connecté, mais interdit
  404  cette adresse n'existe pas
  429  tu demandes trop vite, calme-toi
5xx  MON serveur a un problème
  500  erreur interne (un bug côté serveur)
  503  serveur indisponible / surchargé`],
        ['p', "Retiens la frontière : <b>4xx = ta faute</b> (adresse, droits, format), <b>5xx = la faute du serveur</b>. Ça change complètement où tu vas chercher le bug."],
        ['h', "Les en-têtes"],
        ['p', "Chaque demande et chaque réponse portent des <b>en-têtes</b> : de petites étiquettes autour du contenu. <code>Content-Type</code> dit quel format est envoyé, <code>Authorization</code> porte le jeton de connexion, <code>Cache-Control</code> dit combien de temps on peut garder la réponse en mémoire."]
      ],
      exos: [
        { type: 'qcm',
          q: "Ton application reçoit un code <b>403</b>. Que s'est-il passé ?",
          choix: ["La page n'existe pas", "Le serveur a planté", "Tu es identifié mais tu n'as pas le droit", "Tu n'es pas connecté du tout"],
          bon: 2,
          expl: "401 = « je ne sais pas qui tu es ». 403 = « je sais qui tu es, et c'est non »." },
        { type: 'code',
          q: "Écris <code>lireCode</code> : elle reçoit un code HTTP (nombre) et rend <code>\"client\"</code> pour les 4xx, <code>\"serveur\"</code> pour les 5xx, <code>\"ok\"</code> pour les 2xx, et <code>\"autre\"</code> pour le reste.",
          nom: 'lireCode',
          depart: `function lireCode(code) {

}`,
          tests: [ {args:[200], att:'ok'}, {args:[201], att:'ok'}, {args:[404], att:'client'}, {args:[500], att:'serveur'}, {args:[301], att:'autre'} ],
          indice: "Compare des tranches : <code>if (code >= 500) return \"serveur\";</code> puis 400, puis 200.",
          expl: "On teste les tranches de la plus haute à la plus basse, sinon 500 tomberait aussi dans « ≥ 400 »." },
        { type: 'qcm',
          q: "Quel verbe utiliser pour enregistrer une nouvelle réservation ?",
          choix: ['GET', 'POST', 'DELETE', 'PATCH'],
          bon: 1,
          expl: "POST crée quelque chose de nouveau. GET ne doit jamais rien modifier." }
      ]
    },
    {
      id: 'srv-3',
      titre: "Mettre en ligne, et rester en ligne",
      minutes: 6,
      but: "Passer de « ça marche chez moi » à « ça marche pour tout le monde ».",
      contenu: [
        ['p', "Un site sur ton ordinateur n'existe pour personne. Le mettre en ligne, c'est trois choses : un <b>hébergement</b>, un <b>nom de domaine</b>, et un <b>certificat</b> pour le https."],
        ['h', "1. L'hébergement"],
        ['p', "Aujourd'hui, pour un site fait de fichiers (HTML, CSS, JS), l'hébergement statique est gratuit ou presque, et distribué dans le monde entier : ton visiteur est servi par la machine la plus proche de lui. C'est plus rapide et plus solide qu'un serveur unique."],
        ['h', "2. Le nom de domaine"],
        ['p', "Tu loues un nom à l'année. Ensuite tu règles ses <b>enregistrements DNS</b> pour le faire pointer vers ton hébergement. Compte quelques minutes à quelques heures avant que le changement se propage partout."],
        ['h', "3. HTTPS"],
        ['p', "Le certificat chiffre la connexion entre le visiteur et toi. Sans lui, le navigateur affiche « site non sécurisé » et personne ne paie chez toi. Les hébergeurs sérieux l'installent et le renouvellent automatiquement, gratuitement."],
        ['h', "Ce qui casse en production"],
        ['code', `• Le cache : tu publies, le visiteur voit l'ancienne version
  → change le nom des fichiers ou force le rechargement
• Les secrets dans le code public
  → tout ce qui part au navigateur est lisible par tous
• La base de données sans sauvegarde
  → une sauvegarde qu'on n'a jamais restaurée n'existe pas
• « ça marche chez moi »
  → teste sur un vrai téléphone, en connexion lente`],
        ['note', "Le vrai test aux Comores : ouvre ton site sur un téléphone d'entrée de gamme, en 3G, sans vider le cache. Si c'est agréable là, c'est agréable partout."],
        ['h', "Sauvegarder, versionner"],
        ['p', "Un dépôt <b>Git</b> garde l'historique de chaque modification et te permet de revenir en arrière. Poussé sur un service en ligne, il devient aussi ta sauvegarde. Une machine qui grille ne doit jamais coûter plus qu'une journée de travail."]
      ],
      exos: [
        { type: 'qcm',
          q: "Tu as publié une correction mais les visiteurs voient encore l'ancienne page. Le coupable le plus probable ?",
          choix: ["Le DNS", "Le cache", "Le certificat https", "La base de données"],
          bon: 1,
          expl: "Le navigateur garde les fichiers en mémoire pour aller plus vite. Il faut lui signaler que le fichier a changé." },
        { type: 'qcm',
          q: "Où ne faut-il JAMAIS écrire un mot de passe ou une clé secrète ?",
          choix: ["Dans un fichier JavaScript envoyé au navigateur", "Dans un coffre de secrets côté serveur", "Dans un gestionnaire de mots de passe", "Dans une variable d'environnement du serveur"],
          bon: 0,
          expl: "Tout ce qui part au navigateur est lisible par n'importe qui : clic droit, « afficher le code source », et c'est vu. Un secret ne vit que côté serveur." },
        { type: 'ordre',
          q: "Remets la mise en ligne dans l'ordre.",
          items: [ "Le code est prêt et testé en local", "On le pousse sur un dépôt Git", "L'hébergeur publie les fichiers", "On fait pointer le nom de domaine dessus", "Le certificat https est activé" ],
          expl: "Le domaine et le certificat viennent en dernier : ils s'accrochent à quelque chose qui existe déjà en ligne." }
      ]
    }
  ]
});

window.KODO_COURS.push({
  id: 'ia',
  nom: 'API & IA',
  sigle: 'AI',
  couleur: '#8B5CF6',
  pitch: "Faire parler ton application avec le reste du monde.",
  lecons: [
    {
      id: 'ia-1',
      titre: "Une API, c'est quoi",
      minutes: 6,
      but: "Aller chercher des données chez quelqu'un d'autre et t'en servir.",
      contenu: [
        ['p', "Une <b>API</b> est une porte ouverte volontairement par un service pour que d'autres programmes viennent lui parler. Pas une page pour les yeux humains : des données brutes, pour les machines. La météo, les cartes, le paiement, l'IA : tout passe par des API."],
        ['h', "Appeler une API depuis le navigateur"],
        ['code', `async function meteo() {
  const url = "https://api.open-meteo.com/v1/forecast"
            + "?latitude=-12.3&longitude=43.7&hourly=wave_height";

  const reponse = await fetch(url);

  if (!reponse.ok) {              // reponse.ok = code 2xx
    throw new Error("Erreur " + reponse.status);
  }

  const data = await reponse.json();
  return data.hourly.wave_height[0];
}`],
        ['h', "Les trois mots à comprendre"],
        ['p', "<code>fetch</code> lance la demande. <code>await</code> veut dire « attends la réponse avant de continuer » — sans lui, tu récupères une promesse vide au lieu des données. <code>async</code> devant la fonction est obligatoire pour avoir le droit d'utiliser <code>await</code> dedans."],
        ['note', "L'erreur de débutant numéro un : oublier un <code>await</code>. Tu obtiens alors <code>[object Promise]</code> au lieu de tes données. Chaque <code>fetch</code> et chaque <code>.json()</code> en demandent un."],
        ['h', "Toujours gérer l'échec"],
        ['p', "<code>fetch</code> ne se plaint <b>pas</b> tout seul quand le serveur renvoie 404 ou 500 : il te rend quand même une réponse. C'est à toi de tester <code>reponse.ok</code>. Aux Comores, prévois aussi le cas « pas de réseau » : entoure l'appel d'un <code>try / catch</code> et affiche quelque chose d'utile plutôt qu'un écran blanc."],
        ['code', `try {
  const h = await meteo();
  afficher(h);
} catch (e) {
  afficher("Météo indisponible, réessayez plus tard.");
}`],
        ['h', "La clé d'API"],
        ['p', "Beaucoup d'API demandent une <b>clé</b> : une longue chaîne secrète qui dit qui appelle, et qui fait payer. Elle s'envoie dans un en-tête, jamais dans l'adresse."]
      ],
      exos: [
        { type: 'qcm',
          q: "Que rend <code>fetch(url)</code> si le serveur répond 404 ?",
          choix: ["Il déclenche une erreur tout seul", "Une réponse avec <code>ok = false</code>", "<code>null</code>", "Il réessaie automatiquement"],
          bon: 1,
          expl: "<code>fetch</code> n'échoue que si la connexion échoue. Un 404 est une réponse valide : à toi de tester <code>reponse.ok</code>." },
        { type: 'code',
          q: "Écris <code>estOk</code> : elle reçoit un objet réponse (avec un champ <code>status</code>) et rend <code>true</code> seulement si le code est entre 200 et 299.",
          nom: 'estOk',
          depart: `function estOk(reponse) {

}`,
          tests: [ {args:[{status:200}], att:true}, {args:[{status:299}], att:true}, {args:[{status:404}], att:false}, {args:[{status:500}], att:false}, {args:[{status:199}], att:false} ],
          indice: "Un seul <code>return</code> avec un ET : <code>return reponse.status >= 200 && reponse.status < 300;</code>",
          expl: "Une comparaison rend déjà <code>true</code> ou <code>false</code> — pas besoin de <code>if</code>." },
        { type: 'ordre',
          q: "Remets un appel d'API dans l'ordre.",
          items: [ "Construire l'adresse avec ses paramètres", "await fetch(url)", "Vérifier reponse.ok", "await reponse.json()", "Utiliser les données dans la page" ],
          expl: "On vérifie AVANT de lire le contenu : lire le JSON d'une page d'erreur ne donne rien d'utile." }
      ]
    },
    {
      id: 'ia-2',
      titre: "L'IA en pratique : modèle, tokens, coût",
      minutes: 7,
      but: "Savoir ce que tu achètes quand tu appelles une IA.",
      contenu: [
        ['p', "Une IA de texte est un <b>modèle</b> : un très gros programme entraîné, qui reçoit du texte et prédit la suite. Tu ne l'installes pas, tu l'appelles par une API, comme la météo. Tu paies à l'usage."],
        ['h', "1. Le token, l'unité de facturation"],
        ['p', "Le modèle ne lit pas des lettres mais des <b>tokens</b> : des morceaux de mots. En français, un token vaut à peu près 3 à 4 caractères ; un texte de 100 mots pèse environ 150 tokens. On te facture séparément :"],
        ['code', `tokens d'entrée   tout ce que tu envoies (la question,
                  les consignes, l'historique de la discussion)
tokens de sortie  tout ce que le modèle écrit
                  (nettement plus cher que l'entrée)`],
        ['note', "Piège classique : dans une conversation, tu renvoies TOUT l'historique à chaque message. Le 20ᵉ message coûte donc bien plus cher que le 1ᵉʳ. Coupe l'historique ou résume-le."],
        ['h', "2. Choisir son modèle"],
        ['p', "Chez Anthropic, en août 2026, trois familles se partagent le travail :"],
        ['code', `claude-opus-5     le plus capable : raisonnement,
                  code, travail long et autonome
claude-sonnet-5   très bon rapport qualité / prix,
                  pour le gros du volume
claude-haiku-4-5  le plus rapide et le moins cher,
                  pour les tâches simples (classer, trier)`],
        ['p', "La règle est simple : commence par le modèle le plus fort pour vérifier que ton idée marche, puis descends d'un cran tant que la qualité tient. Descendre d'abord fait perdre du temps à débugger une qualité insuffisante."],
        ['h', "3. Le prompt : ce que tu écris compte plus que le modèle"],
        ['code', `Mauvais :  « Écris un texte sur MoheliGo. »

Bon :      « Tu es responsable communication de MoheliGo,
             réservation de traversées Grande Comore ↔ Mohéli.
             Écris un post Facebook de 60 mots pour annoncer
             la traversée de samedi, ton direct, sans emoji,
             et termine par : moheligo.com »`],
        ['p', "Donne le <b>rôle</b>, le <b>contexte</b>, le <b>format</b> et les <b>contraintes</b>. Un modèle n'invente pas ce que tu ne dis pas : il choisit un défaut passe-partout."],
        ['h', "4. Ce qu'une IA ne sait pas"],
        ['p', "Elle ne connaît pas tes données privées, ni ce qui s'est passé après son entraînement, et elle peut affirmer une chose fausse avec beaucoup d'aplomb. Pour tout ce qui compte — un prix, un horaire, un chiffre — donne-lui la donnée dans la question, ou vérifie sa réponse."]
      ],
      exos: [
        { type: 'qcm',
          q: "Environ combien de tokens pour un texte français de 100 mots ?",
          choix: ['Environ 20', 'Environ 150', 'Environ 1000', 'Exactement 100'],
          bon: 1,
          expl: "Compte à peu près 1,5 token par mot en français. C'est une estimation : pour un chiffre exact, il existe une API de comptage." },
        { type: 'qcm',
          q: "Ta facture d'IA explose sur un chat qui dure. Le coupable le plus probable ?",
          choix: ["Le modèle est trop cher", "Tu renvoies tout l'historique à chaque message", "Les réponses sont trop courtes", "Tu appelles trop rarement"],
          bon: 1,
          expl: "Chaque message renvoie toute la conversation en entrée. Plus elle est longue, plus chaque tour coûte cher. Coupe ou résume l'historique." },
        { type: 'code',
          q: "Écris <code>coutFC</code> : elle reçoit un nombre de tokens et un prix en FC pour mille tokens, et rend le coût total.",
          nom: 'coutFC',
          depart: `function coutFC(tokens, prixMille) {

}`,
          tests: [ {args:[1000, 25], att:25}, {args:[2500, 25], att:62.5}, {args:[0, 25], att:0} ],
          indice: "Combien de milliers de tokens ? <code>tokens / 1000</code>, multiplié par le prix.",
          expl: "<code>return (tokens / 1000) * prixMille;</code> — c'est la règle de trois qui gouverne toute facture d'IA." }
      ]
    },
    {
      id: 'ia-3',
      titre: "Brancher une IA sur ton application",
      minutes: 7,
      but: "Faire l'appel pour de vrai, sans se faire voler sa clé.",
      contenu: [
        ['p', "Voici l'appel réel à l'API Messages d'Anthropic. Une seule adresse, trois en-têtes, un corps en JSON. Une fois compris, tous les autres services d'IA se ressemblent."],
        ['h', "La requête"],
        ['code', `POST https://api.anthropic.com/v1/messages

En-têtes :
  x-api-key: TA_CLE_SECRETE
  anthropic-version: 2023-06-01
  content-type: application/json

Corps :
{
  "model": "claude-opus-5",
  "max_tokens": 1024,
  "messages": [
    { "role": "user", "content": "Résume ce texte en 3 phrases : ..." }
  ]
}`],
        ['p', "<code>model</code> choisit le moteur. <code>max_tokens</code> est le plafond de la réponse — le dépasser coupe le texte au milieu, alors laisse de la marge. <code>messages</code> est la conversation : chaque tour a un <code>role</code> (<code>user</code> ou <code>assistant</code>) et un contenu."],
        ['h', "La réponse"],
        ['code', `{
  "content": [ { "type": "text", "text": "La réponse..." } ],
  "stop_reason": "end_turn",
  "usage": { "input_tokens": 412, "output_tokens": 96 }
}`],
        ['p', "Le texte est dans <code>content</code>, qui est une <b>liste</b> de blocs : prends celui dont le <code>type</code> vaut <code>text</code> plutôt que de prendre le premier les yeux fermés. <code>usage</code> te donne la facture exacte du tour. <code>stop_reason</code> te dit pourquoi ça s'est arrêté : <code>end_turn</code> (fini normalement) ou <code>max_tokens</code> (coupé, ton plafond était trop bas)."],
        ['h', "⚠️ La clé ne va JAMAIS dans le navigateur"],
        ['p', "C'est la règle qui coûte le plus cher quand on l'oublie. Si tu mets ta clé dans le JavaScript de ta page, n'importe quel visiteur peut l'afficher en trois clics, s'en servir, et c'est <b>toi</b> qui paies — parfois des milliers d'euros avant que tu ne t'en rendes compte."],
        ['code', `❌ INTERDIT — la clé part chez tous les visiteurs
  fetch("https://api.anthropic.com/v1/messages", {
    headers: { "x-api-key": "sk-ant-..." }
  })

✅ CORRECT — deux étages
  navigateur  →  ton petit serveur  →  l'API d'IA
                 (la clé vit ici,
                  et seulement ici)`],
        ['p', "Ton serveur intermédiaire fait trois choses qu'un navigateur ne peut pas faire : il garde la clé, il vérifie qui a le droit d'appeler, et il limite le nombre d'appels par personne pour qu'un seul utilisateur ne vide pas ton budget."],
        ['h', "Les garde-fous à poser dès le premier jour"],
        ['code', `• Un plafond de dépense chez le fournisseur
• Une limite d'appels par utilisateur et par heure
• Une longueur maximale acceptée en entrée
• Un journal : qui a appelé, quand, combien de tokens
• Un message propre quand ça échoue
  (le réseau tombe, l'API répond 429 : trop de demandes)`],
        ['note', "Si ta clé s'échappe un jour : va la révoquer chez le fournisseur immédiatement, avant toute autre chose. Une clé publiée est une clé morte — même effacée du code, elle reste dans l'historique."]
      ],
      exos: [
        { type: 'qcm',
          q: "Où doit vivre une clé d'API d'IA ?",
          choix: ["Dans le JavaScript de la page", "Sur ton serveur, jamais envoyée au navigateur", "Dans l'adresse de l'appel", "Dans le HTML, cachée dans un commentaire"],
          bon: 1,
          expl: "Tout ce qui atteint le navigateur est public. Le serveur intermédiaire existe uniquement pour garder ce secret." },
        { type: 'qcm',
          q: "La réponse contient <code>\"stop_reason\": \"max_tokens\"</code>. Que s'est-il passé ?",
          choix: ["Le modèle a fini normalement", "La réponse a été coupée avant la fin", "La clé est invalide", "Il n'y a plus de crédit"],
          bon: 1,
          expl: "Le modèle a atteint ton plafond <code>max_tokens</code> et s'est arrêté au milieu. Augmente le plafond." },
        { type: 'code',
          q: "Écris <code>extraireTexte</code> : elle reçoit une réponse de l'API (objet avec une liste <code>content</code>) et rend le texte du premier bloc de type <code>\"text\"</code>, ou <code>\"\"</code> s'il n'y en a aucun.",
          nom: 'extraireTexte',
          depart: `function extraireTexte(reponse) {

}`,
          tests: [
            {args:[{content:[{type:'text', text:'Bonjour'}]}], att:'Bonjour'},
            {args:[{content:[{type:'thinking'},{type:'text', text:'La suite'}]}], att:'La suite'},
            {args:[{content:[]}], att:''}
          ],
          indice: "<code>const bloc = reponse.content.find(b => b.type === \"text\");</code> puis rends <code>bloc ? bloc.text : \"\"</code>.",
          expl: "On cherche le bon bloc au lieu de prendre <code>content[0]</code> : la liste peut commencer par autre chose, et elle peut être vide." },
        { type: 'ordre',
          q: "Remets l'architecture correcte dans l'ordre du trajet.",
          items: [ "Le visiteur écrit sa question dans la page", "La page envoie la question à TON serveur", "Ton serveur vérifie les droits et ajoute la clé secrète", "Ton serveur appelle l'API d'IA", "La réponse revient au visiteur, sans la clé" ],
          expl: "La clé n'entre en scène qu'à l'étape 3, sur ta machine, et n'en ressort jamais." }
      ]
    }
  ]
});
