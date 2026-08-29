#!/usr/bin/env python3
"""Refabrique la photo produit du flyer 43, d'un bout à l'autre.

Une seule commande pour rejouer toute la chaîne — sinon chaque réglage
demande de retrouver l'ordre exact des opérations, et l'ordre compte :
la balance des blancs se mesure sur le MUR, donc AVANT qu'il soit remplacé.
"""
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
CORPS = [(568, 594), (928, 586), (921, 1298), (575, 1306)]
POUCE = [(903, 985, 44)]        # seul doigt qui passe DEVANT la coque

photo = Image.open(PRISE).convert('RGB')
tel = ms.telephone_propre(Image.open('/tmp/photos/ecran-haut.png'))
im = ms.couvrir_telephone(photo, tel, CORPS, doigts=POUCE)
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
