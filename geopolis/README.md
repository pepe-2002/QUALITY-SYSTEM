# 🌍 GÉOPOLIS — Simulateur de Président

Jeu de géopolitique jouable dans le navigateur, en français, sans installation
ni connexion. Vous prenez la tête de l'une des **197 nations** du monde et vous
la gouvernez : impôts, budget, ressources, industrie, commerce, diplomatie,
armée et **course à l'intelligence artificielle**.

**Jouer : [ouvrir le jeu](https://claude.ai/code/artifact/bf0cbaaa-c065-43fe-a30c-4111ec4ea2c4)**
· ou ouvrir `geopolis-un-fichier.html` dans n'importe quel navigateur.

---

## Ce que le jeu simule

Le monde entier tourne en même temps que vous. Les 196 autres gouvernements
construisent, empruntent, commercent, s'allient et se font la guerre sans vous
attendre — chacun avec ses ressources, sa technologie et ses contraintes.

| Domaine | Contenu |
|---|---|
| **Économie** | PIB, croissance, inflation, chômage, dette, taux d'intérêt, défaut souverain |
| **Fiscalité** | Impôt sur le revenu, impôt sur les sociétés, TVA, droits de douane — avec courbe de Laffer |
| **Budget** | Santé, éducation, infrastructure, défense, subventions, en part du PIB |
| **Ressources** | 13 marchés (nourriture, pétrole, gaz, charbon, fer, cuivre, terres rares, uranium, or, électricité, puces, biens, calcul IA) aux prix mondiaux mouvants |
| **Construction** | 23 bâtiments : fermes, puits, mines, centrales (charbon, gaz, nucléaire, solaire), usines, fonderies de puces, centres de données, laboratoires, universités, hôpitaux, routes, ports, bases, complexe nucléaire |
| **Commerce** | Contrats d'approvisionnement négociés (ressource, quantité, prix, durée), offres reçues, rupture de contrat |
| **Diplomatie** | Relations −100/+100, ambassades, aide, pactes, alliances, sanctions, espionnage, votes à l'ONU |
| **Armée** | 11 types d'unités, guerres avec front mobile et pertes, capitulation (annexion, tribut, paix), arme nucléaire et riposte |
| **Course à l'IA** | Terres rares → puces → électricité → centres de données → calcul → 11 paliers, de l'automatisation à la superintelligence |
| **Recherche** | 15 technologies enchaînées, de l'agronomie de précision à la fusion nucléaire |
| **Politique** | Approbation, stabilité, corruption, élections tous les cinq ans, coups d'État, 8 lois activables |
| **Événements** | 20 crises à arbitrer : choc pétrolier, épidémie, grève générale, fuite d'un modèle d'IA, automatisation massive, scandale de corruption… |

**Cinq façons de gagner** : superintelligence, domination économique (30 % du PIB
mondial), conquête (15 nations annexées), leadership diplomatique (90 alliances
et une réputation irréprochable), ou prospérité totale.
**Trois façons de perdre** : élection perdue, coup d'État, insurrection.

## Différences avec *MA 3 – President Simulator*, qui a servi de référence

- **197 nations** aux données réelles (PIB, population, technologie, armée,
  dotations du sous-sol), pas des pays génériques.
- Un **vrai marché mondial** : les prix bougent selon la production et la
  consommation de la planète. Quand tout le monde construit des centres de
  données, les terres rares flambent, et les pays qui en ont s'enrichissent.
- La **course à l'IA**, absente du jeu de référence, avec sa chaîne
  d'approvisionnement complète et ses effets sur la productivité, l'armée,
  l'espionnage et le chômage.
- Une **fiscalité fine** avec effet Laffer, et un budget en part du PIB.
- Des **contrats commerciaux négociés** que le partenaire accepte ou refuse
  selon son besoin réel, le prix et l'état des relations.
- Aucune publicité, aucun achat, aucun serveur : tout tient dans la page.

## Performance

Le monde est stocké dans des **tableaux typés indexés par numéro de pays**
(`Float64Array`, `Int32Array`, `Int8Array`), pas dans des objets. Un jour de jeu
— production et consommation de 197 pays × 13 ressources, marché mondial,
économie, société, recherche, chantiers, guerres, décisions des nations —
coûte **moins d'une milliseconde**. À la vitesse maximale (×20), le jeu tient
50 images par seconde tout en simulant 20 jours par seconde.

Côté interface, chaque panneau est construit une seule fois, puis mis à jour en
n'écrivant que du texte dans des nœuds mémorisés : pas de reconstruction du DOM
à chaque image.

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | Ossature : accueil, barre, navigation, carte, panneaux |
| `geopolis.css` | Feuille de style |
| `g-data.js` | Les 197 nations, les ressources, les bâtiments, les unités, les technologies, les blocs |
| `g-moteur.js` | Simulation : flux, marché, économie, société, recherche, guerre, diplomatie, IA des nations, sauvegarde |
| `g-evenements.js` | Les 20 crises et leurs conséquences |
| `g-carte.js` | Carte du monde en canvas (zoom, déplacement, survol, sélection) |
| `g-ui.js` | Les 13 panneaux, les modales, la boucle de jeu |
| `g-accueil.js` | Sélection de la nation et reprise de partie |
| `sw.js`, `manifest.webmanifest` | Fonctionnement hors ligne, installation sur mobile |
| `construire-fichier-unique.py` | Assemble le tout en un seul fichier HTML |
| `geopolis-un-fichier.html` | **Version autonome** (201 Ko) — la seule chose à envoyer pour partager le jeu |

## Développement

```bash
python3 -m http.server 8899          # servir le dossier
# puis ouvrir http://localhost:8899/index.html

python3 construire-fichier-unique.py # régénérer la version autonome
```

Raccourcis clavier en jeu : `Espace` pause · `1` `2` `3` `4` vitesse ·
`C` carte, `N` nation, `E` économie, `R` ressources, `B` construction,
`M` commerce, `D` diplomatie, `A` armée, `I` IA, `S` recherche, `P` politique,
`L` classements, `J` journal.

## Note sur les données

Les chiffres des 197 pays sont des **ordres de grandeur** calibrés pour le jeu
(PIB, population, technologie, stabilité, armée, richesses du sous-sol). Ils
donnent un monde crédible et jouable, pas une base statistique officielle.
