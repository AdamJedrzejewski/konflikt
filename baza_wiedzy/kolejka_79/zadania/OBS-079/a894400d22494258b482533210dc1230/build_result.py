import json
import sys
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
QUEUE_DIR = ROOT / "OBSIL" / "baza_wiedzy" / "kolejka_79"
PROJECT = ROOT / "OBSIL"
sys.path.insert(0, str(ROOT / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka


state = kolejka.load(QUEUE_DIR)
job = kolejka.get_job(state, "OBS-079")
attempt = job["attempts"][-1]
source_paths = {s["id"]: PROJECT / s["text"] for s in state["sources"]}
source_lines = {
    source_id: path.read_text(encoding="utf-8-sig").splitlines()
    for source_id, path in source_paths.items()
}

quote_norm = source_lines["SRC-04"][176]
quote_case_title = source_lines["SRC-01"][855]
quote_skarzacy = source_lines["SRC-01"][859]
quote_osd = source_lines["SRC-01"][863]

result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-079",
    "label": "świadek",
    "points": ["S1-K2-02"],
    "scope": (
        "Opracowano normę art.27 pkt 2 i odrębne zastosowanie opisane w D 33/18. "
        "Norma wymaga uprzedniego zeznawania jako świadek w sprawie o okolicznościach "
        "sprawy. W D 33/18 oddzielono relację Skarżącego P.(2) w SRC-01 w.860 od "
        "wyraźnej oceny OSD w w.864; fragment nie potwierdza prawomocności ani pełnej "
        "sentencji. D 83/19 w.876-880 rozważa, że nie dowolne zeznania są objęte "
        "przesłanką, i pozytywnie ocenia opis pożyczek oraz nacisków; szczegółowy test "
        "treści zeznań i okoliczności sprawy pozostaje do właściwych kart OBS-075/033, "
        "bez powielania tu pytania. WO-12/20 zawiera złożony układ: wcześniejsze "
        "świadectwo i późniejszą obronę w tej samej sprawie oraz równoległe sprawy "
        "cywilne, w których występowali AB/TM, oraz twierdzenia dotyczące MC; wycinek nie ustala, że MC był ich przeciwnikiem procesowym. Nie sprowadzam go do zakazu każdej kumulacji ról. "
        "Brak oryginałów decyzji odnotowano osobno od pytań eksperckich. Długie źródła "
        "sprawdzono częściowo."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "856-880", "notes": "Przeczytano D 33/18 i D 83/19 w kontekście. W D 33/18 w.860 to relacja Skarżącego, w.864 wyraźna ocena OSD przewinienia. W D 83/19 w.872 opis czynu, bez ustalenia w tym wycinku, czy jest to zarzut czy przypisany czyn; w.876-880 stanowisko OSD i ocena konkretnych zeznań. Szczegółowy test pozostaje w zakresie OBS-075/033."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "36-38", "notes": "WO-12/20: wcześniejsze zeznawanie i późniejsza obrona w tej samej sprawie; obok opisano odrębne postępowania cywilne, w których występowali AB/TM, oraz twierdzenia dotyczące MC. Wycinek nie ustala, że MC był ich przeciwnikiem procesowym. Nie generalizuję tego wielowątkowego fragmentu na zakaz każdej kumulacji ról."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "761-762; 785-797", "notes": "W.761-762 powtarza treść pkt 2, a w.785-797 umieszcza świadka w autorskim podziale pkt 1-2; nie dodaje odrębnego testu. To ten sam autor co SRC-01."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-179", "notes": "Przeczytano art.27 pkt 1-3. W.177 zawiera lokalne brzmienie pkt 2 z warunkiem uprzedniego zeznawania jako świadka o okolicznościach sprawy."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "wyszukanie trafień dla świadka i zeznań; 1524-1527", "notes": "Trafienia w ustawie dotyczą innych reguł i sankcji procesowych, nie objaśniają art.27 pkt 2. Nie deklaruję pełnej lektury ustawy."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "102-106", "notes": "Tekst źródłowy powtarza art.27 pkt 2 i warunek zeznawania o okolicznościach sprawy; brak dalszego objaśnienia."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "65-69; 201", "notes": "Wtórne streszczenie WO-12/20 jako art.27 pkt 2; porównano z fragmentem SRC-02, nie traktowano jako niezależnego potwierdzenia."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Krótki tekst przeczytany w całości; nie zawiera wykładni pkt 2."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Krótki tekst przeczytany w całości; nie zawiera wykładni pkt 2."},
    ],
    "meanings": [
        {
            "id": "OBS-079-M01",
            "context": "Przesłanka wcześniejszego zeznawania jako świadka, art.27 pkt 2 KERP",
            "description": "Norma wymaga łącznie, aby radca uprzednio zeznawał jako świadek w sprawie o okolicznościach sprawy. Sam status świadka lub dowolne zeznanie nie wynika z tekstu jako wystarczające; zakres znaczenia okoliczności sprawy pozostaje do odrębnej analizy.",
            "record_ids": ["OBS-079-R01"],
        },
        {
            "id": "OBS-079-M02",
            "context": "Zastosowanie pkt 2 do zeznań J. przed późniejszą reprezentacją córki w sprawie rozwodowej, D 33/18",
            "description": "Skarżący opisał wcześniejsze zeznania radcy J. w sprawie rozwodowej, a OSD wyraźnie ocenił późniejsze przyjęcie pełnomocnictwa i reprezentację córki przeciw P.(2) po zeznawaniu o okolicznościach tej samej sprawy jako przewinienie dyscyplinarne. Relacja strony i ocena OSD są zachowane osobno.",
            "record_ids": ["OBS-079-R02", "OBS-079-R03"],
        },
    ],
    "records": [
        {
            "id": "OBS-079-R01",
            "kind": "przepis",
            "claim": "Art.27 pkt 2 KERP zakazuje udzielenia pomocy prawnej, jeżeli radca uprzednio zeznawał jako świadek w sprawie o okolicznościach sprawy.",
            "speaker": "KERP w lokalnym tekście źródłowym",
            "role": "tekst przepisu",
            "context": "Samodzielna przesłanka pkt 2 art.27, odrębna od wcześniejszego udziału w wymienionej roli z pkt 1 oraz od relacji innej osoby z pkt 3-6.",
            "court_treatment": "Nie dotyczy; cytat jest tekstem normatywnym z lokalnej kopii.",
            "source_status": "Lokalna kopia KERP w manifeście; aktualności prawa nie ustalano.",
            "evidence": [{"source_id": "SRC-04", "line_start": 177, "line_end": 177, "quote": quote_norm}],
            "limits": "Sam przepis nie definiuje progu ani szczegółowego zakresu zwrotu o okolicznościach sprawy, ani pełnej relacji czasowej poza słowem uprzednio. Nie rozszerzam przesłanki na dowolne zeznania.",
        },
        {
            "id": "OBS-079-R02",
            "kind": "twierdzenie_strony",
            "claim": "W opisie D 33/18 Skarżący P.(2) podał, że radca J. zeznawała jako świadek w jego sprawie rozwodowej, a po złożeniu zeznań wnioskowała o ustanowienie jej pełnomocnikiem córki w dalszym postępowaniu.",
            "speaker": "Skarżący P.(2), według relacji zamieszczonej w wyborze",
            "role": "uczestnik składający twierdzenie w sprawie dyscyplinarnej",
            "context": "Fragment redakcyjny poprzedzający ocenę OSD w D 33/18.",
            "court_treatment": "Jest to wyraźnie przypisana relacja Skarżącego, nie samodzielne ustalenie sądu ani rozstrzygnięcie.",
            "source_status": "Wybór fragmentów materiału OSD D 33/18 w lustrze komentarza redakcyjnego; oryginału decyzji nie ma w manifeście.",
            "evidence": [
                {"source_id": "SRC-01", "line_start": 856, "line_end": 856, "quote": quote_case_title},
                {"source_id": "SRC-01", "line_start": 860, "line_end": 860, "quote": quote_skarzacy},
            ],
            "limits": "To relacja Skarżącego P.(2) przedstawiona w wyborze, nie ustalenie, że wszystkie opisane szczegóły zostały uznane za prawomocne fakty. Fragment nie ujawnia pełnego przebiegu ani rozstrzygnięcia sprawy.",
        },
        {
            "id": "OBS-079-R03",
            "kind": "zastosowanie_osd",
            "claim": "W D 33/18 OSD wyraźnie ocenił jako przewinienie dyscyplinarne przyjęcie pełnomocnictwa i reprezentowanie córki P.(1) przeciw P.(2) w tej samej sprawie rozwodowej, po wcześniejszym zeznawaniu przez radcę J. jako świadka o okolicznościach sprawy.",
            "speaker": "OSD, ocena wyraźnie wprowadzona słowami „W ocenie OSD”",
            "role": "organ dyscyplinarny pierwszej instancji w sprawie D 33/18",
            "context": "Fragment oceny OSD w odniesieniu do zarzutu przedstawionego w wyborze; wiersz 860 osobno relacjonuje stanowisko Skarżącego P.(2).",
            "court_treatment": "Źródło podaje ocenę OSD przewinienia, ale nie pełną sentencję ani informację o prawomocności. Nie przypisuję tego stanowiska WSD.",
            "source_status": "Lustro komentarza redakcyjnego z fragmentem decyzji OSD D 33/18; status redakcyjnego wyboru i brak oryginału ograniczają weryfikację.",
            "evidence": [{"source_id": "SRC-01", "line_start": 864, "line_end": 864, "quote": quote_osd}],
            "limits": "Jednostkowa ocena OSD, nie pełny test zakresu zeznań z pkt 2. Nie potwierdza prawomocności ani końcowego rozstrzygnięcia; szczegółowy próg „okoliczności sprawy” pozostaje poza tym rekordem.",
        },
    ],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-079-G01",
            "issue": "Korpus zawiera wybrane fragmenty D 33/18, D 83/19 i WO-12/20 oraz wtórne streszczenie WO-12/20, nie pełne oryginały decyzji.",
            "needed": "Oryginalne rozstrzygnięcia, jeśli odbiór wymaga weryfikacji pełnego uzasadnienia, sentencji i dalszego statusu orzeczeń; brak ten jest źródłowy i nie zastępuje pytania eksperckiego o wykładnię pkt 2.",
        }
    ],
    "questions": [],
    "self_check": (
        "Normę pkt 2 odróżniono od dwóch głosów w D 33/18: relacji Skarżącego i "
        "wyraźnej oceny OSD. Nie przypisano ocenie OSD prawomocności. D 83/19 i WO-12/20 "
        "odnotowano jako materiał dla szczegółowych kart testu i odrębnych ról; nie "
        "wyprowadzono ogólnego zakazu każdej kumulacji. Brak oryginałów zapisano jako gap, "
        "bez dodawania pytania eksperckiego. Status operatora pozostaje OCZEKUJE."
    ),
}

validated = kolejka.validate_result(state, job, result)
out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "validation": "OK"}, ensure_ascii=True))
