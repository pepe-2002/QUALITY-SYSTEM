"""Web figé du laboratoire — le banc d'essai (spec §18).

Mesurer une stratégie de recherche contre le vrai Internet ne veut rien dire :
les résultats changent d'un jour à l'autre, et deux stratégies ne voient jamais
le même web. Le laboratoire rejoue donc un **corpus figé**, identique pour
toutes les stratégies et pour toutes les exécutions.

Le corpus est conçu pour **discriminer**, pas pour flatter :

* des questions auxquelles la première recherche répond (là, chercher plus est
  du gaspillage — la stratégie adaptative doit s'arrêter, sinon elle perd) ;
* des questions dont la réponse n'arrive qu'à la deuxième requête, ciblée
  (là, la stratégie fixe doit échouer) ;
* des **pièges** : des questions où chercher davantage ramène du bruit, une
  contradiction artificielle ou une source périmée. Ils sont là exprès. Un banc
  d'essai sans piège ne prouve rien.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field


def _norm(text: str) -> set[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return {
        w[:-1] if len(w) > 4 and w.endswith("s") else w
        for w in re.findall(r"[a-z0-9]{3,}", text)
    }


def page(title: str, *paragraphes: str) -> str:
    corps = "".join(f"<p>{p}</p>" for p in paragraphes)
    return f"<html><head><title>{title}</title></head><body>{corps}</body></html>"


# --- Les pages ----------------------------------------------------------------

PAGES: dict[str, str] = {
    # -- traversées : réponse dès la première recherche -----------------------
    "https://compagnie-a.test/tarifs": page(
        "Tarifs des traversées inter-îles",
        "Le billet adulte de la traversée entre Ouroveni et Hoani coûte "
        "15 000 francs comoriens.",
        "La traversée dure environ 3 heures selon l'état de la mer.",
    ),
    "https://compagnie-b.test/billets": page(
        "Billets vedettes rapides",
        "Le billet adulte de la traversée entre Ouroveni et Hoani coûte "
        "15 000 francs comoriens, bagages inclus.",
        "Comptez 3 heures de traversée entre les deux ports.",
    ),
    # -- horaires : la réponse n'est QUE sur la page officielle ---------------
    "https://blog-voyage.test/comores": page(
        "Voyager aux Comores",
        "Les vedettes relient les îles plusieurs fois par semaine, mais les "
        "horaires varient beaucoup selon la saison et la météo marine.",
        "Mieux vaut se renseigner auprès de la compagnie avant de partir.",
    ),
    "https://forum-voyageurs.test/comores": page(
        "Forum : partir à Mohéli",
        "Personne ne semble connaître l'horaire exact, cela change tout le temps.",
        "Un membre indique que le bateau part le matin, sans plus de précision.",
    ),
    "https://autorite-maritime.test/horaires": page(
        "Autorité maritime — horaires officiels",
        "Le départ officiel d'Ouroveni vers Hoani est fixé à 7 heures du matin.",
        "L'embarquement débute 1 heure avant le départ.",
    ),
    # -- distance : deux sources concordantes ---------------------------------
    "https://geo-comores.test/canal": page(
        "Le canal de Mohéli",
        "La distance maritime entre la Grande Comore et Mohéli est de 70 kilomètres.",
    ),
    "https://encyclopedie.test/comores": page(
        "Archipel des Comores",
        "Mohéli est séparée de la Grande Comore par un bras de mer de 70 kilomètres.",
    ),
    # -- bagages : une seule source, jamais confirmée -------------------------
    "https://compagnie-a.test/bagages": page(
        "Bagages à bord",
        "La franchise bagages est fixée à 20 kilogrammes par passager.",
    ),
    # -- PIÈGE : une source périmée contredit la source à jour ----------------
    "https://archive-tarifs.test/2019": page(
        "Tarifs 2019 — archive",
        "En 2019, le billet adulte de la traversée entre Ouroveni et Hoani "
        "coûtait 9 000 francs comoriens.",
    ),
    # -- PIÈGE : page bavarde, chiffres sans rapport --------------------------
    "https://magazine.test/budget-comores": page(
        "Budget d'un voyage aux Comores",
        "Comptez 45 000 francs comoriens pour une nuit d'hôtel en bord de mer.",
        "Un repas au restaurant du port revient à 6 000 francs comoriens.",
        "Le taxi-brousse coûte 1 500 francs comoriens la course.",
    ),
    # -- PIÈGE : contradiction franche mais hors sujet ------------------------
    "https://autre-ile.test/anjouan": page(
        "Traversées vers Anjouan",
        "Le billet adulte de la traversée vers Anjouan coûte 25 000 francs comoriens.",
    ),
}


#: requête → pages retournées, dans l'ordre.
#: Les clés sont comparées par recouvrement de mots : c'est ce que fait un
#: vrai moteur, en beaucoup plus grossier.
INDEX: dict[str, list[str]] = {
    "tarif traversée Ouroveni Hoani": [
        "https://compagnie-a.test/tarifs",
        "https://compagnie-b.test/billets",
        "https://magazine.test/budget-comores",
    ],
    "prix billet traversée officiel": [
        "https://compagnie-a.test/tarifs",
        "https://archive-tarifs.test/2019",
        "https://autre-ile.test/anjouan",
    ],
    "horaire départ Ouroveni Hoani": [
        "https://blog-voyage.test/comores",
        "https://forum-voyageurs.test/comores",
    ],
    "horaire officiel autorité maritime": [
        "https://autorite-maritime.test/horaires",
        "https://blog-voyage.test/comores",
    ],
    "distance Grande Comore Mohéli": [
        "https://geo-comores.test/canal",
        "https://encyclopedie.test/comores",
    ],
    "durée traversée vedette": [
        "https://compagnie-a.test/tarifs",
        "https://compagnie-b.test/billets",
    ],
    "franchise bagages passager": [
        "https://compagnie-a.test/bagages",
    ],
    "bagages officiel confirmation": [
        "https://compagnie-a.test/bagages",
        "https://magazine.test/budget-comores",
    ],
    "budget voyage Comores hôtel repas": [
        "https://magazine.test/budget-comores",
    ],
}


@dataclass
class Corpus:
    """Le web figé, interrogeable comme un moteur."""

    pages: dict[str, str] = field(default_factory=lambda: dict(PAGES))
    index: dict[str, list[str]] = field(default_factory=lambda: dict(INDEX))

    def search(self, query: str, limit: int = 6) -> list[str]:
        """Retourne des URL, appariées par recouvrement de mots.

        Le seuil est volontairement bas : un vrai moteur ramène souvent des
        pages à peu près pertinentes. C'est justement ce bruit que les
        stratégies doivent savoir écarter.
        """
        asked = _norm(query)
        if not asked:
            return []
        scored: list[tuple[float, str]] = []
        for key, urls in self.index.items():
            keyed = _norm(key)
            if not keyed:
                continue
            score = len(keyed & asked) / len(keyed)
            if score >= 0.34:
                scored.append((score, key))
        scored.sort(reverse=True)

        out: list[str] = []
        for _score, key in scored:
            for url in self.index[key]:
                if url not in out:
                    out.append(url)
        return out[:limit]

    def fetch(self, url: str) -> str | None:
        return self.pages.get(url)
