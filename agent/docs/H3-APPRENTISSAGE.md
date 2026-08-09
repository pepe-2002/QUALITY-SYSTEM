# H3 — la mémoire des défauts sert-elle à quelque chose ?

**Pré-enregistrement.** Ce document est écrit et commité **avant** toute
exécution sur le JEU 10. C'est la règle du projet depuis H1 : l'ordre des
commits Git est la preuve, et il est vérifiable.

## Hypothèse

> **H3 — À qualité finale au moins égale, la mémoire des défauts réduit le
> nombre de corrections nécessaires après la première version.**

Autrement dit : un agent qui a déjà raté sait rater moins la fois suivante.
C'est la seule chose que « apprendre de ses erreurs » veut dire ici, et c'est
mesurable.

## Ce qui est comparé

Deux bras, sur les mêmes dix briefs du JEU 10.

| Bras | Mémoire |
|---|---|
| `SANS` | mémoire vide à chaque brief, rien n'est retenu |
| `AVEC` | une seule mémoire, partagée, qui se remplit brief après brief |

Le mécanisme du studio est **identique** dans les deux bras : même générateur,
même critique, mêmes corrections, même note visée, même limite d'itérations. La
seule différence est la persistance des leçons.

### Le biais d'ordre, et comment il est traité

Le bras `AVEC` dépend de l'ordre des briefs : le premier ne bénéficie d'aucune
mémoire, par construction. Un ordre favorable pourrait donc flatter le
résultat. Le bras `AVEC` est donc exécuté sur **cinq permutations** tirées avec
une graine fixe (`SEED = 20260809`), et chaque brief est mesuré par la moyenne
de ses exécutions.

Le premier brief de chaque permutation est **conservé** dans la moyenne, pas
écarté : l'écarter reviendrait à retirer le cas le plus défavorable à
l'hypothèse.

## Mesures

Par brief, dans chaque bras :

1. **corrections** — nombre de versions après la première (`len(versions) − 1`) ;
2. **note de la première version** — ce que l'agent produit *avant* toute
   correction, c'est-à-dire ce que la mémoire est censée améliorer ;
3. **note finale** — ce qui est livré ;
4. **défauts de la première version** — leurs codes ;
5. **défauts bloquants restants** à la livraison.

## Critères de décision, fixés d'avance

* **H3 SOUTENUE** si, simultanément :
  * la moyenne des corrections du bras `AVEC` est **strictement inférieure** à
    celle du bras `SANS` ;
  * cette réduction tient sur **au moins 7 briefs sur 10** (test des signes
    exact, hypothèse nulle : aucun effet ; le seuil de 7/10 correspond à
    p ≤ 0,055 pour n = 10 sans ex æquo) ;
  * la moyenne des **notes finales** du bras `AVEC` n'est pas inférieure de
    plus de **1 point** à celle du bras `SANS` (marge de non-infériorité).
* **H3 PARTIELLEMENT SOUTENUE** si les corrections baissent en moyenne mais que
  la réduction ne tient pas sur 7 briefs, ou si la note finale perd entre 1 et
  3 points.
* **H3 RÉFUTÉE** dans tous les autres cas — en particulier si la mémoire fait
  baisser la note finale de plus de 3 points, ou ne change rien.

## Ce que ce test **ne** prouvera **pas**

* Que les sites produits sont beaux. Le critique mesure du contraste, des
  cibles tactiles et des liens, pas du goût.
* Que la mémoire généralise à des défauts jamais vus. Elle applique d'avance
  des corrections dont l'effet a déjà été constaté ; rien de plus.
* Que l'effet tiendrait avec un générateur non déterministe. Ici le même brief
  produit toujours les mêmes fichiers, donc un défaut se reproduit à
  l'identique. **C'est la limite principale du résultat, quelle qu'en soit la
  valeur**, et elle doit figurer dans le rapport final.

## Limite connue avant l'exécution

Un défaut ne devient une règle préventive que si sa correction a déjà fait
monter la note (`Lesson.actionable`). Un mécanisme qui apprendrait aussi des
corrections inefficaces obtiendrait peut-être un meilleur score sur ce test —
et produirait de plus mauvais sites. Ce garde-fou est délibéré et n'est pas
retiré pour l'expérience.

---

*Rédigé le 9 août 2026, avant exécution. Le verdict est ajouté ci-dessous après
coup, sans que rien de ce qui précède ne soit modifié.*

---

# Verdict, ajouté après exécution le 9 août 2026

## **H3 SOUTENUE**

| Mesure | SANS mémoire | AVEC mémoire |
|---|---:|---:|
| corrections après la première version (moyenne par brief) | **1,30** | **0,30** |
| note de la première version (moyenne) | 85,0 | 94,5 |
| note finale (moyenne) | **97,0** | **97,0** |

* briefs en baisse : **8/10** (seuil pré-enregistré : 7) — hausses : 0, égalités : 2 ;
* test des signes exact : **p = 0,0078** ;
* note finale : identique au dixième de point, donc la marge de non-infériorité
  (1 point) est respectée sans discussion.

Les trois conditions fixées d'avance sont remplies.

## Où l'effet se produit — et où il ne se produit pas

La note **finale est rigoureusement la même** dans les deux bras. La mémoire ne
produit pas de meilleurs sites : elle produit les mêmes, **plus tôt**. Ce qui
change, c'est la première version — 85 → 94,5 — et le travail nécessaire pour
arriver au résultat, divisé par quatre.

Les deux égalités sont les deux briefs propres du jeu (`marche_couvert`,
`cabinet_infirmier`) : sans défaut à la première version, il n'y a rien à
apprendre ni à économiser. C'est le comportement attendu.

## Limites, dont une sérieuse

1. **Le générateur est déterministe.** Un même brief produit toujours les mêmes
   fichiers ; un défaut se reproduit donc à l'identique et une correction connue
   s'applique toujours. Avec un générateur variable, l'effet serait
   vraisemblablement plus faible. Cette limite était annoncée avant l'exécution
   et le résultat ne l'efface pas.
2. **Aucune généralisation.** La mémoire rejoue des corrections déjà constatées
   efficaces. Elle n'induit aucune règle nouvelle et ne transfère rien à un
   défaut jamais rencontré.
3. **Le critère « autonomie » n'a jamais été déclenché** par le JEU 10 : une
   adresse web citée dans le texte d'une section n'est pas une ressource
   chargée. Ce contrôle n'est donc vérifié que par les tests unitaires.
4. **Le goût n'est pas mesuré.** Contraste, cibles tactiles, liens, contenu
   réel — rien ne dit si un site est beau.

Le JEU 10 a jugé. Il devient un jeu de développement ; toute amélioration
ultérieure du studio web devra être évaluée sur un jeu 11 écrit d'avance.

Rapport détaillé et rejouable : `python -m ara.cli --h3`.
