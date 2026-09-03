#!/usr/bin/env python3
"""⬛ LE CONTRÔLE DE LA BARRE — il REFUSE, il ne conseille pas.

29/08/2026. Le patron : « les petites détails comptent, tout doit être correct
et très exigeant. » Une norme qu'on relit de bonne volonté est une intention ;
une norme qu'une machine fait respecter est une norme.

    python3 exigence.py flyer44-quelquun-fb.html
    python3 exigence.py --tous          # toute la bibliothèque

La norme complète : ../../dossier/EXIGENCE.md
Ce programme n'en vérifie que la partie MESURABLE — et c'est déjà beaucoup :
sur la bibliothèque au 29/08, il a trouvé 186 apostrophes droites que personne
n'avait vues en trois semaines.

⚠️ CE QU'IL NE SAIT PAS FAIRE, et qu'aucun programme ne saura :
dire si l'image est juste, si la promesse est vraie, si le sentiment passe.
Il complète l'œil, il ne le remplace pas — règle 7.5 de la norme.
"""
import glob
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))

# ── § 2 : les mots qui parlent de nous au lieu de parler au lecteur ──────────
ABSTRAITS = ['digitalisation', 'digital', 'solution', 'plateforme', 'innovation',
             'révolution', 'écosystème', 'expérience', 'technologie',
             'optimisation', 'modernité']
SUPERLATIFS = ['le meilleur', 'la meilleure', 'le plus rapide', 'unique en',
               'révolutionnaire', 'incontournable', 'leader', 'n°1', 'numéro un']
# ── § 4 : les formules qui ne demandent rien ────────────────────────────────
FAUX_APPELS = ['en savoir plus', 'cliquez ici', 'clique ici', 'découvrez',
               'contactez-nous', "n'hésitez pas", 'nous contacter']
# ⚠️ CETTE LISTE EST FERMÉE, DONC ELLE SERA TOUJOURS INCOMPLÈTE — et c'est un
# choix, pas un oubli : on ne sait pas reconnaître un impératif français par
# programme sans conjugueur, alors qu'une liste dit exactement ce qu'elle
# accepte. Le prix à payer est qu'elle doit GRANDIR quand un verbe légitime se
# présente.
# 📌 02/09/2026 — « scanne » ajouté. Le contrôle refusait « SCANNE ET RÉSERVE »,
# posé à côté d'un QR code : c'est pourtant l'impératif exact du geste demandé.
# La règle avait tort, pas le visuel — comme le 30/08 avec les « 6 mots
# maximum ». On corrige celui qui a tort, on ne contourne jamais.
VRAIS_VERBES = ['réserve', 'prends', 'choisis', 'paie', 'écris', 'appelle',
                'embarque', 'traverse', 'rejoins', 'scanne']
SENTIMENTS = ['LE SOULAGEMENT', 'LA PROXIMITÉ', 'LA FIERTÉ', 'LA CONFIANCE']

# 💎 CE QUI N'EST PAS PREMIUM — posé par le patron le 02/09/2026 : « tous les
# mots et toutes les phrases doivent être premium, je veux du premium partout ».
# Une liste noire de mots n'aurait pas suffi : nos textes n'en contenaient
# presque aucun, et ils n'étaient pas premium pour autant. Ce qui les trahissait
# tenait en trois gestes, et ce sont eux qu'on interdit ici.
#
# 1. S'ATTÉNUER. « un peu », « juste », « simple ». Une marque qui relativise sa
#    propre information invite à ne pas la croire.
# 2. SE JUSTIFIER. « c'est pour ça qu'on publie », « c'est à ça que sert cette
#    page ». Expliquer son propre dispositif, c'est demander la permission
#    d'exister. On énonce, on ne plaide pas.
# 3. SE COMPARER AU TOUT-VENANT. « comme n'importe quel site ». Se rendre
#    ordinaire pour rassurer, c'est renoncer à valoir plus cher.
# 📌 LE PREMIUM N'EST PAS UN VOCABULAIRE, C'EST UNE POSTURE : on affirme, on ne
# se défend pas.
PAS_PREMIUM = [
    (r'\bun peu\b', 'atténuation'),
    (r'\bjuste\b(?! ?\w*prix)', 'atténuation'),
    (r'\bsimplement\b', 'atténuation'),
    (r'\bvraiment\b', 'atténuation'),
    (r'\bplutôt\b', 'atténuation'),
    (r"c[’']est pour ça qu", 'justification'),
    (r"c[’']est à ça que sert", 'justification'),
    (r"comme n[’']importe quel", 'comparaison au tout-venant'),
    (r'\bpas cher\b', 'petit prix'),
    (r'\bpromo\b', 'petit prix'),
    (r'\ben fait\b', 'remplissage'),
    (r'\bdu coup\b', 'remplissage'),
]

FINE = ' '          # espace fine insécable
INSEC = ' '         # espace insécable


def _visible(html):
    """Le texte que le lecteur verra : sans commentaires, sans CSS, sans balises."""
    t = re.sub(r'<!--.*?-->', '', html, flags=re.S)
    t = re.sub(r'<style>.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<svg.*?</svg>', '', t, flags=re.S)
    t = re.sub(r'<br\s*/?>', ' / ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&amp;', '&').replace('&nbsp;', INSEC)
    return ' '.join(t.split())


def _entete(html):
    m = re.match(r'\s*<!--(.*?)-->', html, flags=re.S)
    return m.group(1) if m else ''


def _titre(html):
    """Le contenu de `.acc` — l'accroche, la seule chose lue en trois secondes.

    🚩 CORRIGÉ LE 30/08/2026 : UN `<span>` NE COUPE PAS TOUJOURS LA LIGNE.
    On coupait le titre à chaque `<span>`. Or un span ne fait une ligne que s'il
    est en `display:block` — sinon il dore quelques mots À L'INTÉRIEUR de la
    ligne. Le flyer 43 écrivait `EST <span>LÀ.</span>` : deux lignes à l'œil,
    trois pour le contrôle, qui refusait un visuel juste.
    📌 Une machine qui compte autre chose que ce que le lecteur voit ne mesure
    rien — elle invente. On lit donc la règle CSS avant de compter.
    """
    m = re.search(r'class="acc"[^>]*>(.*?)</div>', html, flags=re.S)
    if not m:
        return None
    coupe = r'<br\s*/?>'
    bloc = re.search(r'\.acc\s+span\s*\{[^}]*display\s*:\s*block', html)
    if bloc:
        coupe += r'|<span[^>]*>|</span>'
    t = re.sub(r'<[^>]+>', ' | ', m.group(1))
    return ' '.join(t.replace('|', ' ').split()), [
        ' '.join(re.sub(r'<[^>]+>', ' ', l).split())
        for l in re.split(coupe, m.group(1)) if l.strip()]


def controler(chemin):
    html = open(chemin, encoding='utf-8').read()
    vis = _visible(html)
    ent = _entete(html)
    refus, alertes = [], []

    def refuse(regle, quoi):
        refus.append(f'§{regle}  {quoi}')

    def alerte(regle, quoi):
        alertes.append(f'§{regle}  {quoi}')

    # ── § 5 MICRO-TYPOGRAPHIE ────────────────────────────────────────────────
    n = vis.count("'")
    if n:
        refuse('5', f"{n} apostrophe(s) droite ' — il faut ’ (U+2019)")
    if '"' in vis:
        refuse('5', 'guillemets droits " — il faut « … »')
    for m in re.finditer(r'([^\s  ])([;:!?])', vis):
        refuse('5', f'espace fine manquante avant « {m.group(2)} » : '
                    f'…{vis[max(0, m.start()-24):m.start()+6]}…')
    for c in set(vis):
        if ord(c) > 0x2019 and c not in '—…·’€  ':
            refuse('5', f'caractère hors latin : « {c} » (U+{ord(c):04X}, '
                        f'{unicodedata.name(c, "?")}) — absent de nos woff2')

    # ── § 2 LA PHRASE ────────────────────────────────────────────────────────
    if '!' in vis:
        refuse('2', "point d'exclamation sur le visuel")
    for a in ABSTRAITS:
        if re.search(r'\b' + a, vis, re.I):
            alerte('2', f'mot abstrait « {a} » — un seul toléré dans le corps')
    # ⚠️ ON RETIRE D'ABORD LES NOMS PROPRES. « Young Leader Mohéli » est le nom
    # de notre partenaire, pas une prétention. Faux positif vu le 29/08 : la
    # règle refusait un visuel parce qu'il nommait correctement quelqu'un.
    # 📌 Un contrôle qui punit un fait exact rend la norme absurde, et une norme
    # absurde finit contournée. On la corrige, on ne contourne pas.
    sans_noms = vis
    for propre in ('Young Leader', 'kartaPay', 'MoheliGo'):
        sans_noms = re.sub(propre, ' ', sans_noms, flags=re.I)
    for s in SUPERLATIFS:
        if s in sans_noms.lower():
            refuse('2', f'superlatif invérifiable « {s} »')
    # ⚠️ on retire d'abord les numéros de téléphone : « +269 479 43 28 » n'est
    # pas un volume inventé. Faux positif vu au premier essai sur le flyer 40.
    sans_tel = re.sub(r'\+\s?269[\d  ]+', ' ', vis)
    if re.search(r'\+\s?\d{3,}', sans_tel):
        refuse('7.1', 'chiffre non mesuré (règle du 29/08 : jamais de volume inventé)')

    t = _titre(html)
    if not t:
        alerte('2', 'aucun bloc `.acc` trouvé — titre non contrôlable')
    else:
        plat, lignes = t
        # 🚩 6 MOTS PAR LIGNE, ET NON PAR TITRE — corrigé le 30/08/2026.
        # La règle « 6 mots pour tout le titre » refusait « ON NE VISITE PAS
        # MOHÉLI. ON Y REVIENT. » (8 mots) — une de nos meilleures lignes, notée
        # 9/10 par un relecteur extérieur, et deux phrases de 5 et 3 mots.
        # 📌 Une règle qui refuse ce qu'on a fait de mieux n'est pas une règle
        # exigeante : c'est une règle mal écrite. La vraie contrainte est ce que
        # l'œil saisit d'un coup, donc elle se compte PAR LIGNE. Les 32 signes
        # par ligne restent la limite qui mord vraiment.
        # 🚩 02/09/2026 — LA FOURCHETTE PASSE DE « ≤ 6 » À « 2 À 5 ».
        # Le patron : « les écritures doivent être vraiment style Apple, deux à
        # cinq mots mais très impactant, et inspirer le respect de la marque. »
        # Ce n'est pas un resserrement cosmétique : à six mots on explique
        # encore, à quatre on affirme. « Think different. » « Privacy. That's
        # iPhone. » — personne n'y finit une phrase, on y pose une idée.
        # ⚠️ LE PLAFOND SE COMPTE PAR LIGNE, LE PLANCHER SUR LE TITRE ENTIER —
        # et j'ai écrit l'inverse au premier jet, ce qui a immédiatement refusé
        # « TU L'AS / DÉJÀ. » (publié le jour même) et « TU PARS VOIR /
        # QUELQU'UN. » (noté 9/10 dehors), au motif que leur seconde ligne ne
        # fait qu'un mot.
        # 📌 UNE LIGNE D'UN SEUL MOT N'EST PAS UNE ÉTIQUETTE : C'EST UNE
        # CADENCE. C'est même le geste exact qu'on cherche — « Bigger than /
        # bigger », « Privacy. / That's iPhone. » Le mot isolé porte l'accent
        # parce que le regard s'y arrête. Ce qu'il faut interdire, c'est un
        # TITRE d'un seul mot (« MOHÉLI. » ne dit rien), pas une ligne courte
        # dans un titre qui, lui, a un sujet et un verbe.
        # ✅ Comptée PAR LIGNE, comme depuis le 30/08 : « ON NE VISITE PAS
        # MOHÉLI. / ON Y REVIENT. » fait 5 et 3, et reste notre meilleure ligne.
        for l in lignes:
            n = len(l.split())
            if n > 5:
                refuse('2', f'ligne de titre de {n} mots (maximum 5) : « {l} »')
        if len(plat.split()) < 2:
            refuse('2', f'titre d’un seul mot — c’est une étiquette, pas une '
                        f'accroche : « {plat} »')

        # 🚩 UN SEUL TRAITEMENT DE TITRE POUR TOUTE LA MARQUE — 02/09/2026.
        # Le patron : « va regarder les règles d'Apple ou Coca-Cola, même si
        # c'est très strict on les suit au détail près ». Les deux disent la
        # même chose, et c'est la règle la plus dure des deux chartes :
        # · Coca-Cola, Design Standards § 2.35 : « Do not use any font other
        #   than Gotham Bold as the primary headline font » + « don't use
        #   lowercase-only typography for long headlines or sentences » ;
        # · Apple, Identity Guidelines p. 12 : « Do not change the font or
        #   alter the spacing between letters. »
        # Ce n'est pas une question de goût : une marque doit avoir l'air
        # d'avoir été faite par UNE SEULE MAIN. Deux traitements de titre dans
        # la même bibliothèque, et le lecteur voit deux entreprises.
        # ⛔ MESURÉ LE JOUR MÊME : nos CINQ meilleurs visuels sont en capitales
        # à 100 % — dont celui noté 9/10 dehors. Les autres étaient en
        # minuscules… **y compris les deux que je venais de réparer le matin.**
        # J'ai donc fabriqué l'incohérence en croyant corriger.
        # 📌 On ne juge pas un visuel tout seul : on le juge À CÔTÉ DES AUTRES.
        lettres = [c for c in plat if c.isalpha()]
        if lettres:
            caps = sum(c.isupper() for c in lettres) / len(lettres)
            if caps < 0.9:
                refuse('2', f'titre en minuscules ({caps*100:.0f} % de '
                            f'capitales) — la marque n’a qu’un seul traitement '
                            f'de titre, et c’est LES CAPITALES : « {plat} »')
        for l in lignes:
            if len(l) > 32:
                refuse('2', f'ligne de titre de {len(l)} signes (maximum 32) : « {l} »')
        if len(lignes) > 2:
            refuse('2', f'{len(lignes)} lignes de titre (maximum 2)')
        for a in ABSTRAITS:
            if re.search(r'\b' + a, plat, re.I):
                refuse('2', f'mot abstrait « {a} » DANS LE TITRE — interdit')
        lecteur = re.search(r'\b(tu|ton|ta|tes|toi)\b', plat, re.I) or \
            any(plat.lower().startswith(v) for v in VRAIS_VERBES) or \
            re.search(r'\bon\b', plat, re.I)
        if not lecteur:
            refuse('2', f'le titre ne parle pas au lecteur : « {plat} » — '
                        'il faut un tu/ton/ta, un impératif, ou une situation vécue')

    # ── § 4 L'APPEL À L'ACTION ───────────────────────────────────────────────
    for f in FAUX_APPELS:
        if f in vis.lower():
            refuse('4', f'appel creux « {f} »')
    cta = re.search(r'class="cta"[^>]*>(.*?)</div>', html, flags=re.S)
    if not cta:
        refuse('4', 'aucun appel à l’action (`.cta`)')
    else:
        texte = ' '.join(re.sub(r'<[^>]+>', ' ', cta.group(1)).split())
        if not any(texte.lower().startswith(v) for v in VRAIS_VERBES):
            refuse('4', f'l’appel ne commence pas par un verbe d’action : « {texte} »')
    if 'moheligo.com' not in vis.lower():
        refuse('4', 'aucune adresse où agir — un verbe sans adresse est un vœu')

    # ── § 2 bis LE PREMIUM ───────────────────────────────────────────────────
    for motif, famille in PAS_PREMIUM:
        m = re.search(motif, vis, re.I)
        if m:
            refuse('2', f'« {m.group(0)} » — {famille}. Le premium n’est pas un '
                        f'vocabulaire, c’est une posture : on affirme, on ne se '
                        f'défend pas.')

    # ── § 3 LE SENTIMENT DÉCLARÉ ─────────────────────────────────────────────
    # 🚩 03/09/2026 — ON LIT LA LIGNE DE DÉCLARATION, PAS TOUT L'EN-TÊTE.
    # Le contrôle cherchait les quatre noms n'importe où dans le commentaire de
    # tête. Un visuel dont l'en-tête EXPLIQUE la palette — en citant les quatre
    # sentiments et le nombre de fois qu'on les joue — se faisait donc refuser
    # pour « 4 sentiments déclarés ». Il n'en déclarait qu'un : il en MENTIONNAIT
    # quatre.
    # 📌 **DÉCLARER ET MENTIONNER NE SONT PAS LA MÊME CHOSE.** Un contrôle qui
    # confond les deux punit précisément les fichiers qui documentent le mieux ce
    # qu'ils font — donc il décourage exactement le comportement qu'on veut.
    # La norme dit « déclaré dans l'en-tête » : la déclaration est la ligne
    # `SENTIMENT : X`, et c'est elle seule qu'on lit.
    ligne = re.search(r'SENTIMENT\s*:\s*(.+)', ent)
    dec = [s for s in SENTIMENTS if s in ligne.group(1)] if ligne else []
    if not dec:
        refuse('3', 'aucun SENTIMENT déclaré dans l’en-tête '
                    f'(un parmi : {", ".join(SENTIMENTS)})')
    elif len(dec) > 1:
        refuse('3', f'{len(dec)} sentiments déclarés — un visuel n’en porte qu’un')

    # ── § 6 LE DESSIN ────────────────────────────────────────────────────────
    css = html
    if 'left:76px' not in css.replace(' ', ''):
        alerte('6', 'marge de gauche différente de 76 px')
    if not re.search(r'width:\s*404px;\s*height:\s*172px', css):
        alerte('6', 'coin blanc hors gabarit (404 × 172)')
    if 'height:74px' not in css.replace(' ', ''):
        alerte('6', 'vague différente de 74 px')
    if not re.search(r'width:\s*1080px;\s*height:\s*1350px', css):
        alerte('6', 'format différent de 1080 × 1350')

    return refus, alertes


def _rapport(chemin, refus, alertes):
    nom = os.path.basename(chemin)
    if refus:
        print(f'\n❌ REFUSÉ — {nom}   ({len(refus)} manquement(s))')
        for r in refus:
            print(f'   {r}')
    elif alertes:
        print(f'\n⚠️  PASSE avec réserve — {nom}')
    else:
        print(f'\n✅ CONFORME — {nom}')
    for a in alertes:
        print(f'   · {a}')
    return not refus


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == '--tous':
        fichiers = sorted(glob.glob(os.path.join(ICI, 'flyer*-fb.html')))
    else:
        fichiers = args
    ok = 0
    for f in fichiers:
        r, a = controler(f)
        ok += _rapport(f, r, a)
    print(f'\n{"─" * 62}\n{ok} conforme(s) sur {len(fichiers)}')
    sys.exit(0 if ok == len(fichiers) else 1)
