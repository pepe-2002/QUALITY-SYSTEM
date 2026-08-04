/* ═══════════════════════════════════════════════════════════
   KODO — l'école qui se joue
   Moteur de jeu + interface. Tout tient en local, hors ligne.
   ═══════════════════════════════════════════════════════════ */
(function () {
'use strict';

const COURS = window.KODO_COURS || [];
const CLE = 'kodo_partie_v1';

/* ─────────── Réglages d'équilibre ─────────── */
const R = {
  argentDepart: 300000,
  energieMax: 5,
  revenuParUser: 25,          // FC / utilisateur / jour
  coutServeurJour: 6000,
  coutEmployeJour: 30000,
  capaciteServeur: 1500,      // utilisateurs supportés par serveur
  prixServeur: 250000,
  prixEmploye: 150000,
  prixPub: 80000,
  objectif: 25000,            // utilisateurs pour gagner
  paliers: [
    { seuil: 0,     nom: 'Chambre' },
    { seuil: 1000,  nom: 'Bureau' },
    { seuil: 5000,  nom: 'Agence' },
    { seuil: 12000, nom: 'Studio' },
    { seuil: 25000, nom: 'Groupe' }
  ]
};

/* ─────────── Catalogue de contrats ─────────── */
const CONTRATS = [
  { t:"Page de présentation d'un lodge", cli:"Lodge Ylang, Nioumachoua", br:'web', niv:0, travail:2, paie:120000, users:90 },
  { t:"Carte de visite numérique",       cli:"Taxi Hassani",             br:'web', niv:0, travail:2, paie:100000, users:60 },
  { t:"Calculateur de tarifs",           cli:"Coopérative des pêcheurs", br:'code',niv:1, travail:3, paie:190000, users:140 },
  { t:"Formulaire de commande en ligne", cli:"Boulangerie Fomboni",      br:'web', niv:1, travail:3, paie:210000, users:180 },
  { t:"Gestion de stock au comptoir",    cli:"Quincaillerie Mitsamiouli",br:'code',niv:2, travail:4, paie:340000, users:260 },
  { t:"Espace client avec comptes",      cli:"Auto-école Moroni",        br:'web', niv:2, travail:4, paie:390000, users:420 },
  { t:"Sauvegarde et mise en ligne",     cli:"Clinique de Fomboni",      br:'serveur', niv:1, travail:3, paie:260000, users:150 },
  { t:"Diagnostic d'un site en panne",   cli:"Radio Mwezi",              br:'serveur', niv:2, travail:4, paie:430000, users:300 },
  { t:"Passage en haute disponibilité",  cli:"Groupe hôtelier Itsandra", br:'serveur', niv:3, travail:6, paie:820000, users:1400 },
  { t:"Météo mer branchée sur une API",  cli:"Compagnie maritime",       br:'ia',  niv:1, travail:3, paie:280000, users:340 },
  { t:"Suivi de livraison temps réel",   cli:"Transit Anjouan",          br:'ia',  niv:1, travail:4, paie:360000, users:480 },
  { t:"Assistant de réponse aux clients",cli:"Banque de la place",       br:'ia',  niv:2, travail:5, paie:640000, users:1100 },
  { t:"Tri automatique des réclamations",cli:"Opérateur télécom",        br:'ia',  niv:3, travail:7, paie:1250000, users:3200 },
  { t:"Refonte complète de la plateforme",cli:"Office du tourisme",      br:'web', niv:3, travail:7, paie:980000, users:2400 },
  { t:"Moteur de recherche interne",     cli:"Ministère de l'éducation", br:'code',niv:3, travail:8, paie:1400000, users:4000 },
  { t:"Application de caisse hors ligne",cli:"Chaîne de supérettes",     br:'code',niv:2, travail:5, paie:520000, users:700 },
  // — niveau 4 : les gros dossiers —
  { t:"Audit et reprise d'un code en panne", cli:"Régie des transports",  br:'code',niv:4, travail:9,  paie:1900000, users:5200 },
  { t:"Portail national allégé pour la 3G",  cli:"Administration des Comores", br:'web', niv:4, travail:9, paie:2100000, users:6400 },
  { t:"Base de données centrale des patients", cli:"Réseau de santé",     br:'serveur', niv:4, travail:10, paie:2400000, users:7000 },
  { t:"Assistant branché sur la documentation", cli:"Compagnie d'assurance", br:'ia', niv:4, travail:10, paie:2600000, users:8000 },
  // — niveau 5 : on ne construit plus, on tient debout —
  { t:"Suite de tests sur un code sans filet", cli:"Éditeur de logiciel",   br:'code',niv:5, travail:11, paie:3200000, users:9000 },
  { t:"Refonte des formulaires d'inscription", cli:"Université des Comores", br:'web', niv:5, travail:11, paie:3400000, users:10000 },
  { t:"Surveillance et astreinte 24 h",       cli:"Opérateur de paiement",  br:'serveur', niv:5, travail:12, paie:3800000, users:11000 },
  { t:"Maîtrise du budget IA d'un service",   cli:"Plateforme régionale",   br:'ia',  niv:5, travail:12, paie:4000000, users:12000 },
  // — niveau 6 : les dossiers qu'on ne confie qu'aux gens sûrs —
  { t:"Reprise d'un projet abandonné",        cli:"Groupe agroalimentaire", br:'code',niv:6, travail:14, paie:5200000, users:15000 },
  { t:"Audit de sécurité du site public",     cli:"Banque centrale",        br:'web', niv:6, travail:14, paie:5800000, users:16000 },
  { t:"Comptes et droits de 40 000 agents",   cli:"Fonction publique",      br:'serveur', niv:6, travail:15, paie:6500000, users:18000 },
  { t:"Évaluation d'un assistant en service", cli:"Opérateur télécom",      br:'ia',  niv:6, travail:15, paie:7000000, users:20000 }
];

/* ─────────── État ─────────── */
let S = null;
let vue = 'bureau';

function neuf() {
  return {
    jour: 1, argent: R.argentDepart, energie: R.energieMax,
    users: 0, reput: 50,
    fait: {},                 // id de leçon -> true
    contrats: [], offres: [],
    serveurs: 1, employes: 0,
    maintenanceAujourdhui: false,
    journal: [], fini: false, victoire: false,
    prospecte: 0
  };
}
function sauver() { try { localStorage.setItem(CLE, JSON.stringify(S)); } catch (e) {} }
function charger() { try { const b = localStorage.getItem(CLE); return b ? JSON.parse(b) : null; } catch (e) { return null; } }

/* ─────────── Outils ─────────── */
const $ = s => document.querySelector(s);
const esc = t => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const fc = n => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ') + ' FC';
const nb = n => Math.round(n).toLocaleString('fr-FR').replace(/ | /g, ' ');

function toast(txt, genre) {
  const d = document.createElement('div');
  d.className = 'toast' + (genre ? ' ' + genre : '');
  d.textContent = txt;
  $('#toasts').appendChild(d);
  setTimeout(() => { d.style.transition = 'opacity .3s'; d.style.opacity = '0';
    setTimeout(() => d.remove(), 300); }, 2600);
}
function noter(txt) {
  S.journal.unshift({ j: S.jour, t: txt });
  if (S.journal.length > 40) S.journal.pop();
}

/* Le contenu des blocs `code` est réécrit proprement, quelles que soient
   les entités HTML utilisées dans la source du cours. */
function bloc(t) {
  const brut = String(t).replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
  return '<pre>' + esc(brut) + '</pre>';
}

/* ─────────── Compétences ─────────── */
function branche(id) { return COURS.find(b => b.id === id); }
function niveau(brId) {
  const b = branche(brId);
  if (!b) return 0;
  return b.lecons.filter(l => S.fait[l.id]).length;
}
function niveauTotal() { return COURS.reduce((s, b) => s + niveau(b.id), 0); }
function capacite() { return S.serveurs * R.capaciteServeur; }
function palier() {
  let p = R.paliers[0];
  for (const x of R.paliers) if (S.users >= x.seuil) p = x;
  return p.nom;
}
function pointsDev() { return 1 + niveau('code') + niveau('web') + S.employes; }

/* ═══════════════════════════════════════════════════════════
   RENDU — barre du haut
   ═══════════════════════════════════════════════════════════ */
function rendreHud() {
  $('#hudStats').innerHTML = `
    <div class="st"><b>${S.jour}</b><span>Jour</span></div>
    <div class="st eng"><b>${'●'.repeat(S.energie)}${'○'.repeat(R.energieMax - S.energie)}</b><span>Énergie</span></div>
    <div class="st fc"><b>${nb(S.argent)}</b><span>Francs</span></div>
    <div class="st us"><b>${nb(S.users)}</b><span>Clients</span></div>
    <div class="st rp"><b>${S.reput}</b><span>Réput.</span></div>`;
}

/* ═══════════════════════════════════════════════════════════
   VUE — BUREAU
   ═══════════════════════════════════════════════════════════ */
function vueBureau() {
  const surcharge = S.users > capacite();
  let h = '';

  h += `<div class="carte" style="display:flex;justify-content:space-between;align-items:center">
    <div><b style="font-size:15px">${palier()}</b>
      <div class="sous">${nb(S.users)} / ${nb(capacite())} clients supportés
      ${surcharge ? ' — <span style="color:#FCA5A5;font-weight:700">saturé !</span>' : ''}</div>
    </div>
    <div style="text-align:right"><b style="font-size:15px;color:var(--cyan)">${pointsDev()}</b>
      <div class="sous">dév. / action</div></div>
  </div>`;

  h += `<div class="actions">
    <button class="act" data-act="dev" ${S.energie < 1 || !S.contrats.length ? 'disabled' : ''}>
      <div class="t"><i>⌨</i>Développer</div>
      <div class="d">Avancer les contrats en cours</div>
      <div class="c">1 énergie · +${pointsDev()}</div></button>
    <button class="act" data-act="prospect" ${S.energie < 1 ? 'disabled' : ''}>
      <div class="t"><i>☏</i>Prospecter</div>
      <div class="d">Trouver de nouveaux clients</div>
      <div class="c">1 énergie</div></button>
    <button class="act" data-act="maint" ${S.energie < 1 || S.maintenanceAujourdhui ? 'disabled' : ''}>
      <div class="t"><i>⚙</i>Maintenance</div>
      <div class="d">${S.maintenanceAujourdhui ? 'Déjà faite aujourd\'hui' : 'Éviter la panne du jour'}</div>
      <div class="c">1 énergie</div></button>
    <button class="act" data-act="pub" ${S.energie < 1 || S.argent < R.prixPub ? 'disabled' : ''}>
      <div class="t"><i>◈</i>Faire de la pub</div>
      <div class="d">Attirer de nouveaux clients</div>
      <div class="c">1 énergie · ${nb(R.prixPub)} FC</div></button>
    <button class="act" data-act="ecole">
      <div class="t"><i>✦</i>Étudier</div>
      <div class="d">Apprendre pour débloquer</div>
      <div class="c">1 énergie / leçon</div></button>
    <button class="act" data-act="dormir">
      <div class="t"><i>☾</i>Fin de journée</div>
      <div class="d">Encaisser, payer, recommencer</div>
      <div class="c">Énergie au maximum</div></button>
  </div>`;

  h += `<div class="titre-sec">Contrats en cours</div>`;
  if (!S.contrats.length) {
    h += `<div class="carte sous">Aucun contrat signé. Prospecte pour trouver des clients — mais un contrat ne s'accepte que si tu as la compétence qu'il demande.</div>`;
  } else {
    for (const c of S.contrats) {
      const pct = Math.min(100, Math.round(c.avance / c.travail * 100));
      h += `<div class="contrat">
        <div class="haut"><div><h4>${esc(c.t)}</h4><div class="cli">${esc(c.cli)}</div></div>
        <div class="paie">${nb(c.paie)} FC</div></div>
        <div class="jauge"><i style="width:${pct}%"></i></div>
        <div class="sous" style="margin-top:6px;font-size:11.5px">${c.avance} / ${c.travail} points de développement${pct === 100 ? ' — prêt à livrer' : ''}</div>
        ${pct === 100 ? `<button class="btn vert mini" style="margin-top:9px" data-livrer="${c.uid}">Livrer le projet</button>` : ''}
      </div>`;
    }
  }

  h += `<div class="titre-sec">Offres disponibles</div>`;
  if (!S.offres.length) {
    h += `<div class="carte sous">Rien pour l'instant. Utilise « Prospecter ».</div>`;
  } else {
    for (const o of S.offres) {
      const b = branche(o.br);
      const ok = niveau(o.br) >= o.niv;
      h += `<div class="contrat ${ok ? '' : 'verrou'}">
        <div class="haut"><div><h4>${esc(o.t)}</h4><div class="cli">${esc(o.cli)}</div></div>
        <div class="paie">${nb(o.paie)} FC</div></div>
        <div class="badges">
          <span class="bdg ${ok ? 'ok' : 'no'}">${esc(b.nom)} niveau ${o.niv}${ok ? '' : ' — manquant'}</span>
          <span class="bdg">${o.travail} pts de dév.</span>
          <span class="bdg">+${nb(o.users)} clients</span>
        </div>
        <button class="btn ${ok ? 'plein' : ''} mini" style="margin-top:10px" data-signer="${o.uid}" ${ok ? '' : 'disabled'}>
          ${ok ? 'Signer' : 'Apprends d\'abord ' + esc(b.nom) + ' niveau ' + o.niv}</button>
      </div>`;
    }
  }
  return h;
}

/* ═══════════════════════════════════════════════════════════
   VUE — ÉCOLE
   ═══════════════════════════════════════════════════════════ */
function vueEcole() {
  let h = `<div class="carte sous">Chaque leçon coûte <b>1 énergie</b> et se termine par des exercices corrigés. Une leçon réussie = un niveau de plus dans sa branche, et de nouveaux contrats accessibles.</div>`;
  for (const b of COURS) {
    h += `<div class="branche">
      <div class="branche-tete">
        <div class="branche-sig" style="background:${b.couleur}22;color:${b.couleur};border:1px solid ${b.couleur}55">${esc(b.sigle)}</div>
        <div><h3>${esc(b.nom)}</h3><p>${esc(b.pitch)} · niveau ${niveau(b.id)}/${b.lecons.length}</p></div>
      </div>`;
    b.lecons.forEach((l, i) => {
      const fini = !!S.fait[l.id];
      const ouvert = i === 0 || S.fait[b.lecons[i - 1].id];
      h += `<button class="lecon ${fini ? 'fini' : ''}" data-lecon="${l.id}" ${ouvert ? '' : 'disabled'}>
        <div class="num">${fini ? '✓' : i + 1}</div>
        <div class="txt"><b>${esc(l.titre)}</b><span>${ouvert ? esc(l.but) : 'Termine la leçon précédente'} · ${l.minutes} min</span></div>
        <div class="fl">${fini ? '↻' : '›'}</div>
      </button>`;
    });
    h += `</div>`;
  }
  return h;
}

/* ═══════════════════════════════════════════════════════════
   VUE — BOUTIQUE
   ═══════════════════════════════════════════════════════════ */
function vueBoutique() {
  return `
  <div class="titre-sec">Investir</div>
  <div class="article">
    <div class="em" style="background:rgba(59,130,246,.16)">▤</div>
    <div class="in"><b>Un serveur de plus</b>
      <span>+${nb(R.capaciteServeur)} clients supportés · ${nb(R.coutServeurJour)} FC de charges par jour</span>
      <span>Tu en as ${S.serveurs} — capacité ${nb(capacite())}</span></div>
    <button class="btn mini ${S.argent >= R.prixServeur ? 'plein' : ''}" data-achat="serveur" ${S.argent >= R.prixServeur ? '' : 'disabled'}>${nb(R.prixServeur)}</button>
  </div>
  <div class="article">
    <div class="em" style="background:rgba(139,92,246,.16)">☺</div>
    <div class="in"><b>Embaucher un développeur</b>
      <span>+1 point de développement par action · ${nb(R.coutEmployeJour)} FC de salaire par jour</span>
      <span>Équipe : ${S.employes} personne${S.employes > 1 ? 's' : ''}</span></div>
    <button class="btn mini ${S.argent >= R.prixEmploye ? 'plein' : ''}" data-achat="employe" ${S.argent >= R.prixEmploye ? '' : 'disabled'}>${nb(R.prixEmploye)}</button>
  </div>
  <div class="titre-sec">Ta progression</div>
  <div class="carte">
    ${COURS.map(b => {
      const n = niveau(b.id), m = b.lecons.length;
      return `<div class="comp"><div class="n">${esc(b.nom)}</div>
        <div class="b"><i style="width:${n / m * 100}%;background:${b.couleur}"></i></div>
        <div class="v">${n}/${m}</div></div>`;
    }).join('')}
  </div>
  <div class="carte">
    <div class="sous">Objectif de la partie : atteindre <b style="color:var(--or)">${nb(R.objectif)} clients</b>.
    Tu es à ${nb(S.users)}, soit ${Math.round(S.users / R.objectif * 100)} %.</div>
    <div class="jauge" style="margin-top:9px"><i style="width:${Math.min(100, S.users / R.objectif * 100)}%"></i></div>
  </div>`;
}

/* ═══════════════════════════════════════════════════════════
   VUE — PROFIL
   ═══════════════════════════════════════════════════════════ */
function vueProfil() {
  const revenus = S.users * R.revenuParUser;
  const charges = S.serveurs * R.coutServeurJour + S.employes * R.coutEmployeJour;
  return `
  <div class="carte">
    <div class="titre-sec" style="margin-top:0">Comptes du jour</div>
    <div class="journal">
      <div><b>Revenus des clients</b> — ${fc(revenus)}</div>
      <div><b>Charges serveurs</b> — ${fc(S.serveurs * R.coutServeurJour)}</div>
      <div><b>Salaires</b> — ${fc(S.employes * R.coutEmployeJour)}</div>
      <div><b>Résultat net</b> — <span style="color:${revenus - charges >= 0 ? 'var(--vert)' : 'var(--rouge)'}">${fc(revenus - charges)}</span> par jour</div>
    </div>
  </div>
  <div class="carte">
    <div class="titre-sec" style="margin-top:0">Compétences acquises</div>
    <div class="sous">${niveauTotal()} leçons terminées sur ${COURS.reduce((s, b) => s + b.lecons.length, 0)}.
    ${niveauTotal() === COURS.reduce((s, b) => s + b.lecons.length, 0) ? ' Programme complet — bravo.' : ''}</div>
  </div>
  <div class="titre-sec">Journal</div>
  <div class="carte journal">
    ${S.journal.length ? S.journal.map(e => `<div><b>Jour ${e.j}</b> — ${esc(e.t)}</div>`).join('')
      : '<div class="sous">Rien encore.</div>'}
  </div>
  <button class="btn" style="margin-top:14px;color:#FCA5A5" id="btnReset">Recommencer une partie</button>`;
}

/* ═══════════════════════════════════════════════════════════
   ROUTAGE
   ═══════════════════════════════════════════════════════════ */
function rendre() {
  rendreHud();
  const e = $('#ecran');
  if (S.fini) { e.innerHTML = vueFin(); return; }
  if (vue === 'bureau') e.innerHTML = vueBureau();
  else if (vue === 'ecole') e.innerHTML = vueEcole();
  else if (vue === 'boutique') e.innerHTML = vueBoutique();
  else e.innerHTML = vueProfil();
  document.querySelectorAll('.nav button').forEach(b =>
    b.classList.toggle('on', b.dataset.vue === vue));
  window.scrollTo(0, 0);
  sauver();
}
function vueFin() {
  return `<div class="fin">
    <div class="gd">${S.victoire ? 'PARTIE GAGNÉE' : 'PARTIE TERMINÉE'}</div>
    <p class="sous" style="margin:12px 0 20px">${S.victoire
      ? `Tu as bâti un groupe de ${nb(S.users)} clients en ${S.jour} jours, avec ${niveauTotal()} compétences acquises pour de vrai.`
      : `La caisse est vide au jour ${S.jour}. Les charges ont dépassé les revenus — recommence en gardant moins de serveurs inutiles.`}</p>
    <button class="btn or" id="btnReset">Nouvelle partie</button>
  </div>`;
}

/* ═══════════════════════════════════════════════════════════
   ACTIONS
   ═══════════════════════════════════════════════════════════ */
function depenserEnergie() {
  if (S.energie < 1) { toast('Plus d\'énergie. Termine la journée.', 'rouge'); return false; }
  S.energie--; return true;
}

function actionDev() {
  if (!S.contrats.length) return;
  if (!depenserEnergie()) return;
  let pts = pointsDev();
  for (const c of S.contrats) {
    if (c.avance >= c.travail) continue;
    const met = Math.min(pts, c.travail - c.avance);
    c.avance += met; pts -= met;
    if (pts <= 0) break;
  }
  toast('Développement avancé de ' + pointsDev() + ' points.');
  rendre();
}

function actionProspect() {
  if (!depenserEnergie()) return;
  const dejaVus = new Set([...S.offres, ...S.contrats].map(x => x.t));
  const nMax = niveauTotal();
  const dispo = CONTRATS.filter(c => !dejaVus.has(c.t) && c.niv <= niveau(c.br) + 1);
  const pool = dispo.length ? dispo : CONTRATS.filter(c => !dejaVus.has(c.t));
  let n = 0;
  for (let i = 0; i < 2 && pool.length; i++) {
    const c = pool.splice(Math.floor(Math.random() * pool.length), 1)[0];
    S.offres.push(Object.assign({}, c, { uid: 'o' + (S.prospecte++) + '_' + Date.now() + i }));
    n++;
  }
  toast(n ? n + ' nouvelle' + (n > 1 ? 's offres' : ' offre') + ' au tableau.' : 'Aucun nouveau client aujourd\'hui.');
  vue = 'bureau'; rendre();
}

function actionMaint() {
  if (S.maintenanceAujourdhui) return;
  if (!depenserEnergie()) return;
  S.maintenanceAujourdhui = true;
  S.reput = Math.min(100, S.reput + 1);
  toast('Serveurs vérifiés. Pas de panne aujourd\'hui.', 'vert');
  rendre();
}

function actionPub() {
  if (S.argent < R.prixPub) return;
  if (!depenserEnergie()) return;
  S.argent -= R.prixPub;
  const gagnes = Math.round(40 + S.reput * 4 + Math.random() * 60);
  S.users += gagnes;
  noter('Campagne de pub : +' + nb(gagnes) + ' clients.');
  toast('+' + nb(gagnes) + ' clients grâce à la pub.', 'vert');
  verifierVictoire(); rendre();
}

function signer(uid) {
  const i = S.offres.findIndex(o => o.uid === uid);
  if (i < 0) return;
  const o = S.offres[i];
  if (niveau(o.br) < o.niv) return;
  S.offres.splice(i, 1);
  o.avance = 0;
  S.contrats.push(o);
  noter('Contrat signé : ' + o.t + ' (' + o.cli + ').');
  toast('Contrat signé. Au travail.', 'vert');
  rendre();
}

function livrer(uid) {
  const i = S.contrats.findIndex(c => c.uid === uid);
  if (i < 0) return;
  const c = S.contrats[i];
  if (c.avance < c.travail) return;
  S.contrats.splice(i, 1);
  S.argent += c.paie;
  S.users += c.users;
  S.reput = Math.min(100, S.reput + 4);
  noter('Projet livré : ' + c.t + ' → ' + fc(c.paie) + ', +' + nb(c.users) + ' clients.');
  toast('Livré ! ' + fc(c.paie) + ' encaissés.', 'vert');
  verifierVictoire(); rendre();
}

function acheter(quoi) {
  if (quoi === 'serveur' && S.argent >= R.prixServeur) {
    S.argent -= R.prixServeur; S.serveurs++;
    noter('Nouveau serveur — capacité ' + nb(capacite()) + '.');
    toast('Serveur ajouté.', 'vert');
  } else if (quoi === 'employe' && S.argent >= R.prixEmploye) {
    S.argent -= R.prixEmploye; S.employes++;
    noter('Embauche d\'un développeur.');
    toast('Bienvenue dans l\'équipe.', 'vert');
  }
  rendre();
}

function finDeJournee() {
  const revenus = S.users * R.revenuParUser;
  const charges = S.serveurs * R.coutServeurJour + S.employes * R.coutEmployeJour;
  S.argent += revenus - charges;

  let msg = 'Journée close : ' + fc(revenus) + ' encaissés, ' + fc(charges) + ' de charges.';

  // Panne si les serveurs sont saturés et la maintenance n'a pas été faite
  if (S.users > capacite() && !S.maintenanceAujourdhui && Math.random() < 0.45) {
    const perdus = Math.round(S.users * 0.12);
    S.users -= perdus; S.reput = Math.max(0, S.reput - 8);
    noter('PANNE : serveurs saturés, ' + nb(perdus) + ' clients perdus.');
    toast('Panne ! ' + nb(perdus) + ' clients partis.', 'rouge');
  } else {
    // Bouche-à-oreille : la réputation ramène du monde
    const bouche = Math.round(S.users * (S.reput / 100) * 0.05);
    if (bouche > 0) { S.users += bouche; msg += ' Bouche-à-oreille : +' + nb(bouche) + '.'; }
  }

  noter(msg);
  S.jour++;
  S.energie = R.energieMax;
  S.maintenanceAujourdhui = false;

  if (S.argent < 0) { S.fini = true; S.victoire = false; }
  verifierVictoire();
  toast('Jour ' + S.jour + '. Énergie refaite.');
  vue = 'bureau'; rendre();
}

function verifierVictoire() {
  if (S.users >= R.objectif && !S.fini) { S.fini = true; S.victoire = true; }
}

/* ═══════════════════════════════════════════════════════════
   LEÇONS ET EXERCICES
   ═══════════════════════════════════════════════════════════ */
let ctx = null;   // { lecon, branche, etape, iExo, reussis }

function trouverLecon(id) {
  for (const b of COURS) { const l = b.lecons.find(x => x.id === id); if (l) return { b, l }; }
  return null;
}

function ouvrirLecon(id) {
  const t = trouverLecon(id);
  if (!t) return;
  if (!S.fait[t.l.id] && S.energie < 1) {
    toast('Plus d\'énergie pour étudier. Termine la journée.', 'rouge'); return;
  }
  ctx = { lecon: t.l, br: t.b, etape: 'cours', iExo: 0, reussis: 0, revision: !!S.fait[t.l.id] };
  $('#panneau').hidden = false;
  document.body.style.overflow = 'hidden';
  rendrePanneau();
}
function fermerPanneau() {
  $('#panneau').hidden = true;
  document.body.style.overflow = '';
  ctx = null;
  rendre();
}

function rendrePanneau() {
  if (!ctx) return;
  $('#panneauTitre').textContent = ctx.lecon.titre;
  if (ctx.etape === 'cours') rendreCours();
  else if (ctx.etape === 'exo') rendreExo();
  else rendreBilan();
  $('#panneauCorps').scrollTop = 0;
}

function rendreCours() {
  const l = ctx.lecon;
  let h = `<div class="lec"><div class="but"><b>Ce que tu sauras faire</b>${l.but}</div>`;
  for (const [type, txt] of l.contenu) {
    if (type === 'p') h += `<p>${txt}</p>`;
    else if (type === 'h') h += `<h4>${txt}</h4>`;
    else if (type === 'code') h += bloc(txt);
    else if (type === 'note') h += `<div class="note">${txt}</div>`;
  }
  h += `</div>`;
  $('#panneauCorps').innerHTML = h;
  $('#panneauPied').innerHTML = `<button class="btn or" id="btnExo">Passer aux exercices (${l.exos.length})</button>`;
  $('#btnExo').onclick = () => { ctx.etape = 'exo'; ctx.iExo = 0; rendrePanneau(); };
}

/* — Exécution d'un exercice de code — */
function testerCode(src, nom, tests) {
  let f;
  try {
    f = new Function(src + '\n;return typeof ' + nom + " === 'function' ? " + nom + ' : null;')();
  } catch (e) {
    return { ok: false, msg: 'Ton code ne se lit pas : ' + e.message };
  }
  if (!f) return { ok: false, msg: 'Je ne trouve pas de fonction nommée <code>' + esc(nom) + '</code>.' };
  for (const t of tests) {
    let r;
    try { r = f.apply(null, JSON.parse(JSON.stringify(t.args))); }
    catch (e) { return { ok: false, msg: 'Erreur pendant le calcul : ' + esc(e.message) }; }
    if (JSON.stringify(r) !== JSON.stringify(t.att)) {
      return { ok: false, msg: 'Avec <code>' + esc(t.args.map(a => JSON.stringify(a)).join(', ')) +
        '</code> j\'attends <code>' + esc(JSON.stringify(t.att)) +
        '</code>, ton code rend <code>' + esc(r === undefined ? 'undefined' : JSON.stringify(r)) + '</code>.' };
    }
  }
  return { ok: true };
}

function rendreExo() {
  const l = ctx.lecon, e = l.exos[ctx.iExo];
  let h = `<div class="exo-tete"><span>Exercice ${ctx.iExo + 1} / ${l.exos.length}</span><span>${esc(ctx.br.nom)}</span></div>
    <div class="q">${e.q}</div>`;

  if (e.type === 'qcm') {
    h += e.choix.map((c, i) => `<button class="choix" data-c="${i}">${c}</button>`).join('');
  } else if (e.type === 'code') {
    h += `<textarea class="code" id="zoneCode" spellcheck="false">${esc(e.depart)}</textarea>
      ${e.indice ? `<button class="btn mini" id="btnIndice" style="margin-top:9px">Voir un indice</button>
      <div id="indice" hidden class="note" style="margin-top:9px">${e.indice}</div>` : ''}`;
  } else if (e.type === 'ordre') {
    const melange = e.items.map((t, i) => ({ t, i })).sort(() => Math.random() - 0.5);
    ctx.ordre = { melange, choisis: [] };
    h += melange.map((o, k) => `<button class="ordre-item" data-o="${o.i}"><div class="rang">·</div><div>${o.t}</div></button>`).join('');
  }
  h += `<div id="verdict"></div>`;
  $('#panneauCorps').innerHTML = h;

  const pied = $('#panneauPied');
  if (e.type === 'qcm') {
    pied.innerHTML = `<button class="btn" id="btnValider" disabled>Valider</button>`;
    let choisi = -1;
    $('#panneauCorps').querySelectorAll('.choix').forEach(b => b.onclick = () => {
      if (ctx.corrige) return;
      $('#panneauCorps').querySelectorAll('.choix').forEach(x => x.classList.remove('sel'));
      b.classList.add('sel'); choisi = +b.dataset.c;
      $('#btnValider').disabled = false; $('#btnValider').classList.add('or');
    });
    $('#btnValider').onclick = () => corrigerQcm(choisi);
  } else if (e.type === 'code') {
    pied.innerHTML = `<button class="btn or" id="btnValider">Vérifier mon code</button>`;
    if ($('#btnIndice')) $('#btnIndice').onclick = () => {
      $('#indice').hidden = false; $('#btnIndice').hidden = true;
    };
    $('#btnValider').onclick = () => corrigerCode();
  } else {
    pied.innerHTML = `<button class="btn" id="btnValider" disabled>Valider l'ordre</button>`;
    $('#panneauCorps').querySelectorAll('.ordre-item').forEach(b => b.onclick = () => {
      if (ctx.corrige) return;
      const idx = +b.dataset.o;
      const p = ctx.ordre.choisis.indexOf(idx);
      if (p >= 0) ctx.ordre.choisis.splice(p, 1);
      else ctx.ordre.choisis.push(idx);
      // rafraîchir les rangs
      $('#panneauCorps').querySelectorAll('.ordre-item').forEach(x => {
        const r = ctx.ordre.choisis.indexOf(+x.dataset.o);
        x.classList.toggle('pris', r >= 0);
        x.querySelector('.rang').textContent = r >= 0 ? (r + 1) : '·';
      });
      const complet = ctx.ordre.choisis.length === e.items.length;
      $('#btnValider').disabled = !complet;
      $('#btnValider').classList.toggle('or', complet);
    });
    $('#btnValider').onclick = () => corrigerOrdre();
  }
  ctx.corrige = false;
}

function verdict(bon, titre, texte) {
  $('#verdict').innerHTML = `<div class="verdict ${bon ? 'bon' : 'mauv'}"><b>${titre}</b>${texte}</div>`;
  ctx.corrige = bon;
  if (bon) {
    ctx.reussis++;
    const dernier = ctx.iExo >= ctx.lecon.exos.length - 1;
    $('#panneauPied').innerHTML = `<button class="btn vert" id="btnSuite">${dernier ? 'Terminer la leçon' : 'Exercice suivant'}</button>`;
    $('#btnSuite').onclick = () => {
      if (dernier) { ctx.etape = 'bilan'; }
      else { ctx.iExo++; }
      rendrePanneau();
    };
  }
}

function corrigerQcm(choisi) {
  const e = ctx.lecon.exos[ctx.iExo];
  const btns = $('#panneauCorps').querySelectorAll('.choix');
  btns.forEach((b, i) => {
    b.classList.remove('sel');
    if (i === e.bon) b.classList.add('bon');
    else if (i === choisi) b.classList.add('mauv');
  });
  if (choisi === e.bon) verdict(true, 'Exact.', e.expl);
  else {
    verdict(false, 'Pas tout à fait.', e.expl);
    $('#panneauPied').innerHTML = `<button class="btn or" id="btnRe">Réessayer</button>`;
    $('#btnRe').onclick = () => rendreExo();
  }
}

function corrigerCode() {
  const e = ctx.lecon.exos[ctx.iExo];
  const src = $('#zoneCode').value;
  const res = testerCode(src, e.nom, e.tests);
  if (res.ok) verdict(true, 'Ça marche, tous les cas passent.', e.expl);
  else {
    verdict(false, 'Pas encore.', res.msg);
    $('#panneauPied').innerHTML = `<button class="btn or" id="btnRe">Corriger et revérifier</button>`;
    $('#btnRe').onclick = () => corrigerCode();
  }
}

function corrigerOrdre() {
  const e = ctx.lecon.exos[ctx.iExo];
  const attendu = e.items.map((_, i) => i);
  const bon = JSON.stringify(ctx.ordre.choisis) === JSON.stringify(attendu);
  if (bon) verdict(true, 'Dans le bon ordre.', e.expl);
  else {
    verdict(false, 'L\'ordre n\'est pas bon.', e.expl);
    $('#panneauPied').innerHTML = `<button class="btn or" id="btnRe">Réessayer</button>`;
    $('#btnRe').onclick = () => rendreExo();
  }
}

function rendreBilan() {
  const l = ctx.lecon, premiere = !S.fait[l.id];
  if (premiere) {
    S.fait[l.id] = true;
    S.energie = Math.max(0, S.energie - 1);
    S.reput = Math.min(100, S.reput + 2);
    noter('Compétence acquise : ' + l.titre + ' (' + ctx.br.nom + ').');
  }
  const niv = niveau(ctx.br.id);
  const debloques = CONTRATS.filter(c => c.br === ctx.br.id && c.niv === niv).length;

  $('#panneauCorps').innerHTML = `<div class="fin">
    <div class="gd">${premiere ? 'COMPÉTENCE ACQUISE' : 'RÉVISION FAITE'}</div>
    <p class="sous" style="margin:12px 0 18px">
      ${esc(l.titre)} — ${ctx.reussis} exercice${ctx.reussis > 1 ? 's' : ''} réussi${ctx.reussis > 1 ? 's' : ''}.</p>
    ${premiere ? `<div class="carte" style="text-align:left">
      <div class="comp"><div class="n">${esc(ctx.br.nom)}</div>
        <div class="b"><i style="width:${niv / ctx.br.lecons.length * 100}%;background:${ctx.br.couleur}"></i></div>
        <div class="v">${niv}/${ctx.br.lecons.length}</div></div>
      <div class="sous" style="margin-top:8px">${debloques
        ? 'Tu peux maintenant prendre les contrats « ' + esc(ctx.br.nom) + ' niveau ' + niv + ' ».'
        : 'Continue : la suite de la branche débloque des contrats plus gros.'}</div>
    </div>` : ''}
  </div>`;
  $('#panneauPied').innerHTML = `<button class="btn or" id="btnFin">Retour au bureau</button>`;
  $('#btnFin').onclick = () => { vue = 'bureau'; fermerPanneau(); };
  sauver();
}

/* ═══════════════════════════════════════════════════════════
   ÉVÉNEMENTS
   ═══════════════════════════════════════════════════════════ */
document.addEventListener('click', ev => {
  const t = ev.target.closest('[data-act],[data-signer],[data-livrer],[data-achat],[data-lecon],[data-vue],#btnReset');
  if (!t) return;

  if (t.dataset.vue) { vue = t.dataset.vue; rendre(); return; }
  if (t.id === 'btnReset') {
    if (confirm('Effacer la partie en cours et recommencer ?')) { S = neuf(); vue = 'bureau'; rendre(); }
    return;
  }
  if (t.dataset.lecon) { ouvrirLecon(t.dataset.lecon); return; }
  if (t.dataset.signer) { signer(t.dataset.signer); return; }
  if (t.dataset.livrer) { livrer(t.dataset.livrer); return; }
  if (t.dataset.achat) { acheter(t.dataset.achat); return; }

  switch (t.dataset.act) {
    case 'dev': actionDev(); break;
    case 'prospect': actionProspect(); break;
    case 'maint': actionMaint(); break;
    case 'pub': actionPub(); break;
    case 'ecole': vue = 'ecole'; rendre(); break;
    case 'dormir': finDeJournee(); break;
  }
});
$('#panneauFermer').onclick = fermerPanneau;

/* ═══════════════════════════════════════════════════════════
   DÉMARRAGE
   ═══════════════════════════════════════════════════════════ */
function demarrer(reprise) {
  S = reprise || neuf();
  if (!reprise) {
    // deux offres pour ne pas commencer devant un tableau vide
    const debut = CONTRATS.filter(c => c.niv === 0);
    debut.forEach((c, i) => S.offres.push(Object.assign({}, c, { uid: 'o_dep' + i })));
    noter('Création de la startup. ' + fc(R.argentDepart) + ' en caisse.');
  }
  $('#intro').style.display = 'none';
  vue = 'bureau';
  rendre();
}

const sauvegarde = charger();
if (sauvegarde) $('#btnReprendre').hidden = false;
$('#btnJouer').onclick = () => demarrer(null);
$('#btnReprendre').onclick = () => demarrer(sauvegarde);

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('sw.js').catch(() => {}));
}
})();
