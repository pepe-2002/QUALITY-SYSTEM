# 🎬 La publicité Young Leader — le montage

**`MoheliGo-YoungLeader.mp4`** — 40,4 s, 576×1024 vertical, sous-titres incrustés.
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
| `../flyers/carte-fin-video.html` | la carte finale, rendue par l'atelier des flyers |

## Ce qui a été corrigé

| Défaut d'origine | Correction |
|---|---|
| **aucune adresse**, écran noir illisible 5,5 s | carte finale : signature exacte + **moheligo.com** |
| nom MoheliGo à la 25ᵉ seconde | **logo dès la 1ʳᵉ seconde** |
| 5 fautes incrustées (*proposez, entre…vers, rendiez, abonnez, sur lien*) | **sous-titres entièrement refaits** |
| « Moheligo » puis « MoheliGo » | **`MoheliGo` partout**, en or |
| 50 s d'un seul plan fixe | **4 photos réelles** dont le port de Hoani |
| 52,5 s | **40,4 s** |

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
