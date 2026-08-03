/* ================================================================
   🎬 STUDIO MOHELIGO — moteur de scènes
   Reçoit un épisode (JSON) + une enveloppe de voix (une valeur par
   image) et sait dessiner N'IMPORTE QUELLE image de la vidéo à
   partir du seul temps t. Déterministe : rejouer = même résultat.
   ================================================================ */
(function (global) {
  "use strict";
  var D = global.D, C = D.C;

  var EP = null, ENV = null, W = 1080, H = 1920;
  var cvBase = null, cxBase = null;   // calque de travail (pour les fondus)

  function init(episode, enveloppe) {
    EP = episode; ENV = enveloppe || [];
    W = EP.largeur || 1080; H = EP.hauteur || 1920;
    cvBase = document.createElement("canvas"); cvBase.width = W; cvBase.height = H;
    cxBase = cvBase.getContext("2d");
    /* horaires des plans */
    var t = 0;
    EP.plans.forEach(function (p) { p._debut = t; t += p._duree; });
    EP._duree = t;
  }

  /* ---------------- DÉCORS ---------------- */
  var DECORS = {
    /* le village au petit matin */
    village_matin: function (c, t) {
      D.ciel(c, W, H, t, "aube");
      var yh = H * 0.52;
      D.ile(c, W * 0.22, yh, W * 1.1, H * 0.20, "#2b6a53");
      D.ile(c, W * 0.86, yh, W * 0.9, H * 0.15, "#255f4a");
      c.fillStyle = "#3d8a5f"; c.fillRect(0, yh - 2, W, H - yh);
      c.fillStyle = "#4d9b6c";
      c.beginPath(); c.moveTo(0, yh + H * 0.06);
      c.quadraticCurveTo(W * 0.5, yh + H * 0.02, W, yh + H * 0.07); c.lineTo(W, H); c.lineTo(0, H); c.fill();
      D.maison(c, W * 0.17, yh + H * 0.10, W * 0.30, H * 0.10);
      D.maison(c, W * 0.78, yh + H * 0.12, W * 0.34, H * 0.11, "#e8d6bd");
      D.palmier(c, W * 0.06, yh + H * 0.14, 0.9, t, 5);
      D.palmier(c, W * 0.95, yh + H * 0.17, 1.05, t, 11);
      /* chemin de terre */
      c.fillStyle = "#cbae7f";
      c.beginPath(); c.moveTo(W * 0.30, H); c.lineTo(W * 0.44, yh + H * 0.13);
      c.lineTo(W * 0.60, yh + H * 0.13); c.lineTo(W * 0.82, H); c.closePath(); c.fill();
    },
    /* le quai d'Ouroveni, la vedette à l'amarrage */
    port_ouroveni: function (c, t) {
      D.ciel(c, W, H, t, "aube");
      var ym = H * 0.46;
      D.ile(c, W * 0.75, ym, W * 0.8, H * 0.10, "#2f6d57", true);
      D.mer(c, W, H, t, ym, 0);
      D.vedette(c, W * 0.62, ym + H * 0.12, 1.25, t, false);
      D.quai(c, W, H, H * 0.70);
      D.palmier(c, W * 0.08, H * 0.74, 1.1, t, 3);
    },
    /* pleine mer, la vedette file vers Mohéli */
    mer_large: function (c, t) {
      D.ciel(c, W, H, t, "jour");
      var ym = H * 0.44;
      D.ile(c, W * 0.80, ym, W * 0.85, H * 0.12, "#2f6d57", true);
      D.mer(c, W, H, t, ym, 1);
      D.vedette(c, W * (0.46 + 0.14 * Math.sin(t * 0.10 - 1.2)), ym + H * 0.20, 1.7, t, true);
    },
    /* à bord : le bastingage, la mer défile */
    a_bord: function (c, t) {
      D.ciel(c, W, H, t, "jour");
      var ym = H * 0.34;
      D.ile(c, W * (0.62 + 0.3 * Math.cos(t * 0.06)), ym, W * 0.7, H * 0.09, "#357a60", true);
      D.mer(c, W, H, t, ym, 1);
      /* pont du bateau */
      c.fillStyle = "#e9eef4"; c.fillRect(0, H * 0.70, W, H * 0.30);
      c.fillStyle = "#d3dbe4";
      for (var i = 0; i < 8; i++) c.fillRect(0, H * 0.70 + i * 46, W, 6);
      D.railBateau(c, W, H, H * 0.52);
      c.fillStyle = C.jaune; c.fillRect(0, H * 0.695, W, 10);
    },
    /* l'arrivée à Hoani */
    hoani: function (c, t) {
      D.ciel(c, W, H, t, "or");
      var ym = H * 0.44;
      D.ile(c, W * 0.3, ym, W * 1.2, H * 0.24, "#2e7a58");
      D.ile(c, W * 0.9, ym, W * 0.8, H * 0.17, "#276a4c");
      D.mer(c, W, H, t, ym, 0);
      D.vedette(c, W * 0.80, ym + H * 0.10, 0.85, t, false);
      c.fillStyle = C.sable;
      c.beginPath(); c.moveTo(0, H * 0.66); c.quadraticCurveTo(W * 0.5, H * 0.62, W, H * 0.68);
      c.lineTo(W, H); c.lineTo(0, H); c.fill();
      c.fillStyle = D.C.sableOmbre;
      c.beginPath(); c.moveTo(0, H * 0.66); c.quadraticCurveTo(W * 0.5, H * 0.62, W, H * 0.68);
      c.quadraticCurveTo(W * 0.5, H * 0.66, 0, H * 0.70); c.fill();
      D.palmier(c, W * 0.10, H * 0.72, 1.15, t, 7);
      D.palmier(c, W * 0.90, H * 0.75, 1.0, t, 13);
    },
    /* fond de marque, pour les cartons */
    carton: function (c, t) {
      c.fillStyle = D.grad(c, 0, 0, W, H, [[0, "#0a2550"], [0.55, "#123a72"], [1, "#0a2550"]]);
      c.fillRect(0, 0, W, H);
      var g = c.createRadialGradient(W * 0.5, H * 0.38, 20, W * 0.5, H * 0.38, W * 0.9);
      g.addColorStop(0, "rgba(246,188,28,.20)"); g.addColorStop(1, "rgba(246,188,28,0)");
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      var r = D.rng(41);
      for (var i = 0; i < 40; i++) {
        var x = r() * W, y = r() * H, ph = r() * 6.3;
        c.fillStyle = "rgba(255,255,255," + (0.06 + 0.10 * (0.5 + 0.5 * Math.sin(t * 1.6 + ph))).toFixed(3) + ")";
        c.beginPath(); c.arc(x, y, 2 + r() * 3, 0, 7); c.fill();
      }
      D.mer(c, W, H, t, H * 0.80, 0);
      D.vedette(c, W * (0.30 + 0.10 * Math.sin(t * 0.35)), H * 0.88, 0.72, t, true);
    }
  };

  /* ---------------- OBJETS de scène ---------------- */
  function objets(c, plan, tl, k) {
    (plan.objets || []).forEach(function (o) {
      var app = o.apparait || 0, kk = D.clamp((tl - app) / 0.5, 0, 1), e = D.ease(kk);
      if (kk <= 0) return;
      c.save(); c.globalAlpha = e;
      if (o.type === "telephone") {
        var s = (o.taille || 1) * (0.9 + 0.1 * e);
        D.telephone(c, W * o.x, H * o.y + (1 - e) * 60, s, o.ecran, tl, o.prog === undefined ? D.clamp((tl - app) / (o.duree_prog || 1.6), 0, 1) : o.prog);
      } else if (o.type === "bulle") {
        bulle(c, W * o.x, H * o.y, o.texte, o.taille || 1, e);
      }
      c.restore();
    });
  }
  function bulle(c, x, y, texte, s, e) {
    c.save(); c.translate(x, y); c.scale(s * (0.9 + 0.1 * e), s * (0.9 + 0.1 * e));
    c.font = "700 40px Poppins, sans-serif"; c.textAlign = "center";
    var w = c.measureText(texte).width + 70;
    c.fillStyle = "rgba(255,255,255,.96)"; D.rrect.call(c, -w / 2, -46, w, 92, 46); c.fill();
    c.beginPath(); c.moveTo(-16, 40); c.lineTo(6, 78); c.lineTo(22, 38); c.fill();
    c.fillStyle = C.nuit; c.fillText(texte, 0, 14); c.restore();
  }

  /* ---------------- HABILLAGE : titres et sous-titres ---------------- */
  function titre(c, plan, tl) {
    if (!plan.titre) return;
    var e = D.ease(D.clamp(tl / 0.7, 0, 1));
    c.save(); c.globalAlpha = e;
    c.textAlign = "center";
    c.fillStyle = C.jaune; c.font = "900 96px Poppins, sans-serif";
    c.fillText(plan.titre, W / 2, H * 0.42 - (1 - e) * 30);
    if (plan.sousTitre) {
      c.fillStyle = "rgba(255,255,255,.92)"; c.font = "600 44px Inter, sans-serif";
      lignes(c, plan.sousTitre, W * 0.8).forEach(function (L, i) {
        c.fillText(L, W / 2, H * 0.42 + 78 + i * 58);
      });
    }
    c.restore();
  }
  function lignes(c, texte, largeurMax) {
    var mots = texte.split(" "), out = [], cur = "";
    mots.forEach(function (m) {
      var essai = cur ? cur + " " + m : m;
      if (c.measureText(essai).width > largeurMax && cur) { out.push(cur); cur = m; }
      else cur = essai;
    });
    if (cur) out.push(cur);
    return out;
  }
  function sousTitre(c, texte, tl, duree) {
    if (!texte) return;
    var e = D.ease(D.clamp(tl / 0.25, 0, 1)) * D.ease(D.clamp((duree - tl) / 0.25, 0, 1));
    c.save(); c.globalAlpha = e;
    c.font = "600 46px Inter, sans-serif"; c.textAlign = "center";
    var Ls = lignes(c, texte, W * 0.82), hh = Ls.length * 62 + 40, y0 = H * 0.855 - hh / 2;
    c.fillStyle = "rgba(6,20,44,.82)"; D.rrect.call(c, W * 0.06, y0, W * 0.88, hh, 26); c.fill();
    c.strokeStyle = "rgba(246,188,28,.5)"; c.lineWidth = 3; c.stroke();
    c.fillStyle = "#fff";
    Ls.forEach(function (L, i) { c.fillText(L, W / 2, y0 + 62 + i * 62); });
    c.restore();
  }
  function logoFinal(c, tl) {
    var e = D.ease(D.clamp(tl / 0.8, 0, 1));
    c.save(); c.globalAlpha = e; c.textAlign = "center";
    var img = global._logo;
    if (img && img.complete && img.naturalWidth) {
      /* le logo présenté comme une icône d'application : carte blanche à coins arrondis */
      var cote = W * 0.40, cx0 = W / 2 - cote / 2, cy0 = H * 0.34 - cote / 2 - (1 - e) * 24;
      c.save();
      c.shadowColor = "rgba(0,0,0,.45)"; c.shadowBlur = 46; c.shadowOffsetY = 16;
      c.fillStyle = "#fff"; D.rrect.call(c, cx0, cy0, cote, cote, cote * 0.22); c.fill();
      c.restore();
      c.save(); D.rrect.call(c, cx0, cy0, cote, cote, cote * 0.22); c.clip();
      var s = (cote * 0.86) / img.naturalWidth;
      c.drawImage(img, W / 2 - img.naturalWidth * s / 2, cy0 + cote / 2 - img.naturalHeight * s / 2,
        img.naturalWidth * s, img.naturalHeight * s);
      c.restore();
    }
    c.fillStyle = "#fff"; c.font = "900 82px Poppins, sans-serif";
    c.fillText("moheligo.com", W / 2, H * 0.53);
    c.fillStyle = C.jaune; c.font = "600 46px Inter, sans-serif";
    c.fillText("Réserve ta traversée, garde ton billet", W / 2, H * 0.585);
    c.restore();
  }

  /* ---------------- un plan complet ---------------- */
  function dessinerPlan(c, plan, tl, tGlobal) {
    c.save();
    /* caméra : zoom + travelling */
    var cam = plan.camera || {}, k = D.ease(D.clamp(tl / plan._duree, 0, 1));
    var z = cam.zoom ? D.lerp(cam.zoom[0], cam.zoom[1], k) : 1;
    var px = cam.pan ? D.lerp(cam.pan[0], cam.pan[1], k) : 0;
    var py = cam.panY ? D.lerp(cam.panY[0], cam.panY[1], k) : 0;
    var fx = (cam.focus ? cam.focus[0] : 0.5) * W, fy = (cam.focus ? cam.focus[1] : 0.5) * H;
    c.translate(fx, fy); c.scale(z, z); c.translate(-fx + px * W, -fy + py * H);

    (DECORS[plan.decor] || DECORS.carton)(c, tGlobal);

    /* mode « insert » : le décor s'efface derrière l'objet montré en gros */
    if (plan.insert) {
      c.fillStyle = "rgba(6,20,44,.70)"; c.fillRect(-W, -H, W * 3, H * 3);
      var fx2 = (plan.insertFocus ? plan.insertFocus[0] : 0.5) * W;
      var fy2 = (plan.insertFocus ? plan.insertFocus[1] : 0.46) * H;
      var lueur = c.createRadialGradient(fx2, fy2, 20, fx2, fy2, W * 0.75);
      lueur.addColorStop(0, "rgba(246,188,28,.28)");
      lueur.addColorStop(0.5, "rgba(63,198,216,.10)");
      lueur.addColorStop(1, "rgba(0,0,0,0)");
      c.fillStyle = lueur; c.fillRect(-W, -H, W * 3, H * 3);
    }

    /* acteurs, du plus lointain au plus proche */
    (plan.acteurs || []).slice().sort(function (a, b) { return (a.h || 700) - (b.h || 700); })
      .forEach(function (a) {
        var perso = (EP.personnages || {})[a.qui] || {};
        var look = perso.look || {};
        var parle = plan.replique && plan.replique.qui === a.qui;
        var img = Math.floor(tGlobal * EP.fps);
        var amp = parle ? (ENV[img] || 0) : 0;
        /* clignement : chaque personnage a son rythme */
        var g = (a.qui.charCodeAt(0) * 7 + a.qui.length * 13) % 97;
        var cyc = (tGlobal * 1000 + g * 137) % 4200;
        var clign = cyc < 130 ? Math.sin(cyc / 130 * Math.PI) : 0;
        var entree = a.entre ? D.ease(D.clamp((tl - (a.entre[0] || 0)) / (a.entre[1] || 1), 0, 1)) : 1;
        var x = W * (a.xFin !== undefined ? D.lerp(a.x, a.xFin, D.ease(D.clamp(tl / plan._duree, 0, 1))) : a.x);
        D.personnage(c, {
          x: x, y: H * (a.y || 0.86), h: (a.h || 700),
          peau: look.peau, tenue: look.tenue, motif: look.motif, coiffe: look.coiffe,
          coifCouleur: look.coifCouleur, robe: look.robe,
          dir: a.dir || 1, pose: a.pose || "debout", bras: a.bras || "repos",
          bouche: amp, clign: clign, sourire: a.sourire === undefined ? 0.4 : a.sourire,
          sourcils: a.sourcils || 0, graine: g
        }, tGlobal * entree);
      });

    objets(c, plan, tl, k);
    c.restore();
    /* habillage hors caméra */
    if (plan.logo) logoFinal(c, tl);
    titre(c, plan, tl);
    if (plan.replique && plan.replique.texte && plan.sousTitres !== false)
      sousTitre(c, plan.replique.texte, tl, plan._duree);
  }

  /* ---------------- image finale (avec fondus enchaînés) ---------------- */
  function rendre(cx, t) {
    var i = 0;
    for (var k = 0; k < EP.plans.length; k++) if (t >= EP.plans[k]._debut) i = k;
    var plan = EP.plans[i], tl = t - plan._debut;
    dessinerPlan(cx, plan, tl, t);
    /* fondu enchaîné avec le plan suivant */
    var suiv = EP.plans[i + 1], fondu = EP.fondu === undefined ? 0.45 : EP.fondu;
    if (suiv && tl > plan._duree - fondu) {
      var a = D.ease((tl - (plan._duree - fondu)) / fondu);
      cxBase.clearRect(0, 0, W, H);
      dessinerPlan(cxBase, suiv, tl - plan._duree, t);
      cx.save(); cx.globalAlpha = a; cx.drawImage(cvBase, 0, 0); cx.restore();
    }
    /* ouverture / fermeture au noir */
    var ouv = 0.6;
    if (t < ouv) { cx.fillStyle = "rgba(0,0,0," + (1 - D.ease(t / ouv)) + ")"; cx.fillRect(0, 0, W, H); }
    var reste = EP._duree - t;
    if (reste < ouv) { cx.fillStyle = "rgba(0,0,0," + (1 - D.ease(D.clamp(reste / ouv, 0, 1))) + ")"; cx.fillRect(0, 0, W, H); }
  }

  global.MG = { init: init, rendre: rendre, DECORS: DECORS, get EP() { return EP; } };
})(window);
