/* GÉOPOLIS — Carte du monde
 * Rendu canvas : masses continentales schématiques + un point par nation.
 * Zoom molette, déplacement au glisser, survol et sélection.
 * Tout est redessiné en un seul passage : ~200 cercles, aucun coût mesurable.
 */
(function (G) {
  'use strict';

  const CONT = {
    eurasie: [[-9,37],[-9,43],[-2,43],[0,48],[2,51],[4,53],[8,54],[8,57],[5,59],[11,64],[16,69],[28,71],[40,68],[60,70],[75,73],[100,76],[112,74],[130,72],[145,70],[170,68],[180,66],[172,60],[160,60],[155,52],[142,46],[135,43],[128,38],[122,31],[120,24],[110,20],[105,10],[103,1],[100,7],[98,16],[92,21],[89,22],[80,15],[77,8],[72,20],[68,24],[60,25],[57,25],[50,27],[48,30],[43,13],[44,12],[35,28],[34,31],[36,36],[30,40],[28,41],[24,40],[20,40],[16,38],[13,38],[18,40],[13,45],[12,44],[8,44],[3,42],[-2,37]],
    afrique: [[-17,15],[-16,20],[-12,28],[-6,36],[10,37],[25,32],[35,31],[43,12],[51,12],[42,-1],[40,-10],[35,-20],[32,-26],[25,-34],[18,-34],[12,-18],[9,-1],[3,5],[-8,5],[-13,9]],
    amnord: [[-168,66],[-160,71],[-140,70],[-125,70],[-110,68],[-95,68],[-85,70],[-75,68],[-65,60],[-55,52],[-60,47],[-67,45],[-70,42],[-74,40],[-76,35],[-81,25],[-85,30],[-90,29],[-97,26],[-97,20],[-92,15],[-84,10],[-78,8],[-83,15],[-90,17],[-95,17],[-105,20],[-110,24],[-115,30],[-122,37],[-124,45],[-130,54],[-140,60],[-150,60],[-160,58]],
    amsud: [[-79,9],[-72,12],[-62,10],[-52,5],[-50,0],[-44,-2],[-35,-6],[-38,-13],[-42,-22],[-48,-25],[-53,-34],[-58,-38],[-62,-40],[-65,-45],[-68,-52],[-73,-52],[-75,-45],[-73,-38],[-71,-30],[-70,-20],[-75,-14],[-81,-6],[-80,0],[-77,7]],
    australie: [[113,-22],[114,-26],[116,-32],[120,-34],[129,-32],[135,-34],[140,-38],[147,-38],[150,-35],[153,-28],[146,-19],[142,-11],[136,-12],[130,-11],[126,-14],[122,-17]],
    groenland: [[-45,60],[-52,66],[-55,71],[-45,76],[-30,82],[-20,80],[-22,72],[-32,66]],
    inde: [[68,24],[72,20],[75,15],[77,8],[80,13],[82,17],[87,21],[89,22],[80,15]],
    madagascar: [[43,-12],[50,-15],[48,-25],[44,-22],[43,-16]],
    japon: [[130,31],[135,34],[140,36],[142,42],[145,44],[141,45],[138,37],[133,33]],
    gb: [[-5,50],[-6,54],[-5,58],[-2,58],[0,53],[1,51]],
    indonesie: [[95,5],[104,-2],[112,-7],[120,-8],[131,-4],[141,-6],[135,-2],[125,1],[117,3],[108,3],[100,3]],
    nz: [[173,-35],[178,-38],[176,-41],[171,-44],[167,-46],[170,-42]],
    philippines: [[120,18],[124,13],[126,7],[122,6],[119,11]],
    islande: [[-24,64],[-22,66],[-15,66],[-14,64],[-19,63]],
    antarctique: [[-180,-62],[-140,-66],[-100,-72],[-60,-64],[-20,-70],[20,-68],[60,-66],[100,-64],[140,-66],[180,-62],[180,-78],[-180,-78]]
  };

  const C = G.carte = {
    zoom: 1, ox: 0, oy: 0, survol: -1, choisi: -1,
    dpr: 1, largeur: 0, hauteur: 0
  };

  let cv, ctx, glisse = null, surSelection = null;

  G.initCarte = function (canvas, onSelection) {
    cv = canvas; ctx = cv.getContext('2d', { alpha: false });
    surSelection = onSelection;
    redimensionner();
    window.addEventListener('resize', redimensionner);

    cv.addEventListener('mousemove', e => {
      const r = cv.getBoundingClientRect();
      const x = e.clientX - r.left, y = e.clientY - r.top;
      if (glisse) {
        C.ox += x - glisse.x; C.oy += y - glisse.y;
        glisse = { x: x, y: y };
        limiter(); dessiner();
        return;
      }
      const p = paysSous(x, y);
      if (p !== C.survol) { C.survol = p; dessiner(); }
      cv.style.cursor = p >= 0 ? 'pointer' : 'grab';
      C.souris = { x: x, y: y };
    });
    cv.addEventListener('mousedown', e => {
      const r = cv.getBoundingClientRect();
      glisse = { x: e.clientX - r.left, y: e.clientY - r.top, x0: e.clientX, y0: e.clientY };
      cv.style.cursor = 'grabbing';
    });
    window.addEventListener('mouseup', e => {
      if (glisse && Math.abs(e.clientX - glisse.x0) < 4 && Math.abs(e.clientY - glisse.y0) < 4) {
        const r = cv.getBoundingClientRect();
        const p = paysSous(e.clientX - r.left, e.clientY - r.top);
        if (p >= 0) { C.choisi = p; surSelection && surSelection(p); }
      }
      glisse = null;
      if (cv) cv.style.cursor = 'grab';
    });
    cv.addEventListener('mouseleave', () => { C.survol = -1; C.souris = null; dessiner(); });
    cv.addEventListener('wheel', e => {
      e.preventDefault();
      const r = cv.getBoundingClientRect();
      const mx = e.clientX - r.left, my = e.clientY - r.top;
      const k = e.deltaY < 0 ? 1.18 : 1 / 1.18;
      const z2 = G.clamp(C.zoom * k, 1, 9);
      const f = z2 / C.zoom;
      C.ox = mx - (mx - C.ox) * f;
      C.oy = my - (my - C.oy) * f;
      C.zoom = z2;
      limiter(); dessiner();
    }, { passive: false });

    // ── Gestes tactiles : un doigt déplace, deux doigts zooment, une tape
    //    sélectionne. Les événements souris seuls ne suffisent pas sur mobile.
    let toucheDep = null, pince = null;
    const pos = t => { const r = cv.getBoundingClientRect(); return { x: t.clientX - r.left, y: t.clientY - r.top }; };
    const ecart = ts => Math.hypot(ts[0].clientX - ts[1].clientX, ts[0].clientY - ts[1].clientY);

    cv.addEventListener('touchstart', e => {
      if (e.touches.length === 1) {
        const p = pos(e.touches[0]);
        toucheDep = { x: p.x, y: p.y, x0: p.x, y0: p.y, t: Date.now() };
        pince = null;
      } else if (e.touches.length === 2) {
        const r = cv.getBoundingClientRect();
        pince = {
          d: ecart(e.touches), zoom: C.zoom,
          cx: (e.touches[0].clientX + e.touches[1].clientX) / 2 - r.left,
          cy: (e.touches[0].clientY + e.touches[1].clientY) / 2 - r.top
        };
        toucheDep = null;
      }
    }, { passive: true });

    cv.addEventListener('touchmove', e => {
      if (pince && e.touches.length === 2) {
        e.preventDefault();
        const z2 = G.clamp(pince.zoom * (ecart(e.touches) / pince.d), 1, 9);
        const f = z2 / C.zoom;
        C.ox = pince.cx - (pince.cx - C.ox) * f;
        C.oy = pince.cy - (pince.cy - C.oy) * f;
        C.zoom = z2;
        limiter(); dessiner();
      } else if (toucheDep && e.touches.length === 1) {
        e.preventDefault();
        const p = pos(e.touches[0]);
        C.ox += p.x - toucheDep.x; C.oy += p.y - toucheDep.y;
        toucheDep.x = p.x; toucheDep.y = p.y;
        limiter(); dessiner();
      }
    }, { passive: false });

    cv.addEventListener('touchend', e => {
      if (toucheDep && Date.now() - toucheDep.t < 400 &&
          Math.abs(toucheDep.x - toucheDep.x0) < 12 && Math.abs(toucheDep.y - toucheDep.y0) < 12) {
        const p = paysSous(toucheDep.x0, toucheDep.y0);
        if (p >= 0) {
          C.choisi = p; C.survol = p; C.souris = { x: toucheDep.x0, y: toucheDep.y0 };
          dessiner();
          surSelection && surSelection(p);
        }
      }
      toucheDep = null; pince = null;
    }, { passive: true });

    dessiner();
  };

  function redimensionner() {
    if (!cv) return;
    C.dpr = Math.min(window.devicePixelRatio || 1, 2);
    const r = cv.getBoundingClientRect();
    C.largeur = r.width; C.hauteur = r.height;
    cv.width = Math.round(r.width * C.dpr);
    cv.height = Math.round(r.height * C.dpr);
    ctx.setTransform(C.dpr, 0, 0, C.dpr, 0, 0);
    limiter(); dessiner();
  }
  G.redimensionnerCarte = redimensionner;

  // Pixels par degré, identiques en longitude et en latitude : les proportions
  // du monde sont conservées quelle que soit la forme de l'écran.
  function ech() { return (C.largeur / 360) * C.zoom; }

  function limiter() {
    const s = ech(), w = 360 * s, h = 148 * s;
    C.ox = w <= C.largeur ? (C.largeur - w) / 2 : G.clamp(C.ox, C.largeur - w, 0);
    C.oy = h <= C.hauteur ? (C.hauteur - h) / 2 : G.clamp(C.oy, C.hauteur - h, 0);
  }

  function px(lon) { return (lon + 180) * ech() + C.ox; }
  function py(lat) { return (78 - lat) * ech() + C.oy; }

  function paysSous(x, y) {
    const tolerance = ('ontouchstart' in window) ? 30 : 18;   // le doigt est moins précis
    let best = -1, bestD = tolerance * tolerance;
    for (let i = 0; i < G.N; i++) {
      const p = G.PAYS[i];
      const dx = px(p.lon) - x, dy = py(p.lat) - y;
      const d = dx * dx + dy * dy;
      const r = rayon(i) + 4;
      if (d < Math.max(r * r, bestD) && d < bestD) { bestD = d; best = i; }
    }
    return best;
  }

  function rayon(i) {
    const E = G.E;
    const pib = E && E.pib ? E.pib[i] : G.PAYS[i].pib;
    return G.clamp(2.1 + Math.pow(pib, 0.30) * 0.85, 2.4, 17) * Math.min(1 + (C.zoom - 1) * 0.12, 1.6);
  }

  const COUL = {
    joueur:  '#f5c542',
    allie:   '#4fd18b',
    pacte:   '#7ad0e8',
    guerre:  '#ff4d4d',
    sanction:'#c064ff',
    ami:     '#69a8e0',
    neutre:  '#8a95a8',
    hostile: '#e08a5a'
  };

  function statut(i) {
    const E = G.E;
    if (i === E.joueur) return 'joueur';
    if (E.guerres.some(g => (g.a === E.joueur && g.d === i) || (g.d === E.joueur && g.a === i))) return 'guerre';
    if (G.estAllie(E.joueur, i)) return 'allie';
    if (E.sanctions.some(s => (s[0] === E.joueur && s[1] === i) || (s[1] === E.joueur && s[0] === i))) return 'sanction';
    if (E.pactes.some(p => (p[0] === E.joueur && p[1] === i) || (p[1] === E.joueur && p[0] === i))) return 'pacte';
    const r = E.rel[E.joueur * G.N + i];
    if (r > 35) return 'ami';
    if (r < -35) return 'hostile';
    return 'neutre';
  }
  G.statutCarte = statut;

  function dessiner() {
    if (!ctx) return;
    const E = G.E;
    ctx.fillStyle = '#0a1220';
    ctx.fillRect(0, 0, C.largeur, C.hauteur);

    // Grille
    ctx.strokeStyle = 'rgba(120,160,220,0.055)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let lon = -180; lon <= 180; lon += 30) { ctx.moveTo(px(lon), 0); ctx.lineTo(px(lon), C.hauteur); }
    for (let lat = -60; lat <= 75; lat += 15) { ctx.moveTo(0, py(lat)); ctx.lineTo(C.largeur, py(lat)); }
    ctx.stroke();

    // Continents
    ctx.fillStyle = '#16283f';
    ctx.strokeStyle = 'rgba(110,160,215,0.30)';
    ctx.lineWidth = 1;
    for (const k in CONT) {
      const poly = CONT[k];
      ctx.beginPath();
      for (let n = 0; n < poly.length; n++) {
        const x = px(poly[n][0]), y = py(poly[n][1]);
        n === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath(); ctx.fill(); ctx.stroke();
    }

    if (!E || !E.pib) return;

    // Liens : alliances et guerres du joueur
    ctx.lineWidth = 1.4;
    E.alliances.forEach(a => {
      const o = a[0] === E.joueur ? a[1] : a[1] === E.joueur ? a[0] : -1;
      if (o < 0) return;
      ctx.strokeStyle = 'rgba(79,209,139,0.35)';
      trait(E.joueur, o);
    });
    E.guerres.forEach(g => {
      const o = g.a === E.joueur ? g.d : g.d === E.joueur ? g.a : -1;
      if (o < 0) return;
      ctx.strokeStyle = 'rgba(255,77,77,0.6)';
      ctx.lineWidth = 2.4;
      trait(E.joueur, o);
      ctx.lineWidth = 1.4;
    });
    E.contrats.forEach(k => {
      const o = k.v === E.joueur ? k.a : k.a === E.joueur ? k.v : -1;
      if (o < 0) return;
      ctx.strokeStyle = 'rgba(245,197,66,0.22)';
      trait(E.joueur, o);
    });

    // Points
    for (let i = 0; i < G.N; i++) {
      const p = G.PAYS[i];
      const x = px(p.lon), y = py(p.lat);
      if (x < -30 || x > C.largeur + 30 || y < -30 || y > C.hauteur + 30) continue;
      const r = rayon(i), st = statut(i);
      const enG = E.guerres.some(g => g.a === i || g.d === i);

      if (i === E.joueur) {
        const puls = 1 + Math.sin(Date.now() / 420) * 0.16;
        ctx.beginPath(); ctx.arc(x, y, r * 2.1 * puls, 0, 6.2832);
        ctx.fillStyle = 'rgba(245,197,66,0.16)'; ctx.fill();
      }
      ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832);
      ctx.fillStyle = COUL[st]; ctx.fill();
      if (enG && i !== E.joueur) {
        ctx.strokeStyle = '#ff4d4d'; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;
      } else if (i === C.choisi) {
        ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.stroke(); ctx.lineWidth = 1;
      }
      // Étiquette des grandes puissances et des pays survolés
      if ((C.zoom > 2.2 && r > 6) || i === C.survol || i === E.joueur || r > 12) {
        ctx.fillStyle = i === C.survol ? '#fff' : 'rgba(214,228,246,0.78)';
        ctx.font = (i === C.survol || i === E.joueur ? '600 ' : '') + '11px system-ui,sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(p.code, x, y - r - 4);
      }
    }

    // Infobulle
    if (C.survol >= 0 && C.souris) infobulle(C.survol, C.souris.x, C.souris.y);
  }
  G.dessinerCarte = dessiner;

  function trait(a, b) {
    const pa = G.PAYS[a], pb = G.PAYS[b];
    ctx.beginPath();
    const x1 = px(pa.lon), y1 = py(pa.lat), x2 = px(pb.lon), y2 = py(pb.lat);
    const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - Math.abs(x2 - x1) * 0.12;
    ctx.moveTo(x1, y1); ctx.quadraticCurveTo(mx, my, x2, y2); ctx.stroke();
  }

  function infobulle(i, x, y) {
    const E = G.E, p = G.PAYS[i];
    const lignes = [
      `${p.drapeau}  ${p.nom}`,
      `PIB ${G.fmtMd(E.pib[i])}   ·   ${G.fmtPop(E.pop[i])} hab.`,
      `Armée ${G.fmtNb(G.puissance(i, true) / 1000)} k   ·   IA niveau ${E.ia[i] | 0}`,
      i === E.joueur ? 'Votre nation' : `Relations ${E.rel[E.joueur * G.N + i] > 0 ? '+' : ''}${E.rel[E.joueur * G.N + i]}`
    ];
    ctx.font = '12px system-ui,sans-serif';
    let w = 0;
    lignes.forEach((l, n) => { ctx.font = n === 0 ? '600 13px system-ui,sans-serif' : '12px system-ui,sans-serif'; w = Math.max(w, ctx.measureText(l).width); });
    w += 20;
    const h = lignes.length * 17 + 12;
    let bx = x + 14, by = y + 14;
    if (bx + w > C.largeur) bx = x - w - 14;
    if (by + h > C.hauteur) by = y - h - 14;
    ctx.fillStyle = 'rgba(10,18,32,0.95)';
    ctx.strokeStyle = 'rgba(120,170,230,0.45)';
    ctx.beginPath(); ctx.roundRect(bx, by, w, h, 7); ctx.fill(); ctx.stroke();
    ctx.textAlign = 'left';
    lignes.forEach((l, n) => {
      ctx.font = n === 0 ? '600 13px system-ui,sans-serif' : '12px system-ui,sans-serif';
      ctx.fillStyle = n === 0 ? '#fff' : 'rgba(200,215,235,0.85)';
      ctx.fillText(l, bx + 10, by + 20 + n * 17);
    });
  }

  // Vue d'ouverture : la carte remplit l'écran en hauteur et se cale sur la
  // nation du joueur. Sur un téléphone en portrait, sans cela, le monde
  // n'occupe qu'une mince bande au milieu d'un océan de vide.
  G.vueInitiale = function (i) {
    const voulu = (C.hauteur * 0.80 / 148) / (C.largeur / 360);
    C.zoom = G.clamp(voulu, 1, 4);
    const s = ech(), p = G.PAYS[i];
    C.ox = C.largeur / 2 - (p.lon + 180) * s;
    C.oy = C.hauteur / 2 - (78 - p.lat) * s;
    limiter(); dessiner();
  };

  G.centrerSur = function (i) {
    const p = G.PAYS[i];
    C.zoom = Math.max(C.zoom, 2.6);
    const s = ech();
    C.ox = C.largeur / 2 - (p.lon + 180) * s;
    C.oy = C.hauteur / 2 - (78 - p.lat) * s;
    limiter(); dessiner();
  };
})(window.GEO = window.GEO || {});
