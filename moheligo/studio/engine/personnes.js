/* ================================================================
   🧍🏾 STUDIO MOHELIGO — personnages « réalistes »
   Proportions humaines (7,3 têtes), visage travaillé (iris,
   paupières, lèvres, ombre du nez), volumes en dégradés, plis de
   vêtements, mains. Style illustration réaliste — pas une photo.

   Utilisation : D.personneRealiste(ctx, p, t)   (mêmes champs que
   D.personnage, plus lum:{dir,force})
   ================================================================ */
(function (global) {
  "use strict";
  var D = global.D;
  var clamp = D.clamp, lerp = D.lerp;

  function tint(hex, k) {
    var m = /^#?([\da-f]{2})([\da-f]{2})([\da-f]{2})$/i.exec(hex || "");
    if (!m) return hex;
    var v = [1, 2, 3].map(function (i) { return clamp(Math.round(parseInt(m[i], 16) * k), 0, 255); });
    return "rgb(" + v[0] + "," + v[1] + "," + v[2] + ")";
  }
  /* un membre = des articulations reliées par des troncs coniques.
     Tout est peint d'UNE SEULE couleur : aucune couture visible.
     (le modelé est appliqué à la fin, sur la silhouette entière) */
  function membre(c, pts, couleur) {
    c.fillStyle = couleur;
    for (var i = 0; i < pts.length - 1; i++) {
      var a = pts[i], b = pts[i + 1];
      var ang = Math.atan2(b[1] - a[1], b[0] - a[0]) + Math.PI / 2;
      var dx = Math.cos(ang), dy = Math.sin(ang);
      c.beginPath();
      c.moveTo(a[0] + dx * a[2], a[1] + dy * a[2]);
      c.lineTo(b[0] + dx * b[2], b[1] + dy * b[2]);
      c.lineTo(b[0] - dx * b[2], b[1] - dy * b[2]);
      c.lineTo(a[0] - dx * a[2], a[1] - dy * a[2]);
      c.closePath(); c.fill();
    }
    pts.forEach(function (p) {
      c.beginPath(); c.arc(p[0], p[1], p[2], 0, 7); c.fill();
    });
  }

  /* ---------------------------------------------------------------
     LE VISAGE — c'est lui qui fait le réalisme
     u = hauteur de tête ; (cx, cy) = centre du visage
     --------------------------------------------------------------- */
  function visage(c, cx, cy, u, p, dirL, t) {
    var peau = p.peau || "#8d5524";
    var lw = u * 0.40, lh = u * 0.50;      // demi-largeur / demi-hauteur du crâne
    var regard = (p.dir || 1);

    /* --- crâne + mâchoire (un seul tracé, menton effilé) --- */
    c.beginPath();
    c.moveTo(cx - lw, cy - lh * 0.15);
    c.bezierCurveTo(cx - lw * 1.02, cy - lh * 0.95, cx - lw * 0.55, cy - lh * 1.30, cx, cy - lh * 1.30);
    c.bezierCurveTo(cx + lw * 0.55, cy - lh * 1.30, cx + lw * 1.02, cy - lh * 0.95, cx + lw, cy - lh * 0.15);
    c.bezierCurveTo(cx + lw * 0.98, cy + lh * 0.42, cx + lw * 0.62, cy + lh * 0.92, cx, cy + lh * 1.06);
    c.bezierCurveTo(cx - lw * 0.62, cy + lh * 0.92, cx - lw * 0.98, cy + lh * 0.42, cx - lw, cy - lh * 0.15);
    c.closePath();
    var gp = c.createLinearGradient(cx - lw, cy - lh, cx + lw, cy + lh);
    gp.addColorStop(0, tint(peau, dirL < 0 ? 1.14 : 0.80));
    gp.addColorStop(0.5, peau);
    gp.addColorStop(1, tint(peau, dirL < 0 ? 0.78 : 1.12));
    c.fillStyle = gp; c.fill();

    c.save(); c.clip();
    /* pommettes + creux des joues */
    c.fillStyle = "rgba(120,50,25,.16)";
    c.beginPath(); c.ellipse(cx - lw * 0.62, cy + lh * 0.22, lw * 0.34, lh * 0.30, -0.3, 0, 7); c.fill();
    c.beginPath(); c.ellipse(cx + lw * 0.62, cy + lh * 0.22, lw * 0.34, lh * 0.30, 0.3, 0, 7); c.fill();
    /* front éclairé */
    var gf = c.createRadialGradient(cx - dirL * lw * 0.3, cy - lh * 0.72, u * 0.02, cx, cy - lh * 0.5, u * 0.5);
    gf.addColorStop(0, "rgba(255,232,200,.22)"); gf.addColorStop(1, "rgba(255,232,200,0)");
    c.fillStyle = gf; c.fillRect(cx - lw * 1.2, cy - lh * 1.4, lw * 2.4, lh * 1.4);
    /* ombre du côté opposé à la lumière */
    var go = c.createLinearGradient(cx + dirL * lw * 0.1, 0, cx - dirL * lw, 0);
    go.addColorStop(0, "rgba(40,18,6,0)"); go.addColorStop(1, "rgba(40,18,6,.30)");
    c.fillStyle = go; c.fillRect(cx - lw * 1.2, cy - lh * 1.4, lw * 2.4, lh * 2.6);
    c.restore();

    /* --- oreilles --- */
    [-1, 1].forEach(function (s) {
      c.fillStyle = tint(peau, s === dirL ? 1.04 : 0.88);
      c.beginPath(); c.ellipse(cx + s * lw * 0.98, cy + lh * 0.05, lw * 0.14, lh * 0.24, s * 0.12, 0, 7); c.fill();
      c.strokeStyle = "rgba(60,25,8,.35)"; c.lineWidth = u * 0.012;
      c.beginPath(); c.arc(cx + s * lw * 0.98, cy + lh * 0.05, lh * 0.11, 0, 7); c.stroke();
    });

    /* --- yeux --- */
    var ey = cy - lh * 0.02, ex = lw * 0.40, eL = lw * 0.30, eH = lh * 0.135;
    var ouvert = 1 - (p.clign || 0);
    [-1, 1].forEach(function (s) {
      var X = cx + s * ex;
      /* creux orbitaire */
      c.fillStyle = "rgba(60,28,10,.18)";
      c.beginPath(); c.ellipse(X, ey - eH * 0.4, eL * 1.25, eH * 1.9, 0, 0, 7); c.fill();
      /* amande de l'œil */
      c.save();
      c.beginPath();
      c.moveTo(X - eL, ey);
      c.quadraticCurveTo(X - eL * 0.3, ey - eH * 1.5 * ouvert, X + eL * 0.85, ey - eH * 0.35 * ouvert);
      c.quadraticCurveTo(X + eL * 0.2, ey + eH * 1.25 * ouvert, X - eL, ey);
      c.closePath();
      c.fillStyle = "#f3ece2"; c.fill();
      c.clip();
      /* iris + pupille + reflet */
      var ix = X + regard * eL * 0.18;
      c.fillStyle = "#4a2a12";
      c.beginPath(); c.arc(ix, ey - eH * 0.1, eH * 1.02, 0, 7); c.fill();
      c.fillStyle = "#6b4020";
      c.beginPath(); c.arc(ix, ey - eH * 0.05, eH * 0.78, 0, 7); c.fill();
      c.fillStyle = "#150c05";
      c.beginPath(); c.arc(ix, ey - eH * 0.08, eH * 0.42, 0, 7); c.fill();
      c.fillStyle = "rgba(255,255,255,.92)";
      c.beginPath(); c.arc(ix - eH * 0.32, ey - eH * 0.48, eH * 0.24, 0, 7); c.fill();
      /* ombre de la paupière supérieure */
      c.fillStyle = "rgba(40,18,6,.28)";
      c.fillRect(X - eL, ey - eH * 2, eL * 2, eH * 0.75);
      c.restore();
      /* trait de la paupière + cils */
      c.strokeStyle = "rgba(24,12,4,.85)"; c.lineWidth = u * 0.020; c.lineCap = "round";
      c.beginPath();
      c.moveTo(X - eL, ey);
      c.quadraticCurveTo(X - eL * 0.3, ey - eH * 1.5 * ouvert, X + eL * 0.85, ey - eH * 0.35 * ouvert);
      c.stroke();
      c.strokeStyle = "rgba(24,12,4,.35)"; c.lineWidth = u * 0.012;
      c.beginPath();
      c.moveTo(X - eL * 0.9, ey + eH * 0.15);
      c.quadraticCurveTo(X + eL * 0.2, ey + eH * 1.1 * ouvert, X + eL * 0.82, ey - eH * 0.3);
      c.stroke();
      /* sourcil */
      c.strokeStyle = "#241608"; c.lineWidth = u * 0.045; c.lineCap = "round";
      c.beginPath();
      c.moveTo(X - eL * 1.15, ey - eH * 2.0 - (p.sourcils || 0) * eH * 0.7);
      c.quadraticCurveTo(X - eL * 0.1, ey - eH * 3.0 - (p.sourcils || 0) * eH * 1.1, X + eL * 1.05, ey - eH * 1.9);
      c.stroke();
    });

    /* --- nez : deux ombres et un reflet, pas de trait --- */
    var ny = cy + lh * 0.36;
    c.fillStyle = "rgba(60,26,8,.22)";
    c.beginPath();
    c.moveTo(cx - dirL * lw * 0.055, cy - lh * 0.02);
    c.quadraticCurveTo(cx - dirL * lw * 0.20, ny - lh * 0.02, cx - dirL * lw * 0.15, ny + lh * 0.06);
    c.quadraticCurveTo(cx - dirL * lw * 0.02, ny + lh * 0.12, cx + dirL * lw * 0.02, ny);
    c.closePath(); c.fill();
    c.fillStyle = "rgba(255,235,205,.20)";
    c.beginPath(); c.ellipse(cx + dirL * lw * 0.04, ny - lh * 0.12, lw * 0.07, lh * 0.20, 0, 0, 7); c.fill();
    c.fillStyle = "rgba(45,18,6,.45)";
    [-1, 1].forEach(function (s) {
      c.beginPath(); c.ellipse(cx + s * lw * 0.155, ny + lh * 0.10, lw * 0.05, lh * 0.035, s * 0.4, 0, 7); c.fill();
    });
    c.fillStyle = "rgba(60,26,8,.16)";
    c.beginPath(); c.ellipse(cx, ny + lh * 0.16, lw * 0.24, lh * 0.06, 0, 0, 7); c.fill();

    /* --- bouche : lèvres dessinées, s'ouvrent avec la voix --- */
    var my = cy + lh * 0.66, b = clamp(p.bouche || 0, 0, 1), lgL = lw * 0.38;
    var sour = (p.sourire === undefined ? 0.4 : p.sourire);
    if (b > 0.06) {
      /* bouche ouverte : cavité, dents, lèvres autour */
      var oh = lh * (0.06 + b * 0.30), ow = lgL * (1 + b * 0.12);
      c.fillStyle = "#3d1216";
      c.beginPath(); c.ellipse(cx, my + oh * 0.15, ow, oh, 0, 0, 7); c.fill();
      c.fillStyle = "#f6f1e8";
      c.beginPath(); c.ellipse(cx, my - oh * 0.55, ow * 0.82, oh * 0.34, 0, 0, 7); c.fill();
      c.fillStyle = "#8e2f38";
      c.beginPath(); c.ellipse(cx, my + oh * 0.72, ow * 0.55, oh * 0.30, 0, 0, 7); c.fill();
      c.strokeStyle = "rgba(120,45,45,.75)"; c.lineWidth = u * 0.022;
      c.beginPath(); c.ellipse(cx, my + oh * 0.15, ow, oh, 0, 0, 7); c.stroke();
    } else {
      /* lèvres fermées : arc de Cupidon + lèvre inférieure pleine */
      c.fillStyle = tint(peau, 0.62);
      c.beginPath();
      c.moveTo(cx - lgL, my);
      c.quadraticCurveTo(cx - lgL * 0.5, my - lh * 0.10, cx - lgL * 0.14, my - lh * 0.045);
      c.quadraticCurveTo(cx, my - lh * 0.10, cx + lgL * 0.14, my - lh * 0.045);
      c.quadraticCurveTo(cx + lgL * 0.5, my - lh * 0.10, cx + lgL, my);
      c.quadraticCurveTo(cx + lgL * 0.45, my + lh * (0.13 + sour * 0.03), cx, my + lh * (0.15 + sour * 0.04));
      c.quadraticCurveTo(cx - lgL * 0.45, my + lh * (0.13 + sour * 0.03), cx - lgL, my);
      c.closePath(); c.fill();
      c.strokeStyle = "rgba(70,25,20,.55)"; c.lineWidth = u * 0.018; c.lineCap = "round";
      c.beginPath();
      c.moveTo(cx - lgL, my);
      c.quadraticCurveTo(cx, my + lh * sour * 0.10, cx + lgL, my);
      c.stroke();
      c.fillStyle = "rgba(255,225,205,.28)";
      c.beginPath(); c.ellipse(cx, my + lh * 0.075, lgL * 0.4, lh * 0.035, 0, 0, 7); c.fill();
    }
    /* sillon menton + ombre sous la lèvre */
    c.fillStyle = "rgba(60,26,8,.14)";
    c.beginPath(); c.ellipse(cx, my + lh * 0.26, lgL * 0.7, lh * 0.08, 0, 0, 7); c.fill();
  }

  /* ---------------------------------------------------------------
     CHEVELURE / COIFFE
     --------------------------------------------------------------- */
  function coiffe(c, cx, cy, u, p, dirL, phase) {
    var lw = u * 0.40, lh = u * 0.50, type = p.coiffe || "cheveux";
    /* le voile et la masse de cheveux passent DERRIÈRE le visage,
       la casquette du kofia par-dessus. Sinon on efface la figure. */
    if (phase === "arriere" && type === "kofia") return;
    if (phase === "avant" && type === "kofia") { /* la calotte se pose sur le crâne */ }
    else if (phase === "avant") {
      /* le bord du voile / la frange repasse DEVANT le visage :
         sans ça, le personnage a l'air chauve. */
      if (type === "shiromani" || type === "foulard") {
        var vb = p.coifCouleur || "#e94f6a";
        var gv2 = c.createLinearGradient(cx - lw * 1.4, cy - lh, cx + lw * 1.4, cy + lh);
        gv2.addColorStop(0, tint(vb, dirL < 0 ? 1.16 : 0.84));
        gv2.addColorStop(1, tint(vb, 0.78));
        c.fillStyle = gv2;
        c.beginPath();
        c.moveTo(cx - lw * 1.16, cy + lh * 0.55);
        c.bezierCurveTo(cx - lw * 1.34, cy - lh * 1.30, cx - lw * 0.60, cy - lh * 1.72, cx, cy - lh * 1.70);
        c.bezierCurveTo(cx + lw * 0.60, cy - lh * 1.72, cx + lw * 1.34, cy - lh * 1.30, cx + lw * 1.16, cy + lh * 0.55);
        c.bezierCurveTo(cx + lw * 1.24, cy + lh * 1.30, cx + lw * 1.0, cy + lh * 1.55, cx + lw * 0.9, cy + lh * 1.6);
        c.lineTo(cx - lw * 0.9, cy + lh * 1.6);
        c.bezierCurveTo(cx - lw * 1.0, cy + lh * 1.55, cx - lw * 1.24, cy + lh * 1.30, cx - lw * 1.16, cy + lh * 0.55);
        c.closePath();
        /* le trou : l'ouverture du visage */
        c.ellipse(cx, cy + lh * 0.12, lw * 0.88, lh * 1.06, 0, 0, Math.PI * 2, true);
        c.fill("evenodd");
        /* ombre portée du voile sur le front */
        c.save();
        c.beginPath(); c.ellipse(cx, cy + lh * 0.12, lw * 0.88, lh * 1.06, 0, 0, 7); c.clip();
        c.fillStyle = "rgba(40,16,6,.28)";
        c.beginPath(); c.ellipse(cx, cy - lh * 0.86, lw * 0.9, lh * 0.30, 0, 0, 7); c.fill();
        c.restore();
      } else {
        /* frange de cheveux */
        c.fillStyle = p.coifCouleur || "#1a1310";
        c.beginPath();
        c.moveTo(cx - lw * 1.04, cy - lh * 0.32);
        c.bezierCurveTo(cx - lw * 1.1, cy - lh * 1.3, cx + lw * 1.1, cy - lh * 1.3, cx + lw * 1.04, cy - lh * 0.32);
        c.bezierCurveTo(cx + lw * 0.6, cy - lh * 0.78, cx - lw * 0.2, cy - lh * 0.5, cx - lw * 1.04, cy - lh * 0.32);
        c.closePath(); c.fill();
      }
      return;
    }
    if (type === "shiromani" || type === "foulard") {
      var base = p.coifCouleur || "#e94f6a";
      var g = c.createLinearGradient(cx - lw * 1.5, cy - lh, cx + lw * 1.5, cy + lh * 1.6);
      g.addColorStop(0, tint(base, dirL < 0 ? 1.16 : 0.82));
      g.addColorStop(0.55, base);
      g.addColorStop(1, tint(base, 0.72));
      c.fillStyle = g;
      c.beginPath();
      c.moveTo(cx - lw * 1.16, cy + lh * 0.55);
      c.bezierCurveTo(cx - lw * 1.34, cy - lh * 1.30, cx - lw * 0.60, cy - lh * 1.72, cx, cy - lh * 1.70);
      c.bezierCurveTo(cx + lw * 0.60, cy - lh * 1.72, cx + lw * 1.34, cy - lh * 1.30, cx + lw * 1.16, cy + lh * 0.55);
      c.bezierCurveTo(cx + lw * 1.30, cy + lh * 1.75, cx + lw * 0.75, cy + lh * 2.05, cx + lw * 0.45, cy + lh * 2.05);
      c.lineTo(cx - lw * 0.45, cy + lh * 2.05);
      c.bezierCurveTo(cx - lw * 0.75, cy + lh * 2.05, cx - lw * 1.30, cy + lh * 1.75, cx - lw * 1.16, cy + lh * 0.55);
      c.closePath(); c.fill();
      /* plis du tissu */
      c.strokeStyle = "rgba(255,255,255,.22)"; c.lineWidth = u * 0.03; c.lineCap = "round";
      [0.25, 0.55, 0.85].forEach(function (k) {
        c.beginPath();
        c.moveTo(cx - lw * (1.02 + k * 0.12), cy + lh * (0.3 + k));
        c.quadraticCurveTo(cx - lw * (0.7 + k * 0.2), cy + lh * (1.5 + k * 0.3), cx - lw * (0.2 + k * 0.3), cy + lh * 1.95);
        c.stroke();
      });
      c.fillStyle = "rgba(30,10,20,.22)";
      c.beginPath();
      c.ellipse(cx, cy - lh * 0.95, lw * 0.95, lh * 0.28, 0, 0, Math.PI); c.fill();
    } else if (type === "kofia") {
      c.fillStyle = "#1c130c";
      c.beginPath(); c.ellipse(cx, cy - lh * 0.42, lw * 1.02, lh * 0.86, 0, Math.PI, 0); c.fill();
      var gk = c.createLinearGradient(cx - lw, cy - lh * 1.5, cx + lw, cy - lh * 0.6);
      gk.addColorStop(0, "#ffffff"); gk.addColorStop(1, "#ddd6c2");
      c.fillStyle = gk;
      c.beginPath();
      c.moveTo(cx - lw * 0.92, cy - lh * 0.78);
      c.lineTo(cx + lw * 0.92, cy - lh * 0.78);
      c.quadraticCurveTo(cx + lw * 0.88, cy - lh * 1.62, cx, cy - lh * 1.62);
      c.quadraticCurveTo(cx - lw * 0.88, cy - lh * 1.62, cx - lw * 0.92, cy - lh * 0.78);
      c.closePath(); c.fill();
      c.fillStyle = "rgba(150,130,80,.55)";
      for (var q = 0; q < 6; q++) {
        c.beginPath(); c.arc(cx - lw * 0.66 + q * lw * 0.26, cy - lh * 1.08, u * 0.018, 0, 7); c.fill();
      }
      c.fillStyle = "rgba(0,0,0,.20)";
      c.fillRect(cx - lw * 0.92, cy - lh * 0.84, lw * 1.84, lh * 0.09);
    } else {
      var ch = p.coifCouleur || "#1a1310";
      c.fillStyle = ch;
      c.beginPath();
      c.moveTo(cx - lw * 1.06, cy + lh * 0.30);
      c.bezierCurveTo(cx - lw * 1.16, cy - lh * 1.42, cx + lw * 1.16, cy - lh * 1.42, cx + lw * 1.06, cy + lh * 0.30);
      c.bezierCurveTo(cx + lw * 0.9, cy - lh * 0.55, cx - lw * 0.9, cy - lh * 0.55, cx - lw * 1.06, cy + lh * 0.30);
      c.closePath(); c.fill();
      c.fillStyle = "rgba(255,255,255,.14)";
      c.beginPath(); c.ellipse(cx - dirL * lw * 0.4, cy - lh * 0.95, lw * 0.34, lh * 0.20, -0.4, 0, 7); c.fill();
    }
  }

  /* ---------------------------------------------------------------
     LE PERSONNAGE ENTIER
     --------------------------------------------------------------- */
  function personneRealiste(cFinal, p, t, lum) {
    lum = lum || {};
    var dirL = lum.dir === undefined ? -1 : lum.dir;
    var force = lum.force === undefined ? 0.6 : lum.force;
    /* on dessine dans un tampon : l'éclairage est appliqué ensuite sur
       toute la silhouette d'un coup (pas de couture entre les membres) */
    var bw = Math.ceil(p.h * 1.9), bh = Math.ceil(p.h * 1.45);
    var bx = p.x - bw / 2, by = p.y - p.h * 1.22;
    var T = D.tampon("perso-r", bw, bh);
    var c = T.cx;
    c.translate(-bx, -by);

    var h = p.h, x = p.x, sol = p.y, dir = p.dir || 1;
    var peau = p.peau || "#8d5524", tissu = p.tenue || "#e94f6a";
    var robe = p.robe !== false;
    var u = h / 7.3;                                   /* hauteur d'une tête */
    var marche = p.pose === "marche", assis = p.pose === "assis";
    var pas = marche ? Math.sin(t * 5.4) : 0;
    var resp = Math.sin(t * 1.5 + (p.graine || 0)) * h * 0.003;
    var bob = (marche ? Math.abs(Math.sin(t * 5.4)) * h * 0.010 : 0) + resp;

    var yTete = sol - h + bob;                         /* sommet du crâne */
    var cy = yTete + u * 0.52, cx = x;                 /* centre du visage */
    var yCou = yTete + u * 1.02;
    var yEp = yTete + u * 1.30;                        /* épaules */
    var yTaille = yTete + u * 3.15;
    var yHanche = yTete + u * (assis ? 3.55 : 3.95);
    var yGenou = yTete + u * 5.55;
    var yPied = assis ? yHanche + u * 1.5 : sol + bob;
    var demiEp = u * (robe ? 0.78 : 0.92);
    var demiHanche = u * (robe ? 0.80 : 0.70);

    var peauO = tint(peau, 0.78), peauC = tint(peau, 1.10);
    var tisO = tint(tissu, 0.70), tisC = tint(tissu, 1.12);

    /* ---- ombre au sol ---- */
    c.save();
    c.fillStyle = "rgba(8,18,38,.26)";
    c.beginPath(); c.ellipse(x - dirL * u * 0.5, sol + u * 0.06, u * 1.35, u * 0.20, 0, 0, 7); c.fill();
    c.restore();

    /* ---- jambes ---- */
    var pantalon = robe ? tint(peau, 0.94) : "#33405a";
    if (!assis) {
      [[-1, pas], [1, -pas]].forEach(function (j) {
        var s = j[0], sw = j[1];
        var hx = x + s * demiHanche * 0.52, gx = hx + sw * u * 0.38, px = hx + sw * u * 0.66;
        membre(c, [[hx, yHanche, u * 0.30], [gx, yGenou, u * 0.20], [px, yPied - u * 0.12, u * 0.13]], pantalon);
        c.fillStyle = "#241a12";
        c.beginPath(); c.ellipse(px + dir * u * 0.10, yPied - u * 0.06, u * 0.28, u * 0.11, 0, 0, 7); c.fill();
      });
    } else {
      membre(c, [[x, yHanche, u * 0.30], [x + dir * u * 1.15, yHanche + u * 0.18, u * 0.24],
        [x + dir * u * 1.30, yPied, u * 0.14]], pantalon);
      c.fillStyle = "#241a12";
      c.beginPath(); c.ellipse(x + dir * u * 1.42, yPied, u * 0.28, u * 0.11, 0, 0, 7); c.fill();
    }

    /* ---- buste : épaules arrondies, taille marquée, jupe évasée ---- */
    var basRobe = yTete + u * 5.9;
    c.fillStyle = tissu;
    /* les deltoïdes, pour que les épaules ne fassent pas « planche » */
    [-1, 1].forEach(function (s) {
      c.beginPath(); c.arc(x + s * demiEp * 0.86, yEp + u * 0.30, u * 0.22, 0, 7); c.fill();
    });
    c.beginPath();
    c.moveTo(x - demiEp, yEp + u * 0.16);
    c.bezierCurveTo(x - demiEp * 1.02, yEp + u * 1.1, x - u * 0.70, yTaille - u * 0.4, x - u * 0.66, yTaille);
    if (robe) {
      c.bezierCurveTo(x - u * 0.78, yHanche + u * 0.5, x - u * 1.16, basRobe - u * 0.8, x - u * 1.34, basRobe);
      c.quadraticCurveTo(x, basRobe + u * 0.30, x + u * 1.34, basRobe);
      c.bezierCurveTo(x + u * 1.16, basRobe - u * 0.8, x + u * 0.78, yHanche + u * 0.5, x + u * 0.66, yTaille);
    } else {
      c.bezierCurveTo(x - u * 0.72, yHanche - u * 0.2, x - demiHanche, yHanche, x - demiHanche, yHanche + u * 0.18);
      c.lineTo(x + demiHanche, yHanche + u * 0.18);
      c.bezierCurveTo(x + demiHanche, yHanche, x + u * 0.72, yHanche - u * 0.2, x + u * 0.66, yTaille);
    }
    c.bezierCurveTo(x + u * 0.70, yTaille - u * 0.4, x + demiEp * 1.02, yEp + u * 1.1, x + demiEp, yEp + u * 0.16);
    c.quadraticCurveTo(x, yEp - u * 0.30, x - demiEp, yEp + u * 0.16);
    c.closePath(); c.fill();

    /* motif du tissu */
    if (p.motif) {
      c.save(); c.clip();
      c.fillStyle = p.motif; c.globalAlpha = 0.85;
      for (var i = 0; i < 16; i++) {
        var mx = x - u * 1.2 + (i % 4) * u * 0.8, my2 = yEp + u * 0.5 + Math.floor(i / 4) * u * 1.1;
        c.beginPath(); c.ellipse(mx, my2, u * 0.11, u * 0.17, 0.4, 0, 7); c.fill();
      }
      c.restore();
    }
    /* plis du vêtement */
    c.save();
    c.beginPath();
    c.moveTo(x - demiEp, yEp); c.lineTo(x + demiEp, yEp);
    c.lineTo(x + u * 1.4, yTete + u * 5.9); c.lineTo(x - u * 1.4, yTete + u * 5.9); c.closePath();
    c.clip();
    c.strokeStyle = "rgba(0,0,0,.13)"; c.lineWidth = u * 0.05; c.lineCap = "round";
    [-0.55, 0, 0.55].forEach(function (k, idx) {
      c.beginPath();
      c.moveTo(x + k * u * 0.9, yTaille - u * 0.3);
      c.quadraticCurveTo(x + k * u * 1.2 + u * 0.1, yTaille + u * 1.1, x + k * u * 1.5, yTete + u * 5.5);
      c.stroke();
    });
    /* ombre sous la poitrine / du col */
    c.fillStyle = "rgba(0,0,0,.16)";
    c.beginPath(); c.ellipse(x, yEp + u * 0.16, demiEp * 0.86, u * 0.22, 0, 0, Math.PI); c.fill();
    c.restore();

    /* ---- bras : manche courte puis peau, main en bout ---- */
    function bras(s, coudeX, coudeY, mainX, mainY) {
      var epX = x + s * demiEp * 0.94, epY = yEp + u * 0.22;
      var mx = lerp(epX, coudeX, 0.42), my = lerp(epY, coudeY, 0.42);
      membre(c, [[mx, my, u * 0.23], [coudeX, coudeY, u * 0.17], [mainX, mainY, u * 0.13]], peau);
      membre(c, [[epX, epY, u * 0.26], [mx, my, u * 0.21]], tissu);
      c.fillStyle = peau;
      c.beginPath();
      c.ellipse(mainX + (mainX - coudeX) * 0.12, mainY + (mainY - coudeY) * 0.12, u * 0.15, u * 0.19,
        Math.atan2(mainY - coudeY, mainX - coudeX) - Math.PI / 2, 0, 7);
      c.fill();
    }
    var poseB = p.bras || "repos";
    if (poseB === "telephone") {
      bras(-dir, x - dir * demiEp * 1.15, yEp + u * 1.25, x - dir * demiEp * 1.05, yEp + u * 2.35, 1);
      bras(dir, x + dir * demiEp * 1.20, yEp + u * 1.20, x + dir * u * 0.34, yEp + u * 1.55, 1);
      /* téléphone tenu en main */
      c.save(); c.translate(x + dir * u * 0.36, yEp + u * 1.62); c.rotate(-dir * 0.22);
      c.fillStyle = "#10161f"; D.rrect.call(c, -u * 0.22, -u * 0.40, u * 0.44, u * 0.80, u * 0.07); c.fill();
      c.fillStyle = "#173a72"; D.rrect.call(c, -u * 0.18, -u * 0.35, u * 0.36, u * 0.70, u * 0.05); c.fill();
      c.fillStyle = "#F6BC1C"; c.fillRect(-u * 0.12, -u * 0.24, u * 0.24, u * 0.045);
      c.fillStyle = "rgba(255,255,255,.45)"; c.fillRect(-u * 0.12, -u * 0.12, u * 0.17, u * 0.035);
      c.restore();
    } else if (poseB === "salut") {
      var ag = Math.sin(t * 4.6) * 0.22;
      bras(-dir, x - dir * demiEp * 1.15, yEp + u * 1.25, x - dir * demiEp * 1.05, yEp + u * 2.35, 1);
      bras(dir, x + dir * demiEp * 1.35, yEp + u * 0.35, x + dir * (demiEp * 1.5 + ag * u * 0.6), yEp - u * 0.85, 1);
    } else if (poseB === "ouverts") {
      bras(-1, x - demiEp * 1.5, yEp + u * 0.85, x - demiEp * 2.3, yEp + u * 0.55, 1);
      bras(1, x + demiEp * 1.5, yEp + u * 0.85, x + demiEp * 2.3, yEp + u * 0.55, 1);
    } else if (poseB === "valise") {
      bras(-dir, x - dir * demiEp * 1.18, yEp + u * 1.25, x - dir * demiEp * 1.12, yEp + u * 2.45, 1);
      bras(dir, x + dir * demiEp * 1.18, yEp + u * 1.25, x + dir * demiEp * 1.12, yEp + u * 2.45, 1);
      var vx = x - dir * demiEp * 1.12, vy = yEp + u * 2.62;
      c.strokeStyle = "#5b4632"; c.lineWidth = u * 0.07;
      c.beginPath(); c.arc(vx, vy + u * 0.30, u * 0.24, Math.PI, 0); c.stroke();
      var gv = c.createLinearGradient(vx - u * 0.5, vy, vx + u * 0.5, vy + u * 0.9);
      gv.addColorStop(0, "#d1793a"); gv.addColorStop(1, "#9c5222");
      c.fillStyle = gv; D.rrect.call(c, vx - u * 0.46, vy + u * 0.28, u * 0.92, u * 0.78, u * 0.10); c.fill();
      c.fillStyle = "rgba(0,0,0,.18)"; c.fillRect(vx - u * 0.46, vy + u * 0.58, u * 0.92, u * 0.10);
    } else {
      bras(-1, x - demiEp * 1.16, yEp + u * 1.25, x - demiEp * 1.06, yEp + u * 2.42, 1);
      bras(1, x + demiEp * 1.16, yEp + u * 1.25, x + demiEp * 1.06, yEp + u * 2.42, 1);
    }

    /* ---- cou ---- */
    membre(c, [[x, yCou - u * 0.25, u * 0.23], [x, yEp + u * 0.10, u * 0.28]], tint(peau, 0.90));
    c.fillStyle = "rgba(50,20,6,.20)";
    c.beginPath(); c.ellipse(x, yCou + u * 0.02, u * 0.26, u * 0.11, 0, 0, 7); c.fill();

    /* ---- tête : voile/cheveux DERRIÈRE, visage, puis kofia DEVANT ---- */
    coiffe(c, cx, cy, u, p, dirL, "arriere");
    visage(c, cx, cy, u, p, dirL, t);
    coiffe(c, cx, cy, u, p, dirL, "avant");

    /* ---- éclairage de toute la silhouette, d'un seul coup ---- */
    c.setTransform(1, 0, 0, 1, 0, 0);
    c.globalCompositeOperation = "source-atop";
    var mil = bw / 2, larg = h * 0.30;
    var gA = dirL < 0 ? mil - larg : mil + larg, gB = dirL < 0 ? mil + larg : mil - larg;
    var gl = c.createLinearGradient(gA, 0, gB, 0);
    gl.addColorStop(0, "rgba(255,238,206," + (0.26 * force).toFixed(3) + ")");
    gl.addColorStop(0.45, "rgba(0,0,0,0)");
    gl.addColorStop(1, "rgba(10,24,56," + (0.50 * force).toFixed(3) + ")");
    c.fillStyle = gl; c.fillRect(0, 0, bw, bh);
    var gr = c.createLinearGradient(gA, 0, gA + (dirL < 0 ? 1 : -1) * larg * 0.30, 0);
    gr.addColorStop(0, "rgba(255,228,175," + (0.55 * force).toFixed(3) + ")");
    gr.addColorStop(1, "rgba(0,0,0,0)");
    c.fillStyle = gr; c.fillRect(0, 0, bw, bh);
    var go2 = c.createLinearGradient(0, bh - h * 0.30, 0, bh - h * 0.05);
    go2.addColorStop(0, "rgba(0,0,0,0)");
    go2.addColorStop(1, "rgba(8,18,40," + (0.34 * force).toFixed(3) + ")");
    c.fillStyle = go2; c.fillRect(0, 0, bw, bh);
    c.globalCompositeOperation = "source-over";

    cFinal.drawImage(T.cv, bx, by);
  }

  D.personneRealiste = personneRealiste;
})(window);
