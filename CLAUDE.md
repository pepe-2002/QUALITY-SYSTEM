# Dépôt QUALITY-SYSTEM — briefing de session

Ce dépôt contient **deux projets distincts** :

1. **RA-QDMS** (racine) — plateforme de gestion documentaire qualité de Royal Air
   (conformité ANACM/OACI/ISO 9001, flotte LET 410). Voir `README.md`.
2. **MoheliGo** (`moheligo/`) — site de réservation des traversées maritimes des
   Comores (Grande Comore ↔ Mohéli), déployé en production sur **https://moheligo.com**.

## Rôle confié par le propriétaire (pepe-2002 / Nayam)

Claude dirige MoheliGo pour tous les postes **sauf** la direction générale et le
service client, que le patron garde (décision du 11/08/2026 ; répartition,
limites et règle de décision A / B / C au § 12.2 du manuel).

## 📁 TOUT EST DANS `moheligo/dossier/` — le lire avant de produire

À chaque session concernant MoheliGo, dans cet ordre :

1. **LIRE `moheligo/dossier/README.md`** — l'index du dossier : il dit **quoi
   lire avant quoi** selon le travail à faire, et donne l'état du système
   (ce qui publie tout seul, à quelle heure, avec quel interrupteur).
2. **LIRE `moheligo/dossier/MEMOIRE.md`** — l'état du projet et le journal de
   toutes les décisions. **Je n'ai aucun souvenir en dehors de ce fichier.**
3. **LIRE la ligne du tableau de `README.md`** qui correspond à ce que je vais
   produire (flyer, texte, rapport, plan, décision produit).
4. **METTRE À JOUR `MEMOIRE.md`** avant de pousser, à chaque avancée notable —
   et le manuel quand j'apprends quelque chose de réutilisable.
5. **COMMITTER ET POUSSER** sur la branche en cours : l'environnement de session
   est éphémère, seul GitHub survit.

⚠️ Les publications automatiques ne lisent que la branche **`main`** : un visuel
resté sur une branche de travail n'existe pas pour le robot.

## Repères rapides MoheliGo

- **Documents de référence** : `moheligo/dossier/` (mémoire, manuel, feuille de
  route, plan publicitaire, textes, modes d'emploi). Rien d'autre ne fait foi.
- Code source du site : `moheligo/` (récupéré depuis le site en production le 02/08/2026).
- Supports marketing et scripts : `moheligo/pub/` (flyers, vidéos, photos,
  robots de publication).
- Ce qui est **généré par un programme** reste à côté du programme, jamais dans
  le dossier — sinon on corrige la copie au lieu de la source.
- Le patron communique en français, style direct — répondre en français.
