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
 * 🔀 DEUX FORMES, ET C'EST UNE DÉCISION, PAS UN RENONCEMENT (02/09, le soir).
 * En voulant tout ramener au bandeau, je me suis heurté à deux visuels dont le
 * sujet est VERTICAL : le téléphone du mercredi et le portrait du vendredi. Un
 * bandeau horizontal les couperait au milieu — on perdrait l'écran dans un cas,
 * le visage dans l'autre. Les forcer aurait donné une famille uniforme et deux
 * visuels ratés.
 * 📌 **UNE FAMILLE N'EST PAS FAITE DE VISUELS IDENTIQUES, ELLE EST FAITE DE
 * VISUELS QUI PARTAGENT LES MÊMES CONSTANTES.** Ce qu'on reconnaît chez des
 * frères, ce n'est pas qu'ils soient superposables — c'est ce qui ne change
 * jamais d'un visage à l'autre.
 *
 * TROIS CONSTANTES, OBLIGATOIRES DANS LES DEUX FORMES :
 *   · la vague d'or, qui fait un travail (coudre la photo, ou asseoir la page) ;
 *   · une seule verticale à gauche, à 76 px ;
 *   · le pied partagé : appel à gauche, adresse à droite.
 * PUIS DEUX POINTS SELON LA FORME :
 *   BANDEAU — photo pleine largeur en haut, titre dessous.
 *   SUJET   — un sujet vertical sur un côté, titre dans la colonne libre.
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

    // --- le sujet vertical : une image haute sur un côté --------------------
    let sujet = null;
    for (const img of document.querySelectorAll('img')) {
      const b = img.getBoundingClientRect();
      if (b.height < 700 || b.width > 1000) continue;
      if (!sujet || b.height > sujet.b - sujet.h) {
        sujet = { g: Math.round(b.left), d: Math.round(b.right),
                  h: Math.round(b.top), b: Math.round(b.bottom) };
      }
    }

    return { bandeau, sujet, vague, sur: boite('.sur'), acc: boite('.acc'),
             dit: boite('.dit'), cta: boite('.cta'), web: boite('.web') };
  }, { MARGE, TOL });

  await page.close();
  return r;
}

function juger(r) {
  const points = [];
  const ok = (b, quoi, detail) => points.push({ b, quoi, detail });
  // La forme se DÉDUIT du visuel, elle ne se déclare pas : un fichier qui se
  // décrit lui-même finit toujours par se décrire faux.
  const forme = r.bandeau ? 'BANDEAU' : r.sujet ? 'SUJET' : 'AUCUNE';

  // ── les trois constantes, obligatoires dans les deux formes ──────────────
  if (r.vague && forme === 'BANDEAU') {
    const ecart = Math.abs(r.vague.b - r.bandeau.b);
    ok(ecart <= 60, 'la vague fait un travail',
       `couture : vague à ${r.vague.b}, photo à ${r.bandeau.b} — ${ecart} px`);
  } else if (r.vague && forme === 'SUJET') {
    ok(r.vague.b >= 1330, 'la vague fait un travail',
       `assise de page : vague jusqu’à ${r.vague.b}`);
  } else {
    ok(false, 'la vague fait un travail', 'aucune vague d’or');
  }

  const alignes = ['sur', 'acc', 'dit', 'cta'].filter((k) => r[k]);
  const faux = alignes.filter((k) => Math.abs(r[k].g - MARGE) > TOL);
  ok(faux.length === 0, 'une seule verticale à gauche',
     faux.length ? `hors marge : ${faux.map((k) => `.${k}=${r[k].g}`).join(', ')}`
                 : `${alignes.length} blocs alignés sur ${MARGE} px`);

  // ── puis les deux points de la forme ────────────────────────────────────
  if (forme === 'BANDEAU') {
    ok(true, 'forme BANDEAU — photo pleine largeur en haut',
       `du bord au ${r.bandeau.b} px`);
    ok(!!r.acc && r.acc.h >= r.bandeau.b - 10, 'titre sous la photo',
       r.acc ? `titre à ${r.acc.h}, photo finit à ${r.bandeau.b}` : 'pas de titre');
  } else if (forme === 'SUJET') {
    ok(true, 'forme SUJET — sujet vertical sur un côté',
       `${r.sujet.d - r.sujet.g} × ${r.sujet.b - r.sujet.h} px, à droite de ${r.sujet.g}`);
    ok(!!r.acc && r.acc.d <= r.sujet.g + 40, 'titre dans la colonne libre',
       r.acc ? `titre finit à ${r.acc.d}, sujet commence à ${r.sujet.g}` : 'pas de titre');
  } else {
    ok(false, 'une forme reconnaissable', 'ni bandeau photo, ni sujet vertical');
    ok(false, 'titre placé selon la forme', 'pas de forme');
  }

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
