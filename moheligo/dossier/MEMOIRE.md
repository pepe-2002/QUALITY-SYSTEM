# 📚 MÉMOIRE — Directeur Marketing MoheliGo (Claude)

> 📕 **AVANT TOUTE PRODUCTION — lire `MANUEL-MARKETING.md`.** C'est la grille
> de décision, en deux parties :
> **PARTIE I (§ 1-11)** marketing, écriture, vente aux gens qui n'ont jamais
> acheté en ligne, et mes interdits — à relire avant un flyer ou un texte ;
> **PARTIE II (§ 12-16)** diriger (les postes et le chiffre dont chacun répond),
> faire adopter un produit à qui n'en a pas envie (B = MAP, leçon M-Pesa), les
> erreurs des fondateurs de la Silicon Valley — à relire avant un plan, un
> recrutement ou une décision produit. Chaque partie finit par des **checklists
> à passer**. Exigé par le patron le 11/08/2026, enrichi le même soir.
> 📖 Copie lisible pour le patron : `python3 pub/flyers/manuel_page.py --sortie
> /tmp/manuel.html` — **générée depuis le manuel, jamais recopiée à la main**.
> 🗺️ **`FEUILLE-DE-ROUTE.md`** — les quatre étapes avec leurs seuils de décision,
> et les risques. À relire avant de promettre un délai au patron.
> ⚖️ **Répartition des postes et règle A / B / C : manuel § 12.2 à 12.2 ter.**
> En cas de doute entre « je décide » et « je propose », **je propose**.
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

Textes des publications Facebook : `moheligo/dossier/TEXTES-PUBLICATIONS.md`
(une section par flyer, avec le premier commentaire et la version WhatsApp).

➡️ **PROCHAINE SESSION** : repartir de **`flyer7-promo-brillant-fb.html`**
(version la plus aboutie, passe « brillance » appliquée), jamais de zéro. La
recette complète de la brillance est écrite dans `dossier/ATELIER-FLYERS.md`,
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

📌 **Le plan publicitaire complet est dans `dossier/PLAN-PUBLICITAIRE.md`**
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
     système de design est écrit dans `dossier/ATELIER-FLYERS.md`.
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

- **26/08/2026 (🎬 LA VIDÉO DU YOUNG LEADER EST ARRIVÉE)** — le patron envoie
  « la pub faite par le Young Leader ». **Analysée image par image** (1 575
  images extraites, sous-titres relevés en entier) → **`VIDEO-YOUNG-LEADER-RECUE.md`**.
  ✅ **Ce qui est réussi** : **il a repris NOTRE phrase** (« c'est la mer qui
  décide, nous on te le dit avant ») — **le brief est arrivé jusqu'à lui**, notre
  signature sort de la bouche de quelqu'un d'autre que nous. Vrai visage
  mohélien en écharpe officielle, format **vertical ✅**, **sous-titres
  incrustés ✅**, décor réel, notre logo bien dessiné sur la moitié du film.
  🔴 **Ce qui empêche de publier tel quel** : **(1) aucun appel à l'action** — la
  vidéo dit « cliquez sur le lien » et **ne montre jamais `moheligo.com`** ;
  l'écran final est noir 5,5 s avec un texte illisible. **La dernière image est
  celle qui convertit, ici elle ne convertit rien.** **(2)** le nom MoheliGo
  n'arrive qu'à la **25ᵉ seconde** (les 3 premières sont le logo d'un autre
  organisme). **(3) cinq fautes de français incrustées** (proposez/entre…vers/
  rendiez/abonnez/sur lien) — et **notre cible est la diaspora, qui les verra**.
  **(4)** notre nom écrit **deux fois différemment** dans le même film
  (« Moheligo » puis « MoheliGo ») — c'est **`MoheliGo`, G majuscule, toujours**.
  **(5)** un seul plan fixe de 50 s : **on ne voit jamais la mer, la vedette, ni
  l'application**. **(6)** 576×1024 = **compression WhatsApp, redemander
  l'original**. **(7)** 52,5 s au lieu des 30 s du brief.
  🛠️ **Presque tout se répare au montage**, de notre côté : refaire les
  sous-titres, couper à 30 s, poser notre logo dès la 1ʳᵉ seconde, **remplacer la
  carte finale** par la signature exacte + `moheligo.com`.
  📌 **Ton à tenir** : ce qu'il a donné — sa figure, son écharpe, notre phrase
  dans sa bouche — **on ne pouvait pas le produire seuls**. Le reste est de la
  technique, **et la technique est notre métier, pas le sien**. On lui demande
  **une seule chose** : le fichier d'origine.
  🔴 **La phrase de droits à l'image n'est toujours pas obtenue par écrit** —
  à demander **avant** publication.
  ⚠️ **Le rendez-vous du mardi 25/08 n'a pas eu lieu** : les trois livraisons
  (chiffres, conversation avec le commandant, départs dans les écrans) sont
  toujours attendues. Le flyer des prix reste hors rotation, rien n'est écrit sur
  les tarifs.

- ## ⏰ 23/08/2026 — RENDEZ-VOUS PRIS POUR LE **MARDI 25/08/2026**
  **À LIRE EN PREMIER EN DÉBUT DE SESSION.** Le patron : « je te donne les
  chiffres le mardi, et la conversation, et les améliorations sur mettre voir les
  départs dans les endroits où on consulte le plus ». **Trois livraisons
  attendues** — ne rien décider sur le prix avant de les avoir.

  | # | Ce qu'il apporte | Ce que j'en fais |
  |---|---|---|
  | **1** | **les chiffres** (écrans 7 j + depuis le lancement, traversées payées, abonnés) | comparer semaine à semaine — c'est la 1ʳᵉ fois qu'on aura deux points |
  | **2** | **la conversation avec le commandant** | le prix affiché qu'il accepte → alors seulement on touche au tarif |
  | **3** | **les départs là où on consulte le plus** | son idée, et c'est la bonne : voir le plan chiffré ci-dessous |

  ❓ **Les deux questions à lui reposer en même temps** :
  · **« Accueil » (90) compte quoi** — des ouvertures distinctes, ou seulement les
    retours à l'accueil ? Sans ça, le taux réel de la première marche est
    incalculable (question ouverte depuis le 18/08).
  · **Le commandant vend-il en direct à 12 500, ou descend-il à 10 000 ?** Tout le
    calcul de commission repose sur son plancher réel.

- **23/08/2026 (🎯 SON IDÉE : LES DÉPARTS LÀ OÙ ON REGARDE — et elle vise juste)** —
  le patron propose de **montrer les départs dans les écrans les plus consultés**.
  📌 **C'est exactement le chantier n°1 identifié le 18/08**, et il y arrive par
  lui-même en regardant ses chiffres. Rappel de l'entonnoir : **140 ouvertures →
  16 sur Traversées (11 %)**. Neuf personnes sur dix ouvrent l'application et **ne
  voient jamais un départ**.
  🚨 **Le plan, classé par le trafic réel (7 jours)** :

  | Écran | vues | Ce qu'on y met | Pourquoi lui |
  |---|---|---|---|
  | **Accueil** | **41** | **le prochain départ en haut**, date + heure + bouton Réserver | **2,5× plus vu que Traversées**. Le départ doit aller au client, pas l'inverse |
  | **Météo mer** | **21** | sous le bulletin : « mer calme mardi → prochain départ » + bouton | **plus consulté que les Traversées elles-mêmes** ; qui regarde la mer est en train de décider s'il part |
  | **Découvrir** | 15 | en bas : « y aller : prochain départ le… » | il rêve de Mohéli — on lui donne la marche suivante |
  | **Messagerie** | 11 | message d'accueil automatique avec le prochain départ | il nous parle déjà, c'est le plus chaud |

  💡 **L'arithmétique qui rend ça prioritaire** : si **Accueil (41)** et **Météo
  (21)** envoyaient seulement **un tiers** de leurs visiteurs vers un départ, ça
  ferait **+20 vues** sur les 16 actuelles. ➡️ **On passerait de 11 % à ~26 % —
  plus du double — SANS UN SEUL VISITEUR DE PLUS.** Aucune publicité ne donne ce
  rendement.
  ⚠️ **Et ça répare le revers signalé le 18/08** : la Météo est plus consultée que
  les Traversées, on était en train de **devenir un service météo gratuit**. Un
  pont de la Météo vers les départs transforme ce défaut en meilleur atout.
  📌 **À retenir sur la méthode** : c'est **le patron** qui a proposé la bonne
  priorité, à partir de ses propres chiffres. Les statistiques d'écrans sont la
  donnée la plus rentable qu'il m'ait donnée — **les redemander chaque semaine**.

- **23/08/2026 (💸 « ON PEUT RÉDUIRE NOTRE COMMISSION » — pourquoi j'ai répondu
  « pas d'abord »)** — le patron : « on peut réduire notre commission pour attirer
  les clients, je gagne ma vie avec un autre travail et le site ne coûte rien pour
  le moment ». Il a raison sur la contrainte — rien ne nous oblige à gagner de
  l'argent cette année. Mais le calcul dit que **ce levier est faible**.
  🚨 **LE FAIT QUI TRANCHE** : le commandant doit toucher ses 12 500, et **les 3 %
  KartaPay ne sont pas à nous** — on ne peut pas les offrir. Donc **même à ZÉRO
  commission, le client paie 12 875 contre 12 500 au port**. Donner 100 % de notre
  commission lui fait gagner **1 431 FC** et on reste **plus cher**. ➡️ **Si on
  choisit le terrain du prix, on perd par construction.** C'est de l'arithmétique.
  🔍 **Et le prix n'est pas le blocage prouvé** : l'entonnoir dit **140 → 16 → 6 →
  3**. La perte massive est **140 → 16 (89 % partent avant de voir un prix)**, et
  **6 → 3 = 50 %**, un bon taux parmi ceux qui ont vu le prix. **On n'a aucune
  preuve que le prix nous tue ; on a la preuve que la portée nous tue.**
  ⚠️ **Une baisse ne se reprend pas.** Les 4 350 FC gagnés depuis juillet (3 ×
  1 450) disent deux choses : c'est **abordable** de les donner, et **ce n'est pas
  la marge qui est cassée, c'est le volume**.
  ✅ **Recommandation, dans cet ordre** : **1)** prix **tout compris à 14 000**
  (358 FC/siège, on récupère notre promesse) ; **2) parler au commandant AVANT de
  toucher à notre marge** — il a **550 FC de marge dont il ignore l'existence**,
  s'il affiche 13 500 le client gagne **1 000 FC pour 0 FC de notre poche** ;
  **3)** si on baisse, en faire **une offre visible, limitée et comptée** (« les 20
  premiers billets de septembre : zéro commission »), réversible et **qui nous dit
  enfin si le prix était le blocage**.
  📌 **Le rapport décisif** : **une conversation avec le commandant déplace le prix
  de 1 000 FC et ne coûte rien ; donner toute notre commission le déplace de
  1 431 FC et coûte tout.** On commence par la conversation.
  ⚠️ **Un prix bas en silence, personne ne le remarque** — on aurait payé sans rien
  acheter. Si on baisse, ça doit être un **événement**.

- **23/08/2026 (🚨 LA CAUSE DU PRIX TROUVÉE : LE COMMANDANT GAGNE PLUS QUAND IL
  NOUS ANNONCE PLUS CHER)** — le patron a répondu à mes quatre questions, et le
  calcul qui en découle règle le sujet.
  📌 **Ses réponses** : « **c'est nous qui écrivons les chiffres donnés par le
  commandant** » ; les **10 % sont compris** dans le prix ; les **3 % KartaPay
  sont ajoutés** par-dessus ; **KartaPay est l'API qui permet le paiement MVola
  en ligne** ; et **on n'a qu'UN SEUL commandant**.
  🚨 **Le mécanisme, enfin identifié.** Sur un siège affiché 14 500 : le client
  paie **14 935** (14 500 × 1,03), le commandant touche **13 050** (90 %),
  MoheliGo **1 450**, KartaPay **435**. Or **le même commandant qui vend 12 500
  en direct touche 12 500**. ➡️ **En passant par nous à 14 500, il gagne 550 FC
  de PLUS par siège — et le client paie 2 435 FC de plus.** Le prix vient de lui,
  les 10 % sont pris dessus : **plus il annonce haut, plus il gagne**. Le système
  tel qu'il est construit **le récompense de nous donner le tarif officiel**.
  🚫 **Ce n'est pas une tricherie** — je me suis déjà trompé deux fois en
  cherchant un coupable. Il a donné le tarif officiel parce que **personne ne lui
  a jamais demandé autre chose**. Ce n'est pas une trahison, **c'est une
  conversation qui n'a jamais eu lieu**.
  💰 **Proposition (catégorie B, le patron tranche) : afficher 14 000 FC TOUT
  COMPRIS**, les 3 % à l'intérieur. Le commandant toucherait 12 233 FC, soit
  **267 FC de moins que sa vente directe**, mais sur des clients qu'il n'aurait
  pas eus (diaspora, voyageurs rares). En dessous de 14 000, on lui demande de
  gagner franchement moins qu'en direct : ça ne se négocie qu'avec du volume, et
  on ne l'a pas encore.
  🔴 **Ce qu'on peut réparer seuls et gratuitement** : le client voit 14 500 et
  paie 14 935. **Notre propre flyer dit « LE PRIX, TU LE CONNAIS AVANT DE
  PAYER »** — on se contredit sur la seule promesse qui nous distingue. **Le prix
  affiché doit être le prix payé.**
  ⛔ **Le retournement « afficher tous les commandants » est mort pour l'instant** :
  avec **un seul** commandant il n'y a rien à comparer. Il devient un argument de
  recrutement. 📌 **Et c'est structurel** : recruter un 2ᵉ et un 3ᵉ commandant est
  **la seule façon que le prix se règle par le marché au lieu de la négociation** —
  et tant qu'il n'y en a qu'un, MoheliGo a **un point de panne unique**.
  ✅ **Question KartaPay classée** : KartaPay **est** la passerelle MVola en ligne,
  il n'y a pas de « MVola moins cher » à côté. L'alternative manuelle
  économiserait 435 FC et rouvrirait le doute « c'est ainsi ? » vu en WhatsApp.
  📌 **Leçon confirmée** : les quatre questions posées avant d'analyser ont donné
  en un seul message ce que trois analyses confiantes n'avaient pas trouvé.

- **23/08/2026 (🔴🔴 LE PRIX : ON VEND AU TARIF OFFICIEL DANS UN MARCHÉ QUI NE LE
  PRATIQUE PAS)** — ⚠️ **Il m'a fallu trois explications du patron pour
  comprendre**, et j'ai écrit deux analyses fausses que j'ai supprimées de ce
  journal plutôt que corrigées : d'abord « les clients négocient au port », puis
  « nos commandants nous sous-cotent déloyalement ». Les deux étaient à côté.
  📌 **Ce qu'il a fini par me dire** : « **15 000, c'est le prix officiel, mais
  personne ne paie ça.** Nous on a **10 % du billet**, et **3 % s'ajoutent pour
  KartaPay**. Les commandants réduisent leurs prix pour avoir des clients, car
  **les clients sont aussi habitués aux commandants**. »
  🚨 **Les trois conclusions, qui renversent mes deux analyses précédentes :**
  1. **Ce n'est pas de la déloyauté, c'est un marché.** Les commandants ne cassent
     pas les prix *contre nous* : ils les cassent **entre eux**, pour capter des
     clients déjà habitués à eux. Nous ne sommes même pas leur cible.
  2. **Notre problème n'est pas la commission.** 10 % + 3 % sur 12 500 ≈ 1 600 FC.
     **L'écart de 5 000 FC ne vient pas de notre marge, il vient du prix qu'on
     affiche** : on vend au tarif officiel dans un marché qui ne l'applique
     jamais. C'est afficher le prix du catalogue quand tout le monde est en solde.
  3. **Le vrai concurrent n'est pas le prix, c'est l'HABITUDE.** On appelle son
     commandant comme on appelle son taxi. C'est la *disponibilité mentale* du
     § 1 — elle se construit par la régularité, jamais par une remise.
  💡 **LE RETOURNEMENT PROPOSÉ** : aujourd'hui, pour comparer, un voyageur doit
  appeler ses commandants un par un. **Si MoheliGo affiche les départs de
  plusieurs commandants avec leurs VRAIS prix, la guerre des prix cesse d'être
  notre problème : elle devient notre produit.** Le voyageur ne compare plus
  « MoheliGo contre le commandant », il compare **les commandants entre eux, chez
  nous**.
  📌 **Et notre public n'est pas celui qui a déjà son commandant** — le § 1 le dit
  et les chiffres le confirment : la croissance vient des **acheteurs légers**.
  Nos clients sont la diaspora (qui n'a le numéro de personne), ceux qui
  traversent rarement, et ceux qui ne veulent pas appeler cinq personnes.
  🔴 **Quatre questions avant d'écrire quoi que ce soit sur les prix** : qui fixe
  le prix affiché (nous ou le commandant) ? les 10 % sont-ils **pris sur** le prix
  ou **ajoutés par-dessus** ? MVola coûte-t-il moins que les 3 % de KartaPay ?
  et **combien de commandants sont sur la plateforme** — s'ils sont plusieurs,
  l'affichage comparatif est possible tout de suite.
  ⚠️ **Le flyer « les prix » reste hors rotation** : afficher un tarif que
  personne ne pratique, c'est se présenter comme le plus cher du marché.
  📌 **Leçon de méthode, la troisième de la journée** : j'ai produit deux analyses
  complètes et confiantes sur des faits que je n'avais pas. **Sur un sujet
  économique, poser les questions AVANT d'analyser** — une analyse fausse est plus
  dangereuse qu'un chiffre faux, parce qu'elle ressemble à un raisonnement.

- **23/08/2026 (⏰ L'HEURE DU BUS : 6H30 — et l'erreur que l'attente a évitée)** —
  Le patron tranche : **le bus part à 6h30**.
  🚨 **Ça valide une prudence qui aurait pu passer pour de la lenteur.** Dans la
  conversation WhatsApp montrée plus tôt, la réponse donnée au client était
  **« 7h00 »** — qui est en réalité l'heure de la **vedette**, celle imprimée sur
  la carte d'embarquement. **Un voyageur arrivé à 7h à Kartala aurait raté son
  bus, et sa traversée avec.** Si j'avais imprimé « 7h00 » sur un visuel diffusé
  à des centaines de personnes, on aurait industrialisé l'erreur.
  📌 **La règle du § 11 (« jamais un horaire dont on n'est pas sûr ») vient de
  payer pour la première fois de façon mesurable.**
  📌 **Et un second enseignement** : répondre à la main, cent fois, finit
  toujours par produire une erreur — un soir de fatigue, on donne l'heure de
  l'autre chose. **Une information juste, écrite une fois au bon endroit, vaut
  mieux que cent réponses de mémoire.**
  ✅ `flyer37-vraiprix` distingue désormais explicitement les deux heures :
  **6h30 le bus, l'heure du billet la vedette.**

- **23/08/2026 (🔴 UNE VENTE PERDUE DONT ON CONNAÎT LA PHRASE EXACTE — et ce
  qu'elle vaut)** — Le patron donne les faits du trajet terrestre **et** raconte
  un appel : *« est-ce qu'on paie tous ces frais ici ? comme ça on va juste
  là-bas pour voyager sans se casser la tête »* — réponse non — *« ça ne vaut pas
  la peine alors »*. Le client n'a pas réservé.
  📌 **Les faits** : bus au départ de **Kartala, à Moroni** (point de rendez-vous
  des clients et des commandants, bus réservés par les commandants), **1 000 FC**
  par client, **500 FC par colis**, **1 000 FC au port**. Tout est déjà écrit
  dans l'application, partie « info pratique ».
  🚨 **CE QUE LA VENTE PERDUE DIT VRAIMENT** : ce n'est pas le montant qui a fait
  fuir — c'est de **payer trois fois, à trois endroits, sans connaître le total**.
  Il n'achetait pas moins cher : il achetait **de ne plus avoir à y penser**.
  C'est mot pour mot notre positionnement (§ 2) — *supprimer l'incertitude* — et
  on l'a fait pour la place, l'heure et la mer, **mais pas pour l'argent**.
  💡 **Décision proposée au patron (catégorie C) : le forfait tout compris** —
  traversée + bus + port, un seul paiement en ligne. La chaîne existe déjà (les
  commandants réservent les bus, le rendez-vous existe, on encaisse déjà) ; il ne
  manque que d'encaisser le tout et de reverser. Les quatre points à regarder en
  face (trésorerie, droit d'encaisser pour le port, remboursement total,
  jours de mer forte) sont écrits dans `QUESTIONS-CLIENTS.md`.
  ✅ **En attendant, ce qui ne coûte rien : tout dire.** `flyer37-vraiprix`
  (« Ton voyage, sans surprise ») détaille les trois postes. Il ne supprime pas
  les trois paiements, il supprime **la surprise** — et une surprise au port, la
  valise à la main, coûte bien plus qu'un client qui renonce chez lui.
  📌 **Et un enseignement qui vaut pour tout** : le patron précise que ces infos
  **sont déjà dans l'application**. Les clients appellent quand même. **Une
  information écrite au mauvais endroit n'existe pas.** On n'ouvre pas « info
  pratique » avant de réserver, on l'ouvre quand on a déjà un problème. Le total
  du voyage doit s'afficher **sur l'écran de réservation**.
  ⭐ **Le témoignage est autorisé** : le patron a obtenu l'accord de la cliente,
  à condition d'effacer son numéro. Le visuel reste à faire.

- **23/08/2026 (⚠️ J'AI REDATÉ CINQ ENTRÉES — la même erreur, en pire)** — En
  vérifiant le calendrier, je découvre qu'on est le **23 août au soir** (le 24 au
  petit matin aux Comores) et non le 18. J'avais daté du 18/08 tout ce qui a été
  écrit ce soir : le premier chiffre de visites, le tunnel, les trois ventes, les
  conversations clients, le blocage humain. **Corrigé au 23/08.** Les trois
  entrées du 18 qui restent (reprise, « les pubs ne partent pas », semaine
  préparée) sont vérifiées par les exécutions GitHub, elles.
  📌 **C'est la deuxième fois en une semaine.** La cause est structurelle : **je
  n'ai aucune horloge entre deux messages du patron** — cinq jours peuvent passer
  sans que rien ne me le signale, et je continue au dernier repère connu.
  ✅ **La garde, désormais dans la règle en trois lignes du dossier** : *lancer
  `date` AVANT d'écrire quoi que ce soit de daté.* Une leçon écrite mais non
  outillée ne tient pas — celle-ci est maintenant dans le README, à l'endroit
  qu'on lit en premier.

- **23/08/2026 (🚨 LE BLOCAGE N°1 EST HUMAIN, PAS TECHNIQUE — la phrase qui
  renverse mon analyse)** — Le patron, à propos de deux des trois premières
  clientes : **« elles m'avaient appelé sur WhatsApp AVANT de valider le
  paiement, elles voulaient être sûres qu'il y avait quelqu'un derrière. »**
  Je cherchais le blocage dans la mécanique du tunnel — trop d'étapes, MVola,
  prix peu clair. **Il n'est pas là.** Ces clientes savaient payer. Elles
  doutaient de NOUS : *y a-t-il un vrai humain derrière ce site, ou est-ce que je
  vais perdre mon argent ?*
  📌 **Les trois conséquences, écrites dans `QUESTIONS-CLIENTS.md`** :
  1. **le WhatsApp n'est pas le service après-vente, c'est le dernier maillon de
     la vente** — sans l'appel, pas de vente ; et les 3 paiements abandonnés sont
     probablement ceux de gens qui ont eu le même doute sans appeler ;
  2. **il ne faut pas éviter l'appel, il faut le provoquer** : chaque appel est
     une vente presque faite. C'est exactement M-Pesa (§ 13.2) — l'adoption est
     venue de l'agent humain, pas de l'application ;
  3. **ce qui manque au site n'est pas une fonction, c'est une preuve de vie** :
     un numéro qui répond, un nom, un visage, un lieu.
  ✅ **`flyer36-quelquun` créé dans la foulée** — « Tu veux être sûr qu'il y a
  quelqu'un ? C'est normal. Alors appelle avant de payer. » Placé le **mercredi**,
  le jour où l'on parle d'argent et donc où le doute est le plus vif ; il sort
  demain (semaine ISO 34). Il encourage l'appel au lieu de le dissuader, et il
  utilise enfin le commandant nommé sur le billet comme preuve.
  ⏳ **Décision produit proposée au patron** : mettre le numéro WhatsApp **dans
  l'écran de paiement**, pas dans un pied de page, avec « un doute ? appelle
  avant de payer ». C'est probablement le changement le plus rentable du site.

- **23/08/2026 (🗣️ LES CONVERSATIONS CLIENTS — et le trou qu'elles révèlent dans
  le produit)** — Le patron montre deux échanges WhatsApp avec des acheteurs.
  **C'est la matière la plus utile qu'on ait eue depuis le début**, et ça a
  ouvert `dossier/QUESTIONS-CLIENTS.md`.
  🚨 **LA DÉCOUVERTE** : un client **qui avait déjà payé** demande *« le bus part
  à quelle heure ? »* puis *« à combien on paie pour le bus ? »*. Il y a un point
  de rendez-vous à terre avant l'embarquement.
  **On vend une traversée de port à port ; le client, lui, achète un voyage de
  chez lui jusqu'à Mohéli.** Le trou n'était ni dans le paiement, ni dans les
  flyers : il est dans la **définition du produit**. Et la question qu'un client
  pose *après* avoir payé est très probablement celle qui a fait renoncer ceux
  qui n'ont pas payé.
  ⛔ **Je n'écris rien là-dessus tant que je n'ai pas les faits** (§ 11 : jamais
  d'horaire ni de prix inventé). Quatre questions posées au patron : le bus
  est-il à nous ? d'où et à quelle heure part-il ? combien coûte-t-il ? vaut-il
  pour les deux liaisons ?
  ⭐ **PREMIER TÉMOIGNAGE, ET IL EST SPONTANÉ** : au « Bien arrivé ? » du patron,
  le client répond *« Oui alhamdoulillah. Remercie le commandant de notre part.
  Il est très professionnel et bienveillant. »* C'est le levier preuve sociale
  (§ 3), le seul qui nous manquait — **mais c'est un message privé : on ne le
  publie pas sans l'accord de la personne.**
  💡 **Un actif qu'on n'utilisait pas : le commandant.** Son nom est **déjà
  imprimé sur la carte d'embarquement** — le voyageur sait qui pilote avant de
  monter. Dans un métier où la peur est réelle, c'est un argument de confiance
  rare, déjà dans le produit, et absent de tous nos visuels.
  📌 **Le « Bien arrivé ? » du lendemain est du service client de très haut
  niveau** — probablement la raison pour laquelle les trois acheteurs ont suivi
  la page. À garder comme règle de maison.
  🔒 **RAPPEL DE SÉCURITÉ, dit au patron** : le dépôt est **public**. Les captures
  de conversation contiennent nom, numéro et référence de billet : elles ne
  doivent **jamais** y être déposées. Dans `QUESTIONS-CLIENTS.md` on ne garde que
  la question, jamais la personne.

- **23/08/2026 (🎉 LES TROIS PREMIÈRES VENTES — la chaîne fonctionne de bout en
  bout)** — Le patron : « 543 c'est depuis le lancement en juillet, et 3 personnes
  ont payé et suivi MoheliGo. »
  🚨 **C'est le jour le plus important du projet depuis le premier flyer.**
  Jusqu'ici, « quelqu'un peut réserver et payer une traversée depuis son
  téléphone » était une hypothèse. **Ce n'en est plus une.** Trois personnes ont
  choisi un départ, payé, et reçu leur billet — et elles ont suivi la page
  ensuite, ce qui veut dire qu'elles n'ont pas été déçues.
  📊 **Le tunnel réel, depuis juillet** : 543 ouvertures → 6 tentatives de
  paiement → **3 payées**. Soit **une réussite sur deux au paiement** : pour un
  marché où presque personne n'a jamais acheté en ligne, ce n'est pas mauvais.
  Le vrai goulot reste plus haut (11 % seulement vont voir les Traversées).
  🚦 **Position dans la feuille de route** : l'étape 1 demande **10 réservations
  d'inconnus**. On est à **3**. Le seuil n'est plus théorique.
  📌 **CE QUI DOIT ÊTRE FAIT MAINTENANT, ET QUI VAUT PLUS QUE DIX FLYERS** :
  1. **Parler à ces trois personnes, une par une.** Comment ont-elles connu
     MoheliGo ? Qu'est-ce qui les a fait hésiter ? Qu'ont-elles cru qui était
     faux ? C'est la leçon d'Airbnb (§ 14.3) : aller voir ses premiers clients un
     par un ne passe pas à l'échelle, et c'est exactement pour ça que ça marche.
  2. **Rappeler les trois qui ont abandonné** — si leur numéro a été saisi avant
     l'abandon. Un message simple (« on a vu que ça n'a pas abouti, on peut vous
     aider ? ») peut en récupérer un : ce serait +33 % de ventes en une heure de
     travail, sans un franc de publicité.
  3. **Demander UN mot ou UNE photo du billet** à l'un des trois. Un témoignage
     vrai vaut plus que tout ce que je peux dessiner — c'est le levier « preuve
     sociale » (§ 3), le seul qu'on n'a pas encore.
  ⚠️ **Ce qu'on ne fera PAS** : afficher « déjà 3 traversées réservées » sur un
  flyer. Trois, ça se dit entre nous, pas en public — un chiffre trop petit
  affiché comme un exploit fait l'effet inverse.

- **23/08/2026 (📊 LE TUNNEL COMPLET — et il dit que le trou n'est PAS où je le
  cherchais)** — Le patron envoie les statistiques d'écrans de l'application, et
  le chiffre d'abandon : **« 3 ont commencé et n'ont pas fini. »**

  | Écran | 7 jours | 30 jours |
  |---|---|---|
  | **Ouvertures de l'application** | **140** | **543** |
  | Accueil | 41 | 90 |
  | Messagerie | 11 | 74 |
  | Traversées | 16 | 67 |
  | Météo mer | 21 | 66 |
  | Découvrir | 15 | 46 |
  | Billets | 9 | 31 |
  | Compte | 8 | 25 |

  🚨 **CE QUE ÇA RÉVÈLE, ET C'EST LA DÉCOUVERTE LA PLUS IMPORTANTE DEPUIS LE
  DÉBUT** : sur **140 ouvertures en 7 jours, seulement 16 vont voir les
  Traversées** — **11 %**. Neuf personnes sur dix ouvrent l'application et ne
  regardent jamais un départ. **Le trou n'est pas au paiement : il est tout en
  haut du tunnel.**
  📌 **Et la Météo mer (21) est plus consultée que les Traversées (16).** C'est à
  double tranchant, et il faut le dire franchement :
  · ✅ **la preuve que notre stratégie marche** — le bulletin du soir amène du
    monde, c'est bien lui qui fait venir ;
  · ⚠️ **et son revers** : on est en train de devenir un service météo. Les gens
    viennent chercher ce qu'on donne gratuitement, prennent l'information, et
    repartent sans jamais voir un départ. **Le pont entre les deux écrans est le
    chantier n°1.**
  ⚠️ **CORRIGÉ LE 18/08 — j'avais mal lu.** J'avais écrit « 3 commencés, 0 fini ».
  Le patron a précisé : **3 personnes ONT PAYÉ**, en plus des 3 qui ont abandonné.
  Le paiement aboutit donc **une fois sur deux** — ce qui, pour un marché sans
  habitude d'achat en ligne, n'est pas mauvais du tout. Ne jamais compléter un
  chiffre manquant par l'hypothèse la plus sombre : c'est encore inventer.
  📌 **Messagerie : 74 ouvertures sur 30 jours**, plus que les Billets (31). Les
  gens écrivent. Chaque message est une vente possible et une question à noter
  (étape 1 de la feuille de route : 30 vraies conversations).
  ⚠️ **La colonne « 30 j » est en réalité « depuis le lancement en juillet »**
  (précisé par le patron). Donc **140 ouvertures en 7 jours sur 543 depuis le
  début = 26 % de toute l'activité de l'application s'est produite dans la
  dernière semaine.** L'accélération n'est pas une impression.
  ⚠️ **Ce que je ne sais pas et que je n'invente pas** : pourquoi « Accueil » (90)
  est très inférieur aux ouvertures (543) — écran distinct, ou seulement les
  retours à l'accueil ? Sans le savoir, on ne peut pas calculer le taux réel de
  la première étape. À demander avant de bâtir dessus.
  ➡️ **Le renversement de priorité** : jusqu'ici je poussais l'acquisition. Les
  chiffres disent que l'acquisition marche et que **la marche à monter est le
  passage météo → départs**. Publier plus n'y changerait rien : c'est un problème
  de produit, pas de publicité (§ 8 et § 13.3, audit de friction).

- **23/08/2026 (📈 LE PREMIER CHIFFRE DE RÉSULTAT — les visites ont été
  multipliées par cinq)** — Le patron : « je commence à voir une montée des
  visiteurs sur le site, c'était 5-6 par jour, c'est monté à 25-26 par jour. »
  **C'est la première mesure qu'on obtient depuis le début du projet**, et c'est
  l'un des trois chiffres que je réclame chaque dimanche (§ 8 du manuel).
  📊 **Ce que ça dit** : ×4 à ×5 en une semaine et demie de présence quotidienne.
  Avec 26 abonnés Facebook, la page seule ne peut pas expliquer 25 visites par
  jour — ça veut dire que ça circule ailleurs : partages, bouche-à-oreille, QR
  des flyers, recherche. **C'est la meilleure nouvelle possible : l'audience
  n'est plus le problème.**
  ⚠️ **Ce que ça ne dit PAS, et qu'il ne faut pas surinterpréter** : quelques
  jours ne font pas une tendance, la reprise des traversées crée forcément un
  pic, et une visite n'est pas une réservation. Sur de petits nombres, un
  quintuplement peut aussi être trois personnes curieuses de plus par jour.
  🚦 **Ce que ça change dans la conduite** : la question n'est plus « comment
  faire venir du monde » mais **« pourquoi ceux qui viennent ne réservent pas —
  ou combien réservent »**. C'est le passage de l'acquisition à la conversion.
  Le seuil de l'étape 1 de la feuille de route (**10 réservations d'inconnus en
  6 semaines**) devient mesurable : ~175 visites par semaine, donc si les
  réservations restent à 0, le problème est **dans le site ou le paiement**, pas
  dans la publicité. Le manuel est formel : ne pas payer de publicité pour
  remplir un seau percé.
  📌 **Les deux chiffres qui manquent maintenant, et ils sont urgents** :
  **1)** réservations payées sur la semaine ; **2)** réservations commencées
  moins terminées (l'abandon au paiement). Sans le second, on ne saura pas si
  c'est l'offre ou le tunnel de paiement qui bloque.
  ✅ **Le hasard fait bien les choses** : le visuel de la garantie (« et si la
  vedette ne part pas ? ») est parti aujourd'hui même. C'est exactement le
  levier de conversion dont on a besoin maintenant — il lève la peur de perdre
  son argent chez quelqu'un qui est déjà sur le site.

- **18/08/2026 (LA SEMAINE PRÉPARÉE — et la rotation qui existe enfin)** — Le
  patron : « prépare les flyers de la semaine, note les traversées sont
  ouvertes. » L'ouverture était déjà notée (`OUVERT = True`, poussé le matin même).
  ⚠️ **Le vrai problème était ailleurs, et il fallait le voir** : la semaine était
  déjà « couverte »… par **exactement les mêmes sept visuels que la semaine
  précédente**. Les abonnés allaient revoir les mêmes, jour pour jour. Préparer
  la semaine, ce n'était donc pas vérifier qu'elle est remplie : c'était la
  **renouveler**.
  🆕 **Trois angles neufs, choisis pour ce qu'ils débloquent, pas pour faire
  nombre** — les trois répondent à une objection qu'aucun visuel ne traitait :
  · **`flyer33-garantie`** — « et si la vedette ne part pas ? » C'est l'objection
    numéro un dans un pays où la mer décide, et on venait de passer six jours à
    la démontrer en public. Rien d'inventé : le changement de date gratuit et le
    remboursement avant départ sont ceux qu'on annonce déjà les jours de mer
    forte. Le visuel les sort de la crise pour en faire un argument permanent.
    **La ligne du pied porte tout : « Nous ne garantissons pas la mer. Nous
    garantissons ton argent. »** — on garantit le remboursement, jamais le départ.
  · **`flyer34-premierefois`** — pour qui n'a jamais payé sur internet (§ 5 du
    manuel). Il ne dit pas « c'est simple » (interdit § 11 : ça humilie celui qui
    a peur de ne pas savoir) : il rattache le geste à **MVola**, que la personne
    fait déjà. « C'est le même geste qu'envoyer du MVola. »
  · **`flyer35-ports`** — « je pars d'où, moi ? » On nomme quatre ports dans tous
    nos textes sans jamais dire lequel choisir. Un obstacle pratique non levé
    arrête autant qu'un prix trop élevé (§ 13.3, audit de friction). **Aucun
    horaire ni durée** : non vérifiés.
  🔄 **La rotation par numéro de semaine ISO sert enfin à quelque chose** : lundi,
  mardi et samedi ont maintenant deux variantes (comme dimanche depuis le 12/08),
  et les neuves sont en **position [0]** pour sortir dès cette semaine (34 % 2 = 0).
  Semaine 35 : les anciennes reviennent. **La condition écrite dans
  `calendrier.py` est respectée — les deux variantes sont du même système.**
  📌 **Ce que « préparer la semaine » veut dire, pour la prochaine fois** :
  vérifier que chaque jour a un visuel, puis vérifier qu'il n'est pas le même que
  la semaine d'avant. Le second contrôle est celui qui compte.

- **18/08/2026 (🚨 « LES PUBS NE PARTENT PAS AUTOMATIQUEMENT » — elles partaient,
  c'est le RAPPORT qui mentait)** — Le patron avait raison de s'inquiéter et tort
  sur les faits, et c'est ma faute : il lisait un chiffre que je fabriquais mal.
  🔍 **Les faits, relevés dans les journaux GitHub** (14 exécutions programmées) :
  · **Bulletin du soir : 7 soirs sur 7**, du 11 au 17 août, tous en succès ;
  · **Publication du jour : 5 jours sur 5**, du 13 au 17 août ;
  · **Matin : lundi et jeudi**, exactement comme prévu (à blanc, `PUBLIER_MATIN`
    est toujours désarmé).
  Et la preuve qu'elles publiaient vraiment : lundi 17/08 à 12h54,
  `…_122116129533374081` — « RIEN À INSTALLER. C'EST JUSTE UNE PAGE ».
  ⏰ Retards de GitHub observés : de 26 min à 1 h 12. Le cron à `:07` avec marge
  d'avance fait bien tomber la publication autour de midi. Rien à changer.
  🚨 **LA VRAIE PANNE, ET ELLE ÉTAIT DANS MON RAPPORT** : `rapport.py` comptait
  les lignes de `journal-publications.json`, un fichier écrit **sur le serveur
  GitHub, effacé à la fin de chaque travail**. Il affichait donc « 1 publication
  en 7 jours » tous les jours, quoi qu'il arrive. C'est ce chiffre que le patron
  lisait — et il en a conclu, logiquement, que rien ne partait.
  📌 **LA LEÇON, à ne jamais oublier** : *un compteur qui repart de zéro à chaque
  exécution ne mesure rien.* Et surtout : **un chiffre faux dans un rapport coûte
  plus cher qu'une panne.** Une panne se voit et se répare ; un chiffre faux
  détruit la confiance dans tout le système, y compris dans ce qui marche.
  Je connaissais ce défaut depuis le 12/08 et je l'avais classé « à faire plus
  tard » : c'était une erreur de priorité.
  ✅ **Corrigé** : `publier_fb.publications_recentes()` demande les vraies
  publications à la page (`published_posts`, puis `feed` en secours). `rapport.py`
  s'en sert comme source de vérité et n'utilise le journal local qu'en dernier
  recours, **en écrivant noir sur blanc que le compte est alors incomplet**.
  Nouvelle case `rapport_seulement` pour produire un rapport sans rien publier.
  ⚠️ **Et le premier essai a produit un autre chiffre faux** : « 50 publications
  en 7 jours », c'est-à-dire la limite de l'appel — **Facebook ignore le
  paramètre `since`** sur ces deux bords. Le filtrage par date se fait maintenant
  chez nous. Corriger un chiffre faux par un autre chiffre faux aurait été pire
  que tout : **vérifier ce que renvoie une API avant de s'appuyer dessus**.

- **18/08/2026 (✅ REPRISE DES TRAVERSÉES)** — Le patron, mardi au petit matin :
  « aujourd'hui c'est la reprise des traversées, publie maintenant. » La fermeture
  aura duré **six jours** (12 → 18/08) — et elle s'est terminée exactement le
  mardi qu'il avait dit « possible » le 12.
  📌 **La leçon vaut d'être gardée** : la date est tombée juste, et on a quand
  même eu raison de ne jamais l'annoncer. Six jours à promettre mardi, c'était
  six jours à jouer notre parole aux dés — le résultat ne change pas le calcul.
  ⚠️ **Erreur de ma part, corrigée** : j'avais daté cette reprise du 13/08 dans
  `service.py`, `MEMOIRE.md` et `README.md`, parce que ma session s'était arrêtée
  ce jour-là. **Je n'ai aucune horloge entre deux messages du patron : cinq jours
  peuvent passer sans que je le sache.** Vérifier la date réelle (`date -u`) avant
  d'écrire un événement daté — surtout dans les fichiers qui font foi.
  **Les deux gestes, dans l'ordre écrit dans `service.py`** :
  1. `OUVERT = True` — et tout se remet en place tout seul : plus de mention de
     fermeture sur les pubs, bandeau du soir redevenu « RÉSERVE POUR DEMAIN »,
     conseil de mer normal, calendrier de la semaine reparti.
  2. **l'annonce de reprise publiée** (`flyer-reprise-facebook.png`).
  🔧 **Nouveau chemin `programme.py --reprise`** (+ case `reprise` dans le
  workflow) : le patron avait dit « ne le donne pas au robot », puis « publie
  maintenant » — les deux sont vrais, d'où un chemin **explicite, jamais sur
  minuterie**. Et une sécurité : il **refuse de publier si `service.py` dit encore
  fermé**, sinon l'annonce de reprise partirait sous la mention « les départs sont
  suspendus » — deux messages qui se contredisent le même jour.
  🗄️ **La fermeture est archivée, pas effacée** : dates, mots du patron, raison.
  C'est le modèle de la prochaine. Refermer = `OUVERT = False` + `depuis` à jour.

- **13/08/2026 (🚨 DÉCISION DU PATRON : LES PUBS CONTINUENT PENDANT LA FERMETURE)** —
  « Les pubs continuent même si c'est fermé jusqu'à mardi. »
  J'avais recommandé l'inverse, et je l'avais dit clairement. **Il a tranché : sa
  décision, son entreprise** (règle A/B/C, § 12.2 ter — la direction générale
  garde ce poste). Exécuté sans discuter davantage.
  📌 **Ce qui est juste dans sa décision, et que j'avais sous-estimé** : on ne
  vend pas une traversée « pour demain », on vend **une place sur un départ à
  venir**. Réserver aujourd'hui pour la semaine prochaine n'a jamais été un
  mensonge. Et six jours de page commercialement muette coûtent une habitude
  qu'on met des mois à bâtir. Mon garde-fou était juste sur le principe et trop
  large dans son application.
  ✅ **Ce que j'ai gardé, parce que ça ne coûte rien et que ça évite le seul
  dégât irréparable** : `service.MENTION_FERMETURE`, collée automatiquement à
  **chaque** publication commerciale tant que `OUVERT = False` —
  « ⚠️ en ce moment les départs sont suspendus (mer agitée) ; tu peux prendre ta
  place pour les jours qui viennent ; ne descends pas au port avant qu'on annonce
  la reprise ici. » Elle dit la vérité, autorise la réservation à l'avance, et ne
  promet aucune date. Placée **avant les mots-dièse** : au-dessus elle tuerait
  l'offre, sous les hashtags personne ne la lirait.
  🔧 **L'interrupteur** : `PUB_PENDANT_FERMETURE = True` dans `service.py`. Le
  remettre à `False` recoupe les pubs et remet le point du service à midi
  (`texte_du_point` reste écrit, et `programme.py --point` le publie à la main).
  ⚠️ **Ce qui NE change pas, et pourquoi** :
  · **le bandeau du bulletin du soir reste « TRAVERSÉES SUSPENDUES »** — lui parle
    de la mer de DEMAIN, donc « réserve pour demain » y serait faux, mention ou
    pas. C'est la seule chose que je n'ai pas rouverte.
  · **le matin reste muet** : la démonstration explique le geste « réserve ton
    départ », qui n'aboutit pas aujourd'hui.
  🔬 **`controle.py` : l'invariant s'est INVERSÉ.** Avant : aucun mot commercial
  pendant une fermeture. Maintenant : **aucune publication commerciale sans la
  mention**. Vérifié dans les deux sens — en effaçant la mention exprès, le
  contrôle crie ; en la remettant, il se taît. Un contrôle qu'on n'a pas testé
  après avoir changé la règle ne vaut rien.

- **13/08/2026 (🚨 « LE FLYER DE 12 N'EST PAS PARTI » — ce n'était pas une panne,
  et c'était quand même une erreur)** — Le patron, 15h20 : « le flyer de 12 n'est
  pas parti. »
  🔍 **Vérifié avant de répondre** : le travail programmé a bien tourné
  (exécution `31690579346`, lancée à 10h19 UTC = **13h19 aux Comores**, soit
  72 min après le cron de 12h07 — le retard habituel de GitHub, en pire), il
  s'est terminé en succès, et il n'a rien publié **parce que le service est
  fermé**. Le garde-fou écrit hier a fonctionné exactement comme prévu.
  ⚠️ **Mais il avait raison de le remarquer, et j'avais tort de me satisfaire du
  silence.** Ma règle d'hier (l'avis une fois, puis plus rien à midi) laissait la
  page muette six jours d'affilée. Deux dégâts : la page perd l'habitude qu'elle
  est en train de construire (c'est son seul actif, § 1 du manuel), et les gens
  qui ne voient plus rien concluent tout seuls — « ils ont coulé », « ils ont
  fermé ». Le silence n'est pas neutre : il est interprété.
  ✅ **Corrigé — LE POINT DU SERVICE à midi, tous les jours de fermeture** :
  `service.texte_du_point()` écrit l'état du jour (« OÙ EN EST LE SERVICE —
  JOUR N »), **avec les vrais chiffres de la mer** relevés par `mer.niveau()`, et
  sans eux si Open-Meteo ne répond pas. Visuel : celui de l'avis (un avis officiel
  a le droit de se répéter, comme un panneau). **Zéro appel commercial, aucune
  date de reprise.**
  📌 **Ce qui distingue les trois messages, pour ne pas les confondre :**
  · **l'avis** (jour 1) annonce la fermeture ;
  · **le point de midi** dit où en est le SERVICE aujourd'hui ;
  · **le bulletin du soir** dit où en sera la MER demain.
  Trois angles, aucun doublon — c'est ce qui permet de publier deux fois par jour
  pendant une fermeture sans fatiguer personne.
  🔧 **Deux corrections de robustesse au passage** : le matin ne part plus du tout
  pendant une fermeture (montrer *comment réserver* un jour où on ne peut pas
  réserver n'a aucun sens), et `avis_de_gros_temps()` ne plante plus si
  Open-Meteo répond au premier appel puis pas au second (il déballait trois
  valeurs d'un `None`).
  ⚠️ **`controle.py` a été remis en phase avec le vrai robot.** Il décrivait
  encore l'ancien comportement (« rien ne part »). **Un contrôle qui décrit un
  robot différent du vrai est pire que pas de contrôle** — c'est la même famille
  d'erreur que le voyant menteur d'hier. À vérifier à chaque fois que
  `programme.main()` change.

- **12/08/2026 (LE VISUEL DE REPRISE — et pourquoi il n'est PAS dans le robot)** —
  Le patron : « fais un flyer de reprise alors, mais pas de date au cas où. Ne le
  donne pas au robot, donne-le-moi, je le publierai. »
  `flyer32-reprise-fb.html` → **`flyer-reprise-facebook.png`**, texte dans
  `page.py`. **Aucune date, aucun jour, aucune heure dans l'image** : il resservira
  à la prochaine fermeture sans être refait.
  📌 **Il a raison de le garder à la main** : le robot publie à 12h07, or une
  reprise ne se décide pas à 12h07 — elle se décide quand la vedette part
  vraiment. Un visuel de reprise parti une heure trop tôt serait exactement la
  promesse qu'on a passé la semaine à ne pas faire.
  ⚠️ Cette consigne ne tient pas dans un commentaire : **`controle.py` la
  vérifie** désormais (dictionnaire `MANUELS`) et signale une erreur si le visuel
  entre dans `calendrier.py`. Et la marche à suivre de la réouverture est écrite
  en tête de `service.py` : **1)** le patron publie la reprise à la main,
  **2)** `OUVERT = True` et pousser sur `main`. Faire le 2 sans le 1, c'est
  reprendre la vente sans avoir annoncé la reprise.
  🎨 **Ce qui porte le visuel** : le fond revient au bleu de tous les jours
  (`#0F2A5C`) au lieu du marine profond des avis — le changement de fond EST le
  message. Et la ligne qui paie toute la semaine d'honnêteté : « **Tu l'as su le
  jour où ça s'est arrêté. Tu le sais le jour où ça repart.** » C'est le seul
  visuel d'avis avec un appel commercial complet (QR, adresse, paiement) : les
  jours de fermeture on ne demandait rien, donc ici on peut demander.
  🔬 **Le contrôleur a servi tout de suite** : l'accroche était à 82px d'après ma
  règle des 0,47 — elle passait à la ligne et recouvrait le bloc suivant.
  `verifier.js` l'a vu, j'ai **mesuré** (876px à 78px dans 920 disponibles) au
  lieu d'estimer. **La règle sert à viser, le contrôleur tranche.**

- **12/08/2026 (LA VIDÉO PROMO CONFIÉE À YOUNG LEADER)** — Le patron : « fais-moi
  un prompt pour une vidéo promo de MoheliGo qui sera faite par Young Leader. »
  Écrit dans **`dossier/BRIEF-VIDEO-YOUNG-LEADER.md`**, et publié en page lisible :
  https://claude.ai/code/artifact/9c05c5c9-f9d5-4b66-84dc-3154b314f9c4
  Le document se lit dans les deux sens : le § 1 est **le message à envoyer tel
  quel** (la page a un bouton qui le copie), les § 2 à 9 sont le brief à leur
  transmettre, le reste est pour nous.
  📌 **Les choix qui portent le brief, et pourquoi :**
  · **un seul but** — que le spectateur ouvre moheligo.com. Une vidéo qui veut
    tout dire ne fait rien faire, et un brief qui ne nomme pas le geste attendu
    ramène de belles images inutilisables ;
  · **vertical 9:16, 30 s + 15 s, lisible sans le son**, sous-titres incrustés :
    Facebook coupe le son par défaut ;
  · **commentaire en shimwali, sous-titres en français** — une pub en français
    seul dit « c'est pour les gens de la ville » ; les sous-titres ouvrent à la
    diaspora, qui paie souvent la traversée d'un proche ;
  · **le déroulé en 7 plans** suit l'ordre qui fait agir (le doute → la solution →
    la preuve → le geste), avec les textes à l'écran déjà écrits ;
  · **les interdits de tournage** reprennent le § 11 du manuel : aucun horaire ni
    prix promis, aucune fausse affluence, aucun billet de vrai client, rien de
    généré, rien de dangereux à l'image ;
  · **les 30 photos** — c'est la vraie demande cachée : nos affiches n'ont
    toujours aucune photo à nous (vedette, ports, billet en main). Format
    d'origine, minimum 3000 px, **jamais par WhatsApp** qui divise la qualité
    par quatre ;
  · **les deux phrases de droits** (auteur + personnes) à archiver dans
    `CREDITS-PARTENAIRES.md` dès réception ;
  · **la fermeture est prise en compte** : la moitié des plans se tourne cette
    semaine, l'embarquement attend la reprise.
  ⏳ **En attente** : leur délai et leur budget.

- **12/08/2026 (🚨🚨 LES TRAVERSÉES SONT FERMÉES — le robot vendait des places
  qui n'existent pas)** — Le patron, en fin de journée : « les traversées sont
  fermées jusqu'à nouvel ordre, ouverture possible mardi », puis « à cause de la
  mer agitée ».
  🚨 **Pourquoi c'était urgent** : le robot de midi publie « réserve ta place »
  tous les jours, et le bulletin du soir finit par « RÉSERVE POUR DEMAIN ». Sans
  rien faire, on aurait promis pendant six jours un départ inexistant. Quelqu'un
  descend au port, il n'y a pas de vedette : ce client est perdu pour de bon, et
  dans un pays où tout le monde se connaît ça coûte plus cher que six mois de
  publicité.
  ✅ **Ce qui a été fait, et où ça vit :**
  - **`pub/flyers/service.py`** — la seule source de vérité sur « est-ce qu'on
    vend ? ». `OUVERT = False`, le dictionnaire `FERMETURE` (depuis, annonce
    mot pour mot, raison « mer agitée », date à revérifier), et deux fonctions
    qui servent le bulletin : `cta_bulletin()` et `conseil_bulletin()`.
    **Pour rouvrir : une seule ligne, `OUVERT = True`, puis pousser sur `main`.**
  - **`programme.py`** consulte `service.py` **avant** le calendrier et avant le
    garde-fou de la mer : fermé, aucun message commercial ne peut partir. À la
    place, l'avis de suspension — **une seule fois, le premier jour** (règle sans
    mémoire : on compare la date, le robot ne garde aucun état entre deux
    exécutions). `programme.py --avis` le republie à la main.
  - **`flyer31-suspension-fb.html` → `flyer-suspension-facebook.png`** : l'avis
    public, dans la famille bleu et blanc. **Aucune date dans l'image** : il
    resservira à la prochaine fermeture. Texte de publication dans `page.py`
    (`{depuis}` et `{raison}` remplis par `programme.py`).
  - **Le bulletin du soir continue** — informer n'est pas vendre, et c'est les
    jours sans traversée qu'un bulletin gratuit se remarque. Mais son bandeau
    d'or dit maintenant **« TRAVERSÉES SUSPENDUES »** (trois placeholders
    ajoutés au gabarit : `CTA_TITRE`, `CTA_ADR`, `CTA_WA`, servis par
    `service.py`), et le conseil de Douglas — qui suppose toujours qu'une
    vedette part — est remplacé par « Service suspendu : aucun départ prévu ».
  - **`verifier.js`** (nouveau) — le contrôleur de mise en page qu'on
    réinventait à chaque flyer : il compare les rectangles des blocs et signale
    chevauchements et débordements. `node verifier.js flyer31-suspension-fb.html`.
  📌 **Deux règles apprises, écrites dans le manuel :**
  1. **Ne jamais annoncer une date de reprise.** Le patron a dit « ouverture
     POSSIBLE mardi » : on écrit « peut-être mardi », jamais « ça reprend
     mardi ». Une date annoncée puis non tenue fait plus de mal que pas de date.
  2. **Ne jamais écrire « on ne te vend rien ».** Le patron : « on te vend rien,
     ça fait trop demander. » Nommer la vente la remet dans la tête du lecteur,
     et la phrase parle de nous au lieu de parler de lui. On écrit ce qu'il
     gagne (« tu le sais avant de descendre au port »). Corrigé sur l'avis de
     suspension **et** sur l'avis de grosse mer, image et texte.
  ✅ **Il a donné les deux accords le soir même** : « publie l'avis et aussi pour
  les Young Leader tu as le go. »
  - **L'avis est parti**, lancé à la main depuis le workflow (nouvelle case
    `avis_de_suspension` dans `publication-du-jour.yml`). ⚠️ Piège évité de
    justesse : `PUBLIER_FB` étant armé en permanence, l'étape « Publier »
    normale aurait envoyé le **même avis une deuxième fois** — d'où la condition
    `&& !inputs.avis_de_suspension`. À se rappeler pour toute future case de ce
    genre : deux étapes qui publient dans le même travail doivent s'exclure.
  - 🔍 **Trouvé dans le journal de ce lancement, et corrigé** : l'étape de
    diagnostic annonçait **« Publication DESARMEE »** dans les trois workflows,
    alors que tout partait. La variable `PUBLIER_FB` vaut **« Oui »** avec une
    majuscule : les conditions `if:` de GitHub ignorent la casse, mais le `bash`
    du voyant, non. C'est ce voyant qui m'a fait chercher au mauvais endroit
    quand le patron a signalé le poste de midi manquant. Normalisé en minuscules
    dans les trois fichiers. **Leçon : un voyant qui ment coûte plus cher que
    pas de voyant du tout** — vérifier ce qu'affiche un diagnostic avant de s'y
    fier, et ne jamais comparer une variable saisie à la main sans la normaliser.
  - 🔬 **« Y'a pas d'erreur ? vérifie jusqu'à mardi »** — d'où **`controle.py`** :
    il déroule chaque jour et chaque créneau jusqu'à la date demandée, sans rien
    publier, et vérifie que le visuel existe au bon format, que le texte n'a plus
    de trou `{...}`, qu'aucun mot commercial ne sort pendant la fermeture et
    qu'aucun interdit du manuel n'est écrit. `--ouvert` simule la réouverture.
    Résultat : **rien à signaler**, fermé comme ouvert.
    Ce contrôle a corrigé **quatre fausses alertes que j'aurais présentées comme
    des erreurs** — leçon plus utile que le résultat lui-même :
    · les PNG lourds ne sont pas un problème (`publier_fb.preparer()` repasse en
      JPEG 92) — le contrôle fait maintenant tourner l'allègement pour le prouver ;
    · `el.className` sur un `<svg>` renvoie un objet, pas une chaîne : aucun SVG
      décoratif n'était ignoré (le ruban doré du flyer de mardi, déjà validé) ;
    · un dessin qui déborde du cadre est normal (`overflow:hidden` le coupe) —
      seul du **texte** coupé compte ;
    · surtout : comparer des **boîtes** signale des croisements qui n'existent pas
      à l'œil. Le contrôleur compare désormais **les lignes de texte rendues**
      (Range.getClientRects), et distingue « deux textes se croisent » (défaut) de
      « une image passe derrière un texte » (souvent voulu). Vérifié ensuite en
      cassant volontairement un flyer : il voit toujours la vraie erreur.
    📌 **Un voyant qui crie au loup finit ignoré ; un voyant aveugle ne sert à
    rien.** Chaque nouveau contrôle doit être testé DANS LES DEUX SENS.
    ⚠️ **Trou trouvé et signalé au patron** : le jour de la réouverture, le robot
    publiera simplement la case du calendrier (« les prix », « l'île »). Il n'y a
    **pas de visuel de reprise**, alors que c'est la meilleure publication de la
    semaine à faire. À produire avant mardi.
  - **Young Leader autorisé.** `flyer30-partenariat` passe d'essai à visuel
    publiable ; la trace est dans `pub/photos-partenaires/CREDITS-PARTENAIRES.md`
    avec ses mots et la date. La phrase écrite du responsable **reste à
    obtenir** : elle ne bloque plus rien, elle protège. Il entre dans `page.py`
    et le **dimanche alterne** désormais institutionnel / partenariat — la
    deuxième variante du dimanche redevient légitime parce que les deux visuels
    sont du même système et du même registre (condition écrite dans
    `calendrier.py`). Corrigé au passage la seule ligne du visuel qui promettait
    une place (« votre place réservée à l'avance ») : elle parle maintenant de
    l'état du service, vrai même pendant la fermeture.

- **12/08/2026 (🚨 LE POSTE DE MIDI N'EST PAS PARTI — retard, pas panne)** — Le
  patron à 13h07 (Comores) : « le poste de midi n'est pas parti. »
  🔍 **Diagnostic** : aucune exécution **programmée** de `publication-du-jour` —
  que des lancements manuels de la veille. Les quatre workflows sont pourtant
  `active`, sur `main`, et le fichier est en place.
  💡 **La cause : GitHub exécute les crons « au mieux », et sature aux minutes
  rondes.** La preuve dans nos propres journaux : le bulletin du soir, programmé
  à **16h30 UTC**, s'est lancé à **17h26** — **56 minutes de retard**. Les
  minutes `:00` et `:30` sont celles où tout le monde programme.
  ✅ **Correctif appliqué aux trois workflows : minute creuse ET marge d'avance.**
  On ne programme plus à l'heure voulue, on programme **avant**, pour que le
  retard habituel (20 à 40 min) fasse tomber la publication à l'heure visée :
  | Robot | Avant | Après | Cible locale |
  |---|---|---|---|
  | Publication du jour | `30 9` (12h30) | **`7 9`** (12h07) | ~12h30 |
  | Bulletin du soir | `30 16` (19h30) | **`7 16`** (19h07) | ~19h30 |
  | Démonstration du matin | `30 4` (07h30) | **`7 4`** (07h07) | ~07h30 |
  ⚠️ **Conséquence à accepter et à dire au patron : un cron GitHub n'est pas une
  horloge.** Il peut arriver en retard, et il peut être **sauté** en cas de
  charge. Un rendez-vous « à la minute » ne peut pas reposer là-dessus. Si un
  jour la précision devient nécessaire, il faudra un déclencheur payant ou un
  petit serveur — pas un cron gratuit.
  ✅ **Publication du jour lancée à la main dans la foulée, et vérifiée dans le
  journal** — pas seulement le voyant vert :
  `Publié : 1166058113262206_122115123117374081`, `flyer-prix-facebook.png`
  (857 ko), texte de 926 caractères. **Page : 25 abonnés.**
  📌 **Réflexe à garder** : quand une publication manque, regarder d'abord s'il
  existe une exécution **`event: schedule`**. S'il n'y en a aucune, c'est le
  déclencheur, pas le code — inutile de chercher un bogue dans les scripts.
  🐛 Le rapport dit « 1 publication en 7 jours » : c'est le **défaut connu du
  journal** qui ne survit pas d'une exécution à l'autre, déjà consigné. À
  corriger, sinon tous les rapports resteront amnésiques.

- **12/08/2026 (NETTOYER ET AGRANDIR UNE PHOTO — et le mot juste)** — Le patron :
  « essaie de les décompresser et essaie un flyer. »
  ⚠️ **On ne « décompresse » pas une photo.** Ce que le JPEG a jeté est
  définitivement perdu, aucun programme ne le retrouve. Ce qu'on peut faire, et
  qui change vraiment le rendu : **effacer les artefacts**, **agrandir en
  Lanczos**, **remonter la netteté locale**. Le résultat est **plus propre,
  jamais plus détaillé**.
  ✅ **`pub/photos-partenaires/agrandir.py`** — et le point important : le
  débruitage est **dosé sur une mesure**, pas au hasard. Netteté = variance du
  laplacien ; artefacts = écart au filtre médian. Relevé sur les trois photos :
  | Photo | Reçue | Netteté | Artefacts | Débruitage appliqué |
  |---|---|---|---|---|
  | ocean-indien | 1280 × 1280 | 1896 | 5,13 | 5 (la plus abîmée) |
  | podium | 1080 × 856 | 1255 | 2,91 | 3 |
  | 2e-challenger | 854 × 1280 | 176 | 0,67 | 0 (nette mais douce) |
  Sortie ×2 : 2160 × 1712 pour le podium, 2560 × 2560 pour le portrait.
  💡 **Réglage appris** : masque flou à **1,35 / −0,35**, pas 1,55 / −0,55 — la
  première version créait des halos autour de la barbe. **Sur un visage, trop de
  netteté se voit plus qu'un léger flou.**
  🧪 **Essai livré : `flyer30-partenariat-fb.html` → `flyer-partenariat-facebook.png`**
  « Ceux qui font bouger l'île. » Registre institutionnel, vouvoiement, photo
  **tenue dans la carte claire** (famille bleu et blanc), crédit imprimé.
  ⛔ **NON BRANCHÉ dans `page.py` NI dans `calendrier.py`, volontairement** : le
  robot ne peut pas le publier par accident tant que la confirmation écrite sur
  le droit à l'image n'existe pas. **Ne pas l'y ajouter avant cet accord.**
  ✅ Vérifié : aucun chevauchement, rien hors cadre, et la photo est **nette à
  cette taille** (source 2160 px réduite dans un cadre de 900 px).

- **12/08/2026 (PREMIÈRES PHOTOS DE PARTENAIRE ARCHIVÉES)** — Le patron a envoyé
  **trois photos de Young Leader Mohéli** : « ils sont là, archive-les. » Fait,
  dans **`pub/photos-partenaires/`**, avec leur fiche de droits
  (`CREDITS-PARTENAIRES.md`) : ce qu'on voit, la taille, si des personnes sont
  identifiables, et si c'est utilisable.
  | Fichier | Sujet | Taille |
  |---|---|---|
  | `young-leader-ocean-indien-2025-2026.jpg` | lauréat, écharpe dorée Océan Indien | 1280 × 1280 |
  | `young-leader-2e-challenger-comores-2026.jpg` | lauréat, écharpe verte 2ᵉ challenger | 854 × 1280 |
  | `young-leader-moheli-podium-2025-2026.jpg` | les trois lauréats de Mohéli | 1080 × 856 |
  ⏸️ **AUCUNE N'EST PUBLIABLE POUR L'INSTANT** : les trois montrent des visages
  nets. Le contrat couvre le droit d'**auteur** ; il manque la confirmation écrite
  sur le droit à l'**image des personnes** (modèle de phrase dans la fiche). Poste
  « C » : le patron, jamais moi. **Ne pas céder à la tentation de publier « juste
  une fois ».**
  ⚠️ **Limite technique à retenir** : elles font 1080-1280 px, nos visuels 2160 px.
  Utilisables **dans un cadre jusqu'à ~600 px de large** (net), **jamais en fond
  plein cadre** (agrandissement 1,7× = flou visible). Demander les **fichiers
  d'origine** à l'association : ceux-là ont déjà été recompressés par les réseaux.
  💡 **Recommandation écrite dans la fiche** : ces portraits servent la **preuve
  sociale** (visuel de partenariat, registre institutionnel du dimanche), pas la
  vente. Ce qui vend une traversée, ce sont les photos du **produit et du
  terrain** : la vedette, les ports d'Ouroveni et Hoani, un billet dans une main.
  **Un portrait dit « on est sérieux » ; une vedette au port dit « ta place
  existe ». Deux registres, on ne les mélange pas.**

- **12/08/2026 (L'ÉCRAN RÉEL DE L'APPLICATION SUR LES VISUELS)** — « Tu peux
  mettre l'accueil MoheliGo sur l'écran ? » Oui, et **sans rien dessiner**.
  🎉 **Découverte importante : le site TOURNE en local depuis le dépôt.** Il
  suffit de le servir (`python3 -m http.server 8899` depuis `moheligo/`) et de
  l'ouvrir avec Chromium sur `127.0.0.1` — le navigateur n'a pas de réseau
  extérieur, mais **localhost n'en a pas besoin**. L'application affiche son
  accueil, ses cartes et **ses vrais ports**.
  ✅ `pub/flyers/capture_accueil.js` → `ecran-accueil.png` (1170 × 2400) puis
  `flyer29-telephone-fb.html` → `flyer-telephone-facebook.png` : l'écran est posé
  dans un téléphone dessiné en CSS. **Un cadre n'est pas une fausse preuve ; un
  écran inventé, si.** Départ **Ouroveni → Hoani** comme demandé par le patron.
  🐛 **Trois pièges payés dans cette capture, tous consignés dans le script :**
  ① **les ports arrivent APRÈS le chargement** — une attente fixe de 6 s
  sélectionnait le port par défaut, puis la liste se remplissait juste avant la
  photo : le patron a vu Chindini alors qu'on demandait Ouroveni. Solution :
  `waitForFunction` sur la présence des options, puis `selectOption({label})` de
  Playwright, qui attend et réessaie tout seul.
  ② **l'écran de BIENVENUE se pose en dernier** (« Bienvenue sur MoheliGo »,
  bouton « Passer ») : trop tôt on capture l'accueil, plus tard on capture la
  bienvenue. Solution propre : poser **`localStorage.mg_ob_done = '1'`** avant le
  chargement (`addInitScript`) — la clé que l'application utilise elle-même.
  **Leçon : chercher le drapeau que le produit pose déjà, plutôt que de lutter
  contre son interface.**
  ③ **mon garde-fou testait la PRÉSENCE du texte, pas sa VISIBILITÉ** : le bloc
  de bienvenue existe toujours dans le HTML, donc il était « trouvé » même caché
  et refusait toutes les captures. **Un test de visibilité regarde
  `offsetParent`, la taille, `visibility` et `opacity`.**
  ✅ Le script **relit ce qu'il va photographier** et échoue si le départ affiché
  n'est pas celui demandé, ou si ce n'est pas l'accueil. Une capture qui montre le
  mauvais port est pire qu'une capture absente.
  ⚙️ Deux retouches cosmétiques assumées et écrites dans le script : la date est
  renseignée à demain (sinon « mm/dd/yyyy » fait croire à un formulaire cassé) et
  les bulles flottantes sont masquées car elles recouvrent la carte. **Aucun
  départ, aucun prix, aucun horaire inventé.**

- **12/08/2026 (PHOTOS : CE QUI EST POSSIBLE ET CE QUI NE L'EST PAS)** — Le
  patron : « prends les photos de **Young Leader Mohéli** sur Facebook et
  Instagram, on a un contrat avec eux » et « trouve des photos sans droit
  d'auteur sur Pinterest ».
  ❌ **Je ne peux pas récupérer une image sur Facebook ni Instagram** : le
  navigateur de la session n'a aucun accès réseau, et ces pages exigent une
  connexion. **Et même avec le réseau, il ne faudrait pas** : les réseaux
  sociaux recompressent à ~1080 px avec des artefacts, alors que nos visuels
  sortent en 2160 px — une photo reprise d'un fil se voit sur une affiche.
  ➡️ Il faut les **fichiers d'origine**, demandés à Young Leader Mohéli.
  🚨 **Pinterest n'est PAS une source d'images libres** : c'est un répertoire
  d'images prises partout sur le web, quasi toutes protégées. Une réclamation
  peut faire **retirer une publication Facebook**. Les vraies sources sont
  **Pexels, Unsplash, Pixabay** (usage commercial, sans attribution) et
  **Wikimedia Commons** (attribution obligatoire en CC BY). Aucune n'a de photos
  de Mohéli : pour Mohéli il n'y a que Wikimedia (rare) et nous.
  ⚖️ **Distinction à ne pas confondre** : le contrat règle le droit d'**auteur**
  (celui du photographe). Le droit à l'**image des personnes** est une autre
  question — une association obtient souvent l'accord pour SA communication, pas
  automatiquement pour la publicité d'une entreprise partenaire. D'où la phrase
  écrite à obtenir une fois (modèle dans `pub/photos-partenaires/README.md`).
  **Tant qu'elle n'existe pas : uniquement des photos où personne n'est
  identifiable.** C'est un poste « C » (juridique) — jamais moi.
  📁 Zone de dépôt créée : **`pub/photos-partenaires/`**, avec le mode d'emploi,
  la liste des vérifications et ce que je fais dès que les fichiers arrivent.

- **12/08/2026 (LE BULLETIN DU SOIR PASSE EN BLEU ET BLANC)** — Le patron :
  « je l'ai approuvé parce que je ne savais pas que tu pouvais faire d'aussi
  beaux flyers ; **un beau flyer attire l'attention**. »
  🎓 **Leçon sur moi-même, pas sur le design : une approbation obtenue quand le
  client ne savait pas ce qui était possible n'est pas une validation, c'est un
  plafond.** Je ne dois pas m'abriter derrière un « il a déjà dit oui » — c'est
  à moi de proposer mieux quand je sais faire mieux.
  ✅ **`flyer8-soir-fb.template.html` réécrit dans la famille** : coin blanc,
  aplat marine, carte claire, bandeau d'or avec QR. **Plus de photo de fond** —
  l'objet regardé est désormais **la donnée elle-même**, qui est notre seul actif
  incopiable. Le verdict est l'accroche (« Demain matin, MER AGITÉE. »).
  🔒 **Aucun script ni workflow touché** : les **dix-huit valeurs** du gabarit
  gardent exactement leurs noms (OVER, TITRE_BULLETIN, ETAT, CONSEIL, HOULE,
  VENT, DIRV, PERIODE, AMPLI, AMPLI_LAB, PLAGE, COURBE, AIRE, POINTS, HEURES,
  GAUGE, GAUGE_LAB, MAJ). L'ancien gabarit est gardé sous
  `flyer8-soir-v1.template.html` — on ne jette pas ce qui a servi.
  🧪 **Vérifié de bout en bout, comme à 19h30** : `bulletin.py` a interrogé
  Open-Meteo (jeudi 13/08 : mer agitée, houle 1,31 m, vent 27 km/h de sud,
  période 7,5 s), rempli le gabarit, et le rendu est propre. **Zéro `{{` restant**
  dans le HTML produit. Et le poids tombe de **2 656 ko à 945 ko** — la photo de
  fond coûtait 1,7 Mo pour rien.
  🐛 **Piège trouvé et corrigé : le gabarit se remplissait lui-même.** Les noms
  des valeurs étaient cités **avec leurs doubles accolades dans le commentaire**
  d'en-tête, donc `bulletin.py` remplaçait aussi la documentation, qui se
  retrouvait pleine de chiffres du jour. **Règle : dans un gabarit, ne jamais
  écrire un nom de valeur avec ses accolades ailleurs que là où il doit être
  remplacé.**

- **12/08/2026 (LA SEMAINE ENTIÈRE DANS LE ROBOT)** — « Fais tous les flyers
  jusqu'à mardi, mets-les dans le robot, car la limite de la semaine sera
  bientôt atteinte. » Fait : **la semaine complète tourne sans moi.**
  Cinq visuels neufs, tous dans la même famille (coin blanc en biais, aplat
  marine, carte claire, bandeau d'or, QR vérifié) :

  | Jour | Visuel | L'objet regardé, et l'idée unique |
  |---|---|---|
  | lundi | `flyer28-rien-installer` | la **barre d'adresse** — répond à « mon téléphone est plein » |
  | mardi | `flyer17-signature` (déjà validé) | « On se voit de l'autre côté » — le registre émotion |
  | mercredi | `flyer20-prix` | le **billet** — le prix connu avant de payer |
  | jeudi | `flyer24-abonner` | les **sept soirs** — seule demande de la semaine qui n'est pas « réserve » |
  | vendredi | `flyer25-diaspora` | les **deux côtés de la mer** — tu paies d'ici, elle embarque là-bas |
  | samedi | `flyer26-destination` | la **photo tenue dans la carte** (Nioumachoua, crédit imprimé) |
  | dimanche | `flyer27-institutionnel` | le **tableau des liaisons** — registre partenaires, vouvoiement |

  🎯 **Correction du patron en cours de route** : la première version du samedi
  était une photo plein cadre. « Fais le même type que ce que tu viens de faire,
  c'est joli le type bleu et blanc. » → la photo est passée **dans la carte
  claire**, comme le billet du mercredi. **Leçon : la famille avant l'effet.**
  Un visuel qui sort du système abîme la marque plus qu'il ne l'embellit.

  🚨 **PIÈGE ÉVITÉ, à ne pas réintroduire : la rotation tirait dans l'ANCIENNE
  bibliothèque.** `SEMAINE` avait deux variantes par jour et choisissait selon le
  numéro de semaine ISO ; en semaine 33 le tirage tombait sur les visuels
  d'avant le système (pas de coin blanc, pas de QR). **La rotation est
  supprimée : une seule variante par jour.** Elle reviendra quand la bibliothèque
  aura grandi *dans* le système. Publier hors système une semaine sur deux coûte
  plus cher que l'usure.

  🔍 **Contrôles passés avant de pousser** (à refaire à chaque nouvelle série) :
  ① un détecteur de **chevauchements et de débordements** sur les huit visuels —
  il a trouvé trois vrais défauts : accroche sur trois lignes qui recouvrait la
  ligne suivante (dimanche et lundi), et la carte d'avis qui mordait de 6 px sur
  le texte du visuel de **grosse mer** ; ② simulation de `du_jour()` du 12 au
  18/08 : fichier présent, poids sous la limite, aucun texte à trous.
  💡 **Règle de largeur d'accroche** apprise ici : en Archivo 900, compter
  **≈ 0,47 × taille de police par caractère**. Au-delà de 940 px, la ligne casse
  et le bloc suivant est recouvert. Vérifier AVANT de rendre, pas après.

- **12/08/2026 (LE DOSSIER, ET LA V2 DU MODE D'EMPLOI)** —
  📁 **« Écris tout dans un dossier comme le manuel que tu vas consulter. »**
  Fait : `moheligo/dossier/` regroupe les **huit documents de référence**
  (déplacés avec `git mv`, historique conservé), et **`dossier/README.md` est
  l'index** : il dit quoi lire avant quoi selon le travail, ce qui n'est
  volontairement PAS dans le dossier (tout ce qui est **généré** reste à côté du
  programme, sinon on corrige la copie au lieu de la source), et **l'état du
  système** avec ses interrupteurs. `CLAUDE.md` pointe désormais sur le dossier :
  c'est ce qui fait qu'il sera lu et pas seulement rangé. Tous les chemins ont
  été corrigés dans le code, les workflows et les messages d'erreur.
  `manuel_page.py --dossier` assemble tout le dossier en une seule page lisible.

  🎯 **Revue du patron sur le mode d'emploi : 8,7/10, et la phrase à retenir** —
  « je ne veux pas simplement un flyer plus beau, je veux un flyer qui convertit
  davantage ». J'avais optimisé la **compréhension**, pas l'**action**.
  → **Manuel § 10 quater** (nouveau) : la règle des 3 secondes, les six
  corrections avec leur leçon réutilisable, et les ajouts à la checklist FLYER.
  Les trois plus utiles pour la suite :
  ① **relire chaque mot fort comme un malveillant** — « ta place est *prise* »
  pouvait se lire « déjà prise par un autre », l'inverse du message ;
  ② **ne jamais rassurer par la négative** — « personne ne fait ça seul »
  installait le doute qu'il prétendait lever, remplacé par « Besoin d'aide ? On
  est là. » ;
  ③ **un support sans geste faisable tout de suite n'est pas un support de
  vente** — d'où le QR.
  ✅ **`flyer23-modedemploi-v2-fb.html` → `flyer-modedemploi-v2-facebook.png`** :
  slogan « ta place est **réservée** », une ligne par étape (textes secondaires
  −40 %), bandeau d'or avec **QR 200 px + « SCANNE ET RÉSERVE »**,
  `moheligo.com` de 29 à 57 px, MVola et KartaPay en pastilles.
  C'est **elle** qui publie désormais (calendrier du matin) ; la **V1 est gardée**
  dans la bibliothèque pour le test terrain papier, le patron l'ayant jugée
  utilisable telle quelle.

  🚨 **`qr.py` (nouveau) — un QR ne se publie jamais sans être décodé.** Un QR
  est illisible pour un humain : s'il pointe ailleurs, personne ne s'en aperçoit
  avant cent affiches imprimées. Le script **génère** depuis une adresse écrite
  en clair, puis **relit et décode** le PNG produit, et **sort en erreur** si
  l'adresse lue n'est pas la bonne. Correction d'erreur **Q** (25 % du code peut
  être abîmé) pour une affiche exposée dehors.
  ⚠️ **Piège technique payé** : `pyzbar` a besoin de la bibliothèque système
  `zbar`, absente ici et impossible à installer (dépôts incomplets). La
  vérification serait restée annoncée mais jamais faite. Solution :
  **OpenCV** (`pip install opencv-python-headless`), qui embarque son propre
  décodeur dans la roue Python. Vérifié : le QR décode bien
  `https://moheligo.com/`.

- **11/08/2026 (🚨 L'INFORMATION PRODUIT LA PLUS IMPORTANTE DE LA SESSION)** —
  Le patron : « le départ tkt pas, mais **en mauvais temps les vedettes ne
  partent pas**. » Les départs sont donc fiables, sauf par grosse mer.
  🎯 **Ce n'est pas une faiblesse, c'est notre produit** : le seul événement qui
  annule une traversée est **exactement celui que nous sommes seuls à publier**.
  ➡️ **Positionnement corrigé au manuel § 2**, et c'est la formulation à tenir
  partout désormais :
  > **La mer décide. Nous, on te le dit avant.**
  On ne promet **jamais** qu'une vedette partira — ça ne dépend pas de nous. On
  promet de savoir avant de quitter la maison. Plus modeste, toujours vrai.
  ✅ **Garde-fou automatique livré** (et vérifié de bout en bout) :
  - `mer.py` — l'état de la mer d'un jour donné (Open-Meteo Marine, fenêtre
    6h-10h, échelle de Douglas de `bulletin.py`). Seuil **`SEUIL_GROS_TEMPS = 3`**
    = MER FORTE, houle ≥ 2,50 m, le degré où le bulletin dit déjà « vérifiez le
    maintien des départs ». `gros_temps()` renvoie **True / False / None** —
    et **None veut dire « je ne sais pas », pas « beau temps »**.
  - `programme.py` le consulte **avant chaque publication** : mer forte →
    le message commercial est remplacé par l'**avis de mer**
    (`flyer22-grostemps-fb.html` → `flyer-grostemps-facebook.png`), **zéro appel
    à l'action**, avec l'état et la houle réels injectés dans le texte
    (`{etat}` / `{houle}` remplis depuis `mer.niveau()`).
  - **Choix assumé quand la météo est injoignable (None) : on publie quand même**
    et on écrit l'avertissement dans le journal. Nos textes ne promettent jamais
    qu'une vedette partira, et se taire à chaque hoquet d'Open-Meteo ferait des
    trous dans la régularité — notre seul vrai actif.
  - **Anti-doublon sans mémoire** : un jour de mer forte, l'avis part **le matin**
    quand un créneau du matin existe (lundi, jeudi), et **midi se tait** ; les
    autres jours, midi le publie. Décidé par le calendrier seul, aucun état à
    conserver — testé sur lundi 17/08 (matin oui, midi non) et mardi 18/08
    (midi oui, matin rien).
  - Interdictions ajoutées au § 11 : ne jamais écrire « les vedettes ne partent
    pas » (on ne connaît pas le seuil d'annulation de chaque compagnie → « **peuvent**
    ne pas partir »), ne jamais promettre qu'une traversée partira.
  🐛 **DÉFAUT CONNU, À CORRIGER — le journal des publications ne survit pas.**
  `journal-publications.json` est écrit dans le dossier de travail du serveur
  GitHub, qui est **détruit à la fin de chaque exécution**, et le fichier n'est
  **pas suivi par git**. Conséquence : `rapport.py` ne verra jamais l'historique
  des publications, seulement celle du jour. Correctif à faire : le pousser sur
  une branche orpheline comme le bulletin (`bulletin-du-jour`), en le relisant
  avant d'y ajouter une ligne. **Tant que ce n'est pas fait, les rapports
  hebdomadaires sont amnésiques** — à dire au patron dans le premier rapport.
  ❓ **Question B en attente (décision du patron)** : si une traversée est annulée
  pour cause de mer, le client est-il **remboursé intégralement, frais de
  transaction compris**, ou bien changement de date gratuit ? Aujourd'hui le site
  dit « remboursé moins les frais » — c'est correct pour une annulation
  volontaire, mais **injuste si c'est la mer qui annule**. Prendre en charge les
  frais ces jours-là coûterait très peu et vaut mieux que dix publicités.

- **11/08/2026 (NOUVEAU MANDAT + FEUILLE DE ROUTE)** — 🚨 **Décision
  d'organisation du patron** : « je te nomme sur tous les autres postes, moi je
  suis CEO et service client, ça te va ? tu dois me conseiller aussi. »
  **Accepté**, avec mes limites écrites — accepter dix postes sans les dire
  serait la faute reprochée à Theranos au § 14.2 du manuel.
  → Répartition, limites et **règle de décision A / B / C** consignées au manuel,
  **§ 12.2, 12.2 bis et 12.2 ter**. À relire avant de décider quoi que ce soit.
  - **A — je décide et je fais** : visuels, textes, rapports, code, priorités,
    calendrier de publication.
  - **B — je propose, il tranche** : prix, partenariats, dépenses, nouvelle
    ligne, tout ce qui change la promesse au client, tout nouveau canal.
    **En cas de doute entre A et B, c'est B.**
  - **C — jamais moi** : sécurité des passagers, juridique et conformité ANACM,
    argent, embauches, données personnelles d'un client réel.
  - Mes limites réelles, à ne pas oublier : aucun souvenir entre sessions (d'où
    ce fichier), aucune existence entre sessions (d'où les robots), aucune
    réponse à un client à 6 h, aucune valeur légale, aucun accès à l'argent, et
    **je peux me tromper avec assurance** (d'où les sources citées et les
    checklists).
  - Le service client reste au patron : **c'est le bon choix** — c'est là qu'est
    la vérité du produit et le premier détecteur de friction.
  🗺️ **`FEUILLE-DE-ROUTE.md` (nouveau)** — réponse à « dans combien de temps ça
  va se faire ? ». Position tenue : **le produit est fait, c'est l'habitude qui
  n'est pas faite**, et je refuse de donner une date sans chiffres.
  - **Étape 1, 6 semaines : la PREUVE** — 10 traversées payées par des inconnus,
    30 vraies conversations. Seuil : **0 réservation après six semaines de
    présence quotidienne → on arrête de publier plus et on descend au port**, le
    problème n'est pas la publicité (erreur de Webvan).
  - **Étape 2, 2 à 4 mois : l'HABITUDE** — une réservation par jour, premiers
    clients qui reviennent. Signal de bascule à guetter : **les questions passent
    de « c'est fiable ? » à « il y a une place samedi ? »**.
  - **Étape 3, 6 à 12 mois : la NORMALITÉ** — compressible à 4-6 mois avec un
    budget, **mais seulement après l'étape 1**.
  - Risques nommés : le patron seul sur cinq postes (le plus grave), **la
    fiabilité réelle des départs** (notre promesse est « prévisible » — elle
    dépend des compagnies, pas de nous), les trois chiffres manquants, le jeton
    Facebook qui expire vers le 10/10/2026.
  📌 **Question posée au patron et restée ouverte : les départs sont-ils
  réellement fiables aujourd'hui ?** Si les vedettes ne partent pas comme
  annoncé, aucune publicité ne rattrape ça — et c'est le seul point qui peut
  invalider tout le positionnement.

- **11/08/2026 (LE CRÉNEAU DU MATIN — démonstration)** — « On peut pas ajouter un
  flyer ou vidéo de démonstration le matin ? » Oui pour le flyer, **non pour la
  vidéo ce soir** — et la raison est technique, pas une excuse :
  🚨 **Chromium n'a AUCUN accès réseau dans la session** (`ERR_CONNECTION_RESET`,
  testé avec mandataire, sans mandataire, et sur un autre domaine ; `curl` passe,
  le navigateur non). Et le site **ne tourne pas en local** : il charge ses
  départs depuis **Supabase** et son client depuis un **CDN**. Donc ni
  enregistrement du site en ligne, ni exécution locale. J'ai **refusé de
  dessiner une fausse interface** : montrer un écran qui n'existe pas, c'est
  inventer une preuve (§ 11 du manuel), et ça se voit.
  ✅ **Livré à la place** : `flyer21-modedemploi-fb.html` →
  `flyer-modedemploi-facebook.png`, « En trois gestes, ta place est prise ».
  Même famille que le flyer des prix (coin blanc, aplat marine, carte claire) —
  la régularité bat la créativité. L'objet regardé est **la marche à suivre** :
  trois pastilles reliées par un fil doré. Tous les faits viennent du site.
  💡 **Astuce CSS à réutiliser** : pour relier des pastilles par un fil continu,
  ne pas placer un trait absolu sur toute la carte (il dépasse et il faut le
  recalculer à chaque changement de texte). Comme chaque pastille a son centre à
  **64 px du haut de sa rangée**, la distance entre deux centres vaut exactement
  la hauteur de la rangée : `.etape:not(:last-child)::before { top:64px;
  height:100% }` relie un centre au suivant **quel que soit le texte**.
  ⏰ **Le rythme, et pourquoi il est prudent** : **lundi et jeudi 7h30**
  seulement (`.github/workflows/publication-du-matin.yml`, cron `30 4 * * 1,4`).
  Publier trois fois par jour sur une page jeune **ne multiplie pas la portée,
  ça la divise** entre les publications, et ça fatigue les abonnés — or un
  désabonnement se récupère bien plus difficilement qu'une portée faible. Donc
  deux matins, on mesure dans le rapport du dimanche, on décide avec les
  chiffres.
  🔌 **Interrupteur séparé : `PUBLIER_MATIN = oui`** — volontairement distinct de
  `PUBLIER_FB`, pour que le patron puisse garder midi et le soir armés tout en
  laissant le matin à l'essai. **Le créneau est DÉSARMÉ jusqu'à sa décision.**
  `PAUSE_FB` reste au-dessus de tout.
  🧠 Détail de conception : un matin sans démonstration prévue **n'est pas une
  erreur** — `programme.py --matin` sort proprement en code 0. Un voyant rouge
  cinq matins sur sept, on apprend à l'ignorer, et il ne sert plus le jour où il
  compte.
  🎬 **La vidéo attend 4 captures d'écran du patron** (accueil / carte de
  réservation remplie / liste des traversées / **billet avec son QR**, données
  personnelles masquées) → `dossier/VIDEO-DEMONSTRATION.md` dit exactement quoi envoyer et ce
  que j'en ferai. L'encodage est déjà prêt (`pip install imageio-ffmpeg` fournit
  un ffmpeg 7.0.2 autonome) et `pub/demo/capture_site.js` est écrit — il ne lui
  manque que le réseau. ⚠️ Publier une vidéo demandera d'ajouter le point
  d'entrée `/{page}/videos` à `publier_fb.py` (les photos passent par
  `/{page}/photos`) : à faire **le jour où les captures arrivent**, pas avant —
  du code qui attend n'a jamais été testé.

- **11/08/2026 (PARTIE II DU MANUEL — diriger, faire adopter, les erreurs des
  fondateurs)** — Commande du patron : « ajoute comment gérer une compagnie, les
  gros conglomérats et tous les postes ; comment rendre un produit utilisable
  même si le client n'a pas envie ; regarde les histoires des fondateurs de la
  Silicon Valley et ajoute leurs erreurs ; puis donne-moi une copie pour que je
  puisse lire. » Fait, **avec recherche** (pas de mémoire seule) :
  `MANUEL-MARKETING.md` passe de 377 à ~790 lignes, sections **12 à 16**.
  - **§ 12 Diriger** — Sloan (« réconcilier centralisation et décentralisation » :
    liberté d'exécution en bas, contrôle financier en haut) ; Grove (fonctionnel
    contre divisionnaire, toute organisation qui grandit devient hybride) ; le
    **tableau des 13 postes** avec, pour chacun, ce qu'il possède et **le chiffre
    dont il répond** ; l'état réel de MoheliGo (le patron tient cinq postes, moi
    trois, et les **données sont le trou**) ; les rituels ; Sloan qui refusait de
    valider une décision non contestée → **je dois livrer l'objection contre mon
    propre plan** ; Startup Genome (**70 %** grandissent trop tôt, **74 %** des
    échecs à forte croissance) → le prochain poste à ouvrir est **celui qui est
    saturé**, soit la relation client et les revendeurs de proximité.
  - **§ 13 Faire adopter** — **B = MAP** (Fogg, Stanford) : comportement =
    motivation × capacité × déclencheur, et le résultat décisif — **enlever la
    friction est plus rapide et plus durable que d'augmenter l'envie** ; les trois
    types de déclencheurs (étincelle / facilitateur / signal) et l'erreur de
    donner une étincelle à quelqu'un qui est motivé mais bloqué ; **la leçon
    M-Pesa** : le réseau d'agents humains vaut autant que la technologie, on
    utilise **les commerces qui existent déjà**, la confiance est le vrai produit,
    ne pas ériger de nouvelle barrière → **notre réseau d'agents, ce sont les
    boutiquiers, hôteliers et chauffeurs, comme points de vente assistés** ;
    l'audit de friction par les six leviers ; les trois règles d'or (la première
    fois se fait accompagné / ne jamais dire « c'est simple » / rendre l'échec
    réversible).
  - **§ 14 Les fondateurs et leurs erreurs** — les données CB Insights (70 %
    « plus d'argent » = **symptôme**, 43 % pas de marché, 29 % mauvais moment,
    19 % économie unitaire) puis cinq cas : **General Magic** (le smartphone 15
    ans trop tôt ; leçon de Fadell : avancer par versions, pas par un grand
    saut), **Webvan** (26 villes d'un coup, 830 M$ brûlés, ils ont cessé de
    regarder les données → nos **paliers** et notre **seuil d'arrêt**),
    **Better Place** (836 M$, une technologie en quête de problème → chaque
    nouveauté doit répondre à **une phrase entendue au port**), **Quibi**
    (1,75 Md$, six mois, le contexte a annulé l'idée → c'est la raison d'être du
    frein `PAUSE_FB`), **Theranos / WeWork / Enron** (annoncer et espérer que la
    réalité suive → dans un pays où tout le monde se connaît, une promesse non
    tenue coûte plus cher qu'une pub jamais publiée). Contre-exemple **Airbnb** :
    « mieux vaut 100 clients qui vous aiment qu'un million qui vous aiment à peu
    près » → tournée des ports, boutiquiers formés un par un.
  - **§ 15** bibliothèque enrichie (livres **et documentaires** : General Magic,
    The Inventor, WeWork, Enron) avec **où j'ai vérifié**, et l'aveu de méthode :
    je n'ai pas lu ces livres cette nuit, j'ai vérifié faits et chiffres.
  - **§ 16** checklists de décision : avant d'ouvrir un poste, avant d'ajouter
    une étape produit, avant de présenter un plan.
  📖 **Copie lisible pour le patron** (générée, jamais recopiée) :
  `pub/flyers/manuel_page.py` convertit le manuel en page web soignée avec
  sommaire, tableaux qui défilent sur téléphone et thème clair/sombre :
  `python3 manuel_page.py --sortie /tmp/manuel.html`. **Règle : ne jamais
  corriger cette page à la main — corriger le manuel, puis regénérer**, sinon les
  deux versions divergent et je relis un manuel périmé avant une pub.
  Adresse publiée : https://claude.ai/code/artifact/bf9196e3-8a00-414d-82ee-eb2333cda23f
  📌 Le patron **enverra ses images demain (12/08)** → à ce moment-là, passer en
  **sortie A** du § 10 bis (vraie matière : découpe, ombre portée, composition).

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
  ✅ Le patron a validé (« c'est joli, publie-le demain ») et **autorisé
  l'avancée de `main`**.
  🚨 **PIÈGE À NE PLUS JAMAIS OUBLIER — le robot ne voit que `main`.** Un
  workflow déclenché par `schedule` est lancé par GitHub **sur la branche par
  défaut**, et `actions/checkout@v4` sans `ref` télécharge donc **`main`**, pas
  la branche de travail. Un visuel commité seulement sur ma branche
  **n'existe pas** pour la publication de 12h30 : le calendrier retomberait sur
  l'ancienne variante. **Règle : après validation d'un visuel qui doit partir
  automatiquement, vérifier que `main` le contient**
  (`git ls-tree origin/main <fichier>` et `git show origin/main:.../calendrier.py`).
  Avancer `main` demande l'accord explicite du patron — il l'a donné ce soir.
  ✅ Vérifié après l'avancée : `du_jour(2026-08-12)` renvoie bien
  `flyer-prix-facebook.png` (858 ko, sous la limite de 3,5 Mo, donc aucun
  ré-encodage) et le texte « LE PRIX, TU LE CONNAIS AVANT DE PAYER. »

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
  **`dossier/LIER-FACEBOOK.md`** (marche à suivre complète pour le patron).
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
  d'utilisateurs. » Écrit dans `dossier/PLAN-PUBLICITAIRE.md`. La thèse du plan :
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
  `dossier/TEXTES-PUBLICATIONS.md`.

- **09/08/2026** — « Dépasse-toi encore, ça doit être lumineux. » L'affiche a
  été refaite en version claire : rampe duotone qui ne descend jamais dans le
  noir, **voile clair sur les bords au lieu d'un vignettage sombre** (le geste
  qui change tout), bloom généreux, et le **sceau devenu soleil** avec un
  éventail de rayons en dégradé conique. La typo passe en **marine sur fond
  clair** — la lumière vient du contraste, pas de l'ajout de blanc.
  ⚠️ Premier essai trop délavé : les îlots avaient disparu. Réglages retenus :
  voile 140, contraste 1,22, gamma 0,88. Recette complète dans
  `dossier/ATELIER-FLYERS.md`, section « Faire une affiche LUMINEUSE ».
  La page du patron montre maintenant cette affiche à la place de la sombre
  (la sombre reste dans le dépôt).
  Retour immédiat : **« trop lumineux »**. Réglage final : voile de bord 74 au
  lieu de 140, contraste 1,30, gamma 0,96, ombres de la rampe plus profondes,
  et voile crème du bas remonté pour garder le texte marine lisible sur le
  sable. **À retenir : « lumineux » ne veut pas dire « pâle » — la lumière tient
  à la présence des ombres autant qu'à celle des hautes lumières.**
  Ajouté le même jour, sur sa demande : **trois textes seuls** (faire s'abonner
  à la page, faire utiliser l'application, variante courte de l'affiche), dans
  `page.py` (liste `TEXTES`) et dans `dossier/TEXTES-PUBLICATIONS.md`.
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
  ajouté dans `dossier/TEXTES-PUBLICATIONS.md` (version institutionnelle + premier
  commentaire avec le lien + version courte + réponses types aux commentaires).
  Documentation dans `dossier/ATELIER-FLYERS.md`. **À faire à la prochaine session :
  demander au patron s'il valide le ton institutionnel ou s'il veut plus chaud
  / plus commercial, et s'il veut une version shikomori.**
  Il a ensuite demandé **un deuxième support pour plus tard dans la nuit** :
  produit le flyer nuit (ciel étoilé, lune, silhouette des îles) avec un angle
  action — « Réservez ce soir. Partez demain. » — et un encart diaspora
  (France, Mayotte, Golfe : payer la traversée d'un proche). Texte FB nuit dans
  `dossier/TEXTES-PUBLICATIONS.md`. **Leçon de calendrier : ne pas republier la même
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
