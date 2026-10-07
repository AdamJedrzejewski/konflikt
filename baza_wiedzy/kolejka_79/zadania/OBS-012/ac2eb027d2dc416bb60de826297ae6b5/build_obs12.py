import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
previous = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-057" / "80efa5b5c5d64bb2b3709a3fe839d8e1" / "wynik.json"
previous_result = json.loads(previous.read_text(encoding="utf-8"))
coverage = previous_result["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["read_ranges"] = "928; 964-976; 1272-1276"
        item["notes"] = "Komentarz P. Skuczyńskiego: materialna sprzeczność, art. 28 ust. 2 i ostrożne odniesienie do art. 30.1 oraz jego wcześniejszego brzmienia. Wersja do korekty; tezy nie traktuję jako normy ani niezależnego potwierdzenia SRC-03."
    elif item["source_id"] == "SRC-03":
        item["read_ranges"] = "348-365; 625-656; 723-730"
        item["notes"] = "Poradnik rozróżnia konflikt materialny i formalny, wyjaśnia relację interesów przy art. 30 i znaczne ryzyko. Ten sam autor co SRC-01, nie niezależne potwierdzenie. W. 647 zachowuje marker redakcyjny, którego nie używam w nowej tezie."
    elif item["source_id"] == "SRC-04":
        item["read_ranges"] = "187-211"
        item["notes"] = "Lokalny tekst art. 28-30; art. 30 ust. 1 odrębnie wymienia konflikt i znaczne ryzyko. Aktualności kopii nie weryfikowano."

result = {
    "task_id": "ac2eb027d2dc416bb60de826297ae6b5",
    "concept_id": "OBS-012",
    "label": "interes",
    "points": ["S1-K1-04", "S1-K1-06"],
    "scope": (
        "Mapuję S1-K1-04 do interesu radcy prawnego wobec interesu klienta, a S1-K1-06 do interesu osoby najbliższej "
        "wobec interesu klienta, w ramach art. 30 ust. 1. OBS-057-R03 już stosuje objaśnienie materialnej sprzeczności "
        "do obu konfiguracji; nie dodaję nowej tezy. OBS-057-R01 daje ogólną definicję interesów i OBS-057-R02 odróżnia "
        "test materialny od formalnych zakazów. Nie przenoszę bez zastrzeżeń definicji interesu klienta z OBS-015-R01/R02 "
        "na interes radcy lub osoby najbliższej. Art. 15 u.r.p. dotyczy wyłączenia we własnej sprawie; autorskie wskazanie, "
        "że art. 30 dookreśla go „w pewnym zakresie”, nie jest pełną definicją interesu własnego (OBS-018-R01/R02). "
        "OBS-018-R03 dotyczy szczególnej umowy z klientem i nie rozszerza się na art. 30 ust. 1. Lokalny art. 30 ust. 1 "
        "osobno ustanawia konflikt istniejący oraz znaczne ryzyko jego wystąpienia; nie sprowadzam ryzyka do procentu ani "
        "nie utożsamiam z już stwierdzoną sprzecznością. Pytania OBS-057-Q01 o materialny test i próg znacznego ryzyka "
        "oraz OBS-015-Q01 o interes pozaprawny klienta pozostają odrębne. Coverage dziewięciu źródeł reused z odebranego "
        "OBS-057; karta częściowa, bo źródła nie podają kompletnej miary interesu radcy/osoby najbliższej ani eksperckiego "
        "progu ryzyka."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "SP-R08", "ON-R05", "OBS-057-R01", "OBS-057-R02", "OBS-057-R03",
        "OBS-015-R01", "OBS-015-R02", "OBS-018-R01", "OBS-018-R02", "OBS-018-R03"
    ],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-012-M01",
            "context": "S1-K1-04, art. 30 ust. 1 KERP, interes radcy prawnego wobec interesu klienta",
            "description": (
                "OBS-057-R03 ujmuje konflikt z art. 30 ust. 1 jako ocenę zbliżoną do materialnej sprzeczności między "
                "interesem klienta i interesem radcy, obejmującą konflikt rzeczywisty oraz potencjalny, gdy ryzyko jest "
                "znaczne. Jest to ostrożne stanowisko komentarza SRC-01 wobec wcześniejszego brzmienia oraz bardziej "
                "kategoryczne objaśnienie poradnika SRC-03 tego samego autora; nie są to dwie niezależne opinie ani "
                "rozstrzygnięta norma. OBS-057-R01 dostarcza ogólnej definicji materialnej sprzeczności, lecz interesu "
                "klienta opisanego w OBS-015-R01/R02 nie przenoszę bez zastrzeżeń na interes radcy. OBS-018-R01/R02 "
                "oddzielają własną sprawę w art. 15 u.r.p. i tylko częściowe dookreślenie przez art. 30; nie tworzą "
                "pełnego katalogu interesu własnego. Istniejący konflikt i znaczne ryzyko pozostają oddzielnymi "
                "przesłankami lokalnego art. 30 ust. 1, a pytanie o ich relację i próg ryzyka znajduje się w "
                "OBS-057-Q01."
            ),
            "record_ids": ["OBS-057-R01", "OBS-057-R03", "OBS-018-R01", "OBS-018-R02", "SP-R08"]
        },
        {
            "id": "OBS-012-M02",
            "context": "S1-K1-06, art. 30 ust. 1 KERP, interes osoby najbliższej wobec interesu klienta",
            "description": (
                "Art. 30 ust. 1 obejmuje wprost interes osoby najbliższej radcy, nie tylko interes samego radcy. "
                "OBS-057-R03 stosuje do tej konfiguracji ten sam autorski test sprzeczności materialnej i znacznego "
                "ryzyka, a ON-R05 odtwarza zakres normy. OBS-015-R01/R02 dotyczą interesu beneficjenta pomocy i nie "
                "ustalają automatycznie treści interesu osoby najbliższej; zakres tej osoby wynika odrębnie z definicji "
                "art. 5 pkt 7 przyjętej w ON-R05. Także tutaj rzeczywisty konflikt jest odrębny od potencjalnego znacznego "
                "ryzyka. Wątpliwość interpretacyjna i brak kryteriów progu są już ujęte w OBS-057-Q01."
            ),
            "record_ids": ["ON-R05", "OBS-057-R03", "OBS-015-R01", "OBS-015-R02"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": "Oba punkty mapują do art. 30 ust. 1 i odebranego OBS-057-R03. Oddzieliłem interes radcy i osoby najbliższej od interesu klienta, nie przenosząc automatycznie jego definicji. Rozróżniłem konflikt istniejący od znacznego ryzyka i odesłałem do OBS-057-Q01 zamiast tworzyć duplikat. OBS-018 dotyczy własnej sprawy lub umowy w jej właściwym zakresie, nie pełnej definicji art. 30 ust. 1. Wynik pozostaje OCZEKUJE na odbiór Astry."
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": len(result["records"]), "questions": len(result["questions"]), "sources": len(result["coverage"])}, ensure_ascii=False))
