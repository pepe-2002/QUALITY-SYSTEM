#!/usr/bin/env python3
"""
Assemble tout le jeu dans UN seul fichier HTML autonome (kodo-en-ligne.html) :
styles, scripts, cours et polices inclus, aucune ressource extérieure.

Sert à publier Kodo là où on ne peut déposer qu'une seule page.
Le dossier complet (index.html + fichiers séparés) reste la version de
référence, avec le service worker et l'installation sur l'écran d'accueil.

    python3 construire-page-unique.py
"""
import base64
import os
import re

ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ('cours-bases.js', 'cours-tech.js', 'cours-avance.js',
           'solutions.js', 'kodo.js')


def lire(nom):
    return open(os.path.join(ICI, nom), encoding='utf-8').read()


def polices(css_utilise):
    """N'inclut que les polices réellement utilisées, en data: URI."""
    blocs = []
    for b in re.findall(r'@font-face\{[^}]*\}', lire('fonts.css')):
        famille = re.search(r"font-family:'([^']+)'", b).group(1)
        if famille not in css_utilise:
            continue
        chemin = re.search(r"url\('([^']+)'\)", b).group(1)
        with open(os.path.join(ICI, chemin), 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        blocs.append(re.sub(r"url\('[^']+'\)",
                            'url(data:font/woff2;base64,%s)' % data, b))
        print('police incluse :', chemin)
    return '\n'.join(blocs)


def construire():
    css = lire('kodo.css')

    # Le corps de la page, sans doctype/html/head/body : l'hôte les fournit.
    html = lire('index.html')
    corps = re.search(r'<body>(.*?)<script src', html, re.S).group(1)
    corps = re.sub(r'<!--.*?-->', '', corps, flags=re.S)

    js = '\n'.join(lire(f) for f in SCRIPTS)
    # Pas de service worker ici : il n'y a pas de fichier séparé à enregistrer.
    js = js.replace(
        "if ('serviceWorker' in navigator) {\n"
        "  window.addEventListener('load', () => "
        "navigator.serviceWorker.register('sw.js').catch(() => {}));\n}",
        '/* pas de service worker dans cette version en une seule page */')

    page = (
        "<title>Kodo — l'école qui se joue</title>\n"
        "<style>\n:root{color-scheme:dark}\n%s\n%s\n"
        "/* la page hôte fournit body : on lui applique le décor du jeu */\n"
        "body{background:#0B1020;color:#E8EDFA;"
        "font-family:'Manrope',system-ui,sans-serif;margin:0;min-height:100vh}\n"
        "</style>\n%s\n<script>\n%s\n</script>\n"
        % (polices(css), css, corps, js))

    chemin = os.path.join(ICI, 'kodo-en-ligne.html')
    open(chemin, 'w', encoding='utf-8').write(page)
    print('→ kodo-en-ligne.html :', round(len(page.encode()) / 1024), 'Ko')


if __name__ == '__main__':
    construire()
