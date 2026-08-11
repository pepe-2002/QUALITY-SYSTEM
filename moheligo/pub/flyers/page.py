#!/usr/bin/env python3
"""Construit la page web que le patron ouvre pour récupérer ses flyers.

    python3 page.py                    # écrit page-flyers.html
    python3 page.py --sortie /tmp/x.html

Pourquoi ce script existe : les pièces jointes ne s'affichent pas chez le
patron. Le seul canal qui marche est une page web publiée (artifact), toujours
à la même adresse. Elle était retouchée à la main à chaque fois — et une
retouche a fini par effacer deux blocs. Désormais la page est REGÉNÉRÉE
entièrement, jamais rapiécée.

Elle contient : la météo de demain (Open-Meteo, terre + mer), puis chaque flyer
en grand avec son texte de publication et un bouton pour le copier.
Tout est embarqué en base64 : aucune requête réseau à l'ouverture.
"""
import argparse
import base64
import json
import pathlib
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone

from PIL import Image

LAT_MER, LON_MER = -12.08, 43.54        # couloir Ouroveni – Hoani
LAT_TERRE, LON_TERRE = -12.28, 43.74    # Fomboni
CACERT = '/root/.ccr/ca-bundle.crt'
TZ = 'Indian%2FComoro'
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
        'août', 'septembre', 'octobre', 'novembre', 'décembre']
JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
CIEL = {0: 'Ciel dégagé', 1: 'Peu nuageux', 2: 'Partiellement nuageux', 3: 'Couvert',
        45: 'Brouillard', 51: 'Pluie fine', 53: 'Pluie fine', 55: 'Pluie fine dense',
        61: 'Pluie faible', 63: 'Pluie modérée', 65: 'Forte pluie',
        80: 'Averses', 81: 'Averses', 82: 'Fortes averses', 95: 'Orage'}

# Les flyers de la page, dans l'ordre d'affichage.
# (fichier PNG, titre, note, fichier texte ou None si le texte est ici)
FLYERS = [
    dict(png='flyer-affiche-lumineuse-facebook.png', titre="L'affiche MOHÉLI",
         note='Sans date<br>publiable quand vous voulez', texte="""MOHÉLI, À UNE TRAVERSÉE.

Les îlots de Nioumachoua, vus de la plage, un matin sans vent.

Pour y être, il suffit de traverser. Et la traversée se réserve depuis votre
téléphone, en deux minutes :

• Ouroveni ou Chindini au départ, Hoani ou Fomboni à l'arrivée.
• Paiement MVola ou KartaPay, billet QR immédiat.
• L'état de la mer sur 7 jours, consulté avant de partir.

moheligo.com

Photo : Fatima771 (CC BY 3.0, Wikimedia Commons)

#MoheliGo #Mohéli #Nioumachoua #Comores #VisitComoros #Traversée"""),
    dict(png='flyer-soir-facebook.png', titre='Le bulletin du soir',
         note='Annonce demain matin<br>bon pour ce soir seulement', texte='@texte-du-jour.txt'),
    dict(png='flyer-diaspora-facebook.png', titre='Pour la diaspora',
         note='Sans date<br>plutôt le week-end', texte="""TU PAIES ICI. IL EMBARQUE.

Tu es en France, à Mayotte ou dans le Golfe, et ta famille doit traverser
vers Mohéli ?

Depuis ton téléphone, sur moheligo.com :

• Tu choisis le port, la date et la place.
• Tu paies par MVola ou KartaPay.
• Ton proche reçoit son billet QR sur son téléphone. Il n'avance rien.

À partir de 15 000 FC la traversée.

moheligo.com — la place est prise avant même que tu raccroches.

#MoheliGo #DiasporaComorienne #Comores #Mohéli #Mayotte"""),
    dict(png='flyer-promo-brillant-facebook.png', titre='Le promo',
         note='Sans date<br>le plus accrocheur', texte="""TA TRAVERSÉE EN 2 MINUTES.

Plus besoin d'aller au port pour savoir s'il y a une place.
Tu ouvres moheligo.com, tu choisis ton départ, tu paies par MVola.
Ton billet QR arrive tout de suite dans ton téléphone.

À partir de 15 000 FC le trajet.
Ouroveni et Chindini vers Hoani et Fomboni.

Réserve maintenant : moheligo.com
Une question ? WhatsApp +269 479 43 28

#MoheliGo #Mohéli #Comores #Traversée"""),
]


# Textes sans image : à copier tels quels dans une publication Facebook.
TEXTES = [
    dict(titre="Pour faire s'abonner à la page", texte="""POURQUOI S'ABONNER À CETTE PAGE ?

Parce qu'ici, chaque soir, vous trouverez la mer du lendemain matin sur le
trajet Grande Comore – Mohéli : hauteur de houle, vent, et un verdict clair —
mer belle, peu agitée, agitée.

Vous y trouverez aussi :
• les départs et les places qui restent ;
• les alertes quand la mer tourne mal, publiées la veille et pas le matin
  au port ;
• Mohéli comme elle est : les îlots, les tortues d'Itsamia, les baleines
  en saison.

Ce n'est pas une page de publicité. C'est le bulletin de la traversée.

Appuyez sur « S'abonner », et vous ne partirez plus à l'aveugle.

moheligo.com — réservation, billet QR, météo mer 7 jours.

#MoheliGo #Comores #Mohéli #MétéoMer #Traversée"""),

    dict(titre="Pour faire utiliser l'application", texte="""VOUS N'AVEZ RIEN À INSTALLER.

MoheliGo s'ouvre dans le navigateur de votre téléphone. Pas de boutique
d'applications, pas de mise à jour, pas de mémoire prise pour rien.

La première fois, ça prend deux minutes :

1. Ouvrez moheligo.com.
2. Choisissez votre port de départ, la date, le nombre de places.
3. Payez par MVola ou KartaPay.
4. Votre billet QR arrive aussitôt — et il reste dans votre téléphone, même
   sans connexion.

Une fois à l'intérieur, vous avez aussi la météo mer sur 7 jours, le suivi de
la vedette en direct pendant la traversée, le guide de l'île, et l'assistance
WhatsApp si quelque chose bloque.

Un conseil : ajoutez moheligo.com à l'écran d'accueil de votre téléphone.
Ça devient une icône, exactement comme une application.

moheligo.com — et la prochaine fois, votre place est prise avant d'arriver
au port.

#MoheliGo #Comores #Mohéli #BilletQR #MVola"""),

    dict(titre="Variante courte pour l'affiche", texte="""Un matin, la mer est plate. L'île est en face.
Il ne manque qu'une place.

moheligo.com — deux minutes, billet QR, paiement MVola.

#MoheliGo #Mohéli #Comores"""),
]


def api(url, essais=4):
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
    sys.exit('Open-Meteo injoignable : ' + dernier)


def virgule(x, n=1):
    return f'{x:.{n}f}'.replace('.', ',')


def meteo_demain(cible):
    """Quatre lignes lisibles : la mer, le matin, l'après-midi, le soir."""
    jour = cible.isoformat()
    mer = api(f'https://marine-api.open-meteo.com/v1/marine?latitude={LAT_MER}&longitude={LON_MER}'
              f'&hourly=wave_height&timezone={TZ}&forecast_days=2')
    ter = api(f'https://api.open-meteo.com/v1/forecast?latitude={LAT_TERRE}&longitude={LON_TERRE}'
              f'&hourly=temperature_2m,precipitation_probability,weather_code'
              f'&daily=weather_code&timezone={TZ}&forecast_days=2')
    hi = {h: i for i, h in enumerate(ter['hourly']['time'])}
    hm = {h: i for i, h in enumerate(mer['hourly']['time'])}

    def t(h):  return ter['hourly']['temperature_2m'][hi[f'{jour}T{h:02d}:00']]
    def pl(h): return ter['hourly']['precipitation_probability'][hi[f'{jour}T{h:02d}:00']]
    def co(h): return CIEL.get(ter['hourly']['weather_code'][hi[f'{jour}T{h:02d}:00']], '—')

    houle = [mer['hourly']['wave_height'][hm[f'{jour}T{h:02d}:00']] for h in range(6, 11)]
    h_moy = sum(houle) / len(houle)
    etat = ('Belle' if h_moy < .5 else 'Peu agitée' if h_moy < 1.25
            else 'Agitée' if h_moy < 2.5 else 'Forte')
    apm = max(range(12, 18), key=pl)
    return [
        ('Mer', etat, f'houle {virgule(h_moy)} m au petit matin'),
        ('Matin', co(6), f'{t(6):.0f} °C à 6h, {t(9):.0f} °C à 9h'),
        ('Après-midi', co(15), f'risque de pluie {pl(apm)} % vers {apm}h · {t(12):.0f} °C'),
        ('Soir', co(18), f'{t(18):.0f} °C à 18h, {t(21):.0f} °C à 21h'),
    ]


def b64(chemin):
    return base64.b64encode(pathlib.Path(chemin).read_bytes()).decode()


def jpeg_leger(png, largeur=1080):
    """Le patron est sur un téléphone : on embarque du JPEG, pas du PNG de 2,6 Mo."""
    tmp = pathlib.Path('/tmp') / (pathlib.Path(png).stem + '-page.jpg')
    im = Image.open(png).convert('RGB')
    im = im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS)
    im.save(tmp, quality=88, optimize=True)
    return b64(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sortie', default='page-flyers.html')
    args = ap.parse_args()

    maintenant = datetime.now(timezone(timedelta(hours=3)))
    demain = maintenant.date() + timedelta(days=1)
    fr = lambda d: f'{JOURS[d.weekday()]} {d.day} {MOIS[d.month - 1]}'

    lignes = ''.join(
        f'<div class="ligne"><span class="q">{q}</span><span class="v">{v}</span>'
        f'<span class="d">{d}</span></div>' for q, v, d in meteo_demain(demain))

    blocs = ''
    for i, f in enumerate(FLYERS, start=1):
        texte = (pathlib.Path(f['texte'][1:]).read_text().split('--- premier commentaire ---')[0].strip()
                 if f['texte'].startswith('@') else f['texte'])
        blocs += f'''
  <section class="bloc">
    <div class="tete"><b>{f['titre']}</b><span>{f['note']}</span></div>
    <img class="shot" src="data:image/jpeg;base64,{jpeg_leger(f['png'])}" alt="{f['titre']} MoheliGo">
    <p class="howto"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 11l5 5 5-5M4 20h16"/></svg>
      Appui long sur l'image, puis « Enregistrer » ou « Ajouter aux photos ».</p>
    <details><summary>Le texte du post</summary>
      <pre>{texte}</pre>
      <button class="copie" data-cible="t{i}">Copier le texte</button>
      <textarea id="t{i}" hidden>{texte}</textarea>
    </details>
  </section>
'''

    n = len(FLYERS)
    for j, t in enumerate(TEXTES, start=n + 1):
        blocs += f'''
  <section class="bloc">
    <div class="tete"><b>{t['titre']}</b><span>Texte seul<br>sans image</span></div>
    <details open><summary>Le texte</summary>
      <pre>{t['texte']}</pre>
      <button class="copie" data-cible="t{j}">Copier le texte</button>
      <textarea id="t{j}" hidden>{t['texte']}</textarea>
    </details>
  </section>
'''

    html = GABARIT.format(
        arch=b64('fonts/Archivo-800-latin.woff2'),
        in5=b64('fonts/Inter-500-latin.woff2'),
        in7=b64('fonts/Inter-700-latin.woff2'),
        embleme=b64('logo-emblem.png'),
        titre_jour=f'Demain, {fr(demain)}',
        releve=f"Relevé {fr(maintenant.date())} à {maintenant.strftime('%Hh%M')}, heure des Comores",
        lignes=lignes, blocs=blocs)
    pathlib.Path(args.sortie).write_text(html)
    print(args.sortie, round(len(html) / 1024), 'ko —', len(FLYERS), 'flyers,',
          len(TEXTES), 'textes')


GABARIT = '''<title>MoheliGo — la météo de demain et les flyers</title>
<style>
@font-face {{ font-family:'Archivo'; font-weight:800; font-display:swap;
  src:url(data:font/woff2;base64,{arch}) format('woff2'); }}
@font-face {{ font-family:'Inter'; font-weight:500; font-display:swap;
  src:url(data:font/woff2;base64,{in5}) format('woff2'); }}
@font-face {{ font-family:'Inter'; font-weight:700; font-display:swap;
  src:url(data:font/woff2;base64,{in7}) format('woff2'); }}

:root {{
  --ground:#F4F7FC; --card:#FFFFFF; --ink:#0F2A5C; --ink-soft:#5C6E8B;
  --line:#DCE4F1; --gold:#F6BC1C; --gold-ink:#5B4508; --btn:#0F2A5C;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --ground:#071630; --card:#0E2145; --ink:#EAF1FD; --ink-soft:#9FB6D8;
    --line:#1E3766; --gold:#F6BC1C; --gold-ink:#3A2B03; --btn:#1B4A8E;
  }}
}}
:root[data-theme="dark"] {{
  --ground:#071630; --card:#0E2145; --ink:#EAF1FD; --ink-soft:#9FB6D8;
  --line:#1E3766; --gold:#F6BC1C; --gold-ink:#3A2B03; --btn:#1B4A8E;
}}

* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--ground); color:var(--ink);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; font-weight:500;
  line-height:1.55; -webkit-font-smoothing:antialiased; }}
.wrap {{ max-width:560px; margin:0 auto; padding:26px 18px 56px; display:flex;
  flex-direction:column; gap:30px; }}
header {{ display:flex; align-items:center; gap:14px; }}
header img {{ width:50px; height:auto; display:block; }}
header b {{ font-family:'Archivo',sans-serif; font-weight:800; font-size:20px; letter-spacing:-.4px;
  display:block; line-height:1.15; }}
header span {{ display:block; font-size:13.5px; color:var(--ink-soft); }}

.bloc {{ background:var(--card); border:1px solid var(--line); border-radius:16px; overflow:hidden; }}
.tete {{ display:flex; align-items:baseline; justify-content:space-between; gap:12px;
  padding:16px 18px 14px; border-bottom:1px solid var(--line); }}
.tete b {{ font-family:'Archivo',sans-serif; font-weight:800; font-size:17px; letter-spacing:-.2px; }}
.tete span {{ font-size:13px; color:var(--ink-soft); text-align:right; }}

.ligne {{ display:grid; grid-template-columns:92px 1fr; gap:2px 12px; padding:13px 18px;
  border-bottom:1px solid var(--line); }}
.ligne:last-child {{ border-bottom:0; }}
.ligne .q {{ grid-row:span 2; font-size:12.5px; font-weight:700; letter-spacing:.6px;
  text-transform:uppercase; color:var(--ink-soft); padding-top:3px; }}
.ligne .v {{ font-family:'Archivo',sans-serif; font-weight:800; font-size:18px; }}
.ligne .d {{ font-size:14px; color:var(--ink-soft); }}

img.shot {{ width:100%; height:auto; display:block; }}
.howto {{ display:flex; gap:11px; align-items:flex-start; margin:0; padding:15px 18px;
  background:var(--gold); color:var(--gold-ink); font-size:14.5px; font-weight:700; }}
.howto svg {{ flex:none; margin-top:1px; }}

details {{ border-top:1px solid var(--line); }}
details[open] summary {{ border-bottom:1px solid var(--line); margin-bottom:14px; }}
summary {{ padding:15px 18px; font-size:15px; font-weight:700; cursor:pointer; list-style:none;
  display:flex; justify-content:space-between; align-items:center; gap:10px; }}
summary::-webkit-details-marker {{ display:none; }}
summary::after {{ content:'+'; font-family:'Archivo',sans-serif; font-size:20px; color:var(--ink-soft); }}
details[open] summary::after {{ content:'\\2013'; }}
summary:focus-visible {{ outline:3px solid var(--gold); outline-offset:-3px; }}
pre {{ margin:0; padding:0 18px 18px; white-space:pre-wrap; word-wrap:break-word;
  font-family:inherit; font-size:14.5px; line-height:1.6; }}
.copie {{ margin:0 18px 18px; padding:13px 18px; width:calc(100% - 36px);
  font-family:'Archivo',sans-serif; font-weight:800; font-size:15px; color:#fff;
  background:var(--btn); border:0; border-radius:999px; cursor:pointer; }}
.copie:focus-visible {{ outline:3px solid var(--gold); outline-offset:2px; }}
footer {{ font-size:14px; color:var(--ink-soft); border-top:1px solid var(--line); padding-top:20px; }}
footer b {{ color:var(--ink); }}
</style>

<div class="wrap">
  <header>
    <img src="data:image/png;base64,{embleme}" alt="">
    <div><b>{titre_jour}</b><span>{releve}</span></div>
  </header>

  <section class="bloc">
    <div class="tete"><b>La météo de demain</b><span>Mohéli et le couloir<br>Ouroveni – Hoani</span></div>
    {lignes}
  </section>
{blocs}
  <footer>Le bulletin du soir annonce <b>demain matin</b> : bon pour ce soir seulement.
    Les autres flyers n'ont pas de date, gardez-les. Les derniers blocs sont des
    <b>textes seuls</b>, à publier sans image ou avec une de vos photos.</footer>
</div>

<script>
document.querySelectorAll('.copie').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var t = document.getElementById(b.dataset.cible), fini = function () {{
      var a = b.textContent; b.textContent = 'Texte copié';
      setTimeout(function () {{ b.textContent = a; }}, 2200);
    }};
    if (navigator.clipboard) {{ navigator.clipboard.writeText(t.value).then(fini, function () {{ manuel(t, fini); }}); }}
    else {{ manuel(t, fini); }}
  }});
}});
function manuel(t, fini) {{
  t.hidden = false; t.select(); t.setSelectionRange(0, 99999);
  try {{ document.execCommand('copy'); fini(); }} catch (e) {{}}
  t.hidden = true;
}}
</script>
'''

if __name__ == '__main__':
    main()
