import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-062" / "ba59b0698dc24167922c8af73fba0878"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
for sid, a, b in [("SRC-04", 73, 82), ("SRC-04", 115, 124), ("SRC-04", 134, 142), ("SRC-05", 28, 48), ("SRC-03", 293, 330), ("SRC-06", 30, 80)]:
    print(f"\n== {sid} {a}-{b} ==")
    for i in range(a, min(b, len(sources[sid])) + 1):
        print(f"{i}: {sources[sid][i-1]}")
