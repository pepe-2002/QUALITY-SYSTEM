/* ══════════════════════════════════════════════════════════════════════
   « Nous » — messagerie privée (couple + famille)
   ──────────────────────────────────────────────────────────────────────
   Trois idées, et rien d'autre :

   1. C'EST PRIVÉ POUR DE VRAI. Le code du salon ne quitte jamais le
      téléphone. Il sert à (a) calculer l'identifiant du salon — une
      empreinte SHA-256 — et (b) fabriquer la clé AES-GCM qui chiffre
      chaque message avant l'envoi. Le serveur ne garde que des blocs
      illisibles.

   2. ÇA MARCHE MÊME SANS RÉSEAU. Tout est écrit d'abord dans le
      téléphone (IndexedDB). Ce qui n'est pas parti attend son tour et
      part à la prochaine occasion. Sans la base en ligne, l'app
      fonctionne quand même — seule sur l'appareil.

   3. ÇA RATTRAPE LE MANQUE DE TEMPS. Messages écrits à l'avance et
      livrés plus tard, mode « je suis occupé », idées d'activités à
      proposer en deux tapes, rappels, et un compteur des jours depuis
      les dernières nouvelles de chaque proche.

   Aucun inline onclick : la page interdit les scripts en ligne (CSP).
   Tout passe par la délégation d'événements en bas de ce fichier.
   ══════════════════════════════════════════════════════════════════════ */

(function(){
"use strict";

const CFG = window.NOUS_CONFIG || {};
const $ = id => document.getElementById(id);
const enc = new TextEncoder();
const dec = new TextDecoder();

/* ───────────────────────── État courant ───────────────────────── */
let SALON = null;        // {sid, code, nom, moi, cree}
let CLE   = null;        // CryptoKey du salon actif
let MSGS  = [];          // messages déchiffrés du salon actif
let NUAGE = true;        // false → mode local (base en ligne absente)
let VUE   = "fil";
let DEV   = "";          // identifiant de cet appareil (pour savoir qui parle)
let SYNC_T = null, DERNIER_RATTRAPAGE = 0, DERNIER_ETAT = 0, EN_SYNC = false;
let IDEE_COURANTE = null, IDEE_CAT = "5 minutes";
let PIN_SAISIE = "", PIN_ETAPE = "ouvrir", PIN_TEMP = "";

/* ═══════════════════ 1. PETITS OUTILS ═══════════════════ */

function esc(s){
  return String(s == null ? "" : s)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
    .replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}
function toast(t, ms){
  const e = $("toast"); e.textContent = t; e.classList.remove("cache");
  clearTimeout(toast._t); toast._t = setTimeout(()=>e.classList.add("cache"), ms || 2600);
}
function ls(k, v){
  try{
    if(v === undefined) return localStorage.getItem(k);
    if(v === null){ localStorage.removeItem(k); return null; }
    localStorage.setItem(k, v); return v;
  }catch(e){ return null; }
}
function lsj(k, v){
  if(v === undefined){ try{ return JSON.parse(ls(k) || "null"); }catch(e){ return null; } }
  ls(k, JSON.stringify(v)); return v;
}
function hm(d){ return new Date(d).toLocaleTimeString("fr-FR",{hour:"2-digit",minute:"2-digit"}); }
function jourTexte(d){
  const a = new Date(d), b = new Date(), h = new Date(Date.now()-864e5);
  if(a.toDateString() === b.toDateString()) return "Aujourd'hui";
  if(a.toDateString() === h.toDateString()) return "Hier";
  return a.toLocaleDateString("fr-FR",{weekday:"long",day:"numeric",month:"long"});
}
function quandTexte(iso){
  const d = new Date(iso);
  return d.toLocaleDateString("fr-FR",{weekday:"long",day:"numeric",month:"long"}) + " à " + hm(d);
}
function joursEntre(a, b){
  return Math.floor((new Date(b).setHours(0,0,0,0) - new Date(a).setHours(0,0,0,0)) / 864e5);
}
function uid(){
  const t = new Uint8Array(9); crypto.getRandomValues(t);
  return Array.from(t).map(x=>x.toString(36)).join("").slice(0,12);
}
/* Un message tout en emojis s'affiche en grand, sans bulle (comme partout). */
function toutEmoji(s){
  const t = (s||"").trim();
  if(!t || t.length > 8) return false;
  return !/[0-9a-zA-Zà-üÀ-Ü.,;:!?'"()\/\\-]/.test(t);
}

/* ═══════════════════ 2. CHIFFREMENT ═══════════════════ */

function hex(buf){
  return Array.from(new Uint8Array(buf)).map(x=>x.toString(16).padStart(2,"0")).join("");
}
async function sha256hex(txt){
  return hex(await crypto.subtle.digest("SHA-256", enc.encode(txt)));
}
/* base64 par morceaux : une photo dépasse la taille d'appel de String.fromCharCode */
function b64(buf){
  const o = new Uint8Array(buf); let s = "";
  for(let i=0;i<o.length;i+=0x8000) s += String.fromCharCode.apply(null, o.subarray(i, i+0x8000));
  return btoa(s);
}
function deb64(t){
  const b = atob(t), o = new Uint8Array(b.length);
  for(let i=0;i<b.length;i++) o[i] = b.charCodeAt(i);
  return o;
}
/* Du code du salon on tire : l'identifiant public (empreinte) et la clé secrète. */
async function ouvrirCoffre(code){
  const sid = await sha256hex("nous-salon-v1|" + code);
  const base = await crypto.subtle.importKey("raw", enc.encode(code), "PBKDF2", false, ["deriveKey"]);
  const cle = await crypto.subtle.deriveKey(
    { name:"PBKDF2", salt: enc.encode("nous-cle-v1|" + sid), iterations:120000, hash:"SHA-256" },
    base, { name:"AES-GCM", length:256 }, false, ["encrypt","decrypt"]);
  return { sid, cle };
}
async function chiffrer(objOuTexte, cle){
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const clair = enc.encode(typeof objOuTexte === "string" ? objOuTexte : JSON.stringify(objOuTexte));
  const ct = await crypto.subtle.encrypt({name:"AES-GCM", iv}, cle || CLE, clair);
  return b64(iv) + "." + b64(ct);
}
async function dechiffrer(txt, cle){
  const p = String(txt||"").split(".");
  if(p.length !== 2) throw new Error("format");
  const clair = await crypto.subtle.decrypt(
    {name:"AES-GCM", iv: deb64(p[0])}, cle || CLE, deb64(p[1]));
  return dec.decode(clair);
}
async function dechiffrerObj(txt, cle){ return JSON.parse(await dechiffrer(txt, cle)); }

/* Code de salon lisible : nous-XXXX-XXXX-XXXX (alphabet sans O/0/I/1). */
function nouveauCode(){
  const A = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
  const t = new Uint32Array(12); crypto.getRandomValues(t);
  const s = Array.from(t).map(x => A[x % A.length]).join("");
  return "nous-" + s.slice(0,4) + "-" + s.slice(4,8) + "-" + s.slice(8,12);
}
/* Toujours ramener un code tapé à la main, collé, ou reçu dans un lien à
   la MÊME forme — sinon la clé dérivée serait différente et le salon
   resterait illisible. Renvoie "" si ce n'est pas un code valable. */
function normCode(v){
  v = String(v||"").trim();
  const m = v.match(/[#?&]c=([^&\s]+)/);          // on accepte le lien complet
  if(m){ try{ v = decodeURIComponent(m[1]); }catch(e){ v = m[1]; } }
  v = v.replace(/^\s*nous[\s_-]*/i, "").toUpperCase().replace(/[^A-Z0-9]/g, "");
  if(v.length !== 12) return "";
  return "nous-" + v.slice(0,4) + "-" + v.slice(4,8) + "-" + v.slice(8,12);
}

/* ═══════════════════ 3. BASE LOCALE (IndexedDB) ═══════════════════ */

let DB = null;
function dbOuvrir(){
  return new Promise((ok, ko)=>{
    const q = indexedDB.open("nous", 1);
    q.onupgradeneeded = e => {
      const d = e.target.result;
      if(!d.objectStoreNames.contains("msg")){
        const s = d.createObjectStore("msg", { keyPath:"k" });
        s.createIndex("sid", "sid", { unique:false });
      }
    };
    q.onsuccess = e => ok(e.target.result);
    q.onerror   = () => ko(q.error);
  });
}
function dbTx(mode){ return DB.transaction("msg", mode).objectStore("msg"); }
function dbPut(rec){
  return new Promise((ok,ko)=>{ const r = dbTx("readwrite").put(rec); r.onsuccess=()=>ok(rec); r.onerror=()=>ko(r.error); });
}
function dbDel(k){
  return new Promise(ok=>{ const r = dbTx("readwrite").delete(k); r.onsuccess=()=>ok(); r.onerror=()=>ok(); });
}
function dbListe(sid){
  return new Promise(ok=>{
    const out = [], r = dbTx("readonly").index("sid").openCursor(IDBKeyRange.only(sid));
    r.onsuccess = e => { const c = e.target.result; if(c){ out.push(c.value); c.continue(); } else ok(out); };
    r.onerror = () => ok(out);
  });
}

/* ═══════════════════ 4. LE NUAGE (Supabase, sans bibliothèque) ═══════════════════ */

async function rpc(nom, args){
  if(!CFG.SUPABASE_URL || !CFG.SUPABASE_KEY) throw Object.assign(new Error("pas de base"), {local:true});
  const r = await fetch(CFG.SUPABASE_URL + "/rest/v1/rpc/" + nom, {
    method:"POST",
    headers:{ apikey: CFG.SUPABASE_KEY, Authorization:"Bearer " + CFG.SUPABASE_KEY,
              "Content-Type":"application/json" },
    body: JSON.stringify(args)
  });
  if(!r.ok){
    const t = await r.text().catch(()=>"");
    const e = new Error(t || ("HTTP " + r.status));
    e.http = r.status;
    /* 404 = les fonctions SQL n'ont pas été installées → on bascule en local */
    if(r.status === 404 || /schema cache|does not exist/i.test(t)) e.local = true;
    throw e;
  }
  return r.json();
}
function passerEnLocal(pourquoi){
  if(!NUAGE) return;
  NUAGE = false;
  majBandeau(); majStatut();
  console.warn("Nous : mode local —", pourquoi);
}

/* ═══════════════════ 5. SALONS ═══════════════════ */

function salons(){ return lsj("nous_salons") || []; }
function salonsSet(l){ lsj("nous_salons", l); }

async function activerSalon(sid){
  const s = salons().find(x => x.sid === sid);
  if(!s) return false;
  const coffre = await ouvrirCoffre(s.code);
  SALON = s; CLE = coffre.cle;
  ls("nous_actif", sid);
  MSGS = (await dbListe(sid)).sort(triMsg);
  /* mon « je suis occupé » survit au redémarrage, même sans réseau */
  ETATS = {};
  const st = lsj("nous_statut_" + sid);
  if(st && st.jusqua) ETATS["st:" + DEV] = st;
  $("t-nom").textContent = s.nom;
  rendreFil(); rendreNous(); rendreTemps(); rendreFamille(); majStatut();
  sync(true);
  return true;
}
function triMsg(a, b){
  const x = new Date(a.vis).getTime(), y = new Date(b.vis).getTime();
  if(x !== y) return x - y;
  return (a.id || 9e15) - (b.id || 9e15);
}
async function creerSalon(nom, moi, codeDonne){
  const code = codeDonne ? normCode(codeDonne) : nouveauCode();
  if(!code) return null;
  const coffre = await ouvrirCoffre(code);
  const l = salons();
  if(l.some(x => x.sid === coffre.sid)){ await activerSalon(coffre.sid); return coffre.sid; }
  l.push({ sid: coffre.sid, code, nom: nom || "Nous deux", moi: moi || "Moi", cree: new Date().toISOString() });
  salonsSet(l);
  await activerSalon(coffre.sid);
  return coffre.sid;
}

/* ═══════════════════ 6. ENVOI / RÉCEPTION ═══════════════════ */

/* Un message local. `p` = charge utile chiffrée, `media` = photo/vocal. */
function neuf(p, media, quandISO){
  const lid = uid();
  return {
    k: SALON.sid + ":L" + lid, sid: SALON.sid, lid, id: 0,
    t: p.t, a: p.a, b: p.b || "", d: p.d || 0, quand: p.quand || "", ref: p.ref || 0,
    rep: p.rep || "", cat: p.cat || "", dev: p.dev,
    m: media || "", moi: true, etat: "att",
    prog: !!(quandISO && new Date(quandISO) > new Date()),
    vis: quandISO || new Date().toISOString(), cree: new Date().toISOString()
  };
}
async function envoyer(p, media, quandISO){
  if(!SALON) return;
  p.a = SALON.moi; p.dev = DEV;
  const rec = neuf(p, media, quandISO);
  await dbPut(rec);
  /* Les messages programmés vivent dans la même liste : c'est le filtre
     d'affichage (visibleMaintenant) qui les tient hors du fil jusqu'à l'heure. */
  MSGS.push(rec); MSGS.sort(triMsg);
  if(!rec.prog) rendreFil();
  else { rendreTemps(); toast("Message programmé pour " + quandTexte(rec.vis)); }
  pousser(rec);
  return rec;
}
async function pousser(rec){
  if(rec.id) return;
  if(!NUAGE){                       // pas de base en ligne : le message est « à sa place »
    if(rec.etat !== "ok"){ rec.etat = "ok"; await dbPut(rec); rendreFil(); }
    return;
  }
  try{
    const corps = await chiffrer({ t:rec.t, a:rec.a, b:rec.b, d:rec.d, quand:rec.quand,
                                   ref:rec.ref, rep:rec.rep, cat:rec.cat, dev:rec.dev, lid:rec.lid });
    const media = rec.m ? await chiffrer(rec.m) : null;
    const id = await rpc("nous_envoyer", {
      p_salon: SALON.sid, p_corps: corps, p_media: media,
      p_visible_le: rec.prog ? rec.vis : null });
    await dbDel(rec.k);
    rec.id = Number(id); rec.k = SALON.sid + ":" + rec.id; rec.etat = "ok";
    await dbPut(rec);
    rendreFil(); if(rec.prog) rendreTemps();
  }catch(e){
    if(e.local){ passerEnLocal(e.message); rec.etat = "ok"; await dbPut(rec); rendreFil(); return; }
    rec.etat = "att"; await dbPut(rec);
    console.warn("envoi différé :", e.message);
  }
}
/* Ce qui n'est pas parti repart dès qu'on a du réseau. */
async function viderFile(){
  const attente = (await dbListe(SALON.sid)).filter(r => !r.id && r.etat === "att");
  for(const r of attente){ await pousser(r); }
}

async function integrer(lignes){
  let neufs = 0;
  for(const l of lignes){
    const k = SALON.sid + ":" + l.id;
    if(MSGS.some(m => m.id === Number(l.id))) continue;
    let rec;
    if(l.corps === "."){                              // effacé pour tout le monde
      rec = { k, sid: SALON.sid, id: Number(l.id), t:"suppr", a:"", b:"", m:"", moi:false,
              etat:"ok", vis: l.visible_le, cree: l.cree_le };
    }else{
      let p;
      try{ p = await dechiffrerObj(l.corps); }
      catch(e){ continue; }                            // pas notre clé → on ignore
      let media = "";
      if(l.media){ try{ media = await dechiffrer(l.media); }catch(e){} }
      rec = { k, sid: SALON.sid, id: Number(l.id), t: p.t, a: p.a || "", b: p.b || "",
              d: p.d || 0, quand: p.quand || "", ref: p.ref || 0, rep: p.rep || "",
              cat: p.cat || "", dev: p.dev || "", lid: p.lid || "", m: media,
              moi: p.dev === DEV, etat:"ok", vis: l.visible_le, cree: l.cree_le };
    }
    /* Le même message revenu du serveur : on jette la copie locale provisoire.
       On le reconnaît à son identifiant local (lid), glissé dans le bloc chiffré. */
    if(rec.lid){
      const jumeau = MSGS.findIndex(m => !m.id && m.lid === rec.lid);
      if(jumeau >= 0){ await dbDel(MSGS[jumeau].k); MSGS.splice(jumeau, 1); }
    }
    await dbPut(rec);
    MSGS.push(rec);
    if(!rec.moi && rec.t === "sys") ETAT_A_RELIRE = true;
    if(!rec.moi && rec.t !== "suppr") neufs++;
  }
  if(lignes.length){ MSGS.sort(triMsg); }
  return neufs;
}

function dernierId(){
  let m = 0; for(const x of MSGS) if(x.id > m) m = x.id; return m;
}

async function sync(force){
  if(!SALON || EN_SYNC) return;
  EN_SYNC = true;
  try{
    let bougé = false;
    if(NUAGE){
      await viderFile();
      const l = await rpc("nous_lire", { p_salon: SALON.sid, p_depuis: dernierId(), p_limite: 100 });
      const n = await integrer(l || []);
      if(n){ bougé = true; prevenir(n); }
      else if((l||[]).length) bougé = true;

      /* Le statut « je suis occupé » : relu régulièrement, et tout de suite
         quand un message de service vient d'arriver (c'est justement lui). */
      if(force || ETAT_A_RELIRE || Date.now() - DERNIER_ETAT > 20000){
        ETAT_A_RELIRE = false; DERNIER_ETAT = Date.now();
        await lireEtat();
      }

      /* 2. rattrapage (toutes les 60 s) : messages programmés devenus visibles
            « derrière » des messages plus récents, et messages effacés. */
      if(force || Date.now() - DERNIER_RATTRAPAGE > 60000){
        DERNIER_RATTRAPAGE = Date.now();
        const ids = await rpc("nous_ids", { p_salon: SALON.sid, p_limite: 400 });
        const connus = new Set(MSGS.filter(m=>m.id).map(m => m.id));
        const manquants = (ids||[]).filter(x => !connus.has(Number(x.id)) && !x.vide)
                                   .map(x => Number(x.id)).slice(0, 60);
        if(manquants.length){
          const rows = await rpc("nous_par_ids", { p_salon: SALON.sid, p_ids: manquants });
          const n2 = await integrer(rows || []);
          if(n2) prevenir(n2);
          bougé = true;
        }
        /* effacés côté serveur : le contenu est parti, la ligne reste marquée */
        for(const x of (ids||[])){
          if(!x.vide) continue;
          const m = MSGS.find(y => y.id === Number(x.id));
          if(m && m.t !== "suppr"){ m.t = "suppr"; m.b = ""; m.m = ""; await dbPut(m); bougé = true; }
        }
      }
    }
    if(bougé || force){ rendreFil(); rendreNous(); rendreTemps(); }
    majBandeau();
  }catch(e){
    if(e.local) passerEnLocal(e.message);
  }finally{ EN_SYNC = false; }
}

function prevenir(n){
  try{
    if(document.visibilityState === "visible" || Notification.permission !== "granted") {
      if(VUE !== "fil") $("pt-fil").classList.add("on");
      return;
    }
    new Notification(SALON.nom, { body: n > 1 ? n + " nouveaux messages" : "Un nouveau message vous attend",
                                  icon:"icon-192.png", tag:"nous" });
  }catch(e){}
  if(VUE !== "fil") $("pt-fil").classList.add("on");
}

/* ═══════════════════ 7. ÉTAT PARTAGÉ (« je suis occupé ») ═══════════════════ */

let ETATS = {};            // { cleAppareil: {qui, jusqua, quoi, maj} }
let ETAT_A_RELIRE = false; // un message de service vient d'arriver → relire le statut

async function ecrireStatut(jusqua, quoi){
  const v = { qui: SALON.moi, dev: DEV, jusqua: jusqua || "", quoi: quoi || "" };
  ETATS["st:" + DEV] = Object.assign({}, v, { maj: new Date().toISOString() });
  lsj("nous_statut_" + SALON.sid, v);
  majStatut();
  if(!NUAGE) return;
  try{ await rpc("nous_etat_ecrire", { p_salon: SALON.sid, p_cle: "st:" + DEV, p_valeur: await chiffrer(v) }); }
  catch(e){ if(e.local) passerEnLocal(e.message); }
}
async function lireEtat(){
  if(!NUAGE) return;
  try{
    const l = await rpc("nous_etat_lire", { p_salon: SALON.sid });
    const out = {};
    for(const r of (l||[])){
      try{ out[r.cle] = Object.assign(await dechiffrerObj(r.valeur), { maj: r.maj }); }catch(e){}
    }
    ETATS = out; majStatut();
  }catch(e){ if(e.local) passerEnLocal(e.message); }
}
/* Qui est occupé, en ce moment ? (le mien / celui de l'autre) */
function statutsActifs(){
  const now = Date.now();
  let autre = null, mien = null;
  for(const k in ETATS){
    const e = ETATS[k];
    if(!e || !e.jusqua || new Date(e.jusqua).getTime() < now) continue;
    if(e.dev === DEV) mien = e; else autre = e;
  }
  return { mien, autre };
}
/* En-tête : le statut de l'AUTRE s'il est encore valable, sinon le mien. */
function majStatut(){
  const el = $("t-statut"); if(!el || !SALON) return;
  const { mien, autre } = statutsActifs();
  el.classList.remove("occ");
  if(autre){ el.textContent = (autre.qui || "Elle/il") + " est pris jusqu'à " + hm(autre.jusqua); el.classList.add("occ"); }
  else if(mien){ el.textContent = "Vous êtes en mode occupé jusqu'à " + hm(mien.jusqua); el.classList.add("occ"); }
  else el.textContent = NUAGE ? "chiffré de bout en bout" : "sur ce téléphone seulement";
  const st = $("occ-etat");
  if(st) st.textContent = mien ? ("Actif jusqu'à " + hm(mien.jusqua) + " — touchez « Je suis libre » pour arrêter.") : "";
}
function majBandeau(){
  const b = $("fil-prog");
  const att = MSGS.filter(m => !m.id && m.etat === "att" && !m.prog).length;
  if(!NUAGE){ b.textContent = "Mode local : ce salon vit sur ce téléphone (voir SQL-nous.sql)."; b.classList.remove("cache"); }
  else if(att){ b.textContent = att + " message(s) en attente de réseau…"; b.classList.remove("cache"); }
  else b.classList.add("cache");
}

/* ═══════════════════ 8. AFFICHAGE DU FIL ═══════════════════ */

function visibleMaintenant(m){
  return new Date(m.vis).getTime() <= Date.now();
}
function rendreFil(){
  const f = $("fil"); if(!f) return;
  const l = MSGS.filter(visibleMaintenant);
  if(!l.length){
    f.innerHTML = '<div class="vide-fil"><span>❤</span>Rien encore ici.<br>'
      + 'Écrivez un mot — même trois mots comptent.<br><br>'
      + '<small>Pas le temps maintenant ? Le « ＋ » permet d\'écrire un message '
      + 'qui partira ce soir ou demain.</small></div>';
    return;
  }
  let h = "", jour = "";
  for(const m of l){
    const j = jourTexte(m.vis);
    if(j !== jour){ jour = j; h += '<div class="jour">' + esc(j) + '</div>'; }
    h += bulle(m);
  }
  const colle = f.scrollHeight - f.scrollTop - f.clientHeight < 120;
  f.innerHTML = h;
  if(colle || !rendreFil._deja) f.scrollTop = f.scrollHeight;
  rendreFil._deja = true;
  majBandeau();
}
function bulle(m){
  if(m.t === "suppr")
    return '<div class="b sys">Ce message a été effacé.</div>';
  if(m.t === "sys")
    return '<div class="b sys">' + esc(m.b) + '</div>';

  const cls = "b" + (m.moi ? " moi" : "") + (m.t === "texte" && toutEmoji(m.b) ? " gros" : "");
  let inner = "";
  if(!m.moi && m.a) inner += '<div class="qui">' + esc(m.a) + "</div>";

  if(m.t === "photo" && m.m)
    inner += '<img src="' + esc(m.m) + '" alt="photo" loading="lazy">';
  if(m.t === "vocal" && m.m)
    inner += '<audio controls preload="none" src="' + esc(m.m) + '"></audio>'
           + '<div class="h">🎤 ' + Math.round(m.d||0) + ' s</div>';
  if(m.t === "ping")
    inner += "📞 " + esc(m.b || "Appelle-moi quand tu peux.");
  if(m.t === "idee") inner += carteIdee(m);
  if(m.t === "rep")
    inner += (m.rep === "oui" ? "✅ " : "🕊️ ") + esc(m.b);
  if(m.b && ["texte","photo","vocal"].indexOf(m.t) >= 0 && m.t !== "vocal")
    inner += (m.t === "photo" ? '<div style="margin-top:4px">' : "") + esc(m.b) + (m.t === "photo" ? "</div>" : "");

  const etat = m.moi ? ((m.id || m.etat === "ok") ? '<span class="ok">✓</span>' : '<span class="att">⏳</span>') : "";
  inner += '<div class="h">' + hm(m.vis) + " " + etat + "</div>";
  return '<div class="' + cls + '" data-act="msg" data-arg="' + esc(m.k) + '">' + inner + "</div>";
}
function carteIdee(m){
  const rep = MSGS.filter(x => x.t === "rep" && Number(x.ref) === Number(m.id) && m.id);
  const oui = rep.some(x => x.rep === "oui");
  const non = rep.some(x => x.rep === "non");
  let h = '<div class="carte-idee"><b>💡 Une idée pour nous</b>' + esc(m.b);
  if(m.quand) h += '<div class="quand">📅 ' + esc(quandTexte(m.quand)) + "</div>";
  if(oui) h += '<div class="fait">✅ C\'est un rendez-vous !</div>';
  else if(non) h += '<div class="quand">🕊️ Pas cette fois — on retente.</div>';
  else if(!m.moi && m.id)
    h += '<div class="rep"><button data-act="rep-oui" data-arg="' + m.id + '">Oui, on le fait</button>'
       + '<button class="non" data-act="rep-non" data-arg="' + m.id + '">Une autre fois</button></div>';
  else if(m.moi) h += '<div class="quand">En attente de sa réponse…</div>';
  return h + "</div>";
}

/* ═══════════════════ 9. ENVOIS (texte, photo, vocal, idée…) ═══════════════════ */

async function envoyerTexte(){
  const i = $("saisie"), v = i.value.trim();
  if(!v) return;
  i.value = "";
  await envoyer({ t:"texte", b:v });
}

/* ── Photo : on la réduit avant l'envoi (réseaux lents) ── */
function reduirePhoto(file){
  return new Promise((ok, ko)=>{
    const fr = new FileReader();
    fr.onload = () => {
      const img = new Image();
      img.onload = () => {
        const MAX = CFG.PHOTO_PX || 1280;
        let { width:w, height:h } = img;
        if(w > MAX || h > MAX){ const r = Math.min(MAX/w, MAX/h); w = Math.round(w*r); h = Math.round(h*r); }
        const c = document.createElement("canvas"); c.width = w; c.height = h;
        c.getContext("2d").drawImage(img, 0, 0, w, h);
        ok(c.toDataURL("image/jpeg", CFG.PHOTO_Q || 0.72));
      };
      img.onerror = ko; img.src = fr.result;
    };
    fr.onerror = ko; fr.readAsDataURL(file);
  });
}
async function choisirPhoto(e){
  const f = e.target.files && e.target.files[0];
  e.target.value = "";
  if(!f) return;
  toast("Préparation de la photo…");
  try{
    const data = await reduirePhoto(f);
    if(data.length > 2600000){ toast("Photo trop lourde, réessayez avec une plus petite."); return; }
    modale('<h3>Envoyer cette photo</h3>'
      + '<img src="' + esc(data) + '" style="width:100%;border-radius:12px;margin:6px 0 12px">'
      + '<input id="ph-mot" maxlength="200" placeholder="Un mot avec la photo (facultatif)">'
      + '<button class="btn" data-act="photo-ok">Envoyer</button>'
      + '<button class="btn plat" data-act="fermer">Annuler</button>');
    modale._photo = data;
  }catch(err){ toast("Impossible de lire cette photo."); }
}

/* ── Vocal ── */
let REC = null, RECCHUNKS = [], RECT0 = 0, RECTIMER = null;
async function vocalDebut(){
  if(!navigator.mediaDevices || !window.MediaRecorder){ toast("Le micro n'est pas disponible ici."); return; }
  try{
    const flux = await navigator.mediaDevices.getUserMedia({ audio:true });
    REC = new MediaRecorder(flux); RECCHUNKS = []; RECT0 = Date.now();
    REC.ondataavailable = e => { if(e.data && e.data.size) RECCHUNKS.push(e.data); };
    REC.onstop = () => { flux.getTracks().forEach(t => t.stop()); };
    REC.start();
    $("vocal-box").classList.remove("cache");
    $("feuille-plus").classList.add("cache");
    RECTIMER = setInterval(()=>{
      const s = Math.floor((Date.now()-RECT0)/1000);
      $("vocal-t").textContent = Math.floor(s/60) + ":" + String(s%60).padStart(2,"0");
      if(s >= (CFG.VOCAL_MAX_S || 120)) vocalFin(true);
    }, 250);
  }catch(e){ toast("Micro refusé. Autorisez le micro pour envoyer un vocal."); }
}
function vocalFin(envoyerLe){
  if(!REC) return;
  clearInterval(RECTIMER);
  const duree = (Date.now()-RECT0)/1000;
  const r = REC; REC = null;
  $("vocal-box").classList.add("cache");
  $("vocal-t").textContent = "0:00";
  r.onstop = () => {
    r.stream && r.stream.getTracks && r.stream.getTracks().forEach(t=>t.stop());
    if(!envoyerLe || duree < 0.6) return;
    const blob = new Blob(RECCHUNKS, { type: RECCHUNKS[0] && RECCHUNKS[0].type || "audio/webm" });
    if(blob.size > 2400000){ toast("Vocal trop long pour le réseau — réessayez plus court."); return; }
    const fr = new FileReader();
    fr.onload = () => envoyer({ t:"vocal", d: Math.round(duree) }, fr.result);
    fr.readAsDataURL(blob);
  };
  try{ r.stop(); }catch(e){}
}

/* ═══════════════════ 10. IDÉES D'ACTIVITÉS ═══════════════════ */

const IDEES = {
"5 minutes":[
 "Lui envoyer un vocal de trente secondes, juste pour dire pourquoi tu penses à elle.",
 "Préparer son thé et le lui apporter sans qu'elle demande.",
 "Une photo de ce que tu vois là, maintenant, sans commentaire.",
 "Lui masser les épaules pendant qu'elle raconte sa journée.",
 "Lui dire une chose précise qu'elle a bien faite cette semaine.",
 "Ranger la chose qu'elle allait devoir ranger.",
 "L'appeler juste pour entendre sa voix, sans rien demander.",
 "Écrire un mot sur un papier et le laisser où elle le trouvera.",
 "Lui envoyer la chanson qui vous rappelle un souvenir.",
 "Poser le téléphone pendant qu'elle parle. Rien d'autre.",
 "Lui demander : « De quoi tu as besoin, aujourd'hui ? »",
 "Un selfie à deux, même mal cadré."],
"Une heure":[
 "Marcher jusqu'au bord de mer et regarder le soleil descendre.",
 "Cuisiner ensemble un plat qu'elle aime — toi les épices, elle le reste.",
 "Boire un jus dehors, sans parler d'argent ni de travail.",
 "Regarder vos anciennes photos, l'une après l'autre.",
 "Aller au marché ensemble, sans liste.",
 "Un thé sur la terrasse, les téléphones dans l'autre pièce.",
 "Lui apprendre une chose que tu sais faire.",
 "Lui demander un souvenir d'enfance que tu ne connais pas encore.",
 "Faire ensemble la corvée qu'elle déteste le plus.",
 "Une promenade après la prière du soir.",
 "Une chanson chacun son tour, jusqu'à en avoir dix.",
 "Préparer ensemble le prochain voyage à Mohéli."],
"Une journée":[
 "Une traversée jusqu'à Mohéli, rien que tous les deux.",
 "Une journée à la plage : départ tôt, retour au coucher du soleil.",
 "Aller voir les tortues à Itsamia, la nuit.",
 "Rendre visite à sa famille sans prévenir.",
 "Une journée entière sans téléphone, tous les deux.",
 "Un pique-nique au bord de mer, du riz et du poisson.",
 "Dix photos chacun dans la journée — on compare le soir.",
 "Cuisiner un grand repas et inviter les proches.",
 "Une balade dans un endroit où vous n'êtes jamais allés.",
 "Un jour « oui » : c'est elle qui décide tout, du matin au soir.",
 "Refaire exactement ce que vous avez fait la première fois.",
 "Une journée à ne rien faire ensemble. Vraiment rien."],
"À distance":[
 "Un vocal du matin : ta voix avant sa première tasse.",
 "Photographier vos deux repas et manger « ensemble ».",
 "Dix minutes d'appel vidéo, sans rien de sérieux à régler.",
 "Ta photo du ciel contre la sienne.",
 "Regarder le même film chacun de son côté, à la même heure.",
 "Une question par jour, réponse en vocal.",
 "Lui faire livrer quelque chose qu'elle aime.",
 "Compter les jours ensemble : « plus que… ».",
 "Lui écrire ce que tu feras en premier en la revoyant.",
 "Trois vérités et un mensonge : à elle de trouver.",
 "Envoyer une vieille photo de vous deux, sans un mot.",
 "Fixer une heure d'appel — et la tenir, même dix minutes."],
"Des mots":[
 "« Qu'est-ce qui t'a fatiguée, cette semaine ? »",
 "« De quoi tu rêves, en ce moment, pour toi ? »",
 "« Qu'est-ce que je fais qui te fait du bien sans que je le sache ? »",
 "« Il y a quelque chose que tu gardes pour toi ? »",
 "« Qu'est-ce qui te manque de nos débuts ? »",
 "« Comment tu nous vois dans cinq ans ? »",
 "Dire merci pour une chose précise et ancienne.",
 "« Si on partait demain, tu choisirais quoi ? »",
 "Demander pardon pour une chose jamais dite.",
 "« Qu'est-ce que je peux enlever de ta journée ? »",
 "Raconter ta pire journée de la semaine, pour de vrai.",
 "« Qu'est-ce qui t'a fait rire aujourd'hui ? »"]
};
function toutesIdees(){
  const out = [];
  for(const c in IDEES) for(const t of IDEES[c]) out.push({ cat:c, t });
  return out;
}
/* L'idée du jour est la même toute la journée (elle dépend de la date). */
function ideeDuJour(){
  const l = toutesIdees();
  const d = new Date(), n = d.getFullYear()*372 + d.getMonth()*31 + d.getDate();
  return l[n % l.length];
}
function rendreNous(){
  if(!IDEE_COURANTE) IDEE_COURANTE = ideeDuJour();
  const ij = $("idee-jour");
  if(ij) ij.innerHTML = '<span class="cat">' + esc(IDEE_COURANTE.cat) + "</span>" + esc(IDEE_COURANTE.t);

  /* Rendez-vous acceptés, à venir */
  const rdv = MSGS.filter(m => m.t === "idee" && m.quand && m.id
      && MSGS.some(r => r.t === "rep" && Number(r.ref) === Number(m.id) && r.rep === "oui"))
    .filter(m => new Date(m.quand).getTime() > Date.now() - 6*3600e3)
    .sort((a,b) => new Date(a.quand) - new Date(b.quand));
  const rl = $("rdv-liste");
  rl.innerHTML = rdv.length ? rdv.map(m => {
      const j = joursEntre(new Date(), m.quand);
      const q = j === 0 ? "aujourd'hui" : j === 1 ? "demain" : "dans " + j + " jours";
      return '<div class="ligne"><span><b>' + esc(m.b) + "</b><small>" + esc(quandTexte(m.quand))
        + '</small></span><em class="tag vert">' + esc(q) + "</em></div>";
    }).join("") : '<div class="vide-l">Aucun rendez-vous pris. Proposez une idée — deux tapes.</div>';

  /* Dates à ne pas oublier */
  const dts = (lsj("nous_dates_" + (SALON ? SALON.sid : "")) || [])
    .map(d => Object.assign({}, d, { j: prochainAnniv(d.d) }))
    .sort((a,b) => a.j - b.j);
  $("dates-liste").innerHTML = dts.length ? dts.map((d,i) =>
      '<div class="ligne"><span><b>' + esc(d.n) + "</b><small>" + esc(d.d) + "</small></span>"
      + '<em class="tag' + (d.j <= 7 ? " rouge" : "") + '">'
      + (d.j === 0 ? "c'est aujourd'hui !" : "dans " + d.j + " j") + "</em>"
      + '<button data-act="date-suppr" data-arg="' + i + '" class="tag">✕</button></div>').join("")
    : '<div class="vide-l">Anniversaires, date de mariage, jour de votre rencontre…</div>';

  /* Le catalogue */
  const cats = Object.keys(IDEES);
  $("idee-cats").innerHTML = cats.map(c =>
    '<button class="puce' + (c === IDEE_CAT ? " on" : "") + '" data-act="cat" data-arg="' + esc(c) + '">' + esc(c) + "</button>").join("");
  $("idee-liste").innerHTML = (IDEES[IDEE_CAT] || []).map((t,i) =>
    '<button class="ligne" data-act="idee-choix" data-arg="' + esc(IDEE_CAT) + "|" + i + '">'
    + "<span>" + esc(t) + '</span><em class="tag">proposer</em></button>').join("");
}
function prochainAnniv(jjmm){
  const m = String(jjmm||"").match(/^(\d{1,2})[\/-](\d{1,2})/);
  if(!m) return 999;
  const now = new Date(); now.setHours(0,0,0,0);
  let d = new Date(now.getFullYear(), Number(m[2])-1, Number(m[1]));
  if(d < now) d = new Date(now.getFullYear()+1, Number(m[2])-1, Number(m[1]));
  return joursEntre(now, d);
}

/* ═══════════════════ 11. FAMILLE ═══════════════════ */

function proches(l){ return l === undefined ? (lsj("nous_proches") || []) : lsj("nous_proches", l); }
function rendreFamille(){
  const l = proches();
  let enRetard = 0;
  $("fam-liste").innerHTML = l.length ? l.map((p,i)=>{
    const j = p.dernier ? joursEntre(p.dernier, new Date()) : 999;
    const retard = j >= (p.jours || 7);
    if(retard) enRetard++;
    const txt = !p.dernier ? "jamais noté" : j === 0 ? "aujourd'hui" : j === 1 ? "hier" : "il y a " + j + " jours";
    return '<div class="ligne"><span><b>' + esc(p.n) + "</b><small>" + esc(txt)
      + " · tous les " + (p.jours||7) + " jours</small></span>"
      + (p.tel ? '<button class="tag" data-act="fam-tel" data-arg="' + i + '">📞</button>'
               + '<button class="tag" data-act="fam-wa" data-arg="' + i + '">💬</button>' : "")
      + '<button class="tag ' + (retard ? "rouge" : "vert") + '" data-act="fam-ok" data-arg="' + i + '">✓ noté</button>'
      + '<button class="tag" data-act="fam-suppr" data-arg="' + i + '">✕</button></div>';
  }).join("") : '<div class="vide-l">Ajoutez votre mère, vos frères, vos enfants… '
              + "L'app vous dira qui n'a pas eu de vos nouvelles.</div>";
  $("pt-fam").classList.toggle("on", enRetard > 0);

  const s = salons(), act = SALON && SALON.sid;
  $("fam-salons").innerHTML = s.map(x =>
    '<button class="ligne' + (x.sid === act ? " on" : "") + '" data-act="salon" data-arg="' + esc(x.sid) + '">'
    + "<span><b>" + esc(x.nom) + "</b><small>vous : " + esc(x.moi) + "</small></span>"
    + '<em class="tag">' + (x.sid === act ? "ouvert" : "ouvrir") + "</em></button>").join("");
}

/* ═══════════════════ 12. MON TEMPS ═══════════════════ */

const OCCUPES = [
  { l:"1 heure",     h:1 }, { l:"2 heures", h:2 }, { l:"jusqu'à ce soir", soir:true },
  { l:"toute la journée", jour:true }, { l:"Je suis libre", stop:true }
];
function rendreTemps(){
  const mien = statutsActifs().mien;
  $("occ-choix").innerHTML = OCCUPES.map((o,i) => {
    const actif = mien ? (mien.quoi === o.l) : !!o.stop;
    return '<button class="puce' + (actif ? " on" : "") + '" data-act="occ" data-arg="' + i + '">' + esc(o.l) + "</button>";
  }).join("");

  const prog = MSGS.filter(m => m.prog && new Date(m.vis) > new Date())
                   .sort((a,b)=> new Date(a.vis) - new Date(b.vis));
  $("prog-liste").innerHTML = prog.length ? prog.map(m =>
      '<div class="ligne"><span><b>' + esc((m.b||"").slice(0,60)) + "</b><small>partira " + esc(quandTexte(m.vis))
      + "</small></span>" + (m.id ? "" : '<em class="tag">hors ligne</em>')
      + '<button class="tag rouge" data-act="prog-annul" data-arg="' + esc(m.k) + '">annuler</button></div>').join("")
    : '<div class="vide-l">Rien en attente. Écrivez trois mots pour demain matin, '
    + "ils arriveront pendant que vous travaillez.</div>";

  const raps = lsj("nous_rappels") || [];
  $("rap-liste").innerHTML = raps.length ? raps.map((r,i) =>
      '<div class="ligne"><span><b>' + esc(r.t) + "</b><small>tous les jours à " + esc(r.h) + "</small></span>"
      + '<button class="tag rouge" data-act="rap-suppr" data-arg="' + i + '">✕</button></div>').join("")
    : '<div class="vide-l">Par exemple : 12 h 30 « un mot pour elle », 21 h « bonne nuit ».</div>';

  $("rg-etat").textContent = NUAGE
    ? "Synchronisé et chiffré · " + (MSGS.length) + " messages sur ce téléphone."
    : "Mode local : la base en ligne n'est pas installée (SQL-nous.sql). Les messages restent sur ce téléphone.";
}
function finDeJournee(h){
  const d = new Date(); d.setHours(h, 0, 0, 0);
  if(d <= new Date()) d.setDate(d.getDate()+1);
  return d;
}

/* ── Rappels locaux : vérifiés tant que l'app est ouverte ── */
function verifierRappels(){
  const raps = lsj("nous_rappels") || [];
  if(!raps.length) return;
  const now = new Date(), cle = now.toISOString().slice(0,10);
  let chg = false;
  for(const r of raps){
    const [H,M] = String(r.h||"12:00").split(":").map(Number);
    const t = new Date(now); t.setHours(H||0, M||0, 0, 0);
    if(now >= t && r.vu !== cle){
      r.vu = cle; chg = true;
      try{
        if(Notification.permission === "granted")
          new Notification("Nous", { body:r.t, icon:"icon-192.png", tag:"rap"+r.h });
        else toast("⏰ " + r.t, 5000);
      }catch(e){ toast("⏰ " + r.t, 5000); }
    }
  }
  if(chg) lsj("nous_rappels", raps);
}

/* ═══════════════════ 13. MODALES ═══════════════════ */

function modale(html){ $("modale").innerHTML = html; $("voile").classList.remove("cache"); }
function fermer(){ $("voile").classList.add("cache"); $("modale").innerHTML = ""; }

/* Choix d'un moment : les cinq que l'on utilise vraiment, plus le choix libre. */
function choixQuand(nomAct){
  const d = new Date();
  const opts = [
    { l:"Ce soir, 20 h",     v: fixe(20,0) },
    { l:"Demain matin, 7 h", v: fixe(7,0,1) },
    { l:"Demain midi",       v: fixe(12,0,1) },
    { l:"Dans 3 jours",      v: fixe(19,0,3) },
    { l:"Samedi après-midi", v: prochainJour(6, 16) },
    { l:"Dimanche matin",    v: prochainJour(0, 9) }
  ];
  return opts.map((o,i)=>'<button class="ligne" data-act="' + nomAct + '" data-arg="' + o.v + '">'
    + "<span>" + esc(o.l) + '</span><em class="tag">' + esc(new Date(o.v).toLocaleDateString("fr-FR",{day:"numeric",month:"short"})) + "</em></button>").join("");
  function fixe(h, m, plus){
    const x = new Date(); x.setHours(h, m||0, 0, 0);
    if(plus) x.setDate(x.getDate()+plus);
    else if(x <= new Date()) x.setDate(x.getDate()+1);
    return x.toISOString();
  }
  function prochainJour(dow, h){
    const x = new Date(); x.setHours(h,0,0,0);
    let add = (dow - x.getDay() + 7) % 7;
    if(add === 0 && x <= new Date()) add = 7;
    x.setDate(x.getDate() + add);
    return x.toISOString();
  }
}

function modaleProgrammer(){
  modale('<h3>Écrire maintenant, envoyer plus tard</h3>'
    + '<p class="sous">Elle/il ne verra rien avant l\'heure choisie. Parfait le dimanche soir, '
    + 'pour toute la semaine.</p>'
    + '<textarea id="pg-txt" maxlength="600" placeholder="Bonjour toi. Journée chargée, mais tu es dans ma tête."></textarea>'
    + '<label>Ça part quand ?</label><div class="liste">' + choixQuand("prog-ok")
    + '<div class="ligne"><span>Autre moment</span><input id="pg-libre" type="datetime-local" style="margin:0;max-width:180px"></div>'
    + '<button class="btn p" data-act="prog-libre">Programmer à cette date</button></div>'
    + '<button class="btn plat" data-act="fermer">Annuler</button>');
}
function modaleIdee(idee){
  modale('<h3>Proposer une activité</h3>'
    + '<div class="idee-jour" style="margin-bottom:12px"><span class="cat">' + esc(idee.cat) + "</span>" + esc(idee.t) + "</div>"
    + '<label>C\'est pour quand ?</label><div class="liste">' + choixQuand("idee-ok")
    + '<div class="ligne"><span>Autre moment</span><input id="id-libre" type="datetime-local" style="margin:0;max-width:180px"></div>'
    + '<button class="btn p" data-act="idee-libre">Proposer à cette date</button>'
    + '<button class="btn fant p" data-act="idee-sans">Proposer sans date</button></div>'
    + '<button class="btn plat" data-act="fermer">Annuler</button>');
  modale._idee = idee;
}
function modaleSalons(){
  const l = salons();
  modale('<h3>Vos salons</h3><div class="liste">'
    + l.map(x => '<button class="ligne' + (SALON && x.sid === SALON.sid ? " on" : "") + '" data-act="salon" data-arg="' + esc(x.sid) + '">'
      + "<span><b>" + esc(x.nom) + "</b><small>vous : " + esc(x.moi) + "</small></span>"
      + '<em class="tag">' + (SALON && x.sid === SALON.sid ? "ouvert" : "ouvrir") + "</em></button>").join("")
    + "</div>"
    + '<button class="btn p" style="margin-top:12px" data-act="salon-neuf">＋ Créer un salon</button>'
    + '<button class="btn fant p" style="margin-top:8px" data-act="salon-join">Rejoindre avec un code</button>'
    + '<button class="btn plat" data-act="fermer">Fermer</button>');
}
function modaleSalonNeuf(join){
  modale("<h3>" + (join ? "Rejoindre un salon" : "Nouveau salon") + "</h3>"
    + '<p class="sous">' + (join ? "Collez le code (ou le lien) reçu."
        : "Un salon par personne ou par groupe : « Nous deux », « Famille », « Maman »…") + "</p>"
    + (join ? '<label>Le code</label><input id="ns-code" placeholder="nous-XXXX-XXXX-XXXX" spellcheck="false">'
            : '<label>Nom du salon</label><input id="ns-nom" maxlength="30" placeholder="Famille">')
    + '<label>Votre prénom ici</label><input id="ns-moi" maxlength="20" placeholder="'
    + esc((SALON && SALON.moi) || "Moi") + '">'
    + '<button class="btn" data-act="' + (join ? "salon-join-ok" : "salon-neuf-ok") + '">'
    + (join ? "Rejoindre" : "Créer") + "</button>"
    + '<button class="btn plat" data-act="fermer">Annuler</button>');
}

/* ═══════════════════ 14. ACTIONS (délégation) ═══════════════════ */

const ACTIONS = {
  fermer,

  /* ── messages ── */
  async "photo-ok"(){
    const mot = ($("ph-mot") && $("ph-mot").value.trim()) || "";
    const data = modale._photo; fermer();
    if(data) await envoyer({ t:"photo", b:mot }, data);
  },
  async "rep-oui"(id){ await repondreIdee(id, "oui"); },
  async "rep-non"(id){ await repondreIdee(id, "non"); },
  msg(k){
    const m = MSGS.find(x => x.k === k);
    if(!m || !m.moi || m.t === "suppr") return;
    modale('<h3>Ce message</h3><p class="sous">' + esc((m.b || "(pièce jointe)").slice(0,120)) + "</p>"
      + '<button class="btn" data-act="msg-suppr" data-arg="' + esc(k) + '">Effacer pour tout le monde</button>'
      + '<button class="btn plat" data-act="fermer">Annuler</button>');
  },
  async "msg-suppr"(k){
    fermer();
    const m = MSGS.find(x => x.k === k); if(!m) return;
    if(m.id && NUAGE){ try{ await rpc("nous_effacer", { p_salon: SALON.sid, p_id: m.id }); }catch(e){} }
    m.t = "suppr"; m.b = ""; m.m = "";
    await dbPut(m); rendreFil();
  },

  /* ── idées ── */
  cat(c){ IDEE_CAT = c; rendreNous(); },
  "idee-choix"(arg){
    const [c, i] = arg.split("|");
    modaleIdee({ cat:c, t: IDEES[c][Number(i)] });
  },
  "idee-jour-autre"(){
    const l = toutesIdees();
    IDEE_COURANTE = l[Math.floor(Math.random()*l.length)];
    rendreNous();
  },
  async "idee-ok"(iso){ fermer(); await proposer(modale._idee, iso); },
  async "idee-libre"(){
    const v = $("id-libre") && $("id-libre").value;
    if(!v){ toast("Choisissez une date."); return; }
    const idee = modale._idee; fermer();
    await proposer(idee, new Date(v).toISOString());
  },
  async "idee-sans"(){ const i = modale._idee; fermer(); await proposer(i, ""); },

  /* ── programmés ── */
  async "prog-ok"(iso){
    const t = ($("pg-txt") && $("pg-txt").value.trim()) || "";
    if(!t){ toast("Écrivez d'abord le message."); return; }
    fermer(); await envoyer({ t:"texte", b:t }, "", iso);
  },
  async "prog-libre"(){
    const v = $("pg-libre") && $("pg-libre").value;
    const t = ($("pg-txt") && $("pg-txt").value.trim()) || "";
    if(!t){ toast("Écrivez d'abord le message."); return; }
    if(!v){ toast("Choisissez une date."); return; }
    fermer(); await envoyer({ t:"texte", b:t }, "", new Date(v).toISOString());
  },
  async "prog-annul"(k){
    const m = MSGS.find(x => x.k === k) || (await dbListe(SALON.sid)).find(x => x.k === k);
    if(!m) return;
    if(m.id && NUAGE){ try{ await rpc("nous_annuler", { p_salon: SALON.sid, p_id: m.id }); }catch(e){} }
    await dbDel(m.k);
    const i = MSGS.indexOf(m); if(i >= 0) MSGS.splice(i,1);
    rendreTemps(); toast("Message annulé.");
  },

  /* ── mode occupé ── */
  async occ(i){
    const o = OCCUPES[Number(i)];
    if(o.stop){ await ecrireStatut("", ""); rendreTemps(); toast("Vous êtes de nouveau disponible."); return; }
    let fin;
    if(o.soir) fin = finDeJournee(19);
    else if(o.jour){ fin = new Date(); fin.setHours(22,0,0,0); if(fin <= new Date()){ fin.setDate(fin.getDate()+1); } }
    else { fin = new Date(Date.now() + o.h*3600e3); }
    await ecrireStatut(fin.toISOString(), o.l);
    await envoyer({ t:"sys", b:"🕒 " + SALON.moi + " est pris jusqu'à " + hm(fin) + ". Pas parti — juste occupé." });
    rendreTemps();
    toast("C'est noté, elle/il le voit maintenant.");
  },

  /* ── dates ── */
  "date-add"(){
    modale('<h3>Une date à ne pas oublier</h3>'
      + '<label>Quoi ?</label><input id="dt-n" maxlength="40" placeholder="Anniversaire de Fatima">'
      + '<label>Le jour (jj/mm)</label><input id="dt-d" maxlength="5" placeholder="14/02" inputmode="numeric">'
      + '<button class="btn" data-act="date-ok">Ajouter</button>'
      + '<button class="btn plat" data-act="fermer">Annuler</button>');
  },
  "date-ok"(){
    const n = $("dt-n").value.trim(), d = $("dt-d").value.trim();
    if(!n || !/^\d{1,2}[\/-]\d{1,2}$/.test(d)){ toast("Il faut un nom et une date au format 14/02."); return; }
    const k = "nous_dates_" + SALON.sid, l = lsj(k) || [];
    l.push({ n, d }); lsj(k, l); fermer(); rendreNous();
  },
  "date-suppr"(i){
    const k = "nous_dates_" + SALON.sid, l = lsj(k) || [];
    l.splice(Number(i),1); lsj(k, l); rendreNous();
  },

  /* ── famille ── */
  "fam-add"(){
    modale('<h3>Un proche à ne pas perdre de vue</h3>'
      + '<label>Qui ?</label><input id="fa-n" maxlength="30" placeholder="Maman">'
      + '<label>Téléphone (facultatif)</label><input id="fa-t" placeholder="+269…" inputmode="tel">'
      + '<label>Prendre des nouvelles tous les…</label>'
      + '<select id="fa-j"><option value="2">2 jours</option><option value="3">3 jours</option>'
      + '<option value="7" selected>7 jours</option><option value="14">2 semaines</option>'
      + '<option value="30">1 mois</option></select>'
      + '<button class="btn" data-act="fam-ok2">Ajouter</button>'
      + '<button class="btn plat" data-act="fermer">Annuler</button>');
  },
  "fam-ok2"(){
    const n = $("fa-n").value.trim();
    if(!n){ toast("Il faut au moins un nom."); return; }
    const l = proches();
    l.push({ n, tel: $("fa-t").value.trim(), jours: Number($("fa-j").value) || 7, dernier: "" });
    proches(l); fermer(); rendreFamille();
  },
  "fam-ok"(i){
    const l = proches(); l[Number(i)].dernier = new Date().toISOString();
    proches(l); rendreFamille(); toast("Noté — le compteur repart.");
  },
  "fam-suppr"(i){ const l = proches(); l.splice(Number(i),1); proches(l); rendreFamille(); },
  "fam-tel"(i){ const p = proches()[Number(i)]; if(p.tel) location.href = "tel:" + p.tel.replace(/\s/g,""); },
  "fam-wa"(i){
    const p = proches()[Number(i)];
    if(p.tel) window.open("https://wa.me/" + p.tel.replace(/[^0-9]/g,""), "_blank", "noopener");
  },

  /* ── rappels ── */
  "rap-add"(){
    modale('<h3>Un rappel pour moi</h3>'
      + '<p class="sous">Il s\'affiche quand l\'application est ouverte, et en notification '
      + 'si vous les avez autorisées.</p>'
      + '<label>Quoi ?</label><input id="rp-t" maxlength="60" placeholder="Écrire un mot à ma femme">'
      + '<label>À quelle heure ?</label><input id="rp-h" type="time" value="12:30">'
      + '<button class="btn" data-act="rap-ok">Ajouter</button>'
      + '<button class="btn plat" data-act="fermer">Annuler</button>');
  },
  "rap-ok"(){
    const t = $("rp-t").value.trim(), h = $("rp-h").value || "12:30";
    if(!t){ toast("Écrivez le rappel."); return; }
    const l = lsj("nous_rappels") || []; l.push({ t, h, vu:"" }); lsj("nous_rappels", l);
    fermer(); rendreTemps(); demanderNotifs();
  },
  "rap-suppr"(i){ const l = lsj("nous_rappels") || []; l.splice(Number(i),1); lsj("nous_rappels", l); rendreTemps(); },

  /* ── salons ── */
  async salon(sid){ fermer(); await activerSalon(sid); allerVue("fil"); },
  "salon-neuf"(){ modaleSalonNeuf(false); },
  "salon-join"(){ modaleSalonNeuf(true); },
  async "salon-neuf-ok"(){
    const nom = $("ns-nom").value.trim() || "Nouveau salon";
    const moi = $("ns-moi").value.trim() || (SALON && SALON.moi) || "Moi";
    fermer(); await creerSalon(nom, moi); ecranPartage(); rendreFamille();
  },
  async "salon-join-ok"(){
    const code = normCode($("ns-code").value);
    const moi  = $("ns-moi").value.trim() || "Moi";
    if(!code){ toast("Ce code ne ressemble pas à un code de salon."); return; }
    fermer(); await creerSalon("Salon partagé", moi, code);
    toast("Salon ouvert. Les messages arrivent…"); rendreFamille(); allerVue("fil");
  },

  /* ── réglages ── */
  "rg-code"(){ ecranPartage(); },
  "rg-nom"(){
    modale('<h3>Ce salon</h3>'
      + '<label>Nom du salon</label><input id="rn-nom" maxlength="30" value="' + esc(SALON.nom) + '">'
      + '<label>Mon prénom ici</label><input id="rn-moi" maxlength="20" value="' + esc(SALON.moi) + '">'
      + '<button class="btn" data-act="rg-nom-ok">Enregistrer</button>'
      + '<button class="btn plat" data-act="fermer">Annuler</button>');
  },
  "rg-nom-ok"(){
    const nom = $("rn-nom").value.trim() || SALON.nom;
    const moi = $("rn-moi").value.trim() || SALON.moi;
    const l = salons(); const s = l.find(x => x.sid === SALON.sid);
    if(s){ s.nom = nom; s.moi = moi; salonsSet(l); SALON.nom = nom; SALON.moi = moi; }
    $("t-nom").textContent = nom;
    fermer(); rendreFamille(); toast("C'est enregistré ✔");
  },
  "rg-pin"(){ PIN_ETAPE = "def1"; PIN_SAISIE = ""; PIN_TEMP = ""; ls("nous_pin", null); montrerVerrou(); },
  "rg-notif"(){ demanderNotifs(true); },
  "rg-export"(){ exporter(); },
  "rg-quitter"(){
    modale('<h3>Retirer ce salon ?</h3><p class="sous">Les messages seront effacés '
      + "<b>de ce téléphone</b>. Avec le code, vous pourrez le rouvrir plus tard.</p>"
      + '<div class="code-box">' + esc(SALON.code) + "</div>"
      + '<button class="btn" data-act="quitter-ok">Oui, retirer</button>'
      + '<button class="btn plat" data-act="fermer">Annuler</button>');
  },
  async "quitter-ok"(){
    fermer();
    const sid = SALON.sid;
    for(const r of await dbListe(sid)) await dbDel(r.k);
    salonsSet(salons().filter(x => x.sid !== sid));
    ls("nous_dates_" + sid, null);
    const reste = salons();
    if(reste.length){ await activerSalon(reste[0].sid); allerVue("fil"); }
    else location.reload();
  }
};

async function repondreIdee(id, rep){
  const src = MSGS.find(m => Number(m.id) === Number(id));
  await envoyer({ t:"rep", ref: Number(id), rep,
    b: rep === "oui" ? "Oui, on le fait !" : "Pas cette fois — mais on retente." });
  if(rep === "oui" && src && src.quand) toast("C'est dans l'agenda ❤");
  rendreNous();
}
async function proposer(idee, iso){
  if(!idee) return;
  await envoyer({ t:"idee", b: idee.t, cat: idee.cat, quand: iso || "" });
  allerVue("fil");
}
function exporter(){
  const l = MSGS.filter(visibleMaintenant).map(m =>
    "[" + new Date(m.vis).toLocaleString("fr-FR") + "] " + (m.a || "?") + " : "
    + (m.t === "vocal" ? "(vocal)" : m.t === "photo" ? "(photo) " + m.b : m.t === "suppr" ? "(effacé)" : m.b));
  const b = new Blob([SALON.nom + "\n\n" + l.join("\n")], { type:"text/plain;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(b);
  a.download = "nous-" + new Date().toISOString().slice(0,10) + ".txt";
  a.click();
  setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
  toast("Sauvegarde enregistrée dans vos téléchargements.");
}
function demanderNotifs(fort){
  if(!("Notification" in window)){ if(fort) toast("Ce téléphone ne gère pas les notifications."); return; }
  if(Notification.permission === "granted"){ if(fort) toast("Les notifications sont déjà autorisées ✔"); return; }
  if(Notification.permission === "denied"){ if(fort) toast("Elles sont bloquées : réglages du navigateur → notifications."); return; }
  Notification.requestPermission().then(p => { if(fort) toast(p === "granted" ? "C'est autorisé ✔" : "Refusé."); });
}

/* ═══════════════════ 15. VERROU (code à 4 chiffres) ═══════════════════ */

async function pinHash(p){ return sha256hex("nous-pin|" + p); }
function montrerVerrou(){
  $("ec-verrou").classList.remove("cache");
  $("app").classList.add("cache");
  majPin();
}
function majPin(){
  const pts = $("vr-pts").children;
  for(let i=0;i<4;i++) pts[i].classList.toggle("on", i < PIN_SAISIE.length);
  const t = { ouvrir:["Votre code","Personne d'autre n'entre ici."],
              def1:["Choisissez un code","Quatre chiffres, faciles pour vous."],
              def2:["Encore une fois","Pour être sûr."] }[PIN_ETAPE];
  $("vr-titre").textContent = t[0]; $("vr-sous").textContent = t[1];
}
async function pinTape(k){
  if(k === "x"){ PIN_SAISIE = PIN_SAISIE.slice(0,-1); majPin(); return; }
  if(k === "s"){ PIN_SAISIE = ""; majPin(); return; }
  if(PIN_SAISIE.length >= 4) return;
  PIN_SAISIE += k; majPin();
  if(PIN_SAISIE.length < 4) return;

  const saisi = PIN_SAISIE; PIN_SAISIE = "";
  if(PIN_ETAPE === "ouvrir"){
    if(await pinHash(saisi) === ls("nous_pin")){ $("vr-err").textContent = ""; entrer(); }
    else { $("vr-err").textContent = "Ce n'est pas le bon code."; navigator.vibrate && navigator.vibrate(120); majPin(); }
  }else if(PIN_ETAPE === "def1"){
    PIN_TEMP = saisi; PIN_ETAPE = "def2"; $("vr-err").textContent = ""; majPin();
  }else{
    if(saisi === PIN_TEMP){
      ls("nous_pin", await pinHash(saisi));
      PIN_ETAPE = "ouvrir"; $("vr-err").textContent = "";
      toast("Code enregistré ✔"); entrer();
    }else{ PIN_ETAPE = "def1"; $("vr-err").textContent = "Les deux codes sont différents."; majPin(); }
  }
}

/* ═══════════════════ 16. ÉCRANS & NAVIGATION ═══════════════════ */

function ecran(id){
  ["ec-verrou","ec-bienvenue","ec-partage"].forEach(x => $(x).classList.add("cache"));
  if(id) $(id).classList.remove("cache");
  $("app").classList.toggle("cache", !!id);
}
function ecranPartage(){
  ecran("ec-partage");
  $("pt-code").textContent = SALON ? SALON.code : "";
}
function allerVue(v){
  VUE = v;
  ["fil","nous","famille","temps"].forEach(x => $("v-" + x).classList.toggle("cache", x !== v));
  document.querySelectorAll(".nav button").forEach(b => b.classList.toggle("on", b.dataset.v === v));
  $("feuille-plus").classList.add("cache");
  if(v === "fil"){ $("pt-fil").classList.remove("on"); rendreFil(); }
  if(v === "nous") rendreNous();
  if(v === "famille") rendreFamille();
  if(v === "temps") rendreTemps();
}
async function entrer(){
  ecran(null);
  allerVue("fil");
  if(!SALON){
    const l = salons();
    const act = ls("nous_actif");
    if(l.length) await activerSalon(l.find(x=>x.sid===act) ? act : l[0].sid);
  }
  demarrerSync();
}
function demarrerSync(){
  clearInterval(SYNC_T);
  SYNC_T = setInterval(()=>{
    if(document.visibilityState === "visible"){ sync(); verifierRappels(); rendreFilSiEcheance(); }
  }, CFG.SYNC_MS || 6000);
  sync(true); verifierRappels();
}
/* Un message programmé arrive à son heure : on redessine sans rien demander au serveur. */
let DERNIER_COMPTE = 0;
function rendreFilSiEcheance(){
  const n = MSGS.filter(visibleMaintenant).length;
  if(n !== DERNIER_COMPTE){ DERNIER_COMPTE = n; rendreFil(); rendreTemps(); }
}

/* ═══════════════════ 17. DÉMARRAGE ═══════════════════ */

async function demarrer(){
  if(!window.crypto || !crypto.subtle){
    document.body.innerHTML = '<div class="ecran plein"><div class="centre"><h1>Adresse non sécurisée</h1>'
      + '<p class="sous">Le chiffrement a besoin d\'une adresse en https. Ouvrez '
      + "https://moheligo.com/nous/</p></div></div>";
    return;
  }
  DEV = ls("nous_dev") || ls("nous_dev", uid());
  try{ DB = await dbOuvrir(); }catch(e){ toast("Mémoire du téléphone indisponible."); }

  /* Un lien partagé : https://moheligo.com/nous/#c=nous-XXXX-… */
  const lien = (location.hash || "").match(/c=([^&]+)/);
  let codeLien = "";
  if(lien){
    history.replaceState(null, "", location.pathname);
    codeLien = normCode(lien[1]);
  }
  if(codeLien && salons().length){
    /* Déjà installé : on ajoute simplement le salon reçu. */
    const coffre = await ouvrirCoffre(codeLien);
    if(!salons().some(x => x.sid === coffre.sid))
      await creerSalon("Salon partagé", ls("nous_prenom") || "Moi", codeLien);
  }

  if(!salons().length){
    /* Première fois : on pré-remplit le code, mais c'est la personne qui
       donne son prénom — sinon on ne saurait pas qui écrit. */
    if(codeLien){ $("nv-code").value = codeLien; }
    ecran("ec-bienvenue");
    return;
  }
  if(ls("nous_pin")){ PIN_ETAPE = "ouvrir"; ecran("ec-verrou"); majPin(); }
  else { PIN_ETAPE = "def1"; ecran("ec-verrou"); majPin(); }
}

/* ═══════════════════ 18. ÉVÉNEMENTS ═══════════════════ */

document.addEventListener("click", async e => {
  const a = e.target.closest("[data-act]");
  if(a){
    e.preventDefault();
    const f = ACTIONS[a.dataset.act];
    if(f) await f(a.dataset.arg);
    return;
  }
  const k = e.target.closest("[data-k]");
  if(k){ pinTape(k.dataset.k); return; }
  const nav = e.target.closest(".nav button");
  if(nav){ allerVue(nav.dataset.v); return; }
  if(e.target.id === "voile") fermer();
  if(!e.target.closest("#feuille-plus") && !e.target.closest("#b-plus"))
    $("feuille-plus").classList.add("cache");
});

/* Bienvenue */
$("nv-creer").addEventListener("click", async ()=>{
  const nom = $("nv-nom").value.trim() || "Nous deux";
  const moi = $("nv-moi").value.trim();
  if(!moi){ toast("Votre prénom, pour qu'elle sache que c'est vous."); return; }
  ls("nous_prenom", moi);
  await creerSalon(nom, moi);
  ecranPartage();
});
$("nv-rejoindre").addEventListener("click", async ()=>{
  const code = normCode($("nv-code").value);
  const moi = $("nv-moi2").value.trim();
  if(!code){ toast("Collez le code reçu (nous-XXXX-XXXX-XXXX)."); return; }
  if(!moi){ toast("Votre prénom, pour qu'on vous reconnaisse."); return; }
  ls("nous_prenom", moi);
  await creerSalon("Salon partagé", moi, code);
  PIN_ETAPE = ls("nous_pin") ? "ouvrir" : "def1";
  ecran("ec-verrou"); majPin();
});

/* Partage du code */
$("pt-partager").addEventListener("click", ()=>{
  const txt = "Notre messagerie privée : https://moheligo.com/nous/\nLe code du salon : "
    + SALON.code + "\n(à garder pour soi)";
  if(navigator.share) navigator.share({ text: txt }).catch(()=>{});
  else window.open("https://wa.me/?text=" + encodeURIComponent(txt), "_blank", "noopener");
});
$("pt-copier").addEventListener("click", ()=>{
  navigator.clipboard && navigator.clipboard.writeText(SALON.code)
    .then(()=>toast("Code copié ✔")).catch(()=>toast("Recopiez-le à la main."));
});
$("pt-suite").addEventListener("click", ()=>{
  if(ls("nous_pin")){ PIN_ETAPE = "ouvrir"; ecran("ec-verrou"); majPin(); }
  else { PIN_ETAPE = "def1"; ecran("ec-verrou"); majPin(); }
});

/* Fil */
$("b-envoi").addEventListener("click", envoyerTexte);
$("saisie").addEventListener("keydown", e => { if(e.key === "Enter") envoyerTexte(); });
$("b-plus").addEventListener("click", ()=> $("feuille-plus").classList.toggle("cache"));
$("fichier").addEventListener("change", choisirPhoto);
$("vocal-stop").addEventListener("click", ()=> vocalFin(true));
$("vocal-annul").addEventListener("click", ()=> vocalFin(false));
$("feuille-plus").addEventListener("click", async e => {
  const b = e.target.closest("button"); if(!b) return;
  $("feuille-plus").classList.add("cache");
  const a = b.dataset.a;
  if(a === "photo") $("fichier").click();
  if(a === "vocal") vocalDebut();
  if(a === "idee"){ allerVue("nous"); toast("Choisissez une idée, puis « proposer »."); }
  if(a === "prog") modaleProgrammer();
  if(a === "ping") await envoyer({ t:"ping", b:"Appelle-moi quand tu peux ❤" });
});
$("t-salons").addEventListener("click", modaleSalons);
$("t-sync").addEventListener("click", ()=>{ sync(true); lireEtat(); toast("Mise à jour…"); });
$("ij-proposer").addEventListener("click", ()=> modaleIdee(IDEE_COURANTE || ideeDuJour()));
$("ij-autre").addEventListener("click", ()=> ACTIONS["idee-jour-autre"]());
$("date-add").addEventListener("click", ()=> ACTIONS["date-add"]());
$("fam-add").addEventListener("click", ()=> ACTIONS["fam-add"]());
$("fam-salon-add").addEventListener("click", ()=> modaleSalonNeuf(false));
$("prog-add").addEventListener("click", modaleProgrammer);
$("rap-add").addEventListener("click", ()=> ACTIONS["rap-add"]());

document.addEventListener("visibilitychange", ()=>{
  if(document.visibilityState === "visible"){ sync(true); verifierRappels(); }
});

if("serviceWorker" in navigator)
  window.addEventListener("load", ()=> navigator.serviceWorker.register("sw.js").catch(()=>{}));

demarrer();
})();
