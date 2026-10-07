import json
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK = ROOT / "baza_wiedzy/kolejka_79/zadania/OBS-015/2811056334224caa8e3194d41df5b1ca"
job = json.loads((TASK / "zlecenie.json").read_text(encoding="utf-8"))
windows = {
    "SRC-01": [(925, 930)],
    "SRC-02": [(18, 32), (70, 76)],
    "SRC-03": [(340, 365)],
    "SRC-04": [(60, 95)],
    "SRC-05": [(24, 30), (93, 99)],
    "SRC-06": [(22, 44), (121, 137)],
    "SRC-07": [(139, 153), (161, 171)],
    "SRC-08": [(1, 35)],
    "SRC-09": [(1, 37)],
}
for src in job["sources"]:
    lines = (ROOT / src["text"]).read_text(encoding="utf-8-sig").splitlines()
    print(f"\n### {src['id']}")
    for start, end in windows[src["id"]]:
        print(f"--- {start}-{end}")
        for n in range(start, min(end, len(lines)) + 1):
            print(f"{n}: {lines[n-1]}")
