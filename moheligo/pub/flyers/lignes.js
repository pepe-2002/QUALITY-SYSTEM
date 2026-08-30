#!/usr/bin/env node
/* ⬛ LA DÉCOUPE RÉELLE DES BLOCS DE TEXTE — 30/08/2026.
 *
 *     NODE_PATH=/opt/node22/lib/node_modules node lignes.js flyer43-tulasdeja-fb.html
 *
 * La norme interdit la LIGNE VEUVE — un mot seul sur la dernière ligne d'un
 * paragraphe (EXIGENCE.md § 5). Cette règle était écrite et rien ne la faisait
 * respecter : le 30/08, « embarques. » est resté seul sous deux lignes pleines
 * dans un visuel qui passait tous les autres contrôles.
 *
 * 🚩 POURQUOI CE PROGRAMME NE TOUCHE PAS AU DOM — c'est tout le sujet.
 * Premier essai : entourer chaque mot d'un `<span>` pour lire sa position. Ça
 * marchait sur le corps de texte et ça a MENTI sur le titre, parce que
 * `.acc span` est en `display:block` : mes spans ont mis chaque mot sur sa
 * propre ligne, et l'outil a annoncé « 3 lignes, ligne veuve » sur un titre qui
 * en fait deux. Il mesurait sa propre modification.
 * 📌 UNE SONDE QUI MODIFIE CE QU'ELLE MESURE NE MESURE RIEN. On utilise donc
 * des `Range` : un Range lit une position sans rien changer à la page.
 *
 * ⚠️ Ce contrôle est CONSULTATIF et il le reste. « Deux mots sur la dernière
 * ligne » n'est pas toujours mieux qu'un ; c'est l'œil qui tranche. Il signale,
 * il ne refuse pas — au contraire d'`exigence.py`.
 */
const { chromium } = require('playwright');
const path = require('path');

const BLOCS = ['.acc', '.dit', '.sur', '.web', '.ou', '.cta'];

(async () => {
  const fichier = process.argv[2];
  if (!fichier) {
    console.error('usage : node lignes.js <flyer.html>');
    process.exit(2);
  }
  const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const page = await nav.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.resolve(fichier));
  await page.evaluate(() => document.fonts.ready);

  const blocs = await page.evaluate((BLOCS) => {
    // Position d'un mot, lue par un Range : aucune modification de la page.
    const lignesDe = (el) => {
      const marcheur = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      const mots = [];
      for (let n = marcheur.nextNode(); n; n = marcheur.nextNode()) {
        const t = n.textContent;
        const re = /\S+/g;
        let m;
        while ((m = re.exec(t))) {
          const r = document.createRange();
          r.setStart(n, m.index);
          r.setEnd(n, m.index + m[0].length);
          const boite = r.getBoundingClientRect();
          mots.push({ mot: m[0], y: Math.round(boite.top), droite: boite.right });
        }
      }
      const par = new Map();
      for (const w of mots) {
        // on tolère 2 px de flottement (accents, exposants)
        const cle = [...par.keys()].find((k) => Math.abs(k - w.y) <= 2);
        (par.get(cle ?? w.y) ?? par.set(w.y, []).get(w.y)).push(w);
      }
      return [...par.entries()].sort((a, b) => a[0] - b[0]).map(([, v]) => v);
    };
    // 🚩 LA VEUVE NE SE JUGE QUE SUR UN TEXTE QUI SE COUPE TOUT SEUL.
    // Premier jet : l'outil signalait « DÉJÀ. » seul sous « TU L’AS », et
    // « moheligo.com » seul sous sa surtitre. Ce sont des coupures VOULUES —
    // un `<br>`, un span doré en `display:block`, un `<small>` de signature.
    // 📌 Une veuve, c'est un mot que le RETOUR À LA LIGNE AUTOMATIQUE a laissé
    // seul. Là où le dessinateur a coupé lui-même, il n'y a rien à signaler.
    const coupeALaMain = (el) =>
      !!el.querySelector('br') ||
      [...el.querySelectorAll('*')].some(
        (n) => getComputedStyle(n).display !== 'inline');

    const out = {};
    for (const sel of BLOCS) {
      const el = document.querySelector(sel);
      if (!el) continue;
      const b = el.getBoundingClientRect();
      out[sel] = {
        aLaMain: coupeALaMain(el),
        lignes: lignesDe(el).map((l) => ({
          mots: l.map((w) => w.mot),
          fin: Math.round(Math.max(...l.map((w) => w.droite))),
        })),
        boite: {
          gauche: Math.round(b.left), droite: Math.round(b.right),
          largeur: Math.round(b.width), bas: Math.round(b.bottom),
        },
      };
    }
    return out;
  }, BLOCS);

  let veuves = 0;
  for (const [sel, b] of Object.entries(blocs)) {
    const L = b.lignes;
    const der = L[L.length - 1];
    const veuve = L.length > 1 && der.mots.length === 1 && !b.aLaMain;
    if (veuve) veuves++;
    console.log(`\n${sel}  —  ${L.length} ligne(s), colonne ${b.boite.largeur} px` +
      (b.aLaMain ? ', coupure voulue' : ''));
    L.forEach((l, i) => {
      const reste = b.boite.gauche + b.boite.largeur - l.fin;
      console.log(`   ${i + 1}. ${String(l.fin - b.boite.gauche).padStart(4)} px ` +
        `(${String(reste).padStart(4)} px de marge)  ${l.mots.join(' ')}`);
    });
    if (veuve) {
      console.log(`   ❌ LIGNE VEUVE : « ${der.mots[0]} » est seul sur la ` +
        `dernière ligne — norme § 5.`);
    }
  }
  console.log(`\n${'─'.repeat(62)}\n${veuves} ligne(s) veuve(s)`);
  await nav.close();
  process.exit(veuves ? 1 : 0);
})();
