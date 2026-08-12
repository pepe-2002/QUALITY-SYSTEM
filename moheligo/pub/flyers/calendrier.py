#!/usr/bin/env python3
"""Le programme de publication de la semaine MoheliGo.

Le patron (11/08/2026) : « pourquoi le bulletin du soir seulement ? c'est toi le
directeur marketing et commercial, tu vas tout gérer les pubs. » Donc voici le
calendrier complet, celui du plan publicitaire (`dossier/PLAN-PUBLICITAIRE.md`) :

    tous les soirs   le bulletin mer          (daté, fabriqué le jour même)
    lundi            comment ça marche
    mardi            l'île, registre émotion
    mercredi         les prix
    jeudi            s'abonner à la page
    vendredi         la diaspora              (jour de paie en Europe)
    samedi           la destination
    dimanche         l'institutionnel

⚠️ **Une seule source de vérité** : les visuels et les textes viennent de
`page.py` (listes `FLYERS` et `TEXTES`), la même chose que ce que le patron voit
sur sa page. Rien n'est recopié ici — sinon les deux finiraient par se
contredire.

⚠️ **L'usure est le vrai risque.** Sept publications par semaine tirées de
quatre visuels, ça se voit au bout de quinze jours. D'où deux choses : chaque
jour a **plusieurs variantes** et on tourne selon le numéro de semaine ; et il
faut continuer à produire des visuels neufs. Un calendrier automatique ne
remplace pas une bibliothèque qui grandit.
"""
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import page                                   # noqa: E402  (FLYERS, TEXTES)

JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

# --- les briques disponibles, retrouvées dans page.py -----------------------
VISUEL = {f['png']: f['texte'] for f in page.FLYERS}
TEXTE = {t['titre']: t['texte'] for t in page.TEXTES}

AFFICHE = 'flyer-affiche-vraie-facebook.png'
DIASPORA = 'flyer-diaspora-facebook.png'
PROMO = 'flyer-promo-brillant-facebook.png'
PRIX = 'flyer-prix-facebook.png'         # le billet : mercredi, jour des prix
EMPLOI = 'flyer-modedemploi-v2-facebook.png'   # la démonstration du matin (V2)
EMPLOI_V1 = 'flyer-modedemploi-facebook.png'   # V1, gardée pour l'impression papier
# --- la série du 12/08/2026 : un visuel par jour, tous dans le même système ---
# Le patron : « fais tous les flyers jusqu'à mardi, mets-les dans le robot, la
# limite de la semaine sera bientôt atteinte. » Donc la semaine complète est
# désormais couverte par des visuels de la même famille (coin blanc, aplat
# marine, carte claire, bandeau d'or), sans dépendre de moi.
ABONNER = 'flyer-abonner-facebook.png'          # jeudi
DIASPORA_V2 = 'flyer-diaspora-v2-facebook.png'  # vendredi
DESTINATION = 'flyer-destination-facebook.png'  # samedi
INSTIT = 'flyer-institutionnel-facebook.png'    # dimanche
PARTENARIAT = 'flyer-partenariat-facebook.png'  # dimanche, l'autre semaine
RIEN = 'flyer-rien-installer-facebook.png'      # lundi
SIGNATURE = 'flyer-signature-facebook.png'      # mardi (déjà validé par le patron)
# visuels présents dans le dossier mais pas sur la page du patron
DUOTONE = 'flyer-affiche-duotone-facebook.png'
LUMINEUSE = 'flyer-affiche-lumineuse-facebook.png'
CORPORATE = 'flyer-corporate-facebook.png'
NUIT = 'flyer-nuit-facebook.png'

T_APPLI = "Pour faire utiliser l'application"
T_ABO = "Pour faire s'abonner à la page"
T_INSTIT = 'Texte institutionnel — « grand conglomérat »'
T_COURT = 'Version très courte, même registre'
T_AFFICHE = "Variante courte pour l'affiche"

# --- le programme : jour de la semaine -> variantes (visuel, texte) ---------
# On tourne d'une variante à l'autre selon le numéro de semaine ISO.
# ⚠️ UNE SEULE VARIANTE PAR JOUR, ET C'EST VOULU (12/08/2026).
# La rotation par numéro de semaine existait pour lutter contre l'usure, mais
# elle tirait une semaine sur deux dans l'ANCIENNE bibliothèque — des visuels
# d'avant le système actuel (pas de coin blanc, pas de carte claire, pas de QR).
# Publier un visuel hors système une semaine sur deux abîme la marque plus que
# l'usure ne la fatigue : la régularité EST l'actif (§ 1 du manuel).
# La deuxième variante revient au fur et à mesure que la bibliothèque grandit
# DANS le système. Premier retour le 12/08/2026 : le dimanche alterne
# institutionnel et partenariat Young Leader — deux visuels de la même famille,
# même registre (partenaires, vouvoiement), donc l'alternance repose la page sans
# abîmer la marque. C'est la condition, et la seule : jamais un visuel d'avant le
# système.
SEMAINE = {
    0: [(RIEN, VISUEL[RIEN])],                  # lundi : rien à installer
    1: [(SIGNATURE, VISUEL[SIGNATURE])],        # mardi : l'île, registre émotion
    2: [(PRIX, VISUEL[PRIX])],                  # mercredi : les prix
    3: [(ABONNER, VISUEL[ABONNER])],            # jeudi : s'abonner
    4: [(DIASPORA_V2, VISUEL[DIASPORA_V2])],    # vendredi : la diaspora
    5: [(DESTINATION, VISUEL[DESTINATION])],    # samedi : la destination
    6: [(INSTIT, VISUEL[INSTIT]),               # dimanche : l'institutionnel
        (PARTENARIAT, VISUEL[PARTENARIAT])],    #   et, l'autre semaine, le partenariat
}

# --- LE MATIN : la démonstration, et rien d'autre --------------------------
# Le patron (11/08/2026) : « on peut pas ajouter un flyer ou vidéo de
# démonstration le matin ? » Oui — le matin est le bon moment : c'est là qu'on
# décide de descendre au port. Mais PAS tous les jours.
#
# Pourquoi pas tous les jours, écrit noir sur blanc pour ne pas y revenir :
# publier trois fois par jour sur une page jeune ne multiplie pas la portée, ça
# la divise entre les publications, et ça fatigue les abonnés — or un
# désabonnement se récupère beaucoup plus difficilement qu'une portée faible.
# Donc on commence à DEUX matins par semaine, on mesure dans le rapport du
# dimanche, et on décide avec les chiffres (§ 8 et § 16 du manuel).
#
# Le matin ne parle jamais du prix ni de l'île : il parle du GESTE. C'est un
# déclencheur « facilitateur » (§ 13.1 du manuel), destiné à celui qui a envie
# mais qui est bloqué. Une seule idée, un seul appel.
MATIN = {
    0: [(EMPLOI, VISUEL[EMPLOI])],           # lundi : on commence la semaine
    3: [(EMPLOI, VISUEL[EMPLOI])],           # jeudi : avant le week-end
}


def du_matin(jour=None):
    """(visuel, texte, description) pour le matin, ou None si rien n'est prévu."""
    jour = jour or datetime.date.today()
    i = jour.weekday()
    if i not in MATIN:
        return None
    variantes = MATIN[i]
    visuel, texte = variantes[jour.isocalendar()[1] % len(variantes)]
    return visuel, texte, '%s matin — la démonstration' % JOURS[i]


# Ce que le calendrier annonce, pour l'afficher sans publier.
INTENTION = ['comment ça marche', "l'île", 'les prix', 's'"'"'abonner à la page',
             'la diaspora', 'la destination', "l'institutionnel"]


def du_jour(jour=None):
    """(visuel, texte, description) pour la publication de midi de ce jour."""
    jour = jour or datetime.date.today()
    i = jour.weekday()
    variantes = SEMAINE[i]
    choix = variantes[jour.isocalendar()[1] % len(variantes)]
    visuel, texte = choix
    return visuel, texte, '%s — %s' % (JOURS[i], INTENTION[i])


if __name__ == '__main__':
    aujourdhui = datetime.date.today()
    print('Programme de la semaine (variante de la semaine ISO %d) :\n'
          % aujourdhui.isocalendar()[1])
    for n in range(7):
        j = aujourdhui + datetime.timedelta(days=n - aujourdhui.weekday())
        visuel, texte, quoi = du_jour(j)
        print('%-30s %-42s %s' % (quoi, visuel, texte.split('\n')[0][:44]))
    print('\nLes matins prévus (démonstration, 7h30) :\n')
    for n in range(7):
        j = aujourdhui + datetime.timedelta(days=n - aujourdhui.weekday())
        m = du_matin(j)
        if m:
            print('  %-12s %-42s %s' % (JOURS[j.weekday()], m[0],
                                        m[1].splitlines()[0][:44]))
    print('\n+ le bulletin mer, tous les soirs (fabriqué le jour même).')
