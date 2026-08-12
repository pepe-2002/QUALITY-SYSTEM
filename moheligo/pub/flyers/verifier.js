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

// Les blocs DÉCORATIFS, qui ont le droit de passer sous les autres — c'est leur
// travail. Ne pas les ignorer donne des faux signalements (vécu le 12/08/2026
// sur le ruban doré du flyer de mardi, un visuel déjà validé par le patron).
const IGNORE = ['eclat', 'coin', 'fond', 'halo', 'ruban', 'vague', 'lueur'];

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
      // ⚠️ el.className sur un <svg> renvoie un objet SVGAnimatedString, pas une
      // chaine : « [object SVGAnimatedString] ». D'ou getAttribute('class'), qui
      // marche pour les deux. Sans ca, aucun SVG ne pouvait etre ignore.
      const nom = (el.getAttribute('class') || '').trim().split(/\s+/)[0]
        || el.tagName.toLowerCase();
      if (ignore.includes(nom)) return;
      const r = el.getBoundingClientRect();
      if (r.width < 2 || r.height < 2) return;
      // Deux blocs de TEXTE qui se croisent = un defaut, toujours. Un bloc de
      // texte sous une image ou un dessin = une superposition, souvent voulue
      // (un personnage qui passe devant un titre, une photo derriere un pied de
      // page). Le contrôleur doit dire lequel des deux il a trouve, sinon on
      // apprend a ignorer ses alertes — et un voyant qu'on ignore ne sert plus.
      // On releve les rectangles de l'ENCRE, pas ceux des boites : un texte pose
      // dans la partie vide d'un autre bloc n'est pas un defaut, alors que deux
      // boites qui se croisent, oui, tres souvent. Sans cette distinction le
      // controleur criait au loup sur des visuels que le patron a deja publies.
      const encre = [];
      const marche = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      for (let n = marche.nextNode(); n; n = marche.nextNode()) {
        if (!n.textContent.trim()) continue;
        const p = document.createRange();
        p.selectNodeContents(n);
        for (const t of p.getClientRects()) {
          if (t.width > 1 && t.height > 1) encre.push(t);
        }
      }
      const lignes = encre.map((t) => ({ x: t.x, y: t.y, w: t.width, h: t.height }));
      out.push({ nom, texte: lignes.length > 0, lignes,
                 x: r.x, y: r.y, w: r.width, h: r.height });
    });
    return out;
  }, IGNORE);

  const ennuis = [];          // de vrais defauts : deux textes qui se croisent
  const superpositions = [];  // a l'oeil du patron : image sur texte, souvent voulu
  for (const b of blocs) {
    // Un dessin qui deborde volontairement du cadre est normal (le cadre est en
    // overflow:hidden, il est coupe proprement). Ce qui n'est jamais normal,
    // c'est du TEXTE coupe : on ne signale que celui-la.
    if (!b.texte) continue;
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
        const ou = `.${a.nom} et .${b.nom} sur ${dx.toFixed(0)} x ${dy.toFixed(0)} px`;
        const croise = (u, v) =>
          Math.min(u.x + u.w, v.x + v.w) - Math.max(u.x, v.x) > 0.5 &&
          Math.min(u.y + u.h, v.y + v.h) - Math.max(u.y, v.y) > 0.5;
        const encreSurEncre = a.lignes.some((l) => b.lignes.some((m) => croise(l, m)));
        if (encreSurEncre) ennuis.push(`DEUX TEXTES SE CROISENT : ${ou}`);
        else if (a.texte && b.texte) superpositions.push(
          `boites croisees mais aucune ligne ne se touche : ${ou}`);
        else superpositions.push(`superposition (image ou dessin) : ${ou}`);
      }
    }
  }

  console.log(`${blocs.length} blocs examinés dans ${path.basename(fichier)} :`);
  blocs.forEach((b) => console.log(`  .${b.nom.padEnd(12)} y ${b.y.toFixed(0).padStart(5)}` +
    ` → ${(b.y + b.h).toFixed(0).padStart(5)}   hauteur ${b.h.toFixed(0)}`));
  console.log('');
  superpositions.forEach((e) => console.log('· ' + e));
  if (ennuis.length === 0) {
    console.log(superpositions.length
      ? `RIEN À SIGNALER : aucun texte ne se croise (${superpositions.length} superposition(s) d'image, a juger a l'oeil).`
      : 'RIEN À SIGNALER : aucun chevauchement, rien hors du cadre.');
  } else {
    ennuis.forEach((e) => console.log('⛔ ' + e));
  }
  await nav.close();
  process.exit(ennuis.length ? 1 : 0);
})();
