#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LES TROIS DOCUMENTS D'ÉVALUATION, en PDF.

    python3 examen.py

    → RoyalAir-examen-agence.pdf     10 questions, à faire remplir
    → RoyalAir-examen-escale.pdf     10 questions, à faire remplir
    → RoyalAir-examen-corrige.pdf    les réponses des deux, pour le correcteur

Tout le texte vient de `questions.py`. Ici, il n'y a que la mise en page.

📌 POURQUOI DU VRAI PDF ET PAS DES IMAGES
Un PDF fabriqué à partir d'images pèse dix fois plus, s'imprime flou, et ne se
cherche pas : impossible de retrouver « PMR » dans un dossier d'évaluations.
Ces trois-là sont composés en HTML puis imprimés par Chromium — le texte reste
du texte, sélectionnable, cherchable, et le fichier tient en quelques dizaines
de kilo-octets.

📌 POURQUOI LE CORRIGÉ EST UN DOCUMENT SÉPARÉ
Un corrigé rangé dans le même fichier que le sujet finit toujours par circuler
avec lui. Séparé, il porte sa propre mention de diffusion et reste chez le
correcteur.

📌 CE QUE LE CORRIGÉ CONTIENT EN PLUS DES RÉPONSES
La raison de chaque réponse, et le renvoi vers le passage du film. Un correcteur
qui ne peut qu'annoncer « c'est faux » ne corrige rien : l'agent doit savoir
POURQUOI, et où revoir trente secondes de film — pas le film entier.
"""
import base64
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import questions  # noqa: E402

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
DATE = "septembre 2026"
VERSION = "Rév. 01"

# Les couleurs de l'en-tête officielle, comme dans les films.
BLEU = "#004AAD"
BLEU_LOGO = "#1237A1"
ROUGE = "#EC313A"
OR = "#FDC20C"


def _b64(chemin, mime):
    with open(chemin, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())


def _polices():
    """Les mêmes polices que les films, embarquées dans le document.

    Sans cela, le PDF s'imprimerait avec la police par défaut du poste qui
    l'ouvre — et deux tirages du même examen n'auraient pas la même tête."""
    css = []
    for fichier, nom, graisse in (("Inter-500", "Inter", 500), ("Inter-700", "Inter", 700),
                                  ("Archivo-900", "Archivo", 900)):
        css.append("@font-face{font-family:'%s';font-weight:%d;src:url('%s') format('truetype')}"
                   % (nom, graisse, _b64(os.path.join(ICI, "polices", fichier + ".ttf"),
                                         "font/ttf")))
    return "\n".join(css)


STYLE = """
%(polices)s
/* 📌 LA PAGINATION EST AUTOMATIQUE, ET C'EST VOULU.
   Première tentative : des pages de hauteur fixe, avec un nombre de questions
   décidé à l'avance. À la première question un peu longue, la page débordait —
   et le débordement se retrouvait imprimé SOUS l'en-tête de la page suivante.
   Un défaut qu'on ne voit qu'en regardant le PDF, jamais dans le code.
   Ici, le document coule et Chromium coupe où il faut. L'en-tête et le pied
   sont dans le <thead> et le <tfoot> d'un tableau : c'est la seule construction
   que Chromium répète sur chaque page imprimée (les éléments en position fixe,
   eux, ne se répètent pas — vérifié). Ajouter une question ne peut donc plus
   rien casser : le document prend une page de plus, c'est tout. */
@page { size: A4; margin: 13mm 16mm 11mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Inter', sans-serif; color: #17263B;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
table.doc { width: 100%%; border-collapse: collapse; }
table.doc > thead td { padding-bottom: 4mm; }
table.doc > tfoot td { padding-top: 3mm; }

/* l'en-tête : la même bande bleue et rouge que le papier de la compagnie */
.tete { display: flex; align-items: center; gap: 10mm; border-bottom: 2.5pt solid %(bleu)s;
        padding-bottom: 4mm; }
.tete img { height: 17mm; }
.tete .qui { flex: 1; }
.tete .nom { font-family: 'Archivo'; font-weight: 900; font-size: 15pt;
             letter-spacing: .06em; color: %(bleu_logo)s; }
.tete .service { font-size: 8.5pt; letter-spacing: .13em; color: %(bleu)s;
                 font-weight: 700; margin-top: 1mm; }
.tete .ref { text-align: right; font-size: 8pt; line-height: 1.6; color: #5B6C86; }
.tete .ref b { color: %(bleu_logo)s; font-size: 9pt; }
.bande { height: 2.5mm; display: flex; margin-top: 1.5mm; }
.bande i { display: block; height: 100%%; }

h1 { font-family: 'Archivo'; font-weight: 900; font-size: 20pt; margin: 7mm 0 1mm;
     line-height: 1.15; }
.sous { font-size: 10pt; color: #5B6C86; margin-bottom: 5mm; }

/* le bloc d'identification, à remplir à la main */
.identite { border: .8pt solid #C7D2E2; border-left: 3pt solid %(bleu)s;
            padding: 4mm 5mm; display: grid; grid-template-columns: 1fr 1fr;
            gap: 3.5mm 8mm; margin-bottom: 4mm; }
.identite div { font-size: 9pt; color: #5B6C86; }
.identite span { display: inline-block; border-bottom: .6pt solid #9FB0C7;
                 min-width: 42mm; margin-left: 2mm; }

.consigne { background: #EEF3FB; border-left: 3pt solid %(or)s; padding: 3.5mm 5mm;
            font-size: 9pt; line-height: 1.55; margin-bottom: 5mm; }
.consigne b { color: %(bleu_logo)s; }

ol.questions { list-style: none; counter-reset: q; padding: 0; margin: 0; flex: 1; }
ol.questions > li { counter-increment: q; margin-bottom: 4.6mm;
                    break-inside: avoid; }
ol.questions > li > .enonce { font-weight: 700; font-size: 9.8pt; line-height: 1.4;
                              display: flex; gap: 3mm; }
ol.questions > li > .enonce::before { content: counter(q); font-family: 'Archivo';
    font-weight: 900; color: #FFF; background: %(bleu)s; min-width: 6.5mm; height: 6.5mm;
    border-radius: 50%%; display: flex; align-items: center; justify-content: center;
    font-size: 9pt; flex: none; }
ol.questions .choix { margin: 1.8mm 0 0 9.5mm; }
ol.questions .choix div { font-size: 9.2pt; line-height: 1.45; margin-bottom: .9mm;
                          display: flex; gap: 2.5mm; }
ol.questions .choix .lettre { font-weight: 700; color: %(bleu)s; width: 5.5mm;
                              flex: none; }
.case { display: inline-block; width: 3.4mm; height: 3.4mm; border: .8pt solid #7E90AA;
        border-radius: .8mm; flex: none; margin-top: .5mm; }

/* le pied de page */
.pied { border-top: .8pt solid #C7D2E2; padding-top: 2.5mm;
        display: flex; justify-content: space-between; font-size: 7.5pt;
        color: #7E90AA; }
.pied b { color: %(bleu)s; }

/* le corrigé */
.reponses { margin: 0; padding: 0; list-style: none; counter-reset: r; }
.reponses li { counter-increment: r; display: flex; gap: 3.5mm; padding: 2.4mm 0;
               border-bottom: .5pt solid #E1E7F0; break-inside: avoid; }
.reponses .num { font-family: 'Archivo'; font-weight: 900; font-size: 9pt; color: #7E90AA;
                 width: 5mm; flex: none; padding-top: .6mm; }
.reponses .lettre { font-family: 'Archivo'; font-weight: 900; font-size: 12pt;
                    color: #FFF; background: #1B9E4B; width: 7mm; height: 7mm;
                    border-radius: 1.5mm; display: flex; align-items: center;
                    justify-content: center; flex: none; }
.reponses .txt { flex: 1; font-size: 8.6pt; line-height: 1.45; }
.reponses .txt .bonne { font-weight: 700; }
.reponses .txt .pourquoi { color: #40506B; margin-top: .8mm; }
.reponses .txt .renvoi { color: %(bleu)s; font-size: 7.6pt; font-weight: 700;
                         letter-spacing: .04em; margin-top: .8mm; }
.bareme { border: .8pt solid #C7D2E2; border-left: 3pt solid #1B9E4B; padding: 4mm 5mm;
          font-size: 9pt; line-height: 1.5; margin: 4mm 0 5mm; }
.bareme b { color: %(bleu_logo)s; }
h2 { font-family: 'Archivo'; font-weight: 900; font-size: 13pt; margin: 0 0 3mm;
     color: %(bleu_logo)s; padding-bottom: 1.5mm; border-bottom: 2pt solid %(or)s; }
"""


def tete(ref):
    return """
    <div class="tete">
      <img src="%s">
      <div class="qui"><div class="nom">ROYAL AIR</div>
        <div class="service">DÉPARTEMENT QUALITÉ</div></div>
      <div class="ref"><b>%s</b><br>%s · %s</div>
    </div>
    <div class="bande"><i style="background:%s;flex:.7"></i>
      <i style="background:%s;flex:.3"></i></div>
    """ % (_b64(os.path.join(ICI, "marque", "royal-air-logo.png"), "image/png"),
           ref, VERSION, DATE, BLEU, ROUGE)


def document(ref, mention, corps):
    """Le squelette commun : en-tête et pied répétés, contenu au milieu."""
    return ('<table class="doc"><thead><tr><td>%s</td></tr></thead>'
            '<tfoot><tr><td>%s</td></tr></tfoot>'
            '<tbody><tr><td>%s</td></tr></tbody></table>'
            % (tete(ref), pied(ref, mention), corps))


def pied(ref, mention):
    # l'espace du milieu est vide : c'est là que `numeroter` tamponnera le
    # numéro de page une fois le document composé et le total connu.
    return ('<div class="pied"><span><b>%s</b> · Département Qualité Royal Air</span>'
            '<span></span><span>%s</span></div>' % (ref, mention))


def sujet(ev):
    """Un sujet : identification, consigne, puis les dix questions à la suite."""
    items = []
    for q in ev["questions"]:
        choix = "".join(
            '<div><span class="case"></span><span class="lettre">%s.</span>'
            '<span>%s</span></div>' % ("ABCD"[i], o)
            for i, o in enumerate(q["options"]))
        items.append('<li><div class="enonce"><span>%s</span></div>'
                     '<div class="choix">%s</div></li>' % (q["q"], choix))

    corps = """
      <h1>Évaluation — %s</h1>
      <div class="sous">%s · d'après le film de sensibilisation <b>%s</b></div>
      <div class="identite">
        <div>Nom et prénom <span></span></div>
        <div>Fonction <span></span></div>
        <div>Agence / Escale <span></span></div>
        <div>Date <span></span></div>
        <div>Signature de l'agent <span></span></div>
        <div>Visa du responsable <span></span></div>
      </div>
      <div class="consigne">
        <b>Dix questions, une seule bonne réponse par question.</b>
        Cochez la case correspondante. Durée indicative&nbsp;: 15 minutes.
        Sans document. <b>Seuil d'acquisition&nbsp;: %d bonnes réponses sur 10.</b>
        En dessous, le film est à revoir avec le responsable avant nouvelle
        évaluation.
      </div>
      <ol class="questions">%s</ol>""" % (ev["titre"], ev["pour"], ev["film"],
                                          questions.SEUIL, "".join(items))
    return document(ev["reference"],
                    "Document interne — à conserver au dossier de formation", corps)


def corrige():
    """Le corrigé des deux évaluations, avec la raison et le renvoi."""
    blocs = ["""
      <h1>Corrigé des évaluations</h1>
      <div class="sous">Réservé au correcteur — ne pas remettre avec le sujet</div>
      <div class="bareme">
        <b>Barème.</b> 1 point par bonne réponse, pas de point négatif.
        <b>Seuil d'acquisition&nbsp;: %d / 10.</b><br>
        <b>8 à 10</b> — acquis. Consigner la note au dossier de formation.<br>
        <b>Moins de %d</b> — à revoir. Le film est revu avec le responsable
        d'agence ou le chef d'escale, en s'arrêtant aux passages indiqués par la
        mention <b>↳</b>, puis l'évaluation est refaite.<br>
        <b>Une erreur sur une question de sûreté ou de données passager</b>
        (agence&nbsp;7 et&nbsp;10, escale&nbsp;4 et&nbsp;10) se reprend
        immédiatement, quelle que soit la note d'ensemble.
      </div>""" % (questions.SEUIL, questions.SEUIL)]

    for ev in (questions.AGENCE, questions.ESCALE):
        lignes = []
        for n, q in enumerate(ev["questions"], 1):
            i = q["bonne"]
            lignes.append(
                '<li><div class="num">%d</div><div class="lettre">%s</div>'
                '<div class="txt"><div class="bonne">%s</div>'
                '<div class="pourquoi">%s</div>'
                '<div class="renvoi">↳ %s</div></div></li>'
                % (n, "ABCD"[i], q["options"][i], q["pourquoi"], q["renvoi"]))
        blocs.append('<h2>%s — %s</h2><ul class="reponses">%s</ul>'
                     % (ev["reference"], ev["titre"], "".join(lignes)))

    return document("QUA-EVAL-003",
                    "Corrigé — diffusion restreinte au correcteur", "".join(blocs))


def numeroter(pdf):
    """Tamponne « Page i / n » sur chaque page.

    📌 POURQUOI APRÈS COUP ET NON DANS LE HTML
    Le nombre de pages n'est connu qu'une fois le document composé, et Chromium
    ne sait pas écrire un compteur de pages dans un en-tête répété. On l'écrit
    donc sur le PDF fini — avec la police du document, pas celle du lecteur,
    pour que le numéro ne jure pas avec le reste."""
    import pymupdf
    d = pymupdf.open(pdf)
    police = os.path.join(ICI, "polices", "Inter-500.ttf")
    MM = 72 / 25.4                       # un millimètre, en points PDF
    for i, page in enumerate(d, 1):
        # aligné à droite sous la référence et la révision de l'en-tête,
        # dans la même colonne : c'est la place d'un numéro de page sur un
        # document contrôlé.
        # ▸ On ne tamponne pas à une hauteur fixe : sur la DERNIÈRE page, le
        #   pied remonte avec le contenu au lieu de rester en bas. Un numéro
        #   posé à 282 mm s'y retrouverait tout seul, à cinq centimètres de sa
        #   ligne. On cherche donc le pied sur la page et on se cale dessus.
        repere = page.search_for("Département Qualité Royal Air")
        y = repere[0].y0 - 1.2 if repere else 281.6 * MM
        cadre = pymupdf.Rect(page.rect.width / 2 - 30 * MM, y,
                             page.rect.width / 2 + 30 * MM, y + 6 * MM)
        page.insert_textbox(cadre, "Page %d / %d" % (i, d.page_count),
                            fontname="inter", fontfile=police, fontsize=7.5,
                            color=(0.49, 0.56, 0.67),
                            align=pymupdf.TEXT_ALIGN_CENTER)
    # PyMuPDF refuse d'écrire par-dessus le fichier qu'il a ouvert : on passe
    # par un fichier voisin, puis on remplace.
    provisoire = pdf + ".tmp"
    d.save(provisoire, deflate=True, garbage=3)
    d.close()
    os.replace(provisoire, pdf)
    return pdf


def en_pdf(corps, sortie):
    html = ("<!doctype html><html lang=fr><meta charset=utf-8><style>%s</style>%s"
            % (STYLE % {"polices": _polices(), "bleu": BLEU, "bleu_logo": BLEU_LOGO,
                        "rouge": ROUGE, "or": OR}, corps))
    tmp = os.path.join(ICI, ".travail", os.path.basename(sortie) + ".html")
    os.makedirs(os.path.dirname(tmp), exist_ok=True)
    with open(tmp, "w") as f:
        f.write(html)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--print-to-pdf=" + sortie,
                    "file://" + tmp], check=True, capture_output=True)
    return numeroter(sortie)


if __name__ == "__main__":
    travaux = [("RoyalAir-examen-agence.pdf", sujet(questions.AGENCE)),
               ("RoyalAir-examen-escale.pdf", sujet(questions.ESCALE)),
               ("RoyalAir-examen-corrige.pdf", corrige())]
    for nom, corps in travaux:
        f = en_pdf(corps, os.path.join(ICI, nom))
        print("   → %-34s %5.0f Ko" % (nom, os.path.getsize(f) / 1024))
