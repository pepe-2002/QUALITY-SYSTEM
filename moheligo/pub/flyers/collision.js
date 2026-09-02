#!/usr/bin/env node
/* ⬛ LES BLOCS QUI SE MARCHENT DESSUS — 02/09/2026.
 *
 *     NODE_PATH=/opt/node22/lib/node_modules node collision.js flyer28-rien-installer-fb.html
 *     NODE_PATH=/opt/node22/lib/node_modules node collision.js --tous
 *
 * 🚩 POURQUOI IL EXISTE : le flyer du LUNDI sort depuis des semaines avec le mot
 * « page. » — le dernier mot de son titre — IMPRIMÉ SOUS SON PROPRE PARAGRAPHE.
 * Le titre « Rien à installer. C’est juste une page. » est écrit sur deux
 * `<span>`, mais rendu il tient sur TROIS lignes ; la troisième déborde de son
 * cadre et tombe pile sur le corps de texte, qui est en position absolue et ne
 * bouge donc pas d’un pixel pour lui faire de la place.
 *
 * ⛔ AUCUN de nos deux contrôles ne pouvait le voir, et pour deux raisons
 * différentes — c’est ça qui est instructif :
 *   · `exigence.py` LIT LE CODE : il compte les coupures déclarées (`<br>`, span
 *     en bloc). Le code dit deux lignes. Il dit vrai, et il passe à côté.
 *   · `lignes.js` MESURE LE RENDU : il voit bien trois lignes… et n’en conclut
 *     rien, parce qu’il regarde CHAQUE BLOC SÉPARÉMENT. Un bloc de trois lignes
 *     n’a rien d’anormal en soi.
 * 📌 **LE DÉFAUT N’ÉTAIT DANS AUCUN BLOC : IL ÉTAIT ENTRE DEUX BLOCS.** Un
 * contrôle qui n’examine que des éléments un par un ne trouvera jamais un défaut
 * de RELATION, aussi rigoureux soit-il sur chacun.
 *
 * 🔍 CE QU’IL MESURE, ET POURQUOI C’EST L’ENCRE ET PAS LA BOÎTE : la boîte CSS
 * d’un bloc en position absolue ne dit rien de l’endroit où les lettres se
 * posent — c’est justement le débordement qui fait le dégât. On mesure donc les
 * rectangles RÉELS de chaque ligne de texte (`Range.getClientRects`), et on
 * cherche les intersections entre lignes appartenant à des blocs différents.
 *
 * ⚖️ CE QU’IL NE SIGNALE PAS, VOLONTAIREMENT :
 *   · un texte posé sur une photo, un aplat, un dégradé — c’est notre mise en
 *     page normale ; seul le texte-CONTRE-texte est un défaut ;
 *   · un parent et son enfant (un `<b>` est forcément « dans » son paragraphe) ;
 *   · un recouvrement de moins de 2 px sur un axe : c’est du crénage, pas une
 *     collision.
 *
 * Il signale en revanche le FRÔLEMENT — deux textes qui se ratent de peu. Ce
 * n’est pas encore une faute, c’est un visuel qui n’a plus de marge : un mot de
 * plus, une police qui charge une fraction de seconde plus tard, et ça devient
 * la faute du lundi.
 *
 * 🚩 ET LE FRÔLEMENT SE MESURE EN CORPS, PAS EN PIXELS. Premier jet : « moins
 * de 6 px = alerte ». Il a immédiatement accusé nos DEUX seuls visuels
 * irréprochables — les 4 px entre « MoheliGo » et « TRAVERSÉES MARITIMES » dans
 * le coin blanc, qui sont la charte elle-même. 4 px sous une légende de 9,5 px
 * c’est de l’air ; 4 px sous un titre de 56 px c’est un accident qui attend.
 * Le seuil est donc **un quart du plus petit des deux corps**.
 * 📌 Un contrôle qui refuse ce qu’on a fait de mieux n’est pas exigeant, il est
 * mal écrit — la même leçon que le 30/08 sur la règle des « 6 mots maximum ».
 *
 * Sortie : 0 si rien, 1 s’il y a au moins une collision (le frôlement n’échoue
 * pas). Comme `lignes.js`, il ne modifie jamais la page qu’il mesure.
 */
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// Recouvrement minimal pour qu'on parle de collision, exprimé en FRACTION DU
// PLUS GRAND DES DEUX CORPS. Voir l'en-tête : une boîte de ligne est toujours
// plus haute que l'encre qu'elle contient, d'environ un quart de cadratin.
const COLLE = 0.22;
const FROLE = 0.25;   // fraction du plus petit corps sous laquelle on prévient

async function examiner(nav, fichier) {
  const page = await nav.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto('file://' + path.resolve(fichier));
  await page.evaluate(() => document.fonts.ready);

  const trouve = await page.evaluate(({ COLLE, FROLE }) => {
    // --- l’encre : un rectangle par LIGNE de texte réellement dessinée -------
    // On passe par un Range : il lit une position sans rien changer à la page.
    // (La leçon de `lignes.js` : une sonde qui modifie ce qu’elle mesure ne
    // mesure rien.)
    const encreDe = (el) => {
      const rects = [];
      for (const n of el.childNodes) {
        if (n.nodeType !== Node.TEXT_NODE || !n.textContent.trim()) continue;
        const r = document.createRange();
        r.selectNodeContents(n);
        for (const b of r.getClientRects()) {
          if (b.width > 1 && b.height > 1) rects.push(b);
        }
      }
      return rects;
    };

    // 🚩 UN TEXTE INCLINÉ NE SE MESURE PAS AVEC UN RECTANGLE DROIT.
    // getClientRects() rend des rectangles alignés sur les axes : sur la
    // pastille de prix, tournée de quelques degrés, les cadres de « À PARTIR
    // DE », « 15 000 » et « LE TRAJET » se chevauchent forcément alors que
    // l'encre ne se touche nulle part. Le programme accusait donc trois de nos
    // affiches d'un défaut qui n'existe pas.
    // 📌 On ne devine pas : on remonte la chaîne des transformations, et si
    // quelque chose tourne, on le DIT au lieu de conclure.
    const estPenche = (el) => {
      for (let n = el; n && n !== document.documentElement; n = n.parentElement) {
        const tr = getComputedStyle(n).transform;
        if (!tr || tr === 'none') continue;
        const m = tr.match(/matrix\(([^)]+)\)/);
        if (!m) continue;
        const [a, b] = m[1].split(',').map(Number);
        if (Math.abs(Math.atan2(b, a)) > 0.01) return true;   // > 0,6°
      }
      return false;
    };

    const nom = (el) => {
      const cls = (el.className || '').toString().trim().split(/\s+/)[0];
      return el.tagName.toLowerCase() + (cls ? '.' + cls : '');
    };

    // Tout élément qui porte lui-même du texte visible.
    const porteurs = [];
    for (const el of document.querySelectorAll('*')) {
      const s = getComputedStyle(el);
      if (s.visibility === 'hidden' || s.display === 'none' || s.opacity === '0') continue;
      const rects = encreDe(el);
      if (!rects.length) continue;
      porteurs.push({ el, nom: nom(el), rects, corps: parseFloat(s.fontSize) || 0,
                      penche: estPenche(el),
                      texte: el.textContent.trim().slice(0, 46) });
    }

    const chevauche = (a, b) => {
      const x = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const y = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      return { x, y };
    };

    const collisions = [], frolements = [], penches = [];
    for (let i = 0; i < porteurs.length; i++) {
      for (let j = i + 1; j < porteurs.length; j++) {
        const A = porteurs[i], B = porteurs[j];
        // Un parent et son enfant se contiennent par construction.
        if (A.el.contains(B.el) || B.el.contains(A.el)) continue;
        if (A.penche || B.penche) {
          const t = [A.nom, B.nom].sort().join(' × ');
          if (!penches.includes(t)) penches.push(t);
          continue;
        }
        let pire = null, plusProche = null;
        // Le recouvrement se juge lui aussi au corps, et contre le PLUS GRAND
        // des deux : c'est le gros caractère qui apporte le rembourrage.
        const mordu = COLLE * Math.max(A.corps, B.corps);
        // Le frôlement se juge au corps : un quart de la plus petite des deux
        // tailles de police, et jamais moins de 2 px.
        const seuil = Math.max(2, FROLE * Math.min(A.corps, B.corps));
        for (const ra of A.rects) {
          for (const rb of B.rects) {
            const { x, y } = chevauche(ra, rb);
            if (x > 2 && y > mordu) {
              const aire = Math.round(x * y);
              if (!pire || aire > pire.aire) {
                pire = { aire, x: Math.round(x), y: Math.round(y),
                         corps: Math.round(Math.max(A.corps, B.corps)),
                         part: (y / Math.max(A.corps, B.corps)),
                         haut: Math.round(Math.max(ra.top, rb.top)) };
              }
            } else if (x > 0 && y <= 0) {
              // côte à côte verticalement : l’écart est sur y
              const ecart = -y;
              if (ecart < seuil && (!plusProche || ecart < plusProche.ecart)) {
                plusProche = { ecart: Math.round(ecart), seuil: Math.round(seuil),
                               sens: 'vertical' };
              }
            } else if (y > 0 && x <= 0) {
              const ecart = -x;
              if (ecart < seuil && (!plusProche || ecart < plusProche.ecart)) {
                plusProche = { ecart: Math.round(ecart), seuil: Math.round(seuil),
                               sens: 'horizontal' };
              }
            }
          }
        }
        if (pire) {
          collisions.push({ a: A.nom, b: B.nom, ta: A.texte, tb: B.texte, ...pire });
        } else if (plusProche) {
          frolements.push({ a: A.nom, b: B.nom, ta: A.texte, tb: B.texte, ...plusProche });
        }
      }
    }
    return { collisions, frolements, penches };
  }, { COLLE, FROLE });

  await page.close();
  return trouve;
}

(async () => {
  const args = process.argv.slice(2);
  const tous = args.includes('--tous');
  const fichiers = tous
    ? fs.readdirSync('.').filter((f) => /^flyer.*\.html$/.test(f)).sort()
    : args;
  if (!fichiers.length) {
    console.error('usage : node collision.js <flyer.html> | --tous');
    process.exit(2);
  }

  const nav = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let fautifs = 0;
  for (const f of fichiers) {
    const { collisions, frolements, penches } = await examiner(nav, f);
    if (collisions.length) {
      fautifs++;
      console.log(`\n❌ COLLISION — ${f}   (${collisions.length})`);
      for (const c of collisions) {
        console.log(`   ${c.a} × ${c.b} — ${c.x} px sur ${c.y} px, vers y=${c.haut}` +
          `  [corps ${c.corps}, soit ${(c.part * 100).toFixed(0)} %]`);
        console.log(`      « ${c.ta} »`);
        console.log(`      « ${c.tb} »`);
      }
    } else if (frolements.length) {
      console.log(`\n⚠️  FRÔLEMENT — ${f}   (${frolements.length})`);
      for (const c of frolements) {
        console.log(`   ${c.a} × ${c.b} — ${c.ecart} px d’écart ${c.sens} ` +
          `(le corps en demande ${c.seuil})`);
      }
    } else if (!tous) {
      console.log(`\n✅ AUCUNE COLLISION — ${f}`);
    }
    if (penches.length && !tous) {
      console.log(`   ℹ️  non mesurable (texte incliné) : ${penches.join(', ')}` +
        ` — à juger à l’œil.`);
    }
  }
  if (tous) {
    console.log(`\n${'─'.repeat(62)}\n${fautifs} visuel(s) en collision sur ${fichiers.length}`);
  }
  await nav.close();
  process.exit(fautifs ? 1 : 0);
})();
