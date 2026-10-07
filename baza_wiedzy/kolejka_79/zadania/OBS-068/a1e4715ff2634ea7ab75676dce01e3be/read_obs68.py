import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-068" / "a1e4715ff2634ea7ab75676dce01e3be"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
ranges = {
    "SRC-01": [(432, 468), (688, 732)],
    "SRC-02": [(26, 35)],
    "SRC-03": [(340, 365), (1008, 1035)],
    "SRC-04": [(159, 173)],
    "SRC-05": [(30, 45)],
    "SRC-06": [(151, 165)],
    "SRC-07": [(47, 58), (193, 200)],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for sid, blocks in ranges.items():
    print(f"\n== {sid} ==")
    for a, b in blocks:
        for i in range(a, min(b, len(sources[sid])) + 1):
            print(f"{i}: {sources[sid][i-1]}")
print("\n== odebrane_zakresy matching ==")
index = json.loads((task_dir / "odebrane_zakresy.json").read_text(encoding="utf-8"))
for card in index:
    for rec in card.get("records", []):
        if rec.get("id", "").startswith(("OBS-028-", "OBS-076-", "OBS-007-", "OBS-002-")):
            print(rec["id"], rec.get("claim", ""))
    for q in card.get("questions", []):
        if q.get("id", "").startswith(("OBS-028-", "OBS-076-")):
            print(q["id"], q.get("understanding", q.get("change", "")))
