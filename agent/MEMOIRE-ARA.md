# 🧠 MÉMOIRE — projet ARA (agent autonome de recherche et création)

> **À lire en début de toute session ARA, et à mettre à jour avant de pousser.**
> L'environnement de session est éphémère : seul GitHub survit.

Branche de travail : `claude/ai-autonomous-research-creative-agent-0su1cb`
Dossier : `agent/` · Version : **v0.7.0** · **603 tests** hors ligne

---

## 1. Ce qu'est le projet

Un agent — pas un chatbot — qui **cherche → comprend → planifie → utilise des
outils → crée → critique → vérifie → s'arrête**. Lancé par le propriétaire
(pepe-2002 / Nayam) le 07/08/2026 comme **projet de recherche scientifique**.

Contrainte fondatrice, qui explique presque toute l'architecture : **zéro
dépendance obligatoire**. Uniquement la bibliothèque standard, pour que ça
s'installe sur un téléphone Android sous Termux sans rien compiler. Pas de
`requests`, pas de `fastapi`, pas de `python-docx`. PDF, DOCX, QR code et
serveur HTTP sont écrits à la main.

Coût : 0 €. Moteur par défaut **extractif** (il copie des phrases sourcées, il
ne rédige pas) — et l'interface le dit à l'utilisateur.

## 2. Les cinq phases, livrées

1. **Interface** — PWA installable, pipeline en direct (SSE), documents
   PDF/DOCX/MD/TXT **vérifiés avant livraison**, historique, permissions,
   journal sans chaîne de pensée privée.
2. **Recherche adaptative** — relance ciblée quand il manque quelque chose ou
   que deux sources se contredisent ; contradictions chiffrées ; **agent
   contexte** qui tranche vraie contradiction ou écart explicable.
3. **Studio créatif** — 3 concepts de flyer, critique sur 12 critères mesurés,
   amélioration avec retour arrière, QR code en Python pur **relu** avant
   d'être posé.
4. **Laboratoire** — corpus figés, stratégies comparées, hypothèses
   pré-enregistrées.
5. **Automatisation Android** — Termux (notification, presse-papier, voix,
   partage), routines programmées, ordonnanceur.

## 3. LA MÉTHODE — c'est le cœur du projet, ne pas y déroger

Le propriétaire a imposé une discipline expérimentale stricte. **La respecter
prime sur tout le reste**, y compris sur l'envie de bien faire.

1. **Une expérience se pré-enregistre.** Hypothèse, critères de succès ET
   d'échec, métriques : écrits AVANT, dans un commit ANTÉRIEUR à celui des
   résultats. L'antériorité doit être vérifiable dans l'historique Git.
2. **Nouveau mécanisme = nouvelle version nommée.** On ne corrige jamais une
   version qui a produit des résultats publiés : on en crée une à côté et on
   fige l'ancienne. Le laboratoire **épingle** explicitement la version de
   chaque bras, ce qui garde les expériences reproductibles pendant que le
   système avance.
3. **Un jeu de test ne sert qu'une fois à juger.** Après, il devient jeu de
   développement — utile pour constater une régression, plus pour conclure.
4. **Ne jamais ajuster après avoir vu le résultat.** C'est s'entraîner sur son
   propre examen. Une correction tentée puis rejetée se **consigne** (ce
   qu'elle améliorait, ce qu'elle dégradait, pourquoi elle est écartée).
5. **Le résultat mesuré prime sur l'intuition.** Un résultat négatif se garde
   tel quel. On ne cherche pas à obtenir un résultat positif.
6. **Une limite non résolue se fige par un test** qui échouera le jour où
   quelqu'un la résout.

## 4. État des versions

| Composant | Version | Statut |
|---|---|---|
| Contrôleur de difficulté | ADAPTIVE-V1 | **gelée** — baseline de H1/H2 |
| | ADAPTIVE-V2 | **adoptée** (défaut corrigé sur jeu 3) |
| Moteur de recherche | RESEARCH-BASELINE | **gelé** — moteur de H1/H2 |
| | RESEARCH-V2 | **adopté** (jeu 4 : précision 56 % → 66 %) |
| Extracteur de faits | baseline | **gelé** |
| | EXTRACTION-V2 | **adopté** (jeu 6 : 35 % → 100 % de rappel) |
| Contrôle de contexte | CONTEXT-V2 / V3 / V4 | **mesurés, AUCUN adopté** |

`ARA_RESEARCH_ENGINE=baseline` revient au moteur gelé sans toucher au code.

## 5. Les expériences, et leurs verdicts — à ne pas réécrire

| Expérience | Verdict | Commande |
|---|---|---|
| **H1** — la recherche adaptative répond-elle mieux ? | **NON CONCLUANT** (p = 1,000) | `--lab` |
| **H2** — économise-t-elle des recherches ? | **PARTIELLEMENT SOUTENUE** (−56 %, mais exactitude non comparable) | `--h2` |
| **ADAPTIVE-V2** | DÉFAUT CORRIGÉ | `--v2` |
| **RESEARCH-V2** | 2 formes de faux positifs éliminées sur 5 | `--research` |
| **EXTRACTION-V2** | 20/20 sur jeu 6 | `--extraction` |
| **CONTEXT-V2/V3/V4** | aucune adoptable | `--context` |
| Diagnostic par étape | 69 % de réponses correctes | `--diagnostic` |

**Ces chiffres ne se retouchent pas.** Si une modification les fait bouger,
c'est un bug, pas un progrès.

## 6. Les neuf jeux de test, et leur rôle

| Jeu | Fichier | Rôle |
|---|---|---|
| 1 | `lab/dataset.py` | calibration (brûlé) |
| 2 | `lab/heldout.py` | validation H2 (brûlé) |
| 3 | `lab/heldout2.py` | test ADAPTIVE-V2 (brûlé) |
| 4 | `lab/adversarial.py` | test RESEARCH-V2 (brûlé) |
| 5 | `lab/extraction.py` | développement extraction |
| 6 | `lab/extraction_test.py` | test EXTRACTION-V2 (brûlé) |
| 7 | `lab/context_test.py` | test CONTEXT-V2 (brûlé) |
| 8 | `lab/context_test2.py` | test CONTEXT-V3 (brûlé) |
| 9 | `lab/context_test3.py` | test CONTEXT-V4 (brûlé) |

Prochaine amélioration du contexte → **CONTEXT-V5 sur un jeu 10**.

## 7. Ce que la mesure a appris, et qui contredit l'intuition

- **H1 non concluante** : l'affirmation fondatrice du projet n'est pas
  démontrée. Elle n'est pas réfutée non plus.
- **Le contrôleur adaptatif économise sans mieux répondre.**
- **La panne dominante est la RECHERCHE** (63 % des échecs), pas la
  rédaction — contre-intuitif, et mesuré.
- **Trois versions du contrôle de contexte, la plus simple est la meilleure.**
  V3 obtenait 94 % sur son jeu et bloquerait **un quart** des bonnes réponses
  en production. Sans jeux séparés, elle aurait été adoptée.
- **Un jeu écrit à la main produit des phrases plus complètes que le vrai
  web.** C'est le biais qui a trompé les jeux 7 et 8.

## 8. Où en est le déploiement

Aucune adresse publique n'existe. Trois chemins, tous documentés :

- **téléphone** : `bash deploy/termux/install.sh`, puis `--serve` ;
- **tunnel depuis un PC** (choix du propriétaire) :
  `bash deploy/tunnel/tunnel.sh` → adresse `trycloudflare.com` + jeton
  obligatoire, écoute sur `127.0.0.1` seulement ;
- réseau local : `--serve` puis `http://<ip>:8800`.

## 9. Prochaines pistes, par ordre d'intérêt mesuré

1. **La recherche** — 63 % des échecs. C'est là qu'il faut porter l'effort.
2. **Le moteur de synthèse** : le filtre de contexte ne peut que rattraper
   après coup ce que la sélection de phrases choisit mal.
3. CONTEXT-V5 sur un jeu 10, si le contexte reste le sujet.
4. Une réplication par **quelqu'un d'autre** : les neuf jeux sont écrits par
   l'auteur du système, et c'est la limite de fond de tout ce qui précède.
