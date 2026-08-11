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


def config():
    page = os.environ.get('FB_PAGE_ID', '').strip()
    jeton = os.environ.get('FB_PAGE_TOKEN', '').strip()
    manque = [n for n, v in (('FB_PAGE_ID', page), ('FB_PAGE_TOKEN', jeton)) if not v]
    if manque:
        sys.exit('Variables manquantes : %s\nVoir la marche à suivre dans '
                 'pub/flyers/LIER-FACEBOOK.md' % ', '.join(manque))
    return page, jeton


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


def publier(image, texte, pour_de_vrai):
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

    # le message passe par un fichier : « -F champ=<fichier » lit la VALEUR
    # dans le fichier (et non un envoi de fichier), donc pas d'ennui de guillemets
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
        fh.write(post)
        msg = fh.name
    rep = curl(f'{BASE}/{page}/photos', 'POST', jeton=jeton, formulaires=[
        f'source=@{img}', f'message=<{msg}', 'published=true'])
    os.unlink(msg)
    if jetable:
        os.unlink(jetable)
    post_id = rep.get('post_id') or rep.get('id')
    print('Publié :', post_id)

    if commentaire and post_id:
        # le lien va en premier commentaire, pas dans le post
        with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False) as fh:
            fh.write(commentaire)
            cmt = fh.name
        rc = curl(f'{BASE}/{post_id}/comments', 'POST', jeton=jeton,
                  formulaires=[f'message=<{cmt}'])
        os.unlink(cmt)
        print('Premier commentaire :', rc.get('id', '?'))

    print('À voir sur la page : https://facebook.com/' + str(page))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--image', default='flyer-soir-facebook.png')
    ap.add_argument('--texte', default='texte-du-jour.txt')
    ap.add_argument('--verifier', action='store_true',
                    help='teste seulement la liaison, ne publie rien')
    ap.add_argument('--publier', action='store_true',
                    help='publie pour de vrai (sans ce drapeau : répétition à blanc)')
    a = ap.parse_args()
    verifier() if a.verifier else publier(a.image, a.texte, a.publier)


if __name__ == '__main__':
    main()
