# 🚀 Guide de mise en ligne — RA-QDMS

Deux étapes : **A)** créer la base de données (Supabase) puis **B)** mettre le site en ligne (**Cloudflare Pages**, inclus dans votre compte Cloudflare existant).
Durée totale : ~15 minutes.

> ℹ️ **Vos projets existants ne seront pas touchés** : on crée un *nouveau* projet
> Supabase (base et clés totalement séparées) et un *nouveau* projet Cloudflare
> Pages (adresse `xxx.pages.dev` indépendante, aucun changement DNS sur votre
> autre site).

---

## A) Créer la base de données (Supabase)

1. Connectez-vous sur **https://supabase.com/dashboard** avec votre compte existant.
2. Cliquez **New project** (votre projet actuel reste intact — le plan gratuit permet 2 projets actifs) :
   - Name : `ra-qdms`
   - Database Password : choisissez un mot de passe fort et **conservez-le**
   - Region : `East US` ou `Frankfurt` (au choix)
3. Attendez ~2 minutes que le projet soit créé.
4. Menu de gauche → **SQL Editor** → *New query* → ouvrez le fichier
   `supabase-schema.sql` de ce dossier, copiez tout son contenu, collez-le, puis **Run**.
   ✅ Vous devez voir « Success. No rows returned ».
5. Menu de gauche → **Settings → API** :
   - copiez **Project URL** (ex. `https://abcdefgh.supabase.co`)
   - copiez **anon public** key (longue chaîne commençant par `eyJ...`)
6. Ouvrez le fichier `config.js` de ce dossier avec le Bloc-notes et collez les deux valeurs :

```js
window.CONFIG = {
  SUPABASE_URL: "https://abcdefgh.supabase.co",
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIs..."
};
```

7. Enregistrez le fichier. C'est tout : au prochain chargement, l'application affiche
   **« Base en ligne »** (badge vert en haut à droite) et toutes les données sont
   partagées entre les utilisateurs, avec **sauvegarde automatique des 30 dernières
   versions** côté serveur.

---

## B) Mettre le site en ligne (Cloudflare Pages)

1. Connectez-vous sur **https://dash.cloudflare.com** avec votre compte existant.
2. Menu de gauche → **Workers & Pages** → **Create** → onglet **Pages** →
   **Upload assets** (téléversement direct, sans Git).
3. Project name : `raqdms-royalair` → **Create project**.
4. **Glissez-déposez le fichier `RA-QDMS-deploy.zip`** (ou le dossier `RA-QDMS`
   entier) dans la zone de dépôt → **Deploy site**.
5. En ~30 secondes le site est en ligne à l'adresse
   **https://raqdms-royalair.pages.dev** (HTTPS automatique).
6. (Optionnel) *Custom domains* → vous pourrez plus tard ajouter un sous-domaine
   de votre domaine Cloudflare, ex. `qdms.royalairsarl.com` — sans toucher au
   site existant.

✅ Votre autre projet hébergé chez Cloudflare n'est pas affecté : un projet Pages
est indépendant, avec sa propre adresse.

### Mettre à jour le site plus tard
*Workers & Pages → raqdms-royalair → Create new deployment* → re-glissez le zip.

---

## Sécurité — ce qui est en place et la suite

| En place (MVP en ligne) | Phase 2 (sur demande) |
|---|---|
| HTTPS (Cloudflare) | Comptes individuels Supabase Auth (e-mail + mot de passe) |
| Base PostgreSQL avec Row Level Security | Double authentification (2FA TOTP) |
| Sauvegarde automatique (30 versions) | Stockage des PDF/Word dans Supabase Storage |
| Journal des actions dans l'application | Journal des connexions côté serveur |
| Accès par rôles dans l'application | Politiques RLS par rôle |

⚠️ En attendant la phase 2, ne mettez pas de documents confidentiels sensibles :
l'accès aux données est protégé par les mots de passe de l'application, mais la
clé `anon` du site est visible par un informaticien averti. Pour un usage interne
compagnie c'est acceptable ; pour aller plus loin, demandez la phase 2.
