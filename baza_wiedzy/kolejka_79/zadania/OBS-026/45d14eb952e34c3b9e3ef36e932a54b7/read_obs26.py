import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-026" / "45d14eb952e34c3b9e3ef36e932a54b7"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
ranges = {
    "SRC-01": [(438, 448)],
    "SRC-02": [(23, 25), (31, 33), (41, 43), (55, 57), (59, 61)],
    "SRC-03": [(293, 330)],
    "SRC-04": [(159, 165)],
    "SRC-05": [(33, 45)],
    "SRC-06": [(63, 74), (155, 165)],
    "SRC-07": [(33, 46), (95, 105), (162, 165), (197, 199)],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for sid, blocks in ranges.items():
    print(f"\n== {sid} ==")
    for a, b in blocks:
        for i in range(a, min(b, len(sources[sid])) + 1):
            print(f"{i}: {sources[sid][i-1]}")
