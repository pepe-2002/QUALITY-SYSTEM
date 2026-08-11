// Capture les VRAIS écrans de moheligo.com pour la démonstration du matin.
//   node capture_site.js [adresse]
//
// Pourquoi le vrai site et pas une maquette : une démonstration dessinée ne
// prouve rien. Celui qui a peur de payer en ligne doit reconnaître l'écran
// qu'il verra sur son téléphone. Une maquette, c'est encore une promesse.
//
// ⚠️ RÈGLE ABSOLUE : cette capture s'arrête AVANT la connexion et AVANT le
// paiement. On ne crée aucune réservation, on n'entre aucun numéro, on ne
// touche à aucun compte. La démonstration montre le chemin, pas la caisse.
//
// Les écrans sortent en 430x932 (téléphone), ils seront habillés ensuite par
// video.py.
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require('/opt/node22/lib/node_modules/playwright')); }
const fs = require('fs');
const path = require('path');

const ADRESSE = process.argv[2] || 'https://moheligo.com/';
const SORTIE = path.join(__dirname, 'ecrans');
const LARGEUR = 430, HAUTEUR = 932;

// Une pause explicite : le site charge ses données, ses images et ses polices.
const souffle = (ms) => new Promise((r) => setTimeout(r, ms));

(async () => {
  fs.mkdirSync(SORTIE, { recursive: true });
  const local = '/opt/pw-browsers/chromium';
  const options = fs.existsSync(local) ? { executablePath: local } : {};
  // Chromium ne lit pas HTTPS_PROXY tout seul : dans la session Claude, la
  // sortie HTTPS passe par un mandataire local, sinon la connexion est coupée.
  // Sur GitHub Actions la variable n'existe pas et on sort en direct.
  const mandataire = process.env.HTTPS_PROXY || process.env.https_proxy;
  if (mandataire) {
    options.proxy = { server: mandataire };
    console.log('  (sortie par le mandataire', mandataire + ')');
  }
  const navigateur = await chromium.launch(options);
  const page = await navigateur.newPage({
    viewport: { width: LARGEUR, height: HAUTEUR },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
    locale: 'fr-FR',
    timezoneId: 'Indian/Comoro',
    colorScheme: 'light',      // la démonstration doit être lumineuse
  });

  const etapes = [];
  const prendre = async (nom, note) => {
    const fichier = path.join(SORTIE, nom + '.png');
    await page.screenshot({ path: fichier });
    etapes.push({ nom, note });
    console.log('  ✓', nom, '—', note);
  };

  console.log('Capture de', ADRESSE);
  await page.goto(ADRESSE, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await souffle(6000);                       // les données des départs arrivent

  // 1 — l'accueil, tel qu'il s'ouvre
  await prendre('1-accueil', "l'accueil, rien à installer");

  // 2 — la carte « Réserver une traversée », remplie
  const carte = await page.$('.bookcard');
  if (carte) await carte.scrollIntoViewIfNeeded();
  await souffle(700);
  await prendre('2-reserver', 'choisir le départ, l\'arrivée, la date');

  // On renseigne le trajet comme le ferait un voyageur.
  try {
    const dep = await page.$('#f-dep');
    const arr = await page.$('#f-arr');
    if (dep && arr) {
      const valeurs = await page.evaluate(() => ({
        dep: [...document.querySelectorAll('#f-dep option')].map((o) => o.value),
        arr: [...document.querySelectorAll('#f-arr option')].map((o) => o.value),
      }));
      console.log('  ports disponibles :', JSON.stringify(valeurs));
      if (valeurs.dep.length) await dep.selectOption(valeurs.dep[0]);
      if (valeurs.arr.length) await arr.selectOption(valeurs.arr[valeurs.arr.length - 1]);
    }
    // la date du lendemain, au format attendu par un champ date
    const demain = new Date(Date.now() + 86400000).toISOString().slice(0, 10);
    await page.evaluate((d) => {
      const c = document.querySelector('#f-date');
      if (c) { c.value = d; c.dispatchEvent(new Event('change', { bubbles: true })); }
    }, demain);
    await souffle(600);
    await prendre('3-trajet-choisi', 'le trajet est choisi');
  } catch (e) {
    console.log('  ! trajet non renseigné :', e.message);
  }

  // 3 — la recherche : la liste des traversées avec les places et les prix
  try {
    await page.evaluate(() => typeof search === 'function' && search());
    await souffle(3500);
    await prendre('4-traversees', 'les départs, les places, les prix');
  } catch (e) {
    console.log('  ! recherche non déclenchée :', e.message);
  }

  // 4 — l'état de la mer : notre argument d'autorité
  try {
    const meteo = await page.$('#home-weather, .wcard, #windy-tabs');
    if (meteo) {
      await meteo.scrollIntoViewIfNeeded();
      await souffle(1200);
      await prendre('5-mer', 'l\'état de la mer avant de partir');
    }
  } catch (e) {
    console.log('  ! météo non trouvée :', e.message);
  }

  // ⛔ ON S'ARRÊTE ICI. Pas de connexion, pas de numéro, pas de paiement.
  fs.writeFileSync(path.join(SORTIE, 'etapes.json'),
                   JSON.stringify({ adresse: ADRESSE, quand: new Date().toISOString(), etapes }, null, 2));
  console.log('\n' + etapes.length, 'écrans dans', SORTIE);
  await navigateur.close();
})();
