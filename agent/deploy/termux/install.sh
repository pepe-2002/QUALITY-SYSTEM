#!/data/data/com.termux/files/usr/bin/bash
# Installation d'ARA sur un téléphone Android, via Termux.
#
# À lancer une fois, depuis le dossier `agent/` :
#     bash deploy/termux/install.sh
#
# Le script n'installe **rien** en dehors de ce que Termux propose, ne demande
# aucune clé et ne compile aucun paquet : c'est la raison pour laquelle ARA
# n'utilise que la bibliothèque standard de Python.

set -eu

echo "→ Paquets de base"
pkg install -y python git termux-api

echo "→ Accès au stockage partagé (pour retrouver les PDF produits)"
termux-setup-storage || echo "  (refusé : les fichiers resteront dans workspace/)"

RACINE="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$RACINE"

echo "→ Vérification"
python -m ara.cli --phone || true

cat <<MESSAGE

Installation terminée.

  Lancer le serveur   : python -m ara.cli --serve
  Ouvrir l'interface  : http://127.0.0.1:8800  (Chrome → « ajouter à l'écran d'accueil »)
  Activer les routines: ARA_AUTOMATION=1 python -m ara.cli --serve

Pour que l'agent démarre tout seul au redémarrage du téléphone, installez
l'application « Termux:Boot » (F-Droid), puis :

  mkdir -p ~/.termux/boot
  cp $RACINE/deploy/termux/boot-ara.sh ~/.termux/boot/
  chmod +x ~/.termux/boot/boot-ara.sh

Rien ne tourne en arrière-plan tant que vous ne l'avez pas décidé :
ARA_AUTOMATION n'est pas activé par défaut.
MESSAGE
