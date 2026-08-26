#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LES CARTES DES FILMS D'IDENTITÉ — fabriquées dans le langage exact des flyers.

Le patron, 26/08/2026 : « les photos ne sont pas assez neutres, crée des flyers
à nous pour les vidéos », et « bien sûr tu vas mettre le logo et utiliser notre
identité ».

📌 POURQUOI DES CARTES ET PLUS DES PHOTOS. Une photo, même bien étalonnée, reste
la photo de quelqu'un : elle tire l'œil vers son sujet, pas vers la marque. Une
carte dessinée, elle, **n'appartient qu'à nous** — c'est exactement ce qui rend
une publication reconnaissable dans un fil. Les films deviennent donc nos flyers
en mouvement, avec la même grille, les mêmes couleurs, la même typographie.

CE QUI EST REPRIS DES FLYERS, À L'IDENTIQUE :
  · le fond marine #0F2A5C (et #0A1D42 pour les cartes graves)
  · le COIN BLANC EN BIAIS avec l'emblème et « MoheliGo · TRAVERSÉES MARITIMES »
  · le surtitre doré en petites capitales espacées
  · l'accroche Archivo 900, un bloc en dégradé d'or
  · la vague dorée en pied
Rien d'inventé pour l'occasion : ce sont les mêmes règles que `flyer31`.
"""
import os, subprocess
from PIL import ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
FLYERS = os.path.abspath(os.path.join(ICI, "..", "flyers"))
W, H = 1080, 1920

GABARIT = """<meta charset="utf-8">
<style>
@font-face {{ font-family:'Archivo'; font-weight:900; src:url(fonts/Archivo-900-latin.woff2) format('woff2'); }}
@font-face {{ font-family:'Archivo'; font-weight:700; src:url(fonts/Archivo-700-latin.woff2) format('woff2'); }}
@font-face {{ font-family:'Inter'; font-weight:500; src:url(fonts/Inter-500-latin.woff2) format('woff2'); }}
@font-face {{ font-family:'Inter'; font-weight:700; src:url(fonts/Inter-700-latin.woff2) format('woff2'); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ width:{W}px; height:{H}px; font-family:'Inter',sans-serif; -webkit-font-smoothing:antialiased; }}
.page {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; background:{fond}; }}
.eclat {{ position:absolute; inset:0; background:
  radial-gradient(760px 620px at 50% 24%, rgba(80,145,235,.20) 0%, rgba(15,42,92,0) 72%); }}

/* LE COIN — identique aux flyers, c'est notre forme */
.coin {{ position:absolute; top:0; left:0; width:472px; height:196px; background:#fff;
  clip-path:polygon(0 0, 100% 0, 78% 100%, 0 100%); z-index:5;
  display:flex; align-items:center; gap:17px; padding:20px 0 34px 46px;
  box-shadow:0 22px 54px rgba(4,12,40,.42); }}
.coin img {{ width:78px; height:78px; object-fit:contain; display:block; }}
.coin b {{ font-family:'Archivo',sans-serif; font-weight:900; font-size:33px; color:#0F2A5C;
  letter-spacing:-1px; line-height:1; display:block; }}
.coin b i {{ color:#F6BC1C; font-style:normal; }}
.coin small {{ display:block; font-size:10.5px; font-weight:700; letter-spacing:2.1px;
  color:#5C6E8B; margin-top:6px; }}

.sur {{ position:absolute; left:88px; top:{sur_y}px; z-index:3; font-size:19px;
  font-weight:700; letter-spacing:4.4px; color:#F6BC1C; }}
.acc {{ position:absolute; left:88px; right:88px; top:{acc_y}px; z-index:3;
  font-family:'Archivo',sans-serif; font-weight:900; font-size:{taille}px;
  line-height:1.02; letter-spacing:-3px; color:#fff; }}
.acc {{ white-space:nowrap; }}
.acc span {{ display:block; white-space:nowrap;
  background:linear-gradient(178deg, #FFF3C4 4%, #F6BC1C 34%, #C98A05 62%, #FFDD73 96%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  filter:drop-shadow(0 8px 24px rgba(150,100,4,.38)); }}
.note {{ position:absolute; left:88px; right:120px; top:{note_y}px; z-index:3;
  font-size:31px; line-height:1.45; color:#CFDDF3; }}
.note b {{ color:#fff; font-weight:700; }}

/* LA VAGUE — le même geste que les transitions, posé en pied */
.vague {{ position:absolute; left:0; right:0; bottom:0; height:224px; z-index:2; opacity:.95; }}
/* au-dessus de la vague, jamais dessus : l'adresse doit rester nette */
.pied {{ position:absolute; left:88px; right:88px; bottom:262px; z-index:4; }}
.pied .site {{ font-family:'Archivo',sans-serif; font-weight:900; font-size:74px; color:#fff;
  letter-spacing:-1.6px; }}
.pied small {{ display:block; font-family:'Inter',sans-serif; font-weight:700;
  font-size:19px; letter-spacing:3.4px; color:#F6BC1C; margin-bottom:12px; }}
</style>
<div class="page">
  <div class="eclat"></div>
  <div class="coin">
    <img src="logo-emblem.png" alt="">
    <div><b>Moheli<i>Go</i></b><small>TRAVERSÉES MARITIMES</small></div>
  </div>
  {sur}
  <div class="acc">{acc}</div>
  {note}
  <svg class="vague" viewBox="0 0 1080 300" preserveAspectRatio="none">
    <path d="M0,168 C190,96 340,214 540,168 C740,122 910,214 1080,158 L1080,300 L0,300 Z"
          fill="#F6BC1C" opacity=".92"/>
    <path d="M0,214 C210,158 350,254 540,214 C730,174 920,254 1080,206 L1080,300 L0,300 Z"
          fill="#ffffff" opacity=".16"/>
  </svg>
  {pied}
</div>
"""


def carte(sortie, lignes, mot_or=None, surtitre=None, note=None,
          fond="#0F2A5C", pied=None, taille=None):
    """Une carte du film. `lignes` : les lignes de l'accroche ; celles qui
    figurent dans `mot_or` passent en dégradé d'or."""
    # ⚠️ LA TAILLE SE MESURE, elle ne s'estime pas. La règle « Archivo 900 ≈
    # 0,47 × la taille par caractère » sert à viser ; ici on mesure avec la
    # VRAIE police, donc aucune ligne ne peut déborder ni se couper en deux.
    if taille is None:
        dispo = W - 2 * 88
        taille = 124
        arch = os.path.join(ICI, "polices", "Archivo-900.ttf")
        while taille > 52:
            f = ImageFont.truetype(arch, taille)
            if max(f.getlength(l) for l in lignes) <= dispo:
                break
            taille -= 2
    html = ""
    for l in lignes:
        if mot_or and l in mot_or:
            html += f"<span>{l}</span>"
        else:
            html += f"{l}<br>"
    html = html.replace("<br><span>", "<span>")
    # le bloc (surtitre + accroche + note) est centré autour de 46 % de la
    # hauteur : au-dessus le coin, en dessous la vague. Plus de vide au milieu.
    hauteur_bloc = int(taille * 1.02 * len(lignes)) + (150 if note else 0)
    acc_y = int(H * 0.46) - hauteur_bloc // 2
    corps = GABARIT.format(
        W=W, H=H, fond=fond, taille=taille,
        sur_y=acc_y - 58, acc_y=acc_y, note_y=acc_y + 90 + taille * len(lignes),
        sur=f'<div class="sur">{surtitre}</div>' if surtitre else "",
        acc=html,
        note=f'<div class="note">{note}</div>' if note else "",
        pied=(f'<div class="pied"><small>{pied[0]}</small>'
              f'<div class="site">{pied[1]}</div></div>') if pied else "")
    tmp = os.path.join(FLYERS, "_carte_film.html")
    open(tmp, "w", encoding="utf-8").write(corps)
    subprocess.run(["node", "render.js", "_carte_film.html", sortie, str(W), str(H), "1"],
                   cwd=FLYERS, check=True, capture_output=True)
    os.unlink(tmp)
    return sortie
