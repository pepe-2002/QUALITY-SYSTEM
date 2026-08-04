# Prompts de génération — MoheliGo — Port de Hoani

> À coller dans le moteur vidéo (Veo, Kling, Runway, Sora, Hailuo…) ou à envoyer
> par API via `moteur/moteurs_video.py`. **Ne pas reformuler le début du prompt** :
> c'est l'identité verrouillée de l'avatar et du décor, c'est elle qui garantit
> qu'on retrouve le même visage et le même lieu d'une pub à l'autre.

| Plan | Rôle | Durée | Seed |
|---|---|---|---|
| 1 | accroche | 3.3 s | `210001` |
| 2 | situation | 2.8 s | `110324` |
| 3 | objection | 2.8 s | `110324` |
| 4 | solution | 2.8 s | `110227` |
| 5 | demonstration | 3.3 s | `110227` |
| 6 | confirmation | 2.8 s | `110227` |
| 7 | adhesion | 2.8 s | `110324` |
| 8 | embarquement | 3.1 s | `110227` |
| 9 | traversee | 3.3 s | `210011` |
| 10 | chute | 3.0 s | `0` |

## Plan 1 — accroche (3.3 s)

**Seed : `210001`**

```
small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. aerial drone shot, smooth forward push, 40 metres above, slight downward tilt, cinematic. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

## Plan 2 — situation (2.8 s)

**Seed : `110324`**

```
Comorian man, 24 years old, dark brown skin, round friendly face, short dreadlocks tied back, light beard, stocky build, 1m72, gap between front teeth visible when laughing, wearing orange football jersey, black shorts, sandals, short dreadlocks tied back, talking to the other person, natural lip movement and gestures, relaxed, easy posture, half smile, calm breathing AND Comorian man, 27 years old, medium-dark brown skin, square jaw, short black fade haircut, thin moustache, expressive eyebrows, athletic build, 1m78, small scar above right eyebrow, wearing white t-shirt, open light denim shirt, dark chinos, white sneakers, short black fade, smiling warmly, eyes crinkling, relaxed, easy posture, half smile, calm breathing. Location: small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. cinematic medium shot, 35mm lens, shallow depth of field, slow lateral dolly, golden natural light. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

## Plan 3 — objection (2.8 s)

**Seed : `110324`**

```
Comorian man, 24 years old, dark brown skin, round friendly face, short dreadlocks tied back, light beard, stocky build, 1m72, gap between front teeth visible when laughing, wearing orange football jersey, black shorts, sandals, short dreadlocks tied back, talking to the other person, natural lip movement and gestures, worried, furrowed brow, tense jaw, glancing aside AND Comorian man, 27 years old, medium-dark brown skin, square jaw, short black fade haircut, thin moustache, expressive eyebrows, athletic build, 1m78, small scar above right eyebrow, wearing white t-shirt, open light denim shirt, dark chinos, white sneakers, short black fade, smiling warmly, eyes crinkling, relaxed, easy posture, half smile, calm breathing. Location: small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. cinematic medium shot, 35mm lens, shallow depth of field, slow lateral dolly, golden natural light. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

## Plan 4 — solution (2.8 s)

**Seed : `110227`**

```
Comorian man, 27 years old, medium-dark brown skin, square jaw, short black fade haircut, thin moustache, expressive eyebrows, athletic build, 1m78, small scar above right eyebrow, wearing white t-shirt, open light denim shirt, dark chinos, white sneakers, short black fade, turning the smartphone screen towards the other person and pointing at it, the screen clearly visible, enthusiastic, bright eyes, animated gestures, leaning forward AND Comorian man, 24 years old, dark brown skin, round friendly face, short dreadlocks tied back, light beard, stocky build, 1m72, gap between front teeth visible when laughing, wearing orange football jersey, black shorts, sandals, short dreadlocks tied back, smiling warmly, eyes crinkling, surprised, raised eyebrows, slightly open mouth, wide eyes. Location: small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. cinematic medium shot, 35mm lens, shallow depth of field, slow lateral dolly, golden natural light. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

## Plan 5 — demonstration (3.3 s)

**Seed : `110227`**

```
Comorian man, 27 years old, medium-dark brown skin, square jaw, short black fade haircut, thin moustache, expressive eyebrows, athletic build, 1m78, small scar above right eyebrow, wearing white t-shirt, open light denim shirt, dark chinos, white sneakers, short black fade, holding a smartphone, thumb scrolling, eyes on the screen, serious, steady gaze, composed face, professional. Location: small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. close-up shot, 85mm lens, face filling the frame or hands on a phone screen, creamy bokeh. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

> ⚠ L'écran de l'application n'est PAS généré par le moteur : filmer l'app réelle (moheligo.com) puis incruster l'écran dans le téléphone au montage. Procédé documenté dans MEMOIRE.md (Playwright, viewport 540x960).

## Plan 6 — confirmation (2.8 s)

**Seed : `110227`**

```
Comorian man, 27 years old, medium-dark brown skin, square jaw, short black fade haircut, thin moustache, expressive eyebrows, athletic build, 1m78, small scar above right eyebrow, wearing white t-shirt, open light denim shirt, dark chinos, white sneakers, short black fade, confirming a mobile money payment on a phone, small satisfied nod, happy, genuine warm smile, relaxed eyes. Location: small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. close-up shot, 85mm lens, face filling the frame or hands on a phone screen, creamy bokeh. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

> ⚠ L'écran de l'application n'est PAS généré par le moteur : filmer l'app réelle (moheligo.com) puis incruster l'écran dans le téléphone au montage. Procédé documenté dans MEMOIRE.md (Playwright, viewport 540x960).

## Plan 7 — adhesion (2.8 s)

**Seed : `110324`**

```
Comorian man, 24 years old, dark brown skin, round friendly face, short dreadlocks tied back, light beard, stocky build, 1m72, gap between front teeth visible when laughing, wearing orange football jersey, black shorts, sandals, short dreadlocks tied back, talking to the other person, natural lip movement and gestures, enthusiastic, bright eyes, animated gestures, leaning forward AND Comorian man, 27 years old, medium-dark brown skin, square jaw, short black fade haircut, thin moustache, expressive eyebrows, athletic build, 1m78, small scar above right eyebrow, wearing white t-shirt, open light denim shirt, dark chinos, white sneakers, short black fade, laughing out loud, head slightly back, happy, genuine warm smile, relaxed eyes. Location: small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. cinematic medium shot, 35mm lens, shallow depth of field, slow lateral dolly, golden natural light. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

## Plan 8 — embarquement (3.1 s)

**Seed : `110227`**

```
Comorian man, 27 years old, medium-dark brown skin, square jaw, short black fade haircut, thin moustache, expressive eyebrows, athletic build, 1m78, small scar above right eyebrow, wearing white t-shirt, open light denim shirt, dark chinos, white sneakers, short black fade, stepping onto a moored speedboat, one hand held by a crew member, bag on the shoulder, enthusiastic, bright eyes, animated gestures, leaning forward AND Comorian man, 24 years old, dark brown skin, round friendly face, short dreadlocks tied back, light beard, stocky build, 1m72, gap between front teeth visible when laughing, wearing orange football jersey, black shorts, sandals, short dreadlocks tied back, stepping onto a moored speedboat, one hand held by a crew member, bag on the shoulder, happy, genuine warm smile, relaxed eyes. Location: small tropical island harbour at Hoani, Mohéli, Comoros: concrete jetty worn by salt, colourful wooden speedboats moored, turquoise shallow water, volcanic dark sand, coconut palms behind, low green hills in the background, Indian Ocean light. golden hour, warm low sun, long shadows. cinematic medium shot, 35mm lens, shallow depth of field, slow lateral dolly, golden natural light. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/plage-vedettes.jpg`

## Plan 9 — traversee (3.3 s)

**Seed : `210011`**

```
open Indian Ocean between Grande Comore and Mohéli: deep blue water, white wake of a fast speedboat, distant volcanic island silhouette, scattered clouds, strong tropical sunlight. golden hour, warm low sun, long shadows. aerial drone shot, smooth forward push, 40 metres above, slight downward tilt, cinematic. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

*Image de référence (image-to-video) :* `../pub/photos/vedette-mer.jpg`

## Plan 10 — chute (3.0 s)

**Seed : `0`**

```
plain brand background, no location. golden hour, warm low sun, long shadows. static locked-off shot on a tripod, eye level, balanced composition, no camera movement. photorealistic, natural skin texture, realistic anatomy, documentary photography style, shot on a full-frame camera, high dynamic range.
```

*À exclure :* `no text, no watermark, no logo, no subtitles, no distorted hands, no extra fingers, no plastic skin, no cartoon, no stock-photo smile, no snow, no western city`

> ⚠ Carton final composé par le studio (PIL/ffmpeg), pas par le moteur d'image.
