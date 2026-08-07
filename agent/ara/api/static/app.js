/* ARA — logique de l'interface mobile.
   Aucune bibliothèque : tout tient en vanilla JS pour rester léger sur une
   connexion lente (contrainte réelle du terrain, cf. MoheliGo).            */

'use strict';

const STAGES = ['TACHE', 'RECHERCHE', 'ANALYSE', 'CREATION', 'VERIFICATION', 'RESULTAT'];
const LABEL = {
  TACHE: 'Tâche',
  RECHERCHE: 'Recherche',
  ANALYSE: 'Analyse',
  CREATION: 'Création',
  VERIFICATION: 'Vérification',
  RESULTAT: 'Résultat',
};
const MARK = { pending: '○', running: '◐', done: '●', skipped: '–', failed: '✕' };

const $ = (id) => document.getElementById(id);
const token = new URLSearchParams(location.search).get('token') || '';
const api = (path) => path + (token ? (path.includes('?') ? '&' : '?') + 'token=' + encodeURIComponent(token) : '');

let stream = null;
let currentTask = null;

/* ————————————————— Utilitaires ————————————————— */

const escapeHtml = (s) => String(s).replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

function timeAgo(ts) {
  if (!ts) return '';
  const seconds = Math.max(0, (Date.now() / 1000) - ts);
  if (seconds < 60) return "à l'instant";
  if (seconds < 3600) return `il y a ${Math.floor(seconds / 60)} min`;
  if (seconds < 86400) return `il y a ${Math.floor(seconds / 3600)} h`;
  return new Date(ts * 1000).toLocaleDateString('fr-FR');
}

async function getJSON(path) {
  const response = await fetch(api(path));
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).error || response.status);
  return response.json();
}

/* Rendu Markdown minimal — volontairement limité, tout est échappé d'abord. */
function markdown(src) {
  const lines = String(src || '').split('\n');
  const out = [];
  let list = null;   // 'ul' | 'ol'
  let table = null;  // tableau de lignes en cours

  const closeList = () => { if (list) { out.push(`</${list}>`); list = null; } };
  const closeTable = () => {
    if (!table) return;
    const cells = (row, tag) => row.map((c) => `<${tag}>${inline(c)}</${tag}>`).join('');
    out.push('<table><thead><tr>' + cells(table[0], 'th') + '</tr></thead><tbody>' +
      table.slice(1).map((r) => '<tr>' + cells(r, 'td') + '</tr>').join('') + '</tbody></table>');
    table = null;
  };

  const inline = (text) => escapeHtml(text)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|\s)\*([^*]+)\*/g, '$1<em>$2</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>')
    .replace(/\[(S\d+)\]/g, '<span class="cite">$1</span>');

  for (const raw of lines) {
    const line = raw.trim();

    if (!line) { closeList(); closeTable(); continue; }

    if (/^\|.*\|$/.test(line)) {
      const cells = line.replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
      if (cells.every((c) => /^:?-{2,}:?$/.test(c))) continue; // ligne de séparation
      closeList();
      (table = table || []).push(cells);
      continue;
    }
    closeTable();

    const heading = line.match(/^(#{1,4})\s+(.*)$/);
    if (heading) {
      closeList();
      const level = Math.min(heading[1].length + 1, 4);
      out.push(`<h${level}>${inline(heading[2])}</h${level}>`);
      continue;
    }
    if (/^(-{3,}|\*{3,})$/.test(line)) { closeList(); out.push('<hr>'); continue; }
    if (/^>\s?/.test(line)) { closeList(); out.push(`<blockquote>${inline(line.replace(/^>\s?/, ''))}</blockquote>`); continue; }

    const bullet = line.match(/^[-*•]\s+(.*)$/);
    if (bullet) {
      if (list !== 'ul') { closeList(); out.push('<ul>'); list = 'ul'; }
      out.push(`<li>${inline(bullet[1])}</li>`);
      continue;
    }
    const numbered = line.match(/^\d+[.)]\s+(.*)$/);
    if (numbered) {
      if (list !== 'ol') { closeList(); out.push('<ol>'); list = 'ol'; }
      out.push(`<li>${inline(numbered[1])}</li>`);
      continue;
    }

    closeList();
    out.push(`<p>${inline(line)}</p>`);
  }
  closeList(); closeTable();
  return out.join('');
}

/* ————————————————— Pipeline ————————————————— */

function resetPipeline() {
  $('stages').innerHTML = STAGES.map((stage) => `
    <li id="stage-${stage}" class="pending">
      <span class="mark">${MARK.pending}</span>
      <span>${LABEL[stage]}</span>
      <span class="note" id="note-${stage}"></span>
    </li>`).join('');
  $('stage-detail').textContent = '';
  $('pipeline').hidden = false;
  $('result').hidden = true;
  $('notices').hidden = true;
  $('notices').innerHTML = '';
}

function applyStage(event) {
  const node = $('stage-' + event.stage);
  if (!node) return;
  node.className = event.status;
  node.querySelector('.mark').textContent = MARK[event.status] || '○';
  if (event.message) {
    $('note-' + event.stage).textContent = event.message;
    $('stage-detail').textContent = `${LABEL[event.stage] || event.stage} — ${event.message}`;
  }
}

function addNotice(text, alert = false) {
  const box = $('notices');
  box.hidden = false;
  const item = document.createElement('div');
  item.className = alert ? 'notice alert' : 'notice';
  item.textContent = text;
  box.appendChild(item);
}

/* ————————————————— Résultat ————————————————— */

function renderResult(task) {
  currentTask = task;
  $('result').hidden = false;
  $('answer').innerHTML = markdown(task.answer || 'Aucune réponse produite.');

  const report = task.report || {};

  // Les désaccords entre sources passent avant la réponse : c'est ce que
  // l'utilisateur doit voir en premier s'il compte agir sur ces chiffres.
  const contradictions = report.contradictions || [];
  $('contradictions-block').hidden = contradictions.length === 0;
  $('contradictions').innerHTML = contradictions.map((item) => `
    <li>
      <div class="values">${escapeHtml(item.describe || '')}</div>
      <div class="subject">sources ${(item.sources || []).map((s) => 'S' + s).join(', ')}</div>
      ${(item.sentences || []).slice(0, 2).map((s) =>
        `<div class="quote">« ${escapeHtml(s.length > 200 ? s.slice(0, 200) + '…' : s)} »</div>`).join('')}
    </li>`).join('');

  const loop = $('loop-summary');
  if (report.iterations) {
    loop.hidden = false;
    loop.textContent =
      `${report.iterations} cycle(s) de recherche · ${(report.queries || []).length} requête(s) · ` +
      `${report.sources || 0} source(s) sur ${(report.domains || []).length} domaine(s)` +
      (report.stopped_because ? ` · arrêt : ${report.stopped_because}` : '');
  } else {
    loop.hidden = true;
  }

  const notices = $('notices');
  notices.innerHTML = '';
  const messages = [...(task.notices || []), ...(task.errors || [])];
  notices.hidden = messages.length === 0;
  messages.forEach((message) => addNotice(message, message.startsWith('CONTRADICTION')));

  const files = task.files || [];
  $('files-block').hidden = files.length === 0;
  $('files').innerHTML = files.map((file) => {
    const meta = [
      file.pages ? `${file.pages} page(s)` : '',
      file.size ? `${Math.max(1, Math.round(file.size / 1024))} ko` : '',
    ].filter(Boolean).join(' · ');
    return `<li><a href="${api(`/api/tasks/${task.task_id}/files/${encodeURIComponent(file.name)}`)}"
      target="_blank" rel="noopener" download>
      <span><span class="badge">${escapeHtml(file.format || file.kind || '')}</span>
      &nbsp;${escapeHtml(file.name)}</span>
      <span class="meta">${meta}</span></a></li>`;
  }).join('');

  const sources = task.sources || [];
  $('sources-block').hidden = sources.length === 0;
  $('sources').innerHTML = sources.map((source, index) => `
    <li><span class="cite">S${index + 1}</span> ${escapeHtml(source.title || source.domain || '')}
      <div class="dom">${escapeHtml(source.domain || '')}</div>
      <a href="${escapeHtml(source.url)}" target="_blank" rel="noopener">${escapeHtml(source.url)}</a></li>`).join('');

  $('result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ————————————————— Exécution ————————————————— */

function listen(taskId) {
  if (stream) stream.close();
  stream = new EventSource(api(`/api/tasks/${taskId}/events`));

  stream.onmessage = (message) => {
    let event;
    try { event = JSON.parse(message.data); } catch { return; }

    if (event.type === 'stage') applyStage(event);
    else if (event.type === 'log' && event.data && event.data.kind === 'contradiction') {
      addNotice(event.message, true);
    }
    else if (event.type === 'log' && event.data && event.data.kind === 'notice') addNotice(event.message);
    else if (event.type === 'log' && event.message) $('stage-detail').textContent = event.message;
    else if (event.type === 'final') {
      renderResult(event.task);
      stream.close(); stream = null;
      $('btn-send').disabled = false;
      $('btn-send').textContent = 'Lancer la tâche';
      loadHistory();
    }
  };

  stream.onerror = () => {
    // Le flux se ferme normalement à la fin ; on récupère l'état final.
    if (stream) { stream.close(); stream = null; }
    getJSON(`/api/tasks/${taskId}`).then(renderResult).catch(() => {}).finally(() => {
      $('btn-send').disabled = false;
      $('btn-send').textContent = 'Lancer la tâche';
    });
  };
}

async function launch(prompt) {
  resetPipeline();
  $('btn-send').disabled = true;
  $('btn-send').textContent = 'En cours…';
  try {
    const response = await fetch(api('/api/tasks'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Erreur serveur');
    listen(data.task_id);
  } catch (error) {
    addNotice('Impossible de lancer la tâche : ' + error.message);
    $('btn-send').disabled = false;
    $('btn-send').textContent = 'Lancer la tâche';
  }
}

/* ————————————————— Historique ————————————————— */

async function loadHistory() {
  try {
    const data = await getJSON('/api/tasks?limit=50');
    const list = $('history');
    if (!data.tasks.length) {
      list.innerHTML = '<li class="muted small">Aucune tâche pour le moment.</li>';
      return;
    }
    list.innerHTML = data.tasks.map((task) => `
      <li><button data-id="${task.task_id}">
        <div class="row">
          <span>${escapeHtml(task.prompt)}</span>
          <span class="when">${timeAgo(task.created_at)}</span>
        </div>
        <div class="tags">
          <span class="state ${task.status}">${task.status}</span>
          · ${task.complexity || '—'} · ${task.files} fichier(s) · ${task.sources} source(s)
          ${task.cycles ? ` · ${task.cycles} cycle(s)` : ''}
          ${task.contradictions ? ` · <span class="state error">${task.contradictions} contradiction(s)</span>` : ''}
        </div>
      </button></li>`).join('');

    list.querySelectorAll('button').forEach((button) => {
      button.onclick = async () => {
        const task = await getJSON(`/api/tasks/${button.dataset.id}`);
        switchView('run');
        $('prompt').value = task.prompt;
        $('pipeline').hidden = true;
        renderResult(task);
      };
    });
  } catch (error) {
    $('history').innerHTML = `<li class="muted small">Historique indisponible : ${escapeHtml(error.message)}</li>`;
  }
}

/* ————————————————— Configuration ————————————————— */

async function showInfo() {
  $('info-dialog').showModal();
  try {
    const config = await getJSON('/api/config');
    const providers = (list) => list.map((p) =>
      `<li class="${p.available ? 'on' : 'off'}">${p.available ? '✓' : '✕'} <strong>${escapeHtml(p.name)}</strong>` +
      (p.reason ? ` — ${escapeHtml(p.reason)}` : '') + '</li>').join('');

    $('info-body').innerHTML = `
      <h4>Modèle de langage (actuel : ${escapeHtml(config.llm.selected)})</h4>
      <ul>${providers(config.llm.providers)}</ul>
      <h4>Recherche (actuel : ${escapeHtml(config.search.selected)})</h4>
      <ul>${providers(config.search.providers)}</ul>
      <h4>Outils autorisés</h4>
      <ul>${config.tools.map((t) =>
        `<li class="${t.allowed ? 'on' : 'off'}">${t.allowed ? '✓' : '✕'} <strong>${escapeHtml(t.name)}</strong>` +
        (t.sensitive ? ' <em>(confirmation requise)</em>' : '') +
        (t.requires_external ? ' <em>(ressource externe)</em>' : '') + '</li>').join('')}</ul>
      <h4>Limites</h4>
      <ul>${Object.entries(config.limits).map(([k, v]) => `<li>${escapeHtml(k)} : ${v}</li>`).join('')}</ul>`;
  } catch (error) {
    $('info-body').textContent = 'Configuration indisponible : ' + error.message;
  }
}

/* ————————————————— Navigation ————————————————— */

function switchView(name) {
  document.querySelectorAll('.tab').forEach((tab) => tab.classList.toggle('active', tab.dataset.view === name));
  document.querySelectorAll('.view').forEach((view) => view.classList.toggle('active', view.id === 'view-' + name));
  if (name === 'history') loadHistory();
}

/* ————————————————— Démarrage ————————————————— */

document.addEventListener('DOMContentLoaded', () => {
  $('task-form').onsubmit = (event) => {
    event.preventDefault();
    const prompt = $('prompt').value.trim();
    if (prompt) launch(prompt);
  };

  $('chips').onclick = (event) => {
    if (!event.target.classList.contains('chip')) return;
    $('prompt').value = event.target.textContent.trim();
    $('prompt').focus();
  };

  document.querySelectorAll('.tab').forEach((tab) => {
    tab.onclick = () => switchView(tab.dataset.view);
  });

  $('btn-info').onclick = showInfo;
  $('btn-close-info').onclick = () => $('info-dialog').close();

  getJSON('/api/health')
    .then(() => $('health-dot').classList.add('ok'))
    .catch(() => $('health-dot').classList.add('err'));

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }
});
