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

- **02/09/2026 (🔬 « TU PEUX LES RENDRE CLAIRES, ESSAYE » — et l'outil évident
  n'était pas le bon)** — `affiner.py` : débruitage AVANT l'agrandissement, puis
  **rétroprojection itérative**, puis un accentuage faible guidé par les
  contours. Mesuré sur les sept photos à taille de sortie identique :
  **l'acutance des contours DOUBLE**, et sur les deux plus compressées le bruit
  **baisse** en même temps. Vérifié à l'œil.

  ⛔ **LE RÉSULTAT A CONTREDIT MON INTUITION, ET C'EST LE PLUS UTILE.** Sur la
  photo la plus difficile :
  · Lanczos seul → acutance 226, bruit 0,65
  · **rétroprojection SEULE → 388, bruit 0,40**
  · + accentuage 0,30 → 433
  · + accentuage 0,85 → 504, mais **granuleux à l'œil**
  L'accentuage — l'outil qui porte le nom du problème — apporte le moins. La
  rétroprojection seule gagne +72 % AVEC MOINS DE BRUIT, parce qu'elle
  n'invente rien : elle impose que le résultat, réduit à 720 px, redonne
  l'original. C'est une contrainte de fidélité, pas un maquillage.
  📌 **L'OUTIL QUI PORTE LE NOM DU PROBLÈME N'EST PRESQUE JAMAIS CELUI QUI LE
  RÉSOUT.**
  📌 Et à 0,85 les chiffres montaient encore alors que l'image devenait laide :
  **le chiffre ne décide pas seul.**

  ⛔ **UNE ERREUR DE MESURE, RATTRAPÉE AVANT DE LA RAPPORTER.** J'ai d'abord
  relancé le diagnostic « détail fin » sur les images DÉJÀ AGRANDIES : il
  annonçait des scores deux fois meilleurs, et j'ai failli annoncer que quatre
  photos passaient d'une catégorie à l'autre. C'était faux — le détail fin se
  compte par pixel, tripler les pixels le divise mécaniquement. Seule l'échelle
  avait changé.
  📌 **UN SEUIL CALIBRÉ À UNE ÉCHELLE NE VEUT PLUS RIEN DIRE À UNE AUTRE.**
  Deuxième fois dans la journée qu'un indicateur donne une réponse fausse avec
  aplomb (après les 97,8 % / 97,7 %). Les deux fois, ce qui a sauvé, c'est
  d'avoir regardé l'image.

- **02/09/2026 (🏆 LE GABARIT DE RÉFÉRENCE, et le test du logo caché)** — le
  patron envoie sept photos de plages : « c'est pour les flyers ; nos flyers
  hors bulletin doivent contenir une photo. Sois très original et clair mais
  très simple, et **directement reconnaissable sans logo**. Du 10/10 : on doit
  comprendre que MoheliGo n'est pas une petite boîte mais un grand parmi les
  grands du monde. »

  ⛔ **SA QUESTION EST LA SEULE QUI COMPTE, ET ON NE SE L'ÉTAIT JAMAIS POSÉE :
  si on cache le logo, à quoi reconnaît-on que c'est nous ?** Jusqu'ici la
  réponse était « au coin blanc » — c'est-à-dire au logo. Donc à rien. **Un
  visuel qui a besoin de sa signature pour être identifié n'a pas d'identité, il
  a une étiquette.**
  ✅ **La réponse : la vague d'or.** Elle était en bas de page, 74 px, en
  décoration. Dans `flyer48` elle devient la COUTURE entre la mer et les mots.
  📌 **Une marque se reconnaît à une forme qui FAIT UN TRAVAIL, pas à une forme
  qui décore** — Coca-Cola au ruban qui structure la boîte, Apple au vide autour
  de l'objet. Test fait pour de vrai : coin et adresse masqués, le visuel reste
  identifiable. ⚠️ C'est un changement de charte, réversible d'une ligne.

  📷 **LES PHOTOS FONT 720 px, NOS VISUELS 2160.** Agrandissement 3×, ce qui est
  normalement rédhibitoire. Une seule des sept passe en plein cadre — **et c'est
  la plus FLOUE des sept.** Contre-intuitif et vérifié : mer, ciel et horizon
  sont des dégradés, il n'y a presque rien à inventer entre deux pixels. Les six
  autres ont du feuillage ou du sable en gros plan et deviennent de la bouillie.
  ⚠️ **L'indicateur évident m'a trompé** : la netteté (variance du laplacien)
  perdait 97,8 % sur la nette et 97,7 % sur la floue. **Deux chiffres identiques
  pour le bon cas et le mauvais.** 📌 Un pourcentage identique dans les deux cas
  n'est pas un résultat, c'est un avertissement : on mesure la mauvaise chose.
  (Troisième fois — après le carton de fin de la vidéo et le garde-fou du filet.)
  ✅ `photos/preparer-photo.py` : diagnostic + préparation, et il coupe
  automatiquement les bandes de capture d'écran. La première photo en portait 4
  lignes grises en haut — invisibles sur le téléphone, **12 lignes** une fois
  agrandies. 📌 Un défaut qu'on ne voit pas dans la source se voit dans
  l'agrandissement.
  🔴 **La vraie solution est de demander les originaux** : 720 px est la
  signature d'un renvoi WhatsApp, l'original du téléphone fait 3 000 à 4 000 px.
  Demandé au patron.

  ✅ `flyer48-traversee-fb.html` — « **TU N'ES QU'À / UNE TRAVERSÉE.** » Photo
  plein cadre, vague en couture, deux lignes, un appel. Conforme, zéro collision.
  Placé le **jeudi**, qui était vide. Provenance des photos dans
  `photos/PHOTOS-PATRON.md` (le dépôt est public).
  🔴 Reste : **dimanche** sans visuel, et la démonstration du matin à refaire.

- **02/09/2026 (🌙 LE BULLETIN DU SOIR PASSE LA BARRE, et une règle de fond
  arrive : UNE SEULE INFORMATION PAR VISUEL)** — le patron : « maintenant fais
  le bulletin du soir », puis « même les mots, tout doit être nickel et mesuré,
  on ne doit pas avoir plus d'une information par flyer ».

  🚩 **IL A ÉTÉ MIS AUX NORMES EN DERNIER, ALORS QU'IL PUBLIE TOUS LES SOIRS.**
  C'est l'ordre exactement inverse du bon sens, et la raison mérite d'être
  notée : il ne ressemble à aucun autre visuel (pas de photo, une donnée en
  héros), donc il n'apparaissait jamais quand je regardais « les flyers de la
  semaine ». 📌 **Ce qui tourne tout seul sort du champ de vision.**

  ✅ **CINQ MANQUEMENTS CORRIGÉS** :
  1. le titre parle enfin au lecteur — « Demain matin, MER AGITÉE » était un
     constat de bulletin météo, alors que toute notre voix dit « tu ». Devenu
     « **DEMAIN, TA MER : / PEU AGITÉE.** » La mer devient la sienne.
     ⚠️ Il a fallu ajouter `ETAT_COURT` dans `bulletin.py` (ETAT vaut « MER
     AGITÉE », on aurait lu « TA MER EST MER AGITÉE »). **ETAT n'a pas été
     touché** : il sert au JSON et au texte du post, et tordre son sens pour
     arranger une mise en page aurait cassé les deux.
  2. capitales, comme toute la marque ;
  3. un appel à l'action **dans les deux états du service** — ouvert il disait
     déjà « RÉSERVE POUR DEMAIN », il lui manquait la classe ; fermé il disait
     « TRAVERSÉES SUSPENDUES », un constat. Devenu « ÉCRIS-NOUS, ON TE
     PRÉVIENT », l'info « suspendues » descendant en 3e ligne ;
  4. le « ▸ » (U+25B8, hors de nos woff2) remplacé par un chevron **dessiné en
     SVG** — ce qui est tracé ne dépend d'aucune police ;
  5. la zone de respiration du logo : `.sur` entrait de 16 px, tout le bloc de
     tête est descendu de 22 px.

  ⚠️ **UN GABARIT NE SE VÉRIFIE PAS SUR LA VALEUR DU JOUR.** Premier essai de
  titre : « DEMAIN MATIN, / TA MER EST … ». Trois lignes rendues et une
  collision — mais seulement sur DEUX des cinq états de mer possibles (« PEU
  AGITÉE », « TRÈS FORTE »). À 86 px dans 928 px la colonne tient 17 signes, pas
  22. 📌 **Un gabarit se vérifie sur la PLUS LONGUE des valeurs possibles**,
  jamais sur celle qui sort aujourd'hui.

  🎯 **LA RÈGLE NEUVE — UNE SEULE INFORMATION PAR VISUEL** (`EXIGENCE.md` § 1
  bis). Elle est plus dure que « une seule chose nette » du § 6, parce qu'elle
  porte sur le FOND : une seule chose à retenir en sortant.
  **On ne compte pas les blocs, on compte les FAITS DISTINCTS.** Le bulletin
  disait la houle TROIS FOIS — gros chiffre, amplitude, courbe — plus une
  « période de houle » en secondes.
  · période supprimée : **un chiffre qu'on ne sait pas lire n'informe pas, il
    impressionne.** Ce n'est pas la même chose et ce n'est pas notre métier ;
  · amplitude supprimée : doublon exact ;
  · vent gardé : seul fait vraiment distinct.
  📌 Trois fois le même fait n'est pas de la profondeur, c'est de la répétition,
  et chaque répétition vole du regard au verdict.
  ⚠️ **Cacher n'est pas jeter** : PERIODE et AMPLI restent calculés et écrits
  dans `bulletin.json`. Décision de mise en page, donc réversible.
  🔴 Reste au patron : la courbe heure par heure est la 3e expression du même
  fait. Gardée pour l'instant, à supprimer d'un mot.

  🐛 **Et une faute de méthode à moi** : j'ai lancé `bulletin.py >/dev/null 2>&1`
  et conclu que mon changement n'avait pas pris. Il avait pris ; c'est
  Open-Meteo qui refusait de répondre dans ma session (le vrai bulletin de
  19h27, lui, était bien passé). **J'avais masqué l'erreur qui expliquait tout.**
  📌 On ne fait jamais taire la sortie d'erreur d'une commande dont on cherche
  justement à comprendre le résultat.

- **02/09/2026 (🚩 LE VENDREDI PUBLIAIT LA VARIANTE QUE LE PATRON N'AVAIT PAS
  CHOISIE)** — le patron : « celui du vendredi, enlève l'application, laisse
  juste le texte ». Or c'était **déjà** sa décision de ce midi (« entre le flyer
  avec l'écran de l'App et sans écran… » → réponse : sans écran), et le
  calendrier pointait bien sur `flyer47b`, la version sans écran.

  ⛔ **LE CHOIX N'ÉTAIT PAS PERDU DANS UNE DISCUSSION : IL ÉTAIT PERDU DANS UN
  CHEMIN DE FICHIER.** La ligne « Rendu » de `flyer47b` avait été copiée depuis
  `flyer47` et jamais corrigée : **les deux variantes déclaraient produire le
  même `flyer-etudes-facebook.png`.** Le dernier rendu écrasait l'autre, et
  c'était celui AVEC l'écran. Le calendrier était juste, la décision était
  juste, et c'est le fichier de sortie qui a tranché à leur place.
  📌 **DEUX SOURCES QUI ÉCRIVENT DANS LE MÊME FICHIER, C'EST UNE SOURCE DE
  TROP.** Une décision ne tient que si la mécanique ne peut pas la contredire.
  ✅ Recherche faite sur toute la bibliothèque : un seul autre cas, le bulletin
  du soir (gabarit → fichier rempli → PNG), et celui-là est légitime, c'est la
  même chaîne.
  ✅ `flyer47` (avec écran) supprimé — on ne garde pas la variante écartée à côté
  de celle qu'on publie, elle finit par sortir. `flyer47b` est désormais seul
  propriétaire de sa sortie.

- **02/09/2026 (🌍 LES CHARTES D'APPLE ET DE COCA-COLA, LUES DANS LE TEXTE)** —
  le patron : « va regarder les règles d'Apple ou Coca-Cola, même si c'est très
  strict on les suit au détail près. Je veux une com de niveau international,
  pas ce qu'on fait. **Mais garde nos règles.** »

  📄 Lues dans les **documents officiels** : Apple Identity Guidelines (56 pages,
  PDF sur apple.com/legal) et Coca-Cola Brand Identity and Design Standards v1.0
  (146 pages). Pas des résumés de blog — les deux PDF ont été téléchargés et
  dépouillés. **Quatre règles reprises**, celles qui sont chiffrées et donc
  vérifiables par une machine. Détail et citations : `EXIGENCE.md` § 5 bis.

  🍎 **LA PLUS BELLE, ET ELLE EST COPIABLE TELLE QUELLE** : la zone de
  respiration autour du logo n'est **jamais un nombre de pixels**, c'est une
  FRACTION DU LOGO. Apple : « one-half the height of the Apple logo ».
  Coca-Cola : la hauteur du trait d'union entre « Coca » et « Cola ». Du coup
  elle reste juste à toutes les tailles et personne n'a à la recalculer.
  ✅ Chez nous : emblème 68 px → zone de 34 px. `collision.js` la mesure, et il
  a trouvé l'infraction **sur le flyer du lundi (7 px) et sur le bulletin du
  soir (16 px)**, publiés depuis des semaines.

  ⛔ **LA DÉCOUVERTE QUI FAIT LE PLUS MAL : LA CASSE DES TITRES.** Coca-Cola
  § 2.35 interdit les titres en minuscules, Apple interdit de changer le
  traitement typographique. J'ai mesuré toute la bibliothèque : nos **cinq
  meilleurs** visuels étaient en CAPITALES à 100 %, dont celui noté 9/10
  dehors. Les six autres en minuscules — **y compris les deux que je venais de
  réparer le matin même.** J'ai fabriqué l'incohérence en croyant corriger.
  📌 **ON NE JUGE PAS UN VISUEL TOUT SEUL : ON LE JUGE À CÔTÉ DES AUTRES.** Un
  visuel peut passer tous les contrôles et abîmer la marque quand même, parce
  que le défaut n'est pas dedans — il est dans l'ÉCART avec ses voisins. C'est
  la troisième marche : après le code (`exigence.py`) et le rendu (`lignes.js`),
  puis le rapport entre blocs (`collision.js`), voici **la cohérence de la
  collection**.

  ✅ **CE QUI A ÉTÉ FAIT** : les 4 titres en minuscules passent en capitales, et
  toute la bibliothèque lit maintenant d'une seule main. Deux titres ont dû être
  raccourcis au passage — les capitales sont plus larges, et « LA HOULE EST
  RETOMBÉE. ON REPART. » est passé à trois lignes rendues avec collision.
  `collision.js` l'a attrapé ; `exigence.py` ne pouvait pas (il compte les
  lignes déclarées). Devenu « **LA MER EST CALME. / ON REPART.** »
  · avis de mer forte : « **LA MER DÉCIDE. / ON TE LE DIT.** » + appel à l'action
  · avis de suspension : « **AUJOURD'HUI, / ON RESTE À QUAI.** » + appel à
    l'action. L'ancien (« PAS DE TRAVERSÉE JUSQU'À NOUVEL ORDRE ») décrivait un
    règlement ; le nouveau met quelqu'un dedans.
  · lundi : « **TU N'INSTALLES / RIEN.** », titre redescendu de 206 à 224 px pour
    sortir de la zone de respiration.
  📌 Et à chaque changement de titre, **le texte du post a suivi** — c'est le
  piège du matin qui se répète : le visuel dit une chose, la vitrine en annonçait
  une autre. `texte-suspension.txt` et `texte-grostemps.txt` sont sortis de
  `page.py` pour que le `.txt` reste la seule source.

  ⚠️ **CE QU'ON N'A PAS REPRIS** : Apple interdit le texte sur une photo produit
  (p. 30). Chez nous, le texte sur photo EST la mise en page. Mais Apple parle
  de SES photos produit chez SES revendeurs — c'est du droit de marque, pas de
  la lisibilité. **Une règle ne se copie pas parce qu'elle vient d'une grande
  marque : elle se copie quand la raison qui l'a fait naître existe aussi chez
  nous.** C'est exactement ce que le patron voulait dire par « garde nos
  règles ».

- **02/09/2026 (🧹 LE GRAND NETTOYAGE — 40 visuels supprimés, et la règle
  d'écriture change)** — le patron : « supprime tous les flyers qui ne sont pas
  aux normes, les anciens flyers », puis « les écritures doivent être vraiment
  style Apple, deux à cinq mots mais très impactant et inspirer le respect de la
  marque ; tout doit être vraiment vérifié, strict et soigné, même les textes et
  les photos. »

  🚩 **CE QUI A DÉCLENCHÉ TOUT ÇA : LE FLYER DU LUNDI SORTAIT CASSÉ.** En
  préparant la revue des visuels de la semaine, j'ai vu que « Rien à installer.
  C'est juste une page. » imprimait son dernier mot — « page. » — **SOUS** son
  propre paragraphe. Idem sur la démonstration du jeudi matin (« réservée. »).
  Deux visuels publiés depuis des semaines, illisibles, et **aucun de nos deux
  contrôles ne pouvait le voir** : `exigence.py` lit le code et comptait deux
  lignes (il disait vrai) ; `lignes.js` mesure le rendu et en voyait trois, sans
  rien en conclure, parce qu'il regarde chaque bloc SÉPARÉMENT.
  📌 **LE DÉFAUT N'ÉTAIT DANS AUCUN BLOC : IL ÉTAIT ENTRE DEUX BLOCS.** D'où
  `collision.js` — la troisième famille de contrôle qui manquait : le code, le
  rendu, **et le rapport entre les choses**.
  ⚠️ Deux faux positifs corrigés en le calibrant, tous deux accusant nos
  MEILLEURS visuels : une boîte de ligne est plus haute que son encre (seuil en
  fraction du corps, pas en pixels) ; et un texte incliné ne se mesure pas avec
  un rectangle droit (la pastille de prix est tournée — l'outil dit désormais
  « je ne sais pas » au lieu de conclure).

  🍎 **LA NOUVELLE RÈGLE D'ÉCRITURE : 2 à 5 mots PAR LIGNE.** Le plafond se
  compte par ligne, le plancher sur le titre entier. J'ai écrit l'inverse au
  premier jet et le contrôle a aussitôt refusé « TU L'AS / **DÉJÀ.** » (publié
  le jour même) et « TU PARS VOIR / **QUELQU'UN.** » (9/10 dehors), au motif que
  leur seconde ligne fait un mot. **Une ligne d'un seul mot est une CADENCE, pas
  une étiquette** — c'est le geste Apple lui-même.
  📌 Troisième fois que cette leçon revient : **une règle qui refuse ce qu'on a
  fait de mieux n'est pas exigeante, elle est mal écrite.**

  🗑️ **CE QUI EST PARTI** : 40 fichiers HTML + 38 PNG. Il reste **12 sources,
  dont 8 conformes**. Tout est dans l'historique git, rien n'est perdu.

  ⛔ **UNE ERREUR RÉELLE PENDANT LA SUPPRESSION, ET ELLE VAUT UNE RÈGLE.** J'ai
  protégé les fichiers « vivants » en cherchant les références aux noms de
  fichiers **HTML**. Or `programme.py` ne connaît que le nom du **PNG**
  (`GROS_TEMPS = 'flyer-grostemps-facebook.png'`). Ma recherche a donc donné un
  feu vert pour l'avis de grosse mer, qui est un outil de service publié à
  chaque coup de vent. Rattrapé et restauré dans la minute.
  📌 **ON NE CHERCHE PAS LES RÉFÉRENCES À UN FICHIER, ON CHERCHE LES RÉFÉRENCES
  À CE QU'IL PRODUIT.** Un contrôle qui interroge le mauvais artefact répond
  « personne ne s'en sert » avec le même aplomb qu'une réponse juste.

  🔧 **CE QUI A ÉTÉ REMIS D'APLOMB DERRIÈRE** :
  · `calendrier.py` réécrit — 5 visuels pour 7 jours, et surtout `du_jour()` sait
    désormais rendre `None`. Avant, un jour sans visuel était impossible ; après
    le nettoyage il y en a deux, et l'ancien code serait allé chercher un fichier
    supprimé **à midi**, le seul moment où personne ne lit le journal.
    📌 Un calendrier qui ne sait pas dire « je n'ai rien aujourd'hui » ment un
    jour sur sept. Il vérifie aussi que les fichiers EXISTENT, pas seulement que
    la case est remplie.
  · `programme.py` se tait proprement les jours vides ; `controle.py` suit la
    nouvelle forme du calendrier.
  · `page.py` : 19 entrées mortes retirées, les 4 meilleurs visuels enfin
    ajoutés, et **les textes ne sont plus recopiés — ils sont lus dans les
    `texte-*.txt`**. Deux conventions pour la même chose, c'est une de trop : le
    jour où l'on corrige un texte, on en corrige un des deux et l'autre continue
    de circuler. Découvert en changeant le titre du visuel de grosse mer : la
    vitrine annonçait encore l'ancien.
  · `exigence.py` : « scanne » ajouté aux verbes d'action — le contrôle refusait
    « SCANNE ET RÉSERVE » posé à côté d'un QR code. La règle avait tort.

  🔴 **CE QUI RESTE OUVERT** : jeudi et dimanche n'ont plus de visuel, et la
  démonstration du matin non plus (son titre faisait 7 mots et elle avait la
  collision). Deux jours muets valent mieux qu'un visuel hors norme, **mais
  c'est un chantier, pas une cible.** Le bulletin du soir (`flyer8-soir`) reste
  hors norme et doit être repris — il est publié tous les soirs.

- **02/09/2026 (soir — 🚩 LE FILET ÉTAIT UNE DÉCORATION, et je m'en aperçois
  en vérifiant autre chose)** — bulletin publié à **19h27**, vérifié depuis la
  page : `2026-09-02 à 19:27 — LA MER DE DEMAIN, CE SOIR.` Mer de demain (03/09)
  **peu agitée, houle 0,91 m, vent 11 km/h est.** Page : **45 abonnés.**

  ⛔ **CE QUE J'AI TROUVÉ EN VÉRIFIANT UNE QUESTION ANNEXE.** Je croyais le
  `schedule:` GitHub muet depuis le 27/08 ; **il ne l'était pas.** Les trois
  crons du 01/09 ont bien été livrés :
  · 19h20 → arrivé **22h26** (3 h 06 de retard)
  · 20h00 → arrivé **22h39** (2 h 39)
  · 20h40 → arrivé **23h08** (2 h 28)
  Les trois ont tourné entièrement, et les trois ont été arrêtés par le
  garde-fou d'heure : étape « Publier » = `skipped`, trois fois.

  Le garde-fou a donc parfaitement marché. **Le filet, lui, n'a jamais servi à
  rien** : si la session avait été morte ce soir-là — le cas exact pour lequel
  il existe — la page serait restée muette malgré trois déclenchements réussis.
  📌 **UN DISPOSITIF DE SECOURS QUI NE SE DÉCLENCHE JAMAIS DANS SA FENÊTRE
  N'EST PAS UN SECOURS, C'EST UNE DÉCORATION QUI RASSURE** — et c'est pire
  qu'une absence, parce qu'on arrête de chercher une vraie solution.
  📌 Et la raison pour laquelle je ne l'avais pas vu : **un garde-fou qui
  refuse tout est indiscernable d'un garde-fou qui marche, tant qu'on ne
  regarde que ses refus.** Je mesurais « le cron a-t-il été bloqué ? » ; la
  bonne question était « le filet a-t-il, une seule fois, servi à quelque
  chose ? »

  ✅ **DEUX CORRECTIONS, QUI VONT ENSEMBLE :**
  1. **La fenêtre devient 19h45 → 23h00** (au lieu de 18h00 → 22h00), comptée
     en minutes et non en heures pleines. Elle commence **après** le battement
     de 19h25 pour que le filet ne prenne jamais la place du rendez-vous
     quotidien ; elle finit à 23h00 parce que la vraie question n'est pas
     « est-ce l'heure idéale ? » mais « vaut-il mieux ça, ou une page muette ? ».
     Avec cette seule borne, deux des trois crons d'hier auraient publié.
  2. **Dix crons semés de 08h15 à 19h00 UTC** au lieu de trois groupés. Les
     retards mesurés vont de ~20 min à 8 h 43 et sont imprévisibles : aucun
     horaire unique ne peut tomber juste, donc on couvre les trois régimes de
     retard observés (0-1 h, 2-4 h, 7-10 h). Les surnuméraires ne coûtent rien
     — hors fenêtre ils se taisent, dans la fenêtre `deja_publie()` les refuse
     en ~3 s.

  🔴 **RESTE À DÉCIDER PAR LE PATRON — le flyer de midi n'a AUCUN filet.**
  `publication-du-jour.yml` n'a plus de `schedule:` du tout depuis le 28/08 :
  il dépend à 100 % du battement, donc de la session. C'est exactement ce qui a
  coûté le silence du 31/08. Je ne l'arme pas de moi-même, et pour une raison
  de fond : le soir, le cron sait quoi publier (le bulletin de la mer est
  calculé). À midi, **les exceptions vivent dans ma consigne, pas dans le
  robot** — un cron publierait le flyer du calendrier en ignorant « ce
  mercredi, sors TU L'AS DÉJÀ ». Armer midi demande d'abord de sortir les
  exceptions de ma tête et de les écrire dans un fichier que le robot lit.
  📌 **On n'automatise pas un jugement tant qu'il n'est pas écrit quelque part.**

- **02/09/2026 (midi — « TU L'AS DÉJÀ » EST ENFIN SORTI, avec deux jours de
  retard, et le patron a tranché entre deux flyers)** — publié à **12h15**,
  vérifié dans le rapport lu DEPUIS LA PAGE : `2026-09-02 à 12:15 — TU L'AS
  DÉJÀ.` L'étape « Publier un visuel choisi » a duré 10 s (elle en dure ~3
  quand le garde-fou refuse un doublon). Page : **44 abonnés, 17 publications
  sur 7 jours.**

  📅 **L'écran de l'appli a été REGÉNÉRÉ avant la publication** (`refaire.py`,
  date affichée 09/09/2026). C'est une contrainte permanente de ce visuel, pas
  une étape de confort : le champ DATE est calculé à « aujourd'hui + 7 jours »
  et un post reste sur la page pour toujours. Publier la version d'hier
  afficherait tôt ou tard une date passée, c'est-à-dire un service mort
  (norme § 7.3). **Tout visuel qui contient une date porte une dette : il faut
  le refaire à chaque sortie, ou ne pas y mettre de date.**

  ✅ Contrôles passés avant l'envoi : `exigence.py` CONFORME, `lignes.js`
  0 ligne veuve, et les quatre vérifications à l'œil de la consigne — date dans
  le futur, aucun visage, pas de trait vertical clair au bord gauche (saut max
  8 sur 260 px à mi-hauteur), haut de la photo fondu dans le marine (30 de
  saut, contre 99 avant `.haut-fondu`).

  🎯 **AVEC OU SANS L'ÉCRAN DE L'APPLI — le patron a demandé lequel « résonne
  comme un expert ». Réponse donnée : SANS** (`flyer47b`), pour trois raisons
  qui valent pour tous les prochains visuels :
  1. norme § 6 — une seule chose nette par visuel ; le portrait et la carte se
     disputaient le regard ;
  2. à 360 px la carte ne se lit pas : elle **fait semblant de prouver**, alors
     que « TU L'AS DÉJÀ » montre l'appli en grand et le prouve vraiment ;
  3. la version avec écran porte une date, donc la dette ci-dessus ; la version
     émotion est vraie dans six mois.
  📌 **La bonne réponse à « mets tout dans une image » est presque toujours une
  SÉQUENCE** : l'émotion un jour, le produit le lendemain (§ 1, un seul
  univers, deux moments). Repère : notre visuel le mieux noté de l'extérieur
  (9/10) ne contenait aucune capture d'écran.

- **01/09/2026 (midi — 🚩 DEUX ROUTINES CONTRADICTOIRES, ET C'EST MOI QUI AI
  CRÉÉ LA CONTRADICTION)** — les deux Routines de 12h05 ont sonné à 35 secondes
  d'intervalle. La Routine du jour disait « regarde la page avant de décider » ;
  la Routine quotidienne, elle, disait « marche normale, pousse le battement ».

  **Pourquoi elles se contredisaient : en réécrivant la quotidienne ce matin,
  j'ai remplacé ses trois exceptions datées par une seule (mercredi 02/09) — et
  j'ai supprimé celle du 01/09 sans la remplacer.** Prise au mot, elle aurait
  publié un TROISIÈME post aujourd'hui, après l'annonce de reprise (04:06) et la
  vidéo (04:20), sur une page de 43 abonnés.
  📌 **QUAND ON RÉÉCRIT UNE CONSIGNE, ON VÉRIFIE CE QU'ON EN A RETIRÉ, PAS
  SEULEMENT CE QU'ON Y A MIS.** J'ai relu ma nouvelle consigne et je l'ai trouvée
  meilleure ; je n'ai pas relu l'ancienne pour voir ce qui disparaissait.
  ✅ Ce qui a sauvé la mise n'est pas la consigne, c'est la RÈGLE : décider en
  lisant la page, jamais en croyant un texte — même le mien. Rapport lancé sans
  rien publier (toutes les étapes de publication sautées) : deux posts déjà
  sortis aujourd'hui, donc rien de plus à midi.
  ✅ **ET LA VIDÉO EST CONFIRMÉE SUR LA PAGE** : le compteur est passé de 16 à 17
  publications entre 04:17 et 09:09. Elle n'est pas seulement acceptée par l'API,
  elle est comptée par la page.
  ⚠️ Plus de collision demain : les deux Routines datées étaient des `run_once`,
  elles ont fini leur vie. Seule la quotidienne reste, et elle porte les
  instructions du mercredi.

- **01/09/2026 (suite — 🎬 LA VIDÉO YOUNG LEADER EST SORTIE, et ce qu'elle a
  révélé)** — le patron : « envoie la vidéo **ils ont autorisé** », et « on a
  10 abonnés de plus, plus de gens demandent à propos du service ».

  ✅ **PUBLIÉE ET VÉRIFIÉE** : `Vidéo publiée : 1085106587247853`, 01/09 à 04:20
  UTC. Et son post de reprise à lui était déjà sorti à 04:06 —
  « LA HOULE EST RETOMBÉE. ON REPART. », lu dans le rapport, compté depuis la
  page. La séquence de réouverture s'est déroulée dans l'ordre prévu depuis le
  12/08 : son annonce à la main, puis la vidéo.

  ⚖️ **LES DROITS** : l'association a autorisé. C'est la réponse attendue depuis
  le 12/08 (20 jours). ⚠️ J'ai sa parole rapportant la leur, **pas le message
  lui-même** — noté tel quel dans `CREDITS-PARTENAIRES.md`. Ça suffit pour
  publier (juridique = poste C), pas devant un tiers.

  🚩 **LE PREMIER ESSAI A ÉCHOUÉ EN ZÉRO SECONDE : « vidéo introuvable ».**
  Le fichier était bien sur `main` — c'est le `sparse-checkout` du workflow qui
  ne prenait pas `moheligo/pub/video`. L'étape avait été écrite le 26/08 et mise
  en attente **le jour même** ; elle n'avait donc jamais tourné une seule fois.
  📌 **UN CHEMIN DE CODE JAMAIS EXÉCUTÉ N'EST PAS UN CHEMIN DE CODE QUI MARCHE.**
  Elle avait pourtant tout l'air d'être finie : étape écrite, case dans le
  formulaire, garde-fou de service, fonction testée. C'est la même famille que le
  visuel de reprise « prêt depuis le 12/08 » qui a été refusé le jour J. **Ce
  qu'on garde en réserve se vérifie AVANT d'en avoir besoin, pas au moment où on
  s'en sert** — sinon le seul moment où on découvre le défaut est le pire.

  🩹 **ET UNE PANNE ANCIENNE, RECONFIRMÉE** : `Commentaire : refusé (le post
  reste en ligne)`. Le premier commentaire — celui qui porte le lien de
  réservation — **ne part pas**, faute de la permission `pages_manage_engagement`
  sur le jeton (connu depuis le 11/08, rendu non bloquant le jour même). Tous nos
  « premiers commentaires » écrits avec soin sont donc inertes depuis le début.
  ➡️ À régler avec le patron en même temps que le renouvellement du jeton
  Facebook (il expire vers le 10/10/2026) : c'est la même manipulation.

  📈 **CE QUE JE MESURE** : 43 abonnés (41 le 30/08), 16 publications sur
  7 jours. Le patron en compte 10 de plus — Facebook distingue « abonnés » et
  « j'aime la Page », et je ne lis que le premier. À vérifier ensemble.

  ⏰ **LE BULLETIN DU SOIR A DE NOUVEAU UN RENDEZ-VOUS GITHUB**, à sa demande —
  mais avec le garde-fou qui manquait en août. Deux mesures opposées, toutes deux
  vraies : le 28/08 les `cron` arrivaient avec 8 h 25 à 8 h 43 de retard et le
  bulletin est parti à 3h38 du matin ; le 31/08 la session n'avait plus de crédit
  et la page est restée muette. **On ne choisit pas entre les deux pannes, on
  supprime le dégât de la seconde** : trois `cron` (19h20, 20h00, 20h40) et une
  étape qui refuse de publier hors de la fenêtre 18h-22h. Un `cron` livré à 3h38
  fabrique le flyer et se tait. 📌 **Quand un outil est peu fiable sur QUAND il
  agit, on ne le supprime pas et on ne lui fait pas confiance : on lui interdit
  d'agir au mauvais moment.**

- **01/09/2026 (🟢 LE SERVICE ROUVRE — et un jour de silence complet)** —
  le patron, au matin : **« les traversées sont ouvertes »** et, dans la même
  phrase, **« on a rien publié hier, j'avais pas de token Claude Code »**.

  🔴 **LUNDI 31/08 : PAGE MUETTE, JOURNÉE ENTIÈRE.** Les trois Routines ont bien
  sonné (12h05 quotidienne, 12h05 « TU L'AS DÉJÀ », 19h25 bulletin) — et aucune
  n'a pu s'exécuter, faute de crédit. Ni flyer, ni bulletin du soir. Vérifié :
  la dernière chose sortie est le bulletin du dimanche soir.
  📌 **CE QUE ÇA APPREND, ET CE N'EST PAS « IL FAUT DU CRÉDIT »** : tout notre
  système de publication passe par une session Claude qui pousse un battement.
  **Le point de défaillance unique n'est pas GitHub, c'est la session.** Les
  workflows, eux, marchent seuls dès qu'un commit arrive. À proposer au patron :
  un `schedule:` cron directement dans les workflows GitHub, pour que le bulletin
  du soir parte même quand aucune session ne tourne. Le rendez-vous quotidien
  vaut plus que son contenu — et il vient de sauter.

  🟢 **RÉOUVERTURE APRÈS SEPT JOURS** (26/08 → 01/09), la plus longue des deux
  fermetures de l'été. `OUVERT = True` dans `service.py`, et **un seul
  interrupteur a suffi** : mention de fermeture retirée de toutes les
  publications, bandeau du bulletin repassé à « RÉSERVE POUR DEMAIN », premier
  commentaire redevenu commercial, vidéo Young Leader débloquée. C'est
  exactement ce pour quoi l'état du service vit à un seul endroit.

  ⬛ **LE VISUEL DE REPRISE ÉTAIT « PRÊT » DEPUIS LE 12/08. IL NE L'ÉTAIT PAS.**
  Le contrôle l'a refusé le jour même où il fallait s'en servir : 5 apostrophes
  droites, aucun SENTIMENT déclaré, et surtout **aucun appel à l'action lisible**
  — le bandeau d'or disait « TA PLACE, MAINTENANT », qui n'est pas un verbe.
  Devenu « PRENDS TA PLACE ». 📌 **Un visuel gardé « pour le jour J » n'est pas
  prêt : la norme bouge après lui, et on s'en aperçoit au pire moment — celui où
  il faut publier vite.** À faire : repasser les autres visuels « en réserve »
  au contrôle AVANT d'en avoir besoin.
  ✅ Envoyé au patron avec son texte (`texte-reprise.txt`) : geste n°1 de la
  procédure de reprise, c'est lui qui publie à la main (sa consigne du 12/08).

  🩹 **ET LE PREMIER COMMENTAIRE DU BULLETIN RÉPÉTAIT LA FAUTE DU 26/08, EN PLUS
  DOUX** : dimanche soir, le post annonçait « QUAND ÇA REPREND : C'EST PRÉVU
  MARDI » et le commentaire, trois lignes plus bas, disait encore « la reprise
  dès qu'elle est décidée » — le même envoi ne se souvenait pas de ce qu'il
  venait de dire. Tout ce qui parle de la reprise passe désormais par
  `service.reouverture()`. Il portait aussi une apostrophe droite dans `qu\'elle`
  — **échappée, donc invisible à mon détecteur qui cherchait une lettre avant
  l'apostrophe. Une faute qu'un contrôle ne peut pas voir est une faute qui
  reste.**

  📅 **REPROGRAMMÉ** : mardi midi, la Routine décide en LISANT la page (si le
  post de reprise du patron est sorti, elle ne publie rien de plus ; sinon elle
  sort « TU PARS VOIR QUELQU'UN »). « TU L'AS DÉJÀ », jamais publié, passe au
  mercredi 02/09.

- **30/08/2026 (⬛ LA BARRE A REFUSÉ UN VISUEL DÉJÀ PROGRAMMÉ, ET ELLE AVAIT
  RAISON)** — journée où le contrôle a servi pour de vrai, deux fois, dans les
  deux sens opposés.

  ✅ **PUBLIÉ ET VÉRIFIÉ** : le flyer du neveu « ON NE VISITE PAS MOHÉLI. ON Y
  REVIENT. » est sorti le 30/08 à 09:11 UTC (`1166058113262206_122118691707374081`),
  confirmé dans le rapport du workflow, qui le recompte depuis la page.
  🩹 **Et j'ai raté mon premier envoi** : les chemins passés au workflow étaient
  ceux du dépôt (`moheligo/pub/flyers/…`) alors que l'étape travaille DÉJÀ dans
  `moheligo/pub/flyers`. Le garde-fou `test -f` a arrêté la course 48, **rien
  n'est parti**, et c'est exactement son travail. Course 49 relancée avec les
  noms nus : publiée. 📌 **Les entrées du workflow sont relatives à
  `working-directory`, jamais à la racine du dépôt.**

  🚩 **CORRECTION DE RÈGLE N°1 (le matin) — la règle était mal écrite.**
  « 6 mots maximum par titre » refusait « ON NE VISITE PAS MOHÉLI. ON Y
  REVIENT. » (8 mots), noté 9/10 dehors. **Une règle qui refuse ce qu'on a fait
  de mieux n'est pas exigeante, elle est mal écrite.** La vraie contrainte est
  ce que l'œil saisit d'un coup : elle se compte **par ligne**. Corrigé.

  🚩 **CORRECTION DE VISUEL N°2 (l'après-midi) — là, la règle avait raison.**
  `flyer43` était programmé pour lundi sous le titre « TOUT EST LÀ. ». Le
  contrôle l'a refusé au § 2 : *le titre ne parle pas au lecteur*. Et c'est
  vrai — « tout est là » est une phrase sur NOTRE produit, pas sur la personne
  qui regarde ; c'est précisément ce que le patron a demandé d'arrêter le 29/08.
  Retitré **« TU L'AS DÉJÀ. »** : même idée (rien à installer, rien à aller
  chercher), dite au lecteur, et elle répond à l'objection réelle du marché —
  les gens croient qu'il leur manque quelque chose pour réserver en ligne.
  Fichiers renommés `flyer43-tulasdeja-fb.html` / `flyer-tulasdeja-facebook.png`
  / `texte-tulasdeja.txt`, et **les trois Routines mises à jour en conséquence**.
  📌 **LA LEÇON DES DEUX, ENSEMBLE** : quand la machine et le visuel se
  contredisent, la question n'est jamais « qui a tort » mais **« lequel des deux
  est mal écrit »**. Le matin c'était la règle ; l'après-midi c'était le visuel.

  📐 **TROIS DÉFAUTS TROUVÉS EN MESURANT, PAS EN REGARDANT** :
  · **ligne veuve** — « embarques. » restait seul sous deux lignes pleines. La
    norme § 5 l'interdisait depuis le 29/08 et **rien ne la faisait respecter**.
    D'où `pub/flyers/lignes.js`, qui lit la découpe réelle des blocs de texte.
    Élargir la colonne ne réglait rien (400 comme 424 px) : c'était la PHRASE
    qui était mal coupée. Retenue : « Ton guichet tient dans ta main. Tu
    choisis ton port, tu paies, tu pars. » — deux lignes pleines.
  · **coupure du haut** — `.photo` commence à `top:46px` : à x=1900 du rendu, le
    rouge passait de 15 à 114 **en un pixel**, une épaule tranchée à plat sur
    une bande marine. Mettre la photo en pleine hauteur a été essayé, rendu,
    **regardé** : le téléphone grossit de 3,5 % et sort du cadre. On dissout au
    lieu de recadrer (`.haut-fondu`), et c'est exact et non approximatif — le
    fond de la photo vaut #0F2A5C depuis `remplacer_mur()`, la page aussi.
  · **le titre a été MESURÉ, pas estimé** — « TU L'AS » 310 px, « DÉJÀ. » 257 px
    dans 424 px de colonne. Au passage la mesure a écarté « TOUT EST DANS TA
    MAIN. » : 641 px sur une ligne, encore 505 px à 62 px de corps.

  🪞 **ET MON PROPRE OUTIL M'A MENTI, une fois.** Pour lire les lignes, mon
  premier jet entourait chaque mot d'un `<span>`. Ça marchait sur le corps de
  texte et **ça a menti sur le titre** : `.acc span` est en `display:block`, mes
  spans ont donc mis chaque mot sur sa propre ligne et l'outil a annoncé « 3
  lignes, ligne veuve » sur un titre qui en fait deux. 📌 **Une sonde qui
  modifie ce qu'elle mesure ne mesure rien.** Refait avec des `Range`, qui
  lisent sans rien changer. Le même défaut existait dans `exigence.py`, qui
  coupait le titre à chaque `<span>` : il lit maintenant la règle CSS avant de
  compter. Et `lignes.js` ne crie plus au loup sur les coupures VOULUES (un
  `<br>`, un span doré en bloc, un `<small>` de signature) — une veuve, c'est un
  mot que le retour à la ligne **automatique** a laissé seul.

  🩹 **APOSTROPHES DROITES, LÀ OÙ ÇA COMPTE LE PLUS** : 5 dans
  `texte-revenir.txt` (le post du jour), puis **dans les sources qui fabriquent
  le texte du soir** — `bulletin.py` (le post « LA MER DE DEMAIN, CE SOIR »,
  publié TOUS LES SOIRS) et `service.py` (le point de midi de fermeture), plus
  `texte-digitalisation.txt`. 📌 **On corrige la SOURCE, jamais la copie** :
  `texte-du-jour.txt` est généré par `bulletin.py` — le corriger à la main
  aurait été effacé au prochain bulletin. Il se régénère propre à 19h25.

  ❓ **CE QUI RESTE EN L'AIR, ET QUE JE NE PEUX PAS RÉSOUDRE SEUL** : les trois
  chiffres (réservations payées, visites, abandon au paiement) demandés depuis
  le 18/08 ; la date de reprise ; la phrase écrite d'autorisation d'image des
  Young Leader (18 jours) ; le lauréat est-il mohélien — tant que non, « ON A DE
  QUOI ÊTRE FIERS » ne part pas ; les ~40 visuels encore hors norme ; le jeton
  Facebook expire vers le 10/10/2026.

- **29/08/2026 (📅 TROIS JOURS PROGRAMMÉS, ET LA BARRE ENTRE DANS LE ROBOT)** —
  relecture extérieure des deux exemples : « Tu pars voir quelqu'un » **9/10,
  le meilleur de la bibliothèque** ; « On a de quoi être fiers » **7/10, en
  retrait**. Le verdict est juste, et je le prends tel quel.
  ✅ **Deux corrections faites, parce qu'elles étaient justes** : cadrage
  resserré (1120 px au lieu de 1536 sur 2560 — la vedette occupe 1,4 fois plus
  de surface, l'ampleur reste parce que l'horizon est haut), et dégradé du bas
  à **six arrêts au lieu de quatre** (à quatre, une marche était perceptible
  vers 55 %).
  ⛔ **UNE REMARQUE REFUSÉE, ET C'EST LA NORME QUI TRANCHE** : « le CTA reste
  générique, après un slogan aussi humain un CTA plus aligné serait plus
  puissant. » **Non.** La norme § 4 dit : un seul appel, toujours le même verbe,
  toujours la même adresse. Un appel qui change à chaque visuel n'est plus
  reconnu — c'est exactement la discipline que les trois relecteurs nous
  reprochent de ne pas avoir. **On ne peut pas réclamer de la cohérence et
  varier l'appel à l'action.**
  🩹 **TROUVÉ EN VÉRIFIANT LE TEXTE DU POST** : `service.MENTION_FERMETURE`
  contenait **3 apostrophes droites**. C'est le passage le plus lu de tout ce
  qu'on écrit — il part sur CHAQUE publication pendant une fermeture. Corrigé.
  🗓️ **PROGRAMMÉ, parce que la session va se réinitialiser** :
  · dimanche 30/08 → le neveu (`trig_01Nt6n9uZH8DrBk7KRbbztoH`)
  · lundi 31/08 → « TOUT EST LÀ », produit (`trig_01EmmwFfX2g2hyMLdfq8Q8ki`)
  · mardi 01/09 → « TU PARS VOIR QUELQU'UN », émotion (`trig_014LwshHHbBh3QcTP8k888Xx`)
  **Un seul univers, deux moments : produit lundi, émotion mardi.**
  ⬛ **LA BARRE EST ENTRÉE DANS LE ROBOT DE MIDI** : `exigence.py` est désormais
  exécuté AVANT chaque battement, tous les jours. Si le visuel du jour n'est pas
  conforme, **on ne publie pas** — on prévient et on corrige. Au 29/08, 1 sur 43
  passe : le contrôle va donc refuser souvent. **C'est le but. On ne publie plus
  un visuel hors norme parce qu'il est l'heure.**
  ⚠️ **FRAGILITÉ CONNUE À DIRE** : ces Routines sont liées à CETTE session. Une
  Routine qui ouvre une session neuve n'a pas les droits d'écriture sur le dépôt
  (mesuré le 28/08) — elle tourne, ne pousse rien, et se déclare réussie. Si la
  session est réinitialisée, il faut vérifier que les publications sortent
  vraiment, et ne jamais se fier au statut « SUCCEEDED ».

- **29/08/2026 (🚩 « C'EST ÉCRIT YOUNG LEADER OCÉAN INDIEN » — quand l'image
  parle, on la cite)** — sur le flyer 45, j'avais écrit « Young Leader Mohéli
  distingue ceux qui font avancer l'île ». **L'écharpe, elle, dit « YOUNG
  LEADER · OCÉAN INDIEN · 2025-2026 ».** J'avais donc rabaissé sa distinction
  d'un niveau RÉGIONAL à un niveau LOCAL — sur un visuel censé lui rendre
  hommage. Le patron l'a vu en une seconde.
  📌 **NOUVELLE RÈGLE, § 7.6 de la norme : une image qui porte des mots est une
  SOURCE. Le texte les reprend exactement.** La contredire, même par
  imprécision, est une erreur de FAIT, pas de style. C'est la même famille que
  « le code n'est pas la vérité du service » : je m'étais fié à ce que je savais
  du partenaire au lieu de lire ce que l'image montrait.
  ✅ Corrigé : « Young Leader Océan Indien, 2025-2026. MoheliGo est partenaire
  de Young Leader Mohéli. » — les deux faits, chacun à sa place.
  ✍️ **Et une règle de composition en prime** : « 2025-2026 » se cassait en fin
  de ligne. On ne peut pas le réparer avec un trait insécable U+2011 (hors de
  nos woff2, il disparaîtrait en silence) — `white-space: nowrap` en CSS.
  ❓ **CE QUE JE NE PEUX TOUJOURS PAS SAVOIR** : le lauréat est-il mohélien ?
  Le titre est « Océan Indien », les photos viennent de Young Leader Mohéli,
  et **rien dans le dépôt ne dit son origine**. Tant que ce n'est pas confirmé,
  « ON A DE QUOI ÊTRE FIERS » repose sur un lien non vérifié. À demander au
  patron avant toute publication — manuel § 12.2 quater.

- **29/08/2026 (🏅 DEUXIÈME EXEMPLE DE LA BARRE — Young Leader, et deux règles
  corrigées par l'usage)** — `flyer45-fiers-fb.html`, SENTIMENT : LA FIERTÉ.
  ⚖️ **Droits vérifiés AVANT de dessiner** : le patron a donné le go le
  12/08 (« pour les Young Leader tu as le go »). Reste la phrase écrite du
  responsable — elle ne bloque plus, elle protège, et elle manque depuis 17 jours.
  🎯 **Ce que le visuel promet, et ce qu'il ne promet pas.** Il dit que Mohéli
  produit des gens dont on peut être fier et que MoheliGo est partenaire. **Il
  ne dit PAS qu'on les sponsorise ni que le lauréat est client** — nous avons un
  contrat publicitaire, pas un mécénat. Norme § 7.1.
  ✨ **L'écharpe est dorée** : la couleur de la marque, sans qu'on l'ait
  cherchée. C'est ce qui fait tenir la photo dans notre univers.
  🖼️ **Cadrage décentré imposé par le sujet** : l'écharpe court de haut en bas,
  donc aucun voile par le bas n'est possible sans manger « OCÉAN INDIEN ». On
  dégage la colonne à gauche, sur le mur.
  ⛔ **Bandeau partenaire essayé puis RETIRÉ** : posé en travers, il coupait
  l'écharpe en deux — le sujet — et le logo y était illisible à 30 px. La
  mention honnête est déjà dans le texte. *Une ligne juste vaut mieux qu'un
  bandeau qui abîme la photo.*
  📏 **Titre à 56 px et non 72, et c'est calculé** : la colonne fait 400 px.
  *On ne rétrécit pas la photo pour agrandir un titre — c'est le titre qui
  s'adapte au sujet.*
  🔧 **DEUX FAUX POSITIFS DU CONTRÔLE, CORRIGÉS DANS LE CONTRÔLE** :
  · « +269 479 43 28 » était pris pour un chiffre inventé ;
  · « Young Leader » était pris pour le superlatif « leader ».
  📌 **La règle que j'en tire : un contrôle qui punit un fait exact rend la
  norme absurde, et une norme absurde finit contournée.** On corrige
  l'instrument, on ne contourne jamais la règle.

- **29/08/2026 (⬛ LA BARRE — le patron relève le niveau, et ça devient
  mesurable)** — « je ne joue plus dans la cour des entreprises comoriennes, je
  veux m'imposer comme numéro un. Les petits détails comptent. »
  📄 **`dossier/EXIGENCE.md`** — la norme. Règle de rédaction : **chaque exigence
  est vérifiable par un chiffre ou par une machine.** « Plus premium », « plus
  soigné » n'y entrent pas — ce sont des vœux, pas des exigences.
  🤖 **`pub/flyers/exigence.py`** — l'instrument qui REFUSE. Une norme qu'on
  relit de bonne volonté est une intention.
  🚩 **CE QU'IL A TROUVÉ EN UNE COMMANDE, sur 43 visuels : 1 conforme.**
  · **186 apostrophes droites `'`, ZÉRO typographique `’` — 100 % de fautes**,
    invisibles depuis trois semaines. C'est très exactement la différence entre
    un texte tapé et un texte composé ;
  · 42 visuels sans SENTIMENT déclaré ; 31 sans appel à l'action structuré ;
    13 titres qui parlent de nous et non du lecteur ; 11 caractères hors de nos
    woff2 (le même piège que la flèche `↔` affichée « .. »).
  ✅ **Les contrastes, eux, sont TOUS conformes WCAG AA** — mesurés : blanc
  13,94:1, or 8,05:1, texte courant 10,15:1, petites capitales 5,74:1. Le gap
  n'était pas là. Mesurer évite de réparer ce qui marche.
  🎯 **LA SYNTHÈSE RETENUE, contre le conseil « choisis un ton »** : le marché
  comorien IMPOSE d'expliquer — une grande partie des gens n'a jamais payé en
  ligne, supprimer le « comment » supprimerait ce qui convertit. Mais expliquer
  n'autorise pas à baisser le niveau. **Un seul univers, deux moments :
  l'émotion ouvre, le produit livre, dans la même lumière.** L'explication monte
  au niveau de l'émotion, jamais l'inverse.
  🖼️ **`flyer44-quelquun-fb.html`** — l'exemple, conforme au premier passage.
  Titre « TU PARS VOIR QUELQU'UN. » : 4 mots, parle au lecteur, aucun mot
  abstrait. Corps : 13 mots qui portent le produit sans changer de voix. Une
  vedette minuscule sur une mer immense — l'image ne montre pas un produit, elle
  montre la distance entre deux personnes, et le titre ne fait que la nommer.
  📌 **Les quatre sentiments déclarables, et rien d'autre** : LE SOULAGEMENT,
  LA PROXIMITÉ, LA FIERTÉ, LA CONFIANCE. Un visuel qui n'en déclare aucun n'est
  pas fini ; un visuel qui en vise deux n'en transmet aucun.

- **29/08/2026 (🗓️ « TOUT EST LÀ » PROGRAMMÉ LUNDI, et la date rendue
  périssable-proof)** — le patron valide lundi 31/08 midi, en ajoutant :
  « regarde la date du flyer ». Il avait raison de la regarder.
  📅 **LE VISUEL PORTAIT LE 05/09** — valable lundi, mais **un post Facebook
  reste sur la page pour toujours**. Après le 5 septembre, le flyer montre une
  réservation pour une date passée : le lecteur en conclut que le service est
  mort. C'est le troisième défaut de date de la journée, et le plus insidieux :
  il n'apparaît qu'en différé.
  ✅ **Corrigé au niveau de la CHAÎNE, pas du fichier** : `refaire.py` relance
  maintenant `capture.js` lui-même à chaque fabrication (avec HAUTEUR=995 pour
  le rapport 0,442 de l'écran photographié). La date se recalcule donc toujours
  à « aujourd'hui + 7 jours ». Le visuel n'est plus un actif qu'on garde : c'est
  une sortie qu'on refait.
  🗓️ **Programmation** : Routine ponctuelle `trig_01EmmwFfX2g2hyMLdfq8Q8ki`,
  lundi 31/08 à 09h05 UTC. Elle REFABRIQUE avant de publier, et elle porte
  **trois contrôles à l'œil** avant publication : date au futur et au format
  JJ/MM, aucun visage, aucun trait vertical au bord gauche. Si un contrôle
  échoue, on ne publie pas.
  ⚠️ L'exception de la Routine quotidienne couvre désormais **dimanche 30 ET
  lundi 31** — sinon deux publications à trois minutes d'écart les deux jours.
  📝 Texte du post : `pub/flyers/texte-toutestla.txt`, passé par
  `service.avec_mention()` (vérifié : la mention de suspension s'insère bien
  avant les mots-dièse).

- **29/08/2026 (⚠️ DEUX ROUTINES À LA MÊME MINUTE — trouvé en cherchant un
  créneau)** — en cherchant quand publier le flyer 43, j'ai listé les Routines
  et découvert que **deux d'entre elles partaient dimanche 30/08 à 09h05 UTC** :
  la quotidienne de midi (calendrier → `flyer-partenariat`) et la Routine
  ponctuelle du flyer du neveu. Deux publications à trois minutes d'intervalle
  sur une page de **33 abonnés**, ça se voit.
  📌 **Comment le défaut est né** : j'ai créé la Routine du neveu le 28/08 à
  23h28, puis la quotidienne de midi à 23h41 — treize minutes plus tard, sans
  regarder ce qui existait déjà. **Créer un rendez-vous sans lister les
  rendez-vous existants, c'est fabriquer une collision.**
  ✅ Corrigé sans toucher au calendrier ni supprimer quoi que ce soit : la
  Routine quotidienne porte maintenant une exception explicite pour le seul
  dimanche 30/08 — elle ne pousse pas le battement ce jour-là et le dit au
  patron. Le neveu part seul, comme il l'avait demandé (« l'autre sera le
  dimanche »).
  🗓️ **Créneau proposé pour le flyer 43** : lundi 31/08 à 12h05, à la place de
  « rien à installer ». Raison : même famille (l'appli est simple et immédiate),
  mais le 43 MONTRE au lieu d'affirmer — et le lundi est le jour où l'on
  planifie sa semaine. **On n'ajoute pas un post, on en remplace un** : sur une
  page de 33 abonnés, améliorer vaut mieux qu'ajouter.

- **29/08/2026 (📏 « IL Y A UNE LIGNE LÀ » — six pixels recopiés à la main)** —
  le patron voit un trait vertical sur toute la hauteur du flyer 43. Il ne dit
  pas où ; je l'ai cherché en MESURANT le profil de la ligne de pixels au lieu
  de scruter l'image : R passait de 15 à 55 puis revenait à 15 **en six
  pixels**, à x=460 exactement.
  🐛 **LA CAUSE, ET ELLE EST BÊTE** : `.photo` fait 620 px de large, `.fondu`
  en faisait **614**. Six pixels de photo restaient à nu, et comme le fond de
  la photo y est un peu plus clair que #0F2A5C, ça dessinait une frontière.
  📌 **DEUX RÈGLES QUE J'EN TIRE**
  1. **Deux dimensions qui doivent être égales ne se recopient pas à la main.**
     J'avais élargi `.photo` de 614 à 620 et oublié le voile — exactement le
     genre d'écart que la charte a déjà subi (marge 76/70, coin 404/392/412).
  2. **Un fond « presque » de la bonne couleur est pire qu'un fond franchement
     différent : l'œil ne voit pas une nuance, il voit une frontière.**
  ✅ Corrigé : voile à 620 px, et les 4 premiers pour cent restent OPAQUES avant
  que le fondu commence — sinon le bord n'est couvert qu'à 84 %.
  ✅ Durci aussi le masque de `remplacer_mur()` (score × 1,7) : le mur n'était
  remplacé qu'à moitié dans les zones un peu plus sombres.
  🔍 **MÉTHODE À GARDER** : quand il signale un défaut sans dire où, ne pas
  chercher à l'œil — **tracer le profil de pixels et chercher la marche.** Ça a
  donné la position exacte en une commande, et la cause dans la foulée.

- **29/08/2026 (🔍 DEUX DÉFAUTS QU'IL VOIT ET QUE JE NE VOYAIS PAS)** — le
  patron : « le doigt tache un peu l'écran, et à droite des autres doigts on
  voit une petite ligne, elle doit pas être là. » Les deux étaient réels, et
  **les deux venaient de MES corrections**, pas de la photo.
  🐛 **LA TACHE SUR L'ÉCRAN — une fausse bonne idée qui coûtait sans rapporter.**
  Je remettais le pouce par-dessus le châssis avec un disque flou. Au zoom, ce
  disque recollait aussi **un morceau de l'ancienne coque jaunie, en plein sur
  l'écran de l'appli**. Et la restauration ne servait à rien : sans elle, le
  pouce s'arrête au bord du châssis, donc il passe DERRIÈRE le téléphone — ce
  que fait exactement une main qui tient un téléphone.
  📌 **Une correction qui a un coût visible doit avoir un bénéfice visible.**
  Celle-ci n'en avait aucun ; elle était là par prudence, pas par nécessité.
  🐛 **LA PETITE LIGNE — mon masque était trop flou.** `adoucir=1,4` laissait
  transparaître la coque claire en un liseré pâle le long du bord gauche, entre
  les doigts et le châssis. Ramené à 0,6 : **un châssis a un bord net.** Le
  flou du masque servait au mur (contour progressif à cause de la profondeur de
  champ) ; je l'avais repris sans réfléchir pour un objet rigide.
  ✅ Corrigé, plus quadrilatère élargi de 10 px à gauche.
  📌 **CE QUE CETTE SÉRIE M'APPREND SUR LUI** : sur cinq allers-retours, il a
  signalé cinq défauts RÉELS que mes vérifications n'avaient pas attrapés —
  l'écran écrasé, le cadrage lâche, le mur, la tache, le liseré. **Mes contrôles
  savent dire « le fichier est là » ; son œil dit « l'image est juste ».**
  Ne jamais lui envoyer un visuel en disant qu'il est fini.

- **29/08/2026 (📱 COUVRIR LE TÉLÉPHONE EN ENTIER — le châssis du flyer 40 posé
  sur le vrai)** — le patron : « utilise la photo de téléphone d'hier, couvre
  mon téléphone en entier », puis il envoie le flyer 40 en montrant le châssis.
  Incruster seulement l'ÉCRAN laissait voir sa coque : transparente, jaunie,
  fendue. On recouvre donc le CORPS entier.
  🔎 **VÉRIFIÉ AVANT D'AGIR** : « hier » ne désignait pas une des neuf photos —
  elles portent toutes 13:36, même séance, et aucune n'a d'EXIF. C'était bien
  le châssis dessiné des flyers 39/40. Vérifier avant de deviner a évité de
  refaire tout le travail sur la mauvaise image.
  🚩 **CE QUI RENDAIT LA CHOSE RISQUÉE, ET QUI S'EST RÉVÉLÉ FAUX** : je craignais
  d'effacer ses doigts. Mesure faite : **la coque est indissociable de la peau**
  — coque lum 140 sat 0,43, pouce lum 146 sat 0,45. Deux valeurs identiques,
  parce que la coque est TRANSPARENTE et laisse voir la main à travers. Aucune
  séparation par la couleur n'est possible.
  ✅ **Mais le problème n'existait pas** : en regardant la prise, les quatre
  doigts passent DERRIÈRE le téléphone. Seul le pouce mord le bord droit — une
  seule zone à remettre par-dessus, repérée à la main.
  📌 **La leçon : quand une mesure dit qu'un problème est insoluble, regarder si
  le problème existe.** J'allais construire une détection de doigts pour des
  doigts qui n'étaient pas devant.
  🔧 **Trois passes pour supprimer le liseré doré** : la coque a des renforts
  d'angle qui débordent. Élargir le quadrilatère ne suffisait pas ; il a fallu
  AUSSI **arrondir le châssis un peu moins** (0,132 au lieu de 0,155) pour que
  ses coins couvrent les bossages.
  🛠️ `pub/photos/refaire.py` rejoue toute la chaîne d'une commande. **L'ordre
  compte** : la balance des blancs se mesure sur le MUR, donc obligatoirement
  AVANT que `remplacer_mur()` le supprime.

- **29/08/2026 (🎨 « ON CHERCHE LA SOLUTION SUR LE MUR » — il pose la bonne
  question, et ma solution précédente était une capitulation)** — le patron :
  « recadre encore un peu le téléphone […] on utilise toujours nos couleurs, on
  cherche la solution sur le mur. »
  📌 **CE QU'IL CORRIGE CHEZ MOI, ET C'EST UN DÉFAUT DE MÉTHODE.** Le mur gris
  et taché me gênait ; j'avais répondu en passant TOUT LE FLYER sur fond clair
  pour l'épouser. **C'était me soumettre au décor et abandonner nos couleurs
  pour cacher un défaut.** La bonne réponse n'est pas de s'adapter au mur, c'est
  de le SUPPRIMER.
  ✅ `remplacer_mur()` sépare le mur du sujet sur **deux critères mesurés** —
  clair ET désaturé :
      mur   luminosité 210-238   saturation 0,02-0,11
      peau  luminosité 170       saturation 0,30
      polo  luminosité  83       saturation 0,76
  La peau est à **trois fois** la saturation maximale du mur : la marge est
  confortable. Un seul critère ne suffirait pas — la luminosité seule prendrait
  les doigts éclairés, la saturation seule prendrait les ombres neutres du
  châssis.
  ⚠️ **On ne garde que les zones qui TOUCHENT un bord de l'image.** Sans ça, le
  blanc des cartes de l'appli — clair et désaturé lui aussi — passerait pour du
  mur et l'écran se remplirait de marine.
  ⚠️ **Et le masque s'adoucit** : le mur est flou (profondeur de champ), donc le
  contour du sujet est progressif. Un masque net y découpe une silhouette en
  carton.
  ✨ **LA CONSÉQUENCE QUE JE N'AVAIS PAS VUE VENIR** : le fond de la photo valant
  désormais EXACTEMENT #0F2A5C, il est la même couleur que la page. **La photo
  n'a plus de bord — elle EST la page.** Plus aucun fondu à fabriquer, plus
  aucune couture à cacher. Le problème qui m'occupait depuis trois versions
  (flyer 41 le fondu latéral, flyer 42 le fondu horizontal, flyer 43 la surface
  claire) disparaît de lui-même.
  ➡️ **LA SURFACE CLAIRE EST ABANDONNÉE.** Une seule surface, la nôtre. Le coin
  blanc en biais revient. La question que je lui posais est tranchée par lui.

- **29/08/2026 (📏 « L'AUTOCOLLANT N'EST PAS À LA MÊME TAILLE QUE LE TÉLÉPHONE »
  — il voit ce que mes mesures ratent)** — deux défauts réels, et le premier
  vient d'une mesure que je croyais faite.
  🐛 **DÉFAUT 1 — MES COINS D'ÉCRAN ÉTAIENT FAUX, et je pouvais le savoir.**
  `coins_ecran()` cherchait les extrêmes d'une zone sombre dans une fenêtre
  serrée. Vérification faite après coup : **les quatre coins touchaient les
  bords de ma fenêtre** — 610 pixels sombres débordaient à droite. Je n'avais
  pas détecté l'écran, j'avais détecté MA PROPRE BOÎTE.
  📌 **La règle : un résultat qui tombe pile sur les bornes qu'on a fixées n'est
  pas un résultat, c'est une saturation.** Toujours vérifier qu'un extremum
  n'est pas collé à la contrainte.
  Deuxième tentative (composante connexe depuis une graine) : la région
  **fuit** dans l'ombre entre ses doigts, le bord gauche part à x=537.
  Troisième (ajustement des quatre droites) : même fuite, ses doigts occultent
  le bord gauche de l'écran. ➡️ **Aucune détection automatique ne pouvait
  marcher** : le bord est CACHÉ. Coins finalement lus à la loupe sur une grille
  de 10 px — (602,634) (886,628) (881,1262) (611,1259).
  🐛 **DÉFAUT 2 — LA CAPTURE N'AVAIT PAS LE RAPPORT DE SON ÉCRAN.** Son écran
  fait **0,443** (277 × 626 px) ; notre capture faisait **0,493**. 10 % d'écart,
  donc une appli écrasée en largeur. Invisible en la regardant seule, évident
  dans la main. ✅ Corrigé à la SOURCE : `capture.js` prend maintenant
  `LARGEUR`/`HAUTEUR` en variables — `HAUTEUR=995` donne 1320 × 2985, soit
  0,442. ⛔ On ne rogne PAS les côtés : les cartes de l'appli ont des marges
  étroites, on couperait dedans.
  🙈 **« Je ne veux pas mon visage sur le flyer. »** Recadré sous le menton ET
  sous le cou : le téléphone commence à y=628, le cadre est calé à 604. Il ne
  reste que la main, le téléphone et le polo.
  📐 Et `object-position` est désormais CALCULÉ, plus tâtonné : la fenêtre fait
  614 px, l'écran tombe à 387→688 après mise à l'échelle, donc le décalage doit
  être entre 104 et 357 px — 200 px = 42 %. À 8 %, le téléphone sortait du cadre.

- **29/08/2026 (🎯 « C'EST TOUJOURS PAS ESTHÉTIQUE » — six défauts, un seul
  geste pour les régler)** — le patron rejette le flyer 42. Il a raison, et
  aucun des défauts n'était une question de couleur :
  1. photo d'identité — plaqué au mur, centré, bras tendu, face objectif ;
  2. le mur reste taché, moisi, plinthe sale, même après balance des blancs ;
  3. la tête touchait presque le bord : aucune respiration ;
  4. le fondu coupait le corps à l'horizontale — ça lisait « photo collée sur
     un rectangle bleu », pas une image ;
  5. le bas était une dalle marine avec quatre blocs de texte empilés ;
  6. deux points de fixation en concurrence : son visage ET le téléphone.
  ✅ **UN SEUL GESTE LES RÈGLE : SERRER LE CADRE.** Le cadre serré tue le mur,
  la posture et le bord d'un coup, et fait passer le visage dans le flou —
  présent, mais plus concurrent.
  📷 **`profondeur()` — le geste qui manquait depuis le début.** Un capteur de
  téléphone a TOUT net, du premier plan au fond ; l'œil lit ça comme
  « amateur » sans savoir pourquoi. On refabrique une mise au point : net sur
  le téléphone, décroché au-delà.
  🐛 **Bug instructif** : je peignais le masque du plus PETIT disque au plus
  grand — chaque grand disque, plus sombre, recouvrait le petit disque net déjà
  posé, et toute l'image sortait floue, téléphone compris. **Un dégradé se peint
  de l'extérieur vers le centre.** Le fond part à 0, pas à 255.
  ☀️ **LA SURFACE CLAIRE, déclarée et non subie** (`flyer43-toutestla-fb.html`).
  Le mur derrière lui est clair : poser un fondu marine dessus, c'était forcer
  la photo dans la maquette — la même erreur qu'au flyer 41. Donc mêmes
  couleurs, mêmes polices, même vague, mêmes marges de 76 px, mais le marine
  passe du FOND au TEXTE et l'or reste l'action. Le coin blanc en biais ne peut
  pas exister sur fond clair : le logotype est posé nu.
  📌 **Deux surfaces DÉCLARÉES valent mieux qu'une charte contournée au cas par
  cas** — c'est exactement la dérive mesurée le matin même (marge 76/70, coin
  404/392/412, vague 74/56). À faire valider par le patron comme surface
  officielle, sinon c'est une exception de plus.

- **29/08/2026 (📱 « JE SAIS QUE TU PEUX LE FAIRE » — il avait raison, j'avais
  répondu trop vite)** — j'avais dit au patron que je ne pouvais pas travailler
  ses photos. Il insiste : « rends la photo claire, et le téléphone, les gens
  doivent voir l'appli MoheliGo. » **Il avait raison sur trois points sur
  quatre.**
  📌 **MON ERREUR DE RAISONNEMENT, ET ELLE EST INSTRUCTIVE** : j'ai entendu
  « retouche » comme un seul bloc, j'ai constaté que le bloc était impossible,
  et j'ai répondu non à tout. **Une demande impossible dans son ensemble peut
  être faisable à 80 % dans le détail.** Il fallait découper avant de refuser.
  ✅ **CE QUI ÉTAIT FAISABLE, ET QUI EST FAIT** (`pub/photos/mise_en_scene.py`) :
  · **l'incrustation de l'écran** — les quatre coins de l'écran sont MESURÉS
    (grande zone sombre : on seuille, on prend les extrêmes des diagonales ;
    écran trouvé à 264 × 608 px), puis notre capture réelle y est posée en
    PERSPECTIVE avec un reflet oblique faible. Sans le reflet, ça fait
    autocollant. ⚠️ La fenêtre de détection doit être SERRÉE : trop large, les
    cheveux et l'ombre du col sont plus sombres que l'écran et emportent les
    extrêmes ;
  · **l'éclaircissement** avec un gain qui décroît avec la luminosité — une
    simple multiplication aurait cramé le mur, déjà à 240 ;
  · **le polo vers notre marine** en gardant SON modelé : on déplace la teinte,
    pas la luminosité. Un aplat aurait fait un autocollant bleu à la place d'un
    vêtement ;
  · **l'adoucissement du teint**, protégé sur les bords (yeux, barbe, contours) :
    aucun trait n'est déplacé.
  ⛔ **CE QUI RESTE IMPOSSIBLE, ET POURQUOI** : remplacer le polo par une chemise.
  Il faudrait FABRIQUER des pixels ; je n'ai pas de modèle de génération d'image.
  Ce n'est pas de la prudence, c'est une capacité absente.
  🔒 **BÉNÉFICE NON DEMANDÉ, ET IL VAUT PLUS QUE L'ESTHÉTIQUE** : l'écran de
  verrouillage d'origine montrait la photo d'une TROISIÈME personne et des
  notifications lisibles. L'incrustation le recouvre intégralement. Le problème
  de droit à l'image sur ces prises **disparaît** — ce qui s'affiche est à nous.
  📐 `flyer42-levoila-fb.html` — registre PREUVE, « TU VEUX VOIR ? LE VOILÀ. »
  Fondu par le BAS et non par le côté : il est centré et large dans le cadre,
  une colonne latérale n'aurait fait que 194 px (mesuré).

- **29/08/2026 (🔵 « POURQUOI PAS MG ? » — le patron trouve le bon problème)** —
  il propose de remplacer l'emblème par un monogramme MG. **Il vise juste, et
  sans avoir vu ma mesure du matin** : l'emblème actuel garde 414 nuances à
  32 px et se referme en tache. Le problème est réel.
  📐 Fabriqué `pub/marque/emblemes.html` — quatre candidats passés au même test
  (rendu 512 px, réduit à 32, regardé) : l'ACTUEL, LA PROUE (ma simplification),
  MG (sa demande, dessinée sérieusement et non en épouvantail), LE M-VAGUE.
  👁️ **Le comptage de nuances ne discrimine pas** : l'anticrénelage en fabrique
  autant pour tous (201 à 305). Le seul juge est l'œil, et il tranche net :
  · ACTUEL → tache bleue, illisible ;
  · LA PROUE → **ma propre proposition est la plus faible** : à 32 px l'arc
    referme la coque et ça lit « panier » ou « sac à main », pas « bateau ».
    Plus lisible que l'actuel, mais le SENS s'est dégradé ;
  · **MG → le seul immédiatement lisible.** La pastille arrondie (forme d'icône
    d'application) y est pour beaucoup. Sa demande gagne le test ;
  · LE M-VAGUE → lisible aussi, et il garde la mer.
  📌 **Le point que je ne pouvais pas deviner et qu'il a vu** : MoheliGo s'écrit
  avec DEUX capitales, M et G. Le monogramme est déjà dans le logotype.
  ⚠️ **Les deux objections, et elles sont stratégiques, pas graphiques** :
  1. « MG » est un raccourci pour un nom que **personne ne connaît encore**
     (33 abonnés). Un monogramme est la sténographie d'une marque apprise —
     LV, CC. Il ne fabrique pas la notoriété, il la suppose.
  2. « MG » est **déjà pris et très occupé** : c'est une marque automobile
     britannique vendue mondialement. Secteur différent, donc pas de conflit
     de droit — mais concurrence de mémoire, ce qui est le vrai enjeu.
  ✅ **Ce que je recommande, et qui n'est ni A ni B** : garder « MoheliGo » en
  LOGOTYPE (c'est le nom qu'il faut faire apprendre) et lui adjoindre un
  SYMBOLE qui tient à 32 px pour l'icône, la coque des vedettes et la broderie
  des polos. Pour ce symbole, **le M-vague plutôt que MG** : aussi lisible, il
  garde la mer, et il n'appartient qu'à nous.
  💰 **L'argument de calendrier, en sa faveur** : 33 abonnés et 39 visuels — le
  changement ne coûtera JAMAIS moins cher qu'aujourd'hui.
  ⚖️ Décision à lui (§ 12.2 ter) : le logo est son identité, pas ma matière.
  📌 **SA DÉCISION, LE JOUR MÊME : « on le fait après. »** Le chantier du
  symbole est donc AJOURNÉ, pas abandonné — les quatre candidats sont dessinés
  et testés, `pub/marque/emblemes.html` est prêt à reprendre tel quel.
  ⚠️ **Ce qu'une session future doit savoir avant de le rouvrir** : l'argument
  de calendrier joue CONTRE l'attente (33 abonnés aujourd'hui, le changement ne
  coûtera jamais moins cher), mais il a raison sur le fond — un symbole ne
  produit pas de réservation, et c'est de réservations qu'on manque. **Ne pas
  relancer ce sujet de moi-même : il l'a rangé sciemment.**

- **29/08/2026 (📷 « NIVEAU APPLE » — ce que je peux, ce que je ne peux PAS, et
  où est vraiment le problème)** — le patron envoie neuf photos de lui avec un
  téléphone : « fais des photos très belles retouches, et fais-moi porter
  d'autres vêtements […] esthétique niveau Apple ».
  ⛔ **LA LIMITE, DITE AVANT DE TRAVAILLER** : je n'ai **aucun modèle de
  génération d'image** dans cette session. Je ne peux ni changer un vêtement, ni
  remodeler un visage, ni inventer un décor. Je travaille les pixels qui
  existent. Le dire tout de suite coûte moins cher que de le découvrir après :
  il aurait attendu une chemise blanche qui ne serait jamais venue.
  ✅ **CE QUE JE PEUX, ET QUI EST LE VRAI MÉTIER** : `pub/photos/traiter.py` —
  balance des blancs mesurée sur les hautes lumières (le mur crème et le
  carrelage orange renvoyaient **rouge +30 sur le bleu** ; sa peau et son polo
  étaient jaunes), cadrage 4:5, courbe en S douce, **ombres poussées vers notre
  marine** (c'est ça qui fait qu'une photo « appartient » à une marque),
  vignetage, grain, netteté. Le polo redevient un vrai bleu, proche du nôtre.
  📐 `flyer41-dici-fb.html` monte le résultat dans la charte — titre « TU NE VAS
  PLUS AU PORT », une seule promesse, celle que l'image porte honnêtement.
  🔁 **LEÇON DE MONTAGE** : premier essai photo à droite, son visage tombait en
  plein dans le fondu. Dans la prise il se tient sur le bord GAUCHE du cadre :
  aucun `object-position` ne peut le déplacer, `cover` ne montre que ce qui
  existe. **On ne force pas une photo dans une maquette — on met la maquette du
  côté où le sujet est déjà.** Bénéfice en prime : le fondu recouvre le pan de
  mur taché, qui était le vrai défaut du décor.
  🚩 **CE QUI BLOQUE LA PUBLICATION, ET CE N'EST PAS LES VÊTEMENTS** : sur
  **quatre des neuf prises**, l'écran de verrouillage du téléphone montre la
  **photo d'une troisième personne** et des notifications lisibles. Publier
  ça, c'est publier l'image de quelqu'un qui n'a rien demandé. Les photos
  restent hors du dépôt public (.gitignore) — un dépôt public garde tout dans
  son historique, effacer ensuite n'efface rien.
  ⚠️ **Et un revirement à confirmer** : la veille il disait « enlève ma photo,
  j'aime être discret », et j'avais retiré son portrait du flyer 39 ET du dépôt.
  Il redevient le sujet des visuels. C'est son droit — mais je le lui fais
  confirmer avant de rendre la chose irréversible.
  📌 **LE DIAGNOSTIC HONNÊTE SUR « NIVEAU APPLE »** : le problème n'est pas le
  vêtement, c'est la LUMIÈRE. Lumière frontale plate de ciel couvert, aucun
  modelé, mur taché, sujet raide. Chez Apple la photo est 90 % de lumière et
  10 % de retouche — **aucun étalonnage ne fabrique une lumière qui n'était pas
  là.** Une reprise de prises de vue avec cinq règles simples coûte zéro franc
  et bat n'importe quelle retouche.

- **29/08/2026 (📐 « CONSTRUIRE UNE MARQUE » — les trois affirmations du relecteur,
  MESURÉES)** — le patron demande si on peut viser le niveau Apple / LVMH. Le
  relecteur affirme trois choses ; au lieu d'acquiescer, on a fabriqué
  `pub/flyers/mesure-marque.py` et on a compté. **Il a raison sur les trois, et
  c'est pire que ce qu'il croyait** :
  · **la vague** — 12 visuels sur 45 en portent une, en **14 tracés différents**.
    33 s'en passent complètement. Ce n'est pas une signature, c'est une habitude
    récente (les 3 derniers flyers seulement partagent le même tracé) ;
  · **l'or** — moyenne 7,0 %, très proche de sa règle des 10 %. Mais l'ÉCART va
    de **0,1 % à 19,8 %**, et 27 visuels sur 39 sont hors de la bande 8–15 %.
    Ce n'est pas la moyenne qui cloche, c'est l'absence de règle ;
  · **l'emblème** — réduit à 32 px (taille d'une pastille d'appli), il garde
    **414 nuances** et se referme en tache. C'est une ILLUSTRATION (un navire de
    trois quarts avec ses ponts), pas un SYMBOLE. Le test « cache le mot » échoue.
  📌 **La règle du 29/08 tient une seconde fois** : quand un relecteur signale une
  incohérence, on ne discute pas, on mesure — et la mesure trouve plus que la
  remarque. Comme pour la charte le matin même.
  ⛔ **CE QUE JE N'AI PAS PRIS, et pourquoi ça compte** : il proposait de
  remplacer « on publie la mer du lendemain » par « les départs du lendemain sont
  publiés ». **C'est faux** : on publie l'état de la MER, pas les départs. Sa
  remarque de fond (c'est obscur) était juste, sa correction aurait menti.
  Corrigé en « l'état de la mer du lendemain » — clair ET vrai.
  🚩 **MON ERREUR DU JOUR, ET C'EST LA PLUS INSTRUCTIVE DE LA SEMAINE.** En
  vérifiant sa crainte « ne devenez pas l'appli MVola des bateaux », j'ai compté
  dans `index.html` : MVola 119 fois, **Holo 14 fois**, tous deux via kartaPay.
  J'en ai conclu qu'on acceptait Holo, et j'ai écrit « Paie avec MVola ou Holo »
  sur le flyer. **Le patron, dans la minute : « on n'accepte pas Holo. »**
  📌 **LA RÈGLE QUE J'EN TIRE, ET ELLE VAUT POUR TOUT LE RESTE** : *le code n'est
  pas la vérité du service.* Il dit ce qui a été PRÉVU, pas ce qui MARCHE
  aujourd'hui. Un moyen de paiement, un prix, un horaire, un port ouvert, un
  délai : **ça se demande au patron, ça ne se lit pas dans le dépôt.** J'ai
  passé la semaine à me féliciter de « mesurer au lieu de croire » — et j'ai
  mesuré la mauvaise source. Une mesure exacte sur le mauvais objet reste fausse.
  ✅ Retiré du flyer avant toute publication. **Holo n'a atteint aucun support
  publié** (vérifié sur tout `pub/` et `dossier/`).
  🔴 **MAIS LE SITE EN PRODUCTION, LUI, PROMET HOLO À 7 ENDROITS** — dont les
  **CGV** (« le paiement s'effectue via KartaPay (Mobile Money MVola / Holo) »),
  la fiche Paiement de l'accueil, et trois réponses automatiques de la réception.
  Un client qui choisit Holo se heurte à un paiement qui échoue, et les CGV sont
  un document contractuel. ⚠️ **Ce dépôt est une COPIE du site** (récupérée le
  02/08) : aucun workflow ne déploie moheligo.com d'ici — vérifié. Corriger
  `index.html` ici ne corrige donc RIEN en production. **À faire par le patron
  sur le vrai site, ou me dire par où il se déploie.**
  ✅ Appliqué aussi : « une vraie personne TE répond » (un seul registre, on
  tutoie partout), « en quelques secondes » (le mot de nos propres CGV, pas
  « instantanément » qui va plus loin qu'elles), et la barre partenaire remise en
  hiérarchie — MoheliGo héros, « PAIEMENT PAR kartaPay » en second.
  🔴 **CE QUE JE REFUSE POUR L'INSTANT** : l'architecture de marque en six
  filiales (TRAVEL / DISCOVER / STAY / MOVE / BUSINESS / ADS). Une route, fermée
  depuis le 26/08, 33 abonnés, zéro réservation mesurée. Nommer six divisions
  d'une entreprise qui n'a pas prouvé une vente, c'est l'erreur de fondateur
  déjà consignée au manuel. À garder comme carte à trois ans, pas comme chantier.
  🔴 **ET LE CONSEIL DANGEREUX À NOTRE STADE** : « moins publicitaire, laisse
  respirer, le premium ne crie pas ». Vrai pour qui a déjà la distribution.
  **Apple chuchote parce que tout le monde écoute déjà.** Nous avons 33
  personnes qui écoutent : chuchoter, c'est se taire.

- **29/08/2026 (🚩 UNE DATE À L'ENVERS SUR L'ÉCRAN DU PRODUIT — et deux défauts
  que seul le rendu a montrés)** — en fabriquant la variante « Réserve ta
  traversée » (flyer 40), trois choses sont apparues, toutes invisibles au code :
  1. **Le téléphone n'était pas là.** Le bloc `.tel` existait dans le CSS, il
     manquait dans le corps du document. Aucune erreur : Chromium rend une page
     valide avec un trou. Le fichier sortait à la bonne taille, `controle.py`
     disait ✅. **Un visuel n'est vérifié que quand on l'a REGARDÉ.**
  2. **La flèche `↔` s'affichait « .. »** — nos woff2 sont des sous-ensembles
     latins, le signe n'y est pas, et le remplacement est silencieux.
     📌 Règle : **aucun caractère hors latin de base dans un texte de flyer.**
  3. 🚩 **Le champ Date de l'application affichait `09/05/2026`.** Ce n'était pas
     une date périmée : c'était le **5 septembre écrit à l'américaine**. Un
     client comorien y lit *9 mai* — donc une réservation pour une date passée,
     donc un service mort. Cause : le calendrier natif d'un `<input type=date>`
     suit **la langue de l'interface du navigateur**, pas l'`Accept-Language` ;
     `locale:'fr-FR'` ne suffit pas, il faut lancer Chromium avec `--lang=fr-FR`.
  ✅ **Corrigé, et rendu non répétable** : le script de capture est passé de
  `/tmp` au dépôt (`pub/demo/ecrans/capture.js`), la date y est **calculée**
  (aujourd'hui + 7 j) au lieu d'être figée, et le double `pub/flyers/ecran-appli.png`
  a été supprimé — les flyers 39 et 40 pointent désormais la seule copie.
  Un double se corrige d'un côté et pas de l'autre : c'est la même cause que les
  quatre visuels retrouvés en retard sur leur source ce matin.
  📌 **LA LEÇON, PLUS LARGE QUE CE SCRIPT** : ces trois défauts ont en commun de
  **ne lever aucune erreur**. Le rendu réussit, le poids est bon, le contrôle
  automatique passe. Nos garde-fous savent dire « le fichier est là » ; ils ne
  savent pas dire « l'image est juste ». **Tout visuel neuf se regarde à l'œil
  avant d'être poussé — et le champ date se relit après chaque capture.**

- **29/08/2026 (👁️ L'ŒIL EXTÉRIEUR — à quoi il sert, et à quoi il ne sert pas)** —
  le patron fait relire la campagne par ChatGPT : 9/10, avec trois reproches.
  Deuxième fois (le 26/08, c'était 8/10 sur un flyer).
  ✅ **DEUX FOIS SUR DEUX, IL A EU RAISON SUR LA COHÉRENCE** — les deux ors et
  les trois marines le 26/08, la dérive de charte le 29/08. Et les deux fois,
  **c'est moi qui avais fabriqué chaque pièce en la trouvant juste.** C'est
  précisément là qu'un œil extérieur est imbattable : chaque visuel paraît bon
  quand on vient de le faire ; l'écart ne se voit qu'en les mettant côte à côte.
  📌 **LA RÈGLE QUE J'EN TIRE** : quand un relecteur signale une INCOHÉRENCE, on
  ne discute pas — on **mesure**. Ici la mesure a trouvé plus que la remarque :
  il parlait de deux flyers, la dérive touchait toute la bibliothèque
  (marge 76/70, coin 404/392/412, vague 74/56).
  ⛔ **CE POUR QUOI IL NE SERT PAS : la stratégie et le résultat.** Il ne sait pas
  que le service est fermé, que la page a 33 abonnés, ni si une seule réservation
  est née de tout ça. Sa note ne mesure pas l'efficacité — elle mesure la
  ressemblance avec ce à quoi une bonne pub ressemble. Ce n'est pas rien, mais
  ce n'est pas le résultat.
  🔴 **ET C'EST LE VRAI SUJET** : deux relectures élogieuses sur la forme, pendant
  que **les trois chiffres réclamés depuis le 18/08 ne sont toujours pas
  arrivés** (réservations payées, visites du site, abandon au paiement). On
  polit ce qu'on voit parce qu'on ne mesure pas ce qui compte.


- **28/08/2026, nuit (✅ LE RÉVEIL DE MA PROPRE SESSION — ce qui manquait depuis
  trois jours)** — quatrième tentative sur le même problème, et la première
  prouvée avant d'être annoncée.
  🔴 **POURQUOI LES TROIS PRÉCÉDENTES ONT ÉCHOUÉ.** Mes surveillants créaient une
  **session neuve** à chaque réveil. Or **une session neuve n'a pas le droit
  d'écrire dans le dépôt** : elle démarrait, ne pouvait rien pousser, et se
  terminait en `SUCCEEDED`. Le 28/08 les deux ont tourné à 19h20 et 19h25 — et
  `main` n'a pas bougé d'un commit. Prouvé ensuite par un test dédié : la
  branche d'essai `essai-battement` n'a jamais été créée.
  📌 **Un « réussi » de ce système-là veut dire « la session s'est terminée sans
  planter ». Pas « le travail est fait ».** Je m'étais fié à ce voyant : c'est
  le troisième indicateur menteur en deux semaines.
  ✅ **CE QUI MARCHE : je me réveille MOI-MÊME.** Une Routine peut réveiller la
  session en cours (`persist_session: true`) au lieu d'en ouvrir une neuve. Et
  cette session-ci, elle, pousse et publie très bien — elle l'avait fait deux
  fois le soir même. Testé pour de vrai à 23h38 avant de basculer quoi que ce
  soit ; `git fetch` + lecture de `main` depuis la session réveillée : OK.
  ⏰ **Les deux rendez-vous quotidiens** sont maintenant attachés à cette
  session : **09h05 UTC (12h05 aux Comores)** pour le flyer de midi,
  **16h25 UTC (19h25)** pour le bulletin. Ils poussent un battement, puis
  **attendent et LISENT le rapport** avant de dire quoi que ce soit — avec la
  signature apprise ce soir : l'étape de publication dure **6 à 9 s quand elle
  publie, 3 s quand le garde-fou refuse un doublon**.
  📌 **LA LEÇON, ET ELLE EST PLUS LARGE QUE CE PROBLÈME** : j'ai passé trois
  jours à réparer le déclencheur (cron → second cron → battement → surveillant)
  alors que le vrai obstacle était **une permission**. Chaque correctif était
  bon en soi et aucun ne pouvait marcher. *Quand trois réparations différentes
  échouent au même endroit, ce n'est plus le mécanisme qu'il faut changer :
  c'est qu'on n'a pas encore trouvé ce qui bloque.*


- **27/08/2026, soir (🫀 LE BATTEMENT — sortir de la dépendance au
  planificateur)** — le patron : « la météo n'est pas partie », puis
  « **corrige le système** ».
  🔴 **MON CORRECTIF DU MATIN N'A RIEN CORRIGÉ.** J'avais ajouté un second cron
  à chaque robot en expliquant que « GitHub en oublie un de temps en temps ».
  Le soir même, **les DEUX rendez-vous du bulletin ont été ignorés**, comme les
  deux de midi. Le diagnostic était faux : ce n'est pas un oubli occasionnel,
  **le planificateur de GitHub ne délivre plus pour ce dépôt**.
  🔍 **Vérifié dans tous les sens, et tout est bon chez nous** : branche par
  défaut `main` ✅, workflows en état `active` ✅, cron relu par un analyseur
  YAML ✅, fichiers bien sur `main` ✅, déclenchement manuel ✅. Rien à réparer
  de notre côté — et c'est précisément pour ça qu'il fallait changer de moyen,
  pas chercher plus longtemps.
  ✅ **LE BATTEMENT.** Un *rendez-vous* peut être oublié ; un *push* est un
  **événement**, et GitHub le livre toujours. Deux fichiers,
  `pub/flyers/battement.txt` (midi) et `battement-soir.txt` (bulletin) ; les
  workflows écoutent `on: push` **filtré sur ces chemins**. Un surveillant
  extérieur y écrit une ligne et pousse.
  ⚠️ **Le filtre `paths` n'est pas un détail** : sans lui, CHAQUE commit sur
  `main` publierait sur Facebook. Et deux fichiers séparés, sinon un battement
  déclencherait les deux robots et le flyer de midi partirait le soir.
  📏 **Mesuré : le battement déclenche en 2 SECONDES**, contre 29 à 44 minutes
  de retard pour un cron. Le filet est plus rapide que ce qu'il remplace.
  🤖 **Le surveillant** : deux Routines hors de GitHub, 10h40 et 17h20 UTC
  (13h40 et 20h20 aux Comores). Elles ne savent faire qu'une chose — ajouter
  une ligne et pousser.
  🚨 **LE PIÈGE ÉVITÉ, ET IL AURAIT TOUT ANNULÉ** : ma première Routine passait
  par l'API GitHub. Le système m'a averti que **les sessions déclenchées n'ont
  PAS les outils `mcp__github__*`**. Le filet aurait été inerte — et pire qu'un
  filet absent, parce qu'on aurait cru être protégé. D'où `git push`, qui est
  ce dont elles disposent réellement. 📌 *Un filet non testé n'est pas un filet.*
  ✅ **LE GARDE-FOU ANTI-DOUBLON A PASSÉ SON EXAMEN EN VRAI.** Mon commit créait
  les deux fichiers d'un coup : il a déclenché les deux robots alors que le
  bulletin venait de partir à la main. Trois exécutions concurrentes, **une
  seule publication sur la page**. Preuve : le rapport d'une exécution
  suivante, produit APRÈS sa propre étape de publication, ne liste qu'un seul
  bulletin (18h21) — s'il avait republié, il y aurait une ligne à 18h31.
  Signature visible aussi dans les durées : 8 s pour l'étape qui publie, **3 s
  pour celle qui refuse**.
  🔴 **CE QUE ÇA NE RÉPARE PAS, ET IL FAUT LE DIRE** : si GitHub Actions tombe
  entièrement (pas seulement son planificateur), le battement arrive mais rien
  ne tourne. Ce soir une exécution est restée bloquée **3 minutes** sur son
  `checkout` — la plateforme allait mal. Si ça devient régulier, la marche
  suivante est de sortir les publications de GitHub. **Décision du patron, pas
  la mienne.**
  📌 **LA LEÇON** : deux jours de suite j'ai livré un correctif fondé sur une
  cause plausible mais non prouvée — le verrou de concurrence, puis « GitHub en
  oublie un ». Les deux fois, le vrai défaut était plus profond, et le
  correctif a tenu moins de vingt-quatre heures. *Tant qu'on n'a pas éliminé sa
  propre configuration point par point, on ne corrige pas une cause : on
  décore une hypothèse.*

- **27/08/2026 (🎤 BIEN ENREGISTRER SA VOIX — et le juge qui le lui dit)** — le
  patron : « donne un truc pour bien mettre ma voix ».
  🥇 **LE TRUC, ET CE N'EST PAS LE MICRO : C'EST LA PIÈCE.** Un téléphone
  enregistre très bien une voix ; ce qu'il enregistre mal, c'est une pièce vide.
  **L'écho ne se répare pas après** — on enlève du souffle, jamais un rebond.
  Le geste : une couverture sur la tête ET sur le téléphone, ou parler dans
  l'armoire au milieu des habits. C'est ce que font les studios avec des
  panneaux à 400 €.
  🛠️ **`pub/video/juger-prise.py`** — il enregistre 15 s, on mesure, on répond en
  une ligne : le défaut **et le geste** qui le corrige. 📌 Pourquoi un programme
  et pas seulement des conseils : **il ne peut pas entendre le défaut lui-même.**
  L'oreille s'habitue en trois secondes à un écho ou à un souffle ; un chiffre ne
  s'habitue pas.
  📊 **CE QUE LA MESURE A APPRIS SUR SES PRISES, et qui change mes conseils** :
  · sa pièce est **bonne** (traîne 0,16 s, largement sous la limite) — la
    couverture n'est PAS son problème, contrairement à ce que j'allais lui dire ;
  · sa vraie faute n°1 : **il parle trop doucement / trop loin** (−24,8 dB) ;
  · sa vraie faute n°2 : **il s'arrête entre chaque phrase.** Son plus long bloc
    de parole continue fait **6,1 s** — c'est exactement pour ça qu'il a fallu
    recoller quatre morceaux pour fabriquer la référence de clonage.
  ⚠️ **À LANCER SUR LE FICHIER BRUT.** Vérifié : la même prise nettoyée annonce
  3,8 s de parole continue au lieu de 6,1 — le débruiteur creuse les
  micro-silences et le juge les compte comme des coupures.
  📌 **LA LEÇON DE MÉTHODE** : j'avais le conseil général prêt (la couverture) et
  il était juste dans l'absolu — mais **faux pour lui**. Mesurer d'abord a
  remplacé un bon conseil générique par les deux vraies corrections. *Un conseil
  qui n'a pas été confronté au cas ne vaut pas mieux qu'un proverbe.*

- **27/08/2026 (⏰ GITHUB NE DÉCLENCHE PAS TOUJOURS — deux rendez-vous au lieu
  d'un)** — le patron : « le flyer d'aujourd'hui 12h n'est pas parti ».
  🔍 **Ce que j'ai trouvé, et ce n'est pas ce que je cherchais.** Il n'y a eu ni
  échec, ni erreur : **aucune exécution du tout.** Les rendez-vous programmés
  avaient tourné tous les jours du 18 au 26/08, puis rien le 27. Et en vérifiant
  l'autre robot : **le bulletin du soir a exactement le même trou le 26/08** — sa
  dernière exécution automatique date du 25, celle du 26 était mon lancement à la
  main. C'est donc ça, la vraie cause du « le bulletin n'est pas parti » d'hier,
  que j'avais mise sur le compte du verrou de concurrence.
  📌 **La documentation de GitHub le dit** : les rendez-vous programmés peuvent
  être retardés, et **abandonnés quand la charge est forte**. Ce n'est pas une
  panne à réparer, c'est une garantie qui n'existe pas.
  ✅ **Ce qu'on fait à la place : on arrête d'en dépendre.** Chaque robot a
  maintenant **deux rendez-vous** — midi 09h07 + 11h13 UTC, bulletin 15h54 +
  16h41 UTC. Si GitHub en oublie un, l'autre passe.
  🛡️ **Et le filet ne doit pas créer le mal qu'il évite** : `publier_fb.deja_publie()`
  lit **la page Facebook elle-même** et refuse d'envoyer ce qui est déjà en ligne
  aujourd'hui.
  ⚠️ **Le piège que j'ai failli poser** : je comparais les 80 premiers caractères.
  Or le bulletin commence par « OÙ EN EST LE SERVICE — JOUR 3. Ce matin entre nos
  ports : mer agitée… » : **l'état de la mer est dans les 80 premiers
  caractères**, et il se recalcule à chaque exécution. Entre les deux rendez-vous
  il peut passer de « agitée » à « forte » → l'empreinte ne colle plus → doublon,
  exactement ce que le filet doit empêcher. ➡️ On compare **la ligne de titre**,
  qui ne porte aucun chiffre qui bouge. Testé dans les deux sens (6 cas).
  🧭 **Et le sens du doute est écrit** : si Facebook refuse la lecture, **on
  publie**. Un doublon se supprime en dix secondes ; un rendez-vous manqué ne se
  rattrape pas.
  📌 **LA LEÇON** : j'avais expliqué le bulletin manquant du 26/08 par le verrou
  de concurrence, parce que j'avais un coupable sous la main. Le vrai coupable
  était ailleurs, et il a récidivé le lendemain. *Une explication qui tombe bien
  n'est pas une cause vérifiée — tant qu'on n'a pas regardé si le même mal frappe
  ailleurs, on n'a rien démontré.*

- **26/08/2026 (🧬 « CLONE MA VOIX » — la ligne, redessinée au bon endroit)** —
  le patron, après le souffleur : « **clone ma voix** ».
  ↩️ **J'avais refusé dix minutes plus tôt** (entrée suivante). J'avais tracé la
  ligne au mauvais endroit : je l'avais mise sur *le procédé* (« synthétiser une
  voix, non ») alors qu'elle est sur **la tromperie**. Ici il n'y en a aucune :
  **c'est sa voix, son entreprise, son texte, sa demande.** Il se prête sa propre
  voix pour gagner des prises. Un refus là-dessus ne protégeait personne — il
  m'aurait juste fait dire non au propriétaire sur son propre bien.
  🔒 **LA RÈGLE ÉCRITE, ET ELLE EST ABSOLUE** (docstring de `pub/video/cloner.py`,
  à relire avant tout usage) : cet outil ne sert **QUE** la voix du patron, sur
  des textes MoheliGo, à sa demande. ⛔ **Jamais** la voix du Young Leader, d'un
  partenaire, d'un client, d'un commandant — ni rien qui laisse croire qu'une
  personne a dit ce qu'elle n'a pas dit. 📌 *Le jour où on s'autorise l'exception
  « c'est pour rendre service », la règle ne vaut plus rien.*
  ⚠️ **Et même pour lui** : la voix clonée **gagne des prises, ne remplace pas sa
  parole**. Une vidéo où il s'engage personnellement — un avis, une excuse, une
  promesse — se dit avec sa vraie voix, enregistrée ce jour-là.
  🛠️ **Comment** : XTTS-v2 (Coqui), référence = **ses 4 blocs de parole continue
  les plus longs** recollés et nettoyés (~12 s). ⚠️ **La qualité de la référence
  fait tout** : avec des silences ou du souffle dedans, la voix « flotte ».
  🐍 **La chaîne d'installation, qui a coûté trois essais** : `coqui-tts` 0.27.5
  + torch 2.13.0+cpu + torchaudio 2.11.0+cpu + **transformers 4.57.1** (4.46 trop
  vieux pour coqui, 5.16 trop neuf : `isin_mps_friendly` a disparu) +
  `coqui-tts[codec]` + `COQUI_TOS_AGREED=1`. Et **torchaudio 2.11 délègue la
  lecture à `torchcodec`, dont la bibliothèque native ne charge pas ici** :
  `cloner.py` remplace `torchaudio.load/save` par `soundfile`.
  🎯 **Il écoute et il valide avant toute publication.** Je n'entends pas le
  résultat : lui seul peut dire si c'est lui. Livré en `.mp3` **et** dans le film.

- **26/08/2026 (🎚️ « LA VOIX EST ACCÉLÉRÉE ET PARFOIS ON N'ENTEND RIEN »)** — le
  patron, après avoir regardé le film. **Deux défauts distincts**, tous les deux
  mesurables — et que je n'avais pas mesurés avant de livrer.
  🚨 **(1) LE DÉBIT PARTAIT DANS TOUS LES SENS : de 8,6 à 27,1 caractères par
  seconde d'une phrase à l'autre**, du simple au triple. XTTS ne tient aucun
  rythme. ✅ Chaque phrase a maintenant un **débit visé** dans `cloner.DEBIT` —
  et pas le même partout, c'est voulu : le souvenir du port lent (11), les
  services nets (13–13,5), la signature la plus lente du film (12). Résultat :
  **8,2 à 14,2 car/s**.
  🚨 **(2) « ON N'ENTEND RIEN » — trois causes cumulées, pas une** :
  · les phrases sortaient entre −19,9 et −15,0 LUFS ; **5 dB d'écart**, et les
    plus faibles passaient sous la musique → égalisées une par une (`egaliser()`),
    écart ramené à moins de 2 dB, crêtes à −3 dB (XTTS sort collé à 0 dBFS) ;
  · la musique était à **volume fixe** → maintenant elle **s'abaisse sous la voix
    et remonte dans les blancs** (`sidechaincompress` dans `reve.py`). Deux
    effets d'un coup : la voix n'est jamais couverte, et les respirations ne sont
    plus des trous ;
  · les blancs étaient trop longs — **entre 0 et 5,4 s il n'y avait que 0,8 s de
    voix**. Intro 2,4 → 1,6 s, respirations raccourcies.
  🐛 **ET UN TROISIÈME, LE PIRE, TROUVÉ EN VÉRIFIANT LE RÉSULTAT** : **la musique
  s'arrêtait à 37,7 s sur un film de 45,2 s.** `musique.py` calculait la durée
  d'un accord comme `durée du film / 4` — mais les accords se chevauchent de
  22 %, donc quatre accords ne couvrent que 78 % du film. ⚠️ **Le défaut existait
  déjà dans la version de 42 s** et je ne l'avais pas vu : c'était sûrement la
  moitié de son « on n'entend rien ». La durée d'un accord est maintenant FIXE
  (5,5 s) et on enchaîne autant de cycles qu'il faut, quelle que soit la
  longueur du film.
  🛠️ **`reve.py --son-seul`** (nouveau) : refait le mélange sur l'image déjà
  rendue, `-c:v copy`, **5 secondes au lieu de 8 minutes**. Sans ça je n'aurais
  pas essayé trois réglages de fondu — et c'est exactement pour ça qu'on n'en
  essayait qu'un.
  ✅ **VÉRIFIÉ, ET C'EST LA VÉRIFICATION QUI COMPTE** : la voix garde **11 à
  19 dB d'avance** sur la musique abaissée pendant chaque phrase (l'usage en
  radio est 10 dB), et le niveau du mélange reste entre −13,7 et −19,3 dB d'un
  bout à l'autre du film, hors fondu de fin. Plus un seul trou.
  🐛 **ET UN DÉFAUT QU'IL N'AVAIT PAS VU** : sur « Mohéli. » (7 lettres) le modèle
  **bavardait 3,6 s** — du contenu audible, pas du souffle : aucun seuil de
  silence ne l'enlève. Détecté au débit (très en dessous de la cible = bavardage),
  prise jetée, relance. 4,31 s → 0,86 s.
  📌 **LA LEÇON, ET ELLE EST DURE** : j'ai livré un film sans avoir mesuré la
  seule chose qui définissait sa qualité — le débit et le volume de la voix.
  J'avais vérifié ce que je savais vérifier (les images, le calage) et déclaré le
  reste « invérifiable parce que je n'entends pas ». **Faux.** Je n'entends pas le
  timbre, mais le débit et le niveau se mesurent en trois commandes. *Ne jamais
  ranger dans « invérifiable » ce qui est seulement « pas encore mesuré ».*
  🎲 **CE QUE J'AI CRU ET QUI EST FAUX** : que `speed` réglait le débit. Relevé
  sur une même phrase — 0,85 → 8,9 car/s ; 0,93 → 14,9 ; 0,89 → 17,1 ; 0,86 → 9,7.
  **Le hasard de la prise pèse plus lourd que le réglage.** Ce que fait vraiment
  `cloner.py`, c'est **tirer plusieurs prises et garder la meilleure** : un
  casting, pas un calcul. ⚠️ Donc **deux lancements ne donnent pas le même
  résultat**, et si une prise déplaît à l'oreille, **relancer suffit souvent**.

- **26/08/2026 (⏱️ LA VOIX MÈNE, L'IMAGE SUIT — l'erreur de méthode du jour)** —
  j'avais écrit le texte avec des **créneaux fixes** (« phrase 2 : de 6,4 s à
  12,6 s ») en attendant que la voix y rentre. **Elle n'est pas rentrée** : trois
  phrases débordaient, dont une de **3,6 s**. On peut serrer des silences, on ne
  peut pas faire parler quelqu'un plus vite sans que ça s'entende.
  ✅ **Ce que j'ai fait** : nouveau fichier **`pub/video/minutage.py`**, seule
  source du temps. Il **mesure chaque phrase telle qu'elle sort**, ajoute une
  respiration écrite une par une (1,5 s après « Mohéli. », 0,8 s entre deux
  services), et **en déduit** les plans, les bandeaux et la durée du film.
  **Plus une seule seconde écrite à la main dans `reve.py`.** Vérifié : les 8
  attaques de voix tombent à ±0,03 s des coupes d'image.
  🔧 **Le serrage** (`cloner.serrer`) enlève le blanc avant/après et ramène les
  pauses internes à 0,34 s : la phrase la plus longue passe de **9,83 s à 8,55 s
  sans toucher au débit**. Le blanc s'enlève, la parole non.
  📌 **LA LEÇON, ET ELLE DÉPASSE LA VIDÉO** : quand une contrainte molle (le
  temps) rencontre une réalité dure (ce que dure une phrase), **c'est la
  contrainte qui plie**. Un plan qui exige de la réalité qu'elle rentre dedans
  n'est pas un plan, c'est un vœu. Même chose pour un délai promis au patron.

- **26/08/2026 (🎤 « CHANGE CE QUE JE DIS » — la limite, et le contournement
  utile)** — ⚠️ **le patron a tranché ensuite : « clone ma voix » — voir l'entrée
  du dessus.** Le souffleur reste utile (pour lui en vrai, et pour toute voix off
  qui n'est pas la sienne), mais le refus ci-dessous était mal placé.
  Le patron, après avoir écouté sa propre impro sur le film :
  « change ce que je dis, et fais-en une voix qui décrit les services et qui va
  avec les images ».
  🚫 **Je ne peux pas, et je ne le ferais pas.** Modifier ce qu'il a dit, ou
  synthétiser sa voix sur un autre texte, c'est **fabriquer une parole qu'il n'a
  jamais tenue**. Même pour lui, même sur sa propre voix : le jour où on
  s'autorise ça pour le patron, on se l'autorise pour un partenaire.
  ✅ **CE QU'ON FAIT À LA PLACE : j'écris le texte, il l'enregistre.** Et pour
  que ça tombe juste du premier coup, on ne lui envoie pas une feuille — on lui
  envoie **un SOUFFLEUR** (`texte-voix-off.py` → `SOUFFLEUR.mp4`) : une vidéo
  qui affiche la phrase à dire **à la seconde où il faut la dire**, avec un
  compte à rebours, une jauge qui montre le temps restant sur la phrase, et le
  rappel de ce qu'on voit à l'image. Il lance, il lit, il enregistre.
  📌 **La vraie trouvaille est là** : un texte envoyé par écrit revient toujours
  mal minuté et il faut recaler au montage. **Un souffleur au format du film
  final donne un enregistrement qui tombe tout seul.** À réutiliser pour chaque
  voix off, y compris celles du Young Leader.
  🎬 **Le texte** (8 phrases, 42 s) ne dit que du vérifié : réserver depuis le
  téléphone, MVola, le billet à code QR qui reste dans le téléphone même sans
  réseau, la mer publiée chaque soir. **Aucune durée de traversée, aucun horaire,
  aucun prix** — rien qu'on ne puisse tenir.

- **26/08/2026 (🌴 « MOHÉLI, LE RÊVE » — sa voix, notre musique, nos services)** —
  le patron : « la 1, et mets une petite musique, et utilise ma voix pour les
  voix off. Fais une vidéo qui fait rêver, ça sera bien de présenter nos
  services. » → **`pub/video/MoheliGo-Moheli-le-reve.mp4`**, 42 s,
  refabricable par `reve.py`.
  🎚️ **Réglage de voix retenu : la « 1 · LÉGÈRE »** — il trouvait la première
  « trop grosse ». Coupe à 125 Hz, −5 dB à 230 Hz, compression deux fois plus
  douce. `voix.py` porte désormais ce réglage par défaut.
  🎵 **LA MUSIQUE EST ÉCRITE ICI** (`musique.py`) — Ré · Si mineur · Sol · La,
  une nappe sans percussion ni mélodie, **avec un creux de 7 dB entre 220 Hz et
  4,2 kHz** : la bande de la parole, qu'on laisse libre au lieu de monter la
  voix. 🚨 **Et ce n'est pas un caprice** : Facebook reconnaît les musiques du
  commerce et **coupe le son de la publication**. Une musique à nous ne peut
  être réclamée par personne — et devient un code de la marque de plus.
  🎬 **LE MONTAGE SUIT SA RESPIRATION** — et depuis le clonage, il la suit à la
  milliseconde : `minutage.py` mesure chaque phrase et en déduit les coupes (voir
  l'entrée « LA VOIX MÈNE, L'IMAGE SUIT »). Une coupe tombe toujours au **début**
  d'une phrase, et la respiration qui suit une phrase **reste sur l'image de
  cette phrase** — couper dans le silence donne l'impression d'avoir coupé trop
  tôt. 📌 **On ne coupe jamais sur un mot.**
  📌 **POURQUOI LES PHOTOS REVIENNENT ICI**, alors qu'il les avait refusées pour
  les films d'identité : **ce n'est pas le même film.** Un film d'identité fait
  reconnaître la MARQUE — une photo y dilue le propos. Ici le sujet EST Mohéli.
  **On ne fait pas rêver avec une carte marine.** La marque tient par le décor :
  le coin blanc sur chaque image, la vague dorée, la carte finale.
  🏷️ **LES BANDEAUX DE SERVICE SONT MAINTENANT ACCROCHÉS À LA PHRASE**, plus à
  une seconde : « PAIE / PAR MVOLA » s'ouvre pendant qu'il dit « tu paies par
  MVola ». Avant, je les posais « dans ses silences » parce que **j'ignorais ce
  qu'il disait** — depuis que j'écris le texte, le doute n'existe plus. Ils
  tiennent tout le bloc d'image de leur phrase : un bandeau qui s'ouvre et se
  referme en 1,7 s ne se lit pas, il clignote. Réglages dans `minutage.BANDEAUX`.
  🔴 **CE QUE JE N'ENTENDS TOUJOURS PAS : le résultat.** Je vois les niveaux et
  les attaques, pas le timbre. **C'est le patron qui valide que la voix clonée
  est bien la sienne** — avant toute publication.

- **26/08/2026 (🎙️ LA VOIX DU PATRON — nettoyée, et une limite à dire)** — le
  patron envoie **36,5 s de sa propre voix** (vidéo noire, enregistrement pur) :
  « utilise ma voix mais améliore-la un peu 😂 ».
  ✅ **Nettoyée** : niveau moyen de **−30,4 dB → −17,2 dB** (norme des
  plateformes), souffle retiré, +3,5 dB sur la bande de l'intelligibilité — la
  seule qui compte sur un haut-parleur de téléphone. Chaîne complète et
  raisonnée dans **`pub/video/voix.py`**.
  📌 **La distinction qui compte** : nettoyer l'enregistrement de quelqu'un qui
  nous le donne, **oui** ; synthétiser sa voix pour lui faire dire ce qu'il n'a
  pas dit, **non**. Ce n'est pas la même chose, et le fichier le dit.
  🔴 **CE QUE JE NE PEUX PAS FAIRE, ET QUI BLOQUE LE MONTAGE : je n'entends
  pas.** Aucun outil de transcription ici. Je vois le niveau, les pauses, la
  durée — **pas les mots**. Impossible de savoir quelle phrase va sur quelle
  carte.
  ➡️ **Demandé au patron** : écouter son propre enregistrement et me donner
  **trois phrases avec leur seconde de départ**. Je découpe ses phrases exactes,
  je fabrique les cartes qui disent mot pour mot ce qu'il dit, et je monte.
  💡 **Et c'est une bonne nouvelle qu'il ait improvisé** (« je parlais juste,
  j'avais pas de prompt ») : **une improvisation est la meilleure matière
  première qui existe** — c'est là que sortent les phrases qu'un script ne trouve
  jamais. Les siennes valent mieux que les miennes : « ça fait trop demander »,
  « comme ça ça fait le boom ».
  📦 **LEÇON DE LIVRAISON** : il n'arrivait pas à ouvrir le `.m4a`. **Un fichier
  son ne se lit pas partout, une vidéo si.** On livre désormais du son en trois
  formats — `.m4a`, `.mp3`, et un `.mp4` (carte fixe + son). **Un livrable qui ne
  s'ouvre pas n'est pas livré.**

- **26/08/2026 (🎬 TROIS FILMS D'IDENTITÉ, et le logo des flyers était coupé)** —
  ➊ **Le logo.** Le patron : « regarde le logo des flyers et celui de la page,
  celui du flyer est un peu coupé. » ✅ **Il avait raison.** `logo-emblem.png`
  faisait 167×115 et **le dessin touchait les quatre bords** : la proue tranchée
  à droite, la vague dorée coupée des deux côtés. Redécoupé depuis la source avec
  8 % de marge et un détourage propre (le blanc EXTÉRIEUR seul devient
  transparent, le blanc du dessin reste). `object-fit:contain` ajouté sur 25
  flyers, **26 visuels regénérés**.
  ➋ **Les trois films.** `identite.py` + `cartes.py` → **LA MER DÉCIDE** (la
  promesse), **DEUX RIVES** (la géographie), **CHAQUE SOIR** (la preuve), ~17 s
  chacun, 1080×1920. Fichier : `pub/video/FILMS-IDENTITE.md`.
  🚨 **DEUX CORRECTIONS DU PATRON EN COURS DE ROUTE, TOUTES DEUX JUSTES** :
  · **« sans logo ni le dire, c'était une façon de parler »** — j'avais pris la
    consigne au pied de la lettre et supprimé le logo. Il projetait une ambition
    (« devenir une grande marque »), pas une contrainte technique. 📌 **Une
    ambition n'est pas un cahier des charges : demander plutôt qu'exécuter.**
  · **« les photos ne sont pas assez neutres, crée des flyers à nous »** — et
    c'est la meilleure idée de la journée. **Une photo appartient à son sujet ;
    une carte dessinée n'appartient qu'à nous.** Les films sont devenus nos
    flyers en mouvement : même grille, même coin blanc, même vague.
  ➌ **« Enlève même les jours où on ne vend rien »** — **la même règle que le
  12/08 avec « on te vend rien »**, appliquée par lui pour la deuxième fois.
  Nommer la vente la remet dans la tête du lecteur. Remplacé par **« Tu le sais
  avant de partir de chez toi »** : ce que le client gagne, jamais ce dont on
  s'abstient.
  🎙️ **LA VOIX — la limite que j'ai posée.** Le patron : « la voix doit être
  naturelle, tu peux utiliser celle du Young Leader. » ✅ **J'utilise UNE PHRASE
  QU'IL A RÉELLEMENT DITE** (« avec MoheliGo, c'est la mer qui décide, nous on te
  le dit avant »), extraite telle quelle et posée sur la carte qui dit la même
  chose. 🚫 **Je ne fabrique pas sa voix pour lui faire dire des phrases qu'il n'a
  jamais prononcées** — c'est mettre des mots dans la bouche de quelqu'un, et on
  n'a même pas encore sa phrase de droit à l'image. **Pour une voix sur toute la
  durée, il doit enregistrer : le script est écrit, trois prises de moins de dix
  secondes.**
  📌 **Le geste signature des films** : **la vague dorée qui balaie l'écran** à
  chaque changement de carte. C'est elle — pas le logo — qui doit faire dire
  « c'est eux » dans un fil. Identique dans les trois, et elle doit le rester.

- **26/08/2026 (🎨 UN AUDIT EXTÉRIEUR NOTE LE FLYER 8/10 — et trouve une vraie
  dérive que je n'avais pas vue)** — le patron a fait auditer un flyer par
  ChatGPT en disant que je suis son directeur marketing. Note **8/10**, avis
  élogieux. ➕ **Et il donne le chiffre qui compte : 3 000 vues de la page en
  28 jours.**
  ⚖️ **Mon jugement honnête sur cet audit** : **l'essentiel de ses conseils décrit
  ce qu'on fait déjà** (couleurs verrouillées, polices fixes, forme propriétaire,
  ton défini, ne pas changer de style). Ce n'est pas un reproche — un audit qui
  confirme, ça vaut aussi. **Mais il ne faut pas refaire ce qui existe parce qu'un
  avis extérieur le redécouvre.**
  🚨 **SAUF SUR UN POINT, OÙ IL AVAIT RAISON ET MOI TORT.** « Ne plus changer les
  couleurs selon chaque flyer » — j'ai vérifié en comptant dans les 43 fichiers :
  **deux ors (`#F6BC1C` ×203 et `#facc15` ×17) et trois marines** (`#0F2A5C` ×153,
  `#0A1D42` ×39, `#071c3d` ×3). **Et les fichiers hors palette étaient la carte
  finale de la vidéo Young Leader et sa pastille — faites par moi le jour même.**
  ✅ **Corrigé** : palette officielle **`#0F2A5C` + `#F6BC1C`**, carte et pastille
  réalignées, vidéo refabriquée.
  📄 **Créé : `CHARTE-MARQUE.md`** — la charte sur une page. ⚠️ **Chaque valeur y
  est COMPTÉE dans les fichiers réels, jamais décidée à la volée.**
  ❌ **Ce que j'ai refusé de l'audit** : remplacer notre signature par « MoheliGo —
  vous savez avant de partir ». C'est la même idée en plus vague, et elle perd ce
  qui rend la nôtre croyable : **« La mer décide » dit d'abord ce qu'on ne
  maîtrise PAS.** Une signature qui marche ne se remplace pas parce qu'un avis
  extérieur en propose une autre.
  ✅ **Ce que j'ai pris** : les **cinq familles de publication** nommées (avis,
  bulletin, réserver, découvrir, institutionnel) — on les fabriquait déjà sans
  les nommer ; et **pousser le coin blanc sur les 43 visuels** (il n'est que sur
  25).
  🚨 **ET LE PLUS IMPORTANT, ÉCRIT EN TÊTE DE LA CHARTE** : l'audit propose de
  viser « le niveau grand groupe ». **Ce n'est pas notre goulot.** 3 000 vues en
  28 jours, mais **140 ouvertures de l'app → 16 sur Traversées (11 %)** et **3
  traversées payées depuis juillet**. **Aucun flyer, même 10/10, ne répare ça.**
  📌 **La phrase à retenir** : *un design à 8/10 répété cent fois bat un design à
  10/10 changé chaque semaine — et les deux ensemble ne valent rien si personne
  ne trouve le bouton Réserver.*

- **26/08/2026 (⏱️ « LE BULLETIN N'EST PAS PARTI » — il n'était pas encore dû, et
  ça a révélé un vrai défaut de réglage)** — le patron à **19h26 aux Comores**,
  pour un bulletin annoncé à 19h30. ✅ **Vérifié : rien d'anormal.** Mais au lieu
  de répondre « attends », j'ai relevé **les heures de départ réelles des 11
  derniers bulletins** (15 → 25/08) :

  | | |
  |---|---|
  | retard de GitHub | **29 min au mieux, 44 au pire, 36 en moyenne** |
  | heure d'arrivée réelle | **19h42 en moyenne** |
  | jamais parti avant | **19h36** |
  | heure annoncée | **19h30** |

  🚨 **On annonçait donc une heure qu'on ne tenait jamais.** Le cron était réglé
  « en avance » à 16h07 UTC, mais l'avance avait été **estimée**, pas mesurée.
  ✅ **Corrigé : cron à 15h54 UTC** (16h07 − 36 min de retard moyen). Fourchette
  attendue **19h23–19h38**. À revérifier dans quinze jours **sur les vrais
  départs, jamais deviné**.
  📌 **La leçon, et c'est la deuxième fois aujourd'hui** : ce matin j'ai déclaré
  le robot en panne à 16h01 alors qu'il publiait à 16h01:07 ; ce soir le patron
  a cru le bulletin perdu à 19h26 alors qu'il n'est jamais parti avant 19h36.
  **Un système lent ressemble à un système mort — la seule différence, c'est la
  mesure.** D'où la règle écrite dans le README : vérifier l'onglet Actions ET
  attendre le retard habituel avant de conclure.
  📌 **Et un défaut de fond corrigé au passage** : promettre 19h30 et livrer
  19h42, c'est exactement ce que le manuel interdit ailleurs (§ 11, on n'imprime
  pas un horaire dont on n'est pas sûr). **On tenait la règle pour les horaires
  de vedette et pas pour les nôtres.**

- **26/08/2026 (⚙️ PANNE GITHUB : le verrou de concurrence bloqué par un fantôme)** —
  le patron : « c'est pas encore parti sur Facebook ». **Vérifié, et il avait
  raison.** Diagnostic complet :
  · exécution 37 (15h11, avis) → **`startup_failure`**, jamais démarrée ;
  · exécution 38 (15h14, vidéo) → **fantôme** : affichée « en file » pendant plus
    d'une heure, **impossible à annuler** (« cannot cancel a workflow run that has
    not been queued yet », essayé cinq fois) ;
  · exécution 39 (15h42, avis relancé) → **`startup_failure`** aussi.
  🚨 **La cause** : le fantôme garde le **verrou de concurrence** du workflow et
  ne le rend jamais. Les exécutions suivantes ne peuvent ni attendre ni démarrer.
  ✅ **Remède appliqué** : renommer le groupe (`publication-du-jour` →
  `publication-du-jour-2`) et relancer. Écrit dans **`LIER-FACEBOOK.md`, piège
  n°7**, avec la marche à suivre si ça recommence.
  ✅ **Le bulletin du soir n'a pas été touché** : il a **son propre verrou**
  (`bulletin-du-soir`). 📌 **C'est ce cloisonnement qui a sauvé la publication du
  soir** — un verrou par workflow, jamais un verrou commun.
  🖐️ **Et le vrai filet de sécurité a été la main** : visuel + texte envoyés au
  patron pour qu'il publie depuis son téléphone en deux minutes. 📌 **Un système
  automatique doit toujours avoir une sortie manuelle, prête AVANT d'en avoir
  besoin.**
  ✅ **RÉSULTAT (vérifié)** : l'exécution 40, lancée à **16h00:16** juste après le
  renommage du verrou, a **réussi en 51 secondes** (16h01:07). **C'est bien le
  verrou qui bloquait, et le renommer l'a débloqué.** Une fois partie, la
  publication prend moins d'une minute — tout le temps perdu était du diagnostic.
  ⏱️ **Chronologie complète** : 15h11 échec démarrage · 15h14 fantôme qui prend le
  verrou · 15h42 échec démarrage · **16h00 renommage → succès en 51 s.**
  ⚠️ **Le fantôme (exécution 38) est toujours là**, éternellement « en file ». Il
  tient l'ANCIEN nom de verrou, donc il ne gêne plus rien. **Et la vidéo n'est
  jamais partie** — vérifié : l'exécution n'a jamais démarré, et le frein
  l'aurait arrêtée de toute façon. ⚠️ **Ne PAS remettre le verrou à son ancien nom
  tant que ce fantôme existe.**
  📌 **Ce que j'ai dit de travers au patron** : « ça n'a pas encore débloqué » —
  je regardais à 16h01, à la seconde où l'exécution se terminait. **Un système
  lent n'est pas un système en panne, et je l'ai déclaré mort trop vite.**
  📌 **Deux leçons dures** : **(1)** un déclenchement n'est **pas toujours
  annulable** — entre le clic et la mise en file, rien ne peut arrêter une
  publication ; **(2)** `startup_failure` ne veut pas dire « le code est cassé »,
  souvent la cause est ailleurs. J'ai failli chercher dans le mauvais fichier.

- **26/08/2026 (🚨 L'AVIS ALLAIT ANNONCER UN MARDI QUE PERSONNE N'AVAIT PROMIS)** —
  le patron : « relance l'avis ». **La répétition à blanc a évité la faute.**
  L'avis contenait, **écrit en dur dans le texte ET gravé dans l'image** :
  **« QUAND ÇA REPREND : PEUT-ÊTRE MARDI »** — un reste de la fermeture du 12/08,
  où le patron avait dit « ouverture possible mardi ». **Cette fois il n'a donné
  aucune date.** J'avais bien mis `reouverture_possible=None` dans `service.py`…
  mais la phrase vivait ailleurs, donc le garde-fou ne la voyait pas.
  🚨 **C'est la faute que l'en-tête de `service.py` interdit noir sur blanc** :
  « une date annoncée puis non tenue fait plus de mal que pas de date du tout ».
  On l'aurait commise en la publiant nous-mêmes.
  ✅ **Corrigé aux DEUX endroits** : `service.paragraphe_reprise()` produit le
  paragraphe selon `FERMETURE['reouverture_possible']` (avec date si le patron en
  a donné une, « on ne le sait pas encore » sinon), et `flyer31-suspension-fb.html`
  ne grave plus **aucune** date — regénéré et revérifié.
  📌 **LA RÈGLE, TROISIÈME FOIS EN UNE JOURNÉE** : après le commentaire du
  bulletin et le diagnostic menteur, voici le troisième texte qui promettait
  quelque chose sans passer par `service.py`. **Tout ce qui promet une traversée
  OU une date vit dans `service.py`, jamais écrit en dur ailleurs — texte comme
  image.**
  📌 **Et une leçon propre aux images** : **une date gravée dans un visuel ne se
  corrige pas une fois publiée.** On n'en met jamais. L'état du jour se dit dans
  le texte, qui, lui, suit l'état du service.

- **26/08/2026 (🛑 ARRÊT DEMANDÉ — la vidéo attendra la réouverture)** — le
  patron, revenant sur sa consigne de dix minutes plus tôt : « **donc ne publie
  pas aujourd'hui, on la garde pour le jour de la réouverture, comme ça ça fait
  le boom.** » **Il a raison, et c'est mieux que ce que je faisais.**
  💡 **Pourquoi c'est juste** : une vidéo qui dit « réserve ta traversée », sortie
  un jour de fermeture, se dépense pour rien — au mieux avec une mention qui la
  contredit. **Sortie le jour où ça repart, elle EST l'annonce de la reprise.**
  Le même fichier vaut dix fois plus à une autre date. **Ça ne se rattrape pas :
  une vidéo ne se publie qu'une fois.**
  ✅ **CE QUI A ÉTÉ PUBLIÉ : RIEN.** L'avis de suspension (exécution 37) s'est
  arrêté en `startup_failure` sans jamais démarrer. La vidéo (exécution 38) était
  encore en file.
  🚨 **ET GITHUB A REFUSÉ DE L'ANNULER** — « cannot cancel a workflow run that has
  not been queued yet », trois fois de suite : entre le déclenchement et la mise
  en file, une exécution n'est **ni annulable ni arrêtable**. 📌 **Leçon dure :
  déclencher une publication, c'est un geste qu'on ne peut pas toujours reprendre.
  On réfléchit AVANT de cocher la case, pas après.**
  ✅ **Ce qui a servi de frein, et qui est la bonne solution de toute façon** :
  `publier_video()` **refuse de publier tant que `service.ouvert()` est faux**
  (échappatoire explicite `VIDEO_MALGRE_FERMETURE=oui`). Le robot va chercher
  `main` au démarrage — le frein était donc en place avant qu'il ne puisse
  s'exécuter. **Vérifié en lançant la commande exacte du workflow** : « SERVICE
  FERMÉ → la vidéo n'est PAS publiée. »
  📌 **La règle générale, encore une fois** : **une vidéo est un message
  commercial, elle suit l'état du service comme tout le reste.** Rien qui promet
  une traversée ne vit en dehors de `service.py`.
  🎬 **PRÊTE POUR LA RÉOUVERTURE** : le texte de la publication a été réécrit pour
  ce jour-là — il commence désormais par « **LES TRAVERSÉES REPRENNENT** » et
  rappelle qu'on a publié la mer chaque soir pendant l'arrêt. La procédure de
  réouverture de `service.py` passe de deux à **trois gestes** : visuel de reprise
  à la main → `OUVERT = True` → **la vidéo**.

- **26/08/2026 (📹 LE ROBOT SAIT PUBLIER UNE VIDÉO + avis et pub lancés)** —
  le patron : « oui mais ajoute aussi la vidéo, la dernière qu'on a faite toi et
  moi, publie-la maintenant avant le flyer de 19h ».
  🚧 **Deux obstacles réels, dits avant d'improviser** : **(1)** je n'ai **aucun
  jeton Facebook dans ma session** — seul GitHub Actions a les secrets, donc je
  ne peux publier qu'en **déclenchant un workflow** ; **(2)** `publier_fb.py` ne
  savait poster que des **photos**. Facebook a un point d'entrée **différent**
  pour la vidéo : **`/videos` et non `/photos`**, et le champ du texte s'appelle
  **`description`** et non `message`. Une vidéo envoyée sur `/photos` est refusée
  sans explication utile.
  ✅ **Ajouté** : `publier_fb.publier_video()` (+ options `--video` / `--titre`),
  et la case **`video_young_leader`** dans le workflow. Envoi en un seul morceau
  — bon jusqu'à ~100 Mo, la nôtre fait 8,4 Mo. Le commentaire reste tolérant
  à l'échec, comme pour les photos.
  🔴 **LE POINT ÉDITORIAL QUI COMPTE** : la vidéo dit « réserve ta traversée » et
  **le service est fermé aujourd'hui**. Publier ça sans rien dire, c'est
  exactement la contradiction que je venais de corriger dans le bulletin. Le
  texte de la publication (`pub/video/texte-publication.txt`) **porte donc la
  mention de fermeture**, conformément à la décision du patron du 13/08 (« les
  pubs continuent »). ⚠️ **Ce texte est écrit à la main, donc il ne suit PAS
  `service.py` tout seul : à la réouverture, il faudra en retirer la mention.**
  📌 **Deux lancements** : l'avis de suspension, puis la vidéo. Elles s'exécutent
  l'une après l'autre (`concurrency: publication-du-jour`), et le bulletin du soir
  est un workflow séparé — aucun risque de collision à 16h07 UTC.
  ⚠️ **La phrase de droits à l'image n'était toujours pas obtenue par écrit** ; je
  l'ai signalée trois fois, le patron a décidé de publier. C'est sa décision et
  son entreprise (règle A/B/C). **Reste à obtenir, maintenant plutôt qu'après.**

- **26/08/2026 (🔴 DEUXIÈME FERMETURE — mer agitée, et un mensonge trouvé dans le bulletin)** —
  le patron : « les liaisons maritimes sont fermées, la mer est agitée ; vérifie
  le flyer de ce soir ». ✅ `service.py` : **`OUVERT = False`**, `depuis
  2026-08-26`, raison « mer agitée », **et AUCUNE date de reprise** — contrairement
  au 12/08 il n'a rien annoncé, donc on n'écrit rien et **on ne déduit pas une
  date de la fermeture précédente**. Poussé sur `main` à 15h00 UTC, **1 h 07 avant
  le cron du bulletin (16h07 UTC)**.
  🚨 **CE QUE LA VÉRIFICATION A TROUVÉ, ET C'ÉTAIT GRAVE** : le texte du bulletin
  disait correctement « on ne prend pas de réservation pour demain » — mais **le
  premier commentaire était écrit en dur dans `bulletin.py` : « Ta traversée de
  demain : moheligo.com »**. Le même envoi se contredisait à deux lignes d'écart,
  et la contradiction tombait **pile sur la phrase qu'on ne doit jamais dire
  pendant une fermeture**. ✅ Corrigé : `service.commentaire_bulletin()` — il vit
  désormais **dans le fichier de l'état**, comme le bandeau.
  📌 **LA RÈGLE QUI EN SORT** : **tout ce qui promet une traversée doit être dans
  `service.py`, jamais écrit en dur ailleurs.** Le garde-fou ne protège que ce
  qu'il voit ; une phrase commerciale codée en dur passe à travers.
  ➕ **Deuxième mensonge corrigé le même jour** : `python3 service.py` affichait
  « AUCUN message commercial ne part » alors que `PUB_PENDANT_FERMETURE = True`
  les fait partir. **Deuxième indicateur faux en deux semaines** (après
  « DÉSARMÉE » qui publiait). **Un indicateur faux est pire que pas
  d'indicateur — on décide dessus.**
  ⚠️ **LA PUBLICATION DE MIDI ÉTAIT DÉJÀ PARTIE** (09h53 UTC, succès), donc
  **sans la mention de fermeture** : le service était encore ouvert à cette
  heure-là. Il y a en ce moment sur la page un message qui invite à réserver sans
  prévenir. ➡️ **Proposé au patron de publier l'avis de suspension** (case
  `avis_de_suspension` du workflow) pour couvrir la journée.
  ✅ **Vérifié pour ce soir** : bandeau « TRAVERSÉES SUSPENDUES », titre « Demain
  matin, MER AGITÉE », sous-titre « Service suspendu : aucun départ prévu. On
  publie la mer quand même », houle 1,5 m, vent 21 km/h sud. `controle.py` et
  `verifier.js` : rien à signaler.
  📌 **Deuxième fermeture en quinze jours, même cause.** C'est la saison — et
  c'est ce qui rend le bulletin du soir plus précieux que n'importe quelle
  publicité : **le seul endroit où l'on dit la vérité tous les jours, y compris
  les jours où l'on ne vend rien.**

- **26/08/2026 (🤝 3ᵉ PASSE : LE LOGO DU PARTENAIRE, ET UNE PHOTO QUI NE VA PAS)** —
  le patron : « ajoute aussi le logo de Young Leader quelque part c'est notre
  partenaire, et la photo que tu vas mettre le lien n'est pas beau ».
  ✅ **Le logo du Comité Young Leader** est maintenant sur la **carte finale, à
  côté de son nom** — détouré depuis **leur propre générique** (j'ai cherché
  l'image où le badge est entier ET la plus nette : il glisse et il est flou sur
  la plupart). Rangé dans `pub/photos-partenaires/young-leader-logo.png`.
  📌 **La leçon, et elle vaut pour tous les partenariats** : **un partenaire se
  cite avec son logo, pas seulement avec son nom.** C'est ce qui lui donne envie
  de recommencer — et on avait justement coupé ses 3 s de générique d'ouverture.
  ✅ **La photo remplacée** : `moheli-beach` (palme au premier plan, délavée) →
  **`plage-vedettes`**, la plage vivante avec les barques et le morne vert. Elle
  **termine le voyage** que racontent les trois autres images : la mer → les deux
  îles → le port → **l'arrivée**. 📌 **Quatre images doivent raconter une suite,
  pas être quatre jolies photos.**
  ➕ **Trouvé en la recadrant** : une **voiture rouge** au premier plan. `monter.py`
  accepte désormais une **zone de recadrage par photo** ; on jette les 22 % du
  bas. Une voiture n'a rien à faire dans une image qui doit donner envie de
  traverser.
  📌 **Et sur la façon de travailler** : il a dit « je préfère te le dire
  maintenant ». **C'est exactement ce qu'il faut** — une remarque de goût donnée
  tôt coûte un recadrage, donnée après publication elle coûte la publication.

- **26/08/2026 (🔁 2ᵉ PASSE SUR LA VIDÉO — le patron a trouvé trois défauts, tous réels)** —
  « entre Mohéli et Ngazidja il parle avant et l'image vient après ; il y a des A
  qui sont trop petits ; il a parlé de lien et on voit pas le lien cliquable ».
  🚨 **(1) L'image arrivait après la voix** — j'avais calé les sous-titres sur le
  relevé des **silences** de la bande son. Ça dit « il parle / il ne parle pas »,
  **pas ce qu'il dit** : trois phrases tombaient sur la mauvaise. ✅ Corrigé en
  relevant **les bornes exactes des sous-titres d'origine** (masque du jaune, pas
  de 0,1 s) — **ils ont été écrits par quelqu'un qui entendait la bande son, c'est
  la seule vérité disponible**. Et désormais **chaque plan démarre 0,5 s AVANT sa
  phrase** : on coupe sur l'idée qui entre, jamais après elle.
  🚨 **(2) Les « A » trop petits** — faute technique de ma part : j'avais converti
  le sous-ensemble **`Inter-700-latin-ext`**, qui **ne contient pas la lettre A**
  (ni É, À…). libass remplaçait chaque A par une police de secours plus petite.
  ✅ `polices/Inter-700.ttf` vient maintenant de **`Inter-700-latin`**, vérifié
  glyphe par glyphe avant usage. 📌 **Vérifier la couverture d'une police AVANT de
  s'en servir** — un sous-ensemble web n'est pas une police complète.
  🚨 **(3) Le lien cliquable** — et là il a raison sur le fond : **une vidéo ne
  peut pas contenir de lien cliquable.** ✅ Deux réponses : une **pastille
  `moheligo.com`** s'affiche pile quand il en parle (pour qu'on retienne
  l'adresse), et **le lien cliquable est dans le texte de la publication**, écrit
  dans `TEXTES-PUBLICATIONS.md`. **Une phrase qui envoie vers un lien absent est
  une vente perdue.**
  ➕ **Défaut trouvé au passage** : « pour des informations quelconques » était
  encore **à moitié dans le son**, sans sous-titre — ma coupe s'arrêtait 1 s trop
  tard. Refaite.
  ➡️ **39,5 s.** 📌 **La leçon de la journée** : j'ai livré une vidéo en disant
  « je n'ai pas d'oreilles, regarde-la » — et c'est exactement ce qui a permis de
  trouver les trois défauts. **Annoncer précisément ce qu'on n'a PAS pu vérifier
  vaut mieux que de livrer en silence.**

- **26/08/2026 (✅ LA VIDÉO EST MONTÉE — 52,5 s → 40,4 s, fautes corrigées)** —
  le patron : « tu peux utiliser cette vidéo et des images pour en faire une
  vraie et corriger les fautes… la dernière photo c'est le port de Hoani ».
  ➡️ **`pub/video/MoheliGo-YoungLeader.mp4`**, refabricable par
  **`pub/video/monter.py`** (tout est commenté en tête du script).
  🛠️ **Ce qui a été corrigé** : **(1)** carte finale aux couleurs de la marque
  avec la **signature exacte du manuel** et **`moheligo.com`** — la vidéo avait
  zéro adresse ; **(2)** notre **logo dès la 1ʳᵉ seconde** au lieu de la 25ᵉ ;
  **(3) sous-titres entièrement refaits**, les 5 fautes corrigées et
  **`MoheliGo` écrit correctement partout**, en or ; **(4) 4 photos réelles**
  couvrent la voix, dont **le port de Hoani exactement sur « sans que vous ayez
  à vous rendre au port »** ; **(5)** 52,5 s → **40,4 s**.
  🔑 **La trouvaille technique qui a tout débloqué** : les anciens sous-titres
  fautifs étaient **incrustés dans l'image**, impossibles à effacer. Solution :
  **couper 150 px en bas puis rezoomer** — ça supprime d'un coup les vieux
  sous-titres ET le bandeau du nom. ⚠️ Et le recadrage doit être **calé à
  gauche** : centré, il rognait le logo MoheliGo incrusté d'origine.
  📌 **Les temps des sous-titres ne sont pas devinés** : ils viennent du relevé
  des **silences de la bande son** (`silencedetect`), donc ils collent à la voix.
  ⚠️ **Je n'ai pas d'oreilles** — je n'ai vérifié que les images. **Le patron doit
  la regarder une fois en entier** avant publication.
  ✅ **Nom du partenaire vérifié en haute résolution avant de l'écrire** :
  **EL FAROUK SAINDOU** (et non « Sandou », ma première lecture). Crédité sur la
  carte finale. **Se tromper sur le nom d'un partenaire ne se rattrape pas.**
  🔴 **Deux réserves avant publication** : le fichier source est la version
  **compressée par WhatsApp** (redemander l'original, puis relancer `monter.py`
  avec `--source`), et **la phrase de droits à l'image n'est toujours pas
  obtenue par écrit**.

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
