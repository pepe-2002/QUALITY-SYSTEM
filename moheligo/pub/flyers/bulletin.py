#!/usr/bin/env python3
"""Fabrique le flyer du soir à partir de la VRAIE prévision de mer.

    python3 bulletin.py            # demain matin
    python3 bulletin.py --jour 2   # après-demain

Ce que fait le script :
  1. interroge Open-Meteo (API marine + API météo) sur le couloir
     Ouroveni ↔ Hoani (point milieu -12.08 / 43.54, fuseau Indian/Comoro) ;
  2. calcule la houle et le vent moyens de la tranche 6h-10h, l'état de la mer
     sur l'échelle de Douglas, et la courbe de houle 5h-13h ;
  3. remplit `flyer8-soir-fb.template.html` et écrit `flyer8-soir-fb.html` ;
  4. écrit aussi `bulletin.json` (utile pour le texte de la publication).

Ensuite :  node render.js flyer8-soir-fb.html flyer-soir-facebook.png 1080 1350 2

⚠️ Ce flyer est DATÉ : il annonce la mer d'un matin précis. Le régénérer le
jour même, ne jamais republier celui de la veille.
⚠️ Toujours garder la mention de source et le rappel que le bulletin officiel
fait foi : on publie une prévision, pas une garantie.
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone

LAT, LON = -12.08, 43.54          # milieu du couloir Ouroveni – Hoani
TZ = 'Indian%2FComoro'
CACERT = '/root/.ccr/ca-bundle.crt'

MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
        'août', 'septembre', 'octobre', 'novembre', 'décembre']
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

# échelle de Douglas, simplifiée aux cinq degrés utiles à une traversée
DOUGLAS = [
    (0.50, 'MER BELLE',      'Conditions idéales pour traverser.'),
    (1.25, 'MER PEU AGITÉE', 'Traversée normale, un peu de mouvement.'),
    (2.50, 'MER AGITÉE',     'Ça bouge : prévoyez, et suivez les consignes du commandant.'),
    (4.00, 'MER FORTE',      'Conditions dures : vérifiez le maintien des départs.'),
    (99.0, 'MER TRÈS FORTE', 'Traversée déconseillée : attendez le bulletin officiel.'),
]
LABELS = ['BELLE', 'PEU AGITÉE', 'AGITÉE', 'FORTE', 'TRÈS FORTE']
ROSE = ['nord', 'nord-est', 'est', 'sud-est', 'sud', 'sud-ouest', 'ouest', 'nord-ouest']


def api(url, essais=4):
    """Open-Meteo passe par le proxy de session : prévoir les coupures TLS."""
    dernier = ''
    for n in range(essais):
        out = subprocess.run(['curl', '-sS', '--max-time', '25', '--cacert', CACERT, url],
                             capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip():
            try:
                return json.loads(out.stdout)
            except json.JSONDecodeError as e:
                dernier = str(e)
        else:
            dernier = out.stderr.strip() or 'réponse vide'
        time.sleep(2 * (n + 1))
    sys.exit('Open-Meteo injoignable après %d essais : %s' % (essais, dernier))


def cardinal(deg):
    return ROSE[int((deg % 360) / 45 + .5) % 8]


def fr_date(d):
    return f'{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jour', type=int, default=1, help='1 = demain (défaut)')
    args = ap.parse_args()

    cible = date.today() + timedelta(days=args.jour)
    jours = args.jour + 1

    mer = api(f'https://marine-api.open-meteo.com/v1/marine?latitude={LAT}&longitude={LON}'
              f'&hourly=wave_height,wave_period&timezone={TZ}&forecast_days={jours}')
    vent = api(f'https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}'
               f'&hourly=wind_speed_10m,wind_direction_10m&timezone={TZ}&forecast_days={jours}')

    t = mer['hourly']['time']
    idx = {h: i for i, h in enumerate(t)}
    jour = cible.isoformat()

    def serie(source, cle, h0, h1):
        return [source['hourly'][cle][idx[f'{jour}T{h:02d}:00']]
                for h in range(h0, h1 + 1) if f'{jour}T{h:02d}:00' in idx]

    houle_matin = serie(mer, 'wave_height', 6, 10)
    periode_matin = serie(mer, 'wave_period', 6, 10)
    vent_matin = serie(vent, 'wind_speed_10m', 6, 10)
    dir_matin = serie(vent, 'wind_direction_10m', 6, 10)
    courbe = serie(mer, 'wave_height', 5, 13)
    if not houle_matin or not courbe:
        sys.exit('Pas de données pour ' + jour)

    houle = sum(houle_matin) / len(houle_matin)
    periode = sum(periode_matin) / len(periode_matin)
    v = sum(vent_matin) / len(vent_matin)
    dirv = cardinal(sum(dir_matin) / len(dir_matin))
    etat, conseil = next((n, c) for seuil, n, c in DOUGLAS if houle < seuil)
    niveau = next(i for i, (seuil, _, _) in enumerate(DOUGLAS) if houle < seuil)

    # --- courbe de houle : chemins SVG dans une boîte 908 x 104
    Wc, Hc, pad = 908, 116, 16
    lo, hi = min(courbe), max(courbe)
    if hi - lo < 0.25:                      # évite une courbe écrasée ou plate
        mid = (hi + lo) / 2
        lo, hi = mid - 0.15, mid + 0.15
    pts = []
    for i, val in enumerate(courbe):
        x = round(i * Wc / (len(courbe) - 1), 1)
        y = round(Hc - pad - (val - lo) / (hi - lo) * (Hc - 2 * pad), 1)
        pts.append((x, y))
    courbe_d = 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
    aire_d = f'{courbe_d} L{pts[-1][0]} {Hc} L{pts[0][0]} {Hc} Z'
    points = ''.join(
        f'<circle cx="{x}" cy="{y}" r="3.8" fill="#0B2149" stroke="#FBC93C" stroke-width="2.4"/>'
        for x, y in pts)
    # l'heure de départ la plus courante est repérée avec sa valeur
    ix = 2                                     # 5h + 2 = 7h
    px, py = pts[ix]
    val = f'{courbe[ix]:.1f}'.replace('.', ',')     # la virgule UNIQUEMENT ici :
    ty = py - 32 if py > 46 else py + 12            # jamais sur les coordonnées
    points += (
        f'<circle cx="{px}" cy="{py}" r="7" fill="#FBC93C" stroke="#0B2149" stroke-width="3"/>'
        f'<rect x="{px - 36}" y="{ty}" width="72" height="23" rx="7" fill="#FBC93C"/>'
        f'<text x="{px}" y="{ty + 16.5}" text-anchor="middle" '
        f'font-family="Archivo,Inter,sans-serif" font-size="13.5" font-weight="900" '
        f'fill="#0B2149">7h · {val} m</text>')
    heures = ''.join(f'<span>{h}h</span>' for h in range(5, 14))

    gauge = ''.join(f'<div class="{"on" if i <= niveau else ""}"></div>' for i in range(5))
    gauge_lab = ''.join(f'<span class="{"on" if i == niveau else ""}">{l}</span>'
                        for i, l in enumerate(LABELS))

    # heure des Comores (UTC+3), pas celle du serveur
    maj = datetime.now(timezone(timedelta(hours=3))).strftime('le %d/%m à %Hh%M')
    vals = {
        'OVER': f'BULLETIN MER · {fr_date(cible).upper()} · 6H-10H',
        'TITRE_BULLETIN': f'{fr_date(cible).upper()} MATIN',
        'ETAT': etat,
        'CONSEIL': conseil,
        'HOULE': f'{houle:.1f}'.replace('.', ','),
        'VENT': f'{v:.0f}',
        'DIRV': dirv.upper(),
        'PERIODE': f'{periode:.1f}'.replace('.', ','),
        'HMIN': f'{min(courbe):.1f}'.replace('.', ','),
        'HMAX': f'{max(courbe):.1f}'.replace('.', ','),
        'PLAGE': f'de {min(courbe):.1f} m à {max(courbe):.1f} m'.replace('.', ','),
        'COURBE': courbe_d, 'AIRE': aire_d, 'POINTS': points, 'HEURES': heures,
        'GAUGE': gauge, 'GAUGE_LAB': gauge_lab, 'MAJ': maj,
    }

    html = open('flyer8-soir-fb.template.html').read()
    for k, val in vals.items():
        html = html.replace('{{' + k + '}}', str(val))
    open('flyer8-soir-fb.html', 'w').write(html)

    json.dump({'date': jour, 'etat': etat, 'houle_m': round(houle, 2),
               'periode_s': round(periode, 1), 'vent_kmh': round(v),
               'vent_direction': dirv, 'courbe_5h_13h': courbe,
               'releve': maj, 'source': 'Open-Meteo Marine + Forecast'},
              open('bulletin.json', 'w'), ensure_ascii=False, indent=2)

    print(f'{fr_date(cible)} matin : {etat.lower()}, houle {houle:.2f} m, '
          f'vent {v:.0f} km/h {dirv}, période {periode:.1f} s')
    print('-> flyer8-soir-fb.html + bulletin.json')


if __name__ == '__main__':
    main()
