"""
Modul porownujacy wyniki analizy schematycznej i niezaleznej (dual-analysis).
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ComparisonResult:
    consistent: bool  # czy wyniki zgodne
    schematic_result: str  # CONFLICT / NO_CONFLICT / CONFLICT_WAIVABLE / UNCLEAR
    independent_result: str  # conflict_classification z analizy niezaleznej
    divergence_reason: Optional[str]  # jesli rozbiezne — dlaczego
    additional_questions: list[str] = field(default_factory=list)  # max 2 pytania jesli rozbiezne
    final_result: Optional[str] = None  # None jesli nadal rozbiezne
    confidence: str = "sredni"


# Mapowanie: schematic_result -> zbiory zgodnych conflict_classification
_CONCORDANCE_MAP: dict[str, set[str]] = {
    "CONFLICT": {"konflikt_oczywisty"},
    "CONFLICT_WAIVABLE": {"wysoki_poziom_ryzyka", "potencjalny_konflikt"},
    "NO_CONFLICT": {"brak_konfliktu"},
    "UNCLEAR": {"potencjalny_konflikt", "wysoki_poziom_ryzyka"},
}

# Priorytet wynikow (im wyzsza wartosc, tym powazniejszy wynik)
_SEVERITY: dict[str, int] = {
    "brak_konfliktu": 0,
    "NO_CONFLICT": 0,
    "potencjalny_konflikt": 1,
    "UNCLEAR": 1,
    "wysoki_poziom_ryzyka": 2,
    "CONFLICT_WAIVABLE": 2,
    "konflikt_oczywisty": 3,
    "CONFLICT": 3,
}


def compare_results(schematic: dict, independent: dict) -> ComparisonResult:
    """
    Porownuje wyniki dual-analysis.

    Mapowanie: schematic_result -> independent conflict_classification:
    - CONFLICT -> konflikt_oczywisty
    - CONFLICT_WAIVABLE -> wysoki_poziom_ryzyka lub potencjalny_konflikt
    - NO_CONFLICT -> brak_konfliktu
    - UNCLEAR -> potencjalny_konflikt lub wysoki_poziom_ryzyka

    Jesli rozbiezne: generuje max 2 pytania uzupelniajace skupione na roznicy.
    """
    schematic_result = schematic.get("schematic_result", "UNCLEAR")
    independent_result = independent.get("conflict_classification", "potencjalny_konflikt")

    concordant_set = _CONCORDANCE_MAP.get(schematic_result, set())
    consistent = independent_result in concordant_set

    if consistent:
        return ComparisonResult(
            consistent=True,
            schematic_result=schematic_result,
            independent_result=independent_result,
            divergence_reason=None,
            additional_questions=[],
            final_result=_resolve_consistent(schematic_result, independent_result),
            confidence=_resolve_confidence(schematic, independent),
        )

    divergence_reason = _explain_divergence(schematic_result, independent_result)
    questions = _generate_questions(schematic, independent, schematic_result, independent_result)
    final_result = _try_resolve_divergence(schematic_result, independent_result)

    return ComparisonResult(
        consistent=False,
        schematic_result=schematic_result,
        independent_result=independent_result,
        divergence_reason=divergence_reason,
        additional_questions=questions,
        final_result=final_result,
        confidence="niski",
    )


def _resolve_consistent(schematic_result: str, independent_result: str) -> str:
    """Gdy wyniki zgodne, zwraca wynik koncowy."""
    if schematic_result == "CONFLICT":
        return "CONFLICT"
    if schematic_result == "NO_CONFLICT":
        return "NO_CONFLICT"
    if schematic_result == "CONFLICT_WAIVABLE":
        return "CONFLICT_WAIVABLE"
    # UNCLEAR — obie analizy niepewne
    return "UNCLEAR"


def _resolve_confidence(schematic: dict, independent: dict) -> str:
    """Ustala poziom pewnosci na podstawie obu analiz."""
    schematic_conf = schematic.get("schematic_confidence", "niska")
    independent_conf = independent.get("confidence_level", "niski")

    confidence_values = {"wysoka": 2, "wysoki": 2, "srednia": 1, "sredni": 1, "niska": 0, "niski": 0}
    s_val = confidence_values.get(schematic_conf, 0)
    i_val = confidence_values.get(independent_conf, 0)

    combined = min(s_val, i_val)
    return {0: "niski", 1: "sredni", 2: "wysoki"}[combined]


def _explain_divergence(schematic_result: str, independent_result: str) -> str:
    """Generuje opis przyczyny rozbieznosci."""
    s_severity = _SEVERITY.get(schematic_result, 1)
    i_severity = _SEVERITY.get(independent_result, 1)

    if s_severity > i_severity:
        return (
            f"Analiza schematyczna ({schematic_result}) wskazuje wyzszy poziom ryzyka "
            f"niz analiza niezalezna ({independent_result}). "
            f"Drzewo decyzyjne moglo aktywowac reguly, ktorych analiza niezalezna nie uzna za decydujace."
        )
    if s_severity < i_severity:
        return (
            f"Analiza niezalezna ({independent_result}) wskazuje wyzszy poziom ryzyka "
            f"niz analiza schematyczna ({schematic_result}). "
            f"Analiza niezalezna mogla dostrzec aspekty ryzyka, ktore nie sa ujete w drzewie decyzyjnym."
        )
    return (
        f"Wyniki roznia sie klasyfikacja ({schematic_result} vs {independent_result}), "
        f"mimo podobnego poziomu ryzyka. Rozbieznosc dotyczy kategoryzacji, nie powagi."
    )


def _generate_questions(
    schematic: dict,
    independent: dict,
    schematic_result: str,
    independent_result: str,
) -> list[str]:
    """Generuje max 2 pytania uzupelniajace skupione na roznicy miedzy analizami."""
    questions: list[str] = []

    s_severity = _SEVERITY.get(schematic_result, 1)
    i_severity = _SEVERITY.get(independent_result, 1)

    if s_severity > i_severity:
        # Schematyczna bardziej surowa — pytaj o okolicznosci lagodzace
        triggered = schematic.get("triggered_absolute", []) + schematic.get("triggered_waivable", [])
        if triggered:
            questions.append(
                "Czy istnieja okolicznosci, ktore moglby lagodzic stwierdzone naruszenia regul "
                f"({', '.join(triggered)}), np. zgoda klientow lub bariery organizacyjne?"
            )
        questions.append(
            "Czy w stanie faktycznym wystepuja dodatkowe okolicznosci nieujete w opisie, "
            "ktore moglyby wplynac na ocene ryzyka konfliktu interesow?"
        )
    elif s_severity < i_severity:
        # Niezalezna bardziej surowa — pytaj o dodatkowe ryzyka
        independent_risk_fields = [
            ("confidential_information_risk", "ryzyko naruszenia tajemnicy zawodowej"),
            ("adversity_risk", "ryzyko sprzecznosci interesow"),
            ("successive_representation_risk", "ryzyko z uprzedniego swiadczenia pomocy"),
        ]
        high_risks = [
            label
            for field_name, label in independent_risk_fields
            if independent.get(field_name) in ("wysokie", "krytyczne")
        ]
        if high_risks:
            questions.append(
                f"Analiza niezalezna wskazuje wysokie ryzyko w obszarach: {', '.join(high_risks)}. "
                "Czy mozesz potwierdzic lub wykluczyc te ryzyka na podstawie dodatkowych informacji?"
            )
        questions.append(
            "Czy istnieja fakty dotyczace relacji miedzy stronami, ktore nie zostaly ujete w opisie stanu faktycznego?"
        )
    else:
        questions.append(
            "Czy mozesz doprecyzowac okolicznosci stanu faktycznego, ktore pozwolylyby rozstrzygnac "
            "rozbieznosc miedzy analiza schematyczna a niezalezna?"
        )

    return questions[:2]


def _try_resolve_divergence(schematic_result: str, independent_result: str) -> Optional[str]:
    """
    Proba rozstrzygniecia rozbieznosci.

    Zasada ostroznosci: jesli jedna analiza wskazuje CONFLICT (zakaz bezwzgledny),
    przyjmujemy ten wynik. W pozostalych przypadkach rozbieznosc jest nierozstrzygalna
    bez dodatkowych danych.
    """
    s_severity = _SEVERITY.get(schematic_result, 1)
    i_severity = _SEVERITY.get(independent_result, 1)

    # Jesli ktorykolwiek wynik wskazuje zakaz bezwzgledny — przyjmij ostrozniejszy
    if s_severity == 3 or i_severity == 3:
        return "CONFLICT"

    # W pozostalych przypadkach rozbieznosc wymaga dodatkowych danych
    return None
