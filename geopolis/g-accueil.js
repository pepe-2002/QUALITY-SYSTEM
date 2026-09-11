/* GÉOPOLIS — Écran d'accueil et sélection de la nation */
(function (G) {
  'use strict';

  const q = s => document.querySelector(s);
  const nf0 = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });
  let choisi = -1, selectionnee = null;

  function difficulte(p) {
    const s = Math.log10(Math.max(p.pib, 0.1)) * 22 + p.tech * 0.45 + p.stab * 0.25 + p.arm * 0.2;
    if (s > 105) return { n: 1, t: 'Confortable', c: 'd1' };
    if (s > 82)  return { n: 2, t: 'Équilibrée',  c: 'd2' };
    if (s > 62)  return { n: 3, t: 'Exigeante',   c: 'd3' };
    if (s > 45)  return { n: 4, t: 'Difficile',   c: 'd4' };
    return { n: 5, t: 'Extrême', c: 'd5' };
  }

  function construire() {
    const rech = (q('#acc-rech').value || '').toLowerCase().trim();
    const tri = q('#acc-tri').value;
    const cont = q('#acc-cont').value;
    const g = q('#acc-grille');

    let ids = [];
    for (let i = 0; i < G.N; i++) {
      const p = G.PAYS[i];
      if (cont && p.cont !== cont) continue;
      if (rech && p.nom.toLowerCase().indexOf(rech) < 0 && p.code.toLowerCase().indexOf(rech) < 0) continue;
      ids.push(i);
    }
    const tris = {
      pib: (a, b) => G.PAYS[b].pib - G.PAYS[a].pib,
      pop: (a, b) => G.PAYS[b].pop - G.PAYS[a].pop,
      arm: (a, b) => G.PAYS[b].arm - G.PAYS[a].arm,
      nom: (a, b) => G.PAYS[a].nom.localeCompare(G.PAYS[b].nom),
      def: (a, b) => difficulte(G.PAYS[a]).n - difficulte(G.PAYS[b]).n
    };
    ids.sort(tris[tri]);

    g.innerHTML = '';
    selectionnee = null;
    const frag = document.createDocumentFragment();
    ids.forEach(i => {
      const p = G.PAYS[i], d = difficulte(p);
      const c = document.createElement('button');
      c.className = 'acc-c' + (i === choisi ? ' actif' : '');
      if (i === choisi) selectionnee = c;
      c.innerHTML = `
        <span class="ac-f">${p.drapeau}</span>
        <span class="ac-n">${p.nom}</span>
        <span class="ac-d ${d.c}">${d.t}</span>
        <span class="ac-s">
          <i><b>${p.pib >= 1000 ? (p.pib / 1000).toFixed(1) + ' T$' : nf0.format(p.pib) + ' Md$'}</b>PIB</i>
          <i><b>${p.pop >= 1e6 ? (p.pop / 1e6).toFixed(p.pop >= 1e7 ? 0 : 1) + ' M' : nf0.format(p.pop / 1e3) + ' k'}</b>habitants</i>
          <i><b>${nf0.format(p.tech)}</b>techno</i>
          <i><b>${nf0.format(p.arm)}</b>armée</i>
        </span>`;
      c.onclick = () => {
        if (selectionnee) selectionnee.classList.remove('actif');
        selectionnee = c;
        c.classList.add('actif');
        choisi = i;
        majSelection();
      };
      frag.appendChild(c);
    });
    g.appendChild(frag);
    if (!ids.length) g.innerHTML = '<div class="vide">Aucun pays ne correspond à cette recherche.</div>';
  }

  function majSelection() {
    const s = q('#acc-sel'), b = q('#acc-jouer');
    if (choisi < 0) {
      s.textContent = 'Choisissez une nation ci-dessus';
      b.disabled = true;
      b.textContent = 'Prendre le pouvoir';
      return;
    }
    const p = G.PAYS[choisi], d = difficulte(p);
    b.textContent = `Prendre le pouvoir — ${p.drapeau} ${p.nom}`;
    const dot = p.dot;
    const noms = ['pétrole','gaz','charbon','fer','cuivre','terres rares','uranium','or','agriculture'];
    const riches = noms.filter((_, k) => dot[k] >= 5);
    s.innerHTML = `<b>${p.drapeau} ${p.nom}</b> — partie <b class="${d.c}">${d.t.toLowerCase()}</b>.
      ${riches.length ? 'Richesses du sous-sol : ' + riches.join(', ') + '.' : 'Peu de ressources naturelles : votre avenir passera par l\'industrie, les services ou l\'IA.'}`;
    b.disabled = false;
  }

  window.addEventListener('DOMContentLoaded', () => {
    G.ajusterHauteur();
    window.addEventListener('resize', G.ajusterHauteur);
    window.addEventListener('orientationchange', () => setTimeout(G.ajusterHauteur, 250));
    q('#acc-rech').oninput = construire;
    q('#acc-tri').onchange = construire;
    q('#acc-cont').onchange = construire;
    construire();

    q('#acc-jouer').onclick = () => {
      if (choisi < 0) return;
      G.nouvellePartie(G.PAYS[choisi].code);
      G.appliquerGeopolitique();
      G.amorcerDefis();
      lancer();
    };

    q('#acc-charger').onclick = () => G.chargerFichier(lancer);
    G.rafraichirAccueil();
  });

  G.rafraichirAccueil = function () {
    choisi = -1; selectionnee = null;
    // On repart d'une liste complète : en revenant au menu, le filtre de la
    // partie précédente ne laissait voir qu'un seul pays.
    q('#acc-rech').value = '';
    construire();
    majSelection();

    // La partie sauvegardée est présentée à part, tout en haut, et jamais
    // à côté du bouton qui lance une nouvelle partie.
    const carte = q('#acc-partie');
    let save = null;
    try { save = localStorage.getItem('geopolis-save'); } catch (e) { /* stockage bloqué */ }
    if (!save) { carte.classList.add('cache'); return; }
    let etiquette = 'partie sauvegardée';
    try {
      const s = JSON.parse(save);
      const an = Math.floor(s.jour / 365);
      etiquette = `${G.PAYS[s.joueur].drapeau} ${G.PAYS[s.joueur].nom} — ${an ? an + ' an' + (an > 1 ? 's' : '') + ' de mandat' : 'mandat commencé'}`;
    } catch (e) { /* étiquette par défaut */ }
    q('#acc-partie-nom').textContent = etiquette;
    carte.classList.remove('cache');
    q('#acc-reprendre').onclick = () => {
      try { G.charger(save); lancer(); }
      catch (e) { G.notifier('Sauvegarde illisible : ' + e.message, 'mauvais'); }
    };
    q('#acc-effacer').onclick = () => {
      try { localStorage.removeItem('geopolis-save'); } catch (e) { /* stockage bloqué */ }
      carte.classList.add('cache');
    };
  };

  function lancer() {
    const p = G.PAYS[G.E.joueur];
    q('#b-drapeau').textContent = p.drapeau;
    q('#b-nom').textContent = p.nom;
    document.title = `GÉOPOLIS — ${p.nom}`;
    G.demarrer();
    G.brancherControles();
  }

  // Service worker : le jeu fonctionne hors ligne une fois chargé
  if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }
})(window.GEO = window.GEO || {});
