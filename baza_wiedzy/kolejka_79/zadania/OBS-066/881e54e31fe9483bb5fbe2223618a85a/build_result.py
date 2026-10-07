import json
import sys
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
QUEUE_DIR = ROOT / "OBSIL" / "baza_wiedzy" / "kolejka_79"
sys.path.insert(0, str(ROOT / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka


state = kolejka.load(QUEUE_DIR)
job = kolejka.get_job(state, "OBS-066")
attempt = job["attempts"][-1]
result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-066",
    "label": "udział w sprawie",
    "points": ["S1-K2-00", "S1-K2-01"],
    "scope": (
        "Punkt S1-K2-00 mapuje systematykę art.27 pkt 1-6 do OBS-048-R01: pkt 1-2 "
        "dotyczą udziału samego radcy lub zeznawania jako świadka, a pkt 3-6 relacji "
        "radcy z inną osobą. Zasada interpretacyjna autora o skutku wystąpienia "
        "wymienionej okoliczności i braku dalszej oceny, po spełnieniu warunków "
        "danego punktu, jest już w OBS-048-R02. Punkt S1-K2-01 mapuje szerokie "
        "objaśnienie udziału z pkt 1 do OBS-025-R02 oraz przykład zastosowania do "
        "byłego funkcjonariusza ABW do OBS-035-R02. Oddzielne, węższe znaczenie "
        "udziału w rozstrzygnięciu z pkt 3 jest w ON-R07; pytanie OBS-065-Q01 pozostaje "
        "przypisane temu punktowi. Wnioski z pkt 1 nie są przenoszone na pkt 3. "
        "Znaczenie zeznawania jako świadka o okolicznościach sprawy z pkt 2 pozostaje "
        "poza punktami tego zadania. SRC-01 i SRC-03 pochodzą od tego samego autora, "
        "więc równoległe ujęcia nie są niezależnym potwierdzeniem. Nie stwierdzono "
        "nowej tezy, pytania ani luki ponad istniejące mapowanie. Długie źródła "
        "sprawdzono w wycinkach, kompletność jest częściowa."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "OBS-025-R01",
        "OBS-025-R02",
        "OBS-035-R02",
        "OBS-048-R01",
        "OBS-048-R02",
        "ON-R03",
        "ON-R07",
    ],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "804-832", "notes": "Przeczytano otoczenie podziału pkt 1-2 i 3-6 oraz objaśnienie udziału. Tezy o systematyce, skutku przesłanek i szerokim udziale są już mapowane do OBS-048-R01/R02 i OBS-025-R02; komentarz pozostaje redakcyjny."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "44-46", "notes": "Przeczytano fragment WO-131/23 o udziale funkcjonariusza ABW w postępowaniu; zastosowanie do tego przypadku jest już w OBS-035-R02. Nie przeniesiono jego wniosków na pkt 3 ani na inne role."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "754-815", "notes": "Przeczytano wykaz pkt 1-6, katalog, ogólne objaśnienie udziału i przejście do pkt 3-6. Jest to równoległy tekst tego samego autora co SRC-01, nie odrębne potwierdzenie."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-185", "notes": "Przeczytano art.27 pkt 1-6. Tekst odróżnia udział radcy w sprawie z pkt 1, zeznawanie jako świadek z pkt 2 i udział osoby najbliższej/zależnej w rozstrzygnięciu z pkt 3. Pkt 2 nie jest tu rozwijany."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "wyszukanie odniesień do art.27 i udziału w sprawie", "notes": "W sprawdzonych trafieniach nie znaleziono dodatkowej wykładni dla wskazanych punktów; nie deklaruję pełnej lektury ustawy."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "102-110", "notes": "Sprawdzono źródłowe brzmienie art.27 pkt 1-3; nie dodaje ono wykładni poza normą i znanym rozdzieleniem punktów."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "77-82", "notes": "Wtórne streszczenie WO-131/23 o szerokim udziale funkcjonariusza w sprawie; to samo orzeczenie i przypadek co SRC-02, nie niezależne potwierdzenie."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Krótki tekst przeczytany w całości; nie zawiera nowej wykładni art.27 pkt 1-2."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Krótki tekst przeczytany w całości; nie zawiera nowej wykładni art.27 pkt 1-2."},
    ],
    "meanings": [
        {
            "id": "OBS-066-M01",
            "context": "Systematyka przesłanek udziału w art.27 pkt 1-6 KERP, S1-K2-00",
            "description": "Autor dzieli pkt 1-2 jako wcześniejszy udział samego radcy lub zeznawania jako świadka od pkt 3-6 dotyczących relacji radcy z inną osobą. Odrębnie ujmuje skutek przesłanek art.27, po spełnieniu literalnych warunków właściwego punktu. Jest to systematyka i pogląd autora, nie jedna norma zbiorcza; przyjęto już w OBS-048-R01/R02.",
            "record_ids": ["OBS-048-R01", "OBS-048-R02"],
        },
        {
            "id": "OBS-066-M02",
            "context": "Szerokie znaczenie udziału radcy w sprawie z art.27 pkt 1, S1-K2-01",
            "description": "Odebrany pogląd autora obejmuje udział bezpośredni oraz faktycznie podjęte czynności przygotowawcze, techniczne, nadzorcze i kontrolne, z wyłączeniem samych niewykorzystanych uprawnień oraz udziału w tworzeniu prawa w roli decydenta politycznego, legislatora lub lobbysty. Jednostkowe zastosowanie do byłego funkcjonariusza ABW w WO-131/23 zachowuje OBS-035-R02. Węższe znaczenie udziału w rozstrzygnięciu z pkt 3 pozostaje w ON-R03/ON-R07 i nie jest objęte tym testem.",
            "record_ids": ["OBS-025-R02", "OBS-035-R02", "ON-R03", "ON-R07"],
        },
    ],
    "records": [],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": (
        "Nie dodano nowej tezy ani pytania: oba punkty mają odebrane mapowanie w "
        "OBS-048-R01/R02, OBS-025-R02 i kartach powiązanych. Zachowano odrębność pkt 1, "
        "pkt 2 i pkt 3; OBS-065-Q01 pozostaje ograniczone do udziału w rozstrzygnięciu "
        "z pkt 3. Długie źródła oznaczono jako częściowo sprawdzone, operator pozostaje OCZEKUJE."
    ),
}

validated = kolejka.validate_result(state, job, result)
out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "validation": "OK"}, ensure_ascii=True))
