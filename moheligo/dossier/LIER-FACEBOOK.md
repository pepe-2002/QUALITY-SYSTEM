# Lier la page Facebook MoheliGo au robot

But : le bulletin du soir se publie **tout seul** sur la page, chaque jour, sans
que personne n'ouvre Facebook.

## Ce qu'il faut comprendre d'abord

Il n'existe **pas de connecteur Facebook dans Claude** : je ne peux pas
« me connecter » à la page, et de toute façon ma session est fermée la plupart
du temps. Ce qui tient dans le temps, c'est GitHub.

La liaison marche donc comme ça :

```
Meta  ──(jeton de page)──▶  Secrets GitHub  ──▶  GitHub Actions (chaque jour 16h)
                                                        │
                                    bulletin.py + render.js  (fabrique le flyer)
                                                        │
                                    publier_fb.py  ──▶  la page Facebook
```

**Le jeton reste chez toi et chez GitHub. Je ne le vois jamais.** J'écris le
code qui s'en sert ; GitHub le lui donne au moment de publier.

🚫 **Ne m'envoie jamais le jeton dans la conversation.** Tout ce qui est écrit
ici est enregistré. Un jeton collé dans un message est un jeton à refaire.

---

## ⚠️ Étape 0 — LE PLUS URGENT : sécuriser l'accès au compte

Le patron a signalé le 11/08/2026 qu'il **n'a plus le numéro de téléphone avec
lequel il ouvre la page**. C'est le vrai risque du projet, bien avant les jetons :
**si ce compte se déconnecte, la page est perdue**, avec ses abonnés.

Ce qui compte pour Facebook, ce n'est pas le numéro : c'est **d'être connecté au
compte qui administre la page**. Donc, tant que la session est encore ouverte sur
le téléphone :

1. **Ne pas se déconnecter. Ne pas désinstaller l'application. Ne pas
   « nettoyer » le téléphone.** Tant que la session vit, tout est récupérable.
2. Dans **Centre de comptes → Informations personnelles → Coordonnées** :
   **ajouter le numéro actuel** et une **adresse e-mail** qu'on contrôle, puis
   retirer l'ancien numéro. C'est ça qui rend le compte récupérable plus tard.
3. Vérifier qu'on connaît **le mot de passe** (le changer maintenant si ce n'est
   pas le cas — il faut être connecté pour le faire sans SMS).
4. Mettre la double authentification **par application** (Google Authenticator,
   Duo…) et **pas par SMS** : plus jamais dépendant d'un numéro.
5. Enregistrer les **codes de secours** que Facebook propose, ailleurs que dans
   le téléphone.
6. **Ajouter un second administrateur à la page** (un compte de confiance, ou un
   deuxième compte à soi bien sécurisé). Une page avec un seul administrateur
   est une page à un seul point de rupture.

Si le compte est **déjà déconnecté et inaccessible** : la récupération passe par
`facebook.com/login/identify` avec l'e-mail ou le nom, puis par les procédures de
Meta (pièce d'identité). Un autre administrateur de la page, s'il en existe un,
peut de son côté générer le jeton — la page n'a pas besoin de *ce* compte-là en
particulier, seulement d'**un** administrateur.

⚠️ Créer une nouvelle page est le dernier recours, et c'est cher : les abonnés,
l'ancienneté et l'historique ne se transfèrent pas.

---

## Étape 1 — Créer l'application chez Meta (une seule fois, 10 minutes)

Il faut être **administrateur** de la page MoheliGo (tu l'es).

1. Va sur **developers.facebook.com** avec ton compte Facebook, et crée un
   compte développeur si c'est la première fois.
2. **Mes apps → Créer une app.** Type : **Entreprise** (ou « Autre » si le type
   Entreprise n'est pas proposé). Nom : `MoheliGo Bulletin`.
3. Note l'app, tu n'as rien d'autre à configurer dedans.

ℹ️ **Pas besoin de « revue de l'application ».** La revue sert à agir sur les
pages des *autres*. Tant que tu publies sur **ta** page avec **ton** jeton,
l'application peut rester en mode développement.

## Étape 1 bis — Ajouter le cas d'utilisation « Page »

Meta a changé son interface (« Espace App ») : les permissions ne se demandent
plus directement, elles viennent d'un **cas d'utilisation**.

1. Dans le menu de gauche : **Cas d'utilisation → Ajouter des cas d'utilisation**.
2. Cherche celui qui parle des **Pages** — « Gérer tout ce qui concerne votre
   Page » ou « Gérer les Pages ». Ajoute-le.
3. Ouvre-le, clique **Personnaliser**, et vérifie que ces trois permissions
   apparaissent : `pages_show_list`, `pages_read_engagement`,
   `pages_manage_posts`. Ajoute-les si elles ne sont pas déjà là.

ℹ️ L'app peut rester **« Non publiée »** : la publication d'app sert à agir sur
les pages des autres. Pour ta propre page, le mode développement suffit.

## 📱 Si tu fais ça depuis le téléphone

L'explorateur d'API est presque inutilisable en affichage mobile. Dans Chrome :
**menu ⋮ → cocher « Site pour ordinateur »**. La page devient petite mais tous
les boutons apparaissent, et on peut zoomer.

## Étape 2 — Obtenir le jeton de page

1. Va sur l'**explorateur d'API** : `developers.facebook.com/tools/explorer`.
2. En haut à droite, choisis ton app `MoheliGo`.
3. Clique **« Générer un token d'accès utilisateur »** et vérifie que ces trois
   permissions sont bien cochées :
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
4. Connecte-toi, et **autorise la page MoheliGo** quand il demande laquelle.
   ⚠️ Si l'écran propose « Toutes les Pages » ou une sélection, il faut que
   MoheliGo soit bien cochée — sinon le jeton ne verra rien.
5. Dans la barre de requête, tape `me/accounts` puis **Envoyer**.
   La réponse liste tes pages. Pour MoheliGo, relève deux choses :
   - `"id"` → c'est le **FB_PAGE_ID** (une longue suite de chiffres)
   - `"access_token"` → c'est le **jeton de page**

💡 Sur téléphone, la réponse est longue et pénible à lire. Astuce : dans la barre
de requête, demande directement `me/accounts?fields=name,id,access_token` — tu
n'auras que les trois lignes utiles.

### Le chemin le plus court (celui qu'on a pris le 11/08/2026)

Dans l'explorateur, le menu **« Utilisateur ou Page »** permet de choisir
directement la page. Quand la page y est sélectionnée :

- le jeton affiché **est déjà le jeton de page** ;
- la requête `me?fields=id,name` renvoie la page, et son `id` est le
  **FB_PAGE_ID**.

Pas besoin de passer par `me/accounts`. Deux vérifications quand même :

1. plus bas dans le panneau, la liste des **autorisations** doit contenir
   `pages_manage_posts` (sinon : « Ajouter une autorisation ») ;
2. la version d'API du menu déroulant (v26.0 en août 2026) doit correspondre à
   celle de `publier_fb.py`, sinon poser `FB_API_VERSION`.

⏳ **Le jeton de l'explorateur est éphémère** (une à deux heures). C'est parfait
pour l'essai du jour, mais il faut ensuite le rendre durable (« Étendre le token »
dans le débogueur, ou un utilisateur système dans Business Manager) — sinon le
travail automatique du soir échouera dès demain.

🚫 **Ne pas photographier l'écran du jeton.** Une capture d'écran qui montre le
champ « Token d'accès » est une fuite : quelqu'un qui le lit peut publier sur la
page. En cas de doute, cliquer **« Generate Access Token »** : l'ancien devient
inutile.

### Rendre le jeton durable

Le jeton obtenu comme ça expire vite. Deux façons de le rendre durable :

**Simple** — `developers.facebook.com/tools/debug/accesstoken` : colle le jeton
*utilisateur*, clique **« Étendre le token d'accès »** (60 jours), puis refais
`me/accounts` avec ce jeton étendu. Le jeton de page qui en sort n'a
normalement plus de date d'expiration.

**Solide** — dans **Business Manager → Paramètres → Utilisateurs système** :
crée un utilisateur système, donne-lui la page en « Gérer la page », puis génère
un jeton avec `pages_manage_posts`. Celui-là ne périme pas.

⚠️ Un jeton peut quand même être invalidé (changement de mot de passe,
permission retirée, alerte de sécurité Meta). Si ça arrive, le travail du soir
échoue, GitHub t'envoie un mail, et tu refais l'étape 2. Le script affiche alors
exactement : « Jeton expiré ou permission manquante ».

## Étape 3 — Ranger le jeton dans GitHub

Dans le dépôt : **Settings → Secrets and variables → Actions**.

| Onglet | Nom | Valeur |
|---|---|---|
| **Secrets** | `FB_PAGE_TOKEN` | le jeton de page (il devient illisible, même pour toi) |
| **Variables** | `FB_PAGE_ID` | l'identifiant numérique de la page |
| **Variables** | `PUBLIER_FB` | `oui` — **seulement quand tu veux armer la publication** |

Tant que `PUBLIER_FB` n'existe pas ou ne vaut pas `oui`, **rien n'est jamais
publié** : le tuyau continue à fabriquer le flyer et à le déposer sur la branche
`bulletin-du-jour`, comme aujourd'hui.

## Étape 4 — Essayer, avant d'armer

Onglet **Actions → Bulletin du soir → Run workflow**. Laisse
`publier_sur_facebook` sur **false** : le script fait une **répétition à blanc**
et affiche ce qu'il publierait, sans rien publier.

Quand la répétition est bonne : relance avec `publier_sur_facebook` = **true**
pour une vraie publication de contrôle. Si elle te plaît, ajoute la variable
`PUBLIER_FB = oui` et c'est automatique tous les jours à 16h.

Depuis ton ordinateur, la même chose se teste comme ça :

```bash
cd moheligo/pub/flyers
export FB_PAGE_ID=...          # à ne pas mettre dans un fichier du dépôt
export FB_PAGE_TOKEN=...
python3 publier_fb.py --verifier      # « Liaison OK — page « MoheliGo » »
python3 publier_fb.py                 # répétition à blanc
python3 publier_fb.py --publier       # pour de vrai
```

---

## Ce que le robot publie

- Le **flyer du jour** en image (`flyer-soir-facebook.png`).
- Le **texte du post** (`texte-du-jour.txt`), avec les vrais chiffres de la mer.
- Le **lien en premier commentaire**, automatiquement — jamais dans le post.

C'est exactement ce que tu ferais à la main, à la même heure, tous les jours.

## Les garde-fous, et pourquoi ils sont là

Publier est **public et difficile à défaire**. Donc :

1. Sans `--publier`, le script ne publie rien.
2. Sans la variable `PUBLIER_FB = oui`, l'étape du workflow ne tourne même pas.
3. Le jeton n'apparaît **jamais** dans une ligne de commande (il serait visible
   dans les journaux GitHub et dans la liste des processus) : il est passé à
   curl par son entrée standard, en en-tête `Authorization`.
4. Un seul bulletin par jour : le workflow a un verrou (`concurrency`).

## Si tu ne veux pas de jetons du tout

C'est une position parfaitement défendable. L'alternative sans code :
**Meta Business Suite → Planificateur**. Le dimanche soir, tu programmes les
sept publications de la semaine en une vingtaine de minutes, en piochant les
visuels sur ta page web.

| | Robot (ce document) | Business Suite à la main |
|---|---|---|
| Mise en place | 30 min une fois | rien |
| Chaque semaine | 0 min | ~20 min |
| Le bulletin daté | toujours juste, calculé le jour même | il faut le regénérer et le reposter soi-même |
| Risque | un jeton à refaire de temps en temps | un oubli le soir |

Mon avis de directeur marketing : **le bulletin quotidien doit être automatisé**
(c'est le seul contenu qui ne pardonne pas l'oubli, et c'est notre rendez-vous),
et les autres publications peuvent rester à la main — elles gagnent à être
choisies.

## Plus tard, si tu veux

Instagram se branche sur le même jeton, à condition que le compte Instagram soit
un compte **professionnel rattaché à la page**. Ça se fait en ajoutant une
requête dans `publier_fb.py`. À faire seulement quand la page Facebook tourne.
