/* ══════════════════════════════════════════════════════════════
   « Nous » — configuration
   ══════════════════════════════════════════════════════════════
   Le salon se synchronise entre deux téléphones grâce à Supabase
   (le même projet que MoheliGo, mais des tables à part : nous_*).

   AVANT d'utiliser à deux : ouvrir Supabase → SQL Editor →
   coller le contenu de SQL-nous.sql → Run. Une seule fois.

   Tant que ce n'est pas fait, l'application marche quand même,
   mais SEULE sur le téléphone (mode local, rien n'est envoyé).

   ⚠️ Ce que le serveur voit : un identifiant de salon (une
   empreinte du code, pas le code) et des blocs chiffrés. Les
   messages, prénoms, photos et vocaux sont chiffrés SUR LE
   TÉLÉPHONE avec le code du salon (AES-GCM 256). Le code ne
   quitte jamais l'appareil.
   ══════════════════════════════════════════════════════════════ */

window.NOUS_CONFIG = {
  SUPABASE_URL: "https://gnfodquywolxeeqpmzun.supabase.co",
  SUPABASE_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImduZm9kcXV5d29seGVlcXBtenVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2OTgwMDYsImV4cCI6MjA5ODI3NDAwNn0.8V8z9UdcUCkVzFXmtpjuL-pQc2i7GwHBuQYbv_pYMWc",

  /* Toutes les 6 secondes quand l'app est ouverte : assez vif pour une
     conversation, assez sobre pour les forfaits data des Comores. */
  SYNC_MS: 6000,

  /* Garde-fous d'envoi (connexions lentes) */
  PHOTO_PX: 1280,      // la photo est réduite à ce côté max avant envoi
  PHOTO_Q: 0.72,       // qualité JPEG
  VOCAL_MAX_S: 120     // durée maximale d'un vocal
};
