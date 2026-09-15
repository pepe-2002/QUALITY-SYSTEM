/* GÉOPOLIS — Interface
 * Chaque panneau se construit une fois puis se met à jour en n'écrivant que
 * du texte dans des nœuds mémorisés : pas de reconstruction du DOM à chaque
 * image, donc pas de saccade même à vitesse ×20 avec 197 nations simulées.
 */
(function (G) {
  'use strict';

  const E = G.E, R = G.R, B = G.B, U = G.U;
  const q = s => document.querySelector(s);
  const clamp = G.clamp;

  // ── Formatage ─────────────────────────────────────────────────────────────
  const nf0 = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });
  const nf1 = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 1 });
  const nf2 = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 2 });

  G.fmtNb = v => Math.abs(v) >= 100 ? nf0.format(v) : Math.abs(v) >= 10 ? nf1.format(v) : nf2.format(v);
  G.fmtMd = v => v >= 1000 ? nf1.format(v / 1000) + ' T$' : nf0.format(v) + ' Md$';
  G.fmtM = v => Math.abs(v) >= 1e6 ? nf2.format(v / 1e6) + ' T$'
              : Math.abs(v) >= 1000 ? nf1.format(v / 1000) + ' Md$'
              : nf0.format(v) + ' M$';
  G.fmtPop = v => v >= 1e9 ? nf2.format(v / 1e9) + ' Md' : v >= 1e6 ? nf1.format(v / 1e6) + ' M' : nf0.format(v / 1e3) + ' k';
  const pct = v => (v >= 0 ? '+' : '') + nf1.format(v) + ' %';
  const el = (t, c, x) => { const n = document.createElement(t); if (c) n.className = c; if (x !== undefined) n.textContent = x; return n; };
  const sig = v => v > 0 ? 'bon' : v < 0 ? 'mauvais' : '';

  // ── Rattrapage des tapes ──────────────────────────────────────────────────
  // Sur écran tactile, la séquence touchstart / pointerup / touchend n'est pas
  // toujours suivie du clic que le navigateur est censé synthétiser. Résultat :
  // taper sur une nation ne la sélectionnait pas, et rien ne réagissait au
  // doigt. On déclenche donc le clic nous-mêmes quand il n'arrive pas.
  (function rattraperTapes() {
    const CIBLES = 'button, .acc-c, .lp, .sugg-p, .onglet, .btn, .btn-ic';
    let cible = null, debut = 0, depX = 0, depY = 0, dernierClic = 0;

    document.addEventListener('click', () => { dernierClic = Date.now(); }, true);

    document.addEventListener('touchstart', e => {
      const t = e.touches[0];
      cible = (e.target.closest && e.target.closest(CIBLES)) || null;
      debut = Date.now();
      if (t) { depX = t.clientX; depY = t.clientY; }
    }, true);

    document.addEventListener('touchend', e => {
      const c = cible; cible = null;
      if (!c || Date.now() - debut > 600) return;
      const t = e.changedTouches && e.changedTouches[0];
      if (t && (Math.abs(t.clientX - depX) > 12 || Math.abs(t.clientY - depY) > 12)) return;
      const avant = dernierClic;
      setTimeout(() => {
        if (dernierClic !== avant) return;            // le navigateur a fait le travail
        if (!document.contains(c) || c.disabled) return;
        c.click();
      }, 120);
    }, true);
  })();

  // ── Hauteur de la scène ───────────────────────────────────────────────────
  // Le jeu occupe tout l'écran en position fixe. Dans une page publiée, il est
  // affiché dans un cadre dont l'hôte règle la hauteur sur celle du contenu —
  // or un élément en position fixe ne compte pas comme contenu. Le cadre restait
  // donc bloqué à sa hauteur initiale (400 px), la liste des nations passait
  // hors champ et plus rien n'était cliquable. On impose donc une hauteur
  // explicite en pixels : le contenu mesure alors exactement ce qu'il occupe, et
  // le cadre s'y accorde du premier coup.
  G.ajusterHauteur = function () {
    let h;
    if (window === window.top) {
      h = window.innerHeight;
    } else {
      // Dans un cadre, innerHeight vaut ce que l'hôte a décidé : s'en servir
      // reviendrait à se mordre la queue. L'écran physique, lui, est fiable.
      // On laisse de la place à l'habillage de la page hôte, sinon la barre de
      // commandes du bas tombe sous le bord visible du téléphone.
      const ecran = (window.screen && window.screen.height) || 800;
      h = clamp(Math.round(ecran - 250), 480, 900);
    }
    if (h === UI.hauteur) return;
    UI.hauteur = h;
    document.documentElement.style.height = h + 'px';
    document.body.style.height = h + 'px';
    if (UI.carteInstallee) G.redimensionnerCarte();
  };

  // ── État de l'interface ───────────────────────────────────────────────────
  const UI = G.UI = { panneau: 'carte', paysVise: -1, refs: {}, construits: {}, dernierMaj: 0, hauteur: 0 };
  let boucle = null, tempsAccum = 0, dernierTemps = 0;

  const VITESSES = { 1: 700, 2: 340, 3: 150, 4: 45 };   // ms par jour de jeu

  // ══════════════════════════════════════════════════════ Démarrage
  G.demarrer = function () {
    G.ajusterHauteur();
    q('#accueil').classList.add('cache');
    q('#jeu').classList.remove('cache');
    construireNav();
    if (!UI.carteInstallee) {
      G.initCarte(q('#carte'), p => { UI.paysVise = p; if (UI.panneau === 'diplomatie') majDiplo(true); });
      UI.carteInstallee = true;
    } else {
      G.redimensionnerCarte();
    }
    UI.enJeu = true;
    UI.dernierAuto = -1;
    ouvrir('carte');
    G.vueInitiale(E.joueur);
    majBarre();
    dernierTemps = performance.now();
    tempsAccum = 0;
    if (!boucle) boucle = requestAnimationFrame(tourner);
    if (!UI.clavierInstalle) { window.addEventListener('keydown', clavier); UI.clavierInstalle = true; }
  };

  function clavier(e) {
    if (!UI.enJeu) return;
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
    if (e.code === 'Space') { e.preventDefault(); basculerPause(); }
    if (e.key >= '1' && e.key <= '4') { E.pause = false; E.vitesse = +e.key; majVitesse(); }
    const raccourcis = { c:'carte', n:'nation', e:'economie', r:'ressources', b:'construction',
                         m:'commerce', d:'diplomatie', a:'armee', i:'ia', s:'recherche',
                         p:'politique', f:'defis', l:'classements', j:'journal' };
    if (raccourcis[e.key]) ouvrir(raccourcis[e.key]);
  }

  // ══════════════════════════════════════════════════════ Boucle principale
  function tourner(t) {
    const dt = Math.min(t - dernierTemps, 400);
    dernierTemps = t;
    if (!UI.enJeu) { boucle = requestAnimationFrame(tourner); return; }
    if (!E.pause && !E.fini && !E.evenement && !E.capitulation) {
      tempsAccum += dt;
      const pas = VITESSES[E.vitesse];
      let n = 0;
      while (tempsAccum >= pas && n < 40) { G.tick(); tempsAccum -= pas; n++; }
      if (E.evenement || E.capitulation || E.fini) { E.pause = true; tempsAccum = 0; }
    }
    if (t - UI.dernierMaj > 120) {
      UI.dernierMaj = t;
      majBarre();
      const p = PANNEAUX[UI.panneau];
      if (p && p.maj) p.maj();
      if (UI.panneau === 'carte') G.dessinerCarte();
      if (E.evenement && !q('#modale').classList.contains('ouvert')) modaleEvenement();
      if (E.capitulation && !q('#modale').classList.contains('ouvert')) modaleCapitulation();
      if (E.onu && !E.onu.montre) { E.onu.montre = true; modaleONU(); }
      if (E.defisQueue.length && !q('#modale').classList.contains('ouvert')) modaleDefi();
      if (E.fini && !q('#modale').classList.contains('ouvert')) modaleFin();
      if (E.nouveauJournal) { E.nouveauJournal = false; pastilleJournal(); }
      if (E.jour > 0 && E.jour !== UI.dernierAuto && E.jour % 30 === 0 && !E.fini) {
        UI.dernierAuto = E.jour;
        G.sauverLocal(true);
      }
    }
    boucle = requestAnimationFrame(tourner);
  }

  G.confirmer = function (titre, texte, onOui, libelleOui) {
    modale(`<div class="mo-i">⚠️</div><h2>${titre}</h2><p>${texte}</p>`,
      [[libelleOui || 'Confirmer', onOui, 'danger'], ['Annuler', () => {}, 'sec']]);
  };

  G.retourAccueil = function () {
    UI.enJeu = false;
    E.pause = true;
    E.fini = null; E.evenement = null; E.capitulation = null; E.onu = null;
    tempsAccum = 0;
    q('#modale').classList.remove('ouvert');
    q('#modale').innerHTML = '';
    q('#jeu').classList.add('cache');
    q('#accueil').classList.remove('cache');
    q('#contenu').innerHTML = '';
    UI.construits = {}; UI.refs = {}; UI.paysVise = -1;
    G.carte.choisi = -1; G.carte.survol = -1; G.carte.zoom = 1; G.carte.ox = 0; G.carte.oy = 0;
    document.title = 'GÉOPOLIS — Simulateur de Président';
    if (G.rafraichirAccueil) G.rafraichirAccueil();
  };

  function basculerPause() { E.pause = !E.pause; majVitesse(); }
  function majVitesse() {
    q('#btn-pause').textContent = E.pause ? '▶' : '⏸';
    document.querySelectorAll('.vit').forEach(b => b.classList.toggle('actif', !E.pause && +b.dataset.v === E.vitesse));
  }

  // ══════════════════════════════════════════════════════ Barre supérieure
  function majBarre() {
    const i = E.joueur, r = UI.refs;
    if (!r.date) {
      r.date = q('#b-date'); r.tresor = q('#b-tresor'); r.pib = q('#b-pib');
      r.croiss = q('#b-croiss'); r.approb = q('#b-approb'); r.ia = q('#b-ia');
      r.solde = q('#b-solde'); r.score = q('#b-score');
    }
    r.date.textContent = G.dateTexte();
    r.tresor.textContent = G.fmtM(E.tresor[i]);
    r.solde.textContent = (E.dernierBilan[i] >= 0 ? '+' : '') + G.fmtM(E.dernierBilan[i]) + '/j';
    r.solde.className = 'sous ' + sig(E.dernierBilan[i]);
    r.pib.textContent = G.fmtMd(E.pib[i]);
    r.croiss.textContent = pct(E.croiss[i]);
    r.croiss.className = 'sous ' + sig(E.croiss[i] - 0.5);
    r.approb.textContent = nf0.format(E.approb[i]) + ' %';
    r.approb.className = 'val ' + (E.approb[i] > 55 ? 'bon' : E.approb[i] < 35 ? 'mauvais' : '');
    r.ia.textContent = 'N' + (E.ia[i] | 0);
    r.score.textContent = nf0.format(E.score);
  }

  // ══════════════════════════════════════════════════════ Navigation
  const ONGLETS = [
    ['carte', '🗺️', 'Carte', 'c'], ['nation', '🏛️', 'Nation', 'n'],
    ['economie', '💰', 'Économie', 'e'], ['ressources', '⛏️', 'Ressources', 'r'],
    ['construction', '🏗️', 'Construction', 'b'], ['commerce', '📜', 'Commerce', 'm'],
    ['diplomatie', '🤝', 'Diplomatie', 'd'], ['armee', '⚔️', 'Armée', 'a'],
    ['ia', '🧠', 'Course à l\'IA', 'i'], ['recherche', '🔬', 'Recherche', 's'],
    ['politique', '⚖️', 'Politique', 'p'], ['defis', '🎯', 'Défis', 'f'],
    ['classements', '🏆', 'Classements', 'l'],
    ['journal', '📰', 'Journal', 'j']
  ];

  function construireNav() {
    const nav = q('#nav');
    nav.innerHTML = '';
    ONGLETS.forEach(o => {
      const b = el('button', 'onglet');
      b.dataset.p = o[0];
      b.innerHTML = `<span class="ic">${o[1]}</span><span class="lb">${o[2]}</span><span class="kb">${o[3].toUpperCase()}</span>`;
      b.onclick = () => ouvrir(o[0]);
      nav.appendChild(b);
    });
  }

  function ouvrir(id) {
    UI.panneau = id;
    document.querySelectorAll('.onglet').forEach(b => b.classList.toggle('actif', b.dataset.p === id));
    q('#carte-zone').classList.toggle('cache', id !== 'carte');
    const c = q('#contenu');
    c.classList.toggle('cache', id === 'carte');
    if (id !== 'carte') {
      if (!UI.construits[id]) {
        c.innerHTML = '';
        const d = el('div', 'panneau'); d.id = 'p-' + id;
        c.appendChild(d);
        PANNEAUX[id].build(d);
        UI.construits = {}; UI.construits[id] = true;
      } else {
        // Déjà construit : on le laisse en place
      }
      const p = PANNEAUX[id];
      if (p.maj) p.maj(true);
    } else {
      G.redimensionnerCarte();
    }
    if (id === 'journal') q('#pastille').classList.add('cache');
  }
  G.ouvrirPanneau = ouvrir;

  function pastilleJournal() {
    if (UI.panneau !== 'journal') q('#pastille').classList.remove('cache');
  }

  // ══════════════════════════════════════════════════════ Briques réutilisables
  function tuile(parent, titre, cle, indice) {
    const d = el('div', 'tuile');
    d.appendChild(el('div', 'tuile-t', titre));
    const v = el('div', 'tuile-v', '—'); d.appendChild(v);
    const s = el('div', 'tuile-s', indice || ''); d.appendChild(s);
    parent.appendChild(d);
    UI.refs[cle] = v; UI.refs[cle + '_s'] = s;
    return d;
  }

  function jauge(parent, titre, cle) {
    const d = el('div', 'jauge');
    const h = el('div', 'jauge-h');
    h.appendChild(el('span', '', titre));
    const v = el('span', 'jauge-v', '—'); h.appendChild(v);
    d.appendChild(h);
    const b = el('div', 'barre'); const f = el('div', 'barre-f'); b.appendChild(f); d.appendChild(b);
    parent.appendChild(d);
    UI.refs[cle] = v; UI.refs[cle + '_b'] = f;
    return d;
  }

  function majJauge(cle, v, max, inverse) {
    const t = UI.refs[cle], b = UI.refs[cle + '_b'];
    if (!t) return;
    t.textContent = nf1.format(v) + (max === 100 ? ' %' : '');
    const r = clamp(v / max, 0, 1);
    b.style.width = (r * 100).toFixed(1) + '%';
    const bon = inverse ? 1 - r : r;
    b.style.background = bon > 0.6 ? 'linear-gradient(90deg,#2fa96b,#4fd18b)'
                       : bon > 0.3 ? 'linear-gradient(90deg,#c9922a,#f0c14b)'
                       : 'linear-gradient(90deg,#b03434,#e05555)';
  }

  function curseur(parent, label, min, max, pas, valeur, onChange, format) {
    const d = el('div', 'curseur');
    const h = el('div', 'curseur-h');
    h.appendChild(el('span', '', label));
    const v = el('span', 'curseur-v', format(valeur)); h.appendChild(v);
    d.appendChild(h);
    const i = document.createElement('input');
    i.type = 'range'; i.min = min; i.max = max; i.step = pas; i.value = valeur;
    i.oninput = () => { v.textContent = format(+i.value); onChange(+i.value); };
    d.appendChild(i);
    parent.appendChild(d);
    return { input: i, val: v };
  }

  function bouton(txt, cls, onClick) {
    const b = el('button', 'btn ' + (cls || ''), txt);
    b.onclick = onClick;
    return b;
  }

  function notifier(msg, type) {
    const n = el('div', 'notif ' + (type || ''), msg);
    q('#notifs').appendChild(n);
    setTimeout(() => { n.classList.add('sort'); setTimeout(() => n.remove(), 400); }, 3600);
  }
  G.notifier = notifier;

  function resultat(r) { notifier(r.msg, r.ok ? 'bon' : 'mauvais'); }

  function sectionTitre(parent, txt, sous) {
    const h = el('div', 'sect');
    h.appendChild(el('h2', '', txt));
    if (sous) h.appendChild(el('p', 'sous-titre', sous));
    parent.appendChild(h);
    return h;
  }

  // ══════════════════════════════════════════════════════ Panneaux
  const PANNEAUX = {};

  // ─────────────────────────────────────────────── NATION
  PANNEAUX.nation = {
    build(d) {
      const p = G.PAYS[E.joueur];
      sectionTitre(d, `${p.drapeau} ${p.nom}`, `${G.CONTINENTS[p.cont]} · ${({D:'République démocratique',A:'Régime autoritaire',M:'Monarchie',P:'Parti unique'})[p.reg]}`);
      const g = el('div', 'grille-tuiles');
      tuile(g, 'Produit intérieur brut', 'n_pib');
      tuile(g, 'PIB par habitant', 'n_pibhab');
      tuile(g, 'Croissance annuelle', 'n_croiss');
      tuile(g, 'Population', 'n_pop');
      tuile(g, 'Trésor public', 'n_tresor');
      tuile(g, 'Dette publique', 'n_dette');
      tuile(g, 'Solde quotidien', 'n_solde');
      tuile(g, 'Inflation', 'n_infl');
      tuile(g, 'Chômage', 'n_chom');
      tuile(g, 'Puissance militaire', 'n_mil');
      tuile(g, 'Niveau d\'IA', 'n_ia');
      tuile(g, 'Rang mondial (PIB)', 'n_rang');
      d.appendChild(g);

      sectionTitre(d, 'État de la nation');
      const j = el('div', 'grille-jauges');
      jauge(j, 'Approbation populaire', 'n_app');
      jauge(j, 'Stabilité', 'n_stab');
      jauge(j, 'Technologie', 'n_tech');
      jauge(j, 'Éducation', 'n_educ');
      jauge(j, 'Santé', 'n_sante');
      jauge(j, 'Infrastructure', 'n_infra');
      jauge(j, 'Corruption', 'n_corr');
      jauge(j, 'Réputation internationale', 'n_rep');
      jauge(j, 'Moral des armées', 'n_moral');
      d.appendChild(j);

      sectionTitre(d, 'Alertes');
      const a = el('div', 'alertes'); a.id = 'n-alertes'; d.appendChild(a);
      UI.refs.n_alertes = a;
    },
    maj() {
      const i = E.joueur, r = UI.refs;
      if (!r.n_pib) return;
      r.n_pib.textContent = G.fmtMd(E.pib[i]);
      r.n_pibhab.textContent = nf0.format(E.pib[i] * 1e9 / Math.max(E.pop[i], 1)) + ' $';
      r.n_croiss.textContent = pct(E.croiss[i]);
      r.n_croiss.className = 'tuile-v ' + sig(E.croiss[i] - 0.5);
      r.n_pop.textContent = G.fmtPop(E.pop[i]);
      r.n_tresor.textContent = G.fmtM(E.tresor[i]);
      r.n_dette.textContent = G.fmtM(E.dette[i]);
      r.n_dette_s.textContent = nf0.format(E.dette[i] / Math.max(E.pib[i] * 10, 1)) + ' % du PIB · taux ' + nf1.format(G.tauxInteret(i) * 100) + ' %';
      r.n_solde.textContent = (E.dernierBilan[i] >= 0 ? '+' : '') + G.fmtM(E.dernierBilan[i]);
      r.n_solde.className = 'tuile-v ' + sig(E.dernierBilan[i]);
      r.n_infl.textContent = nf1.format(E.inflation[i]) + ' %';
      r.n_infl.className = 'tuile-v ' + (E.inflation[i] > 8 ? 'mauvais' : E.inflation[i] < 4 ? 'bon' : '');
      r.n_chom.textContent = nf1.format(E.chomage[i]) + ' %';
      r.n_chom.className = 'tuile-v ' + (E.chomage[i] > 12 ? 'mauvais' : E.chomage[i] < 6 ? 'bon' : '');
      r.n_mil.textContent = nf0.format(G.puissance(i, true) / 1000) + ' k';
      r.n_mil_s.textContent = G.fmtPop(G.effectifs(i)) + ' militaires';
      r.n_ia.textContent = 'Niveau ' + (E.ia[i] | 0);
      r.n_ia_s.textContent = G.PALIERS_IA[E.ia[i] | 0].nom;
      let rang = 1; for (let j = 0; j < G.N; j++) if (E.pib[j] > E.pib[i]) rang++;
      r.n_rang.textContent = rang + 'ᵉ';
      r.n_rang_s.textContent = 'sur ' + G.N + ' nations';

      majJauge('n_app', E.approb[i], 100);
      majJauge('n_stab', E.stab[i], 100);
      majJauge('n_tech', E.tech[i], 100);
      majJauge('n_educ', E.educ[i], 100);
      majJauge('n_sante', E.sante[i], 100);
      majJauge('n_infra', E.infra[i], 100);
      majJauge('n_corr', E.corrupt[i], 100, true);
      majJauge('n_rep', E.reput[i], 100);
      majJauge('n_moral', E.moral[i], 100);

      const al = [];
      for (let k = 0; k < G.NRES; k++) {
        const p = E.penurie[i * G.NRES + k];
        if (p > 0.02) al.push(['mauvais', `${G.RES[k].icone} Pénurie de ${G.RES[k].nom.toLowerCase()} : ${nf0.format(p * 100)} % des besoins non couverts.`]);
      }
      if (E.dernierBilan[i] < 0) al.push(['attention', `💸 Déficit budgétaire de ${G.fmtM(-E.dernierBilan[i])} par jour : la dette augmente.`]);
      if (E.dette[i] / (E.pib[i] * 1000) > 1) al.push(['mauvais', '🏦 Dette supérieure au PIB : les taux d\'intérêt s\'envolent.']);
      if (E.approb[i] < 35) al.push(['mauvais', '📉 Approbation critique : votre pouvoir est menacé.']);
      if (E.stab[i] < 25) al.push(['mauvais', '🔥 Stabilité critique : risque de coup d\'État.']);
      if (E.chomage[i] > 15) al.push(['attention', '🧑‍🏭 Chômage de masse.']);
      if (E.inflation[i] > 12) al.push(['attention', '📈 Inflation hors de contrôle.']);
      const men = G.menacePercue(i);
      if (men > 1) al.push(['mauvais', `🎯 Menace militaire élevée à vos frontières (indice ${nf1.format(men)}).`]);
      E.guerres.filter(g => g.a === i || g.d === i).forEach(g => {
        const adv = g.a === i ? g.d : g.a;
        const f = g.a === i ? g.front : -g.front;
        al.push([f > 0 ? 'bon' : 'mauvais', `⚔️ Guerre contre ${G.PAYS[adv].nom} — front à ${nf0.format(f)} %.`]);
      });
      if (!al.length) al.push(['bon', '✅ Aucune alerte. Le pays fonctionne.']);
      const zone = UI.refs.n_alertes;
      const sign = al.map(a => a[1]).join('|');
      if (zone.dataset.sign === sign) return;
      zone.dataset.sign = sign;
      zone.innerHTML = '';
      al.forEach(a => zone.appendChild(el('div', 'alerte ' + a[0], a[1])));
    }
  };

  // ─────────────────────────────────────────────── ÉCONOMIE
  PANNEAUX.economie = {
    build(d) {
      const i = E.joueur;
      sectionTitre(d, 'Fiscalité', 'Chaque point de prélèvement rapporte — et coûte en approbation et en croissance. La courbe de Laffer est active : au-delà d\'un certain seuil, augmenter le taux réduit la recette.');
      const f = el('div', 'grille-2');
      const pc = v => nf0.format(v) + ' %';
      curseur(f, 'Impôt sur le revenu', 0, 60, 1, E.tIR[i] * 100, v => E.tIR[i] = v / 100, pc);
      curseur(f, 'Impôt sur les sociétés', 0, 55, 1, E.tIS[i] * 100, v => E.tIS[i] = v / 100, pc);
      curseur(f, 'TVA', 0, 35, 1, E.tTVA[i] * 100, v => E.tTVA[i] = v / 100, pc);
      curseur(f, 'Droits de douane', 0, 40, 1, E.tDou[i] * 100, v => E.tDou[i] = v / 100, pc);
      d.appendChild(f);

      sectionTitre(d, 'Budget de l\'État', 'Exprimé en part du PIB. Les dépenses sociales achètent de l\'approbation et de la croissance future ; la défense, de la sécurité.');
      const b = el('div', 'grille-2');
      const pc1 = v => nf1.format(v) + ' % du PIB';
      curseur(b, 'Santé', 0, 16, 0.2, E.bSante[i] * 100, v => E.bSante[i] = v / 100, pc1);
      curseur(b, 'Éducation', 0, 14, 0.2, E.bEduc[i] * 100, v => E.bEduc[i] = v / 100, pc1);
      curseur(b, 'Infrastructure', 0, 14, 0.2, E.bInfra[i] * 100, v => E.bInfra[i] = v / 100, pc1);
      curseur(b, 'Défense', 0, 20, 0.2, E.bDef[i] * 100, v => E.bDef[i] = v / 100, pc1);
      curseur(b, 'Subventions et aides', 0, 16, 0.2, E.bSub[i] * 100, v => E.bSub[i] = v / 100, pc1);
      d.appendChild(b);

      sectionTitre(d, 'Comptes publics');
      const g = el('div', 'grille-tuiles');
      tuile(g, 'Recettes / jour', 'e_rec');
      tuile(g, 'Dépenses / jour', 'e_dep');
      tuile(g, 'Solde', 'e_solde');
      tuile(g, 'Trésor', 'e_tresor');
      tuile(g, 'Dette', 'e_dette');
      tuile(g, 'Intérêts / jour', 'e_int');
      tuile(g, 'Entretien (bâtiments + armée)', 'e_entr');
      tuile(g, 'Pression fiscale totale', 'e_pression');
      d.appendChild(g);

      const act = el('div', 'actions');
      act.appendChild(bouton('Emprunter 5 % du PIB', 'sec', () => {
        const m = E.pib[i] * 50;
        E.tresor[i] += m; E.dette[i] += m * 1.02;
        notifier(`${G.fmtM(m)} empruntés sur les marchés.`, '');
      }));
      act.appendChild(bouton('Rembourser 25 % du trésor', 'sec', () => {
        const m = Math.min(E.dette[i], E.tresor[i] * 0.25);
        E.dette[i] -= m; E.tresor[i] -= m;
        notifier(`${G.fmtM(m)} de dette remboursés.`, 'bon');
      }));
      act.appendChild(bouton('Fiscalité nordique', 'sec', () => {
        E.tIR[i] = 0.42; E.tIS[i] = 0.25; E.tTVA[i] = 0.25; E.bSante[i] = 0.09; E.bEduc[i] = 0.07;
        reconstruire('economie'); notifier('Modèle social-démocrate appliqué.', '');
      }));
      act.appendChild(bouton('Fiscalité attractive', 'sec', () => {
        E.tIR[i] = 0.12; E.tIS[i] = 0.10; E.tTVA[i] = 0.08; E.bSub[i] = 0.01;
        reconstruire('economie'); notifier('Modèle à bas impôts appliqué.', '');
      }));
      d.appendChild(act);
    },
    maj() {
      const i = E.joueur, r = UI.refs;
      if (!r.e_rec) return;
      const pibJour = E.pib[i] * 1000 / 365;
      const laf = G.laffer;
      const rec = pibJour * (0.62 * E.tIR[i] * laf(E.tIR[i]) + 0.19 * E.tIS[i] * laf(E.tIS[i]) + 0.62 * E.tTVA[i] * laf(E.tTVA[i])) * (1 - E.corrupt[i] / 260);
      const entr = G.coutEntretien(i);
      const inter = E.dette[i] * G.tauxInteret(i) / 365;
      const dep = pibJour * (E.bSante[i] + E.bEduc[i] + E.bInfra[i] + E.bDef[i] + E.bSub[i] + 0.042) + entr + inter;
      r.e_rec.textContent = G.fmtM(rec);
      r.e_dep.textContent = G.fmtM(dep);
      r.e_solde.textContent = (rec - dep >= 0 ? '+' : '') + G.fmtM(rec - dep);
      r.e_solde.className = 'tuile-v ' + sig(rec - dep);
      r.e_tresor.textContent = G.fmtM(E.tresor[i]);
      r.e_dette.textContent = G.fmtM(E.dette[i]);
      r.e_dette_s.textContent = nf0.format(E.dette[i] / Math.max(E.pib[i] * 10, 1)) + ' % du PIB';
      r.e_int.textContent = G.fmtM(inter);
      r.e_entr.textContent = G.fmtM(entr);
      const pression = (E.tIR[i] * 0.62 + E.tIS[i] * 0.19 + E.tTVA[i] * 0.62) * 100;
      r.e_pression.textContent = nf1.format(pression) + ' % du PIB';
      r.e_pression_s.textContent = pression > 32 ? 'Élevée : croissance et approbation freinées' : pression < 14 ? 'Faible : recettes limitées' : 'Équilibrée';
    }
  };

  // ─────────────────────────────────────────────── RESSOURCES
  PANNEAUX.ressources = {
    build(d) {
      sectionTitre(d, 'Ressources et marché mondial',
        'Ce que vous ne produisez pas, vous l\'achetez au prix du marché — s\'il vous reste du trésor. Sinon, c\'est la pénurie, et la pénurie fait tomber les gouvernements.');
      const t = el('table', 'tab');
      t.innerHTML = `<thead><tr>
        <th>Ressource</th><th class="n">Production/j</th><th class="n">Consommation/j</th>
        <th class="n">Solde</th><th class="n">Stock</th><th class="n">Prix mondial</th>
        <th class="n">Valeur du solde</th><th>État</th></tr></thead>`;
      const tb = el('tbody');
      UI.refs.r_lignes = [];
      G.RES.forEach((res, k) => {
        const tr = el('tr');
        tr.innerHTML = `<td class="res-nom">${res.icone} ${res.nom}</td>` + '<td class="n">—</td>'.repeat(6) + '<td>—</td>';
        tb.appendChild(tr);
        UI.refs.r_lignes.push(tr.querySelectorAll('td'));
      });
      t.appendChild(tb);
      const wrap = el('div', 'tab-wrap'); wrap.appendChild(t); d.appendChild(wrap);

      sectionTitre(d, 'Dotations naturelles', 'Ce que contient votre sous-sol. On ne construit pas une mine là où il n\'y a rien.');
      const dot = el('div', 'grille-dot');
      const noms = ['Pétrole','Gaz','Charbon','Fer','Cuivre','Terres rares','Uranium','Or','Agriculture'];
      const ico = ['🛢️','🔥','⚫','⛓️','🟠','💠','☢️','🥇','🌾'];
      G.PAYS[E.joueur].dot.forEach((v, k) => {
        const c = el('div', 'dot-c');
        c.appendChild(el('div', 'dot-i', ico[k]));
        c.appendChild(el('div', 'dot-n', noms[k]));
        const b = el('div', 'dot-b');
        for (let n = 0; n < 9; n++) b.appendChild(el('span', 'pt' + (n < v ? ' plein' : '')));
        c.appendChild(b);
        c.appendChild(el('div', 'dot-v', v === 0 ? 'Aucune' : v <= 2 ? 'Marginale' : v <= 4 ? 'Modeste' : v <= 6 ? 'Solide' : 'Colossale'));
        dot.appendChild(c);
      });
      d.appendChild(dot);
    },
    maj() {
      const i = E.joueur, L = UI.refs.r_lignes;
      if (!L) return;
      G.RES.forEach((res, k) => {
        const b = i * G.NRES + k;
        const pr = E.prod[b], co = E.conso[b], so = pr - co, st = E.stock[b], px = E.prix[k];
        const c = L[k];
        c[1].textContent = G.fmtNb(pr);
        c[2].textContent = G.fmtNb(co);
        c[3].textContent = (so >= 0 ? '+' : '') + G.fmtNb(so);
        c[3].className = 'n ' + sig(so);
        c[4].textContent = G.fmtNb(st);
        const dev = (px / E.prixBase[k] - 1) * 100;
        c[5].textContent = nf0.format(px) + ' $  (' + (dev >= 0 ? '+' : '') + nf0.format(dev) + ' %)';
        c[5].className = 'n ' + (dev > 12 ? 'mauvais' : dev < -12 ? 'bon' : '');
        c[6].textContent = (so >= 0 ? '+' : '') + G.fmtM(so * px / 1e6);
        c[6].className = 'n ' + sig(so);
        const pen = E.penurie[b];
        c[7].innerHTML = pen > 0.02 ? `<span class="etat mauvais">Pénurie ${nf0.format(pen * 100)} %</span>`
                       : so > 0 ? '<span class="etat bon">Exportateur</span>'
                       : '<span class="etat">Importateur</span>';
      });
    }
  };

  // ─────────────────────────────────────────────── CONSTRUCTION
  PANNEAUX.construction = {
    build(d) {
      sectionTitre(d, 'Ministère de la Construction',
        'Choisissez un bâtiment et cliquez sur Construire : la somme est prélevée sur le trésor, ' +
        'le chantier démarre et le bâtiment produit dès sa livraison. Si le trésor ne suffit pas, ' +
        'le bouton propose de financer le chantier par l\'emprunt — c\'est ainsi que démarrent les petits pays.');
      const ch = el('div', 'chantiers'); ch.id = 'c-chantiers'; d.appendChild(ch);
      UI.refs.c_chantiers = ch;

      const cats = [['ressources','Ressources'],['energie','Énergie'],['industrie','Industrie'],
                    ['ia','Recherche et IA'],['social','Société'],['militaire','Militaire']];
      UI.refs.c_cartes = [];
      cats.forEach(cat => {
        sectionTitre(d, cat[1]);
        const g = el('div', 'grille-bat');
        G.BAT.forEach((bd, k) => {
          if (bd.cat !== cat[0]) return;
          const c = el('div', 'carte-bat');
          const h = el('div', 'cb-h');
          h.appendChild(el('span', 'cb-i', bd.icone));
          const ht = el('div', 'cb-ht');
          ht.appendChild(el('div', 'cb-n', bd.nom));
          const pos = el('div', 'cb-p', '0 en service');
          ht.appendChild(pos);
          h.appendChild(ht);
          c.appendChild(h);
          c.appendChild(el('p', 'cb-d', bd.desc));
          const eff = [];
          if (bd.prod) for (const x in bd.prod) eff.push(`+${G.fmtNb(bd.prod[x])} ${G.RES[R[x]].nom.toLowerCase()}/j`);
          if (bd.conso) for (const x in bd.conso) eff.push(`−${G.fmtNb(bd.conso[x])} ${G.RES[R[x]].nom.toLowerCase()}/j`);
          if (bd.rech) eff.push(`+${bd.rech} recherche/j`);
          if (bd.educ) eff.push('+ éducation');
          if (bd.sante) eff.push('+ santé');
          if (bd.infra) eff.push('+ infrastructure');
          if (bd.export) eff.push('+ capacité d\'exportation');
          if (bd.milcap) eff.push('+ capacité militaire');
          if (bd.nuke) eff.push('Débloque l\'arme nucléaire');
          const ul = el('div', 'cb-e');
          eff.forEach(x => ul.appendChild(el('span', 'pastille', x)));
          c.appendChild(ul);
          const pied = el('div', 'cb-f');
          const cout = el('div', 'cb-c', '—');
          pied.appendChild(cout);
          const btn = bouton('Construire', 'principal', () => {
            resultat(G.construire(E.joueur, k, btn.dataset.credit === '1'));
            PANNEAUX.construction.maj();
          });
          pied.appendChild(btn);
          c.appendChild(pied);
          g.appendChild(c);
          UI.refs.c_cartes.push({ k: k, pos: pos, cout: cout, btn: btn, carte: c });
        });
        d.appendChild(g);
      });
    },
    maj() {
      const i = E.joueur;
      const C = UI.refs.c_cartes;
      if (!C) return;
      C.forEach(x => {
        const n = E.bat[i * G.NBAT + x.k];
        const enc = E.chantiers.filter(c => c.p === i && c.b === x.k).length;
        x.pos.textContent = `${n} en service` + (enc ? ` · ${enc} en chantier` : '');
        const cout = G.coutBatiment(i, x.k);
        const bd = G.BAT[x.k];
        x.cout.textContent = `${G.fmtM(cout)} · ${bd.jours} j · entretien ${nf2.format(bd.entretien)} M$/j`;
        const manque = cout - E.tresor[i];
        let etat = 'ok', libelle = 'Construire';
        if (bd.tech && E.tech[i] < bd.tech) { etat = 'off'; libelle = `Technologie ${bd.tech} requise`; }
        else if (bd.dot !== undefined && G.PAYS[i].dot[bd.dot] < 1) { etat = 'off'; libelle = 'Pas de gisement'; }
        else if (manque > 0) {
          if (manque <= G.capaciteEmprunt(i)) { etat = 'credit'; libelle = `Construire à crédit (+${G.fmtM(manque)} de dette)`; }
          else { etat = 'off'; libelle = 'Endettement au plafond'; }
        }
        x.btn.dataset.credit = etat === 'credit' ? '1' : '0';
        x.btn.className = 'btn ' + (etat === 'off' ? 'off' : etat === 'credit' ? 'sec' : 'principal');
        x.btn.textContent = libelle;
        x.btn.disabled = etat === 'off';
      });
      const ch = UI.refs.c_chantiers;
      const mes = E.chantiers.filter(c => c.p === i).concat(E.casernes.filter(c => c.p === i).map(c => ({ u: c.u, reste: c.reste, n: c.n, total: G.UNI[c.u].jours })));
      const sign = mes.map(c => (c.b !== undefined ? 'b' + c.b : 'u' + c.u) + ':' + c.reste).join(',');
      if (ch.dataset.sign === sign) return;
      ch.dataset.sign = sign;
      ch.innerHTML = '';
      if (!mes.length) { ch.appendChild(el('div', 'vide', 'Aucun chantier en cours.')); return; }
      mes.forEach(c => {
        const def = c.b !== undefined ? G.BAT[c.b] : G.UNI[c.u];
        const tot = c.b !== undefined ? Math.max(c.total, 1) : Math.max(def.jours, 1);
        const av = clamp(1 - c.reste / tot, 0, 1);
        const li = el('div', 'chantier');
        li.innerHTML = `<span class="ch-i">${def.icone}</span><span class="ch-n">${def.nom}${c.n ? ' ×' + c.n : ''}</span>
          <span class="ch-b"><i style="width:${(av * 100).toFixed(0)}%"></i></span>
          <span class="ch-j">${c.reste} j</span>`;
        ch.appendChild(li);
      });
    }
  };

  // ─────────────────────────────────────────────── COMMERCE
  PANNEAUX.commerce = {
    build(d) {
      const i = E.joueur;
      sectionTitre(d, 'Contrats commerciaux',
        'Votre excédent part déjà seul sur le marché mondial au prix du jour. Un contrat sert à autre chose : ' +
        'verrouiller un prix et un volume sur plusieurs années, avec un pays précis. ' +
        'Un pays n\'accepte que s\'il manque vraiment de la ressource — la liste ci-dessous vous dit qui.');

      const of = el('div', 'bloc'); of.id = 'm-offres'; d.appendChild(of);
      UI.refs.m_offres = of;

      sectionTitre(d, 'Proposer un contrat');
      const form = el('div', 'form');
      const selRes = el('select', 'champ');
      G.RES.forEach((r, k) => { const o = el('option', '', `${r.icone} ${r.nom}`); o.value = k; selRes.appendChild(o); });
      const selPays = el('select', 'champ');
      G.PAYS.forEach((p, k) => { if (k === i) return; const o = el('option', '', `${p.drapeau} ${p.nom}`); o.value = k; selPays.appendChild(o); });
      const inQte = el('input', 'champ'); inQte.type = 'number'; inQte.value = 1000; inQte.min = 1;
      const inPrix = el('input', 'champ'); inPrix.type = 'number'; inPrix.value = 100; inPrix.min = 0.01; inPrix.step = 0.01;
      const selDur = el('select', 'champ');
      [[180,'6 mois'],[365,'1 an'],[730,'2 ans'],[1825,'5 ans']].forEach(x => { const o = el('option', '', x[1]); o.value = x[0]; selDur.appendChild(o); });
      selDur.value = 365;

      const champ = (lab, node) => { const w = el('div', 'champ-w'); w.appendChild(el('label', '', lab)); w.appendChild(node); return w; };
      form.appendChild(champ('Ressource', selRes));
      form.appendChild(champ('Partenaire', selPays));
      form.appendChild(champ('Quantité par jour', inQte));
      form.appendChild(champ('Prix unitaire ($)', inPrix));
      form.appendChild(champ('Durée', selDur));
      d.appendChild(form);

      const suggestions = el('div', 'bloc'); d.appendChild(suggestions);
      const info = el('div', 'form-info'); d.appendChild(info);
      const majSuggestions = () => {
        const k = +selRes.value;
        const ach = G.meilleursAcheteurs(k, 5), ven = G.meilleursVendeurs(k, 5);
        suggestions.innerHTML = '';
        const colonne = (titre, liste, sousTitre) => {
          const c = el('div', 'sugg');
          c.appendChild(el('h4', '', titre));
          c.appendChild(el('p', 'mini', sousTitre));
          if (!liste.length) { c.appendChild(el('div', 'vide', 'Aucun pays dans ce cas.')); return c; }
          liste.forEach(x => {
            const vente = titre.indexOf('acheteurs') >= 0;
            const mien = E.prod[i * G.NRES + k] - E.conso[i * G.NRES + k];
            // On ne propose que ce que les deux parties peuvent réellement assumer.
            const volume = vente
              ? Math.min(x.qte * 0.8, Math.max(0, mien) * 0.7)
              : Math.min(x.qte * 0.8, Math.max(0, -mien) * 0.9);
            const b = el('button', 'sugg-p');
            b.innerHTML = `<span>${G.PAYS[x.j].drapeau} ${G.PAYS[x.j].nom}</span>
              <em>${volume >= 1 ? (vente ? 'vendre ' : 'acheter ') + G.fmtNb(volume) + '/j' : 'volume nul'}
              · relations ${x.rel > 0 ? '+' : ''}${x.rel}</em>`;
            b.onclick = () => {
              selPays.value = x.j;
              inQte.value = Math.max(1, Math.round(volume));
              inPrix.value = nf2.format(E.prix[k] * (vente ? 0.99 : 1.01)).replace(/\s/g, '').replace(',', '.');
              majInfo();
              if (volume < 1) {
                notifier(vente ? 'Vous n\'avez aucun excédent de cette ressource à vendre.'
                               : 'Vous n\'avez besoin d\'aucune quantité de cette ressource.', 'mauvais');
                return;
              }
              const r = vente
                ? G.proposerContrat(i, x.j, k, +inQte.value, +inPrix.value, +selDur.value)
                : G.proposerContrat(x.j, i, k, +inQte.value, +inPrix.value, +selDur.value);
              resultat(r);
              PANNEAUX.commerce.maj(true);
              majSuggestions();
            };
            c.appendChild(b);
          });
          return c;
        };
        const g = el('div', 'grille-sugg');
        g.appendChild(colonne('Qui manque de ' + G.RES[k].nom.toLowerCase() + ' — vos acheteurs', ach,
          'Un clic propose la vente sur-le-champ, au volume que vous pouvez livrer et au prix du marché.'));
        g.appendChild(colonne('Qui en a en trop — vos vendeurs', ven,
          'Un clic propose l\'achat, à hauteur de ce qui vous manque.'));
        suggestions.appendChild(g);
      };

      const majInfo = () => {
        const k = +selRes.value, j = +selPays.value;
        const px = E.prix[k];
        const bj = j * G.NRES + k;
        const besoin = Math.max(0, E.conso[bj] - E.prod[bj]);
        const mien = E.prod[i * G.NRES + k] - E.conso[i * G.NRES + k];
        const rel = E.rel[i * G.N + j];
        const revenu = +inQte.value * +inPrix.value / 1e6;
        info.innerHTML = `<span>Prix du marché : <b>${nf0.format(px)} $</b></span>
          <span>Besoin de ${G.PAYS[j].nom} : <b>${G.fmtNb(besoin)}/j</b></span>
          <span>Votre solde : <b class="${sig(mien)}">${(mien >= 0 ? '+' : '') + G.fmtNb(mien)}/j</b></span>
          <span>Relations : <b class="${sig(rel)}">${rel > 0 ? '+' : ''}${rel}</b></span>
          <span>Recette : <b>${G.fmtM(revenu)}/j</b></span>`;
      };
      selRes.onchange = () => {
        inPrix.value = nf2.format(E.prix[+selRes.value]).replace(/\s/g, '').replace(',', '.');
        majSuggestions(); majInfo();
      };
      [selPays, inQte, inPrix, selDur].forEach(x => x.onchange = majInfo);
      inQte.oninput = majInfo; inPrix.oninput = majInfo;
      // On ouvre sur la ressource où le joueur a le plus gros excédent à placer.
      let meilleure = 0, meilleurSurplus = -Infinity;
      for (let k = 0; k < G.NRES; k++) {
        const sol = E.prod[i * G.NRES + k] - E.conso[i * G.NRES + k];
        const valeur = sol * E.prix[k];
        if (sol > 0 && valeur > meilleurSurplus) { meilleurSurplus = valeur; meilleure = k; }
      }
      selRes.value = meilleure;
      selRes.onchange();
      const premier = G.meilleursAcheteurs(meilleure, 1)[0];
      if (premier) {
        selPays.value = premier.j;
        inQte.value = Math.max(1, Math.round(Math.min(premier.qte, Math.max(0, E.prod[i * G.NRES + meilleure] - E.conso[i * G.NRES + meilleure])) * 0.6));
        majInfo();
      }

      const act = el('div', 'actions');
      act.appendChild(bouton('Proposer la vente', 'principal', () => {
        const r = G.proposerContrat(i, +selPays.value, +selRes.value, +inQte.value, +inPrix.value, +selDur.value);
        resultat(r); PANNEAUX.commerce.maj(true);
      }));
      act.appendChild(bouton('Proposer l\'achat', 'sec', () => {
        const r = G.proposerContrat(+selPays.value, i, +selRes.value, +inQte.value, +inPrix.value, +selDur.value);
        resultat(r); PANNEAUX.commerce.maj(true);
      }));
      act.appendChild(bouton('Prix du marché', 'sec', () => {
        inPrix.value = nf2.format(E.prix[+selRes.value]).replace(/\s/g, '').replace(',', '.');
        majInfo(); notifier('Prix aligné sur le marché mondial.', '');
      }));
      act.appendChild(bouton('Actualiser les partenaires', 'sec', () => { majSuggestions(); majInfo(); }));
      d.appendChild(act);

      sectionTitre(d, 'Contrats en cours');
      const li = el('div', 'bloc'); li.id = 'm-liste'; d.appendChild(li);
      UI.refs.m_liste = li;
    },
    maj(force) {
      const i = E.joueur;
      // Offres reçues
      const of = UI.refs.m_offres;
      const offres = E.offres || [];
      const sgo = offres.map(o => o.v + '-' + o.r + '-' + (o.qte | 0)).join(',');
      if (of.dataset.sign !== sgo) {
        of.dataset.sign = sgo;
        of.innerHTML = '';
        if (offres.length) {
          of.appendChild(el('h3', '', 'Offres reçues'));
          offres.forEach((o, n) => {
            const c = el('div', 'offre');
            c.innerHTML = `<span class="of-t">${G.PAYS[o.v].drapeau} <b>${G.PAYS[o.v].nom}</b> vous propose
              ${G.RES[o.r].icone} <b>${G.fmtNb(o.qte)}</b> ${G.RES[o.r].nom.toLowerCase()}/jour à
              <b>${nf0.format(o.prix)} $</b> l'unité pendant ${Math.round(o.jours / 365)} an(s)
              — soit ${G.fmtM(o.qte * o.prix / 1e6)}/jour.</span>`;
            const a = el('div', 'of-a');
            a.appendChild(bouton('Accepter', 'principal', () => {
              E.contrats.push({ v: o.v, a: i, r: o.r, qte: o.qte, prix: o.prix, jours: o.jours, id: E.idContrat++ });
              G.modifierRelation(i, o.v, 6);
              E.offres.splice(n, 1); notifier('Contrat signé.', 'bon'); PANNEAUX.commerce.maj(true);
            }));
            a.appendChild(bouton('Refuser', 'sec', () => {
              G.modifierRelation(i, o.v, -3);
              E.offres.splice(n, 1); PANNEAUX.commerce.maj(true);
            }));
            c.appendChild(a);
            of.appendChild(c);
          });
        }
      }

      const li = UI.refs.m_liste;
      const mes = E.contrats.filter(c => c.v === i || c.a === i);
      const sign = mes.map(c => c.id + ':' + c.jours).join(',');
      if (!force && li.dataset.sign === sign) return;
      li.dataset.sign = sign;
      li.innerHTML = '';
      if (!mes.length) { li.appendChild(el('div', 'vide', 'Aucun contrat en cours. Le marché libre reste votre seul débouché.')); return; }
      const t = el('table', 'tab');
      t.innerHTML = `<thead><tr><th>Sens</th><th>Partenaire</th><th>Ressource</th>
        <th class="n">Quantité/j</th><th class="n">Prix</th><th class="n">Flux/j</th><th class="n">Reste</th><th></th></tr></thead>`;
      const tb = el('tbody');
      mes.forEach(c => {
        const vend = c.v === i;
        const autre = vend ? c.a : c.v;
        const tr = el('tr');
        tr.innerHTML = `<td><span class="etat ${vend ? 'bon' : ''}">${vend ? 'Vente' : 'Achat'}</span></td>
          <td>${G.PAYS[autre].drapeau} ${G.PAYS[autre].nom}</td>
          <td>${G.RES[c.r].icone} ${G.RES[c.r].nom}</td>
          <td class="n">${G.fmtNb(c.qte)}</td>
          <td class="n">${nf0.format(c.prix)} $ <span class="mini">(marché ${nf0.format(E.prix[c.r])} $)</span></td>
          <td class="n ${vend ? 'bon' : 'mauvais'}">${vend ? '+' : '−'}${G.fmtM(c.qte * c.prix / 1e6)}</td>
          <td class="n">${Math.round(c.jours / 30)} mois</td>`;
        const td = el('td');
        td.appendChild(bouton('Rompre', 'danger mini-b', () => {
          const k = E.contrats.indexOf(c);
          if (k >= 0) { E.contrats.splice(k, 1); G.modifierRelation(i, autre, -15); notifier('Contrat rompu unilatéralement. Relations −15.', 'mauvais'); PANNEAUX.commerce.maj(true); }
        }));
        tr.appendChild(td);
        tb.appendChild(tr);
      });
      t.appendChild(tb);
      const w = el('div', 'tab-wrap'); w.appendChild(t); li.appendChild(w);
    }
  };

  // ─────────────────────────────────────────────── DIPLOMATIE
  PANNEAUX.diplomatie = {
    build(d) {
      sectionTitre(d, 'Ministère des Affaires étrangères',
        'Les relations vont de −100 à +100. En dessous de −35, un pays vous considère comme un adversaire ; au-dessus de +55, une alliance devient possible.');
      const barre = el('div', 'filtres');
      const rech = el('input', 'champ'); rech.placeholder = 'Rechercher un pays…';
      const tri = el('select', 'champ');
      [['rel','Relations'],['pib','Puissance économique'],['arm','Puissance militaire'],['nom','Nom'],['prox','Proximité géographique']]
        .forEach(x => { const o = el('option', '', x[1]); o.value = x[0]; tri.appendChild(o); });
      const filtre = el('select', 'champ');
      [['tous','Tous les pays'],['allies','Alliés'],['ennemis','Hostiles'],['guerre','En guerre'],['contrats','Partenaires commerciaux']]
        .forEach(x => { const o = el('option', '', x[1]); o.value = x[0]; filtre.appendChild(o); });
      barre.appendChild(rech); barre.appendChild(tri); barre.appendChild(filtre);
      d.appendChild(barre);
      UI.refs.d_rech = rech; UI.refs.d_tri = tri; UI.refs.d_filtre = filtre;
      [rech, tri, filtre].forEach(x => { x.oninput = () => majDiplo(true); x.onchange = () => majDiplo(true); });

      const split = el('div', 'split');
      const liste = el('div', 'liste-pays'); liste.id = 'd-liste';
      const detail = el('div', 'detail-pays'); detail.id = 'd-detail';
      split.appendChild(liste); split.appendChild(detail);
      d.appendChild(split);
      UI.refs.d_liste = liste; UI.refs.d_detail = detail;
      if (UI.paysVise < 0) UI.paysVise = premierAutre();
      majDiplo(true);
    },
    maj(force) { majDiplo(force); }
  };

  function premierAutre() { return E.joueur === 0 ? 1 : 0; }

  let dernierListeSign = '';
  function majDiplo(force) {
    const i = E.joueur;
    const liste = UI.refs.d_liste;
    if (!liste) return;
    const rech = (UI.refs.d_rech.value || '').toLowerCase();
    const tri = UI.refs.d_tri.value, filtre = UI.refs.d_filtre.value;

    let ids = [];
    for (let k = 0; k < G.N; k++) {
      if (k === i) continue;
      const p = G.PAYS[k];
      if (rech && p.nom.toLowerCase().indexOf(rech) < 0 && p.code.toLowerCase().indexOf(rech) < 0) continue;
      const st = G.statutCarte(k);
      if (filtre === 'allies' && st !== 'allie' && st !== 'pacte') continue;
      if (filtre === 'ennemis' && st !== 'hostile' && st !== 'guerre' && st !== 'sanction') continue;
      if (filtre === 'guerre' && st !== 'guerre') continue;
      if (filtre === 'contrats' && !E.contrats.some(c => (c.v === k && c.a === i) || (c.a === k && c.v === i))) continue;
      ids.push(k);
    }
    const tris = {
      rel: (a, b) => E.rel[i * G.N + b] - E.rel[i * G.N + a],
      pib: (a, b) => E.pib[b] - E.pib[a],
      arm: (a, b) => G.puissance(b, true) - G.puissance(a, true),
      nom: (a, b) => G.PAYS[a].nom.localeCompare(G.PAYS[b].nom),
      prox: (a, b) => G.distance(G.PAYS[i], G.PAYS[a]) - G.distance(G.PAYS[i], G.PAYS[b])
    };
    ids.sort(tris[tri]);
    ids = ids.slice(0, 90);

    const sign = tri + filtre + rech + ids.join(',') + ids.map(k => E.rel[i * G.N + k]).join(',') + UI.paysVise;
    if (!force && sign === dernierListeSign) { majDetail(); return; }
    dernierListeSign = sign;

    liste.innerHTML = '';
    ids.forEach(k => {
      const p = G.PAYS[k], rel = E.rel[i * G.N + k], st = G.statutCarte(k);
      const row = el('div', 'lp' + (k === UI.paysVise ? ' actif' : ''));
      row.innerHTML = `<span class="lp-f">${p.drapeau}</span>
        <span class="lp-n">${p.nom}<em>${G.fmtMd(E.pib[k])} · IA N${E.ia[k] | 0}</em></span>
        <span class="lp-r ${rel > 20 ? 'bon' : rel < -20 ? 'mauvais' : ''}">${rel > 0 ? '+' : ''}${rel}</span>
        <span class="pl-s pt-${st}"></span>`;
      row.onclick = () => { UI.paysVise = k; G.carte.choisi = k; majDiplo(true); };
      liste.appendChild(row);
    });
    majDetail();
  }

  function majDetail() {
    const det = UI.refs.d_detail, i = E.joueur, j = UI.paysVise;
    if (!det || j < 0) return;
    if (det.dataset.p == j && det.dataset.t == (E.jour / 30 | 0)) return;
    det.dataset.p = j; det.dataset.t = (E.jour / 30 | 0);
    const p = G.PAYS[j], rel = E.rel[i * G.N + j];
    const enGuerre = E.guerres.some(g => (g.a === i && g.d === j) || (g.a === j && g.d === i));
    const allie = G.estAllie(i, j);
    const sanction = E.sanctions.some(s => s[0] === i && s[1] === j);
    const rapport = G.puissance(i, true) / (G.puissance(j, false) + 1);

    det.innerHTML = `
      <div class="dp-h"><span class="dp-f">${p.drapeau}</span>
        <div><h3>${p.nom}</h3><p>${G.CONTINENTS[p.cont]} · ${({D:'Démocratie',A:'Autoritaire',M:'Monarchie',P:'Parti unique'})[p.reg]}</p></div></div>
      <div class="dp-rel ${rel > 20 ? 'bon' : rel < -20 ? 'mauvais' : ''}">Relations : ${rel > 0 ? '+' : ''}${rel}
        ${allie ? ' · <b>Allié</b>' : ''}${enGuerre ? ' · <b>EN GUERRE</b>' : ''}${sanction ? ' · sous sanctions' : ''}</div>
      <div class="dp-stats">
        <div><span>PIB</span><b>${G.fmtMd(E.pib[j])}</b></div>
        <div><span>PIB/hab</span><b>${nf0.format(E.pib[j] * 1e9 / Math.max(E.pop[j], 1))} $</b></div>
        <div><span>Population</span><b>${G.fmtPop(E.pop[j])}</b></div>
        <div><span>Croissance</span><b class="${sig(E.croiss[j] - 0.5)}">${pct(E.croiss[j])}</b></div>
        <div><span>Technologie</span><b>${nf0.format(E.tech[j])}</b></div>
        <div><span>Niveau d'IA</span><b>N${E.ia[j] | 0}</b></div>
        <div><span>Puissance militaire</span><b>${nf0.format(G.puissance(j, true) / 1000)} k</b></div>
        <div><span>Rapport de force</span><b class="${rapport > 1.2 ? 'bon' : rapport < 0.8 ? 'mauvais' : ''}">${nf2.format(rapport)} ×</b></div>
        <div><span>Stabilité</span><b>${nf0.format(E.stab[j])}</b></div>
        <div><span>Ogives</span><b>${nf0.format(E.uni[j * G.NUNI + U.ogive])}</b></div>
      </div>`;
    const act = el('div', 'dp-actions');
    const A = (txt, cls, type, montant) => act.appendChild(bouton(txt, cls, () => {
      resultat(G.actionDiplo(i, j, type, montant)); det.dataset.p = -1; majDiplo(true);
    }));
    A('Ouvrir une ambassade (120 M$)', 'sec', 'ambassade');
    A('Aide de 500 M$', 'sec', 'aide', 500);
    A('Aide de 5 Md$', 'sec', 'aide', 5000);
    A('Pacte de non-agression', 'sec', 'pacte');
    A('Proposer une alliance', 'principal', 'alliance');
    A('Opération d\'espionnage (250 M$)', 'sec', 'espion');
    if (sanction) A('Lever les sanctions', 'sec', 'leversanction');
    else A('Décréter des sanctions', 'danger', 'sanction');
    if (!enGuerre) {
      act.appendChild(bouton('Déclarer la guerre', 'danger', () => {
        G.confirmer(`Déclarer la guerre à ${p.nom} ?`,
          `Rapport de force estimé : ${nf2.format(rapport)} × en votre faveur. ` +
          'Leurs alliés peuvent entrer dans le conflit, et votre réputation en souffrira.',
          () => { resultat(G.declarerGuerre(i, j)); det.dataset.p = -1; majDiplo(true); },
          'Déclarer la guerre');
      }));
    }
    act.appendChild(bouton('Centrer sur la carte', 'sec', () => { ouvrir('carte'); G.centrerSur(j); }));
    det.appendChild(act);
  }

  // ─────────────────────────────────────────────── ARMÉE
  PANNEAUX.armee = {
    build(d) {
      sectionTitre(d, 'État-major',
        'La puissance ne se compte pas en soldats mais en soldats × technologie × moral. Une armée nombreuse et mal équipée perd contre une armée réduite et moderne.');
      const g = el('div', 'grille-tuiles');
      tuile(g, 'Puissance offensive', 'a_off');
      tuile(g, 'Puissance défensive', 'a_def');
      tuile(g, 'Effectifs', 'a_eff');
      tuile(g, 'Entretien / jour', 'a_ent');
      tuile(g, 'Moral', 'a_moral');
      tuile(g, 'Rang militaire mondial', 'a_rang');
      d.appendChild(g);

      const gu = el('div', 'bloc'); gu.id = 'a-guerres'; d.appendChild(gu);
      UI.refs.a_guerres = gu;

      sectionTitre(d, 'Forces et recrutement');
      const t = el('div', 'grille-bat');
      UI.refs.a_cartes = [];
      G.UNI.forEach((ud, k) => {
        const c = el('div', 'carte-bat');
        const h = el('div', 'cb-h');
        h.appendChild(el('span', 'cb-i', ud.icone));
        const ht = el('div', 'cb-ht');
        ht.appendChild(el('div', 'cb-n', ud.nom));
        const pos = el('div', 'cb-p', '—'); ht.appendChild(pos);
        h.appendChild(ht); c.appendChild(h);
        c.appendChild(el('p', 'cb-d', ud.desc));
        const e = el('div', 'cb-e');
        e.appendChild(el('span', 'pastille', `Attaque ${ud.att}`));
        e.appendChild(el('span', 'pastille', `Défense ${ud.def}`));
        e.appendChild(el('span', 'pastille', `${nf0.format(ud.hommes)} hommes`));
        if (ud.tech) e.appendChild(el('span', 'pastille', `Techno ${ud.tech}`));
        c.appendChild(e);
        const f = el('div', 'cb-f');
        const cout = el('div', 'cb-c', '—'); f.appendChild(cout);
        const lots = el('div', 'lots');
        [1, 10, 50].forEach(n => lots.appendChild(bouton('×' + n, 'sec mini-b', () => {
          resultat(G.recruter(E.joueur, k, n)); PANNEAUX.armee.maj();
        })));
        f.appendChild(lots);
        c.appendChild(f);
        t.appendChild(c);
        UI.refs.a_cartes.push({ k: k, pos: pos, cout: cout });
      });
      d.appendChild(t);
    },
    maj() {
      const i = E.joueur, r = UI.refs;
      if (!r.a_off) return;
      r.a_off.textContent = nf0.format(G.puissance(i, true) / 1000) + ' k';
      r.a_def.textContent = nf0.format(G.puissance(i, false) / 1000) + ' k';
      r.a_eff.textContent = G.fmtPop(G.effectifs(i));
      let ent = 0;
      for (let u = 0; u < G.NUNI; u++) ent += E.uni[i * G.NUNI + u] * G.UNI[u].entretien;
      r.a_ent.textContent = G.fmtM(ent);
      r.a_moral.textContent = nf0.format(E.moral[i]) + ' %';
      let rang = 1; const mine = G.puissance(i, true);
      for (let j = 0; j < G.N; j++) if (G.puissance(j, true) > mine) rang++;
      r.a_rang.textContent = rang + 'ᵉ';

      r.a_cartes.forEach(x => {
        const ud = G.UNI[x.k];
        x.pos.textContent = nf0.format(E.uni[i * G.NUNI + x.k]) + ' en service';
        x.cout.textContent = `${G.fmtM(ud.cout)} l'unité · ${ud.jours} j · ${nf0.format(ud.entretien * 1000)} k$/j`;
      });

      const gz = r.a_guerres;
      const mes = E.guerres.filter(g => g.a === i || g.d === i);
      const sign = mes.map(g => g.a + '-' + g.d + ':' + (g.front | 0)).join(',');
      if (gz.dataset.sign === sign) return;
      gz.dataset.sign = sign;
      gz.innerHTML = '';
      if (!mes.length) return;
      gz.appendChild(el('h3', '', 'Guerres en cours'));
      mes.forEach(g => {
        const att = g.a === i, adv = att ? g.d : g.a;
        const f = att ? g.front : -g.front;
        const c = el('div', 'guerre');
        c.innerHTML = `<div class="gu-h">${att ? '🗡️ Offensive contre' : '🛡️ Défense face à'}
            ${G.PAYS[adv].drapeau} <b>${G.PAYS[adv].nom}</b> · ${g.jours} jours de conflit</div>
          <div class="gu-front"><i class="${f >= 0 ? 'p' : 'n'}" style="width:${Math.abs(f) / 2}%;${f >= 0 ? 'left:50%' : 'right:50%'}"></i><span class="gu-m"></span></div>
          <div class="gu-s">Front à <b class="${f > 0 ? 'bon' : 'mauvais'}">${nf0.format(f)} %</b> ·
            Vos pertes : ${G.fmtPop(att ? g.mortsA : g.mortsD)} · Pertes ennemies : ${G.fmtPop(att ? g.mortsD : g.mortsA)} ·
            Rapport ${nf2.format(G.puissance(i, att) / (G.puissance(adv, !att) + 1))} ×</div>`;
        const a = el('div', 'gu-a');
        a.appendChild(bouton('Proposer la paix', 'sec', () => {
          const k = E.guerres.indexOf(g);
          const accepte = f < -15 || (Math.abs(f) < 25 && Math.random() < 0.5);
          if (accepte) { E.guerres.splice(k, 1); G.modifierRelation(i, adv, 20); notifier('Paix signée.', 'bon'); }
          else notifier(`${G.PAYS[adv].nom} refuse : ils pensent pouvoir l'emporter.`, 'mauvais');
          PANNEAUX.armee.maj();
        }));
        if (E.uni[i * G.NUNI + U.ogive] > 0) {
          a.appendChild(bouton('☢️ Frappe nucléaire', 'danger', () => {
            G.confirmer(`Frapper ${G.PAYS[adv].nom} à l'arme nucléaire ?`,
              'Des millions de morts, votre réputation détruite, le monde entier contre vous — ' +
              'et une riposte si l\'adversaire dispose lui aussi de l\'arme.',
              () => { resultat(G.frappeNucleaire(i, adv)); PANNEAUX.armee.maj(); },
              'Lancer la frappe');
          }));
        }
        c.appendChild(a);
        gz.appendChild(c);
      });
    }
  };

  // ─────────────────────────────────────────────── IA
  PANNEAUX.ia = {
    build(d) {
      sectionTitre(d, 'Course à l\'intelligence artificielle',
        'Le calcul se produit dans les centres de données, qui consomment des puces et de l\'électricité. Les puces sortent des fonderies, qui consomment des terres rares. Celui qui tient cette chaîne tient le siècle.');
      const g = el('div', 'grille-tuiles');
      tuile(g, 'Palier atteint', 'i_niv');
      tuile(g, 'Calcul cumulé', 'i_cum');
      tuile(g, 'Calcul produit / jour', 'i_jour');
      tuile(g, 'Centres de données', 'i_dc');
      tuile(g, 'Fonderies de puces', 'i_fo');
      tuile(g, 'Rang mondial', 'i_rang');
      tuile(g, 'Bonus de productivité', 'i_prod');
      tuile(g, 'Bonus militaire', 'i_mil');
      d.appendChild(g);

      const pg = el('div', 'bloc');
      pg.appendChild(el('h3', '', 'Progression vers le palier suivant'));
      jauge(pg, 'Avancement', 'i_prog');
      const nx = el('p', 'sous-titre', ''); pg.appendChild(nx);
      UI.refs.i_next = nx;
      d.appendChild(pg);

      sectionTitre(d, 'Chaîne de valeur');
      const ch = el('div', 'chaine');
      ['💠 Terres rares','🔲 Puces','⚡ Électricité','🖥️ Centres de données','🧠 Calcul'].forEach((x, k, arr) => {
        ch.appendChild(el('div', 'ch-e', x));
        if (k < arr.length - 1) ch.appendChild(el('div', 'ch-fl', '→'));
      });
      d.appendChild(ch);
      const cd = el('div', 'grille-tuiles');
      tuile(cd, 'Terres rares (solde/j)', 'i_tr');
      tuile(cd, 'Puces (solde/j)', 'i_pu');
      tuile(cd, 'Électricité (solde/j)', 'i_el');
      tuile(cd, 'Goulot d\'étranglement', 'i_goulot');
      d.appendChild(cd);

      sectionTitre(d, 'Classement mondial de l\'IA');
      const cl = el('div', 'bloc'); cl.id = 'i-classement'; d.appendChild(cl);
      UI.refs.i_cl = cl;

      sectionTitre(d, 'Paliers');
      const pl = el('div', 'paliers');
      G.PALIERS_IA.forEach(p => {
        const c = el('div', 'palier');
        c.dataset.n = p.n;
        c.innerHTML = `<b>N${p.n} · ${p.nom}</b><span>${nf0.format(p.seuil)} unités de calcul</span><em>${p.bonus}</em>`;
        pl.appendChild(c);
      });
      d.appendChild(pl);
      UI.refs.i_paliers = pl;
    },
    maj() {
      const i = E.joueur, r = UI.refs;
      if (!r.i_niv) return;
      const n = E.ia[i] | 0;
      r.i_niv.textContent = 'N' + n;
      r.i_niv_s.textContent = G.PALIERS_IA[n].nom;
      r.i_cum.textContent = nf0.format(E.calcul[i]);
      const parJour = E.prod[i * G.NRES + R.calcul];
      r.i_jour.textContent = G.fmtNb(parJour);
      r.i_dc.textContent = nf0.format(E.bat[i * G.NBAT + B.datacenter]);
      r.i_fo.textContent = nf0.format(E.bat[i * G.NBAT + B.fonderie]);
      let rang = 1; for (let j = 0; j < G.N; j++) if (E.calcul[j] > E.calcul[i]) rang++;
      r.i_rang.textContent = rang + 'ᵉ';
      r.i_prod.textContent = pct((G.multIA(i) - 1) * 100);
      r.i_mil.textContent = pct(([0,0,0,6,10,14,25,32,40,50,65][n]));

      const suiv = G.PALIERS_IA[Math.min(n + 1, 10)];
      const prec = G.PALIERS_IA[n];
      const av = suiv.seuil > prec.seuil ? (E.calcul[i] - prec.seuil) / (suiv.seuil - prec.seuil) * 100 : 100;
      majJauge('i_prog', clamp(av, 0, 100), 100);
      const reste = Math.max(0, suiv.seuil - E.calcul[i]);
      const jours = parJour > 0 ? Math.ceil(reste / parJour) : Infinity;
      r.i_next.textContent = n >= 10 ? 'Superintelligence atteinte : plus rien au-dessus.'
        : `Prochain palier : N${suiv.n} — ${suiv.nom}. ${nf0.format(reste)} unités manquantes, ` +
          (isFinite(jours) ? `soit ${nf0.format(jours)} jours au rythme actuel.` : 'aucune production de calcul : construisez des centres de données.');

      const so = k => E.prod[i * G.NRES + k] - E.conso[i * G.NRES + k];
      r.i_tr.textContent = (so(R.terresrares) >= 0 ? '+' : '') + G.fmtNb(so(R.terresrares));
      r.i_tr.className = 'tuile-v ' + sig(so(R.terresrares));
      r.i_pu.textContent = (so(R.puces) >= 0 ? '+' : '') + G.fmtNb(so(R.puces));
      r.i_pu.className = 'tuile-v ' + sig(so(R.puces));
      r.i_el.textContent = (so(R.electricite) >= 0 ? '+' : '') + G.fmtNb(so(R.electricite));
      r.i_el.className = 'tuile-v ' + sig(so(R.electricite));
      const pen = [[R.electricite,'Électricité'],[R.puces,'Puces'],[R.terresrares,'Terres rares']]
        .filter(x => E.penurie[i * G.NRES + x[0]] > 0.02);
      r.i_goulot.textContent = pen.length ? pen.map(x => x[1]).join(', ') : (E.bat[i * G.NBAT + B.datacenter] === 0 ? 'Aucun centre de données' : 'Aucun');
      r.i_goulot.className = 'tuile-v ' + (pen.length || E.bat[i * G.NBAT + B.datacenter] === 0 ? 'mauvais' : 'bon');

      Array.from(r.i_paliers.children).forEach(c => c.classList.toggle('atteint', +c.dataset.n <= n));

      if (E.jour % 20 === 0 || !r.i_cl.dataset.f) {
        r.i_cl.dataset.f = 1;
        const ids = Array.from({ length: G.N }, (_, k) => k).sort((a, b) => E.calcul[b] - E.calcul[a]).slice(0, 12);
        r.i_cl.innerHTML = '';
        ids.forEach((k, n2) => {
          const li = el('div', 'rang' + (k === i ? ' moi' : ''));
          li.innerHTML = `<span class="rg-n">${n2 + 1}</span><span class="rg-f">${G.PAYS[k].drapeau}</span>
            <span class="rg-p">${G.PAYS[k].nom}</span><span class="rg-v">N${E.ia[k] | 0} · ${nf0.format(E.calcul[k])}</span>`;
          r.i_cl.appendChild(li);
        });
      }
    }
  };

  // ─────────────────────────────────────────────── RECHERCHE
  PANNEAUX.recherche = {
    build(d) {
      sectionTitre(d, 'Recherche scientifique',
        'Les laboratoires et les universités produisent des points de recherche. L\'IA les multiplie.');
      const g = el('div', 'grille-tuiles');
      tuile(g, 'Points / jour', 'z_jour');
      tuile(g, 'Points accumulés', 'z_pts');
      tuile(g, 'En cours', 'z_cours');
      tuile(g, 'Technologies acquises', 'z_acq');
      d.appendChild(g);
      const gr = el('div', 'grille-bat');
      UI.refs.z_cartes = [];
      G.TECHS.forEach((t, k) => {
        const c = el('div', 'carte-bat tech');
        c.innerHTML = `<div class="cb-h"><span class="cb-i">${t.icone}</span>
          <div class="cb-ht"><div class="cb-n">${t.nom}</div><div class="cb-p">${nf0.format(t.cout)} points</div></div></div>
          <p class="cb-d">${t.effet}</p>
          <div class="cb-e">${t.req.length ? t.req.map(x => `<span class="pastille">Requiert : ${G.TECHS.find(y => y.id === x).nom}</span>`).join('') : '<span class="pastille">Aucun prérequis</span>'}</div>`;
        const f = el('div', 'cb-f');
        const et = el('div', 'cb-c', ''); f.appendChild(et);
        const b = bouton('Lancer', 'principal', () => {
          E.rechCours[E.joueur] = k; notifier(`Recherche lancée : ${t.nom}.`, ''); PANNEAUX.recherche.maj();
        });
        f.appendChild(b); c.appendChild(f);
        gr.appendChild(c);
        UI.refs.z_cartes.push({ k: k, et: et, btn: b, carte: c });
      });
      d.appendChild(gr);
    },
    maj() {
      const i = E.joueur, r = UI.refs, NT = G.TECHS.length;
      if (!r.z_jour) return;
      r.z_jour.textContent = G.fmtNb(E.rechAcc[i]);
      r.z_pts.textContent = nf0.format(E.rech[i]);
      const kc = E.rechCours[i];
      r.z_cours.textContent = kc >= 0 ? G.TECHS[kc].nom : 'Aucune';
      if (kc >= 0) {
        const reste = G.TECHS[kc].cout - E.rech[i];
        r.z_cours_s.textContent = E.rechAcc[i] > 0 ? `${nf0.format(Math.max(0, reste / E.rechAcc[i]))} jours restants` : 'aucun laboratoire';
      } else r.z_cours_s.textContent = '';
      let acq = 0; for (let k = 0; k < NT; k++) if (E.techs[i * NT + k]) acq++;
      r.z_acq.textContent = acq + ' / ' + NT;

      r.z_cartes.forEach(x => {
        const t = G.TECHS[x.k];
        const ok = E.techs[i * NT + x.k];
        const dispo = t.req.every(y => G.aTech(i, y));
        x.carte.classList.toggle('acquise', !!ok);
        if (ok) { x.et.textContent = 'Acquise'; x.btn.textContent = '✓'; x.btn.disabled = true; x.btn.className = 'btn off'; }
        else if (!dispo) { x.et.textContent = 'Prérequis manquants'; x.btn.disabled = true; x.btn.className = 'btn off'; x.btn.textContent = 'Verrouillé'; }
        else if (kc === x.k) { x.et.textContent = `En cours — ${nf0.format(E.rech[i])} / ${nf0.format(t.cout)}`; x.btn.disabled = true; x.btn.className = 'btn off'; x.btn.textContent = 'En cours'; }
        else { x.et.textContent = `${nf0.format(t.cout)} points`; x.btn.disabled = false; x.btn.className = 'btn principal'; x.btn.textContent = 'Lancer'; }
      });
    }
  };

  // ─────────────────────────────────────────────── POLITIQUE
  PANNEAUX.politique = {
    build(d) {
      const p = G.PAYS[E.joueur];
      sectionTitre(d, 'Politique intérieure',
        p.reg === 'D' ? 'Vous êtes élu. Tous les cinq ans, le peuple tranche : sous 45 % d\'approbation, la partie s\'arrête.'
                      : 'Vous n\'êtes pas élu. Mais une stabilité trop faible amène l\'armée à la porte du palais.');
      const g = el('div', 'grille-tuiles');
      tuile(g, 'Approbation', 'q_app');
      tuile(g, 'Stabilité', 'q_stab');
      tuile(g, 'Corruption', 'q_corr');
      tuile(g, 'Prochaine échéance', 'q_elec');
      d.appendChild(g);

      sectionTitre(d, 'Lois et doctrines', 'Activables et révocables à tout moment. Chacune a un prix.');
      const gr = el('div', 'grille-bat');
      UI.refs.q_lois = [];
      G.LOIS.forEach(l => {
        const c = el('div', 'carte-bat');
        c.innerHTML = `<div class="cb-h"><span class="cb-i">${l.icone}</span>
          <div class="cb-ht"><div class="cb-n">${l.nom}</div><div class="cb-p">${l.effets}</div></div></div>`;
        const f = el('div', 'cb-f');
        const b = bouton('Promulguer', 'principal', () => {
          if (E.lois.has(l.id)) { E.lois.delete(l.id); notifier(`${l.nom} abrogée.`, ''); }
          else { E.lois.add(l.id); notifier(`${l.nom} promulguée.`, 'bon'); }
          PANNEAUX.politique.maj();
        });
        f.appendChild(el('div', 'cb-c', ''));
        f.appendChild(b); c.appendChild(f);
        gr.appendChild(c);
        UI.refs.q_lois.push({ id: l.id, btn: b, carte: c });
      });
      d.appendChild(gr);
    },
    maj() {
      const i = E.joueur, r = UI.refs;
      if (!r.q_app) return;
      r.q_app.textContent = nf0.format(E.approb[i]) + ' %';
      r.q_app.className = 'tuile-v ' + (E.approb[i] > 55 ? 'bon' : E.approb[i] < 40 ? 'mauvais' : '');
      r.q_stab.textContent = nf0.format(E.stab[i]) + ' %';
      r.q_stab.className = 'tuile-v ' + (E.stab[i] > 55 ? 'bon' : E.stab[i] < 30 ? 'mauvais' : '');
      r.q_corr.textContent = nf0.format(E.corrupt[i]) + ' %';
      r.q_corr.className = 'tuile-v ' + (E.corrupt[i] < 25 ? 'bon' : E.corrupt[i] > 50 ? 'mauvais' : '');
      if (G.PAYS[i].reg === 'D') {
        const reste = 1825 - (E.jour % 1825);
        r.q_elec.textContent = nf0.format(reste) + ' jours';
        r.q_elec_s.textContent = 'Élection présidentielle · ' + G.dateDe(E.jour + reste);
      } else {
        r.q_elec.textContent = 'Aucune';
        r.q_elec_s.textContent = 'Régime non électif';
      }
      r.q_lois.forEach(x => {
        const on = E.lois.has(x.id);
        x.carte.classList.toggle('acquise', on);
        x.btn.textContent = on ? 'Abroger' : 'Promulguer';
        x.btn.className = 'btn ' + (on ? 'danger' : 'principal');
      });
    }
  };

  // ─────────────────────────────────────────────── CLASSEMENTS
  PANNEAUX.classements = {
    build(d) {
      sectionTitre(d, 'Classements mondiaux', 'Votre position dans le concert des nations, mise à jour en continu.');
      const g = el('div', 'grille-classements'); g.id = 'l-g'; d.appendChild(g);
      UI.refs.l_g = g;
    },
    maj() {
      const g = UI.refs.l_g, i = E.joueur;
      if (!g) return;
      if (g.dataset.t == (E.jour / 15 | 0)) return;
      g.dataset.t = (E.jour / 15 | 0);
      const cats = [
        ['💵 Produit intérieur brut', j => E.pib[j], v => G.fmtMd(v)],
        ['👤 PIB par habitant', j => E.pib[j] * 1e9 / Math.max(E.pop[j], 1), v => nf0.format(v) + ' $'],
        ['⚔️ Puissance militaire', j => G.puissance(j, true), v => nf0.format(v / 1000) + ' k'],
        ['🧠 Course à l\'IA', j => E.calcul[j], v => nf0.format(v)],
        ['🔬 Technologie', j => E.tech[j], v => nf1.format(v)],
        ['🕊️ Réputation', j => E.reput[j], v => nf0.format(v)],
        ['😊 Approbation', j => E.approb[j], v => nf0.format(v) + ' %'],
        ['👥 Population', j => E.pop[j], v => G.fmtPop(v)]
      ];
      g.innerHTML = '';
      cats.forEach(c => {
        const bloc = el('div', 'classement');
        bloc.appendChild(el('h3', '', c[0]));
        const ids = Array.from({ length: G.N }, (_, k) => k).sort((a, b) => c[1](b) - c[1](a));
        const monRang = ids.indexOf(i) + 1;
        const liste = ids.slice(0, 10);
        if (monRang > 10) liste.push(i);
        liste.forEach((k) => {
          const n = ids.indexOf(k) + 1;
          const li = el('div', 'rang' + (k === i ? ' moi' : ''));
          li.innerHTML = `<span class="rg-n">${n}</span><span class="rg-f">${G.PAYS[k].drapeau}</span>
            <span class="rg-p">${G.PAYS[k].nom}</span><span class="rg-v">${c[2](c[1](k))}</span>`;
          bloc.appendChild(li);
        });
        g.appendChild(bloc);
      });
    }
  };

  // ─────────────────────────────────────────────── JOURNAL
  PANNEAUX.journal = {
    build(d) {
      sectionTitre(d, 'Journal de la présidence', 'Tout ce qui s\'est passé depuis votre entrée en fonction.');
      const l = el('div', 'journal'); l.id = 'j-l'; d.appendChild(l);
      UI.refs.j_l = l;
    },
    maj() {
      const l = UI.refs.j_l;
      if (!l) return;
      if (l.dataset.n == E.journal.length) return;
      l.dataset.n = E.journal.length;
      l.innerHTML = '';
      E.journal.slice(0, 120).forEach(x => {
        const c = el('div', 'jl ' + x.type);
        c.innerHTML = `<span class="jl-i">${x.icone || '•'}</span><span class="jl-d">${x.d}</span><span class="jl-t">${x.txt}</span>`;
        l.appendChild(c);
      });
    }
  };

  PANNEAUX.defis = {
    build(d) {
      sectionTitre(d, 'Défis',
        'Treize objectifs, du plus accessible au plus lointain. En accomplir un ne met jamais fin à la partie : ' +
        'vous notez le résultat et vous continuez à gouverner. Chaque défi relevé vaut 1 500 points de score.');
      const g = el('div', 'grille-bat'); d.appendChild(g);
      UI.refs.x_cartes = [];
      G.DEFIS.forEach(x => {
        const c = el('div', 'carte-bat');
        c.innerHTML = `<div class="cb-h"><span class="cb-i">${x.icone}</span>
          <div class="cb-ht"><div class="cb-n">${x.nom}${x.majeur ? ' <span class="pastille">majeur</span>' : ''}</div></div></div>
          <p class="cb-d">${x.desc}</p>`;
        jauge(c, 'Progression', 'x_' + x.id);
        g.appendChild(c);
        UI.refs.x_cartes.push({ d: x, carte: c });
      });
    },
    maj() {
      const i = E.joueur;
      if (!UI.refs.x_cartes) return;
      UI.refs.x_cartes.forEach(x => {
        const fait = G.defiFait(x.d.id);
        x.carte.classList.toggle('acquise', fait);
        const p = fait ? 1 : (x.d.progres ? x.d.progres(E, i) : 0);
        majJauge('x_' + x.d.id, clamp(p * 100, 0, 100), 100);
      });
    }
  };

  PANNEAUX.carte = { build() {}, maj() {} };

  function reconstruire(id) { UI.construits = {}; ouvrir(id); }

  // ══════════════════════════════════════════════════════ Modales
  function modale(html, boutons, cls) {
    const m = q('#modale');
    m.className = 'modale ouvert ' + (cls || '');
    m.innerHTML = '';
    const box = el('div', 'modale-box');
    box.innerHTML = html;
    const a = el('div', 'modale-a');
    boutons.forEach(b => a.appendChild(bouton(b[0], b[2] || 'principal', () => { m.classList.remove('ouvert'); b[1](); })));
    box.appendChild(a);
    m.appendChild(box);
  }

  function modaleEvenement() {
    const ev = E.evenement;
    modale(`<div class="mo-i">${ev.icone}</div><h2>${ev.titre}</h2><p>${ev.texte}</p>`,
      ev.choix.map((c, k) => [c.txt, () => { G.repondreEvenement(k); E.pause = false; majVitesse(); }, k === 0 ? 'principal' : 'sec']),
      'evenement');
  }

  function modaleONU() {
    const s = E.onu.sujet;
    modale(`<div class="mo-i">🕊️</div><h2>Assemblée générale des Nations unies</h2>
      <p>Résolution soumise au vote : <b>${s.txt}</b></p><p class="sous-titre">${s.pour}</p>`,
      [['Voter pour', () => G.voterONU(true), 'principal'],
       ['Voter contre', () => G.voterONU(false), 'sec'],
       ['S\'abstenir', () => { E.onu = null; }, 'sec']]);
  }

  function modaleCapitulation() {
    const c = E.capitulation, p = G.PAYS[c.vaincu];
    modale(`<div class="mo-i">🏳️</div><h2>${p.nom} capitule</h2>
      <p>Leur gouvernement demande vos conditions. Ce que vous choisirez ici, le monde entier le verra.</p>`,
      [['Annexer le pays', () => { G.appliquerCapitulation(c.vainqueur, c.vaincu, 'annexion'); E.capitulation = null; E.pause = false; majVitesse(); }, 'danger'],
       ['Imposer un tribut', () => { G.appliquerCapitulation(c.vainqueur, c.vaincu, 'tribut'); E.capitulation = null; E.pause = false; majVitesse(); }, 'principal'],
       ['Paix magnanime', () => { G.appliquerCapitulation(c.vainqueur, c.vaincu, 'paix'); E.capitulation = null; E.pause = false; majVitesse(); }, 'sec']]);
  }

  function modaleDefi() {
    const d = E.defisQueue.shift();
    const restants = G.DEFIS.filter(x => !G.defiFait(x.id));
    const suivant = restants.sort((a, b) => (b.progres ? b.progres(E, E.joueur) : 0) - (a.progres ? a.progres(E, E.joueur) : 0))[0];
    modale(`<div class="mo-i">${d.icone}</div><h2>Défi accompli</h2>
      <p><b>${d.nom}</b> — ${d.desc}</p>
      <p class="sous-titre">${restants.length
        ? `Il vous reste ${restants.length} défi${restants.length > 1 ? 's' : ''} à relever.` +
          (suivant ? ` Le plus proche : <b>${suivant.nom}</b>, ${nf0.format((suivant.progres ? suivant.progres(E, E.joueur) : 0) * 100)} % du chemin parcouru.` : '')
        : 'Vous les avez tous relevés. Le monde n\'a plus rien à vous apprendre — reste à durer.'}</p>`,
      [['Continuer à gouverner', () => { if (!E.defisQueue.length) { E.pause = false; majVitesse(); } }, 'principal'],
       ['Voir mes défis', () => { ouvrir('defis'); }, 'sec']], 'fin');
  }

  function modaleFin() {
    const f = E.fini;
    const i = E.joueur;
    modale(`<div class="mo-i">${f.type === 'victoire' ? '🏆' : '💀'}</div>
      <h2>${f.type === 'victoire' ? 'Victoire' : 'Fin de mandat'}</h2>
      <p>${f.msg}</p>
      <div class="mo-bilan">
        <div><span>Durée</span><b>${nf0.format(f.jour / 365)} ans</b></div>
        <div><span>PIB final</span><b>${G.fmtMd(E.pib[i])}</b></div>
        <div><span>Niveau d'IA</span><b>N${E.ia[i] | 0}</b></div>
        <div><span>Approbation</span><b>${nf0.format(E.approb[i])} %</b></div>
        <div><span>Score</span><b>${nf0.format(E.score)}</b></div>
        <div><span>Défis relevés</span><b>${E.defisFaits.length} / ${G.DEFIS.length}</b></div>
      </div>`,
      [['Choisir une autre nation', () => G.retourAccueil(), 'principal'],
       ['Rejouer ' + G.PAYS[i].nom, () => {
         const code = G.PAYS[i].code;
         G.nouvellePartie(code); G.appliquerGeopolitique();
         q('#b-drapeau').textContent = G.PAYS[E.joueur].drapeau;
         q('#b-nom').textContent = G.PAYS[E.joueur].nom;
         UI.construits = {}; UI.refs = {};
         q('#contenu').innerHTML = '';
         UI.enJeu = true; ouvrir('carte'); majBarre(); majVitesse();
       }, 'sec']], 'fin');
  }

  // ══════════════════════════════════════════════════════ Contrôles globaux
  G.stockageDispo = function () {
    try { localStorage.setItem('geopolis-test', '1'); localStorage.removeItem('geopolis-test'); return true; }
    catch (e) { return false; }
  };

  G.sauverLocal = function (silencieux) {
    try {
      localStorage.setItem('geopolis-save', G.sauver());
      if (!silencieux) notifier('Partie sauvegardée dans ce navigateur.', 'bon');
      return true;
    } catch (e) {
      if (!silencieux) notifier('Ce navigateur refuse le stockage. Téléchargez plutôt le fichier de sauvegarde.', 'mauvais');
      return false;
    }
  };

  G.telechargerSauvegarde = function () {
    const p = G.PAYS[E.joueur];
    const blob = new Blob([G.sauver()], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `geopolis-${p.code}-an${Math.floor(E.jour / 365) + 1}.json`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    notifier('Fichier de sauvegarde téléchargé. Gardez-le : il rouvre la partie où qu\'elle soit.', 'bon');
  };

  G.chargerFichier = function (auDemarrage) {
    const input = document.createElement('input');
    input.type = 'file'; input.accept = '.json,application/json';
    input.onchange = () => {
      const f = input.files[0];
      if (!f) return;
      const lecteur = new FileReader();
      lecteur.onload = () => {
        try {
          G.charger(lecteur.result);
          if (auDemarrage) auDemarrage();
          else { UI.construits = {}; ouvrir('carte'); majBarre(); majVitesse(); }
          notifier(`Partie reprise : ${G.PAYS[E.joueur].nom}, ${Math.floor(E.jour / 365)} an(s) de mandat.`, 'bon');
        } catch (e) { notifier('Fichier illisible : ' + e.message, 'mauvais'); }
      };
      lecteur.readAsText(f);
    };
    input.click();
  };

  G.brancherControles = function () {
    q('#btn-pause').onclick = basculerPause;
    document.querySelectorAll('.vit').forEach(b => b.onclick = () => { E.pause = false; E.vitesse = +b.dataset.v; majVitesse(); });
    q('#btn-sauver').onclick = () => {
      if (!G.sauverLocal(false)) G.telechargerSauvegarde();
    };
    q('#btn-fichier').onclick = () => G.telechargerSauvegarde();
    q('#btn-ouvrir').onclick = () => G.chargerFichier();
    if (!G.stockageDispo())
      notifier('Ce navigateur bloque la sauvegarde automatique. Utilisez ⬇ pour télécharger votre partie.', 'mauvais');
    q('#btn-menu').onclick = () => {
      G.confirmer('Quitter la partie ?',
        'Vous reviendrez au choix des nations. Votre partie est sauvegardée automatiquement, ' +
        'mais vous pouvez aussi la télécharger avec le bouton ⬇ avant de partir.',
        () => G.retourAccueil(), 'Revenir au menu');
    };
    majVitesse();
  };
})(window.GEO = window.GEO || {});
