/* GÉOPOLIS — Événements
 * Chaque crise a des conditions d'apparition et deux à trois issues, toutes
 * défendables. Aucune n'est gratuite : gouverner, c'est arbitrer.
 */
(function (G) {
  'use strict';
  const c = G.clamp;
  const R = G.R, B = G.B, U = G.U;
  const J = (E) => E.joueur;

  G.EVENEMENTS = [
    {
      icone: '🛢️', titre: 'Choc pétrolier',
      texte: "Un conflit lointain ferme un détroit stratégique. Le baril s'envole. Vos automobilistes hurlent, vos raffineurs jubilent.",
      choix: [
        { txt: 'Bloquer les prix à la pompe', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 1.5; E.approb[i] += 6; return 'Subvention massive, trésor entamé.'; } },
        { txt: 'Laisser filer', effet: (E, i) => { E.approb[i] -= 7; E.inflation[i] += 2.5; return 'Le pouvoir d\'achat encaisse.'; } },
        { txt: 'Taxer les superprofits', effet: (E, i) => { E.tresor[i] += E.pib[i] * 1.2; E.approb[i] += 3; E.croiss[i] -= 0.6; return 'Recettes exceptionnelles, investisseurs refroidis.'; } }
      ]
    },
    {
      icone: '🌪️', titre: 'Catastrophe naturelle',
      texte: "Un cyclone dévaste une région entière. Routes coupées, récoltes perdues, images terribles à la télévision.",
      choix: [
        { txt: 'Plan de reconstruction national', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 2.2; E.approb[i] += 9; E.infra[i] += 2; return 'Coûteux, mais le pays vous voit agir.'; } },
        { txt: 'Faire appel à l\'aide internationale', effet: (E, i) => { E.tresor[i] += 300; E.reput[i] -= 4; E.approb[i] -= 3; return 'Aide reçue, fierté nationale écornée.'; } }
      ]
    },
    {
      icone: '🦠', titre: 'Épidémie',
      texte: "Un virus respiratoire se propage. Les hôpitaux saturent et le conseil scientifique attend vos instructions.",
      choix: [
        { txt: 'Confinement strict', effet: (E, i) => { E.croiss[i] -= 3.5; E.sante[i] += 4; E.approb[i] -= 5; return 'Vies sauvées, économie à l\'arrêt.'; } },
        { txt: 'Vivre avec le virus', effet: (E, i) => { E.pop[i] *= 0.996; E.sante[i] -= 5; E.approb[i] -= 8; return 'L\'activité continue, le bilan humain s\'alourdit.'; } },
        { txt: 'Miser sur les vaccins', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 1.1; E.sante[i] += 6; E.tech[i] += 0.5; return 'Pari technologique payant.'; } }
      ]
    },
    {
      icone: '✊', titre: 'Grève générale',
      texte: "Les syndicats bloquent raffineries, ports et transports. Le pays est à l'arrêt depuis six jours.",
      cond: (E, i) => E.approb[i] < 55,
      choix: [
        { txt: 'Négocier et augmenter les salaires', effet: (E, i) => { E.approb[i] += 8; E.inflation[i] += 1.4; E.croiss[i] -= 0.5; return 'Paix sociale achetée.'; } },
        { txt: 'Réquisitionner', effet: (E, i) => { E.approb[i] -= 10; E.stab[i] -= 6; E.croiss[i] += 0.4; return 'Ordre rétabli, colère intacte.'; } }
      ]
    },
    {
      icone: '💎', titre: 'Découverte d\'un gisement',
      texte: "Des prospecteurs identifient un gisement considérable sous une région jusqu'ici sans intérêt.",
      choix: [
        { txt: 'Exploitation nationale', effet: (E, i) => { const b = [B.puits, B.minefer, B.mineor, B.minecuivre, B.mineterres][(Math.random() * 5) | 0]; E.bat[i * G.NBAT + b] += 3; return '3 sites ouverts aux frais de l\'État.'; } },
        { txt: 'Concession à un groupe étranger', effet: (E, i) => { E.tresor[i] += E.pib[i] * 3; E.approb[i] -= 4; E.corrupt[i] += 3; return 'Chèque immédiat, souveraineté entamée.'; } }
      ]
    },
    {
      icone: '🧠', titre: 'Fuite d\'un modèle de pointe',
      texte: "Les poids de votre modèle d'IA le plus avancé circulent sur les réseaux. Le monde entier peut les télécharger.",
      cond: (E, i) => E.ia[i] >= 3,
      choix: [
        { txt: 'Étouffer l\'affaire', effet: (E, i) => { E.corrupt[i] += 4; for (let k = 0; k < G.N; k++) if (k !== i) E.calcul[k] *= 1.02; return 'Silence obtenu, la fuite fait son chemin.'; } },
        { txt: 'Publier officiellement et prendre la tête de l\'IA ouverte', effet: (E, i) => { E.reput[i] += 12; E.approb[i] += 5; E.calcul[i] *= 0.94; return 'Prestige mondial, avance rognée.'; } }
      ]
    },
    {
      icone: '🤖', titre: 'Automatisation massive',
      texte: "Vos entreprises remplacent des centaines de milliers de postes par des systèmes autonomes. Les gains de productivité sont réels, les licenciements aussi.",
      cond: (E, i) => E.ia[i] >= 4,
      choix: [
        { txt: 'Revenu de transition financé par l\'impôt', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 2; E.approb[i] += 8; E.chomage[i] -= 1.5; return 'Filet social déployé.'; } },
        { txt: 'Laisser le marché s\'ajuster', effet: (E, i) => { E.chomage[i] += 3; E.approb[i] -= 9; E.croiss[i] += 1.2; return 'Croissance plus forte, société sous tension.'; } },
        { txt: 'Taxer les robots', effet: (E, i) => { E.tresor[i] += E.pib[i] * 1.4; E.croiss[i] -= 0.9; return 'Recettes nouvelles, investissement ralenti.'; } }
      ]
    },
    {
      icone: '⚠️', titre: 'Incident d\'IA',
      texte: "Un système autonome de gestion du réseau électrique a pris une décision imprévue. Trois régions ont été privées de courant pendant onze heures.",
      cond: (E, i) => E.ia[i] >= 5 && !E.lois.has('iaouverte'),
      choix: [
        { txt: 'Créer une autorité de contrôle', effet: (E, i) => { E.calcul[i] *= 0.96; E.approb[i] += 6; E.stab[i] += 3; return 'Sécurité renforcée, rythme ralenti.'; } },
        { txt: 'Poursuivre sans rien changer', effet: (E, i) => { E.approb[i] -= 6; E.stab[i] -= 4; return 'La course continue. L\'opinion note.'; } }
      ]
    },
    {
      icone: '🏦', titre: 'Attaque contre votre monnaie',
      texte: "Des fonds spéculatifs parient contre votre dette. Les taux montent, la monnaie décroche.",
      cond: (E, i) => E.dette[i] / (E.pib[i] * 1000) > 0.8,
      choix: [
        { txt: 'Austérité immédiate', effet: (E, i) => { E.bSante[i] *= 0.8; E.bEduc[i] *= 0.8; E.bSub[i] *= 0.7; E.approb[i] -= 10; E.dette[i] *= 0.96; return 'Marchés rassurés, rue en colère.'; } },
        { txt: 'Tenir bon et laisser filer la dette', effet: (E, i) => { E.dette[i] *= 1.05; E.inflation[i] += 2; return 'Le pari est risqué.'; } }
      ]
    },
    {
      icone: '🕵️', titre: 'Espion démasqué',
      texte: "Un agent étranger est arrêté dans un de vos laboratoires. Les preuves sont accablantes.",
      choix: [
        { txt: 'Rendre l\'affaire publique', effet: (E, i) => { E.approb[i] += 5; for (let k = 0; k < G.N; k++) if (E.rel[i * G.N + k] < -30) G.modifierRelation(i, k, -8); return 'Opinion galvanisée, tensions accrues.'; } },
        { txt: 'Échange discret de prisonniers', effet: (E, i) => { E.reput[i] += 3; return 'Réglé en coulisses, sans casse.'; } }
      ]
    },
    {
      icone: '🌾', titre: 'Mauvaise récolte',
      texte: "Sécheresse prolongée. Les silos se vident plus vite que prévu.",
      choix: [
        { txt: 'Importer en urgence', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 1.2; E.stock[i * G.NRES + R.nourriture] += E.conso[i * G.NRES + R.nourriture] * 30; return 'Les rayons restent pleins.'; } },
        { txt: 'Rationner', effet: (E, i) => { E.approb[i] -= 8; E.stab[i] -= 4; return 'Files d\'attente et ressentiment.'; } }
      ]
    },
    {
      icone: '🚀', titre: 'Programme spatial',
      texte: "Vos ingénieurs proposent un lanceur national. Coûteux, incertain, mais un pays qui lance est un pays qui compte.",
      cond: (E, i) => E.tech[i] > 60,
      choix: [
        { txt: 'Financer', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 4; E.tech[i] += 2.5; E.approb[i] += 6; E.reput[i] += 6; return 'Le drapeau ira plus haut.'; } },
        { txt: 'Renoncer', effet: (E, i) => { E.approb[i] -= 2; return 'Les crédits iront ailleurs.'; } }
      ]
    },
    {
      icone: '⚖️', titre: 'Scandale de corruption',
      texte: "Trois de vos ministres sont mis en cause dans une affaire de marchés publics truqués.",
      cond: (E, i) => E.corrupt[i] > 35,
      choix: [
        { txt: 'Les démettre et saisir la justice', effet: (E, i) => { E.corrupt[i] -= 8; E.approb[i] += 6; E.stab[i] -= 3; return 'Coup de balai salué.'; } },
        { txt: 'Les couvrir', effet: (E, i) => { E.corrupt[i] += 6; E.approb[i] -= 9; return 'Le pouvoir tient, la confiance non.'; } }
      ]
    },
    {
      icone: '🛰️', titre: 'Offre d\'un partenaire étranger',
      texte: "Une grande puissance propose de financer vos infrastructures. En échange : accès privilégié à vos ressources pendant vingt ans.",
      cond: (E, i) => E.pib[i] < 800,
      choix: [
        { txt: 'Accepter', effet: (E, i) => { E.bat[i * G.NBAT + B.route] += 6; E.bat[i * G.NBAT + B.port] += 1; E.tresor[i] += 800; E.reput[i] -= 5; return 'Routes neuves, sous-sol hypothéqué.'; } },
        { txt: 'Refuser au nom de la souveraineté', effet: (E, i) => { E.approb[i] += 5; E.reput[i] += 4; return 'Fierté préservée, chantiers ajournés.'; } }
      ]
    },
    {
      icone: '🎓', titre: 'Fuite des cerveaux',
      texte: "Vos meilleurs chercheurs partent à l'étranger : salaires trois fois supérieurs, équipements neufs.",
      cond: (E, i) => E.educ[i] > 45 && E.pib[i] / (E.pop[i] / 1e6) < 25000,
      choix: [
        { txt: 'Plan de rétention : salaires et laboratoires', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 1.6; E.bat[i * G.NBAT + B.labo] += 2; return 'Les meilleurs restent, pour l\'instant.'; } },
        { txt: 'Laisser partir et miser sur la diaspora', effet: (E, i) => { E.tech[i] -= 0.8; E.tresor[i] += 200; return 'Transferts d\'argent, savoir perdu.'; } }
      ]
    },
    {
      icone: '🔥', titre: 'Émeutes urbaines',
      texte: "Trois nuits d'affrontements dans les grandes villes. Le ministre de l'Intérieur demande des renforts.",
      cond: (E, i) => E.approb[i] < 40 || E.chomage[i] > 18,
      choix: [
        { txt: 'Répression ferme', effet: (E, i) => { E.stab[i] += 6; E.approb[i] -= 8; E.reput[i] -= 6; return 'Le calme est revenu, sous tension.'; } },
        { txt: 'Plan d\'urgence pour les quartiers', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 1.4; E.approb[i] += 7; E.chomage[i] -= 1; return 'Investissement plutôt que matraque.'; } }
      ]
    },
    {
      icone: '🤝', titre: 'Médiation demandée',
      texte: "Deux nations en conflit vous demandent d'arbitrer. Un rôle honorifique — et un piège possible.",
      cond: (E, i) => E.reput[i] > 55,
      choix: [
        { txt: 'Accepter la médiation', effet: (E, i) => { E.reput[i] += 10; for (let k = 0; k < G.N; k++) if (Math.random() < 0.15) G.modifierRelation(i, k, 4); return 'Votre stature diplomatique grandit.'; } },
        { txt: 'Se tenir à l\'écart', effet: (E, i) => { return 'Neutralité prudente.'; } }
      ]
    },
    {
      icone: '💰', titre: 'Excédent budgétaire',
      texte: "Les recettes dépassent les prévisions. Le débat sur l'usage de la cagnotte occupe tous les plateaux.",
      cond: (E, i) => E.dernierBilan[i] > E.pib[i] * 1000 / 365 * 0.08,
      choix: [
        { txt: 'Baisser les impôts', effet: (E, i) => { E.tIR[i] = c(E.tIR[i] - 0.02, 0.02, 0.55); E.approb[i] += 6; return 'Geste populaire.'; } },
        { txt: 'Rembourser la dette', effet: (E, i) => { const m = Math.min(E.dette[i], E.tresor[i] * 0.4); E.dette[i] -= m; E.tresor[i] -= m; return `${m.toFixed(0)} M$ de dette effacés.`; } },
        { txt: 'Investir dans la recherche', effet: (E, i) => { E.bat[i * G.NBAT + B.labo] += 3; E.tresor[i] *= 0.7; return 'Trois laboratoires de plus.'; } }
      ]
    },
    {
      icone: '☢️', titre: 'Prolifération',
      texte: "Vos services révèlent qu'un pays hostile est à quelques mois de l'arme nucléaire.",
      cond: (E, i) => E.tech[i] > 55,
      choix: [
        { txt: 'Alerter l\'ONU', effet: (E, i) => { E.reput[i] += 8; return 'La communauté internationale est saisie.'; } },
        { txt: 'Frappe préventive sur les installations', effet: (E, i) => { E.reput[i] -= 20; E.approb[i] += 4; for (let k = 0; k < G.N; k++) if (Math.random() < 0.3) G.modifierRelation(i, k, -10); return 'Le programme est retardé. Le monde s\'inquiète de vous.'; } },
        { txt: 'Ne rien faire', effet: (E, i) => { return 'L\'histoire jugera.'; } }
      ]
    },
    {
      icone: '📉', titre: 'Récession mondiale',
      texte: "Les grandes places financières décrochent. Les commandes s'effondrent partout.",
      choix: [
        { txt: 'Relance par la dépense publique', effet: (E, i) => { E.tresor[i] -= E.pib[i] * 3; E.croiss[i] += 2.2; E.approb[i] += 4; return 'Le carnet de commandes repart.'; } },
        { txt: 'Rigueur et confiance', effet: (E, i) => { E.croiss[i] -= 1.5; E.dette[i] *= 0.97; return 'Le choc est encaissé sans dette nouvelle.'; } }
      ]
    }
  ];
})(window.GEO = window.GEO || {});
