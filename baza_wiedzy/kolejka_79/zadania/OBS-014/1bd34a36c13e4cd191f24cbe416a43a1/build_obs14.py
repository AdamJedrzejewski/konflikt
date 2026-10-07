import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
previous = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-013" / "e139f38ef9e544dc8d22f8a69ee1cc73" / "wynik.json"
previous_result = json.loads(previous.read_text(encoding="utf-8"))
coverage = previous_result["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["notes"] += " Dla zakresu uprzednich czynności wykorzystuję odrębne historyczne KL-R08/R09 i SP-R06; nie mieszam ich manifestów z nowym lustrem."
    elif item["source_id"] == "SRC-04":
        item["read_ranges"] = "63-75; 171-209"
        item["notes"] = "Art. 6-9 KERP oraz art. 26a i 27-30 przeczytane w kontekście; tekst odróżnia wcześniejsze czynności, tajemnicę i szczególne zakazy. Aktualności kopii nie weryfikowano."

result = {
    "task_id": "1bd34a36c13e4cd191f24cbe416a43a1",
    "concept_id": "OBS-014",
    "label": "interes byłego klienta",
    "points": ["S2-K4-03", "S2-K4-06"],
    "scope": (
        "Mapuję S2-K4-03 na reprezentację lub obronę z art. 28 ust. 3, a S2-K4-06 na doradzanie z art. 29 ust. 1 pkt 2. "
        "W obu konfiguracjach chodzi o sprzeczność interesu aktualnego klienta z interesami osoby, na rzecz której radca "
        "uprzednio wykonywał czynności zawodowe, w tej samej lub związanej sprawie (SP-R06/R07). Samo oznaczenie tej osoby "
        "jako byłego klienta nie tworzy innej treści jej interesu: znaczenie interesu odsyła do OBS-015-R01/R02 i OBS-057-R01, "
        "a materialna sprzeczność pozostaje odrębnym warunkiem (OBS-057-R02). Nie utożsamiam interesu tej osoby z zakresem "
        "tajemnicy z OBS-007-R02 ani z aktualnymi oczekiwaniami nowego klienta, które nie są same w sobie miarą interesu. "
        "KL-R08/R09 to autorskie objaśnienia uprzednich czynności i terminu były klient; nie wyznaczają ogólnej daty ustania "
        "relacji. KL-R04 również nie podaje takiej daty, a ten brak i zdarzenia kończące relację pozostają w KL-G02 oraz "
        "OBS-002-Q01. Przy doradzaniu art. 29 ust. 2 zachowuje zgodę klienta lub klientów oraz osób uprzednio obsługiwanych; "
        "zgody nie można uzyskać, gdy radca jest lub był obrońcą w sprawie karnej co najmniej jednego z nich. Nie stosuję "
        "art. 28 ust. 2 dotyczącego aktualnych klientów będących przeciwnikami jako reguły dla byłego klienta. Jednostkowe "
        "przykłady SP-R09/R10 nie stanowią uniwersalnego testu interesu ani czasu. Nie dodaję pytań, bo treść interesu "
        "pozaprawnego i sprzeczność mają istniejące konsultacje OBS-015-Q01/OBS-057-Q01, a omyłkowe odesłanie komentarza "
        "pozostaje OBS-007-Q01. Coverage 9 źródeł reused z OBS-013, częściowe i bez weryfikacji oryginałów orzeczeń."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "KL-R04", "KL-R08", "KL-R09", "SP-R06", "SP-R07", "SP-R09", "SP-R10",
        "OBS-007-R01", "OBS-007-R02", "OBS-015-R01", "OBS-015-R02", "OBS-015-R03",
        "OBS-057-R01", "OBS-057-R02"
    ],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-014-M01",
            "context": "S2-K4-03, art. 28 ust. 3 KERP, interes aktualnego klienta wobec osoby uprzednio obsługiwanej",
            "description": (
                "W art. 28 ust. 3 aktualny klient może mieć interes sprzeczny z interesami osoby, na rzecz której radca "
                "uprzednio wykonywał czynności zawodowe w tej samej lub związanej sprawie. SP-R06 zachowuje, że uprzednie "
                "czynności mogą obejmować reprezentację lub doradztwo. Interes tej osoby nie zmienia treści tylko dlatego, "
                "że jest ona uprzednio obsługiwana: OBS-015-R01/R02 ujmują cel ochrony interesów i lojalność, a OBS-057-R01 "
                "obejmuje interes prawny, procesowy i pozaprawny. Właściwe ustalenie materialnej sprzeczności pozostaje "
                "osobnym warunkiem z OBS-057-R02. Tego interesu nie utożsamiam z tajemnicą zawodową: OBS-007-R02 rozdziela "
                "zakres i trwanie tajemnicy od statusu klienta. Oczekiwania nowego klienta nie przesądzają interesu osoby "
                "uprzednio obsługiwanej. KL-R04 i przykłady SP-R09/R10 nie ustanawiają ogólnej daty ustania relacji ani "
                "uniwersalnego testu; koniec relacji pozostaje w KL-G02/OBS-002-Q01."
            ),
            "record_ids": ["SP-R06", "KL-R04", "OBS-015-R01", "OBS-015-R02", "OBS-057-R01", "OBS-057-R02", "OBS-007-R02", "SP-R09", "SP-R10"]
        },
        {
            "id": "OBS-014-M02",
            "context": "S2-K4-06, art. 29 ust. 1 pkt 2 KERP, doradzanie w konflikcie z osobą uprzednio obsługiwaną",
            "description": (
                "Art. 29 ust. 1 pkt 2 dotyczy doradzania aktualnemu klientowi, gdy jego interesy są sprzeczne w tej samej "
                "lub związanej sprawie z interesami osoby, na rzecz której radca uprzednio wykonywał czynności zawodowe. "
                "SP-R07 zachowuje wyjątek zgody z ust. 2: zgodę wyrażają klient lub klienci oraz osoby uprzednio obsługiwane; "
                "nie można jej uzyskać, gdy radca jest lub był obrońcą w sprawie karnej co najmniej jednego z nich. "
                "OBS-007-R01 wskazuje rozbieżność między komentarzowym odesłaniem do pkt 1 a lokalnym tekstem pkt 2; "
                "pytanie o zamierzoną podstawę tego fragmentu pozostaje OBS-007-Q01. Pojęcie interesu i jego materialna "
                "sprzeczność zachowują granice OBS-015-R01/R02 i OBS-057-R01/R02."
            ),
            "record_ids": ["SP-R07", "OBS-007-R01", "OBS-015-R01", "OBS-015-R02", "OBS-057-R01", "OBS-057-R02"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-014-G01",
            "issue": "W wykorzystanych kartach i fragmentach nie ma ogólnej daty, która kończyłaby status osoby uprzednio obsługiwanej dla wszystkich celów; czas tajemnicy jest odrębny i może trwać dalej.",
            "needed": "Ustalenie konkretnego zdarzenia kończącego relację w danej konfiguracji; wspólne pytanie o to pozostaje w KL-G02 i OBS-002-Q01, bez nowego pytania w tej karcie."
        }
    ],
    "questions": [],
    "self_check": "Dwa punkty mapują się do art. 28 ust. 3 i art. 29 ust. 1 pkt 2. Interes osoby uprzednio obsługiwanej oddzielono od tajemnicy i od aktualnych oczekiwań nowego klienta; nie nadano mu odmiennej treści wyłącznie z powodu statusu byłego klienta. Zachowano zgodę i wyjątek obrońcy karnego z art. 29 ust. 2. Jawnie odnotowano brak ogólnej daty końca relacji i odesłano do KL-G02/OBS-002-Q01. Ograniczenia przykładów SP-R09/R10 pozostają. Wynik OCZEKUJE na odbiór Astry."
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": len(result["records"]), "questions": len(result["questions"]), "sources": len(result["coverage"])}, ensure_ascii=False))
