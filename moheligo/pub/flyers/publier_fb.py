#!/usr/bin/env python3
"""Publie le bulletin du soir sur la page Facebook MoheliGo.

    python3 publier_fb.py --verifier             # la liaison marche-t-elle ?
    python3 publier_fb.py                        # répétition à blanc, rien n'est publié
    python3 publier_fb.py --publier              # publie pour de vrai

Comment la liaison est faite (il n'y a pas de connecteur Facebook dans Claude) :
le patron crée un **jeton de page** chez Meta et le range dans les secrets
GitHub. Ce script s'en sert. Moi, je n'ai jamais le jeton entre les mains — je
n'écris que le code qui l'utilise, et GitHub le fournit au moment de publier.

Deux variables d'environnement :
    FB_PAGE_ID     l'identifiant numérique de la page (pas un secret)
    FB_PAGE_TOKEN  le jeton de page (SECRET — jamais dans le dépôt, jamais dans
                   une conversation, jamais dans un message)

⚠️ Publier est un geste public et difficile à défaire. Donc :
  * sans `--publier`, ce script ne publie RIEN, il montre seulement ce qu'il
    ferait ;
  * dans le workflow, l'étape est désarmée par défaut : elle ne tourne que si la
    variable de dépôt `PUBLIER_FB` vaut « oui ».

Le jeton ne passe jamais par la ligne de commande (il serait visible dans la
liste des processus et dans les journaux) : il est donné à curl par son entrée
standard, en en-tête `Authorization`.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone

#  v26.0 = la version proposée par l'explorateur d'API en août 2026. Meta sort
#  environ deux versions par an et retire les plus anciennes : quand un appel
#  échoue en parlant de version, monter d'un cran (ou poser FB_API_VERSION).
API = os.environ.get('FB_API_VERSION', 'v26.0')
BASE = f'https://graph.facebook.com/{API}'
CACERT = '/root/.ccr/ca-bundle.crt'               # proxy de session ; absent sur GitHub


def curl(url, methode='GET', formulaires=(), jeton=None, strict=True):
    """Appel Graph API. Le jeton passe par l'entrée standard, jamais par argv."""
    cmd = ['curl', '-sS', '--max-time', '40', '-X', methode]
    if os.path.isfile(CACERT):
        cmd += ['--cacert', CACERT]
    for f in formulaires:
        cmd += ['-F', f]
    entree = None
    if jeton:
        cmd += ['-K', '-']
        entree = f'header = "Authorization: Bearer {jeton}"\n'
    cmd.append(url)
    out = subprocess.run(cmd, input=entree, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit('curl a échoué : ' + (out.stderr.strip() or 'sans message'))
    try:
        rep = json.loads(out.stdout)
    except json.JSONDecodeError:
        sys.exit('Réponse illisible de Facebook : ' + out.stdout[:400])
    if isinstance(rep, dict) and 'error' in rep:
        e = rep['error']
        if not strict:                      # appel facultatif : on renvoie vide
            return {}
        sys.exit('Facebook refuse : %s (code %s, type %s)\n%s' % (
            e.get('message', '?'), e.get('code', '?'), e.get('type', '?'),
            "Jeton expiré ou permission manquante : refaire un jeton de page "
            "avec pages_manage_posts et pages_read_engagement."))
    return rep


def nettoyer_jeton(brut):
    """Accepte un jeton collé n'importe comment, y compris une adresse entière.

    Sur un téléphone, extraire le jeton d'une barre d'adresse
    (`...login_success.html#access_token=EAA...&expires_in=...`) est pénible et
    source d'erreur. Le patron colle donc l'adresse complète : on retrouve la
    clé nous-mêmes. Coûte trois lignes, économise un aller-retour.
    """
    from urllib.parse import unquote
    j = (brut or '').strip().strip('"\'')
    # Chrome copie parfois l'adresse ENCODÉE (%23access_token%3D...) : sans ce
    # décodage, le motif n'est pas reconnu, l'adresse entière part comme jeton,
    # et Facebook répond « Bad signature » (code 190). Vécu le 11/08/2026.
    j = unquote(unquote(j))
    if 'access_token=' in j:
        j = j.split('access_token=', 1)[1]
    for sep in ('&', '#', '?', ' ', '\n', '\r', '\t'):
        j = j.split(sep, 1)[0]
    j = j.strip()
    # un jeton Meta commence par EAA et fait au moins ~80 caractères : si ce
    # n'est pas le cas, mieux vaut le dire tout de suite que de laisser
    # Facebook répondre « Bad signature ».
    if j and not (j.startswith('EAA') and len(j) > 60):
        print('⚠️ La valeur de FB_PAGE_TOKEN ne ressemble pas à un jeton Meta '
              '(%d caractères, commence par « %s »). Recoller la clé.'
              % (len(j), j[:6]), file=sys.stderr)
    return j


def jeton_de_page(page, jeton):
    """Dérive le jeton de PAGE à partir d'un jeton d'UTILISATEUR, si besoin.

    ⚠️ Piège majeur, découvert le 11/08/2026 : Facebook laisse un jeton
    d'utilisateur LIRE une page, mais refuse de le laisser PUBLIER au nom de la
    page — même quand on en est administrateur. Publier exige un jeton de page.
    Le dialogue OAuth, lui, ne rend qu'un jeton d'utilisateur.
    Plutôt que d'exiger du patron une manipulation de plus, on fait la
    conversion ici : /me/accounts liste ses pages avec LEUR jeton.
    Si le jeton fourni est déjà un jeton de page, l'appel ne renvoie rien
    d'utilisable et on le garde tel quel.
    """
    rep = curl(f'{BASE}/me/accounts?fields=id,access_token&limit=100',
               jeton=jeton, strict=False)
    for compte in rep.get('data', []) or []:
        if str(compte.get('id')) == str(page) and compte.get('access_token'):
            print('Jeton de page dérivé du jeton utilisateur (conversion automatique).')
            return compte['access_token']
    return jeton


def config():
    page = os.environ.get('FB_PAGE_ID', '').strip()
    jeton = nettoyer_jeton(os.environ.get('FB_PAGE_TOKEN', ''))
    manque = [n for n, v in (('FB_PAGE_ID', page), ('FB_PAGE_TOKEN', jeton)) if not v]
    if manque:
        sys.exit('Variables manquantes : %s\nVoir la marche à suivre dans '
                 'dossier/LIER-FACEBOOK.md' % ', '.join(manque))
    return page, jeton_de_page(page, jeton)


def verifier():
    """Lecture seule : qui est au bout du fil, et est-ce bien une PAGE ?

    On ne demande que `name`, plus `metadata=1` qui donne le type de l'objet.
    Demander un champ propre aux pages (followers_count) sur un compte
    personnel fait échouer l'appel avec un message trompeur — c'est arrivé.
    """
    page, jeton = config()
    # `category` (Transport, Service…) n'existe que sur une Page : c'est le
    # marqueur le plus fiable. `metadata=1` a été essayé d'abord et Facebook ne
    # le renvoie pas toujours — un test qui ne répond pas ne prouve rien.
    # ⚠️ un seul champ invalide fait rejeter TOUT l'appel : on ne demande ici
    # que des champs sûrs, et le nombre d'abonnés dans un appel facultatif.
    rep = curl(f'{BASE}/{page}?fields=name,category,link', jeton=jeton)
    print('Répond au nom de :', '« %s »' % rep.get('name', '?'))
    print('Champs obtenus   :', ', '.join(sorted(k for k in rep if k != 'id')))

    if 'category' not in rep:
        sys.exit(
            "\nAucune catégorie : ce n'est pas une Page, ou le jeton n'a pas la\n"
            "permission de la lire. FB_PAGE_ID contient probablement "
            "l'identifiant\ndu compte personnel — qui porte le même nom que la "
            "page, d'où la confusion.\n\n"
            "Le bon couple s'obtient avec cette requête dans l'explorateur :\n"
            "    me/accounts?fields=name,id,access_token\n"
            "Le « id » de la ligne MoheliGo va dans FB_PAGE_ID, son "
            "« access_token » dans FB_PAGE_TOKEN.")

    print('\nLiaison OK — page « %s » (%s)' % (rep.get('name'), rep['category']))
    abo = curl(f'{BASE}/{page}?fields=followers_count', jeton=jeton, strict=False)
    if 'followers_count' in abo:
        print('Abonnés :', abo['followers_count'])
    print('Adresse :', rep.get('link', '—'))


def publications_recentes(jours=7):
    """Les publications RÉELLEMENT parties, lues sur Facebook lui-même.

    🚨 POURQUOI CETTE FONCTION EXISTE (18/08/2026). Le patron : « les pubs ne
    partent pas automatiquement. » Vérification faite : elles partaient — cinq
    jours d'affilée, à l'heure. Ce qui ne partait pas, c'était **la preuve** : le
    rapport comptait les publications dans `journal-publications.json`, un fichier
    écrit sur le serveur GitHub… qui est effacé à la fin de chaque travail. Le
    rapport annonçait donc « 1 publication en 7 jours » tous les jours, et c'est
    ce chiffre-là que le patron lisait.

    📌 LA LEÇON : un compteur qui repart de zéro à chaque exécution ne mesure
    rien, et un chiffre faux dans un rapport détruit la confiance dans le
    système entier — bien plus vite qu'une panne, qu'on voit et qu'on répare.
    La source de vérité, c'est la PAGE, pas notre journal.

    Renvoie une liste [{quand, texte}] triée du plus récent au plus ancien, ou
    None si Facebook refuse la lecture (permission manquante) — dans ce cas
    l'appelant retombe sur le journal local, en le disant.
    """
    page, jeton = config()
    depuis = (datetime.now(timezone.utc)
              - timedelta(days=jours)).strftime('%Y-%m-%dT%H:%M:%S+0000')
    # `published_posts` demande pages_read_engagement ; `feed` marche parfois
    # quand l'autre échoue. On essaie les deux avant d'abandonner.
    for bord in ('published_posts', 'feed'):
        rep = curl(f'{BASE}/{page}/{bord}?fields=created_time,message&limit=100'
                   f'&since={depuis}', jeton=jeton, strict=False)
        donnees = rep.get('data')
        if donnees is None:
            continue
        # ⚠️ 18/08/2026 : `since` est IGNORÉ par Facebook sur ces deux bords —
        # l'appel a renvoyé les 50 dernières publications de toute l'histoire de
        # la page, et le rapport a affiché « 50 publications en 7 jours ».
        # Exactement le genre de chiffre faux que cette fonction devait tuer.
        # Donc on filtre NOUS-MÊMES sur la date, et on ne fait plus confiance à
        # un paramètre qu'on n'a pas vérifié.
        recentes = [p for p in donnees if p.get('created_time', '') >= depuis]
        return [{'quand': p.get('created_time', '')[:16].replace('T', ' à '),
                 'texte': (p.get('message') or '').strip()}
                for p in recentes]
    return None


def decouper(chemin):
    """Le texte du post, et le premier commentaire s'il y en a un."""
    brut = pathlib.Path(chemin).read_text()
    if '--- premier commentaire ---' in brut:
        post, commentaire = brut.split('--- premier commentaire ---', 1)
        return post.strip(), commentaire.strip()
    return brut.strip(), ''


LIMITE = 3.5 * 1024 * 1024        # Facebook refuse au-delà d'environ 4 Mo


def preparer(image):
    """Nos PNG font 4 à 6,5 Mo : au-delà de la limite, on repasse en JPEG.

    Facebook recompresse de toute façon tout ce qu'on lui envoie ; un JPEG de
    qualité 92 en 2160 px de large est visuellement identique au PNG et pèse
    quatre fois moins. Renvoie (chemin_à_envoyer, chemin_temporaire_ou_None).
    """
    p = pathlib.Path(image)
    if not p.exists():
        sys.exit('Image introuvable : ' + str(image))
    if p.stat().st_size <= LIMITE:
        return p, None
    from PIL import Image
    im = Image.open(p).convert('RGB')
    if im.width > 2160:
        im = im.resize((2160, round(im.height * 2160 / im.width)), Image.LANCZOS)
    tmp = pathlib.Path(tempfile.gettempdir()) / (p.stem + '-fb.jpg')
    im.save(tmp, quality=92, optimize=True)
    print('Image allégée : %d ko -> %d ko (JPEG, limite Facebook)'
          % (p.stat().st_size // 1024, tmp.stat().st_size // 1024))
    return tmp, tmp


def deja_publie(post):
    """Ce texte est-il DÉJÀ sur la page aujourd'hui ?

    🚨 POURQUOI (27/08/2026). Le patron : « le flyer d'aujourd'hui 12h n'est pas
    parti. » Vérification : GitHub **n'a pas déclenché le rendez-vous du tout** —
    ni réussite, ni échec, aucune exécution. Le bulletin du soir avait raté le
    sien la veille de la même façon. Les rendez-vous programmés de GitHub sont
    au mieux « on essaiera » : la documentation prévient qu'ils peuvent être
    retardés, et abandonnés quand la charge est forte.
    📌 On ne peut pas réparer ça chez GitHub. On peut **arrêter d'en dépendre** :
    chaque robot a maintenant DEUX rendez-vous, et ce garde-fou empêche le
    second de publier ce que le premier a déjà mis en ligne.

    ⚠️ On compare le TEXTE, pas la date. Un simple « quelque chose est parti
    aujourd'hui » ferait sauter le flyer de midi les jours où seul le bulletin
    du soir est passé — et on perdrait la publication qu'on voulait sauver.
    ➡️ Si Facebook refuse la lecture, on renvoie False : **dans le doute on
    publie**. Un doublon se supprime en dix secondes ; un rendez-vous manqué ne
    se rattrape pas.
    """
    recentes = publications_recentes(jours=2)
    if recentes is None:
        print('⚠️ lecture de la page impossible : on ne peut pas savoir si '
              'c\'est déjà parti. Dans le doute, on publie.')
        return False
    # la date des Comores (UTC+3), pas celle du serveur
    aujourdhui = (datetime.now(timezone.utc) + timedelta(hours=3)).strftime('%Y-%m-%d')
    cherchee = _empreinte(post)
    for p in recentes:
        if p['quand'][:10] != aujourdhui:
            continue
        if _empreinte(p['texte']) == cherchee:
            print('→ DÉJÀ PUBLIÉ aujourd\'hui (%s). Rien n\'est renvoyé.' % p['quand'])
            return True
    return False


def _empreinte(texte):
    """La LIGNE DE TITRE, pas les premiers caractères.

    ⚠️ Piège évité de justesse : je comparais les 80 premiers caractères. Or le
    bulletin commence par « OÙ EN EST LE SERVICE — JOUR 3. Ce matin entre nos
    ports : mer agitée — houle de… » : **l'état de la mer est dedans**. Il se
    recalcule à chaque exécution, donc entre les deux rendez-vous il peut passer
    de « agitée » à « forte » — l'empreinte ne correspondrait plus et le filet
    de sécurité publierait un doublon, exactement ce qu'il doit empêcher.
    ➡️ La première ligne, elle, est un titre : « OÙ EN EST LE SERVICE — JOUR 3. »
    Elle ne porte aucun chiffre qui bouge dans la journée.
    📌 Si un titre est très court, on prend la ligne suivante avec : une
    empreinte de trois mots pourrait confondre deux publications différentes.
    """
    lignes = [' '.join(l.split()) for l in texte.strip().splitlines()]
    lignes = [l for l in lignes if l]
    if not lignes:
        return ''
    empreinte = lignes[0]
    if len(empreinte) < 16 and len(lignes) > 1:
        empreinte += ' | ' + lignes[1]
    return empreinte[:90]


def publier(image, texte, pour_de_vrai, essai=False, forcer=False):
    # frein d'urgence : une variable de dépôt suffit à tout arrêter
    if os.environ.get('PAUSE_FB', '').strip().lower() == 'oui':
        print('PAUSE_FB = oui → publication suspendue, rien n\'a été envoyé.')
        return
    page, jeton = config()
    post, commentaire = decouper(texte)
    img, jetable = preparer(image)

    print('Page      :', page)
    print('Image     : %s (%d ko)' % (img.name, img.stat().st_size // 1024))
    print('Post      : %d caractères, %d lignes' % (len(post), post.count('\n') + 1))
    print('Commentaire:', ('%d caractères' % len(commentaire)) if commentaire else 'aucun')
    if not pour_de_vrai:
        if jetable:
            os.unlink(jetable)
        print('\n--- RÉPÉTITION À BLANC : rien n\'a été publié. '
              'Relancer avec --publier pour de vrai. ---')
        print('\n' + post)
        return

    # 🔁 LE FILET DE SÉCURITÉ. Chaque robot a deux rendez-vous depuis le
    # 27/08/2026 ; celui-ci empêche le second de faire un doublon. Un essai
    # d'écriture (`--essai`) n'apparaît pas sur la page, donc il ne compte pas.
    if not essai and not forcer and deja_publie(post):
        if jetable:
            os.unlink(jetable)
        return

    # le message passe par un fichier : « -F champ=<fichier » lit la VALEUR
    # dans le fichier (et non un envoi de fichier), donc pas d'ennui de guillemets
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write(post)
        msg = fh.name
    # `published=false` : la photo entre dans la bibliothèque de la page sans
    # apparaître nulle part. C'est le seul moyen de prouver que le jeton a bien
    # le droit de PUBLIER, sans rien montrer à personne.
    rep = curl(f'{BASE}/{page}/photos', 'POST', jeton=jeton, formulaires=[
        f'source=@{img}', f'message=<{msg}',
        'published=false' if essai else 'published=true'])
    os.unlink(msg)
    if jetable:
        os.unlink(jetable)
    post_id = rep.get('post_id') or rep.get('id')
    if essai:
        print('ESSAI RÉUSSI : le jeton a bien le droit de publier.')
        print('Photo déposée NON PUBLIÉE (invisible sur la page), id', post_id)
        print('À supprimer quand vous voulez, dans la bibliothèque de la page.')
        return
    print('Publié :', post_id)

    if commentaire and post_id:
        # le lien va en premier commentaire, pas dans le post
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
            fh.write(commentaire)
            cmt = fh.name
        # ⚠️ Commenter demande `pages_manage_engagement`, une permission
        # DIFFÉRENTE de celle qui sert à publier. Sans elle, le commentaire est
        # refusé — mais la photo est déjà en ligne. Le post compte plus que le
        # lien : on ne fait donc jamais échouer une publication réussie pour ça.
        rc = curl(f'{BASE}/{post_id}/comments', 'POST', jeton=jeton,
                  formulaires=[f'message=<{cmt}'], strict=False)
        os.unlink(cmt)
        if rc.get('id'):
            print('Premier commentaire :', rc['id'])
        else:
            print('⚠️ Commentaire refusé (permission pages_manage_engagement '
                  'manquante). La publication, elle, est bien en ligne — '
                  'ajouter le lien à la main sous le post.')

    journaliser(page, post_id, img.name, post)
    print('À voir sur la page : https://facebook.com/' + str(page))


def publier_video(video, texte, pour_de_vrai, titre=None):
    """Publie une VIDÉO sur la page.

    ⚠️ Facebook a un point d'entrée DIFFÉRENT pour la vidéo : `/videos`, et non
    `/photos`. Même jeton, même permission (`pages_manage_posts`), mais le champ
    du texte s'appelle `description` et non `message`. Une vidéo envoyée sur
    `/photos` est refusée sans explication utile.

    📌 Ajouté le 26/08/2026 : le patron a demandé de publier la vidéo montée avec
    le Young Leader. Le robot ne savait poster que des images.

    ⚠️ L'envoi est en un seul morceau. C'est bon jusqu'à ~100 Mo ; au-delà,
    Facebook veut un envoi repris en plusieurs fois. Nos vidéos font ~9 Mo.
    """
    if os.environ.get('PAUSE_FB', '').strip().lower() == 'oui':
        print('PAUSE_FB = oui → publication suspendue, rien n\'a été envoyé.')
        return
    # 🚨 GARDE-FOU AJOUTÉ LE 26/08/2026, sur décision du patron : « ne publie pas
    # aujourd'hui, on la garde pour le jour de la réouverture, comme ça ça fait
    # le boom. » Il a raison : une vidéo qui dit « réserve ta traversée » sortie
    # un jour de fermeture se dépense pour rien, et sortie le jour où ça repart
    # elle EST l'annonce de la reprise.
    # Une vidéo est un message commercial : elle suit donc l'état du service,
    # comme tout le reste (§ « tout ce qui promet une traversée est dans
    # service.py »). Pour passer outre : VIDEO_MALGRE_FERMETURE=oui.
    import service
    if not service.ouvert() and \
            os.environ.get('VIDEO_MALGRE_FERMETURE', '').strip().lower() != 'oui':
        print('SERVICE FERMÉ → la vidéo n\'est PAS publiée.')
        print('Une vidéo qui dit « réserve ta traversée » attend la réouverture.')
        print('Pour forcer malgré tout : VIDEO_MALGRE_FERMETURE=oui')
        return
    v = pathlib.Path(video)
    if not v.exists():
        raise SystemExit('vidéo introuvable : %s' % v)
    page, jeton = config()
    post, commentaire = decouper(texte)

    print('Page       :', page)
    print('Vidéo      : %s (%d ko)' % (v.name, v.stat().st_size // 1024))
    print('Description: %d caractères' % len(post))
    print('Commentaire:', ('%d caractères' % len(commentaire)) if commentaire else 'aucun')
    if not pour_de_vrai:
        print('\n--- RÉPÉTITION À BLANC : rien n\'a été publié. ---')
        print('\n' + post)
        return

    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write(post)
        msg = fh.name
    formulaires = [f'source=@{v}', f'description=<{msg}']
    if titre:
        formulaires.append(f'title={titre}')
    rep = curl(f'{BASE}/{page}/videos', 'POST', jeton=jeton, formulaires=formulaires)
    os.unlink(msg)
    vid = rep.get('id')
    print('Vidéo publiée :', vid)

    if commentaire and vid:
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
            fh.write(commentaire)
            cmt = fh.name
        # comme pour les photos : un commentaire refusé ne fait jamais échouer
        # une publication déjà en ligne (permission `pages_manage_engagement`)
        r = curl(f'{BASE}/{vid}/comments', 'POST', jeton=jeton,
                 formulaires=[f'message=<{cmt}'], strict=False)
        os.unlink(cmt)
        print('Commentaire :', r.get('id') or 'refusé (le post reste en ligne)')

    journaliser(page, vid, v.name, post)
    return vid

def journaliser(page, post_id, visuel, texte):
    """Chaque publication est consignée : c'est la matière première des rapports.

    Sans ce journal, aucun rapport n'est possible — l'API ne dira jamais ce que
    NOUS avons voulu publier, seulement ce qui est en ligne.
    """
    fichier = pathlib.Path(__file__).parent / 'journal-publications.json'
    try:
        journal = json.loads(fichier.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        journal = []
    journal.append({
        'quand': datetime.now(timezone(timedelta(hours=3))).isoformat(timespec='minutes'),
        'page': str(page), 'post_id': str(post_id), 'visuel': visuel,
        'accroche': texte.split('\n')[0][:80],
    })
    fichier.write_text(json.dumps(journal, ensure_ascii=False, indent=2))
    print('Journalisé :', fichier.name, '(%d publications)' % len(journal))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', default='flyer-soir-facebook.png')
    ap.add_argument('--texte', default='texte-du-jour.txt')
    ap.add_argument('--verifier', action='store_true',
                    help='teste seulement la liaison, ne publie rien')
    ap.add_argument('--publier', action='store_true',
                    help='publie pour de vrai (sans ce drapeau : répétition à blanc)')
    ap.add_argument('--essai', action='store_true',
                    help='envoie la photo en NON PUBLIÉE : prouve le droit de publier '
                         'sans que personne ne voie quoi que ce soit')
    ap.add_argument('--video', help='publie une VIDÉO au lieu d\'une image '
                                    '(point d\'entrée /videos, voir publier_video)')
    ap.add_argument('--titre', help='titre de la vidéo (facultatif)')
    # 🔓 LA SOUPAPE DU GARDE-FOU ANTI-DOUBLON.
    # 🚨 Le cas qui l'a rendue nécessaire (28/08/2026) : un `cron` livré avec
    # 8 h 30 de retard a publié le bulletin à 3h38 du matin. Celui de 19h25,
    # pourtant porteur d'une AUTRE prévision, se faisait alors refuser — le
    # garde-fou compare la ligne de titre, et celle du bulletin est toujours
    # « LA MER DE DEMAIN, CE SOIR. »
    # 📌 À n'utiliser que quand on SAIT que le contenu diffère. Sans ça, on
    # republie la même chose deux fois dans la journée, et la page se fait
    # masquer par les abonnés.
    ap.add_argument('--forcer', action='store_true',
                    help='publier MÊME si un texte au même titre est déjà '
                         'paru aujourd\'hui (à n\'utiliser qu\'à bon escient)')
    a = ap.parse_args()
    if a.verifier:
        verifier()
    elif a.video:
        publier_video(a.video, a.texte, a.publier, titre=a.titre)
    else:
        publier(a.image, a.texte, a.publier or a.essai, essai=a.essai,
                forcer=a.forcer)


if __name__ == '__main__':
    main()
