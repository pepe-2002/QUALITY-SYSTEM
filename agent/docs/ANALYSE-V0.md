# Analyse de la spécification et architecture V0

> Livrable demandé par la spec §22, points 1 à 4. Rédigé **avant** le code,
> corrigé **après** la mise au point en conditions réelles.

---

## 1. Ce que demande la spécification

La spec décrit un **agent**, pas un chatbot. La différence tient en une phrase :
l'agent décide *quoi faire* avant de répondre, utilise des outils, vérifie son
travail, et sait s'arrêter. Sept exigences structurent tout le reste :

| # | Exigence | Où elle se traduit dans le code |
|---|---|---|
| §1 | Orchestrateur qui choisit l'agent | `ara/agents/orchestrator.py` |
| §4 | Calcul proportionné à la tâche | `ara/core/complexity.py` |
| §13 | Outils indépendants | `ara/tools/` + `registry.py` |
| §15 | Confirmation humaine | `ara/core/permissions.py` |
| §16 | Aucune permission implicite | liste blanche `ARA_ALLOWED_TOOLS` |
| §17 | Journal reproductible, sans pensée privée | `ara/core/journal.py` |
| §19 | Rien de payant obligatoire | `ara/providers/` |

---

## 2. Réalisable sans le moindre coût

Tout le MVP. Vérifié, pas supposé :

| Fonction | Moyen retenu | Coût |
|---|---|---|
| Interface mobile | PWA servie par `http.server` | 0 |
| Serveur + temps réel | bibliothèque standard + SSE | 0 |
| Recherche web | DuckDuckGo (HTML public) + API Wikipédia | 0 |
| Extraction de texte | `html.parser` de la bibliothèque standard | 0 |
| Synthèse | moteur **extractif** intégré | 0 |
| Synthèse rédigée | Ollama en local | 0 (matériel de l'utilisateur) |
| PDF | ReportLab, sinon moteur de repli intégré | 0 |
| DOCX | OOXML écrit avec `zipfile` | 0 |
| MD / TXT | bibliothèque standard | 0 |
| Historique + journal | JSON / JSONL sur disque | 0 |
| Tests | pytest, corpus figé, sans réseau | 0 |

**Le choix structurant** : zéro dépendance obligatoire. Ni `requests`, ni
`fastapi`, ni `python-docx`. Motif : le prototype doit s'installer sur un
téléphone Android via Termux, où chaque paquet à compiler est un échec
probable. `pip install reportlab` reste conseillé, jamais requis.

**Le compromis assumé** : sans LLM, la synthèse est *extractive* — elle
sélectionne et cite des phrases des sources, elle n'en rédige pas. C'est
honnête et vérifiable (un test s'assure que chaque phrase rendue existe
mot pour mot dans une source), mais ce n'est pas de la rédaction. L'interface
le dit à l'utilisateur au lieu de le laisser croire le contraire.

---

## 3. Ce qui exige une ressource externe

| Fonction | Pourquoi | Traitement |
|---|---|---|
| Synthèse **rédigée** de qualité | aucun LLM gratuit distant fiable | Ollama en local (gratuit) ou clé d'API |
| Génération d'**images** par IA | pas d'équivalent gratuit et local simple | outil déclaré, refuse de s'exécuter, explique |
| Recherche à fort volume | quotas des moteurs publics | SearXNG auto-hébergé, ou clé |
| OCR, transcription audio | hors périmètre Phase 1 | non implémenté |

Règle appliquée partout : **rien ne s'active tout seul**. Un fournisseur
indisponible ne fait pas échouer la tâche — le système bascule sur le moteur
gratuit et affiche : « Cette fonction nécessite une ressource externe », suivi
de ce qui manque exactement.

---

## 4. Architecture V0

```
        TÉLÉPHONE (PWA)
              │  HTTP + Server-Sent Events
        ┌─────▼─────────────────────────────────┐
        │  api/server.py    service.py          │  tâches en arrière-plan
        └─────┬─────────────────────────────────┘  historique sur disque
              │
        ┌─────▼─────────────────────────────────┐
        │  ORCHESTRATEUR                        │
        │  planner → gather → analyse →         │
        │  document_agent → vérification        │
        └──┬────────────┬───────────┬───────────┘
           │            │           │
     ┌─────▼────┐ ┌─────▼─────┐ ┌───▼──────────┐
     │ OUTILS   │ │FOURNISSEURS│ │ SOCLE        │
     │ registre │ │ LLM        │ │ permissions  │
     │ + garde  │ │ recherche  │ │ journal      │
     │          │ │ stockage   │ │ complexité   │
     └──────────┘ └────────────┘ └──────────────┘
```

Trois principes :

1. **Un seul passage obligé pour les outils.** Aucun agent n'appelle une
   fonction d'outil directement ; tout passe par `ToolBox.call()`, qui vérifie
   la permission, demande confirmation si l'action est sensible, journalise et
   convertit toute exception en erreur maîtrisée.
2. **Les fournisseurs sont interchangeables.** Changer de LLM ou de moteur de
   recherche est une variable d'environnement, pas une modification de code.
3. **Le contexte de tâche est isolé.** Une tâche = un `TaskContext` = un
   dossier. C'est ce qui rendra le RESEARCH LAB (Phase 4) capable de rejouer
   la même tâche avec des réglages différents.

---

## 5. Ce que la mise au point réelle a corrigé

Le MVP a été lancé contre le vrai web, pas seulement contre le corpus de test.
Quatre défauts sont apparus, chacun corrigé **et** couvert par un test :

| Défaut observé | Cause | Correction |
|---|---|---|
| Requêtes du type « … et fais-moi un PDF » envoyées aux moteurs | la consigne était confondue avec le sujet | `subject()` retire verbes d'instruction et noms de livrables |
| Un article sur l'Algérie retenu comme source sur les Comores | mots communs (« entre », « grande », « pdf » du menu Wikipédia) | filtre de pertinence sur le sujet seul, seuil proportionnel |
| Même page comptée deux fois (`?lang=fr`) | dédoublonnage sur l'URL brute | `canonical()` ignore les paramètres cosmétiques |
| Réponses 429 des moteurs | requêtes enchaînées sans pause | temporisation + réessai avec retrait progressif |

C'est le point important de cette V0 : les corrections viennent de
l'observation, pas de l'intuition.

---

## 6. Limites connues de la Phase 1

À lire avant d'en attendre plus qu'elle ne donne :

- **Pas de boucle de recherche adaptative.** Les requêtes sont produites en une
  passe ; l'agent ne relance pas de recherche après analyse. → Phase 2.
- **Pas de détection de contradictions.** Les sources sont collectées et
  citées, jamais confrontées. → Phase 2.
- **Le contrôleur de complexité n'est pas validé.** C'est une heuristique
  lexicale, sans aucune preuve empirique qu'elle améliore quoi que ce soit.
  Le rôle de la Phase 4 sera d'essayer de la **réfuter**, pas de la confirmer.
- **Le filtre de pertinence est lexical.** Il écarte le hors-sujet grossier ;
  il ne détecte ni la source douteuse, ni la date périmée.
- **Aucun envoi de fichier depuis le téléphone.** « Analyse ce document »
  n'est pas encore possible.
