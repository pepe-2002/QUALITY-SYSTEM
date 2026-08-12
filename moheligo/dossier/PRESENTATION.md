# 🪪 PRÉSENTATION DE MoheliGo — les versions officielles

> Demandée par le patron le 12/08/2026. **Quatre longueurs**, à choisir selon
> l'endroit. Toutes disent la même chose : c'est ça qui construit une marque.
>
> ⚠️ **Tous les faits d'ici sont vérifiés dans le code du site** (`index.html`,
> `moheli-savoir.js`). Aucun chiffre de fréquentation, aucun classement, aucune
> date de création : je ne les ai pas. **Ne jamais ajouter un chiffre à ces
> textes sans l'avoir vérifié** — voir « Ce qu'on ne dit pas » à la fin.

---

## 1. En une phrase (signature, pied de mail, carte de visite)

> **MoheliGo — la traversée Grande Comore ↔ Mohéli, réservée et payée depuis
> ton téléphone.**

---

## 2. En trois lignes (bio de page Facebook, annuaire)

> **MoheliGo, c'est la traversée entre la Grande Comore et Mohéli, prise
> d'avance depuis ton téléphone.** Tu choisis ton départ, tu paies par MVola ou
> KartaPay, et ton billet arrive avec son code — il reste dans le téléphone même
> sans réseau.
> Et chaque soir, on publie l'état de la mer du lendemain. Gratuitement.
> 🚤 moheligo.com · WhatsApp +269 479 43 28

---

## 3. Le paragraphe (à copier dans un message, un groupe WhatsApp, un post)

> **Avant, pour traverser, on descendait au port et on attendait de savoir.**
> S'il y avait une place. Si la vedette partait. Combien ça coûtait.
>
> **MoheliGo, c'est pour ne plus avoir à deviner.** Sur moheligo.com, tu vois les
> départs entre Ouroveni, Chindini, Hoani et Fomboni, avec les places qui restent
> et les prix — sans avoir à donner ton nom. Quand tu réserves, ta place est
> bloquée quinze minutes le temps de payer par MVola ou KartaPay, et ton billet
> arrive tout de suite avec son code. Il reste dans ton téléphone même sans
> réseau : c'est lui qu'on scanne à l'embarquement.
>
> Tu peux changer la date gratuitement, et annuler tant que la traversée n'est
> pas partie. Il n'y a rien à installer : ça s'ouvre comme une page.
>
> **Et chaque soir, on publie l'état de la mer du lendemain — la houle, le vent,
> heure par heure.** Gratuitement, qu'elle soit belle ou mauvaise. Parce que la
> mer, ce n'est pas nous qui la décidons ; mais te la dire avant que tu quittes
> la maison, ça, on peut.
>
> **moheligo.com** — une question ? WhatsApp **+269 479 43 28**, quelqu'un répond.

---

## 4. La demi-page (partenaires, hôtels, agences, autorités — VOUVOIEMENT)

> ### MoheliGo — réservation et billetterie des traversées maritimes des Comores
>
> MoheliGo est un service de **réservation et de billetterie en ligne** pour les
> traversées entre la **Grande Comore** et **Mohéli** : Ouroveni et Chindini au
> départ, Hoani et Fomboni à l'arrivée.
>
> **Ce que le service permet aujourd'hui**
> - Consulter librement les départs, les places restantes et les tarifs, sans
>   compte et sans application à installer.
> - Réserver et payer par **MVola** ou **KartaPay**, avec délivrance immédiate
>   d'un **billet à code**, consultable hors réseau.
> - Modifier la date sans frais sur la même liaison, et annuler avec
>   remboursement tant que la traversée n'est pas partie.
> - Tarif réduit pour les enfants.
> - Consulter **l'état de la mer sur sept jours**, avec un bulletin publié chaque
>   soir pour le lendemain (source : Open-Meteo Marine, citée sur chaque
>   publication).
>
> **Notre position, dite précisément**
> Nous ne décidons pas des départs : ils dépendent des compagnies, du commandant
> et de la mer. **Notre métier est de rendre l'information disponible avant que
> le voyageur quitte sa maison**, et de lui permettre de prendre sa place à
> l'avance. Le bulletin officiel affiché à l'embarquement fait toujours foi.
>
> **Ce que nous cherchons**
> Des **points de vente assistés** : hôteliers, agences, commerçants qui
> réservent pour leurs clients n'achetant pas en ligne. La première réservation
> se fait souvent accompagnée ; la suivante, seul, en trois minutes.
>
> **moheligo.com** — WhatsApp **+269 479 43 28**

---

## 5. 🚨 Ce qu'on ne dit pas dans une présentation MoheliGo

Écrit noir sur blanc, parce que c'est là qu'on abîme une marque :

- ❌ **« Le leader », « le n° 1 », « la référence »** — on ne l'a pas mesuré.
- ❌ **Un nombre de clients, de traversées ou d'utilisateurs.** Le jour où on
  l'aura, il viendra du journal des réservations, pas de l'enthousiasme.
- ❌ **Une durée de traversée, une fréquence, un horaire.** Non vérifiés, et un
  partenaire qui relève une erreur ne revient pas.
- ❌ **« Nous garantissons votre départ »** — la mer décide, pas nous.
- ❌ **« C'est simple »** adressé à quelqu'un qui a peur : on décrit les gestes,
  on ne juge pas sa difficulté (manuel § 5).
- ❌ **Le jargon** : plateforme, solution digitale, écosystème, disruptif.
- ✅ En revanche, on **cite toujours la source** d'un chiffre de mer, et on
  rappelle que **le bulletin officiel à l'embarquement fait foi**.

---

## Où sont les faits, si on doit les revérifier

| Fait | Source dans le dépôt |
|---|---|
| Les quatre ports | `moheligo/index.html` (sélecteurs de départ et d'arrivée) |
| Tarif adulte indicatif, prix exact affiché en direct | `moheligo/index.html` (bloc FAQ) |
| Tarif enfant réduit, place bloquée 15 min, changement de date gratuit, remboursement, fidélité | `moheligo/moheli-savoir.js` |
| Consultation libre sans compte | `moheligo/index.html` (« la connexion n'est demandée qu'au moment de réserver ») |
| Bulletin mer quotidien, source Open-Meteo | `moheligo/pub/flyers/bulletin.py` |
| Positionnement et règles d'écriture | `dossier/MANUEL-MARKETING.md` § 2 et § 4 |
