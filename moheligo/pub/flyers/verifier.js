// LE CONTRÔLEUR DE MISE EN PAGE — ce que l'œil ne voit pas.
//
//     node verifier.js flyer31-suspension-fb.html
//
// À quoi ça sert : nos flyers sont en positionnement absolu (chaque bloc a son
// `top`). Quand un titre s'allonge d'une ligne, il passe SOUS le bloc suivant
// au lieu de le pousser — et selon les couleurs, un recouvrement de 6 px ne se
// voit pas à l'écran, mais se voit sur un téléphone. C'est arrivé trois fois
// (dimanche, lundi, vendredi) et une quatrième sur l'avis de grosse mer.
//
// Ce script ouvre le HTML dans le vrai Chromium et compare les rectangles des
// blocs de premier niveau de `.page` : il signale ce qui se chevauche et ce qui
// sort du cadre 1080 x 1350. Les fonds décoratifs (.eclat) et le coin blanc
// (.coin, volontairement par-dessus tout) sont ignorés.
//
// ⚠️ Un flyer qui sort d'ici « RIEN À SIGNALER » n'est pas pour autant beau :
// ça dit seulement qu'il n'est pas cassé. Le regard du patron reste le juge.
// Playwright : celui du projet s'il existe, sinon celui de la session (comme render.js)
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const fs = require('fs');
const path = require('path');

const IGNORE = ['eclat', 'coin', 'fond', 'halo'];

(async () => {
  const fichier = process.argv[2];
  if (!fichier) { console.error('usage: node verifier.js <fichier.html>'); process.exit(2); }

  const local = '/opt/pw-browsers/chromium';
  const nav = await chromium.launch(
    fs.existsSync(local) ? { executablePath: local } : {});
  const page = await nav.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.resolve(fichier));
  await page.evaluate(() => document.fonts.ready);

  const blocs = await page.evaluate((ignore) => {
    const out = [];
    document.querySelectorAll('.page > *').forEach((el) => {
      const nom = el.className.toString().split(' ')[0] || el.tagName.toLowerCase();
      if (ignore.includes(nom)) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      out.push({ nom, x: r.x, y: r.y, w: r.width, h: r.height });
    });
    return out;
  }, IGNORE);

  const ennuis = [];
  for (const b of blocs) {
    if (b.y < -0.5 || b.x < -0.5 || b.x + b.w > 1080.5 || b.y + b.h > 1350.5) {
      ennuis.push(`DÉBORDE du cadre : .${b.nom} occupe ` +
        `x ${b.x.toFixed(0)}→${(b.x + b.w).toFixed(0)}, y ${b.y.toFixed(0)}→${(b.y + b.h).toFixed(0)}`);
    }
  }
  for (let i = 0; i < blocs.length; i++) {
    for (let j = i + 1; j < blocs.length; j++) {
      const a = blocs[i], b = blocs[j];
      const dx = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
      const dy = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
      if (dx > 0.5 && dy > 0.5) {
        ennuis.push(`SE CHEVAUCHENT : .${a.nom} et .${b.nom} ` +
          `sur ${dx.toFixed(0)} x ${dy.toFixed(0)} px`);
      }
    }
  }

  console.log(`${blocs.length} blocs examinés dans ${path.basename(fichier)} :`);
  blocs.forEach((b) => console.log(`  .${b.nom.padEnd(12)} y ${b.y.toFixed(0).padStart(5)}` +
    ` → ${(b.y + b.h).toFixed(0).padStart(5)}   hauteur ${b.h.toFixed(0)}`));
  console.log('');
  if (ennuis.length === 0) {
    console.log('RIEN À SIGNALER : aucun chevauchement, rien hors du cadre.');
  } else {
    ennuis.forEach((e) => console.log('⛔ ' + e));
  }
  await nav.close();
  process.exit(ennuis.length ? 1 : 0);
})();
