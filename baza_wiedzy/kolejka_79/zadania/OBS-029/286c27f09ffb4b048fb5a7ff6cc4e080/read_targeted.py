import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-029" / "286c27f09ffb4b048fb5a7ff6cc4e080"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
for sid, a, b in [("SRC-04", 64, 76), ("SRC-04", 347, 355), ("SRC-05", 155, 163), ("SRC-03", 261, 292), ("SRC-01", 452, 456), ("SRC-06", 47, 52), ("SRC-07", 113, 118)]:
    print(f"\n== {sid} {a}-{b} ==")
    for i in range(a, b + 1):
        print(f"{i}: {sources[sid][i-1]}")
