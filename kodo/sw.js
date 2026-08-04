/* Kodo — service worker : l'application marche entièrement hors connexion. */
const CACHE = 'kodo-v1';
const FICHIERS = [
  './', './index.html', './kodo.css', './kodo.js',
  './cours-bases.js', './cours-tech.js',
  './fonts.css', './manifest.webmanifest',
  './icon-192.png', './icon-512.png',
  './fonts/manrope-400.woff2', './fonts/manrope-800.woff2',
  './fonts/bebasneue-400.woff2', './fonts/jetbrainsmono-400.woff2',
  './fonts/jetbrainsmono-700.woff2', './fonts/playfairdisplay-700.woff2'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => Promise.all(FICHIERS.map(f => c.add(f).catch(() => {}))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    caches.match(e.request).then(rep => rep || fetch(e.request).then(net => {
      // On garde une copie des fichiers de l'application
      if (net.ok && new URL(e.request.url).origin === location.origin) {
        const copie = net.clone();
        caches.open(CACHE).then(c => c.put(e.request, copie));
      }
      return net;
    }).catch(() => caches.match('./index.html')))
  );
});
