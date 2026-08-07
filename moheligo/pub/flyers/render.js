// Rendu des flyers MoheliGo : HTML/CSS -> PNG haute résolution (Chromium).
//   node render.js flyer2-corporate.html flyer-corporate-A4.png 1240 1754 2
// Le dernier argument est le facteur d'échelle (2 sur du 1240x1754 = A4 à 300 dpi).
// Playwright : celui du projet s'il existe, sinon celui installé globalement
// dans la session Claude. Permet de faire tourner le même script sur un
// serveur GitHub Actions comme ici.
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const fs = require('fs');
const path = require('path');

(async () => {
  const [src, out, w, h, scale] = process.argv.slice(2);
  // Chromium préinstallé dans la session ; ailleurs, celui de Playwright
  const local = '/opt/pw-browsers/chromium';
  const browser = await chromium.launch(
    fs.existsSync(local) ? { executablePath: local } : {});
  const page = await browser.newPage({
    viewport: { width: +w, height: +h },
    deviceScaleFactor: +(scale || 2),
  });
  await page.goto('file://' + path.resolve(src));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(600);
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: +w, height: +h } });
  await browser.close();
  console.log('OK ->', out);
})();
