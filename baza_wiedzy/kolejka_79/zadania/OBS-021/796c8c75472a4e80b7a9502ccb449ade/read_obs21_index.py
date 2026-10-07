import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
task = Path(__file__).parent
index = json.loads((task / "odebrane_zakresy.json").read_text(encoding="utf-8"))
ids = {"KL-R01", "KL-R05", "KL-R06", "KL-R12", "KL-R13", "ON-R09"}
prefixes = ("OBS-002-", "OBS-007-", "OBS-015-", "OBS-069-")
for card in index:
    records = [r for r in card.get("records", []) if r.get("id") in ids or r.get("id", "").startswith(prefixes)]
    questions = [q for q in card.get("questions", []) if q.get("id", "").startswith(prefixes) or any(x in q.get("record_ids", q.get("basis_ids", [])) for x in ids)]
    if records or questions:
        print(f"\n== {card.get('path')} ==")
        for r in records:
            print("RECORD", r["id"], r.get("claim", ""))
        for q in questions:
            print("QUESTION", q.get("id"), q.get("understanding", q.get("change", "")))
