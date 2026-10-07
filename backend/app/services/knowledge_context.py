"""Prepare substantive knowledge and share repeated text in the model context."""
from collections import Counter
import json


def pack_context(payload):
    """Every repeated long string is retained once and referenced explicitly."""
    counts = Counter()

    def count(value):
        if isinstance(value, str) and len(value) >= 40:
            counts[value] += 1
        elif isinstance(value, dict):
            for item in value.values():
                count(item)
        elif isinstance(value, list):
            for item in value:
                count(item)

    payload = json.loads(json.dumps(payload, ensure_ascii=False))
    # These are logs of the research/acceptance process. Substantive scope,
    # meanings, records, exceptions, gaps, questions and review limits remain.
    audit_fields = ("coverage", "self_check", "control_results")
    for concept in payload.get("concepts", []):
        for field in audit_fields:
            concept.pop(field, None)
    for note in payload.get("addenda", []):
        if "review" in note and "content" in note:
            if json.loads(note["content"]) == note["review"]:
                del note["content"]
                note["review"].pop("checks", None)
    payload["context_scope"] = {
        "included": "Wszystkie pojęcia, znaczenia, zakresy, rekordy, cytaty, wyjątki, ograniczenia, luki, pytania, powiązania i odrębne noty korekt.",
        "audit_not_sent": [*audit_fields, "review.checks"],
        "note": "Dzienniki kontroli pozostają w plikach objętych wersją bazy. Ich pominięcie w kontekście nie oznacza pełnego pokrycia źródeł.",
    }
    # Evidence retains source_key; the same full source exists in sources.
    for record in payload.get("records", {}).values():
        for evidence in record.get("evidence", []):
            key = evidence.get("source_key")
            source = payload.get("sources", {}).get(key)
            if source and evidence.get("source") == {k: v for k, v in source.items() if k != "source_key"}:
                del evidence["source"]
    count(payload)
    text_ids = {value: f"T{index:04d}" for index, (value, n) in enumerate(counts.items()) if n > 1}

    def replace(value):
        if isinstance(value, str) and value in text_ids:
            return {"text_ref": text_ids[value]}
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        if isinstance(value, list):
            return [replace(item) for item in value]
        return value

    return {"format": "shared_text_v1", "texts": {ref: value for value, ref in text_ids.items()}, "bundle": replace(payload)}
