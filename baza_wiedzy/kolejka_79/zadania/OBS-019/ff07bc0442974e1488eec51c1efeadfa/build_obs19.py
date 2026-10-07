import json
from pathlib import Path

root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
task_dir = Path(__file__).parent
job_data = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
src04 = next(s for s in job_data["sources"] if s["id"] == "SRC-04")
source_lines = (root / src04["text"]).read_text(encoding="utf-8-sig").splitlines()
quote_line = 191
quote = source_lines[quote_line - 1]

result = {
    "task_id": "ff07bc0442974e1488eec51c1efeadfa",
    "concept_id": "OBS-019",
    "label": "jakakolwiek sprawa",
    "points": ["S2-K3-02", "S3-K6-03"],
    "scope": "Mapuję S2-K3-02 i S3-K6-03 na tekst art. 28 ust. 2 oraz oddzielam go od art. 28 ust. 1 i 3. Dodaję jedną tezę normatywną z lokalnego tekstu KERP, ponieważ SP-R05 jest poglądem autora o zakresie tego sformułowania, a nie samym tekstem normy. Według autora „jakakolwiek sprawa” obejmuje też sprawy różne i niepowiązane, przy czym jego objaśnienie mówi o przeciwnikach procesowych. Nie przenoszę tego reżimu na byłych klientów ani na doradztwo: wykładnię o doradzaniu zawiera osobno OBS-076-R06 i pytanie OBS-076-Q03. Przy art. 26a ust. 2 art. 28 ust. 2 jest wyłączeniem od kancelaryjnej ścieżki zarządzania konfliktem, OBS-076-R04. Karta jest częściowa: korzysta z lokalnego tekstu i wtórnych opracowań, bez weryfikacji aktualności prawa ani oryginałów orzeczeń.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "SP-R04", "SP-R05", "SP-R06", "SP-R07", "OBS-076-R04", "OBS-076-R06"
    ],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "918-920, 964-988", "notes": "Autor wyraźnie rozróżnia zwroty z art. 28 ust. 1-3, następnie omawia szczególny zakres ust. 2 i odrębną wątpliwość dotyczącą doradztwa. Zachowano status komentarza roboczego z redakcyjnymi zmianami."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "82-85", "notes": "Relacjonowany przykład jednoczesnej reprezentacji wierzyciela i dłużnika z art. 28 ust. 1-2; dotyczy przeciwstawnych ról w jednej sprawie, nie samodzielnie znaczenia zwrotu jakakolwiek sprawa."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "841-870", "notes": "Opracowanie rozróżnia art. 28 ust. 1 i 2 oraz omawia sprawy niepowiązane; to ten sam autor co SRC-01, więc nie liczę go jako niezależnego potwierdzenia."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "169-171, 189-203", "notes": "Lokalny tekst art. 26a i art. 28-29. Brzmienie art. 28 ust. 2 cytowane w nowym rekordzie; aktualności lokalnej kopii nie weryfikowano."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "95-98", "notes": "Wybrane rodzaje pomocy prawnej z art. 6 u.r.p. jako kontekst odróżnienia reprezentacji od doradztwa; nie wywodzę z nich rozszerzenia art. 28 ust. 2."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "123-127, 167-179, 299-303", "notes": "Pomocnicze zestawienie tekstu i konfiguracji art. 28 ust. 2 oraz jego wyłączenia w art. 26a; nie zastępuje lokalnego KERP."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "149-154", "notes": "Wtórne opracowanie relacji sprawy WO-42/24 o przeciwnikach procesowych w różnych sprawach; nie zastępuje oryginału orzeczenia."},
        {"source_id": "SRC-08", "status": "BRAK_TRESCI", "read_ranges": "1-35", "notes": "Krótki plik przeczytany w całości; omawia tę samą lub związaną sprawę, bez odrębnej treści o jakiejkolwiek sprawie z art. 28 ust. 2."},
        {"source_id": "SRC-09", "status": "BRAK_TRESCI", "read_ranges": "1-37", "notes": "Krótki plik przeczytany w całości; dotyczy aktualnego i byłego klienta, bez odrębnej treści o jakiejkolwiek sprawie z art. 28 ust. 2."}
    ],
    "meanings": [
        {
            "id": "OBS-019-M01",
            "context": "S2-K3-02 oraz S3-K6-03, art. 28 ust. 2 KERP",
            "description": "Nowy rekord OBS-019-R01 zachowuje literalną przesłankę: radca ma być obrońcą lub pełnomocnikiem klienta, a przeciwnik tego klienta również jest klientem radcy w jakiejkolwiek sprawie. SP-R05 odnotowuje pogląd autora, że obejmuje to także sprawy różne i niepowiązane, w jego objaśnieniu chodzi o przeciwników procesowych; nie przypisuję tej wykładni samemu przepisowi. SP-R04 wymaga odrębnej oceny sprzeczności i tej samej lub związanej sprawy przy art. 28 ust. 1, a SP-R06 dotyczy byłych klientów w ust. 3; zakresów tych nie łączę. Art. 26a ust. 2 wyłącza możliwość kancelaryjnego zarządzania konfliktem w sytuacjach art. 28 ust. 2 (OBS-076-R04). Rozszerzenie na doradzanie pozostaje wyłącznie poglądem autora z OBS-076-R06 oraz pytaniem OBS-076-Q03.",
            "record_ids": ["OBS-019-R01", "SP-R04", "SP-R05", "SP-R06", "OBS-076-R04", "OBS-076-R06"]
        }
    ],
    "records": [
        {
            "id": "OBS-019-R01",
            "kind": "norma",
            "claim": "Art. 28 ust. 2 lokalnego KERP zakazuje radcy bycia obrońcą lub pełnomocnikiem klienta, jeżeli przeciwnik tego klienta jest również jego klientem w jakiejkolwiek sprawie.",
            "speaker": "Kodeks Etyki Radcy Prawnego, art. 28 ust. 2",
            "role": "tekst normatywny w lokalnej kopii KERP",
            "context": "S2-K3-02 i S3-K6-03; odrębna przesłanka od art. 28 ust. 1 i 3 oraz od komentarzowej tezy o doradzaniu.",
            "court_treatment": "To brzmienie przepisu, nie teza sądu ani rozstrzygnięcie sprawy.",
            "source_status": "Lokalna kopia KERP; aktualności tekstu nie weryfikowano.",
            "evidence": [{"source_id": "SRC-04", "line_start": quote_line, "line_end": quote_line, "quote": quote}],
            "limits": "Przepis nie zawiera zwrotu ta sama lub związana sprawa, użytego w ust. 1 i 3. Nie definiuje samodzielnie, kogo uznawać za przeciwnika klienta ani nie stanowi podstawy do rozszerzenia zakazu z reprezentacji na doradztwo. Pogląd autora o przeciwnikach procesowych pozostaje odrębny."
        }
    ],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": "Sprawdzono oba punkty, literalny art. 28 ust. 2 oraz kontekst ust. 1, ust. 3, art. 26a i art. 29. SP-R05 zachowano jako pogląd autora, nie normę; OBS-076-R06 pozostaje odrębną wykładnią dotyczącą doradzania. Nie rozszerzono punktu na byłych klientów ani nie opracowano ogólnego testu spraw powiązanych. Cytat nowego rekordu pobrano dosłownie z SRC-04, wiersz 191. Wynik pozostaje OCZEKUJE na odbiór Astry i decyzję operatora."
}

def repair_mojibake(value):
    if isinstance(value, str):
        try:
            return value.encode("cp1252").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return value
    if isinstance(value, list):
        return [repair_mojibake(item) for item in value]
    if isinstance(value, dict):
        return {key: repair_mojibake(item) for key, item in value.items()}
    return value

result = repair_mojibake(result)
(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "citation_source": "SRC-04", "line": quote_line, "quote": quote}, ensure_ascii=False))
