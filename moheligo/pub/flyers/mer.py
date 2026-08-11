#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'état de la mer d'un jour donné, pour décider s'il faut publier ou se taire.

    python3 mer.py              # aujourd'hui
    python3 mer.py --jour 2026-08-15

Le patron, 11/08/2026 : « le départ tkt pas, mais en mauvais temps les vedettes
ne partent pas. »

C'est l'information la plus utile qu'il m'ait donnée sur le produit. Elle veut
dire deux choses :

1. Notre promesse est juste, à condition de la formuler exactement :
   **la mer décide, nous on te le dit avant.** Pas « la traversée est garantie ».
2. Les jours de grosse mer, une publicité enjouée n'est pas seulement inutile :
   elle est fausse. Elle invite à descendre au port un jour où la vedette peut
   ne pas partir. Une promesse non tenue coûte plus cher qu'une pub jamais
   publiée (§ 11 et § 14.2 du manuel).

D'où ce module : `programme.py` le consulte AVANT de publier, et remplace le
message commercial par un message honnête quand la mer est forte.

⚠️ CE QU'ON NE SAIT PAS, ET QU'ON N'INVENTERA PAS : le seuil exact auquel chaque
compagnie annule. Donc on n'écrit JAMAIS « les vedettes ne partent pas » — on
écrit « les vedettes peuvent ne pas partir, vérifie avant de descendre ». La
nuance est toute la différence entre informer et se tromper à voix haute.
"""

import argparse
import datetime
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import bulletin                                # noqa: E402  (api, DOUGLAS, LAT…)

# Le niveau de l'échelle de Douglas à partir duquel on arrête de vendre.
# 3 = MER FORTE (houle ≥ 2,50 m), le degré où le bulletin dit déjà
# « vérifiez le maintien des départs ». En dessous (mer agitée), la traversée
# est normale et il n'y a aucune raison de se taire.
SEUIL_GROS_TEMPS = 3


def niveau(jour=None, heures=(6, 10)):
    """(niveau, état, houle_m) pour la fenêtre du matin, ou None si injoignable.

    None ne veut pas dire « beau temps » : ça veut dire « je ne sais pas ».
    C'est à l'appelant de décider quoi faire de l'ignorance — voir programme.py.
    """
    jour = jour or datetime.date.today()
    j = jour.isoformat()
    try:
        mer = bulletin.api(
            'https://marine-api.open-meteo.com/v1/marine'
            f'?latitude={bulletin.LAT}&longitude={bulletin.LON}'
            f'&hourly=wave_height&timezone={bulletin.TZ}&start_date={j}&end_date={j}',
            essais=2)
    except SystemExit:
        # bulletin.api sort du programme quand l'API ne répond pas : ici, une
        # météo indisponible ne doit pas tuer la publication du jour.
        return None

    t = mer.get('hourly', {}).get('time') or []
    h = mer.get('hourly', {}).get('wave_height') or []
    idx = {x: i for i, x in enumerate(t)}
    valeurs = [h[idx[f'{j}T{n:02d}:00']] for n in range(heures[0], heures[1] + 1)
               if f'{j}T{n:02d}:00' in idx and h[idx[f'{j}T{n:02d}:00']] is not None]
    if not valeurs:
        return None

    houle = sum(valeurs) / len(valeurs)
    n = next(i for i, (seuil, _, _) in enumerate(bulletin.DOUGLAS) if houle < seuil)
    return n, bulletin.DOUGLAS[n][1], round(houle, 2)


def gros_temps(jour=None):
    """True si la mer est forte, False si elle ne l'est pas, None si on ne sait pas."""
    r = niveau(jour)
    if r is None:
        return None
    return r[0] >= SEUIL_GROS_TEMPS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jour', help='AAAA-MM-JJ, par défaut aujourd\'hui')
    a = ap.parse_args()
    jour = datetime.date.fromisoformat(a.jour) if a.jour else datetime.date.today()

    r = niveau(jour)
    if r is None:
        print('Mer du %s : INCONNUE (Open-Meteo injoignable).' % jour.isoformat())
        return
    n, etat, houle = r
    print('Mer du %s : %s — houle %.2f m au matin (niveau %d/4).'
          % (jour.isoformat(), etat, houle, n))
    print('Gros temps :', 'OUI — on ne vend pas aujourd\'hui.' if n >= SEUIL_GROS_TEMPS
          else 'non — publication commerciale normale.')


if __name__ == '__main__':
    main()
