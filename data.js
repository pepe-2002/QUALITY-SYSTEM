/* ============================================================
   RA-QDMS — Royal Air Quality Document Management System
   Données initiales (seed) — basées sur la documentation réelle
   Royal Air : MANEX A-D, MCM, MEL, GOM, SGS, ERP, FNC ANACM…
   ============================================================ */

const SEED_DB = {
  meta: { version: 1, seededAt: "2026-07-02" },

  /* ---------- Utilisateurs et rôles ---------- */
  users: [
    { id: "u1", username: "admin",  pass: "RoyalAir2026", name: "Administrateur Système", role: "Administrateur", dept: "IT" },
    { id: "u2", username: "nayam",  pass: "Qualite2026",  name: "Nayam Madi",             role: "Responsable Qualité", dept: "Qualité" },
    { id: "u3", username: "wahidi", pass: "Direction2026", name: "M. Wahidi",             role: "Direction", dept: "Direction Générale" },
    { id: "u4", username: "ops",    pass: "Ops2026",      name: "Kamal Abdou",            role: "Operations", dept: "Opérations" },
    { id: "u5", username: "mx",     pass: "Mx2026",       name: "Ibrahim Soilihi",        role: "Maintenance", dept: "Maintenance" },
    { id: "u6", username: "ground", pass: "Ground2026",   name: "Said Hassan",            role: "Ground Handling", dept: "Escale" },
    { id: "u7", username: "pilote", pass: "Pilote2026",   name: "Cpt. Ahmed Bacar",       role: "Pilotes", dept: "Opérations Vol" },
    { id: "u8", username: "cabine", pass: "Cabine2026",   name: "Fatima Mohamed",         role: "Cabin Crew", dept: "Opérations Vol" },
    { id: "u9", username: "invite", pass: "Invite2026",   name: "Invité / Auditeur",      role: "Invités", dept: "Externe" }
  ],

  /* Droits par rôle : v = voir, e = éditer, a = approuver, x = administrer */
  roles: {
    "Administrateur":      { modules: "all", rights: "x" },
    "Responsable Qualité": { modules: "all", rights: "a" },
    "Direction":           { modules: "all", rights: "a" },
    "Operations":          { modules: ["dashboard","aircraft","manuals","procedures","checklists","crew","scheduling","training","risks"], rights: "e" },
    "Maintenance":         { modules: ["dashboard","aircraft","manuals","procedures","checklists","training","risks"], rights: "e" },
    "Ground Handling":     { modules: ["dashboard","procedures","checklists","training","scheduling","risks"], rights: "e" },
    "Pilotes":             { modules: ["dashboard","manuals","procedures","checklists","crew","scheduling","training","risks"], rights: "v" },
    "Cabin Crew":          { modules: ["dashboard","manuals","procedures","checklists","crew","scheduling","training","risks"], rights: "v" },
    "Invités":             { modules: ["dashboard","manuals","policies"], rights: "v" }
  },

  /* ---------- Flotte ---------- */
  aircraft: [
    {
      id: "ac1", immat: "D6-RAA", type: "LET 410 UVP-E20", msn: "912634", base: "Moroni (HAH)",
      status: "En service",
      docs: [
        { num: "RA-AOC-001", titre: "Air Operator Certificate (AOC)", type: "AOC", revision: "Éd.1", date: "2024-06-15", expire: "2026-06-14", statut: "Approuvé", autorite: "ANACM" },
        { num: "RA-OPS-SPEC-001", titre: "Operations Specifications", type: "OpSpecs", revision: "Rév.2", date: "2025-04-13", expire: "2026-06-14", statut: "Approuvé", autorite: "ANACM" },
        { num: "RA-CDN-001", titre: "Certificat de Navigabilité (CofA)", type: "Certificat", revision: "—", date: "2025-01-10", expire: "2026-01-09", statut: "Approuvé", autorite: "ANACM" },
        { num: "RA-CIM-001", titre: "Certificat d'Immatriculation (CofR)", type: "Certificat", revision: "—", date: "2023-08-01", expire: "", statut: "Approuvé", autorite: "ANACM" },
        { num: "RA-ASS-001", titre: "Attestation d'Assurance Responsabilité Civile", type: "Certificat", revision: "2026", date: "2026-01-01", expire: "2026-12-31", statut: "Approuvé", autorite: "Assureur" },
        { num: "RA-LSA-001", titre: "Licence Station Aéronef (Radio)", type: "Certificat", revision: "—", date: "2025-03-01", expire: "2026-08-01", statut: "Approuvé", autorite: "ANRTIC" },
        { num: "RA-W&B-001", titre: "LET 410 Weight & Balance Trim Sheet", type: "Document technique", revision: "Rév.1", date: "2025-05-20", expire: "", statut: "Approuvé", autorite: "Royal Air" }
      ]
    },
    {
      id: "ac2", immat: "5Y-SYF", type: "LET 410 UVP-E20 (affrété)", msn: "871936", base: "Moroni (HAH)",
      status: "Maintenance (Airworks Kenya)",
      docs: [
        { num: "RA-CTR-AWK-002", titre: "Contrat de maintenance Airworks Kenya 2025", type: "Contrat", revision: "Part Payment N°02", date: "2025-06-01", expire: "2025-12-31", statut: "Approuvé", autorite: "Royal Air / Airworks" },
        { num: "RA-ARC-002", titre: "Airworthiness Review Certificate (ARC)", type: "Certificat", revision: "—", date: "2025-02-15", expire: "2026-02-14", statut: "Approuvé", autorite: "KCAA" }
      ]
    }
  ],

  /* ---------- Personnel ---------- */
  personnel: [
    {
      id: "p1", nom: "Nayam Madi", fonction: "Responsable Qualité", dept: "Qualité", embauche: "2023-09-01",
      docs: [
        { type: "Attestation", titre: "Attestation formation SMQ", date: "2025-05-30", expire: "2027-05-30", statut: "Valide" },
        { type: "Attestation", titre: "Attestation formation SGS", date: "2025-05-30", expire: "2027-05-30", statut: "Valide" },
        { type: "CV", titre: "Curriculum Vitae", date: "2023-09-01", expire: "", statut: "Valide" },
        { type: "Contrat", titre: "Contrat de travail CDI", date: "2023-09-01", expire: "", statut: "Valide" },
        { type: "Nomination", titre: "Lettre de nomination Responsable Qualité", date: "2024-11-15", expire: "", statut: "Valide" }
      ],
      qualifications: ["Audit interne", "SGS", "SMQ ISO 9001", "Lois et RAC"]
    },
    {
      id: "p2", nom: "Cpt. Ahmed Bacar", fonction: "Commandant de bord LET 410", dept: "Opérations Vol", embauche: "2023-10-01",
      docs: [
        { type: "Licence", titre: "ATPL — Licence de pilote de ligne", date: "2024-03-15", expire: "2026-09-10", statut: "Valide" },
        { type: "Medical", titre: "Certificat médical Classe 1", date: "2025-09-20", expire: "2026-09-20", statut: "Valide" },
        { type: "Training", titre: "Contrôle hors ligne (OPC) LET 410", date: "2026-01-15", expire: "2026-07-15", statut: "Expire bientôt" },
        { type: "Training", titre: "CRM Recurrent", date: "2025-08-10", expire: "2026-08-10", statut: "Valide" }
      ],
      qualifications: ["LET 410 UVP-E20", "IFR", "Instructeur TRI"]
    },
    {
      id: "p3", nom: "F/O Youssouf Ali", fonction: "Copilote LET 410", dept: "Opérations Vol", embauche: "2024-02-01",
      docs: [
        { type: "Licence", titre: "CPL — Licence de pilote professionnel", date: "2024-02-01", expire: "2026-07-20", statut: "Expire bientôt" },
        { type: "Medical", titre: "Certificat médical Classe 1", date: "2025-07-01", expire: "2026-07-01", statut: "Expire bientôt" },
        { type: "Training", titre: "Formation SGS initiale", date: "2025-05-28", expire: "2027-05-28", statut: "Valide" }
      ],
      qualifications: ["LET 410 UVP-E20", "IFR"]
    },
    {
      id: "p4", nom: "Fatima Mohamed", fonction: "Chef de cabine", dept: "Opérations Vol", embauche: "2023-11-01",
      docs: [
        { type: "Licence", titre: "Attestation Cabin Crew (CCA)", date: "2023-11-01", expire: "2026-11-01", statut: "Valide" },
        { type: "Medical", titre: "Certificat médical Classe 2", date: "2025-04-15", expire: "2027-04-15", statut: "Valide" },
        { type: "Training", titre: "Sécurité-Sauvetage Recurrent", date: "2025-11-20", expire: "2026-11-20", statut: "Valide" }
      ],
      qualifications: ["LET 410", "Premiers secours", "Marchandises dangereuses Cat.11"]
    },
    {
      id: "p5", nom: "Ibrahim Soilihi", fonction: "Technicien de maintenance", dept: "Maintenance", embauche: "2023-09-15",
      docs: [
        { type: "Licence", titre: "Licence Part-66 B1.1", date: "2023-06-01", expire: "2026-06-01", statut: "Expiré" },
        { type: "Training", titre: "Facteurs humains maintenance", date: "2025-03-10", expire: "2027-03-10", statut: "Valide" },
        { type: "Qualification", titre: "Qualification de type LET 410", date: "2024-01-20", expire: "", statut: "Valide" }
      ],
      qualifications: ["Part-66 B1.1", "LET 410 UVP-E20"]
    },
    {
      id: "p6", nom: "Kamal Abdou", fonction: "Agent d'opérations (Dispatch)", dept: "Opérations", embauche: "2024-01-10",
      docs: [
        { type: "Attestation", titre: "Attestation formation Dispatch", date: "2025-05-30", expire: "2027-05-30", statut: "Valide" },
        { type: "Training", titre: "Formation sécurité en piste (RAMP)", date: "2025-05-29", expire: "2026-05-29", statut: "Expiré" }
      ],
      qualifications: ["Flight Dispatch", "Weight & Balance LET 410"]
    },
    {
      id: "p7", nom: "Said Hassan", fonction: "Chef d'escale Anjouan (AJN)", dept: "Escale", embauche: "2023-10-15",
      docs: [
        { type: "Training", titre: "Formation sécurité en piste (RAMP) — R.A Anjouan", date: "2025-05-30", expire: "2026-05-30", statut: "Expiré" },
        { type: "Training", titre: "Formation ERP — R.A Anjouan", date: "2025-05-30", expire: "2027-05-30", statut: "Valide" }
      ],
      qualifications: ["Ground Handling", "ERP"]
    },
    {
      id: "p8", nom: "Sylvain N.", fonction: "Instructeur / Consultant Qualité", dept: "Qualité", embauche: "2024-05-01",
      docs: [
        { type: "Attestation", titre: "Attestation instructeur SGS / SMQ", date: "2025-05-30", expire: "2027-05-30", statut: "Valide" },
        { type: "Contrat", titre: "Contrat de prestation", date: "2025-01-01", expire: "2026-12-31", statut: "Valide" }
      ],
      qualifications: ["SGS", "SMQ", "Audit", "ERP", "RAMP Safety"]
    }
  ],

  /* ---------- Documents (registre central) ---------- */
  documents: [
    /* Manuels */
    { id: "d1",  module: "manuals", categorie: "Manuel", num: "RA-OMA", titre: "MANEX Partie A — Généralités / Fondements", revision: "Éd.1 Rév.2", date: "2025-04-13", auteur: "Direction des Opérations", verificateur: "Nayam Madi", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [
        { rev: "Éd.1 Rév.0", date: "2023-09-11", note: "1ère édition déposée à l'ANACM" },
        { rev: "Éd.1 Rév.1", date: "2023-12-15", note: "Corrections suite remarques ANACM (Manex Chap 0-2)" },
        { rev: "Éd.1 Rév.2", date: "2025-04-13", note: "Approbation ANACM du 13/04/2025" }
      ] },
    { id: "d2",  module: "manuals", categorie: "Manuel", num: "RA-OMB", titre: "MANEX Partie B — Utilisation de l'avion (LET 410)", revision: "Éd.1 Rév.2", date: "2025-04-13", auteur: "Direction des Opérations", verificateur: "Cpt. Ahmed Bacar", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Éd.1 Rév.2", date: "2025-04-13", note: "Approbation Manex B ANACM du 13/04/2025" }] },
    { id: "d3",  module: "manuals", categorie: "Manuel", num: "RA-OMC", titre: "MANEX Partie C — Routes et aérodromes", revision: "Éd.1 Rév.2", date: "2025-04-13", auteur: "Direction des Opérations", verificateur: "Kamal Abdou", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Éd.1 Rév.2", date: "2025-04-13", note: "Approbation Manex C ANACM du 13/04/2025" }] },
    { id: "d4",  module: "manuals", categorie: "Manuel", num: "RA-OMD", titre: "MANEX Partie D — Formation du personnel", revision: "Éd.1 Rév.2", date: "2025-04-13", auteur: "Direction des Opérations", verificateur: "Sylvain N.", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Éd.1 Rév.2", date: "2025-04-13", note: "Approbation Manex D ANACM du 13/04/2025" }] },
    { id: "d5",  module: "manuals", categorie: "Manuel", num: "RA-MEL", titre: "MEL — Minimum Equipment List LET 410", revision: "Éd. Avril 2024 Rév.1", date: "2025-04-13", auteur: "Maintenance", verificateur: "Ibrahim Soilihi", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Rév.1", date: "2025-04-13", note: "Approbation du MEL ANACM 13/04/2025" }] },
    { id: "d6",  module: "manuals", categorie: "Manuel", num: "RA-MCM", titre: "MCM — Maintenance Control Manual", revision: "Éd. Jan 2024 Rév.2", date: "2025-04-14", auteur: "Maintenance", verificateur: "Ibrahim Soilihi", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [
        { rev: "Rév.1", date: "2024-01-05", note: "MCM corrigé en janvier 2024 (Partie 0)" },
        { rev: "Rév.2", date: "2025-04-14", note: "Approbation MCM ANACM du 14/04/2025" }
      ] },
    { id: "d7",  module: "manuals", categorie: "Manuel", num: "RA-AMP", titre: "AMP — Programme d'entretien aéronef", revision: "Éd. 15/12/2023 Rév.1", date: "2025-04-14", auteur: "Maintenance", verificateur: "Ibrahim Soilihi", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Rév.1", date: "2025-04-14", note: "Approbation AMP ANACM du 14/04/2025" }] },
    { id: "d8",  module: "manuals", categorie: "Manuel", num: "RA-GOM", titre: "GOM — Ground Operations Manual", revision: "Éd.1 Rév.1", date: "2025-04-13", auteur: "Escale", verificateur: "Said Hassan", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Rév.1", date: "2025-04-13", note: "Approbation GOM ANACM du 13/04/2025" }] },
    { id: "d9",  module: "manuals", categorie: "Manuel", num: "RA-SMS", titre: "Manuel SGS — Système de Gestion de la Sécurité", revision: "Éd.1 Rév.1", date: "2025-04-13", auteur: "Qualité / Sécurité", verificateur: "Nayam Madi", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Rév.1", date: "2025-04-13", note: "Approbation SGS ANACM du 13/04/2025" }] },
    { id: "d10", module: "manuals", categorie: "Manuel", num: "RA-ERP", titre: "ERP — Plan d'Intervention d'Urgence", revision: "Éd.1 Rév.1", date: "2025-04-13", auteur: "Qualité / Sécurité", verificateur: "Sylvain N.", approbateur: "ANACM", statut: "Approuvé", expire: "",
      historique: [{ rev: "Rév.1", date: "2025-04-13", note: "Approbation Plan d'intervention d'urgence ANACM 13/04/2025" }] },
    { id: "d11", module: "manuals", categorie: "Manuel", num: "RA-QM", titre: "Manuel Qualité Royal Air", revision: "Éd.1 Rév.0 (projet)", date: "2026-05-15", auteur: "Nayam Madi", verificateur: "Sylvain N.", approbateur: "", statut: "En révision", expire: "",
      historique: [{ rev: "Rév.0", date: "2026-05-15", note: "Projet en cours de revue interne avant dépôt ANACM" }] },
    { id: "d12", module: "manuals", categorie: "Manuel", num: "RA-SECM", titre: "Manuel de Sûreté (Security Manual)", revision: "Éd.1 Rév.0 (projet)", date: "2026-04-20", auteur: "Sûreté", verificateur: "Nayam Madi", approbateur: "", statut: "Brouillon", expire: "",
      historique: [{ rev: "Rév.0", date: "2026-04-20", note: "Rédaction en cours — chapitre AVSEC suite FNC-AE-25-AVSEC" }] },
    { id: "d13", module: "manuals", categorie: "Manuel", num: "RA-MOE", titre: "MOE — Manuel des spécifications de l'organisme d'entretien", revision: "Éd.2023 Rév.1", date: "2023-11-24", auteur: "AMO", verificateur: "Ibrahim Soilihi", approbateur: "ANACM", statut: "Archivé", expire: "",
      historique: [{ rev: "Rév.1", date: "2023-11-24", note: "Parties I à V — archivé, entretien confié à Airworks Kenya" }] },

    /* Politiques */
    { id: "d20", module: "policies", categorie: "Politique", num: "RA-POL-SAF", titre: "Politique de Sécurité (Safety Policy)", revision: "Rév.1", date: "2025-02-17", auteur: "Direction Générale", verificateur: "Nayam Madi", approbateur: "M. Wahidi (DG)", statut: "Approuvé", expire: "" },
    { id: "d21", module: "policies", categorie: "Politique", num: "RA-POL-SEC", titre: "Politique de Sûreté (Security Policy)", revision: "Rév.1 du 17/02/2025", date: "2025-02-17", auteur: "Direction Générale", verificateur: "Nayam Madi", approbateur: "M. Wahidi (DG)", statut: "Approuvé", expire: "" },
    { id: "d22", module: "policies", categorie: "Politique", num: "RA-POL-QUA", titre: "Politique Qualité", revision: "Rév.0", date: "2026-03-01", auteur: "Nayam Madi", verificateur: "Sylvain N.", approbateur: "M. Wahidi (DG)", statut: "Approuvé", expire: "" },
    { id: "d23", module: "policies", categorie: "Politique", num: "RA-POL-DA", titre: "Politique Drogues & Alcool (Drug & Alcohol Policy)", revision: "Rév.0", date: "2026-06-10", auteur: "Qualité", verificateur: "Nayam Madi", approbateur: "", statut: "En révision", expire: "" },
    { id: "d24", module: "policies", categorie: "Politique", num: "RA-POL-HF", titre: "Politique Facteurs Humains (Human Factors Policy)", revision: "Rév.0", date: "2026-06-25", auteur: "Qualité", verificateur: "", approbateur: "", statut: "Brouillon", expire: "" }
  ],

  /* ---------- Procédures (rédigées à partir des documents Royal Air) ---------- */
  procedures: [
    {
      id: "pr1", num: "DOC-PROC-001", titre: "Procédure de gestion documentaire", famille: "Quality",
      revision: "V1.0", date: "2026-01-15", auteur: "Responsable Documentation", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Définir les règles pour la création, la validation, la diffusion, la révision et l'archivage des documents de Royal Air, conformément au RAC applicable, à l'Annexe 19 OACI et à l'ISO 9001:2015 (§7.5 — Informations documentées)."],
        ["2. Domaine d'application", "S'applique à tous les documents réglementaires et techniques utilisés par Royal Air (manuels, politiques, procédures, checklists, formulaires, enregistrements)."],
        ["3. Définitions", "Document maître : version officielle valide. Révision : modification d'un document approuvé. Archivage : conservation d'une version non active."],
        ["4. Responsabilités", "Responsable Documentation : supervision globale. Éditeur : rédaction initiale. Validateur : chef de service concerné. Diffusion : département documentation. Approbation finale : Responsable Qualité et, le cas échéant, ANACM."],
        ["5.1 Création", "L'auteur rédige le document selon le modèle standard (en-tête Royal Air, cartouche de révision). Le document est transmis pour validation avec le statut « Brouillon »."],
        ["5.2 Validation", "Le chef de service concerné valide le contenu (statut « En révision »). Le Responsable Documentation effectue une vérification finale de forme et de conformité."],
        ["5.3 Diffusion", "La version validée est publiée dans le RA-QDMS avec le statut « Approuvé ». Le registre de diffusion est mis à jour et les destinataires sont notifiés."],
        ["5.4 Révision", "Toute modification passe par un formulaire de demande de révision. Même cycle de validation et de diffusion. L'historique des révisions est conservé intégralement."],
        ["5.5 Archivage", "L'ancienne version est marquée « Obsolète/Archivé », déplacée au répertoire d'archives avec date et motif, conformément à la procédure DOC-PROC-002."],
        ["6. Contrôle des documents", "Tout document porte : titre, numéro de référence, version, date d'entrée en vigueur, pagination X/Y, code de classification (ex : OP-001), auteur, vérificateur et approbateur."]
      ]
    },
    {
      id: "pr2", num: "DOC-PROC-002", titre: "Procédure de retrait des documents obsolètes", famille: "Quality",
      revision: "V1.0", date: "2026-01-15", auteur: "Responsable Documentation", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Garantir qu'aucun document périmé n'est utilisé dans les opérations, conformément à l'ISO 9001:2015 §7.5.3 et aux exigences ANACM de contrôle documentaire."],
        ["2. Déclenchement", "Le retrait est déclenché dès l'approbation d'une nouvelle révision, ou sur décision du Responsable Qualité (document annulé)."],
        ["3. Processus", "1) Identification de toutes les copies distribuées via le registre de diffusion. 2) Retrait physique et électronique des copies. 3) Marquage « OBSOLÈTE » de la copie conservée. 4) Renseignement du Formulaire de retrait de document obsolète. 5) Mise à jour du registre."],
        ["4. Conservation", "Une copie maître obsolète est conservée 5 ans minimum à des fins de traçabilité (voir DOC-PROC-003), puis détruite avec procès-verbal."],
        ["5. Enregistrements", "Formulaire de retrait signé, registre de diffusion mis à jour, journal RA-QDMS."]
      ]
    },
    {
      id: "pr3", num: "DOC-PROC-003", titre: "Méthode de conservation de la copie maître (Master Copy)", famille: "Quality",
      revision: "V1.0", date: "2026-01-15", auteur: "Responsable Documentation", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Définir les modalités de conservation des copies maîtres des documents Royal Air (papier et électronique)."],
        ["2. Copie maître électronique", "Stockée dans le RA-QDMS (Supabase Storage en production) avec sauvegarde automatique quotidienne et chiffrement. Accès en écriture réservé au Responsable Documentation."],
        ["3. Copie maître papier", "Conservée au bureau Qualité dans une armoire fermant à clé, à l'abri de l'humidité. Tampon « MASTER COPY » en première page."],
        ["4. Durées de conservation", "Manuels et amendements : durée de vie + 5 ans. Enregistrements de formation : 3 ans après départ de l'employé. Dossiers de vol : 3 mois minimum (RAC OPS). CRM/ATL : 24 mois après dernière inscription."],
        ["5. Traçabilité", "Chaque consultation ou sortie de la copie maître est inscrite au registre SUIVI DE DOCUMENT."]
      ]
    },
    {
      id: "pr4", num: "QUA-PROC-001", titre: "Procédure d'audit interne", famille: "Quality",
      revision: "V1.0", date: "2026-02-01", auteur: "Nayam Madi", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Définir la planification, la conduite et le suivi des audits internes du système qualité et sécurité de Royal Air (ISO 9001:2015 §9.2, Annexe 19 OACI, RAC OPS 1.035)."],
        ["2. Plan annuel d'audit", "Le Responsable Qualité établit un plan annuel couvrant tous les domaines (OPS, AIR, AVSEC, GRH, Escale, Sous-traitants) et toutes les stations (Moroni, Anjouan/Ouani, Mohéli) au moins une fois par an."],
        ["3. Préparation", "Notification à l'audité 15 jours avant. Élaboration de la checklist d'audit (CHK-AUD-001) basée sur le référentiel applicable."],
        ["4. Conduite", "Réunion d'ouverture, examen documentaire, observations terrain, entretiens, réunion de clôture avec présentation des constats."],
        ["5. Constats", "Chaque écart fait l'objet d'une Fiche de Non-Conformité (FNC) numérotée : FNC-AE-AA-DOMAINE-XX-NN. Classement : Niveau 1 (majeur, 15 jours), Niveau 2 (30-60 jours), Observation."],
        ["6. Suivi", "L'audité propose un plan d'action correctif (analyse cause racine incluse). Le Responsable Qualité valide, suit les échéances dans le RA-QDMS et clôture après vérification d'efficacité."],
        ["7. Rapport", "Rapport d'audit diffusé sous 10 jours ouvrés à la Direction et à l'audité. Synthèse annuelle en revue de direction."]
      ]
    },
    {
      id: "pr5", num: "QUA-PROC-002", titre: "Gestion des non-conformités et actions correctives", famille: "Quality",
      revision: "V1.0", date: "2026-02-01", auteur: "Nayam Madi", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Traiter les non-conformités internes et externes (ANACM, clients, sous-traitants) et prévenir leur récurrence (ISO 9001:2015 §10.2)."],
        ["2. Enregistrement", "Toute FNC est enregistrée dans le Tableau de suivi des FNC avec : référence, source, description, exigence non respectée, niveau, échéance."],
        ["3. Analyse des causes", "Méthode des 5 Pourquoi ou Ishikawa. L'action corrective traite la cause racine, pas seulement le symptôme."],
        ["4. Plan d'action correctif", "Actions, responsables, échéances. Validation par le Responsable Qualité avant transmission à l'ANACM le cas échéant."],
        ["5. Vérification d'efficacité", "Contrôle à échéance + vérification d'efficacité 3 mois après clôture. Réouverture si récurrence."],
        ["6. Indicateurs", "Taux de clôture dans les délais, FNC ouvertes par domaine, âge moyen des FNC — suivis au tableau de bord RA-QDMS."]
      ]
    },
    {
      id: "pr6", num: "OPS-PROC-001", titre: "Préparation et suivi des vols (Flight Dispatch)", famille: "Flight Operations",
      revision: "V1.0", date: "2026-03-01", auteur: "Kamal Abdou", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Définir la préparation des vols Royal Air conformément au MANEX A/C et au RAC OPS 1."],
        ["2. Dossier de vol (Flight Dispatch Folio)", "Contenu : plan de vol exploitation (OFP), NOTAM, météo (METAR/TAF HAH-AJN-NWA), devis de masse et centrage (LET 410 Trim Sheet), liste passagers/fret, MEL le cas échéant."],
        ["3. Devis de masse et centrage", "Établi sur le LET 410 W&B Trim Sheet approuvé. Vérification des limites MTOW/MLW et du centrage avant chaque vol. Signature du CDB obligatoire."],
        ["4. Suivi du vol", "Le dispatch assure le suivi (movement message, heures bloc). Le Daily Voyage Report est renseigné et archivé."],
        ["5. Conservation", "Dossier de vol conservé 3 mois minimum au bureau OPS."]
      ]
    },
    {
      id: "pr7", num: "GRD-PROC-001", titre: "Sécurité en piste (Ramp Safety)", famille: "Ground Procedures",
      revision: "V1.0", date: "2026-03-01", auteur: "Said Hassan", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Prévenir les dommages aux aéronefs et les accidents de personnes en piste (Moroni, Anjouan/Ouani, Mohéli), conformément au GOM."],
        ["2. Zones et périmètres", "Périmètre de sécurité hélices : 5 m. Aucune circulation sous voilure moteur tournant. Zone ERA balisée avant arrivée avion."],
        ["3. EPI obligatoires", "Gilet haute visibilité, protection auditive à moins de 30 m moteurs tournants, chaussures de sécurité."],
        ["4. Avitaillement", "Pas d'avitaillement passagers à bord sans procédure spécifique MANEX A 8.2. Extincteur à proximité. Mise à la terre."],
        ["5. FOD", "Inspection FOD de l'aire avant chaque arrivée/départ (checklist CHK-RAMP-001). Collecte et signalement au chef d'escale."],
        ["6. Incidents", "Tout dommage ou presque-accident en piste est rapporté sous 24h via le système de comptes rendus SGS."]
      ]
    },
    {
      id: "pr8", num: "SEC-PROC-001", titre: "Contrôle des accès et gestion des badges", famille: "Security",
      revision: "V1.0", date: "2026-04-01", auteur: "Sûreté", statut: "En révision",
      contenu: [
        ["1. Objet", "Contrôler l'accès aux zones de sûreté à réglementation d'accès (documents, bureaux, aire de trafic), conformément au Programme de Sûreté et à l'Annexe 17 OACI."],
        ["2. Tableau de suivi des accès", "Tout accès aux locaux Qualité/Documentation est enregistré : nom, date, motif, heure entrée/sortie, visa."],
        ["3. Badges", "Attribution nominative validée par le responsable sûreté. Restitution à la fin du contrat. Inventaire trimestriel."],
        ["4. Visiteurs", "Accompagnement permanent par un titulaire de badge. Registre visiteurs à l'accueil."],
        ["5. Sensibilisation", "Programme de sensibilisation sûreté Royal Air dispensé à tout nouvel employé et recyclage tous les 24 mois."]
      ]
    },
    {
      id: "pr9", num: "SMS-PROC-001", titre: "Comptes rendus d'événements de sécurité", famille: "Safety",
      revision: "V1.0", date: "2026-03-15", auteur: "Qualité / Sécurité", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Organiser le recueil, l'analyse et le traitement des comptes rendus d'événements conformément au Manuel SGS et à l'Annexe 19 OACI."],
        ["2. Culture juste", "Aucune sanction pour un signalement de bonne foi. Signalement confidentiel possible auprès du Responsable SGS."],
        ["3. Délais", "Événement notifiable ANACM : 72 h. Compte rendu interne : 48 h via formulaire SGS."],
        ["4. Analyse des risques", "Matrice de risque 5x5 (probabilité x gravité) du Manuel SGS. Actions de mitigation suivies au registre des risques."],
        ["5. Retour d'information", "Le rapporteur est informé des suites. Les enseignements sont diffusés (bulletins sécurité, indoctrination)."]
      ]
    },
    {
      id: "pr10", num: "MNT-PROC-001", titre: "Suivi de navigabilité et coordination AMO", famille: "Maintenance",
      revision: "V1.0", date: "2026-03-20", auteur: "Ibrahim Soilihi", statut: "Approuvé",
      contenu: [
        ["1. Objet", "Assurer le maintien de la navigabilité de la flotte LET 410 conformément au MCM et au RAC 08 Part M."],
        ["2. Programme d'entretien", "Application de l'AMP approuvé ANACM (14/04/2025). Suivi des heures/cycles et butées dans le tableau de suivi navigabilité."],
        ["3. Coordination AMO", "Entretien confié à Airworks Kenya (AMO agréé KCAA). Contrat et paiements suivis au registre contrats. Vérification des CRS à chaque restitution."],
        ["4. AD/SB", "Revue des consignes de navigabilité à réception et au minimum mensuelle. Enregistrement de l'applicabilité et de l'accomplissement."],
        ["5. Déclaration de conformité", "Déclaration RAC 08 Part M (Form 07) tenue à jour et re-déposée à l'ANACM à chaque changement significatif."]
      ]
    }
  ],

  /* ---------- Checklists (version contrôlée) ---------- */
  checklists: [
    {
      id: "ck1", num: "CHK-AUD-001", titre: "Checklist d'audit interne — Station", revision: "V1.0", date: "2026-02-01", statut: "Approuvé", famille: "Quality",
      items: [
        "Organigramme de la station affiché et à jour",
        "Fiches de poste signées et disponibles",
        "Manuels applicables (MANEX, GOM) en dernière révision",
        "Registre de diffusion documentaire à jour",
        "Formations du personnel valides (RAMP, ERP, sûreté)",
        "Checklists opérationnelles en version contrôlée",
        "Tableau de suivi des accès renseigné",
        "Matériel de piste conforme et inspecté (FOD, EPI)",
        "Comptes rendus SGS disponibles et traités",
        "Actions correctives des FNC précédentes soldées"
      ]
    },
    {
      id: "ck2", num: "CHK-DOC-001", titre: "Checklist de contrôle documentaire", revision: "V1.0", date: "2026-01-20", statut: "Approuvé", famille: "Quality",
      items: [
        "Le document porte un numéro de référence unique",
        "Cartouche de révision complet (rév., date, pages)",
        "Auteur, vérificateur et approbateur identifiés",
        "Liste des pages effectives (LEP) à jour",
        "Registre des révisions renseigné",
        "Conformité au modèle standard Royal Air",
        "Références réglementaires citées (RAC, OACI, ISO)",
        "Anciennes versions retirées et marquées OBSOLÈTE",
        "Copie maître identifiée et sécurisée",
        "Diffusion enregistrée au registre"
      ]
    },
    {
      id: "ck3", num: "CHK-OPS-001", titre: "Checklist Dispatch avant vol (RAS OPS)", revision: "V1.0", date: "2026-03-01", statut: "Approuvé", famille: "Flight Operations",
      items: [
        "Plan de vol exploitation (OFP) établi et vérifié",
        "NOTAM HAH / AJN / NWA consultés",
        "Dossier météo (METAR/TAF) joint au folio",
        "Devis de masse et centrage LET 410 signé CDB",
        "Carburant conforme à la politique MANEX A",
        "MEL vérifiée — items ouverts acceptables",
        "Documents de bord valides (AOC, assurance, CDN, LSA)",
        "Manifeste passagers / fret finalisé",
        "Briefing équipage effectué",
        "Daily Voyage Report préparé"
      ]
    },
    {
      id: "ck4", num: "CHK-RAMP-001", titre: "Checklist inspection piste (Ramp/FOD)", revision: "V1.0", date: "2026-03-01", statut: "Approuvé", famille: "Ground Procedures",
      items: [
        "Inspection FOD de l'aire de stationnement effectuée",
        "Balisage et cônes en place",
        "EPI portés par tout le personnel en piste",
        "Extincteur disponible et en cours de validité",
        "Cales et matériel de piste en bon état",
        "Zone hélices dégagée avant mise en route",
        "Chargement conforme au devis de masse",
        "Aucun avitaillement non autorisé passagers à bord",
        "Passagers escortés sur cheminement balisé",
        "Anomalies signalées au chef d'escale"
      ]
    },
    {
      id: "ck5", num: "CHK-SMS-001", titre: "Checklist d'évaluation SGS (conformité Annexe 19)", revision: "V1.0", date: "2026-03-15", statut: "Approuvé", famille: "Safety",
      items: [
        "Politique de sécurité signée par le Dirigeant Responsable",
        "Responsable SGS nommé et formé",
        "Registre des risques tenu à jour",
        "Système de comptes rendus opérationnel",
        "Indicateurs de performance sécurité (SPI) définis",
        "Revues de sécurité tenues (comité SGS)",
        "Plan de mise en œuvre SGS suivi (phases 1-4)",
        "Formation SGS initiale et récurrente tracée",
        "ERP testé (exercice) dans les 24 derniers mois",
        "Interfaces sous-traitants (Airworks, escales) maîtrisées"
      ]
    },
    {
      id: "ck6", num: "CHK-AMO-001", titre: "Checklist de surveillance AMO / sous-traitant", revision: "V1.0", date: "2026-03-20", statut: "En révision", famille: "Maintenance",
      items: [
        "Agrément AMO valide (portée couvrant LET 410)",
        "Contrat de maintenance signé et en vigueur",
        "Personnel de certification qualifié (Part-66)",
        "CRS émis conformes après chaque chantier",
        "Traitement AD/SB documenté",
        "Outillage étalonné (registre d'étalonnage)",
        "Pièces avec certificats (Form 1 / 8130-3)",
        "Audit du sous-traitant réalisé dans les 12 mois",
        "FNC du sous-traitant suivies et clôturées",
        "Rapports de fiabilité transmis à l'exploitant"
      ]
    }
  ],

  /* ---------- Audits & FNC ---------- */
  audits: [
    { id: "a1", type: "Interne", ref: "AUD-INT-26-01", titre: "Audit interne — Station Aéroport de Ouani (Anjouan)", domaine: "Escale / OPS", date: "2026-07-21", statut: "Planifié", auditeur: "Nayam Madi", checklist: "CHK-AUD-001" },
    { id: "a2", type: "Interne", ref: "AUD-INT-26-02", titre: "Audit interne — Documentation et SMQ Moroni", domaine: "Qualité", date: "2026-05-12", statut: "Clôturé", auditeur: "Sylvain N.", checklist: "CHK-DOC-001" },
    { id: "a3", type: "Interne", ref: "AUD-INT-26-03", titre: "Audit interne — Station Mohéli", domaine: "Escale", date: "2026-09-15", statut: "Planifié", auditeur: "Nayam Madi", checklist: "CHK-AUD-001" },
    { id: "a4", type: "Externe", ref: "ANACM-PH4-25", titre: "Inspections ANACM Phase 4 — Certification AOC", domaine: "Tous domaines", date: "2025-07-10", statut: "Clôturé", auditeur: "ANACM", checklist: "" },
    { id: "a5", type: "Externe", ref: "AUD-EXT-26-01", titre: "Audit de surveillance ANACM (reprogrammé)", domaine: "OPS / AIR / AVSEC", date: "2026-08-18", statut: "Planifié", auditeur: "ANACM", checklist: "" },
    { id: "a6", type: "Interne", ref: "AUD-SST-26-01", titre: "Audit sous-traitant — Airworks Kenya (AMO)", domaine: "Maintenance", date: "2026-10-06", statut: "Planifié", auditeur: "Nayam Madi + Ibrahim Soilihi", checklist: "CHK-AMO-001" }
  ],

  fnc: [
    { id: "f1", ref: "FNC-AE-25-OPS-01-76", source: "ANACM Phase 4", domaine: "OPS", niveau: "Niveau 2", description: "Suivi des temps de vol et de repos des équipages non formalisé", action: "Mise en place du tableau de suivi des temps de vol/repos et intégration au module Scheduling du RA-QDMS", responsable: "Kamal Abdou", echeance: "2026-07-15", statut: "En cours" },
    { id: "f2", ref: "FNC-AE-25-OPS-01-77", source: "ANACM Phase 4", domaine: "OPS", niveau: "Niveau 2", description: "Dossiers de vol incomplets (NOTAM manquants sur 2 folios)", action: "Application stricte de la checklist CHK-OPS-001 avant chaque vol, contrôle qualité mensuel des folios", responsable: "Kamal Abdou", echeance: "2026-06-30", statut: "Clôturée" },
    { id: "f3", ref: "FNC-AE-25-AVSEC-01-01", source: "ANACM Phase 4", domaine: "AVSEC", niveau: "Niveau 2", description: "Programme de sensibilisation sûreté non déployé sur toutes les stations", action: "Déploiement du programme de sensibilisation Royal Air à Anjouan et Mohéli, feuilles d'émargement archivées", responsable: "Said Hassan", echeance: "2026-07-31", statut: "En cours" },
    { id: "f4", ref: "FNC-AE-25-AVSEC-01-02", source: "ANACM Phase 4", domaine: "AVSEC", niveau: "Observation", description: "Tableau de suivi des accès partiellement renseigné", action: "Rappel de la procédure SEC-PROC-001, contrôle hebdomadaire par le chef d'escale", responsable: "Sûreté", echeance: "2026-06-15", statut: "Clôturée" },
    { id: "f5", ref: "FNC-AE-25-AVSEC-01-03", source: "ANACM Phase 4", domaine: "AVSEC", niveau: "Niveau 2", description: "Manuel de sûreté en cours de rédaction, non encore déposé", action: "Finaliser le Manuel de Sûreté (RA-SECM) et le déposer à l'ANACM pour approbation", responsable: "Nayam Madi", echeance: "2026-08-30", statut: "En cours" },
    { id: "f6", ref: "FNC-AE-25-AIR-01-13", source: "ANACM Phase 4", domaine: "AIR", niveau: "Niveau 2", description: "Licence Part-66 du technicien expirée, prorogation non demandée", action: "Renouvellement de la licence B1.1 d'Ibrahim Soilihi auprès de l'autorité, suivi des échéances dans RA-QDMS", responsable: "Ibrahim Soilihi", echeance: "2026-07-20", statut: "En retard" },
    { id: "f7", ref: "FNC-AE-25-AIR-01-14", source: "ANACM Phase 4", domaine: "AIR", niveau: "Observation", description: "Registre AD/SB sans revue mensuelle tracée", action: "Mise en place de la revue mensuelle AD/SB conformément à MNT-PROC-001", responsable: "Ibrahim Soilihi", echeance: "2026-06-30", statut: "Clôturée" },
    { id: "f8", ref: "FNC-AE-25-AIR-01-16", source: "ANACM Phase 4", domaine: "AIR", niveau: "Niveau 2", description: "Déclaration de conformité RAC 08 Part M à mettre à jour (Form 07)", action: "Mise à jour et re-dépôt de la déclaration de conformité corrigée à l'ANACM", responsable: "Ibrahim Soilihi", echeance: "2026-09-15", statut: "En cours" }
  ],

  /* ---------- Formations ---------- */
  trainings: [
    { id: "t1", titre: "Formation SGS (initiale)", ref: "TRG-SGS-INIT", duree: "3 jours", validite: 24, prochaine: "2026-09-08", participants: ["Nouvel employé escale Mohéli"], statut: "Planifiée", formateur: "Sylvain N." },
    { id: "t2", titre: "Sécurité en piste (RAMP Safety) — recyclage", ref: "TRG-RAMP-REC", duree: "1 jour", validite: 12, prochaine: "2026-07-10", participants: ["Kamal Abdou", "Said Hassan", "Équipe escale Moroni"], statut: "Planifiée", formateur: "Sylvain N." },
    { id: "t3", titre: "ERP — Plan d'intervention d'urgence (exercice)", ref: "TRG-ERP-EX", duree: "1 jour", validite: 24, prochaine: "2026-11-05", participants: ["Toutes stations"], statut: "Planifiée", formateur: "Sylvain N." },
    { id: "t4", titre: "SMQ / Lois et RAC — recyclage", ref: "TRG-SMQ-REC", duree: "2 jours", validite: 24, prochaine: "2027-05-30", participants: ["Nayam Madi", "Direction"], statut: "Planifiée", formateur: "Consultant externe" },
    { id: "t5", titre: "Marchandises dangereuses (DG) Cat. 10", ref: "TRG-DG-10", duree: "2 jours", validite: 24, prochaine: "2026-08-20", participants: ["Kamal Abdou", "Fatima Mohamed"], statut: "Planifiée", formateur: "Organisme agréé" },
    { id: "t6", titre: "CRM récurrent équipages", ref: "TRG-CRM-REC", duree: "1 jour", validite: 12, prochaine: "2026-08-10", participants: ["Cpt. Ahmed Bacar", "F/O Youssouf Ali", "Fatima Mohamed"], statut: "Planifiée", formateur: "Cpt. Ahmed Bacar (TRI)" },
    { id: "t7", titre: "Cours d'endoctrinement compagnie (Company Indoc)", ref: "TRG-INDOC", duree: "2 jours", validite: 0, prochaine: "2026-07-28", participants: ["Nouveaux employés"], statut: "Planifiée", formateur: "Nayam Madi" }
  ],

  /* ---------- Équipages ---------- */
  crew: [
    { id: "c1", nom: "Cpt. Ahmed Bacar", type: "Pilote", poste: "CDB LET 410", licence: "ATPL", licExp: "2026-09-10", medExp: "2026-09-20", quals: ["LET 410", "IFR", "TRI"], statut: "Apte" },
    { id: "c2", nom: "F/O Youssouf Ali", type: "Pilote", poste: "OPL LET 410", licence: "CPL", licExp: "2026-07-20", medExp: "2026-07-01", quals: ["LET 410", "IFR"], statut: "Vigilance échéances" },
    { id: "c3", nom: "Fatima Mohamed", type: "Cabin Crew", poste: "Chef de cabine", licence: "CCA", licExp: "2026-11-01", medExp: "2027-04-15", quals: ["LET 410", "DG Cat.11", "Premiers secours"], statut: "Apte" },
    { id: "c4", nom: "Amina Said", type: "Cabin Crew", poste: "Hôtesse", licence: "CCA", licExp: "2027-02-15", medExp: "2026-10-05", quals: ["LET 410", "Premiers secours"], statut: "Apte" }
  ],

  /* ---------- Planning (vols, congés) ---------- */
  flights: [
    { id: "v1", date: "2026-07-03", num: "RLK101", route: "HAH → AJN", dep: "06:30", arr: "07:00", avion: "D6-RAA", cdb: "Cpt. Ahmed Bacar", opl: "F/O Youssouf Ali", pnc: "Fatima Mohamed", statut: "Programmé" },
    { id: "v2", date: "2026-07-03", num: "RLK102", route: "AJN → HAH", dep: "07:30", arr: "08:00", avion: "D6-RAA", cdb: "Cpt. Ahmed Bacar", opl: "F/O Youssouf Ali", pnc: "Fatima Mohamed", statut: "Programmé" },
    { id: "v3", date: "2026-07-03", num: "RLK201", route: "HAH → NWA", dep: "09:00", arr: "09:25", avion: "D6-RAA", cdb: "Cpt. Ahmed Bacar", opl: "F/O Youssouf Ali", pnc: "Amina Said", statut: "Programmé" },
    { id: "v4", date: "2026-07-03", num: "RLK202", route: "NWA → HAH", dep: "10:00", arr: "10:25", avion: "D6-RAA", cdb: "Cpt. Ahmed Bacar", opl: "F/O Youssouf Ali", pnc: "Amina Said", statut: "Programmé" },
    { id: "v5", date: "2026-07-04", num: "RLK103", route: "HAH → AJN", dep: "06:30", arr: "07:00", avion: "D6-RAA", cdb: "Cpt. Ahmed Bacar", opl: "F/O Youssouf Ali", pnc: "Fatima Mohamed", statut: "Programmé" },
    { id: "v6", date: "2026-07-02", num: "RLK101", route: "HAH → AJN", dep: "06:30", arr: "07:02", avion: "D6-RAA", cdb: "Cpt. Ahmed Bacar", opl: "F/O Youssouf Ali", pnc: "Fatima Mohamed", statut: "Réalisé" }
  ],

  leaves: [
    { id: "l1", nom: "Fatima Mohamed", type: "Congé annuel", debut: "2026-07-20", fin: "2026-08-03", statut: "Approuvé" },
    { id: "l2", nom: "Kamal Abdou", type: "Congé annuel", debut: "2026-08-10", fin: "2026-08-24", statut: "Demandé" },
    { id: "l3", nom: "Ibrahim Soilihi", type: "Formation externe", debut: "2026-07-18", fin: "2026-07-22", statut: "Approuvé" }
  ],

  /* ---------- Registre des risques SGS (matrice OACI 5x5) ----------
     p = probabilité (1 Extrêmement improbable … 5 Fréquent)
     g = gravité (1 Négligeable … 5 Catastrophique)
     L'indice, le score et la tolérabilité sont CALCULÉS automatiquement. */
  risks: [
    { id: "r1", ref: "RISK-26-01", danger: "FOD sur l'aire de trafic (Ouani, Mohéli)", domaine: "Ground",
      consequences: "Ingestion / dommage hélices LET 410, dommage aéronef",
      pi: 3, gi: 3, mitigation: "Inspection FOD systématique avant chaque arrivée/départ (CHK-RAMP-001), sensibilisation du personnel de piste (GRD-PROC-001)",
      pr: 2, gr: 3, responsable: "Said Hassan", revue: "2026-10-01", statut: "Maîtrisé" },
    { id: "r2", ref: "RISK-26-02", danger: "Vol avec licence, qualification ou medical expiré", domaine: "OPS",
      consequences: "Non-conformité RAC OPS, retrait AOC, assurance invalidée",
      pi: 3, gi: 4, mitigation: "Alertes automatiques d'échéances RA-QDMS à 60 j, contrôle dispatch avant affectation équipage (CHK-OPS-001)",
      pr: 1, gr: 4, responsable: "Nayam Madi", revue: "2026-09-15", statut: "Maîtrisé" },
    { id: "r3", ref: "RISK-26-03", danger: "Dossier de vol incomplet (NOTAM, météo)", domaine: "OPS",
      consequences: "Préparation de vol inadéquate, déroutement non anticipé (FNC-AE-25-OPS-01-77)",
      pi: 3, gi: 3, mitigation: "Checklist dispatch obligatoire avant chaque vol, contrôle qualité mensuel des folios",
      pr: 2, gr: 3, responsable: "Kamal Abdou", revue: "2026-08-30", statut: "Maîtrisé" },
    { id: "r4", ref: "RISK-26-04", danger: "Erreur de masse et centrage LET 410", domaine: "OPS",
      consequences: "Dépassement MTOW / centrage hors limites, perte de contrôle",
      pi: 2, gi: 5, mitigation: "Trim Sheet approuvé obligatoire, double contrôle dispatch + CDB, pesée fret systématique",
      pr: 1, gr: 5, responsable: "Kamal Abdou", revue: "2026-09-30", statut: "Maîtrisé" },
    { id: "r5", ref: "RISK-26-05", danger: "Dépendance à un AMO unique distant (Airworks Kenya)", domaine: "AIR",
      consequences: "Immobilisation prolongée avion, pression opérationnelle sur la planification",
      pi: 3, gi: 2, mitigation: "Planification anticipée des chantiers, stock de pièces critiques, veille sur AMO alternatifs de la région",
      pr: 3, gr: 2, responsable: "Ibrahim Soilihi", revue: "2026-11-15", statut: "Ouvert" },
    { id: "r6", ref: "RISK-26-06", danger: "Météo inter-îles dégradée (saison kashkazi)", domaine: "OPS",
      consequences: "Déroutement, atterrissage en conditions limites",
      pi: 4, gi: 3, mitigation: "Minima MANEX C respectés, emport carburant dégagement systématique, formation météo tropicale équipages",
      pr: 3, gr: 2, responsable: "Cpt. Ahmed Bacar", revue: "2026-12-01", statut: "Maîtrisé" },
    { id: "r7", ref: "RISK-26-07", danger: "Accès non contrôlé aux zones et documents sensibles", domaine: "AVSEC",
      consequences: "Atteinte à la sûreté, perte ou altération de documents réglementaires (FNC-AE-25-AVSEC-01-02)",
      pi: 3, gi: 3, mitigation: "Procédure SEC-PROC-001, tableau de suivi des accès contrôlé chaque semaine, badges nominatifs",
      pr: 2, gr: 2, responsable: "Sûreté", revue: "2026-08-15", statut: "Maîtrisé" },
    { id: "r8", ref: "RISK-26-08", danger: "Incursion de piste (personnes, animaux) sur aérodromes secondaires", domaine: "OPS",
      consequences: "Collision au décollage / atterrissage",
      pi: 3, gi: 4, mitigation: "Coordination avec l'exploitant d'aérodrome, inspection visuelle avant atterrissage, remise de gaz au moindre doute",
      pr: 2, gr: 4, responsable: "Cpt. Ahmed Bacar", revue: "2026-07-25", statut: "Ouvert" }
  ],

  /* ---------- Journal (traçabilité) ---------- */
  journal: [
    { date: "2026-07-01 08:12", user: "nayam", action: "Connexion au système" },
    { date: "2026-07-01 08:25", user: "nayam", action: "Consultation MANEX Partie A (RA-OMA)" },
    { date: "2026-06-30 16:40", user: "admin", action: "Sauvegarde automatique effectuée" }
  ],

  /* Notifications manuelles (les alertes d'échéances sont calculées automatiquement) */
  notices: [
    { date: "2026-06-28", type: "info", texte: "Revue de direction Qualité programmée le 15/09/2026." },
    { date: "2026-06-25", type: "warn", texte: "Audit de surveillance ANACM reprogrammé au 18/08/2026 — préparer les preuves de clôture des FNC." }
  ]
};
