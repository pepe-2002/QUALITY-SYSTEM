#!/usr/bin/env python3
"""Le programme de publication de la semaine MoheliGo.

Le patron (11/08/2026) : « pourquoi le bulletin du soir seulement ? c'est toi le
directeur marketing et commercial, tu vas tout gérer les pubs. »

    tous les soirs   le bulletin mer          (daté, fabriqué le jour même)
    lundi            comment ça marche
    mardi            la proximité
    mercredi         le produit
    jeudi            la proximité de l'île
    vendredi         partir et revenir
    samedi           la destination
    dimanche         la fierté

🚩 RÉÉCRIT LE 02/09/2026, APRÈS LE GRAND NETTOYAGE.
Le patron : « supprime tous les flyers qui ne sont pas aux normes, les anciens
flyers », puis « les écritures doivent être vraiment style Apple, deux à cinq
mots mais très impactant ». Quarante visuels sont partis le même jour ; il en
reste sept, et ce fichier ne connaît plus qu'eux.

⛔ CE QUI A CHANGÉ DANS LA MÉCANIQUE, ET C'EST LE PLUS IMPORTANT : avant, un jour
SANS visuel était impossible — chaque jour avait forcément sa case. Après le
nettoyage, deux jours n'ont plus rien. L'ancien code serait allé chercher un
fichier supprimé et aurait planté au moment de publier, c'est-à-dire à midi, le
seul moment où personne ne regarde le journal.
📌 **UN CALENDRIER QUI NE SAIT PAS DIRE « JE N'AI RIEN AUJOURD'HUI » MENT UN JOUR
SUR SEPT.** `du_jour()` rend donc `None`, exactement comme `du_matin()` le fait
depuis toujours, et `programme.py` se tait proprement.

⚠️ **Le texte du post vit à côté du visuel, dans un `texte-*.txt`.** C'est la
convention des visuels récents et elle gagne : le fichier porte le même nom que
l'image, on voit d'un coup d'œil ce qui va avec quoi, et rien n'est recopié.
`page.py` reste la vitrine du patron, plus la source.

🏆 **LE JEUDI EST LE NOUVEAU GABARIT** (`flyer48`, 02/09) : photo plein cadre,
vague d'or en COUTURE entre la mer et les mots, titre en deux lignes. Le patron
a demandé un visuel « directement reconnaissable SANS LOGO » — c'est celui-là qui
répond, et les prochains le suivent.

⚠️ **L'usure reste le vrai risque**, et elle est PIRE qu'avant : cinq visuels
pour sept jours. Deux jours vides valent mieux qu'un visuel hors norme — mais
c'est un état de chantier, pas une cible. La bibliothèque doit regrandir, DANS
le système cette fois.
"""
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))

ICI = pathlib.Path(__file__).parent
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

# --- les sept jours : (visuel, texte du post, ce qu'on y raconte) ------------
# `None` = rien de prévu ce jour-là. Ce n'est pas une panne, c'est un trou connu
# dans la bibliothèque, et il est écrit ici plutôt que découvert à midi.
SEMAINE = {
    0: ('flyer-rien-installer-facebook.png', 'texte-rien-installer.txt',
        'comment ça marche'),
    1: ('flyer-quelquun-v2-facebook.png', 'texte-quelquun-v2.txt',
        'la proximité'),
    2: ('flyer-tulasdeja-facebook.png', 'texte-tulasdeja.txt',
        'le produit'),
    3: ('flyer-traversee-facebook.png', 'texte-traversee.txt',
        'la proximité de l’île'),
    4: ('flyer-etudes-facebook.png', 'texte-etudes.txt',
        'partir et revenir'),
    5: ('flyer-revenir-facebook.png', 'texte-revenir.txt',
        'la destination'),
    6: ('flyer-chez-nous-facebook.png', 'texte-chez-nous.txt',
        'la fierté'),
}

# --- 🔴 LES VISUELS RETENUS : la décision de NE PAS publier, écrite -----------
# 09/09/2026, et c'est une faute à moi qui a écrit cette section.
#
# Ce matin j'ai constaté que le visuel du mercredi était impubliable : l'écran de
# l'appli y affiche une date calculée à la fabrication, et elle valait le
# 09/09/2026 — c'est-à-dire AUJOURD'HUI, premier jour de la fermeture. Une
# recherche de traversée pour un jour sans départ. Je ne l'ai donc pas publié à
# midi, et je l'ai écrit au patron.
#
# ⛔ IL EST SORTI QUAND MÊME, À 14h36, PUBLIÉ PAR LE FILET DE `cron` QUE J'AVAIS
# POSÉ LA VEILLE. Le filet a fait exactement ce pour quoi il est fait : voir
# qu'aucune publication de midi n'était partie, et rattraper.
# 📌 **MA DÉCISION DE NE PAS PUBLIER N'EXISTAIT QUE DANS MA TÊTE.** Le système,
# lui, ne connaissait qu'une seule information : « rien n'est parti à midi ».
# Il ne pouvait pas distinguer « personne n'a poussé le battement » de « on a
# examiné ce visuel et on l'a écarté ». **Un jugement qui ne s'écrit nulle part
# n'est pas une décision : c'est une intention, et une intention ne survit pas à
# la première automatisation.**
# ⚖️ Et c'est le prix exact du filet, payé le lendemain de sa pose : un système
# plus fiable exécute aussi plus fidèlement ce qu'on a oublié de lui dire.
#
# ✅ D'où ce tableau. Un visuel qui y figure ne part par AUCUN chemin — ni
# battement, ni `cron`, ni rattrapage — et la raison est lisible par le prochain
# qui passe. On le retire d'ici le jour où le défaut est réparé, pas avant.
RETENUS = {
    'flyer-tulasdeja-facebook.png':
        'l’écran de l’appli affiche une date calculée à la fabrication, et elle '
        'est dépassée. Elle ne peut pas être regénérée : `refaire.py` lit la '
        'photo d’origine du patron dans un dossier de session effacé avec le '
        'conteneur. 👉 redemander la photo au patron, et la ranger DANS le dépôt.',
}


# --- LE MATIN : plus rien, et il faut le dire ------------------------------
# La démonstration du matin (« EN TROIS GESTES, TA PLACE EST RÉSERVÉE ») est
# partie au nettoyage du 02/09 : son titre faisait sept mots, et son dernier mot
# s'imprimait SOUS le paragraphe — le même défaut de collision que le lundi.
# Elle reviendra quand elle sera refaite au standard. En attendant, `du_matin()`
# rend `None` tous les jours, ce que `programme.py` sait déjà traiter.
MATIN = {}


def _lire(nom):
    """Le texte du post, lu à côté du visuel. None si le fichier manque."""
    f = ICI / nom
    return f.read_text(encoding='utf-8').strip() if f.exists() else None


def _valide(entree, jour, moment):
    """(visuel, texte, description) — ou None si quoi que ce soit manque.

    🚩 ON VÉRIFIE QUE LES DEUX FICHIERS EXISTENT VRAIMENT, et pas seulement que
    la case du tableau est remplie. Le 02/09, quarante visuels ont été supprimés
    alors que le calendrier les nommait encore : il annonçait sept publications
    par semaine et six d'entre elles n'avaient plus d'image. Un tableau qui cite
    un fichier absent est un tableau qui a l'air juste jusqu'au jour J.
    """
    if entree is None:
        return None
    visuel, fichier, quoi = entree
    # 🔴 LE VISUEL EST-IL RETENU ? Ce contrôle passe AVANT tous les autres :
    # un visuel écarté n'a pas à être publiable même si ses fichiers existent.
    if visuel in RETENUS:
        print('⛔ %s %s : « %s » est RETENU et ne sera pas publié.\n   %s'
              % (JOURS[jour.weekday()], moment, quoi, RETENUS[visuel]),
              file=sys.stderr)
        return None
    texte = _lire(fichier)
    if texte is None or not (ICI / visuel).exists():
        manque = visuel if not (ICI / visuel).exists() else fichier
        print('⚠️  %s %s : « %s » est au programme mais %s est introuvable —'
              ' rien ne sera publié.' % (JOURS[jour.weekday()], moment, quoi,
                                         manque), file=sys.stderr)
        return None
    return visuel, texte, '%s — %s' % (JOURS[jour.weekday()], quoi)


def du_jour(jour=None):
    """(visuel, texte, description) pour la publication de midi, ou None."""
    jour = jour or datetime.date.today()
    return _valide(SEMAINE.get(jour.weekday()), jour, 'midi')


def du_matin(jour=None):
    """(visuel, texte, description) pour le matin, ou None si rien n'est prévu."""
    jour = jour or datetime.date.today()
    return _valide(MATIN.get(jour.weekday()), jour, 'matin')


if __name__ == '__main__':
    aujourdhui = datetime.date.today()
    print('Programme de la semaine :\n')
    vides = 0
    for n in range(7):
        j = aujourdhui + datetime.timedelta(days=n - aujourdhui.weekday())
        prevu = du_jour(j)
        if prevu is None:
            vides += 1
            print('%-12s —  rien au programme' % JOURS[j.weekday()])
            continue
        visuel, texte, quoi = prevu
        print('%-12s %-40s %s' % (JOURS[j.weekday()], visuel,
                                  texte.split('\n')[0][:44]))
    print('\nLes matins prévus : %s' % ('aucun — la démonstration est à refaire'
                                        if not MATIN else ''))
    print('\n+ le bulletin mer, tous les soirs (fabriqué le jour même).')
    if vides:
        print('\n⚠️  %d jour(s) sans visuel. Deux jours muets valent mieux'
              " qu'un visuel hors norme, mais c'est un chantier, pas une cible."
              % vides)
