#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fabrique le dossier PDF du TOUR DE MORONI, prêt à envoyer à un partenaire.

Assemble la couverture, les quatre documents du dossier et la carte du parcours
en un seul fichier :

    python3 fabriquer_dossier_pdf.py        # écrit Dossier-Tour-de-Moroni.pdf

`MEMOIRE.md` n'y est volontairement pas : c'est le journal interne du projet
(décisions en attente, contacts, ce qui reste à trancher). Il ne sort pas.

Comment ça marche : les fichiers Markdown du dossier sont convertis en une page
HTML unique mise en page pour l'impression (A4, plus une page en paysage pour la
carte), puis Chromium l'imprime en PDF. Pas de bibliothèque à installer — juste
un Chromium sur la machine. Si le binaire n'est pas trouvé automatiquement :

    CHROME=/chemin/vers/chrome python3 fabriquer_dossier_pdf.py

Sortie intermédiaire : dossier.html, gardé à côté du PDF — pratique pour
vérifier la mise en page dans un navigateur avant d'imprimer.
"""

import html as html_mod
import json
import math
import os
import re
import shutil
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER = os.path.join(ICI, "dossier")
CARTE = os.path.join(ICI, "carte", "carte-tour-de-moroni.svg")
HTML = os.path.join(ICI, "dossier.html")
PDF = os.path.join(ICI, "Dossier-Tour-de-Moroni.pdf")

# Les documents retenus, dans l'ordre de lecture d'un partenaire.
CHAPITRES = [
    ("PROJET.md", "Le projet"),
    ("PARCOURS.md", "Le parcours"),
    ("BUDGET.md", "Le budget"),
    ("PARTENAIRES.md", "Les partenariats"),
]

# Dans le PDF, les renvois d'un fichier à l'autre n'ont plus de sens : on les
# remplace par des renvois de chapitre à chapitre.
RENVOIS = {
    "`PROJET.md`": "le chapitre 1",
    "`PARCOURS.md`": "le chapitre 2",
    "`BUDGET.md`": "le chapitre 3",
    "`PARTENAIRES.md`": "le chapitre 4",
    "`MEMOIRE.md`": "le journal interne du projet",
    "`../carte/carte-tour-de-moroni.svg`": "la carte en fin de dossier",
    "`../carte/parcours.geojson`": "le fichier GeoJSON du parcours",
    "`../carte/donnees/points_blocage.csv`": "la liste des points de blocage",
    "`../carte/calculer_parcours.py`": "le programme de calcul du parcours",
    "`../carte/`": "les fichiers techniques du projet",
}


CHROMES = [
    os.environ.get("CHROME"),
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    shutil.which("chromium"), shutil.which("chromium-browser"),
    shutil.which("google-chrome"), shutil.which("chrome"),
]


# --- Markdown → HTML ---------------------------------------------------------
# Volontairement minimal : il ne gère que ce que nos documents utilisent
# (titres, tableaux, listes, citations, gras, italique, code, liens, filets).

def en_ligne(t):
    t = html_mod.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t


def cellules(ligne):
    ligne = ligne.strip()
    if ligne.startswith("|"):
        ligne = ligne[1:]
    if ligne.endswith("|"):
        ligne = ligne[:-1]
    return [c.strip() for c in ligne.split("|")]


def alignements(ligne):
    out = []
    for c in cellules(ligne):
        if c.endswith(":") and c.startswith(":"):
            out.append("center")
        elif c.endswith(":"):
            out.append("right")
        else:
            out.append("left")
    return out


def convertir(md):
    lignes = md.split("\n")
    sortie, i = [], 0
    pile_liste = []                       # ('ul'|'ol') en cours

    def fermer_listes(jusqu_a=0):
        while len(pile_liste) > jusqu_a:
            sortie.append(f"</{pile_liste.pop()}>")

    while i < len(lignes):
        ligne = lignes[i]
        nu = ligne.strip()

        if not nu:
            fermer_listes()
            i += 1
            continue

        if nu.startswith("```"):          # bloc de code
            fermer_listes()
            i += 1
            bloc = []
            while i < len(lignes) and not lignes[i].strip().startswith("```"):
                bloc.append(html_mod.escape(lignes[i]))
                i += 1
            sortie.append("<pre><code>" + "\n".join(bloc) + "</code></pre>")
            i += 1
            continue

        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", nu):
            fermer_listes()
            sortie.append('<hr>')
            i += 1
            continue

        m = re.match(r"(#{1,6})\s+(.*)", nu)
        if m:
            fermer_listes()
            n = len(m.group(1))
            sortie.append(f"<h{n}>{en_ligne(m.group(2))}</h{n}>")
            i += 1
            continue

        if nu.startswith(">"):            # citation, éventuellement multi-lignes
            fermer_listes()
            bloc = []
            while i < len(lignes) and lignes[i].strip().startswith(">"):
                bloc.append(re.sub(r"^\s*>\s?", "", lignes[i]))
                i += 1
            sortie.append("<blockquote>" + convertir("\n".join(bloc)) + "</blockquote>")
            continue

        if nu.startswith("|") and i + 1 < len(lignes) and \
                re.fullmatch(r"\|[\s:|-]+\|?", lignes[i + 1].strip()):
            fermer_listes()
            entetes = cellules(nu)
            aligns = alignements(lignes[i + 1])
            i += 2
            corps = []
            while i < len(lignes) and lignes[i].strip().startswith("|"):
                corps.append(cellules(lignes[i]))
                i += 1
            vide = not any(c.strip() for c in entetes)
            t = ["<table>"]
            if not vide:
                t.append("<thead><tr>")
                for c, a in zip(entetes, aligns):
                    t.append(f'<th class="a-{a}">{en_ligne(c)}</th>')
                t.append("</tr></thead>")
            t.append("<tbody>")
            for r in corps:
                t.append("<tr>")
                for j, c in enumerate(r):
                    a = aligns[j] if j < len(aligns) else "left"
                    t.append(f'<td class="a-{a}">{en_ligne(c)}</td>')
                t.append("</tr>")
            t.append("</tbody></table>")
            sortie.append("".join(t))
            continue

        m = re.match(r"(\s*)([-*+]|\d+\.)\s+(.*)", ligne)
        if m:
            indent, puce, texte = m.group(1), m.group(2), m.group(3)
            genre = "ul" if puce in "-*+" else "ol"
            niveau = 1 + len(indent) // 3
            if niveau > len(pile_liste):
                sortie.append(f"<{genre}>")
                pile_liste.append(genre)
            elif niveau < len(pile_liste):
                fermer_listes(niveau)
            i += 1
            suite = [texte]
            while i < len(lignes) and lignes[i].strip() and \
                    not re.match(r"\s*([-*+]|\d+\.)\s+|\s*[|#>]|```", lignes[i]):
                suite.append(lignes[i].strip())
                i += 1
            sortie.append(f"<li>{en_ligne(' '.join(suite))}</li>")
            continue

        fermer_listes()                    # paragraphe
        para = [nu]
        i += 1
        while i < len(lignes) and lignes[i].strip() and \
                not re.match(r"\s*([-*+#>|]|\d+\.)\s|```", lignes[i]):
            para.append(lignes[i].strip())
            i += 1
        sortie.append(f"<p>{en_ligne(' '.join(para))}</p>")

    fermer_listes()
    return "\n".join(sortie)


# --- Assemblage --------------------------------------------------------------
def carte_en_ligne():
    """La carte SVG, insérée telle quelle et mise à la largeur de la page."""
    if not os.path.exists(CARTE):
        return '<p><em>Carte absente : lancer carte/carte.py.</em></p>'
    with open(CARTE, encoding="utf-8") as f:
        svg = f.read()
    svg = svg.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
    svg = re.sub(r'<svg([^>]*?)width="[^"]*"\s+height="[^"]*"',
                 r'<svg\1preserveAspectRatio="xMidYMid meet"', svg, count=1)
    return svg


def glyphe_parcours(hauteur=400, marge=14):
    """Le parcours réduit à son trait : la signature visuelle du Tour.
    Le cadre épouse la forme du parcours — pas de blanc autour."""
    chemin = os.path.join(ICI, "carte", "donnees", "parcours_calcule.json")
    if not os.path.exists(chemin):
        return ""
    with open(chemin, encoding="utf-8") as f:
        p = json.load(f)
    pts = p["sud"] + p["nord"]
    k = math.cos(math.radians(sum(c[1] for c in pts) / len(pts)))
    xs = [c[0] * k for c in pts]
    ys = [-c[1] for c in pts]
    ech = (hauteur - 2 * marge) / (max(ys) - min(ys))
    largeur = (max(xs) - min(xs)) * ech + 2 * marge

    def trace(coords):
        return " ".join(f"{marge + (c[0] * k - min(xs)) * ech:.1f},"
                        f"{marge + (-c[1] - min(ys)) * ech:.1f}" for c in coords)

    depart = p["sud"][0]
    dx = marge + (depart[0] * k - min(xs)) * ech
    dy = marge + (-depart[1] - min(ys)) * ech
    return (f'<svg viewBox="0 0 {largeur:.0f} {hauteur}" '
            f'xmlns="http://www.w3.org/2000/svg">'
            f'<polyline points="{trace(p["sud"])}" fill="none" stroke="#d9481f" '
            f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<polyline points="{trace(p["nord"])}" fill="none" stroke="#14607f" '
            f'stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="10" fill="#2f2b27"/>'
            f'<circle cx="{dx:.1f}" cy="{dy:.1f}" r="16" fill="none" stroke="#2f2b27" '
            f'stroke-width="2.4"/></svg>')


STYLE = """
@page { size: A4 portrait; margin: 18mm 16mm 16mm 16mm; }
@page paysage { size: A4 landscape; margin: 10mm; }
@page couverture { margin: 0; }

* { box-sizing: border-box; }
body { font-family: "Bitstream Charter", "Liberation Serif", Georgia, serif;
       font-size: 10.2pt; line-height: 1.45; color: #23201d; margin: 0; }
h1, h2, h3, h4, th { font-family: "Liberation Sans", Arial, sans-serif; }

h1 { font-size: 19pt; margin: 0 0 4mm 0; color: #9c3412; letter-spacing: -0.2pt; }
h2 { font-size: 13pt; margin: 7mm 0 2.5mm 0; padding-bottom: 1.2mm;
     border-bottom: 1.6pt solid #d9481f; break-after: avoid; }
h3 { font-size: 11pt; margin: 5mm 0 2mm 0; color: #14607f; break-after: avoid; }
h4 { font-size: 10pt; margin: 4mm 0 1.5mm 0; }
p { margin: 0 0 2.4mm 0; text-align: justify; }
hr { border: 0; border-top: 0.6pt solid #d8d2c7; margin: 5mm 0; }
a { color: #14607f; text-decoration: none; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.6pt;
       background: #f3efe8; padding: 0 0.6mm; border-radius: 1pt; }
pre { background: #f6f3ed; border-left: 2.4pt solid #d8d2c7; padding: 2.5mm 3mm;
      font-size: 8.6pt; overflow: hidden; break-inside: avoid; }
pre code { background: none; }

ul, ol { margin: 0 0 2.4mm 0; padding-left: 5mm; }
li { margin-bottom: 1.2mm; text-align: justify; }

blockquote { margin: 3mm 0; padding: 2.5mm 3.5mm; background: #fbf7f0;
             border-left: 2.4pt solid #d9481f; break-inside: avoid; }
blockquote p:last-child { margin-bottom: 0; }

table { width: 100%; border-collapse: collapse; margin: 2.5mm 0 4mm 0;
        font-family: "Liberation Sans", Arial, sans-serif; font-size: 8.4pt;
        break-inside: auto; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { background: #2f2b27; color: #fff; text-align: left; font-weight: 600;
     padding: 1.6mm 2mm; line-height: 1.25; }
td { border-bottom: 0.5pt solid #e2ddd3; padding: 1.5mm 2mm;
     vertical-align: top; line-height: 1.3; }
tbody tr:nth-child(even) td { background: #faf8f4; }
.a-right { text-align: right; } .a-center { text-align: center; }

/* Couverture */
.couverture { page: couverture; break-after: page; height: 297mm; width: 210mm;
              position: relative; color: #23201d; overflow: hidden; }
.couv-bande { position: absolute; top: 0; left: 0; right: 0; height: 84mm;
              background: #d9481f; }
.couv-haut { position: absolute; top: 18mm; left: 20mm; right: 20mm; color: #fff; }
.couv-surtitre { font-family: "Liberation Sans", sans-serif; font-size: 10pt;
                 letter-spacing: 2.6pt; text-transform: uppercase; opacity: .9; }
.couv-titre { font-family: "Liberation Sans", sans-serif; font-weight: 700;
              font-size: 42pt; line-height: 1.02; margin-top: 6mm;
              letter-spacing: -0.8pt; }
.couv-signature { font-size: 13pt; font-style: italic; margin-top: 4mm; }
.couv-corps { position: absolute; top: 94mm; left: 20mm; right: 20mm; }
.couv-phrase { font-size: 12.5pt; line-height: 1.5; text-align: justify; }
.couv-chiffres { display: flex; gap: 6mm; margin-top: 10mm; }
.chiffre { flex: 1; border-top: 2pt solid #d9481f; padding-top: 2.5mm; }
.chiffre .n { font-family: "Liberation Sans", sans-serif; font-size: 20pt;
              font-weight: 700; color: #9c3412; display: block; line-height: 1.1; }
.chiffre .l { font-size: 8.6pt; color: #6c645a; }
.couv-glyphe { position: absolute; bottom: 36mm; left: 20mm; right: 20mm;
               display: flex; align-items: center; gap: 12mm; }
.couv-glyphe svg { height: 82mm; width: auto; flex: none; }
.couv-glyphe .texte { font-family: "Liberation Sans", sans-serif; font-size: 8.8pt;
                      color: #6c645a; line-height: 1.6; }
.couv-glyphe .texte b { color: #23201d; display: block; font-size: 9.4pt;
                        margin-bottom: 1.5mm; }
.couv-date { position: absolute; bottom: 22mm; left: 20mm; right: 20mm;
             border-top: 0.8pt solid #d8d2c7; padding-top: 3mm;
             font-family: "Liberation Sans", sans-serif; font-size: 9pt;
             color: #6c645a; display: flex; justify-content: space-between; }

/* Sommaire et séparateurs de chapitre */
.sommaire { break-after: page; }
.sommaire ol { list-style: none; padding: 0; }
.sommaire li { border-bottom: 0.5pt solid #e2ddd3; padding: 2.5mm 0;
               font-family: "Liberation Sans", sans-serif; font-size: 10.5pt; }
.sommaire .num { color: #d9481f; font-weight: 700; margin-right: 3mm; }
.sommaire .quoi { color: #6c645a; font-size: 9pt; display: block; margin-top: 1mm;
                  font-family: "Bitstream Charter", serif; }
.chapitre { break-before: page; }
.chapitre > h1:first-child { border-bottom: 2.4pt solid #d9481f; padding-bottom: 2mm; }

/* Page carte, en paysage */
.page-carte { page: paysage; break-before: page; break-inside: avoid;
              height: 190mm; display: flex; align-items: center;
              justify-content: center; }
.page-carte svg { width: 100%; height: 100%; }

.pied { margin-top: 8mm; border-top: 0.6pt solid #d8d2c7; padding-top: 2.5mm;
        font-size: 8pt; color: #8c857b; font-family: "Liberation Sans", sans-serif; }
"""


def construire_html():
    corps = []

    corps.append(("""
<div class="couverture">
  <div class="couv-bande"></div>
  <div class="couv-haut">
    <div class="couv-surtitre">Dossier de partenariat · Moroni, Union des Comores</div>
    <div class="couv-titre">TOUR DE<br>MORONI</div>
    <div class="couv-signature">Toute la ville, au même pas</div>
  </div>
  <div class="couv-corps">
    <p class="couv-phrase">Un dimanche matin par an, Moroni ferme ses grands axes
    et la capitale court dix kilomètres. Coureurs, familles, fauteuils, joëlettes,
    personnes déficientes visuelles&nbsp;: même départ, même parcours, même arche
    d'arrivée. Ce n'est pas une course où les personnes handicapées ont une épreuve
    à part — c'est une course où tout le monde prend le même départ.</p>
    <div class="couv-chiffres">
      <div class="chiffre"><span class="n">10,02 km</span><span class="l">un huit autour de la place de l'Indépendance</span></div>
      <div class="chiffre"><span class="n">6 déc. 2026</span><span class="l">1<sup>re</sup> édition, puis chaque 1<sup>er</sup> dimanche de décembre</span></div>
      <div class="chiffre"><span class="n">800</span><span class="l">participants visés, dont 40 en situation de handicap</span></div>
      <div class="chiffre"><span class="n">17,3 M</span><span class="l">KMF de budget, dont 13,5 M à financer</span></div>
    </div>
  </div>
  <div class="couv-glyphe">
    {GLYPHE}
    <div class="texte">
      <b>Le parcours, en un trait</b>
      Boucle Sud 6,05 km, en rouge&nbsp;: front de mer, Palais du Peuple, Karthala.<br>
      Boucle Nord 3,98 km, en bleu&nbsp;: Hankunu, Union Africaine, Corniche.<br>
      Les deux se referment sur la place de l'Indépendance&nbsp;— un seul village,
      et le public voit les coureurs trois fois.
    </div>
  </div>
  <div class="couv-date">
    <span>Dossier établi le 19 septembre 2026 — version 1</span>
    <span>Départ&nbsp;: place de l'Indépendance, 6&nbsp;h&nbsp;30</span>
  </div>
</div>""").replace("{GLYPHE}", glyphe_parcours()))

    corps.append("""
<div class="sommaire">
  <h1>Ce que contient ce dossier</h1>
  <ol>
    <li><span class="num">1</span>Le projet
      <span class="quoi">L'idée, la date et pourquoi elle, les quatre formats de course, les sept engagements d'inclusion, l'organisation, le calendrier, les dix indicateurs, les risques et la pérennité.</span></li>
    <li><span class="num">2</span>Le parcours
      <span class="quoi">Le tracé au mètre près, la feuille de route rue par rue, les ravitaillements, les postes de secours, les stands, le plan de fermeture de la ville, l'accessibilité et le règlement sportif.</span></li>
    <li><span class="num">3</span>Le budget
      <span class="quoi">Les deux formats chiffrés, le détail poste par poste, les recettes, la trésorerie, les lignes sensibles, les points d'arrêt et la trajectoire sur trois éditions.</span></li>
    <li><span class="num">4</span>Les partenariats
      <span class="quoi">Sponsoring, mécénat, subvention : les niveaux et leurs contreparties, à qui l'on s'adresse, le pitch, le courrier de premier contact et le rapport rendu après la course.</span></li>
    <li><span class="num">5</span>La carte du parcours
      <span class="quoi">Le huit de 10,02 km, les trois ravitaillements, les postes de secours, le relais joëlettes et le profil altimétrique.</span></li>
  </ol>
  <p class="pied">Le journal interne du projet (décisions en attente, contacts,
  arbitrages à rendre) n'est pas joint : il reste dans le dossier de travail.</p>
</div>""")

    for i, (fichier, titre) in enumerate(CHAPITRES, start=1):
        with open(os.path.join(DOSSIER, fichier), encoding="utf-8") as f:
            md = f.read()
        for quoi, par in RENVOIS.items():
            md = md.replace(quoi, par)
        corps.append(f'<div class="chapitre">\n{convertir(md)}\n</div>')

    corps.append(f"""
<div class="page-carte">
  {carte_en_ligne()}
</div>""")

    return (f'<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8">'
            f'<title>Dossier Tour de Moroni</title><style>{STYLE}</style></head>'
            f'<body>{"".join(corps)}</body></html>')


def imprimer(chemin_html, chemin_pdf):
    chrome = next((c for c in CHROMES if c and os.path.exists(c)), None)
    if not chrome:
        print("Chromium introuvable. Le HTML est prêt : ouvrez-le et imprimez en PDF,")
        print(f"ou relancez avec CHROME=/chemin/vers/chrome.\n  {chemin_html}")
        return False
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=10000",
                    f"--print-to-pdf={chemin_pdf}", f"file://{chemin_html}"],
                   check=True, capture_output=True)
    return True


if __name__ == "__main__":
    with open(HTML, "w", encoding="utf-8") as f:
        f.write(construire_html())
    print(f"écrit : {os.path.basename(HTML)}")
    if imprimer(HTML, PDF):
        taille = os.path.getsize(PDF) / 1024
        print(f"écrit : {os.path.basename(PDF)} ({taille:.0f} Ko)")
    else:
        sys.exit(1)
