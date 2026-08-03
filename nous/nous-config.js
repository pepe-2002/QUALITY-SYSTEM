/* ══════════════════════════════════════════════════════════════
   « Nous » — configuration
   ══════════════════════════════════════════════════════════════
   ⚠️ RÈGLE ABSOLUE : cette application est INDÉPENDANTE.
   Elle n'utilise ni le code, ni l'adresse, ni la base de données de
   MoheliGo. On ne met JAMAIS ici le projet Supabase de MoheliGo :
   « Nous » a sa propre base, rien qu'à elle. Comme ça, quoi qu'il
   arrive à l'une, l'autre n'est pas touchée.

   ── TEL QUEL, ÇA MARCHE DÉJÀ ──
   Les deux lignes ci-dessous sont vides : l'application tourne alors
   avec sa base intégrée, DANS LE TÉLÉPHONE (IndexedDB). Tout est
   gardé, rien ne sort de l'appareil. C'est le mode le plus privé qui
   existe — mais un seul téléphone : l'autre personne ne voit rien.

   ── POUR PARLER À DEUX TÉLÉPHONES ──
   Il faut un point de rendez-vous entre les deux appareils. Créez une
   base à vous, gratuite, en 3 minutes (voir README.md § 2) :
     1. supabase.com → « New project » → nom : « nous » (un NOUVEAU
        projet, PAS celui de MoheliGo).
     2. SQL Editor → coller SQL-nous.sql → Run.
     3. Settings → API : copier « Project URL » et « anon public » et
        les coller ci-dessous.

   Même dans ce cas, la base ne voit rien de lisible : les messages
   sont chiffrés sur le téléphone (AES-GCM 256, clé dérivée du code du
   salon, qui ne quitte jamais l'appareil).
   ══════════════════════════════════════════════════════════════ */

window.NOUS_CONFIG = {
  SUPABASE_URL: "",     // ex. "https://abcdefgh.supabase.co"  ← VOTRE projet à vous
  SUPABASE_KEY: "",     // la clé « anon public » de CE projet

  /* Toutes les 6 secondes quand l'app est ouverte : assez vif pour une
     conversation, assez sobre pour les forfaits data des Comores. */
  SYNC_MS: 6000,

  /* Garde-fous d'envoi (connexions lentes) */
  PHOTO_PX: 1280,      // la photo est réduite à ce côté max avant envoi
  PHOTO_Q: 0.72,       // qualité JPEG
  VOCAL_MAX_S: 120     // durée maximale d'un vocal
};
