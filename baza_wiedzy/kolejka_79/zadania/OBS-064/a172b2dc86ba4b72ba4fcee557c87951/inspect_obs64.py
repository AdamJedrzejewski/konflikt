import json
from pathlib import Path

root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
cards = {
    "OBS-008": r"baza_wiedzy/kolejka_79/zadania/OBS-008/8b873552db184a7092be87beafb9f636/wynik.json",
    "OBS-069": r"baza_wiedzy/kolejka_79/zadania/OBS-069/9aa4b35470a94a92853d772bf0b155a0/wynik.json",
}
for name, rel in cards.items():
    data = json.loads((root / rel).read_text(encoding="utf-8"))
    print("\n##", name)
    for rec in data.get("records", []):
        print(rec["id"], rec["claim"])
    for meaning in data.get("meanings", []):
        print(meaning["id"], meaning["context"], meaning["description"])
