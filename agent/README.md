# ARA — Autonomous Research & Creative Agent

**v0.5 — Phases 1 à 5**

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

445 tests, hors ligne, déterministes (corpus figé, réseau coupé). Ils couvrent
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
├── tests/             445 tests hors ligne
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
- Le contrôleur de complexité est désormais **mesuré**, et le résultat n'est
  pas celui qu'on visait : il économise beaucoup de recherches (−56 % sur le
  jeu de test, H2), mais il **ne détecte pas la difficulté** — il coupe autant
  sur les questions profondes que sur les faciles, et y perd en exactitude.
  H1, sur le gain d'exactitude, reste non concluante.
- Le laboratoire mesure **son propre corpus**. Un web figé de huit tâches
  écrites par l'auteur du système ne remplace pas le vrai web : il sert à
  réfuter, pas à décerner un satisfecit.
- Seuls les faits **chiffrés** sont comparés. Deux sources qui se contredisent
  en prose passent inaperçues.
- Pas d'envoi de fichier depuis le téléphone : « analyse ce document » n'est
  pas encore possible.

Détail et journal des corrections dans
[`docs/ANALYSE-V0.md`](docs/ANALYSE-V0.md).
