import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
prior = json.loads((root / "baza_wiedzy/kolejka_79/zadania/OBS-017/76f7d3c8bc7e450298a220db8baf3e69/wynik.json").read_text(encoding="utf-8"))
coverage = prior["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["read_ranges"] = "1272-1276"
        item["notes"] = "Ponownie wykorzystana lektura komentarza do art. 30.1; w. 1276 odsyła do definicji z art. 5 pkt 7 i ujmuje konflikt lub znaczne ryzyko jako autorską wykładnię."
    elif item["source_id"] == "SRC-02":
        item["read_ranges"] = "110-112"
        item["notes"] = "Odczytano fragment wyboru WO-87/21. W. 112 opisuje przypisany czyn; oryginału orzeczenia brak, a przytoczone oznaczenie art. 115 § 1 wymaga odróżnienia od odesłania KERP do § 11. Nie wywodzę stąd ogólnego zakazu pomocy rodzinie."
    elif item["source_id"] == "SRC-03":
        item["read_ranges"] = "723-730"
        item["notes"] = "Ponownie wykorzystana lektura poradnika: autor odnosi standard art. 30 do interesu osoby najbliższej, konfliktu rzeczywistego i potencjalnego znacznego ryzyka. Ten sam autor co SRC-01."
    elif item["source_id"] == "SRC-04":
        item["read_ranges"] = "39-53; 207-209"
        item["notes"] = "Lokalny tekst art. 5 pkt 7 odsyła do art. 115 § 11 k.k.; art. 30 ust. 1 osobno wymaga tej samej lub związanej sprawy oraz konfliktu albo znacznego ryzyka."
    elif item["source_id"] == "SRC-07":
        item["read_ranges"] = "175-187"
        item["notes"] = "Wtórne opracowanie SRC-07 przy art. 30 opisuje WO-87/21 i formułuje wniosek o braku bezwzględnego zakazu pomocy rodzinie; zakres i autorstwo wniosku są ograniczone. ON-R09 oraz OBS-018-R05 dokumentują tę samą relację, nie dwa niezależne potwierdzenia."

result = {
    "task_id": "0ffa132749e340879b03c362d86c9e4d",
    "concept_id": "OBS-016",
    "label": "interes osoby najbliższej",
    "points": ["S1-K1-02"],
    "scope": (
        "Mapuję S1-K1-02 na osobny element art. 30 ust. 1 KERP: interes osoby najbliższej radcy prawnego wobec interesu klienta. "
        "ON-R01 odtwarza odesłanie definicyjne z art. 5 pkt 7 do art. 115 § 11 k.k.; ON-R08 przypisuje autorowi komentarza wniosek, "
        "że zwrot w art. 30 ma znaczenie zdefiniowane w art. 5 pkt 7; ON-R05 odtwarza normę art. 30. Definicja określa krąg osób, "
        "ale sama nie ustanawia konfliktu ani zakazu pomocy rodzinie. Zastosowanie wymaga danej lub związanej sprawy i konfliktu "
        "interesów albo znacznego ryzyka jego wystąpienia. Interpretacja konfliktu jako materialnej sprzeczności i objęcie ryzyka "
        "pozostaje poglądem autora z OBS-057-R03, nie nowym niezależnym potwierdzeniem. OBS-012 i OBS-017 już rozdzielają interes "
        "radcy od interesu osoby najbliższej, nie tworzę ich ponownie. ON-R09 i OBS-018-R05 odnoszą się do jednej wtórnie opisanej "
        "sprawy WO-87/21; nie traktuję ich jako niezależnych potwierdzeń, a atrybucja twierdzenia w SRC-07 jest ograniczona. SRC-02 "
        "przedstawia opis przypisanego czynu, bez oryginału orzeczenia. Nie powielam istniejących ON-P01/ON-P03: pierwsze odnotowuje "
        "późniejszą kontrolę brzmienia art. 115 § 11, drugie problem błędnego wskazania § 1 w materiale o WO-87/21. Brak tekstu "
        "art. 115 § 11 w korpusie i brak oryginału orzeczenia pozostają jawne; coverage wykorzystuje rzeczywiście przeczytane zakresy "
        "źródeł z tej i wcześniejszych kart, nie deklaruje pełnej lektury."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "ON-R01", "ON-R05", "ON-R08", "ON-R09", "OBS-018-R05",
        "OBS-057-R03", "SP-R08"
    ],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-016-M01",
            "context": "S1-K1-02, interes osoby najbliższej wobec klienta w art. 30 ust. 1 KERP",
            "description": (
                "Art. 30 ust. 1 wymienia osobę najbliższą radcy jako odrębny podmiot, którego interes może pozostawać w konflikcie "
                "z interesem klienta. Definicja jest odesłana przez art. 5 pkt 7 KERP do art. 115 § 11 k.k. (ON-R01), a autor komentarza "
                "wiąże tę definicję z użyciem zwrotu w art. 30 (ON-R08); samą normę art. 30 odtwarza ON-R05. Znaczenie definicji nie "
                "zastępuje pozostałych przesłanek: pomoc dotyczy danej lub związanej sprawy, a między klientem i osobą najbliższą "
                "musi istnieć konflikt lub znaczne ryzyko jego wystąpienia. Interpretacja konfliktu i ryzyka pochodzi z poglądu autora "
                "OBS-057-R03, już rozważanego wraz z interesem radcy w OBS-012/017. Nie wynika stąd ogólny zakaz pomocy osobom z rodziny. "
                "Wtórne twierdzenie SRC-07 o braku bezwzględnego zakazu i sporze między bliskimi z osobistym interesem radcy jest "
                "ograniczone do opisywanej konfiguracji; ON-R09 i dokumentacyjne OBS-018-R05 opisują tę samą relację i nie są "
                "niezależnymi potwierdzeniami. Oryginału WO-87/21 nie ma w korpusie."
            ),
            "record_ids": ["ON-R01", "ON-R05", "ON-R08", "OBS-057-R03", "ON-R09", "OBS-018-R05", "SP-R08"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-016-G01",
            "issue": "W korpusie nie ma tekstu art. 115 § 11 k.k.; historyczne ON-P01 odnotowuje późniejszą kontrolę odesłania, ale nie zastępuje źródła ani nie rozstrzyga zakresu osób.",
            "needed": "Pozyskać właściwe brzmienie art. 115 § 11 k.k. oraz potwierdzić jego zakres w konsultacji ON-P01; nie rekonstruować katalogu z pamięci."
        },
        {
            "id": "OBS-016-G02",
            "issue": "Fragment SRC-02 dotyczący WO-87/21 podaje art. 115 § 1 k.k.; nie ma oryginału orzeczenia ani pewnej atrybucji całej tezy wtórnego opracowania SRC-07. Problem błędnego paragrafu jest odnotowany w ON-P03.",
            "needed": "Pozyskać oryginał lub wiarygodny pełny tekst WO-87/21 i ustalić, kto formułuje rozważanie o osobie najbliższej; zachować różnicę § 1 i § 11."
        }
    ],
    "questions": [],
    "self_check": (
        "Zachowałem warunki art. 30 ust. 1 i odrębność definicji od konfliktu; nie dopisałem ogólnego zakazu pomocy rodzinie. "
        "ON-R09 i OBS-018-R05 potraktowałem jako jedną relację wtórnie udokumentowaną, z ograniczoną atrybucją. Odesłałem do istniejących "
        "ON-P01/ON-P03 zamiast powielać pytania. Nowych rekordów i pytań nie dodano. Wynik pozostaje OCZEKUJE na odbiór Astry."
    )
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": 0, "questions": 0, "gaps": len(result["gaps"]), "sources": len(coverage)}))
