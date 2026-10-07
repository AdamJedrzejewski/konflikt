import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.services.knowledge_analysis import analyze_with_knowledge


class Bundle:
    version = "test-version"
    records = {"R1": {"id": "R1", "claim": "Literal source claim", "evidence": [{"quote": "Exact quotation"}]}}
    addenda = [{"scope": "test", "text": "Authoritative correction"}]

    def __init__(self, _):
        pass

    def metadata(self):
        return {"version": self.version}

    def as_payload(self):
        return {"records": self.records, "addenda": self.addenda}


class Adapter:
    last_metadata = {"provider": "codex_chatgpt", "authentication": "chatgpt"}

    def __init__(self, result):
        self.result = result

    async def call_json(self, instruction, payload, schema):
        assert "Exact quotation" in payload
        assert "Authoritative correction" in payload
        return copy.deepcopy(self.result)


def answer():
    return dict(entities=[], roles=[], relationships=[], matter_type="test",
        missing_information=[], knowledge_gaps=[], analysis_completeness="czesciowa",
        conflict_classification="NO_CONFLICT", risk_level="niskie", confidence_level="umiarkowany",
        justification="Test [R1]", legal_basis=[], record_ids=["R1"], checked_points=[],
        unassessed_scope=[], article_evaluations=[])


class KnowledgeAnalysisTests(unittest.IsolatedAsyncioTestCase):
    @patch("app.services.knowledge_analysis.KnowledgeBundle", Bundle)
    async def test_insufficient_analysis_prevents_no_conflict_without_reported_gaps(self):
        value = answer()
        value["analysis_completeness"] = "niedostateczna"
        value["checked_points"] = ["test-point"]
        result = await analyze_with_knowledge(Adapter(value), "case", Path("."))
        self.assertEqual(result["conflict_classification"], "UNCLEAR")

    @patch("app.services.knowledge_analysis.KnowledgeBundle", Bundle)
    async def test_saved_citations_come_from_bundle_with_version_and_status(self):
        result = await analyze_with_knowledge(Adapter(answer()), "synthetic case", Path("."))
        self.assertEqual(result["sources_used"], [Bundle.records["R1"]])
        self.assertEqual(result["knowledge"]["version"], "test-version")
        self.assertEqual(result["knowledge"]["operator_status"], "OCZEKUJE")
        self.assertEqual(result["review_addenda"], Bundle.addenda)

    @patch("app.services.knowledge_analysis.KnowledgeBundle", Bundle)
    async def test_unknown_reference_fails_instead_of_becoming_source(self):
        result = answer()
        result["record_ids"] = ["invented"]
        with self.assertRaisesRegex(ValueError, "nieistniejące"):
            await analyze_with_knowledge(Adapter(result), "case", Path("."))

    @patch("app.services.knowledge_analysis.KnowledgeBundle", Bundle)
    async def test_missing_facts_prevent_no_conflict(self):
        result = answer()
        result["missing_information"] = ["Is the representation current?"]
        out = await analyze_with_knowledge(Adapter(result), "case", Path("."))
        self.assertEqual(out["conflict_classification"], "UNCLEAR")
        self.assertIn("result_guard", out)

    @patch("app.services.knowledge_analysis.KnowledgeBundle", Bundle)
    async def test_unassessed_scope_prevents_general_no_conflict(self):
        result = answer()
        result["unassessed_scope"] = ["one branch not evaluated"]
        out = await analyze_with_knowledge(Adapter(result), "case", Path("."))
        self.assertEqual(out["conflict_classification"], "UNCLEAR")


if __name__ == "__main__":
    unittest.main()
