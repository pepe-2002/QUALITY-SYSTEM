#!/usr/bin/env python3
"""Le programme de publication de la semaine MoheliGo.

Le patron (11/08/2026) : « pourquoi le bulletin du soir seulement ? c'est toi le
directeur marketing et commercial, tu vas tout gérer les pubs. » Donc voici le
calendrier complet, celui du plan publicitaire (`pub/plan-publicitaire.md`) :

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
    2: [(PROMO, VISUEL[PROMO]), (PROMO, VISUEL[PROMO])],
    3: [(DUOTONE, TEXTE[T_ABO]), (AFFICHE, TEXTE[T_ABO])],
    4: [(DIASPORA, VISUEL[DIASPORA]), (DIASPORA, VISUEL[DIASPORA])],
    5: [(LUMINEUSE, TEXTE[T_AFFICHE]), (DUOTONE, VISUEL[AFFICHE])],
    6: [(CORPORATE, TEXTE[T_INSTIT]), (CORPORATE, TEXTE[T_COURT])],
}

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
    print('\n+ le bulletin mer, tous les soirs (fabriqué le jour même).')
