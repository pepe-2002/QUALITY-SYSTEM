# RA-QDMS — Royal Air Quality Document Management System

Plateforme web du Département Qualité de Royal Air : gestion des documents réglementaires
avec traçabilité complète, contrôle des versions et accès par rôles (ANACM · OACI · ISO 9001:2015).

## Lancer l'application (local)

```
py -m http.server 8456 --directory RA-QDMS
```

Puis ouvrir http://localhost:8456

## Comptes de démonstration

| Identifiant | Mot de passe   | Rôle                 |
|-------------|----------------|----------------------|
| admin       | RoyalAir2026   | Administrateur       |
| nayam       | Qualite2026    | Responsable Qualité  |
| wahidi      | Direction2026  | Direction            |
| ops         | Ops2026        | Operations           |
| mx          | Mx2026         | Maintenance          |
| ground      | Ground2026     | Ground Handling      |
| pilote      | Pilote2026     | Pilotes              |
| cabine      | Cabine2026     | Cabin Crew           |
| invite      | Invite2026     | Invités (lecture)    |

Chaque rôle ne voit que les modules et droits qui lui sont nécessaires.

## Modules

1. **Aircraft** — AOC, OpSpecs, certificats D6-RAA / 5Y-SYF
2. **Personnel** — dossiers individuels (licences, medical, formations, CV, contrats), recherche par nom
3. **Manuals** — MANEX A/B/C/D, MEL, MCM, AMP, GOM, SGS, ERP, Manuel Qualité, Manuel de Sûreté, MOE (historique + workflow d'approbation)
4. **Policies** — Safety, Security, Quality, Drug & Alcohol, Human Factors
5. **Audit** — plan annuel, audits internes/externes, FNC ANACM Phase 4 et actions correctives avec échéances
6. **Training** — calendrier, validités, renouvellements (programme triennal 2024-2026)
7. **Procedures** — DOC-PROC, QUA-PROC, OPS-PROC, GRD-PROC, SEC-PROC, SMS-PROC, MNT-PROC (texte intégral consultable)
8. **Checklists** — checklists contrôlées interactives et imprimables
9. **Crew** — pilotes et PNC : licences, medical, qualifications
10. **Scheduling** — planning vols HAH·AJN·NWA, congés
11. **Risk Management (SGS)** — registre des risques avec **calcul automatique** :
    matrice OACI 5×5 (Doc 9859), indice (ex. 4B), score P×G et tolérabilité
    (Acceptable / Tolérable / Intolérable) calculés en direct, risque initial →
    mitigation → risque résiduel, alertes automatiques sur les risques intolérables
    et les revues en retard

Plus : tableau de bord KPI, notifications d'échéances automatiques, recherche instantanée globale,
rapports avec export Excel (CSV) et PDF (impression), journal système, mode sombre, responsive.

## Sensibilisation du personnel — les films (`sensibilisation/`)

Deux films internes du Département Qualité sur **l'accueil des passagers**, à
diffuser dans le groupe WhatsApp du personnel (jamais sur les réseaux publics) :

| Film | Public | Durée |
|---|---|---|
| `RoyalAir-accueil-agence.mp4` | comptoirs de vente et réservation | 6 min 05 |
| `RoyalAir-accueil-escale.mp4` | agents d'escale HAH · AJN · NWA | 6 min 24 |

Les deux sont **dits par une voix off française**, sur une nappe musicale qui
s'efface pendant la parole, et restent entièrement lisibles sans le son. Chacun
existe aussi en version allégée `-whatsapp.mp4` (720 × 1280, ~6,5 Mo), et
s'accompagne d'une **fiche à afficher** au comptoir et du **relevé de la voix
off**. Tout est refabriqué par `python3 sensibilisation/film.py tout` à partir
d'une source unique, `sensibilisation/scenarios.py` — voir
[`sensibilisation/README.md`](sensibilisation/README.md).

## Workflow documentaire (conforme DOC-PROC-001)

Brouillon → En révision → **Approuvé** (signature électronique) → Archivé.
Chaque transition est enregistrée dans l'historique du document et le journal système.

## Données

Version locale : les données sont stockées dans le navigateur (localStorage), pré-remplies avec
les documents réels de Royal Air (approbations ANACM d'avril 2025, FNC Phase 4, personnel, flotte LET 410).

Pour réinitialiser les données : console du navigateur → `localStorage.removeItem("raqdms_db_v1")` puis recharger.

## Mise en production 🚀

**Suivre le fichier [GUIDE-MISE-EN-LIGNE.md](GUIDE-MISE-EN-LIGNE.md)** (~15 min) :

1. **Supabase** : créer un nouveau projet (n'affecte pas les projets existants),
   exécuter `supabase-schema.sql` (table d'état + sauvegardes automatiques des
   30 dernières versions), copier l'URL et la clé anon dans `config.js`.
2. **Cloudflare Pages** (compte existant) : Workers & Pages → Create → Upload assets
   → glisser `RA-QDMS-deploy.zip` → site en ligne sur `raqdms-royalair.pages.dev`.
   (Le fichier `netlify.toml` est conservé si vous préférez Netlify.)

Quand `config.js` est rempli, le badge **« Base en ligne »** apparaît en haut à droite
et les données sont partagées entre tous les utilisateurs, synchronisées à chaque action.

Phase 2 (sur demande) : Supabase Auth (comptes individuels, JWT, 2FA TOTP), stockage
des PDF/Word dans Supabase Storage, politiques RLS par rôle.
