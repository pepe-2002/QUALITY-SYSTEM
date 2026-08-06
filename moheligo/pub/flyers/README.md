# Flyers MoheliGo

## Ce qui est prêt à utiliser

| Fichier | Format | Usage |
|---|---|---|
| `flyer-corporate-A4.png` | 2480 × 3508 (A4, 300 dpi) | Impression, affichage aux ports, dossier partenaires (hôtels, agences) |
| `flyer-corporate-facebook.png` | 2160 × 2700 (4:5) | Publication Facebook / Instagram (feed) |
| `flyer-nuit-facebook.png` | 2160 × 2700 (4:5) | Deuxième publication, fin de soirée (22h30 – minuit) |
| `flyer-affiche-facebook.png` | 2160 × 2700 (4:5) | Affiche « destination » — îlots de Nioumachoua (photo libre CC BY 3.0, crédit imprimé) |
| `flyer-affiche-vedette-facebook.png` | 2160 × 2700 (4:5) | Même affiche avec NOTRE photo (vedette en pleine mer) — aucun crédit à afficher |
| `flyer-promo-brillant-facebook.png` | 2160 × 2700 (4:5) | **⭐ LE PLUS ABOUTI** — promo « brillant » (or métallique, reflets, lumière) |
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
- `flyer1.html` — première version.
- `render.js` — HTML/CSS → PNG haute résolution (Chromium).
- `fonts/` — Montserrat + Inter en woff2 (latin/latin-ext), locales : aucun
  appel réseau au rendu, donc rendu identique d'une session à l'autre.
- `logo-lockup.png` / `logo-emblem.png` — logo officiel détouré (recadré sur
  le contenu) et emblème seul, extraits de `../../MoheliGo-logo.png`.
- `qr-moheligo.png` — QR vers https://moheligo.com (correction d'erreur H).

## Regénérer

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
8. **Éclats** (petites étoiles à quatre branches) posés **à la main**, jamais en
   semis : un gros près du titre, deux moyens autour de la bulle, un petit en
   contrepoint. Au-delà de quatre, ça fait sapin de Noël.

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
