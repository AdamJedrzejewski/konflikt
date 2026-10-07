import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-077" / "f28f661bb38c4d75adf8c981cb95cdd6"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
ranges = {
    "SRC-01": [(428, 448)],
    "SRC-02": [(22, 26)],
    "SRC-03": [(241, 260), (293, 312)],
    "SRC-04": [(118, 163)],
    "SRC-05": [(33, 45)],
    "SRC-06": [(150, 165)],
    "SRC-07": [(31, 46), (193, 200)],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for sid, blocks in ranges.items():
    print(f"\n== {sid} ==")
    for a, b in blocks:
        for i in range(a, min(b, len(sources[sid])) + 1):
            print(f"{i}: {sources[sid][i-1]}")
