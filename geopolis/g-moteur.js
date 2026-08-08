/* GÉOPOLIS — Moteur de simulation
 *
 * Conception : orientée données. Tout l'état du monde tient dans des tableaux
 * typés indexés par le numéro du pays, ce qui permet de simuler 197 nations,
 * 23 bâtiments, 11 unités et 13 marchés à chaque jour de jeu sans allocation
 * ni parcours d'objets. Un tour de simulation coûte ~40 000 opérations
 * arithmétiques : négligeable, même à vitesse ×20.
 */
(function (G) {
  'use strict';

  const N = G.N, NRES = G.NRES, NBAT = G.NBAT, NUNI = G.NUNI, R = G.R, B = G.B, U = G.U;
  const clamp = (v, a, b) => v < a ? a : v > b ? b : v;
  const NTECH = G.TECHS.length;
  const f64 = n => new Float64Array(n);
  G.clamp = clamp;

  const E = G.E = {};

  // ───────────────────────────────────────────────────────────── Initialisation
  G.nouvellePartie = function (codeJoueur, difficulte) {
    E.joueur = G.PARCODE[codeJoueur];
    E.difficulte = difficulte || 'normal';
    E.jour = 0;
    E.date = new Date(2026, 0, 1);
    E.vitesse = 1;
    E.pause = true;
    E.fini = null;

    E.pop = f64(N); E.pib = f64(N); E.croiss = f64(N);
    E.tresor = f64(N); E.dette = f64(N);
    E.tech = f64(N); E.stab = f64(N); E.approb = f64(N);
    E.corrupt = f64(N); E.chomage = f64(N); E.inflation = f64(N);
    E.educ = f64(N); E.sante = f64(N); E.infra = f64(N);
    E.expCap = f64(N); E.milcap = f64(N); E.moral = f64(N);
    E.rech = f64(N); E.calcul = f64(N); E.ia = f64(N);
    E.reput = f64(N); E.dernierBilan = f64(N);

    E.bat = new Int32Array(N * NBAT);
    E.uni = f64(N * NUNI);
    E.stock = f64(N * NRES);
    E.prod = f64(N * NRES);
    E.conso = f64(N * NRES);
    E.penurie = f64(N * NRES);
    E.rel = new Int8Array(N * N);
    E.techs = new Uint8Array(N * G.TECHS.length);
    E.rechCours = new Int16Array(N).fill(-1);
    E.rechAcc = f64(N);

    // Fiscalité et budget (parts du PIB)
    E.tIR = f64(N); E.tIS = f64(N); E.tTVA = f64(N); E.tDou = f64(N);
    E.bSante = f64(N); E.bEduc = f64(N); E.bInfra = f64(N); E.bDef = f64(N); E.bSub = f64(N);

    E.prix = f64(NRES);
    E.prixBase = f64(NRES);
    E.calib = f64(NRES).fill(1);
    G.RES.forEach((r, k) => { E.prix[k] = r.prix; E.prixBase[k] = r.prix; });

    E.chantiers = [];   // { p, b, reste, total }
    E.casernes = [];    // { p, u, reste, n }
    E.contrats = [];    // { v, a, r, qte, prix, jours, id }
    E.guerres = [];     // { a, d, front, jour, mortsA, mortsD }
    E.alliances = [];   // [i, j]
    E.pactes = [];      // [i, j]
    E.sanctions = [];   // [i, j]
    E.lois = new Set();
    E.defisFaits = [];
    E.defisQueue = [];
    E.journal = [];
    E.evenement = null;
    E.onu = null;
    E.idContrat = 1;
    E.score = 0;

    for (let i = 0; i < N; i++) {
      const p = G.PAYS[i];
      E.pop[i] = p.pop;
      E.pib[i] = p.pib;
      E.tech[i] = p.tech;
      E.stab[i] = p.stab;
      E.approb[i] = clamp(p.stab * 0.6 + 22, 25, 78);
      E.corrupt[i] = clamp(100 - p.stab * 0.9 - p.tech * 0.15, 3, 88);
      E.chomage[i] = clamp(14 - p.tech * 0.09 + (60 - p.stab) * 0.07, 2.5, 32);
      E.inflation[i] = clamp(9 - p.stab * 0.07 - p.tech * 0.02, 0.6, 45);
      E.educ[i] = clamp(p.tech * 0.85 + 8, 8, 96);
      E.sante[i] = clamp(p.tech * 0.8 + p.stab * 0.15, 8, 95);
      E.infra[i] = clamp(p.tech * 0.75 + p.stab * 0.2, 8, 96);
      E.moral[i] = 60;
      E.reput[i] = clamp(p.stab * 0.7 + 20, 15, 92);
      E.tresor[i] = p.pib * 80;                 // ≈ 8 % du PIB, soit un mois de budget
      E.dette[i] = p.pib * 1000 * (0.35 + Math.random() * 0.4);

      const nord = p.tech > 70;
      E.tIR[i] = nord ? 0.28 : 0.16;
      E.tIS[i] = nord ? 0.24 : 0.20;
      E.tTVA[i] = nord ? 0.19 : 0.13;
      E.tDou[i] = nord ? 0.03 : 0.09;
      E.bSante[i] = nord ? 0.070 : 0.030;
      E.bEduc[i] = nord ? 0.050 : 0.030;
      E.bInfra[i] = nord ? 0.030 : 0.025;
      E.bDef[i]  = clamp(p.arm / 1400 + 0.008, 0.008, 0.055);
      E.bSub[i]  = 0.020;

      dotationsInitiales(i, p);
      forcesInitiales(i, p);
      relationsInitiales(i, p);
      technosInitiales(i, p);

      // Stocks de départ : 30 jours de consommation
      for (let r = 0; r < NRES; r++) E.stock[i * NRES + r] = 0;
    }

    // Calibrage du monde : on met la production mondiale en face de la
    // consommation mondiale, ressource par ressource. Sans cela, les valeurs
    // écrites à la main dans les fiches de bâtiments produiraient un monde
    // structurellement en pénurie dès le premier jour.
    aplatirDefinitions();
    calculerFlux();
    for (let r = 0; r < NRES; r++) {
      let P = 0, C = 0;
      for (let i = 0; i < N; i++) { P += E.prod[i * NRES + r]; C += E.conso[i * NRES + r]; }
      E.calib[r] = (C > 0 && P > 0) ? clamp(C * 1.06 / P, 0.15, 60) : 1;
    }
    calculerFlux();

    for (let i = 0; i < N; i++)
      for (let r = 0; r < NRES; r++)
        E.stock[i * NRES + r] = E.conso[i * NRES + r] * 22 + 40;

    // Référence de rattrapage : le pays le plus riche par habitant parmi ceux
    // qui pèsent au moins dix millions d'âmes (sinon les micro-États faussent tout).
    E.refPibHab = 0;
    for (let i = 0; i < N; i++) {
      if (E.pop[i] < 1e7) continue;
      const h = E.pib[i] / (E.pop[i] / 1e6);
      if (h > E.refPibHab) E.refPibHab = h;
    }

    E.rel[E.joueur * N + E.joueur] = 100;
    journal('👑', `Vous prenez la tête de ${G.PAYS[E.joueur].nom}. Le monde vous regarde.`, 'important');
    return E;
  };

  function dotationsInitiales(i, p) {
    // Parc de bâtiments cohérent avec la taille et la richesse du pays
    const ech = Math.pow(p.pib, 0.62) / 6;          // échelle économique
    const pop = p.pop / 1e6;
    const set = (b, n) => { E.bat[i * NBAT + b] = Math.max(0, Math.round(n)); };

    set(B.ferme,     pop * 0.55 + ech * 0.10);
    set(B.route,     ech * 0.42 + pop * 0.05);
    set(B.hopital,   pop * 0.16 + ech * 0.10);
    set(B.universite,ech * 0.16 + pop * 0.04);
    set(B.usine,     ech * 0.34);
    set(B.port,      p.cont === 'OC' || p.pib > 200 ? ech * 0.05 + 1 : ech * 0.03);
    set(B.base,      p.arm * 0.13);
    set(B.labo,      p.tech > 55 ? ech * 0.07 : ech * 0.015);

    const d = p.dot;
    set(B.puits,     d[0] >= 1 ? ech * 0.05 * d[0] : 0);
    set(B.gaziere,   d[1] >= 1 ? ech * 0.04 * d[1] : 0);
    set(B.houillere, d[2] >= 1 ? ech * 0.035 * d[2] : 0);
    set(B.minefer,   d[3] >= 1 ? ech * 0.035 * d[3] : 0);
    set(B.minecuivre,d[4] >= 1 ? ech * 0.030 * d[4] : 0);
    set(B.mineterres,d[5] >= 2 && p.tech > 45 ? ech * 0.012 * d[5] : 0);
    set(B.mineuran,  d[6] >= 3 && p.tech > 50 ? ech * 0.010 * d[6] : 0);
    set(B.mineor,    d[7] >= 2 ? ech * 0.012 * d[7] : 0);

    set(B.thermique, ech * 0.10 * (d[2] >= 3 ? 1.5 : 0.7));
    set(B.cycle,     ech * 0.09 * (d[1] >= 3 ? 1.5 : 0.7));
    set(B.solaire,   ech * 0.09 * (p.tech > 65 ? 1.6 : 0.6));
    set(B.nucleaire, p.tech > 62 && p.pib > 250 ? ech * 0.05 : 0);
    set(B.fonderie,  p.tech > 82 && p.pib > 400 ? ech * 0.010 : 0);
    set(B.datacenter,p.tech > 72 ? ech * 0.016 : 0);

    const nuk = ['US','RU','CN','FR','GB','IN','PK','IL','KP'];
    set(B.silo, nuk.indexOf(p.code) >= 0 ? 1 + Math.round(p.arm / 40) : 0);
  }

  function forcesInitiales(i, p) {
    const a = p.arm, ech = Math.pow(p.pib, 0.55) / 4;
    const set = (u, n) => { E.uni[i * NUNI + u] = Math.max(0, Math.round(n)); };
    set(U.infanterie, a * 1.5 + p.pop / 3.5e6);
    set(U.blindes,    a * 0.30 * (ech / 10 + 0.5));
    set(U.artillerie, a * 0.36 * (ech / 10 + 0.5));
    set(U.dca,        a * 0.20 * (ech / 10 + 0.5));
    set(U.chasse,     p.tech > 50 ? a * 0.16 * (ech / 12 + 0.4) : a * 0.03);
    set(U.drones,     p.tech > 55 ? a * 0.20 : a * 0.04);
    set(U.helico,     p.tech > 45 ? a * 0.13 : 0);
    set(U.navire,     p.tech > 45 ? a * 0.11 : a * 0.02);
    set(U.sousmarin,  p.tech > 65 ? a * 0.05 : 0);
    set(U.missile,    p.tech > 60 ? a * 0.14 : a * 0.02);
    const nuk = { US:1700, RU:1710, CN:600, FR:290, GB:225, IN:180, PK:170, IL:90, KP:50 };
    set(U.ogive, nuk[p.code] || 0);
  }

  function technosInitiales(i, p) {
    G.TECHS.forEach((t, k) => {
      const seuil = 38 + k * 3.6;
      if (p.tech >= seuil) E.techs[i * G.TECHS.length + k] = 1;
    });
    // Le calcul cumulé de départ reflète l'avance technologique réelle
    const dc = E.bat[i * NBAT + B.datacenter];
    E.calcul[i] = dc * 900 * Math.pow(p.tech / 70, 3);
    E.ia[i] = niveauIA(E.calcul[i]);
  }

  function relationsInitiales(i, p) {
    for (let j = 0; j < N; j++) {
      if (i === j) { E.rel[i * N + j] = 100; continue; }
      const q = G.PAYS[j];
      let r = 8;
      if (q.cont === p.cont) r += 12;
      if (q.reg === p.reg) r += 10; else r -= 6;
      const d = distance(p, q);
      r += d > 8000 ? 4 : d < 1500 ? -6 : 0;      // les voisins se disputent
      E.rel[i * N + j] = clamp(Math.round(r), -100, 100);
    }
  }

  // Blocs et inimitiés historiques appliqués après la construction de la table
  G.appliquerGeopolitique = function () {
    const set = (a, b, v) => {
      const i = G.PARCODE[a], j = G.PARCODE[b];
      if (i === undefined || j === undefined) return;
      E.rel[i * N + j] = clamp(v, -100, 100);
      E.rel[j * N + i] = clamp(v, -100, 100);
    };
    G.BLOCS.forEach(bloc => {
      for (let a = 0; a < bloc.membres.length; a++)
        for (let b = a + 1; b < bloc.membres.length; b++) {
          const i = G.PARCODE[bloc.membres[a]], j = G.PARCODE[bloc.membres[b]];
          if (i === undefined || j === undefined) continue;
          E.rel[i * N + j] = clamp(E.rel[i * N + j] + 22, -100, 100);
          E.rel[j * N + i] = E.rel[i * N + j];
        }
      if (bloc.id === 'otan' || bloc.id === 'ue') {
        for (let a = 0; a < bloc.membres.length; a++)
          for (let b = a + 1; b < bloc.membres.length; b++) {
            const i = G.PARCODE[bloc.membres[a]], j = G.PARCODE[bloc.membres[b]];
            if (i !== undefined && j !== undefined) E.alliances.push([i, j]);
          }
      }
    });
    [['US','RU',-62],['US','CN',-38],['US','IR',-72],['US','KP',-80],['RU','UA',-92],
     ['CN','TW',-70],['CN','IN',-34],['IN','PK',-68],['IL','IR',-85],['KP','KR',-72],
     ['RU','PL',-58],['SA','IR',-60],['AM','AZ',-64],['MA','DZ',-48],['ET','ER',-46],
     ['VE','US',-52],['CU','US',-40],['GR','TR',-28],['RS','XK',-70],['JP','CN',-32]
    ].forEach(x => set(x[0], x[1], x[2]));
  };

  function distance(a, b) {
    const dl = (a.lat - b.lat) * 111, dg = (a.lon - b.lon) * 111 * Math.cos((a.lat + b.lat) / 2 * Math.PI / 180);
    return Math.sqrt(dl * dl + dg * dg);
  }
  G.distance = distance;

  function niveauIA(c) {
    let n = 0;
    for (let k = G.PALIERS_IA.length - 1; k >= 0; k--)
      if (c >= G.PALIERS_IA[k].seuil) { n = k; break; }
    return n;
  }
  G.niveauIA = niveauIA;

  // ───────────────────────────────────────────────────────────── Multiplicateurs
  const TIDX = {}; G.TECHS.forEach((t, k) => { TIDX[t.id] = k; });
  function aTech(i, id) {
    const k = TIDX[id];
    return k !== undefined && E.techs[i * NTECH + k] === 1;
  }
  G.aTech = aTech;

  function multProd(i, bat) {
    let m = 1 + E.infra[i] / 320 + E.tech[i] / 420;
    if (bat.id === 'ferme' && aTech(i, 'agro')) m *= 1.35;
    if ((bat.id === 'puits' || bat.id === 'gaziere') && aTech(i, 'forage')) m *= 1.30;
    if (bat.cat === 'ressources' && bat.id !== 'ferme' && aTech(i, 'metallo')) m *= 1.30;
    if (bat.cat === 'energie' && aTech(i, 'reseau')) m *= 1.25;
    if (bat.id === 'nucleaire' && aTech(i, 'fission')) m *= 1.40;
    if (bat.id === 'nucleaire' && aTech(i, 'fusion')) m *= 2.50;
    if (bat.id === 'usine' && aTech(i, 'automat')) m *= 1.35;
    if (bat.id === 'fonderie' && aTech(i, 'litho')) m *= 1.60;
    if (bat.id === 'datacenter' && aTech(i, 'quantique')) m *= 1.45;
    if (bat.cat === 'ressources' && bat.id !== 'ferme' && E.lois.has('ecologie') && i === E.joueur) m *= 0.9;
    m *= (0.55 + E.stab[i] / 220);                     // un pays instable produit mal
    return m;
  }

  function multIA(i) { return 1 + [0,.02,.05,.09,.14,.20,.27,.35,.45,.60,.80][E.ia[i] | 0]; }
  G.multIA = multIA;

  function multMil(i) {
    const n = E.ia[i] | 0;
    return (1 + E.tech[i] / 190) * (1 + [0,0,0,.06,.10,.14,.25,.32,.40,.50,.65][n]);
  }
  G.multMil = multMil;

  // ───────────────────────────────────────────────────────────── Flux physiques
  // Les fiches de bâtiments sont écrites avec des objets lisibles ; on les
  // aplatit une fois en tableaux de paires [ressource, quantité] pour que la
  // boucle quotidienne n'ait plus à parcourir de propriétés d'objet.
  let BPROD, BCONSO, UCONSO;
  function aplatirDefinitions() {
    const plat = o => { const a = []; if (o) for (const k in o) a.push(R[k], o[k]); return a; };
    BPROD = G.BAT.map(b => plat(b.prod));
    BCONSO = G.BAT.map(b => plat(b.conso));
    UCONSO = G.UNI.map(u => plat(u.conso));
  }

  function calculerFlux() {
    E.prod.fill(0); E.conso.fill(0);
    for (let i = 0; i < N; i++) {
      const base = i * NRES, popM = E.pop[i] / 1e6, dots = G.PAYS[i].dot;
      let rechJour = 0, educB = 0, santeB = 0, infraB = 0, expB = 0, milB = 0;

      for (let b = 0; b < NBAT; b++) {
        const n = E.bat[i * NBAT + b];
        if (n === 0) continue;
        const bd = G.BAT[b];
        const m = multProd(i, bd);
        const facteur = bd.dot !== undefined ? 0.30 + 0.19 * dots[bd.dot] : 1;
        const pp = BPROD[b], cc = BCONSO[b];
        for (let k = 0; k < pp.length; k += 2) E.prod[base + pp[k]] += pp[k + 1] * n * m * facteur;
        for (let k = 0; k < cc.length; k += 2) E.conso[base + cc[k]] += cc[k + 1] * n;
        if (bd.rech)   rechJour += bd.rech * n;
        if (bd.educ)   educB += bd.educ * n;
        if (bd.sante)  santeB += bd.sante * n;
        if (bd.infra)  infraB += bd.infra * n;
        if (bd.export) expB += bd.export * n;
        if (bd.milcap) milB += bd.milcap * n;
      }

      // Consommation civile
      E.conso[base + R.nourriture]  += popM * 900;
      E.conso[base + R.electricite] += popM * (140 + E.tech[i] * 9);
      E.conso[base + R.biens]       += popM * (16 + E.tech[i] * 1.5);
      E.conso[base + R.petrole]     += popM * (30 + E.tech[i] * 3.2);
      E.conso[base + R.gaz]         += popM * (20 + E.tech[i] * 2.4);

      // Entretien militaire
      for (let u = 0; u < NUNI; u++) {
        const n = E.uni[i * NUNI + u];
        if (n === 0) continue;
        const uc = UCONSO[u];
        for (let k = 0; k < uc.length; k += 2) E.conso[base + uc[k]] += uc[k + 1] * n;
      }

      // Calibrage mondial appliqué à la production
      for (let r = 0; r < NRES; r++) E.prod[base + r] *= E.calib[r];

      // Capacités agrégées (moyennes glissantes)
      const popRef = Math.max(popM, 0.4);
      cible(E.educ, i, clamp(18 + (educB / popRef) * 130 + E.tech[i] * 0.35 + (aTech(i,'educ') ? 12 : 0), 5, 100), 0.004);
      cible(E.sante, i, clamp(15 + (santeB / popRef) * 95 + E.tech[i] * 0.32 + (aTech(i,'medecine') ? 12 : 0), 5, 100), 0.004);
      cible(E.infra, i, clamp(12 + (infraB / popRef) * 120 + E.tech[i] * 0.30 + (aTech(i,'logistique') ? 10 : 0), 5, 100), 0.004);
      E.expCap[i] = 1 + expB * 1.4 + E.infra[i] * 0.06 + (aTech(i,'logistique') ? 3 : 0);
      E.milcap[i] = 1 + milB;
      E.rechAcc[i] = rechJour * (1 + E.educ[i] / 130) * multIARech(i) * (aTech(i,'educ') ? 1.3 : 1);
    }
  }

  function multIARech(i) {
    const n = E.ia[i] | 0;
    return 1 + [0,0,.10,.15,.22,.40,.48,.60,.75,.95,1.2][n];
  }

  function cible(arr, i, v, k) { arr[i] += (v - arr[i]) * k; }

  // ───────────────────────────────────────────────────────────── Marché mondial
  function marche() {
    // 1. Contrats : livraisons à prix fixe, prioritaires sur le marché libre
    for (let c = E.contrats.length - 1; c >= 0; c--) {
      const k = E.contrats[c];
      const bv = k.v * NRES + k.r, ba = k.a * NRES + k.r;
      const dispo = Math.min(k.qte, Math.max(0, E.stock[bv] + E.prod[bv] - E.conso[bv]));
      const valeur = dispo * k.prix / 1e6;                 // M$
      const credit = Math.max(0, E.tresor[k.a]) + E.pib[k.a] * 1000 / 365 * 0.35;
      if (credit < valeur) {                               // acheteur réellement insolvable
        k.impayes = (k.impayes || 0) + 1;
        if (k.impayes > 20) rompreContrat(c, 'insolvabilité de l\'acheteur');
        continue;
      }
      k.impayes = 0;
      E.stock[bv] -= dispo; E.stock[ba] += dispo;
      E.tresor[k.v] += valeur; E.tresor[k.a] -= valeur;
      k.livre = (k.livre || 0) + valeur;
      if (dispo < k.qte * 0.6) {
        k.defauts = (k.defauts || 0) + 1;
        if (k.defauts > 20) rompreContrat(c, 'livraisons non honorées');
        continue;
      }
      if (--k.jours <= 0) {
        modifierRelation(k.v, k.a, 3);
        journalSi(k, `📜 Contrat ${G.RES[k.r].nom} ${G.PAYS[k.v].code}→${G.PAYS[k.a].code} arrivé à terme.`);
        E.contrats.splice(c, 1);
      }
    }

    // 2. Marché libre : chaque pays équilibre ses stocks
    const offre = f64(NRES), demande = f64(NRES);
    for (let i = 0; i < N; i++) {
      const base = i * NRES;
      const sanctionne = estSanctionne(i);
      for (let r = 0; r < NRES; r++) {
        let s = E.stock[base + r] + E.prod[base + r] - E.conso[base + r];
        if (s < 0) {
          // Déficit : on importe, au comptant ou à crédit
          const besoin = -s;
          const px = E.prix[r] * (1.08 + (sanctionne ? 0.35 : 0)) / 1e6;
          const credit = Math.max(0, E.tresor[i]) + E.pib[i] * 1000 / 365 * 0.35;
          const abordable = Math.min(besoin, credit / Math.max(px, 1e-12));
          const achat = sanctionne ? abordable * 0.45 : abordable;
          E.tresor[i] -= achat * px;
          E.stock[base + r] = 0;
          E.penurie[base + r] = clamp(1 - achat / besoin, 0, 1);
          demande[r] += besoin;
          if (E.tDou[i] > 0) E.tresor[i] += achat * px * E.tDou[i] * 0.9;   // droits de douane
        } else {
          E.penurie[base + r] = 0;
          const plafond = E.conso[base + r] * 20 + 60;
          const excedent = Math.max(0, s - plafond);
          const capacite = E.expCap[i] * (G.RES[r].strat ? 900 : 26000) * (sanctionne ? 0.3 : 1);
          const vente = Math.min(excedent, capacite);
          E.tresor[i] += vente * E.prix[r] * 0.95 / 1e6;
          E.stock[base + r] = s - vente;
          offre[r] += excedent;
        }
      }
    }

    // 3. Ajustement des prix : tension entre la production et la consommation
    //    mondiales. C'est le seul signal honnête — les seuls flux réellement
    //    expédiés dépendent des capacités portuaires et fausseraient tout.
    for (let r = 0; r < NRES; r++) {
      let P = 0, C = 0;
      for (let i = 0; i < N; i++) { P += E.prod[i * NRES + r]; C += E.conso[i * NRES + r]; }
      const tot = P + C + 1;
      const tension = C > 0.10 * P ? (C - P) / tot : 0;
      E.prix[r] *= clamp(1 + tension * 0.010, 0.994, 1.008);
      E.prix[r] += (E.prixBase[r] - E.prix[r]) * 0.0008;         // rappel vers la moyenne
      E.prix[r] = clamp(E.prix[r], E.prixBase[r] * 0.30, E.prixBase[r] * 5.5);
    }
  }

  function estSanctionne(i) {
    for (let s = 0; s < E.sanctions.length; s++) if (E.sanctions[s][1] === i) return true;
    return false;
  }
  G.estSanctionne = estSanctionne;

  function rompreContrat(idx, raison) {
    const k = E.contrats[idx];
    modifierRelation(k.v, k.a, -12);
    journalSi(k, `⚠️ Contrat ${G.RES[k.r].nom} ${G.PAYS[k.v].code}→${G.PAYS[k.a].code} rompu (${raison}).`, 'mauvais');
    E.contrats.splice(idx, 1);
  }
  function journalSi(k, txt, t) { if (k.v === E.joueur || k.a === E.joueur) journal('', txt, t); }

  // ───────────────────────────────────────────────────────────── Économie
  function economie() {
    const pibMax = E.refPibHab || 80000;
    for (let i = 0; i < N; i++) {
      const base = i * NRES;
      const pibHab = E.pib[i] / Math.max(E.pop[i] / 1e6, 0.02);
      const pibJour = E.pib[i] * 1000 / 365;                       // M$/jour

      // ── Croissance
      const usines = E.bat[i * NBAT + B.usine];
      const capital = clamp(usines / Math.max(Math.pow(E.pib[i], 0.62) / 6 * 0.34, 1) - 1, -0.5, 1.2);
      const rattrapage = clamp((1 - pibHab / pibMax) * 2.4, 0, 2.4);
      const fisc = (E.tIR[i] * 0.5 + E.tIS[i] * 0.35 + E.tTVA[i] * 0.3);
      const penNour = E.penurie[base + R.nourriture];
      const penElec = E.penurie[base + R.electricite];
      const penBiens = E.penurie[base + R.biens];
      const guerre = enGuerre(i) ? 3.2 : 0;

      let g = 1.1
        + capital * 1.6
        + rattrapage
        + (multIA(i) - 1) * 5.2
        + (E.educ[i] - 50) * 0.020
        + (E.infra[i] - 50) * 0.016
        + (E.sante[i] - 50) * 0.008
        + (E.stab[i] - 50) * 0.020
        + E.bInfra[i] * 22 + E.bEduc[i] * 14 + E.bSub[i] * 8
        - (fisc - 0.20) * 9.5
        - E.corrupt[i] * 0.035
        - penNour * 7 - penElec * 9 - penBiens * 3.5
        - guerre
        - clamp(E.dette[i] / (E.pib[i] * 1000) - 0.85, 0, 3) * 3.2
        - (E.inflation[i] > 8 ? (E.inflation[i] - 8) * 0.22 : 0);

      if (E.lois.has('liberalisme') && i === E.joueur) g += 0.8;
      if (E.lois.has('protection') && i === E.joueur) g -= 0.5;
      g = clamp(g, -14, 15);
      E.croiss[i] += (g - E.croiss[i]) * 0.03;
      E.pib[i] *= (1 + E.croiss[i] / 36500);

      // ── Recettes
      const collecte = 1 - E.corrupt[i] / 260;
      let rec = pibJour * (
        0.62 * E.tIR[i]  * laffer(E.tIR[i]) +
        0.19 * E.tIS[i]  * laffer(E.tIS[i]) +
        0.62 * E.tTVA[i] * laffer(E.tTVA[i])
      ) * collecte;

      // ── Dépenses
      const entretien = coutEntretien(i);
      let dep = pibJour * (E.bSante[i] + E.bEduc[i] + E.bInfra[i] + E.bDef[i] + E.bSub[i] + 0.042)
              + entretien
              + E.dette[i] * tauxInteret(i) / 365;
      if (E.lois.has('gratuite') && i === E.joueur) dep += pibJour * (E.bSante[i] + E.bEduc[i]) * 0.4;

      const solde = rec - dep;
      E.dernierBilan[i] = solde;
      E.tresor[i] += solde;

      if (E.tresor[i] < 0) { E.dette[i] -= E.tresor[i]; E.tresor[i] = 0; }
      else if (E.tresor[i] > pibJour * 45 && E.dette[i] > 0) {          // remboursement automatique
        const rb = Math.min(E.dette[i], (E.tresor[i] - pibJour * 45) * 0.25);
        E.dette[i] -= rb; E.tresor[i] -= rb;
      }

      // ── Inflation, chômage
      const deficit = clamp(-solde / Math.max(pibJour, 0.01), -0.5, 0.9);
      const cibleInf = clamp(1.8 + deficit * 14 + penNour * 22 + penBiens * 9 + E.croiss[i] * 0.22
                             + (E.dette[i] / (E.pib[i] * 1000) > 1.2 ? 5 : 0), 0, 90);
      cible(E.inflation, i, cibleInf, 0.006);

      const iaChom = (E.ia[i] | 0) * (E.lois.has('gratuite') && i === E.joueur ? 0.45 : 0.85);
      const cibleChom = clamp(11.5 - E.croiss[i] * 1.15 - E.educ[i] * 0.028 + iaChom
                              + E.corrupt[i] * 0.045 + (guerre ? -2 : 0), 1.8, 45);
      cible(E.chomage, i, cibleChom, 0.005);
    }
  }

  // Courbe de Laffer : au-delà d'un certain taux, l'assiette se dérobe.
  function laffer(t) { return clamp(1 - 0.62 * Math.pow(t / 0.62, 2.1), 0.22, 1); }
  G.laffer = laffer;

  function tauxInteret(i) {
    const ratio = E.dette[i] / Math.max(E.pib[i] * 1000, 1);
    return clamp(0.018 + ratio * 0.045 + (100 - E.stab[i]) * 0.0008, 0.012, 0.35);
  }
  G.tauxInteret = tauxInteret;

  function coutEntretien(i) {
    let c = 0;
    for (let b = 0; b < NBAT; b++) c += E.bat[i * NBAT + b] * G.BAT[b].entretien;
    for (let u = 0; u < NUNI; u++) c += E.uni[i * NUNI + u] * G.UNI[u].entretien;
    return c;
  }
  G.coutEntretien = coutEntretien;

  // ───────────────────────────────────────────────────────────── Société
  function societe() {
    for (let i = 0; i < N; i++) {
      const base = i * NRES;
      const penNour = E.penurie[base + R.nourriture], penElec = E.penurie[base + R.electricite];
      const joueur = i === E.joueur;

      let cibleApp = 50
        + clamp((E.croiss[i] - 1.5) * 5.5, -20, 20)
        - clamp((E.chomage[i] - 6) * 1.5, -10, 24)
        - clamp((E.inflation[i] - 3) * 1.6, -8, 26)
        - (E.tIR[i] * 42 + E.tTVA[i] * 34 + E.tIS[i] * 10 - 22)
        + (E.sante[i] - 50) * 0.22 + (E.educ[i] - 50) * 0.15 + (E.infra[i] - 50) * 0.10
        - E.corrupt[i] * 0.30
        - penNour * 45 - penElec * 22
        + (E.bSub[i] - 0.02) * 260;

      if (joueur) {
        if (E.lois.has('servicemil')) cibleApp -= 6;
        if (E.lois.has('ecologie')) cibleApp += 5;
        if (E.lois.has('surveillance')) cibleApp -= 7;
        if (E.lois.has('gratuite')) cibleApp += 8;
        if (E.lois.has('iaouverte')) cibleApp += 4;
        if (E.lois.has('antitrust')) cibleApp -= 3;
      }
      const gu = guerreDe(i);
      if (gu) cibleApp += (gu.a === i ? gu.front : -gu.front) * 0.16 - 4;

      cible(E.approb, i, clamp(cibleApp, 0, 100), 0.010);

      let cibleStab = 30 + E.approb[i] * 0.45 + E.educ[i] * 0.10 + E.sante[i] * 0.06
                      - E.corrupt[i] * 0.22 - E.chomage[i] * 0.35 - penNour * 30;
      if (joueur && E.lois.has('surveillance')) cibleStab += 10;
      if (joueur && E.lois.has('antitrust')) cibleStab += 4;
      cible(E.stab, i, clamp(cibleStab, 0, 100), 0.008);

      let cibleCor = 70 - E.educ[i] * 0.35 - E.stab[i] * 0.20 - (E.ia[i] | 0) * 1.6;
      if (joueur && E.lois.has('antitrust')) cibleCor -= 18;
      if (joueur && E.lois.has('liberalisme')) cibleCor += 7;
      cible(E.corrupt, i, clamp(cibleCor, 1, 95), 0.004);

      // Population
      const fec = clamp(0.028 - E.educ[i] * 0.00018 - E.pib[i] / Math.max(E.pop[i] / 1e6, 1) * 0.00000012, 0.001, 0.036);
      const mort = clamp(0.014 - E.sante[i] * 0.00008 + penNour * 0.02, 0.004, 0.06);
      E.pop[i] *= (1 + (fec - mort) / 365);

      cible(E.moral, i, clamp(45 + E.approb[i] * 0.3 + E.stab[i] * 0.2 + (E.lois.has('servicemil') && joueur ? 8 : 0), 10, 100), 0.01);
      cible(E.reput, i, clamp(50 + E.stab[i] * 0.2 - E.uni[i * NUNI + U.ogive] * 0.004 - E.guerres.filter(g => g.a === i).length * 15, 0, 100), 0.003);
    }
  }

  // ───────────────────────────────────────────────────────────── Recherche & IA
  function recherche() {
    const NT = G.TECHS.length;
    for (let i = 0; i < N; i++) {
      E.rech[i] += E.rechAcc[i];
      let k = E.rechCours[i];
      if (k < 0 || E.techs[i * NT + k]) { k = choisirRecherche(i); E.rechCours[i] = k; }
      if (k >= 0) {
        const t = G.TECHS[k];
        if (E.rech[i] >= t.cout) {
          E.rech[i] -= t.cout;
          E.techs[i * NT + k] = 1;
          E.tech[i] = clamp(E.tech[i] + 1.6, 0, 100);
          E.rechCours[i] = -1;
          if (i === E.joueur) journal('🔬', `Percée scientifique : ${t.nom}. ${t.effet}.`, 'bon');
        }
      }
      // Course à l'IA : le calcul produit s'accumule
      const c = E.prod[i * NRES + R.calcul] * (1 - E.penurie[i * NRES + R.electricite]);
      const frein = (i === E.joueur && E.lois.has('iaouverte')) ? 0.85 : 1;
      E.calcul[i] += c * frein;
      const n = niveauIA(E.calcul[i]);
      if (n > E.ia[i]) {
        E.ia[i] = n;
        E.tech[i] = clamp(E.tech[i] + 0.8, 0, 100);
        if (i === E.joueur) journal('🧠', `Palier IA ${n} atteint : ${G.PALIERS_IA[n].nom}. ${G.PALIERS_IA[n].bonus}.`, 'bon');
        else if (n >= 7) journal('🌍', `${G.PAYS[i].drapeau} ${G.PAYS[i].nom} atteint le palier IA ${n} (${G.PALIERS_IA[n].nom}).`, 'important');
      }
      E.tech[i] = clamp(E.tech[i] + (E.educ[i] - 60) * 0.000012, 0, 100);
    }
  }

  function choisirRecherche(i) {
    const NT = G.TECHS.length;
    let meilleur = -1, meilleurCout = Infinity;
    for (let k = 0; k < NT; k++) {
      if (E.techs[i * NT + k]) continue;
      const t = G.TECHS[k];
      if (!t.req.every(r => aTech(i, r))) continue;
      if (t.cout < meilleurCout) { meilleurCout = t.cout; meilleur = k; }
    }
    return meilleur;
  }

  // ───────────────────────────────────────────────────────────── Chantiers
  function chantiers() {
    for (let c = E.chantiers.length - 1; c >= 0; c--) {
      const x = E.chantiers[c];
      x.reste--;
      if (x.reste <= 0) {
        E.bat[x.p * NBAT + x.b]++;
        if (x.p === E.joueur) journal(G.BAT[x.b].icone, `${G.BAT[x.b].nom} livré et opérationnel.`, 'bon');
        E.chantiers.splice(c, 1);
      }
    }
    for (let c = E.casernes.length - 1; c >= 0; c--) {
      const x = E.casernes[c];
      x.reste--;
      if (x.reste <= 0) {
        E.uni[x.p * NUNI + x.u] += x.n;
        if (x.p === E.joueur) journal(G.UNI[x.u].icone, `${x.n} × ${G.UNI[x.u].nom} rejoignent vos forces.`, 'bon');
        E.casernes.splice(c, 1);
      }
    }
  }

  // ───────────────────────────────────────────────────────────── Guerre
  function puissance(i, off) {
    let p = 0;
    const m = multMil(i) * (0.55 + E.moral[i] / 220) * (0.7 + Math.min(E.milcap[i] / Math.max(effectifs(i) / 60, 1), 1.3) * 0.3);
    for (let u = 0; u < NUNI; u++) {
      const n = E.uni[i * NUNI + u];
      if (!n) continue;
      const ud = G.UNI[u];
      let v = off ? ud.att : ud.def;
      if (ud.id === 'drones') v *= (1 + (E.ia[i] | 0) * 0.09);
      if ((ud.id === 'chasse' || ud.id === 'navire' || ud.id === 'sousmarin') && aTech(i, 'furtif')) v *= 1.25;
      if (ud.id === 'missile' && aTech(i, 'hyperson')) v *= 1.5;
      p += n * v;
    }
    return p * m;
  }
  G.puissance = puissance;

  function effectifs(i) {
    let h = 0;
    for (let u = 0; u < NUNI; u++) h += E.uni[i * NUNI + u] * G.UNI[u].hommes;
    return h;
  }
  G.effectifs = effectifs;

  function enGuerre(i) { return E.guerres.some(g => g.a === i || g.d === i); }
  function guerreDe(i) { return E.guerres.find(g => g.a === i || g.d === i); }
  G.enGuerre = enGuerre; G.guerreDe = guerreDe;

  function guerres() {
    for (let k = E.guerres.length - 1; k >= 0; k--) {
      const g = E.guerres[k];
      const pa = puissance(g.a, true), pd = puissance(g.d, false);
      const tot = pa + pd + 1;
      const avance = (pa - pd) / tot * 1.5;
      g.front = clamp(g.front + avance, -100, 100);

      const intensite = Math.min(pa, pd) / tot;
      pertes(g.a, intensite * 0.0075 * (1 + (pd / tot)), g, 'A');
      pertes(g.d, intensite * 0.0075 * (1 + (pa / tot)), g, 'D');
      E.moral[g.a] += (g.front > 0 ? 0.05 : -0.07);
      E.moral[g.d] += (g.front < 0 ? 0.05 : -0.07);
      E.pib[g.a] *= (1 - 0.00006); E.pib[g.d] *= (1 - 0.00012);
      g.jours++;

      if (g.front >= 100) finGuerre(k, g.a, g.d);
      else if (g.front <= -100) finGuerre(k, g.d, g.a);
      else if (g.jours > 40 && Math.abs(g.front) < 12 && Math.random() < 0.006) {
        journal('🕊️', `Paix blanche entre ${G.PAYS[g.a].nom} et ${G.PAYS[g.d].nom} : le front est figé.`,
                (g.a === E.joueur || g.d === E.joueur) ? 'important' : '');
        E.guerres.splice(k, 1);
      }
    }
  }

  function pertes(i, taux, g, cote) {
    let morts = 0;
    for (let u = 0; u < NUNI; u++) {
      if (G.UNI[u].id === 'ogive') continue;
      const perdu = E.uni[i * NUNI + u] * taux;
      E.uni[i * NUNI + u] = Math.max(0, E.uni[i * NUNI + u] - perdu);
      morts += perdu * G.UNI[u].hommes;
    }
    if (cote === 'A') g.mortsA += morts; else g.mortsD += morts;
    E.pop[i] -= morts * 0.75;
  }

  function finGuerre(k, vainqueur, vaincu) {
    const joueurConcerne = vainqueur === E.joueur || vaincu === E.joueur;
    E.guerres.splice(k, 1);
    if (vainqueur === E.joueur) {
      E.capitulation = { vainqueur, vaincu };
      journal('🏳️', `${G.PAYS[vaincu].nom} capitule. À vous de décider du sort de ce pays.`, 'important');
    } else {
      appliquerCapitulation(vainqueur, vaincu, 'tribut');
      journal('🏳️', `${G.PAYS[vainqueur].nom} l'emporte sur ${G.PAYS[vaincu].nom}.`,
              joueurConcerne ? 'mauvais' : '');
    }
  }

  G.appliquerCapitulation = appliquerCapitulation;
  function appliquerCapitulation(v, d, mode) {
    if (mode === 'annexion') {
      E.pop[v] += E.pop[d] * 0.9; E.pib[v] += E.pib[d] * 0.55;
      for (let b = 0; b < NBAT; b++) { E.bat[v * NBAT + b] += Math.floor(E.bat[d * NBAT + b] * 0.6); E.bat[d * NBAT + b] = 0; }
      E.pop[d] *= 0.1; E.pib[d] *= 0.25;
      E.stab[v] -= 18; E.approb[v] -= 8; E.reput[v] -= 30;
      for (let j = 0; j < N; j++) if (j !== v) modifierRelation(v, j, -22);
      E.annexes = (E.annexes || new Set()); E.annexes.add(d);
    } else if (mode === 'tribut') {
      E.tresor[v] += E.tresor[d] * 0.7; E.tresor[d] *= 0.3;
      E.contrats.push({ v: d, a: v, r: R.or, qte: 0.004 * (E.pib[d] / 100 + 1), prix: 1, jours: 1095, id: E.idContrat++, tribut: true });
      E.reput[v] -= 12;
      for (let j = 0; j < N; j++) if (j !== v) modifierRelation(v, j, -8);
    } else {
      E.reput[v] += 4;
    }
    E.stab[d] -= 25; E.approb[d] -= 25; E.moral[d] = 25;
    modifierRelation(v, d, -60);
  }

  // ───────────────────────────────────────────────────────────── Diplomatie
  let allieCache = null, allieLen = -1;
  function estAllie(i, j) {
    if (allieLen !== E.alliances.length) {
      allieCache = new Set();
      for (let k = 0; k < E.alliances.length; k++) {
        const a = E.alliances[k];
        allieCache.add(a[0] * N + a[1]); allieCache.add(a[1] * N + a[0]);
      }
      allieLen = E.alliances.length;
    }
    return allieCache.has(i * N + j);
  }
  G.estAllie = estAllie;

  function modifierRelation(i, j, d) {
    E.rel[i * N + j] = clamp(E.rel[i * N + j] + d, -100, 100);
    E.rel[j * N + i] = clamp(E.rel[j * N + i] + d, -100, 100);
  }
  G.modifierRelation = modifierRelation;
  G.relation = (i, j) => E.rel[i * N + j];

  function derive() {
    // Les relations dérivent lentement vers la moyenne, sauf entre alliés/ennemis
    const i = E.jour % N;
    for (let j = 0; j < N; j++) {
      if (i === j) continue;
      const idx = i * N + j;
      let d = 0;
      if (estAllie(i, j)) d = 1;
      else if (E.guerres.some(g => (g.a === i && g.d === j) || (g.a === j && g.d === i))) d = -3;
      else if (E.sanctions.some(s => (s[0] === i && s[1] === j) || (s[0] === j && s[1] === i))) d = -1;
      else d = E.rel[idx] > 0 ? -0.02 : 0.02;
      if (d) { const v = clamp(E.rel[idx] + d, -100, 100); E.rel[idx] = v; E.rel[j * N + i] = v; }
    }
  }

  // ───────────────────────────────────────────────────────────── IA des nations
  // On ne traite qu'une tranche de pays par jour : coût constant, décisions
  // réparties, comportement identique à un traitement complet sur la durée.
  let curseurIA = 0;
  function cerveaux() {
    const parJour = 10;
    for (let n = 0; n < parJour; n++) {
      const i = curseurIA = (curseurIA + 1) % N;
      if (i === E.joueur) continue;
      decider(i);
    }
  }

  function decider(i) {
    const base = i * NRES;
    const pibJour = E.pib[i] * 1000 / 365;
    const richesse = E.tresor[i] / Math.max(pibJour, 0.01);

    // 1. Ajuster la fiscalité si le budget dérape
    if (E.dernierBilan[i] < -pibJour * 0.06) {
      E.tIR[i] = clamp(E.tIR[i] + 0.004, 0.02, 0.55);
      E.tTVA[i] = clamp(E.tTVA[i] + 0.003, 0.02, 0.32);
    } else if (E.dernierBilan[i] > pibJour * 0.08 && E.approb[i] < 55) {
      E.tIR[i] = clamp(E.tIR[i] - 0.004, 0.02, 0.55);
    }

    // 1 bis. Quand la dette dérape, on serre les dépenses ; au-delà de trois fois
    //        le PIB, on restructure — avec les conséquences politiques qui vont avec.
    const ratioDette0 = E.dette[i] / Math.max(E.pib[i] * 1000, 1);
    if (ratioDette0 > 1.5) {
      E.bSante[i] *= 0.999; E.bEduc[i] *= 0.999; E.bInfra[i] *= 0.999;
      E.bDef[i] *= 0.999; E.bSub[i] *= 0.998;
      E.tIR[i] = clamp(E.tIR[i] + 0.002, 0.02, 0.55);
      E.tTVA[i] = clamp(E.tTVA[i] + 0.002, 0.02, 0.32);
    }
    if (ratioDette0 > 3) {
      E.dette[i] *= 0.35;
      E.stab[i] -= 18; E.approb[i] -= 14; E.reput[i] -= 12;
      E.tresor[i] = Math.max(E.tresor[i], pibJour * 5);
      journal('🏦', `${G.PAYS[i].drapeau} ${G.PAYS[i].nom} fait défaut et restructure sa dette.`,
              G.relation(E.joueur, i) > 30 ? 'mauvais' : '');
    }

    // 2. Construire : on comble le manque le plus criant
    const maxCh = clamp(2 + Math.log10(Math.max(E.pib[i], 10)) * 1.7, 2, 11) | 0;
    if (nbChantiers(i) < maxCh) {
      const b = batimentPrioritaire(i);
      if (b >= 0) {
        const bd = G.BAT[b];
        const lourd = bd.cat === 'energie' || b === B.ferme;
        const lot = clamp(Math.round(E.pib[i] / 1500), 1, lourd ? 2 : 6);
        const cout = coutBatiment(i, b) * lot;
        const ratioDette = E.dette[i] / Math.max(E.pib[i] * 1000, 1);
        const comptant = E.tresor[i] > cout * 1.6;
        const aCredit = !comptant && ratioDette < 1.0 && cout < pibJour * 30;
        if (comptant || aCredit) {
          if (comptant) E.tresor[i] -= cout; else E.dette[i] += cout * 1.02;
          const duree = Math.ceil(bd.jours * (1.4 - E.infra[i] / 220));
          for (let n = 0; n < lot; n++)
            E.chantiers.push({ p: i, b: b, reste: duree, total: bd.jours });
        }
      }
    }

    // 3. Armée : réagir à la menace
    const menace = menacePercue(i);
    if (richesse > 14 && menace > 0.6 && E.casernes.filter(c => c.p === i).length < 3) {
      const u = uniteSouhaitee(i);
      const ud = G.UNI[u], lot = Math.max(1, Math.round(E.pib[i] / 900));
      const cout = ud.cout * lot;
      if (E.tresor[i] > cout * 2.2) {
        E.tresor[i] -= cout;
        E.casernes.push({ p: i, u: u, n: lot, reste: ud.jours });
      }
    }

    // 4. Commerce : proposer un contrat quand un excédent durable existe
    if (Math.random() < 0.08) proposerContratIA(i);

    // 5. Diplomatie et guerre
    if (Math.random() < 0.02) {
      let pire = -1, pireV = -35;
      for (let j = 0; j < N; j++) if (j !== i && E.rel[i * N + j] < pireV) { pireV = E.rel[i * N + j]; pire = j; }
      if (pire >= 0 && !enGuerre(i) && !enGuerre(pire)) {
        const rapport = puissance(i, true) / (puissance(pire, false) + 1);
        const dissuade = E.uni[pire * NUNI + U.ogive] > 0 && E.uni[i * NUNI + U.ogive] === 0;
        const allie = estAllie(i, pire);
        const voisin = distance(G.PAYS[i], G.PAYS[pire]) < 4200;
        if (rapport > 1.9 && !dissuade && !allie && voisin && E.stab[i] > 40 && Math.random() < 0.25) {
          declarerGuerre(i, pire);
        }
      }
    }
    if (Math.random() < 0.03) {
      const j = (Math.random() * N) | 0;
      if (j !== i && E.rel[i * N + j] > 30 && !estAllie(i, j) && Math.random() < 0.1)
        E.alliances.push([i, j]);
    }
  }

  function nbChantiers(i) {
    let n = 0;
    for (let k = 0; k < E.chantiers.length; k++) if (E.chantiers[k].p === i) n++;
    return n;
  }

  function batimentPrioritaire(i) {
    const base = i * NRES;
    const ratio = r => E.prod[base + r] / Math.max(E.conso[base + r], 1e-6);
    const px = r => E.prix[r] / E.prixBase[r];
    const d = G.PAYS[i].dot;
    const cand = [];
    const besoin = (r, seuil, poids) => {
      const x = ratio(r);
      if (x < seuil) cand.push([null, (seuil - x) * poids, r]);
      return x;
    };

    // 1. Couvrir les besoins vitaux, sans surconstruire
    const rNour = ratio(R.nourriture), rElec = ratio(R.electricite), rBiens = ratio(R.biens);
    if (rNour < 1.06) cand.push([B.ferme, (1.06 - rNour) * 4.5]);
    if (rElec < 1.10) {
      const choix = E.tech[i] > 62 && E.tresor[i] > 14000 ? B.nucleaire
                  : d[1] >= 3 ? B.cycle : d[2] >= 3 ? B.thermique : B.solaire;
      cand.push([choix, (1.10 - rElec) * 4.5]);
    }
    if (rBiens < 1.05) cand.push([B.usine, (1.05 - rBiens) * 3.2]);

    // 2. Exploiter le sous-sol quand le marché mondial le paye cher
    const mines = [[0, B.puits, R.petrole], [1, B.gaziere, R.gaz], [2, B.houillere, R.charbon],
                   [3, B.minefer, R.fer], [4, B.minecuivre, R.cuivre], [5, B.mineterres, R.terresrares],
                   [6, B.mineuran, R.uranium], [7, B.mineor, R.or]];
    mines.forEach(m => {
      if (d[m[0]] < 2) return;
      const bd = G.BAT[m[1]];
      if (bd.tech && E.tech[i] < bd.tech) return;
      const rentable = px(m[2]);
      const manqueLocal = Math.max(0, 1 - ratio(m[2]));
      cand.push([m[1], d[m[0]] * 0.09 * rentable + manqueLocal * 1.2]);
    });

    // 3. Course à l'IA, proportionnée au poids économique
    if (E.tech[i] > 70) cand.push([B.datacenter, 0.5 + Math.log10(Math.max(E.pib[i], 10)) * 0.55]);
    if (E.tech[i] > 82 && E.pib[i] > 500) cand.push([B.fonderie, 0.4 + Math.log10(E.pib[i]) * 0.35]);

    // 4. Services publics
    if (E.educ[i] < 62) cand.push([B.universite, (62 - E.educ[i]) * 0.02]);
    if (E.sante[i] < 58) cand.push([B.hopital, (58 - E.sante[i]) * 0.02]);
    if (E.infra[i] < 62) cand.push([B.route, (62 - E.infra[i]) * 0.022]);
    if (E.expCap[i] < 6 + E.pib[i] / 400) cand.push([B.port, 0.45]);
    cand.push([B.labo, 0.40]);

    const utiles = cand.filter(c => c[0] !== null && c[1] > 0);
    if (!utiles.length) return -1;
    utiles.sort((a, b) => b[1] - a[1]);
    return utiles[Math.min((Math.random() * 2) | 0, utiles.length - 1)][0];
  }

  function uniteSouhaitee(i) {
    const t = E.tech[i];
    const opts = [U.infanterie, U.artillerie, U.dca];
    if (t > 45) opts.push(U.helico, U.blindes);
    if (t > 55) opts.push(U.drones, U.drones);
    if (t > 60) opts.push(U.chasse, U.missile);
    if (t > 68) opts.push(U.sousmarin);
    return opts[(Math.random() * opts.length) | 0];
  }

  function menacePercue(i) {
    let m = 0;
    const pi = puissance(i, false) + 1;
    for (let j = 0; j < N; j++) {
      if (j === i) continue;
      const rel = E.rel[i * N + j];
      if (rel > -15) continue;
      if (distance(G.PAYS[i], G.PAYS[j]) > 5000) continue;
      m += (puissance(j, true) / pi) * (-rel / 100);
    }
    return m;
  }
  G.menacePercue = menacePercue;

  function proposerContratIA(i) {
    const base = i * NRES;
    for (let r = 0; r < NRES; r++) {
      const surplus = E.prod[base + r] - E.conso[base + r];
      if (surplus < E.conso[base + r] * 0.15 || surplus <= 0) continue;
      let meilleur = -1, meilleurScore = 0;
      for (let j = 0; j < N; j++) {
        if (j === i) continue;
        const dj = j * NRES + r;
        const besoin = E.conso[dj] - E.prod[dj];
        if (besoin <= 0) continue;
        const s = besoin * (100 + E.rel[i * N + j]) / 100;
        if (s > meilleurScore) { meilleurScore = s; meilleur = j; }
      }
      if (meilleur >= 0 && !E.contrats.some(c => c.v === i && c.a === meilleur && c.r === r)) {
        if (meilleur === E.joueur) {
          // Offre soumise au joueur
          E.offres = E.offres || [];
          if (E.offres.length < 6)
            E.offres.push({ v: i, a: meilleur, r: r, qte: Math.min(surplus * 0.5, (E.conso[meilleur * NRES + r] - E.prod[meilleur * NRES + r]) * 0.9),
                            prix: E.prix[r] * (0.94 + Math.random() * 0.16), jours: 365 * (1 + ((Math.random() * 3) | 0)) });
        } else {
          E.contrats.push({ v: i, a: meilleur, r: r,
                            qte: Math.min(surplus * 0.5, (E.conso[meilleur * NRES + r] - E.prod[meilleur * NRES + r]) * 0.9),
                            prix: E.prix[r] * 0.99, jours: 365 * (1 + ((Math.random() * 3) | 0)), id: E.idContrat++ });
          modifierRelation(i, meilleur, 2);
        }
        return;
      }
    }
  }

  // ───────────────────────────────────────────────────────────── Actions joueur
  G.coutBatiment = coutBatiment;
  function coutBatiment(i, b) {
    const n = E.bat[i * NBAT + b] + E.chantiers.filter(c => c.p === i && c.b === b).length;
    return G.BAT[b].cout * (1 + n * 0.012) * (1 + E.inflation[i] / 260);
  }

  // Marge d'endettement encore disponible, en M$.
  G.capaciteEmprunt = function (i) {
    const plafond = E.pib[i] * 1000 * 1.5;
    return Math.max(0, plafond - E.dette[i]);
  };

  G.construire = function (i, b, aCredit) {
    const bd = G.BAT[b];
    if (bd.tech && E.tech[i] < bd.tech) return { ok: false, msg: `Technologie insuffisante : niveau ${bd.tech} requis, vous êtes à ${E.tech[i].toFixed(0)}.` };
    if (bd.dot !== undefined && G.PAYS[i].dot[bd.dot] < 1) return { ok: false, msg: `Votre sous-sol ne contient pas de ${G.RES[R[Object.keys(bd.prod)[0]]].nom.toLowerCase()}.` };
    const cout = coutBatiment(i, b);
    const manque = cout - E.tresor[i];
    if (manque > 0) {
      if (!aCredit) return { ok: false, msg: `Il vous manque ${manque.toFixed(0)} M$. Empruntez, ou attendez que le trésor se remplisse.` };
      if (manque > G.capaciteEmprunt(i))
        return { ok: false, msg: 'Les marchés refusent de vous prêter davantage : votre dette atteint 150 % du PIB.' };
      E.dette[i] += manque * 1.02;
      E.tresor[i] += manque;
    }
    E.tresor[i] -= cout;
    E.chantiers.push({ p: i, b: b, reste: Math.max(5, Math.ceil(bd.jours * (1.4 - E.infra[i] / 220))), total: bd.jours });
    return { ok: true, msg: manque > 0
      ? `Chantier lancé : ${bd.nom} (${cout.toFixed(0)} M$, dont ${manque.toFixed(0)} M$ empruntés).`
      : `Chantier lancé : ${bd.nom} (${cout.toFixed(0)} M$).` };
  };

  G.recruter = function (i, u, n) {
    const ud = G.UNI[u];
    if (ud.tech && E.tech[i] < ud.tech) return { ok: false, msg: `Technologie insuffisante (${ud.tech} requis).` };
    if (ud.bat && E.bat[i * NBAT + B[ud.bat]] < 1) return { ok: false, msg: `Nécessite : ${G.BAT[B[ud.bat]].nom}.` };
    const mult = E.lois.has('servicemil') && i === E.joueur ? 0.75 : 1;
    const cout = ud.cout * n * mult;
    const manque = cout - E.tresor[i];
    if (manque > 0) {
      if (manque > G.capaciteEmprunt(i))
        return { ok: false, msg: `Il vous manque ${manque.toFixed(0)} M$ et les marchés ne vous prêtent plus.` };
      E.dette[i] += manque * 1.02; E.tresor[i] += manque;
    }
    E.tresor[i] -= cout;
    E.casernes.push({ p: i, u: u, n: n, reste: Math.ceil(ud.jours * mult) });
    return { ok: true, msg: `${n} × ${ud.nom} en formation (${cout.toFixed(0)} M$).` };
  };

  G.declarerGuerre = declarerGuerre;
  function declarerGuerre(a, d) {
    if (enGuerre(a) || enGuerre(d)) return { ok: false, msg: 'Un des deux pays est déjà en guerre.' };
    E.guerres.push({ a: a, d: d, front: 0, jour: E.jour, jours: 0, mortsA: 0, mortsD: 0 });
    modifierRelation(a, d, -80);
    E.reput[a] -= 18;
    for (let j = 0; j < N; j++) {
      if (j === a || j === d) continue;
      if (E.rel[j * N + d] > 25) modifierRelation(a, j, -14);
    }
    // Les alliés du défenseur peuvent entrer en guerre
    E.alliances.forEach(al => {
      const allie = al[0] === d ? al[1] : al[1] === d ? al[0] : -1;
      if (allie >= 0 && allie !== a && !enGuerre(allie) && Math.random() < 0.45) {
        E.guerres.push({ a: allie, d: a, front: 0, jour: E.jour, jours: 0, mortsA: 0, mortsD: 0 });
        journal('⚔️', `${G.PAYS[allie].nom} honore son alliance et déclare la guerre à ${G.PAYS[a].nom}.`, 'important');
      }
    });
    journal('⚔️', `${G.PAYS[a].nom} déclare la guerre à ${G.PAYS[d].nom}.`,
            (a === E.joueur || d === E.joueur) ? 'important' : '');
    return { ok: true, msg: 'La guerre est déclarée.' };
  }

  G.frappeNucleaire = function (a, d) {
    if (E.uni[a * NUNI + U.ogive] < 1) return { ok: false, msg: 'Aucune ogive disponible.' };
    E.uni[a * NUNI + U.ogive]--;
    const morts = E.pop[d] * 0.035;
    E.pop[d] -= morts;
    E.pib[d] *= 0.72; E.stab[d] -= 30; E.approb[d] -= 20; E.moral[d] -= 25;
    for (let b = 0; b < NBAT; b++) E.bat[d * NBAT + b] = Math.floor(E.bat[d * NBAT + b] * 0.75);
    for (let u = 0; u < NUNI; u++) if (u !== U.ogive) E.uni[d * NUNI + u] *= 0.7;
    E.reput[a] = clamp(E.reput[a] - 60, 0, 100);
    for (let j = 0; j < N; j++) if (j !== a) modifierRelation(a, j, -45);
    E.approb[a] -= 12;
    journal('☢️', `Frappe nucléaire sur ${G.PAYS[d].nom} : ${(morts / 1e6).toFixed(1)} millions de morts. Le monde ne l'oubliera pas.`, 'mauvais');
    // Riposte
    if (E.uni[d * NUNI + U.ogive] > 0) {
      setTimeout(() => G.frappeNucleaire(d, a), 0);
    }
    return { ok: true, msg: 'Frappe exécutée.' };
  };

  G.meilleursAcheteurs = function (r, n) {
    const l = [];
    for (let j = 0; j < N; j++) {
      if (j === E.joueur) continue;
      const besoin = E.conso[j * NRES + r] - E.prod[j * NRES + r];
      if (besoin <= 0) continue;
      l.push({ j: j, qte: besoin, rel: E.rel[E.joueur * N + j] });
    }
    l.sort((x, y) => y.qte * (120 + y.rel) - x.qte * (120 + x.rel));
    return l.slice(0, n || 6);
  };

  G.meilleursVendeurs = function (r, n) {
    const l = [];
    for (let j = 0; j < N; j++) {
      if (j === E.joueur) continue;
      const surplus = E.prod[j * NRES + r] - E.conso[j * NRES + r];
      if (surplus <= 0) continue;
      l.push({ j: j, qte: surplus, rel: E.rel[E.joueur * N + j] });
    }
    l.sort((x, y) => y.qte * (120 + y.rel) - x.qte * (120 + x.rel));
    return l.slice(0, n || 6);
  };

  G.proposerContrat = function (v, a, r, qte, prix, jours) {
    const px = E.prix[r];
    const rel = E.rel[a * N + v];
    // L'acheteur juge : prix relatif, besoin réel, relations, sanctions
    const dj = a * NRES + r;
    const besoin = Math.max(0, E.conso[dj] - E.prod[dj]);
    const attrait = (px / prix - 1) * 100 + rel * 0.4 + (besoin > qte ? 22 : besoin > qte * 0.4 ? 8 : -18)
                    - (E.sanctions.some(s => s[0] === a && s[1] === v) ? 60 : 0);
    if (attrait < 5) return { ok: false, msg: `Refus : ${nomRefus(r, a, px, prix, besoin, qte, rel)}` };
    E.contrats.push({ v: v, a: a, r: r, qte: qte, prix: prix, jours: jours, id: E.idContrat++ });
    modifierRelation(v, a, 6);
    return { ok: true, msg: `${G.PAYS[a].nom} signe le contrat.` };
  };

  function nomRefus(r, a, px, prix, besoin, qte, rel) {
    if (besoin < qte * 0.4) {
      const autres = G.meilleursAcheteurs(r, 3).map(x => G.PAYS[x.j].nom);
      const piste = autres.length ? ` En revanche, ${autres.join(', ')} en manquent.` : '';
      return `${G.PAYS[a].nom} produit déjà assez de ${G.RES[r].nom.toLowerCase()}.${piste}`;
    }
    if (prix > px * 1.15) return `votre prix (${prix.toFixed(0)} $) dépasse trop le marché (${px.toFixed(0)} $).`;
    if (rel < 0) return `les relations avec ${G.PAYS[a].nom} sont trop mauvaises (${rel}).`;
    return 'les conditions ne les convainquent pas — baissez le prix ou améliorez vos relations.';
  }

  G.actionDiplo = function (i, j, type, montant) {
    switch (type) {
      case 'ambassade':
        if (E.tresor[i] < 120) return { ok: false, msg: 'Trésor insuffisant (120 M$).' };
        E.tresor[i] -= 120; modifierRelation(i, j, 10);
        return { ok: true, msg: `Ambassade ouverte à ${G.PAYS[j].nom}. Relations +10.` };
      case 'aide': {
        const m = montant || 500;
        if (E.tresor[i] < m) return { ok: false, msg: 'Trésor insuffisant.' };
        E.tresor[i] -= m; E.tresor[j] += m;
        const gain = clamp(m / Math.max(E.pib[j] * 1.2, 20), 1, 30);
        modifierRelation(i, j, gain); E.reput[i] = clamp(E.reput[i] + gain * 0.2, 0, 100);
        return { ok: true, msg: `${m} M$ versés. Relations +${gain.toFixed(0)}.` };
      }
      case 'pacte':
        if (E.rel[i * N + j] < 25) return { ok: false, msg: 'Relations trop faibles (25 requis).' };
        if (E.pactes.some(p => (p[0] === i && p[1] === j) || (p[0] === j && p[1] === i)))
          return { ok: false, msg: 'Pacte déjà en vigueur.' };
        E.pactes.push([i, j]); modifierRelation(i, j, 12);
        return { ok: true, msg: 'Pacte de non-agression signé.' };
      case 'alliance': {
        if (E.rel[i * N + j] < 55) return { ok: false, msg: 'Relations trop faibles (55 requis).' };
        if (estAllie(i, j)) return { ok: false, msg: 'Alliance déjà conclue.' };
        const interet = puissance(i, true) / (puissance(j, true) + 1);
        if (interet < 0.25 && E.rel[i * N + j] < 75) return { ok: false, msg: `${G.PAYS[j].nom} ne voit pas son intérêt dans cette alliance.` };
        E.alliances.push([i, j]); modifierRelation(i, j, 18);
        return { ok: true, msg: `Alliance militaire avec ${G.PAYS[j].nom}.` };
      }
      case 'sanction':
        if (E.sanctions.some(s => s[0] === i && s[1] === j)) return { ok: false, msg: 'Sanctions déjà en place.' };
        E.sanctions.push([i, j]); modifierRelation(i, j, -25);
        E.contrats = E.contrats.filter(c => !((c.v === i && c.a === j) || (c.v === j && c.a === i)));
        return { ok: true, msg: `Sanctions décrétées contre ${G.PAYS[j].nom}. Vos contrats avec eux sont annulés.` };
      case 'leversanction': {
        const k = E.sanctions.findIndex(s => s[0] === i && s[1] === j);
        if (k < 0) return { ok: false, msg: 'Aucune sanction en cours.' };
        E.sanctions.splice(k, 1); modifierRelation(i, j, 12);
        return { ok: true, msg: 'Sanctions levées.' };
      }
      case 'espion': {
        const cout = 250;
        if (E.tresor[i] < cout) return { ok: false, msg: 'Trésor insuffisant (250 M$).' };
        E.tresor[i] -= cout;
        const chance = clamp(0.30 + (aTech(i, 'cyber') ? 0.28 : 0) + (E.ia[i] | 0) * 0.035 - E.tech[j] / 400, 0.05, 0.92);
        if (Math.random() > chance) {
          modifierRelation(i, j, -18); E.reput[i] -= 6;
          return { ok: false, msg: 'Opération éventée. Scandale diplomatique, relations −18.' };
        }
        const NT = G.TECHS.length;
        for (let k = 0; k < NT; k++) {
          if (E.techs[j * NT + k] && !E.techs[i * NT + k] && G.TECHS[k].req.every(r => aTech(i, r))) {
            E.techs[i * NT + k] = 1; E.tech[i] = clamp(E.tech[i] + 1.2, 0, 100);
            return { ok: true, msg: `Technologie dérobée : ${G.TECHS[k].nom}.` };
          }
        }
        E.stab[j] -= 4;
        return { ok: true, msg: `Sabotage réussi : la stabilité de ${G.PAYS[j].nom} recule.` };
      }
    }
    return { ok: false, msg: 'Action inconnue.' };
  };

  // ───────────────────────────────────────────────────────────── ONU
  const SUJETS = [
    { id:'embargo',  txt:'Embargo sur les armes à destination des zones de conflit', pour:'+réputation, −ventes d\'armes', effet:(v)=>{ if(v)E.reput[E.joueur]+=4; } },
    { id:'climat',   txt:'Traité climatique contraignant',                            pour:'+approbation, −rendement du charbon', effet:(v)=>{ if(v){E.approb[E.joueur]+=3;} } },
    { id:'ia',       txt:'Moratoire international sur les IA de pointe',              pour:'−calcul mondial, −risque d\'accident', effet:(v)=>{ if(v){ for(let i=0;i<N;i++) E.calcul[i]*=0.97; } } },
    { id:'nuke',     txt:'Interdiction des essais nucléaires',                        pour:'+réputation des signataires',   effet:(v)=>{ if(v)E.reput[E.joueur]+=6; } },
    { id:'commerce', txt:'Zone de libre-échange élargie',                             pour:'+commerce, −douanes',           effet:(v)=>{ if(v){ for(let i=0;i<N;i++) E.tDou[i]*=0.9; } } },
    { id:'aide',     txt:'Fonds mondial pour les pays les plus pauvres',              pour:'−trésor des riches, +stabilité mondiale', effet:(v)=>{ if(v){ for(let i=0;i<N;i++) if(E.pib[i]>800) E.tresor[i]*=0.98; } } }
  ];

  function onu() {
    if (E.onu || E.jour % 180 !== 90) return;
    const s = SUJETS[(Math.random() * SUJETS.length) | 0];
    E.onu = { sujet: s, jours: 20, pour: 0, contre: 0 };
    journal('🕊️', `Assemblée générale : ${s.txt}. Votre vote est attendu.`, 'important');
  }

  G.voterONU = function (pour) {
    if (!E.onu) return;
    let p = 0, c = 0;
    for (let i = 0; i < N; i++) {
      if (i === E.joueur) continue;
      const enclin = (E.rel[E.joueur * N + i] * 0.3 + (E.tech[i] > 60 ? 12 : -8) + (Math.random() - 0.5) * 60) > 0;
      if (enclin) p++; else c++;
      if (enclin === pour) modifierRelation(E.joueur, i, 1);
      else modifierRelation(E.joueur, i, -1);
    }
    if (pour) p++; else c++;
    const adopte = p > c;
    if (adopte) E.onu.sujet.effet(pour);
    journal('🗳️', `Résolution « ${E.onu.sujet.txt} » ${adopte ? 'adoptée' : 'rejetée'} (${p} pour / ${c} contre).`, adopte === pour ? 'bon' : '');
    E.onu = null;
  };

  // ───────────────────────────────────────────────────────────── Événements
  function evenements() {
    if (E.evenement || Math.random() > 0.010) return;
    const dispo = G.EVENEMENTS.filter(e => !e.cond || e.cond(E, E.joueur));
    if (!dispo.length) return;
    E.evenement = dispo[(Math.random() * dispo.length) | 0];
  }

  G.repondreEvenement = function (k) {
    const ev = E.evenement;
    if (!ev) return;
    const msg = ev.choix[k].effet(E, E.joueur);
    journal(ev.icone, `${ev.titre} → ${ev.choix[k].txt}. ${msg || ''}`, 'important');
    E.evenement = null;
  };

  // ───────────────────────────────────────────────────────────── Politique
  function politique() {
    const i = E.joueur, reg = G.PAYS[i].reg;
    if (reg === 'D' && E.jour > 0 && E.jour % 1825 === 0) {
      const score = E.approb[i] + (Math.random() - 0.5) * 12;
      if (score < 45) {
        finPartie('defaite', `Élections perdues avec ${E.approb[i].toFixed(0)} % d'approbation. Le peuple vous a remercié.`);
      } else {
        E.approb[i] = clamp(E.approb[i] + 5, 0, 100);
        journal('🗳️', `Réélu avec ${score.toFixed(0)} % : cinq années de plus pour finir le travail.`, 'bon');
      }
    }
    if (E.stab[i] < 12 && Math.random() < 0.004)
      finPartie('defaite', 'Coup d\'État : l\'armée vous destitue au petit matin.');
    if (E.approb[i] < 8 && Math.random() < 0.003)
      finPartie('defaite', 'Insurrection populaire : le palais est pris, vous fuyez le pays.');
    if (E.pop[i] < 1000)
      finPartie('defaite', 'Votre nation a cessé d\'exister.');
  }

  // Treize défis, du plus accessible au plus lointain. En accomplir un ne met
  // pas fin à la partie : on le note, on félicite, et le jeu continue — il
  // reste toujours quelque chose à viser.
  G.DEFIS = [
    { id:'budget',   icone:'💰', nom:'Comptes en ordre',
      desc:'Dégager un excédent budgétaire tout en gardant plus de 55 % d\'approbation.',
      fait:(E,i) => E.dernierBilan[i] > 0 && E.approb[i] > 55,
      progres:(E,i) => Math.min(1, (E.approb[i] / 55) * (E.dernierBilan[i] > 0 ? 1 : 0.5)) },

    { id:'autonomie',icone:'🌾', nom:'Autonomie vitale',
      desc:'Produire soi-même sa nourriture et son électricité, sans aucune pénurie.',
      fait:(E,i) => E.prod[i*NRES+R.nourriture] >= E.conso[i*NRES+R.nourriture] &&
                    E.prod[i*NRES+R.electricite] >= E.conso[i*NRES+R.electricite],
      progres:(E,i) => Math.min(1, (Math.min(1, E.prod[i*NRES+R.nourriture]/Math.max(E.conso[i*NRES+R.nourriture],1)) +
                                    Math.min(1, E.prod[i*NRES+R.electricite]/Math.max(E.conso[i*NRES+R.electricite],1))) / 2) },

    { id:'dette',    icone:'🏦', nom:'Nation désendettée',
      desc:'Ramener la dette publique sous 20 % du produit intérieur brut.',
      fait:(E,i) => E.dette[i] / Math.max(E.pib[i]*1000,1) < 0.20,
      progres:(E,i) => G.clamp(1 - (E.dette[i]/Math.max(E.pib[i]*1000,1) - 0.20) / 0.8, 0, 1) },

    { id:'savoir',   icone:'🎓', nom:'Nation savante',
      desc:'Porter l\'éducation et la santé au-dessus de 80.',
      fait:(E,i) => E.educ[i] > 80 && E.sante[i] > 80,
      progres:(E,i) => G.clamp((E.educ[i] + E.sante[i]) / 160, 0, 1) },

    { id:'techno',   icone:'🔬', nom:'Toutes les sciences',
      desc:'Acquérir les quinze technologies de l\'arbre de recherche.',
      fait:(E,i) => { for (let k=0;k<NTECH;k++) if (!E.techs[i*NTECH+k]) return false; return true; },
      progres:(E,i) => { let n=0; for (let k=0;k<NTECH;k++) if (E.techs[i*NTECH+k]) n++; return n/NTECH; } },

    { id:'militaire',icone:'⚔️', nom:'Première armée du monde',
      desc:'Détenir la puissance militaire la plus élevée de la planète.',
      fait:(E,i) => { const m = puissance(i,true); for (let j=0;j<N;j++) if (j!==i && puissance(j,true) > m) return false; return true; },
      progres:(E,i) => { const m = puissance(i,true); let max=0; for (let j=0;j<N;j++) if (j!==i) max=Math.max(max,puissance(j,true)); return G.clamp(m/Math.max(max,1),0,1); } },

    { id:'richesse', icone:'💎', nom:'Richesse par habitant',
      desc:'Devenir le pays le plus riche par habitant parmi ceux de plus de dix millions d\'âmes.',
      fait:(E,i) => { if (E.pop[i] < 1e7) return false; const h = E.pib[i]/(E.pop[i]/1e6);
        for (let j=0;j<N;j++) if (j!==i && E.pop[j]>=1e7 && E.pib[j]/(E.pop[j]/1e6) > h) return false; return true; },
      progres:(E,i) => { const h = E.pib[i]/Math.max(E.pop[i]/1e6,0.01); let max=0;
        for (let j=0;j<N;j++) if (j!==i && E.pop[j]>=1e7) max=Math.max(max,E.pib[j]/(E.pop[j]/1e6)); return G.clamp(h/Math.max(max,1),0,1); } },

    { id:'reputation',icone:'🕊️', nom:'Voix qui compte',
      desc:'Atteindre une réputation internationale supérieure à 90.',
      fait:(E,i) => E.reput[i] > 90,
      progres:(E,i) => G.clamp(E.reput[i]/90, 0, 1) },

    { id:'economie', majeur:true, icone:'💵', nom:'Domination économique',
      desc:'Peser plus de 30 % du produit intérieur brut mondial, au premier rang.',
      fait:(E,i) => { let monde=0, rang=1; for (let j=0;j<N;j++){ monde+=E.pib[j]; if (E.pib[j]>E.pib[i]) rang++; }
        return rang===1 && E.pib[i]/Math.max(monde,1) > 0.30; },
      progres:(E,i) => { let monde=0; for (let j=0;j<N;j++) monde+=E.pib[j]; return G.clamp((E.pib[i]/Math.max(monde,1))/0.30,0,1); } },

    { id:'diplomatie',majeur:true, icone:'🤝', nom:'Concert des nations',
      desc:'Nouer quatre-vingt-dix alliances en conservant une réputation supérieure à 80.',
      fait:(E,i) => E.alliances.filter(a => a[0]===i||a[1]===i).length >= 90 && E.reput[i] > 80,
      progres:(E,i) => G.clamp(E.alliances.filter(a => a[0]===i||a[1]===i).length/90, 0, 1) },

    { id:'empire',   majeur:true, icone:'🏛️', nom:'Empire',
      desc:'Annexer quinze nations.',
      fait:(E,i) => (E.annexes ? E.annexes.size : 0) >= 15,
      progres:(E,i) => G.clamp((E.annexes ? E.annexes.size : 0)/15, 0, 1) },

    { id:'prosperite',majeur:true, icone:'🌟', nom:'Prospérité totale',
      desc:'Plus de 92 % d\'approbation, santé et éducation au-dessus de 88, chômage sous 4 %.',
      fait:(E,i) => E.approb[i]>92 && E.sante[i]>88 && E.educ[i]>88 && E.chomage[i]<4,
      progres:(E,i) => G.clamp((Math.min(E.approb[i]/92,1)+Math.min(E.sante[i]/88,1)+Math.min(E.educ[i]/88,1)+Math.min(4/Math.max(E.chomage[i],0.5),1))/4,0,1) },

    { id:'agi',      majeur:true, icone:'🧠', nom:'Superintelligence',
      desc:'Atteindre le dernier palier de la course à l\'intelligence artificielle.',
      fait:(E,i) => E.ia[i] >= 10,
      progres:(E,i) => G.clamp(E.calcul[i] / G.PALIERS_IA[10].seuil, 0, 1) }
  ];

  G.defiFait = id => E.defisFaits.indexOf(id) >= 0;

  // silencieux : au premier jour, on enregistre sans fêter les défis que la
  // nation remplit déjà par sa seule situation de départ.
  function verifierDefis(silencieux) {
    if (E.fini) return;
    const i = E.joueur;
    for (let k = 0; k < G.DEFIS.length; k++) {
      const d = G.DEFIS[k];
      if (E.defisFaits.indexOf(d.id) >= 0) continue;
      let ok = false;
      try { ok = d.fait(E, i); } catch (e) { ok = false; }
      if (!ok) continue;
      E.defisFaits.push(d.id);
      if (silencieux) continue;
      journal(d.icone, `Défi accompli : ${d.nom}. ${d.desc}`, 'bon');
      E.defisQueue.push(d);                   // l'interface les fête un par un
    }
  }
  G.amorcerDefis = () => verifierDefis(true);

  function finPartie(type, msg) {
    E.fini = { type: type, msg: msg, jour: E.jour };
    E.pause = true;
    try { localStorage.removeItem('geopolis-save'); } catch (e) { /* stockage bloqué */ }
    journal(type === 'victoire' ? '🏆' : '💀', msg, type === 'victoire' ? 'bon' : 'mauvais');
  }
  G.finPartie = finPartie;

  // ───────────────────────────────────────────────────────────── Journal
  function journal(icone, txt, type) {
    E.journal.unshift({ j: E.jour, d: dateTexte(), icone: icone, txt: txt, type: type || '' });
    if (E.journal.length > 250) E.journal.length = 250;
    E.nouveauJournal = true;
  }
  G.journal = journal;

  function dateTexte() {
    const d = new Date(2026, 0, 1 + E.jour);
    return d.toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });
  }
  G.dateTexte = dateTexte;
  G.dateDe = j => new Date(2026, 0, 1 + j).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short', year: 'numeric' });

  // ───────────────────────────────────────────────────────────── Tour de jeu
  G.tick = function () {
    if (E.fini) return;
    E.jour++;
    calculerFlux();
    marche();
    economie();
    societe();
    recherche();
    chantiers();
    guerres();
    cerveaux();
    derive();
    onu();
    if (E.onu && --E.onu.jours <= 0) { G.voterONU(Math.random() < 0.5); }
    evenements();
    politique();
    if (E.jour % 15 === 0) verifierDefis();
    E.score = calculScore();
  };

  function calculScore() {
    const i = E.joueur;
    return Math.round(
      E.pib[i] * 0.5 +
      E.approb[i] * 40 +
      E.tech[i] * 60 +
      (E.ia[i] | 0) * 900 +
      E.reput[i] * 20 +
      (E.alliances.filter(a => a[0] === i || a[1] === i).length) * 60 +
      E.defisFaits.length * 1500 -
      E.dette[i] * 0.02
    );
  }

  // ───────────────────────────────────────────────────────────── Sauvegarde
  G.sauver = function () {
    const brut = {};
    ['pop','pib','croiss','tresor','dette','tech','stab','approb','corrupt','chomage','inflation',
     'educ','sante','infra','expCap','milcap','moral','rech','calcul','ia','reput','dernierBilan',
     'tIR','tIS','tTVA','tDou','bSante','bEduc','bInfra','bDef','bSub','prix','prixBase','calib',
     'bat','uni','stock','rel','techs','rechCours','rechAcc'
    ].forEach(k => { brut[k] = Array.from(E[k]); });
    return JSON.stringify({
      v: 1, joueur: E.joueur, jour: E.jour, difficulte: E.difficulte, brut: brut,
      chantiers: E.chantiers, casernes: E.casernes, contrats: E.contrats, guerres: E.guerres,
      alliances: E.alliances, pactes: E.pactes, sanctions: E.sanctions,
      lois: Array.from(E.lois), defisFaits: E.defisFaits,
      journal: E.journal.slice(0, 60), idContrat: E.idContrat,
      annexes: E.annexes ? Array.from(E.annexes) : [], fini: E.fini, score: E.score
    });
  };

  G.charger = function (txt) {
    const s = JSON.parse(txt);
    G.nouvellePartie(G.PAYS[s.joueur].code, s.difficulte);
    for (const k in s.brut) {
      const src = s.brut[k], dst = E[k];
      for (let n = 0; n < src.length && n < dst.length; n++) dst[n] = src[n];
    }
    E.jour = s.jour; E.chantiers = s.chantiers; E.casernes = s.casernes;
    E.contrats = s.contrats; E.guerres = s.guerres; E.alliances = s.alliances;
    E.pactes = s.pactes; E.sanctions = s.sanctions; E.lois = new Set(s.lois);
    E.journal = s.journal; E.idContrat = s.idContrat; E.fini = s.fini; E.score = s.score || 0;
    E.defisFaits = s.defisFaits || []; E.defisQueue = [];
    E.annexes = new Set(s.annexes || []);
    E.pause = true;
    return E;
  };
})(window.GEO = window.GEO || {});
