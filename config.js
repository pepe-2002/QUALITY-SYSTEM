/* ============================================================
   RA-QDMS — Configuration de la base de données en ligne
   ============================================================
   ÉTAPES (voir GUIDE-MISE-EN-LIGNE.md) :
   1. Créez un projet gratuit sur https://supabase.com
   2. Dans le projet : SQL Editor → collez le contenu de
      supabase-schema.sql → Run
   3. Dans Settings → API, copiez :
      - "Project URL"       → SUPABASE_URL
      - "anon public key"   → SUPABASE_ANON_KEY
   4. Remplacez les valeurs ci-dessous, enregistrez, et
      redéployez le dossier sur Netlify.

   Tant que ces valeurs sont vides, l'application fonctionne
   en mode local (données dans le navigateur uniquement).
   ============================================================ */

window.CONFIG = {
  SUPABASE_URL: "https://sgfguotmbyxiieijqjvb.supabase.co",
  SUPABASE_ANON_KEY: "sb_publishable_aPPipGlj3a9P7tQHQ3bKLA_ldVYL41L"
};
