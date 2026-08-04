# RA-TMS — Gestion et suivi des formations · Royal Air

Module **Formation & Compétences** de la plateforme qualité Royal Air.
Programmation des sessions, suivi des échéances réglementaires et matrice de
conformité (référentiel **ANACM · OACI · ISO 9001:2015**).

Application web autonome : un seul fichier `index.html`, aucune dépendance,
données enregistrées dans le navigateur. Ouvre le fichier, ça marche.

## Ce que fait le module

### Tableau de bord
Taux de conformité global, nombre de qualifications **expirées** (interdiction
d'exercice), échéances **sous 60 jours**, formations **jamais réalisées**, les
priorités immédiates triées de la plus urgente à la moins urgente, les
prochaines sessions programmées et la conformité **par service**.

### Échéances
La liste complète de tout ce qui est à renouveler, filtrable par statut, par
service et par recherche de nom. **Export CSV** pour l'audit ou la direction.

### Programmation
Créer une session : formation, date, heure, formateur/examinateur, lieu,
observations, et sélection des participants — seuls les agents **concernés par
la formation** sont proposés, avec leur statut affiché en face pour savoir qui
convoquer en priorité.

Quand la session a eu lieu, on **enregistre la réalisation** en cochant les
présents : la nouvelle échéance de chacun est calculée automatiquement
(date de réalisation + périodicité réglementaire). La **feuille de présence**
avec cases d'émargement s'imprime en un clic.

### Matrice de conformité
Le tableau croisé agents × formations que demande tout auditeur : vert =
valide (échéance affichée en mm/aa), orange = sous 60 jours, rouge = expiré,
gris = jamais réalisé, point = formation non applicable à la fonction.
Imprimable.

### Personnel
Fiche de chaque agent (matricule, fonction, service, date d'entrée), taux de
conformité individuel, **dossier de formation complet** et génération de
l'**attestation de formation** officielle imprimable.

### Catalogue
Les 20 matières réglementaires avec périodicité, durée, référence
réglementaire et fonctions concernées, plus le nombre d'agents à jour pour
chacune.

## Référentiel intégré

| Code | Formation | Périodicité | Référence |
|---|---|---|---|
| CRM | Gestion des ressources de l'équipage | 12 mois | OACI Annexe 6 · RAC-OPS 1.943 |
| SGS | Système de gestion de la sécurité | 24 mois | OACI Annexe 19 |
| DGR | Marchandises dangereuses | 24 mois | OACI Doc 9284 · IATA DGR |
| AVSEC | Sûreté de l'aviation civile | 24 mois | OACI Annexe 17 |
| FH | Facteurs humains | 24 mois | OACI Doc 9683 · Part-145 |
| SEP | Sécurité-sauvetage | 12 mois | RAC-OPS 1.1015 |
| SECOURS | Premiers secours | 36 mois | RAC-OPS 1.1005 |
| FEU | Lutte contre l'incendie (feu réel) | 36 mois | RAC-OPS 1.1015 (d) |
| EVAC | Évacuation d'urgence et amerrissage | 36 mois | RAC-OPS 1.1015 (e) |
| PC | Contrôle hors ligne | 6 mois | RAC-OPS 1.965 |
| LC | Contrôle en ligne | 12 mois | RAC-OPS 1.965 (c) |
| L410 | Qualification de type LET L-410 UVP-E20 | 12 mois | OACI Annexe 1 · RAC-FCL |
| SIM | Entraînement périodique sur simulateur | 6 mois | RAC-OPS 1.965 (b) |
| MB | Chargement et centrage | 24 mois | RAC-OPS 1 Subpart J |
| FUEL | Politique carburant | 24 mois | RAC-OPS 1.255 |
| RT | Radiotéléphonie et phraséologie | 24 mois | OACI Annexe 10 Vol. II |
| FOD | Prévention FOD et conduite sur aire | 12 mois | OACI Annexe 14 |
| EWIS | EWIS et sécurité des réservoirs | 24 mois | Part-145 · AMC 20-21/22 |
| AUDIT | Audit interne ISO 9001:2015 | 36 mois | ISO 19011 · ISO 9001 |
| GH | Assistance en escale | 24 mois | IATA AHM · OACI Annexe 6 |

Chaque formation ne s'applique qu'aux fonctions concernées (PNT, PNC,
maintenance, exploitation, piste, sûreté, qualité) — la matrice le gère
automatiquement.

## Lancer

```
python3 -m http.server 8457 --directory formation
```
Puis ouvrir http://localhost:8457 — ou simplement double-cliquer sur
`index.html`.

Le module s'ouvre avec un **jeu de démonstration** de 18 agents et 4 sessions,
volontairement imparfait pour montrer l'intérêt de l'outil. Le bouton
« Réinitialiser les données » le remet à zéro. Pour partir de ta vraie
équipe : supprime les agents de démonstration et ajoute les tiens.
