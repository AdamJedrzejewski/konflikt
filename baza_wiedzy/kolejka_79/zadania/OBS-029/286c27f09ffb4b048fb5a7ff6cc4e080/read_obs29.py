import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-029" / "286c27f09ffb4b048fb5a7ff6cc4e080"
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
ranges = {
    "SRC-01": [(440, 465)],
    "SRC-02": [(1, 112)],
    "SRC-03": [(250, 300)],
    "SRC-04": [(60, 80), (345, 365)],
    "SRC-05": [(150, 165)],
    "SRC-06": [(1, 325)],
    "SRC-07": [(1, 218)],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for src in job["sources"]:
    sid = src["id"]
    lines = (root / src["text"]).read_text(encoding="utf-8-sig").splitlines()
    print(f"\n===== {sid} ({len(lines)} lines) =====")
    selected = ranges.get(sid, [])
    if sid in {"SRC-02", "SRC-06", "SRC-07"}:
        hits = [i for i, line in enumerate(lines, 1) if re.search(r"niezale|art\. ?7|art\. ?13|art\. ?14|art\. ?41", line, re.I)]
        selected = [(max(1, i - 1), min(len(lines), i + 1)) for i in hits]
    merged = []
    for a, b in sorted(selected):
        if merged and a <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    for a, b in merged:
        for i in range(a, b + 1):
            print(f"{i}: {lines[i-1]}")
