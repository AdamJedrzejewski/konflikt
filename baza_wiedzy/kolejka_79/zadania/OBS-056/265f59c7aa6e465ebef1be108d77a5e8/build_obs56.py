import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
job = json.loads((task_dir / "zlecenie.json").read_text(encoding="utf-8"))
previous = root / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-060" / "5b9ee3d0aa8a4018bd9b626bec5f2f03" / "wynik.json"
previous_result = json.loads(previous.read_text(encoding="utf-8"))
coverage = previous_result["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["read_ranges"] = "920-928, 964-972"
        item["notes"] = "Komentarz roboczy; blok 924 z definicjami kryteriów odczytano z otoczeniem 920-928. Dalsze konteksty art. 28 ust. 2/doradztwa sprawdzono w 964-972. Materiał do korekty, nie niezależne potwierdzenie autora SRC-03."
    elif item["source_id"] == "SRC-03":
        item["notes"] += " Ponownie wykorzystano odebrane odczyty dotyczące art. 28-30; Astra sprawdziła obraz strony 17."
    elif item["source_id"] == "SRC-04":
        item["read_ranges"] = "171-209"
        item["notes"] = "Lokalny tekst art. 26a oraz art. 27-30; zachowano odrębne standardy i zakresy, bez weryfikacji aktualności kopii."

src01_meta = next(item for item in job["sources"] if item["id"] == "SRC-01")
src01_lines = (root / src01_meta["text"]).read_text(encoding="utf-8-sig").splitlines()
line_start = line_end = 924
line_text = src01_lines[line_start - 1]
quote_start = line_text.index("Natomiast powiązanie spraw")
quote = line_text[quote_start:]

result = {
    "task_id": "265f59c7aa6e465ebef1be108d77a5e8",
    "concept_id": "OBS-056",
    "label": "sprawa związana",
    "points": ["S1-K1-03", "S1-K1-05", "S2-K3-04", "S2-K3-07", "S2-K4-02", "S2-K4-05"],
    "scope": (
        "Mapuję sześć punktów do istniejących konfiguracji: S1-K1-03/S1-K1-05 to art. 30 ust. 1 (SP-R08), "
        "S2-K3-04/S2-K3-07 to art. 28 ust. 1 oraz art. 29 ust. 1 pkt 1 (SP-R04/R07), a S2-K4-02/S2-K4-05 to "
        "art. 28 ust. 3 oraz art. 29 ust. 1 pkt 2 (SP-R06/R07). Uzupełniam rzeczywistą lukę w claimach SP-R02/R03: "
        "SRC-01 w. 924 nie tylko wymienia trzy alternatywne kryteria i podkreśla wagę gospodarczego, lecz definiuje "
        "każde z nich. Nowy rekord odtwarza te autorskie objaśnienia bez dodawania zamkniętego testu. Nie utożsamiam "
        "powiązania spraw z całym testem konfliktu: SP-R04/R06 zachowują odrębne warunki sprzeczności i właściwe "
        "zakresy czynności, SP-R07 warunki doradztwa, zgody oraz wyjątek obrońcy karnego, a SP-R08 konfigurację art. 30. "
        "Przykłady jednostkowe SP-R09/R10 nie stają się uniwersalną definicją, a SP-R12 pozostaje niezweryfikowaną "
        "syntezą karty aplikacji. Pytanie o granice łączników pozostaje w SP-P01; OBS-054-Q01 dotyczy odrębnie "
        "tożsamości sprawy. Zakres częściowy; źródła i lokalne przepisy wykorzystano z wcześniejszego odczytu oraz "
        "ponownie sprawdzono blok 924 w kontekście."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["SP-R01", "SP-R02", "SP-R03", "SP-R04", "SP-R05", "SP-R06", "SP-R07", "SP-R08", "SP-R09", "SP-R10", "SP-R12", "OBS-054-R01"],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-056-M01",
            "context": "Podmiotowe, przedmiotowe i gospodarcze kryteria oceny związku spraw",
            "description": (
                "Autor komentarza określa kryteria stosowane alternatywnie: podmiotowe jako tożsamość stron "
                "postępowania w różnych sprawach, przedmiotowe jako tożsamość przedmiotu sporu lub czynu "
                "podlegającego rozpoznaniu w różnych sprawach, a gospodarcze jako realizację wspólnego celu "
                "gospodarczego. Sformułowanie „przede wszystkim” zachowuje otwarty charakter wyjaśnienia. SP-R02 "
                "odnotowuje samo wskazanie alternatywnych kryteriów, a claim SP-R03 skupia się na możliwości "
                "samodzielnego znaczenia kryterium gospodarczego i przykładzie skomplikowanych relacji ekonomicznych; "
                "nowy zakres dotyczy szczegółowych definicji kryteriów z SRC-01 w. 924. Autor podkreśla, że kryterium "
                "gospodarcze może mieć znaczenie nawet bez powiązań podmiotowych i przedmiotowych, ale nie wynika stąd, "
                "że dowolna więź ekonomiczna wystarcza. Pytanie o granice łączników pozostaje w SP-P01."
            ),
            "record_ids": ["OBS-056-R01", "SP-R02", "SP-R03"]
        },
        {
            "id": "OBS-056-M02",
            "context": "S1-K1-03 i S1-K1-05, art. 30 ust. 1 KERP",
            "description": "SP-R08 mapuje te punkty do konfliktu lub znacznego ryzyka konfliktu między klientem a radcą prawnym lub osobą mu najbliższą. Samo powiązanie spraw nie zastępuje tej przesłanki i zakresu normy.",
            "record_ids": ["SP-R08", "OBS-056-R01"]
        },
        {
            "id": "OBS-056-M03",
            "context": "S2-K3-04 i S2-K3-07, art. 28 ust. 1 oraz art. 29 ust. 1 pkt 1 KERP",
            "description": "SP-R04 zachowuje wymóg odrębnej sprzeczności interesów obok ustalenia tożsamości lub związku spraw w reprezentacji lub obronie aktualnych klientów. Art. 29 ust. 1 pkt 1 dotyczy doradzania przy sprzeczności interesów aktualnych klientów w tej samej lub związanej sprawie; zgoda z art. 29 ust. 2 wymaga zgody klienta lub klientów i osób uprzednio obsługiwanych, z wyjątkiem braku możliwości uzyskania jej, gdy radca jest lub był obrońcą w sprawie karnej co najmniej jednego z nich (SP-R07).",
            "record_ids": ["SP-R04", "SP-R07", "OBS-056-R01"]
        },
        {
            "id": "OBS-056-M04",
            "context": "S2-K4-02 i S2-K4-05, art. 28 ust. 3 oraz art. 29 ust. 1 pkt 2 KERP",
            "description": "SP-R06 zachowuje sprzeczność interesów aktualnego klienta z interesami osoby uprzednio obsługiwanej oraz wymóg tej samej lub związanej sprawy dla reprezentacji lub obrony; art. 29 ust. 1 pkt 2 dotyczy doradzania w tej konfiguracji. Zgoda z art. 29 ust. 2 wymaga zgody klienta lub klientów oraz osób uprzednio obsługiwanych i nie może być uzyskana, gdy radca jest lub był obrońcą w sprawie karnej co najmniej jednego z nich (SP-R07).",
            "record_ids": ["SP-R06", "SP-R07", "OBS-056-R01"]
        }
    ],
    "records": [
        {
            "id": "OBS-056-R01",
            "kind": "poglad_autora",
            "claim": "Autor komentarza definiuje trzy alternatywne kryteria oceny związku spraw: podmiotowe jako tożsamość stron w różnych sprawach, przedmiotowe jako tożsamość przedmiotu sporu lub czynu rozpoznawanego w różnych sprawach, a gospodarcze jako realizację wspólnego celu gospodarczego.",
            "speaker": "dr Paweł Skuczyński",
            "role": "autor komentarza do KERP, wersja robocza do korekty autorskiej",
            "context": "Objaśnienie łączników przy ocenie powiązania spraw w różnych postępowaniach.",
            "court_treatment": "Nie dotyczy; to pogląd autora komentarza, nie teza sądu.",
            "source_status": "SRC-01 jest komentarzem oznaczonym do korekty autorskiej; lustro może nie obejmować wszystkich zmian. Cytat z w. 924 pobrano z lokalnego lustra. SRC-01 i SRC-03 są opracowaniami tego samego autora.",
            "evidence": [{"source_id": "SRC-01", "line_start": line_start, "line_end": line_end, "quote": quote}],
            "limits": "Kryteria są według autora stosowane alternatywnie i „przede wszystkim”; tekst nie ustanawia zamkniętego testu ani automatycznego wyniku dla każdej wspólnej strony, przedmiotu lub relacji gospodarczej. SP-R09/R10 są jednostkowymi przykładami, a SP-R12 nie jest potwierdzoną regułą prawną. Nie utożsamiać związku spraw z pełnym testem konfliktu z art. 28-30. Granice kryteriów pozostają w SP-P01."
        }
    ],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": "Nowy cytat pobrano programowo jako ciąg od początku definicji powiązania do końca wiersza 924 SRC-01. Claim ograniczono do definicji kryteriów, których SP-R02/R03 nie wypowiadają wprost; szeroki cytat SP-R03 nie potraktowano jako wcześniejszego claimu tych definicji. Wszystkie sześć punktów przypisano do art. 30, 28 ust. 1/3 i 29 ust. 1 pkt 1/2 z odrębnymi przesłankami. SP-P01 pozostaje pytaniem o granice łączników; OBS-054-Q01 dotyczy tożsamości. Wynik pozostaje OCZEKUJE na odbiór Astry."
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "citation_source": "SRC-01", "line": line_start, "records": len(result["records"]), "questions": len(result["questions"]), "sources": len(result["coverage"])}, ensure_ascii=False))
