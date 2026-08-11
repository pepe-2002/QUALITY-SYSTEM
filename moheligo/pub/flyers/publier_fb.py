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

API = os.environ.get('FB_API_VERSION', 'v21.0')   # Meta sort ~2 versions par an
BASE = f'https://graph.facebook.com/{API}'
CACERT = '/root/.ccr/ca-bundle.crt'               # proxy de session ; absent sur GitHub


def curl(url, methode='GET', formulaires=(), jeton=None):
    """Appel Graph API. Le jeton passe par l'entrée standard, jamais par argv."""
    cmd = ['curl', '-sS', '--max-time', '40', '-X', methode]
    if pathlib.Path(CACERT).exists():
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
    page, jeton = config()
    rep = curl(f'{BASE}/{page}?fields=name,followers_count,link', jeton=jeton)
    print('Liaison OK — page « %s »' % rep.get('name', '?'))
    if 'followers_count' in rep:
        print('Abonnés :', rep['followers_count'])
    print('Adresse :', rep.get('link', '—'))


def decouper(chemin):
    """Le texte du post, et le premier commentaire s'il y en a un."""
    brut = pathlib.Path(chemin).read_text()
    if '--- premier commentaire ---' in brut:
        post, commentaire = brut.split('--- premier commentaire ---', 1)
        return post.strip(), commentaire.strip()
    return brut.strip(), ''


def publier(image, texte, pour_de_vrai):
    page, jeton = config()
    post, commentaire = decouper(texte)
    img = pathlib.Path(image)
    if not img.exists():
        sys.exit('Image introuvable : ' + image)

    print('Page      :', page)
    print('Image     : %s (%d ko)' % (img.name, img.stat().st_size // 1024))
    print('Post      : %d caractères, %d lignes' % (len(post), post.count('\n') + 1))
    print('Commentaire:', ('%d caractères' % len(commentaire)) if commentaire else 'aucun')
    if not pour_de_vrai:
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
