/* ═══════════════════════════════════════════════════════════════════
   Kodo — les solutions des exercices de code.

   Personne ne doit rester bloqué. Après deux essais, le jeu propose
   de montrer la solution : on la lit, on la comprend, on continue.
   Elles sont écrites simplement et commentées, pour servir de modèle.
   ═══════════════════════════════════════════════════════════════════ */
window.KODO_SOLUTIONS = {

  /* ── Le code ── */
  total:
`function total(prix, nombre) {
  return prix * nombre;
}`,

  bienvenue:
`function bienvenue(nom) {
  return "Bonjour " + nom;   // ne pas oublier l'espace
}`,

  statut:
`function statut(places) {
  if (places === 0) {
    return "complet";
  } else if (places < 5) {
    return "presque complet";
  } else {
    return "disponible";
  }
}`,

  recette:
`function recette(prix) {
  let somme = 0;
  for (let i = 0; i < prix.length; i = i + 1) {
    somme = somme + prix[i];
  }
  return somme;
}`,

  disponibles:
`function disponibles(places) {
  return places.filter(n => n > 0);
}`,

  moyenne:
`function moyenne(nombres) {
  if (nombres.length === 0) {   // le cas limite d'abord
    return 0;
  }
  let somme = 0;
  for (let i = 0; i < nombres.length; i = i + 1) {
    somme = somme + nombres[i];
  }
  return somme / nombres.length;
}`,

  reussis:
`function reussis(cas) {
  return cas.filter(c => c.obtenu === c.attendu).length;
}`,

  /* ── Le web ── */
  montant:
`function montant(billet) {
  return billet.prix * billet.places;
}`,

  secondes3G:
`function secondes3G(ko) {
  return ko / 100;
}`,

  nettoyerTel:
`function nettoyerTel(saisi) {
  return saisi.replace(/[^0-9]/g, "");   // on ne garde que les chiffres
}`,

  echapper:
`function echapper(texte) {
  return texte
    .replace(/&/g, "&amp;")    // l'esperluette EN PREMIER
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}`,

  /* ── Les serveurs ── */
  lireCode:
`function lireCode(code) {
  if (code >= 500) {
    return "serveur";
  } else if (code >= 400) {
    return "client";
  } else if (code >= 200 && code < 300) {
    return "ok";
  } else {
    return "autre";
  }
}`,

  chercher:
`function chercher(lignes, date) {
  return lignes.filter(l => l.date === date && l.payee);
}`,

  disponibilite:
`function disponibilite(minutesArret) {
  return (43200 - minutesArret) / 43200 * 100;
}`,

  motDePasseFort:
`function motDePasseFort(mdp) {
  return mdp.length >= 12 && /[0-9]/.test(mdp);
}`,

  /* ── API & IA ── */
  estOk:
`function estOk(reponse) {
  return reponse.status >= 200 && reponse.status < 300;
}`,

  coutFC:
`function coutFC(tokens, prixMille) {
  return (tokens / 1000) * prixMille;
}`,

  extraireTexte:
`function extraireTexte(reponse) {
  const bloc = reponse.content.find(b => b.type === "text");
  return bloc ? bloc.text : "";
}`,

  morceauxUtiles:
`function morceauxUtiles(textes, mot) {
  return textes.filter(t =>
    t.toLowerCase().includes(mot.toLowerCase())
  );
}`,

  sousPlafond:
`function sousPlafond(faits, plafond) {
  return faits < plafond;   // au plafond exact, c'est déjà non
}`,

  tauxReussite:
`function tauxReussite(resultats) {
  if (resultats.length === 0) {
    return 0;
  }
  const justes = resultats.filter(r => r.juste).length;
  return Math.round(justes / resultats.length * 100);
}`

};
