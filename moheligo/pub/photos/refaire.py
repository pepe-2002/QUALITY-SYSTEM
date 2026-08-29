#!/usr/bin/env python3
"""Refabrique la photo produit du flyer 43, d'un bout à l'autre.

Une seule commande pour rejouer toute la chaîne — sinon chaque réglage
demande de retrouver l'ordre exact des opérations, et l'ordre compte :
la balance des blancs se mesure sur le MUR, donc AVANT qu'il soit remplacé.
"""
import os
import subprocess
import sys
from PIL import Image, ImageFilter
sys.path.insert(0, '/home/user/QUALITY-SYSTEM/moheligo/pub/photos')
import mise_en_scene as ms
import traiter

U = '/root/.claude/uploads/dd65582f-da94-5ee8-ace1-6aec9514fe93'
PRISE = f'{U}/f1e1ccfe-image.jpg'
SORTIE = '/home/user/QUALITY-SYSTEM/moheligo/pub/flyers/photo-modele-produit.jpg'

# 📐 LE CORPS DE LA COQUE, lu à la loupe puis élargi de 24 px : les deux
# premiers essais laissaient un liseré doré de l'ancienne coque affleurer à
# droite et en bas à gauche. Mieux vaut mordre un peu sur la main que laisser
# voir un bout de coque jaunie — la main, elle, est floue à cet endroit.
CORPS = [(558, 592), (930, 584), (923, 1300), (565, 1308)]

# ⛔ PLUS AUCUNE RESTAURATION DE DOIGT — et c'était une fausse bonne idée.
# Je remettais le pouce par-dessus le châssis avec un disque flou. Résultat vu
# au zoom : le disque recollait aussi un morceau de l'ANCIENNE COQUE jaunie,
# en plein sur l'écran de l'appli. Le patron : « le doigt tache un peu
# l'écran. »
# 📌 Et la restauration ne servait à rien : sans elle, le pouce s'arrête au
# bord du châssis, donc il passe DERRIÈRE le téléphone — ce qui est exactement
# ce que fait une main qui tient un téléphone. Le défaut coûtait quelque chose
# et ne rapportait rien.
POUCE = []

photo = Image.open(PRISE).convert('RGB')
# 📅 LA CAPTURE SE REFAIT ICI, À CHAQUE FOIS — elle n'est pas un fichier qu'on
# garde. La date affichée dans l'appli vaut « aujourd'hui + 7 jours » ; figée,
# elle montre une réservation pour une date PASSÉE quelques jours plus tard, et
# un post Facebook reste sur la page pour toujours.
# ⚠️ HAUTEUR=995 : il faut le rapport de l'écran photographié (0,443), pas
# celui de la capture par défaut (0,493), sinon l'appli est écrasée en largeur.
ECRAN = '/tmp/ecran-haut.png'
subprocess.run(['node', 'capture.js'], check=True,
               cwd=os.path.join(os.path.dirname(__file__), '..', 'demo', 'ecrans'),
               env={**os.environ, 'LARGEUR': '440', 'HAUTEUR': '995', 'SORTIE': ECRAN,
                    'NODE_PATH': os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules')})
tel = ms.telephone_propre(Image.open(ECRAN))
# ⚠️ `adoucir=0.6` et non 1,4 : un bord de masque trop flou laissait
# transparaître la coque claire en un LISERÉ PÂLE le long du bord gauche,
# entre les doigts et le châssis. Le patron : « à droite des autres doigts on
# voit une petite ligne, elle doit pas être là. » Un châssis a un bord NET.
im = ms.couvrir_telephone(photo, tel, CORPS, doigts=POUCE, adoucir=0.6)
im = ms.eclaircir(im)
im = ms.polo_vers_marine(im)
im = ms.adoucir_peau(im)
im = ms.profondeur(im, (748, 945), 360, force=15)
im = im.crop((500, 575, 1300, 1575))            # 800 x 1000 — sous le menton
im = traiter.balance_des_blancs(im)             # ⚠️ AVANT de supprimer le mur
im = traiter.courbe(im)
im = ms.remplacer_mur(im, lum_bas=140, lum_haut=190, sat_haut=0.26, adoucir=2.4)
im = im.filter(ImageFilter.UnsharpMask(radius=1.8, percent=60, threshold=3))
im.save(SORTIE, quality=96, subsampling=0)
print('OK ->', SORTIE, im.size)
