# ARA — Autonomous Research & Creative Agent

**v0.3 — Phases 1 à 3**

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

320 tests, hors ligne, déterministes (corpus figé, réseau coupé). Ils couvrent
la recherche, l'extraction, les citations, la boucle adaptative (relance,
arrêt, budget), la détection **et la validation** des contradictions, l'encodeur
QR (aller-retour + comparaison à une bibliothèque de référence), les concepts,
les douze critères du critique, le retour arrière de la boucle créative, la
**vérification** PDF/DOCX/SVG/MD/TXT, les permissions, la confirmation humaine,
les réessais réseau et la gestion des erreurs.

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
│   ├── api/           serveur HTTP + PWA (static/)
│   ├── service.py     tâches en arrière-plan et historique
│   └── cli.py         ligne de commande
├── tests/             320 tests hors ligne
└── docs/ANALYSE-V0.md analyse de la spec, choix techniques, limites
```

---

## Feuille de route

| Phase | Contenu | État |
|---|---|---|
| **1** | Interface mobile · LLM · recherche · fichiers · PDF · historique | **fait** |
| **2** | Research Agent : boucle adaptative, contradictions, relances | **fait** |
| **3** | Creative Agent + Design Critic : flyers, QR code, itérations notées | **fait** |
| 4 | Research Lab : mesurer et **tenter de réfuter** le raisonnement adaptatif | à venir |
| 5 | Automatisation Android | à venir |

**Limites connues** — à lire avant d'en attendre trop :

- La détection de contradictions est **lexicale**. Elle voit deux prix
  incompatibles ; elle ne comprend pas qu'une page parle de 2019 et l'autre de
  2026. Sur un sujet encyclopédique riche, elle produit encore des alertes
  discutables.
- Le contrôleur de complexité n'est toujours **pas validé empiriquement**.
  C'est le travail de la Phase 4 : essayer de le réfuter, pas de le confirmer.
- Seuls les faits **chiffrés** sont comparés. Deux sources qui se contredisent
  en prose passent inaperçues.
- Pas d'envoi de fichier depuis le téléphone : « analyse ce document » n'est
  pas encore possible.

Détail et journal des corrections dans
[`docs/ANALYSE-V0.md`](docs/ANALYSE-V0.md).
