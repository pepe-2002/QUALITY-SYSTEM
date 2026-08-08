"""Rapport EXTRACTION-V2, en quatre parties nettement séparées.

L'ordre est imposé par le propriétaire du projet, et il est bon : les
résultats historiques d'abord — pour qu'on voie qu'ils n'ont pas bougé — la
nouveauté ensuite, la nouvelle métrique après, les limites en dernier.
"""

from __future__ import annotations

from .extraction import compare_versions as compare_dev
from .extraction_test import CASES, compare as compare_test


def render() -> str:
    dev = compare_dev()
    test = compare_test()
    base, v2 = test["baseline"], test["v2"]

    lignes: list[str] = [
        "# EXTRACTION-V2 — devises identifiées, ou déclarées inconnues",
        "",
        "## 1. Résultats historiques — inchangés",
        "",
        "Aucun des résultats déjà publiés n'est modifié par ce travail. Les",
        "expériences épinglent explicitement l'extracteur qui les a produites,",
        "et redonnent les mêmes chiffres :",
        "",
        "| Expérience | Verdict | Statut |",
        "|---|---|---|",
        "| **H1** — recherche adaptative | RÉSULTAT NON CONCLUANT | inchangé |",
        "| **H2** — économie de recherches | PARTIELLEMENT SOUTENUE | inchangé |",
        "| **ADAPTIVE-V1** | baseline gelée | inchangée |",
        "| **ADAPTIVE-V2** | DÉFAUT CORRIGÉ (jeu 3) | inchangé |",
        "| **RESEARCH-BASELINE** | moteur gelé de H1/H2 | inchangé |",
        "| **RESEARCH-V2** | 56 % → 66 % de précision (jeu 4) | inchangé |",
        "",
        "Les quatre jeux déjà utilisés ne sont pas touchés non plus. La version",
        "corrigée de l'extracteur ne s'applique qu'à l'application et aux",
        "expériences **nouvelles**.",
        "",
        "## 2. EXTRACTION-V2",
        "",
        "### Le défaut",
        "",
        "Un montant écrit « 3 200 francs » n'était pas vu du tout. Le diagnostic",
        "l'avait chiffré : dix pannes d'extraction sur dix venaient de là.",
        "",
        "### Ce qui n'a pas été fait",
        "",
        "Décréter que « francs » vaut la devise du projet. Un agent qui",
        "comparerait des francs comoriens à des francs CFA produirait des",
        "contradictions imaginaires et des réponses fausses avec l'aplomb de la",
        "certitude. **La devise n'est jamais supposée.**",
        "",
        "### Trois niveaux de confiance",
        "",
        "| Niveau | Quand | Exemple |",
        "|---|---|---|",
        "| `certaine` | la devise est écrite | « 15 000 francs comoriens » |",
        "| `probable` | le contexte ne laisse qu'une possibilité | « À Dakar, 25 000 francs » |",
        "| `inconnue` | rien ne permet de trancher | « Prix : 900 francs » |",
        "",
        "Règle de sécurité : dans le doute, **le montant est conservé et la",
        "devise marquée `UNKNOWN`**. Jamais l'inverse.",
        "",
        "L'ordre de résolution va du plus sûr au plus fragile : devise écrite",
        "dans la phrase, puis devise unique du document, puis contexte",
        "géographique. Une marque de conversion (« soit », « contre », « ≈ »)",
        "annule la déduction : la devise écrite appartient alors à l'autre",
        "montant.",
        "",
        f"### Jeu 6 — indépendant, {len(CASES)} cas, jamais utilisé auparavant",
        "",
        "Autre univers lexical, six familles : devise écrite, devise déduite,",
        "devise indéterminée, conversions, plusieurs devises dans un document,",
        "et pièges (nombres qui ne sont pas des montants).",
        "",
        "| Mesure | RESEARCH-BASELINE | EXTRACTION-V2 |",
        "|---|---|---|",
        f"| Montants correctement extraits | {base.amounts_found}/{base.amounts_expected} "
        f"({base.amount_recall:.0%}) | **{v2.amounts_found}/{v2.amounts_expected}** "
        f"({v2.amount_recall:.0%}) |",
        f"| Devises correctement identifiées | {base.currencies_correct} "
        f"({base.currency_accuracy:.0%}) | **{v2.currencies_correct}** "
        f"({v2.currency_accuracy:.0%}) |",
        f"| Fausses identifications | {base.currencies_wrong} | "
        f"**{v2.currencies_wrong}** |",
        f"| Montants ignorés à tort | {base.amounts_expected - base.amounts_found} | "
        f"**{v2.amounts_expected - v2.amounts_found}** |",
        f"| Confiance correcte | {base.confidence_accuracy:.0%} | "
        f"**{v2.confidence_accuracy:.0%}** |",
        f"| Faux positifs | {base.false_positives} | **{v2.false_positives}** |",
        "",
        f"Sur le jeu 5 (développement) : rappel {dev['baseline'].recall:.0%} → "
        f"{dev['v2'].recall:.0%}, faux positifs "
        f"{dev['baseline'].false_positives} → {dev['v2'].false_positives}, "
        f"doubles comptages {dev['baseline'].duplicates} → {dev['v2'].duplicates}.",
        "",
        "**Ce que ces chiffres ne disent pas.** Le jeu 6 est écrit par l'auteur",
        "du système, dans la même session que le mécanisme qu'il évalue. Un",
        "score parfait y mesure surtout la cohérence entre ce qui a été pensé et",
        "ce qui a été codé — pas la robustesse face à des textes qu'on n'a pas",
        "imaginés.",
        "",
        "### Effet mesuré sur le système entier",
        "",
        "Le diagnostic, rejoué avec la correction :",
        "",
        "| | avant | après |",
        "|---|---|---|",
        "| Réponses correctes (160 exécutions) | 103 (64 %) | **110 (69 %)** |",
        "| Pannes d'EXTRACTION | 10 | **0** |",
        "| Pannes de CONTEXTUALISATION | 11 | **16** |",
        "",
        "Le gain est réel — sept réponses correctes de plus — mais il n'est pas",
        "gratuit, et il faut le dire : **cinq pannes se sont déplacées vers",
        "l'aval**. Des montants jusque-là invisibles sont désormais lus, et",
        "certains sont précisément les valeurs pièges du jeu 4 — celles d'un",
        "autre pays ou d'une archive. L'extracteur voyait moins ; il se",
        "trompait moins souvent aussi. La correction déplace une partie du",
        "problème vers l'agent contexte, qui devra suivre.",
        "",
        "## 3. FINAL_ANSWER_ACCURACY — la nouvelle métrique",
        "",
        "La métrique historique note la réponse **entière**, bilan d'analyse",
        "compris. Une valeur enfouie dans les traces y compte donc comme une",
        "réponse, alors que personne ne l'a lue. C'est ce que le diagnostic",
        "avait signalé.",
        "",
        "`FINAL_ANSWER_ACCURACY` ne regarde que ce qui est **présenté** :",
        "tout ce qui suit un marqueur de trace (« Déroulé de la recherche »,",
        "« Sources », « Informations manquantes »…) est retiré avant notation.",
        "",
        "Elle attrape trois pannes que l'ancienne laissait passer :",
        "",
        "| Panne | Ce qu'elle signale |",
        "|---|---|",
        "| information cachée | la valeur n'est que dans les traces → `hidden` |",
        "| silence coupable | « je n'ai pas trouvé » alors que la valeur était connue → `silent_success` |",
        "| erreur assurée | une valeur fausse affichée, la bonne dans les logs → `confidently_wrong` |",
        "",
        "**Elle ne réécrit rien.** H1 et H2 gardent leur métrique ; un test",
        "vérifie que les deux donnent des résultats différents sur le même cas,",
        "ce qui échouerait si quelqu'un « harmonisait » les deux.",
        "",
        "Elle s'appliquera aux expériences à venir, pas aux anciennes.",
        "",
        "## 4. Limites restantes",
        "",
        "- **Les indices géographiques sont une courte liste.** Un pays absent",
        "  ne lève aucune ambiguïté — le montant reste `UNKNOWN`, ce qui est le",
        "  comportement voulu, mais la couverture est faible.",
        "- **Une zone à devise partagée reste indécidable** : « francs CFA »",
        "  recouvre XOF et XAF ; sans pays nommé, on ne tranche pas.",
        "- **Un pays ayant changé de devise** ferait mentir la table. Elle ne",
        "  contient que des zones stables, et ce choix devra être revu.",
        "- **La confiance n'est pas une probabilité** : trois niveaux ordonnés,",
        "  pas un calcul. Rien ne dit qu'un « probable » se vérifie neuf fois",
        "  sur dix.",
        "- **Les noms de lieux voisins** et les **sources hors période**",
        "  résistent toujours (voir le rapport RESEARCH-V2) : ce travail-ci n'y",
        "  change rien.",
        "- **Le jeu 6 est écrit par l'auteur du système**, comme les cinq autres.",
        "  Une réplication par un tiers reste le seul vrai contrôle.",
    ]
    return "\n".join(lignes)


__all__ = ["render"]
