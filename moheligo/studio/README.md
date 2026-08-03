# 🎬 Studio MoheliGo — fabrique de dessins animés

Un mini-studio d'animation maison : on écrit un **épisode** dans un fichier
texte (JSON), le studio **dessine**, **fait parler** les personnages et
**monte** la vidéo tout seul. Aucun service payant, aucune image extérieure.

## Fabriquer un épisode

```bash
cd moheligo/studio
node rendre.mjs episodes/ep1-le-billet-damina.json
```

Sortie : `moheligo/pub/serie/<fichier>.mp4` (1080×1920) et
`<fichier>-leger.mp4` (720×1280, pour les connexions comoriennes).

Options :

| Option | Effet |
|---|---|
| `--apercu 3,12,40` | ne sort que des images fixes PNG à ces secondes (pour juger le style sans attendre le rendu) |
| `--muet` | réutilise les voix déjà fabriquées (pas de nouvel appel au service de voix) |
| `--sortie <dossier>` | change le dossier de sortie |

Prérequis de la machine : `ffmpeg`, `edge-tts` (`pip install edge-tts imageio-ffmpeg`),
Chromium de Playwright (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`).

## Écrire un épisode

Un épisode = une liste de **plans**. Chaque plan a un décor, des acteurs, une
réplique. **La durée d'un plan est calculée toute seule** à partir de la voix
(0,25 s avant, 0,55 s après) ; `duree_min` impose un minimum.

```jsonc
{
  "titre": "…", "fichier": "ep2-...", "fps": 25,
  "personnages": {
    "amina": { "voix": "fr-FR-DeniseNeural", "rate": "-6%",
               "look": { "peau": "#8d5524", "tenue": "#e94f6a", "motif": "#ffd75e",
                         "coiffe": "shiromani", "coifCouleur": "#f6bc1c" } }
  },
  "plans": [
    { "decor": "village_matin",
      "camera": { "zoom": [1.0, 1.06], "focus": [0.5, 0.7] },
      "acteurs": [ { "qui": "amina", "x": 0.36, "y": 0.93, "h": 760, "dir": 1,
                     "bras": "telephone", "pose": "debout" } ],
      "replique": { "qui": "amina", "texte": "Ce qui s'affiche en sous-titre",
                    "dit": "ce qui est prononcé (optionnel)" } }
  ]
}
```

### Décors disponibles
`village_matin` · `port_ouroveni` · `mer_large` · `a_bord` · `hoani` · `carton`

### Acteurs
- `x`, `y` : position en fraction de l'écran (`y` = le sol sous les pieds) ·
  `xFin` : le personnage se déplace pendant le plan.
- `h` : hauteur en pixels · `dir` : 1 (regarde à droite) ou -1.
- `pose` : `debout` · `marche` · `assis`.
- `bras` : `repos` · `telephone` (un téléphone apparaît dans la main) ·
  `salut` · `ouverts` · `valise`.
- `sourire` (0→1), `sourcils` (1 = froncés).
- **La bouche est synchronisée automatiquement** sur la voix du personnage qui
  parle dans ce plan.

### Objets
```jsonc
"objets": [ { "type": "telephone", "x": 0.5, "y": 0.45, "taille": 1.5,
              "ecran": "billet", "apparait": 0.1 } ]
```
Écrans de l'appli : `accueil` · `recherche` · `resultats` · `paiement` · `billet`.
`{"type":"bulle","texte":"…"}` affiche une bulle de BD.

`"insert": true` efface le décor derrière l'objet (gros plan publicitaire).
`"logo": true` affiche la carte finale (logo + moheligo.com).
`"titre"` / `"sousTitre"` affichent un carton.

### Voix
Voix neuronales Microsoft (edge-tts) :
`fr-FR-DeniseNeural` (femme) · `fr-FR-HenriNeural` (homme) ·
`fr-FR-RemyMultilingualNeural` · `fr-FR-VivienneMultilingualNeural`.
Si une voix n'est pas disponible, le studio bascule sur Henri/Denise.

## Comment ça marche

1. `rendre.mjs` fabrique un fichier de voix par réplique (edge-tts).
2. Il mesure chaque voix → en déduit la durée de chaque plan.
3. Il calcule l'**enveloppe** du son (une valeur par image) → l'ouverture de
   la bouche.
4. Chromium ouvre `engine/index.html` et dessine chaque image sur un canvas
   (`engine/dessin.js` = décors et personnages, `engine/moteur.js` = scènes,
   caméra, fondus, sous-titres).
5. Les images partent directement dans ffmpeg (rien n'est stocké sur le disque),
   puis la bande son est collée dessus.

Tout est **déterministe** : deux rendus du même épisode donnent exactement la
même vidéo.

## Limites connues

- Style dessin animé 2D, pas photoréaliste (voir `MEMOIRE.md`).
- Rendu ~4 à 8 images/seconde sur cette machine : compter environ 6 à 10 min
  pour 90 s de film.
- Pas de musique (le patron ne veut pas de nappe synthétique) : voix seules.
