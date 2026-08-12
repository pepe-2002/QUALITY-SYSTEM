#!/usr/bin/env python3
"""Le rapport MoheliGo — ce qui a été publié, ce que ça a donné, et la décision.

    python3 rapport.py                 # affiche le rapport et écrit RAPPORT.md
    python3 rapport.py --jours 7       # sur les 7 derniers jours (défaut)

Commande du patron (11/08/2026) : « je veux des rapports, au début il m'en faut
beaucoup pour pouvoir améliorer ».

Ce que ce rapport sait tout seul :
  · les publications réellement parties (journal-publications.json)
  · le nombre d'abonnés de la page (API Graph, lecture seule)
  · la mer annoncée le jour même (bulletin.json)

Ce qu'il ne peut PAS savoir, et qu'il réclame donc explicitement au patron :
  · les réservations payées
  · les visites du site
  · l'abandon au paiement
  → Ce sont les trois chiffres du plan (`dossier/PLAN-PUBLICITAIRE.md`) qui décident
    s'il faut dépenser plus ou réparer. Un rapport qui les invente ne sert à rien.

⚠️ Règle du manuel (§ checklists) : un rapport commence par LA DÉCISION à
prendre, pas par la liste des actions. C'est pour ça que la conclusion est en
haut.
"""
import argparse
import json
import os
import pathlib
import sys
from datetime import date, datetime, timedelta, timezone

ICI = pathlib.Path(__file__).parent
COMORES = timezone(timedelta(hours=3))
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
        'août', 'septembre', 'octobre', 'novembre', 'décembre']
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']


def fr(d):
    return f'{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}'


def lire(nom, defaut):
    try:
        return json.loads((ICI / nom).read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return defaut


def abonnes():
    """Lecture seule, et tolérante : un rapport ne doit jamais échouer pour ça."""
    page = os.environ.get('FB_PAGE_ID', '').strip()
    jeton = os.environ.get('FB_PAGE_TOKEN', '').strip()
    if not (page and jeton):
        return None
    sys.path.insert(0, str(ICI))
    import publier_fb
    # ⚠️ UN SEUL champ invalide fait rejeter TOUT l'appel chez Facebook. Donc un
    # champ par appel, et on garde le premier qui répond. (Piège déjà rencontré
    # le 11/08 sur followers_count — ne pas le repayer une troisième fois.)
    for champ in ('followers_count', 'fan_count'):
        rep = publier_fb.curl(f'{publier_fb.BASE}/{page}?fields={champ}',
                              jeton=jeton, strict=False)
        if champ in rep:
            return rep[champ]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jours', type=int, default=7)
    a = ap.parse_args()

    maintenant = datetime.now(COMORES)
    depuis = (maintenant - timedelta(days=a.jours)).isoformat(timespec='minutes')

    journal = [p for p in lire('journal-publications.json', []) if p.get('quand', '') >= depuis]
    bulletin = lire('bulletin.json', {})
    abo = abonnes()

    # --- la décision d'abord, comme l'exige le manuel
    if not journal:
        decision = ('**Rien n\'a été publié sur la période.** Tant que la page ne '
                    'reçoit rien, aucun chiffre ne peut bouger : c\'est le seul '
                    'point à régler avant tout le reste.')
    elif len(journal) < a.jours:
        decision = (f'**Le rythme n\'est pas tenu** : {len(journal)} publications '
                    f'en {a.jours} jours. Le bulletin du soir est le seul contenu '
                    'qui crée une habitude — un soir manqué casse le rendez-vous.')
    else:
        decision = (f'**Le rythme est tenu** ({len(journal)} publications en '
                    f'{a.jours} jours). La question devient : est-ce que ça se '
                    'transforme en réservations ? Il me manque les chiffres du bas.')

    L = []
    L.append(f'# Rapport MoheliGo — {fr(maintenant.date())}')
    L.append(f'\n_Période : {a.jours} derniers jours. Relevé à '
             f'{maintenant.strftime("%Hh%M")}, heure des Comores._')
    L.append('\n## La décision\n\n' + decision)

    L.append('\n## Ce qui est parti sur la page\n')
    if journal:
        L.append('| Quand | Visuel | Accroche |')
        L.append('|---|---|---|')
        for p in journal:
            quand = p['quand'].replace('T', ' à ')[:16]
            L.append(f"| {quand} | `{p.get('visuel','—')}` | {p.get('accroche','—')} |")
    else:
        L.append('_Aucune publication enregistrée._')

    L.append('\n## Ce que je peux mesurer seul\n')
    L.append(f"- **Abonnés de la page** : {abo if abo is not None else '_non lisible (jeton sans permission de lecture)_'}")
    L.append(f"- **Publications sur la période** : {len(journal)}")
    if bulletin:
        L.append(f"- **Dernier bulletin fabriqué** : {bulletin.get('date','?')} — "
                 f"{bulletin.get('etat','?').lower()}, houle {bulletin.get('houle_m','?')} m, "
                 f"vent {bulletin.get('vent_kmh','?')} km/h {bulletin.get('vent_direction','')}")

    L.append('\n## 🔴 Les trois chiffres qu\'il me faut, et que je ne peux pas deviner\n')
    L.append('| Chiffre | Où le trouver | Pourquoi il décide |')
    L.append('|---|---|---|')
    L.append('| **Réservations payées** | ton back-office MoheliGo | c\'est le seul résultat qui compte |')
    L.append('| **Visites du site** | statistiques Cloudflare | mesure si la pub amène du monde |')
    L.append('| **Abandon au paiement** | commencées − finies | si c\'est haut, on arrête la pub et on répare |')
    L.append('\n⚠️ Sans le troisième, on risque de payer pour remplir un seau percé — '
             'c\'est la faute la plus chère du métier (manuel, § 8).')

    L.append('\n## Ce que je propose pour la suite\n')
    if not journal:
        L.append('1. Armer la publication du bulletin du soir : c\'est lui qui fait s\'abonner.')
        L.append('2. Laisser les visuels promo de côté jusqu\'aux images du patron.')
    else:
        L.append('1. Tenir le bulletin chaque soir sans exception : le rendez-vous vaut plus que le contenu.')
        L.append('2. Me donner les trois chiffres ci-dessus, une fois par semaine, le dimanche.')
        L.append('3. Ne rien dépenser en publicité avant de connaître l\'abandon au paiement.')

    texte = '\n'.join(L) + '\n'
    (ICI.parent / 'RAPPORT.md').write_text(texte)
    print(texte)
    print('-> écrit dans moheligo/pub/RAPPORT.md')


if __name__ == '__main__':
    main()
