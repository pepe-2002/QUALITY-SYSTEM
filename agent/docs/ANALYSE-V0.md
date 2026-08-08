# Analyse de la spécification et architecture V0

> Livrable demandé par la spec §22, points 1 à 4. Rédigé **avant** le code,
> corrigé **après** la mise au point en conditions réelles.

---

## 1. Ce que demande la spécification

La spec décrit un **agent**, pas un chatbot. La différence tient en une phrase :
l'agent décide *quoi faire* avant de répondre, utilise des outils, vérifie son
travail, et sait s'arrêter. Sept exigences structurent tout le reste :

| # | Exigence | Où elle se traduit dans le code |
|---|---|---|
| §1 | Orchestrateur qui choisit l'agent | `ara/agents/orchestrator.py` |
| §4 | Calcul proportionné à la tâche | `ara/core/complexity.py` |
| §13 | Outils indépendants | `ara/tools/` + `registry.py` |
| §15 | Confirmation humaine | `ara/core/permissions.py` |
| §16 | Aucune permission implicite | liste blanche `ARA_ALLOWED_TOOLS` |
| §17 | Journal reproductible, sans pensée privée | `ara/core/journal.py` |
| §19 | Rien de payant obligatoire | `ara/providers/` |

---

## 2. Réalisable sans le moindre coût

Tout le MVP. Vérifié, pas supposé :

| Fonction | Moyen retenu | Coût |
|---|---|---|
| Interface mobile | PWA servie par `http.server` | 0 |
| Serveur + temps réel | bibliothèque standard + SSE | 0 |
| Recherche web | DuckDuckGo (HTML public) + API Wikipédia | 0 |
| Extraction de texte | `html.parser` de la bibliothèque standard | 0 |
| Synthèse | moteur **extractif** intégré | 0 |
| Synthèse rédigée | Ollama en local | 0 (matériel de l'utilisateur) |
| PDF | ReportLab, sinon moteur de repli intégré | 0 |
| DOCX | OOXML écrit avec `zipfile` | 0 |
| MD / TXT | bibliothèque standard | 0 |
| Historique + journal | JSON / JSONL sur disque | 0 |
| Tests | pytest, corpus figé, sans réseau | 0 |

**Le choix structurant** : zéro dépendance obligatoire. Ni `requests`, ni
`fastapi`, ni `python-docx`. Motif : le prototype doit s'installer sur un
téléphone Android via Termux, où chaque paquet à compiler est un échec
probable. `pip install reportlab` reste conseillé, jamais requis.

**Le compromis assumé** : sans LLM, la synthèse est *extractive* — elle
sélectionne et cite des phrases des sources, elle n'en rédige pas. C'est
honnête et vérifiable (un test s'assure que chaque phrase rendue existe
mot pour mot dans une source), mais ce n'est pas de la rédaction. L'interface
le dit à l'utilisateur au lieu de le laisser croire le contraire.

---

## 3. Ce qui exige une ressource externe

| Fonction | Pourquoi | Traitement |
|---|---|---|
| Synthèse **rédigée** de qualité | aucun LLM gratuit distant fiable | Ollama en local (gratuit) ou clé d'API |
| Génération d'**images** par IA | pas d'équivalent gratuit et local simple | outil déclaré, refuse de s'exécuter, explique |
| Recherche à fort volume | quotas des moteurs publics | SearXNG auto-hébergé, ou clé |
| OCR, transcription audio | hors périmètre Phase 1 | non implémenté |

Règle appliquée partout : **rien ne s'active tout seul**. Un fournisseur
indisponible ne fait pas échouer la tâche — le système bascule sur le moteur
gratuit et affiche : « Cette fonction nécessite une ressource externe », suivi
de ce qui manque exactement.

---

## 4. Architecture V0

```
        TÉLÉPHONE (PWA)
              │  HTTP + Server-Sent Events
        ┌─────▼─────────────────────────────────┐
        │  api/server.py    service.py          │  tâches en arrière-plan
        └─────┬─────────────────────────────────┘  historique sur disque
              │
        ┌─────▼─────────────────────────────────┐
        │  ORCHESTRATEUR                        │
        │  planner → gather → analyse →         │
        │  document_agent → vérification        │
        └──┬────────────┬───────────┬───────────┘
           │            │           │
     ┌─────▼────┐ ┌─────▼─────┐ ┌───▼──────────┐
     │ OUTILS   │ │FOURNISSEURS│ │ SOCLE        │
     │ registre │ │ LLM        │ │ permissions  │
     │ + garde  │ │ recherche  │ │ journal      │
     │          │ │ stockage   │ │ complexité   │
     └──────────┘ └────────────┘ └──────────────┘
```

Trois principes :

1. **Un seul passage obligé pour les outils.** Aucun agent n'appelle une
   fonction d'outil directement ; tout passe par `ToolBox.call()`, qui vérifie
   la permission, demande confirmation si l'action est sensible, journalise et
   convertit toute exception en erreur maîtrisée.
2. **Les fournisseurs sont interchangeables.** Changer de LLM ou de moteur de
   recherche est une variable d'environnement, pas une modification de code.
3. **Le contexte de tâche est isolé.** Une tâche = un `TaskContext` = un
   dossier. C'est ce qui rendra le RESEARCH LAB (Phase 4) capable de rejouer
   la même tâche avec des réglages différents.

---

## 5. Ce que la mise au point réelle a corrigé

Le MVP a été lancé contre le vrai web, pas seulement contre le corpus de test.
Quatre défauts sont apparus, chacun corrigé **et** couvert par un test :

| Défaut observé | Cause | Correction |
|---|---|---|
| Requêtes du type « … et fais-moi un PDF » envoyées aux moteurs | la consigne était confondue avec le sujet | `subject()` retire verbes d'instruction et noms de livrables |
| Un article sur l'Algérie retenu comme source sur les Comores | mots communs (« entre », « grande », « pdf » du menu Wikipédia) | filtre de pertinence sur le sujet seul, seuil proportionnel |
| Même page comptée deux fois (`?lang=fr`) | dédoublonnage sur l'URL brute | `canonical()` ignore les paramètres cosmétiques |
| Réponses 429 des moteurs | requêtes enchaînées sans pause | temporisation + réessai avec retrait progressif |

C'est le point important de cette V0 : les corrections viennent de
l'observation, pas de l'intuition.

---

## 6. Phase 2 — la boucle adaptative

### Le choix structurant : comparer suppose du comparable

Du texte brut ne se compare pas. Pour qu'une machine puisse **constater** que
deux sources se contredisent, il lui faut des grandeurs : prix, durées,
distances, pourcentages. `ara/analysis/facts.py` les extrait avec leur
voisinage immédiat ; `compare.py` les confronte ; `coverage.py` recense ce qui
manque. Le tout est **déterministe** : la détection ne dépend pas du LLM, donc
elle reste reproductible — condition nécessaire au LAB de la Phase 4.

### Ce que la mise au point réelle a encore corrigé

Six défauts, tous observés en lançant l'agent contre le vrai web, tous corrigés
et couverts par un test :

| Défaut observé | Cause | Correction |
|---|---|---|
| Aucune relance possible | le cycle 1 dépensait tout le budget | dépense incrémentale (2 requêtes au départ) |
| 29 fausses contradictions | prix d'hôtel comparé au prix d'un billet | recentrage sur les mots-clés de la question |
| 14 fausses contradictions | pages d'un même site comparées entre elles | deux pages d'un site ≠ deux sources |
| « 6 m d'antenne ≠ 330 m de tour » | valeurs d'ordres de grandeur différents | rapport max de 5 entre valeurs comparables |
| « 312 m ≠ 125 m » sur une même page | contexte = phrase entière, trop large | contexte = 6 mots autour du chiffre |
| 10 sources, 1 seul domaine | rien n'était réellement croisé | quota par domaine + manque « diversité » |

Le point important reste le même qu'en Phase 1 : ces règles viennent de
l'observation, pas de l'intuition. Chacune a un test qui échoue si on la retire.

### Ce qui borne la boucle

Quatre limites indépendantes, pour qu'aucune question ne puisse faire tourner
l'agent indéfiniment :

- `MAX_RESEARCH_STEPS` — plafond dur de recherches (10 par défaut) ;
- `MAX_CYCLES` — plafond de cycles (4) ;
- un désaccord n'est cherché **qu'une fois** : s'il persiste, chercher plus ne
  le résoudra pas ;
- le temps maximal de tâche.

L'agent nomme toujours la limite qui l'a arrêté.

---

## 7. Phase 4 — le laboratoire, ou l'art de se contredire soi-même

### Ce que la phase devait faire

Les phases 1 à 3 reposent sur une affirmation jamais vérifiée : *un agent qui
décide lui-même quand chercher répond mieux qu'un agent à budget fixe.* La
spec §18 dit quoi en faire — « le système doit chercher à réfuter l'hypothèse,
pas à la confirmer ». La Phase 4 construit donc un banc d'essai dont le but
avoué est de **faire tomber** le travail des trois premières.

### Le choix structurant : geler le web

Une mesure n'a de valeur que si elle est reproductible. Le vrai web ne l'est
pas : les pages changent, les moteurs limitent, l'ordre des résultats varie.
`lab/corpus.py` contient donc un **web figé** — un ensemble de pages écrites à
la main, servies par un faux moteur de recherche. `frozen_network()` remplace
le client HTTP le temps de l'expérience : aucune requête ne sort.

Conséquence : deux exécutions du même banc donnent le même chiffre, et deux
stratégies sont comparées **sur les mêmes pages** (comparaison appariée). Sans
cela, on mesurerait la météo du web, pas la stratégie.

### Les quatre bras, et pourquoi ils ne diffèrent que d'une chose

| Bras | Décision de chercher |
|---|---|
| `MODEL ONLY` | ne cherche jamais — témoin bas |
| `FIXED` | budget constant, 3 recherches, quelle que soit la question |
| `ADAPTIVE` | budget variable selon la difficulté estimée |
| `ADAPTIVE + RESEARCH` | recherche **uniquement lorsque nécessaire**, avec relances ciblées sur les manques |

Le moteur de synthèse est **le même partout**. Si les bras différaient aussi
par leur rédaction, on ne saurait pas ce que mesure l'écart.

### Comment l'exactitude est mesurée sans juge humain

Chaque tâche porte une vérité de référence **chiffrée** (`dataset.py` :
15 000 FC, 3 heures, 70 km, 7 h du matin…). La réponse produite est passée dans
l'extracteur de faits de la Phase 2, et on regarde si la bonne valeur y est.
Aucune appréciation, aucun jugement de style : un nombre est là ou il n'y est
pas.

Le jeu contient trois familles, et la troisième est la plus importante :
`facile` (une recherche suffit), `profond` (il faut relancer), et surtout
`piege` — trois tâches où chercher davantage ramène une archive de 2019, le
prix d'une autre liaison, ou trois prix sur la même page. **Elles sont là
exprès pour faire perdre la stratégie adaptative.** Un banc d'essai qu'on ne
peut pas perdre ne mesure rien.

À l'exactitude s'ajoute le **bruit** : une valeur piège présentée comme la
réponse. La note retenue est *nette* = exactitude − ½ bruit — répondre faux
coûte, ce n'est pas neutre.

### Les conditions de réfutation, écrites avant

Inscrites dans `experiment.py` **avant** la première exécution :

- gain d'exactitude nette < +0,05 → hypothèse réfutée ;
- coût > 1,5× la référence → réfutée ;
- dégradation sur les tâches pièges → réfutée ;
- p > 0,05 au test des signes → non concluant.

Le verdict ne prononce jamais « confirmée » : au mieux « non réfutée ». Un test
le vérifie littéralement (`test_le_verdict_ne_dit_jamais_confirmee`).

### Le résultat, tel quel

| Stratégie | Exactitude | Bruit | Nette | Qualité | Recherches | Jetons |
|---|---|---|---|---|---|---|
| MODEL ONLY | 0.00 | 0.00 | 0.00 | 0.75 | 0.0 | 106 |
| FIXED REASONING | 0.62 | 0.12 | 0.62 | 0.84 | 3.0 | 213 |
| ADAPTIVE REASONING | 0.62 | 0.12 | 0.62 | 0.84 | 1.5 | 213 |
| ADAPTIVE RESEARCH | 0.75 | 0.12 | 0.75 | 0.91 | 2.4 | 294 |

**Verdict principal : NON CONCLUANT.** 1 victoire, 0 défaite, 7 égalités ; gain
moyen +0,125, mais p = 1,000 au test des signes et l'intervalle de confiance à
95 % — [+0,000 ; +0,375] — contient zéro. Aucune condition de réfutation n'est
remplie, mais la preuve manque : huit tâches ne suffisent pas.

**Verdict secondaire : NON RÉFUTÉE.** `ADAPTIVE` obtient exactement la même
exactitude nette que `FIXED` avec **moitié moins de recherches**. C'est le seul
résultat net de la phase, et ce n'est pas celui qu'on cherchait : l'adaptation
n'a pas démontré qu'elle rend plus juste, elle a montré qu'elle rend moins cher.

Le rapport complet, régénérable par `python -m ara.cli --lab`, est écrit dans
`workspace/lab-report.md` et se termine par une section « ce que cette
expérience ne prouve pas ».

### Ce que le banc a réellement rapporté : quatre bugs

L'apport le plus solide de la phase n'est pas son verdict, c'est ce qu'elle a
trouvé en chemin. Quatre défauts du système **de production**, invisibles
jusque-là :

| Défaut trouvé par le banc | Cause | Correction |
|---|---|---|
| « À quelle heure **part** le bateau ? » déclenchait une recherche de pourcentage | « part » était un mot déclencheur de l'aspect *proportion* | mot retiré des déclencheurs (`coverage.py`) |
| « 7 h du matin » lu comme une durée de 7 heures | un seul motif pour l'heure et la durée | motif `_TIME` dédié, extrait en premier, ses positions consommées |
| Deux prix, l'un daté de 2019, l'autre non : contradiction annoncée | le validateur n'examinait que le cas où **les deux** sources sont datées | règle « une seule source datée, écart ≥ 2 ans → écart d'ancienneté » |
| La boucle relançait une recherche sans motif | les requêtes de réserve étaient consommées même sans manque constaté | relance seulement pour une raison nommée ; sinon arrêt explicite |

### Divulgation — pourquoi cette exécution n'est pas confirmatoire

Ces quatre corrections ont été faites **après** avoir vu les résultats du banc.
Le protocole était pré-enregistré, mais le système mesuré a changé entre-temps.
Cette exécution est donc **exploratoire**, pas confirmatoire : elle a servi à
trouver des défauts, ce qu'un banc d'essai fait très bien, et non à trancher
l'hypothèse, ce qu'elle ne peut plus faire honnêtement.

Ce qui n'a **pas** été fait, et qui aurait été la façon simple de sauver
l'hypothèse : déplacer les seuils de réfutation après coup. Ils sont restés à
+0,05 et 1,5×. Une vraie confirmation demanderait un corpus neuf, plus grand,
écrit par quelqu'un d'autre, sur un système désormais figé.

---

## 8. H2 — l'adaptation économise-t-elle vraiment des recherches ?

### Pourquoi une seconde hypothèse

H1 est restée **non concluante**, et le reste : elle n'est ni révisée, ni
reformulée, ni repêchée. Mais son échec disait quelque chose d'utile — l'effet
cherché (« l'adaptation répond mieux ») était peut-être trop petit pour huit
tâches. H2 porte sur une affirmation différente, plus mesurable :

> H2 — À exactitude comparable, ADAPTIVE REASONING réduit significativement le
> nombre de recherches nécessaires par rapport à FIXED.

Elle a l'avantage d'être réfutable pour de bon : il suffit que la réduction
n'existe pas, ou qu'elle se paie en exactitude.

### Ce que la Phase 4 avait de faible, et que H2 corrige

| Faiblesse de H1 | Correction |
|---|---|
| Un seul jeu, et il avait servi à corriger le système | Deux jeux : calibration (brûlé) et **test tenu à l'écart**, autre domaine, aucune page commune |
| Une seule exécution, déterministe | **5 graines** : la formulation de la question et l'ordre des résultats varient, jamais les faits |
| « Non concluant » sans dire *pourquoi* l'agent s'arrête | Taxonomie des **raisons d'arrêt**, instrumentée dans le système lui-même |
| Aucune analyse des erreurs | Taxonomie des **erreurs** : arrêt trop tôt, recherche inutile, suffisance mal jugée, contradiction manquée ou signalée à tort |
| Coût en jetons seulement | Recherches, pages, **appels LLM**, jetons, latence, **coût estimé**, **recherches par réponse correcte** |

Deux points de méthode méritent d'être dits :

- **L'unité statistique est la tâche, pas le couple tâche×graine.** Cinq
  graines d'une même tâche ne sont pas cinq observations indépendantes ; les
  compter comme telles ferait baisser la p-valeur sans rien prouver. L'analyse
  par couple est donnée à part, étiquetée *pseudo-réplication*.
- **Les critères sont écrits avant l'expérience**, et le commit qui les
  contient précède celui des résultats. L'antériorité est vérifiable dans
  l'historique Git, elle ne repose pas sur ma parole.

Critères pré-enregistrés :

- **A — exactitude comparable** : borne basse de l'IC95 de l'écart d'exactitude
  nette ≥ −0,05 (non-infériorité) ;
- **B — réduction significative** : ≥ 20 % de recherches en moins **et**
  p < 0,05 au test des signes apparié ;
- SOUTENUE = A et B · PARTIELLEMENT SOUTENUE = B sans A · RÉFUTÉE = B non
  vérifié.

### Le résultat, sur le jeu de test tenu à l'écart

| Stratégie | Exactitude | Nette | Recherches | Appels LLM | Jetons | Rech./réponse juste |
|---|---|---|---|---|---|---|
| MODEL ONLY | 0.00 | 0.00 | 0.00 | 1.00 | 109 | — |
| FIXED REASONING | 0.78 | 0.73 | 3.00 | 2.00 | 228 | 3.85 |
| ADAPTIVE REASONING | 0.74 | 0.69 | 1.32 | 1.16 | 214 | **1.78** |
| ADAPTIVE RESEARCH | 0.78 | 0.73 | 2.54 | 1.16 | 319 | 3.26 |

**H2 PARTIELLEMENT SOUTENUE.**

- **B vérifié** : 56 % de recherches en moins (écart moyen −1,68 par tâche,
  IC95 [−1,92 ; −1,44]), 10 tâches sur 10 moins chères, p = 0,002.
- **A non vérifié** : la borne basse de l'IC95 de l'écart d'exactitude
  (−0,120) descend sous la marge de −0,05. L'exactitude n'est pas comparable.

### Ce que l'analyse des arrêts et des erreurs a révélé

L'économie est réelle mais **elle n'est pas sélective** :

| Famille | Recherches ADAPTIVE | Recherches FIXED | Exactitude ADAPTIVE | Exactitude FIXED |
|---|---|---|---|---|
| facile | 1.40 | 3.00 | 0.80 | 0.80 |
| profond | 1.00 | 3.00 | **0.80** | **1.00** |
| piège | 1.40 | 3.00 | 0.54 | 0.54 |

Le contrôleur coupe **autant sur les tâches profondes que sur les faciles** —
davantage, même. Il ne détecte donc pas la difficulté : il rationne partout.
C'est précisément là que le critère A tombe, sur les tâches profondes, où
FIXED trouve ce qu'ADAPTIVE manque.

C'est un résultat négatif utile, et il contredit ce que la conception
annonçait. La première version de la section « pourquoi ADAPTIVE cherche
moins » affirmait que le contrôleur *maintient* le budget sur les tâches
difficiles. Les mesures disent l'inverse ; c'est la version conforme aux
mesures qui a été gardée.

Les erreurs relevées après coup complètent le tableau : sur le jeu de test,
FIXED lance **64 recherches au-delà du minimum** qui suffisait à trouver la
bonne réponse, contre 0 pour ADAPTIVE. Une bonne part de l'économie consiste
simplement à ne pas les faire.

Enfin, la mesure la plus dure — **recherches par réponse correcte**, qui punit
immédiatement une stratégie qui économise en se trompant — reste à l'avantage
d'ADAPTIVE : 1,78 contre 3,85.

### Ce qui n'a pas été fait pour sauver l'hypothèse

- Le contrôleur n'a **pas** été ajusté après la calibration, alors que celle-ci
  montrait déjà le critère A à la limite (IC95 [−0,075 ; 0,000]). Régler le
  système pour faire passer un critère qu'on vient de voir échouer est
  exactement ce que le pré-enregistrement sert à empêcher.
- Les seuils (−0,05 et 20 %) n'ont pas bougé.
- H1 n'a pas été retouchée.

### Divulgation — un effet de bord de l'instrumentation

Ajouter les codes d'arrêt a modifié une **phrase** du rapport de recherche
(l'agent annonçait « aucun manque » alors qu'un manque subsistait ; il dit
maintenant ce qui manque). Cette phrase fait partie de la réponse rendue, donc
le nombre de jetons d'ADAPTIVE RESEARCH augmente légèrement : le coût relatif
de H1 passe de 1,38× à **1,48×**, toujours sous la limite de 1,5× annoncée.
Exactitude, recherches, verdict de H1 : identiques.

### Ce que H2 ne prouve pas

- Le jeu de test est écrit par l'auteur du système : séparation calibration /
  test, **pas** réplication indépendante.
- Les graines varient la formulation et le classement, pas le contenu du web.
- Une réduction de recherches n'est un gain que si les recherches coûtent. Sur
  un moteur gratuit et rapide, l'économie reste théorique.

---

## 9. ADAPTIVE-V2 — corriger le défaut que H2 avait mis au jour

### Le défaut

H2 avait montré, chiffres à l'appui, que le contrôleur ne distingue pas une
tâche facile d'une tâche profonde : il rationne uniformément. Économie réelle,
exactitude perdue là où il aurait fallu chercher.

### Ce qui a été gelé avant de toucher à quoi que ce soit

- **ADAPTIVE-V1 est figée définitivement.** Les quatre bras de H1 et H2
  épinglent explicitement `v1` (`CONTROLLER_BY_STRATEGY`) : faire avancer le
  contrôleur ne peut plus rendre ces expériences irreproductibles. Vérifié
  après coup : H1 et H2 rejoués donnent exactement les mêmes chiffres.
- **Le contrôleur par défaut de l'application reste V1.** On adopte une version
  après l'expérience qui la juge, pas avant.

### Les trois jeux, trois rôles

| Jeu | Fichier | Rôle |
|---|---|---|
| 1 | `lab/dataset.py` | développement et calibration |
| 2 | `lab/heldout.py` | première validation — résultats observés, V2 conçue à partir de là |
| 3 | `lab/heldout2.py` | **jamais utilisé auparavant**, porte seul le verdict |

### La logique de V2

1. **Estimer la difficulté avant de chercher** (`estimate_difficulty`), sur des
   caractéristiques de la seule question :
   - la **grandeur demandée** — un horaire officiel ou un taux statistique est
     publié à un seul endroit, un prix courant est répété partout ;
   - l'**exigence d'autorité** — « officiel », « exact », « règlement » ;
   - l'**ampleur** — comparaison, plusieurs grandeurs, propositions enchaînées ;
   - la **longueur**, qui ne pèse plus qu'un peu : croire qu'une question courte
     est une question facile était précisément l'erreur de V1.
2. **Trois niveaux, trois budgets** : simple → 1, intermédiaire → 3, profonde
   → 6 recherches, toujours plafonnés.
3. **Réviser sur preuve** : grandeur introuvable → le budget monte ; grandeur
   trouvée → arrêt anticipé ; doute → on ne touche à rien.

L'estimateur ne voit **jamais** le corpus, ni un résultat de recherche, ni la
vérité de référence. Trois tests le vérifient — un contrôleur qui donnerait un
gros budget aux questions dont il connaît la réponse aurait d'excellents
chiffres et aucune valeur.

### Les garde-fous demandés

| Risque | Mécanisme |
|---|---|
| Arrêt prématuré sur tâche difficile | l'arrêt anticipé exige que la grandeur demandée ait été **trouvée**, pas seulement que des pages soient revenues |
| Recherche inutile sur tâche facile | dès que c'est trouvé, la collecte s'arrête |
| Dépassement du budget maximal | `min(…, max_search_steps)` à chaque allocation et à chaque montée |
| Boucle infinie | `MAX_REVISIONS` révisions au plus, une seule requête de repli par tâche |

### Le résultat, sur le jeu 3

| Stratégie | Exactitude | Nette | Recherches | Appels LLM | Jetons | Rech./réponse juste |
|---|---|---|---|---|---|---|
| FIXED | 0.82 | 0.79 | 3.00 | 2.00 | 176 | 3.66 |
| ADAPTIVE-V1 | 0.82 | 0.80 | 1.00 | 1.00 | 172 | **1.22** |
| ADAPTIVE-V2 | **0.90** | **0.88** | 1.46 | 1.24 | 179 | 1.62 |

Par famille — c'est là que le défaut se lit :

| Stratégie | facile | profond | piège | écart profond − facile |
|---|---|---|---|---|
| FIXED | 3.00 / 1.00 | 3.00 / 0.53 | 3.00 / 0.77 | +0.00 |
| ADAPTIVE-V1 | 1.00 / 1.00 | 1.00 / 0.53 | 1.00 / 0.80 | **+0.00** |
| ADAPTIVE-V2 | 1.25 / 1.00 | 2.07 / 0.67 | 1.13 / 0.93 | **+0.82** |

*(recherches / exactitude nette)*

**Verdict : DÉFAUT CORRIGÉ** — les trois critères pré-enregistrés sont vérifiés.

- **C1** : sur les tâches profondes, V2 obtient 0,67 d'exactitude nette contre
  0,53 pour FIXED, et alloue +0,82 recherche de plus au profond qu'au facile
  (seuil : +0,50). Elle distingue enfin les deux.
- **C2** : 51 % de recherches en moins que FIXED (seuil : 20 %).
- **C3** : 0,88 contre 0,80 pour V1 — pas de régression, un gain.

Et les erreurs, qui disent la même chose autrement : **0 arrêt prématuré** pour
V2 contre 4 pour V1 ; 5 recherches gaspillées contre 82 pour FIXED.

### Ce que cela ne prouve pas

- **V2 n'est pas une preuve de H2.** H2 reste *partiellement soutenue*, H1
  *non concluante*. Corriger un défaut n'est pas valider une hypothèse.
- Le classement des grandeurs par difficulté (`ASPECT_DIFFICULTY`) a été formé
  en lisant les jeux 1 et 2. Il ne dépend d'aucune valeur d'or, mais il n'est
  pas tombé du ciel non plus.
- Les trois jeux sont écrits par l'auteur du système.
- Toute amélioration ultérieure de V2 devra faire l'objet d'une **nouvelle**
  expérience, sur un jeu encore jamais utilisé. Le jeu 3 est brûlé.

### Adoption

Sur décision du propriétaire du projet, **V2 devient le contrôleur de
l'application** (`DEFAULT_CONTROLLER = "v2"`). Trois conséquences, toutes
vérifiées :

- V1 n'est pas supprimée : elle reste figée, et le laboratoire épingle
  explicitement la version de chaque bras. H1 et H2 rejoués après l'adoption
  donnent les mêmes chiffres au bit près.
- Deux tests ont dû changer d'énoncé, non parce qu'ils échouaient à tort mais
  parce que leur prémisse ne tenait plus : la question « combien coûte la
  traversée ? » n'est plus sur-estimée par le contrôleur, il n'y a donc plus
  rien à réduire. Le test de réduction de budget porte désormais sur une
  question que V2 sur-estime réellement (« tarif **officiel** »), et le test de
  temporisation réseau épingle V1 pour garantir deux requêtes.
- Réserve inchangée et assumée : la validation porte sur dix tâches d'un seul
  corpus, écrites par l'auteur du système. C'est une décision de produit
  appuyée sur une mesure, pas une preuve.

### Une correction d'affichage, pas de contrôleur

Après la première exécution, le tableau des raisons d'arrêt affichait « passe
unique » pour V2, alors qu'elle prend bel et bien des décisions d'arrêt : le
code d'arrêt n'était renseigné que par la boucle de recherche complète. Seul
l'enregistrement a été corrigé — la logique de V2 n'a pas bougé, et les
chiffres de la ré-exécution sont identiques au bit près.

---

## 10. RESEARCH-V2 — pertinence des sources

### Le défaut, trouvé en lançant l'agent en vrai

Question posée au vrai web : « quel est le tarif officiel de la traversée en
vedette entre la Grande Comore et Mohéli ? ». L'agent a répondu en citant les
**Vedettes de Bréhat** et les **Vedettes de l'Odet** — des traversées
bretonnes. Trois causes, toutes générales :

| # | Défaut | Ce qu'on voyait |
|---|---|---|
| 1 | requête finissant sur une préposition, complément dupliqué | « …en vedette **entre** tarif officiel » |
| 2 | mot générique isolé promu en complément de requête | « …entre **grande** », « …entre **comore** » |
| 3 | pertinence purement lexicale | « traversée + vedette + tarif » suffisait à retenir une page bretonne |

### Le choix : une version séparée, pas une correction

Corriger `research.py` aurait rendu H1 et H2 irreproductibles — les chiffres
publiés ne correspondraient plus au code. Le moteur est donc **gelé**, et
`research_v2.py` vit à côté avec son propre identifiant. Le seul point de
contact est un paramètre `relevance=None` ajouté au collecteur : à `None`, le
comportement de la baseline est inchangé, et un test le verrouille.

### Les corrections, toutes générales

- `compose_query` — nettoie les mots grammaticaux en bord de fragment et
  n'ajoute au sujet que des mots **nouveaux** ;
- `is_orphan` — un complément d'un seul mot générique n'oriente rien et est
  écarté ; une requête garde toujours le sujet nettoyé ;
- `distinctive_terms` / `is_on_topic` — une source doit contenir au moins un
  terme qui **identifie** le sujet (nom propre, ou mot rare à défaut), et non
  seulement des mots qui le décrivent. Les qualificatifs génériques —
  « grande », « saint », « nord » — ne comptent pas comme identité.

**Aucune liste noire.** Un test parcourt l'arbre syntaxique du module et vérifie
qu'aucun nom de site ni de lieu n'apparaît dans ses données ou ses
identifiants — seulement dans la prose qui explique le défaut.

### Le jeu 4, adversarial

Quatrième corpus, jamais utilisé, sans lien avec les trois autres. Ses pièges
ne sont pas des chiffres trompeurs mais des pages qui *ressemblent* à la
réponse : autre pays au même vocabulaire, nom voisin, vocabulaire générique,
archive périmée, même lieu dans un autre contexte. Chaque page est étiquetée,
ce qui permet de compter les faux positifs par nature.

### Résultats

| Moteur | Exactitude | Précision des sources | Faux positifs | Mauvais lieux | Recherches | Temps | Jetons |
|---|---|---|---|---|---|---|---|
| RESEARCH-BASELINE | 0.25 | 56 % | 2.65 | 1.55 | 2.70 | 8 ms | 614 |
| RESEARCH-V2 | 0.25 | **66 %** | **1.65** | **0.95** | 2.25 | 7 ms | 540 |

Faux positifs par nature de piège, sur l'ensemble des exécutions :

| Moteur | autre pays | nom voisin | générique | périmé | autre contexte |
|---|---|---|---|---|---|
| BASELINE | 12 | 19 | 7 | 15 | 0 |
| V2 | **0** | 19 | **0** | 14 | 0 |

Lecture honnête : V2 élimine complètement deux formes de faux positifs — les
pages d'un autre lieu au même vocabulaire, et les pages purement génériques.
Elle ne change **rien** aux deux autres, et c'était prévisible :

- les **noms voisins** demanderaient un référentiel géographique ;
- le **hors-période** n'est pas l'affaire du filtre de pertinence : une
  archive parle bien du sujet, c'est sa date qui doit être lue — travail de
  l'agent contexte.

Ces deux limites ont chacune un test qui **fige le comportement actuel**,
pour qu'elles restent visibles plutôt que d'être oubliées.

L'exactitude, elle, ne bouge pas : 0,25 pour les deux. De meilleures sources
n'ont pas donné de meilleures réponses sur ce jeu — le moteur de synthèse
extractif reste le facteur limitant. Le résultat est conservé tel quel.

### Adoption

Sur décision du propriétaire du projet, **RESEARCH-V2 devient le moteur de
l'application** (`agents/engines.py`, `DEFAULT_ENGINE = "v2"`).

- La baseline n'est pas supprimée : elle reste joignable, et le laboratoire la
  nomme explicitement pour chaque bras. H1 rejoué après l'adoption donne les
  mêmes chiffres, verdict compris. Un test vérifie qu'aucun module du
  laboratoire n'emprunte le moteur par défaut.
- `ARA_RESEARCH_ENGINE=baseline` revient au moteur gelé sans modifier une
  ligne de code.
- Vérification en conditions réelles, sur la question même qui avait déraillé :
  3 sources retenues (moheligo.com, comorese.com, comorosmayottetours.com),
  **2 écartées hors sujet**, un seul cycle, aucune requête malformée. Faute de
  trouver un prix, l'agent le dit — au lieu de servir le tarif d'un autre pays.

### Ce que cette expérience ne prouve pas

- Quatre tâches, un domaine, un corpus écrit par l'auteur du système.
- Aucun résultat de H1 ou H2 n'a servi à calibrer cette version, et aucun n'a
  été modifié : les expériences rejouées donnent les mêmes chiffres.
- Deux formes de faux positifs sur cinq résistent, et resteront visibles tant
  que leurs tests les figent.

---

## 11. Limites connues

À lire avant d'en attendre plus que le système ne donne :

- **Toute l'analyse est lexicale.** Elle voit deux prix incompatibles ; elle ne
  comprend pas qu'une page date de 2019 et l'autre de 2026, ni que « 312 m » et
  « 330 m » désignent la même tour avant et après son antenne. Sur un sujet
  encyclopédique riche, des alertes discutables subsistent. C'est précisément
  ce qu'un vrai LLM sait faire — et c'est pourquoi l'abstraction existe.
- **Seuls les faits chiffrés sont confrontés.** Deux sources qui se
  contredisent en prose passent inaperçues.
- **Le contrôleur de complexité est mesuré, mais non démontré.** La Phase 4 lui
  a donné toutes ses chances d'être réfuté ; il ne l'a pas été, mais il n'a pas
  non plus prouvé qu'il rend les réponses plus justes (p = 1,000 sur huit
  tâches). Ce qu'on peut en dire aujourd'hui : à exactitude égale, il dépense
  deux fois moins.
- **Le laboratoire mesure son propre corpus.** Huit tâches et un web écrits par
  l'auteur du système : cela peut réfuter une hypothèse, pas l'établir. Et la
  dernière exécution est exploratoire, le système ayant été corrigé après avoir
  vu les résultats (§7).
- **Le filtre de pertinence est lexical.** Il écarte le hors-sujet grossier ;
  il ne détecte ni la source douteuse, ni la date périmée.
- **Aucun envoi de fichier depuis le téléphone.** « Analyse ce document »
  n'est pas encore possible.
