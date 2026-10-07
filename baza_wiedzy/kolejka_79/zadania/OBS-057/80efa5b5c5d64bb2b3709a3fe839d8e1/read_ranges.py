import json
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK = ROOT / "baza_wiedzy/kolejka_79/zadania/OBS-057/80efa5b5c5d64bb2b3709a3fe839d8e1"
job = json.loads((TASK / "zlecenie.json").read_text(encoding="utf-8"))
windows = {
    "SRC-01": [(928, 928), (964, 976), (1276, 1283)],
    "SRC-02": [(18, 32), (70, 76)],
    "SRC-03": [(348, 365), (625, 656), (723, 730)],
    "SRC-04": [(187, 210)],
    "SRC-05": [(580, 625)],
    "SRC-06": [(100, 140)],
    "SRC-07": [(110, 145)],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for src in job["sources"]:
    ranges = windows.get(src["id"], [])
    path = ROOT / src["text"]
    lines = path.read_text(encoding="utf-8").splitlines()
    print(f"\n### {src['id']} {path}")
    for start, end in ranges:
        print(f"--- {start}-{end}")
        for n in range(start, min(end, len(lines)) + 1):
            print(f"{n}: {lines[n-1]}")
