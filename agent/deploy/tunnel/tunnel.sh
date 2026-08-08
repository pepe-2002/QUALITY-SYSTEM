#!/usr/bin/env bash
# Expose ARA sur une adresse publique, depuis votre PC, par un tunnel Cloudflare.
#
#     bash deploy/tunnel/tunnel.sh
#
# Ce que fait ce script, et pourquoi il le fait ainsi :
#
# * il **exige un jeton**. Sans lui, quiconque tombe sur l'adresse pilote votre
#   agent : lance des recherches, produit des fichiers, consomme votre réseau.
#   Si `ARA_TOKEN` n'est pas défini, le script en fabrique un et vous le montre.
# * il fait écouter ARA sur **127.0.0.1 seulement**. Le tunnel s'y connecte
#   localement ; l'agent n'est donc jamais exposé sur votre Wi-Fi, même le
#   temps de la session.
# * il coupe tout — serveur et tunnel — quand vous faites Ctrl+C.
#
# L'adresse obtenue est temporaire : elle change à chaque lancement et meurt
# avec le script. C'est voulu. Une adresse permanente demande un compte
# Cloudflare et un nom de domaine, et se règle dans `README.md`.

set -uo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$RACINE" || exit 1

PORT="${ARA_PORT:-8800}"
PYTHON="${PYTHON:-python3}"
[ -x ".venv/bin/python" ] && PYTHON=".venv/bin/python"

# --- 1. cloudflared ----------------------------------------------------------
if ! command -v cloudflared > /dev/null 2>&1; then
  cat <<'AIDE'
✕ cloudflared n'est pas installé.

  Debian / Ubuntu :
    curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o /tmp/cf.deb
    sudo dpkg -i /tmp/cf.deb

  macOS :
    brew install cloudflared

  Windows :
    winget install --id Cloudflare.cloudflared

Puis relancez ce script.
AIDE
  exit 1
fi

# --- 2. Le jeton, non négociable --------------------------------------------
if [ -z "${ARA_TOKEN:-}" ]; then
  ARA_TOKEN="$("$PYTHON" -c 'import secrets; print(secrets.token_urlsafe(24))')"
  echo "→ Aucun ARA_TOKEN fourni : un jeton a été fabriqué pour cette session."
fi
export ARA_TOKEN

# --- 3. ARA, sur la boucle locale uniquement ---------------------------------
export ARA_HOST=127.0.0.1
export ARA_PORT="$PORT"

JOURNAL="$(mktemp -t ara-tunnel-XXXXXX.log)"
"$PYTHON" -m ara.cli --serve > "$JOURNAL" 2>&1 &
ARA_PID=$!

nettoyer() {
  echo
  echo "→ Arrêt…"
  [ -n "${TUNNEL_PID:-}" ] && kill "$TUNNEL_PID" 2> /dev/null
  kill "$ARA_PID" 2> /dev/null
  wait 2> /dev/null
  echo "→ Serveur et tunnel arrêtés. L'adresse publique n'existe plus."
}
trap nettoyer EXIT INT TERM

for _ in $(seq 1 20); do
  curl -s --noproxy '*' "http://127.0.0.1:$PORT/api/health?token=$ARA_TOKEN" \
    > /dev/null 2>&1 && break
  sleep 0.5
done

if ! kill -0 "$ARA_PID" 2> /dev/null; then
  echo "✕ ARA n'a pas démarré :"
  cat "$JOURNAL"
  exit 1
fi
echo "→ ARA écoute sur 127.0.0.1:$PORT (pas sur votre Wi-Fi)."

# --- 4. Le tunnel ------------------------------------------------------------
TUNNEL_LOG="$(mktemp -t cloudflared-XXXXXX.log)"
cloudflared tunnel --no-autoupdate --url "http://127.0.0.1:$PORT" \
  > "$TUNNEL_LOG" 2>&1 &
TUNNEL_PID=$!

echo "→ Ouverture du tunnel…"
ADRESSE=""
for _ in $(seq 1 40); do
  ADRESSE="$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUNNEL_LOG" \
    | head -1)"
  [ -n "$ADRESSE" ] && break
  kill -0 "$TUNNEL_PID" 2> /dev/null || break
  sleep 0.5
done

if [ -z "$ADRESSE" ]; then
  echo "✕ Le tunnel ne s'est pas ouvert :"
  tail -20 "$TUNNEL_LOG"
  exit 1
fi

cat <<MESSAGE

────────────────────────────────────────────────────────────────
  Votre agent est joignable ici :

  $ADRESSE/?token=$ARA_TOKEN

  Ouvrez ce lien sur le téléphone, puis « Ajouter à l'écran
  d'accueil ». Gardez-le pour vous : ce lien EST la clé.
────────────────────────────────────────────────────────────────

  · L'adresse meurt quand vous faites Ctrl+C.
  · Elle change à chaque lancement.
  · Sans le jeton, l'interface s'affiche mais ne répond rien.

  Journal du serveur : $JOURNAL
  Journal du tunnel  : $TUNNEL_LOG

MESSAGE

wait "$ARA_PID"
