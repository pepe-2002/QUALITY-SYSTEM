// Rendu des flyers MoheliGo : HTML/CSS -> PNG haute résolution (Chromium).
//   node render.js flyer2-corporate.html flyer-corporate-A4.png 1240 1754 2
// Le dernier argument est le facteur d'échelle (2 sur du 1240x1754 = A4 à 300 dpi).
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const [src, out, w, h, scale] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
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
