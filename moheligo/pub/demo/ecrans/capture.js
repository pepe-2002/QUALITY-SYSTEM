/* 📱 LA CAPTURE DE L'APPLICATION — le script, dans le dépôt.
 *
 * 29/08/2026. Il existait déjà, mais il ne vivait que dans /tmp : la marche à
 * suivre était écrite et l'outil avait disparu. Une procédure qu'on ne peut pas
 * rejouer n'est pas une procédure, c'est un souvenir. Il est ici maintenant.
 *
 *   cd moheligo/pub/demo/ecrans
 *   npm install --no-save playwright@1.56.1     # une fois
 *   node capture.js
 *
 * ⛔ ON NE PHOTOGRAPHIE PAS https://moheligo.com : le navigateur de ma session
 * n'a aucun accès réseau (ERR_CONNECTION_RESET, revérifié le 28/08/2026). On
 * rend `moheligo/index.html` en local — c'est le même code que la production.
 *
 * 📅 DEUX PIÈGES SUR LE CHAMP DATE, ET LE SECOND EST LE VRAI.
 *
 * 1. La date était écrite en dur. Une capture de produit périme : figée en mai,
 *    elle montre en août une réservation pour une date passée, et le lecteur en
 *    conclut que le service est mort. Ici elle est CALCULÉE — aujourd'hui + 7
 *    jours — donc toujours crédible au moment du tirage.
 *
 * 2. 🚩 LA LANGUE DU NAVIGATEUR DÉCIDE DU FORMAT AFFICHÉ. Sans `locale`,
 *    Chromium est en en-US et un <input type=date> au 5 septembre s'affiche
 *    « 09/05/2026 ». Un lecteur comorien lit 9 MAI. La capture n'était pas
 *    fausse, elle était ILLISIBLE — et c'est pire, parce que rien ne se voit.
 *    `locale: 'fr-FR'` → « 05/09/2026 ». À vérifier À L'ŒIL après chaque
 *    capture : c'est le genre de défaut qu'aucun contrôle automatique n'attrape.
 */
const { chromium } = require('playwright');
const path = require('path');

const APPLI = path.resolve(__dirname, '../../../index.html');
const SORTIE = path.join(__dirname, 'accueil-reservation.png');

// 440 px et pas 390 : à 390, « MoheliGo » et « Commandants » sont tronqués en
// « Mohel… ». Densité 3 → 1320 x 2700 pixels réels, largement de quoi tenir
// dans un châssis de téléphone sur un visuel 2160 x 2700.
const LARGEUR = 440, HAUTEUR = 892, DENSITE = 3;

const dans = (jours) => {
  const d = new Date(Date.now() + jours * 86400000);
  return d.toISOString().slice(0, 10);          // yyyy-mm-dd, ce qu'attend <input type=date>
};

(async () => {
  // ⚠️ `--lang` AU LANCEMENT, et pas seulement `locale` sur la page : le petit
  // calendrier natif d'un <input type=date> suit la langue de l'INTERFACE du
  // navigateur, pas l'Accept-Language du contexte. Avec `locale` seul, la date
  // sortait encore en 09/05/2026. Mesuré le 29/08/2026.
  const nav = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium',
    args: ['--lang=fr-FR'],
    env: { ...process.env, LANG: 'fr_FR.UTF-8', LANGUAGE: 'fr_FR' },
  });
  const page = await nav.newPage({
    viewport: { width: LARGEUR, height: HAUTEUR }, deviceScaleFactor: DENSITE,
    isMobile: true, hasTouch: true,
    locale: 'fr-FR', timezoneId: 'Indian/Comoro',   // sinon la date sort en MM/JJ/AAAA
  });

  // On coupe le bandeau « Reçois tes rappels » à la source plutôt que de courir
  // après sa croix : il s'affiche seulement si cette clé est absente.
  await page.addInitScript(() => {
    try { localStorage.setItem('mg_push_asked', '1'); } catch (e) {}
  });

  await page.goto('file://' + APPLI, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2500);

  // Le premier écran est l'accueil « Bienvenue », pas la réservation.
  const passer = page.locator('.ob-skip');
  if (await passer.count() && await passer.first().isVisible()) {
    await passer.first().click();
    await page.waitForTimeout(900);
  }

  const date = dans(7);
  await page.evaluate((d) => {
    const b = document.getElementById('install-banner'); if (b) b.remove();
    // les bulles flottantes (micro, chat) passent devant le formulaire
    document.querySelectorAll('body > *').forEach((el) => {
      const s = getComputedStyle(el);
      if (s.position === 'fixed' && el.getBoundingClientRect().width < 200) el.style.display = 'none';
    });
    const champ = document.getElementById('f-date');
    if (champ) { champ.value = d; champ.dispatchEvent(new Event('change', { bubbles: true })); }
  }, date);

  await page.waitForTimeout(1200);
  await page.screenshot({ path: SORTIE });
  console.log('OK ->', SORTIE, '— date affichée :', date);
  await nav.close();
})();
