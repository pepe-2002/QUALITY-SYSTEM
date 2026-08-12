# 📁 LE DOSSIER MoheliGo — à consulter AVANT de produire

> **Commande du patron, 11/08/2026** : « écris tout dans un dossier comme le
> manuel que tu vas consulter. »
>
> **Consigne pour moi-même (Claude, directeur de MoheliGo)** : tout ce qui
> gouverne mon travail est ici. Un document rangé ailleurs est un document qu'on
> ne lit pas — et un document qu'on ne lit pas ne sert à rien.

---

## ⚡ La règle, en trois lignes

1. **Début de session MoheliGo** → lire `MEMOIRE.md`. C'est l'état du projet et
   tout ce qui a été décidé. **Je n'ai aucun souvenir en dehors de ce fichier.**
2. **Avant de produire quoi que ce soit** → lire la ligne correspondante du
   tableau ci-dessous.
3. **Avant de pousser** → mettre `MEMOIRE.md` à jour. Ce qui n'est pas écrit est
   perdu à la fin de la session.

---

## 🎯 Quoi lire avant quoi

| Ce que je vais faire | Ce que je lis d'abord |
|---|---|
| **Un flyer, un visuel** | `MANUEL-MARKETING.md` § 1-4 (marque, positionnement, écriture), **§ 10 bis et 10 ter** (pourquoi mes visuels faisaient débutant, et pourquoi sobre ≠ vide), § 10 checklist « avant de publier un FLYER » |
| **Un texte de publication** | `MANUEL-MARKETING.md` § 4 (écrire), **§ 5 (vendre à qui n'a jamais acheté en ligne)**, § 10 checklist « TEXTE » ; `TEXTES-PUBLICATIONS.md` pour ne pas me répéter |
| **Un rapport** | `MANUEL-MARKETING.md` § 8 (mesurer : cinq chiffres et un seuil) et § 10 checklist « RAPPORT » ; `FEUILLE-DE-ROUTE.md` pour savoir à quelle étape on est |
| **Un plan, une campagne** | `PLAN-PUBLICITAIRE.md` (les trois paliers et leurs seuils) ; `FEUILLE-DE-ROUTE.md` ; § 16 checklist de décision |
| **Une décision produit ou d'organisation** | `MANUEL-MARKETING.md` **§ 12 à 13** (les postes, l'adoption) et **§ 16** (checklist) ; la **règle A / B / C** au § 12.2 ter |
| **Toucher à la publication Facebook** | `LIER-FACEBOOK.md` (la recette qui marche et les six pièges déjà payés) |
| **La vidéo de démonstration** | `VIDEO-DEMONSTRATION.md` (ce qui manque, et ce que j'en ferai) |
| **Regénérer un visuel, comprendre un script** | `ATELIER-FLYERS.md` |

⚠️ **En cas de doute entre « je décide » et « je demande au patron » : je
demande.** (Manuel § 12.2 ter — la règle A / B / C.)

---

## 📚 Les documents du dossier

| Fichier | Ce que c'est | Qui l'écrit |
|---|---|---|
| **`MEMOIRE.md`** | 🧠 l'état du projet, l'index des fichiers, et le **journal de toutes les décisions**. Le plus important : sans lui je repars de zéro | moi, à chaque avancée |
| **`MANUEL-MARKETING.md`** | 📕 **la grille de décision.** Partie I : marketing, écriture, vente. Partie II : diriger, les postes, faire adopter un produit, les erreurs des fondateurs de la Silicon Valley. Finit par des checklists | moi, quand j'apprends quelque chose |
| **`FEUILLE-DE-ROUTE.md`** | 🗺️ « dans combien de temps ça va se faire ? » — quatre étapes, **chacune avec son seuil de décision** | moi, révisé avec les chiffres |
| **`PLAN-PUBLICITAIRE.md`** | 📣 la stratégie : les étages organiques, les trois paliers de budget, les seuils d'arrêt | moi |
| **`TEXTES-PUBLICATIONS.md`** | ✍️ la bibliothèque des textes déjà écrits, par angle | moi |
| **`LIER-FACEBOOK.md`** | 🔗 la recette de la liaison Facebook **qui marche**, et les six pièges déjà payés en heures perdues | moi, après chaque incident |
| **`VIDEO-DEMONSTRATION.md`** | 🎬 pourquoi la vidéo n'existe pas encore, et les **4 captures d'écran** qu'il me faut | moi |
| **`ATELIER-FLYERS.md`** | 🛠️ le mode d'emploi technique : quel script fabrique quoi, comment regénérer | moi |

---

## 📌 Ce qui n'est PAS dans le dossier, et pourquoi

Tout ce qui est **fabriqué par un programme** reste à côté du programme : sinon
on finit par corriger la copie au lieu de la source, et les deux se contredisent.

| Fichier | Où | Pourquoi pas ici |
|---|---|---|
| `pub/RAPPORT.md` | à côté de `rapport.py` | **généré** chaque semaine — le corriger à la main n'aurait aucun sens |
| `pub/flyers/journal-publications.json` | à côté de `publier_fb.py` | écrit par le robot à chaque publication |
| `pub/flyers/bulletin.json` | idem | les chiffres de mer du jour |
| `pub/photos-cc/CREDITS.md` | avec les photos | l'attribution doit rester collée aux fichiers qu'elle couvre |
| `pub/demo/ecrans/` | avec le script de capture | c'est là que le patron dépose ses captures |

**Les pages lisibles pour le patron sont générées, jamais recopiées :**

```
cd moheligo/pub/flyers
python3 manuel_page.py --sortie /tmp/manuel.html          # le manuel
python3 manuel_page.py --dossier --sortie /tmp/dossier.html   # TOUT le dossier
python3 page.py --sortie /tmp/flyers.html                 # les flyers et leurs textes
```

---

## 🚦 L'état du système, en un coup d'œil

Ce tableau est le seul endroit à jour sur ce qui tourne tout seul. **Vérifier
qu'il est encore vrai avant de l'annoncer au patron.**

| Quoi | Quand | Interrupteur | État |
|---|---|---|---|
| **Bulletin mer** (daté, fabriqué le jour même) | tous les soirs 19h30 | `PUBLIER_FB` | ✅ armé |
| **Publication du jour** (calendrier de la semaine) | tous les jours 12h30 | `PUBLIER_FB` | ✅ armé — **les 7 jours sont couverts par des visuels du système** |
| **Démonstration du matin** | lundi et jeudi 7h30 | `PUBLIER_MATIN` | ⏸️ **désarmé**, attend la décision du patron |
| **Avis de mer forte** (remplace la pub) | automatique, houle ≥ 2,50 m | — | ✅ actif |
| **Frein d'urgence** | à tout moment | `PAUSE_FB = oui` | 🛑 arrête tout |

⚠️ **Le robot ne voit que la branche `main`.** Un visuel commité seulement sur une
branche de travail n'existe pas pour les publications automatiques.

⚠️ **Le jeton Facebook expire vers le 10/10/2026.** À renouveler avant, sinon les
publications s'arrêtent en silence.
