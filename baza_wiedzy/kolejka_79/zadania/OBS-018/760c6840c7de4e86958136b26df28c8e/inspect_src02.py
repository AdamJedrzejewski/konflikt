import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-018" / "760c6840c7de4e86958136b26df28c8e"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
src = next(x for x in job["sources"] if x["id"] == "SRC-02")
lines = (root / src["text"]).read_text(encoding="utf-8-sig").splitlines()
for i in range(104, 113):
    print(f"{i}: {lines[i-1]}")
