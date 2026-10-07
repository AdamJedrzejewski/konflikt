import json
from pathlib import Path

root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
paths = {
    "OBS-076": r"baza_wiedzy/kolejka_79/zadania/OBS-076/343aedc764a243139971f5b5b887f422/wynik.json",
    "OBS-030": r"baza_wiedzy/kolejka_79/zadania/OBS-030/746b96d89d2f41e8ac54168d6304581d/wynik.json",
    "OBS-010": r"baza_wiedzy/kolejka_79/zadania/OBS-010/cdda4dd48d1e4f0b86268504ac7e7c9e/wynik.json",
    "OBS-043": r"baza_wiedzy/kolejka_79/zadania/OBS-043/688e7da9f2b74c91a96d0345878c6d1b/wynik.json",
}
for label, rel in paths.items():
    data = json.loads((root / rel).read_text(encoding="utf-8"))
    print("\n", label)
    for rec in data.get("records", []):
        print(rec["id"], rec["claim"])
    for q in data.get("questions", []):
        print(q["id"], q["question"])
