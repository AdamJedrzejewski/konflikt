import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-032" / "e9947a58fcbc472bbb869bd3b3397956"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
for sid, a, b in [("SRC-01", 432, 436), ("SRC-01", 450, 456), ("SRC-02", 64, 70), ("SRC-03", 243, 292), ("SRC-04", 157, 165), ("SRC-06", 155, 165), ("SRC-07", 31, 40), ("SRC-07", 113, 118)]:
    print(f"\n== {sid} {a}-{b} ==")
    for i in range(a, min(b, len(sources[sid])) + 1):
        print(f"{i}: {sources[sid][i-1]}")
