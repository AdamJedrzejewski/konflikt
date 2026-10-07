"""Integrity and normalization checks for the file based OBSIL knowledge bundle."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.knowledge_bundle import KnowledgeBundle  # noqa: E402


PROJECT = Path(__file__).resolve().parents[1]
HAS_KNOWLEDGE = (PROJECT / "baza_wiedzy/ZREALIZOWANE_OPRACOWANIA.json").exists()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def source_entry(project: Path, source_id: str, source_path: str, text_path: str) -> dict:
    source_file = project / source_path
    text_file = project / text_path
    return {
        "id": source_id,
        "source": source_path,
        "text": text_path,
        "source_sha256": digest(source_file),
        "text_sha256": digest(text_file),
        "lines": len(text_file.read_text(encoding="utf-8").splitlines()),
        "characters": len(text_file.read_text(encoding="utf-8")),
    }


def build_tiny_project(project: Path) -> tuple[str, str]:
    """Build a two-manifest fixture with one historical and one queue card."""
    (project / "sources").mkdir(parents=True)
    historical_text = "Historical quote.\nSecond line.\n"
    current_text = "Current quote.\nSecond line.\n"
    (project / "sources/historical.docx").write_bytes(b"fixture historical source")
    (project / "sources/historical.txt").write_text(historical_text, encoding="utf-8")
    (project / "sources/current.pdf").write_bytes(b"fixture current source")
    (project / "sources/current.txt").write_text(current_text, encoding="utf-8")

    hist_source = source_entry(project, "SRC-01", "sources/historical.docx", "sources/historical.txt")
    hist_manifest_path = project / "baza_wiedzy/kandydaci/2026-09-24_proba_3_pojec/00_MANIFEST_ZRODEL.json"
    write_json(hist_manifest_path, [hist_source])
    hist_card_path = project / "baza_wiedzy/kandydaci/2026-09-24_proba_3_pojec/01_historical.json"
    hist_card = {
        "concept_id": "HIST-01",
        "concept": "historyczne pojęcie",
        "model": "fixture",
        "status": "CZESCIOWY",
        "scope": "historyczny zakres",
        "scheme_points": ["S1-K1-01"],
        "coverage": [{"source_id": "SRC-01", "status": "częściowy", "read_ranges": "1", "notes": ""}],
        "meanings": [{"id": "HIST-M01", "context": "test", "description": "znaczenie historyczne", "record_ids": ["HIST-R01"]}],
        "records": [
            {
                "id": "HIST-R01",
                "kind": "test",
                "claim": "Teza historyczna.",
                "speaker": "Autor historyczny",
                "role": "autor",
                "context": "kontekst",
                "court_treatment": "nie_dotyczy",
                "source_status": "lokalna kopia",
                "evidence": [{"source_id": "SRC-01", "line_start": 1, "line_end": 1, "quote": "Historical quote."}],
                "limits": "Granica historyczna.",
                "related_record_ids": [],
            }
        ],
        "relations": [],
        "gaps": [{"id": "HIST-G01", "description": "luka"}],
        "proposals": [],
        "control_results": {},
        "self_check": "fixture",
        "review": {"reviewer": "Astra", "status": "OCZEKUJE"},
    }
    write_json(hist_card_path, hist_card)
    historical_report_path = project / "baza_wiedzy/kandydaci/2026-09-24_proba_3_pojec/review.md"
    historical_report_path.write_text("Historyczny odbiór częściowy.\n", encoding="utf-8")

    queue_card_path = project / "baza_wiedzy/kolejka_79/zadania/OBS-001/run/wynik.json"
    queue_card = {
        "task_id": "task-1",
        "concept_id": "OBS-001",
        "label": "pojęcie kolejki",
        "points": ["S1-K1-01"],
        "scope": "nowy zakres",
        "completeness": "partial",
        "operator_status": "OCZEKUJE",
        "existing_record_refs": ["HIST-R01"],
        "coverage": [{"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "1", "notes": ""}],
        "meanings": [{"id": "OBS-001-M01", "context": "test", "description": "znaczenie nowe", "record_ids": ["HIST-R01", "OBS-001-R01"]}],
        "records": [
            {
                "id": "OBS-001-R01",
                "kind": "test",
                "claim": "Teza nowa.",
                "speaker": "Autor nowy",
                "role": "autor",
                "context": "kontekst",
                "court_treatment": "nie_dotyczy",
                "source_status": "lokalna kopia",
                "evidence": [{"source_id": "SRC-01", "line_start": 1, "line_end": 1, "quote": "Current quote."}],
                "limits": "Granica nowa.",
            }
        ],
        "relations": [{"from": "OBS-001-R01", "relation": "uzupełnia", "to": "HIST-R01", "status": "kandydat", "record_ids": ["OBS-001-R01"]}],
        "gaps": [{"id": "OBS-001-G01", "description": "nowa luka"}],
        "questions": [{"id": "OBS-001-Q01", "record_ids": ["OBS-001-R01"], "understanding": "test", "variants": "test", "consequences": "test", "question": "test"}],
        "self_check": "fixture",
    }
    write_json(queue_card_path, queue_card)
    card_hash = digest(queue_card_path)
    review_path = project / "baza_wiedzy/kolejka_79/zadania/OBS-001/run/odbior.json"
    write_json(review_path, {"concept_id": "OBS-001", "artifact_sha256": card_hash, "verdict": "CZESCIOWY"})
    current_source = source_entry(project, "SRC-01", "sources/current.pdf", "sources/current.txt")

    queue_path = project / "baza_wiedzy/kolejka_79/kolejka.json"
    queue = {
        "version": 1,
        "sources": [current_source],
        "jobs": [
            {
                "id": "OBS-001",
                "points": ["S1-K1-01"],
                "historical_cards": [
                    {"path": hist_card_path.relative_to(project).as_posix(), "sha256": digest(hist_card_path), "basis_record_ids": ["HIST-R01"]}
                ],
                "status": "CZESCIOWE_Z_BRAKAMI",
                "review_status": "CZESCIOWY",
                "operator_status": "OCZEKUJE",
                "artifact": "zadania/OBS-001/run/wynik.json",
                "artifact_sha256": card_hash,
                "review_artifact": "zadania/OBS-001/run/odbior.json",
            }
        ],
        "historical_manifest_sha256": digest(hist_manifest_path),
        "completed_baseline": {"accepted_partial_cards": 1},
    }
    write_json(queue_path, queue)
    registry = {
        "version": 1,
        "entries": [
            {
                "id": "HIST-ENTRY",
                "concept": "historyczne pojęcie",
                "path": hist_card_path.relative_to(project).as_posix(),
                "sha256": digest(hist_card_path),
                "execution_status": "ZREALIZOWANE_W_ZAKRESIE_PROBY",
                "completeness": "CZESCIOWY",
                "accepted_record_ids": ["HIST-R01"],
                "quotes": 1,
                "review_basis": historical_report_path.relative_to(project).as_posix(),
                "historical_review": {"status": "OCZEKUJE"},
                "remaining_gap_ids": ["HIST-G01"],
                "pending_proposal_ids": [],
                "related_queue_ids": ["OBS-001"],
                "operator_status": "OCZEKUJE",
                "reuse_rule": "odwołaj się do istniejącej pracy",
            },
            {
                "id": "QUEUE-ENTRY",
                "concept": "pojęcie kolejki",
                "path": queue_card_path.relative_to(project).as_posix(),
                "sha256": card_hash,
                "execution_status": "ZREALIZOWANE_W_ZAKRESIE_ODBIORU",
                "completeness": "CZESCIOWY",
                "accepted_record_ids": ["OBS-001-R01"],
                "existing_record_refs": ["HIST-R01"],
                "quotes": 1,
                "review_basis": review_path.relative_to(project).as_posix(),
                "remaining_gap_ids": ["OBS-001-G01"],
                "pending_proposal_ids": [],
                "related_queue_ids": ["OBS-001"],
                "operator_status": "OCZEKUJE",
            },
        ],
        "record_links": [{"from": "OBS-001-R01", "to": "HIST-R01", "relation": "uzupelnienie"}],
        "question_links": [{"question_id": "OBS-001-Q01", "basis_question_ids": ["OBS-001-Q01"]}],
    }
    write_json(project / "baza_wiedzy/ZREALIZOWANE_OPRACOWANIA.json", registry)
    return digest(hist_manifest_path), card_hash


class KnowledgeBundleTests(unittest.TestCase):
    @unittest.skipUnless(HAS_KNOWLEDGE, "brak katalogu baza_wiedzy/ w repozytorium")
    def test_real_project_counts_provenance_and_non_approval_status(self):
        bundle = KnowledgeBundle(PROJECT)
        metadata = bundle.metadata()
        payload = bundle.as_payload()

        self.assertEqual(metadata["concepts"], 82)
        self.assertEqual(metadata["records"], 136)
        self.assertEqual(metadata["points"], 46)
        self.assertEqual(metadata["operator_statuses"], {"OCZEKUJE": 82})
        self.assertEqual(metadata["completeness"], {"CZESCIOWY": 82})
        self.assertEqual(len(bundle.concepts), 82)
        self.assertEqual(len(bundle.records), 136)
        self.assertFalse(any("records" in card for card in payload["concepts"]))
        self.assertEqual(sum(1 for card in payload["concepts"] if not card["accepted_record_ids"]), 38)

        source_01 = [source for source in payload["sources"].values() if source["id"] == "SRC-01"]
        self.assertEqual(len(source_01), 2)
        self.assertEqual(len({source["source_key"] for source in source_01}), 2)
        self.assertEqual(len({source["text_sha256"] for source in source_01}), 2)

        note = next(addendum for addendum in payload["addenda"] if addendum["path"].endswith("DOPRECYZOWANIE_OBS_024.md"))
        self.assertEqual(note["integrity"], "declared_hash_verified")
        self.assertEqual(note["scope"], "OBS-024-M02")
        self.assertEqual(note["basis_record_ids"], ["OBS-047-R03"])
        self.assertIn("pierwszenstwo", note["precedence"])

        serialized = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.assertGreater(len(serialized), 1_000_000)

    def test_tiny_fixture_keeps_duplicate_source_ids_separate_and_resolves_refs(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            build_tiny_project(project)
            bundle = KnowledgeBundle(project)
            payload = bundle.as_payload()

        self.assertEqual(len(bundle.concepts), 2)
        self.assertEqual(set(bundle.records), {"HIST-R01", "OBS-001-R01"})
        self.assertEqual(len([source for source in payload["sources"].values() if source["id"] == "SRC-01"]), 2)
        new_record = bundle.records["OBS-001-R01"]
        self.assertTrue(new_record["evidence"][0]["source_key"].startswith(bundle.metadata()["current_manifest_sha256"]))
        self.assertEqual(new_record["evidence"][0]["quote"], "Current quote.")
        queue_concept = next(card for card in bundle.concepts if card["concept_id"] == "OBS-001")
        self.assertEqual(queue_concept["existing_record_refs"], ["HIST-R01"])
        self.assertEqual(payload["record_links"][0]["to"], "HIST-R01")
        self.assertEqual(payload["question_links"][0]["question_id"], "OBS-001-Q01")

    def test_source_hash_mismatch_fails_without_skipping_source(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            build_tiny_project(project)
            (project / "sources/current.txt").write_text("tampered text\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Hash tekstu źródłowego niezgodny"):
                KnowledgeBundle(project)


class WindowsPathTests(unittest.TestCase):
    def test_backslash_paths_resolve_on_any_system(self):
        with tempfile.TemporaryDirectory() as tmp:
            bundle = object.__new__(KnowledgeBundle)
            bundle.project = Path(tmp).resolve()
            self.assertEqual(
                bundle._project_path("baza_wiedzy\\kolejka_79\\zadania\\odbior.json"),
                bundle.project / "baza_wiedzy/kolejka_79/zadania/odbior.json",
            )


if __name__ == "__main__":
    unittest.main()
