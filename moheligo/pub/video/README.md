# 🎬 La publicité Young Leader — le montage

**`MoheliGo-YoungLeader.mp4`** — 39,5 s, 576×1024 vertical, sous-titres incrustés.
Montée le 26/08/2026 à partir de la vidéo tournée par **El Farouk Saindou,
Young Leader Mohéli 2026**, sur commande du patron : *« tu peux utiliser cette
vidéo et des images pour en faire une vraie et corriger les fautes ».*

## Refabriquer

```bash
cd moheligo/pub/video
python3 monter.py --source /chemin/vers/la-video-recue.mp4
```

Tout est dans `monter.py`, en tête de fichier : les coupes, le recadrage, les
plans de coupe, la carte finale. **Ne rien corriger à la main sur le .mp4** —
on corrigerait la copie au lieu de la source.

| Fichier | Ce que c'est |
|---|---|
| `monter.py` | le montage complet, commenté |
| `sous-titres.ass` | **les sous-titres refaits**, fautes corrigées, calés sur les silences de la voix |
| `polices/` | Inter 700 de la marque, convertie en TTF pour ffmpeg |
| `port-hoani.jpg` | le port de Hoani, envoyé par le patron le 26/08/2026 |
| `bande-lien.png` | la pastille `moheligo.com`, affichée quand il parle du lien |
| `../flyers/carte-fin-video.html` | la carte finale, rendue par l'atelier des flyers |

## Ce qui a été corrigé

| Défaut d'origine | Correction |
|---|---|
| **aucune adresse**, écran noir illisible 5,5 s | carte finale : signature exacte + **moheligo.com** |
| nom MoheliGo à la 25ᵉ seconde | **logo dès la 1ʳᵉ seconde** |
| 5 fautes incrustées (*proposez, entre…vers, rendiez, abonnez, sur lien*) | **sous-titres entièrement refaits** |
| « Moheligo » puis « MoheliGo » | **`MoheliGo` partout**, en or |
| 50 s d'un seul plan fixe | **4 photos réelles** dont le port de Hoani |
| 52,5 s | **39,5 s** |

## 🔁 Deuxième passe — les trois défauts vus par le patron (26/08/2026)

> « entre Mohéli et Ngazidja il parle avant et l'image vient après ; il y a des A
> qui sont trop petits ; il a parlé de lien et on voit pas le lien cliquable »

| Défaut | Cause | Correction |
|---|---|---|
| **l'image arrive après la voix** | mes temps venaient des **silences** de la bande son — trois phrases tombaient à côté | **relevé exact des sous-titres d'origine** (masque du jaune, pas de 0,1 s) ; chaque plan démarre **0,5 s avant** sa phrase |
| **les « A » trop petits** | j'avais pris le sous-ensemble **`latin-ext`** de la police Inter — **il ne contient pas le « A »**, une police de secours le remplaçait | `polices/Inter-700.ttf`, converti depuis **`Inter-700-latin`**, qui a tout |
| **pas de lien cliquable** | **une vidéo ne peut pas en contenir** | pastille **`moheligo.com`** affichée pendant qu'il en parle + le lien cliquable dans le **texte de la publication** (`dossier/TEXTES-PUBLICATIONS.md`) |

📌 **Et un défaut trouvé au passage** : « pour des informations quelconques »
était encore **à moitié dans le son**, sans sous-titre. La coupe a été refaite.

⚠️ **La leçon** : les sous-titres du tournage sont la seule vérité disponible sur
qui dit quoi et quand — **ils ont été écrits par quelqu'un qui entendait**. Les
silences ne disent que « il parle / il ne parle pas ».

## ⚠️ Deux réserves à lever avant publication

1. **Le fichier source est une version compressée par WhatsApp (576×1024).**
   Demander l'original au Young Leader et relancer `monter.py` : rien d'autre à
   changer que `--source`.
2. 🔴 **La phrase de droits à l'image n'est pas obtenue par écrit** (voir
   `dossier/BRIEF-VIDEO-YOUNG-LEADER.md`). L'accord était verbal.

## Un point de méthode

Les temps des sous-titres **ne sont pas devinés** : ils viennent du relevé des
silences de la bande son. Le patron devrait tout de même **la regarder une fois
en entier** — je n'ai pas d'oreilles, je n'ai vérifié que les images.
