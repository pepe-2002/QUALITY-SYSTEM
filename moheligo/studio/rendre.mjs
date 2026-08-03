#!/usr/bin/env node
/* ================================================================
   🎬 STUDIO MOHELIGO — programme de rendu
   Épisode (JSON) ➜ voix neuronales ➜ images dessinées ➜ MP4.

   Usage :
     node rendre.mjs episodes/ep1-le-billet-damina.json
     node rendre.mjs <episode> --apercu 3,12,40      (images fixes PNG)
     node rendre.mjs <episode> --muet                (sans refaire les voix)
   ================================================================ */
import { createRequire } from "node:module";
import { spawn, spawnSync, execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const ICI = path.dirname(fileURLToPath(import.meta.url));

function charger(nom) {
  try { return require(nom); }
  catch { return require("/opt/node22/lib/node_modules/" + nom); }
}
const { chromium } = charger("playwright");

/* ---------- outils ---------- */
const FFMPEG = process.env.FFMPEG || "ffmpeg";
const CERT = "/root/.ccr/ca-bundle.crt";
const args = process.argv.slice(2);
const epPath = path.resolve(args[0] || path.join(ICI, "episodes/ep1-le-billet-damina.json"));
const opt = (n, d) => { const i = args.indexOf("--" + n); return i < 0 ? d : (args[i + 1] || true); };
const flag = (n) => args.includes("--" + n);

const EP = JSON.parse(fs.readFileSync(epPath, "utf8"));
const BUILD = path.join(ICI, "build", EP.fichier);
const VOIX = path.join(BUILD, "voix");
fs.mkdirSync(VOIX, { recursive: true });
const SORTIE = path.resolve(opt("sortie", path.join(ICI, "../pub/serie")));
fs.mkdirSync(SORTIE, { recursive: true });

const log = (...m) => console.log("·", ...m);
const FPS = EP.fps || 25;

/* ================================================================
   1. LES VOIX (edge-tts, voix neuronales)
   ================================================================ */
function voixDuPlan(plan) {
  const r = plan.replique;
  if (!r) return null;
  const dit = (r.dit !== undefined ? r.dit : r.texte) || "";
  if (!dit.trim()) return null;
  const perso = EP.personnages[r.qui] || {};
  return { texte: dit, voix: perso.voix || "fr-FR-HenriNeural", rate: perso.rate || "-6%" };
}

function fabriquerVoix() {
  const secours = { "fr-FR-RemyMultilingualNeural": "fr-FR-HenriNeural", "fr-FR-VivienneMultilingualNeural": "fr-FR-DeniseNeural" };
  EP.plans.forEach((plan, i) => {
    const v = voixDuPlan(plan);
    if (!v) return;
    const cle = crypto.createHash("sha1").update(v.texte + v.voix + v.rate).digest("hex").slice(0, 10);
    const out = path.join(VOIX, `${String(i).padStart(2, "0")}-${cle}.mp3`);
    plan._voix = out;
    if (fs.existsSync(out) && fs.statSync(out).size > 500) return;
    for (const voix of [v.voix, secours[v.voix]].filter(Boolean)) {
      const r = spawnSync("edge-tts", ["--proxy", process.env.HTTPS_PROXY || "", "--voice", voix,
        `--rate=${v.rate}`, "--text", v.texte, "--write-media", out],
        { env: { ...process.env, SSL_CERT_FILE: CERT }, stdio: ["ignore", "pipe", "pipe"] });
      if (fs.existsSync(out) && fs.statSync(out).size > 500) {
        log(`voix ${i} (${voix}) : ${v.texte.slice(0, 46)}…`);
        return;
      }
      console.error(`  ⚠︎ voix ${voix} indisponible, essai suivant`, (r.stderr || "").toString().slice(0, 160));
    }
    throw new Error("Impossible de générer la voix du plan " + i);
  });
}

/* PCM mono 16 kHz d'un mp3 → Float32Array */
function pcm(fichier) {
  const brut = execFileSync(FFMPEG, ["-v", "quiet", "-i", fichier, "-ac", "1", "-ar", "16000",
    "-f", "s16le", "-"], { maxBuffer: 1 << 28 });
  const n = Math.floor(brut.length / 2), out = new Float32Array(n);
  for (let i = 0; i < n; i++) out[i] = brut.readInt16LE(i * 2) / 32768;
  return out;
}

/* ================================================================
   2. MONTAGE DU TEMPS : durée de chaque plan + enveloppe des bouches
   ================================================================ */
const AVANT = 0.25, APRES = 0.55;   // respiration avant / après chaque réplique

function minuter() {
  let t = 0;
  EP.plans.forEach((plan) => {
    let duree = plan.duree_min || 2.2;
    if (plan._voix) {
      const s = pcm(plan._voix);
      plan._dureeVoix = s.length / 16000;
      plan._pcm = s;
      duree = Math.max(duree, AVANT + plan._dureeVoix + APRES);
    }
    plan._debut = t; plan._duree = duree; t += duree;
  });
  EP._duree = t;
  return t;
}

/* une valeur d'ouverture de bouche (0..1) par image de la vidéo */
function enveloppe(total) {
  const n = Math.ceil(total * FPS) + 4, env = new Float32Array(n);
  EP.plans.forEach((plan) => {
    if (!plan._pcm) return;
    const s = plan._pcm, fen = Math.round(16000 / FPS);
    const f0 = Math.round((plan._debut + AVANT) * FPS);
    const nb = Math.ceil(s.length / fen);
    let max = 0; const vals = new Float32Array(nb);
    for (let k = 0; k < nb; k++) {
      let somme = 0, c = 0;
      for (let j = k * fen; j < Math.min((k + 1) * fen, s.length); j++) { somme += s[j] * s[j]; c++; }
      const v = Math.sqrt(somme / Math.max(1, c));
      vals[k] = v; if (v > max) max = v;
    }
    for (let k = 0; k < nb; k++) {
      const v = max > 0 ? Math.min(1, Math.pow(vals[k] / max, 0.65) * 1.25) : 0;
      if (f0 + k >= 0 && f0 + k < n) env[f0 + k] = v;
    }
  });
  /* lissage : la mâchoire n'est pas un interrupteur */
  const liss = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    liss[i] = (env[Math.max(0, i - 1)] * 0.25 + env[i] * 0.5 + env[Math.min(n - 1, i + 1)] * 0.25);
  }
  return Array.from(liss);
}

/* ================================================================
   3. LA BANDE SON (voix placées dans le temps, mixées)
   ================================================================ */
function bandeSon(total) {
  const parlants = EP.plans.filter((p) => p._voix);
  const sortie = path.join(BUILD, "bande-son.wav");
  if (!parlants.length) {
    execFileSync(FFMPEG, ["-y", "-v", "error", "-f", "lavfi", "-i", `anullsrc=r=48000:cl=stereo`,
      "-t", total.toFixed(3), sortie]);
    return sortie;
  }
  const entrees = [], filtres = [];
  parlants.forEach((p, i) => {
    entrees.push("-i", p._voix);
    const ms = Math.round((p._debut + AVANT) * 1000);
    filtres.push(`[${i}:a]aresample=48000,volume=5dB,adelay=${ms}|${ms}[v${i}]`);
  });
  const mix = parlants.map((_, i) => `[v${i}]`).join("") +
    `amix=inputs=${parlants.length}:normalize=0:dropout_transition=0[m];` +
    `[m]alimiter=limit=0.95,apad,atrim=0:${total.toFixed(3)}[out]`;
  execFileSync(FFMPEG, ["-y", "-v", "error", ...entrees, "-filter_complex",
    filtres.join(";") + ";" + mix, "-map", "[out]", "-ac", "2", "-ar", "48000", sortie],
    { maxBuffer: 1 << 28 });
  log("bande son :", path.basename(sortie));
  return sortie;
}

/* ================================================================
   4. LE DESSIN : Chromium rend chaque image, ffmpeg les enfile
   ================================================================ */
async function dessiner(env, total, apercu) {
  const navigateur = await chromium.launch({
    executablePath: process.env.CHROMIUM || undefined,
    /* --allow-file-access-from-files : sinon le logo (file://) « salit » le canvas
       et toDataURL refuse d'exporter l'image. */
    args: ["--no-sandbox", "--allow-file-access-from-files", "--disable-lcd-text",
      "--font-render-hinting=none", "--force-color-profile=srgb"]
  });
  const page = await navigateur.newPage({ viewport: { width: 520, height: 900 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("  ⚠︎ page :", e.message));
  await page.goto("file://" + path.join(ICI, "engine/index.html"));
  await page.evaluate(() => window.pretes());
  const propre = JSON.parse(JSON.stringify(EP, (k, v) => (k === "_pcm" ? undefined : v)));
  const info = await page.evaluate(([e, v]) => window.chargerEpisode(e, v), [propre, env]);
  log(`épisode chargé : ${info.plans} plans, ${info.duree.toFixed(1)} s`);

  if (apercu) {
    const dir = path.join(BUILD, "apercu"); fs.mkdirSync(dir, { recursive: true });
    for (const t of apercu) {
      const b64 = await page.evaluate((tt) => { window.image(tt); return document.getElementById("scene").toDataURL("image/png"); }, t);
      const f = path.join(dir, `t${String(t).replace(".", "_")}.png`);
      fs.writeFileSync(f, Buffer.from(b64.split(",")[1], "base64"));
      log("aperçu", f);
    }
    await navigateur.close();
    return null;
  }

  const videoSeule = path.join(BUILD, "video-muette.mp4");
  const ff = spawn(FFMPEG, ["-y", "-v", "error", "-f", "image2pipe", "-vcodec", "mjpeg",
    "-framerate", String(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart", videoSeule], { stdio: ["pipe", "inherit", "inherit"] });

  const nb = Math.round(total * FPS);
  const debut = Date.now();
  for (let i = 0; i < nb; i++) {
    const b64 = await page.evaluate((t) => {
      window.image(t);
      return document.getElementById("scene").toDataURL("image/jpeg", 0.94);
    }, i / FPS);
    const buf = Buffer.from(b64.split(",")[1], "base64");
    if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once("drain", r));
    if (i % (FPS * 5) === 0) {
      const pct = (100 * i / nb).toFixed(0), vit = (i + 1) / ((Date.now() - debut) / 1000);
      log(`images ${i}/${nb} (${pct} %) — ${vit.toFixed(1)} img/s`);
    }
  }
  ff.stdin.end();
  await new Promise((r) => ff.on("close", r));
  await navigateur.close();
  log("vidéo muette :", path.basename(videoSeule));
  return videoSeule;
}

/* ================================================================
   5. ASSEMBLAGE
   ================================================================ */
function assembler(video, son) {
  const final = path.join(SORTIE, EP.fichier + ".mp4");
  execFileSync(FFMPEG, ["-y", "-v", "error", "-i", video, "-i", son, "-map", "0:v", "-map", "1:a",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", final]);
  const leger = path.join(SORTIE, EP.fichier + "-leger.mp4");
  execFileSync(FFMPEG, ["-y", "-v", "error", "-i", final, "-vf", "scale=720:1280", "-c:v", "libx264",
    "-preset", "slow", "-crf", "26", "-c:a", "aac", "-b:a", "80k", "-ac", "1",
    "-movflags", "+faststart", leger], { maxBuffer: 1 << 28 });
  const mo = (f) => (fs.statSync(f).size / 1048576).toFixed(1) + " Mo";
  log("✅", final, mo(final));
  log("✅", leger, mo(leger), "(version connexions lentes)");
  return final;
}

/* ================================================================ */
(async function principal() {
  console.log(`\n🎬 ${EP.titre}\n`);
  if (!flag("muet")) fabriquerVoix();
  else EP.plans.forEach((p, i) => {
    const f = fs.readdirSync(VOIX).find((x) => x.startsWith(String(i).padStart(2, "0") + "-"));
    if (f) p._voix = path.join(VOIX, f);
  });
  const total = minuter();
  log(`durée totale : ${total.toFixed(1)} s (${EP.plans.length} plans)`);
  const env = enveloppe(total);
  const apercu = opt("apercu", null);
  const video = await dessiner(env, total, apercu ? String(apercu).split(",").map(Number) : null);
  if (!video) return;
  const son = bandeSon(total);
  assembler(video, son);
})().catch((e) => { console.error("\n❌", e.message); process.exit(1); });
