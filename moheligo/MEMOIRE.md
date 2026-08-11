# 📚 MÉMOIRE — Directeur Marketing MoheliGo (Claude)

> **Consigne pour moi-même** : lire ce fichier en début de session MoheliGo,
> le mettre à jour à chaque avancée, et le pousser sur GitHub.
> Dernière mise à jour : **07/08/2026** — flyers promo brillants + **bulletin du
> soir généré depuis la vraie prévision de mer**. **Index des fichiers : section 2 bis.**

---

## 1. Le projet

**MoheliGo** — plateforme de réservation des traversées maritimes des Comores
(Grande Comore ↔ Mohéli). En production : **https://moheligo.com** (Cloudflare,
backend Supabase, PWA autonome en un seul index.html + modules js).

- Fonctions clés : réservation avec billet QR, paiement MVola/KartaPay, météo
  mer 7 jours (Open-Meteo + bulletin ANACM), suivi GPS des vedettes, guide de
  l'île (hôtels, tortues, baleines), espaces client/commandant/admin, chat
  « Réception MoheliGo », support WhatsApp.
- Ports : Chindini, Ouroveni (Grande Comore) · Hoani, Fomboni (Mohéli).
- Prix typiques : 15 000 – 17 500 FC. Vedettes : Mwezi Express, Ylang Star…
- Réseaux : page Facebook « MoheliGo » (à faire grandir), vidéos sur
  videos.moheligo.com.

**Le patron** : pepe-2002 (Nayam). Parle français, style direct, veut du
niveau « grand conglomérat » (Apple/Coca-Cola). M'a nommé Directeur Marketing
le 02/08/2026.

## 2. État des livrables marketing (02/08/2026)

Tout est dans `moheligo/pub/` :

| Fichier | Contenu | Durée | Poids léger |
|---|---|---|---|
| `v1-demo(-leger).mp4` | Visite guidée de l'app | 63 s | 2,7 Mo |
| `v2-premium(-leger).mp4` | Cartons typo sur photos + app | 63 s | 4,1 Mo |
| `v3-cinema(-leger).mp4` | Photos réelles + app | 72 s | 5,2 Mo |
| `v4-film(-leger).mp4` | Mini-film « Amina » (histoire d'une voyageuse) | 60 s | 4,4 Mo |
| `textes-publications.md` | Légendes FB/WhatsApp + conseils de diffusion | — | — |
| `photos/` | 6 photos réelles de Mohéli fournies par le patron | — | — |
| `scenario-film.txt` | Script voix du film Amina | — | — |
| `v5-destination(-leger).mp4` | Pub tourisme : satellite, tortues, dauphins, coraux, carte satellite interactive + app (Ouroveni → Hoani) | 54 s | 4,4 Mo |
| `flyers/` | Flyer premium 2160×2700 (HTML source + PNG) — QR vers moheligo.com | — | — |
| `photos-cc/` + `CREDITS.md` | 6 images CC de Mohéli (Wallace, Stanley, Commons) + obligations de crédit | — | — |
| `flyers/flyer-corporate-A4.png` | Flyer institutionnel A4 300 dpi (07/08) — impression, partenaires | — | — |
| `flyers/flyer-corporate-facebook.png` | Même flyer en 4:5 pour le feed FB/Insta | — | — |
| `flyers/flyer-nuit-facebook.png` | Flyer nuit 4:5 — 2ᵉ publication du soir (22h30-minuit), angle « réservez ce soir, partez demain » + diaspora | — | — |
| `flyers/flyer-affiche-facebook.png` | Affiche « destination » 4:5 — îlots de Nioumachoua (photo libre CC BY 3.0 étalonnée), 3ᵉ publication, registre émotion | — | — |
| `flyers/flyer-affiche-vedette-facebook.png` | Même affiche avec notre photo de vedette en pleine mer (aucune licence, aucun crédit) | — | — |
| `flyers/flyer-promo-facebook.png` | Flyer promo 4:5 style « affiche locale » : vague, bulle de prix, bande d'action or — le plus accrocheur | — | — |
| `flyers/flyer-promo-A4.png` | Le promo en A4 300 dpi imprimable + bande « comment ça marche » (ports, boutiques, hôtels) | — | — |
| `flyers/flyer-promo-brillant-facebook.png` | ⭐ Le plus abouti : promo « brillant » (or métallique, reflets spéculaires, soleil sur la mer, éclats) | — | — |
| `flyers/flyer-promo-brillant-A4.png` | Le brillant en A4 300 dpi imprimable | — | — |
| `flyers/flyer-affiche-duotone-facebook.png` | ⭐ **La plus belle** : affiche de voyage duotone marine/or (`duotone.py`), une seule idée, grain, anneau de soleil. Sans date. | — | — |
| `flyers/flyer-diaspora-facebook.png` | Flyer pub « diaspora » : « Tu paies ici. Il embarque. » — payer la traversée d'un proche depuis la France, Mayotte ou le Golfe. Sans date. | — | — |
| `flyers/flyer-soir-facebook.png` | ⭐ **Bulletin du soir** : la vraie mer de demain matin (Open-Meteo), jauge Douglas + courbe de houle, panneau en verre. **Daté : à regénérer chaque jour.** | — | — |

Retours du patron : ①voix Piper jugée trop rapide/robotique → remplacée par
edge-tts Henri, validé ; ②nappe « océan » synthétique perçue comme un bug →
supprimée, silence propre ; ③fichiers trop lourds pour les connexions
comoriennes → versions 720p ~3-5 Mo.

## 2 bis. 📌 OÙ SONT LES FICHIERS DES FLYERS (à ouvrir en premier)

Tout est dans **`moheligo/pub/flyers/`**. Le fichier à ouvrir dépend de ce
qu'on veut faire :

| Je veux… | Fichier source à modifier | PNG produit |
|---|---|---|
| **L'AFFICHE À UTILISER (mer vraie)** | `flyer12-affiche-vraie-fb.html` + `affiche.py` | `flyer-affiche-vraie-facebook.png` |
| L'affiche lumineuse duotone (gardée) | `flyer11-affiche-lumineuse-fb.html` + `duotone.py` | `flyer-affiche-lumineuse-facebook.png` |
| L'affiche duotone sombre (gardée) | `flyer10-affiche-duotone-fb.html` + `duotone.py` | `flyer-affiche-duotone-facebook.png` |
| Le flyer diaspora (angle le plus rentable) | `flyer9-diaspora-fb.html` | `flyer-diaspora-facebook.png` |
| **Le bulletin du soir (format le plus fort)** | `bulletin.py` + `flyer8-soir-fb.template.html` | `flyer-soir-facebook.png` — **regénérer chaque jour** |
| **Améliorer le design (LE MEILLEUR, repartir de là)** | **`flyer7-promo-brillant-fb.html`** | `flyer-promo-brillant-facebook.png` (2160×2700) |
| Le brillant en A4 imprimable | `flyer7-promo-brillant-A4.html` | `flyer-promo-brillant-A4.png` (2480×3508, 300 dpi) |
| Le promo mat (version précédente, gardée) | `flyer6-promo-fb.html` / `flyer6-promo-A4.html` | `flyer-promo-facebook.png` / `flyer-promo-A4.png` |
| Le flyer institutionnel A4 | `flyer2-corporate.html` | `flyer-corporate-A4.png` |
| Le flyer institutionnel pour le feed | `flyer2-corporate-fb.html` | `flyer-corporate-facebook.png` |
| Le flyer nuit (publication de fin de soirée) | `flyer3-nuit-fb.html` | `flyer-nuit-facebook.png` |
| L'affiche destination (îlots de Nioumachoua) | `flyer4-affiche-fb.html` | `flyer-affiche-facebook.png` |
| L'affiche destination (notre vedette) | `flyer5-affiche-vedette-fb.html` | `flyer-affiche-vedette-facebook.png` |

Fichiers de service, dans le même dossier :

- **`render.js`** — transforme un HTML en PNG :
  `node render.js source.html sortie.png LARGEUR HAUTEUR 2` (le 2 = ×2, donc
  1240×1754 → A4 300 dpi, 1080×1350 → 2160×2700 pour Facebook).
- **`affiche.py`** — étalonne les photos des affiches (dévoilage, lumière).
- **`nuit.py`** — transforme une photo de jour en nuit (flyer nuit).
- **`soir.py`** — étalonnage fin de journée (ciel de crépuscule, soleil bas,
  chemin de lumière, bloom) → `vedette-soir.jpg`. Compter ~1 min de calcul.
- **`bulletin.py`** — va chercher la vraie prévision de mer et fabrique le
  flyer du soir. `bulletin.json` garde les chiffres pour le texte du post.
- **`page.py`** — regénère **toute** la page web du patron (météo de demain +
  les flyers en grand + textes + boutons copier), à publier ensuite comme
  artifact sur la même adresse. ⚠️ **Ne jamais rapiécer la page à la main** :
  une retouche par recherche-remplacement a déjà effacé deux blocs. On modifie
  la liste `FLYERS` en haut de `page.py` et on relance.
- **`duotone.py`** — mappage de dégradé marine→or + grain : transforme une
  photo en image d'affiche. C'est ce traitement qui a donné le plus beau
  visuel de tous. Recette expliquée dans `README.md`.
- **`fonts/`** — Montserrat + Inter en local, ne pas retélécharger.
- **`logo-emblem.png` / `logo-lockup.png`** — logo officiel détouré.
- **`qr-moheligo.png`** — QR vers moheligo.com.
- **`README.md`** — le **système de design** complet (couleurs exactes, rayons,
  ombres, recette de la vague et du bloc surligneur) + toutes les commandes de
  regénération. **À relire avant de retoucher un flyer.**

Textes des publications Facebook : `moheligo/pub/textes-publications.md`
(une section par flyer, avec le premier commentaire et la version WhatsApp).

➡️ **PROCHAINE SESSION** : repartir de **`flyer7-promo-brillant-fb.html`**
(version la plus aboutie, passe « brillance » appliquée), jamais de zéro. La
recette complète de la brillance est écrite dans `pub/flyers/README.md`,
section « La recette ça brille » — **la relire avant de toucher un flyer**.
Question encore ouverte : ce flyer **tutoie**, les trois autres vouvoient —
demander au patron laquelle des deux formes devient la règle.

🔑 **CE QUE LE PATRON APPELLE « UN TRAVAIL DE DESIGNER PRO »** (07/08/2026,
en comparant avec Yas) : « c'est comme si ça brille ». Traduction technique —
aucun aplat, tout est dégradé ; liseré blanc intérieur en haut + ombre chaude
intérieure en bas sur chaque élément or ; reflet spéculaire flouté ; balayage
de lumière en diagonale ; texte rempli d'un dégradé (`background-clip:text`) ;
lumière du soleil sur la photo. **Retenir : quand il dit « améliore le
design », il parle de matière et de lumière, pas de mise en page.**

🚫 **DEUX REFUS DU 07/08/2026, définitifs :**
1. **Pas d'éclats / petites étoiles** sur les visuels — « ça fait enfants et
   femme ». La brillance vient de la matière, jamais d'un décor ajouté.
2. **Montserrat écartée pour les titres** : il voulait « une écriture façon
   pro » → **Archivo 800/900** (plus sèche, plus éditoriale), Inter pour le
   texte courant, plate de titre droite sans rotation, rayons resserrés,
   fond clair froid sans halo crème. Polices déjà commitées dans
   `pub/flyers/fonts/`. ⚠️ Archivo est plus large que Montserrat : compter
   71-78 px de corps là où Montserrat tenait à 84-90 px, sinon le titre passe
   sur trois lignes et écrase la mise en page.

## 3. Acquis techniques (comment refaire)

### Filmer l'app en local
- Servir `moheligo/` : `python3 -m http.server 8877`.
- Playwright + Chromium préinstallé (`/opt/pw-browsers/chromium`), contexte
  persistant, viewport mobile 540×960, `recordVideo`, locale fr-FR,
  timezone Indian/Comoro, `serviceWorkers: 'block'`.
- **Bloquer** supabase/jsdelivr/unpkg/etc. (route abort) → l'app passe en mode
  local. **Intercepter** open-meteo et servir un JSON réel récupéré via curl
  (proxy: `--cacert /root/.ccr/ca-bundle.crt`).
- Données de démo : IndexedDB `moheligo` v2, store `traversees`
  `{id, boat, dep, arr, date, time, price, cap, booked}` — dates à J+1 sinon
  filtrées comme « passées ».
- localStorage : `mg_ob_done=1` (masquer l'onboarding), `mg_lang=fr`,
  `mg_push_asked=1`, `mg_pt_seen=1`. ⚠️ `mg_seen` doit être un TABLEAU JSON
  (jamais "1", sinon crash au boot `seen.indexOf`).
- Sélecteurs utiles : `#f-dep/#f-arr/#f-date` + `.bk-cta` (recherche),
  `openAuth()` puis « Créer un compte gratuit » puis `#su-name/#su-phone`,
  `.cnav >> text=Onglet` (navigation), `.wx-cta` (météo fiable — éviter la
  story qui défile), `.stories` (stories accueil).
- Faux « doigt » : div fixe qui suit mousemove (injectée en addInitScript).

### Voix off
- **edge-tts** (voix naturelle, LA bonne solution) :
  `edge-tts --proxy "$HTTPS_PROXY" --voice fr-FR-HenriNeural --rate=-8%`
  avec `SSL_CERT_FILE=/root/.ccr/ca-bundle.crt` et `</dev/null` dans les
  boucles shell (sinon il avale stdin). Autres voix : DeniseNeural (femme),
  RemyMultilingual.
- Piper local en secours (fr_FR-siwis-medium) — qualité inférieure.
- Booster la voix au montage : `volume=5dB` (edge-tts sort à −22 dB moyen).

### Montage ffmpeg
- Segments uniformes 1080×1920/30fps h264 crf19, enchaînés par `xfade`
  (offsets cumulés = somme des durées − n×fondu). Calculer les offsets en
  python et générer la commande.
- Voix placées par `adelay` + `amix normalize=0` + `alimiter`.
- Ken Burns photos : PIL pour composer (fond flouté pour photos < 1080p,
  cartons texte sur photo assombrie 0.62) puis
  `-loop 1 -framerate 30 -t D -i img` + zoompan (⚠️ sans `-framerate 30`,
  les durées rétrécissent ×25/30).
- Cartons finaux : logo en « icône d'app » (coins arrondis + ombre PIL).
- Pas de nappe sonore synthétique (le patron n'aime pas). Si ambiance un
  jour : vrai enregistrement, jamais du bruit filtré.
- Compression diffusion : 720×1280, crf 26, preset slow, aac 80k mono,
  `+faststart` → ~3-5 Mo/min, qualité nickel sur téléphone.

### Flyers (acquis)
- Méthode : HTML/CSS + capture Chromium (deviceScaleFactor 2) = design premium
  (glassmorphism, dégradés) en 2160×2700. Source dans `pub/flyers/flyer1.html`.
- Polices : API Google Fonts via curl (UA navigateur) → woff2 latin locaux.
  ⚠️ Dans le CSS importé, les url() se résolvent relativement AU FICHIER CSS.
- QR code : python `qrcode` (fill #0a2550, ERROR_CORRECT_H).
- RETOURS PATRON sur les flyers : PAS d'emojis → icônes SVG dessinées (traits
  #facc15 sur badge arrondi) ; vedette orientée VERS Hoani et alignée sur la
  ligne ; logo Facebook OFFICIEL (f blanc sur #1877F2), pas l'emoji livre.
- GitHub raw (github.com/google/fonts) est bloqué par la session — passer par
  fonts.googleapis.com/css2.
- **07/08/2026 — acquis à ne plus refaire** :
  - Les polices sont maintenant **commitées** dans `pub/flyers/fonts/`
    (Montserrat 600-900 + Inter 400-700, latin & latin-ext, ~1 Mo). Plus besoin
    de les retélécharger, et `flyer1.html` se rend enfin correctement.
  - `pub/flyers/render.js` fait le rendu : `node render.js src.html out.png L H échelle`.
    Chromium est en `/opt/pw-browsers/chromium` (le chemin `.../chromium/chrome-linux/chrome`
    n'existe pas, c'est un lien direct vers le binaire).
  - `1240 × 1754` CSS × 2 = **A4 exactement à 300 dpi** (2480 × 3508) → format
    imprimable pour les hôtels, agences, affichage aux ports.
  - Mise en page en **flex column** (pas en `position:absolute` comme flyer1) :
    plus rien ne se chevauche quand un texte s'allonge.
  - Le logo officiel a été **détouré** (`logo-lockup.png`, `logo-emblem.png`).
    L'emblème seul, à 78 px, reste net ; le lockup complet (281 px de large)
    devient flou au-delà de ~200 px → à l'en-tête : emblème + « MoheliGo »
    retypographié en Montserrat 800 aux couleurs du logo.
  - Palette : utiliser les couleurs **du site** (`#1C4FA8`, `#0F2A5C`, `#F6BC1C`)
    et non celles de flyer1 (`#071c3d`, `#facc15`).
  - ⚠️ La flèche `↔` (U+2194) n'est PAS dans le sous-ensemble latin d'Inter :
    elle tombe sur une police système et jure. L'écrire en mots
    (« entre Grande Comore et Mohéli ») ou en SVG.
  - Règle que je m'impose : **aucun chiffre inventé** sur les supports
    (pas de « 10 000 passagers », pas de « 24/7 ») — uniquement du vérifiable.
  - **Nuit sans photo de nuit** : `pub/flyers/nuit.py` transforme une photo de
    jour en nuit crédible (courbes par canal R×0.30 / V×0.40 / B×0.55 en gamma,
    dégradé vers `#040A1C`, étoiles seulement au-dessus de l'horizon, lune +
    halo flouté, reflet en traits horizontaux élargissants sur l'eau).
    `random.seed(7)` → rendu reproductible. Sur fond sombre, l'emblème du logo
    doit être posé sur une **pastille blanche** (il est marine + or, invisible
    sinon) et le QR sur un **fond blanc** avec marge, sinon il ne scanne pas.

## 4. Plan marketing (validé dans l'esprit, à exécuter)

1. Lancement : publier v4 (film Amina) sur Facebook + statuts WhatsApp.
   Textes prêts dans `textes-publications.md`. Lien en 1er commentaire
   (l'algorithme FB pénalise les liens dans le post).
2. Rythme hebdo : météo mer du week-end, départ à la une, photo de l'île.
3. Preuve sociale dès les premiers clients (billet QR anonymisé + témoignage).
4. Partenariats : lodges, chauffeurs, guides tortues/baleines de Mohéli.
5. Offre de lancement : « 100 premiers comptes = priorité d'embarquement ».
6. Heures de pointe Comores : 12h-14h et 19h-22h.

## 5. Prochaines étapes possibles

- [ ] Rushes réels : le patron peut filmer (réservation au téléphone, montée
      à bord, retrouvailles à l'arrivée) → remonter le film Amina avec de
      vraies séquences.
- [ ] Déclinaisons : 30 s pour statuts, format carré 1:1 pour le feed FB,
      versions anglais / shikomori.
- [ ] Visuels fixes (affiches, bannière FB) à partir des photos + cartons.
- [ ] Page Facebook : calendrier de publication, réponses types.
- [ ] Vérifier si le patron veut brancher les pubs sur le site
      (videos.moheligo.com).

### Registre « affiche locale » (demande du patron du 07/08/2026)

Le patron veut des flyers « qui donnent envie de regarder », comme ceux de
**Yas** (ex-Telma Comores, rebaptisé en novembre 2024) et de **Royal Air**.
Ce qu'il faut retenir de ces codes :

- Yas = **jaune vif + bleu profond**, formes très arrondies, bulles, diagonales,
  prix mis en avant « À partir de X FC », accroches de trois mots, tutoiement
  (« Dis Yas ! »). Coup de chance : notre or `#F6BC1C` + marine `#0F2A5C` sont
  déjà cette paire — inutile de changer de charte.
- Compagnies locales = destination et prix énormes, numéro de téléphone très
  visible, gros bouton « Réserve maintenant ».
- Recette appliquée dans `flyer6-promo-fb.html` : photo coupée en **diagonale**
  (`clip-path`), **bulle de prix cerclée de blanc** posée à cheval sur la coupe
  (`box-shadow:0 0 0 9px #fff` — elle reste lisible sur le bleu comme sur le
  blanc), trois cartes arrondies (rayon 26 px), bandeau des ports en marine,
  bande d'action or à coins arrondis en pied, pastilles WhatsApp/Facebook.
- ⚠️ **Ne jamais reprendre le logo, la typo ou le slogan de Yas ou de Royal
  Air** : on s'inspire de l'énergie, pas de l'identité. Contrefaçon sinon.
- **Ce qui a fait passer le design d'« correct » à « bon »** (demande
  « améliore encore le design » du 07/08) — recettes réutilisables :
  1. Découpe photo → fond en **vague SVG** remplie de la couleur du fond, au
     lieu d'une diagonale droite : instantanément maritime et plus doux.
  2. **Bloc surligneur** or derrière la deuxième ligne du titre (`::before`
     tourné de −1,1°, `z-index:-1`, texte en marine) : l'œil se pose là.
  3. **Anneau de la couleur du fond** autour de la bulle de prix
     (`box-shadow:0 0 0 10px var(--paper)`) : elle reste lisible à cheval sur
     la photo et sur le fond clair.
  4. Cartes **blanches ombrées** sur fond bleuté (au lieu de cartes teintées
     sur blanc) : elles avancent au lieu de s'enfoncer. Pastilles d'icône en
     **or** avec icône marine (plus de couleur que l'inverse).
  5. **Halo doré diffus + trame d'ondes à 5,5 %** dans la zone claire : sans
     ça le fond est plat.
  6. Un **vrai bouton** (gélule marine, flèche or) plutôt qu'une ligne de
     texte « Réserve maintenant » : ça se lit comme une action.
  7. Trois niveaux d'ombre et quatre rayons **et pas plus** — le reste du
     système de design est écrit dans `pub/flyers/README.md`.
- Le texte de ce support **tutoie** (registre télécom local) alors que les trois
  autres vouvoient. À faire valider par le patron.

### Recherche d'images libres (acquis)
- 🚫 **RÈGLE DU PATRON (07/08/2026) : aucune personne sur les visuels.**
  Il a refusé l'affiche dès qu'une personne y figurait (« pas de photo qui a
  une image » = droit à l'image). Désormais : paysages, vedettes, bateaux,
  animaux — jamais quelqu'un de reconnaissable, même de dos.
- **Photo libre de Mohéli retenue** : « Îlot de Nioumachoua.jpg » (Fatima771,
  **CC BY 3.0**, 2032×1520, Commons) — plage vide, aucune personne, et CC BY
  n'impose pas le partage à l'identique (mieux que BY-SA pour de la publicité).
  Voilée à l'origine → `pub/flyers/affiche.py` la dévoile
  (`ImageOps.autocontrast(cutoff=(2,8))`, contraste 1.14, couleur 1.45, halo
  chaud sur l'horizon en `ImageChops.add`, bleu renforcé sous l'horizon,
  vignettage, UnsharpMask). Copie source dans
  `pub/photos-cc/nioumachoua-ilot-fatima.jpg`.
- ⚠️ **Nos propres photos : attention aux tailles.** Seules `mer-bateau.jpg`,
  `vedette-mer.jpg` (2560×1920) et `rochers.jpg` (1920×2560) sont grandes ;
  `horizon.jpg` et `plage-vedettes.jpg` ne font que 1080×810 → à réserver aux
  bandeaux, jamais en pleine page 2160 px. `rochers.jpg` est inutilisable en
  pub (eau boueuse, bidon rouillé, déchets).
- **Astuce mise en page** : quand la photo est trop petite pour un fond perdu
  4:5, la mettre en **bandeau** (haut de l'affiche) et poser la typo sur un
  bloc marine en dessous — elle reste nette et l'affiche gagne en structure.
- **Méthode de recherche qui marche** : l'API Wikimedia Commons
  (`generator=search` + `generator=categorymembers` sur `Category:Mohéli` et
  ses sous-catégories) donne bien plus que l'API Openverse pour Mohéli.
  Openverse est utile pour Flickr. Les deux passent par curl + `--cacert`.
- ⚠️ **Pièges relevés** : les résultats « Chissioua / M'Bouzi / Mtsamboro /
  Bandrélé » sont **Mayotte** ; « Blue Guardian Comoros » et « Vue prise à
  l'île wenefu » montrent des **personnes identifiables** → droit à l'image,
  écartées pour de la publicité. Détail dans `pub/photos-cc/CREDITS.md`.
- ⚠️ **CC BY-SA = partage à l'identique** sur l'œuvre dérivée. Pour un support
  sans aucune contrainte, viser CC BY / CC0 ou nos propres photos.
- Openverse API (`api.openverse.org/v1/images/?q=...`) et l'API Wikimedia
  Commons fonctionnent via curl + proxy. Flickr : suffixe `_b` = 1024 px.
- ⚠️ AUCUNE photo/vidéo libre du port de Hoani n'existe. « Hoani » sur Commons
  = sites maoris de Nouvelle-Zélande. « Moheli d (21).jpg » = une policière (piège).
- Toujours archiver les crédits (CC BY / BY-SA) dans `pub/photos-cc/CREDITS.md`
  et les afficher sur l'écran final.
- ⚠️ RETENU DU PATRON : le départ des vedettes est **OUROVENI** (pas Chindini) ;
  pas de « Embarquez » à la fin — sobre : « MoheliGo point com ».
- Carte touristique satellite filmable : Chromium ne sort PAS par le proxy
  (ERR_CONNECTION_RESET) → intercepter unpkg/maptiler/arcgis avec ctx.route et
  fulfill via curl (execFileSync + cache). Précharger 14 s + pan aller-retour
  avant la fenêtre filmée, sinon tuiles blanches (le patron l'a repéré).

## 5 bis. Projet personnel du patron, HORS MoheliGo

Le 03/08/2026 il a demandé une messagerie privée pour son couple et sa
famille. Elle est **volontairement séparée** : dossier `nous/` à la racine
du dépôt, sa propre base de données, sa propre adresse. Consigne explicite
du patron : **« ne touche à rien à MoheliGo, faut pas abîmer l'appli »**.
Donc : aucun partage de code, d'adresse, de projet Supabase ni de service
worker avec MoheliGo. Tout est expliqué dans `nous/README.md` — ne pas
recharger ce sujet ici, ce n'est pas du marketing.

## 6. Journal des sessions

- **09/08/2026 (suite)** — « Écris un autre texte pour la pub style grand
  conglomérat, réessaie. » Deuxième tentative, nettement plus tenue que celle du
  07/08 : « ENTRE DEUX ÎLES, IL Y A UN SERVICE » — phrases courtes, aucune liste
  de fonctionnalités, aucun hashtag, aucun appel à l'action, et une chute qui
  assume la position (« C'est le travail d'une infrastructure : retirer
  l'incertitude, puis se faire oublier »). Plus une version en trois lignes.
  **Ce que ce registre coûte, à dire au patron** : sans hashtags ni appel à
  l'action, on gagne en autorité et on perd en clics. À réserver aux
  publications d'image ; garder le registre promo pour faire réserver le soir.
  Les deux textes sont dans `page.py` (liste `TEXTES`) et dans
  `pub/textes-publications.md`.

- **09/08/2026** — « Dépasse-toi encore, ça doit être lumineux. » L'affiche a
  été refaite en version claire : rampe duotone qui ne descend jamais dans le
  noir, **voile clair sur les bords au lieu d'un vignettage sombre** (le geste
  qui change tout), bloom généreux, et le **sceau devenu soleil** avec un
  éventail de rayons en dégradé conique. La typo passe en **marine sur fond
  clair** — la lumière vient du contraste, pas de l'ajout de blanc.
  ⚠️ Premier essai trop délavé : les îlots avaient disparu. Réglages retenus :
  voile 140, contraste 1,22, gamma 0,88. Recette complète dans
  `pub/flyers/README.md`, section « Faire une affiche LUMINEUSE ».
  La page du patron montre maintenant cette affiche à la place de la sombre
  (la sombre reste dans le dépôt).
  Retour immédiat : **« trop lumineux »**. Réglage final : voile de bord 74 au
  lieu de 140, contraste 1,30, gamma 0,96, ombres de la rampe plus profondes,
  et voile crème du bas remonté pour garder le texte marine lisible sur le
  sable. **À retenir : « lumineux » ne veut pas dire « pâle » — la lumière tient
  à la présence des ombres autant qu'à celle des hautes lumières.**
  Ajouté le même jour, sur sa demande : **trois textes seuls** (faire s'abonner
  à la page, faire utiliser l'application, variante courte de l'affiche), dans
  `page.py` (liste `TEXTES`) et dans `pub/textes-publications.md`.
  ⚠️ Le texte d'abonnement promet un bulletin **chaque soir** : soit on tient le
  rythme, soit on retire la phrase.
  Dernier retour du jour : **« la mer doit être vraie »**. Le duotone, aussi beau
  qu'il soit, recolore la mer — le patron n'en veut pas sur l'affiche. Version
  définitive : `flyer12-affiche-vraie-fb.html`, photo en **couleurs réelles**
  (`affiche.py → plein_cadre()` : recadrage, netteté, grain, rien d'autre), même
  mise en page, et une **bande de papier crème en pied** pour que l'adresse et le
  QR restent lisibles sur le sable orange. **Règle à garder : le duotone pour un
  visuel graphique, jamais quand la vérité de la scène compte.**

- **08/08/2026 (soir)** — « Dépasse-toi, va chercher sur internet comment faire
  un flyer très joli. » Recherche faite (tendances graphiques 2026 + principes
  de l'affiche de voyage), quatre enseignements retenus et appliqués :
  **duotone deux couleurs** (marine + or = le registre « sophistiqué », et
  c'est notre charte), **une seule idée** au lieu d'une fiche produit,
  **composition en tiers** sans rien de centré, **grain** pour enlever le côté
  ordinateur. Résultat : `flyer10-affiche-duotone-fb.html` — nom de l'île en
  218 px sur une mer marine, ciel doré, anneau de soleil fin. **C'est le plus
  beau visuel produit à ce jour, et le moins chargé.** Leçon de fond : jusque-là
  j'ajoutais des éléments pour faire riche (bulles, pastilles, cartes) ; ce qui
  fait beau, c'est d'en enlever.
  Bonus technique : le grain masque l'agrandissement d'une photo un peu petite —
  utile avec nos sources en 2032 px de large.
  **Idée du patron, retenue** : mettre le logo dans le cercle du milieu. L'anneau
  de soleil est devenu un **sceau** contenant l'emblème du navire en silhouette
  marine — c'est la signature de l'affiche, et le logo est enfin grand. ⚠️ Au
  passage : `logo-emblem.png` a un **fond blanc opaque** ; pour en faire une
  silhouette il faut passer par la luminance (fichiers `logo-emblem-marine.png`
  et `logo-emblem-creme.png`, à réutiliser). Et l'emblème ne doit figurer
  **qu'une fois** par visuel : il a été retiré de l'en-tête.

- **08/08/2026** — Le patron ne voyait pas les fichiers envoyés dans la
  conversation (« je trouve pas le flyer », deux fois) et disait le projet
  fatigant. ⚠️ **LEÇON À RETENIR : chez lui, les pièces jointes ne s'affichent
  pas. Le canal qui marche, c'est une PAGE WEB publiée** (artifact) avec les
  flyers en grand et le texte à copier :
  `https://claude.ai/code/artifact/d08c3def-2c4b-418a-b7bd-b19c477df307`
  — republier le même fichier garde la même adresse, donc il n'a qu'un seul
  lien à retenir. Deuxième leçon : **je lui ai sorti huit versions et noyé sous
  les liens GitHub**. Quand il est fatigué : une page, deux flyers, rien à
  décider.
  Produit ce jour-là : le bulletin du soir remis à jour (dimanche 9 août, mer
  peu agitée) et un **nouveau flyer pub « diaspora »** — « Tu paies ici. Il
  embarque. » : payer la traversée d'un proche depuis la France, Mayotte ou le
  Golfe. C'est l'angle le plus rentable qui restait, et il n'existait qu'en
  encart dans le flyer nuit.

- **08/08/2026, 18h40 (Comores)** — La session a franchi minuit : attention, le
  flyer du soir généré la veille annonçait « samedi 8 » et était donc périmé.
  Regénéré pour **dimanche 9 août** (mer peu agitée, houle 1,0 m, vent 9 km/h
  sud-est, matin dégagé, pluie fine l'après-midi).
  **Leçon de livraison, la plus importante de la session** : le patron ne
  voyait pas les fichiers envoyés dans la conversation (« je trouve pas »,
  « toujours pas »), et les liens GitHub ne lui parlent pas. Ce qui marche :
  une **page web publiée** (artifact) avec les flyers en grand, un appui long
  pour enregistrer, le texte du post et un bouton copier. L'adresse reste la
  même quand on republie — la lui redonner au lieu d'en créer une nouvelle :
  https://claude.ai/code/artifact/d08c3def-2c4b-418a-b7bd-b19c477df307
  ⚠️ Il a dit aussi : « le projet me fatigue mentalement ». Ne plus empiler les
  versions ni les étapes à faire de son côté : **une page, deux flyers, rien à
  décider.** Le tuyau automatique, la fusion dans main et la publication
  Facebook attendent qu'il les redemande.

- **07/08/2026 (fin de journée)** — Demande : « un flyer pour cette aprem ou ce
  soir, avec une amélioration très avancée ». Créé **le bulletin du soir** :
  un flyer qui affiche **la vraie mer de demain matin** sur le couloir
  Ouroveni–Hoani, tiré d'Open-Meteo (API marine + vent), avec jauge d'état de
  la mer (échelle de Douglas), courbe de houle heure par heure, panneau en
  verre dépoli, et photo étalonnée fin de journée. Tout est **généré** :
  `bulletin.py` remplit un gabarit, donc le flyer se refait en une commande.
  → C'est le format à installer en **rituel quotidien** (publication 16h-19h).
  Personne d'autre aux Comores ne publie l'état de la mer du lendemain :
  c'est ce qui transformera la page Facebook en service que les gens
  consultent, pas en page de pub qu'on ignore.
  ⚠️ Garde-fous : regénérer chaque jour, garder la source, rappeler que le
  bulletin officiel fait foi, et **publier aussi quand la mer est mauvaise**.
  **Le tuyau est construit** : `.github/workflows/bulletin-du-soir.yml` refait
  le flyer chaque jour à 16h (heure des Comores) sur un serveur GitHub et le
  dépose sur la branche `bulletin-du-jour` (branche réécrite à chaque fois, donc
  le dépôt ne grossit pas). Adresses fixes pour le patron :
  `.../blob/bulletin-du-jour/flyer-soir-facebook.png` et `.../texte-du-jour.txt`.
  ⚠️ **Une tâche planifiée ne tourne que depuis la branche par défaut** : tant
  que le workflow n'est pas fusionné dans `main`, seul le bouton « Run workflow »
  marche. À faire valider par le patron (c'est lui qui fusionne).
  Dernière marche possible, si le patron la veut : **publier directement sur la
  page Facebook** via l'API Graph (il faut une app Meta, un jeton de page longue
  durée mis en secret GitHub, et accepter que ça poste sans relecture).

- **07/08/2026 (fin de session)** — Le patron valide : « c'est super le design,
  la prochaine fois on va encore améliorer ». Design du flyer promo retravaillé
  (vague SVG, bloc surligneur, bulle cerclée, cartes blanches ombrées, halo +
  trame, vrai bouton, photo agrandie) et décliné en **A4 300 dpi imprimable**
  avec la bande « comment ça marche ». Il m'a demandé d'inscrire dans cette
  mémoire **où sont les fichiers** → section 2 bis. Reprendre là la prochaine
  fois, à partir de `pub/flyers/flyer6-promo-fb.html`.

- **07/08/2026** — Le patron demande « un flyer type grand conglomérat + un
  écrit pour publier sur FB ». Produit : flyer institutionnel A4 300 dpi
  (en-tête, bandeau photo, schéma du réseau des 4 ports, 6 services numérotés,
  bande de chiffres clés, pied avec QR + WhatsApp + Facebook) et sa déclinaison
  feed 4:5. Registre corporate assumé : filet institutionnel, sections
  numérotées 01/02, aucun emoji, couleurs officielles du site. Texte Facebook
  ajouté dans `pub/textes-publications.md` (version institutionnelle + premier
  commentaire avec le lien + version courte + réponses types aux commentaires).
  Documentation dans `pub/flyers/README.md`. **À faire à la prochaine session :
  demander au patron s'il valide le ton institutionnel ou s'il veut plus chaud
  / plus commercial, et s'il veut une version shikomori.**
  Il a ensuite demandé **un deuxième support pour plus tard dans la nuit** :
  produit le flyer nuit (ciel étoilé, lune, silhouette des îles) avec un angle
  action — « Réservez ce soir. Partez demain. » — et un encart diaspora
  (France, Mayotte, Golfe : payer la traversée d'un proche). Texte FB nuit dans
  `pub/textes-publications.md`. **Leçon de calendrier : ne pas republier la même
  vitrine deux fois dans la soirée — deux posts = deux angles.**
  Puis il a demandé un troisième support avec **une belle image de Mohéli
  trouvée sur le net** : affiche « destination ». Première tentative refusée
  (une personne à l'image) → refaite avec une photo libre de plage vide
  (Fatima771, CC BY 3.0) + une variante avec notre vedette en pleine mer.
  Trois angles disponibles pour la page : institutionnel (vitrine) → nuit
  (action) → destination (émotion). Enfin il a demandé des flyers « comme Yas
  et Royal Air, qui donnent envie de regarder » → flyer promo (voir la section
  « Registre affiche locale »). C'est probablement celui-là qui marchera le
  mieux sur Facebook aux Comores : prix visible, formes rondes, tutoiement.
- **03/08/2026** — Hors marketing : création de « Nous », la messagerie
  privée couple + famille (voir 5 bis). Sortie de `moheligo/` à la demande
  du patron, base de données à elle, aucune dépendance à MoheliGo.
  Testée à deux téléphones (Playwright) : envoi/réception chiffrés, photo,
  effacement des deux côtés, message programmé livré à l'heure, statut
  « occupé » transmis. **Rien à faire côté MoheliGo.**
- **02/08/2026 (suite)** — v5 « Destination Mohéli » : recherche d'images CC
  (pas de photo libre de Hoani → utilisé satellite, tortues, dauphin, corail,
  plages CC + nos photos), montage 48 s, crédits en règle.
- **02/08/2026** — Session fondatrice. Récupéré le site depuis moheligo.com
  (le code n'était sur aucun dépôt) → sauvegardé dans `moheligo/`. Produit
  4 pubs vidéo + textes de publication. Itérations selon retours patron
  (voix, bruit, poids). Nommé Directeur Marketing. Créé cette mémoire.
