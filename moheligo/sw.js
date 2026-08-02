/* MoheliGo — service worker, optimisé pour les connexions lentes.

   ⚠️ CORRECTIF DU 01/08/2026 — LE PLUS IMPORTANT DE CE FICHIER
   Avant : la page était servie DEPUIS LE CACHE d'abord. Résultat, après
   un déploiement, l'utilisateur continuait de voir l'ANCIENNE version
   (parfois plusieurs jours). Les mises à jour n'arrivaient jamais.
   Maintenant : la page est demandée AU RÉSEAU d'abord, avec un repli
   immédiat sur le cache s'il n'y a pas de connexion. On garde donc le
   fonctionnement hors ligne, sans jamais servir du périmé.

   · Page de l'app (HTML)      : réseau d'abord, cache en secours.
   · Images, icônes, manifeste : cache d'abord (elles ne changent pas).
   · Bibliothèques CDN          : cache d'abord (versionnées).
   · Données (API, météo, cartes, Windy) : réseau normal, non intercepté. */

const CACHE = "moheligo-v139";
const ASSETS = [
  "./", "./index.html",
  "./MoheliGo-logo.png", "./MoheliGo-banner.jpg",
  "./icon-192.png", "./icon-512.png", "./manifest.webmanifest",
  "./admin.html", "./manifest-admin.webmanifest"
];
const CDN_HOSTS = ["cdn.jsdelivr.net", "unpkg.com", "fonts.googleapis.com", "fonts.gstatic.com"];

self.addEventListener("install", e => {
  self.skipWaiting();
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS).catch(() => {})));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

/* Est-ce la page elle-même ? (navigation, ou un .html) */
function estLaPage(req, url) {
  return req.mode === "navigate"
      || (req.destination === "document")
      || /\.html$/.test(url.pathname)
      || url.pathname === "/";
}

self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET") return;
  let url;
  try { url = new URL(req.url); } catch (_) { return; }

  if (url.origin === location.origin) {

    // 1) LA PAGE : réseau d'abord — l'utilisateur a toujours la dernière version
    if (estLaPage(req, url)) {
      e.respondWith(
        fetch(req).then(res => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
          }
          return res;
        }).catch(() =>
          // pas de réseau : on ressort la dernière version connue
          caches.match(req).then(c => c || caches.match("./index.html"))
        )
      );
      return;
    }

    // 2) Images, icônes, manifeste : cache d'abord + rafraîchissement discret
    e.respondWith(
      caches.match(req).then(cached => {
        const network = fetch(req).then(res => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
          }
          return res;
        }).catch(() => cached);
        return cached || network;
      })
    );
    return;
  }

  // 3) Bibliothèques/polices CDN : cache d'abord (elles ne changent pas)
  if (CDN_HOSTS.indexOf(url.hostname) >= 0) {
    e.respondWith(
      caches.match(req).then(cached => cached || fetch(req).then(res => {
        if (res && (res.status === 200 || res.type === "opaque")) {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {});
        }
        return res;
      }).catch(() => cached))
    );
    return;
  }

  // 4) Tout le reste (API données, tuiles, Windy) : réseau normal
});

/* ===== NOTIFICATIONS PUSH ===== */
self.addEventListener("push", e => {
  let d = {};
  try { d = e.data ? e.data.json() : {}; } catch (_) { try { d = { title: "MoheliGo", body: e.data.text() }; } catch (__) {} }
  const title = d.title || "MoheliGo";
  const opts = {
    body: d.body || "",
    icon: d.icon || "./icon-192.png",
    badge: "./icon-192.png",
    image: d.image || undefined,
    tag: d.tag || undefined,
    data: { url: d.url || "./" },
    vibrate: [80, 40, 80]
  };
  e.waitUntil(self.registration.showNotification(title, opts));
});

self.addEventListener("notificationclick", e => {
  e.notification.close();
  const target = (e.notification.data && e.notification.data.url) || "./";
  e.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then(list => {
      for (const c of list) { if ("focus" in c) { c.navigate(target).catch(() => {}); return c.focus(); } }
      if (self.clients.openWindow) return self.clients.openWindow(target);
    })
  );
});
