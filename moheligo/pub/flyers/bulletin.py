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
import os
import pathlib
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import service                                 # noqa: E402  (état du service)

LAT, LON = -12.08, 43.54          # milieu du couloir Ouroveni – Hoani
TZ = 'Indian%2FComoro'
# Le proxy de session impose son propre certificat ; sur GitHub ce fichier
# n'existe pas et curl refuse de démarrer (erreur 77). D'où le test d'existence.
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
        cmd = ['curl', '-sS', '--max-time', '25']
        if os.path.isfile(CACERT):
            cmd += ['--cacert', CACERT]
        out = subprocess.run(cmd + [url], capture_output=True, text=True)
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
    # tous les conseils de Douglas supposent qu'une vedette part : pendant une
    # fermeture, celui-ci est remplacé (service.py, une seule source de vérité)
    conseil = service.conseil_bulletin(conseil)
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

    # amplitude de la matinée. Quand la houle est régulière (ce qui arrive
    # souvent en saison sèche), l'arrondi au décimètre donnait « 0,9–0,9 m » :
    # ça ressemble à un bug alors que c'est une bonne nouvelle. On la nomme.
    hmin, hmax = f'{min(courbe):.1f}', f'{max(courbe):.1f}'
    virg = lambda s: s.replace('.', ',')
    if hmin == hmax:
        ampli = f'{virg(hmin)}<i>m</i>'
        ampli_lab = 'HOULE RÉGULIÈRE 5H-13H'
        plage = f'régulière, autour de {virg(hmin)} m'
    else:
        ampli = f'{virg(hmin)}–{virg(hmax)}<i>m</i>'
        ampli_lab = 'MATINÉE 5H-13H'
        plage = f'de {virg(hmin)} m à {virg(hmax)} m'

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
        'AMPLI': ampli, 'AMPLI_LAB': ampli_lab, 'PLAGE': plage,
        'COURBE': courbe_d, 'AIRE': aire_d, 'POINTS': points, 'HEURES': heures,
        'GAUGE': gauge, 'GAUGE_LAB': gauge_lab, 'MAJ': maj,
    }

    # --- le bandeau d'or dépend de l'état du service, pas de la mer ---------
    # Fermé, « RÉSERVE POUR DEMAIN » serait un mensonge imprimé sur un bulletin
    # par ailleurs exact. Le bulletin continue de partir (informer n'est pas
    # vendre, et c'est les jours sans traversée qu'il se remarque), mais il
    # n'appelle plus à réserver.
    cta_titre, cta_adr, cta_wa = service.cta_bulletin()
    vals.update({'CTA_TITRE': cta_titre, 'CTA_ADR': cta_adr, 'CTA_WA': cta_wa})

    html = open('flyer8-soir-fb.template.html').read()
    for k, val in vals.items():
        html = html.replace('{{' + k + '}}', str(val))
    open('flyer8-soir-fb.html', 'w').write(html)

    json.dump({'date': jour, 'etat': etat, 'houle_m': round(houle, 2),
               'periode_s': round(periode, 1), 'vent_kmh': round(v),
               'vent_direction': dirv, 'courbe_5h_13h': courbe,
               'releve': maj, 'source': 'Open-Meteo Marine + Forecast'},
              open('bulletin.json', 'w'), ensure_ascii=False, indent=2)

    # --- l'appel de fin, lui aussi suspendu quand le service l'est ----------
    if service.ouvert():
        appel = """Ta place pour demain se prend maintenant :
• Tu choisis ton départ sur moheligo.com
• Tu paies par MVola ou kartaPay
• Ton billet QR arrive tout de suite

moheligo.com — et demain matin, tu embarques tranquille."""
    else:
        # 🚩 30/08/2026 — CE BLOC NE DIT PLUS « JUSQU’À NOUVEL ORDRE » EN DUR.
        # Le patron a donné une date de reprise (prévue mardi). « Jusqu’à nouvel
        # ordre » resterait vrai au sens strict et FAUX au sens utile : on aurait
        # une nouvelle et on continuerait à dire qu’on n’en a pas. Le bulletin du
        # soir est le rendez-vous quotidien — c’est là que la nouvelle doit
        # tomber, pas dans un post commercial.
        # 📌 La phrase vient de `service.paragraphe_reprise()`, pas d’ici : une
        # date de reprise ne doit exister qu’à UN endroit dans tout le dépôt,
        # sinon on en corrige une et on en oublie trois (leçon du 26/08).
        appel = """⛔ RAPPEL : LES TRAVERSÉES SONT ENCORE SUSPENDUES CE SOIR.
On ne prend pas de réservation pour demain matin — et on continue à publier la
mer chaque soir, pour que tu voies le calme revenir en même temps que nous.

""" + service.paragraphe_reprise() + """

Si tu as un billet : changer la date est gratuit, et le remboursement est
possible tant que la traversée n’est pas partie. Écris-nous sur WhatsApp.

moheligo.com — WhatsApp +269 479 43 28"""

    # texte de publication prêt à copier, avec les chiffres du jour
    # le premier commentaire vit dans service.py, comme le bandeau : tout ce
    # qui promet une traversée doit suivre l’état du service
    commentaire = service.commentaire_bulletin()

    texte = f"""LA MER DE DEMAIN, CE SOIR.

Demain matin entre Ouroveni et Hoani : {etat.lower()}.
Houle {vals['HOULE']} m, vent {vals['VENT']} km/h de {dirv}, période {vals['PERIODE']} secondes.
{conseil}

C’est ça, MoheliGo : tu sais avant de quitter la maison.
La météo mer des 7 prochains jours est dans l’application, mise à jour en continu.

{appel}

Prévision Open-Meteo relevée {maj}. Le bulletin officiel affiché dans
l’application fait foi avant l’embarquement.

#MoheliGo #Mohéli #Comores #MétéoMer #Traversée #Ouroveni #Hoani

--- premier commentaire ---
{commentaire}
"""
    open('texte-du-jour.txt', 'w').write(texte)

    print(f'{fr_date(cible)} matin : {etat.lower()}, houle {houle:.2f} m, '
          f'vent {v:.0f} km/h {dirv}, période {periode:.1f} s')
    print('-> flyer8-soir-fb.html + bulletin.json + texte-du-jour.txt')


if __name__ == '__main__':
    main()
