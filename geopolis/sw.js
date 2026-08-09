/* GÉOPOLIS — service worker : le jeu se joue hors ligne une fois chargé. */
const CACHE = 'geopolis-v1';
const FICHIERS = [
  './', './index.html', './geopolis.css',
  './g-data.js', './g-moteur.js', './g-evenements.js',
  './g-carte.js', './g-ui.js', './g-accueil.js',
  './manifest.webmanifest'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FICHIERS)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(k => Promise.all(k.filter(x => x !== CACHE).map(x => caches.delete(x))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(rep => rep || fetch(e.request).then(r => {
      const copie = r.clone();
      caches.open(CACHE).then(c => c.put(e.request, copie)).catch(() => {});
      return r;
    }).catch(() => caches.match('./index.html')))
  );
});
