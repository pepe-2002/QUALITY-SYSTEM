"""Agent contexte : « est-ce une vraie contradiction ? » (2ᵉ étage de détection).

Le détecteur déterministe est réglé pour le rappel : il propose. L'agent
contexte dispose : il rejette ce qui s'explique, confirme ce qui ne s'explique
pas, et laisse « à vérifier » ce qu'il ne sait pas trancher.
"""

from __future__ import annotations

from ara.analysis.compare import find_contradictions
from ara.analysis.facts import extract_facts
from ara.analysis.validate import (
    CONFIRMED,
    REJECTED,
    UNCERTAIN,
    ContradictionValidator,
    rule_verdict,
)
from ara.providers.llm.base import LLMResult
from ara.providers.llm.offline import OfflineLLM


def _anomalies(*textes: str):
    facts = []
    for index, texte in enumerate(textes, start=1):
        facts.extend(extract_facts(texte, index))
    return find_contradictions(facts)


# --- Rejets par règles --------------------------------------------------------


def test_deux_epoques_differentes_ne_sont_pas_une_contradiction():
    """Le cas de la tour Eiffel : 312 m à l'origine, 330 m aujourd'hui."""
    anomalies = _anomalies(
        "La hauteur de la tour est de 312 mètres à l'origine, lors de sa construction.",
        "La hauteur de la tour est aujourd'hui de 500 mètres, antenne comprise.",
    )
    assert anomalies, "le détecteur déterministe doit bien la proposer"

    verdict = rule_verdict(anomalies[0])
    assert verdict is not None and verdict.status == REJECTED
    assert "époque" in verdict.reason


def test_deux_annees_differentes_expliquent_lecart():
    anomalies = _anomalies(
        "Le tarif de la traversée en 2019 était de 15 000 francs comoriens.",
        "Le tarif de la traversée en 2026 est de 45 000 francs comoriens.",
    )
    verdict = rule_verdict(anomalies[0])
    assert verdict is not None and verdict.status == REJECTED
    assert "années différentes" in verdict.reason


def test_deux_variantes_differentes_expliquent_lecart():
    anomalies = _anomalies(
        "Le billet de la traversée en classe adulte coûte 15 000 francs comoriens.",
        "Le billet de la traversée en classe enfant coûte 45 000 francs comoriens.",
    )
    verdict = rule_verdict(anomalies[0])
    assert verdict is not None and verdict.status == REJECTED
    assert "variantes" in verdict.reason


def test_un_chiffre_approximatif_nest_pas_un_dementi():
    anomalies = _anomalies(
        "La traversée du canal dure environ 180 minutes.",
        "La traversée du canal dure 45 minutes.",
    )
    verdict = rule_verdict(anomalies[0])
    assert verdict is not None and verdict.status == REJECTED


# --- Ce qui reste une vraie contradiction -------------------------------------


def test_un_vrai_desaccord_nest_pas_rejete():
    """Même objet, même époque, mêmes conditions : les règles ne l'expliquent pas."""
    anomalies = _anomalies(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 45 000 francs comoriens.",
    )
    assert rule_verdict(anomalies[0]) is None


def test_sans_explication_le_moteur_hors_ligne_marque_a_verifier():
    """Le moteur extractif ne juge pas : il s'abstient, il n'invente pas."""
    anomalies = _anomalies(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 45 000 francs comoriens.",
    )
    validator = ContradictionValidator(OfflineLLM(), question="Combien coûte la traversée ?")
    retenues = validator.validate(anomalies)

    assert len(retenues) == 1
    assert retenues[0].verdict.status == UNCERTAIN
    assert retenues[0].verdict.decided_by == "defaut"
    assert "à vérifier" in retenues[0].describe()


# --- Jugement du LLM ----------------------------------------------------------


class _LLMJuge(OfflineLLM):
    """Faux modèle non dégradé, pour éprouver l'étage de jugement."""

    degraded = False

    def __init__(self, verdict: str, raison: str = "les deux mesurent la même chose"):
        self.verdict = verdict
        self.raison = raison
        self.appels: list[str] = []

    def complete(self, request):
        self.appels.append(request.render_prompt())
        return LLMResult(
            text=f"VERDICT: {self.verdict}\nRAISON: {self.raison}",
            provider="test",
        )


def test_le_llm_peut_confirmer_une_contradiction():
    anomalies = _anomalies(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 45 000 francs comoriens.",
    )
    juge = _LLMJuge("CONTRADICTION")
    retenues = ContradictionValidator(juge, "Combien coûte la traversée ?").validate(anomalies)

    assert len(retenues) == 1
    assert retenues[0].verdict.status == CONFIRMED
    assert retenues[0].verdict.decided_by == "llm"
    assert "15 000" in juge.appels[0], "les phrases en conflit doivent être fournies au juge"


def test_le_llm_peut_ecarter_un_faux_positif():
    anomalies = _anomalies(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 45 000 francs comoriens.",
    )
    validator = ContradictionValidator(_LLMJuge("FAUX_POSITIF", "l'une inclut les taxes"))
    retenues = validator.validate(anomalies)

    assert retenues == []
    assert validator.rejected, "un rejet doit rester traçable, pas disparaître"
    assert "taxes" in validator.rejected[0][1].reason


def test_les_regles_priment_sur_le_llm():
    """Ce que les règles savent trancher n'a pas besoin d'un appel de modèle."""
    anomalies = _anomalies(
        "La hauteur de la tour est de 312 mètres à l'origine.",
        "La hauteur de la tour est aujourd'hui de 500 mètres.",
    )
    juge = _LLMJuge("CONTRADICTION")
    ContradictionValidator(juge).validate(anomalies)
    assert juge.appels == [], "aucun appel inutile au modèle"


def test_un_llm_en_panne_ne_fait_pas_echouer_la_validation():
    from ara.core.errors import ProviderError

    class Panne(_LLMJuge):
        def complete(self, request):
            raise ProviderError("modèle indisponible")

    anomalies = _anomalies(
        "Le billet de la traversée coûte 15 000 francs comoriens.",
        "Le billet de la traversée coûte 45 000 francs comoriens.",
    )
    retenues = ContradictionValidator(Panne("CONTRADICTION")).validate(anomalies)
    assert len(retenues) == 1 and retenues[0].verdict.status == UNCERTAIN


# --- Traçabilité --------------------------------------------------------------


def test_les_rejets_sont_expliques_dans_le_rapport(ctx, toolbox):
    """Un écart écarté doit rester visible : on ne masque pas une décision."""
    from ara.analysis.report import ResearchReport

    anomalies = _anomalies(
        "La hauteur de la tour est de 312 mètres à l'origine.",
        "La hauteur de la tour est aujourd'hui de 500 mètres.",
    )
    validator = ContradictionValidator(OfflineLLM())
    report = ResearchReport(question="hauteur de la tour")
    report.anomalies = validator.validate(anomalies)
    report.dismissed = validator.rejected

    payload = report.to_dict()
    assert payload["contradictions"] == []
    assert payload["dismissed"] and "époque" in payload["dismissed"][0]["reason"]
