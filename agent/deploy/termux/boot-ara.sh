#!/data/data/com.termux/files/usr/bin/sh
# Démarrage d'ARA au boot du téléphone (application « Termux:Boot »).
#
# Copier dans ~/.termux/boot/ et rendre exécutable. Le verrou de réveil évite
# qu'Android endorme le processus au bout de quelques minutes — sans lui, une
# routine programmée à 7 h ne se déclencherait jamais.

termux-wake-lock

# Adapter ce chemin si le dépôt est ailleurs.
RACINE="$HOME/QUALITY-SYSTEM/agent"
cd "$RACINE" || exit 1

# Les routines ne tournent que si on l'a explicitement demandé.
export ARA_AUTOMATION=1

# Hors du réseau domestique, définissez aussi un jeton :
#   export ARA_TOKEN="une-phrase-longue"

exec python -m ara.cli --serve >> "$RACINE/workspace/boot.log" 2>&1
