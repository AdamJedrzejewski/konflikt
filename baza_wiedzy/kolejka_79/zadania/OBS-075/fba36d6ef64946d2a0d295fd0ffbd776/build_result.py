import json
import sys
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
KANCELARIA = TASK_DIR.parents[5]
PROJECT = KANCELARIA / "OBSIL"
QUEUE_DIR = PROJECT / "baza_wiedzy" / "kolejka_79"
sys.path.insert(0, str(PROJECT / "narzedzia" / "kolejka_pojec"))
import kolejka


state = kolejka.load(QUEUE_DIR)
job = kolejka.get_job(state, "OBS-075")
attempt = job["attempts"][-1]
sources = {s["id"]: PROJECT / s["text"] for s in state["sources"]}
lines = {sid: path.read_text(encoding="utf-8-sig").splitlines() for sid, path in sources.items()}

opinion = lines["SRC-01"][875]
assessment = lines["SRC-01"][879]

result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-075",
    "label": "zeznanie",
    "points": ["S1-K2-02"],
    "scope": (
        "Uzupełniono OBS-079-R01 o zastosowanie art.27 pkt 2 w D 83/19, bez ponownego zapisu normy. "
        "W w.876 OSD przyjmuje stanowisko Obwinionego, że zakaz nie dotyczy dowolnych zeznań, lecz zeznań o okolicznościach sprawy. "
        "W w.880 wyciąg relacjonuje pozytywną ocenę zeznań o pożyczkach zaciąganych pod naciskiem władz S. oraz o zmuszaniu C.(1) do pożyczek „na słupy”. "
        "Jest to jednostkowe zastosowanie, nie wyłączny typ zeznań objętych normą. W.872 pozostawiono jako opis czynu bez ustalenia, czy to zarzut czy przypisany czyn. "
        "Zakres kryterium związku treści zeznań z okolicznościami sprawy pozostaje pytaniem wspólnym do skoordynowania z OBS-033. Oryginału D 83/19 nie ma w manifeście; długie źródła sprawdzono częściowo."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-079-R01", "OBS-079-R02", "OBS-079-R03", "OBS-025-R02"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "868-880", "notes": "D 83/19: w.872 to opis czynu bez ustalonego statusu; w.876 OSD jawnie przyjmuje pogląd Obwinionego o nieobjęciu dowolnych zeznań; w.880 fragment podaje pozytywną ocenę konkretnych zeznań. Nie przypisano w.872 statusu zarzutu ani przypisanego czynu."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "36-38", "notes": "WO-12/20 jako kontekst: wcześniejsze zeznanie i późniejsza obrona w tej samej sprawie; odrębnie opisano zastępstwo AB/TM w sprawach cywilnych oraz twierdzenia o MC. Nie uogólniono tej konfiguracji na każdą kumulację ról."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "761-762; 785-797", "notes": "Powtórzenie normy pkt 2 i autorska systematyka pkt 1-2; nie podaje dodatkowego kryterium zakresu treści zeznań. Ten sam autor co SRC-01."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-179", "notes": "Lokalne brzmienie art.27 pkt 2 w w.177 było już podstawą OBS-079-R01; nie powielono go jako nowej tezy."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "wyszukiwanie: świadek/zeznania; 1525", "notes": "Trafienie dotyczy sankcji procesowej za niestawiennictwo lub odmowę zeznań, nie wykładni art.27 pkt 2; nie deklaruję pełnej lektury ustawy."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "101-106", "notes": "Zestawienie powtarza tekst normatywny pkt 2; nie zawiera osobnego objaśnienia granicy treści zeznań."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "65-69; 201", "notes": "Wtórne omówienie WO-12/20; dotyczy innego wyboru orzeczenia, nie D 83/19, i nie stanowi niezależnego potwierdzenia."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały krótki plik przeczytany; dotyczy tożsamości i związku spraw, nie zakresu wcześniejszych zeznań z art.27 pkt 2."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Cały krótki plik przeczytany; dotyczy klienta i czasu relacji, nie zakresu wcześniejszych zeznań z art.27 pkt 2."},
    ],
    "meanings": [
        {
            "id": "OBS-075-M01",
            "context": "Granica art.27 pkt 2: wcześniejsze zeznania o okolicznościach sprawy",
            "description": "OBS-079-R01 zawiera tekst normy. W D 83/19 OSD wyraźnie popiera stanowisko Obwinionego, że nie każde zeznanie świadka uruchamia zakaz, lecz zeznania dotyczące okoliczności sprawy. Dostępny fragment nie daje abstrakcyjnego testu takiego związku.",
            "record_ids": ["OBS-075-R01"],
        },
        {
            "id": "OBS-075-M02",
            "context": "Jednostkowa ocena treści zeznań w D 83/19",
            "description": "Wyciąg z D 83/19 relacjonuje pozytywną ocenę zeznań Obwinionego opisujących pożyczki zaciągane pod naciskiem władz S. i zmuszanie C.(1) do zaciągania pożyczek „na słupy”. Jest to przykład zastosowania kryterium w konkretnej sprawie, nie definicja wyczerpująca.",
            "record_ids": ["OBS-075-R02"],
        },
    ],
    "records": [
        {
            "id": "OBS-075-R01",
            "kind": "zastosowanie_osd",
            "claim": "W wyciągu z D 83/19 OSD uznaje za trafne stanowisko Obwinionego, że art.27 pkt 2 nie zakazuje pomocy po złożeniu dowolnych zeznań świadka, lecz obejmuje zeznania dotyczące okoliczności sprawy.",
            "speaker": "OSD, wprost popierający argument Obwinionego",
            "role": "organ dyscyplinarny rozpoznający sprawę D 83/19, według wybranego fragmentu komentarza",
            "context": "Wyjaśnienie treści przesłanki art.27 pkt 2 w odniesieniu do wcześniej przesłuchanego świadka; uzupełnia normę OBS-079-R01 i nie powiela jej tekstu.",
            "court_treatment": "Sformułowanie „Rację ma Obwiniony wskazując” wyraźnie pokazuje przyjęcie tego argumentu w przytoczonym fragmencie. Brak pełnego oryginału uniemożliwia ustalenie pełnego kontekstu i sentencji.",
            "source_status": "Wybór fragmentów komentarza z lustra SRC-01, nie oryginał decyzji D 83/19; autorstwo oceny przypisano OSD tylko w zakresie wprost przytoczonym.",
            "evidence": [{"source_id": "SRC-01", "line_start": 876, "line_end": 876, "quote": opinion}],
            "limits": "Fragment odróżnia dowolne zeznania od zeznań o okolicznościach sprawy, ale nie wyznacza kompletnego ani wyłącznego testu relewancji. Nie wynika z niego, że tylko bezpośrednie zeznania o określonym rodzaju faktów podlegają normie.",
        },
        {
            "id": "OBS-075-R02",
            "kind": "zastosowanie_osd",
            "claim": "Wyciąg D 83/19 podaje, że ocena zeznań Obwinionego doprowadziła do pozytywnych ustaleń w zakresie okoliczności sprawy; jako treść zeznań wskazuje informacje o pożyczkach zaciąganych pod naciskiem władz S. oraz zmuszaniu C.(1) do pożyczek „na słupy”.",
            "speaker": "OSD według relacji w wybranym fragmencie komentarza",
            "role": "organ dyscyplinarny, którego ocenę zeznań przytacza fragment dotyczący D 83/19",
            "context": "Konkretny przykład treści uznanej w przytoczonym rozumowaniu za dotyczącą okoliczności sprawy; odrębny od ogólnego argumentu o nieobjęciu dowolnych zeznań.",
            "court_treatment": "W.880 mówi o pozytywnych ustaleniach na podstawie oceny zeznań. Nie wywodzę z tego pełnej sentencji, prawomocności ani katalogu wyłącznych typów zeznań.",
            "source_status": "Wybrany fragment komentarza SRC-01 opisujący D 83/19; oryginalnego rozstrzygnięcia nie ma w manifeście.",
            "evidence": [{"source_id": "SRC-01", "line_start": 880, "line_end": 880, "quote": assessment}],
            "limits": "Jednostkowa ilustracja, nie reguła że każdy przypadek pożyczki, nacisku lub zeznań o faktach gospodarczych spełnia przesłankę. Nie przesądza też, że podobny rodzaj informacji jest wymagany w innych sprawach.",
        },
    ],
    "relations": [
        {"from": "OBS-075-R01", "relation": "uzupelnia_norme_i_poprzednie_zastosowanie", "to": "OBS-079-R01", "status": "KANDYDAT", "record_ids": ["OBS-075-R01"]},
        {"from": "OBS-075-R02", "relation": "ilustruje_jednostkowe_zastosowanie", "to": "OBS-075-R01", "status": "KANDYDAT", "record_ids": ["OBS-075-R02"]},
    ],
    "gaps": [
        {
            "id": "OBS-075-G01",
            "issue": "Oryginał decyzji D 83/19 nie znajduje się w manifeście; dostępne są wybrane fragmenty lustra komentarza. W.872 pozostaje opisem czynu bez ustalonej atrybucji lub statusu.",
            "needed": "Oryginał, jeśli potrzebna będzie weryfikacja pełnego uzasadnienia, dokładnej atrybucji zdań i sentencji. Pytanie eksperckie o zakres art.27 pkt 2 jest odrębną luką interpretacyjną.",
        }
    ],
    "questions": [
        {
            "id": "OBS-075-Q01",
            "record_ids": ["OBS-075-R01", "OBS-075-R02"],
            "understanding": "Z tekstu normy OBS-079-R01 i przyjętego poglądu w D 83/19 wynika, że nie wystarcza samo dowolne wcześniejsze zeznawanie. W.880 pokazuje jako przykład zeznania o pożyczkach i naciskach w opisywanej sprawie, ale materiał nie formułuje testu ogólnego.",
            "variants": "Źródła nie przedstawiają zamkniętych wariantów. Do rozstrzygnięcia pozostaje, jakiego związku treści zeznań z okolicznościami sprawy wymaga pkt 2; przykład z D 83/19 nie powinien być traktowany jako wyłączny typ.",
            "consequences": "Kryterium wyznaczy granicę między każdym wcześniejszym zeznaniem a zeznaniami mającymi relewantny związek z daną sprawą, bez automatycznego ograniczenia do treści podobnej do przykładu D 83/19.",
            "question": "Jak ustalać, czy wcześniejsze zeznania świadka dotyczyły „okoliczności sprawy” w rozumieniu art.27 pkt 2? Czy przykład D 83/19 ilustruje jedynie zastosowanie do konkretnej sprawy, a jeśli tak, jakie kryterium pozwala objąć lub wyłączyć inne rodzaje zeznań? Prosimy skoordynować odpowiedź z OBS-033, jeśli dotyczy tego samego zakresu.",
            "needed": "Stanowisko eksperta co do zakresu pojęcia. Oryginał D 83/19 należy pozyskać osobno, jeżeli odpowiedź ma opierać się na pełnym uzasadnieniu, a nie tylko przytoczonym fragmencie.",
        }
    ],
    "self_check": "Nie skopiowano normy z OBS-079-R01 ani zastosowania z D 33/18. W D 83/19 oddzielono przyjęty przez OSD argument Obwinionego w w.876 od oceny zeznań przytoczonej w w.880. W.872 opisano bez dopisywania statusu zarzutu lub ustalenia. Nie wywiedziono wyłącznego katalogu treści zeznań; pytanie o zakres oznaczono do skoordynowania z OBS-033. Cytaty pobrano bezpośrednio z wierszy lustra SRC-01. Oryginał D 83/19 pozostaje nieobecny; status operatora OCZEKUJE.",
}

validated = kolejka.validate_result(state, job, result)
out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "validation": "OK"}, ensure_ascii=True))
