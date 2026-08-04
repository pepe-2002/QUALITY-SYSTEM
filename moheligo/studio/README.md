# MoheliGo Studio IA — v1.0

Studio de production publicitaire privé de MoheliGo. Il repose sur une idée simple,
celle du cahier des charges du patron : **on ne réinvente pas les personnages à chaque
vidéo**. On dispose d'une troupe permanente — 26 avatars au visage et à la voix
verrouillés — qu'on retrouve d'une pub à l'autre. À force, le public les reconnaît :
c'est ça, une identité de marque.

---

## Ce que le studio fait vraiment

Il y a deux moitiés dans une pub avec avatars : **décider** et **rendre**.

Le studio fait la totalité de la première moitié, et tout ce qui vient après le rendu :

| Étape | État |
|---|---|
| Bibliothèque de 26 avatars (identité, tenues, coiffures, expressions, voix) | ✅ opérationnel |
| Bibliothèque de 14 décors (dont Hoani, Ouroveni, Fomboni, vedette, marché…) | ✅ opérationnel |
| Grammaire : 8 caméras, 16 actions, 8 expressions, 11 ambiances | ✅ opérationnel |
| Compréhension d'une demande en français courant | ✅ opérationnel |
| Écriture du scénario, des dialogues, du découpage plan par plan | ✅ opérationnel |
| Prompts verrouillés (identité + seed) prêts pour le moteur vidéo | ✅ opérationnel |
| Voix off et dialogues synthétisés, calés à la milliseconde | ✅ opérationnel |
| Sous-titres SRT + incrustés | ✅ opérationnel |
| Animatique : le film complet en storyboard animé, avec le son | ✅ opérationnel |
| Montage, exports TikTok / Facebook / carré / YouTube / 4K, versions légères | ✅ opérationnel |
| Règles de marque appliquées automatiquement (mineurs, prix, mention IA) | ✅ opérationnel |
| **Génération des visages photoréalistes** | ⛔ **nécessite un moteur externe** |

**Le point important, dit franchement :** aucun modèle capable de fabriquer un visage
humain photoréaliste ne tourne dans cet environnement, et il n'en existe pas de gratuit
qui tienne la qualité voulue. Cette partie-là s'achète, chez un fournisseur (fal.ai,
Replicate, Runway, Kling, HeyGen). Le studio est construit pour ça : il prépare tout,
et le jour où une clé d'API est posée dans l'environnement, une seule commande envoie
les plans à générer et remonte le film avec les vraies images.

En attendant, l'animatique n'est pas un pis-aller : c'est **l'étape de validation**.
On voit le film, on l'entend, on ajuste le texte et le rythme — puis on ne paie la
génération que pour la version validée. C'est l'ordre de travail de n'importe quelle
agence.

---

## Les commandes

```bash
cd moheligo/studio

# la troupe : fiches individuelles + planche d'ensemble
python3 studio.py casting

# une demande en français → scénario + storyboard + prompts
python3 studio.py brief "Fais une publicité de 30 secondes où deux amis discutent
  au port de Hoani. L'un montre MoheliGo sur son téléphone. Ils réservent leur
  traversée puis montent dans la vedette. Voix en français et sous-titres." \
  --nom demo-hoani-30s --formats tiktok,facebook,youtube

# voix + animatique + exports (+ versions légères pour les Comores)
python3 studio.py produire demo-hoani-30s

# quand une clé d'API est disponible : génération des vraies images
python3 studio.py generer demo-hoani-30s --moteur fal
python3 studio.py monter  demo-hoani-30s      # remonte avec les rushes générés

# explorer la bibliothèque
python3 studio.py lister avatars|decors|cameras|actions|expressions|moteurs
```

---

## Les deux voies pour écrire un scénario

**1. L'analyseur automatique** (`moteur/langage.py`) — il tourne seul, sans connexion.
Il reconnaît les lieux, les rôles, les actions, la durée, la langue, les formats, et
construit un film en dix plans selon une structure éprouvée : accroche, objection,
solution, démonstration, preuve, embarquement, chute. C'est ce qui répond à
`studio.py brief`.

**2. Claude directement.** Quand je suis dans la session, j'écris le `scenario.json`
à la main : dialogues sur mesure, ruptures de rythme, jeux de mots en shikomori,
personnages secondaires. Le format est le même, toutes les commandes suivantes
fonctionnent pareil. La voie 1 sert quand le patron travaille seul ; la voie 2 quand
on cherche la finesse.

---

## Comment la cohérence est garantie

C'est le cœur du système, et ça tient en trois champs.

- **`identite`** — la description physique du personnage, en anglais, figée. Elle est
  recopiée telle quelle en tête de chaque prompt. On ne la reformule jamais.
- **`seed`** — le même nombre à chaque génération. Même identité + même seed = même
  visage.
- **`empreinte vocale`** — voix, débit et hauteur. Le stock de voix françaises étant
  limité (deux masculines, deux féminines), c'est le réglage débit/hauteur qui
  différencie les 24 personnages parlants : le Commandant Baco parle 14 % plus lentement
  et 12 Hz plus grave que la moyenne, Chamsia 6 % plus vite et 14 Hz plus haut.

Tenues, coiffures et expressions changent librement — c'est fait pour. Le visage, non.

---

## Les garde-fous

Le moteur **refuse de produire** un projet qui les viole, en expliquant pourquoi.

- **Enfants** (Salim, 9 ans ; Nailat, 7 ans) : jamais seuls à l'image, jamais de
  dialogue commercial, jamais de gros plan isolé, aucune voix de synthèse, aucun
  ciblage publicitaire. C'est la lecture stricte de la ligne du cahier des charges
  (« uniquement dans des contextes appropriés et non promotionnels ciblés »).
- **Prix** : tout montant hors de la fourchette réelle (15 000 – 17 500 FC) déclenche
  un avertissement à vérifier avant diffusion.
- **Mention IA** : « Personnages générés par intelligence artificielle » est incrusté
  sur le carton final de toutes les vidéos. Meta, TikTok et YouTube l'exigent, et le
  public comorien mérite de le savoir.
- **Interdits du patron** appliqués : pas d'emojis, pas de nappe sonore synthétique,
  pas d'impératif publicitaire à la fin, départ à **Ouroveni** et pas à Chindini,
  fichiers légers (3-5 Mo par minute).

---

## Organisation des fichiers

```
studio/
  bible/
    avatars.json      26 personnages permanents
    decors.json       14 lieux
    grammaire.json    caméras, actions, expressions, ambiances, musiques
    voix.json         casting vocal, empreintes, politique des langues
    marque.json       charte, interdits, règles, formats d'export
  moteur/
    bible.py          chargement + contrôle des règles
    langage.py        français → intentions
    scenario.py       intentions → plans et dialogues
    prompts.py        plans → prompts verrouillés
    voix.py           edge-tts + SRT
    montage.py        animatique, montage final, exports
    casting.py        fiches et planche de casting
    moteurs_video.py  branchement fal / Replicate / Runway / HeyGen
  casting/            fiches PNG + planche d'ensemble
  projets/<nom>/      scenario.json, storyboard.md, prompts.md, audio/, rushes/, mp4
  studio.py           ligne de commande
```

---

## Brancher un moteur de génération

Aucune clé n'est stockée dans le dépôt. On pose la variable dans l'environnement,
le studio détecte le reste.

| Moteur | Variable | Ce qu'il apporte | Ordre de prix constaté |
|---|---|---|---|
| fal.ai | `FAL_KEY` | images Flux + vidéo Kling | ~0,3 à 0,5 € par plan de 5 s |
| Replicate | `REPLICATE_API_TOKEN` | images + vidéo, large catalogue | comparable |
| Runway | `RUNWAY_API_KEY` | image-to-video Gen-3, bon mouvement | abonnement |
| HeyGen | `HEYGEN_API_KEY` | synchronisation labiale sur avatar photo | abonnement |

`python3 studio.py lister moteurs` indique lesquels sont configurés.

**Méthode recommandée**, la moins chère et la plus stable pour la cohérence :
1. générer **une fois** un portrait par avatar (26 images), les déposer dans
   `casting/portraits/AVA-0XX.png` — ils deviennent la référence permanente ;
2. pour chaque pub, faire de l'**image-to-video** à partir de ces portraits plutôt
   que du texte pur : le visage ne dérive pas ;
3. pour les plans de dialogue, passer la piste voix du studio dans un outil de
   synchronisation labiale.

Les chiffres de prix ci-dessus sont des ordres de grandeur de marché à vérifier au
moment de souscrire — ils ne sont pas contractuels.

---

## Ce qui reste à faire (feuille de route)

- [ ] Générer les 26 portraits de référence dès qu'une clé d'API est disponible.
- [ ] Enregistrer une banque de voix **shikomori humaines** (une vingtaine de phrases
      de marque). Aucune voix de synthèse shikomori n'existe ; le studio approxime
      aujourd'hui avec du swahili, ce qui convient pour caler une maquette mais **pas
      pour diffuser**.
- [ ] Incruster de vraies captures de l'application dans les plans « écran » (procédé
      Playwright déjà documenté dans `moheligo/MEMOIRE.md`).
- [ ] Déposer musiques et ambiances libres de droits dans `studio/audio/` avec leurs
      licences.
- [ ] Étendre la troupe si un segment manque (le cahier des charges prévoit
      l'ajout de nouveaux avatars — c'est une entrée à ajouter dans `avatars.json`,
      rien de plus).
