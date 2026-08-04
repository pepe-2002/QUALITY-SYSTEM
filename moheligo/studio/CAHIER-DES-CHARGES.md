# Cahier des charges — Moheligo Studio IA v1.0

Réponse point par point à la demande du patron (04/08/2026). Chaque ligne indique
où la chose se trouve dans le studio, et ce qui reste ouvert.

Légende : ✅ fait · ⛔ dépend d'un moteur externe payant · 🕓 prévu

---

## Objectif

> *Créer un studio IA privé capable de produire des vidéos publicitaires avec des
> avatars humains photoréalistes réutilisables, principalement pour Moheligo.*

Le studio est en place. La chaîne complète — comprendre la demande, écrire le film,
verrouiller les personnages, produire le son, monter, exporter — fonctionne ici et
maintenant. La **fabrication des visages photoréalistes** est la seule brique qui ne
peut pas tourner dans cet environnement : elle s'achète chez un fournisseur, et le
studio est câblé pour s'y brancher en une commande (`studio.py generer --moteur fal`).

---

## Bibliothèque d'avatars

> *Environ 20 à 30 personnages permanents.*

✅ **26 avatars** dans `bible/avatars.json`. Tous les rôles demandés sont couverts :

| Demandé | Avatar |
|---|---|
| Jeune homme (20–30) | Nassim Abdallah (27), Toiwilou Mbaé (24) |
| Jeune femme (20–30) | Amina Saïd (26), Chamsia Bacar (21) |
| Père de famille | Saïd Ahmed (41) |
| Mère de famille | Hadidja Ali (38) |
| Étudiant | Anfane Mmadi (20), Chamsia Bacar (21) |
| Touriste européen | Camille Vasseur (33), Lukas Berger (45) |
| Touriste africain | Kwame Mensah (35), Aisha Njeri (29) |
| Capitaine de vedette | Commandant Baco Mmadi (52) |
| Hôtelier | Fatima Halifa (44), Youssouf Bacar (50) |
| Commerçant | Moinaecha Combo (47), Ibrahim Soilihi (39) |
| Guide touristique | Nadjat Abdou (tortues), Ali Mzé (baleines) |
| Enfant | Salim (9) et Nailat (7), **usage encadré** |

Ajoutés parce que la marque en a besoin : le second de bord Momo (scan des billets),
les deux agents MoheliGo Zainaba et Abdou (service client et quai), la voyageuse aînée
Farida (accessibilité), le chauffeur Djoumoi (chaîne du trajet), la cadre Roukia
(voyage professionnel).

> *Chaque avatar possède : un nom interne ; une apparence fixe ; plusieurs tenues ;
> différentes coiffures ; des expressions ; une voix attribuée.*

✅ Tout y est. L'apparence fixe est le champ `identite` + le `seed` — c'est ce couple
qui garantit le même visage d'une pub à l'autre. Voir `studio.py casting` pour les
fiches imprimables.

> *Enfant (uniquement dans des contextes appropriés et non promotionnels ciblés).*

✅ Traduit en règles que le moteur **fait respecter par un refus** : jamais seul à
l'image, jamais de réplique commerciale, jamais de gros plan isolé, aucune voix de
synthèse, aucun ciblage publicitaire. Vérifié : un scénario fautif est rejeté avec
le motif exact.

---

## Animations, expressions, décors, caméras

> *Marcher, courir, parler, sourire, rire, se serrer la main, utiliser un téléphone,
> montrer une application, monter à bord d'une vedette, prendre des selfies, saluer.*

✅ Les 11 demandées, plus 5 utiles à MoheliGo (retrouvailles, scanner le billet, porter
un bagage, regarder la mer, payer au mobile) — `bible/grammaire.json`.

> *Heureux, triste, étonné, inquiet, en colère, détendu, enthousiaste.*

✅ Les 7, plus « sérieux » (indispensable au commandant et aux agents).

> *Port de Hoani, Chindini, Fomboni, plages, hôtels, restaurants, aéroport, intérieur
> de vedette, marché, routes, bureau Moheligo.*

✅ **14 décors**, dont les 11 demandés. Ajoutés : le **port d'Ouroveni** (c'est de là
que partent les vedettes, comme tu me l'avais corrigé), la pleine mer entre les îles,
et la plage aux tortues d'Itsamia. Sept décors sont adossés à de vraies photos de
`pub/` — elles servent d'image de référence au moteur, ce qui ancre le rendu dans le
vrai paysage comorien.

> *Drone, plan cinématographique, selfie, caméra fixe, vue aérienne, ralenti, timelapse.*

✅ Les 7, plus le gros plan (obligatoire pour montrer l'écran de l'app).

---

## Audio

> *Voix masculine, féminine ; français, shikomori, anglais, arabe ; musiques libres de
> droits ; bruit de la mer, ambiance du port.*

✅ Français, anglais, arabe : voix disponibles et testées.

⚠️ **Shikomori : point à trancher.** Aucune voix de synthèse shikomori n'existe, chez
aucun fournisseur. Le studio approxime avec du swahili — c'est assez proche pour caler
une maquette, ce n'est **pas diffusable**. La bonne solution coûte une demi-journée :
enregistrer une vingtaine de phrases de marque avec une vraie voix comorienne, une
fois pour toutes. Dis-moi si tu veux qu'on organise ça.

Pour les ambiances : la liste est décrite (`bible/grammaire.json`), et la règle que tu
avais posée est inscrite en dur — **pas de nappe synthétique**. Il faut de vrais
enregistrements libres de droits, à déposer dans `studio/audio/`. Tant qu'il n'y en a
pas, c'est voix nette sur silence propre, comme sur les pubs v1 à v5.

---

## L'IA en langage naturel

> *« Fais une publicité de 30 secondes où deux amis discutent au port de Hoani.
> L'un montre Moheligo sur son téléphone. Ils réservent leur traversée puis montent
> dans la vedette. Ajoute une voix en français et des sous-titres. »*

✅ C'est exactement la commande qui a produit le projet `projets/demo-hoani-30s/`.
Le studio en a tiré, sans autre intervention : le casting (Nassim et Toiwilou), le
découpage en 10 plans, les dialogues, les expressions, les mouvements de caméra, les
voix, les sous-titres, le montage et les trois exports.

Le scénario généré est un fichier texte lisible (`scenario.json`) : tout se corrige à
la main, ou je le réécris moi-même quand on cherche plus fin.

---

## Export

✅ TikTok/Reels/Shorts 9:16, Facebook 4:5, carré 1:1, YouTube 16:9, statut WhatsApp
(30 s), YouTube 4K. Chaque export a sa **version légère** au réglage que tu avais
validé — 3 à 5 Mo par minute, pour que ça passe sur les connexions d'ici.

Le 4K n'a de sens qu'avec des sources réellement en 4K : agrandir une image plus
petite ne fabrique aucun détail, ça ne fait que gonfler le fichier.

---

## Évolutions futures

| Demandé | État |
|---|---|
| Création de nouveaux avatars | ✅ une entrée à ajouter dans `avatars.json`, rien d'autre |
| Clonage de voix avec autorisation | 🕓 prévu — la condition reste l'autorisation écrite signée |
| Lip-sync très réaliste | ⛔ adaptateur HeyGen déjà écrit, en attente d'une clé |
| Génération de foules | ⛔ dépend du moteur vidéo |
| Publicités en plusieurs langues | ✅ français/anglais/arabe ; shikomori en attente de voix humaines |
| Personnages récurrents de la marque | ✅ c'est le principe même de la bibliothèque |

---

## Ce qu'il faut décider

1. **Le moteur de génération.** Sans clé d'API, pas de visages. Compter environ
   0,30 à 0,50 € par plan de 5 secondes chez fal.ai ou Replicate — soit **de l'ordre
   de 5 à 10 € pour une pub de 30 secondes**, hors essais ratés (ordres de grandeur de
   marché, à revérifier au moment de souscrire). Le plus économique : générer **une
   fois** les 26 portraits de référence, puis animer ces portraits.
2. **Les voix shikomori.** Synthèse approximative pour les maquettes, voix humaines
   pour la diffusion.
3. **Les ambiances sonores.** Trouver des enregistrements libres de droits, ou en
   capter sur place — un vrai son de port de Hoani vaudrait mieux que n'importe quelle
   banque de sons.
