# ⬛ LA BARRE — norme de communication MoheliGo

> **Posée par le patron le 29/08/2026** : « je ne joue plus dans la cour des
> entreprises comoriennes, je veux m'imposer comme numéro un dans mon domaine.
> Les petites détails comptent. Tout doit être correct. »
>
> 📏 **RÈGLE DE RÉDACTION DE CE DOCUMENT** : chaque exigence est **vérifiable
> par un chiffre ou par une machine**. Pas un adjectif. « Plus soigné », « plus
> premium », « plus émotionnel » ne sont pas des exigences — ce sont des vœux.
> Ce qui n'est pas mesurable n'entre pas ici.
>
> 🤖 Le contrôle automatique : `python3 pub/flyers/exigence.py <fichier.html>`.
> Il **refuse**. Une norme que personne ne peut enfreindre est une norme ; une
> norme qu'on relit de bonne volonté est une intention.

---

## 0. Ce que « exigeant » veut dire ici

Trois relecteurs extérieurs indépendants (26, 29 et 29/08) ont convergé sur le
même diagnostic : notre point faible n'est ni le goût ni les idées — c'est **la
discipline**. Noté 5,5/10, l'écart le plus fort.

Et la mesure interne du 29/08 leur donne raison, en pire :

| Ce qu'on croyait tenir | Ce que la mesure a trouvé |
|---|---|
| « notre vague est notre signature » | **14 tracés différents**, et 33 visuels sur 45 n'en portent aucune |
| « l'or est notre couleur d'accent » | de **0,1 % à 19,8 %** selon les visuels ; 27 sur 39 hors bande |
| « notre emblème est reconnaissable » | **414 nuances à 32 px** : une tache, pas un symbole |
| « nos textes sont propres » | **186 apostrophes droites, 0 typographique — 100 % de fautes** |

📌 **La barre n'est donc pas « faire plus beau ». C'est : ne plus jamais laisser
passer ce qui se mesure.**

---

## 1. UN SEUL UNIVERS, DEUX MOMENTS — et non deux tons

Le marché comorien **impose** d'expliquer : une grande partie des gens n'a
jamais réservé ni payé en ligne. Supprimer le « comment », c'est supprimer ce
qui convertit. Mais expliquer n'autorise pas à baisser le niveau.

> **La règle : l'émotion ouvre, le produit livre — dans le même univers.**
> Même lumière, même typographie, même calme, même marge. Ce qui change entre
> les deux, c'est le SUJET de la phrase, jamais le soin.

| | Le moment ÉMOTION | Le moment PRODUIT |
|---|---|---|
| ce qu'il fait | donne envie de traverser | montre que c'est faisable |
| sujet de la phrase | quelqu'un, un lieu, un retour | un geste que le lecteur fait |
| ce qui est interdit | un mode d'emploi | un ton de notice |
| exemple qui passe | « On ne traverse pas la mer. On va voir quelqu'un. » | « Tu ne vas plus au port. » |
| exemple qui échoue | — | « Voici comment ça marche » |

⛔ **Le piège nommé** : une explication a le droit d'être précise, jamais d'être
plate. « Voici comment ça marche » est une notice. « C'est aussi simple que ça »
est la même information, avec une posture.

---

## 1 bis. UNE SEULE INFORMATION PAR VISUEL

> Commande du patron, 02/09/2026 : « même les mots, tout doit être nickel et
> mesuré. **On ne doit pas avoir plus d'une information par flyer.** »

Le § 6 disait déjà « une seule chose nette ». Cette règle-ci est plus dure et
elle porte sur le FOND, pas sur le dessin : ce n'est pas « un seul point de
fixation », c'est **une seule chose à retenir en sortant**.

**Comment on compte, et c'est là que ça devient utile :** on ne compte pas les
blocs, on compte les FAITS DISTINCTS. Un chiffre, sa jauge et sa légende ne font
qu'une information s'ils disent tous la même chose. En revanche, **le même fait
répété sous trois formes fait trois informations** — parce que le lecteur, lui,
croit qu'on lui en donne trois, et il partage son attention en trois.

⛔ **LE CAS QUI A SERVI DE TEST : LE BULLETIN DU SOIR, 02/09/2026.** Il disait la
houle **trois fois** — en gros chiffre (0,9 m), en amplitude (0,9–1,0 m), puis en
courbe heure par heure. Plus une « période de houle » en secondes.
· *période de houle* → **supprimée**. C'est un chiffre de météorologue. Aucun
  voyageur ne sait quoi en faire, et **un chiffre qu'on ne sait pas lire
  n'informe pas : il impressionne.** Ce n'est pas la même chose, et ce n'est pas
  notre métier.
· *amplitude* → **supprimée**, doublon exact du gros chiffre.
· *vent* → **gardé** : seul fait réellement distinct de la houle, et il change la
  traversée pour de bon.
📌 **TROIS FOIS LE MÊME FAIT N'EST PAS DE LA PROFONDEUR, C'EST DE LA
RÉPÉTITION** — et chaque répétition vole du regard au verdict, qui est la seule
chose à retenir.

⚠️ **La donnée supprimée de l'affichage n'est pas supprimée du système.**
`PERIODE`, `AMPLI` et `AMPLI_LAB` restent calculés par `bulletin.py` et écrits
dans `bulletin.json`. On pourra les réafficher sans rien recalculer. **Cacher
n'est pas jeter** : c'est une décision de mise en page, elle doit rester
réversible.

🔴 **Ce qui reste en question, et c'est au patron :** la courbe heure par heure
est la troisième expression du même fait. Elle répond quand même à une question
que le chiffre seul ne couvre pas — « est-ce que ça change dans la matinée ? ».
Gardée pour l'instant, à supprimer d'un mot.

---

## 2. LA PHRASE

> 🍎 **LA RÈGLE D'ÉCRITURE, POSÉE PAR LE PATRON LE 02/09/2026** — elle prime sur
> tout le reste de cette section : « les écritures doivent être vraiment style
> Apple, deux à cinq mots mais très impactant, et inspirer le respect de la
> marque. Tout doit être vraiment vérifié, strict et soigné, même les textes et
> les photos. »
>
> Ce que ça change concrètement, et pourquoi ce n'est pas cosmétique :
> **à six mots on explique encore, à quatre on affirme.** « Think different. »
> « Bigger than bigger. » « Privacy. That's iPhone. » Personne n'y finit une
> phrase — on y pose une idée, et on laisse le lecteur la terminer. Un titre qui
> explique demande la permission ; un titre qui affirme inspire le respect.
> C'est exactement ce que le patron appelle « inspirer le respect de la marque ».

**Le titre**
- **2 à 5 mots PAR LIGNE**, **32 signes maximum par ligne**, **2 lignes maximum**.
  - Le plafond se compte **par ligne**, parce que c'est ce que l'œil saisit d'un
    coup (règle du 30/08). « ON NE VISITE PAS MOHÉLI. / ON Y REVIENT. » fait 5
    et 3 : elle passe, et elle reste notre meilleure ligne.
  - Le plancher se compte **sur le titre entier**. ⚠️ Une ligne d'UN SEUL MOT
    n'est pas une faute, c'est une **cadence** — « TU L'AS / **DÉJÀ.** », « TU
    PARS VOIR / **QUELQU'UN.** ». Le mot isolé porte l'accent parce que le
    regard s'y arrête ; c'est le geste Apple lui-même. Ce qui est interdit,
    c'est un titre entier d'un seul mot : « MOHÉLI. » n'est pas une accroche,
    c'est une étiquette.
  - 📌 J'ai écrit l'inverse au premier jet (plancher par ligne) et le contrôle a
    immédiatement refusé les deux visuels les mieux notés de toute la
    bibliothèque. **Une règle qui refuse ce qu'on a fait de mieux n'est pas
    exigeante, elle est mal écrite** — troisième fois que cette leçon revient.
- Il parle du **LECTEUR**, pas du produit. Test binaire : il contient un
  *tu / ton / ta / tes*, un verbe à l'impératif, ou il nomme une situation vécue.
  ⛔ « L'ère de la digitalisation » — échoue : sujet = une abstraction.
  ✅ « Tu ne vas plus au port » — passe : sujet = le lecteur.
- **Aucun mot abstrait** dans le titre. La liste noire, mesurée par la machine :
  *digitalisation, solution, plateforme, innovation, révolution, ère, écosystème,
  expérience, service, technologie, optimisation, digital*.

**Le corps**
- **25 mots maximum** au total, **12 mots maximum par phrase**.
- Un seul mot abstrait toléré, zéro recommandé.
- **Aucun point d'exclamation.** Aucun emoji sur le visuel (le texte du post en
  autorise, le visuel jamais).
- **Aucun superlatif invérifiable** : *le meilleur, le plus rapide, unique,
  révolutionnaire, incontournable, leader*.
- **Aucun chiffre non mesuré.** Règle du 29/08, née d'un conseil dangereux :
  écrire « +1 000 voyageurs » avec 33 abonnés et zéro réservation mesurée, dans
  une île où tout le monde se connaît, ne coûte pas une pub — ça coûte la
  confiance, et la confiance est exactement ce qu'on essaie de construire.

---

## 3. LE SENTIMENT — déclaré, pas supposé

On ne vend pas une traversée. On vend l'état dans lequel elle met quelqu'un.
**Quatre sentiments, et rien d'autre** — ce sont les seuls qui soient vrais chez
nous :

| | Le sentiment | Ce qu'il dit vraiment |
|---|---|---|
| **1** | **LE SOULAGEMENT** | ne plus descendre au port pour rien, ne plus attendre sans savoir |
| **2** | **LA PROXIMITÉ** | on ne traverse pas la mer, on va voir quelqu'un |
| **3** | **LA FIERTÉ** | ça vient de chez nous, et ça marche |
| **4** | **LA CONFIANCE** | une vraie personne répond quand tu écris |

⚠️ **Chaque visuel DÉCLARE le sien**, en clair, dans son commentaire d'en-tête :
`SENTIMENT : LA PROXIMITÉ`. Un visuel qui n'en déclare aucun **n'est pas fini** —
et la machine le refuse. Ce n'est pas une formalité : un visuel qui vise deux
sentiments à la fois n'en transmet aucun.

---

## 4. L'APPEL À L'ACTION

- **Un seul par visuel.** Deux appels = zéro appel.
- **Verbe à l'impératif + objet.** « Réserve ta traversée. »
- ⛔ Interdits : *En savoir plus, Cliquez ici, Découvrez, Contactez-nous,
  N'hésitez pas*. Ce sont des formules qui ne demandent rien.
- **Toujours accompagné du lieu où agir** : `moheligo.com`. Un verbe sans
  adresse est un vœu.
- **Toute action est en or.** L'inverse n'est pas vrai — l'or est aussi notre
  couleur de marque (203 emplois mesurés), donc tout ce qui est or n'est pas une
  action. Mais aucune action n'est d'une autre couleur.

---

## 5. LA MICRO-TYPOGRAPHIE FRANÇAISE — c'est ici que « le détail » se mesure

> **Mesuré le 29/08 sur toute la bibliothèque : 186 apostrophes droites, 0
> typographique. 100 % de fautes.** C'est le genre de défaut que personne ne
> nomme et que tout le monde ressent : c'est exactement la différence entre un
> document tapé et un document composé.

| Règle | ⛔ Faux | ✅ Juste |
|---|---|---|
| **Apostrophe** typographique U+2019 | `L'océan` | `L’océan` |
| **Espace fine insécable** U+202F avant `; : ! ?` | `Tu veux voir ?` | `Tu veux voir␣?` |
| **Guillemets français** avec leurs espaces | `"la mer"` | `«␣la mer␣»` |
| **Tiret cadratin** pour l'incise | `- comme ça -` | `— comme ça —` |
| **Espace insécable** dans un nombre, un numéro, avant une unité | `2minutes` | `2␣minutes` |
| **Aucun caractère hors latin de base** | `MOHÉLI ↔ GRANDE COMORE` | `MOHÉLI · GRANDE COMORE` |

⚠️ La dernière ligne n'est pas une préférence : nos woff2 sont des
sous-ensembles latins. Un signe absent **ne lève aucune erreur** — Chromium le
remplace en silence. Le 29/08, la flèche `↔` s'est affichée « .. » sur un visuel
fini. **Un caractère absent ne fait pas un bug, il fait un visuel faux.**

Et trois règles de composition :
- **Aucun mot seul sur la dernière ligne** d'un paragraphe (une « ligne veuve »).
  🤖 Mesuré par `node lignes.js <flyer.html>` — ajouté le 30/08 parce que cette
  règle était écrite depuis la veille et que **rien ne la faisait respecter** :
  « embarques. » est resté seul sous deux lignes pleines dans un visuel qui
  passait tous les autres contrôles. ⚠️ L'outil ne juge que les coupures
  **automatiques** : là où le dessinateur a coupé lui-même (`<br>`, span doré en
  `display:block`, `<small>` de signature), il n'y a rien à signaler.
  📌 Et ce n'est pas la COLONNE qu'on élargit, c'est la PHRASE qu'on recoupe :
  le 30/08, 400 px et 424 px donnaient la même veuve.
- **Aucune date, aucun nombre, aucun numéro coupé en fin de ligne.** Vu le
  29/08 : « 2025-2026 » se cassait en « 2025- » / « 2026 ». ⚠️ On ne corrige PAS
  avec un trait insécable U+2011 — il est hors de nos woff2 et disparaîtrait en
  silence. La seule solution propre est `white-space: nowrap` en CSS.
- **L'espacement des lettres se règle en CSS, jamais en tapant des espaces.**
  Écrire `T R A V E R S É E S` puis appliquer `letter-spacing` cumule les deux :
  le `S` final est passé sous la diagonale du coin, en août.
- **Aucun bloc de texte ne doit en toucher un autre.**
  🤖 Mesuré par `node collision.js <flyer.html>` ou `--tous`, ajouté le 02/09.
  ⛔ **NÉ D'UN VISUEL QUI SORTAIT CASSÉ TOUS LES LUNDIS DEPUIS DES SEMAINES** :
  le titre « Rien à installer. C'est juste une page. » déclarait deux lignes,
  en rendait TROIS, et son dernier mot — « page. » — s'imprimait **sous** le
  paragraphe. Même défaut sur la démonstration du jeudi matin (« réservée. »).
  📌 **AUCUN DE NOS DEUX CONTRÔLES NE POUVAIT LE VOIR, ET POUR DEUX RAISONS
  DIFFÉRENTES.** `exigence.py` lit le CODE : il comptait deux lignes, et il
  disait vrai. `lignes.js` mesure le RENDU : il voyait bien trois lignes, et
  n'en concluait rien, parce qu'il examine chaque bloc **séparément**.
  ⛔ **LE DÉFAUT N'ÉTAIT DANS AUCUN BLOC : IL ÉTAIT ENTRE DEUX BLOCS.** Un
  contrôle qui n'examine que des éléments un par un ne trouvera jamais un défaut
  de RELATION, aussi rigoureux soit-il sur chacun. C'est la troisième famille de
  contrôle, et elle manquait : le code, le rendu, **et le rapport entre les
  choses**.
  ⚠️ Deux pièges appris en le calibrant, tous deux des FAUX POSITIFS qui
  accusaient nos meilleurs visuels :
  · **une boîte de ligne est plus haute que son encre** d'environ un quart de
    cadratin. Un recouvrement se juge donc en fraction du plus grand corps
    (seuil : 22 %), jamais en pixels absolus ;
  · **un texte incliné ne se mesure pas avec un rectangle droit.** Sur la
    pastille de prix, tournée de quelques degrés, les cadres alignés sur les
    axes se chevauchent forcément alors que rien ne se touche. L'outil détecte
    la rotation et **dit qu'il ne sait pas** plutôt que de conclure.
  📌 Un contrôle qui ne sait pas mesurer doit le DIRE. Un faux positif coûte
  plus cher qu'un silence : il apprend à ignorer l'alarme.

---

## 5 bis. CE QU'ON A REPRIS AUX CHARTES INTERNATIONALES

> Commande du patron, 02/09/2026 : « va regarder les règles d'Apple ou
> Coca-Cola, même si c'est très strict on les suit au détail près. Je veux une
> com de niveau international. **Mais garde nos règles.** »

Lues dans les **documents officiels**, pas dans des résumés de blog :
[Apple Identity Guidelines](https://www.apple.com/legal/sales-support/certification/docs/logo_guidelines.pdf)
(56 pages) et **Coca-Cola Brand Identity and Design Standards v1.0** (146 pages).
Quatre règles seulement ont été reprises — celles qui sont **chiffrées et donc
vérifiables par une machine**. Le reste est du droit de marque qui ne nous
concerne pas.

**1. La zone de respiration du logo = une FRACTION DU LOGO, jamais des pixels.**
> Apple, p. 10 : « *The minimum clear space around the signature is equal to
> one-half the height of the Apple logo […] Do not allow photos, typography, or
> other graphic elements to enter the minimum clear space area.* »
> Coca-Cola : la zone vaut la « **hyphen height** » — la hauteur du trait
> d'union entre « Coca » et « Cola ».

📌 **C'est le vrai coup de génie, et il est copiable tel quel** : dans les deux
chartes la zone n'est pas un nombre, c'est une proportion du logo lui-même. Elle
grandit et rétrécit avec lui, donc elle reste juste à toutes les tailles et
personne n'a jamais à la recalculer.
✅ Chez nous : emblème **68 px** → zone de **34 px**, et **rien** n'y entre.
🤖 Mesuré par `collision.js`. Il a trouvé l'infraction sur le flyer du lundi (7 px)
et sur le bulletin du soir (16 px), tous deux publiés depuis des semaines.

**2. Taille minimale du logo à l'écran : 35 px** (Apple, p. 11 — 8 mm en
impression, mesurés sur la hauteur du logo). On ne descend jamais en dessous.
🤖 `collision.js`.

**3. Un seul traitement de titre pour toute la marque — LES CAPITALES.**
> Coca-Cola, § 2.35 : « *Do not use any font other than Gotham Bold as the
> primary headline font* » + « *don't use lowercase-only typography for long
> headlines or sentences.* »
> Apple, p. 12 : « *Do not change the font or alter the spacing between
> letters.* »

⛔ **MESURÉ LE JOUR MÊME, ET LE RÉSULTAT FAIT MAL** : nos **cinq meilleurs**
visuels étaient en capitales à 100 %, dont celui noté 9/10 en relecture
extérieure. Les six autres étaient en minuscules — **y compris les deux que je
venais de réparer le matin même.** J'ai fabriqué l'incohérence en croyant
corriger.
📌 **ON NE JUGE PAS UN VISUEL TOUT SEUL : ON LE JUGE À CÔTÉ DES AUTRES.** Un
visuel peut passer tous les contrôles et abîmer quand même la marque, parce que
le défaut n'est pas dedans — il est dans l'écart avec ses voisins. C'est la même
leçon que la collision, d'un cran plus haut : après le code et le rendu, **la
cohérence de la collection**.
🤖 `exigence.py` § 2 : au moins 90 % de capitales dans `.acc`.

**4. Le logo n'est jamais seul, jamais recoloré, jamais sur un fond chargé.**
> Apple, p. 9-10 : signature en noir OU blanc uniquement, « *never place […] on
> a visually cluttered or patterned background* », et « *never use the Apple
> logo alone* ».

✅ Notre coin blanc fait déjà exactement ça : fond blanc plein, emblème +
« MoheliGo » toujours ensemble. C'était juste avant de le lire — on le garde,
et maintenant on sait **pourquoi** c'est juste.

⚠️ **CE QU'ON N'A PAS REPRIS, ET POURQUOI.** Apple interdit de poser du texte
sur une photo produit et de placer une photo sur un fond chargé (p. 30). Chez
nous le texte sur photo est la mise en page même — mais Apple parle de SES
photos produit dans les communications de SES revendeurs, un problème de droit
de marque, pas de lisibilité. **Une règle ne se copie pas parce qu'elle vient
d'une grande marque : elle se copie quand la raison qui l'a fait naître existe
aussi chez nous.** Le patron a dit « garde nos règles » — c'est ce filtre-là.

---

## 6. LE DESSIN

| Ce qui est fixe | Valeur | Vérifié par |
|---|---|---|
| marge de gauche | **76 px** | `exigence.py` |
| zone de respiration du logo | **½ de la hauteur de l'emblème** (34 px) | `collision.js` |
| taille mini de l'emblème à l'écran | **35 px** | `collision.js` |
| coin blanc en biais | **404 × 172**, `polygon(0 0, 100% 0, 78% 100%, 0 100%)` | `exigence.py` |
| vague dorée | **74 px**, **un seul tracé** | `mesure-marque.py` |
| part d'or dans le visuel | **8 – 15 %** | `mesure-marque.py` |
| contraste du texte courant | **≥ 4,5:1** (WCAG AA) | `exigence.py` |
| contraste du gros texte | **≥ 3,0:1** | `exigence.py` |
| format | **1080 × 1350**, rendu ×2 | `exigence.py` |

- **Une seule chose nette par visuel.** Deux points de fixation = aucun.
- **Aucune dimension recopiée à la main.** Le 29/08, un voile à 614 px sur une
  photo à 620 px a dessiné un trait clair sur toute la hauteur. Deux valeurs qui
  doivent être égales se calculent, ne se retapent pas.
- **Un fond « presque » de la bonne couleur est pire qu'un fond franchement
  différent** : l'œil ne voit pas une nuance, il voit une frontière.

---

## 7. CE QUI INTERDIT LA PUBLICATION — sans discussion

1. un **chiffre non mesuré** ou une promesse que le service ne tient pas ;
2. l'**image d'une personne** sans son accord écrit (et jamais l'écran d'un
   téléphone montrant un tiers) ;
3. une **date gravée dans le visuel** — un post reste sur la page pour toujours,
   et une date passée fait croire que le service est mort. Ce qui porte une date
   se **regénère** avant chaque publication, jamais ne se garde ;
4. un **fait opérationnel lu dans le code** et non confirmé par le patron —
   moyens de paiement, prix, lignes ouvertes, horaires, délais. Le dépôt dit ce
   qui a été prévu, pas ce qui marche (manuel § 12.2 quater) ;
6. 🚩 **une image qui porte des MOTS, et un texte qui ne les reprend pas
   exactement.** Une image écrite est une SOURCE : la contredire, même par
   imprécision, est une erreur de fait, pas de style.
   *Né le 29/08 :* l'écharpe du lauréat dit « YOUNG LEADER · OCÉAN INDIEN ·
   2025-2026 ». J'avais écrit « Young Leader Mohéli distingue ceux qui font
   avancer l'île » — **rabaissant sa distinction d'un niveau régional à un
   niveau local, sur un visuel censé lui rendre hommage.** Le patron l'a vu en
   une seconde. Depuis : quand l'image parle, on la cite.
   *Recommencé le 01/09*, sur la même association et en quatre jours : le carton
   de fin de la vidéo présentait le lauréat comme « **Comité** Young Leader
   Mohéli 2026 » alors que son écharpe dit « YOUNG LEADER · MOHÉLI · 2026 ».
   Le patron : « c'est le vrai Young Leader. »
   *Et le 01/09 au soir, la vraie leçon arrive* : « on a un partenariat avec
   Young Leader **Mohéli**, pas Océan Indien. » Le visuel entier est retiré.
   Je m'étais demandé si le lauréat était mohélien ; la bonne question était
   ailleurs. **Un accord porte sur une organisation précise, pas sur une famille
   de noms qui se ressemblent** — et avant de mettre l'image d'une personne sur
   un visuel, on vérifie qu'elle entre dans le PÉRIMÈTRE de l'accord, pas
   seulement qu'un accord existe.
   *Et le 01/09 au soir, la même faute une TROISIÈME fois en quatre jours* :
   j'avais titré un visuel « PARTENARIAT · YOUNG LEADER MOHÉLI » sur la photo
   d'un jeune homme. Le patron : « lui c'est pas un Young Leader, c'est un jeune
   de Mohéli. » Il m'avait dit la veille que notre partenariat était avec Young
   Leader Mohéli, puis, au message suivant, « utilise celui-ci » — et j'ai lu la
   seconde phrase comme la RÉPONSE à la première. Elle ne l'était pas : il me
   donnait une photo, pas une identité.
   ⛔ **UNE APPARTENANCE NE SE DÉDUIT JAMAIS DU CONTEXTE. Elle se dit, ou elle
   ne s'écrit pas.** Trois fois de suite, j'ai comblé un trou d'information avec
   ce qui était plausible autour. Le remède n'est pas « faire plus attention » :
   c'est que **le visuel ne doit rien affirmer sur la personne qu'il montre**
   tant que la phrase exacte n'a pas été donnée. Un visage peut être le VISAGE
   d'une idée sans être un CAS NOMMÉ — et c'est aussi ce qui protège sa vie
   privée.
   📌 **DEUX FOIS LA MÊME FAUTE, C'EST UN RÉFLEXE À CORRIGER, PAS UN ACCIDENT :**
   quand un visuel nomme une personne, son titre ne s'écrit pas de mémoire ni par
   déduction — **il se relit sur l'image, ou il se demande.** Une organisation et
   une personne ne portent jamais le même nom : le logo cite l'organisation, la
   ligne de crédit cite la personne.
7. un visuel **non regardé à l'œil** après rendu. Nos contrôles savent dire
   « le fichier est là » ; ils ne savent pas dire « l'image est juste ».

---

## 8. LA MÉTHODE QUAND UN DÉFAUT EST SIGNALÉ

Le patron signale souvent un défaut **sans dire où**. Trois fois sur trois le
29/08, la bonne méthode n'a pas été de scruter l'image :

> **On trace le profil de pixels et on cherche la marche.**
> Le trait vertical a été localisé en une commande : le rouge passait de 15 à 55
> puis revenait à 15, **en six pixels**, à x = 460.

Le 30/08, la même commande a trouvé un défaut que **personne n'avait signalé** :
le rouge passait de 15 à 114 en un pixel au bord haut de la photo — une épaule
tranchée à plat. 📌 **Le profil de pixels ne sert pas qu'à retrouver un défaut
qu'on vous montre ; il en trouve qu'on ne vous montre pas.** À passer sur les
quatre bords de chaque photo détourée, avant de dire qu'un visuel est fini.

⚠️ **ET LA SONDE NE DOIT PAS MODIFIER CE QU'ELLE MESURE.** Le 30/08, un outil
qui entourait chaque mot d'un `<span>` pour lire sa position a annoncé « 3
lignes, ligne veuve » sur un titre qui en fait deux : `.acc span` est en
`display:block`, ses propres spans avaient cassé la mise en page. **Une mesure
qui déplace son sujet ne mesure rien.** On lit avec des `Range`, jamais en
réécrivant la page.

Et pour ses remarques de fond, la règle posée le 29/08 tient trois fois :
**quand un relecteur signale une incohérence, on ne discute pas — on mesure.**
La mesure a toujours trouvé **plus** que la remarque.
