#!/usr/bin/env python3
"""Détoure le portrait et le pose sur notre marine. Reproductible d'un bout à
l'autre : on relance et on obtient exactement la même chose.

⚠️ Pas de modèle d'apprentissage disponible hors ligne (ni rembg ni onnxruntime).
On travaille donc avec `grabCut`, qui a besoin qu'on lui DISE ce qu'il ne peut
pas deviner. Les trois choses qu'il rate seul, mesurées et corrigées ici :

1. LA COIFFURE. Cheveux noirs devant un tronc sombre : il les jetait au fond et
   coupait le crâne À PLAT à y=920, alors que le sommet est à y=785. 135 px de
   perdus. → repère « sûrement le sujet » posé sur les cheveux.
2. LA VOITURE BLEUE. Elle restait ACCROCHÉE au sujet, donc elle survivait au
   filtre « on ne garde que la plus grosse tache ». → la manche drapée, point le
   plus à gauche du sujet, est à x≈780 : tout ce qui est avant est du fond.
3. LE MUR BEIGE À L'ÉPAULE. Invisible sur fond blanc, criant sur le marine.
   → séparé par B−R, mesuré sur des vignettes VÉRIFIÉES À L'ŒIL :
     mur +1 · chemise +30 · gilet +56 · peau −72.
   Le noir des cheveux est aussi à +18, d'où la condition de clarté : le mur est
   à 146, les cheveux à 31.
"""
import cv2, numpy as np

MARINE = np.array([92, 42, 15], np.float32)          # #0F2A5C en BGR
im = cv2.imread('source.jpg'); H, L = im.shape[:2]

m = np.full((H, L), cv2.GC_PR_BGD, np.uint8)
cv2.fillPoly(m, [np.array([[1180, 740], [1700, 900], [1720, 1500], [1620, 2100],
                           [1560, H], [745, H], [745, 1850], [900, 1500],
                           [1150, 1000]])], cv2.GC_PR_FGD)
for x0, y0, x1, y1 in [(1330, 830, 1580, 900),      # les cheveux (défaut n°1)
                       (1360, 950, 1520, 1050), (1150, 1250, 1300, 1450),
                       (1250, 1500, 1450, 1900), (800, 2050, 1050, 2350)]:
    m[y0:y1, x0:x1] = cv2.GC_FGD
m[:700, :] = cv2.GC_BGD
m[:, :745] = cv2.GC_BGD                              # la voiture (défaut n°2)
m[:, 1780:] = cv2.GC_BGD
f, a = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
cv2.grabCut(im, m, None, f, a, 8, cv2.GC_INIT_WITH_MASK)
s = np.where((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)

b, g, r = im[..., 0].astype(int), im[..., 1].astype(int), im[..., 2].astype(int)
clarte = im.max(2)
mur = (b - r >= -12) & (b - r <= 18) & (clarte > 90)  # le mur (défaut n°3)
s[mur] = 0

# 🚩 DÉFAUT n°4 — LE CARRÉ DE MUR TAN POSÉ SUR L'ÉPAULE, et il se corrige par la
# POSITION, pas par la couleur. Le tan du mur et la peau sont trop proches en
# teinte : toute règle assez large pour prendre l'un mange l'autre. En revanche
# sa position est nette et vérifiée à l'image — il est AU-DESSUS de la ligne
# d'épaule, qui commence à y=1288 à cet endroit. On coupe donc jusqu'à 1280,
# ⚠️ ET C'EST UN QUADRILATÈRE, PAS UN RECTANGLE. Premier essai : un rectangle
# coupé à y=1280. Il en restait 26 px plus bas — parce que la ligne d'épaule est
# DIAGONALE (y≈1318 à x=1135, y≈1282 à x=1265). Un rectangle ne peut pas suivre
# une pente : il coupe trop haut d'un côté ou mord de l'autre.
# 📌 Quand deux choses ne se séparent pas par ce qu'elles SONT, on regarde où
# elles sont — mais alors il faut épouser la forme réelle, pas la simplifier.
cv2.fillPoly(s, [np.array([[1120, 1185], [1270, 1185], [1270, 1282],
                           [1120, 1322]])], 0)

n, lab, stats, _ = cv2.connectedComponentsWithStats(s, 8)
if n > 1:
    s = np.where(lab == 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
s = cv2.morphologyEx(s, cv2.MORPH_CLOSE, np.ones((11, 11), np.uint8))

# 🚩 DÉFAUT n°5 — DES TROUS DANS LE GILET. La règle du mur (B−R entre −12 et
# +18) a aussi mangé les zones sombres du gilet et le passepoil bleu marine, qui
# tombent dans la même fenêtre. Invisible sur fond blanc ; sur le marine, le
# fond transparaissait EN PLEIN MILIEU du vêtement, en taches bleues.
# 📌 UN TROU À L'INTÉRIEUR D'UNE SILHOUETTE N'EST JAMAIS LÉGITIME ICI : il n'y a
# aucun endroit où l'on doive voir le fond à travers lui. Plutôt que d'assouplir
# la règle de couleur — ce qui ramènerait le mur — on rebouche par la FORME :
# on inonde depuis le bord, et tout ce que l'inondation n'atteint pas est un
# trou. Une fermeture morphologique ne suffisait pas : elle ne comble que les
# petits creux, pas une tache de 40 px.
inonde = s.copy()
bord = np.zeros((H + 2, L + 2), np.uint8)
cv2.floodFill(inonde, bord, (0, 0), 255)          # le fond, vu depuis le coin
trous = (inonde == 0)                             # ni sujet, ni fond joignable
print('trous rebouches : %d px' % trous.sum())
s[trous] = 255

ys, xs = np.where(s > 0)
print('sujet : x %d..%d, y %d..%d — %.1f %% de l’image' %
      (xs.min(), xs.max(), ys.min(), ys.max(), s.mean() / 2.55))

alpha = cv2.GaussianBlur(s, (0, 0), 2.0).astype(np.float32) / 255.
c = np.clip(im.astype(np.float32) * alpha[..., None] + MARINE * (1 - alpha[..., None]), 0, 255)
cv2.imwrite('sur-marine.png', c.astype(np.uint8))
cv2.imwrite('alpha.png', s)
cv2.imwrite('zoom-epaule.png', cv2.resize(c[1050:1450, 1050:1450].astype(np.uint8), (500, 500)))
cv2.imwrite('vue.png', cv2.resize(c.astype(np.uint8), (L // 4, H // 4)))
