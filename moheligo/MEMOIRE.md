# 📚 MÉMOIRE — Directeur Marketing MoheliGo (Claude)

> 📕 **AVANT TOUTE PRODUCTION — lire `MANUEL-MARKETING.md`.** C'est la grille
> de décision (Sharp, Cialdini, Ogilvy, Ries & Trout, vente aux gens qui n'ont
> jamais acheté en ligne) et elle finit par des **checklists à passer** avant de
> livrer un flyer, un texte, un rapport ou un plan. Exigé par le patron le
> 11/08/2026.
>
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

📌 **Le plan publicitaire complet est dans `pub/plan-publicitaire.md`**
(écrit le 11/08/2026 à la demande du patron : « décris un plan publicitaire pour
avoir plus d'utilisateurs »). Trois étages — organique (rythme quotidien),
terrain (affiches aux ports, commandants, lodges), payant (diaspora d'abord) —
plus trois paliers de budget et cinq chiffres à suivre. La liste ci-dessous en
est le résumé historique.

⚠️ Cinq réponses attendues du patron pour exécuter : la **marge par
réservation** (sans elle, aucune publicité n'est jugeable), une **carte pour
payer Meta** (MVola ne paie pas Facebook), le budget d'impression, trois
témoignages de vrais clients, et le registre tu/vous.

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

- **11/08/2026 (« TROP BASIC » — la leçon la plus utile de la journée)** — Carte
  blanche donnée : « fais-moi un flyer, ne suis pas mes indications ». J'ai rendu
  `flyer19-chiffre-fb.html` : aplat marine, un seul fait géant (la mer à 0,9 m),
  zéro décor — l'application littérale de la **sortie B** de mon § 10 bis.
  Verdict : **« c'est trop basic, mais explique-moi ce choix. »**
  🎓 **Ce que j'avais mal compris, écrit dans le manuel au § 10 ter : sobre ≠
  vide.** Enlever le décor n'est que la moitié du travail ; il faut ensuite
  travailler ce qui reste. Les cinq points de contrôle pour un visuel sans photo :
  ① un **objet** justifié par le sujet (pas un décor) ; ② un vrai contraste de
  matière (marine profond / carte claire) ; ③ de la **densité** — six secondes de
  lecture, pas une ; ④ du détail typographique (`tabular-nums`, filets fins,
  trois niveaux de hiérarchie) ; ⑤ **aucune zone morte** : un grand vide non
  encadré se lit comme un oubli, jamais comme du calme.
  ➡️ Nouveau modèle de référence pour tout visuel **sans image fournie** :
  `pub/flyers/flyer20-prix-fb.html` → `flyer-prix-facebook.png`. Sujet : **les
  prix** (mercredi du calendrier). L'objet, c'est un **billet** (carte claire,
  encoches taillées dans le marine, ligne de perforation) — un dispositif qui a
  un sens puisqu'on parle du prix d'un billet. **Sans date → réutilisable tous
  les mercredis.** Branché dans `calendrier.py` (variante mercredi) et ajouté à
  `page.py`.
  ⚠️ Tous les chiffres sont **vérifiés dans le code du site**, aucun inventé :
  ~14 500 FC adulte + prix exact affiché en direct (`index.html`, FAQ) ; enfant
  −30 à −50 %, place bloquée 15 min, changement de date gratuit, remboursement
  intégral moins les frais, 10 traversées = un bon (`moheli-savoir.js`) ;
  1 € = 492 FC. **Avant chaque visuel « prix », relire ces deux fichiers** — un
  tarif faux sur une affiche, c'est une promesse qu'on ne tient pas.
  🔓 **Le seul verrou qui reste sur les visuels promo : les images du patron.**

- **11/08/2026 (LA LIAISON FACEBOOK MARCHE)** — 🎉 **Premier bulletin publié
  automatiquement sur la page** (mercredi 12 août, mer peu agitée), et jeton
  durable posé. `PUBLIER_FB = oui` : à partir du 12/08, **bulletin à 19h30 et
  publication du jour à 12h30, sans intervention**.
  **LA RECETTE QUI MARCHE, à ne plus jamais chercher :**
  1. app dédiée avec le cas d'utilisation **« Tout gérer sur votre Page »**
     (les cas d'utilisation ne se mélangent pas : une app « publicité » n'offre
     jamais `pages_manage_posts`) ;
  2. explorateur → **Utilisateur actuel** → quatre permissions :
     `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`,
     **`pages_manage_engagement`** (celle-ci pour COMMENTER — permission
     différente de celle qui publie) ;
  3. débogueur → **« Étendre le token d'accès »** → 60 jours ;
  4. coller ce jeton **utilisateur** dans le secret : `jeton_de_page()` en dérive
     tout seul le jeton de page, qui ne périme plus.
  **LES SIX PIÈGES DE LA JOURNÉE** (quatre étaient de mon fait) :
  ① un seul champ invalide fait rejeter TOUT l'appel Graph ; ② un jeton
  d'utilisateur peut LIRE une page mais pas y PUBLIER ; ③ Chrome copie parfois
  l'adresse encodée → « Bad signature » ; ④ stdout tamponné plaçait les erreurs
  au mauvais endroit du journal (`PYTHONUNBUFFERED`) ; ⑤ commenter demande une
  autre permission que publier — et son refus faisait échouer une publication
  déjà réussie ; ⑥ une étape sautée laisse le voyant vert.
  **Reste à faire** : refaire le jeton avant le 10/10/2026 (60 jours), et
  fournir les images pour les visuels promo (les miens font « débutant »).

- **11/08/2026 (les trois modèles)** — « Montre les flyers d'Apple et
  Coca-Cola pour trancher le modèle. » Recherche faite, et **trois registres
  coexistent désormais dans le dépôt** :
  ① **Yas / affiche locale** (`flyer7-promo-brillant`) — prix énorme, bouton,
  urgence : **fait réserver** ;
  ② **Apple / institutionnel** (`flyer15-conglomerat`) — une phrase, du vide,
  logo petit, aucun prix : **fait respecter** ;
  ③ **Coca-Cola** (`flyer16-couleur`) — **une couleur possède tout le cadre**,
  un ruban (notre vague = leur « dynamic ribbon »), une phrase d'émotion et
  aucun argument : **fait aimer**.
  **Recommandation donnée : ne pas choisir, doser.** Un institutionnel par
  semaine (le dimanche, déjà prévu au calendrier), du concret le reste du temps.
  ⚠️ Argument à réutiliser : **Apple peut se permettre le vide parce que tout le
  monde connaît Apple** ; MoheliGo construit encore sa notoriété — ne publier
  que du conglomérat, c'est être élégant et inconnu.
  ⚠️ Leçon de mise en page : **le vide doit ENTOURER le texte**. Accumulé en bas,
  il se lit comme un oubli, pas comme du calme.
  🚫 **Consigne du 11/08 au soir : NE RIEN PUBLIER SUR FACEBOOK** jusqu'à nouvel
  ordre. La liaison reste inachevée : le jeton d'utilisateur système n'a ni
  `pages_read_engagement` ni `pages_manage_posts` (essai d'écriture refusé, donc
  **rien n'a jamais atteint la page**). Reprendre par : générer le jeton système
  en cochant les trois permissions, et vérifier que la page est bien attribuée à
  `moheligobot` avec « Gérer la Page ».
  ⚠️ Piège Meta découvert : **les cas d'utilisation d'une app ne se mélangent
  pas**. La première app (`MoheliGo`, 1055072317068064) était partie sur la
  publicité et n'offrait donc jamais `pages_manage_posts`. Il a fallu créer une
  seconde app (`Moheligo publicite`, 4081944208770808) avec le cas
  **« Tout gérer sur votre Page »**. Et `manage_ads` ≠ `manage_posts` : un mot
  d'écart, une heure perdue.

- **11/08/2026 (personnages)** — Le patron a montré une affiche **Royal Air**
  (fond dégradé profond, objets qui flottent, arche pointillée, barre sociale en
  pied) et demandé la même énergie. Résultat : `flyer13-aerien-fb.html` →
  `flyer-aerien-facebook.png`, avec un **hublot** (notre vedette) et un billet QR
  à la place de l'humain.
  Il a ensuite assoupli sa règle : **« si tu peux générer des personnes ça va,
  mais jamais des personnes réelles »**. Or **aucun outil de génération d'images
  n'est disponible dans cette session** : j'ai donc dessiné un voyageur en SVG à
  plat (`flyer14-personnage-fb.html`, conservé comme gabarit).
  🚫 **Verdict du patron : « ça fait débutant ».** Le personnage a été retiré de
  la page. **RÈGLE À TENIR : pas de personnage dessiné à la main.** Un dessin
  vectoriel se voit toujours à côté d'un rendu 3D ou d'une photo. Le patron
  **fournira lui-même des images générées** ; d'ici là, **aucune personne sur
  les visuels**, on reste sur les objets, la mer et la typographie.

- **11/08/2026 (liaison Facebook, diagnostic)** — 🚨 **Le numéro donné par le
  patron (1055072317068064) n'est PAS une Page** : la requête ne renvoie que
  `name` et `link`, **jamais `category`** — or `category` n'existe que sur une
  Page. C'est donc un **compte** qui porte le nom « MoheliGo ». Question posée au
  patron : `me/accounts?fields=name,id,access_token` renvoie-t-il une ligne
  MoheliGo, ou une liste vide ?
  - Si une ligne existe → prendre **son** `id` et **son** `access_token`.
  - Si la liste est vide → **MoheliGo est un profil, pas une Page**, et
    **aucune API ne peut publier sur un profil personnel**. Il faudra créer une
    vraie Page (ce qui apporte en plus : statistiques, publicité payante,
    plusieurs administrateurs, pas de plafond d'amis).
  ⚠️ Leçons de la mise au point, à ne pas repayer : ① **Facebook rejette la
  requête entière dès qu'un seul champ demandé est invalide** — demander
  `followers_count` faisait échouer `name` et `category` avec ; les champs
  facultatifs vont dans un appel séparé tolérant (`curl(..., strict=False)`).
  ② `metadata=1` n'est pas toujours renvoyé : un test qui ne répond pas ne
  prouve rien. ③ Une étape de workflow **sautée laisse le voyant vert** — d'où
  l'étape qui annonce l'état réel de la liaison.
  ⚠️ Le patron a collé un jeton dans la conversation. Règle rappelée et écrite :
  **une clé se colle dans un champ masqué, jamais dans une phrase.**

- **11/08/2026 (fin de journée)** — « Pourquoi le bulletin du soir seulement ?
  c'est toi le directeur marketing et commercial, tu vas tout gérer les pubs. »
  Il a raison, et je m'étais arrêté trop tôt. **Toute la semaine est désormais
  automatisée** : `calendrier.py` (lundi comment ça marche, mardi l'île,
  mercredi les prix, jeudi s'abonner, vendredi la diaspora, samedi la
  destination, dimanche l'institutionnel) + `programme.py` + le workflow
  `publication-du-jour.yml` à **12h30**. Le bulletin passe de 16h à **19h30**.
  Deux publications par jour, aux deux heures de pointe.
  - `calendrier.py` **tire ses visuels et ses textes de `page.py`** : une seule
    source de vérité, rien n'est recopié. Chaque jour a plusieurs variantes,
    choisies selon le numéro de semaine ISO, **contre l'usure** — sept
    publications par semaine tirées de quatre visuels se voient au bout de
    quinze jours. Il faut continuer à produire des visuels neufs.
  - Nouveau **frein d'urgence** : variable de dépôt `PAUSE_FB = oui` → plus rien
    ne part. Vérifié dans les scripts, pas seulement dans les workflows. À
    utiliser sans hésiter s'il arrive quelque chose en mer : une pub joyeuse le
    jour d'un accident ne se rattrape pas.
  - 🚨 **DEUX BOGUES QUI AURAIENT TUÉ LA PROMESSE, trouvés en lançant le
    workflow pour de vrai** : ① les scripts passaient `--cacert` vers le
    certificat du proxy de session, absent sur GitHub (curl erreur 77) — et ma
    première correction, `Path.exists()`, levait `PermissionError` parce que
    `/root` n'est pas lisible chez GitHub ; la bonne forme est
    `os.path.isfile()`. ② **Facebook refuse les photos de plus de ~4 Mo** et nos
    flyers pèsent 4 à 6,5 Mo : toutes les publications auraient été rejetées.
    `publier_fb.preparer()` repasse en JPEG 92 au-delà de 3,5 Mo.
    **Leçon : un workflow qu'on n'a jamais lancé est un workflow qui ne marche
    pas.** Le tuyau a échoué trois fois avant de déposer son premier bulletin
    (branche `bulletin-du-jour`, 11/08 à 13h22 heure des Comores).
  - La branche a été **fusionnée dans `main`** avec l'accord explicite du patron
    (sans quoi GitHub n'affiche pas « Run workflow » et n'applique pas
    l'horaire : une tâche planifiée ne tourne que depuis la branche par défaut).
  - Reste à faire de son côté : ranger `FB_PAGE_TOKEN` (secret) et `FB_PAGE_ID`
    (variable), essayer à blanc, puis créer `PUBLIER_FB = oui`. Et **refaire un
    jeton durable** : celui de l'explorateur expire en une à deux heures.

- **11/08/2026 (soir)** — « Montre comment lier la page FB à toi. » Il n'existe
  **aucun connecteur Facebook dans Claude** : la liaison durable passe par
  GitHub. Construit : `pub/flyers/publier_fb.py` (Graph API, publie l'image +
  le texte + le lien en premier commentaire) et
  **`pub/flyers/LIER-FACEBOOK.md`** (marche à suivre complète pour le patron).
  Le workflow du bulletin a deux nouvelles étapes, **désarmées par défaut** :
  rien n'est publié tant que la variable de dépôt `PUBLIER_FB` ne vaut pas
  « oui ». Sécurité : le jeton n'est jamais dans argv (passé à curl par son
  entrée standard, en-tête `Authorization`), et **jamais demandé dans la
  conversation** — un jeton collé dans un message est un jeton à refaire.
  🚨 **LE VRAI RISQUE DU PROJET, révélé ce jour-là** : le patron **n'a plus le
  numéro de téléphone avec lequel il ouvre la page Facebook** (il a seulement
  celui du compte). Tant que la session reste ouverte sur son téléphone, tout
  est récupérable ; s'il se déconnecte, **la page et ses abonnés sont perdus**.
  Priorité absolue, avant tout travail marketing : ajouter le numéro actuel et
  un e-mail dans le Centre de comptes, double authentification **par
  application et pas par SMS**, codes de secours conservés ailleurs, et
  **un second administrateur sur la page**. À reposer à chaque session tant que
  ce n'est pas fait.

- **11/08/2026 (suite)** — « Décris un plan publicitaire pour avoir plus
  d'utilisateurs. » Écrit dans `pub/plan-publicitaire.md`. La thèse du plan :
  **on a déjà tout le matériel (5 vidéos, 10 flyers), ce qui manque c'est du
  rythme, du terrain et une mesure.** Trois idées à retenir :
  ① le **bulletin mer quotidien** est notre seul actif que personne d'autre n'a —
  il transforme la page en service, et on s'abonne à un service, pas à une
  vitrine ; ② aux Comores l'**affiche au port** bat le ciblage publicitaire,
  parce qu'elle est là au moment où la personne pense au voyage ; ③ la
  **diaspora** est la seule cible qui paie en euros, donc la première à cibler
  en payant. Recommandation budget : palier 1 (~25 000 FC/mois) pendant un mois,
  et on ne monte que si le coût par réservation le justifie.

- **11/08/2026** — « C'est toi le directeur marketing, fais aussi la météo de
  demain. » Bulletin régénéré pour **mercredi 12 août** (mer peu agitée, houle
  0,93 m, vent 17 km/h de sud-est, période 9,0 s) et bloc « météo de demain »
  de la page rafraîchi (matin dégagé 22→27 °C, **pluie fine l'après-midi,
  57 % vers 15h**, soir dégagé 24-25 °C).
  ⚠️ **Amélioration à garder** : la houle était si régulière (0,92 → 0,94 m) que
  l'arrondi au décimètre affichait « 0,9–0,9 m » et « de 0,9 m à 0,9 m » — ça
  ressemblait à un bug alors que c'est une bonne nouvelle. `bulletin.py` détecte
  maintenant ce cas et écrit **« 0,9 m · HOULE RÉGULIÈRE 5H-13H »** et
  « régulière, autour de 0,9 m ». Le gabarit n'a plus `{{HMIN}}/{{HMAX}}` mais
  `{{AMPLI}}` et `{{AMPLI_LAB}}`.
  Leçon de fond : **un chiffre juste peut quand même mal se lire ; nommer la
  situation vaut mieux que répéter le nombre.**

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
