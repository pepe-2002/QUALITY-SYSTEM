// Capture le VRAI écran d'accueil de MoheliGo, pour le poser dans un téléphone
// sur les visuels. Le site est servi en local depuis le dépôt : le HTML, le CSS
// et les données de ports sont les siens. Rien n'est redessiné.
//   python3 -m http.server 8899   (depuis moheligo/)
//   node capture_accueil.js
//
// ⚠️ Deux retouches, et deux seulement, toutes deux cosmétiques et assumées :
//   1. la DATE est renseignée à demain — un client la choisit, un champ vide
//      afficherait « mm/dd/yyyy » et ferait croire à un formulaire cassé ;
//   2. les bulles flottantes (chat, bouton service client) sont masquées : elles
//      recouvrent la carte de réservation. Elles existent bien dans le produit.
// On n'invente AUCUN départ, AUCUN prix, AUCUN horaire.
let chromium; try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }

(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 390, height: 800 }, deviceScaleFactor: 3,
                              isMobile: true, hasTouch: true, locale: 'fr-FR' });
  await p.addInitScript(() => {
    try { localStorage.setItem('mg_ob_done', '1'); } catch (e) {}
  });
  await p.goto('http://127.0.0.1:8899/index.html', { waitUntil: 'domcontentloaded', timeout: 30000 });

  // ⚠️ PIÈGE PAYÉ n° 2 : au premier passage, l'application affiche son écran de
  // BIENVENUE (« Bienvenue sur MoheliGo », trois pages, bouton « Passer »). Une
  // capture prise trop tôt attrapait l'accueil AVANT que cet écran se pose, une
  // capture prise plus tard attrapait la bienvenue. On fait comme un vrai
  // client : on appuie sur « Passer ».
  // ⚠️ PIÈGE PAYÉ : les ports arrivent APRÈS le chargement (l'application les
  // remplit une fois ses données prêtes). Une simple attente de 6 secondes
  // choisissait le port par défaut, puis la liste se remplissait juste avant la
  // capture — le patron a vu Chindini alors qu'on avait demandé Ouroveni.
  // On attend donc que la liste EXISTE avant d'y toucher.
  await p.waitForFunction(
    () => document.querySelectorAll('#f-dep option').length > 1,
    { timeout: 30000 });
  await new Promise(r => setTimeout(r, 1500));

  await p.selectOption('#f-dep', { label: 'Ouroveni (Grande Comore)' });
  await p.selectOption('#f-arr', { label: 'Hoani (Mohéli)' });
  await p.evaluate(() => {
    const demain = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
    const d = document.querySelector('#f-date');
    if (d) { d.value = demain; d.dispatchEvent(new Event('change', { bubbles: true })); }
    ['.fab', '.chatbot-fab', '.wa-fab', '#chat-fab', '#wa-float', '.floating',
     '[class*="fab"]', '[class*="float"]'].forEach(s =>
      document.querySelectorAll(s).forEach(e => { e.style.display = 'none'; }));
  });
  // On RELIT ce qui est affiché avant de capturer : une capture qui montre le
  // mauvais port est pire qu'une capture absente.
  const choisi = await p.evaluate(() => {
    const s = (id) => { const e = document.querySelector(id);
      return e && e.options[e.selectedIndex] ? e.options[e.selectedIndex].textContent.trim() : ''; };
    return { depart: s('#f-dep'), arrivee: s('#f-arr'),
             date: document.querySelector('#f-date')?.value || '' };
  });
  console.log('affiché à l\'écran :', JSON.stringify(choisi));
  if (!/ouroveni/i.test(choisi.depart)) {
    throw new Error('le départ affiché n\'est pas Ouroveni : ' + choisi.depart);
  }
  const propre = await p.evaluate(() => {
    // ⚠️ Tester la VISIBILITÉ, pas la présence : le bloc de bienvenue existe
    // toujours dans le HTML, donc un simple test de texte le trouvait même
    // caché — et refusait toutes les captures.
    const affiche = (e) => {
      if (!e) return false;
      const r = e.getBoundingClientRect();
      const s = getComputedStyle(e);
      return !!e.offsetParent && r.width > 20 && r.height > 20 &&
             s.visibility !== 'hidden' && parseFloat(s.opacity || '1') > 0.1;
    };
    const bienvenue = [...document.querySelectorAll('*')].some(
      (e) => e.children.length === 0 && /Bienvenue sur MoheliGo/.test(e.textContent || '')
             && affiche(e));
    const c = document.querySelector('.bookcard');
    return { bienvenue, carteVisible: affiche(c) };
  });
  if (propre.bienvenue || !propre.carteVisible) {
    throw new Error('ce n\'est pas l\'accueil : ' + JSON.stringify(propre));
  }
  await p.screenshot({ path: 'ecran-accueil.png' });
  console.log('ecran-accueil.png écrit (390x800 @3 = 1170x2400)');
  await b.close();
})();
