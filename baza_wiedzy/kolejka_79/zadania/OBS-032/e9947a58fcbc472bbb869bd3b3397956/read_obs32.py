import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-032" / "e9947a58fcbc472bbb869bd3b3397956"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
ranges = {
    "SRC-01": [(425, 456)],
    "SRC-02": [(33, 40), (59, 76), (79, 83), (109, 112)],
    "SRC-03": [(241, 300), (330, 375)],
    "SRC-04": [(156, 168)],
    "SRC-05": [(155, 180)],
    "SRC-06": [(150, 170), (190, 210)],
    "SRC-07": [(30, 40), (110, 120), (130, 140), (190, 200)],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for sid, blocks in ranges.items():
    print(f"\n=== {sid} ===")
    for a, b in blocks:
        for i in range(a, min(b, len(sources[sid])) + 1):
            print(f"{i}: {sources[sid][i-1]}")
