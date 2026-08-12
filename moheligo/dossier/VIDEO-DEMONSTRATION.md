# 🎬 La vidéo de démonstration — ce qui manque, et pourquoi

**Demande du patron, 11/08/2026** : « on peut pas ajouter un flyer ou vidéo de
démonstration le matin ? »

**Livré ce soir** : le flyer `flyer21-modedemploi-fb.html` (les trois gestes),
publié les **lundis et jeudis à 7h30** par `.github/workflows/publication-du-matin.yml`.

**Pas livré** : la vidéo. Voici pourquoi, et exactement ce qu'il faut pour
qu'elle existe.

---

## Pourquoi la vidéo n'a pas pu être faite dans la session

Trois obstacles, vérifiés un par un le 11/08/2026 :

| Ce que j'ai essayé | Résultat |
|---|---|
| Filmer **moheligo.com en ligne** avec Chromium | ❌ `ERR_CONNECTION_RESET` — Chromium n'a **aucun accès réseau** dans la session (testé avec et sans mandataire, et sur un autre domaine : même échec). `curl` passe, le navigateur non. |
| Faire tourner le site **en local** depuis le dépôt | ❌ le site charge ses départs depuis **Supabase** (`gnfodquywolxeeqpmzun.supabase.co`) et son client depuis un **CDN** — sans réseau pour le navigateur, l'application s'ouvre vide. |
| **Dessiner** une fausse interface et l'animer | ⛔ **refusé.** Montrer un écran qui n'existe pas, c'est inventer une preuve — interdit par le § 11 du manuel. Et ça se voit : un écran redessiné a toujours l'air d'un écran redessiné, exactement le reproche « ça fait débutant ». |

✅ **Ce qui, en revanche, est prêt** : l'encodage vidéo fonctionne
(`pip install imageio-ffmpeg` fournit un ffmpeg 7.0.2 autonome), et le script de
capture `capture_site.js` est écrit et fonctionnel — il ne lui manque que le
réseau.

---

## Ce qu'il me faut de la part du patron : 4 captures d'écran

Deux minutes de son téléphone valent mieux qu'une heure de contournement.
**Sur son propre téléphone, sur moheligo.com**, capture d'écran de :

1. **L'accueil** — tel qu'il s'ouvre.
2. **La carte « Réserver une traversée »** avec un départ, une arrivée et une
   date déjà choisis.
3. **La liste des traversées** — les horaires, les places, les prix.
4. **Un billet payé avec son code QR** — s'il en a un ; c'est **la capture la
   plus précieuse**, parce que c'est la preuve matérielle (§ 5 du manuel).

⚠️ **Avant d'envoyer** : masquer tout nom, numéro de téléphone et numéro de
billet appartenant à un vrai client. On ne publie jamais la donnée de quelqu'un.
Un billet à son nom à lui, ou un billet d'essai, c'est parfait.

À déposer dans `moheligo/pub/demo/ecrans/` (n'importe quel nom, PNG ou JPEG).

---

## Ce que j'en ferai

Une vidéo verticale **1080 × 1350, 4:5** (le format qui occupe le plus de place
dans le fil Facebook), 18 à 22 secondes, muette et **lisible sans le son** —
la plupart des gens regardent sans son :

1. un titre court sur le marine : « Ta place, en trois gestes » ;
2. les quatre écrans **réels**, l'un après l'autre, dans un cadre de téléphone,
   avec un doigt qui montre où appuyer et une légende de cinq mots par écran ;
3. la fin : `moheligo.com` + le WhatsApp, tenue trois secondes.

Fabrication : les images composées en HTML/CSS, une image par vingt-cinquième de
seconde rendue par Chromium (`render.js` fait déjà ça), puis assemblage en MP4
avec le ffmpeg de `imageio-ffmpeg`.

⚠️ **Une chose à prévoir avant de publier une vidéo** : `publier_fb.py` sait
déposer une **photo** (`/{page}/photos`). Une vidéo passe par un autre point
d'entrée (`/{page}/videos`) et un envoi en plusieurs morceaux. C'est une demi-
heure de travail, à faire **le jour où les captures arrivent**, pas avant : du
code qui attend n'a jamais été testé.

---

## Les fichiers de ce dossier

| Fichier | Rôle |
|---|---|
| `capture_site.js` | capture les vrais écrans du site (prêt, en attente de réseau) |
| `ecrans/` | où déposer les captures — c'est ce qui débloque tout |
