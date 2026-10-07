import json
from pathlib import Path

root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
cards = {
    "OBS-028": r"baza_wiedzy/kolejka_79/zadania/OBS-028/fd89a1fdd9a14414a785f795e6ddb624/wynik.json",
    "OBS-068": r"baza_wiedzy/kolejka_79/zadania/OBS-068/a1e4715ff2634ea7ab75676dce01e3be/wynik.json",
    "OBS-069": r"baza_wiedzy/kolejka_79/zadania/OBS-069/9aa4b35470a94a92853d772bf0b155a0/wynik.json",
    "OBS-076": r"baza_wiedzy/kolejka_79/zadania/OBS-076/343aedc764a243139971f5b5b887f422/wynik.json",
    "OBS-070": r"baza_wiedzy/kolejka_79/zadania/OBS-070/d51becec30a141f2a1ab9476ea4834e3/wynik.json",
}
for name, rel in cards.items():
    data = json.loads((root / rel).read_text(encoding="utf-8"))
    print("\n##", name)
    for rec in data.get("records", []):
        print(rec["id"], rec["claim"])
    for meaning in data.get("meanings", []):
        print(meaning["id"], meaning["context"], meaning["description"])
    for q in data.get("questions", []):
        print(q["id"], q["question"])
