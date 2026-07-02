/* ============================================================
   RA-QDMS — Application
   Version locale (localStorage). En production : Supabase
   (PostgreSQL + Auth + Storage) — voir README.md.
   ============================================================ */

"use strict";

/* ---------------- Icônes (style Lucide, inline SVG) ---------------- */
const I = (name, s = 18) => {
  const p = {
    dashboard: '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
    plane: '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    book: '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    clipboard: '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><path d="m9 14 2 2 4-4"/>',
    grad: '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5"/>',
    file: '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/>',
    check: '<path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>',
    crew: '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 1 0-16 0"/><path d="M12 3v2"/><path d="M7 6.5 5.5 5"/><path d="m17 6.5 1.5-1.5"/>',
    cal: '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    chart: '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/><path d="M3 20h18"/>',
    bell: '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
    moon: '<path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M2 12h2m16 0h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    search: '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    eye: '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>',
    edit: '<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/>',
    history: '<path d="M3 3v5h5"/><path d="M3.05 13A9 9 0 1 0 6 5.3L3 8"/><path d="M12 7v5l4 2"/>',
    sign: '<path d="m12 19 7-7 3 3-7 7-3-3z"/><path d="m18 13-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="m2 2 7.586 7.586"/><circle cx="11" cy="11" r="2"/>',
    plus: '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    menu: '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    journal: '<path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/>',
    archive: '<rect x="2" y="3" width="20" height="5" rx="1"/><path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/>',
    print: '<polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    alert: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    cloud: '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9z"/>'
  }[name] || "";
  return `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${p}</svg>`;
};

const LOGO = (s = 40, withText = true) => `
  <svg width="${s}" height="${s}" viewBox="0 0 64 64">
    <rect width="64" height="64" rx="14" fill="#0A2342"/>
    <path d="M12 44 L32 14 L52 44 L44 44 L32 26 L20 44 Z" fill="#2f7bff"/>
    <path d="M24 44 L32 32 L40 44 Z" fill="#fff"/>
    <rect x="14" y="48" width="36" height="3" rx="1.5" fill="#0056D2"/>
  </svg>
  ${withText ? '<div class="name">ROYAL AIR<small>Quality Document Management</small></div>' : ""}`;

/* ---------------- Base de données locale ---------------- */
const DB_KEY = "raqdms_db_v1";
let DB;

function loadDB() {
  try {
    const raw = localStorage.getItem(DB_KEY);
    if (raw) { DB = JSON.parse(raw); migrateDB(); localStorage.setItem(DB_KEY, JSON.stringify(DB)); return; }
  } catch (e) { /* seed */ }
  DB = JSON.parse(JSON.stringify(SEED_DB));
  saveDB();
}
/* Ajoute les nouveautés (module risques, rôles) aux bases déjà installées */
function migrateDB() {
  if (!DB.risks) DB.risks = JSON.parse(JSON.stringify(SEED_DB.risks));
  DB.roles = SEED_DB.roles; // les droits sont de la configuration, toujours à jour
}
function saveDB() {
  localStorage.setItem(DB_KEY, JSON.stringify(DB));
  cloudSave();
}

/* ---------------- Synchronisation cloud (Supabase) ----------------
   Activée quand config.js contient SUPABASE_URL et SUPABASE_ANON_KEY.
   La base est partagée entre tous les utilisateurs connectés au site. */
let SB = null, cloudTimer = null, cloudState = "local";

async function initCloud() {
  const cfg = window.CONFIG || {};
  if (!cfg.SUPABASE_URL || !cfg.SUPABASE_ANON_KEY) return;
  cloudState = "connecting";
  try {
    await new Promise((res, rej) => {
      const s = document.createElement("script");
      s.src = "https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js";
      s.onload = res; s.onerror = rej;
      document.head.appendChild(s);
    });
    SB = window.supabase.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY);
    const { data, error } = await SB.from("qdms_state").select("state").eq("id", "royalair").maybeSingle();
    if (error) throw error;
    if (data && data.state) {
      DB = data.state; migrateDB();
      localStorage.setItem(DB_KEY, JSON.stringify(DB));
    } else {
      await SB.from("qdms_state").upsert({ id: "royalair", state: DB, updated_at: new Date().toISOString() });
    }
    cloudState = "online";
  } catch (e) {
    console.warn("Supabase indisponible, mode local :", e.message || e);
    cloudState = "error";
  }
  updateCloudChip();
}
function cloudSave() {
  if (!SB) return;
  clearTimeout(cloudTimer);
  cloudTimer = setTimeout(async () => {
    try {
      const { error } = await SB.from("qdms_state").upsert({ id: "royalair", state: DB, updated_at: new Date().toISOString() });
      cloudState = error ? "error" : "online";
    } catch (e) { cloudState = "error"; }
    updateCloudChip();
  }, 1200);
}
function updateCloudChip() {
  const el = $("#cloudChip");
  if (!el) return;
  const map = {
    local: ["st-gray", "Mode local"],
    connecting: ["st-blue", "Connexion…"],
    online: ["st-green", "Base en ligne"],
    error: ["st-red", "Hors ligne"]
  };
  const [cls, label] = map[cloudState] || map.local;
  el.innerHTML = `<span class="badge-st ${cls}">${I("cloud", 12)} ${label}</span>`;
}

/* ---------------- Utilitaires ---------------- */
const $ = (sel) => document.querySelector(sel);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const TODAY = new Date(); TODAY.setHours(0, 0, 0, 0);

/* Date locale au format AAAA-MM-JJ (évite le décalage UTC de toISOString) */
function localISO(d = new Date()) {
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}

function daysTo(dateStr) {
  if (!dateStr) return Infinity;
  return Math.round((new Date(dateStr) - TODAY) / 86400000);
}
function fmtDate(d) {
  if (!d) return "—";
  const [y, m, dd] = d.split("-");
  return dd && m ? `${dd}/${m}/${y}` : d;
}
function expiryBadge(dateStr) {
  const d = daysTo(dateStr);
  if (!dateStr) return `<span class="badge-st st-gray">Sans échéance</span>`;
  if (d < 0) return `<span class="badge-st st-red">Expiré (${fmtDate(dateStr)})</span>`;
  if (d <= 60) return `<span class="badge-st st-orange">Expire dans ${d} j</span>`;
  return `<span class="badge-st st-green">Valide → ${fmtDate(dateStr)}</span>`;
}
function statutBadge(st) {
  const map = { "Approuvé": "st-green", "Valide": "st-green", "Apte": "st-green", "Clôturée": "st-green", "Clôturé": "st-green", "Réalisé": "st-green",
    "En révision": "st-orange", "En cours": "st-orange", "Planifié": "st-blue", "Planifiée": "st-blue", "Programmé": "st-blue", "Demandé": "st-blue",
    "Brouillon": "st-gray", "Archivé": "st-gray", "En retard": "st-red", "Expiré": "st-red", "Expire bientôt": "st-orange", "Vigilance échéances": "st-orange",
    "En service": "st-green", "Maintenance (Airworks Kenya)": "st-orange", "Ouvert": "st-orange", "Maîtrisé": "st-green" };
  return `<span class="badge-st ${map[st] || "st-gray"}">${esc(st)}</span>`;
}
function toast(msg) {
  const t = $("#toast");
  t.innerHTML = I("check", 16) + " " + esc(msg);
  t.classList.add("show");
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove("show"), 2600);
}
function logAction(action) {
  const now = new Date();
  const ts = localISO(now) + " " + now.toTimeString().slice(0, 5);
  DB.journal.unshift({ date: ts, user: SESSION ? SESSION.username : "—", action });
  if (DB.journal.length > 400) DB.journal.length = 400;
  saveDB();
}

/* ---------------- Gestion des risques : calcul automatique ----------------
   Matrice OACI (Doc 9859 SMS) 5x5 : Probabilité (1-5) x Gravité (1-5).
   Indice = P + lettre de gravité (5=A Catastrophique … 1=E Négligeable).
   Tolérabilité calculée automatiquement à partir du score P x G. */
const PROBA = { 1: "Extrêmement improbable", 2: "Improbable", 3: "Occasionnel", 4: "Probable", 5: "Fréquent" };
const GRAV = { 5: "Catastrophique", 4: "Dangereux", 3: "Majeur", 2: "Mineur", 1: "Négligeable" };
const GRAV_LETTRE = { 5: "A", 4: "B", 3: "C", 2: "D", 1: "E" };

function riskCalc(p, g) {
  p = +p; g = +g;
  const score = p * g;
  const index = p + GRAV_LETTRE[g];
  let tol, cls;
  if (score >= 15 || (p >= 4 && g >= 4)) { tol = "Intolérable"; cls = "st-red"; }
  else if (score >= 6) { tol = "Tolérable (mitigation requise)"; cls = "st-orange"; }
  else { tol = "Acceptable"; cls = "st-green"; }
  return { score, index, tol, cls };
}
function riskBadge(p, g) {
  const r = riskCalc(p, g);
  return `<span class="badge-st ${r.cls}" title="P${p} (${PROBA[p]}) × G${g} (${GRAV[g]}) = ${r.score}">${r.index} · ${r.tol.split(" ")[0]}</span>`;
}

/* ---------------- Session & droits ---------------- */
let SESSION = null;

function canEdit() { return SESSION && "eax".includes(DB.roles[SESSION.role]?.rights); }
function canApprove() { return SESSION && "ax".includes(DB.roles[SESSION.role]?.rights); }
function isAdmin() { return SESSION && DB.roles[SESSION.role]?.rights === "x"; }
function allowedModules() {
  const r = DB.roles[SESSION.role];
  if (!r) return ["dashboard"];
  if (r.modules === "all") return MODULES.map(m => m.id);
  return r.modules.concat(isAdmin() ? ["users", "journal"] : []);
}

/* ---------------- Modules / navigation ---------------- */
const MODULES = [
  { id: "dashboard", label: "Tableau de bord", icon: "dashboard", section: "Pilotage" },
  { id: "aircraft", label: "Aircraft", icon: "plane", section: "Modules" },
  { id: "personnel", label: "Personnel", icon: "users", section: "Modules" },
  { id: "manuals", label: "Manuals", icon: "book", section: "Modules" },
  { id: "policies", label: "Policies", icon: "shield", section: "Modules" },
  { id: "audit", label: "Audit", icon: "clipboard", section: "Modules" },
  { id: "risks", label: "Risk Management", icon: "alert", section: "Modules" },
  { id: "training", label: "Training", icon: "grad", section: "Modules" },
  { id: "procedures", label: "Procedures", icon: "file", section: "Modules" },
  { id: "checklists", label: "Checklists", icon: "check", section: "Modules" },
  { id: "crew", label: "Crew", icon: "crew", section: "Modules" },
  { id: "scheduling", label: "Scheduling", icon: "cal", section: "Modules" },
  { id: "reports", label: "Rapports & KPI", icon: "chart", section: "Pilotage" },
  { id: "users", label: "Utilisateurs", icon: "users", section: "Administration", admin: true },
  { id: "journal", label: "Journal système", icon: "journal", section: "Administration", admin: true }
];
let CURRENT = "dashboard";

/* ---------------- Notifications (calculées) ---------------- */
function computeNotifications() {
  const out = [];
  const push = (level, texte, date) => out.push({ level, texte, date });

  DB.documents.forEach(d => {
    if (d.statut === "En révision") push("warn", `Document en attente de revue : ${d.num} — ${d.titre}`, d.date);
    const dd = daysTo(d.expire);
    if (d.expire && dd < 0) push("crit", `Document expiré : ${d.num} — ${d.titre}`, d.expire);
    else if (d.expire && dd <= 60) push("warn", `Document ${d.num} expire dans ${dd} j`, d.expire);
  });
  DB.aircraft.forEach(ac => ac.docs.forEach(d => {
    const dd = daysTo(d.expire);
    if (d.expire && dd < 0) push("crit", `${ac.immat} : ${d.titre} EXPIRÉ`, d.expire);
    else if (d.expire && dd <= 60) push("warn", `${ac.immat} : ${d.titre} expire dans ${dd} j`, d.expire);
  }));
  DB.personnel.forEach(p => p.docs.forEach(d => {
    const dd = daysTo(d.expire);
    if (d.expire && dd < 0) push("crit", `${p.nom} : ${d.titre} EXPIRÉ`, d.expire);
    else if (d.expire && dd <= 60) push("warn", `${p.nom} : ${d.titre} expire dans ${dd} j`, d.expire);
  }));
  DB.fnc.forEach(f => {
    const dd = daysTo(f.echeance);
    if (f.statut !== "Clôturée" && dd < 0) push("crit", `Action corrective en retard : ${f.ref} (échéance ${fmtDate(f.echeance)})`, f.echeance);
    else if (f.statut !== "Clôturée" && dd <= 21) push("warn", `Échéance proche pour ${f.ref} : ${fmtDate(f.echeance)}`, f.echeance);
  });
  DB.audits.forEach(a => {
    const dd = daysTo(a.date);
    if (a.statut === "Planifié" && dd >= 0 && dd <= 45) push("info", `Audit à venir : ${a.titre} le ${fmtDate(a.date)}`, a.date);
  });
  DB.trainings.forEach(t => {
    const dd = daysTo(t.prochaine);
    if (t.statut === "Planifiée" && dd >= 0 && dd <= 30) push("info", `Formation à venir : ${t.titre} le ${fmtDate(t.prochaine)}`, t.prochaine);
  });
  DB.risks.forEach(r => {
    const res = riskCalc(r.pr, r.gr);
    if (res.tol === "Intolérable") push("crit", `Risque INTOLÉRABLE : ${r.ref} — ${r.danger} (indice ${res.index})`, r.revue);
    const dd = daysTo(r.revue);
    if (dd < 0) push("warn", `Revue de risque en retard : ${r.ref} (prévue le ${fmtDate(r.revue)})`, r.revue);
    else if (dd <= 30) push("info", `Revue du risque ${r.ref} à faire avant le ${fmtDate(r.revue)}`, r.revue);
  });
  DB.notices.forEach(n => push(n.type === "warn" ? "warn" : "info", n.texte, n.date));

  out.sort((a, b) => ({ crit: 0, warn: 1, info: 2 }[a.level] - ({ crit: 0, warn: 1, info: 2 }[b.level])));
  return out;
}

/* ---------------- Rendu global ---------------- */
function renderShell() {
  $("#loginPage").style.display = "none";
  $("#app").style.display = "block";
  $("#brandLogo").innerHTML = LOGO(38);
  $("#searchIcon").innerHTML = I("search", 16);
  $("#themeBtn").innerHTML = document.documentElement.dataset.theme === "dark" ? I("sun") : I("moon");
  $("#notifBtn").insertAdjacentHTML("afterbegin", I("bell"));
  $("#logoutBtn").innerHTML = I("logout");
  $("#menuBtn").innerHTML = I("menu");
  if (window.innerWidth <= 900) $("#menuBtn").style.display = "grid";

  $("#userName").textContent = SESSION.name;
  $("#userRole").textContent = SESSION.role;
  $("#userAvatar").textContent = SESSION.name.split(" ").map(w => w[0]).slice(0, 2).join("").toUpperCase();

  const allowed = allowedModules();
  let html = "", lastSection = "";
  MODULES.forEach(m => {
    if (!allowed.includes(m.id)) return;
    if (m.admin && !isAdmin()) return;
    if (m.section !== lastSection) { html += `<div class="section-label">${m.section}</div>`; lastSection = m.section; }
    html += `<button class="nav-item ${m.id === CURRENT ? "active" : ""}" data-mod="${m.id}">${I(m.icon)} ${m.label}</button>`;
  });
  $("#sidebar").innerHTML = html;
  document.querySelectorAll(".nav-item").forEach(b =>
    b.addEventListener("click", () => { navigate(b.dataset.mod); $("#sidebar").classList.remove("open"); }));

  updateNotifBadge();
  updateCloudChip();
  navigate(CURRENT);
}

function updateNotifBadge() {
  const n = computeNotifications().filter(x => x.level !== "info").length;
  $("#notifBadge").textContent = n;
  $("#notifBadge").style.display = n ? "grid" : "none";
}

function navigate(mod) {
  if (!allowedModules().includes(mod)) mod = "dashboard";
  CURRENT = mod;
  document.querySelectorAll(".nav-item").forEach(b => b.classList.toggle("active", b.dataset.mod === mod));
  const views = {
    dashboard: viewDashboard, aircraft: viewAircraft, personnel: viewPersonnel, manuals: viewManuals,
    policies: viewPolicies, audit: viewAudit, risks: viewRisks, training: viewTraining, procedures: viewProcedures,
    checklists: viewChecklists, crew: viewCrew, scheduling: viewScheduling, reports: viewReports,
    users: viewUsers, journal: viewJournal
  };
  $("#main").innerHTML = (views[mod] || viewDashboard)();
  bindView(mod);
  window.scrollTo(0, 0);
}

function pageHead(title, subtitle, actions = "") {
  return `<div class="page-head"><div><h2>${title}</h2><p>${subtitle}</p></div><div class="page-actions">${actions}</div></div>`;
}

/* ---------------- Vues ---------------- */

function viewDashboard() {
  const docsAll = DB.documents;
  const approuves = docsAll.filter(d => d.statut === "Approuvé").length;
  const enRevision = docsAll.filter(d => d.statut === "En révision" || d.statut === "Brouillon").length;
  const auditsPlan = DB.audits.filter(a => a.statut === "Planifié").length;
  const fncOuvertes = DB.fnc.filter(f => f.statut !== "Clôturée").length;
  const licSoon = [];
  DB.personnel.forEach(p => p.docs.forEach(d => { const dd = daysTo(d.expire); if (d.expire && dd <= 90) licSoon.push({ p, d, dd }); }));
  const notifs = computeNotifications();

  const conf = Math.round(100 * DB.fnc.filter(f => f.statut === "Clôturée").length / (DB.fnc.length || 1));
  const domCount = {};
  DB.fnc.forEach(f => domCount[f.domaine] = (domCount[f.domaine] || 0) + 1);

  // Donut conformité
  const r = 54, c = 2 * Math.PI * r, off = c * (1 - conf / 100);
  const donut = `
    <svg width="150" height="150" viewBox="0 0 140 140">
      <circle cx="70" cy="70" r="${r}" fill="none" stroke="var(--surface-2)" stroke-width="16"/>
      <circle cx="70" cy="70" r="${r}" fill="none" stroke="var(--green)" stroke-width="16" stroke-linecap="round"
        stroke-dasharray="${c}" stroke-dashoffset="${off}" transform="rotate(-90 70 70)"/>
      <text x="70" y="66" text-anchor="middle" font-size="26" font-weight="700" fill="var(--text)">${conf}%</text>
      <text x="70" y="86" text-anchor="middle" font-size="10" fill="var(--text-2)">FNC clôturées</text>
    </svg>`;

  const maxDom = Math.max(...Object.values(domCount), 1);
  const bars = Object.entries(domCount).map(([k, v]) => {
    const open = DB.fnc.filter(f => f.domaine === k && f.statut !== "Clôturée").length;
    const cls = open === 0 ? "g" : open >= 2 ? "r" : "o";
    return `<div class="bar-g"><div style="font-size:.78rem;font-weight:700">${v}</div><div class="bar ${cls}" style="height:${Math.round(100 * v / maxDom)}%"></div><div class="bl">${k}</div></div>`;
  }).join("");

  // Calendrier du mois (événements qualité)
  const now = new Date(TODAY);
  const y = now.getFullYear(), m = now.getMonth();
  const first = new Date(y, m, 1), start = (first.getDay() + 6) % 7, nDays = new Date(y, m + 1, 0).getDate();
  const events = {};
  DB.audits.forEach(a => { if (a.date?.startsWith(`${y}-${String(m + 1).padStart(2, "0")}`)) (events[+a.date.slice(8)] ||= []).push("var(--royal)"); });
  DB.trainings.forEach(t => { if (t.prochaine?.startsWith(`${y}-${String(m + 1).padStart(2, "0")}`)) (events[+t.prochaine.slice(8)] ||= []).push("var(--orange)"); });
  DB.fnc.forEach(f => { if (f.statut !== "Clôturée" && f.echeance?.startsWith(`${y}-${String(m + 1).padStart(2, "0")}`)) (events[+f.echeance.slice(8)] ||= []).push("var(--red)"); });
  let cal = ["L", "M", "M", "J", "V", "S", "D"].map(d => `<div class="ch">${d}</div>`).join("");
  for (let i = 0; i < start; i++) cal += `<div class="cd out"></div>`;
  for (let d = 1; d <= nDays; d++) {
    const ev = (events[d] || []).slice(0, 3).map(cc => `<i style="background:${cc}"></i>`).join("");
    cal += `<div class="cd ${d === now.getDate() ? "today" : ""}">${d}<span class="ev">${ev}</span></div>`;
  }

  return pageHead("Tableau de bord", `Bienvenue ${SESSION.name} — situation qualité au ${fmtDate(localISO(now))}`,
    `<button class="btn" onclick="window.print()">${I("print", 15)} Imprimer</button>`) + `
  <div class="kpi-grid">
    <div class="kpi"><div class="ic st-blue">${I("file", 21)}</div><div><div class="val">${docsAll.length + DB.procedures.length + DB.checklists.length}</div><div class="lbl">Documents au total</div></div></div>
    <div class="kpi"><div class="ic st-green">${I("check", 21)}</div><div><div class="val">${approuves}</div><div class="lbl">Documents approuvés</div></div></div>
    <div class="kpi"><div class="ic st-orange">${I("edit", 21)}</div><div><div class="val">${enRevision}</div><div class="lbl">En révision / brouillon</div></div></div>
    <div class="kpi"><div class="ic st-blue">${I("clipboard", 21)}</div><div><div class="val">${auditsPlan}</div><div class="lbl">Audits programmés</div></div></div>
    <div class="kpi"><div class="ic st-red">${I("shield", 21)}</div><div><div class="val">${fncOuvertes}</div><div class="lbl">Actions correctives ouvertes</div></div></div>
    <div class="kpi"><div class="ic st-orange">${I("users", 21)}</div><div><div class="val">${licSoon.length}</div><div class="lbl">Licences / docs personnel ≤ 90 j</div></div></div>
    <div class="kpi"><div class="ic st-red">${I("alert", 21)}</div><div><div class="val">${DB.risks.filter(r => riskCalc(r.pr, r.gr).tol !== "Acceptable").length}</div><div class="lbl">Risques SGS à surveiller</div></div></div>
  </div>
  <div class="grid-31">
    <div class="card">
      <div class="card-head"><h3>Non-conformités par domaine (ANACM Phase 4)</h3><span class="badge-st st-blue">${DB.fnc.length} FNC</span></div>
      <div class="card-body"><div class="bars">${bars}</div></div>
    </div>
    <div class="card">
      <div class="card-head"><h3>Indicateur de conformité</h3></div>
      <div class="card-body donut-wrap">${donut}
        <div class="legend">
          <div class="li"><span class="sw" style="background:var(--green)"></span> Clôturées : ${DB.fnc.filter(f => f.statut === "Clôturée").length}</div>
          <div class="li"><span class="sw" style="background:var(--orange)"></span> En cours : ${DB.fnc.filter(f => f.statut === "En cours").length}</div>
          <div class="li"><span class="sw" style="background:var(--red)"></span> En retard : ${DB.fnc.filter(f => f.statut === "En retard").length}</div>
        </div>
      </div>
    </div>
  </div>
  <div class="grid-2" style="margin-top:16px">
    <div class="card">
      <div class="card-head"><h3>Alertes prioritaires</h3><span class="badge-st st-red">${notifs.filter(n => n.level === "crit").length} critiques</span></div>
      <div class="card-body" style="padding:12px">
        ${notifs.slice(0, 7).map(n => `
          <div class="notif"><span class="dot" style="background:var(--${n.level === "crit" ? "red" : n.level === "warn" ? "orange" : "royal"})"></span>
          <div>${esc(n.texte)}<small>${fmtDate(n.date)}</small></div></div>`).join("") || `<div class="empty">Aucune alerte 🎉</div>`}
      </div>
    </div>
    <div class="card">
      <div class="card-head"><h3>Calendrier qualité — ${now.toLocaleDateString("fr-FR", { month: "long", year: "numeric" })}</h3></div>
      <div class="card-body">
        <div class="cal">${cal}</div>
        <div class="legend" style="margin-top:12px;display:flex;gap:16px">
          <div class="li"><span class="sw" style="background:var(--royal)"></span> Audits</div>
          <div class="li"><span class="sw" style="background:var(--orange)"></span> Formations</div>
          <div class="li"><span class="sw" style="background:var(--red)"></span> Échéances FNC</div>
        </div>
      </div>
    </div>
  </div>`;
}

function viewAircraft() {
  return pageHead("Aircraft", "AOC, Operations Specifications, certificats et documents aéronefs",
    exportBtns("aircraft")) +
    DB.aircraft.map(ac => `
    <div class="card" style="margin-bottom:16px">
      <div class="card-head">
        <h3>${I("plane", 17)} &nbsp;${esc(ac.immat)} — ${esc(ac.type)} <span style="color:var(--text-2);font-weight:400;font-size:.8rem">(MSN ${esc(ac.msn)} · ${esc(ac.base)})</span></h3>
        ${statutBadge(ac.status)}
      </div>
      <div class="card-body" style="padding:0;overflow-x:auto">
        <table class="tbl"><thead><tr><th>Numéro</th><th>Document</th><th>Type</th><th>Révision</th><th>Émission</th><th>Autorité</th><th>Validité</th><th>Statut</th></tr></thead>
        <tbody>${ac.docs.map(d => `
          <tr><td class="mono">${esc(d.num)}</td><td><strong>${esc(d.titre)}</strong></td><td>${esc(d.type)}</td><td>${esc(d.revision)}</td>
          <td>${fmtDate(d.date)}</td><td>${esc(d.autorite)}</td><td>${expiryBadge(d.expire)}</td><td>${statutBadge(d.statut)}</td></tr>`).join("")}
        </tbody></table>
      </div>
    </div>`).join("");
}

function viewPersonnel() {
  return pageHead("Personnel", "Dossiers individuels : licences, medical, formations, contrats, qualifications",
    `<input type="search" id="persSearch" placeholder="Recherche par nom…" style="padding:9px 13px;border:1.5px solid var(--border);border-radius:9px;background:var(--surface);color:var(--text);outline:none">` + exportBtns("personnel")) + `
  <div class="pers-grid" id="persGrid">${persCards(DB.personnel)}</div>`;
}
function persCards(list) {
  if (!list.length) return `<div class="empty">Aucun employé trouvé.</div>`;
  return list.map(p => {
    const worst = p.docs.reduce((acc, d) => Math.min(acc, daysTo(d.expire)), Infinity);
    const st = worst < 0 ? `<span class="badge-st st-red">Document expiré</span>` : worst <= 60 ? `<span class="badge-st st-orange">Échéance ≤ 60 j</span>` : `<span class="badge-st st-green">À jour</span>`;
    return `
    <div class="pers-card" data-pid="${p.id}">
      <div class="ph"><div class="avatar">${p.nom.split(" ").map(w => w[0]).slice(0, 2).join("")}</div>
        <div><div class="pn">${esc(p.nom)}</div><div class="pf">${esc(p.fonction)} · ${esc(p.dept)}</div></div></div>
      ${st}
      <div style="margin-top:10px">${p.qualifications.map(q => `<span class="tag">${esc(q)}</span>`).join("")}</div>
      <div style="margin-top:10px;font-size:.78rem;color:var(--text-2)">${p.docs.length} documents · embauché le ${fmtDate(p.embauche)}</div>
    </div>`;
  }).join("");
}

function viewManuals() {
  return docTableView("manuals", "Manuals", "OM-A, OM-B, OM-C, OM-D, MEL, MCM, AMP, GOM, SGS, ERP, Manuel Qualité, Manuel de Sûreté, MOE");
}
function viewPolicies() {
  return docTableView("policies", "Policies", "Safety, Security, Quality, Drug & Alcohol et Human Factors Policies");
}
function docTableView(mod, title, subtitle) {
  const docs = DB.documents.filter(d => d.module === mod);
  const statuts = [...new Set(docs.map(d => d.statut))];
  return pageHead(title, subtitle,
    (canEdit() ? `<button class="btn solid" id="newDocBtn">${I("plus", 15)} Nouveau document</button>` : "") + exportBtns(mod)) + `
  <div class="filters">
    <input type="search" id="docSearch" placeholder="Filtrer par numéro, titre, auteur…">
    <select id="docStatusFilter"><option value="">Tous les statuts</option>${statuts.map(s => `<option>${s}</option>`).join("")}</select>
  </div>
  <div class="card"><div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Numéro</th><th>Titre</th><th>Révision</th><th>Date</th><th>Auteur</th><th>Approbateur</th><th>Statut</th><th></th></tr></thead>
    <tbody id="docRows">${docRows(docs)}</tbody></table>
  </div></div>`;
}
function docRows(docs) {
  if (!docs.length) return `<tr><td colspan="8"><div class="empty">Aucun document.</div></td></tr>`;
  return docs.map(d => `
    <tr class="clickable" data-doc="${d.id}">
      <td class="mono">${esc(d.num)}</td><td><strong>${esc(d.titre)}</strong></td><td>${esc(d.revision)}</td>
      <td>${fmtDate(d.date)}</td><td>${esc(d.auteur)}</td><td>${esc(d.approbateur || "—")}</td>
      <td>${statutBadge(d.statut)}</td>
      <td style="white-space:nowrap"><button class="btn sm" data-open="${d.id}">${I("eye", 14)} Voir</button></td>
    </tr>`).join("");
}

function viewAudit() {
  const int = DB.audits.filter(a => a.type === "Interne"), ext = DB.audits.filter(a => a.type === "Externe");
  const auditTable = list => `
    <table class="tbl"><thead><tr><th>Réf.</th><th>Audit</th><th>Domaine</th><th>Date</th><th>Auditeur</th><th>Checklist</th><th>Statut</th></tr></thead>
    <tbody>${list.map(a => `<tr><td class="mono">${esc(a.ref)}</td><td><strong>${esc(a.titre)}</strong></td><td>${esc(a.domaine)}</td>
      <td>${fmtDate(a.date)}</td><td>${esc(a.auditeur)}</td><td>${a.checklist ? `<span class="tag">${esc(a.checklist)}</span>` : "—"}</td><td>${statutBadge(a.statut)}</td></tr>`).join("")}</tbody></table>`;
  return pageHead("Audit", "Plan annuel, audits internes et externes, non-conformités et actions correctives", exportBtns("audit")) + `
  <div class="grid-2">
    <div class="card"><div class="card-head"><h3>Audits internes — Plan annuel 2026</h3></div>
      <div class="card-body" style="padding:0;overflow-x:auto">${auditTable(int)}</div></div>
    <div class="card"><div class="card-head"><h3>Audits externes (ANACM)</h3></div>
      <div class="card-body" style="padding:0;overflow-x:auto">${auditTable(ext)}</div></div>
  </div>
  <div class="card" style="margin-top:16px">
    <div class="card-head"><h3>Non-conformités (FNC) & actions correctives</h3>
      <span class="badge-st st-orange">${DB.fnc.filter(f => f.statut !== "Clôturée").length} ouvertes</span></div>
    <div class="card-body" style="padding:0;overflow-x:auto">
      <table class="tbl"><thead><tr><th>Référence</th><th>Domaine</th><th>Niveau</th><th>Description</th><th>Action corrective</th><th>Responsable</th><th>Échéance</th><th>Statut</th>${canEdit() ? "<th></th>" : ""}</tr></thead>
      <tbody>${DB.fnc.map(f => `<tr>
        <td class="mono">${esc(f.ref)}</td><td>${esc(f.domaine)}</td>
        <td>${f.niveau === "Niveau 1" ? `<span class="badge-st st-red">${f.niveau}</span>` : f.niveau === "Niveau 2" ? `<span class="badge-st st-orange">${f.niveau}</span>` : `<span class="badge-st st-gray">${f.niveau}</span>`}</td>
        <td style="max-width:260px">${esc(f.description)}</td><td style="max-width:280px;color:var(--text-2)">${esc(f.action)}</td>
        <td>${esc(f.responsable)}</td><td>${daysTo(f.echeance) < 0 && f.statut !== "Clôturée" ? `<strong style="color:var(--red)">${fmtDate(f.echeance)}</strong>` : fmtDate(f.echeance)}</td>
        <td>${statutBadge(f.statut)}</td>
        ${canEdit() ? `<td>${f.statut !== "Clôturée" ? `<button class="btn sm" data-closefnc="${f.id}">${I("check", 13)} Clôturer</button>` : ""}</td>` : ""}
      </tr>`).join("")}</tbody></table>
    </div>
  </div>`;
}

function viewRisks() {
  const risks = DB.risks;
  const nIntol = risks.filter(r => riskCalc(r.pr, r.gr).tol === "Intolérable").length;
  const nTol = risks.filter(r => riskCalc(r.pr, r.gr).tol.startsWith("Tolérable")).length;
  const nAcc = risks.length - nIntol - nTol;

  // Matrice 5x5 : lignes = probabilité (5 en haut), colonnes = gravité (A à gauche)
  const cellRisks = {};
  risks.forEach(r => { const k = r.pr + "-" + r.gr; (cellRisks[k] ||= []).push(r.ref); });
  let matrix = `<table class="tbl" style="text-align:center"><thead><tr><th style="text-align:center">P \\ G</th>${[5, 4, 3, 2, 1].map(g =>
    `<th style="text-align:center">${GRAV_LETTRE[g]}<br><small style="font-weight:400">${GRAV[g]}</small></th>`).join("")}</tr></thead><tbody>`;
  for (let p = 5; p >= 1; p--) {
    matrix += `<tr><th style="text-align:center">${p}<br><small style="font-weight:400">${PROBA[p]}</small></th>`;
    for (let g = 5; g >= 1; g--) {
      const rc = riskCalc(p, g);
      const refs = cellRisks[p + "-" + g] || [];
      const bg = rc.cls === "st-red" ? "var(--red)" : rc.cls === "st-orange" ? "var(--orange)" : "var(--green)";
      matrix += `<td style="background:${bg};color:#fff;font-weight:700;border-radius:6px;padding:10px 6px" title="${rc.index} — ${rc.tol}${refs.length ? " : " + refs.join(", ") : ""}">
        ${rc.index}${refs.length ? `<div style="font-size:.68rem;background:rgba(255,255,255,.25);border-radius:8px;margin-top:4px;padding:1px 4px">${refs.length} risque${refs.length > 1 ? "s" : ""}</div>` : ""}</td>`;
    }
    matrix += "</tr>";
  }
  matrix += "</tbody></table>";

  return pageHead("Risk Management (SGS)", "Registre des risques — indice, score et tolérabilité calculés automatiquement (matrice OACI 5×5, Doc 9859)",
    (canEdit() ? `<button class="btn solid" id="newRiskBtn">${I("plus", 15)} Nouveau risque</button>` : "") + exportBtns("risks")) + `
  <div class="kpi-grid">
    <div class="kpi"><div class="ic st-red">${I("alert", 21)}</div><div><div class="val">${nIntol}</div><div class="lbl">Risques intolérables (résiduels)</div></div></div>
    <div class="kpi"><div class="ic st-orange">${I("shield", 21)}</div><div><div class="val">${nTol}</div><div class="lbl">Tolérables — mitigation requise</div></div></div>
    <div class="kpi"><div class="ic st-green">${I("check", 21)}</div><div><div class="val">${nAcc}</div><div class="lbl">Acceptables</div></div></div>
    <div class="kpi"><div class="ic st-blue">${I("clipboard", 21)}</div><div><div class="val">${risks.filter(r => r.statut === "Ouvert").length}</div><div class="lbl">Risques ouverts (à traiter)</div></div></div>
  </div>
  <div class="card" style="margin-bottom:16px">
    <div class="card-head"><h3>Matrice de risque 5×5 — position des risques résiduels</h3>
      <span style="font-size:.76rem;color:var(--text-2)">Rouge : intolérable · Orange : tolérable avec mitigation · Vert : acceptable</span></div>
    <div class="card-body" style="overflow-x:auto">${matrix}</div>
  </div>
  <div class="card">
    <div class="card-head"><h3>Registre des risques</h3><span class="badge-st st-blue">${risks.length} risques</span></div>
    <div class="card-body" style="padding:0;overflow-x:auto">
      <table class="tbl"><thead><tr><th>Réf.</th><th>Danger / menace</th><th>Domaine</th><th>Risque initial</th><th>Mitigation</th><th>Risque résiduel</th><th>Responsable</th><th>Revue</th><th>Statut</th><th></th></tr></thead>
      <tbody>${risks.map(r => `
        <tr class="clickable" data-risk="${r.id}">
          <td class="mono">${esc(r.ref)}</td>
          <td style="max-width:230px"><strong>${esc(r.danger)}</strong><div style="font-size:.76rem;color:var(--text-2);margin-top:2px">${esc(r.consequences)}</div></td>
          <td><span class="tag">${esc(r.domaine)}</span></td>
          <td>${riskBadge(r.pi, r.gi)}</td>
          <td style="max-width:250px;color:var(--text-2);font-size:.8rem">${esc(r.mitigation)}</td>
          <td>${riskBadge(r.pr, r.gr)}</td>
          <td>${esc(r.responsable)}</td>
          <td>${daysTo(r.revue) < 0 ? `<strong style="color:var(--red)">${fmtDate(r.revue)}</strong>` : fmtDate(r.revue)}</td>
          <td>${statutBadge(r.statut)}</td>
          <td>${canEdit() ? `<button class="btn sm" data-editrisk="${r.id}">${I("edit", 13)} Évaluer</button>` : ""}</td>
        </tr>`).join("")}</tbody></table>
    </div>
  </div>`;
}

function openRiskModal(id) {
  const r = id ? DB.risks.find(x => x.id === id) : null;
  const val = (f, dflt = "") => r ? r[f] : dflt;
  const selP = (name, cur) => `<select id="${name}" style="width:100%;padding:10px;border:1.5px solid var(--border);border-radius:8px;background:var(--surface);color:var(--text)">
    ${[1, 2, 3, 4, 5].map(v => `<option value="${v}" ${+cur === v ? "selected" : ""}>${v} — ${PROBA[v]}</option>`).join("")}</select>`;
  const selG = (name, cur) => `<select id="${name}" style="width:100%;padding:10px;border:1.5px solid var(--border);border-radius:8px;background:var(--surface);color:var(--text)">
    ${[5, 4, 3, 2, 1].map(v => `<option value="${v}" ${+cur === v ? "selected" : ""}>${GRAV_LETTRE[v]} (${v}) — ${GRAV[v]}</option>`).join("")}</select>`;
  const inp = (id2, v, ph = "") => `<input id="${id2}" value="${esc(v)}" placeholder="${ph}" style="width:100%;padding:10px;border:1.5px solid var(--border);border-radius:8px;background:var(--surface);color:var(--text)">`;

  openModal(`
    <div class="m-head"><div><span class="mono">${r ? esc(r.ref) : "Nouveau risque"}</span><h3>${r ? "Évaluation du risque" : "Identifier un nouveau risque"}</h3></div>
      <button class="m-close" data-close>✕</button></div>
    <div class="m-body">
      <div class="grid-2">
        <div class="field"><label>Référence</label>${inp("rkRef", val("ref", "RISK-26-0" + (DB.risks.length + 1)))}</div>
        <div class="field"><label>Domaine</label>${inp("rkDom", val("domaine"), "OPS / AIR / AVSEC / Ground…")}</div>
      </div>
      <div class="field"><label>Danger / menace identifié</label>${inp("rkDanger", val("danger"))}</div>
      <div class="field"><label>Conséquences possibles</label>${inp("rkCons", val("consequences"))}</div>
      <div class="card" style="padding:14px;margin-bottom:14px;box-shadow:none">
        <strong style="font-size:.85rem">Risque INITIAL (avant mitigation)</strong>
        <div class="grid-2" style="margin-top:10px">
          <div class="field"><label>Probabilité</label>${selP("rkPi", val("pi", 3))}</div>
          <div class="field"><label>Gravité</label>${selG("rkGi", val("gi", 3))}</div>
        </div>
        <div id="rkCalcInit" style="font-size:.9rem"></div>
      </div>
      <div class="field"><label>Mesures de mitigation / barrières</label>${inp("rkMit", val("mitigation"))}</div>
      <div class="card" style="padding:14px;margin-bottom:14px;box-shadow:none">
        <strong style="font-size:.85rem">Risque RÉSIDUEL (après mitigation)</strong>
        <div class="grid-2" style="margin-top:10px">
          <div class="field"><label>Probabilité</label>${selP("rkPr", val("pr", 2))}</div>
          <div class="field"><label>Gravité</label>${selG("rkGr", val("gr", 3))}</div>
        </div>
        <div id="rkCalcRes" style="font-size:.9rem"></div>
      </div>
      <div class="grid-2">
        <div class="field"><label>Responsable</label>${inp("rkResp", val("responsable", SESSION.name))}</div>
        <div class="field"><label>Prochaine revue (AAAA-MM-JJ)</label>${inp("rkRevue", val("revue"), "2026-12-31")}</div>
      </div>
      <button class="btn solid" id="rkSave">${I("check", 15)} Enregistrer l'évaluation</button>
    </div>`);

  const refresh = () => {
    const ci = riskCalc($("#rkPi").value, $("#rkGi").value);
    const cr = riskCalc($("#rkPr").value, $("#rkGr").value);
    $("#rkCalcInit").innerHTML = `Calcul automatique : indice <strong>${ci.index}</strong> · score <strong>${ci.score}</strong> → <span class="badge-st ${ci.cls}">${ci.tol}</span>`;
    $("#rkCalcRes").innerHTML = `Calcul automatique : indice <strong>${cr.index}</strong> · score <strong>${cr.score}</strong> → <span class="badge-st ${cr.cls}">${cr.tol}</span>` +
      (cr.score > ci.score ? `<div style="color:var(--red);font-size:.78rem;margin-top:4px">⚠ Le risque résiduel est supérieur au risque initial — vérifiez l'évaluation.</div>` : "");
  };
  ["rkPi", "rkGi", "rkPr", "rkGr"].forEach(i => $("#" + i).addEventListener("change", refresh));
  refresh();

  $("#rkSave").addEventListener("click", () => {
    if (!$("#rkDanger").value.trim()) { toast("Décrivez le danger identifié"); return; }
    const data = {
      ref: $("#rkRef").value.trim(), domaine: $("#rkDom").value.trim(), danger: $("#rkDanger").value.trim(),
      consequences: $("#rkCons").value.trim(), pi: +$("#rkPi").value, gi: +$("#rkGi").value,
      mitigation: $("#rkMit").value.trim(), pr: +$("#rkPr").value, gr: +$("#rkGr").value,
      responsable: $("#rkResp").value.trim(), revue: $("#rkRevue").value.trim()
    };
    const res = riskCalc(data.pr, data.gr);
    data.statut = res.tol === "Acceptable" ? "Maîtrisé" : "Ouvert";
    if (r) Object.assign(r, data);
    else DB.risks.push({ id: "r" + Date.now(), ...data });
    logAction(`${r ? "Réévaluation" : "Création"} du risque ${data.ref} — résiduel ${res.index} (${res.tol})`);
    saveDB(); closeModal(); navigate("risks"); updateNotifBadge();
    toast(`Risque ${data.ref} enregistré — tolérabilité calculée : ${res.tol}`);
  });
}

function viewTraining() {
  return pageHead("Training", "Calendrier des formations, validités et renouvellements — Programme triennal 2024-2026", exportBtns("training")) + `
  <div class="card"><div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Réf.</th><th>Formation</th><th>Durée</th><th>Validité</th><th>Prochaine session</th><th>Participants</th><th>Formateur</th><th>Statut</th></tr></thead>
    <tbody>${DB.trainings.map(t => `<tr>
      <td class="mono">${esc(t.ref)}</td><td><strong>${esc(t.titre)}</strong></td><td>${esc(t.duree)}</td>
      <td>${t.validite ? t.validite + " mois" : "Une fois"}</td>
      <td>${daysTo(t.prochaine) <= 30 ? `<strong style="color:var(--orange)">${fmtDate(t.prochaine)}</strong>` : fmtDate(t.prochaine)}</td>
      <td style="max-width:240px">${t.participants.map(p => `<span class="tag">${esc(p)}</span>`).join("")}</td>
      <td>${esc(t.formateur)}</td><td>${statutBadge(t.statut)}</td></tr>`).join("")}</tbody></table>
  </div></div>
  <div class="card" style="margin-top:16px">
    <div class="card-head"><h3>Validités individuelles (certificats de formation)</h3></div>
    <div class="card-body" style="padding:0;overflow-x:auto">
      <table class="tbl"><thead><tr><th>Employé</th><th>Certificat / formation</th><th>Obtenu le</th><th>Validité</th></tr></thead>
      <tbody>${DB.personnel.flatMap(p => p.docs.filter(d => ["Training", "Attestation"].includes(d.type)).map(d =>
        `<tr><td><strong>${esc(p.nom)}</strong></td><td>${esc(d.titre)}</td><td>${fmtDate(d.date)}</td><td>${expiryBadge(d.expire)}</td></tr>`)).join("")}</tbody></table>
    </div>
  </div>`;
}

function viewProcedures() {
  const familles = ["Ground Procedures", "Flight Operations", "Maintenance", "Safety", "Security", "Quality"];
  return pageHead("Procedures", "Procédures classées par domaine — rédigées selon vos documents Royal Air (DOC-PROC, QUA-PROC…)", exportBtns("procedures")) +
    familles.map(f => {
      const procs = DB.procedures.filter(p => p.famille === f);
      if (!procs.length) return "";
      return `<div class="card" style="margin-bottom:16px">
        <div class="card-head"><h3>${esc(f)}</h3><span class="badge-st st-blue">${procs.length}</span></div>
        <div class="card-body" style="padding:0;overflow-x:auto">
          <table class="tbl"><thead><tr><th>Numéro</th><th>Titre</th><th>Révision</th><th>Date</th><th>Auteur</th><th>Statut</th><th></th></tr></thead>
          <tbody>${procs.map(p => `<tr class="clickable" data-proc="${p.id}">
            <td class="mono">${esc(p.num)}</td><td><strong>${esc(p.titre)}</strong></td><td>${esc(p.revision)}</td>
            <td>${fmtDate(p.date)}</td><td>${esc(p.auteur)}</td><td>${statutBadge(p.statut)}</td>
            <td><button class="btn sm" data-openproc="${p.id}">${I("eye", 14)} Consulter</button></td></tr>`).join("")}</tbody></table>
        </div></div>`;
    }).join("");
}

function viewChecklists() {
  return pageHead("Checklists", "Checklists officielles en version contrôlée — cochez, puis imprimez pour vos audits et opérations", exportBtns("checklists")) + `
  <div class="pers-grid">${DB.checklists.map(c => `
    <div class="card" style="cursor:pointer" data-ck="${c.id}">
      <div class="card-head"><h3 style="font-size:.9rem">${esc(c.num)}</h3>${statutBadge(c.statut)}</div>
      <div class="card-body">
        <strong style="font-size:.93rem">${esc(c.titre)}</strong>
        <div style="font-size:.78rem;color:var(--text-2);margin-top:7px">${esc(c.famille)} · ${esc(c.revision)} · ${fmtDate(c.date)} · ${c.items.length} points</div>
        <button class="btn sm" style="margin-top:12px" data-openck="${c.id}">${I("check", 14)} Ouvrir la checklist</button>
      </div>
    </div>`).join("")}</div>`;
}

function viewCrew() {
  return pageHead("Crew", "Équipages : pilotes et cabin crew — licences, medical, qualifications", exportBtns("crew")) + `
  <div class="card"><div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Membre</th><th>Type</th><th>Poste</th><th>Licence</th><th>Validité licence</th><th>Validité medical</th><th>Qualifications</th><th>Statut</th></tr></thead>
    <tbody>${DB.crew.map(c => `<tr>
      <td><strong>${esc(c.nom)}</strong></td><td>${esc(c.type)}</td><td>${esc(c.poste)}</td>
      <td><span class="tag">${esc(c.licence)}</span></td><td>${expiryBadge(c.licExp)}</td><td>${expiryBadge(c.medExp)}</td>
      <td>${c.quals.map(q => `<span class="tag">${esc(q)}</span>`).join("")}</td><td>${statutBadge(c.statut)}</td></tr>`).join("")}</tbody></table>
  </div></div>`;
}

function viewScheduling() {
  return pageHead("Scheduling", "Planning des vols, affectation équipages, congés et disponibilités", exportBtns("scheduling")) + `
  <div class="card"><div class="card-head"><h3>Planning des vols — réseau HAH · AJN · NWA</h3></div>
    <div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Date</th><th>Vol</th><th>Route</th><th>Dép.</th><th>Arr.</th><th>Avion</th><th>CDB</th><th>OPL</th><th>PNC</th><th>Statut</th></tr></thead>
    <tbody>${DB.flights.map(v => `<tr>
      <td>${fmtDate(v.date)}</td><td class="mono">${esc(v.num)}</td><td><strong>${esc(v.route)}</strong></td>
      <td>${esc(v.dep)}</td><td>${esc(v.arr)}</td><td>${esc(v.avion)}</td><td>${esc(v.cdb)}</td><td>${esc(v.opl)}</td><td>${esc(v.pnc)}</td>
      <td>${statutBadge(v.statut)}</td></tr>`).join("")}</tbody></table>
  </div></div>
  <div class="card" style="margin-top:16px"><div class="card-head"><h3>Congés & disponibilités</h3></div>
    <div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Employé</th><th>Type</th><th>Du</th><th>Au</th><th>Statut</th></tr></thead>
    <tbody>${DB.leaves.map(l => `<tr><td><strong>${esc(l.nom)}</strong></td><td>${esc(l.type)}</td>
      <td>${fmtDate(l.debut)}</td><td>${fmtDate(l.fin)}</td><td>${statutBadge(l.statut)}</td></tr>`).join("")}</tbody></table>
  </div></div>`;
}

function viewReports() {
  const expDocs = [];
  DB.aircraft.forEach(ac => ac.docs.forEach(d => { if (d.expire && daysTo(d.expire) <= 90) expDocs.push({ ctx: ac.immat, ...d }); }));
  DB.documents.forEach(d => { if (d.expire && daysTo(d.expire) <= 90) expDocs.push({ ctx: d.module, ...d }); });
  const expLic = [];
  DB.personnel.forEach(p => p.docs.forEach(d => { if (d.expire && daysTo(d.expire) <= 90) expLic.push({ nom: p.nom, ...d }); }));
  const closRate = Math.round(100 * DB.fnc.filter(f => f.statut === "Clôturée").length / (DB.fnc.length || 1));
  const onTime = DB.fnc.filter(f => f.statut === "Clôturée" || daysTo(f.echeance) >= 0).length;

  return pageHead("Rapports & KPI Qualité", "Génération automatique : audits, documents expirés, licences, statistiques",
    `<button class="btn" onclick="window.print()">${I("print", 15)} Export PDF</button>
     <button class="btn solid" id="exportAllBtn">${I("download", 15)} Export Excel (CSV)</button>`) + `
  <div class="kpi-grid">
    <div class="kpi"><div class="ic st-green">${I("chart", 21)}</div><div><div class="val">${closRate}%</div><div class="lbl">Taux de clôture des FNC</div></div></div>
    <div class="kpi"><div class="ic st-blue">${I("clipboard", 21)}</div><div><div class="val">${Math.round(100 * onTime / (DB.fnc.length || 1))}%</div><div class="lbl">FNC dans les délais</div></div></div>
    <div class="kpi"><div class="ic st-orange">${I("file", 21)}</div><div><div class="val">${expDocs.length}</div><div class="lbl">Documents expirant ≤ 90 j</div></div></div>
    <div class="kpi"><div class="ic st-red">${I("users", 21)}</div><div><div class="val">${expLic.length}</div><div class="lbl">Licences / certificats ≤ 90 j</div></div></div>
  </div>
  <div class="grid-2">
    <div class="card"><div class="card-head"><h3>Documents expirés ou expirant sous 90 jours</h3></div>
      <div class="card-body" style="padding:0;overflow-x:auto">
      <table class="tbl"><thead><tr><th>Contexte</th><th>Document</th><th>Échéance</th></tr></thead>
      <tbody>${expDocs.map(d => `<tr><td class="mono">${esc(d.ctx)}</td><td><strong>${esc(d.titre)}</strong></td><td>${expiryBadge(d.expire)}</td></tr>`).join("") || `<tr><td colspan="3"><div class="empty">Rien à signaler.</div></td></tr>`}</tbody></table>
    </div></div>
    <div class="card"><div class="card-head"><h3>Licences & certificats personnel ≤ 90 jours</h3></div>
      <div class="card-body" style="padding:0;overflow-x:auto">
      <table class="tbl"><thead><tr><th>Employé</th><th>Document</th><th>Échéance</th></tr></thead>
      <tbody>${expLic.map(d => `<tr><td><strong>${esc(d.nom)}</strong></td><td>${esc(d.titre)}</td><td>${expiryBadge(d.expire)}</td></tr>`).join("") || `<tr><td colspan="3"><div class="empty">Rien à signaler.</div></td></tr>`}</tbody></table>
    </div></div>
  </div>
  <div class="card" style="margin-top:16px"><div class="card-head"><h3>Rapport d'audit — synthèse annuelle</h3></div>
    <div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Réf.</th><th>Audit</th><th>Type</th><th>Date</th><th>Statut</th><th>FNC associées</th></tr></thead>
    <tbody>${DB.audits.map(a => `<tr><td class="mono">${esc(a.ref)}</td><td><strong>${esc(a.titre)}</strong></td><td>${esc(a.type)}</td>
      <td>${fmtDate(a.date)}</td><td>${statutBadge(a.statut)}</td>
      <td>${a.ref.includes("PH4") ? DB.fnc.length + " FNC (voir module Audit)" : "—"}</td></tr>`).join("")}</tbody></table>
  </div></div>`;
}

function viewUsers() {
  return pageHead("Utilisateurs & rôles", "Chaque rôle possède uniquement les droits nécessaires (moindre privilège)", "") + `
  <div class="card"><div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Utilisateur</th><th>Identifiant</th><th>Rôle</th><th>Département</th><th>Droits</th></tr></thead>
    <tbody>${DB.users.map(u => {
      const r = DB.roles[u.role] || {};
      const droits = { x: "Administration complète", a: "Lecture + édition + approbation", e: "Lecture + édition", v: "Lecture seule" }[r.rights] || "—";
      return `<tr><td><strong>${esc(u.name)}</strong></td><td class="mono">${esc(u.username)}</td>
        <td><span class="tag">${esc(u.role)}</span></td><td>${esc(u.dept)}</td><td>${droits}</td></tr>`;
    }).join("")}</tbody></table>
  </div></div>
  <div class="card" style="margin-top:16px"><div class="card-head"><h3>Sécurité (production)</h3></div>
    <div class="card-body" style="font-size:.88rem;line-height:1.7;color:var(--text-2)">
    En déploiement Netlify + Supabase : HTTPS obligatoire, authentification <strong>Supabase Auth</strong> (JWT), double authentification (2FA TOTP),
    mots de passe chiffrés (bcrypt), Row Level Security par rôle, journal des connexions, sauvegardes automatiques quotidiennes et protection contre les attaques (rate limiting).
    </div></div>`;
}

function viewJournal() {
  return pageHead("Journal système", "Traçabilité complète : connexions, consultations, approbations, modifications", "") + `
  <div class="card"><div class="card-body" style="padding:0;overflow-x:auto">
    <table class="tbl"><thead><tr><th>Horodatage</th><th>Utilisateur</th><th>Action</th></tr></thead>
    <tbody>${DB.journal.map(j => `<tr><td class="mono">${esc(j.date)}</td><td><strong>${esc(j.user)}</strong></td><td>${esc(j.action)}</td></tr>`).join("")}</tbody></table>
  </div></div>`;
}

/* ---------------- Modals ---------------- */
function openModal(html) {
  $("#modalBox").innerHTML = html;
  $("#modalBack").classList.add("open");
  $("#modalBox").querySelectorAll("[data-close]").forEach(b => b.addEventListener("click", closeModal));
}
function closeModal() { $("#modalBack").classList.remove("open"); }

function openDocModal(id) {
  const d = DB.documents.find(x => x.id === id);
  if (!d) return;
  logAction(`Consultation ${d.num} — ${d.titre}`);
  const hist = (d.historique || []).slice().reverse();
  const actions = [];
  if (canEdit() && d.statut === "Brouillon") actions.push(`<button class="btn" data-wf="review">${I("edit", 14)} Soumettre en révision</button>`);
  if (canApprove() && (d.statut === "En révision" || d.statut === "Brouillon")) actions.push(`<button class="btn solid" data-wf="approve">${I("sign", 14)} Approuver (signature électronique)</button>`);
  if (canEdit() && d.statut === "Approuvé") actions.push(`<button class="btn" data-wf="revise">${I("history", 14)} Nouvelle révision</button>`);
  if (canApprove() && d.statut !== "Archivé") actions.push(`<button class="btn danger" data-wf="archive">${I("archive", 14)} Archiver</button>`);

  openModal(`
    <div class="m-head"><div><span class="mono">${esc(d.num)} · ${esc(d.revision)}</span><h3>${esc(d.titre)}</h3></div>
      <button class="m-close" data-close>✕</button></div>
    <div class="m-body">
      <div class="meta-grid">
        <div class="mi"><div class="k">Statut</div><div class="v">${statutBadge(d.statut)}</div></div>
        <div class="mi"><div class="k">Date</div><div class="v">${fmtDate(d.date)}</div></div>
        <div class="mi"><div class="k">Auteur</div><div class="v">${esc(d.auteur)}</div></div>
        <div class="mi"><div class="k">Vérificateur</div><div class="v">${esc(d.verificateur || "—")}</div></div>
        <div class="mi"><div class="k">Approbateur</div><div class="v">${esc(d.approbateur || "—")}</div></div>
        <div class="mi"><div class="k">Catégorie</div><div class="v">${esc(d.categorie)}</div></div>
      </div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px">
        <button class="btn sm" onclick="toast('Version PDF disponible après connexion à Supabase Storage')">${I("download", 14)} PDF</button>
        <button class="btn sm" onclick="toast('Version Word disponible après connexion à Supabase Storage')">${I("download", 14)} Word</button>
        ${actions.join("")}
      </div>
      <h4 style="font-size:.85rem;margin-bottom:12px;color:var(--text-2);text-transform:uppercase;letter-spacing:.8px">Historique des révisions</h4>
      <div class="hist">${hist.map(h => `<div class="h-item"><div class="h-rev">${esc(h.rev)} — ${fmtDate(h.date)}</div><div class="h-note">${esc(h.note)}</div></div>`).join("") || "<div class='empty'>Aucun historique.</div>"}</div>
    </div>`);

  $("#modalBox").querySelectorAll("[data-wf]").forEach(b => b.addEventListener("click", () => {
    const wf = b.dataset.wf;
    d.historique = d.historique || [];
    const nowStr = localISO();
    if (wf === "review") { d.statut = "En révision"; d.historique.push({ rev: d.revision, date: nowStr, note: `Soumis en révision par ${SESSION.name}` }); toast("Document soumis en révision"); }
    if (wf === "approve") { d.statut = "Approuvé"; d.approbateur = SESSION.name; d.historique.push({ rev: d.revision, date: nowStr, note: `✍ Approuvé et signé électroniquement par ${SESSION.name} (${SESSION.role})` }); toast("Document approuvé — signature électronique enregistrée"); }
    if (wf === "revise") {
      const m = d.revision.match(/Rév\.(\d+)/);
      d.revision = m ? d.revision.replace(/Rév\.\d+/, "Rév." + (+m[1] + 1)) : d.revision + " Rév.1";
      d.statut = "Brouillon"; d.date = nowStr;
      d.historique.push({ rev: d.revision, date: nowStr, note: `Nouvelle révision initiée par ${SESSION.name}` });
      toast("Nouvelle révision créée (statut Brouillon)");
    }
    if (wf === "archive") { d.statut = "Archivé"; d.historique.push({ rev: d.revision, date: nowStr, note: `Archivé par ${SESSION.name} (cf. DOC-PROC-002)` }); toast("Document archivé"); }
    logAction(`${wf.toUpperCase()} sur ${d.num}`);
    saveDB(); closeModal(); navigate(CURRENT); updateNotifBadge();
  }));
}

function openProcModal(id) {
  const p = DB.procedures.find(x => x.id === id);
  if (!p) return;
  logAction(`Consultation procédure ${p.num}`);
  openModal(`
    <div class="m-head"><div><span class="mono">${esc(p.num)} · ${esc(p.revision)} · ${fmtDate(p.date)}</span><h3>${esc(p.titre)}</h3></div>
      <button class="m-close" data-close>✕</button></div>
    <div class="m-body">
      <div style="display:flex;gap:8px;margin-bottom:18px">${statutBadge(p.statut)}<span class="tag">${esc(p.famille)}</span><span class="tag">Auteur : ${esc(p.auteur)}</span></div>
      ${p.contenu.map(([h, t]) => `<div class="proc-section"><h4>${esc(h)}</h4><p>${esc(t)}</p></div>`).join("")}
      <div style="margin-top:18px;display:flex;gap:8px">
        <button class="btn" onclick="window.print()">${I("print", 14)} Imprimer</button>
      </div>
    </div>`);
}

function openCkModal(id) {
  const c = DB.checklists.find(x => x.id === id);
  if (!c) return;
  logAction(`Ouverture checklist ${c.num}`);
  openModal(`
    <div class="m-head"><div><span class="mono">${esc(c.num)} · ${esc(c.revision)}</span><h3>${esc(c.titre)}</h3></div>
      <button class="m-close" data-close>✕</button></div>
    <div class="m-body">
      <div style="display:flex;gap:8px;margin-bottom:16px;align-items:center">${statutBadge(c.statut)}<span class="tag">${esc(c.famille)}</span>
        <span style="font-size:.8rem;color:var(--text-2)" id="ckProgress">0 / ${c.items.length}</span></div>
      <div id="ckList">${c.items.map((it, i) => `
        <label class="ck-item"><input type="checkbox" data-cki="${i}"><span>${esc(it)}</span></label>`).join("")}</div>
      <div style="margin-top:16px;display:flex;gap:8px">
        <button class="btn" onclick="window.print()">${I("print", 14)} Imprimer</button>
        <button class="btn solid" id="ckDone">${I("check", 14)} Valider l'exécution</button>
      </div>
    </div>`);
  const upd = () => {
    const n = $("#ckList").querySelectorAll("input:checked").length;
    $("#ckProgress").textContent = `${n} / ${c.items.length}`;
    $("#ckList").querySelectorAll(".ck-item").forEach(el => el.classList.toggle("done", el.querySelector("input").checked));
  };
  $("#ckList").addEventListener("change", upd);
  $("#ckDone").addEventListener("click", () => {
    const n = $("#ckList").querySelectorAll("input:checked").length;
    logAction(`Checklist ${c.num} exécutée (${n}/${c.items.length} points conformes) par ${SESSION.name}`);
    toast(`Checklist enregistrée au journal : ${n}/${c.items.length} points conformes`);
    closeModal();
  });
}

function openPersModal(id) {
  const p = DB.personnel.find(x => x.id === id);
  if (!p) return;
  logAction(`Consultation dossier ${p.nom}`);
  openModal(`
    <div class="m-head"><div><span class="mono">${esc(p.dept)}</span><h3>${esc(p.nom)} — ${esc(p.fonction)}</h3></div>
      <button class="m-close" data-close>✕</button></div>
    <div class="m-body">
      <div class="meta-grid">
        <div class="mi"><div class="k">Embauche</div><div class="v">${fmtDate(p.embauche)}</div></div>
        <div class="mi"><div class="k">Documents</div><div class="v">${p.docs.length}</div></div>
        <div class="mi"><div class="k">Qualifications</div><div class="v">${p.qualifications.length}</div></div>
      </div>
      <div style="margin-bottom:16px">${p.qualifications.map(q => `<span class="tag">${esc(q)}</span>`).join("")}</div>
      <table class="tbl"><thead><tr><th>Type</th><th>Document</th><th>Date</th><th>Validité</th></tr></thead>
      <tbody>${p.docs.map(d => `<tr><td><span class="tag">${esc(d.type)}</span></td><td><strong>${esc(d.titre)}</strong></td>
        <td>${fmtDate(d.date)}</td><td>${expiryBadge(d.expire)}</td></tr>`).join("")}</tbody></table>
    </div>`);
}

/* ---------------- Nouveau document ---------------- */
function openNewDocModal(mod) {
  openModal(`
    <div class="m-head"><div><h3>Nouveau document — ${mod === "manuals" ? "Manuel" : "Politique"}</h3></div>
      <button class="m-close" data-close>✕</button></div>
    <div class="m-body">
      <div class="field"><label>Numéro de référence</label><input id="ndNum" placeholder="ex. RA-XXX-001" style="width:100%;padding:10px;border:1.5px solid var(--border);border-radius:8px;background:var(--surface);color:var(--text)"></div>
      <div class="field"><label>Titre</label><input id="ndTitre" placeholder="Titre du document" style="width:100%;padding:10px;border:1.5px solid var(--border);border-radius:8px;background:var(--surface);color:var(--text)"></div>
      <div class="field"><label>Auteur</label><input id="ndAuteur" value="${esc(SESSION.name)}" style="width:100%;padding:10px;border:1.5px solid var(--border);border-radius:8px;background:var(--surface);color:var(--text)"></div>
      <button class="btn solid" id="ndCreate" style="margin-top:6px">${I("plus", 15)} Créer (statut Brouillon)</button>
    </div>`);
  $("#ndCreate").addEventListener("click", () => {
    const num = $("#ndNum").value.trim(), titre = $("#ndTitre").value.trim();
    if (!num || !titre) { toast("Numéro et titre obligatoires"); return; }
    const nowStr = localISO();
    DB.documents.push({
      id: "d" + Date.now(), module: mod, categorie: mod === "manuals" ? "Manuel" : "Politique",
      num, titre, revision: "Éd.1 Rév.0", date: nowStr, auteur: $("#ndAuteur").value.trim(),
      verificateur: "", approbateur: "", statut: "Brouillon", expire: "",
      historique: [{ rev: "Éd.1 Rév.0", date: nowStr, note: `Créé par ${SESSION.name} (conforme DOC-PROC-001 §5.1)` }]
    });
    logAction(`Création du document ${num} — ${titre}`);
    saveDB(); closeModal(); navigate(CURRENT); toast("Document créé au statut Brouillon");
  });
}

/* ---------------- Export CSV ---------------- */
function exportBtns(mod) {
  return `<button class="btn" data-export="${mod}">${I("download", 15)} Export Excel</button>`;
}
function toCSV(rows) {
  return "﻿" + rows.map(r => r.map(c => `"${String(c ?? "").replace(/"/g, '""')}"`).join(";")).join("\r\n");
}
function download(name, content) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([content], { type: "text/csv;charset=utf-8" }));
  a.download = name; a.click(); URL.revokeObjectURL(a.href);
}
function exportModule(mod) {
  let rows = [];
  if (mod === "manuals" || mod === "policies") {
    rows = [["Numéro", "Titre", "Révision", "Date", "Auteur", "Vérificateur", "Approbateur", "Statut"]];
    DB.documents.filter(d => d.module === mod).forEach(d => rows.push([d.num, d.titre, d.revision, d.date, d.auteur, d.verificateur, d.approbateur, d.statut]));
  } else if (mod === "aircraft") {
    rows = [["Immat", "Numéro", "Document", "Type", "Révision", "Date", "Expire", "Statut"]];
    DB.aircraft.forEach(ac => ac.docs.forEach(d => rows.push([ac.immat, d.num, d.titre, d.type, d.revision, d.date, d.expire, d.statut])));
  } else if (mod === "personnel") {
    rows = [["Nom", "Fonction", "Type", "Document", "Date", "Expire", "Statut"]];
    DB.personnel.forEach(p => p.docs.forEach(d => rows.push([p.nom, p.fonction, d.type, d.titre, d.date, d.expire, d.statut])));
  } else if (mod === "audit") {
    rows = [["Référence", "Domaine", "Niveau", "Description", "Action", "Responsable", "Échéance", "Statut"]];
    DB.fnc.forEach(f => rows.push([f.ref, f.domaine, f.niveau, f.description, f.action, f.responsable, f.echeance, f.statut]));
  } else if (mod === "training") {
    rows = [["Réf", "Formation", "Durée", "Validité (mois)", "Prochaine", "Formateur", "Statut"]];
    DB.trainings.forEach(t => rows.push([t.ref, t.titre, t.duree, t.validite, t.prochaine, t.formateur, t.statut]));
  } else if (mod === "crew") {
    rows = [["Nom", "Type", "Poste", "Licence", "Exp. licence", "Exp. medical", "Statut"]];
    DB.crew.forEach(c => rows.push([c.nom, c.type, c.poste, c.licence, c.licExp, c.medExp, c.statut]));
  } else if (mod === "scheduling") {
    rows = [["Date", "Vol", "Route", "Départ", "Arrivée", "Avion", "CDB", "OPL", "PNC", "Statut"]];
    DB.flights.forEach(v => rows.push([v.date, v.num, v.route, v.dep, v.arr, v.avion, v.cdb, v.opl, v.pnc, v.statut]));
  } else if (mod === "procedures") {
    rows = [["Numéro", "Titre", "Famille", "Révision", "Date", "Auteur", "Statut"]];
    DB.procedures.forEach(p => rows.push([p.num, p.titre, p.famille, p.revision, p.date, p.auteur, p.statut]));
  } else if (mod === "risks") {
    rows = [["Référence", "Danger", "Domaine", "Conséquences", "P init", "G init", "Indice init", "Tolérabilité init", "Mitigation", "P rés", "G rés", "Indice rés", "Tolérabilité rés", "Responsable", "Revue", "Statut"]];
    DB.risks.forEach(r => {
      const ci = riskCalc(r.pi, r.gi), cr = riskCalc(r.pr, r.gr);
      rows.push([r.ref, r.danger, r.domaine, r.consequences, r.pi, r.gi, ci.index, ci.tol, r.mitigation, r.pr, r.gr, cr.index, cr.tol, r.responsable, r.revue, r.statut]);
    });
  } else if (mod === "checklists") {
    rows = [["Numéro", "Titre", "Famille", "Révision", "Points"]];
    DB.checklists.forEach(c => rows.push([c.num, c.titre, c.famille, c.revision, c.items.length]));
  } else {
    rows = [["Numéro", "Titre", "Module", "Statut"]];
    DB.documents.forEach(d => rows.push([d.num, d.titre, d.module, d.statut]));
  }
  download(`RA-QDMS_${mod}_${localISO()}.csv`, toCSV(rows));
  logAction(`Export Excel du module ${mod}`);
  toast("Export CSV téléchargé (compatible Excel)");
}

/* ---------------- Recherche globale ---------------- */
function globalSearch(q) {
  q = q.toLowerCase().trim();
  if (q.length < 2) return [];
  const res = [];
  const test = (...fields) => fields.some(f => String(f || "").toLowerCase().includes(q));
  DB.documents.forEach(d => { if (test(d.num, d.titre, d.auteur, d.revision, d.date, d.statut)) res.push({ type: d.categorie, label: `${d.num} — ${d.titre}`, go: () => { navigate(d.module); setTimeout(() => openDocModal(d.id), 60); } }); });
  DB.procedures.forEach(p => { if (test(p.num, p.titre, p.auteur, p.famille)) res.push({ type: "Procédure", label: `${p.num} — ${p.titre}`, go: () => { navigate("procedures"); setTimeout(() => openProcModal(p.id), 60); } }); });
  DB.checklists.forEach(c => { if (test(c.num, c.titre, c.famille)) res.push({ type: "Checklist", label: `${c.num} — ${c.titre}`, go: () => { navigate("checklists"); setTimeout(() => openCkModal(c.id), 60); } }); });
  DB.personnel.forEach(p => { if (test(p.nom, p.fonction, p.dept)) res.push({ type: "Personnel", label: `${p.nom} — ${p.fonction}`, go: () => { navigate("personnel"); setTimeout(() => openPersModal(p.id), 60); } }); });
  DB.fnc.forEach(f => { if (test(f.ref, f.description, f.domaine, f.responsable)) res.push({ type: "FNC", label: `${f.ref} — ${f.description}`, go: () => navigate("audit") }); });
  DB.audits.forEach(a => { if (test(a.ref, a.titre, a.domaine)) res.push({ type: "Audit", label: `${a.ref} — ${a.titre}`, go: () => navigate("audit") }); });
  DB.aircraft.forEach(ac => ac.docs.forEach(d => { if (test(d.num, d.titre, ac.immat)) res.push({ type: `Aéronef ${ac.immat}`, label: `${d.num} — ${d.titre}`, go: () => navigate("aircraft") }); }));
  DB.risks.forEach(r => { if (test(r.ref, r.danger, r.domaine, r.responsable)) res.push({ type: "Risque SGS", label: `${r.ref} — ${r.danger}`, go: () => navigate("risks") }); });
  return res.slice(0, 12);
}

/* ---------------- Liaison des vues ---------------- */
function bindView(mod) {
  document.querySelectorAll("[data-export]").forEach(b => b.addEventListener("click", () => exportModule(b.dataset.export)));
  document.querySelectorAll("[data-open]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); openDocModal(b.dataset.open); }));
  document.querySelectorAll("tr[data-doc]").forEach(tr => tr.addEventListener("click", () => openDocModal(tr.dataset.doc)));
  document.querySelectorAll("[data-openproc]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); openProcModal(b.dataset.openproc); }));
  document.querySelectorAll("tr[data-proc]").forEach(tr => tr.addEventListener("click", () => openProcModal(tr.dataset.proc)));
  document.querySelectorAll("[data-openck]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); openCkModal(b.dataset.openck); }));
  document.querySelectorAll("[data-ck]").forEach(c => c.addEventListener("click", () => openCkModal(c.dataset.ck)));
  document.querySelectorAll(".pers-card[data-pid]").forEach(c => c.addEventListener("click", () => openPersModal(c.dataset.pid)));
  document.querySelectorAll("[data-closefnc]").forEach(b => b.addEventListener("click", () => {
    const f = DB.fnc.find(x => x.id === b.dataset.closefnc);
    f.statut = "Clôturée";
    logAction(`Clôture de la FNC ${f.ref} par ${SESSION.name}`);
    saveDB(); navigate("audit"); updateNotifBadge(); toast(`FNC ${f.ref} clôturée`);
  }));
  const nd = $("#newDocBtn");
  if (nd) nd.addEventListener("click", () => openNewDocModal(mod));

  const nr = $("#newRiskBtn");
  if (nr) nr.addEventListener("click", () => openRiskModal(null));
  document.querySelectorAll("[data-editrisk]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); openRiskModal(b.dataset.editrisk); }));
  if (canEdit()) document.querySelectorAll("tr[data-risk]").forEach(tr => tr.addEventListener("click", () => openRiskModal(tr.dataset.risk)));

  const ps = $("#persSearch");
  if (ps) ps.addEventListener("input", () => {
    const q = ps.value.toLowerCase();
    $("#persGrid").innerHTML = persCards(DB.personnel.filter(p => p.nom.toLowerCase().includes(q) || p.fonction.toLowerCase().includes(q)));
    bindView(mod);
  });

  const ds = $("#docSearch"), df = $("#docStatusFilter");
  if (ds) {
    const apply = () => {
      const q = ds.value.toLowerCase(), st = df.value;
      const docs = DB.documents.filter(d => d.module === mod &&
        (!st || d.statut === st) &&
        (!q || [d.num, d.titre, d.auteur, d.date, d.revision].some(f => String(f).toLowerCase().includes(q))));
      $("#docRows").innerHTML = docRows(docs);
      $("#docRows").querySelectorAll("[data-open]").forEach(b => b.addEventListener("click", e => { e.stopPropagation(); openDocModal(b.dataset.open); }));
      $("#docRows").querySelectorAll("tr[data-doc]").forEach(tr => tr.addEventListener("click", () => openDocModal(tr.dataset.doc)));
    };
    ds.addEventListener("input", apply);
    df.addEventListener("change", apply);
  }

  const ea = $("#exportAllBtn");
  if (ea) ea.addEventListener("click", () => exportModule("all"));
}

/* ---------------- Notifications drawer ---------------- */
function renderDrawer() {
  const notifs = computeNotifications();
  $("#drawerBody").innerHTML = notifs.map(n => `
    <div class="notif"><span class="dot" style="background:var(--${n.level === "crit" ? "red" : n.level === "warn" ? "orange" : "royal"})"></span>
    <div>${esc(n.texte)}<small>${fmtDate(n.date)}</small></div></div>`).join("") || `<div class="empty">Aucune notification.</div>`;
}

/* ---------------- Initialisation ---------------- */
async function init() {
  loadDB();

  // Connexion à la base en ligne (si configurée dans config.js)
  initCloud().then(() => { if (SESSION) renderShell(); });

  // Thème
  const savedTheme = localStorage.getItem("raqdms_theme");
  if (savedTheme) document.documentElement.dataset.theme = savedTheme;

  $("#loginLogo").innerHTML = LOGO(58, false);

  // Session persistée
  const savedSess = sessionStorage.getItem("raqdms_session");
  if (savedSess) { SESSION = JSON.parse(savedSess); renderShell(); }

  $("#loginForm").addEventListener("submit", e => {
    e.preventDefault();
    const u = $("#loginUser").value.trim().toLowerCase(), p = $("#loginPass").value;
    const user = DB.users.find(x => x.username === u && x.pass === p);
    if (!user) {
      $("#loginError").style.display = "block";
      logAction(`Tentative de connexion échouée (${u})`);
      return;
    }
    SESSION = { username: user.username, name: user.name, role: user.role, dept: user.dept };
    sessionStorage.setItem("raqdms_session", JSON.stringify(SESSION));
    logAction("Connexion réussie");
    $("#loginError").style.display = "none";
    renderShell();
    toast(`Bienvenue, ${user.name}`);
  });

  $("#forgotLink").addEventListener("click", e => {
    e.preventDefault();
    alert("Contactez l'Administrateur ou le Responsable Qualité pour réinitialiser votre mot de passe.\n(En production : lien de réinitialisation par e-mail via Supabase Auth.)");
  });

  $("#logoutBtn").addEventListener("click", () => {
    logAction("Déconnexion");
    SESSION = null; sessionStorage.removeItem("raqdms_session");
    $("#app").style.display = "none"; $("#loginPage").style.display = "flex";
    $("#loginUser").value = ""; $("#loginPass").value = "";
  });

  $("#themeBtn").addEventListener("click", () => {
    const cur = document.documentElement.dataset.theme === "dark" ? "" : "dark";
    document.documentElement.dataset.theme = cur;
    localStorage.setItem("raqdms_theme", cur);
    $("#themeBtn").innerHTML = cur === "dark" ? I("sun") : I("moon");
  });

  $("#notifBtn").addEventListener("click", () => { renderDrawer(); $("#drawer").classList.toggle("open"); });
  $("#drawerClose").addEventListener("click", () => $("#drawer").classList.remove("open"));
  $("#modalBack").addEventListener("click", e => { if (e.target === $("#modalBack")) closeModal(); });
  $("#menuBtn").addEventListener("click", () => $("#sidebar").classList.toggle("open"));

  // Recherche globale
  const gs = $("#globalSearch"), sr = $("#searchResults");
  gs.addEventListener("input", () => {
    const res = globalSearch(gs.value);
    if (!res.length) { sr.classList.remove("open"); return; }
    sr.innerHTML = res.map((r, i) => `<div class="sr-item" data-sri="${i}"><div class="sr-type">${esc(r.type)}</div>${esc(r.label)}</div>`).join("");
    sr.classList.add("open");
    sr.querySelectorAll(".sr-item").forEach(el => el.addEventListener("click", () => { res[+el.dataset.sri].go(); sr.classList.remove("open"); gs.value = ""; }));
  });
  document.addEventListener("click", e => { if (!e.target.closest(".search-wrap")) sr.classList.remove("open"); });
  document.addEventListener("keydown", e => { if (e.key === "Escape") { closeModal(); $("#drawer").classList.remove("open"); } });
}

document.addEventListener("DOMContentLoaded", init);
