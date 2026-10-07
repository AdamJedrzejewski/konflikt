"""Diagnostic: account mode and a harmless model response. Never prints tokens."""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.adapters.codex_transport import CodexSession

parser = argparse.ArgumentParser()
parser.add_argument("--model", default="gpt-6-astra")
parser.add_argument("--probe", action="store_true")
args = parser.parse_args()
with CodexSession(timeout=120) as session:
    print(json.dumps({"authentication": "chatgpt", "plan": session.plan, "models": session.models()}, ensure_ascii=False))
    if args.probe:
        result, meta = session.complete("Odpowiedz wyłącznie obiektem JSON. To test połączenia OBSIL.",
            'Zwróć {"status":"OK","application":"OBSIL"}.',
            {"type":"object","properties":{"status":{"type":"string"},"application":{"type":"string"}},"required":["status","application"],"additionalProperties":False}, args.model)
        assert result == {"status":"OK","application":"OBSIL"}
        print(json.dumps({"result": result, "connection": meta}, ensure_ascii=False))
