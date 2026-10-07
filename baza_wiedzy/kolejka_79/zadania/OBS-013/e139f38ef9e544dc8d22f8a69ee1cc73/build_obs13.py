import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
previous = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-015" / "2811056334224caa8e3194d41df5b1ca" / "wynik.json"
previous_result = json.loads(previous.read_text(encoding="utf-8"))
coverage = previous_result["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["notes"] += " Dla relacji z osobą uprzednio obsługiwaną wykorzystuję osobno odebrany SP-R06 z jego historycznym manifestem; nie przenoszę numeracji do obecnego lustra."
    elif item["source_id"] == "SRC-04":
        item["read_ranges"] = "63-75; 187-203"
        item["notes"] = "Art. 6-9 KERP oraz lokalny tekst art. 28-29 przeczytane w kontekście; art. 28 ust. 3 i art. 29 ust. 1 pkt 2 odróżniają reprezentację/obronę od doradzania. Aktualności kopii nie weryfikowano."

result = {
    "task_id": "e139f38ef9e544dc8d22f8a69ee1cc73",
    "concept_id": "OBS-013",
    "label": "interes aktualnego klienta",
    "points": ["S2-K4-03", "S2-K4-06"],
    "scope": (
        "Mapuję S2-K4-03 na reprezentację lub obronę z art. 28 ust. 3, a S2-K4-06 na doradzanie z art. 29 ust. 1 pkt 2 "
        "w konflikcie interesów aktualnego klienta z osobą, na rzecz której radca uprzednio wykonywał czynności zawodowe. "
        "Treść interesu odsyła do OBS-015-R01/R02 i OBS-057-R01; jego materialna sprzeczność pozostaje odrębnym warunkiem "
        "z OBS-057-R02. Nie wyprowadzam aktualności relacji z samego interesu: KL-R04 ogranicza dawny kontekst art. 28 ust. 3, "
        "a OBS-007-R02 rozdziela czas tajemnicy od statusu klienta. Nie przenoszę na byłego klienta zakazu z art. 28 ust. 2, "
        "który dotyczy przeciwnika będącego również klientem radcy. Przy doradzaniu zachowuję art. 29 ust. 2, zgodę klienta lub "
        "klientów oraz osób uprzednio obsługiwanych i wyjątek, gdy radca jest lub był obrońcą w sprawie karnej co najmniej "
        "jednego z nich (SP-R07); rozbieżność komentarzowego odesłania pozostaje w OBS-007-R01/Q01. Nie tworzę nowych rekordów "
        "ani pytań: interes pozaprawny jest w OBS-015-Q01, materialna sprzeczność i art. 30 w OBS-057-Q01, a koniec relacji "
        "w KL-G02/OBS-002-Q01. Coverage dziewięciu źródeł przejęto z rzeczywistej lektury OBS-015 i uzupełniono o istniejące "
        "źródłowe odniesienia KL/SP; opracowanie pozostaje częściowe."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "KL-R01", "KL-R04", "SP-R06", "SP-R07", "OBS-015-R01", "OBS-015-R02", "OBS-015-R03",
        "OBS-057-R01", "OBS-057-R02", "OBS-007-R01", "OBS-007-R02"
    ],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-013-M01",
            "context": "S2-K4-03, art. 28 ust. 3 KERP, reprezentacja lub obrona wobec interesów osoby uprzednio obsługiwanej",
            "description": (
                "Interes aktualnego klienta w tej konfiguracji jest celem ochrony prawnej pomocy prawnej (OBS-015-R01) "
                "i w autorskim ujęciu obejmuje dążenie do korzystnej sytuacji klienta, z granicami prawa, etyki i "
                "niezależności (OBS-015-R02/R03). Jeżeli zastosowanie ma art. 28 ust. 3, SP-R06 wymaga ustalenia "
                "sprzeczności interesów aktualnego klienta z interesami osoby wcześniej obsługiwanej oraz związku lub "
                "tożsamości spraw. OBS-057-R01/R02 rozdzielają treść interesu od oceny materialnej sprzeczności. "
                "KL-R04 opisuje wcześniejsze czynności w tej samej lub związanej sprawie, ale nie wyznacza daty końca "
                "każdej relacji. OBS-007-R02 stwierdza, że trwanie tajemnicy nie przesądza statusu klienta. Nie stosuję "
                "tu art. 28 ust. 2, który dotyczy innej konfiguracji aktualnych klientów będących procesowymi przeciwnikami."
            ),
            "record_ids": ["OBS-015-R01", "OBS-015-R02", "OBS-015-R03", "OBS-057-R01", "OBS-057-R02", "SP-R06", "KL-R04", "OBS-007-R02"]
        },
        {
            "id": "OBS-013-M02",
            "context": "S2-K4-06, art. 29 ust. 1 pkt 2 KERP, doradzanie aktualnemu klientowi w konflikcie z osobą uprzednio obsługiwaną",
            "description": (
                "Art. 29 ust. 1 pkt 2 odnosi zakaz doradzania do sprzeczności interesów klienta z interesami osoby, "
                "na rzecz której radca uprzednio wykonywał czynności zawodowe, w tej samej lub związanej sprawie. "
                "SP-R07 zachowuje wyjątek zgody z ust. 2: potrzebna jest zgoda klienta lub klientów oraz osób uprzednio "
                "obsługiwanych; radca nie może jej uzyskać, gdy jest lub był obrońcą w sprawie karnej co najmniej jednego "
                "z nich. Lokalny tekst KERP ma pkt 2 dla byłej obsługi; odsyłacz komentarza do pkt 1 i pytanie o jego "
                "zamierzoną podstawę pozostają w OBS-007-R01/Q01. Treść interesu i próg sprzeczności nie zastępują "
                "odrębnego ustalenia, kto jest aktualnym lub uprzednio obsługiwanym klientem."
            ),
            "record_ids": ["SP-R07", "OBS-007-R01", "OBS-015-R01", "OBS-015-R02", "OBS-057-R02"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": "Dwa punkty mapują się do art. 28 ust. 3 i art. 29 ust. 1 pkt 2. Oddzielono cel ochrony interesu, ustalenie sprzeczności, wcześniejszą obsługę i aktualność relacji. Zachowano warunki zgody oraz wyjątek obrońcy z art. 29 ust. 2; nie zastosowano art. 28 ust. 2 do byłego klienta. Istniejące pytania OBS-015-Q01, OBS-057-Q01, OBS-007-Q01 i OBS-002-Q01 wskazano zamiast ich duplikowania. Wynik pozostaje OCZEKUJE na odbiór Astry."
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": len(result["records"]), "questions": len(result["questions"]), "sources": len(result["coverage"])}, ensure_ascii=False))
