import json
import sys
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
QUEUE_DIR = ROOT / "OBSIL" / "baza_wiedzy" / "kolejka_79"
sys.path.insert(0, str(ROOT / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka


state = kolejka.load(QUEUE_DIR)
job = kolejka.get_job(state, "OBS-045")
attempt = job["attempts"][-1]
result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-045",
    "label": "przedstawiciel organu władzy publicznej",
    "points": ["S1-K2-01"],
    "scope": (
        "Mapowanie punktu S1-K2-01 do odebranych OBS-025-R01/R02 oraz OBS-035-R01/R02. "
        "SRC-03 w.798-811 zawiera równoległy katalog przedstawicieli organów i osób "
        "pełniących funkcję publiczną oraz to samo ogólne objaśnienie udziału; jest to "
        "ten sam autor co SRC-01, nie niezależne potwierdzenie. Wypowiedź nie dzieli "
        "obu kategorii na osobne testy. WO-131/23 pozostaje jednostkowym przykładem z "
        "udziałem wcześniejszego funkcjonariusza ABW, a WO-52/24 kontekstem art.26, "
        "nie wykładnią art.27 pkt 1. Wspólna luka OBS-035-G01 i pytanie OBS-035-Q01 "
        "dotyczą także przedstawiciela organu; należy je skoordynować, bez tworzenia "
        "nowej karty pytania. Długie źródła sprawdzono częściowo."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-025-R01", "OBS-025-R02", "OBS-035-R01", "OBS-035-R02"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "776; 812; 816; 820; 840", "notes": "Przywołane fragmenty z wcześniejszej lektury tego samego komentarza. W.816 podaje wspólny katalog dwóch kategorii; treść i status redakcyjny ujęte w OBS-035-R01. W.812/820 to ogólne rozumienie udziału z OBS-025-R02."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "44-50", "notes": "Wcześniej odczytano fragmenty WO-131/23 i WO-52/24. Rozdzielono stanowisko OSD i WSD w pierwszej sprawie; druga dotyczy głównie art.26 i oddzielnych spraw, nie ogólnej wykładni przedstawiciela organu z art.27 pkt 1."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "754-784; 795-811", "notes": "W.798-811 zawiera równoległy katalog i objaśnienie udziału. Porównano je z wcześniejszym fragmentem w.754-784. Ten sam autor co SRC-01, więc nie jest to niezależne potwierdzenie ani nowa teza."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-175", "notes": "Brzmienie art.27 pkt 1 już zapisane w OBS-025-R01; norma wymienia przedstawiciela organu i osobę pełniącą funkcję publiczną."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "wyszukanie trafień dotyczących art.27 pkt 1 i przedstawiciela organu", "notes": "Nie wykorzystano odrębnego objaśnienia kategorii z tego źródła; nie deklaruję pełnej lektury ustawy."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "102-104", "notes": "Powtórzenie przepisu art.27 pkt 1; zakres normy jest ujęty w OBS-025-R01."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "77-87; 203-204", "notes": "Wtórne streszczenia WO-131/23 i WO-52/24, już sprawdzone przy OBS-035. Nie traktowano ich jako niezależnego potwierdzenia ani jako odrębnej wykładni art.27 pkt 1 dla każdej funkcji publicznej."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Krótki tekst przeczytany w całości; nie dodaje kryterium przedstawiciela organu publicznego."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Krótki tekst przeczytany w całości; nie dodaje kryterium przedstawiciela organu publicznego."},
    ],
    "meanings": [
        {
            "id": "OBS-045-M01",
            "context": "Przedstawiciel organu władzy publicznej w art.27 pkt 1 KERP",
            "description": "Art.27 pkt 1 obejmuje tę rolę przy wcześniejszym udziale radcy w sprawie. Autor komentarza wspólnie z osobą pełniącą funkcję publiczną wymienia m.in. sędziów, ławników, referendarzy, asystentów sędziów, urzędników sądowych, komorników sądowych oraz urzędników państwowych i samorządowych; nie przypisuje przykładów osobno do każdej z dwóch kategorii. Wspólna granica obu kategorii i przykładowy katalog są już ujęte w OBS-035-R01.",
            "record_ids": ["OBS-025-R01", "OBS-035-R01"],
        },
        {
            "id": "OBS-045-M02",
            "context": "Zakres wcześniejszego udziału w sprawie jako przedstawiciel organu publicznego",
            "description": "Ogólne objaśnienie obejmuje faktyczne czynności przygotowawcze, techniczne, nadzorcze lub kontrolne; zastosowanie do wcześniejszej aktywności funkcjonariusza ABW w WO-131/23 zostało opisane w OBS-035-R02 jako jednostkowa ocena WSD. SRC-03 powtarza tę samą autorską wykładnię i nie stanowi drugiego niezależnego stanowiska.",
            "record_ids": ["OBS-025-R02", "OBS-035-R02"],
        },
    ],
    "records": [],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": (
        "Nie dodano nowych rekordów ani pytań: równoległy katalog SRC-03 pochodzi od "
        "tego samego autora i mapuje się na OBS-035-R01; zastosowanie WO-131/23 jest "
        "już OBS-035-R02, a wspólny zakres pytania i luki jest w OBS-035-Q01/G01. "
        "WO-52/24 pozostaje kontekstem art.26. Źródła długie oznaczono jako częściowo "
        "sprawdzone, operator pozostaje OCZEKUJE."
    ),
}

validated = kolejka.validate_result(state, job, result)
out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "validation": "OK"}, ensure_ascii=True))
