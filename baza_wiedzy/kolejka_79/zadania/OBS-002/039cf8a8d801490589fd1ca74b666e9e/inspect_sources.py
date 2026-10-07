import json
import re
import sys
from pathlib import Path

TASK_DIR = Path(__file__).parent
PROJECT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK = json.loads((TASK_DIR / "zlecenie.json").read_text(encoding="utf-8-sig"))
sys.stdout.reconfigure(encoding="utf-8")
args = sys.argv[1:]
search_mode = bool(args and args[0] == "SEARCH")
requested = args[1] if search_mode and len(args) > 1 else (args[0] if args else "")
ranges = [] if search_mode else [(int(a), int(b)) for a, b in (x.split(":") for x in args[1:])]
pattern = re.compile(r"klient|świadcze|czynno|obsług|uprzedn|wcześn|był|był[ay]|zakoń|ustani|termin|data|czas|zakres|umow|pełnomocnictw|rejestr", re.I)
for source in TASK["sources"]:
    if requested and source["id"] != requested:
        continue
    path = PROJECT / source["text"]
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    print(f"\n===== {source['id']} {source['text']} lines={len(lines)} =====")
    if search_mode:
        hits = [i for i, line in enumerate(lines) if pattern.search(line)]
        shown = set()
        for i in hits:
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                if j not in shown:
                    print(f"{j + 1}: {lines[j]}")
                    shown.add(j)
        continue
    for start, end in ranges:
        for i in range(start - 1, min(end, len(lines))):
            print(f"{i + 1}: {lines[i]}")
