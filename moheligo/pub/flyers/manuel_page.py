#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique les versions LISIBLES des documents, à partir des documents eux-mêmes.

    python3 manuel_page.py --sortie /tmp/manuel.html            # le manuel seul
    python3 manuel_page.py --dossier --sortie /tmp/dossier.html  # TOUT le dossier
    python3 manuel_page.py --source ../../dossier/FEUILLE-DE-ROUTE.md ...

Le patron a demandé « une copie pour que je puisse lire aussi ». Elle est
GÉNÉRÉE, jamais recopiée à la main : `moheligo/dossier/MANUEL-MARKETING.md` reste la
seule source de vérité. Si on recopiait, les deux versions divergeraient au
premier ajout — et je finirais par relire une version périmée avant une pub.

Pas de bibliothèque externe : un petit convertisseur Markdown → HTML qui gère
exactement ce que le manuel utilise (titres, tableaux, listes, citations, code,
gras, italique, cases à cocher). Rien de plus, pour ne rien casser en silence.
"""

import argparse
import html
import pathlib
import re
import unicodedata

DOSSIER = pathlib.Path(__file__).resolve().parents[2] / 'dossier'
MANUEL = DOSSIER / 'MANUEL-MARKETING.md'

# L'ordre de lecture du dossier, celui qu'annonce dossier/README.md. L'index
# vient en premier : c'est lui qui dit quoi lire avant quoi.
ORDRE = ['README.md', 'MEMOIRE.md', 'MANUEL-MARKETING.md', 'FEUILLE-DE-ROUTE.md',
         'PRESENTATION.md', 'PLAN-PUBLICITAIRE.md', 'TEXTES-PUBLICATIONS.md',
         'LIER-FACEBOOK.md', 'VIDEO-DEMONSTRATION.md', 'ATELIER-FLYERS.md']

MARINE = '#0F2A5C'
OR = '#F6BC1C'


def ancre(texte):
    """Identifiant d'ancre stable pour le sommaire (sans accent ni ponctuation)."""
    plat = unicodedata.normalize('NFKD', texte).encode('ascii', 'ignore').decode()
    return 's-' + re.sub(r'[^a-z0-9]+', '-', plat.lower()).strip('-')


def enligne(texte):
    """Le balisage à l'intérieur d'une ligne. L'ordre compte : le code d'abord,
    sinon un `*` dans du code serait pris pour de l'italique."""
    morceaux = []

    def garder(m):
        morceaux.append(m.group(1))
        return '\x00%d\x00' % (len(morceaux) - 1)

    texte = re.sub(r'`([^`]+)`', garder, texte)
    texte = html.escape(texte)
    texte = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', texte)
    texte = re.sub(r'(?<![\w*])\*([^*]+)\*(?![\w*])', r'<em>\1</em>', texte)
    # les adresses nues du manuel : cliquables, mais sans inventer de protocole
    texte = re.sub(r'(?<![\w/@.])((?:www\.|[a-z0-9-]+\.(?:com|org|vc))[^\s,;)]*)',
                   r'<a href="https://\1">\1</a>', texte)
    return re.sub(r'\x00(\d+)\x00',
                  lambda m: '<code>%s</code>' % html.escape(morceaux[int(m.group(1))]),
                  texte)


def cellules(ligne):
    return [c.strip() for c in ligne.strip().strip('|').split('|')]


def convertir(md):
    """Markdown → HTML. Renvoie (corps, sommaire)."""
    lignes = md.split('\n')
    out, sommaire = [], []
    i = 0
    liste = None            # 'ul' ou 'ol' en cours, sinon None

    def fermer_liste():
        nonlocal liste
        if liste:
            out.append('</%s>' % liste)
            liste = None

    while i < len(lignes):
        ligne = lignes[i]
        nu = ligne.strip()

        if not nu:
            fermer_liste()
            i += 1
            continue

        # ----- tableau : une ligne de | suivie d'une ligne de tirets -----
        if (nu.startswith('|') and i + 1 < len(lignes)
                and re.match(r'^\|[\s:|-]+\|$', lignes[i + 1].strip())):
            fermer_liste()
            entete = cellules(nu)
            i += 2
            corps = []
            while i < len(lignes) and lignes[i].strip().startswith('|'):
                corps.append(cellules(lignes[i].strip()))
                i += 1
            out.append('<div class="tableau"><table><thead><tr>'
                       + ''.join('<th>%s</th>' % enligne(c) for c in entete)
                       + '</tr></thead><tbody>')
            for r in corps:
                out.append('<tr>' + ''.join('<td>%s</td>' % enligne(c) for c in r) + '</tr>')
            out.append('</tbody></table></div>')
            continue

        # ----- bloc de code -----
        if nu.startswith('```'):
            fermer_liste()
            i += 1
            bloc = []
            while i < len(lignes) and not lignes[i].strip().startswith('```'):
                bloc.append(lignes[i])
                i += 1
            i += 1
            out.append('<pre>%s</pre>' % html.escape('\n'.join(bloc)))
            continue

        # ----- citation (le bandeau de consigne, en tête) -----
        if nu.startswith('>'):
            fermer_liste()
            bloc = []
            while i < len(lignes) and lignes[i].strip().startswith('>'):
                bloc.append(lignes[i].strip()[1:].strip())
                i += 1
            interne, _ = convertir('\n'.join(bloc))
            out.append('<blockquote>%s</blockquote>' % interne)
            continue

        # ----- trait de séparation -----
        if re.match(r'^-{3,}$', nu):
            fermer_liste()
            out.append('<hr>')
            i += 1
            continue

        # ----- titres -----
        m = re.match(r'^(#{1,4})\s+(.*)$', nu)
        if m:
            fermer_liste()
            n, titre = len(m.group(1)), m.group(2)
            a = ancre(titre)
            out.append('<h%d id="%s">%s</h%d>' % (n, a, enligne(titre), n))
            if n <= 2:
                sommaire.append((n, titre, a))
            i += 1
            continue

        # ----- listes (dont les cases à cocher des checklists) -----
        m = re.match(r'^([-*])\s+(.*)$', nu)
        if m:
            if liste != 'ul':
                fermer_liste()
                out.append('<ul>')
                liste = 'ul'
            contenu = m.group(2)
            case = re.match(r'^\[[ xX]\]\s*(.*)$', contenu)
            if case:
                out.append('<li class="case">%s</li>' % enligne(case.group(1)))
            else:
                out.append('<li>%s</li>' % enligne(contenu))
            i += 1
            continue

        m = re.match(r'^(\d+)[.)]\s+(.*)$', nu)
        if m:
            if liste != 'ol':
                fermer_liste()
                out.append('<ol>')
                liste = 'ol'
            out.append('<li>%s</li>' % enligne(m.group(2)))
            i += 1
            continue

        # ----- paragraphe : on recolle les lignes coupées à 80 colonnes -----
        fermer_liste()
        bloc = [nu]
        i += 1
        while i < len(lignes):
            s = lignes[i].strip()
            if (not s or s.startswith(('#', '>', '|', '-', '*', '`'))
                    or re.match(r'^\d+[.)]\s', s)):
                break
            bloc.append(s)
            i += 1
        out.append('<p>%s</p>' % enligne(' '.join(bloc)))

    fermer_liste()
    return '\n'.join(out), sommaire


GABARIT = '''<title>{titre_page}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
/* Palette claire complète sur :root nu — le sombre ne redéfinit que les jetons.
   --bandeau est distinct de --marine : en sombre, le marine s'éclaircit pour
   rester lisible sur fond noir, alors que le bandeau doit rester profond. */
:root {{
  --marine:{marine}; --or:{oren}; --encre:#12203A; --encre2:#4A5D7C;
  --fond:#F7F9FD; --carte:#FFFFFF; --filet:#DCE5F2; --surlignage:#FFF8E4;
  --bandeau:{marine};
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --marine:#8FB6F0; --encre:#E6EDF9; --encre2:#9FB2CE;
    --fond:#0A1526; --carte:#101E36; --filet:#25375A; --surlignage:#2A2410;
    --bandeau:#0B1B34;
  }}
}}
:root[data-theme="dark"] {{
  --marine:#8FB6F0; --encre:#E6EDF9; --encre2:#9FB2CE;
  --fond:#0A1526; --carte:#101E36; --filet:#25375A; --surlignage:#2A2410;
  --bandeau:#0B1B34;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--fond); color:var(--encre);
  font:16.5px/1.62 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  -webkit-text-size-adjust:100%; }}

.bandeau {{ background:var(--bandeau); color:#fff; padding:30px 22px 26px; }}
.bandeau .dedans {{ max-width:820px; margin:0 auto; }}
.bandeau h1 {{ margin:0; font-size:26px; line-height:1.2; letter-spacing:-.5px; }}
.bandeau h1 i {{ color:var(--or); font-style:normal; }}
.bandeau p {{ margin:12px 0 0; font-size:14.5px; color:rgba(255,255,255,.82); }}
.bandeau .quand {{ margin-top:16px; font-size:11.5px; font-weight:700;
  letter-spacing:2px; color:rgba(255,255,255,.6); }}

.enveloppe {{ max-width:820px; margin:0 auto; padding:0 18px 90px; }}

nav.sommaire {{ background:var(--carte); border:1px solid var(--filet);
  border-radius:14px; padding:18px 20px; margin:22px 0 30px; }}
nav.sommaire b {{ display:block; font-size:11.5px; letter-spacing:2px;
  color:var(--encre2); margin-bottom:12px; }}
nav.sommaire a {{ display:block; padding:5px 0; color:var(--encre);
  text-decoration:none; border-bottom:1px solid transparent; font-size:15px; }}
nav.sommaire a:hover {{ border-bottom-color:var(--or); }}
nav.sommaire a.n1 {{ font-weight:800; margin-top:12px; color:var(--marine); }}
nav.sommaire a.n1:first-child {{ margin-top:0; }}

h1, h2, h3, h4 {{ line-height:1.24; letter-spacing:-.3px; scroll-margin-top:14px; }}
h1 {{ font-size:25px; margin:44px 0 14px; padding-bottom:12px;
  border-bottom:3px solid var(--or); }}
h2 {{ font-size:21px; margin:40px 0 12px; color:var(--marine); }}
h3 {{ font-size:17.5px; margin:28px 0 10px; }}
h4 {{ font-size:15.5px; margin:22px 0 8px; color:var(--encre2); }}
p {{ margin:0 0 14px; }}
strong {{ font-weight:700; }}
a {{ color:var(--marine); }}
hr {{ border:0; border-top:1px solid var(--filet); margin:34px 0; }}

ul, ol {{ margin:0 0 16px; padding-left:24px; }}
li {{ margin-bottom:7px; }}
li.case {{ list-style:none; position:relative; padding-left:30px; margin-left:-24px; }}
li.case::before {{ content:''; position:absolute; left:0; top:4px; width:17px;
  height:17px; border:2px solid var(--marine); border-radius:4px; }}

blockquote {{ margin:0 0 22px; padding:16px 20px; background:var(--surlignage);
  border-left:4px solid var(--or); border-radius:0 10px 10px 0; font-size:15px; }}
blockquote p:last-child {{ margin-bottom:0; }}

code {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.88em;
  background:var(--surlignage); padding:1px 5px; border-radius:4px; }}
pre {{ background:var(--carte); border:1px solid var(--filet); border-radius:10px;
  padding:15px; overflow-x:auto; font-size:13.5px; line-height:1.55; }}

.tableau {{ overflow-x:auto; margin:0 0 22px; border:1px solid var(--filet);
  border-radius:12px; background:var(--carte); }}
table {{ border-collapse:collapse; width:100%; font-size:14.5px; }}
th, td {{ text-align:left; padding:11px 13px; border-bottom:1px solid var(--filet);
  vertical-align:top; }}
th {{ background:var(--surlignage); font-size:12px; letter-spacing:.6px;
  text-transform:uppercase; color:var(--encre2); white-space:nowrap; }}
tr:last-child td {{ border-bottom:0; }}

.pied {{ max-width:820px; margin:0 auto; padding:26px 18px 60px;
  border-top:1px solid var(--filet); color:var(--encre2); font-size:13px; }}
</style>

<div class="bandeau"><div class="dedans">
  <h1>{titre_h1}</h1>
  <p>{chapeau}</p>
  <div class="quand">VERSION DU {quand} · {mots} MOTS · SOURCE : moheligo/{source}</div>
</div></div>

<div class="enveloppe">
<nav class="sommaire"><b>SOMMAIRE</b>
{sommaire}
</nav>
{corps}
</div>

<div class="pied">Généré depuis <code>moheligo/{source}</code> par
<code>pub/flyers/manuel_page.py</code>. Ne jamais corriger cette page à la main :
corriger le manuel, puis regénérer.</div>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sortie', default='manuel.html')
    ap.add_argument('--source', default=str(MANUEL))
    # Le même gabarit sert à plusieurs documents (manuel, feuille de route) :
    # sans ces trois options, la feuille de route sortait sous le titre du
    # manuel — un document qui se présente sous un faux nom, personne ne le lit.
    ap.add_argument('--titre', default='📕 Manuel Moheli<i>Go</i> — marketing, direction, adoption')
    ap.add_argument('--chapeau', default='La grille de décision du directeur marketing. '
                    'À relire avant chaque flyer, chaque texte, chaque rapport, chaque plan.')
    ap.add_argument('--onglet', default='Manuel MoheliGo — marketing, direction, adoption')
    ap.add_argument('--dossier', action='store_true',
                    help='assembler tout le dossier en une seule page')
    args = ap.parse_args()

    if args.dossier:
        # Un document manquant doit être VISIBLE dans la page, pas ignoré : un
        # trou silencieux dans le dossier, c'est un document qu'on croit avoir.
        morceaux = []
        for nom in ORDRE:
            f = DOSSIER / nom
            if f.is_file():
                morceaux.append(f.read_text(encoding='utf-8').rstrip())
            else:
                morceaux.append('# ⚠️ %s — INTROUVABLE\n\nCe document est annoncé '
                                'dans l\'ordre de lecture mais absent du dossier.' % nom)
        md = '\n\n---\n\n'.join(morceaux)
        args.source = str(DOSSIER)
        if args.onglet == ap.get_default('onglet'):
            args.onglet = 'Le dossier MoheliGo'
            args.titre = '📁 Le dossier Moheli<i>Go</i>'
            args.chapeau = ('Tout ce qui gouverne le travail du directeur : mémoire, '
                            'manuel, feuille de route, plan publicitaire, textes et '
                            'modes d\'emploi. Assemblé depuis les documents eux-mêmes.')
    else:
        md = pathlib.Path(args.source).read_text(encoding='utf-8')
    corps, sommaire = convertir(md)

    liens = '\n'.join(
        '<a class="n%d" href="#%s">%s</a>' % (n, a, html.escape(t))
        for n, t, a in sommaire if n <= 2)

    quand = __import__('datetime').date.today().strftime('%d/%m/%Y')
    page = GABARIT.format(marine=MARINE, oren=OR, corps=corps, sommaire=liens,
                          quand=quand, mots=len(md.split()),
                          titre_page=html.escape(args.onglet), titre_h1=args.titre,
                          chapeau=args.chapeau,
                          source=html.escape(
                              'dossier/' if args.dossier
                              else pathlib.Path(args.source).name))
    pathlib.Path(args.sortie).write_text(page, encoding='utf-8')
    print(args.sortie, round(len(page) / 1024), 'ko —',
          len(sommaire), 'entrées de sommaire,', len(md.split()), 'mots')


if __name__ == '__main__':
    main()
