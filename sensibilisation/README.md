# 🎬 Films de sensibilisation — l'accueil des passagers

Deux films internes du **Département Qualité de Royal Air**, destinés au
**groupe WhatsApp du personnel**. Pas de publication Facebook, pas de diffusion
publique : la mention est incrustée sur chaque image du film, pas seulement au
générique — une vidéo qui sort du groupe emporte sa règle avec elle.

| Film | Pour qui | Durée | À envoyer sur WhatsApp |
|---|---|---|---|
| **L'accueil en agence** | comptoirs de vente, réservation | 4 min 51 | `RoyalAir-accueil-agence-whatsapp.mp4` |
| **L'accueil en escale** | agents d'escale HAH · AJN · NWA | 4 min 56 | `RoyalAir-accueil-escale-whatsapp.mp4` |

Chaque film existe en **deux fichiers** :

- `RoyalAir-accueil-*.mp4` — 1080 × 1920, la version d'archive et de projection
  (réunion, formation, salle de briefing) ;
- `RoyalAir-accueil-*-whatsapp.mp4` — 720 × 1280, **environ 3 Mo**. C'est
  celui qu'on envoie. WhatsApp recompresse tout ce qu'on lui donne : mieux vaut
  lui remettre un fichier déjà léger et bien encodé qu'un gros fichier qu'il
  abîmera lui-même.

À côté des films, deux documents par sujet, **générés depuis le même
scénario** :

- `fiche-agence.md` / `fiche-escale.md` — tout le contenu en une page, à
  imprimer et à afficher au comptoir. Un film se regarde une fois, une fiche
  punaisée se relit ;
- `voix-off-agence.md` / `voix-off-escale.md` — le texte à lire, minuté sur le
  montage, si l'on veut poser une voix plus tard.

---

## Pourquoi ces films ont été fabriqués et non trouvés

La demande était de **chercher** deux vidéos professionnelles en français et
d'y mettre notre logo. Ce qui existe en français sur l'accueil aéroportuaire,
ce sont des **vidéos de promotion d'écoles de formation** et des reportages
métier de trois minutes. Deux raisons de ne pas les prendre :

1. **Le droit.** Coller le logo Royal Air sur le film de quelqu'un d'autre,
   c'est s'approprier son œuvre. Un film interne finit toujours par être
   réexpédié hors du groupe, et ce jour-là c'est la compagnie qui est en faute.
2. **Le fond.** Ces films montrent les règles d'un autre aéroport. Ils ne
   parlent ni du LET 410, ni de nos escales, ni du GOM, ni de la franchise
   bagages telle que nous l'appliquons. Un agent formé dessus n'est pas formé
   sur nos procédures — et en audit ANACM, cela ne compte pas.

Ces deux films-ci **appartiennent à Royal Air**, citent nos propres documents
(GOM, GRD-PROC-001, QUA-PROC-002), nos escales et notre flotte. Ils sont donc
opposables : un agent qui les a vus a été sensibilisé sur nos règles, et la
diffusion peut être tracée comme une action de sensibilisation.

## Ce qui a été repris des meilleurs films de formation

Trois choses reviennent dans tous ceux qui obtiennent un résultat, et elles
structurent nos deux films :

1. **Une situation avant la règle.** Chaque partie s'ouvre sur une scène réelle
   — Moroni à 5 h 30, un vol reporté, un collègue qui demande un passe-droit —
   et sur une question laissée en suspens. La règle qui suit répond à une
   question que l'agent s'est déjà posée dans sa tête.
2. **Le côte à côte « ne dites pas / dites ».** On ne change pas une habitude
   de langage avec un principe : on la change en donnant la phrase de
   remplacement, mot pour mot.
3. **Une idée par écran.** Les points apparaissent un par un. On ne montre
   jamais un mur de texte, et on ne montre jamais la suite avant qu'elle soit
   lue.

Ajouté pour notre cas : une **barre d'avancement** en haut de chaque image. Un
film de cinq minutes sur un téléphone, sans savoir où il en est, se referme au
bout de deux.

Et une contrainte de forme qui décide de tout : **sur WhatsApp, une vidéo
démarre sans le son.** La plupart des agents la regarderont muette, dans un
couloir. Donc **tout ce qui compte est écrit en grand à l'écran**, et la
musique ne porte jamais d'information.

## L'identité

Les couleurs et le logo ne sont pas approchés : ils sont **relevés au pixel sur
l'en-tête officielle de la compagnie** (courrier « Demande de clearance
positionnement F100 5Y-MMX » du 31/08/2026).

| | |
|---|---|
| bleu de l'en-tête | `#004AAD` |
| bleu du mot ROYAL AIR | `#1237A1` |
| rouge de la sphère | `#EC313A` |
| jaune de l'orbite | `#FDC20C` |

Le logo (`marque/royal-air-logo.png`) est posé **tel quel, sur une réserve
blanche**. Sur fond marine, son nom écrit en bleu foncé disparaîtrait : le
détourer obligerait à le retoucher, c'est-à-dire à le déformer. La réserve
blanche est la règle de toutes les compagnies, et le logo reste exactement
lui-même. La bande bleue et rouge en biais des cartes de garde est celle du
papier à en-tête, redessinée au vecteur.

---

## Refabriquer les films

```bash
cd sensibilisation
python3 film.py tout          # les deux films  (~9 min de calcul)
python3 film.py agence        # un seul
python3 texte.py              # les fiches et les textes de voix off
```

Il faut `ffmpeg`, `python3-pil` et `numpy`.

### Où corriger quoi

| Ce qu'on veut changer | Le fichier |
|---|---|
| une phrase, un point, une durée, l'ordre des chapitres | **`scenarios.py`** |
| la mise en page, les couleurs, les types de cartes | `film.py` |
| la musique | `musique.py` |
| les fiches et la voix off | rien — `python3 texte.py` les régénère |

⚠️ **Ne jamais retoucher un `.mp4`.** On corrigerait la copie au lieu de la
source, et la correction serait perdue au prochain montage. Tout ce qui se lit
à l'écran est dans `scenarios.py`, et nulle part ailleurs.

### Ce que le montage vérifie tout seul

À la fin de chaque film, le programme relit la durée du fichier livré avec
`ffprobe` et la compare à celle du scénario. Un écart de plus d'une seconde
arrête le montage.

Ce contrôle n'est pas décoratif : le premier montage annonçait 4 min 51 et
livrait 5 min 31, dont **quarante secondes d'écran vide** — le démultiplexeur
`concat` d'ffmpeg tient la dernière image d'une séquence plus longtemps que
demandé, et les fondus de sortie tombaient à côté. Chaque image est désormais
encodée en clip `-loop 1 -t <durée>`, exact à la frame près.

## La musique

Elle est **composée ici** (`musique.py`), pas prise ailleurs : une nappe de
quatre accords en fa majeur, sans percussion ni mélodie, avec un creux de 6 dB
entre 250 Hz et 4 kHz. Ce creux est la place de la parole : si l'on pose une
voix off un jour, il n'y aura rien à baisser au mixage.

Une musique du commerce serait un risque inutile — un film interne finit
toujours par circuler, et ce jour-là il diffuserait l'œuvre d'un tiers.

## Ajouter un troisième film

1. Copier un bloc de `scenarios.py` (les types de scènes disponibles :
   `ouverture`, `situation`, `chapitre`, `liste`, `duo`, `regle`, `cloture`,
   `fin`) ;
2. l'ajouter au dictionnaire `choix` dans `film.py` ;
3. `python3 film.py <nom>`.

Aucune image, aucune police, aucun son à aller chercher : tout est dans ce
dossier.
