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
EMPLOI = 'flyer-modedemploi-facebook.png'   # la démonstration : le matin
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
SEMAINE = {
    0: [(PROMO, TEXTE[T_APPLI]), (NUIT, TEXTE[T_APPLI])],
    1: [(AFFICHE, VISUEL[AFFICHE]), (LUMINEUSE, TEXTE[T_AFFICHE])],
    2: [(PROMO, VISUEL[PROMO]), (PRIX, VISUEL[PRIX])],
    3: [(DUOTONE, TEXTE[T_ABO]), (AFFICHE, TEXTE[T_ABO])],
    4: [(DIASPORA, VISUEL[DIASPORA]), (DIASPORA, VISUEL[DIASPORA])],
    5: [(LUMINEUSE, TEXTE[T_AFFICHE]), (DUOTONE, VISUEL[AFFICHE])],
    6: [(CORPORATE, TEXTE[T_INSTIT]), (CORPORATE, TEXTE[T_COURT])],
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
