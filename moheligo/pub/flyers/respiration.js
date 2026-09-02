#!/usr/bin/env node
/* ⬛ COMBIEN DE VIDE RESTE-T-IL ? — 02/09/2026.
 *
 *     NODE_PATH=/opt/node22/lib/node_modules node respiration.js --tous
 *
 * Relecture extérieure transmise par le patron : « le style reste très digital /
 * Instagram. Ça n'a pas le raffinement d'une marque type Air France ou d'une
 * compagnie maritime haut de gamme : polices plus élégantes, compositions plus
 * aérées, moins de blocs texte denses. Un vrai positionnement premium aurait
 * encore plus d'espace blanc et de respirations. »
 *
 * 🎯 « PLUS AÉRÉ » N'EST PAS UNE EXIGENCE TANT QU'ON NE SAIT PAS LE COMPTER.
 * C'est la règle de rédaction de la norme : ce qui n'est pas mesurable n'y entre
 * pas. Ce programme compte donc le TAUX D'OCCUPATION — la part de la page
 * couverte par quelque chose qui demande à être lu.
 *
 * 🔍 CE QU'IL COMPTE, ET CE QU'IL NE COMPTE PAS :
 *   · compté : chaque bloc de texte, chaque carte claire, chaque pastille. Tout
 *     ce qui arrête l'œil et réclame une lecture ;
 *   · pas compté : la photo, l'aplat marine, la vague. Ce n'est pas du vide,
 *     mais ce n'est pas de la charge non plus — on les regarde, on ne les lit
 *     pas. Une grande photo REPOSE, un bloc de texte FATIGUE.
 * 📌 Le luxe ne se mesure pas en pixels blancs : il se mesure en **nombre de
 * choses à lire**. Une page peut être remplie d'image et rester aérée ; deux
 * petits blocs de texte de trop la rendent bavarde.
 *
 * ⚖️ LES SEUILS, ÉTALONNÉS SUR NOS PROPRES VISUELS ET SUR CE QU'ON VISE :
 *      ≤ 22 %   aéré           le registre d'une marque premium
 *      ≤ 32 %   acceptable     un visuel de service, qui doit informer
 *      > 32 %   bavard         on lit avant de regarder — à alléger
 * Et un second compte, souvent plus parlant que la surface : le NOMBRE DE BLOCS
 * à lire. Au-delà de six, l'œil ne hiérarchise plus, il balaie.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const SELS = ['.sur', '.acc', '.dit', '.sous', '.cta', '.web', '.ligne', '.trait',
              '.carte', '.avis', '.action', '.fin', '.credit', '.don', '.pied'];

async function mesurer(nav, fichier) {
  const page = await nav.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.resolve(fichier));
  await page.evaluate(() => document.fonts.ready);

  const r = await page.evaluate((SELS) => {
    // Une grille de 1080 × 1350 à la maille de 5 px : on marque ce qui est
    // couvert, ce qui règle le problème des blocs qui se recouvrent (les
    // additionner compterait deux fois la même surface).
    const P = 5, W = 1080 / P, H = 1350 / P;
    const grille = new Uint8Array(W * H);
    const blocs = [];
    for (const sel of SELS) {
      for (const el of document.querySelectorAll(sel)) {
        const b = el.getBoundingClientRect();
        if (b.width < 4 || b.height < 4) continue;
        blocs.push({ sel, l: Math.round(b.width), h: Math.round(b.height) });
        for (let y = Math.max(0, b.top / P); y < Math.min(H, b.bottom / P); y++) {
          for (let x = Math.max(0, b.left / P); x < Math.min(W, b.right / P); x++) {
            grille[(y | 0) * W + (x | 0)] = 1;
          }
        }
      }
    }
    let n = 0;
    for (const v of grille) n += v;
    return { taux: n / grille.length, blocs };
  }, SELS);

  await page.close();
  return r;
}

(async () => {
  const args = process.argv.slice(2);
  const tous = args.includes('--tous');
  const fichiers = tous
    ? fs.readdirSync('.').filter((f) => /^flyer.*\.html$/.test(f) && !/soir-v1|template/.test(f)).sort()
    : args;
  const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let somme = 0;
  console.log('  visuel                                 occupé   blocs   verdict');
  console.log('  ' + '─'.repeat(70));
  for (const f of fichiers) {
    const { taux, blocs } = await mesurer(nav, f);
    somme += taux;
    const v = taux <= 0.22 ? 'aéré' : taux <= 0.32 ? 'acceptable' : 'BAVARD';
    const alerte = (taux > 0.32 || blocs.length > 6) ? '⚠️ ' : '   ';
    console.log(`${alerte}${f.replace('-fb.html', '').padEnd(38)}` +
                `${(taux * 100).toFixed(1).padStart(5)} %  ${String(blocs.length).padStart(4)}   ${v}`);
  }
  if (fichiers.length > 1) {
    console.log('  ' + '─'.repeat(70));
    console.log(`  moyenne : ${(somme / fichiers.length * 100).toFixed(1)} % de la page occupée`);
  }
  await nav.close();
})();
