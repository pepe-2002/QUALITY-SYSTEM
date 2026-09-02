# 📷 Les photos fournies par le patron — provenance et usage

> **Le dépôt est PUBLIC.** Toute photo commitée ici est visible par n'importe
> qui. Ce fichier dit d'où vient chaque image et ce qu'on a le droit d'en faire.
> Une photo sans provenance écrite est une photo qu'on ne republie pas.

## 02/09/2026 — sept photos de plages de Mohéli

Envoyées par le patron (pepe-2002) avec la consigne : « les photos là c'est pour
les flyers ; nos flyers hors bulletin doivent contenir une photo ».
**Origine déclarée : ses propres prises de vue.** Aucune ne porte de mention
d'auteur tiers, aucune n'est créditée ailleurs.

### Ce que la mesure dit de chacune

Toutes font **720 px de large** ; nos visuels en font **2160**. Le verdict vient
de `preparer-photo.py <fichier>` — il mesure le **détail fin**, c'est-à-dire ce
qu'un agrandissement ne saura pas inventer.

| Photo | Sujet | Détail fin | Verdict |
|---|---|---|---|
| `ff2f2c99` | plage, mer turquoise, îlots à l'horizon | **2,85** | ✅ **plein cadre** |
| `f8e49809` | mangrove, rochers noirs, anse | 5,56 | demi-page |
| `a8e67ba2` | anse, barques au fond, rochers | 5,74 | demi-page |
| `35a48775` | anse vue de haut, mangrove | 6,37 | vignette |
| `351bb23e` | plage, colline boisée | 6,50 | vignette |
| `687575d6` | mangrove en gros plan | 9,30 | vignette |
| `86669324` | plage de sable sombre, colline | 9,97 | vignette |

📌 **La seule utilisable en plein cadre est la plus FLOUE des sept**, et ce n'est
pas un paradoxe : mer, ciel et horizon sont des dégradés, il n'y a presque rien à
inventer entre deux pixels. Les six autres ont du feuillage ou du sable en gros
plan — agrandies trois fois, elles deviennent une bouillie plastique. Le
raisonnement complet et la mesure sont dans `preparer-photo.py`.

### 🔧 02/09 (le soir) — « tu peux les rendre claires si tu veux, essaye »

Fait, et ça marche mieux que prévu. `affiner.py` remplace le simple
agrandissement par une chaîne en trois temps : débruitage **avant** d'agrandir,
puis **rétroprojection itérative**, puis un accentuage faible guidé par les
contours.

Mesuré sur les sept, **à taille de sortie identique** (c'est la seule
comparaison qui veut dire quelque chose) :

| Photo | acutance Lanczos | acutance chaîne | bruit avant → après |
|---|---|---|---|
| `ff2f2c99` | 81 | **105** | 0,15 → 0,30 |
| `351bb23e` | 126 | **224** | 0,77 → **0,57** |
| `a8e67ba2` | 174 | **330** | 0,07 → 0,28 |
| `f8e49809` | 161 | **320** | 0,19 → 0,33 |
| `35a48775` | 173 | **336** | 0,18 → 0,29 |
| `687575d6` | 226 | **433** | 0,65 → **0,41** |
| `86669324` | 168 | **329** | 1,66 → 1,72 |

**L'acutance double partout**, et sur les deux photos les plus compressées le
bruit **baisse** en même temps. Vérifié à l'œil : sur la colline boisée, on
distingue les palmes là où Lanczos donnait une purée verte.

⛔ **ET UNE ERREUR DE MESURE QUE J'AI FAITE, PARCE QU'ELLE PEUT SE REFAIRE :**
j'ai d'abord relancé le diagnostic « détail fin » sur les images DÉJÀ AGRANDIES,
et il annonçait des scores deux fois meilleurs — donc des verdicts flatteurs.
C'était faux : le détail fin se compte par pixel, et tripler les pixels le
divise mécaniquement. La seule chose qui avait changé, c'était l'échelle.
📌 **UN SEUIL CALIBRÉ À UNE ÉCHELLE NE VEUT PLUS RIEN DIRE À UNE AUTRE.** Le
diagnostic se lit sur la SOURCE, jamais sur le résultat.
✅ Les verdicts du tableau plus haut restent donc valables tels quels. Ce que la
chaîne change, c'est la QUALITÉ à l'intérieur de chaque catégorie — une photo
« demi-page » reste demi-page, mais sa demi-page est nettement meilleure.
Chaque promotion se décide à l'œil, sur le visuel fini, pas sur un chiffre.

### 🔴 Ce qu'il faut demander, et pourquoi c'est la vraie solution

Ces sept fichiers sont des **copies compressées** — 720 px, c'est la signature
d'un renvoi WhatsApp. **Les originaux du téléphone font 3 000 à 4 000 px.**
Avec eux, tout ce qui précède devient inutile : les sept passent en plein cadre.
👉 Les redemander depuis la galerie du téléphone, ou par Drive / e-mail en
« taille réelle ». C'est cinq minutes de sa part contre des visuels deux crans
au-dessus.

### 🔒 Droit à l'image (norme § 7.2)

- `ff2f2c99` — **utilisée** (`flyer48`). Plage vide ; deux embarcations à
  l'horizon, aucune personne identifiable. ✅
- `a8e67ba2`, `86669324` — barques et silhouettes lointaines, non identifiables.
  À recadrer si un jour on les utilise près du bord.
- Les autres : aucun sujet humain.

⚠️ **Aucune de ces photos ne montre un lieu qu'on nomme.** On dit « Mohéli »,
jamais le nom d'une plage précise : on ne l'a pas vérifié, et une légende fausse
sur un lieu que les gens connaissent coûte plus cher que pas de légende du tout.
