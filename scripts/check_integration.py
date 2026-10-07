"""Exercise the actual API, adapter and corpus, without opening a public server."""
import argparse
import json
from pathlib import Path
import sys

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP / "backend"))
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

parser = argparse.ArgumentParser()
parser.add_argument("--live", action="store_true", help="Use the ChatGPT subscription for one synthetic case")
args = parser.parse_args()
assert settings.local_test_mode and settings.llm_provider == "codex_chatgpt"
assert settings.knowledge_mode == "experimental"
from app.services.knowledge_bundle import KnowledgeBundle
bundle = KnowledgeBundle(Path(settings.knowledge_project_path))
print(json.dumps({"knowledge": bundle.metadata(), "payload_characters": len(json.dumps(bundle.as_payload(), ensure_ascii=False)), "provider": settings.llm_provider, "model": settings.llm_model_name}, ensure_ascii=False))

with TestClient(app) as client:
    assert client.get("/health").status_code == 200
    if args.live:
        response = client.post("/api/v1/analyze", json={"fact_pattern":
            "Kazus syntetyczny do testu. Radca prawny otrzymał od spółki Alfa prośbę o poradę dotyczącą umowy ze spółką Beta. W przeszłości radca wykonywał czynności dla Bety. Nie podano ich zakresu ani dat, nie wiadomo, czy obsługa Bety trwa. Nie opisano sporu ani treści umowy. Oceń wyłącznie w dostępnym zakresie i wskaż fakty potrzebne do dalszej analizy."})
        assert response.status_code == 202, response.text
        aid = response.json()["id"]
        result = client.get("/api/v1/analyze/" + aid).json()
        target = APP.parent / "dokumentacja/2026-09-27_integracja_modelu_i_bazy"
        target.mkdir(exist_ok=True)
        (target / "proba_api.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        assert result["status"] == "complete", result.get("final_result")
        final = result["final_result"]
        assert final["knowledge"]["version"] == bundle.version
        assert final["model_connection"]["authentication"] == "chatgpt"
        assert final["record_ids"] and final["missing_information"]
        assert {r["id"] for r in final["sources_used"]} == set(final["record_ids"])
        assert all(r == bundle.records[r["id"]] for r in final["sources_used"])
        assert final["conflict_classification"] == "UNCLEAR"
        history = client.get("/api/v1/history/" + aid).json()
        assert history["final_result"] == final
        print(json.dumps({"result": "OK", "analysis_id": aid, "classification": final["conflict_classification"], "record_ids": final["record_ids"], "questions": len(final["missing_information"]), "saved_and_reopened": True}, ensure_ascii=False))
