import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.services.knowledge_context import pack_context
from app.services.knowledge_bundle import KnowledgeBundle


def expand(packed):
    def walk(value):
        if isinstance(value, dict):
            if set(value) == {"text_ref"}:
                return packed["texts"][value["text_ref"]]
            return {k: walk(v) for k, v in value.items()}
        if isinstance(value, list):
            return [walk(v) for v in value]
        return value
    return walk(packed["bundle"])


class KnowledgeContextTests(unittest.TestCase):
    def test_shared_text_roundtrip_and_no_source_mutation(self):
        text = "Exact quotation with punctuation, dates and important limits. " * 3
        original = {"records": {"R1": {"claim": text, "evidence": [{"quote": text}]}}, "addenda": [{"content": text}]}
        snapshot = copy.deepcopy(original)
        expanded = expand(pack_context(original))
        expanded.pop("context_scope")
        self.assertEqual(expanded, original)
        self.assertEqual(original, snapshot)

    def test_real_substantive_content_preserved(self):
        bundle = KnowledgeBundle(Path(__file__).resolve().parents[2])
        original = bundle.as_payload()
        expanded = expand(pack_context(original))
        self.assertEqual(expanded["sources"], original["sources"])
        for actual, before in zip(expanded["concepts"], original["concepts"]):
            for key, value in before.items():
                if key not in {"coverage", "self_check", "control_results"}:
                    self.assertEqual(actual[key], value)
        for rid, record in expanded["records"].items():
            for evidence in record["evidence"]:
                if "source" not in evidence:
                    evidence["source"] = {k: v for k, v in expanded["sources"][evidence["source_key"]].items() if k != "source_key"}
            self.assertEqual(record, original["records"][rid])
        notes = [n for n in expanded["addenda"] if n.get("scope") == "OBS-024-M02"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes, [n for n in original["addenda"] if n.get("scope") == "OBS-024-M02"])


if __name__ == "__main__":
    unittest.main()
