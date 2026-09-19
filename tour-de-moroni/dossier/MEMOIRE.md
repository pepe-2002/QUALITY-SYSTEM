# MÉMOIRE — Tour de Moroni

> **Je n'ai aucun souvenir en dehors de ce fichier.** Tout ce qui est décidé,
> contacté, signé, refusé ou appris s'écrit ici le jour où ça arrive. Un
> renseignement non écrit est un renseignement perdu à la fin de la session.
>
> Règle de départ de session : **lancer `date` avant tout** — plusieurs jours
> peuvent passer entre deux messages sans que rien ne me le signale.

---

## 1. Où en est le projet

| | |
|---|---|
| **État** | Dossier de conception terminé. **Rien n'est engagé, rien n'est contacté.** |
| **Date visée** | Dimanche 6 décembre 2026 — première édition |
| **Aujourd'hui** | 19 septembre 2026 → **J-77** |
| **Prochain jalon** | 30 septembre : statuts de l'association déposés |
| **Prochain point d'arrêt** | 10 octobre : GO / NO-GO n° 1 (autorisations + 60 % du budget) |
| **Budget socle** | 17 334 000 KMF (≈ 35 200 €) — recettes à trouver : 13 500 000 KMF |
| **Décision en attente du patron** | Confirmer 2026 ou basculer sur « Tour d'essai 2026 + édition 1 en décembre 2027 » |

---

## 2. Ce qui est décidé

| Décidé le | Décision | Pourquoi |
|---|---|---|
| 19/09/2026 | **Nom : Tour de Moroni** ; signature : *Toute la ville, au même pas* | Demandé par le patron |
| 19/09/2026 | **Date : premier dimanche de décembre**, chaque année. 2026 : 6 déc. · 2027 : 5 déc. · 2028 : 3 déc. | Suit immédiatement la Journée internationale des personnes handicapées (3 décembre) — l'ancrage du projet. Dates vérifiées : ce sont bien des dimanches |
| 19/09/2026 | **Départ à 6 h 30** | Lever du soleil vers 5 h 25 ; une heure de fraîcheur avant la chaleur. Décembre = début de saison des pluies |
| 19/09/2026 | **Parcours : un huit de 10,02 km** autour de la place de l'Indépendance — boucle Sud 6,05 km puis boucle Nord 3,98 km | Calculé sur le réseau réel (OSM + SRTM) : le tracé le plus plat à 96 % sur grands axes, parmi 112 combinaisons testées. Le huit permet trois passages devant le public et une option 6 km sans dispositif supplémentaire |
| 19/09/2026 | **Quatre formats** : 10 km chrono, 10 km allure libre, boucle Sud inclusive 6 km, Tour des enfants 1,2 km | Un seul parcours, un seul village, quatre manières d'y entrer |
| 19/09/2026 | **Gratuité d'inscription** pour les participants en situation de handicap et leurs accompagnateurs | Cohérence du projet ; compensée par le dossard entreprise à 10 000 KMF |
| 19/09/2026 | **Deux scénarios budgétaires** : socle 2026 (17,3 M KMF, 800 participants) et cible 2027 (37,6 M, 2 000) | On ne construit pas l'édition 2 sur l'espoir |
| 19/09/2026 | **Deux points d'arrêt** : 10 octobre et 6 novembre, avec repli « Tour d'essai » | Une première édition ratée coûte trois ans de crédibilité |
| 19/09/2026 | **Ce qu'on ne coupe jamais** : secours, assurance, eau, fermetures de voirie, dispositif d'inclusion | Une course sans t-shirt reste une course ; sans secours, c'est une faute |

---

## 3. Ce qui est fabriqué, et où

| Quoi | Où | Fabriqué par |
|---|---|---|
| Dossier de projet | `dossier/PROJET.md` | à la main |
| Parcours détaillé, road-book, règlement | `dossier/PARCOURS.md` | à la main |
| Budget et plan de financement | `dossier/BUDGET.md` | à la main |
| Partenariats, pitch, courrier type | `dossier/PARTENAIRES.md` | à la main |
| **Carte du parcours (A3)** | `carte/carte-tour-de-moroni.svg` | `carte/carte.py` |
| Tracé numérique (Google Earth, QGIS, GPS) | `carte/parcours.geojson` | `carte/calculer_parcours.py` |
| Liste des 53 points de blocage, avec GPS | `carte/donnees/points_blocage.csv` | `carte/calculer_parcours.py` |
| Données OSM + altitudes | `carte/donnees/` | `carte/extraire_osm.py` |
| **Dossier PDF à envoyer (25 pages)** | `Dossier-Tour-de-Moroni.pdf` | `fabriquer_dossier_pdf.py` |

**Ce qui est généré par un programme reste à côté du programme** — sinon on
corrige la copie au lieu de la source.

---

## 4. Contacts — journal

*(Aucun contact pris à ce jour. Une ligne par échange : date, organisation,
interlocuteur, ce qui a été dit, prochaine action, date de relance.)*

| Date | Organisation | Interlocuteur | Échange | Suite | Relance |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

---

## 5. Ce qui reste à trancher

| Question | Qui décide | Quand |
|---|---|---|
| Édition 2026 complète, ou « Tour d'essai » 2026 + édition 1 en 2027 ? | **Le patron** | Avant le 30 septembre |
| Qui préside l'association et qui signe au compte bancaire ? | **Le patron** | Avant le 30 septembre |
| Nom du chef de projet et des 8 responsables de commission | **Le patron** | Avant le 10 octobre |
| Joëlettes : achat, mécénat fléché, ou prêt pour 2026 ? | Commission inclusion, arbitrage patron | Avant le 1ᵉʳ novembre |
| Chronométrage manuel ou à puces dès 2026 ? | Commission inscriptions | Avant le 25 octobre |
| Le Tour reste-t-il une association, ou devient-il un produit touristique avec un opérateur ? | **Le patron** | Après l'édition 2026 |

---

## 6. Ce qu'on a appris, et qui servira l'année prochaine

| Leçon | D'où elle vient |
|---|---|
| Le relief commande le tracé, pas l'esthétique de la boucle : les 10 km les plus « jolis » de Moroni montent à 124 m d'altitude, les 10 km retenus plafonnent à 38 m | Calcul du parcours, 19/09/2026 |
| Une forme en huit vaut mieux qu'une grande boucle : un seul village, trois passages devant le public, et l'option 6 km sans dispositif supplémentaire | Conception du parcours |
| Les altitudes SRTM 30 m ont ±5 m d'incertitude : elles prouvent qu'un parcours est plat, elles ne valident pas une pente devant un fauteuil. La roue et le clinomètre restent obligatoires | Limite des données utilisées |
| Les précédents comoriens existent (Marathon de Moroni de la Fédération d'athlétisme, Course des femmes du 8 mars, sponsoring MVola du basket) : on n'arrive pas en terrain vierge, on arrive après des gens | Recherche du 19/09/2026 |
| Sur les courses joëlette éprouvées, la règle est stable : 6 accompagnateurs maximum, départ en fin de sas, dossards hors classement, certificat médical pour la personne transportée | Règlements Grand Raid des Pyrénées, Tout Rennes Court, Marathon des Capables |

---

## 7. Journal de session

**19/09/2026 — création du projet.** Demande du patron : un cross de 10 km à
Moroni, inclusif, avec ravitaillements et stands, un budget, une carte, une date
en décembre à choisir, et des recherches sur les projets comparables.
Livré : les cinq documents du dossier, la carte A3 générée depuis les données
OpenStreetMap, le tracé GeoJSON, la liste des 53 points de blocage, et trois
scripts qui permettent de tout recalculer si le parcours change.
Ajouté le même jour, à la demande du patron : le **dossier PDF téléchargeable**
(25 pages — couverture, les quatre documents, la carte en pleine page paysage),
fabriqué par `fabriquer_dossier_pdf.py`. Le PDF se refabrique, il ne se corrige
pas à la main. `MEMOIRE.md` en est volontairement exclu : c'est le journal
interne, il ne sort pas du dossier de travail.
Signalé au patron : **J-77, c'est court** pour une première édition avec
sponsors et import de matériel — d'où les deux points d'arrêt et le repli
« Tour d'essai ». La décision lui revient.
