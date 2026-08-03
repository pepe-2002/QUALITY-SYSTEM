/* ================================================================
   🎨 STUDIO MOHELIGO — bibliothèque de dessin (canvas 2D)
   Tout est dessiné à la main, en vectoriel : décors de Mohéli,
   personnages articulés, vedette, téléphone avec l'appli.
   Aucune image extérieure : le rendu est identique à chaque fois.
   ================================================================ */
(function (global) {
  "use strict";

  /* ---------- palette MoheliGo ---------- */
  var C = {
    nuit: "#0a2550", bleu: "#123a72", bleuClair: "#2a6fd4",
    jaune: "#F6BC1C", jauneClair: "#ffd75e",
    mer: "#0e7fa8", merClair: "#3fc6d8", merSombre: "#0a5c81",
    sable: "#f0dcb0", sableOmbre: "#d9bf8c",
    vert: "#1f7a4d", vertClair: "#37a862", vertSombre: "#14563a",
    blanc: "#ffffff", crème: "#fdf6e7",
    toit: "#a8452f", toitClair: "#c85c42", mur: "#efe3cd",
    peau: ["#8d5524", "#6b3f16", "#a9682f", "#7a4a1d"],
    tissu: ["#e94f6a", "#f6bc1c", "#1fb6a6", "#7b4fd4", "#ef7d3b", "#2a6fd4"]
  };

  /* ---------- utilitaires ---------- */
  function lerp(a, b, k) { return a + (b - a) * k; }
  function clamp(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function ease(k) { return k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2; }
  /* générateur pseudo-aléatoire déterministe (même graine = même image) */
  function rng(graine) {
    var s = graine >>> 0 || 1;
    return function () { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
  }
  function rrect(x, y, w, h, r) {
    var c = this; r = Math.min(r, w / 2, h / 2);
    c.beginPath();
    c.moveTo(x + r, y); c.lineTo(x + w - r, y); c.quadraticCurveTo(x + w, y, x + w, y + r);
    c.lineTo(x + w, y + h - r); c.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    c.lineTo(x + r, y + h); c.quadraticCurveTo(x, y + h, x, y + h - r);
    c.lineTo(x, y + r); c.quadraticCurveTo(x, y, x + r, y); c.closePath();
  }
  function grad(c, x0, y0, x1, y1, stops) {
    var g = c.createLinearGradient(x0, y0, x1, y1);
    stops.forEach(function (s) { g.addColorStop(s[0], s[1]); });
    return g;
  }
  /* éclaircir / assombrir une couleur #rrggbb (pour le volume des tissus) */
  function teinte(hex, k) {
    var m = /^#?([\da-f]{2})([\da-f]{2})([\da-f]{2})$/i.exec(hex || "");
    if (!m) return hex;
    var v = [1, 2, 3].map(function (i) {
      return clamp(Math.round(parseInt(m[i], 16) * k), 0, 255);
    });
    return "rgb(" + v[0] + "," + v[1] + "," + v[2] + ")";
  }
  /* capsule (bras, jambes) */
  function capsule(c, x0, y0, x1, y1, ep, couleur) {
    c.strokeStyle = couleur; c.lineWidth = ep; c.lineCap = "round";
    c.beginPath(); c.moveTo(x0, y0); c.lineTo(x1, y1); c.stroke();
  }

  /* ================================================================
     CIEL — moment: 'aube' | 'jour' | 'or' (fin d'après-midi)
     ================================================================ */
  function ciel(c, W, H, t, moment) {
    var jeux = {
      aube: [[0, "#2b4d8f"], [0.35, "#7a6bb0"], [0.62, "#f39a72"], [1, "#ffd9a0"]],
      jour: [[0, "#1e6fd0"], [0.55, "#68b8f0"], [1, "#c9ecff"]],
      or: [[0, "#1b4f8f"], [0.45, "#f0864e"], [1, "#ffd48a"]]
    };
    c.fillStyle = grad(c, 0, 0, 0, H * 0.62, jeux[moment] || jeux.jour);
    c.fillRect(0, 0, W, H);
    /* soleil */
    var sx = moment === "aube" ? W * 0.74 : W * 0.28, sy = H * (moment === "jour" ? 0.13 : 0.29);
    var g = c.createRadialGradient(sx, sy, 4, sx, sy, W * 0.42);
    g.addColorStop(0, "rgba(255,246,214,.95)"); g.addColorStop(0.25, "rgba(255,225,150,.45)");
    g.addColorStop(1, "rgba(255,225,150,0)");
    c.fillStyle = g; c.fillRect(0, 0, W, H * 0.7);
    c.fillStyle = moment === "jour" ? "#fff9dd" : "#ffe9a8";
    c.beginPath(); c.arc(sx, sy, W * 0.058, 0, 7); c.fill();
    /* nuages qui dérivent lentement */
    var r = rng(7);
    for (var i = 0; i < 6; i++) {
      var base = r() * W, y = H * (0.06 + r() * 0.22), s = 0.5 + r() * 0.9;
      var x = (base + t * (6 + i * 3)) % (W + 500) - 250;
      nuage(c, x, y, s, "rgba(255,255,255," + (0.34 + i * 0.06) + ")");
    }
  }
  function nuage(c, x, y, s, couleur) {
    c.fillStyle = couleur; c.beginPath();
    c.ellipse(x, y, 120 * s, 46 * s, 0, 0, 7);
    c.ellipse(x + 90 * s, y + 10 * s, 80 * s, 36 * s, 0, 0, 7);
    c.ellipse(x - 95 * s, y + 14 * s, 70 * s, 30 * s, 0, 0, 7);
    c.fill();
  }

  /* ================================================================
     MER — nappes de vagues animées, de y0 jusqu'en bas
     agitation : 0 calme · 1 modérée · 2 agitée
     ================================================================ */
  function mer(c, W, H, t, y0, agitation) {
    agitation = agitation || 0;
    c.fillStyle = grad(c, 0, y0, 0, H, [[0, C.merClair], [0.35, C.mer], [1, C.merSombre]]);
    c.fillRect(0, y0, W, H - y0);
    var amp = 5 + agitation * 9;
    for (var n = 0; n < 5; n++) {
      var yy = y0 + (H - y0) * (0.08 + n * 0.2), vit = 0.5 + n * 0.35, a = amp * (0.6 + n * 0.35);
      c.fillStyle = "rgba(255,255,255," + (0.06 + n * 0.03) + ")";
      c.beginPath(); c.moveTo(-40, yy);
      for (var x = -40; x <= W + 40; x += 24) {
        c.lineTo(x, yy + Math.sin(x / (150 - n * 18) + t * vit) * a);
      }
      c.lineTo(W + 40, yy + 70); c.lineTo(-40, yy + 70); c.closePath(); c.fill();
    }
    /* éclats de lumière */
    var r = rng(23);
    for (var i = 0; i < 26; i++) {
      var ex = r() * W, ey = y0 + r() * (H - y0), ph = r() * 6.28;
      var al = 0.18 + 0.22 * (0.5 + 0.5 * Math.sin(t * 2.4 + ph));
      c.fillStyle = "rgba(255,255,255," + al.toFixed(3) + ")";
      c.beginPath(); c.ellipse(ex, ey, 16 + r() * 22, 2.6, 0, 0, 7); c.fill();
    }
  }

  /* ================================================================
     RELIEF : l'île de Mohéli au loin
     ================================================================ */
  function ile(c, x, yBase, larg, haut, couleur, brume) {
    c.fillStyle = couleur;
    c.beginPath(); c.moveTo(x - larg / 2, yBase);
    c.quadraticCurveTo(x - larg * 0.28, yBase - haut * 1.05, x - larg * 0.05, yBase - haut * 0.72);
    c.quadraticCurveTo(x + larg * 0.16, yBase - haut * 1.15, x + larg * 0.34, yBase - haut * 0.6);
    c.quadraticCurveTo(x + larg * 0.44, yBase - haut * 0.3, x + larg / 2, yBase);
    c.closePath(); c.fill();
    if (brume) { c.fillStyle = "rgba(255,255,255,.16)"; c.fill(); }
  }

  /* ================================================================
     PALMIER — le tronc plie, les palmes ondulent
     ================================================================ */
  function palmier(c, x, y, s, t, graine) {
    var r = rng(graine || 3), pli = Math.sin(t * 0.8 + (graine || 0)) * 0.05;
    c.save(); c.translate(x, y); c.scale(s, s); c.rotate(pli);
    c.strokeStyle = "#7a5230"; c.lineWidth = 26; c.lineCap = "round";
    c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(24, -170, 8, -330); c.stroke();
    c.strokeStyle = "#8d6238"; c.lineWidth = 8;
    for (var k = 0; k < 6; k++) { c.beginPath(); c.moveTo(2 + k, -40 - k * 46); c.lineTo(20 + k, -46 - k * 46); c.stroke(); }
    var nb = 7;
    for (var i = 0; i < nb; i++) {
      var a = -Math.PI / 2 + (i - (nb - 1) / 2) * 0.52 + Math.sin(t * 1.4 + i) * 0.045;
      var L = 190 + r() * 60;
      c.save(); c.translate(8, -330); c.rotate(a + Math.PI / 2);
      c.fillStyle = i % 2 ? C.vert : C.vertClair;
      c.beginPath(); c.moveTo(0, 0);
      c.quadraticCurveTo(L * 0.5, -46, L, 6);
      c.quadraticCurveTo(L * 0.5, 22, 0, 0);
      c.fill(); c.restore();
    }
    c.fillStyle = "#6d4a2a"; c.beginPath(); c.arc(8, -330, 16, 0, 7); c.fill();
    c.restore();
  }

  /* ================================================================
     MAISON comorienne (murs clairs, toit de tôle)
     ================================================================ */
  function maison(c, x, y, l, h, teinte) {
    c.fillStyle = teinte || C.mur; rrect.call(c, x - l / 2, y - h, l, h, 6); c.fill();
    c.fillStyle = "rgba(0,0,0,.12)"; c.fillRect(x - l / 2, y - h, l * 0.22, h);
    c.fillStyle = C.toit;
    c.beginPath(); c.moveTo(x - l / 2 - 22, y - h); c.lineTo(x + l / 2 + 22, y - h);
    c.lineTo(x + l / 2 - 6, y - h - 52); c.lineTo(x - l / 2 + 6, y - h - 52); c.closePath(); c.fill();
    c.strokeStyle = "rgba(0,0,0,.10)"; c.lineWidth = 3;
    for (var i = 1; i < 6; i++) {
      c.beginPath(); c.moveTo(x - l / 2 - 22 + i * (l + 44) / 6, y - h);
      c.lineTo(x - l / 2 + 6 + i * (l - 12) / 6, y - h - 52); c.stroke();
    }
    c.fillStyle = C.nuit; rrect.call(c, x - l * 0.34, y - h * 0.62, l * 0.2, h * 0.28, 4); c.fill();
    c.fillStyle = "#6b4a2c"; rrect.call(c, x + l * 0.1, y - h * 0.72, l * 0.22, h * 0.72, 4); c.fill();
  }

  /* ================================================================
     VEDETTE MoheliGo — vue de profil, tangage et sillage
     ================================================================ */
  function vedette(c, x, y, s, t, vitesse) {
    var tang = Math.sin(t * 1.6) * 0.020 * (vitesse ? 1.7 : 1);
    var monte = Math.sin(t * 1.6 + 0.6) * 8 * s;
    c.save(); c.translate(x, y + monte); c.scale(s, s); c.rotate(tang);

    /* sillage derrière la poupe */
    if (vitesse) {
      c.fillStyle = "rgba(255,255,255,.5)";
      c.beginPath(); c.moveTo(-192, 20);
      c.quadraticCurveTo(-340, 8 + Math.sin(t * 7) * 5, -500, 30);
      c.quadraticCurveTo(-340, 50, -192, 42); c.fill();
    }

    /* coque : poupe à gauche, étrave relevée à droite */
    c.fillStyle = C.blanc;
    c.beginPath();
    c.moveTo(-196, -14);                       // haut de la poupe
    c.lineTo(150, -30);                        // ligne de pont vers l'avant
    c.quadraticCurveTo(236, -34, 240, 8);      // étrave
    c.quadraticCurveTo(210, 40, 120, 44);      // dessous de l'étrave
    c.lineTo(-168, 40);
    c.quadraticCurveTo(-202, 30, -196, -14);
    c.closePath(); c.fill();
    /* bande bleue de flottaison */
    c.save(); c.clip();
    c.fillStyle = C.bleuClair; c.fillRect(-210, 14, 470, 40);
    c.fillStyle = C.jaune; c.fillRect(-210, 6, 470, 9);
    c.fillStyle = "rgba(0,0,0,.08)"; c.fillRect(-210, -34, 470, 10);
    c.restore();

    /* cabine + pare-brise incliné (d'un seul tenant) */
    c.fillStyle = C.crème;
    c.beginPath();
    c.moveTo(-110, -14); c.lineTo(-110, -96);
    c.quadraticCurveTo(-110, -110, -94, -110);
    c.lineTo(76, -110); c.quadraticCurveTo(92, -110, 100, -96);
    c.lineTo(134, -40); c.quadraticCurveTo(140, -26, 124, -22);
    c.lineTo(-110, -14); c.closePath(); c.fill();
    c.fillStyle = "rgba(0,0,0,.07)"; c.fillRect(-110, -30, 240, 16);
    /* vitres */
    c.fillStyle = "#173a63"; rrect.call(c, -92, -96, 72, 42, 9); c.fill();
    rrect.call(c, -8, -96, 72, 42, 9); c.fill();
    c.fillStyle = "#1d4c7f";
    c.beginPath(); c.moveTo(78, -96); c.lineTo(104, -54); c.lineTo(78, -54); c.closePath(); c.fill();
    c.fillStyle = "rgba(255,255,255,.28)";
    c.beginPath(); c.moveTo(-88, -54); c.lineTo(-56, -96); c.lineTo(-40, -96); c.lineTo(-72, -54); c.closePath(); c.fill();
    /* casquette de toit */
    c.fillStyle = C.blanc; rrect.call(c, -118, -122, 232, 16, 8); c.fill();

    /* mât + fanion */
    c.strokeStyle = "#cfd8e4"; c.lineWidth = 5;
    c.beginPath(); c.moveTo(-70, -122); c.lineTo(-70, -186); c.stroke();
    c.fillStyle = C.jaune;
    c.beginPath(); c.moveTo(-68, -186); c.lineTo(-68 + 56 + Math.sin(t * 6) * 7, -175);
    c.lineTo(-68, -163); c.closePath(); c.fill();

    /* nom sur la coque */
    c.fillStyle = C.nuit; c.font = "700 24px Poppins, sans-serif"; c.textAlign = "left";
    c.fillText("MoheliGo", -96, -22);

    /* écume à la ligne de flottaison + gerbe d'étrave */
    c.fillStyle = "rgba(255,255,255,.85)";
    c.beginPath(); c.moveTo(-200, 40);
    for (var wx = -200; wx <= 250; wx += 26) c.lineTo(wx, 40 + Math.sin(wx / 40 + t * 5) * 5);
    c.lineTo(250, 70); c.lineTo(-200, 70); c.closePath(); c.fill();
    if (vitesse) {
      c.fillStyle = "rgba(255,255,255,.8)";
      c.beginPath(); c.ellipse(228, 34, 54 + Math.sin(t * 8) * 8, 20, -0.25, 0, 7); c.fill();
      c.beginPath(); c.ellipse(268, 26, 26, 12, -0.3, 0, 7); c.fill();
    }
    c.restore();
  }

  /* ================================================================
     PERSONNAGE
     p = {x,y,h, peau, tenue, motif, coiffe:'shiromani|kofia|cheveux|foulard',
          pose:'debout|marche|assis', dir:1|-1, bouche:0..1, clign:0..1,
          bras:'repos|telephone|salut|ouverts|valise', sourire:0..1, graine}
     y = le SOL sous les pieds · h = hauteur totale en pixels
     ================================================================ */
  function personnage(c, p, t) {
    var h = p.h, x = p.x, y = p.y, dir = p.dir || 1;
    var peau = p.peau || C.peau[0], tissu = p.tenue || C.tissu[0];
    var marche = p.pose === "marche", assis = p.pose === "assis";
    var pas = marche ? Math.sin(t * 6.2) : 0;
    var bob = marche ? Math.abs(Math.sin(t * 6.2)) * h * 0.012 : Math.sin(t * 1.4 + (p.graine || 0)) * h * 0.004;

    var tete = h * 0.155;             // rayon de la tête
    var yTete = y - h + tete + bob;   // centre de la tête
    var yEpaule = yTete + tete * 1.5;
    var yBassin = yEpaule + h * (assis ? 0.20 : 0.30);
    var yPied = assis ? yBassin + h * 0.16 : y + bob;

    c.save();
    /* ombre portée */
    c.fillStyle = "rgba(0,0,0,.18)";
    c.beginPath(); c.ellipse(x, y + 4, h * 0.16, h * 0.026, 0, 0, 7); c.fill();

    /* jambes */
    var largeEp = h * 0.115;
    if (!assis) {
      capsule(c, x - largeEp * 0.4, yBassin, x - largeEp * 0.5 + pas * h * 0.05, yPied, h * 0.055, "#40312a");
      capsule(c, x + largeEp * 0.4, yBassin, x + largeEp * 0.5 - pas * h * 0.05, yPied, h * 0.055, "#4a392f");
    } else {
      capsule(c, x, yBassin, x + dir * h * 0.13, yBassin + h * 0.02, h * 0.055, "#40312a");
      capsule(c, x + dir * h * 0.13, yBassin + h * 0.02, x + dir * h * 0.15, yPied, h * 0.05, "#4a392f");
    }

    /* corps : robe (femme) ou chemise+pantalon (homme) — avec volume */
    var gTissu = c.createLinearGradient(x, yEpaule - h * 0.02, x, yBassin + h * 0.18);
    gTissu.addColorStop(0, teinte(tissu, 1.12));
    gTissu.addColorStop(0.55, tissu);
    gTissu.addColorStop(1, teinte(tissu, 0.72));
    c.fillStyle = gTissu;
    if (p.robe !== false) {
      c.beginPath();
      c.moveTo(x - largeEp, yEpaule);
      c.lineTo(x + largeEp, yEpaule);
      c.quadraticCurveTo(x + largeEp * 1.5, yBassin, x + largeEp * 1.75, yBassin + h * (assis ? 0.06 : 0.16));
      c.lineTo(x - largeEp * 1.75, yBassin + h * (assis ? 0.06 : 0.16));
      c.quadraticCurveTo(x - largeEp * 1.5, yBassin, x - largeEp, yEpaule);
      c.closePath(); c.fill();
      /* motif du tissu */
      if (p.motif) {
        c.save(); c.clip();
        c.fillStyle = p.motif;
        for (var i = 0; i < 7; i++) {
          c.beginPath();
          c.ellipse(x - largeEp * 1.4 + (i % 4) * largeEp * 0.95, yEpaule + h * 0.06 + Math.floor(i / 4) * h * 0.11,
            h * 0.018, h * 0.028, 0.5, 0, 7); c.fill();
        }
        c.restore();
      }
    } else {
      rrect.call(c, x - largeEp, yEpaule, largeEp * 2, yBassin - yEpaule + h * 0.04, h * 0.03); c.fill();
    }
    /* col */
    c.fillStyle = "rgba(0,0,0,.13)";
    c.beginPath(); c.ellipse(x, yEpaule + h * 0.008, largeEp * 0.42, h * 0.016, 0, 0, 7); c.fill();

    /* bras */
    var epX = largeEp * 0.92, brasC = peau, ep = h * 0.045;
    var yMain = yEpaule + h * 0.20;
    if (p.bras === "telephone") {
      /* bras droit replié : le téléphone est tenu devant la poitrine */
      var cx0 = x + dir * largeEp * 0.55, cy0 = yEpaule + h * 0.10;
      capsule(c, x + dir * epX, yEpaule + h * 0.03, x + dir * epX * 1.18, yEpaule + h * 0.15, ep, brasC);
      capsule(c, x + dir * epX * 1.18, yEpaule + h * 0.15, cx0, cy0, ep, brasC);
      capsule(c, x - dir * epX, yEpaule + h * 0.03, x - dir * epX * 1.1, yMain + h * 0.03, ep, brasC);
      /* le téléphone dans la main */
      c.save(); c.translate(cx0, cy0); c.rotate(dir * -0.18);
      c.fillStyle = "#16202e"; rrect.call(c, -h * 0.032, -h * 0.058, h * 0.064, h * 0.116, h * 0.012); c.fill();
      c.fillStyle = "#123a72"; rrect.call(c, -h * 0.026, -h * 0.05, h * 0.052, h * 0.1, h * 0.008); c.fill();
      c.fillStyle = C.jaune; c.fillRect(-h * 0.018, -h * 0.036, h * 0.036, h * 0.006);
      c.fillStyle = "rgba(255,255,255,.5)"; c.fillRect(-h * 0.018, -h * 0.02, h * 0.026, h * 0.005);
      c.restore();
      c.fillStyle = brasC;
      c.beginPath(); c.arc(cx0 + dir * h * 0.026, cy0 + h * 0.012, h * 0.024, 0, 7); c.fill();
    } else if (p.bras === "salut") {
      var ag = Math.sin(t * 5) * 0.25;
      capsule(c, x - epX, yEpaule + h * 0.03, x - epX * 1.3, yMain, ep, brasC);
      capsule(c, x + epX, yEpaule + h * 0.03, x + epX * 1.5 + ag * h * 0.05, yEpaule - h * 0.10, ep, brasC);
      c.fillStyle = brasC;
      c.beginPath(); c.arc(x + epX * 1.5 + ag * h * 0.05, yEpaule - h * 0.10, h * 0.028, 0, 7); c.fill();
    } else if (p.bras === "ouverts") {
      capsule(c, x - epX, yEpaule + h * 0.03, x - epX * 1.9, yEpaule + h * 0.02, ep, brasC);
      capsule(c, x + epX, yEpaule + h * 0.03, x + epX * 1.9, yEpaule + h * 0.02, ep, brasC);
    } else if (p.bras === "valise") {
      capsule(c, x - epX, yEpaule + h * 0.03, x - epX * 1.15, yMain, ep, brasC);
      capsule(c, x + epX, yEpaule + h * 0.03, x + epX * 0.9, yMain, ep, brasC);
      var vx = x - epX * 1.15, vy = yMain + h * 0.02;
      c.strokeStyle = "#5b4632"; c.lineWidth = h * 0.008;
      c.beginPath(); c.arc(vx, vy + h * 0.03, h * 0.028, Math.PI, 0); c.stroke();
      c.fillStyle = "#c96a2e"; rrect.call(c, vx - h * 0.05, vy + h * 0.03, h * 0.1, h * 0.085, h * 0.012); c.fill();
      c.fillStyle = "rgba(0,0,0,.15)"; c.fillRect(vx - h * 0.05, vy + h * 0.058, h * 0.1, h * 0.012);
    } else {
      capsule(c, x - epX, yEpaule + h * 0.03, x - epX * 1.12, yMain + h * 0.03, ep, brasC);
      capsule(c, x + epX, yEpaule + h * 0.03, x + epX * 1.12, yMain + h * 0.03, ep, brasC);
    }

    /* cou + tête */
    capsule(c, x, yTete + tete * 0.6, x, yEpaule + h * 0.01, h * 0.05, peau);
    c.fillStyle = peau;
    c.beginPath(); c.ellipse(x, yTete, tete * 0.86, tete, 0, 0, 7); c.fill();
    /* oreilles */
    c.beginPath(); c.ellipse(x - tete * 0.85, yTete + tete * 0.06, tete * 0.14, tete * 0.2, 0, 0, 7); c.fill();
    c.beginPath(); c.ellipse(x + tete * 0.85, yTete + tete * 0.06, tete * 0.14, tete * 0.2, 0, 0, 7); c.fill();

    /* coiffe */
    var coif = p.coiffe || "cheveux";
    if (coif === "shiromani" || coif === "foulard") {
      c.fillStyle = p.coifCouleur || "#e94f6a";
      c.beginPath();
      c.moveTo(x - tete * 1.02, yTete + tete * 0.35);
      c.quadraticCurveTo(x - tete * 1.15, yTete - tete * 1.25, x, yTete - tete * 1.18);
      c.quadraticCurveTo(x + tete * 1.15, yTete - tete * 1.25, x + tete * 1.02, yTete + tete * 0.35);
      c.quadraticCurveTo(x + tete * 1.2, yTete + tete * 1.5, x + tete * 0.5, yTete + tete * 1.5);
      c.lineTo(x - tete * 0.5, yTete + tete * 1.5);
      c.quadraticCurveTo(x - tete * 1.2, yTete + tete * 1.5, x - tete * 1.02, yTete + tete * 0.35);
      c.closePath(); c.fill();
      /* visage dégagé */
      c.fillStyle = peau;
      c.beginPath(); c.ellipse(x, yTete + tete * 0.06, tete * 0.72, tete * 0.86, 0, 0, 7); c.fill();
      /* liseré du voile (jamais de motif sur le visage) */
      c.strokeStyle = "rgba(255,255,255,.45)"; c.lineWidth = tete * 0.07;
      c.beginPath();
      c.moveTo(x - tete * 0.78, yTete + tete * 0.62);
      c.quadraticCurveTo(x - tete * 0.9, yTete - tete * 0.85, x, yTete - tete * 1.0);
      c.quadraticCurveTo(x + tete * 0.9, yTete - tete * 0.85, x + tete * 0.78, yTete + tete * 0.62);
      c.stroke();
      c.fillStyle = "rgba(0,0,0,.10)";
      c.beginPath();
      c.moveTo(x - tete * 1.02, yTete + tete * 0.9);
      c.quadraticCurveTo(x, yTete + tete * 1.2, x + tete * 1.02, yTete + tete * 0.9);
      c.lineTo(x + tete * 0.9, yTete + tete * 1.5);
      c.lineTo(x - tete * 0.9, yTete + tete * 1.5); c.closePath(); c.fill();
    } else if (coif === "kofia") {
      /* cheveux courts d'abord, PUIS le kofia posé dessus */
      c.fillStyle = "#1a1310";
      c.beginPath(); c.ellipse(x, yTete - tete * 0.12, tete * 0.90, tete * 0.78, 0, Math.PI, 0); c.fill();
      c.fillStyle = "#fdfdf5";
      c.beginPath();
      c.moveTo(x - tete * 0.80, yTete - tete * 0.58);
      c.lineTo(x + tete * 0.80, yTete - tete * 0.58);
      c.quadraticCurveTo(x + tete * 0.76, yTete - tete * 1.14, x, yTete - tete * 1.14);
      c.quadraticCurveTo(x - tete * 0.76, yTete - tete * 1.14, x - tete * 0.80, yTete - tete * 0.58);
      c.closePath(); c.fill();
      c.fillStyle = "#d9c98f";
      for (var q = 0; q < 5; q++) {
        c.beginPath(); c.arc(x - tete * 0.5 + q * tete * 0.25, yTete - tete * 0.74, tete * 0.055, 0, 7); c.fill();
      }
      c.fillStyle = "rgba(0,0,0,.14)";
      c.fillRect(x - tete * 0.80, yTete - tete * 0.62, tete * 1.60, tete * 0.05);
    } else {
      c.fillStyle = p.coifCouleur || "#1a1310";
      c.beginPath(); c.ellipse(x, yTete - tete * 0.22, tete * 0.94, tete * 0.86, 0, Math.PI, 0); c.fill();
      c.beginPath(); c.ellipse(x - tete * 0.8, yTete + tete * 0.1, tete * 0.2, tete * 0.5, 0, 0, 7); c.fill();
      c.beginPath(); c.ellipse(x + tete * 0.8, yTete + tete * 0.1, tete * 0.2, tete * 0.5, 0, 0, 7); c.fill();
    }

    /* yeux (clignement) */
    var ouvert = 1 - (p.clign || 0), ex = tete * 0.34, ey = yTete + tete * 0.02;
    c.fillStyle = C.blanc;
    [-1, 1].forEach(function (s) {
      c.beginPath(); c.ellipse(x + s * ex, ey, tete * 0.17, tete * 0.14 * ouvert + 0.5, 0, 0, 7); c.fill();
    });
    c.fillStyle = "#1a1310";
    [-1, 1].forEach(function (s) {
      c.beginPath(); c.ellipse(x + s * ex + dir * tete * 0.03, ey, tete * 0.085, tete * 0.1 * ouvert + 0.5, 0, 0, 7); c.fill();
    });
    /* reflet dans l'œil : c'est ce qui rend un regard vivant */
    if (ouvert > 0.4) {
      c.fillStyle = "rgba(255,255,255,.9)";
      [-1, 1].forEach(function (s) {
        c.beginPath();
        c.arc(x + s * ex + dir * tete * 0.055, ey - tete * 0.045, tete * 0.028 * ouvert, 0, 7); c.fill();
      });
    }
    /* ombre douce sous le menton */
    c.fillStyle = "rgba(60,30,10,.16)";
    c.beginPath(); c.ellipse(x, yTete + tete * 0.92, tete * 0.5, tete * 0.16, 0, 0, 7); c.fill();
    /* sourcils */
    c.strokeStyle = "#1a1310"; c.lineWidth = tete * 0.055; c.lineCap = "round";
    [-1, 1].forEach(function (s) {
      c.beginPath();
      c.moveTo(x + s * ex - tete * 0.16, ey - tete * 0.3 - (p.sourcils || 0) * tete * 0.1);
      c.quadraticCurveTo(x + s * ex, ey - tete * 0.4 - (p.sourcils || 0) * tete * 0.14, x + s * ex + tete * 0.16, ey - tete * 0.28);
      c.stroke();
    });
    /* nez */
    c.strokeStyle = "rgba(0,0,0,.28)"; c.lineWidth = tete * 0.05;
    c.beginPath(); c.moveTo(x + dir * tete * 0.02, ey + tete * 0.16);
    c.quadraticCurveTo(x + dir * tete * 0.1, ey + tete * 0.3, x + dir * tete * 0.01, ey + tete * 0.34); c.stroke();

    /* bouche : s'ouvre avec la voix, sourit au repos */
    var b = clamp(p.bouche || 0, 0, 1), my = yTete + tete * 0.56;
    if (b > 0.08) {
      c.fillStyle = "#5a1f22";
      c.beginPath(); c.ellipse(x, my, tete * (0.2 + b * 0.1), tete * (0.05 + b * 0.22), 0, 0, 7); c.fill();
      c.fillStyle = "#fff";
      c.beginPath(); c.ellipse(x, my - tete * (0.03 + b * 0.14), tete * (0.16 + b * 0.06), tete * 0.045, 0, 0, 7); c.fill();
    } else {
      c.strokeStyle = "#7a2f28"; c.lineWidth = tete * 0.06;
      c.beginPath();
      c.moveTo(x - tete * 0.2, my - tete * 0.02);
      c.quadraticCurveTo(x, my + tete * (0.1 + (p.sourire || 0.4) * 0.16), x + tete * 0.2, my - tete * 0.02);
      c.stroke();
    }
    c.restore();
  }

  /* ================================================================
     TÉLÉPHONE avec l'appli MoheliGo
     ecran : 'accueil' | 'recherche' | 'resultats' | 'paiement' | 'billet'
     ================================================================ */
  function telephone(c, x, y, s, ecran, t, prog) {
    c.save(); c.translate(x, y); c.scale(s, s);
    var W = 300, H = 620;
    c.fillStyle = "rgba(0,0,0,.28)"; rrect.call(c, -W / 2 + 8, -H / 2 + 14, W, H, 42); c.fill();
    c.fillStyle = "#16202e"; rrect.call(c, -W / 2, -H / 2, W, H, 42); c.fill();
    c.fillStyle = "#0a2550"; rrect.call(c, -W / 2 + 10, -H / 2 + 10, W - 20, H - 20, 34); c.fill();
    c.save(); rrect.call(c, -W / 2 + 10, -H / 2 + 10, W - 20, H - 20, 34); c.clip();
    var ex = -W / 2 + 10, ey = -H / 2 + 10, ew = W - 20, eh = H - 20;
    /* fond appli */
    c.fillStyle = grad(c, ex, ey, ex, ey + eh, [[0, "#0a2550"], [0.6, "#123a72"], [1, "#0a2550"]]);
    c.fillRect(ex, ey, ew, eh);
    c.fillStyle = "rgba(255,255,255,.9)"; c.font = "600 13px Inter, sans-serif"; c.textAlign = "left";
    c.fillText("7:12", ex + 18, ey + 26);
    c.textAlign = "right"; c.fillText("▮▮▮", ex + ew - 18, ey + 26);
    c.textAlign = "center";
    c.fillStyle = C.jaune; c.font = "900 22px Poppins, sans-serif";
    c.fillText("MoheliGo", ex + ew / 2, ey + 62);

    function carte(yy, hh) {
      c.fillStyle = "rgba(255,255,255,.10)"; rrect.call(c, ex + 16, yy, ew - 32, hh, 16); c.fill();
      c.strokeStyle = "rgba(255,255,255,.18)"; c.lineWidth = 1.5; c.stroke();
    }
    if (ecran === "recherche") {
      carte(ey + 86, 172);
      c.textAlign = "left"; c.fillStyle = "rgba(255,255,255,.6)"; c.font = "400 12px Inter, sans-serif";
      c.fillText("DÉPART", ex + 32, ey + 112);
      c.fillStyle = "#fff"; c.font = "600 17px Inter, sans-serif"; c.fillText("Ouroveni", ex + 32, ey + 134);
      c.fillStyle = "rgba(255,255,255,.6)"; c.font = "400 12px Inter, sans-serif";
      c.fillText("ARRIVÉE", ex + 32, ey + 166);
      c.fillStyle = "#fff"; c.font = "600 17px Inter, sans-serif"; c.fillText("Hoani (Mohéli)", ex + 32, ey + 188);
      c.fillStyle = "rgba(255,255,255,.6)"; c.font = "400 12px Inter, sans-serif";
      c.fillText("DATE", ex + 32, ey + 220);
      c.fillStyle = "#fff"; c.font = "600 17px Inter, sans-serif"; c.fillText("Demain · 7h30", ex + 32, ey + 242);
      c.fillStyle = C.jaune; rrect.call(c, ex + 16, ey + 276, ew - 32, 46, 14); c.fill();
      c.fillStyle = C.nuit; c.font = "700 16px Poppins, sans-serif"; c.textAlign = "center";
      c.fillText("Rechercher", ex + ew / 2, ey + 305);
    } else if (ecran === "resultats") {
      var lignes = [["Mwezi Express", "7h30", "15 000 FC"], ["Ylang Star", "11h00", "17 500 FC"], ["Shukura", "14h30", "15 000 FC"]];
      lignes.forEach(function (L, i) {
        var yy = ey + 96 + i * 96;
        carte(yy, 80);
        if (i === 0 && (prog || 0) > 0.5) { c.strokeStyle = C.jaune; c.lineWidth = 3; rrect.call(c, ex + 16, yy, ew - 32, 80, 16); c.stroke(); }
        c.textAlign = "left"; c.fillStyle = "#fff"; c.font = "600 16px Inter, sans-serif";
        c.fillText(L[0], ex + 32, yy + 30);
        c.fillStyle = "rgba(255,255,255,.65)"; c.font = "400 13px Inter, sans-serif";
        c.fillText("Ouroveni → Hoani · " + L[1], ex + 32, yy + 56);
        c.textAlign = "right"; c.fillStyle = C.jaune; c.font = "700 15px Poppins, sans-serif";
        c.fillText(L[2], ex + ew - 32, yy + 30);
      });
    } else if (ecran === "paiement") {
      carte(ey + 96, 120);
      c.textAlign = "center"; c.fillStyle = "#fff"; c.font = "600 17px Inter, sans-serif";
      c.fillText("Payer 15 000 FC", ex + ew / 2, ey + 132);
      c.fillStyle = "rgba(255,255,255,.65)"; c.font = "400 13px Inter, sans-serif";
      c.fillText("MVola · KartaPay", ex + ew / 2, ey + 158);
      c.fillStyle = "rgba(255,255,255,.18)"; rrect.call(c, ex + 40, ey + 178, ew - 80, 10, 5); c.fill();
      c.fillStyle = C.jaune; rrect.call(c, ex + 40, ey + 178, (ew - 80) * clamp(prog || 0, 0, 1), 10, 5); c.fill();
      if ((prog || 0) > 0.92) {
        c.fillStyle = "#2ecc71"; c.beginPath(); c.arc(ex + ew / 2, ey + 268, 34, 0, 7); c.fill();
        c.strokeStyle = "#fff"; c.lineWidth = 7; c.lineCap = "round";
        c.beginPath(); c.moveTo(ex + ew / 2 - 15, ey + 268); c.lineTo(ex + ew / 2 - 3, ey + 280);
        c.lineTo(ex + ew / 2 + 17, ey + 254); c.stroke();
        c.fillStyle = "#fff"; c.font = "600 15px Inter, sans-serif";
        c.fillText("Paiement accepté", ex + ew / 2, ey + 330);
      }
    } else if (ecran === "billet") {
      c.fillStyle = "#fff"; rrect.call(c, ex + 22, ey + 86, ew - 44, 330, 18); c.fill();
      c.textAlign = "center"; c.fillStyle = C.nuit; c.font = "700 15px Poppins, sans-serif";
      c.fillText("BILLET ÉLECTRONIQUE", ex + ew / 2, ey + 116);
      c.font = "400 12px Inter, sans-serif"; c.fillStyle = "#5a6b82";
      c.fillText("Ouroveni → Hoani · demain 7h30", ex + ew / 2, ey + 138);
      /* QR déterministe */
      var qx = ex + ew / 2 - 78, qy = ey + 152, cell = 156 / 21, r = rng(99);
      c.fillStyle = "#0a2550";
      for (var i = 0; i < 21; i++) for (var j = 0; j < 21; j++) {
        var coin = (i < 7 && j < 7) || (i > 13 && j < 7) || (i < 7 && j > 13);
        if (coin ? ((i % 6 === 0 || j % 6 === 0) || (i > 1 && i < 5 && j > 1 && j < 5)) : r() > 0.52)
          c.fillRect(qx + i * cell, qy + j * cell, cell + 0.6, cell + 0.6);
      }
      c.fillStyle = C.nuit; c.font = "700 14px Poppins, sans-serif";
      c.fillText("AMINA S. · 1 place", ex + ew / 2, ey + 348);
      c.fillStyle = "#2ecc71"; rrect.call(c, ex + ew / 2 - 52, ey + 362, 104, 26, 13); c.fill();
      c.fillStyle = "#fff"; c.font = "700 12px Inter, sans-serif"; c.fillText("CONFIRMÉ", ex + ew / 2, ey + 380);
    } else { /* accueil */
      carte(ey + 90, 140); carte(ey + 246, 100); carte(ey + 358, 100);
      c.textAlign = "left"; c.fillStyle = "#fff"; c.font = "600 15px Inter, sans-serif";
      c.fillText("Réserver ma traversée", ex + 34, ey + 130);
      c.fillText("Météo de la mer", ex + 34, ey + 292);
      c.fillText("Suivre la vedette", ex + 34, ey + 404);
    }
    c.restore();
    /* encoche + reflet */
    c.fillStyle = "#16202e"; rrect.call(c, -46, -H / 2 + 10, 92, 22, 11); c.fill();
    c.fillStyle = "rgba(255,255,255,.07)";
    c.beginPath(); c.moveTo(-W / 2 + 10, H / 2 - 10); c.lineTo(W / 2 - 10, -H / 2 + 120);
    c.lineTo(W / 2 - 10, -H / 2 + 10); c.lineTo(-W / 2 + 90, -H / 2 + 10); c.closePath(); c.fill();
    c.restore();
  }

  /* ================================================================
     Éléments de quai / bord
     ================================================================ */
  function quai(c, W, H, yTop) {
    c.fillStyle = "#b9a889"; c.fillRect(0, yTop, W, H - yTop);
    c.fillStyle = "#a8977a";
    for (var i = 0; i < 14; i++) c.fillRect(0, yTop + i * 46, W, 4);
    c.fillStyle = "rgba(0,0,0,.10)"; c.fillRect(0, yTop, W, 10);
    /* bittes d'amarrage */
    for (var k = 0; k < 3; k++) {
      var x = W * (0.16 + k * 0.34);
      c.fillStyle = "#5c6470"; rrect.call(c, x - 16, yTop + 26, 32, 54, 8); c.fill();
      c.fillStyle = "#767f8c"; rrect.call(c, x - 22, yTop + 18, 44, 14, 7); c.fill();
    }
  }
  function railBateau(c, W, H, y) {
    c.strokeStyle = "#dfe6ee"; c.lineWidth = 12; c.lineCap = "round";
    c.beginPath(); c.moveTo(-20, y); c.lineTo(W + 20, y); c.stroke();
    c.beginPath(); c.moveTo(-20, y + 90); c.lineTo(W + 20, y + 90); c.stroke();
    for (var i = 0; i <= 5; i++) {
      var x = i * W / 5;
      c.beginPath(); c.moveTo(x, y - 8); c.lineTo(x, y + 190); c.stroke();
    }
  }

  /* ================================================================
     🎥 QUALITÉ D'IMAGE — la couche « cinéma »
     Éclairage des personnages, profondeur de champ, étalonnage,
     halo lumineux, grain. C'est ce qui fait la différence entre un
     dessin à plat et une image de film.
     ================================================================ */
  var _tampons = {};
  function tampon(nom, w, h) {
    var t = _tampons[nom];
    if (!t) { t = _tampons[nom] = { cv: document.createElement("canvas") }; t.cx = t.cv.getContext("2d"); }
    if (t.cv.width !== w || t.cv.height !== h) { t.cv.width = w; t.cv.height = h; }
    t.cx.setTransform(1, 0, 0, 1, 0, 0); t.cx.clearRect(0, 0, w, h);
    return t;
  }

  /* le personnage, dessiné à part puis éclairé : ombre douce du côté
     opposé à la lumière + liseré lumineux sur le côté éclairé */
  function personnageEclaire(c, p, t, lum) {
    lum = lum || {};
    var dirL = lum.dir === undefined ? -1 : lum.dir;      // -1 : lumière venant de la gauche
    var force = lum.force === undefined ? 0.55 : lum.force;
    var h = p.h, bw = Math.ceil(h * 1.9), bh = Math.ceil(h * 1.55);
    var bx = p.x - bw / 2, by = p.y - h * 1.32;
    var T = tampon("perso", bw, bh);
    T.cx.translate(-bx, -by);
    personnage(T.cx, p, t);
    T.cx.setTransform(1, 0, 0, 1, 0, 0);
    T.cx.globalCompositeOperation = "source-atop";
    /* les dégradés doivent couvrir LE CORPS, pas tout le tampon —
       sinon le modelé est invisible (erreur commise au 1er essai). */
    var mil = bw / 2, larg = h * 0.34;
    var xL = mil - larg, xR = mil + larg;
    var gA = dirL < 0 ? xL : xR, gB = dirL < 0 ? xR : xL;
    var g1 = T.cx.createLinearGradient(gA, 0, gB, 0);
    g1.addColorStop(0, "rgba(255,238,205," + (0.30 * force).toFixed(3) + ")");
    g1.addColorStop(0.42, "rgba(0,0,0,0)");
    g1.addColorStop(1, "rgba(10,24,56," + (0.62 * force).toFixed(3) + ")");
    T.cx.fillStyle = g1; T.cx.fillRect(0, 0, bw, bh);
    /* liseré de contre-jour sur le bord éclairé */
    var g2 = T.cx.createLinearGradient(gA, 0, gA + (dirL < 0 ? 1 : -1) * larg * 0.42, 0);
    g2.addColorStop(0, (lum.couleur || "rgba(255,226,168,") + (0.75 * force).toFixed(3) + ")");
    g2.addColorStop(1, "rgba(0,0,0,0)");
    T.cx.fillStyle = g2; T.cx.fillRect(0, 0, bw, bh);
    /* occlusion : les pieds et le bas de la robe s'enfoncent dans l'ombre */
    var g3 = T.cx.createLinearGradient(0, bh - h * 0.34, 0, bh - h * 0.03);
    g3.addColorStop(0, "rgba(0,0,0,0)");
    g3.addColorStop(1, "rgba(8,18,40," + (0.42 * force).toFixed(3) + ")");
    T.cx.fillStyle = g3; T.cx.fillRect(0, 0, bw, bh);
    T.cx.globalCompositeOperation = "source-over";

    /* ombre portée au sol, allongée du côté opposé à la lumière */
    c.save();
    c.fillStyle = "rgba(6,16,36,.24)";
    c.beginPath();
    c.ellipse(p.x - dirL * h * 0.10, p.y + 6, h * 0.24, h * 0.030, 0, 0, 7);
    c.fill(); c.restore();

    c.drawImage(T.cv, bx, by);
  }

  /* décor lointain adouci : la profondeur de champ d'un objectif */
  function profondeur(c, dessin, flou) {
    if (!flou) { dessin(c); return; }
    c.save(); c.filter = "blur(" + flou + "px)"; dessin(c); c.restore();
  }

  /* halo lumineux : les hautes lumières « bavent », comme sur pellicule */
  function halo(c, W, H, force) {
    var pw = Math.max(1, Math.round(W / 5)), ph = Math.max(1, Math.round(H / 5));
    var T = tampon("halo", pw, ph);
    T.cx.filter = "blur(7px) brightness(1.25) saturate(1.1)";
    T.cx.drawImage(c.canvas, 0, 0, pw, ph);
    c.save(); c.globalCompositeOperation = "lighter"; c.globalAlpha = force === undefined ? 0.16 : force;
    c.drawImage(T.cv, 0, 0, W, H); c.restore();
  }

  /* étalonnage : hautes lumières chaudes, ombres bleutées, vignettage */
  function etalonnage(c, W, H, force) {
    force = force === undefined ? 1 : force;
    c.save();
    c.globalCompositeOperation = "soft-light";
    var g = grad(c, 0, 0, 0, H, [[0, "rgba(255,196,120," + (0.42 * force).toFixed(3) + ")"],
      [0.55, "rgba(255,255,255,0)"], [1, "rgba(30,70,150," + (0.40 * force).toFixed(3) + ")"]]);
    c.fillStyle = g; c.fillRect(0, 0, W, H);
    c.globalCompositeOperation = "source-over";
    var v = c.createRadialGradient(W / 2, H * 0.46, H * 0.20, W / 2, H * 0.5, H * 0.78);
    v.addColorStop(0, "rgba(0,0,0,0)");
    v.addColorStop(1, "rgba(4,10,26," + (0.46 * force).toFixed(3) + ")");
    c.fillStyle = v; c.fillRect(0, 0, W, H);
    c.restore();
  }

  /* grain argentique (tuile fabriquée une fois, décalée à chaque image) */
  var _grain = null;
  function grain(c, W, H, image, force) {
    if (!_grain) {
      _grain = document.createElement("canvas"); _grain.width = _grain.height = 256;
      var gc = _grain.getContext("2d"), d = gc.createImageData(256, 256), r = rng(1234);
      for (var i = 0; i < d.data.length; i += 4) {
        var v = 118 + Math.round(r() * 74);
        d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255;
      }
      gc.putImageData(d, 0, 0);
    }
    var dx = (image * 71) % 256, dy = (image * 137) % 256;
    c.save();
    c.globalCompositeOperation = "overlay";
    c.globalAlpha = force === undefined ? 0.055 : force;
    var m = c.createPattern(_grain, "repeat");
    c.translate(-dx, -dy); c.fillStyle = m; c.fillRect(0, 0, W + 256, H + 256);
    c.restore();
  }

  /* rayons de lumière (soleil bas, poussière dans l'air) */
  function rayons(c, W, H, t, sx, sy, force) {
    c.save(); c.globalCompositeOperation = "lighter";
    for (var i = 0; i < 7; i++) {
      var a = -1.15 + i * 0.16 + Math.sin(t * 0.25 + i) * 0.015, L = H * 1.25;
      var larg = W * (0.05 + (i % 3) * 0.02);
      c.save(); c.translate(sx, sy); c.rotate(a);
      var g = c.createLinearGradient(0, 0, 0, L);
      g.addColorStop(0, "rgba(255,226,170," + (0.16 * (force === undefined ? 1 : force)).toFixed(3) + ")");
      g.addColorStop(1, "rgba(255,226,170,0)");
      c.fillStyle = g;
      c.beginPath(); c.moveTo(-larg * 0.15, 0); c.lineTo(larg, L); c.lineTo(-larg * 1.6, L); c.closePath(); c.fill();
      c.restore();
    }
    c.restore();
  }

  /* poussière / embruns qui flottent dans le champ */
  function particules(c, W, H, t, nb, couleur) {
    var r = rng(777);
    c.save();
    for (var i = 0; i < (nb || 30); i++) {
      var bx = r() * W, by = r() * H, vit = 6 + r() * 18, ph = r() * 6.3, taille = 1.5 + r() * 4;
      var x = (bx + Math.sin(t * 0.4 + ph) * 40) % W;
      var y = (by - t * vit) % H; if (y < 0) y += H;
      c.fillStyle = (couleur || "rgba(255,240,205,") + (0.10 + 0.28 * (0.5 + 0.5 * Math.sin(t * 1.7 + ph))).toFixed(3) + ")";
      c.beginPath(); c.arc(x, y, taille, 0, 7); c.fill();
    }
    c.restore();
  }

  /* photo réelle en fond, cadrée « cover », avec flou et assombrissement */
  function photoFond(c, img, W, H, opts) {
    if (!img || !img.complete || !img.naturalWidth) return false;
    opts = opts || {};
    var e = Math.max(W / img.naturalWidth, H / img.naturalHeight) * (opts.zoom || 1.06);
    var w = img.naturalWidth * e, h = img.naturalHeight * e;
    var x = (W - w) / 2 + (opts.dx || 0) * W, y = (H - h) / 2 + (opts.dy || 0) * H;
    c.save();
    if (opts.flou) c.filter = "blur(" + opts.flou + "px) saturate(1.05)";
    c.drawImage(img, x, y, w, h);
    c.restore();
    if (opts.assombri) {
      c.fillStyle = "rgba(6,18,42," + opts.assombri + ")";
      c.fillRect(0, 0, W, H);
    }
    return true;
  }

  /* ================================================================
     🎞️ PHOTO VIVANTE — transformer une VRAIE photo en plan filmé
     La mer est redécoupée en bandes qui ondulent, le ciel dérive,
     la lumière scintille. Rien n'est dessiné : ce sont les vrais
     pixels de la photo qui bougent. C'est ce qui donne l'image
     « comme un film » sans aucun modèle d'IA.
     ================================================================ */
  function photoVivante(c, img, W, H, t, cfg) {
    if (!img || !img.complete || !img.naturalWidth) return false;
    cfg = cfg || {};
    var nw = img.naturalWidth, nh = img.naturalHeight;
    var e = Math.max(W / nw, H / nh) * (cfg.zoom || 1.10);
    var dw = nw * e, dh = nh * e;
    var x0 = (W - dw) / 2 + (cfg.dx || 0) * W, y0 = (H - dh) / 2 + (cfg.dy || 0) * H;
    var hor = cfg.horizon === undefined ? 0.42 : cfg.horizon;   // ligne d'horizon (fraction de la photo)
    var yh = y0 + dh * hor;

    /* 1 · la photo entière : ciel, terre, tout ce qui ne bouge pas */
    c.drawImage(img, x0, y0, dw, dh);

    /* 2 · le ciel dérive doucement (les nuages ne sont jamais figés) */
    if (cfg.ciel !== false && hor > 0.04) {
      var glis = Math.sin(t * 0.055) * (cfg.cielAmpl || 16);
      c.save();
      c.beginPath(); c.rect(0, 0, W, Math.max(0, yh)); c.clip();
      c.drawImage(img, 0, 0, nw, nh * hor, x0 + glis, y0, dw, dh * hor + 1);
      c.restore();
    }

    /* 3 · la mer : bandes horizontales qui ondulent (proche = plus ample) */
    if (cfg.mer !== false && yh < H) {
      var n = cfg.bandes || 100;
      var hautM = Math.max(yh, -dh), basM = y0 + dh;
      var hb = (basM - hautM) / n;
      var ampl = cfg.amplitude === undefined ? 15 : cfg.amplitude;
      var vit = cfg.vitesse === undefined ? 1.15 : cfg.vitesse;
      for (var i = 0; i < n; i++) {
        var k = i / n;
        var a = ampl * Math.pow(k, 1.7) + 0.3;
        var ph = t * vit + k * 8.5;
        var ondX = Math.sin(ph) * a + Math.sin(ph * 0.47 + 1.9) * a * 0.5;
        var ondY = Math.cos(ph * 0.9) * a * 0.20;
        var sy = (hautM - y0 + i * hb) / e;
        var sh = hb / e;
        if (sy < 0 || sy + sh > nh) continue;
        c.drawImage(img, 0, sy, nw, sh + 0.8 / e,
          x0 + ondX, hautM + i * hb + ondY, dw, hb + 1.4);
      }
      /* 4 · scintillement du soleil sur l'eau */
      var r = rng(cfg.graine || 91), nb = cfg.eclats === undefined ? 90 : cfg.eclats;
      c.save(); c.globalCompositeOperation = "lighter";
      c.beginPath(); c.rect(0, Math.max(0, yh), W, H); c.clip();
      for (var j = 0; j < nb; j++) {
        var kk = Math.pow(r(), 0.7);
        var ex2 = r() * W, ey2 = yh + kk * (H - yh), pha = r() * 6.3;
        var al = 0.10 + 0.34 * Math.pow(Math.max(0, Math.sin(t * 3.1 + pha)), 3);
        c.fillStyle = "rgba(255,252,235," + al.toFixed(3) + ")";
        c.beginPath();
        c.ellipse(ex2 + Math.sin(t * 1.2 + pha) * 6, ey2, 5 + kk * 26, 1.2 + kk * 2.6, 0, 0, 7);
        c.fill();
      }
      c.restore();
    }
    return true;
  }

  /* caméra portée à l'épaule : le micro-tremblement qui fait « filmé » */
  function camPortee(t, force) {
    var f = force === undefined ? 1 : force;
    return {
      x: (Math.sin(t * 1.7) * 2.6 + Math.sin(t * 3.9 + 1.2) * 1.5 + Math.sin(t * 0.7) * 3.2) * f,
      y: (Math.cos(t * 1.4) * 2.2 + Math.sin(t * 4.6 + 0.5) * 1.1) * f,
      a: (Math.sin(t * 0.9 + 0.4) * 0.0016 + Math.sin(t * 2.3) * 0.0008) * f
    };
  }

  global.D = {
    photoVivante: photoVivante, camPortee: camPortee,
    personnageEclaire: personnageEclaire, profondeur: profondeur, halo: halo,
    etalonnage: etalonnage, grain: grain, rayons: rayons, particules: particules,
    photoFond: photoFond, tampon: tampon,
    C: C, lerp: lerp, clamp: clamp, ease: ease, rng: rng, rrect: rrect, grad: grad,
    ciel: ciel, nuage: nuage, mer: mer, ile: ile, palmier: palmier, maison: maison,
    vedette: vedette, personnage: personnage, telephone: telephone, quai: quai, railBateau: railBateau
  };
})(window);
