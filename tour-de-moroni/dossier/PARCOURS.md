# LE PARCOURS — 10 km, en huit autour de la place de l'Indépendance

> Carte imprimable : `../carte/carte-tour-de-moroni.svg` (A3, s'agrandit jusqu'à
> l'A0 sans perdre en qualité). Tracé numérique : `../carte/parcours.geojson`
> (s'ouvre dans Google Earth, QGIS, Garmin, Strava).

---

## 1. Les chiffres

| | |
|---|---|
| Distance | **10,02 km** mesurés sur le réseau réel |
| Dénivelé positif | 145 m |
| Altitude | de 5 m (front de mer) à 38 m (boulevard Karthala) |
| Nature des voies | 96 % d'axes primaires, secondaires ou tertiaires |
| Forme | un huit : boucle Sud 6,05 km + boucle Nord 3,98 km |
| Départ / arrivée | place de l'Indépendance (−11,70146 ; 43,25269) |
| Sens | Sud d'abord, puis Nord — chaque boucle dans le sens des aiguilles |

**Pourquoi ce tracé et pas un autre.** Il n'a pas été dessiné à la main : il a
été calculé sur les 435 rues de Moroni relevées dans OpenStreetMap, avec un coût
qui pénalise d'abord la pente, ensuite les petites rues, enfin la longueur (voir
`../carte/calculer_parcours.py`). Sur 112 combinaisons de 10 km possibles au
départ de la place, c'est celle qui monte le moins tout en restant à 96 % sur des
axes larges. Pour une course où des fauteuils et des joëlettes prennent le même
départ que les coureurs, c'est le seul critère qui compte vraiment.

> ⚠️ **Ce qui reste à faire sur le terrain.** Les altitudes viennent du modèle
> SRTM 30 m (±5 m d'incertitude) : elles disent que le parcours est plat, elles ne
> remplacent pas un relevé. Avant l'édition : mesure officielle des 10 km **à la
> roue** avec la Fédération comorienne d'athlétisme, relevé des pentes réelles,
> et repérage des trous, caniveaux et bordures qui gênent un fauteuil. Prévu au
> calendrier le 15 novembre.

---

## 2. Feuille de route, rue par rue

### Boucle Sud — km 0 à 6,05

| Depuis | Longueur | Voie | Ce qu'on traverse |
|---|---|---|---|
| km 0,00 | 56 m | Rue de la Corniche | Sortie de la place, face à la mer |
| km 0,06 | 298 m | Mvouvou-djou | Front de mer, Hôtel de ville, vieille ville |
| km 0,37 | 244 m | voie secondaire (Irungudjani) | Ancien marché, mosquée de Chadhuli |
| km 0,63 | 1 017 m | **Rue Itsambuni** | Irungudjani, Basha, Djomani |
| km 1,64 | 716 m | **Bd de la République Populaire de Chine** | Ribatwi, Cour suprême, **Palais du Peuple** |
| km 2,39 | 569 m | Avenue du Président Ali Soilihi | Hamramba — *point le plus au sud* |
| km 2,96 | 1 407 m | **Boulevard Karthala** | Zilimadju, Djivani, Caltex — remontée vers le centre |
| km 4,37 | 776 m | voie tertiaire | Mdjivurize, Mtsizambe |
| km 5,14 | 100 m | voie secondaire | Mbuweni |
| km 5,25 | 197 m | Boulevard Karthala | |
| km 5,48 | 330 m | Avenue de la Place de l'Indépendance | Retour vers la place |
| km 5,82 | 272 m | Rue de la Corniche | **Passage devant le village — km 6** |

### Boucle Nord — km 6,05 à 10,02

| Depuis | Longueur | Voie | Ce qu'on traverse |
|---|---|---|---|
| km 6,09 | 183 m | Avenue de la Place de l'Indépendance | |
| km 6,28 | 1 413 m | voie tertiaire | Buzini, Mangani, Hadudja, Hankunu |
| km 7,70 | 183 m | **Rue de l'Union Africaine** | Marché de Volo Volo à main droite |
| km 7,89 | 388 m | voie résidentielle | Oasis — *point le plus au nord* |
| km 8,27 | 225 m | Route de l'Alliance Française | Alliance Française, Tennis Club |
| km 8,50 | 1 524 m | **Rue de la Corniche** | 1,5 km face à la mer, jusqu'à l'arrivée |

**Le km 6 est le point clé du dispositif.** Les coureurs repassent devant le
village : c'est là que le public se masse, que le speaker annonce les passages,
et c'est là que les participants de la **boucle Sud inclusive terminent leur
course** en franchissant la même arche que tout le monde.

---

## 3. Les postes sur le parcours

| Poste | Km | Position | Ce qu'on y trouve |
|---|---|---|---|
| **Village / PS1** | 0 et 10 | Place de l'Indépendance | Départ, arrivée, stands, podium, poste de secours principal, PC course |
| **PS2** | 2,4 | Palais du Peuple (−11,71923 ; 43,24556) | Poste de secours, ambulance n° 1 |
| **R1** | 2,5 | Hamramba (−11,71943 ; 43,24645) | Eau, jus, fruits, poubelles de tri |
| **B1** | 3,8 | Bd Karthala (−11,71306 ; 43,25190) | Brumisation |
| **R2 + relais PMR** | 5,0 | Mbuweni (−11,70635 ; 43,25558) | Eau, jus, fruits ; relève des équipes joëlette |
| **PS3** | 7,6 | Alliance Française (−11,69046 ; 43,25698) | Poste de secours, ambulance n° 2 |
| **R3** | 7,5 | Hankunu (−11,69132 ; 43,25670) | Eau, jus, fruits |
| **B2** | 8,8 | Corniche (−11,69136 ; 43,25281) | Brumisation |
| **Arrivée** | 10,0 | Place de l'Indépendance | Eau, jus, fruits, médailles, kinés |

**Règle d'espacement** : jamais plus de 2,6 km entre deux points d'eau, et un
point de secours joignable à moins de 1,5 km de n'importe quel endroit du
parcours. En climat tropical, à 6 h 30, avec une barrière horaire à 2 h 30, c'est
le minimum défendable.

### Ce qu'on prévoit à chaque ravitaillement (base 800 participants)

| Article | R1 | R2 | R3 | Arrivée |
|---|---|---|---|---|
| Eau (litres) | 300 | 350 | 300 | 500 |
| Jus locaux (portions) | 150 | 250 | 200 | 400 |
| Fruits (kg — banane, orange) | 25 | 35 | 25 | 60 |
| Glace (kg) | 20 | 25 | 20 | 50 |
| Bénévoles | 6 | 8 | 6 | 12 |
| Poubelles de tri | 4 | 4 | 4 | 10 |

**Zone de dépôt des gobelets** : 60 m après chaque table, signalée au sol et
tenue par deux bénévoles avec des bacs. Le parcours doit être rendu propre à
midi — c'est un des dix indicateurs du projet.

---

## 4. Les stands du village

Le village s'installe sur la place de l'Indépendance, sur trois rangées autour de
l'arche. **25 emplacements** de 3 × 3 m, dont 15 payants (40 000 KMF) et 10
gratuits réservés aux associations et aux institutions partenaires.

| Rangée | Emplacements | Qui |
|---|---|---|
| Face à l'arche | 6 | Sponsor titre (2), sponsors officiels (3), Ministère / Mairie (1) |
| Côté mer | 9 | Jus et fruits locaux, restauration, artisanat |
| Côté ville | 10 | Associations de personnes handicapées, Croix-Rouge, clubs sportifs, santé publique (dépistage tension / diabète) |

**Deux stands ne sont pas négociables** : celui des associations de personnes
handicapées, en première ligne et pas au fond ; et celui de la prévention santé,
qui donne au Tour une utilité au-delà du dimanche matin.

---

## 5. Fermer la ville sans la bloquer

Le tracé compte **53 accès latéraux** — rues et ruelles qui débouchent sur le
parcours. La liste complète, avec coordonnées GPS et kilométrage, est dans
`../carte/donnees/points_blocage.csv` : c'est le document de travail à remettre à
la Police nationale.

| Type de point | Nombre | Qui le tient |
|---|---|---|
| Carrefours majeurs (2 voies latérales ou plus) | 9 | Police nationale, 2 agents |
| Accès nommés et sorties de quartier | 13 | Police ou gendarmerie, 1 agent + 1 bénévole |
| Ruelles et accès riverains | 31 | 1 bénévole, barrière légère et gilet |

**Horaires de fermeture** :

| Tronçon | Fermé de | Rouvert à |
|---|---|---|
| Place de l'Indépendance et abords | 4 h 00 | 11 h 30 |
| Boucle Sud (km 0 à 6) | 5 h 30 | 9 h 30 |
| Boucle Nord (km 6 à 10) | 6 h 00 | 10 h 00 |

**Riverains** : un tract distribué dans les quartiers traversés une semaine
avant (Irungudjani, Basha, Djomani, Ribatwi, Hamramba, Zilimadju, Caltex,
Mdjivurize, Mbuweni, Mangani, Hadudja, Hankunu, Oasis), plus une annonce radio le
samedi et le dimanche à 5 h. Un véhicule bloqué par la course est un opposant
gagné pour l'année suivante ; un riverain prévenu devient spectateur.

**Traversées d'urgence** : deux couloirs de franchissement, au km 3,9 (Djivani)
et au km 7,2 (Mangani), tenus par un chef de poste avec radio, ouverts sur ordre
du PC uniquement, pour laisser passer une ambulance ou un véhicule de secours.

---

## 6. Ce que le parcours exige, côté accessibilité

Un tracé « plat » sur une carte peut rester impraticable en fauteuil. Les six
points à vérifier lors de la reconnaissance du 15 novembre, et à corriger avant
le jour J :

1. **Les bordures et les caniveaux** aux entrées de la place et aux carrefours :
   prévoir des rampes provisoires en bois là où la traversée n'est pas de plain-pied.
2. **Les nids-de-poule** sur le boulevard Karthala et la voie tertiaire du km 4,4 :
   signalés à la peinture et, si possible, rebouchés par les services de la voirie.
3. **Le sable et les gravillons** sur la rue de la Corniche : passage de balai
   mécanique la veille — une roue avant de fauteuil ne pardonne pas le gravier.
4. **La largeur utile** aux deux points les plus étroits (km 4,4 et km 7,9) :
   3 mètres minimum libres, donc pas de barrière posée côté trottoir.
5. **Les pentes réelles** sur les 27 segments que le modèle donne au-dessus de
   6 % : à mesurer au clinomètre. Au-delà de 8 % sur plus de 30 m, on ajoute un
   binôme de pousseurs au poste concerné.
6. **L'ombre** : repérer les zones sans arbre entre le km 2 et le km 5, où la
   brumisation et les bénévoles à l'eau doivent être renforcés.

---

## 7. Règlement sportif — l'essentiel

- **Ouvert à partir de 12 ans** sur le 10 km (autorisation parentale jusqu'à 18
  ans), sans limite d'âge haute. Le Tour des enfants est réservé aux 6-12 ans.
- **Certificat médical** de moins d'un an, ou attestation sur l'honneur pour les
  formats non chronométrés ; certificat obligatoire pour la personne transportée
  en joëlette.
- **Joëlettes** : 6 accompagnateurs maximum par engin, dossards fournis, départ à
  l'arrière du dernier sas, classement au nom de la personne transportée, les
  accompagnateurs n'apparaissent pas au classement.
- **Coureurs déficients visuels** : un guide, cordon de guidage, dossard « GUIDE »,
  départ dans le sas correspondant à l'allure annoncée.
- **Fauteuils manuels** : départ 2 minutes avant le peloton pour dégager le sas ;
  fauteuils à assistance électrique non admis en classement (sécurité du peloton).
- **Écouteurs interdits**, véhicules et vélos suiveurs interdits hors
  organisation, animaux interdits sur le parcours.
- **Dossard porté devant, visible, non plié** — c'est ce qui permet au chrono et
  aux secours de vous identifier.
- **Barrière horaire 2 h 30.** Au-delà, on est invité à rejoindre la voiture-balai
  ou à terminer sur le trottoir : la circulation rouvre.
- **Classements** : scratch hommes / femmes, catégories d'âge (12-17, 18-39,
  40-49, 50-59, 60+), classement fauteuil, classement joëlette, challenge
  entreprises et challenge scolaires (équipe de 4, temps cumulé).

---

## 8. Refaire la carte, ou changer le parcours

Tout est reproductible, sans aucune dépendance à installer :

```bash
cd tour-de-moroni/carte
python3 extraire_osm.py        # rafraîchit les données OSM + altitudes (internet requis)
python3 calculer_parcours.py   # recalcule le parcours, le road-book, les blocages
python3 carte.py               # redessine carte-tour-de-moroni.svg
```

Pour déplacer une boucle, il suffit de changer `PIVOT_SUD` ou `PIVOT_NORD` en
tête de `calculer_parcours.py` : le reste (distance, bornes, postes, road-book,
points de blocage, carte) se recalcule tout seul.

**Attribution obligatoire sur toute carte publiée** : « Fond de carte :
OpenStreetMap (ODbL) » — c'est la licence des données, elle n'est pas optionnelle.
