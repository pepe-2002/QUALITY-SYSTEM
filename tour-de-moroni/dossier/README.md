# 📁 LE DOSSIER TOUR DE MORONI — à lire avant de produire

**Tour de Moroni** — cross inclusif de 10 km, départ et arrivée place de
l'Indépendance, **le premier dimanche de décembre**. Première édition :
**dimanche 6 décembre 2026**.

---

## La règle, en trois lignes

0. 🕐 **Lancer `date` avant tout.** Entre deux sessions, des jours peuvent
   passer sans que rien ne le signale, et les fausses dates se retrouvent dans
   les fichiers qui font foi.
1. **Début de session** → lire `MEMOIRE.md`. C'est l'état du projet et le
   journal de toutes les décisions. **Rien n'est mémorisé ailleurs.**
2. **Avant de pousser** → mettre `MEMOIRE.md` à jour. Ce qui n'est pas écrit est
   perdu à la fin de la session.

---

## Quoi lire avant quoi

| Ce que je vais faire | Ce que je lis d'abord |
|---|---|
| **Présenter le projet** (partenaire, institution, presse) | `PROJET.md` en entier, puis `PARTENAIRES.md` § 5 (le pitch en trois longueurs) |
| **Aller voir un sponsor** | `PARTENAIRES.md` — niveaux, contreparties, liste de cibles, courrier type. Puis `BUDGET.md` § 3 pour savoir ce qui est déjà couvert |
| **Parler chiffres, engager une dépense** | `BUDGET.md` — et vérifier le point d'arrêt en cours (§ 6) |
| **Travailler sur le terrain** (parcours, sécurité, ravitaillement, stands) | `PARCOURS.md`, puis la carte `../carte/carte-tour-de-moroni.svg` et `../carte/donnees/points_blocage.csv` |
| **Parler d'inclusion, former les accompagnateurs** | `PROJET.md` § 5 et `PARCOURS.md` § 6 et § 7 |
| **Changer le parcours** | `PARCOURS.md` § 8, puis les scripts de `../carte/` |
| **Décider quelque chose** | `PROJET.md` § 8 (règle de décision) et `MEMOIRE.md` § 5 (ce qui est en attente du patron) |

⚠️ **En cas de doute entre « je décide » et « je demande au patron » : je
demande.** Tout ce qui engage plus de 1 000 000 KMF, le nom de l'événement, ou
une signature avec une institution, remonte au patron.

---

## Les documents

| Fichier | Ce que c'est |
|---|---|
| **`MEMOIRE.md`** | 🧠 l'état du projet, les décisions, les contacts, ce qui reste à trancher. Le plus important : sans lui, on repart de zéro |
| **`PROJET.md`** | 📘 le dossier de projet : idée, formats, inclusion, organisation, calendrier, indicateurs, risques, pérennité |
| **`PARCOURS.md`** | 🗺️ le parcours au mètre près : road-book, postes, ravitaillements, stands, plan de fermeture, accessibilité, règlement sportif |
| **`BUDGET.md`** | 💰 les deux budgets (socle 2026, cible 2027), les recettes, la trésorerie, les points d'arrêt, ce qu'on coupe et ce qu'on ne coupe jamais |
| **`PARTENAIRES.md`** | 🤝 sponsoring, mécénat, subvention : les niveaux, les contreparties, à qui s'adresser, le pitch, le courrier type, le rapport d'après-course |

## Ce qui n'est pas dans le dossier, et pourquoi

Ce qui est **fabriqué par un programme** reste à côté du programme — sinon on
corrige la copie au lieu de la source, et les deux finissent par se contredire.

| Fichier | Où | Pourquoi pas ici |
|---|---|---|
| `carte-tour-de-moroni.svg` | `../carte/` | dessiné par `carte.py` |
| `parcours.geojson` | `../carte/` | calculé par `calculer_parcours.py` |
| `donnees/points_blocage.csv`, `roadbook.json`, `parcours_calcule.json` | `../carte/donnees/` | recalculés à chaque changement de parcours |
| `donnees/routes_moroni.json`, `contexte_moroni.json`, `altitudes.json` | `../carte/donnees/` | extraits d'OpenStreetMap et du modèle SRTM par `extraire_osm.py` |

---

## L'état du système, en une ligne

Rien ne publie ni ne s'exécute tout seul sur ce projet : **tous les fichiers sont
produits à la demande**, par les trois scripts de `../carte/`. Aucune donnée
personnelle ne doit entrer dans ce dossier — le dépôt est public.
