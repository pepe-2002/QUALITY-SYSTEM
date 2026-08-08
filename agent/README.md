# ARA — Autonomous Research & Creative Agent

**v0.7 — Phases 1 à 5, ADAPTIVE-V2 · RESEARCH-V2**

Un agent personnel qui **cherche → comprend → planifie → utilise des outils →
crée → vérifie → s'arrête**. Il se pilote depuis un téléphone, tourne sans
aucune clé d'API, et n'annonce jamais un fichier qu'il n'a pas réussi à
rouvrir.

Ce n'est pas un chatbot : avant de répondre, il décide s'il doit chercher,
combien de recherches il s'autorise, quels outils il a le droit d'appeler et
quels fichiers produire.

---

## Ce qui fonctionne aujourd'hui

| | |
|---|---|
| **Interface** | PWA installable sur Android, pipeline affiché en direct |
| **Recherche** | boucle adaptative : cherche, analyse, **relance si ça manque** |
| **Budget** | difficulté estimée **avant** de chercher, révisée sur preuve (V2) |
| **Comparaison** | confronte les sources, **détecte les contradictions chiffrées** |
| **Analyse** | synthèse citée `[S1] [S2]`, recoupements et manques explicites |
| **Validation** | un **agent contexte** tranche : vraie contradiction ou écart explicable |
| **Création** | 3 concepts de flyer, critiqués sur 12 critères, améliorés, notés |
| **QR code** | encodé en Python pur et **relu** avant d'être posé |
| **Marque** | `brand_profile.json` : couleurs, ton, et surtout les interdits |
| **Vérification** | la réponse est contrôlée (citations, chiffres non sourcés) |
| **Documents** | PDF, DOCX, Markdown, TXT — **vérifiés avant livraison** |
| **Historique** | conservé sur disque, survit au redémarrage |
| **Journal** | une entrée reproductible par tâche (spec §17) |
| **Sécurité** | liste blanche d'outils, confirmation des actions sensibles |
| **Laboratoire** | banc d'essai qui **tente de réfuter** le raisonnement adaptatif |
| **Téléphone** | notification, presse-papier, voix, partage Android (Termux) |
| **Routines** | tâches programmées : « chaque matin », « chaque lundi à 8h » |
| **Coût** | 0 € — aucune dépendance obligatoire, aucune clé requise |

Le pipeline visible à l'écran est exactement celui qui s'exécute :

```
TÂCHE → RECHERCHE → ANALYSE → CRÉATION → VÉRIFICATION → RÉSULTAT
          ↑____________|
       relance ciblée si une information manque
       ou si deux sources se contredisent
```

Une étape inutile est **sautée** : « bonjour » ne déclenche ni recherche ni
fichier. Et le budget de recherche est un plafond, pas une dépense obligatoire :
si le premier cycle répond à tout, l'agent s'arrête et **réduit** son budget.

## La boucle de recherche (Phase 2)

À chaque cycle, l'agent extrait les **faits chiffrés** des pages lues — prix,
durées, distances, pourcentages — les ramène à une unité commune, puis les
confronte. Il relance une recherche seulement s'il a une raison précise :

| Raison de relancer | Exemple |
|---|---|
| Aspect non couvert | on demande un prix, aucune source n'en donne un |
| Mot-clé absent | « Mohéli » n'apparaît dans aucune page lue |
| Aucun recoupement | toutes les sources viennent du même site |
| Valeur non confirmée | un seul site avance ce tarif |
| **Contradiction** | 15 000 FC d'un côté, 45 000 FC de l'autre |

Et il s'arrête toujours en disant pourquoi : plus rien ne manque, budget
épuisé, plus aucune piste, ou plafond de cycles atteint.

Trois garde-fous évitent les fausses alertes, tous issus d'essais réels :

- une valeur comprise dans une fourchette annoncée ailleurs **confirme**, elle
  ne contredit pas ;
- deux pages d'un **même site** ne sont pas deux sources indépendantes ;
- deux valeurs séparées d'un facteur 5 mesurent autre chose (6 m d'antenne
  contre 330 m de tour), elles ne se contredisent pas.

### Deux étages de détection

Le détecteur déterministe est réglé pour le **rappel** : il propose tous les
écarts chiffrés. Un **agent contexte** dispose ensuite :

```
Données brutes → détection déterministe → anomalie → agent contexte
→ « est-ce une vraie contradiction ? » → validation
```

Il rejette ce qui s'explique (deux époques, deux variantes, une valeur
approchée), confirme ce qui ne s'explique pas, et laisse « à vérifier » ce
qu'il ne sait pas trancher. Sans vrai LLM, il s'abstient plutôt que d'inventer.

## Le studio créatif (Phase 3)

```
Brief marketing → recherche du marché → analyse des concurrents
→ 3 concepts → critique automatique → amélioration → version finale
```

Le studio réutilise la boucle de recherche : les arguments du flyer sont ceux
que **plusieurs sources ont confirmés**, pas des slogans inventés.

- **Trois concepts** systématiquement, jamais un seul jet : bandeau, plein
  cadre, colonne. Chacun est noté, le meilleur est retenu.
- **Douze critères mesurés** — contraste WCAG, hiérarchie, alignement,
  équilibre, espace négatif, collisions… Chaque faiblesse produit une
  correction *applicable*, pas un commentaire.
- **Retour arrière** : si une correction fait baisser la note, l'agent dit
  « version précédente meilleure » et revient en arrière (spec §11).
- **QR code encodé en Python pur**, puis **relu** comme le ferait un lecteur
  avant d'être posé. Toujours sombre sur clair, sinon les téléphones ne le
  scannent pas.
- **Mémoire de marque** (`brand_profile.json`) : couleurs, ton, dimensions, et
  surtout les **interdits** — « pas d'emojis », « le départ est Ouroveni ».
  Un interdit violé est un défaut bloquant, pas une remarque.

Les créations sortent en **SVG** : zéro dépendance, imprimable sans perte, et
surtout *mesurable* — c'est ce qui permet au critique de noter la géométrie
plutôt que de donner un avis.

## Le laboratoire (Phase 4)

Les phases 1 à 3 affirment qu'un agent qui décide **quand** chercher répond
mieux qu'un agent à budget fixe. Ce n'était qu'une affirmation. La phase 4 la
met à l'épreuve — et **cherche à la faire tomber**, conformément à la spec §18.

```bash
python -m ara.cli --lab      # écrit workspace/lab-report.md
```

Le protocole, écrit **avant** de regarder le moindre résultat :

- **corpus figé** — un web en dur, identique pour toutes les stratégies et
  toutes les exécutions ; les comparaisons sont appariées (même tâche, même
  pages) ;
- **quatre stratégies**, un seul moteur de synthèse : seule la décision de
  chercher change. `MODEL ONLY` (aucune recherche), `FIXED` (budget constant),
  `ADAPTIVE` (budget variable selon la difficulté), `ADAPTIVE + RESEARCH`
  (recherche uniquement lorsque nécessaire, avec relances ciblées) ;
- **exactitude mesurée par machine** contre une vérité de référence chiffrée —
  aucun jugement humain dans la boucle ;
- **des tâches pièges exprès**, où chercher plus ramène une archive périmée ou
  le prix d'une autre liaison. Elles existent pour donner à l'hypothèse une
  chance d'être réfutée ;
- **conditions de réfutation pré-enregistrées** : gain < +0,05, ou coût
  > 1,5×, ou dégradation sur les pièges → hypothèse réfutée.

Résultat de l'exécution actuelle :

| Stratégie | Exactitude | Bruit | Nette | Recherches | Jetons |
|---|---|---|---|---|---|
| MODEL ONLY | 0.00 | 0.00 | **0.00** | 0.0 | 106 |
| FIXED REASONING | 0.62 | 0.12 | **0.62** | 3.0 | 213 |
| ADAPTIVE REASONING | 0.62 | 0.12 | **0.62** | 1.5 | 213 |
| ADAPTIVE RESEARCH | 0.75 | 0.12 | **0.75** | 2.4 | 315 |

**Verdict : non concluant.** 1 victoire, 0 défaite, 7 égalités ; gain +0,125
mais p = 1,000 et l'intervalle de confiance [+0,000 ; +0,375] contient zéro.
Le jeu d'essai est trop petit pour trancher. Le rapport dit « non réfutée »,
jamais « confirmée » — et le verdict n'a été lu qu'après coup, sans toucher
aux seuils.

Un résultat annexe, lui, est net : à exactitude **égale**, la stratégie
adaptative dépense **deux fois moins de recherches** que la stratégie fixe.
C'est la seconde hypothèse, et elle n'est pas réfutée.

Le banc a surtout servi à autre chose : il a **trouvé quatre défauts** dans le
système de production (voir `docs/ANALYSE-V0.md`). C'est probablement son
apport le plus solide à ce stade.

### H2 — l'adaptation économise-t-elle des recherches ?

H1 reste non concluante. Une seconde hypothèse, plus mesurable, a été
pré-enregistrée puis testée sur un **jeu tenu à l'écart** :

> À exactitude comparable, ADAPTIVE REASONING réduit significativement le
> nombre de recherches nécessaires par rapport à FIXED.

```bash
python -m ara.cli --h2      # écrit workspace/h2-report.md
```

Protocole renforcé par rapport à H1 : deux jeux séparés (calibration brûlée /
test d'un autre domaine, jamais vu), **5 graines** qui font varier la
formulation des questions et l'ordre des résultats, l'unité statistique restée
la **tâche** (moyenner les graines évite la pseudo-réplication), critères
écrits avant — et le commit qui les contient précède celui des résultats.

| Stratégie (jeu de test) | Exactitude | Recherches | Appels LLM | Rech./réponse juste |
|---|---|---|---|---|
| FIXED REASONING | 0.78 | 3.00 | 2.00 | 3.85 |
| ADAPTIVE REASONING | 0.74 | **1.32** | 1.16 | **1.78** |

**Verdict : H2 PARTIELLEMENT SOUTENUE.** La réduction est là et elle est
franche — 56 % de recherches en moins, 10 tâches sur 10, p = 0,002. Mais le
critère d'exactitude comparable **échoue** (IC95 de l'écart [−0,120 ; 0,000],
sous la marge de −0,05).

L'analyse par famille dit pourquoi, et ce n'est pas ce qui était espéré : le
contrôleur coupe **autant sur les tâches profondes que sur les faciles**. Il
ne lit pas la difficulté, il rationne partout — et c'est sur les tâches
profondes qu'il perd. Le contrôleur n'a pas été retouché après coup : les
seuils et le code sont restés gelés.

### ADAPTIVE-V2 — le défaut est corrigé

Ce défaut a ensuite été corrigé, dans une version **séparée**. V1 est gelée
définitivement (elle reste la baseline de H1 et H2, qui rejoués donnent les
mêmes chiffres au bit près) ; V2 estime la difficulté **avant** de choisir son
budget, puis le révise sur preuve.

```bash
python -m ara.cli --v2      # écrit workspace/v2-report.md
```

Jeu 3 — un troisième corpus, jamais utilisé auparavant :

| Stratégie | Exactitude | Recherches | facile | profond | écart |
|---|---|---|---|---|---|
| FIXED | 0.82 | 3.00 | 3.00 | 3.00 | +0.00 |
| ADAPTIVE-V1 | 0.82 | 1.00 | 1.00 | 1.00 | **+0.00** |
| ADAPTIVE-V2 | **0.90** | 1.46 | 1.25 | 2.07 | **+0.82** |

**Verdict : DÉFAUT CORRIGÉ** — les trois critères pré-enregistrés passent.
V2 dépense enfin *plus* sur les questions profondes que sur les faciles, garde
51 % d'économie face à FIXED, et ne régresse pas face à V1. Zéro arrêt
prématuré, contre 4 pour V1.

Ce n'est **pas** une preuve de H2 : corriger un défaut n'est pas valider une
hypothèse, et le rapport le dit en première ligne.

**V2 est désormais le contrôleur de l'application** (décision du propriétaire
du projet, prise après l'expérience). Concrètement :

```
Question → estimateur de difficulté → simple : 1 recherche
                                      intermédiaire : 3
                                      profonde : 6
              ↓ après chaque recherche
        grandeur demandée trouvée ?  ── oui ──→ arrêt, budget rendu
                                     └─ non ──→ le budget monte
```

V1 n'est pas supprimée : elle reste figée et reste la baseline de H1 et H2,
que le laboratoire épingle explicitement. Les deux expériences rejouées après
l'adoption donnent les mêmes chiffres au bit près.

### RESEARCH-V2 — les sources hors sujet

Lancé sur le vrai web, l'agent a répondu à « tarif officiel de la traversée
Grande Comore ↔ Mohéli » en citant les **Vedettes de Bréhat**. Trois défauts :
requêtes finissant sur une préposition (« …en vedette **entre** tarif
officiel »), mots génériques promus en requêtes (« …entre **grande** »), et un
filtre de pertinence purement lexical (« traversée + vedette + tarif » suffisait).

Le moteur de H1/H2 est **gelé** ; la correction vit dans `research_v2.py`.

```bash
python -m ara.cli --research    # jeu 4 adversarial, écrit workspace/research-report.md
```

| Moteur | Précision des sources | Faux positifs | Mauvais lieux |
|---|---|---|---|
| RESEARCH-BASELINE | 56 % | 2.65 | 1.55 |
| RESEARCH-V2 | **66 %** | **1.65** | **0.95** |

V2 élimine **complètement** deux formes de faux positifs (autre pays au même
vocabulaire, pages purement génériques) et ne change rien aux deux autres —
noms voisins et archives périmées, qui demandent respectivement un référentiel
géographique et une lecture de date. Ces limites ont chacune un test qui les
fige plutôt que de les taire. L'exactitude, elle, ne bouge pas : de meilleures
sources n'ont pas donné de meilleures réponses sur ce jeu.

Aucune liste noire : un test vérifie qu'aucun nom de site ou de lieu
n'apparaît dans le code du filtre.

**RESEARCH-V2 est désormais le moteur de l'application.** Rejouée en vrai, la
question qui avait déraillé donne maintenant :

```
[RECHERCHE] 3 source(s) sur 3 domaine(s) · 2 écartée(s) hors sujet · 1 cycle(s)
            arrêt : il manque encore quelque chose (aucune donnée chiffrée pour
            « prix »), mais aucune relance exploitable
Sources : moheligo.com · comorese.com · comorosmayottetours.com
```

Plus une seule source bretonne, aucune requête malformée — et quand il ne
trouve pas le prix, **il le dit** au lieu de servir celui d'un autre pays.

`ARA_RESEARCH_ENGINE=baseline` revient au moteur gelé sans toucher au code.

### Où l'agent perd-il l'information ?

Une réponse fausse ne dit pas quoi corriger. Chaque échec est donc rangé à
l'étape du pipeline où l'information s'est perdue :

```bash
python -m ara.cli --diagnostic    # écrit workspace/diagnostic-report.md
```

| Étape | Signification |
|---|---|
| RECHERCHE | mauvaise source trouvée |
| EXTRACTION | bonne information présente mais mal extraite |
| CONTEXTUALISATION | bonne information mais mauvais lieu, date ou contexte |
| COMPARAISON | sources correctes mais mal confrontées |
| RAISONNEMENT | informations correctes mais conclusion incorrecte |
| GÉNÉRATION | conclusion correcte mais réponse finale incorrecte |

L'attribution suit l'ordre du pipeline et s'arrête à la **première** étape
fautive — une information jamais trouvée ne peut pas être mal extraite.

État des lieux de la configuration adoptée, sur les quatre jeux
(160 exécutions, **64 % de réponses correctes**) :

| Étape | Pannes | Part |
|---|---|---|
| RECHERCHE | 36 | 63 % |
| CONTEXTUALISATION | 11 | 19 % |
| EXTRACTION | 10 | 18 % |

Deux enseignements, tous deux utiles :

- la recherche reste la panne dominante — c'est là qu'il faut porter l'effort,
  pas sur la rédaction ;
- les 10 pannes d'extraction viennent **toutes** du jeu 4, où les prix sont
  écrits en « francs » sans devise précisée : l'extracteur ne connaît que
  « francs comoriens », « euros », « dollars », « ariary ». Le diagnostic a
  donc trouvé un défaut réel en une exécution.

### EXTRACTION-V2 — la devise n'est jamais devinée

Le diagnostic avait montré qu'un montant écrit « 3 200 francs » n'était pas vu
du tout. La correction n'est pas de décréter que « francs » vaut la devise du
projet : un agent qui comparerait des francs comoriens à des francs CFA
produirait des contradictions imaginaires.

```bash
python -m ara.cli --extraction    # écrit workspace/extraction-report.md
```

| Niveau de confiance | Quand | Exemple |
|---|---|---|
| `certaine` | la devise est écrite | « 15 000 francs comoriens » |
| `probable` | le contexte ne laisse qu'une possibilité | « À Dakar, 25 000 francs » |
| `inconnue` | rien ne permet de trancher | « Prix : 900 francs » |

**Règle de sécurité : dans le doute, le montant est gardé et la devise marquée
`UNKNOWN`.** Une marque de conversion (« soit », « contre », « ≈ ») annule la
déduction — la devise écrite appartient alors à l'autre montant.

Jeu 6, indépendant, 20 cas jamais utilisés :

| Mesure | extracteur gelé | EXTRACTION-V2 |
|---|---|---|
| Montants extraits | 7/20 (35 %) | **20/20 (100 %)** |
| Devises correctes | 100 % | **100 %** |
| Fausses identifications | 0 | **0** |
| Faux positifs | 0 | **0** |

Et sur le système entier, le diagnostic rejoué : **64 % → 69 %** de réponses
correctes, pannes d'extraction **10 → 0**. Mais cinq pannes se sont
**déplacées** vers la contextualisation (11 → 16) : des montants jusque-là
invisibles sont maintenant lus, et certains sont les valeurs pièges. La
correction déplace une partie du problème vers l'aval.

### FINAL_ANSWER_ACCURACY

Une métrique **séparée** qui ne note que ce que l'utilisateur lit : tout ce qui
suit un marqueur de trace est retiré avant notation. Elle attrape trois pannes
que la métrique historique laissait passer — information cachée dans les
traces, « je n'ai pas trouvé » alors que la valeur était connue, valeur fausse
affichée pendant que la bonne dormait dans les logs.

Elle **ne réécrit pas** H1 ni H2, qui gardent la leur ; un test vérifie que les
deux divergent sur le même cas, ce qui échouerait si on les « harmonisait ».

### CONTEXT-V2 — l'information est-elle bien du sujet ?

L'autopsie des 16 erreurs de contextualisation donne un fait décisif :
**dans les 16 cas, la bonne valeur était disponible**. Le système ne manquait
pas d'information — il en avait trop, et servait la mauvaise.

| Cause | Cas |
|---|---|
| **Temps** — archive prise pour l'actuelle | 9 |
| **Objet** — autre bien ou service | 3 |
| **Géographie** — autre lieu / nom voisin | 2 + 2 |

```bash
python -m ara.cli --context    # écrit workspace/context-report.md
```

Quatre états, deux seulement autorisent l'affirmation : `MATCH` et
`PROBABLE_MATCH` oui ; `CONTEXT_UNKNOWN` et `MISMATCH` **jamais**. Rien n'est
jeté pour autant — le filtre rend deux paniers, et chaque blocage porte sa
raison.

Jeu 7, indépendant, 15 cas, neuf familles de pièges :

| Mesure | sans contrôle | CONTEXT-V2 |
|---|---|---|
| Bonnes informations conservées | 5/5 | **5/5** |
| Mauvaises rejetées | 0/10 | **6/10** |
| Faux rejets | 0 | **0** |
| Exactitude | 33 % | **73 %** |

Quatre pièges passent encore, dont trois pour la même raison : le contrôle
d'objet se contente d'**un** terme partagé — « école » suffit à rattacher un
violon à une question sur une guitare. Chacun a un test qui fige le
comportement actuel. Le corriger demandera une version suivante et un jeu neuf.

**Mesuré, pas adopté** : CONTEXT-V2 n'est branché sur aucune version en
production.

### CONTEXT-V3 — jugée sur le jeu 8

V3 pèse les termes au lieu de les compter, traite un objet concurrent comme un
désaveu, et distingue deux noms composés qui partagent leur tête.

| Version | Bonnes conservées | Mauvaises rejetées | Faux rejets | Exactitude |
|---|---|---|---|---|
| sans contrôle | 8/8 | 0/10 | 0 | 44 % |
| CONTEXT-V2 | 8/8 | 6/10 | 0 | 78 % |
| **CONTEXT-V3** | 7/8 | **10/10** | **1** | **94 %** |

V3 rejette **tous** les pièges, homonymie de lieux comprise. Mais elle
introduit un défaut que V2 n'avait pas : une source qui **abrège** un nom
(« Villeneuve » pour « Villeneuve-sur-Loire ») est prise pour une
contradiction, et une information correcte est rejetée.

Le jeu 8 avait été écrit pour attraper exactement ce risque — il l'a attrapé.
Le faux rejet n'est pas corrigé : ce sera CONTEXT-V4 sur un jeu 9.

### L'effet réel, qui renverse la conclusion

Mesuré sur les **vraies exécutions** de l'agent (jeux 1 à 4), pas sur des
phrases écrites pour le mécanisme :

| Version | Pièges bloqués | Bonnes valeurs bloquées **à tort** |
|---|---|---|
| CONTEXT-V2 | 10/22 (46 %) | 12/125 (10 %) |
| CONTEXT-V3 | 15/22 (68 %) | 31/125 (**25 %**) |

**V3, à 94 % sur son propre jeu, bloquerait un quart des bonnes réponses en
production.** L'adopter sur la foi du jeu 8 aurait été une erreur.

L'écart s'explique : les phrases des jeux 7 et 8 sont *autoportantes* — elles
nomment le lieu, l'objet et la période. Les vraies pages ne le font pas. « La
franchise bagages est fixée à 20 kilogrammes par passager » ne répète ni le
lieu ni le service, et V3 y voit un défaut d'ancrage.

**Ni V2 ni V3 ne sont adoptables en l'état.** Un mécanisme utilisable devra
distinguer « la phrase ne répète pas le contexte » de « la phrase parle
d'autre chose ».

## Le téléphone et les routines (Phase 5)

L'agent sort de l'écran : il peut **prévenir**, **partager**, **parler**, et
surtout **revenir tout seul** à heure fixe.

```bash
python -m ara.cli --phone                              # ce que ce téléphone sait faire
python -m ara.cli --add-routine "chaque matin" "Vérifie les tarifs des traversées"
ARA_AUTOMATION=1 python -m ara.cli --serve             # …et les routines tournent
```

| Capacité | Commande Termux | Autorisation |
|---|---|---|
| Notification | `termux-notification` | liste blanche |
| État batterie / Wi-Fi | `termux-battery-status` | liste blanche |
| Presse-papier | `termux-clipboard-set` | liste blanche |
| Lecture à voix haute | `termux-tts-speak` | liste blanche |
| **Partage d'un fichier** | `termux-share` | **hors liste blanche + confirmation** |

Trois décisions valent d'être dites :

- **Pas d'envoi de SMS.** C'est la seule capacité qui engage le propriétaire
  auprès d'un tiers sans qu'il voie ce qui part. `termux-share` passe au
  contraire par le sélecteur d'Android : le destinataire est choisi par
  l'humain, dans son application, hors de portée de l'agent.
- **Liste blanche fermée et aucun shell.** Seules huit commandes `termux-*`
  sont exécutables, les arguments partent en liste — un `;` glissé dans un
  titre de notification ne s'exécute pas.
- **Une routine n'a aucun droit de plus qu'une demande tapée à la main.** Elle
  emprunte le même orchestrateur, la même liste blanche, les mêmes
  confirmations. Une action sensible programmée à 3 h du matin échoue
  proprement au lieu de passer en douce.

Une routine ne naît **que d'un horaire compris**. « De temps en temps » est
refusé avec des exemples — deviner ferait tourner l'agent quand personne ne
l'attend. Et chaque exécution est bornée : plafond quotidien, batterie
minimale, jamais deux fois en parallèle, suspension automatique après trois
échecs consécutifs — en disant lequel.

L'ordonnanceur **ne rattrape pas** ce qu'il a manqué : téléphone éteint à 7 h,
la routine attend le lendemain plutôt que de partir en rafale au réveil.

Installation sur téléphone : `deploy/termux/install.sh`, et
`deploy/termux/boot-ara.sh` pour un démarrage automatique via Termux:Boot.
Rien ne tourne en arrière-plan tant que `ARA_AUTOMATION=1` n'est pas posé.

---

## Démarrage rapide

```bash
cd agent
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt      # optionnel : PDF soigné + tests
python -m ara.cli --serve
```

Puis ouvrez `http://<ip-de-la-machine>:8800`.

Sans rien installer du tout :

```bash
python3 -m ara.cli --serve            # fonctionne, PDF en mode simplifié
```

En ligne de commande :

```bash
python3 -m ara.cli "Recherche les tarifs des traversées aux Comores et fais-moi un PDF"
```

---

## Depuis un téléphone

### Option A — le serveur tourne sur un ordinateur du même Wi-Fi

1. Sur l'ordinateur : `python3 -m ara.cli --serve`
2. Relevez son adresse locale : `hostname -I` (Linux) ou `ipconfig` (Windows).
3. Sur le téléphone, ouvrez `http://192.168.x.x:8800`.
4. Menu Chrome → **Ajouter à l'écran d'accueil**. L'application s'installe et
   se lance comme une vraie application.

### Option B — tout sur le téléphone (Termux, hors ligne possible)

```bash
pkg install python git
git clone <ce-depot> && cd QUALITY-SYSTEM/agent
python -m ara.cli --serve
```

Puis ouvrez `http://127.0.0.1:8800` dans Chrome. Aucune dépendance à
installer : c'est la raison pour laquelle le projet n'utilise que la
bibliothèque standard.

> **Hors du réseau domestique**, définissez un jeton :
> `export ARA_TOKEN=une-phrase-longue`, puis ouvrez
> `http://…:8800/?token=une-phrase-longue`. Toutes les routes `/api/` le
> réclament alors.

---

## Configurer un vrai modèle de langage

Par défaut, ARA utilise un moteur **extractif** : il sélectionne et cite des
phrases des sources, sans rien reformuler. C'est gratuit, vérifiable et
déterministe — mais ce n'est pas de la rédaction, et l'interface le dit.

Pour une vraie synthèse, gratuitement, en local :

```bash
# https://ollama.com
ollama pull llama3.2
export ARA_LLM_PROVIDER=ollama
```

Ou avec un service distant (clé dans `.env`, **jamais** dans le code) :

```bash
cp .env.example .env    # puis renseignez ARA_OPENAI_API_KEY ou ARA_ANTHROPIC_API_KEY
export ARA_LLM_PROVIDER=openai_compat   # ou anthropic
```

Si le fournisseur demandé n'est pas disponible, ARA **ne l'active pas de
force** : il retombe sur le moteur gratuit et affiche pourquoi.

---

## Sécurité

- Aucune clé n'est stockée dans le code ni dans l'objet de configuration —
  uniquement en variables d'environnement, lues à l'usage.
- **Un outil qui existe n'est pas un outil autorisé.** La liste blanche
  (`ARA_ALLOWED_TOOLS`) décide ; le reste est refusé.
- Les actions sensibles (suppression, publication, envoi, achat) exigent une
  confirmation humaine explicite avant exécution.
- Les fichiers d'une tâche sont confinés dans son dossier ; les remontées de
  répertoire sont neutralisées.
- Le client HTTP refuse les adresses locales et privées (garde-fou SSRF).
- Le journal ne contient **aucune chaîne de pensée privée** : uniquement des
  résumés opérationnels et de quoi reproduire la tâche.

---

## Tests

```bash
python -m pytest
```

603 tests, hors ligne, déterministes (corpus figé, réseau coupé). Ils couvrent
la recherche, l'extraction, les citations, la boucle adaptative (relance,
arrêt, budget), la détection **et la validation** des contradictions, l'encodeur
QR (aller-retour + comparaison à une bibliothèque de référence), les concepts,
les douze critères du critique, le retour arrière de la boucle créative, la
**vérification** PDF/DOCX/SVG/MD/TXT, les permissions, la confirmation humaine,
les réessais réseau et la gestion des erreurs.

Le laboratoire est testé comme le reste — y compris sur ce qu'il a le droit de
conclure : un test vérifie que le verdict ne prononce **jamais** le mot
« confirmée », d'autres qu'un gain insuffisant ou une dégradation sur les
tâches pièges réfutent bien l'hypothèse.

---

## Structure

```
agent/
├── ara/
│   ├── core/          config, erreurs, permissions, journal, complexité, HTTP
│   ├── analysis/      faits chiffrés, contradictions, manques, vérification
│   ├── providers/     LLM · recherche · stockage  (interchangeables)
│   ├── tools/         outils indépendants + registre à permissions
│   ├── design/        marque, QR, composition SVG, concepts, critique, studio
│   ├── documents/     modèle commun → PDF, DOCX, MD, TXT + vérification
│   ├── agents/        planificateur, collecte, research agent, documents
│   ├── lab/           corpus figé, stratégies, mesures, expérience, rapport
│   ├── android/       pont Termux : détection, liste blanche de commandes
│   ├── automation/    horaires, routines, ordonnanceur
│   ├── api/           serveur HTTP + PWA (static/)
│   ├── service.py     tâches en arrière-plan et historique
│   └── cli.py         ligne de commande
├── tests/             603 tests hors ligne
└── docs/ANALYSE-V0.md analyse de la spec, choix techniques, limites
```

---

## Feuille de route

| Phase | Contenu | État |
|---|---|---|
| **1** | Interface mobile · LLM · recherche · fichiers · PDF · historique | **fait** |
| **2** | Research Agent : boucle adaptative, contradictions, relances | **fait** |
| **3** | Creative Agent + Design Critic : flyers, QR code, itérations notées | **fait** |
| **4** | Research Lab : mesurer et **tenter de réfuter** le raisonnement adaptatif | **fait** |
| **5** | Automatisation Android : capacités du téléphone, routines programmées | **fait** |

**Limites connues** — à lire avant d'en attendre trop :

- La détection de contradictions est **lexicale**. Elle voit deux prix
  incompatibles ; elle ne comprend pas qu'une page parle de 2019 et l'autre de
  2026. Sur un sujet encyclopédique riche, elle produit encore des alertes
  discutables.
- Le contrôleur de complexité est désormais **mesuré**. V1 économise beaucoup
  (−56 % de recherches, H2) mais ne détecte pas la difficulté ; V2 la détecte
  (écart +0,82 recherche entre profond et facile sur le jeu 3) et gagne en
  exactitude. H1, sur le gain d'exactitude, reste non concluante — et V2 n'y
  change rien : c'est une correction de défaut, pas une validation.
- **Les deux V2 sont adoptées alors que leur validation reste étroite** : dix
  tâches pour le contrôleur, quatre pour le moteur de recherche, sur des
  corpus écrits par l'auteur du système. Ce sont des décisions de produit
  appuyées sur des mesures, pas des preuves — le prochain jeu de test devra
  être écrit par quelqu'un d'autre pour valoir mieux.
- **Deux faux positifs sur cinq résistent** à RESEARCH-V2 : les lieux qui
  partagent un nom (il faudrait un référentiel géographique) et les archives
  périmées (c'est une lecture de date, pas de pertinence).
- Le laboratoire mesure **son propre corpus**. Un web figé de huit tâches
  écrites par l'auteur du système ne remplace pas le vrai web : il sert à
  réfuter, pas à décerner un satisfecit.
- Seuls les faits **chiffrés** sont comparés. Deux sources qui se contredisent
  en prose passent inaperçues.
- Pas d'envoi de fichier depuis le téléphone : « analyse ce document » n'est
  pas encore possible.

Détail et journal des corrections dans
[`docs/ANALYSE-V0.md`](docs/ANALYSE-V0.md).
