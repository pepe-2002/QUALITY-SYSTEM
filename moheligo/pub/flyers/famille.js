#!/usr/bin/env node
/* ⬛ LA FAMILLE — est-ce qu'un visuel ressemble aux autres ? — 02/09/2026.
 *
 *     NODE_PATH=/opt/node22/lib/node_modules node famille.js flyer48-traversee-fb.html
 *     NODE_PATH=/opt/node22/lib/node_modules node famille.js --tous
 *
 * Le patron : « tous les flyers excepté ceux du bulletin doivent avoir des
 * points communs et se ressembler, genre être reconnaissables. »
 *
 * 🚩 CE QUE LA MESURE A TROUVÉ LE JOUR MÊME : nos neuf visuels hors bulletin
 * utilisaient TROIS structures différentes, et le titre changeait de hauteur
 * d'un visuel à l'autre — en haut, au milieu, sous la photo. Mis côte à côte on
 * ne voyait pas une marque, on voyait trois marques qui partagent une couleur.
 *
 * 📌 **LA COULEUR ET LA POLICE NE FONT PAS UNE FAMILLE : LA STRUCTURE LA FAIT.**
 * Deux affiches du même bleu avec la même police, mais dont l'une pose son titre
 * en haut et l'autre au milieu, se ressemblent moins que deux affiches de
 * couleurs différentes bâties pareil. L'œil reconnaît une DISPOSITION avant de
 * reconnaître une teinte — c'est pour ça qu'on identifie une page de journal à
 * dix mètres sans lire un mot.
 *
 * ⚖️ LA GRAMMAIRE, TELLE QU'ELLE EST MESURÉE ICI. Elle vient de `flyer48`, le
 * gabarit validé, et elle tient en cinq points. Ce sont des points de STRUCTURE :
 * on ne vérifie ni les mots, ni les couleurs (§ 2 et § 6 s'en chargent).
 *
 *   1. UNE PHOTO EN BANDEAU HAUT, pleine largeur, collée au bord supérieur.
 *      C'est la règle du patron : tout sauf le bulletin porte une photo.
 *   2. LA VAGUE D'OR EN COUTURE, à la frontière photo / marine. C'est notre
 *      seule forme propriétaire, et c'est elle qui nous rend reconnaissables
 *      sans logo.
 *   3. LE TITRE SOUS LA PHOTO, jamais dessus. Poser du texte sur une image, ce
 *      n'est pas notre grammaire : l'image parle, puis les mots parlent.
 *   4. TOUT ALIGNÉ SUR LA MÊME MARGE DE GAUCHE (76 px) — surtitre, titre, corps
 *      et appel à l'action. Une seule verticale, c'est ce que l'œil suit.
 *   5. LE PIED PARTAGÉ : appel à l'action à gauche, adresse à droite, sur la
 *      même ligne d'horizon.
 *
 * ⚠️ CE PROGRAMME NE REFUSE PAS, IL DÉCRIT. Un visuel peut sortir de la
 * grammaire pour une bonne raison (l'écran de l'appli du mercredi est un objet
 * vertical, il ne rentre pas dans un bandeau). Ce qu'on ne veut pas, c'est en
 * sortir SANS S'EN APERCEVOIR. Il donne donc une note sur 5 et dit ce qui manque.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const MARGE = 76;
const TOL = 8;              // px de tolérance sur les alignements

async function examiner(nav, fichier) {
  const page = await nav.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.resolve(fichier));
  await page.evaluate(() => document.fonts.ready);

  const r = await page.evaluate(({ MARGE, TOL }) => {
    const boite = (sel) => {
      const el = document.querySelector(sel);
      if (!el) return null;
      const b = el.getBoundingClientRect();
      return { g: Math.round(b.left), d: Math.round(b.right),
               h: Math.round(b.top), b: Math.round(b.bottom) };
    };

    // --- 1. la photo en bandeau haut ---------------------------------------
    // On cherche la plus grande image qui touche le bord supérieur et couvre
    // toute la largeur. L'emblème du coin blanc est exclu : il est minuscule.
    let bandeau = null;
    for (const img of document.querySelectorAll('img')) {
      const b = img.getBoundingClientRect();
      if (b.width < 1000 || b.top > 4) continue;
      if (!bandeau || b.height > bandeau.b - bandeau.h) {
        bandeau = { g: Math.round(b.left), d: Math.round(b.right),
                    h: Math.round(b.top), b: Math.round(b.bottom) };
      }
    }
    // le conteneur peut recadrer l'image : on prend le plus petit des deux
    const cadre = document.querySelector('.mer, .photo, .haut');
    if (bandeau && cadre) {
      const c = cadre.getBoundingClientRect();
      if (c.top <= 4 && c.width > 1000) bandeau.b = Math.round(c.bottom);
    }

    // --- 2. la vague d'or ---------------------------------------------------
    let vague = null;
    for (const s of document.querySelectorAll('svg')) {
      const b = s.getBoundingClientRect();
      if (b.width < 1000) continue;
      const rempli = [...s.querySelectorAll('path')]
        .some((p) => (p.getAttribute('fill') || '').toUpperCase().includes('F6BC1C'));
      if (rempli) vague = { h: Math.round(b.top), b: Math.round(b.bottom) };
    }

    return { bandeau, vague, sur: boite('.sur'), acc: boite('.acc'),
             dit: boite('.dit'), cta: boite('.cta'), web: boite('.web') };
  }, { MARGE, TOL });

  await page.close();
  return r;
}

function juger(r) {
  const points = [];
  const ok = (b, quoi, detail) => points.push({ b, quoi, detail });

  ok(!!r.bandeau, 'photo en bandeau haut',
     r.bandeau ? `du bord au ${r.bandeau.b} px` : 'aucune photo pleine largeur en haut');

  if (r.vague && r.bandeau) {
    const ecart = Math.abs(r.vague.b - r.bandeau.b);
    ok(ecart <= 60, 'vague d’or en couture',
       `vague à ${r.vague.b}, photo à ${r.bandeau.b} — ${ecart} px d’écart`);
  } else {
    ok(false, 'vague d’or en couture',
       r.vague ? 'vague présente mais pas de photo à coudre' : 'aucune vague d’or');
  }

  if (r.acc && r.bandeau) {
    ok(r.acc.h >= r.bandeau.b - 10, 'titre SOUS la photo',
       `titre à ${r.acc.h}, photo finit à ${r.bandeau.b}`);
  } else {
    ok(false, 'titre SOUS la photo', r.acc ? 'pas de photo' : 'pas de titre');
  }

  const alignes = ['sur', 'acc', 'dit', 'cta'].filter((k) => r[k]);
  const faux = alignes.filter((k) => Math.abs(r[k].g - MARGE) > TOL);
  ok(faux.length === 0, 'une seule verticale à gauche',
     faux.length ? `hors marge : ${faux.map((k) => `.${k}=${r[k].g}`).join(', ')}`
                 : `${alignes.length} blocs alignés sur ${MARGE} px`);

  if (r.cta && r.web) {
    const dr = Math.abs(1080 - r.web.d - MARGE);
    const meme = Math.abs(((r.cta.h + r.cta.b) / 2) - ((r.web.h + r.web.b) / 2));
    ok(dr <= TOL && meme <= 60, 'pied partagé (appel à gauche, adresse à droite)',
       `adresse à ${1080 - r.web.d} px du bord, décalage vertical ${Math.round(meme)} px`);
  } else {
    ok(false, 'pied partagé (appel à gauche, adresse à droite)',
       !r.cta ? 'pas d’appel à l’action' : 'pas d’adresse');
  }
  return points;
}

(async () => {
  const args = process.argv.slice(2);
  const tous = args.includes('--tous');
  // Le bulletin est HORS FAMILLE, et c'est une décision, pas un oubli : son
  // objet regardé est la donnée, pas une image. Le patron l'a exclu lui-même.
  const fichiers = tous
    ? fs.readdirSync('.').filter((f) => /^flyer.*\.html$/.test(f) && !/soir/.test(f)).sort()
    : args;
  if (!fichiers.length) {
    console.error('usage : node famille.js <flyer.html> | --tous');
    process.exit(2);
  }

  const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let total = 0;
  for (const f of fichiers) {
    const points = juger(await examiner(nav, f));
    const n = points.filter((p) => p.b).length;
    total += n;
    console.log(`\n${n === 5 ? '✅' : n >= 3 ? '⚠️ ' : '❌'} ${n}/5 — ${f}`);
    for (const p of points) {
      console.log(`   ${p.b ? '·' : '✗'} ${p.quoi.padEnd(46)} ${p.detail}`);
    }
  }
  if (tous) {
    console.log(`\n${'─'.repeat(70)}\nmoyenne de famille : ` +
      `${(total / fichiers.length).toFixed(1)}/5 sur ${fichiers.length} visuels`);
  }
  await nav.close();
})();
