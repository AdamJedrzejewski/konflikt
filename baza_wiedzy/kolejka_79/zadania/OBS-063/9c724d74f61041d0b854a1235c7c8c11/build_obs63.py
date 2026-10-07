import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka

state = kolejka.load(ROOT / "OBSIL" / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, "OBS-063")
attempt = job["attempts"][-1]

result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-063",
    "label": "ten sam czas",
    "points": ["S1-K2-04"],
    "scope": (
        "Zakres obejmuje wyłącznie warunek z art. 27 pkt 4, że radca i osoba, z którą może wspólnie wykonywać zawód, wykonują czynności zawodowe „w tym samym czasie na rzecz tego samego klienta”. Pełna norma pozostaje w OBS-008-R01. OBS-008-Q01 dotyczy przede wszystkim tego, jakie działania są czynnościami zawodowymi; niniejsze pytanie dotyczy temporalnego znaczenia równoczesności. Przejrzane źródła przytaczają warunek, ale nie określają, czy miarodajne jest faktyczne nakładanie się okresów wykonywania czynności, czy trwanie zleceń, umocowania lub innej relacji. Nie utożsamiam czasu wykonywania czynności z formalnym zatrudnieniem, pełnomocnictwem, aktualnością klienta ani trwaniem relacji osobistej. Odrębne opisy wymogu równoczesności w art. 28 ust. 2, w tym SRC-01 w. 1044 i SRC-02 w. 84, nie są przenoszone na pkt 4. Zakres częściowy, oparty na wycinkach źródeł."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-008-R01"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "780-820; 1040-1046", "notes": "Nowe lustro. Sprawdzono tekst pkt 4 i kontekst komentarza oraz osobno przykład odnoszący równoczesność do art. 28 ust. 2. Autor w przejrzanym wycinku nie definiuje temporalnego testu art. 27 pkt 4; przykład z art. 28 ust. 2 nie jest użyty jako odpowiedź."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "80-89; wyszukanie „tym samym czasie” w 1-112", "notes": "W małym bloku przejrzano WO–17/24 dotyczące reprezentowania klientów przy art. 28 ust. 1. Opisuje inny punkt i nie jest podstawą do wykładni pkt 4. Reszty wyboru nie czytano w całości."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "762-784", "notes": "Sprawdzono listę przypadków art. 27 i objaśnienie ogólne. Fragment powtarza wymóg równoczesnego wykonywania czynności w pkt 4, bez kryteriów ustalania okresu. Ten sam autor co SRC-01."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-185", "notes": "Sprawdzono art. 27 pkt 1-6 w lokalnym tekście KERP, w tym pkt 4. Przepis nie rozwija temporalnego znaczenia warunku."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "105-131; 161-173", "notes": "Sprawdzono art. 8-9 oraz art. 14-18 u.r.p. Materiał opisuje formy wykonywania zawodu, zatrudnienie i samodzielność, lecz nie definiuje czasu czynności z art. 27 pkt 4. Nie utożsamiono statusu zatrudnienia z równoczesnością."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "99-114", "notes": "Sprawdzono zbiorcze brzmienie art. 27. Zestawienie nie podaje odrębnych kryteriów czasu."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "61-87", "notes": "Sprawdzono przykłady z art. 27 pkt 1 oraz art. 28. Nie odnoszą się do równoczesności czynności z pkt 4 i nie zostały przeniesione na ten punkt."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Przeczytano cały krótki słownik sprawy tej samej lub związanej. Nie definiuje warunku czasu z art. 27 pkt 4."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Przeczytano cały krótki słownik klienta aktualnego i byłego. Status relacji klienta nie rozstrzyga temporalnego warunku czynności z pkt 4."}
    ],
    "meanings": [
        {
            "id": "OBS-063-M01",
            "context": "Warunek temporalny bezwzględnego wyłączenia z art. 27 pkt 4 KERP.",
            "description": "Norma wymaga, by radca i osoba uprawniona do wspólnego wykonywania z nim zawodu wykonywali czynności zawodowe w tym samym czasie na rzecz tego samego klienta. OBS-008-R01 ujmuje całą przesłankę. Przejrzane źródła nie wyjaśniają, czy „ten sam czas” oznacza nakładanie się okresów faktycznego wykonywania czynności, czy także równoległe trwanie zleceń lub umocowań mimo braku jednoczesnych czynności. Wymóg nie został utożsamiony z samym formalnym zatrudnieniem lub statusem klienta. Przykłady odnoszące równoczesność do art. 28 ust. 2 mają inny kontekst normatywny.",
            "record_ids": ["OBS-008-R01"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-063-G01",
            "issue": "Lokalny tekst KERP wymaga, by czynności zawodowe były wykonywane w tym samym czasie, lecz przejrzane materiały nie wyznaczają, jak ustalić nakładanie się okresów ani czy wystarcza równoległe trwanie zleceń lub umocowań. Nie należy zastępować tego warunku statusem zatrudnienia, klienta lub relacji osobistej.",
            "needed": "Bezpośrednia wykładnia art. 27 pkt 4, która określi, do jakiego odcinka czasu odnosi się równoczesność czynności obu osób oraz czy i w jakich granicach znaczenie ma trwanie zlecenia, umocowania lub współpracy."
        }
    ],
    "questions": [
        {
            "id": "OBS-063-Q01",
            "record_ids": ["OBS-008-R01"],
            "understanding": "Art. 27 pkt 4 posługuje się wymogiem wykonywania czynności zawodowych w tym samym czasie na rzecz tego samego klienta. OBS-008-Q01 pyta o rodzaj czynności; obecna karta wyodrębnia nierozstrzygnięty zakres temporalny tego warunku.",
            "variants": "Do ustalenia pozostaje, czy wymóg odnosi się do rzeczywistego nakładania się okresów wykonywania czynności przez obie osoby, czy także do równoległego trwania zleceń lub umocowań, mimo że konkretne czynności są wykonywane w różnych momentach. To warianty do konsultacji, nie stanowiska przypisane źródłom.",
            "consequences": "Kryterium określi, jakie daty i fakty trzeba ustalać dla każdej osoby. Utożsamienie równoczesności z samym zatrudnieniem lub trwaniem pełnomocnictwa mogłoby objąć okres bez równoczesnych czynności, a wymóg ścisłej jednoczesności konkretnych działań może wymagać dokładniejszego ustalenia harmonogramu prac.",
            "question": "Jak wyznaczać „ten sam czas” w art. 27 pkt 4: czy wymagane jest faktyczne nakładanie się okresów wykonywania czynności zawodowych obu osób na rzecz tego samego klienta, czy wystarcza równoległe trwanie zleceń, umocowań lub współpracy, nawet gdy konkretne czynności przypadają na różne momenty? Jak traktować czynności wykonywane okresowo lub etapami?",
            "needed": "Wykładnia temporalnego warunku art. 27 pkt 4, odrębna od zakresu czynności zawodowych podniesionego w OBS-008-Q01. Nie przenosić wymogu art. 28 ust. 2 jako odpowiedzi bez podstawy odnoszącej się do pkt 4."
        }
    ],
    "self_check": "Nie dodano nowego rekordu, ponieważ pełne brzmienie art. 27 pkt 4 jest już ujęte w OBS-008-R01. Jedno pytanie ograniczono do temporalnego znaczenia równoczesności; nie powiela ono pytania o rodzaj czynności zawodowych. Rozdzielono czas wykonywania czynności od zatrudnienia, umocowania i aktualności relacji. Nie przeniesiono przykładów art. 28 ust. 2. Długie źródła zbadano w wycinkach i oznaczono jako częściowe, a operator pozostaje OCZEKUJE."
}

validated = kolejka.validate_result(state, job, result)
target = TASK_DIR / "wynik.json"
target.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"OK: {target}")
