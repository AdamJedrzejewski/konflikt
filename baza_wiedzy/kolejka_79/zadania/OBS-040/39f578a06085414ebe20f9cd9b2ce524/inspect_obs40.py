import json
from pathlib import Path

TASK = Path(__file__).parent
ROOT = TASK.parents[4]
job = json.loads((TASK / "zlecenie.json").read_text(encoding="utf-8"))
terms = ["pomoc prawna", "pomocy prawnej", "działalność zawodowa", "działalności zawodowej", "art. 4", "art. 6", "art. 5", "art. 43"]

for src in job["sources"]:
    p = ROOT / src["text"]
    lines = p.read_text(encoding="utf-8").splitlines()
    found = set()
    for i, line in enumerate(lines):
        if any(t.casefold() in line.casefold() for t in terms):
            found.add(i)
    spans = []
    for i in sorted(found):
        a, b = max(0, i-2), min(len(lines), i+3)
        if spans and a <= spans[-1][1]: spans[-1] = (spans[-1][0], b)
        else: spans.append((a,b))
    print(f"\n### {src['id']} ({len(lines)} lines) {p}")
    for a,b in spans:
        print(f"--- {a+1}-{b} ---")
        for j in range(a,b): print(f"{j+1}: {lines[j]}")
