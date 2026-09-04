# 🎬 Films de sensibilisation — l'accueil des passagers

Deux films internes du **Département Qualité de Royal Air**, destinés au
**groupe WhatsApp du personnel**. Pas de publication Facebook, pas de diffusion
publique : la mention est incrustée sur chaque image du film, pas seulement au
générique — une vidéo qui sort du groupe emporte sa règle avec elle.

| Film | Pour qui | Durée | À envoyer sur WhatsApp |
|---|---|---|---|
| **L'accueil en agence** | comptoirs de vente, réservation | 6 min 53 | `RoyalAir-accueil-agence-whatsapp.mp4` |
| **L'accueil en escale** | agents d'escale HAH · AJN · NWA | 7 min 20 | `RoyalAir-accueil-escale-whatsapp.mp4` |

Les deux films sont **dits par une voix off française**, sur une nappe musicale
qui s'efface pendant la parole. Ils restent entièrement lisibles **sans le
son** : rien n'existe seulement à l'oreille.

Chaque film existe en **deux fichiers** :

- `RoyalAir-accueil-*.mp4` — 1080 × 1920, la version d'archive et de projection
  (réunion, formation, salle de briefing) ;
- `RoyalAir-accueil-*-whatsapp.mp4` — 720 × 1280, **environ 3 Mo**. C'est
  celui qu'on envoie, **environ 6,5 Mo** — sous la limite de WhatsApp. WhatsApp
  recompresse tout ce qu'on lui donne : mieux vaut lui remettre un fichier déjà
  léger et bien encodé qu'un gros fichier qu'il abîmera lui-même.

⏱️ **Sur la durée — arbitrage tranché par le patron le 04/09/2026.** Sans voix,
les films faisaient 4 min 51 et 4 min 56 ; la voix off les porte à **6 min 53**
et **7 min 20**, respirations comprises.

> « même si la vidéo fait 10 min, si la voix paraît naturelle, calme, et que
> les gens ont envie d'écouter, c'est ce qui gagne »

La durée n'est donc plus une contrainte de ce projet, et les silences sont
calculés dans ce sens. Ne pas « optimiser » la longueur d'un film en accélérant
la narration : ce serait défaire la décision.

À côté des films, deux documents par sujet, **générés depuis le même
scénario** :

- `fiche-agence.md` / `fiche-escale.md` — tout le contenu en une page, à
  imprimer et à afficher au comptoir. Un film se regarde une fois, une fiche
  punaisée se relit ;
- `voix-off-agence.md` / `voix-off-escale.md` — le relevé de tout ce que dit la
  voix, image par image, avec la version prononçable en regard. C'est ce qu'on
  relit pour corriger la narration — et le conducteur si l'on réenregistre un
  jour avec une vraie voix.

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

## La voix off

Elle est fabriquée par `voix.py`, en quatre temps :

1. **Écrire ce qui doit être dit** — une phrase par image du film, tirée du même
   scénario que l'image. La voix arrive donc exactement quand la ligne apparaît,
   sans aucun calage à la main.
2. **Le réécrire pour la bouche.** C'est l'étape que tout le monde saute, et
   celle qui trahit le travail bâclé. Une synthèse à qui l'on donne le texte
   affiché tel quel dit « cinq h trente », « trois kg », « gerdeproc zéro zéro
   un » et épelle les mots écrits en capitales. `prononcer()` réécrit les
   heures, les nombres, les unités, les sigles et les références de procédure —
   **en gardant la ponctuation intacte**, deux-points compris : c'est elle qui
   commande le phrasé à l'étape suivante.
3. **Découper sur la ponctuation, et poser les silences soi-même.** C'est ce qui
   fait la différence entre une voix qui débite et une voix qui parle.

   Mesuré sur notre voix : un **point** est bien marqué par la synthèse (0,50 à
   0,65 s de silence), mais une **virgule** ne donne que **0,08 s** — autant
   dire rien. La virgule est avalée, et c'est exactement ce que le patron
   entendait. Le texte est donc découpé à chaque signe, chaque morceau est
   synthétisé séparément, et le silence est posé à la main :

   | signe | silence |
   |---|---|
   | virgule | 0,30 s |
   | point-virgule | 0,38 s |
   | deux-points | 0,46 s |
   | point | 0,62 s |
   | point d'interrogation | 0,72 s |

   Et **1 seconde entre deux points d'une liste** : le temps de faire le lien
   entre ce qu'on vient d'entendre et ce qu'on vient de lire.

   ⚠️ **Et pourquoi ça ne hache pas la phrase.** Recoller des morceaux, c'est
   risquer que chacun se termine comme une phrase : intonation qui retombe,
   lecture en escalier. On garde donc le signe de ponctuation **à la fin** du
   morceau synthétisé. Vérifié à la mesure, sur le même fragment
   « Comptoir propre » : terminé par une **virgule**, la voix se tient à
   150 Hz — la phrase est en suspens ; terminée par un **point**, elle retombe
   à 138 Hz — la phrase est finie. Le morceau à virgule garde donc sa
   suspension, et les raccords ne s'entendent pas.

4. **Synthétiser** — modèle neuronal français, hors ligne, sans compte ni clé.
   Le modèle est chargé **une seule fois** en mémoire : depuis le découpage il
   y a plus de cinq cents morceaux par film, et les relancer un par un en
   ligne de commande rechargeait 63 Mo à chaque fois — plusieurs heures de
   montage pour un résultat identique. Chargé une fois : 0,2 s par morceau.
5. **Polir**, et c'est là que « synthèse vocale » devient « voix off » : coupe
   des graves à 85 Hz, réduction du souffle, −2,5 dB à 260 Hz (le côté
   « boîte »), +3 dB à 3,2 kHz (la bande de l'intelligibilité, celle qui fait
   qu'on comprend dans un couloir), dé-essage, compression, et normalisation à
   −16 LUFS.

**C'est la voix qui commande le montage, pas l'inverse.** Chaque image dure au
moins le temps de sa phrase, plus une respiration. On n'accélère jamais une voix
pour la faire entrer dans un montage déjà fait : cela s'entend toujours. Le
film s'allonge donc — c'est le prix d'une narration qui respire.

La nappe musicale descend de 7 dB pendant qu'on parle et remonte après. Elle
était déjà creusée de 6 dB dans la bande de la parole ; ne pas masquer ne suffit
pas, c'est ce **mouvement** qui donne à un film son air fini.

### La voix retenue

**`fr_FR-siwis`, allure 1,15** — choisie à l'oreille par le patron le
04/09/2026, sur l'extrait `COMPARER-LES-VOIX.mp4` (la deuxième des trois), puis
ralentie à sa demande : la première version « était un peu trop rapide ».

Ces deux réglages sont une décision, pas un paramètre technique. Ne pas les
changer sans redemander.

### Changer de voix — et l'erreur à ne pas refaire

Trois voix françaises sont installées. Pour les entendre sur un même passage :

```bash
python3 voix.py --essai        # → COMPARER-LES-VOIX.mp4
```

Puis changer `VOIX` en tête de `voix.py` et relancer `python3 film.py tout`.

⚠️ **L'allure n'est pas une propriété du réglage : elle dépend de la voix.** Le
même `ALLURE = 0,90` donnait 140 mots par minute avec la voix « tom » et 165
avec « siwis » — d'où le « trop rapide ». Toute nouvelle voix se **recalibre**,
sur un passage réel du film et non sur une phrase d'essai : les silences entre
phrases comptent dans le rythme perçu.

Mesuré sur siwis, sur un vrai passage :

| allure | mots / minute | |
|---|---|---|
| 0,90 | 165 | trop rapide |
| 1,00 | 149 | la norme des voix off |
| **1,15** | **140** | **retenu** |
| 1,25 | 130 | |
| 1,35 | 119 | ça traîne |

Pourquoi 140 et non les 150 de la norme : ces 145-160 sont l'allure d'une voix
qui raconte à quelqu'un qui **écoute**. Ici la voix parle à quelqu'un qui **lit
en même temps** — chaque phrase double une ligne affichée. C'est la lecture qui
commande le rythme, pas la parole.

### Le débit est égalisé

**À allure constante, la synthèse ne parle pas à vitesse constante.** Mesuré sur
nos propres phrases, en phonèmes par seconde : 10,5 sur « Dites plutôt », 14,3
sur « Saluer le premier », 13,6 sur « Le passager ne verra jamais le commandant
de bord… ». Près de 30 % d'écart.

C'est ce que le patron entendait : « si la phrase est longue on a l'impression
que la voix accélère ». Une phrase longue tenue à 14 phonèmes/seconde court
quatre secondes sans respirer — elle n'accélère pas vraiment, elle ne s'arrête
jamais, et cela s'entend pareil.

Chaque fragment est donc **mesuré après avoir été dit**, et **redit plus
lentement** s'il dépasse `DEBIT` (12,6 phonèmes/seconde, le bas de ce qui a été
mesuré, l'allure des passages calmes). Une seule correction suffit : la durée
d'un modèle VITS suit l'échelle de façon quasi linéaire. Après égalisation,
plus aucun fragment ne dépasse 12,8 — la voix ne file plus jamais.

Ce qui est déjà plus lent que la cible est laissé tel quel : on ne presse
jamais, on ne fait que ralentir.

### Vérifier une prononciation sans écouter

```bash
python3 voix.py --phonemes "Sur le LET 410, chaque kilo compte."
```

affiche le texte réécrit pour la bouche **et les sons que la synthèse
fabriquera**. C'est ce qui a permis de trouver le défaut du LET 410 signalé par
le patron (« il dit leté 410 ») :

| écrit | sons | entendu |
|---|---|---|
| `LET` | `lˈɛt` | « lette » — le sigle lu comme un mot |
| `L-E-T` | `ˈɛlˈətˈe` | « leté » — les lettres, mais **collées** |
| `L E T` | `ˈɛl ˈə tˈe` | « èl — eu — té » ✅ |

**Le trait d'union ne sépare pas, l'espace si.** Tous les sigles du tableau
`SIGLES` sont donc écrits avec des espaces. Trois caractères qui décidaient de
la crédibilité de tout le film.

### Le ton

Deux réglages du modèle commandent le timbre — `SOUFFLE` (la part d'aléa dans
la voix) et `VARIATION` (le naturel du débit). **Ils sont laissés à leur valeur
d'origine.** Le naturel qui manquait ne venait pas du timbre mais du phrasé :
la voix ne respirait pas aux virgules. C'est corrigé à la source, par le
découpage. Toucher au timbre par-dessus n'aurait fait que remplacer un défaut
par un autre.

### Ce que ce n'est pas

Ce n'est pas un comédien. Sur les phrases longues, cela s'entend. Le texte a
donc été écrit court et en phrases simples — ce qu'il faut de toute façon pour
une consigne. Un comédien coûterait plus que le film entier et devrait être
rappelé à chaque révision du GOM ; ici, on corrige une phrase du scénario et
tout se refait. Le jour où l'on veut une vraie voix, elle se substitue sans
rien changer d'autre : le montage cale déjà chaque image sur la durée du
fichier son qu'on lui donne.

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
python3 film.py tout          # les deux films, voix comprise (~35 min de calcul)
python3 film.py agence        # un seul
python3 film.py agence --muet # sans voix off
python3 texte.py              # les fiches et le relevé de la voix off
python3 voix.py --essai       # comparer les trois voix disponibles
```

Il faut `ffmpeg`, `python3-pil`, `numpy` et `piper-tts`. Les modèles de voix se
téléchargent une fois dans `.travail/voix/` :

```bash
python3 -m piper.download_voices fr_FR-tom-medium
```

### Où corriger quoi

| Ce qu'on veut changer | Le fichier |
|---|---|
| une phrase, un point, une durée, l'ordre des chapitres | **`scenarios.py`** |
| la mise en page, les couleurs, les types de cartes | `film.py` |
| la musique | `musique.py` |
| la voix, son allure, sa prononciation | `voix.py` |
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
