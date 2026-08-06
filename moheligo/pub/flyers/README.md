# Flyers MoheliGo

## Ce qui est prêt à utiliser

| Fichier | Format | Usage |
|---|---|---|
| `flyer-corporate-A4.png` | 2480 × 3508 (A4, 300 dpi) | Impression, affichage aux ports, dossier partenaires (hôtels, agences) |
| `flyer-corporate-facebook.png` | 2160 × 2700 (4:5) | Publication Facebook / Instagram (feed) |
| `flyer-moheligo.png` | 2160 × 2700 (4:5) | Première version (août 2026), conservée |

Texte de publication Facebook associé : `../textes-publications.md`,
section « Flyer corporate ».

## Sources

- `flyer2-corporate.html` — flyer institutionnel A4 (en-tête, bandeau,
  réseau des 4 ports, 6 services numérotés, chiffres clés, pied avec QR).
- `flyer2-corporate-fb.html` — la même identité en format feed 4:5, moins
  d'éléments et typographie plus grosse (lisible sur téléphone).
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
