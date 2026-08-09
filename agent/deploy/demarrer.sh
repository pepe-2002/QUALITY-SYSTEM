#!/usr/bin/env bash
# ARA — démarrage en une commande. Linux, macOS, Termux.
#
#     bash demarrer.sh              → ouvre l'agent sur cet ordinateur
#     bash demarrer.sh --telephone  → …et fabrique en plus une adresse publique
#
# Ce script fait tout : il récupère le code, vérifie Python, fabrique un jeton,
# lance le serveur sur la boucle locale et ouvre le navigateur.
#
# Aucune installation de bibliothèque : ARA n'a **aucune dépendance
# obligatoire**. Pas de pip, pas d'environnement virtuel, pas de compilateur.
# C'était une contrainte du projet dès le début, et c'est ce qui permet ce
# script de trente lignes utiles.

set -uo pipefail

DEPOT="https://github.com/pepe-2002/QUALITY-SYSTEM.git"
BRANCHE="claude/ai-autonomous-research-creative-agent-0su1cb"
PORT="${ARA_PORT:-8800}"
TELEPHONE=0
[ "${1:-}" = "--telephone" ] && TELEPHONE=1

# --- 1. Python ---------------------------------------------------------------
PYTHON=""
for candidat in python3 python; do
  if command -v "$candidat" > /dev/null 2>&1; then
    if "$candidat" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
      PYTHON="$candidat"
      break
    fi
  fi
done

if [ -z "$PYTHON" ]; then
  cat <<'AIDE'
✕ Python 3.10 ou plus récent est nécessaire, et n'a pas été trouvé.

  Debian / Ubuntu :  sudo apt install python3
  macOS :            brew install python3
  Termux :           pkg install python git

Puis relancez ce script.
AIDE
  exit 1
fi

# --- 2. Le code --------------------------------------------------------------
# Si le script est déjà dans le dépôt, on l'utilise sur place. Sinon on clone.
#
# `BASH_SOURCE` est **vide quand le script arrive par un tuyau** (`curl … | bash`) :
# il n'y a alors aucun fichier sur le disque à désigner. Sans le repli `:-`,
# `set -u` interrompt la ligne et affiche deux erreurs inquiétantes avant de
# continuer quand même. C'est le cas normal d'un premier lancement, pas une panne.
SOURCE="${BASH_SOURCE[0]:-}"
ICI=""
[ -n "$SOURCE" ] && ICI="$(cd "$(dirname "$SOURCE")" 2> /dev/null && pwd)"

if [ -n "$ICI" ] && [ -f "$ICI/../ara/cli.py" ]; then
  RACINE="$(cd "$ICI/.." && pwd)"
  echo "→ Code trouvé sur place : $RACINE"
else
  RACINE="$HOME/ara/agent"
  if [ -d "$HOME/ara/.git" ]; then
    echo "→ Mise à jour du code…"
    git -C "$HOME/ara" fetch --quiet origin "$BRANCHE" \
      && git -C "$HOME/ara" checkout --quiet "$BRANCHE" \
      && git -C "$HOME/ara" pull --quiet origin "$BRANCHE" \
      || echo "  (mise à jour impossible — on continue avec la version locale)"
  else
    command -v git > /dev/null 2>&1 || { echo "✕ git est nécessaire pour récupérer le code."; exit 1; }
    echo "→ Récupération du code dans $HOME/ara…"
    git clone --quiet --branch "$BRANCHE" --depth 1 "$DEPOT" "$HOME/ara" || exit 1
  fi
fi
cd "$RACINE" || exit 1

# --- 3. Le jeton, non négociable ---------------------------------------------
# Sans lui, quiconque atteint l'adresse pilote l'agent. Il est conservé d'une
# fois sur l'autre pour que le lien enregistré sur le téléphone reste valable.
JETON_FICHIER="$RACINE/workspace/.jeton"
if [ -z "${ARA_TOKEN:-}" ]; then
  if [ -f "$JETON_FICHIER" ]; then
    ARA_TOKEN="$(cat "$JETON_FICHIER")"
  else
    ARA_TOKEN="$("$PYTHON" -c 'import secrets; print(secrets.token_urlsafe(24))')"
    mkdir -p "$RACINE/workspace"
    printf '%s' "$ARA_TOKEN" > "$JETON_FICHIER"
    chmod 600 "$JETON_FICHIER" 2> /dev/null
  fi
fi
export ARA_TOKEN
export ARA_HOST="${ARA_HOST:-127.0.0.1}"
export ARA_PORT="$PORT"

# --- 4. Le serveur -----------------------------------------------------------
JOURNAL="$(mktemp -t ara-XXXXXX.log)"
"$PYTHON" -m ara.cli --serve > "$JOURNAL" 2>&1 &
ARA_PID=$!

NETTOYE=0
nettoyer() {
  [ "$NETTOYE" = "1" ] && return
  NETTOYE=1
  echo
  echo "→ Arrêt d'ARA."
  kill "${TUNNEL_PID:-}" 2> /dev/null
  kill "$ARA_PID" 2> /dev/null
  wait 2> /dev/null
}
trap nettoyer EXIT INT TERM

ADRESSE="http://127.0.0.1:$PORT/?token=$ARA_TOKEN"
for _ in $(seq 1 30); do
  curl -s --noproxy '*' "http://127.0.0.1:$PORT/api/health?token=$ARA_TOKEN" \
    > /dev/null 2>&1 && break
  kill -0 "$ARA_PID" 2> /dev/null || break
  sleep 0.5
done

if ! kill -0 "$ARA_PID" 2> /dev/null; then
  echo "✕ ARA n'a pas démarré :"
  cat "$JOURNAL"
  exit 1
fi

# --- 5. Le navigateur --------------------------------------------------------
for ouvreur in xdg-open open termux-open-url; do
  command -v "$ouvreur" > /dev/null 2>&1 && "$ouvreur" "$ADRESSE" > /dev/null 2>&1 && break
done

cat <<MESSAGE

────────────────────────────────────────────────────────────────
  ARA tourne. Ouvrez :

  $ADRESSE

  Essayez, par exemple :
    · « Crée un site vitrine pour le marché couvert de Fomboni »
    · « Fais-moi un flyer pour la traversée du samedi »
    · « Quels sont les tarifs des traversées ? »
────────────────────────────────────────────────────────────────

  · Le jeton est conservé : le lien reste le même à chaque démarrage.
  · L'agent n'écoute que sur cette machine ($ARA_HOST).
  · Ctrl+C pour arrêter.

  Journal : $JOURNAL

MESSAGE

# --- 6. Le téléphone, si demandé ---------------------------------------------
if [ "$TELEPHONE" = "1" ]; then
  if command -v cloudflared > /dev/null 2>&1; then
    echo "→ Ouverture d'une adresse publique temporaire…"
    TUNNEL_LOG="$(mktemp -t cloudflared-XXXXXX.log)"
    cloudflared tunnel --no-autoupdate --url "http://127.0.0.1:$PORT" \
      > "$TUNNEL_LOG" 2>&1 &
    TUNNEL_PID=$!
    for _ in $(seq 1 40); do
      PUBLIQUE="$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$TUNNEL_LOG" | head -1)"
      [ -n "${PUBLIQUE:-}" ] && break
      kill -0 "$TUNNEL_PID" 2> /dev/null || break
      sleep 0.5
    done
    if [ -n "${PUBLIQUE:-}" ]; then
      echo
      echo "  Sur le téléphone : $PUBLIQUE/?token=$ARA_TOKEN"
      echo "  Puis « Ajouter à l'écran d'accueil ». Ce lien EST la clé."
      echo
    else
      echo "  (le tunnel ne s'est pas ouvert — voir $TUNNEL_LOG)"
    fi
  else
    echo "  Pour l'accès depuis le téléphone, installez cloudflared :"
    echo "    voir deploy/tunnel/README.md"
    echo
  fi
fi

wait "$ARA_PID"
