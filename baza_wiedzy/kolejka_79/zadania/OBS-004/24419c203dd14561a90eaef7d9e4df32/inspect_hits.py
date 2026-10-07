import json
import sys
from pathlib import Path

sys.stdout.reconfigure(errors="backslashreplace")
task_dir = Path(__file__).resolve().parent
brief = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
project = Path(brief["project"])
terms = ("biegły", "biegly", "opinia prywatna", "biegłych", "bieglych")
for source in brief["sources"]:
    lines = (project / source["text"]).read_text(encoding="utf-8-sig").splitlines()
    hits = [i for i, line in enumerate(lines) if any(term in line.casefold() for term in terms)]
    print(source["id"], "lines", len(lines), "hits", len(hits))
    for i in hits:
        start, end = max(0, i - 1), min(len(lines), i + 2)
        print(f"  block {start+1}-{end}:")
        for j in range(start, end):
            print(f"    {j+1}: {lines[j]}")
