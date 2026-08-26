# 🎨 LA CHARTE MoheliGo — une page, et rien à discuter

> **Ouverte le 26/08/2026**, après un audit extérieur du flyer de suspension.
> L'audit conseillait de « verrouiller les couleurs et ne plus en changer ».
> **Vérification faite sur les 43 fichiers : il avait raison, ça avait dérivé.**
>
> ⚠️ **CE FICHIER N'INVENTE RIEN.** Chaque valeur ci-dessous a été **comptée dans
> les fichiers réels**, pas décidée à la volée. C'est ce qu'on fait déjà, écrit
> une bonne fois — pour qu'on cesse de le refaire de mémoire.

---

## 1. Les couleurs — mesurées, pas choisies

| Rôle | Valeur | Emplois relevés |
|---|---|---|
| **Marine MoheliGo** | **`#0F2A5C`** | **153** — le fond de tout |
| **Or MoheliGo** | **`#F6BC1C`** | **203** — l'accent, jamais le fond |
| **Marine profond** | `#0A1D42` | 39 — réservé aux **avis** (suspension, mer forte) |
| **Blanc** | `#FFFFFF` | 282 — l'air |
| **Carte claire** | `#F6F9FF` | 21 — les blocs d'information |
| Bleus de texte | `#DBEAFE` `#93C5FD` `#E2ECFB` | sous-titres et légendes |

🚨 **LA DÉRIVE TROUVÉE LE 26/08** : deux fichiers utilisaient **`#facc15`** (un or
plus citron) et **`#071c3d`** (un marine plus froid) — dont **la carte finale de
la vidéo Young Leader, faite le jour même**. Corrigés.

📌 **La règle** : `#0F2A5C` et `#F6BC1C`. **Deux valeurs, pas quatre.** Un or « à
peu près pareil » n'est pas le même or : c'est ce qui fait qu'une page ressemble
à une marque ou à une accumulation de visuels.

---

## 2. Les polices — trois, chacune à sa place

| Police | Poids | Pour quoi | Emplois |
|---|---|---|---|
| **Archivo** | 900 / 800 / 700 | **les grands titres** | 224 |
| **Inter** | 700 / 600 / 500 | le texte courant, les chiffres | 112 |
| **Montserrat** | 900 / 800 | les titres de la famille « affiche » | 35 |

Les fichiers sont **dans le dépôt** (`pub/flyers/fonts/*.woff2`) — jamais chargés
depuis internet, sinon un flyer fabriqué sans réseau change d'allure.

⚠️ **Piège payé le 26/08** : le sous-ensemble **`latin-ext` d'Inter ne contient
pas la lettre A**. Pour un usage hors navigateur (vidéo, image), prendre
**`Inter-700-latin`** et **vérifier la couverture avant de s'en servir**.

---

## 3. La forme propriétaire — le coin blanc

Le **coin blanc en biais** en haut à gauche, qui porte le logo. Présent sur
**25 visuels sur 43**.

📌 **C'est notre signature graphique, et l'audit a raison : il faut la pousser
partout.** Quelqu'un doit reconnaître MoheliGo **logo caché**. Objectif : les 43.

Les autres constantes de forme : la **vague dorée** en pied, les **cartes claires
à bande dorée** pour les listes, les **numéros en pastille** pour les étapes.

---

## 4. Le ton — déjà écrit, et il tient

**On tutoie. On dit ce qu'on sait. On ne promet pas ce qu'on ne tient pas.**

| On écrit | On n'écrit pas |
|---|---|
| « Ne descends pas au port pour rien. » | « Avis important concernant la suspension… » |
| « Tu le sais avant de descendre au port. » | « Nous informons notre aimable clientèle… » |
| « On ne le sait pas encore. » | une date qu'on n'a pas |

---

## 5. La signature — **elle existe déjà, on n'en change pas**

> # La mer décide. Nous, on te le dit avant.

⚠️ L'audit extérieur proposait « MoheliGo — Vous savez avant de partir ».
**C'est la même idée, en moins bien** : plus vague, et surtout **elle a le défaut
que la nôtre évite** — la nôtre dit d'abord *ce qu'on ne maîtrise pas* (la mer),
et c'est ça qui la rend croyable.

📌 **Une signature qui marche ne se remplace pas parce qu'un avis extérieur en
propose une autre.** On la répète jusqu'à ce qu'elle colle à la marque.

---

## 6. Les cinq familles de publication

Reprises de l'audit, parce que l'idée est juste : on les fabrique déjà, on ne les
nommait pas.

| Famille | Fond | Quand |
|---|---|---|
| 🔵 **AVIS** | marine profond `#0A1D42` | suspension, mer forte, reprise |
| 🔵 **BULLETIN** | marine `#0F2A5C` | la mer de demain, tous les soirs |
| 🟡 **RÉSERVER** | marine + or dominant | comment ça marche, garantie, prix |
| 🔵 **DÉCOUVRIR** | photo + voile marine | Mohéli, les ports, la destination |
| 🟡 **INSTITUTIONNEL** | carte claire | partenariats, présentation |

📌 **Le changement de fond EST le message** : quand quelqu'un voit le marine
profond, il sait avant de lire que c'est un avis.

---

## 🚨 CE QUE LA CHARTE NE RÉSOUT PAS — et il faut le dire

L'audit note le flyer **8/10** et propose d'aller vers « le niveau grand groupe ».
**Ce n'est pas notre goulot.**

| Ce qu'on sait | Le chiffre |
|---|---|
| Vues de la page | **3 000 en 28 jours** — la portée monte |
| Ouvertures de l'app → écran Traversées | **140 → 16, soit 11 %** |
| Traversées payées depuis juillet | **3** |

**Neuf personnes sur dix ouvrent l'application et ne voient jamais un départ.**
Aucun flyer, même 10/10, ne répare ça.

➡️ **La charte sert à ne PAS repenser le design à chaque fois** — donc à libérer
du temps pour le vrai chantier : **mettre les départs dans les écrans les plus
consultés**, et régler le prix affiché.

> **Un design à 8/10 répété cent fois bat un design à 10/10 changé chaque semaine.
> Et les deux ensemble ne valent rien si personne ne trouve le bouton Réserver.**
