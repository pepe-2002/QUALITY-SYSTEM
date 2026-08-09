#!/usr/bin/env python3
"""Assemble GÉOPOLIS en un seul fichier HTML autonome.

Le jeu est développé en modules (data, moteur, événements, carte, interface)
parce que c'est ainsi qu'il se lit et se corrige. Mais pour être publié en
Artifact ou envoyé par message, il doit tenir dans un fichier unique, sans
aucune requête réseau. Ce script fait la couture.

    python3 construire-fichier-unique.py [sortie.html]
"""
import re
import sys
from pathlib import Path

RACINE = Path(__file__).parent
SORTIE = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / 'geopolis-un-fichier.html'

html = (RACINE / 'index.html').read_text(encoding='utf-8')
css = (RACINE / 'geopolis.css').read_text(encoding='utf-8')

scripts = re.findall(r'<script src="([^"]+)"></script>', html)
js = []
for nom in scripts:
    code = (RACINE / nom).read_text(encoding='utf-8')
    if nom == 'g-accueil.js':
        # Pas de service worker dans un fichier unique : il n'y a rien à mettre
        # en cache, et l'enregistrement échouerait bruyamment hors serveur.
        code = re.sub(
            r"  // Service worker.*?\n  \}\n", "", code, flags=re.S)
    js.append(f'/* ═══ {nom} ═══ */\n{code}')

corps = html[html.index('<body>') + 6:html.index('<script src=')]
corps = corps.strip()

sortie = f"""<meta charset="utf-8">
<title>GÉOPOLIS — Simulateur de Président</title>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>
{css}
</style>

{corps}

<script>
{chr(10).join(js)}
</script>
"""

SORTIE.write_text(sortie, encoding='utf-8')
print(f'{SORTIE} — {len(sortie) / 1024:.0f} Ko, {len(scripts)} modules assemblés')
