# Flyers MoheliGo

## Ce qui est prêt à utiliser

| Fichier | Format | Usage |
|---|---|---|
| `flyer-corporate-A4.png` | 2480 × 3508 (A4, 300 dpi) | Impression, affichage aux ports, dossier partenaires (hôtels, agences) |
| `flyer-corporate-facebook.png` | 2160 × 2700 (4:5) | Publication Facebook / Instagram (feed) |
| `flyer-nuit-facebook.png` | 2160 × 2700 (4:5) | Deuxième publication, fin de soirée (22h30 – minuit) |
| `flyer-affiche-facebook.png` | 2160 × 2700 (4:5) | Affiche « destination » — îlots de Nioumachoua (photo libre CC BY 3.0, crédit imprimé) |
| `flyer-affiche-vedette-facebook.png` | 2160 × 2700 (4:5) | Même affiche avec NOTRE photo (vedette en pleine mer) — aucun crédit à afficher |
| `flyer-promo-facebook.png` | 2160 × 2700 (4:5) | Flyer promo « affiche locale » (style Yas / compagnies locales) — le plus accrocheur |
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
- `flyer6-promo-fb.html` — flyer promo : diagonale, bulle de prix cerclée de
  blanc à cheval sur la coupe, trois cartes arrondies, bandeau des ports, bande
  d'action or à coins arrondis. Registre des affiches locales (Yas, compagnies
  aériennes) mais **aucune identité d'une autre marque n'est reprise** : nos
  couleurs, notre logo, nos formulations.
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
```

Le dernier argument est le facteur d'échelle : 1240 × 1754 CSS × 2 = A4 à
300 dpi exactement.

## Charte respectée

- Couleurs officielles du site : bleu `#1C4FA8`, marine `#0F2A5C`, or `#F6BC1C`.
- Aucun emoji (consigne du patron) : uniquement des icônes SVG dessinées.
- Logo Facebook officiel (f blanc sur `#1877F2`), logo WhatsApp officiel.
- Vedette orientée vers Mohéli et alignée sur la ligne de liaison.
- Aucun chiffre inventé : seuls des faits vérifiables (tarif indicatif
  15 000 FC, 4 ports, météo 7 jours, 2 minutes pour réserver).
- Photos sous licence libre : crédit imprimé sur le support et consigné dans
  `../photos-cc/CREDITS.md`. Jamais de personne identifiable sans accord.
