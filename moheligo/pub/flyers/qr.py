#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique le QR code de MoheliGo, et VÉRIFIE qu'il pointe au bon endroit.

    python3 qr.py                       # écrit qr-moheligo.png
    python3 qr.py --adresse https://moheligo.com/ --sortie qr-moheligo.png

Pourquoi ce script existe au lieu d'un QR trouvé quelque part : **un QR code est
illisible pour un humain.** S'il pointe vers une mauvaise adresse, personne ne
s'en aperçoit — ni moi, ni le patron, ni le client qui scanne. On l'imprimerait
sur cent affiches avant de le découvrir. Donc :

  1. il est GÉNÉRÉ ici, à partir d'une adresse écrite en clair dans ce fichier ;
  2. il est **relu et décodé** juste après, et le script échoue si l'adresse
     décodée n'est pas exactement celle demandée.

Correction d'erreur **Q** (jusqu'à 25 % du code abîmé) : une affiche collée
dehors prend la pluie, le soleil et les doigts. C'est le niveau qu'utilisent les
transporteurs pour les billets.
"""

import argparse
import pathlib
import sys

import qrcode
from qrcode.constants import ERROR_CORRECT_Q

ADRESSE = 'https://moheligo.com/'
MARINE = '#0F2A5C'


def fabriquer(adresse, sortie, module=20, marge=2):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=module, border=marge)
    q.add_data(adresse)
    q.make(fit=True)
    img = q.make_image(fill_color=MARINE, back_color='white').convert('RGB')
    img.save(sortie)
    return img


def relire(chemin, attendu):
    """Décode le PNG et compare. Sans cette vérification, le script ne prouve rien.

    Le décodage a besoin d'une bibliothèque de lecture ; si elle manque, on le
    DIT au lieu de laisser croire que la vérification a eu lieu.
    """
    # OpenCV plutôt que pyzbar : pyzbar a besoin de la bibliothèque système
    # zbar, absente ici et impossible à installer (dépôts incomplets). OpenCV
    # apporte son propre décodeur dans la roue Python, donc la vérification a
    # lieu vraiment au lieu d'être annoncée puis sautée.
    try:
        import cv2
    except ImportError as e:
        return None, 'lecteur indisponible (%s) — pip install opencv-python-headless' % e
    image = cv2.imread(str(chemin))
    if image is None:
        return False, 'fichier illisible'
    lu, points, _ = cv2.QRCodeDetector().detectAndDecode(image)
    if not lu:
        return False, 'aucun QR détecté dans le fichier produit'
    return lu == attendu, lu


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--adresse', default=ADRESSE)
    ap.add_argument('--sortie', default=str(pathlib.Path(__file__).parent / 'qr-moheligo.png'))
    a = ap.parse_args()

    img = fabriquer(a.adresse, a.sortie)
    print('QR écrit :', a.sortie, '—', img.size[0], 'px, correction Q')
    print('adresse encodée :', a.adresse)

    ok, lu = relire(a.sortie, a.adresse)
    if ok is None:
        print('⚠️  Vérification NON faite :', lu)
        print('   Installer le lecteur : pip install opencv-python-headless')
        return
    if not ok:
        sys.exit('❌ Le QR produit ne décode pas la bonne adresse : « %s »' % lu)
    print('✅ Vérifié : le QR décode bien « %s »' % lu)


if __name__ == '__main__':
    main()
