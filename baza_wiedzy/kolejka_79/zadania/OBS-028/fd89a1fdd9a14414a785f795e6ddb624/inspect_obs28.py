import json, sys
from pathlib import Path

HERE = Path(__file__).parent
PROJECT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
manifest = json.loads((HERE / "zlecenie.json").read_text(encoding="utf-8-sig"))
sys.stdout.reconfigure(encoding="utf-8")
for item in manifest["sources"]:
    if len(sys.argv) < 2 or item["id"] != sys.argv[1]:
        continue
    lines = (PROJECT / item["text"]).read_text(encoding="utf-8-sig").splitlines()
    print(f"===== {item['id']} {item['text']} lines={len(lines)} =====")
    for arg in sys.argv[2:]:
        start, end = map(int, arg.split(":"))
        for i in range(start-1, min(end, len(lines))):
            print(f"{i+1}: {lines[i]}")
