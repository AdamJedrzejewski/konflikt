import json
import sys
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
QUEUE_DIR = ROOT / "OBSIL" / "baza_wiedzy" / "kolejka_79"
sys.path.insert(0, str(ROOT / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka


state = kolejka.load(QUEUE_DIR)
job = kolejka.get_job(state, "OBS-003")
attempt = job["attempts"][-1]
result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-003",
    "label": "arbiter",
    "points": ["S1-K2-01"],
    "scope": (
        "Opracowano punkt S1-K2-01 przez mapowanie odebranej normy art. 27 pkt 1 "
        "i ogólnego objaśnienia udziału w sprawie. W sprawdzonych fragmentach "
        "dziewięciu źródeł nie znaleziono odrębnego wyjaśnienia, kto i na jakiej "
        "podstawie pełni rolę arbitra dla tego punktu ani jakie czynności składają "
        "się na udział w sprawie w tej roli. Wystąpienia arbitra w art. 42 ust. 5 "
        "i art. 44a KERP dotyczą innych kontekstów. Przykład mediatora z OBS-025-R02 "
        "i SP-R13 oraz pytanie OBS-025-Q01 nie są przenoszone na arbitra. Zakres "
        "źródeł długich jest częściowy; brak podstaw do nowej tezy źródłowej."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-025-R01", "OBS-025-R02", "OBS-048-R01"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "112; 776; 812; 820; 1068-1084; 1204", "notes": "Sprawdzono trafienia arbitra i ich kontekst. 112, 1068-1084 i 1204 dotyczą odmiennych kontekstów; fragment o zgodzie z w.1204 nie jest wykładnią art.27 pkt 1."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "wyszukanie trafień; 44-46", "notes": "Nie znaleziono trafienia dotyczącego arbitra. Odczytany fragment WO-131/23 dotyczy udziału w funkcji publicznej, nie roli arbitra; nie deklaruję pełnej lektury źródła."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "754-760; 776-784; 794-797", "notes": "Sprawdzono wykaz ról z art.27 pkt 1 i sąsiednie objaśnienia udziału. Brak odrębnego objaśnienia roli arbitra."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-175; 371-376; 397-403", "notes": "Art.27 pkt 1 to podstawa normatywna; art.42 ust.5 i art.44a dotyczą innych kontekstów i nie definiują arbitra dla pkt 1."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "wyszukanie trafień; 212-216", "notes": "Wzmianka o arbitrażu w kontekście wynagrodzenia i postępowania zagranicznego, nie o roli z art.27 pkt 1."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "99-110", "notes": "Sprawdzono normę art.27 pkt 1; brak szczegółowej definicji arbitra."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "77-82", "notes": "Opis WO-131/23 dotyczy funkcji publicznej, nie arbitra."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Krótki tekst przeczytany w całości; nie zawiera odrębnego objaśnienia arbitra w art.27 pkt 1."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Krótki tekst przeczytany w całości; nie zawiera odrębnego objaśnienia arbitra w art.27 pkt 1."},
    ],
    "meanings": [
        {
            "id": "OBS-003-M01",
            "context": "Udział radcy w sprawie jako arbiter, art.27 pkt 1 KERP",
            "description": (
                "Norma wymienia arbitra jako jedną z ról, w których wcześniejszy udział "
                "radcy w sprawie wyłącza udzielenie pomocy. Odebrany komentarz ujmuje "
                "udział w sprawie szeroko, lecz nie wyjaśnia szczególnej podstawy ani "
                "zakresu roli arbitra. Inne użycia słowa arbiter w art.42 ust.5 i "
                "art.44a KERP nie stanowią definicji tej przesłanki."
            ),
            "record_ids": ["OBS-025-R01", "OBS-025-R02", "OBS-048-R01"],
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-003-G01",
            "issue": "Brak odrębnych kryteriów określających rolę arbitra i wymagany zakres udziału dla art.27 pkt 1 w sprawdzonych fragmentach korpusu.",
            "needed": "Wyjaśnienie eksperta o znaczeniu roli arbitra w art.27 pkt 1, jej podstawie oraz czynnościach stanowiących udział w sprawie; z uwzględnieniem odmiennych kontekstów art.42 ust.5 i art.44a KERP.",
        }
    ],
    "questions": [
        {
            "id": "OBS-003-Q01",
            "record_ids": ["OBS-025-R01", "OBS-025-R02"],
            "understanding": "Art.27 pkt 1 wymienia udział jako arbiter, a ogólne objaśnienie udziału obejmuje różne formy rzeczywistego uczestnictwa, lecz nie podaje szczególnego testu dla arbitra.",
            "variants": "Możliwe jest rozumienie ograniczone do formalnego powierzenia rozstrzygania konkretnego sporu albo szersze ujęcie obejmujące inne funkcje związane z jego rozstrzyganiem; sprawdzone źródła nie pozwalają rozstrzygnąć zakresu.",
            "consequences": "Różne ujęcie może zmienić ocenę, czy wcześniejsza funkcja przy rozstrzyganiu sporu jest udziałem w sprawie z art.27 pkt 1. Użycia arbitra w art.42 ust.5 i art.44a dotyczą innych zagadnień.",
            "question": "Jak rozumieć rolę arbitra i udział w sprawie w art.27 pkt 1 KERP: jaka podstawa powierzenia funkcji oraz jakie czynności wchodzą w zakres tej przesłanki?",
            "needed": "Odrębne stanowisko eksperta co do art.27 pkt 1; pytanie nie dotyczy roli mediatora objętej OBS-025-Q01.",
        }
    ],
    "self_check": (
        "Nie dodano nowego rekordu, ponieważ osobna teza o arbitrze nie wynika z "
        "przeczytanych fragmentów poza normą już ujętą w OBS-025-R01 i ogólnym "
        "objaśnieniem OBS-025-R02. Zachowano rozdział kontekstu art.42 ust.5 i art.44a. "
        "Źródła długie oznaczono jako częściowo sprawdzone; status operatora pozostaje OCZEKUJE."
    ),
}

validated = kolejka.validate_result(state, job, result)
out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "validation": "OK"}, ensure_ascii=True))
