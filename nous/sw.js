/* « Nous » — service worker.
   La PAGE est demandée au réseau
   d'abord (jamais de version périmée après un déploiement), le reste est
   servi depuis le cache. Les appels à la base ne sont jamais interceptés :
   une conversation ne doit jamais sortir d'un cache. */

const CACHE = "nous-v1";
const ASSETS = ["./", "./index.html", "./nous.css?v=1", "./nous.js?v=1",
                "./nous-config.js?v=1", "./manifest.webmanifest",
                "./icon-192.png", "./icon-512.png"];

self.addEventListener("install", e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS).catch(()=>{})));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE && k.indexOf("nous-") === 0).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if(req.method !== "GET") return;
  let url; try{ url = new URL(req.url); }catch(_){ return; }
  if(url.origin !== location.origin) return;          // base de données : réseau direct

  const page = req.mode === "navigate" || req.destination === "document";
  if(page){
    e.respondWith(fetch(req).then(r => {
      if(r && r.status === 200){ const c = r.clone(); caches.open(CACHE).then(x => x.put(req, c)).catch(()=>{}); }
      return r;
    }).catch(() => caches.match(req).then(c => c || caches.match("./index.html"))));
    return;
  }
  e.respondWith(caches.match(req).then(c => c || fetch(req).then(r => {
    if(r && r.status === 200){ const cp = r.clone(); caches.open(CACHE).then(x => x.put(req, cp)).catch(()=>{}); }
    return r;
  })));
});
