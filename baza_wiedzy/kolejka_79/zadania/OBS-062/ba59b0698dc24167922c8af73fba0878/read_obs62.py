import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-062" / "ba59b0698dc24167922c8af73fba0878"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
sources = {x["id"]: (root / x["text"]).read_text(encoding="utf-8-sig").splitlines() for x in job["sources"]}
ranges = {
    "SRC-01": [(430, 450)],
    "SRC-02": [],
    "SRC-03": [(285, 330)],
    "SRC-04": [(73, 84), (113, 126), (133, 143)],
    "SRC-05": [(28, 48)],
    "SRC-06": [(1, 80), (150, 170)],
    "SRC-07": [],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for sid in ("SRC-02", "SRC-07"):
    lines = sources[sid]
    hits = [i for i, line in enumerate(lines, 1) if re.search(r"tajem|confidential|art\. ?16|art\. ?15", line, re.I)]
    ranges[sid] = [(max(1, i - 1), min(len(lines), i + 1)) for i in hits]
for sid, blocks in ranges.items():
    print(f"\n=== {sid} ({len(sources[sid])} lines) ===")
    merged = []
    for a, b in sorted(blocks):
        if merged and a <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    for a, b in merged:
        for i in range(a, b + 1):
            print(f"{i}: {sources[sid][i-1]}")
