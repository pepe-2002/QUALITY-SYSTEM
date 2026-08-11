# Flyers MoheliGo

## Ce qui est prêt à utiliser

| Fichier | Format | Usage |
|---|---|---|
| `flyer-corporate-A4.png` | 2480 × 3508 (A4, 300 dpi) | Impression, affichage aux ports, dossier partenaires (hôtels, agences) |
| `flyer-corporate-facebook.png` | 2160 × 2700 (4:5) | Publication Facebook / Instagram (feed) |
| `flyer-nuit-facebook.png` | 2160 × 2700 (4:5) | Deuxième publication, fin de soirée (22h30 – minuit) |
| `flyer-affiche-facebook.png` | 2160 × 2700 (4:5) | Affiche « destination » — îlots de Nioumachoua (photo libre CC BY 3.0, crédit imprimé) |
| `flyer-affiche-vedette-facebook.png` | 2160 × 2700 (4:5) | Même affiche avec NOTRE photo (vedette en pleine mer) — aucun crédit à afficher |
| `flyer-affiche-vraie-facebook.png` | 2160 × 2700 (4:5) | **⭐⭐⭐ CELLE À UTILISER** — mer en **couleurs réelles**, soleil à rayons, bande de papier crème en pied |
| `flyer-affiche-lumineuse-facebook.png` | 2160 × 2700 (4:5) | Version duotone claire (mer recolorée), conservée |
| `flyer-affiche-duotone-facebook.png` | 2160 × 2700 (4:5) | La même en version sombre (marine dominante), conservée |
| `flyer-soir-facebook.png` | 2160 × 2700 (4:5) | **⭐ BULLETIN DU SOIR** — la mer réelle de demain matin, généré depuis Open-Meteo. **Format daté : à regénérer chaque jour.** |
| `flyer-promo-brillant-facebook.png` | 2160 × 2700 (4:5) | Promo « brillant » (or métallique, reflets, lumière) — intemporel |
| `flyer-promo-brillant-A4.png` | 2480 × 3508 (A4, 300 dpi) | Le brillant en A4 imprimable, avec « comment ça marche » |
| `flyer-promo-facebook.png` | 2160 × 2700 (4:5) | Promo version mate (avant la passe brillance), conservée |
| `flyer-promo-A4.png` | 2480 × 3508 (A4, 300 dpi) | Le même en A4 imprimable, avec la bande « comment ça marche » — ports, boutiques, hôtels |
| `flyer-moheligo.png` | 2160 × 2700 (4:5) | Première version (août 2026), conservée |

Texte de publication Facebook associé : `../textes-publications.md`,
section « Flyer corporate ».

## Sources

- `flyer2-corporate.html` — flyer institutionnel A4 (en-tête, bandeau,
  réseau des 4 ports, 6 services numérotés, chiffres clés, pied avec QR).
- `flyer2-corporate-fb.html` — la même identité en format feed 4:5, moins
  d'éléments et typographie plus grosse (lisible sur téléphone).
- `flyer3-nuit-fb.html` — version nuit (fond marine, message « réservez ce
  soir, partez demain », encart diaspora). Photo : `horizon-nuit.jpg`, obtenue
  par `nuit.py` (étalonnage nocturne de `../photos/horizon.jpg` : bascule bleu
  nuit, étoiles, lune et reflet — aucune photo de nuit n'existait).
- `flyer4-affiche-fb.html` — affiche « destination » : photo en bandeau haut,
  typographie en bas. Photo : `nioumachoua-affiche.jpg` (étalonnage de
  `../photos-cc/nioumachoua-ilot-fatima.jpg` — Fatima771, CC BY 3.0, crédit
  imprimé sur l'affiche, voir `../photos-cc/CREDITS.md`).
- `flyer5-affiche-vedette-fb.html` — même affiche avec `vedette-affiche.jpg`
  (notre photo de vedette en pleine mer) : aucune licence, aucun crédit.
- ⚠️ **Aucune personne sur les visuels** (consigne du patron du 06/08/2026,
  droit à l'image). La première affiche, tirée d'une photo montrant un jeune de
  dos, a été retirée.
- `flyer6-promo-fb.html` — flyer promo, version feed. Registre des affiches
  locales (Yas, compagnies aériennes) mais **aucune identité d'une autre marque
  n'est reprise** : nos couleurs, notre logo, nos formulations. Design :
  découpe basse en **vague SVG**, bloc surligneur or sous l'accroche, bulle de
  prix cerclée de la couleur du fond, cartes blanches ombrées à pastilles or,
  gélule des ports, bande d'action or avec **vrai bouton** et flèche.
- `flyer6-promo-A4.html` — le même en A4 300 dpi, avec en plus la bande
  « comment ça marche » en trois étapes (sur du papier, les gens lisent).
- **`flyer7-promo-brillant-fb.html`** — la version la plus aboutie : même mise
  en page que le promo, plus la passe « brillance » (voir la recette ci-dessous).
- **`flyer7-promo-brillant-A4.html`** — le brillant en A4. Construit à partir de
  `flyer6-promo-A4.html` + une **feuille de surcharge** en fin de `<style>`
  (section « BRILLANCE ») : la mise en page A4 reste maintenue à un seul endroit.
- **`flyer8-soir-fb.template.html` + `bulletin.py`** — le bulletin du soir.
  `bulletin.py` interroge Open-Meteo (marine + vent) sur le couloir
  Ouroveni–Hoani, calcule l'état de la mer sur l'échelle de Douglas, construit
  la courbe de houle 5h-13h, remplit le gabarit et écrit `flyer8-soir-fb.html`
  (fichier **généré**, ne pas le modifier à la main) + `bulletin.json`.
- `soir.py` — étalonnage « fin de journée » de `../photos/vedette-mer.jpg`
  (ciel de crépuscule, soleil bas, chemin de lumière, bloom) → `vedette-soir.jpg`.
- `flyer1.html` — première version.
- `render.js` — HTML/CSS → PNG haute résolution (Chromium).
- `fonts/` — Montserrat + Inter en woff2 (latin/latin-ext), locales : aucun
  appel réseau au rendu, donc rendu identique d'une session à l'autre.
- `logo-lockup.png` / `logo-emblem.png` — logo officiel détouré (recadré sur
  le contenu) et emblème seul, extraits de `../../MoheliGo-logo.png`.
- `qr-moheligo.png` — QR vers https://moheligo.com (correction d'erreur H).

## Regénérer

### La page que le patron ouvre

```bash
python3 bulletin.py                                                    # la mer de demain
node render.js flyer8-soir-fb.html flyer-soir-facebook.png 1080 1350 2
python3 page.py --sortie /tmp/page.html                                # la page complète
```

`page.py` regénère **toute** la page : météo de demain (Open-Meteo terre + mer),
puis chaque flyer en grand avec son texte et un bouton « copier ». Les images
sont converties en JPEG 1080 px avant d'être embarquées — le patron est sur un
téléphone, pas question d'y mettre des PNG de 2,6 Mo.
Puis publier le fichier comme artifact : republier le même chemin garde la même
adresse, donc **le patron n'a qu'un seul lien à retenir**.

⚠️ **Ne jamais retoucher la page à la main.** Elle a été rapiécée une fois par
recherche-remplacement, et le découpage a effacé deux blocs sans prévenir. Pour
changer quelque chose : modifier `page.py` (la liste `FLYERS` en haut) et
relancer.

### Le tuyau : le bulletin se refait tout seul

`.github/workflows/bulletin-du-soir.yml` fait tourner ces deux commandes sur un
serveur GitHub **chaque jour à 16h, heure des Comores**, et dépose le résultat
sur la branche `bulletin-du-jour`. Deux adresses fixes, toujours à jour :

- le visuel : `github.com/pepe-2002/QUALITY-SYSTEM/blob/bulletin-du-jour/flyer-soir-facebook.png`
- le texte : `github.com/pepe-2002/QUALITY-SYSTEM/blob/bulletin-du-jour/texte-du-jour.txt`

La branche est réécrite à chaque exécution (un seul commit) : le dépôt ne
grossit pas. ⚠️ **Une tâche planifiée ne tourne que depuis la branche par
défaut** : le fichier doit être fusionné dans `main` pour que l'horaire
s'applique. Avant ça, seul le bouton « Run workflow » de l'onglet Actions
fonctionne.

### Le bulletin du soir, à la main

```bash
cd moheligo/pub/flyers
python3 bulletin.py                                                   # va chercher la mer de demain
node render.js flyer8-soir-fb.html flyer-soir-facebook.png 1080 1350 2
```

`python3 bulletin.py --jour 2` pour après-demain. La photo `vedette-soir.jpg`
est déjà générée : relancer `soir.py` seulement si on change de photo (compter
une minute, les filtres tournent sur du 2560×1920).

### Tout le reste

```bash
cd moheligo/pub/flyers
node render.js flyer2-corporate.html    flyer-corporate-A4.png       1240 1754 2
node render.js flyer2-corporate-fb.html flyer-corporate-facebook.png 1080 1350 2
python3 nuit.py   # regénère horizon-nuit.jpg (déterministe, random.seed(7))
node render.js flyer3-nuit-fb.html      flyer-nuit-facebook.png      1080 1350 2
python3 affiche.py   # regénère nioumachoua-affiche.jpg et vedette-affiche.jpg
node render.js flyer4-affiche-fb.html         flyer-affiche-facebook.png         1080 1350 2
node render.js flyer5-affiche-vedette-fb.html flyer-affiche-vedette-facebook.png 1080 1350 2
node render.js flyer6-promo-fb.html           flyer-promo-facebook.png           1080 1350 2
node render.js flyer6-promo-A4.html           flyer-promo-A4.png                 1240 1754 2
```

Le dernier argument est le facteur d'échelle : 1240 × 1754 CSS × 2 = A4 à
300 dpi exactement.

## Système de design (à réutiliser tel quel)

- **Typographie d'affiche : `Archivo` 800/900** pour tout le display (titres,
  prix, `moheligo.com`, boutons, noms de ports) et `Inter` pour le texte
  courant. Archivo remplace Montserrat depuis le 06/08/2026 : le patron voulait
  « une écriture façon pro » — Archivo est plus sèche, plus éditoriale, moins
  « gabarit ». ⚠️ Elle est **plus large** que Montserrat : à taille égale le
  titre déborde. Compter environ 71-78 px là où Montserrat tenait à 84-90 px.
- Registre « pro » : plate de titre **droite** (aucune rotation), rayons
  resserrés (18 px sur les cartes, 28 px sur la bande d'action), interlettrage
  des petites capitales à 1,8-2,4 px maximum, fond clair **froid** (pas de halo
  crème).
- Couleurs : marine `#0F2A5C`, or `#F6BC1C`, fond clair `#F3F7FE`, marine
  profonde `#081833` pour les photos, gris texte `#5C6E8B`.
- Rayons : 20 (petits blocs), 26-30 (cartes), 44-52 (bande d'action), 999
  (gélules et pastilles).
- Ombres, trois niveaux seulement : `0 14px 34px rgba(15,42,92,.14)` (cartes),
  `0 22px 48px rgba(8,24,51,.32)` (éléments sur photo), `0 8px 18px` (pastilles).
- Profondeur du fond clair : halo doré en `radial-gradient` + trame d'ondes SVG
  à 5,5 % d'opacité. Sans ça, le blanc paraît plat à l'impression comme à
  l'écran.
- Découpe photo → fond : **vague SVG** remplie de la couleur du fond (pas un
  simple `clip-path` droit), la vague fait tout de suite « maritime ».
- Un élément posé à cheval sur deux fonds (la bulle de prix) porte un anneau de
  la couleur du fond : `box-shadow:0 0 0 10px var(--paper)`.
- Titre surligné : `<span>` en `position:relative` + `::before` en or, légèrement
  tourné (`rotate(-1.1deg)`), `z-index:-1`, texte en marine par-dessus.

## Le bulletin du soir : ce qui le rend impossible à copier

- Deux éléments **pilotés par la donnée**, pas dessinés : la jauge d'état de la
  mer (5 segments, échelle de Douglas) et la courbe de houle heure par heure
  (chemin SVG calculé par `bulletin.py`, avec aire dégradée et points tous les
  deux pas). Si la mer change, le flyer change tout seul.
- Un **panneau en verre dépoli** posé sur la photo : `backdrop-filter:blur(18px)
  saturate(1.25)` + fond marine translucide + liseré blanc intérieur. Le fond
  translucide est indispensable : sans lui, le texte blanc devient illisible dès
  que le panneau déborde sur une zone claire.
- Une photo **étalonnée fin de journée** (`soir.py`), pas un filtre orange.
- ⚠️ Deux garde-fous non négociables : la **mention de source** et le rappel que
  **le bulletin officiel fait foi**. On publie une prévision, pas une promesse.
- ⚠️ **Le PNG publié ne change jamais tout seul** — c'est une image. Ce qui est
  automatique, c'est sa *fabrication* : `bulletin.py` va chercher les données du
  jour et refait le fichier. Il faut donc le relancer et republier chaque jour.
- ⚠️ Piège de code : dans `bulletin.py`, la virgule décimale française ne
  s'applique **qu'aux valeurs affichées**, jamais au fragment SVG entier — un
  `.replace('.', ',')` sur tout le fragment casse les coordonnées (`x="194,0"`)
  et l'étiquette part dans le coin.
- ⚠️ **Mer régulière (11/08/2026)** : quand la houle bouge de moins d'un
  décimètre sur la matinée, l'ancien affichage donnait « 0,9–0,9 m » et « de
  0,9 m à 0,9 m » — juste, mais ça se lit comme un bug. `bulletin.py` compare
  maintenant les deux valeurs arrondies et bascule sur
  **« 0,9 m · HOULE RÉGULIÈRE 5H-13H »** / « régulière, autour de 0,9 m ».
  Les jetons du gabarit sont `{{AMPLI}}` et `{{AMPLI_LAB}}` (plus de
  `{{HMIN}}`/`{{HMAX}}`). Règle générale : **nommer la situation plutôt que
  répéter le chiffre.**

## L'affiche duotone : ce que dit la recherche sur les belles affiches

Recherche du 08/08/2026 (tendances graphiques 2026 + principes de l'affiche de
voyage), appliquée dans `flyer10-affiche-duotone-fb.html` + `duotone.py` :

1. **Duotone, deux couleurs et rien d'autre.** Réduire une photo à deux teintes
   force la clarté graphique : les silhouettes deviennent des formes. Le couple
   **marine + or** est le registre « sophistiqué » du duotone — et c'est notre
   charte. Technique : *gradient map*, la luminance de chaque pixel sert d'index
   dans une rampe de 256 couleurs (marine → bleu → or → crème).
2. **Une seule idée.** Les affiches de voyage qui ont traversé le siècle disent
   une chose, elles ne récitent pas une fiche produit. Ici : le nom de l'île,
   énorme. Pas de pastille, pas de bulle de prix, pas de cartes.
3. **Composition en tiers, rien de centré.** Ciel doré en haut, horizon au
   tiers, le nom posé sur la mer, les informations au dernier tiers.
4. **Le blanc est actif** : marges de 64 px tenues partout, et une grande zone
   vide assumée sous le titre.
5. **Grain.** Un bruit monochrome léger en mode incrustation : ça enlève le côté
   « fait à l'ordinateur », et ça masque l'agrandissement d'une photo un peu
   petite (avantage secondaire très pratique).
6. **Un signe graphique, un seul** : l'anneau de soleil au tracé fin, clin d'œil
   aux affiches des années 50 — devenu un **sceau** sur l'idée du patron :
   l'emblème du navire, en silhouette marine, posé au centre de l'anneau dans le
   ciel doré (double filet, emblème à 196 px, opacité 0,92). C'est la signature
   visuelle de l'affiche, et le logo est enfin grand.
   ⚠️ Deux pièges rencontrés :
   - `logo-emblem.png` a un **fond blanc opaque**, pas transparent. Repeindre
     « tous les pixels visibles » donne un rectangle plein. Il faut construire la
     silhouette depuis la **luminance** (plus sombre = plus opaque) → d'où
     `logo-emblem-marine.png` (fonds clairs) et `logo-emblem-creme.png` (fonds
     sombres), tous deux à fond réellement transparent.
   - L'emblème ne doit apparaître **qu'une fois** : il a été retiré de l'en-tête
     quand le sceau est arrivé, sinon la marque se répète.

## « La mer doit être vraie » (09/08/2026)

Le duotone est beau mais il **recolore la mer** — et le patron veut la vraie.
D'où `flyer12-affiche-vraie-fb.html`, qui garde toute la mise en page (sceau
solaire, un seul grand mot, tiers, marges) mais sur une photo en **couleurs
réelles** : `affiche.py → plein_cadre()` ne fait que recadrer en 4:5, remonter
la netteté et poser un grain léger — aucun mappage de couleurs.

Ce que ça impose en plus : sur du sable orange vif, un texte marine se noie.
La solution est celle des vraies affiches de voyage — **une bande de papier
crème en pied de page** (196 px, `#FFF9E8`) qui porte l'adresse, la ligne de
services et le QR. Le titre remonte au-dessus, sur la limite mer/sable, avec un
voile crème progressif. Personne ne lutte plus contre la photo.

⚠️ Piège rencontré : `affiche.py` n'avait **pas** de garde
`if __name__ == '__main__'`, donc un simple `import affiche` relançait tout
l'étalonnage — et mes deux `replace` sur ce fichier n'avaient rien remplacé
(motifs indentés qui n'existaient pas), sans le moindre message. Le garde-fou
est en place ; et un `assert` avant réécriture évite les remplacements muets.

## Faire une affiche LUMINEUSE (demande du 09/08/2026)

Le patron : « ça doit être lumineux ». La version sombre était belle mais la mer
marine mangeait tout. Ce qui a marché — dans `flyer11-affiche-lumineuse-fb.html`
et la fonction `terminer_clair()` de `duotone.py` :

1. **Une rampe duotone claire** (`RAMPE_CLAIRE`) : les ombres ne descendent
   jamais dans le noir (marine doux `#0E2854`), les tons moyens passent par
   l'aigue-marine, les hautes lumières montent au crème `#FFFCF2`.
   Plus une correction gamma 0,88 qui remonte les basses lumières.
2. **Un voile clair sur les bords au lieu d'un vignettage sombre.** C'est le
   geste qui change tout : la lumière sort du cadre au lieu d'y être enfermée.
3. **Bloom généreux** sur les hautes lumières (seuil 170, flou 2,2 % de la
   largeur, écran à 92/255).
4. **Le sceau devient le soleil** : `repeating-conic-gradient` pour l'éventail
   de rayons, éteint par un `mask-image` radial (trou au centre, extinction à
   52 %). Un halo radial chaud par-dessus.
5. **La typographie passe en marine sur fond clair.** La lumière vient du
   contraste, pas de l'ajout de blanc : un titre crème sur fond clair
   disparaîtrait.
⚠️ **Deux allers-retours pour trouver le point juste** :
- 1ᵉʳ essai trop délavé (voile 210, contraste 1,10, gamma 0,78) : les îlots
  avaient disparu ;
- 2ᵉ essai « trop lumineux » selon le patron (voile 140, contraste 1,22) ;
- **réglage retenu** : voile de bord 74, bloom 62/255, contraste 1,30,
  gamma 0,96, rampe aux ombres plus profondes, et voile crème du bas à
  0,26/0,48/0,62 pour que le texte marine reste lisible sur le sable.
**Leçon** : « lumineux » ne veut pas dire « pâle ». La lumière tient à la
présence des ombres autant qu'à celle des hautes lumières.

## La recette « ça brille » (demande du patron : niveau designer pro)

Huit gestes, tous dans `flyer7-promo-brillant-fb.html` :

1. **L'or n'est jamais plat** : dégradé 4 arrêts `#FFE595 → #FBC93C → #F0AE0B →
   #D89A05` en 142°, + liseré blanc intérieur en haut
   (`inset 0 2px 0 rgba(255,255,255,.62)`) + ombre chaude intérieure en bas
   (`inset 0 -7px 16px rgba(160,102,0,.26)`). C'est ce couple liseré/ombre qui
   fait « objet verni » et non « aplat jaune ».
2. **Reflet spéculaire** : un `::before` en `radial-gradient` blanc flouté sur
   le haut de la bulle et des pastilles d'icônes.
3. **Balayage de lumière** : un `::after` en bande blanche diagonale floutée
   (`rotate(16-20deg)`, `blur`) sur la bande d'action, les cartes et le badge.
4. **Marine métallique** pour les boutons et gélules :
   `linear-gradient(180deg,#1B4A8E,#12356D,#0B2149)` + liseré blanc intérieur.
5. **Soleil sur la mer** : halo `radial-gradient` chaud + deux faisceaux
   obliques en `mix-blend-mode:screen` + une série d'ellipses claires
   (les étincelles sur l'eau).
6. **Crête de vague dorée** : le tracé de la vague est dessiné deux fois — une
   fois rempli de la couleur du fond, une fois en `stroke` avec un dégradé or
   qui s'éteint aux deux bords.
7. **Texte rempli d'un dégradé** : `background-clip:text` + `color:transparent`
   sur le grand titre, le prix et `moheligo.com`, avec
   `drop-shadow(0 2px 0 rgba(255,255,255,.45))` pour l'arête lumineuse.
8. 🚫 **PAS d'éclats ni de petites étoiles.** Essayés le 06/08/2026, refusés
   par le patron : « ça fait enfants et femme ». La brillance doit venir de la
   matière (dégradés, liserés, reflets), jamais d'un décor ajouté.

⚠️ À l'impression, exiger le PNG d'origine : un fichier passé par WhatsApp ou
Facebook perd les dégradés (bandes visibles dans l'or) et les reflets fins.

## Charte respectée

- Couleurs officielles du site : bleu `#1C4FA8`, marine `#0F2A5C`, or `#F6BC1C`.
- Aucun emoji (consigne du patron) : uniquement des icônes SVG dessinées.
- Logo Facebook officiel (f blanc sur `#1877F2`), logo WhatsApp officiel.
- Vedette orientée vers Mohéli et alignée sur la ligne de liaison.
- Aucun chiffre inventé : seuls des faits vérifiables (tarif indicatif
  15 000 FC, 4 ports, météo 7 jours, 2 minutes pour réserver).
- Photos sous licence libre : crédit imprimé sur le support et consigné dans
  `../photos-cc/CREDITS.md`. Jamais de personne identifiable sans accord.
