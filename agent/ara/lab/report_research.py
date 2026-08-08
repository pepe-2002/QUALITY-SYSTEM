"""Rapport RESEARCH-BASELINE contre RESEARCH-V2."""

from __future__ import annotations

from .research_exp import ENGINES, FAUX_POSITIFS, ResearchResult


def render(result: ResearchResult) -> str:
    base = result.stats.get("baseline")
    v2 = result.stats.get("v2")

    lignes: list[str] = [
        "# RESEARCH-V2 — pertinence des sources et hygiène des requêtes",
        "",
        "## Ce que ce rapport n'est pas",
        "",
        "- Il ne révise **aucun** résultat antérieur. H1 reste non concluante,",
        "  H2 partiellement soutenue, ADAPTIVE-V2 corrige son défaut. Leurs",
        "  chiffres sont inchangés et leurs rapports conservés.",
        "- Le moteur qui a produit H1 et H2 est **gelé définitivement**. V2 vit",
        "  à côté, avec son propre identifiant.",
        "",
        f"**Baseline** : {result.baseline_version}",
        f"**Version testée** : {result.v2_version}",
        "",
        "## Les trois défauts corrigés",
        "",
        "Constatés sur une question posée au vrai web — « quel est le tarif",
        "officiel de la traversée en vedette entre la Grande Comore et",
        "Mohéli ? » — à laquelle la baseline avait répondu en citant des",
        "traversées bretonnes.",
        "",
        "| # | Défaut | Correction |",
        "|---|---|---|",
        "| 1 | requête finissant sur une préposition, complément dupliqué : « …en vedette **entre** tarif officiel » | `compose_query` nettoie les bords et n'ajoute que des mots nouveaux |",
        "| 2 | un mot générique isolé devenait un complément de requête : « …entre **grande** » | `is_orphan` écarte les compléments qui n'orientent rien |",
        "| 3 | « traversée + vedette + tarif » suffisait à retenir une page | exigence d'au moins un **terme distinctif** de la question |",
        "",
        "Aucune liste noire : ni nom de compagnie, ni nom de lieu n'apparaît",
        "dans le code. Ce sont les mécanismes qui changent, sinon le problème",
        "reviendrait au domaine suivant.",
        "",
        "## Protocole",
        "",
        "- **Jeu 4**, adversarial, jamais utilisé auparavant, sans lien avec les",
        "  jeux 1 à 3. Ses pièges ne sont pas des chiffres trompeurs mais des",
        "  pages qui *ressemblent* à la réponse : autre pays, nom voisin,",
        "  vocabulaire générique, archive périmée, même lieu autre contexte.",
        f"- **{len(result.seeds)} graines** ; formulation et ordre des résultats",
        "  varient, jamais les faits.",
        "- **Tout est identique entre les deux bras** sauf le moteur de",
        "  recherche : même contrôleur, même corpus, même synthèse.",
        "- Aucun résultat de H1 ou H2 n'a servi à calibrer cette version.",
        "",
        "## Résultats",
        "",
        "| Moteur | Exactitude | Bruit | Précision des sources | Faux positifs | Mauvais lieux | Recherches | Temps | Jetons |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for engine in ENGINES:
        s = result.stats.get(engine)
        if not s:
            continue
        lignes.append(
            f"| {s.label} | {s.accuracy:.2f} | {s.noise:.2f} | "
            f"**{s.precision:.0%}** | {s.false_positives:.2f} | "
            f"{s.wrong_place:.2f} | {s.searches:.2f} | {s.latency_ms:.0f} ms | "
            f"{s.tokens:.0f} |"
        )

    lignes += [
        "",
        "*Précision des sources* : part des pages retenues qui parlent bien du",
        "sujet. *Faux positifs* : pages hors sujet retenues, par exécution.",
        "*Mauvais lieux* : parmi elles, celles qui parlent d'un autre endroit.",
        "",
        "### Faux positifs par nature de piège",
        "",
        "| Moteur | " + " | ".join(FAUX_POSITIFS) + " |",
        "|---|" + "---|" * len(FAUX_POSITIFS),
    ]
    for engine in ENGINES:
        s = result.stats.get(engine)
        if not s:
            continue
        lignes.append(
            f"| {s.label} | "
            + " | ".join(str(s.by_trap.get(piege, 0)) for piege in FAUX_POSITIFS)
            + " |"
        )

    lignes += ["", "### Requêtes réellement émises", ""]
    for engine in ENGINES:
        requetes = result.queries.get(engine) or []
        lignes.append(f"**{ENGINE_LABEL(result, engine)}**")
        lignes.append("")
        for requete in requetes:
            lignes.append(f"- `{requete}`")
        lignes.append("")

    if base and v2:
        lignes += ["## Lecture", ""]
        ecart_precision = v2.precision - base.precision
        ecart_exactitude = v2.net - base.net
        ecart_faux = v2.false_positives - base.false_positives
        ecart_lieux = v2.wrong_place - base.wrong_place

        lignes += [
            f"- Précision des sources : {base.precision:.0%} → {v2.precision:.0%} "
            f"({ecart_precision:+.0%}).",
            f"- Faux positifs retenus par exécution : {base.false_positives:.2f} → "
            f"{v2.false_positives:.2f} ({ecart_faux:+.2f}).",
            f"- Mauvaises géolocalisations : {base.wrong_place:.2f} → "
            f"{v2.wrong_place:.2f} ({ecart_lieux:+.2f}).",
            f"- Exactitude nette : {base.net:.2f} → {v2.net:.2f} "
            f"({ecart_exactitude:+.2f}).",
            f"- Coût : {base.searches:.2f} → {v2.searches:.2f} recherches, "
            f"{base.tokens:.0f} → {v2.tokens:.0f} jetons, "
            f"{base.latency_ms:.0f} → {v2.latency_ms:.0f} ms.",
            "",
        ]

        if ecart_precision > 0 and ecart_exactitude >= -0.02:
            lignes.append(
                "Sur **ce** jeu, V2 retient moins de pages hors sujet sans perdre "
                "en exactitude. Cela ne dit rien de son comportement ailleurs : "
                "un seul corpus, écrit par l'auteur du système."
            )
        elif ecart_precision > 0:
            lignes.append(
                "V2 filtre davantage, mais l'exactitude baisse : le filtre écarte "
                "aussi des sources utiles. À examiner avant toute adoption."
            )
        elif ecart_precision < 0:
            lignes.append(
                "V2 ne filtre pas mieux que la baseline sur ce jeu. Le résultat "
                "est conservé tel quel."
            )
        else:
            lignes.append(
                "Aucune différence mesurable entre les deux moteurs sur ce jeu. "
                "Le résultat est conservé tel quel."
            )

    lignes += [
        "",
        "## Ce que cette expérience ne prouve pas",
        "",
        "- Un seul jeu, quatre tâches, un domaine. C'est assez pour montrer un",
        "  mécanisme, pas pour établir une supériorité générale.",
        "- Le jeu est écrit par l'auteur du système, comme les trois autres.",
        "- **Les noms voisins restent un point faible** : distinguer deux lieux",
        "  qui partagent un nom demanderait un référentiel géographique, que ce",
        "  système n'a pas. Le rapport ci-dessus le mesure au lieu de le taire.",
        "- Le hors-période relève de l'agent contexte, pas du filtre de",
        "  pertinence : une archive correctement identifiée reste une source",
        "  valide, c'est sa date qui doit être lue.",
        "- Rien ici ne dit ce que valent ces moteurs sur le vrai web, où les",
        "  pages ne sont pas étiquetées.",
    ]
    return "\n".join(lignes)


def ENGINE_LABEL(result: ResearchResult, engine: str) -> str:  # noqa: N802
    stats = result.stats.get(engine)
    return stats.label if stats else engine


__all__ = ["render"]
