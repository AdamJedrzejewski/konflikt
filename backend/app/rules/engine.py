import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

RULES_DIR = Path(__file__).resolve().parent.parent.parent.parent / "rules"


@dataclass
class RuleMatch:
    rule_id: str
    article: str
    configuration: str
    waivable: bool
    result: str  # CONFLICT | CONFLICT_WAIVABLE | NO_CONFLICT
    result_classification: str
    confidence: str
    matched_conditions: list[str]
    description_pl: str


@dataclass
class EngineResult:
    has_absolute_conflict: bool
    has_waivable_conflict: bool
    matched_hard: list[RuleMatch]
    matched_soft: list[RuleMatch]
    overall_result: str  # CONFLICT | CONFLICT_WAIVABLE | NO_CONFLICT | UNCLEAR
    stop_reason: Optional[str]  # jeśli absolute conflict — który artykuł


class RuleEngine:
    def __init__(self, rules_dir: Path = RULES_DIR):
        self.rules_dir = rules_dir
        self._hard_rules: list[dict] = []
        self._soft_rules: list[dict] = []
        self._load_rules()

    def _load_rules(self) -> None:
        """Ładuje reguły z JSON według kolejności z index.json."""
        self._hard_rules = self._load_rule_set("hard")
        self._soft_rules = self._load_rule_set("soft")

    def _load_rule_set(self, category: str) -> list[dict]:
        index_path = self.rules_dir / category / "index.json"
        with open(index_path, encoding="utf-8") as f:
            index = json.load(f)

        rules: list[dict] = []
        for entry in sorted(index["rules"], key=lambda r: r["priority"]):
            rule_path = self.rules_dir / category / entry["file"]
            with open(rule_path, encoding="utf-8") as f:
                rule = json.load(f)
            rules.append(rule)
        return rules

    def evaluate(self, extraction: dict) -> EngineResult:
        """
        Ewaluuje ekstrakcję przez reguły.

        Strategia:
        1. Zbuduj "płaski widok" z grafu encji/relacji (bridge do formatu reguł)
        2. Sprawdź hard rules po kolei (wg priority)
           - Jeśli match i waivable=false: STOP, zwróć CONFLICT natychmiast
        3. Sprawdź soft rules po kolei
        4. Zwróć zagregowany wynik
        """
        # Pre-processing: buduj widok faktów z extraction schema
        fact_view = self._build_fact_view(extraction)

        matched_hard: list[RuleMatch] = []
        matched_soft: list[RuleMatch] = []
        stop_reason: Optional[str] = None

        # Step 1: Hard rules
        for rule in self._hard_rules:
            match_result = self._match_rule(rule, fact_view)
            if match_result is not None:
                rm = self._build_rule_match(rule, match_result)
                matched_hard.append(rm)

                if not rule.get("waivable", True):
                    stop_reason = rule["article"]
                    return EngineResult(
                        has_absolute_conflict=True,
                        has_waivable_conflict=False,
                        matched_hard=matched_hard,
                        matched_soft=[],
                        overall_result="CONFLICT",
                        stop_reason=stop_reason,
                    )

        # Step 2: Soft rules
        for rule in self._soft_rules:
            match_result = self._match_rule(rule, fact_view)
            if match_result is not None:
                rm = self._build_rule_match(rule, match_result)
                matched_soft.append(rm)

        # Step 3: Aggregate
        has_absolute = bool(matched_hard)
        has_waivable = any(r.waivable for r in matched_soft)
        has_non_waivable_soft = any(not r.waivable for r in matched_soft)

        if has_absolute or has_non_waivable_soft:
            overall = "CONFLICT"
        elif has_waivable:
            overall = "CONFLICT_WAIVABLE"
        elif matched_hard or matched_soft:
            overall = "CONFLICT"
        else:
            overall = "NO_CONFLICT"

        return EngineResult(
            has_absolute_conflict=has_absolute or has_non_waivable_soft,
            has_waivable_conflict=has_waivable,
            matched_hard=matched_hard,
            matched_soft=matched_soft,
            overall_result=overall,
            stop_reason=stop_reason,
        )

    # Keyword patterns for entity classification (fuzzy matching on free text)
    _RADCA_KEYWORDS = {"radca", "prawnik", "adwokat", "mecenas", "radca_prawny"}
    _KLIENT_AKTUALNY_KEYWORDS = {"klient", "klient_aktualny", "mocodawca", "zleceniodawca"}
    _KLIENT_BYLY_KEYWORDS = {"byly_klient", "klient_byly", "eks_klient", "dawny_klient"}
    _STRONA_PRZECIWNA_KEYWORDS = {"przeciwnik", "strona_przeciwna", "strona_przeciw", "oponent"}
    _PUBLIC_ROLE_KEYWORDS = {"sedzia", "sędzia", "komornik", "prokurator", "organ", "funkcjonariusz",
                             "organ_wladzy", "pelniacy_funkcje"}
    _NEUTRAL_ROLE_KEYWORDS = {"mediator", "arbiter", "biegly", "biegła", "rozjemca", "koncyliator"}

    def _classify_entity(self, entity: dict) -> set[str]:
        """Klasyfikuje encję na podstawie keywords w type + description."""
        text = f"{entity.get('type', '')} {entity.get('description', '')} {entity.get('name', '')}".lower()
        tags = set()
        if any(kw in text for kw in self._RADCA_KEYWORDS):
            tags.add("radca_prawny")
        if any(kw in text for kw in self._KLIENT_AKTUALNY_KEYWORDS):
            # Rozróżnij aktualnego od byłego
            if any(kw in text for kw in {"byly", "byłe", "dawny", "eks", "uprzedni"}):
                tags.add("klient_byly")
            else:
                tags.add("klient_aktualny")
        if any(kw in text for kw in self._KLIENT_BYLY_KEYWORDS):
            tags.add("klient_byly")
        if any(kw in text for kw in self._STRONA_PRZECIWNA_KEYWORDS):
            tags.add("strona_przeciwna")
        if any(kw in text for kw in self._PUBLIC_ROLE_KEYWORDS):
            tags.add("prior_public_role")
        if any(kw in text for kw in self._NEUTRAL_ROLE_KEYWORDS):
            tags.add("prior_neutral_role")
        # Fallback: use type directly if it matches known categories
        etype = entity.get("type", "").lower().replace(" ", "_")
        if etype in ("radca_prawny",):
            tags.add("radca_prawny")
        if etype in ("klient_aktualny", "klient"):
            tags.add("klient_aktualny")
        if etype in ("klient_byly",):
            tags.add("klient_byly")
        if etype in ("strona_przeciwna", "przeciwnik"):
            tags.add("strona_przeciwna")
        return tags

    def _classify_role(self, role_type: str) -> set[str]:
        """Klasyfikuje rolę na podstawie keywords."""
        text = role_type.lower().replace(" ", "_")
        tags = set()
        if any(kw in text for kw in {"pelnomocnik", "obronca", "obrońca", "reprezentant", "doradca"}):
            tags.add("pelnomocnik_obronca")
        if any(kw in text for kw in self._NEUTRAL_ROLE_KEYWORDS):
            tags.add("prior_neutral_role")
        if any(kw in text for kw in self._PUBLIC_ROLE_KEYWORDS):
            tags.add("prior_public_role")
        return tags

    def _classify_relationship(self, rel_type: str) -> set[str]:
        """Klasyfikuje relację na podstawie keywords."""
        text = rel_type.lower().replace(" ", "_")
        tags = set()
        if any(kw in text for kw in {"pelnomocnik", "obronca", "reprezentuje", "reprezentacja"}):
            tags.add("pelnomocnik_obronca")
        if any(kw in text for kw in {"przeciwnik", "spor", "przeciw"}):
            tags.add("przeciwnik_procesowy")
        if any(kw in text for kw in {"uprzednia", "wczesniej", "wcześniej", "dawna"}):
            tags.add("uprzednia_reprezentacja")
        if any(kw in text for kw in self._NEUTRAL_ROLE_KEYWORDS):
            tags.add("mediator_arbiter")
        return tags

    def _build_fact_view(self, extraction: dict) -> dict:
        """
        Buduje płaski widok faktów z grafu encji/relacji.
        Używa keyword matching na wolnym tekście (nie enum).
        """
        entities = extraction.get("entities", [])
        roles = extraction.get("roles", [])
        relationships = extraction.get("relationships", [])

        # Klasyfikuj encje keyword-matching
        entity_tags: dict[str, set[str]] = {}
        for e in entities:
            entity_tags[e["id"]] = self._classify_entity(e)

        # Zbierz role
        role_tags_by_entity: dict[str, set[str]] = {}
        for r in roles:
            eid = r.get("entity_id", "")
            role_tags_by_entity.setdefault(eid, set()).update(self._classify_role(r.get("role_type", "")))

        # Zbierz relacje
        rel_tags: list[tuple[str, str, set[str]]] = []
        for rel in relationships:
            tags = self._classify_relationship(rel.get("relationship_type", ""))
            rel_tags.append((rel.get("from_entity_id", ""), rel.get("to_entity_id", ""), tags))

        # === Identyfikuj encje po tagach ===
        radca_ids = [eid for eid, tags in entity_tags.items() if "radca_prawny" in tags]
        klient_aktualny_ids = [eid for eid, tags in entity_tags.items() if "klient_aktualny" in tags]
        klient_byly_ids = [eid for eid, tags in entity_tags.items() if "klient_byly" in tags]
        strona_przeciwna_ids = [eid for eid, tags in entity_tags.items() if "strona_przeciwna" in tags]

        # Rola radcy
        radca_roles: list[str] = []
        for rid in radca_ids:
            if "pelnomocnik_obronca" in role_tags_by_entity.get(rid, set()):
                radca_roles.append("pelnomocnik_obronca")
            if "prior_neutral_role" in role_tags_by_entity.get(rid, set()):
                radca_roles.append("mediator")
            if "prior_public_role" in role_tags_by_entity.get(rid, set()):
                radca_roles.append("organ_wladzy_publicznej")
        # Z relacji
        for from_id, to_id, tags in rel_tags:
            if from_id in radca_ids and "pelnomocnik_obronca" in tags:
                if "pelnomocnik_obronca" not in radca_roles:
                    radca_roles.append("pelnomocnik_obronca")
        # Z entity tags
        for rid in radca_ids:
            if "prior_neutral_role" in entity_tags.get(rid, set()):
                if "mediator" not in radca_roles:
                    radca_roles.append("mediator")
            if "prior_public_role" in entity_tags.get(rid, set()):
                if "organ_wladzy_publicznej" not in radca_roles:
                    radca_roles.append("organ_wladzy_publicznej")

        # Czy przeciwnik jest jednocześnie klientem aktualnym radcy?
        opponent_is_current_client = False
        for sp_id in strona_przeciwna_ids:
            if sp_id in klient_aktualny_ids:
                opponent_is_current_client = True
                break
        # Z relacji: klient_aktualny jako przeciwnik_procesowy
        for from_id, to_id, tags in rel_tags:
            if "przeciwnik_procesowy" in tags:
                if (from_id in klient_aktualny_ids and to_id in strona_przeciwna_ids) or \
                   (to_id in klient_aktualny_ids and from_id in strona_przeciwna_ids):
                    opponent_is_current_client = True

        # Czy interesy aktualnego klienta sprzeczne z byłym klientem?
        interests_conflict_with_former = False
        for from_id, to_id, tags in rel_tags:
            if "przeciwnik_procesowy" in tags:
                if (from_id in klient_aktualny_ids and to_id in klient_byly_ids) or \
                   (to_id in klient_aktualny_ids and from_id in klient_byly_ids):
                    interests_conflict_with_former = True

        # Sprawa ta sama / powiązana
        matter_is_same_or_related = False
        for from_id, to_id, tags in rel_tags:
            if "uprzednia_reprezentacja" in tags or "mediator_arbiter" in tags:
                matter_is_same_or_related = True
                break
        if opponent_is_current_client:
            matter_is_same_or_related = True

        # Prior roles radcy
        radca_prior_roles: list[str] = []
        for rid in radca_ids:
            for tag in role_tags_by_entity.get(rid, set()):
                if tag == "prior_neutral_role" and "mediator" not in radca_prior_roles:
                    radca_prior_roles.append("mediator")
                if tag == "prior_public_role" and "organ_wladzy_publicznej" not in radca_prior_roles:
                    radca_prior_roles.append("organ_wladzy_publicznej")
            for etag in entity_tags.get(rid, set()):
                if etag == "prior_neutral_role" and "mediator" not in radca_prior_roles:
                    radca_prior_roles.append("mediator")
                if etag == "prior_public_role" and "organ_wladzy_publicznej" not in radca_prior_roles:
                    radca_prior_roles.append("organ_wladzy_publicznej")

        return {
            "radca_prawny": {
                "role": radca_roles[0] if radca_roles else "",
                "roles": radca_roles,
                "prior_role_in_matter": radca_prior_roles[0] if radca_prior_roles else "",
                "prior_roles_in_matter": radca_prior_roles,
            },
            "opponent": {
                "is_current_client_of_radca": opponent_is_current_client,
            },
            "klient_aktualny": {
                "interests_conflict_with_former_client": interests_conflict_with_former,
                "exists": len(klient_aktualny_ids) > 0,
            },
            "klient_byly": {
                "exists": len(klient_byly_ids) > 0,
            },
            "strona_przeciwna": {
                "exists": len(strona_przeciwna_ids) > 0,
            },
            "matter": {
                "is_same_or_related": matter_is_same_or_related,
                "is_same_or_related_to_former": matter_is_same_or_related and len(klient_byly_ids) > 0,
                "type": extraction.get("matter_type", ""),
            },
            "entities": entities,
            "roles": roles,
            "relationships": relationships,
        }

    def _match_rule(
        self, rule: dict, extraction: dict
    ) -> Optional[list[str]]:
        """
        Sprawdza czy reguła pasuje do ekstrakcji.

        Warunki z alternative=true tworzą grupę OR — wystarczy jeden.
        Warunki bez alternative muszą być spełnione (AND).

        Zwraca listę spełnionych warunków lub None jeśli nie pasuje.
        """
        conditions = rule.get("conditions", [])
        if not conditions:
            return None

        matched_descriptions: list[str] = []
        alternative_conditions = [c for c in conditions if c.get("alternative")]
        required_conditions = [c for c in conditions if not c.get("alternative")]

        # Check required conditions (AND)
        for cond in required_conditions:
            if not self._check_condition(cond, extraction):
                return None
            matched_descriptions.append(
                f"{cond['field']} {cond['operator']} {cond['value']}"
            )

        # Check alternative conditions (OR) — at least one must match
        if alternative_conditions:
            any_alt_matched = False
            for cond in alternative_conditions:
                if self._check_condition(cond, extraction):
                    any_alt_matched = True
                    matched_descriptions.append(
                        f"{cond['field']} {cond['operator']} {cond['value']}"
                    )
            if not any_alt_matched:
                return None

        return matched_descriptions

    def _check_condition(self, condition: dict, extraction: dict) -> bool:
        """Sprawdza pojedynczy warunek."""
        field_path = condition["field"]
        operator = condition["operator"]
        expected = condition["value"]

        values = self._get_field_values(extraction, field_path)

        if operator == "exists":
            return len(values) > 0 and any(
                v is not None and v != "" and v != [] for v in values
            )

        if not values:
            return False

        for val in values:
            if self._apply_operator(operator, val, expected):
                return True
        return False

    def _apply_operator(self, operator: str, actual: Any, expected: Any) -> bool:
        if operator == "eq":
            return actual == expected
        if operator == "in":
            return actual in expected
        if operator == "contains":
            if isinstance(actual, list):
                return expected in actual
            if isinstance(actual, str):
                return expected in actual
            return False
        return False

    def _get_field_values(self, extraction: dict, field_path: str) -> list[Any]:
        """
        Pobiera wartość(ci) z nested dict.

        Obsługuje dot notation (np. "radca_prawny.prior_role_in_matter").
        Obsługuje tablice — jeśli na ścieżce jest lista, zwraca wartości
        ze wszystkich elementów.
        """
        parts = field_path.split(".")
        return self._resolve_path(extraction, parts)

    def _resolve_path(self, obj: Any, parts: list[str]) -> list[Any]:
        if not parts:
            return [obj]

        key = parts[0]
        remaining = parts[1:]

        if isinstance(obj, dict):
            if key not in obj:
                return []
            return self._resolve_path(obj[key], remaining)

        if isinstance(obj, list):
            results: list[Any] = []
            for item in obj:
                if isinstance(item, dict) and key in item:
                    results.extend(self._resolve_path(item[key], remaining))
            return results

        return []

    def _build_rule_match(self, rule: dict, matched_conditions: list[str]) -> RuleMatch:
        return RuleMatch(
            rule_id=rule["id"],
            article=rule["article"],
            configuration=rule.get("configuration", ""),
            waivable=rule.get("waivable", False),
            result=rule["result"],
            result_classification=rule.get("result_classification", ""),
            confidence=rule.get("confidence", "medium"),
            matched_conditions=matched_conditions,
            description_pl=rule.get("description_pl", ""),
        )
