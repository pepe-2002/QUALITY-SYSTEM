# Plan publicitaire MoheliGo — gagner des utilisateurs

Rédigé le 11/08/2026 par le Directeur Marketing, à la demande du patron.
Ce document est le plan de référence. Les supports existent déjà (5 vidéos,
une dizaine de flyers, le bulletin mer quotidien) : ce qui manque, ce n'est pas
du matériel, c'est **du rythme, du terrain et une mesure**.

---

## 1. Le diagnostic, en une phrase

Le problème de MoheliGo n'est pas que les gens n'aiment pas le service : c'est
que **la majorité des voyageurs ne sait pas encore qu'on existe**, et que ceux
qui savent hésitent à payer en ligne un service maritime qu'ils ont toujours
réglé en espèces au port.

Donc trois chantiers, dans cet ordre :

| Chantier | Question du voyageur | Ce qui le résout |
|---|---|---|
| **Notoriété** | « MoheliGo, c'est quoi ? » | présence quotidienne + affiches au port |
| **Confiance** | « Si je paie, j'embarque vraiment ? » | preuve : billets QR réels, témoignages, bulletin mer |
| **Friction** | « Comment je paie, moi ? » | MVola/KartaPay expliqué en 3 images, WhatsApp qui répond vite |

⚠️ **Ne jamais payer de la publicité pour envoyer des gens sur un tunnel qui
fuit.** Avant de dépenser un franc : vérifier que réserver + payer se fait en
moins de 3 minutes sur un téléphone bas de gamme en 3G.

---

## 2. Les quatre cibles, classées par valeur

1. **La diaspora payeuse** (France, Mayotte, Golfe) — la plus rentable. Elle a
   une carte bancaire, un revenu en euros, et une famille à faire voyager.
   Elle ne prend pas le bateau : **elle paie le bateau des autres.**
   Support prêt : `flyers/flyer-diaspora-facebook.png` (« Tu paies ici. Il
   embarque. »).
2. **Les habitués de la traversée** — Mohéliens installés à Grande Comore,
   commerçants, fonctionnaires en mission. Ils traversent plusieurs fois par an.
   Un client gagné = dix traversées. C'est le volume.
3. **Les familles pour les grands moments** — mariages, deuils, rentrée
   scolaire, fêtes. Voyage subi, décidé en urgence : celui qui est visible au
   moment de la panique gagne. C'est là que le référencement + WhatsApp comptent.
4. **Les touristes et la clientèle des lodges** — petit volume, gros panier,
   excellent pour l'image. Support prêt : `v5-destination.mp4`,
   `flyer-affiche-duotone-facebook.png`.

---

## 3. Notre arme, celle que personne d'autre n'a

**Le bulletin mer quotidien.** Personne aux Comores ne publie chaque soir, en
chiffres, l'état de la mer du lendemain matin sur le couloir Ouroveni–Hoani.

C'est l'atout central du plan, pour une raison de fond : **on ne s'abonne pas à
une page qui vend, on s'abonne à une page qui sert.** Le bulletin est le service
gratuit qui justifie l'abonnement ; la réservation est ce qu'on vend derrière.

Conséquence stratégique : **MoheliGo doit devenir le média de la mer entre les
deux îles.** Un voyageur qui vérifie la mer chez nous chaque soir réservera
chez nous le jour où il traverse — sans qu'on ait besoin de le convaincre.

⚠️ Le prix à payer : **c'est un engagement quotidien.** Un bulletin publié
un soir sur trois ne crée aucune habitude. Soit on tient le rythme (7 soirs sur
7), soit on annonce « du lundi au vendredi » et on s'y tient.

---

## 4. Le plan à trois étages

### Étage 1 — Organique : le rythme (coût : 0 FC)

C'est la base. Rien de payant ne fonctionne sans ça.

🚩 **CE TABLEAU A ÉTÉ REFAIT LE 08/09/2026, PARCE QU'IL MENTAIT.** Il annonçait
encore `v1-demo.mp4`, `flyer-affiche-vraie`, `flyer-promo-brillant` et
`flyer-diaspora` — **quatre supports supprimés le 02/09 au grand nettoyage**, et
des heures de publication (19h30-21h) qui ne sont plus les nôtres depuis que
midi existe. Un plan qui nomme des fichiers effacés n'est pas un plan, c'est un
souvenir.
📌 **LA SOURCE DE VÉRITÉ DU CALENDRIER EST `pub/flyers/calendrier.py`, PAS CE
DOCUMENT.** Ce tableau en est un reflet daté, à revérifier avec
`python3 calendrier.py` avant de s'en servir. Quand les deux se contredisent,
c'est le programme qui a raison — il publie, le document non.

**Semaine type au 08/09/2026** — deux rendez-vous fixes par jour :

| Jour | 12h05, le visuel | Ce qu'il raconte |
|---|---|---|
| **Tous les soirs 19h25** | **bulletin mer de demain** | la mer, fabriquée le jour même |
| Lundi | `flyer-rien-installer` — TU N'INSTALLES RIEN. | comment ça marche |
| Mardi | `flyer-quelquun-v2` — TU PARS VOIR QUELQU'UN. | la proximité |
| Mercredi | `flyer-tulasdeja` — TU L'AS DÉJÀ. | le produit ⚠️ date à regénérer |
| Jeudi | `flyer-traversee` — TU N'ES QU'À UNE TRAVERSÉE. | la proximité de l'île |
| Vendredi | `flyer-etudes` — TU PARS. TU REVIENS. | partir et revenir |
| Samedi | `flyer-revenir` — ON NE VISITE PAS MOHÉLI. ON Y REVIENT. | la destination |
| Dimanche | `flyer-chez-nous` — ON A FAIT ÇA CHEZ NOUS. | la fierté |

⚠️ **SEPT VISUELS POUR SEPT JOURS : chacun repasse tous les sept jours, à la
minute près.** C'est le vrai risque de la bibliothèque actuelle, et il grandit à
chaque tour. Deux jours vides valaient mieux qu'un visuel hors norme (décision
du 02/09) — mais l'objectif reste dix à douze visuels, pour que la répétition
cesse d'être un métronome.

Règles d'exécution :
- ⛔ **« Le lien dans le premier commentaire » N'A JAMAIS FONCTIONNÉ.** La
  permission `pages_manage_engagement` manque depuis le 11/08 : **aucun premier
  commentaire n'a jamais été publié**. La règle est bonne, le moyen n'existe pas
  — à régler au renouvellement du jeton (~10/10/2026). D'ici là, l'adresse est
  DANS le post, et c'est assumé.
- **Statut WhatsApp chaque soir** avec le bulletin : aux Comores, WhatsApp
  touche plus de monde que le fil Facebook. C'est gratuit et c'est le canal le
  plus sous-exploité qu'on ait.
- **Répondre en moins de 10 minutes** entre 12h-14h et 19h-22h. Un message sans
  réponse le soir est une réservation perdue. C'est le levier de conversion le
  moins cher de tout ce plan. ⚠️ **Et pendant la panne MVola, c'est LE canal de
  vente** : l'annonce dit d'écrire, donc quelqu'un doit répondre.
- Une seule idée par publication. Jamais deux appels à l'action.

### Étage 2 — Terrain : là où se prend vraiment la décision (coût : impression)

Aux Comores, l'affiche physique bat le ciblage publicitaire, parce qu'elle est
là **au moment exact** où la personne pense au voyage.

Cinq points de contact, par ordre d'efficacité :

1. **Les ports** — Chindini, Ouroveni, Hoani, Fomboni. Affiche A4 + QR à
   l'endroit où on attend la vedette. Celui qui attend s'ennuie : il scanne.
2. **Les boutiques et cabines** autour des embarcadères et des gares routières.
3. **Les hôtels et lodges de Mohéli** — ils veulent des clients arrivés sans
   histoires : notre service leur sert. Argumentaire : « vos clients réservent
   leur retour depuis votre réception, en trois minutes ».
4. **Les commandants et équipages** — ce sont eux qu'on croit. Un commandant qui
   dit « réserve sur MoheliGo » vaut mieux que dix publications.
5. **Les taxis et chauffeurs** de la route Moroni–Chindini.

Support prêt à imprimer : `flyer-promo-A4.png` et
`flyer-promo-brillant-A4.png` (300 dpi, QR vers moheligo.com).

**Le code partenaire, sans une ligne de code** : chaque partenaire reçoit un mot
à faire dire (« dis *lodge* sur WhatsApp »). On compte les mots reçus, on sait
qui travaille, on récompense. À mettre en place tout de suite, ça ne coûte rien.

### Étage 3 — Payant : seulement après que 1 et 2 tournent

Ordre d'allumage, du plus rentable au moins rentable :

1. **Diaspora, ciblage géographique** — France (Marseille, Dunkerque, Paris),
   Mayotte, puis Golfe. Intérêts : Comores, Mohéli, Grande Comore. Créa :
   `flyer-diaspora-facebook.png`. C'est la seule cible qui paie en euros : le
   coût par réservation y sera le meilleur.
2. **Mise en avant du bulletin** auprès des utilisateurs Facebook aux Comores :
   objectif abonnés, pas ventes. On achète l'audience une fois, elle revient
   gratuitement chaque soir.
3. **Reciblage** des visiteurs de moheligo.com qui n'ont pas fini de payer.
   Nécessite le pixel Meta sur le site — à installer, c'est du travail de site.

⚠️ **Contrainte à vérifier avant de promettre quoi que ce soit** : Meta se paie
par carte bancaire ou PayPal — **MVola ne paie pas Facebook**. Sans carte
utilisable, l'étage 3 n'existe pas et le plan tient sur les étages 1 et 2 (ce
qui reste très faisable). À trancher par le patron.

---

## 5. Budget : trois paliers, à choisir

Rappel de change : le franc comorien est arrimé à l'euro, **1 € = 492 FC**.

| Palier | Par mois | Ce qu'on fait | Ce qu'on peut espérer |
|---|---|---|---|
| **0 — Zéro franc** | 0 FC | Étage 1 complet + tournée des ports avec des impressions offertes ou faites en noir et blanc | Croissance lente mais réelle, uniquement par le rythme |
| **1 — Sérieux** | ~25 000 FC (≈ 50 €) | 50 affiches A4 couleur + 2 mises en avant par semaine sur les meilleures publications | Le socle : notoriété locale + premiers abonnés payés |
| **2 — Offensif** | ~100 000 FC (≈ 200 €) | Palier 1 + campagne diaspora continue + reciblage | Le seul palier où on peut viser un coût par réservation calculable et le baisser mois après mois |

Ma recommandation : **palier 1 pendant un mois**, en mesurant. On ne passe au
palier 2 que si le mois 1 prouve un coût par réservation acceptable. Dépenser
plus avant d'avoir mesuré, c'est acheter du bruit.

---

## 6. Ce qu'on mesure — cinq chiffres, pas trente

Relevés **chaque dimanche soir**, dans un simple tableau :

1. **Abonnés de la page** (le stock qu'on construit).
2. **Visites sur moheligo.com** (l'intérêt qu'on génère).
3. **Réservations payées** (la seule qui compte vraiment).
4. **Taux d'abandon au paiement** — combien commencent, combien finissent. Si ce
   chiffre est mauvais, **arrêter la publicité et réparer le site d'abord**.
5. **Coût par réservation** = ce qu'on a dépensé ÷ réservations payées.

Le seuil de décision : **le coût par réservation doit rester nettement sous la
marge qu'on gagne sur une traversée.** C'est le seul chiffre qui autorise à
dépenser plus le mois suivant.

---

## 7. Ce qui manque et que je ne peux pas fabriquer seul

- **La preuve sociale.** Il me faut 3 photos ou messages de vrais clients
  (billet QR anonymisé, un mot du genre « payé de Marseille, ma mère a
  embarqué »). C'est le contenu qui convertit le mieux et le seul que je ne
  peux pas inventer — inventer un témoignage, c'est mentir, et ça se retourne
  contre nous.
- **La marge par réservation.** Sans ce chiffre, impossible de dire si une
  publicité est rentable. C'est la donnée la plus importante du plan.
- **Une carte pour payer Meta**, si on veut l'étage 3.
- **Le budget d'impression** et qui fait la tournée des ports.
- **Le registre** : on tutoie ou on vouvoie ? Aujourd'hui les supports sont
  partagés, ça se voit. Ma recommandation : **tutoyer** (registre local, celui
  de Yas), sauf sur l'institutionnel et le A4 destiné aux partenaires.

---

## 8. Les 7 premiers jours, concrètement

| Jour | Action | Qui |
|---|---|---|
| J1 | Publier le film Amina (`v4`) + lien en 1er commentaire. Bulletin le soir. | moi (supports) / patron (publication) |
| J2 | Bulletin. Ouvrir le tableau des 5 chiffres, noter les valeurs de départ. | patron |
| J3 | Imprimer 20 A4. Bulletin. | patron |
| J4 | Tournée Ouroveni + Chindini : affiches, parler aux commandants. Bulletin. | patron |
| J5 | Publication diaspora (vendredi, jour de paie en Europe). Bulletin. | moi / patron |
| J6 | Demander à 3 clients un mot + une photo de billet. Bulletin. | patron |
| J7 | Relever les 5 chiffres. Décider du palier de budget. Bulletin. | patron + moi |

**Le seul engagement qui compte dans cette liste : le bulletin, tous les
soirs.** Le reste peut glisser d'un jour. Pas lui.

---

## 8 bis. 📅 LA SEMAINE DU 9 AU 15 SEPTEMBRE 2026

Demandée par le patron le 08/09 au soir.

🔴 **RÉÉCRITE UNE HEURE PLUS TARD, ET C'EST LA LEÇON DE LA SEMAINE.** Je venais
de finir ce plan quand le patron a écrit : « les liaisons sont suspendues
jusqu'à nouvel ordre ». La version d'avant décrivait une semaine de vente
normale. **Un plan écrit et rangé sans être relu au moment de servir est un plan
faux** — c'est la quatrième fois en sept jours que la faute est la même famille
(la copie qui survit à la source).

**Deux pannes en même temps, et il faut les tenir séparées :**

| | Depuis | État | Ce que ça coupe |
|---|---|---|---|
| **Les traversées** | 09/09 | 🔴 suspendues, aucune date | on ne peut pas partir |
| **Le paiement MVola** | 03/09 | 🔴 hors service | on ne peut pas payer en ligne |

📌 **CE QUI RESTE DEBOUT QUAND LES DEUX TOMBENT : LE RENDEZ-VOUS.** C'est
précisément la semaine où le bulletin du soir vaut le plus cher — il est le seul
endroit du pays où l'on dit la vérité tous les jours, y compris les jours où
l'on ne vend rien. Une page qui ne parle que quand elle vend est une page qu'on
n'ouvre plus.

### Ce qui part tout seul, sans que personne n'y touche

Quatorze publications : sept flyers à 12h05, sept bulletins à 19h25. Depuis le
08/09 les deux ont un filet de `cron` — le rendez-vous ne dépend plus d'une
seule mécanique. **C'est l'engagement, et le seul qui ne glisse pas.**

Chaque post porte maintenant **deux mentions**, ajoutées automatiquement et à
deux endroits différents du code :
- la **fermeture** (`service.avec_mention`, dans `programme.py`) — on réserve
  pour plus tard, on ne descend pas au port ;
- la **panne de paiement** (`service.a_jour`, dans `publier_fb.decouper`) — on
  prend la place à la main sur WhatsApp.

⚠️ **À surveiller à la première publication** : deux avertissements dans le même
post, c'est beaucoup. Si ça alourdit trop, la fermeture prime — c'est elle qui
empêche quelqu'un de descendre au port pour rien.

### Les rendez-vous à surveiller, jour par jour

| Quand | Quoi | Pourquoi ça compte |
|---|---|---|
| **mer. 09, midi** | regénérer la date de `flyer43` avant de publier | une date passée sur un visuel fait croire que le service est mort (norme § 7.3) — et cette semaine, il l'est à moitié |
| **chaque soir** | la houle | à **2,50 m** l'avis de mer forte remplace la pub, tout seul. 1,94 m annoncé pour le 09 : le seuil est à portée |
| **le jour où ça repart** | 1) le patron publie le visuel de reprise À LA MAIN, 2) `OUVERT = True`, 3) la vidéo Young Leader | dans cet ordre. Faire le 2 sans le 1, c'est revendre sans avoir annoncé |
| **le jour où MVola revient** | `PANNE_PAIEMENT = None` + l'annoncer sur la page | on a annoncé la panne, on doit annoncer la fin. Une panne dont on ne dit pas qu'elle est finie continue de coûter |

### Ce que je produis cette semaine, sans rien demander

1. **Trois nouveaux visuels** pour passer de 7 à 10 et casser le métronome des
   sept jours. Registres qui manquent : LE SOULAGEMENT n'est joué que deux fois,
   et la panne MVola nous donne un sujet que personne d'autre ne traite.
2. **La démonstration du matin**, refaite au standard (`MATIN = {}` depuis le
   02/09 — son ancienne version avait un titre de sept mots et une collision).
3. **Le relevé du dimanche**, dès que les chiffres arrivent.

### Ce qui dépend de toi, et qui bloque le reste

| Décision | Depuis | Ce qui est bloqué sans elle |
|---|---|---|
| **Holo passe-t-il encore par kartaPay ?** | 03/09 | une route de paiement peut-être vivante qu'on n'annonce nulle part |
| **Comment on encaisse pendant la panne** (espèces à l'embarquement ? place tenue sans paiement ? les remboursements, qui repassent par MVola) | 03/09 | l'annonce ouvre une conversation sans pouvoir la conclure |
| **Les trois chiffres** (réservations payées, visites, abandon au paiement) | 18/08 | **tout l'étage payant.** On ne dépense pas un franc avant de connaître l'abandon au paiement (§ 6) |
| **La raison de la fermeture** | 09/09 | `FERMETURE['raison']` est vide, donc l'avis ne l'explique pas. Une fermeture expliquée rassure, une muette inquiète — mais je n'invente pas une cause |
| **Publie-t-on l'avis de suspension ?** | 09/09 | `flyer-suspension-facebook.png`, comme le 12/08. Il remplace la pub du jour et prévient franchement |

📌 **CE QUE JE NE PROMETS PAS CETTE SEMAINE : des ventes.** Les traversées sont
suspendues et le paiement en ligne est à terre — juger la semaine aux
réservations n'aurait aucun sens. Elle se juge sur deux choses :

1. **le rendez-vous tenu quatorze fois sur quatorze**, y compris — surtout — les
   jours sans départ ;
2. **le nombre de gens qui écrivent sur WhatsApp.** C'est le seul chiffre de
   conversion qui existe quand ni le port ni le paiement ne fonctionnent, et
   personne ne le compte aujourd'hui.

⚖️ **ET LA VRAIE QUESTION DE LA SEMAINE, QUI N'EST PAS PUBLICITAIRE.** Trois
fermetures en un mois (12→18/08, 26/08→01/09, 09/09→?) : sur trente jours, le
service a été fermé plus d'un tiers du temps. **Ce n'est plus un accident de
saison, c'est le produit.** Vendre « réserve ta traversée » à quelqu'un qui a vu
trois suspensions en un mois, c'est vendre contre son expérience. Il y a
probablement autre chose à vendre — savoir AVANT de descendre au port, changer
sa date gratuitement — mais c'est une décision de produit, donc la tienne
(§ 12.2 ter). À poser quand la mer sera retombée, pas dans l'urgence.

---

## 9. Ce que je ferai, moi, sans rien demander

- Régénérer et publier le bulletin chaque jour sur la page de livraison.
- Écrire les textes de chaque publication du calendrier, prêts à copier.
- Produire les visuels manquants (preuve sociale, « comment payer en
  3 images », bannière de page Facebook).
- Tenir le tableau des 5 chiffres dès que le patron me donne les relevés.
- Mettre ce plan à jour dans `MEMOIRE.md` à chaque décision prise.
