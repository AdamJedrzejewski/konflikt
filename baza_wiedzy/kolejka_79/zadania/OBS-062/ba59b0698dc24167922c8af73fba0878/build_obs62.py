import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK_DIR = ROOT / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-062" / "ba59b0698dc24167922c8af73fba0878"
job = json.loads((TASK_DIR / "zlecenie.json").read_text(encoding="utf-8"))
sources = {
    source["id"]: (ROOT / source["text"]).read_text(encoding="utf-8-sig").splitlines()
    for source in job["sources"]
}

def quote(source_id, start, end):
    return "\n".join(sources[source_id][start - 1:end])

result = {
    "task_id": "ba59b0698dc24167922c8af73fba0878",
    "concept_id": "OBS-062",
    "label": "tajemnica zawodowa",
    "points": ["S2-K5-00", "S2-K5-01"],
    "scope": "Uzupełniam znaczenie tajemnicy o funkcję z art. 9 KERP, zakaz skorzystania z informacji dla własnego lub cudzego interesu z art. 16 oraz odrębny obowiązek zabezpieczenia z art. 23. Ustawowe art. 3 ust. 5-6 ujmuję wyłącznie w granicach lokalnego tekstu, w tym ograniczenie wyjątków do zakresu określonego przepisami AML i Ordynacji podatkowej. Nie powtarzam art. 15 i 17 KERP o przedmiotowym i czasowym zakresie informacji z OBS-007-R02 ani ogólnej przesłanki tajemnicy w konflikcie mimo braku tożsamości lub związku spraw ze SP-R11. Nie rekonstruuję procedur zwolnienia ani nie deklaruję aktualności lokalnej kopii ustawy.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-007-R02", "SP-R11"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "430-448", "notes": "Nowe lustro komentarza: w. 440-448 omawiają ogólną przesłankę konfliktu opartą na tajemnicy, odrębność użycia informacji i przykład używania informacji. SP-R11 już pokrywa autorską tezę o konflikcie mimo braku tożsamości lub związku spraw; nie tworzę jej ponownie."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "23-25; 31-33; 41-43; 55-57; 59-61", "notes": "Wybrane relacje o tajemnicy, wcześniejszej wiedzy, zarzutach i wyniku uniewinniającym. Odczyt nie daje nowej ogólnej normy; nie utożsamiam opisów zarzutów z oceną sądu."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "293-330", "notes": "Komentarz opisuje zakres i czas tajemnicy, w tym informacje sprzed rozpoczęcia czynności; ten zakres jest już ujęty w OBS-007-R02. Nie powielam go jako nowego rekordu."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "73-82; 113-124; 134-142", "notes": "Lokalny KERP: art. 9, art. 15-18 i art. 23-24. Nowe rekordy dotyczą funkcji, zakazu użycia i zabezpieczenia; art. 15 i 17 pozostają w OBS-007-R02. Art. 24 odnotowano jako odrębną szczególną sytuację zawiadomienia na żądanie i z upoważnienia klienta, bez rekonstruowania jej procedury."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "28-48", "notes": "Lokalna kopia u.r.p., art. 3 ust. 3-6 oraz kontekst art. 4. Użyto ust. 5-6; ust. 3-4 o podstawowym zakresie i czasie nie są powielane względem OBS-007-R02. Ust. 6 zachowano z ograniczeniem „w zakresie określonym tymi przepisami”."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "30-80; 150-170", "notes": "Zestawienie definicji, art. 9, art. 15-16 oraz art. 26. Potwierdza istnienie odrębnego zakazu użycia, ale jest materiałem wtórnym; nowy rekord oparto na lokalnym KERP."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "33-46; 95-105; 162-165; 197-199", "notes": "Wybrane streszczenia WO-31/24, WO-150/19, WO-82/20 i tabela tez o zagrożeniu tajemnicy. Są wtórnymi relacjami; nie tworzą tu nowej ogólnej reguły ani pełnej procedury zwolnienia."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały krótki plik dotyczy tej samej i związanej sprawy; nie dodaje treści tajemnicy poza zakresem użytym przez SP-R11."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Cały krótki plik dotyczy klienta aktualnego i byłego; zakres czasowy ochrony jest już ujęty w OBS-007-R02."}
    ],
    "meanings": [
        {"id": "OBS-062-M01", "context": "Tajemnica zawodowa jako prawo i obowiązek oraz zakaz użycia informacji", "description": "Art. 9 KERP określa dochowanie tajemnicy jako prawo i obowiązek radcy oraz podstawę zaufania klienta i gwarancję praw i wolności. Art. 16 odrębnie obejmuje zakaz skorzystania z informacji i dokumentów z art. 15 w interesie własnym lub innej osoby, z zastrzeżeniem przypadków przewidzianych prawem lub KERP. Przedmiotowego zakresu i czasu informacji z art. 15 i 17 nie powtarzam, bo są już objęte OBS-007-R02.", "record_ids": ["OBS-062-R01", "OBS-062-R02", "OBS-007-R02", "SP-R11"]},
        {"id": "OBS-062-M02", "context": "Zabezpieczenie informacji i granice ustawowych wyjątków", "description": "Art. 23 KERP ustanawia obowiązek zabezpieczenia wszystkich informacji objętych tajemnicą przed niepowołanym ujawnieniem. U.r.p. art. 3 ust. 5 stanowi, że radca nie może być zwolniony z tajemnicy co do faktów poznanych przy świadczeniu pomocy lub prowadzeniu sprawy; ust. 6 osobno wskazuje informacje objęte ustawowymi trybami AML oraz Ordynacji podatkowej, i wyraźnie ogranicza to do zakresu określonego tymi przepisami. Nie przesądzam, jak wyjątki współdziałają z zakazem użycia z art. 16 ani nie określam procedury zwalniania.", "record_ids": ["OBS-062-R03", "OBS-062-R04"]}
    ],
    "records": [
        {"id": "OBS-062-R01", "kind": "przepis", "claim": "Art. 9 KERP stanowi, że dochowanie tajemnicy zawodowej jest prawem i obowiązkiem radcy prawnego, podstawą zaufania klienta oraz gwarancją praw i wolności.", "speaker": "Tekst lokalnego KERP, art. 9", "role": "tekst normatywny lokalnej kopii", "context": "Funkcja zasady tajemnicy zawodowej w relacji radcy z klientem.", "court_treatment": "nie_dotyczy", "source_status": "lokalny tekst KERP z manifestu; aktualności prawa nie weryfikowano", "evidence": [{"source_id": "SRC-04", "line_start": 75, "line_end": 75, "quote": quote("SRC-04", 75, 75)}], "limits": "Przepis określa status i funkcję tajemnicy, nie jej pełny zakres przedmiotowy, czasowy ani procedurę zwolnienia. Te zakresy są oddzielnie ujęte w OBS-007-R02."},
        {"id": "OBS-062-R02", "kind": "przepis", "claim": "Art. 16 KERP obejmuje dochowaniem tajemnicy nie tylko zakaz ujawniania informacji i dokumentów z art. 15, ale także zakaz skorzystania z nich w interesie własnym lub innej osoby, chyba że przepisy prawa lub KERP stanowią inaczej.", "speaker": "Tekst lokalnego KERP, art. 16", "role": "tekst normatywny lokalnej kopii", "context": "Odrębny zakaz używania informacji objętych tajemnicą, niezależny od samego ujawnienia ich osobie trzeciej.", "court_treatment": "nie_dotyczy", "source_status": "lokalny tekst KERP z manifestu; aktualności prawa nie weryfikowano", "evidence": [{"source_id": "SRC-04", "line_start": 119, "line_end": 119, "quote": quote("SRC-04", 119, 119)}], "limits": "Zastrzeżenie „chyba że przepisy prawa lub Kodeksu stanowią inaczej” zachowuję bez dopowiadania katalogu wyjątków. Zakres informacji z art. 15, do którego odsyła przepis, jest opisany w OBS-007-R02."},
        {"id": "OBS-062-R03", "kind": "przepis", "claim": "Art. 23 KERP nakłada na radcę obowiązek zabezpieczenia przed niepowołanym ujawnieniem wszelkich informacji objętych tajemnicą zawodową.", "speaker": "Tekst lokalnego KERP, art. 23", "role": "tekst normatywny lokalnej kopii", "context": "Obowiązek ochrony informacji objętych tajemnicą przed nieuprawnionym ujawnieniem.", "court_treatment": "nie_dotyczy", "source_status": "lokalny tekst KERP z manifestu; aktualności prawa nie weryfikowano", "evidence": [{"source_id": "SRC-04", "line_start": 137, "line_end": 137, "quote": quote("SRC-04", 137, 137)}], "limits": "Przepis ustanawia obowiązek zabezpieczenia, lecz przytoczony tekst nie wylicza konkretnych środków technicznych ani organizacyjnych. Nie projektuję ich z pamięci."},
        {"id": "OBS-062-R04", "kind": "przepis", "claim": "U.r.p. art. 3 ust. 5 stanowi, że radca nie może być zwolniony z tajemnicy co do faktów poznanych przy udzielaniu pomocy prawnej lub prowadzeniu sprawy. Ust. 6 odrębnie stanowi, że obowiązek nie dotyczy informacji udostępnianych na podstawie przepisów o przeciwdziałaniu praniu pieniędzy i finansowaniu terroryzmu ani przekazywanych na podstawie wskazanych przepisów Ordynacji podatkowej, w zakresie określonym tymi przepisami.", "speaker": "Tekst lokalnej u.r.p., art. 3 ust. 5-6", "role": "tekst normatywny lokalnej kopii", "context": "Ustawowa niezwalnialność tajemnicy dla wskazanych faktów oraz odrębne, ograniczone odesłaniami wyjątki ustawowe dotyczące informacji AML i podatkowych.", "court_treatment": "nie_dotyczy", "source_status": "lokalna kopia ustawy z manifestu; aktualności ani tekstów ustaw cross-referenced nie weryfikowano", "evidence": [{"source_id": "SRC-05", "line_start": 33, "line_end": 45, "quote": quote("SRC-05", 33, 45)}], "limits": "Nie utożsamiam ust. 5 z nieograniczonym wyjątkiem ani nie rozszerzam ust. 6 poza zakres wyraźnie określony w przywołanych przepisach. Ich treści nie ma w sprawdzonym fragmencie manifestu; nie rekonstruuję procedury ani relacji do każdego przypadku z art. 16 KERP."}
    ],
    "relations": [],
    "gaps": [
        {"id": "OBS-062-G01", "issue": "Lokalna u.r.p. wymienia w art. 3 ust. 6 informacje AML i podatkowe jedynie przez odesłanie oraz ogranicza wyjątki do zakresu określonego tymi przepisami; ich treści nie ma w dziewięciu źródłach w zakresie odczytanym.", "needed": "Teksty właściwych przepisów AML i Ordynacji podatkowej lub eksperckie wskazanie dokładnego zakresu informacji i obowiązków, bez rozszerzania wyjątku na inne ujawnienia lub użycie informacji."},
        {"id": "OBS-062-G02", "issue": "Art. 23 ustanawia ogólny obowiązek zabezpieczenia, ale lokalny przepis i przeczytane fragmenty nie podają katalogu konkretnych środków zabezpieczających.", "needed": "Odrębne, źródłowe określenie wymaganych środków zabezpieczenia, jeśli mają być operacjonalizowane poza zakresem tej karty."}
    ],
    "questions": [
        {"id": "OBS-062-Q01", "record_ids": ["OBS-062-R02", "OBS-062-R04"], "understanding": "Art. 16 KERP zastrzega wyjątki przewidziane prawem lub KERP od zakazu ujawniania i korzystania z informacji, a u.r.p. art. 3 ust. 6 wskazuje konkretne kategorie ustawowe, ograniczając je do zakresu określonego przepisami AML i Ordynacji podatkowej. Korpus nie zawiera tych przepisów cross-referenced, więc nie można tu ustalić dokładnego katalogu informacji ani czynności.", "variants": "A: ujmować wyjątki wyłącznie jako informacje i czynności wyraźnie dopuszczone oraz ograniczone przez właściwe przepisy szczególne. B: przed ustaleniem granic art. 16 i art. 3 ust. 6 pozyskać teksty wskazanych ustaw i ustalić, czy dotyczą ujawnienia informacji, ich przekazania, czy również odrębnego skorzystania z nich. C: zachować wyjątki wyłącznie jako odesłania i nie opisywać ich skutków ponad lokalne brzmienie.", "consequences": "Wariant A pozwala wskazać wąski zakres wyłączeń po ustaleniu przepisów szczególnych. Wariant B wymaga pełnego materiału ustawowego, ale rozdziela ujawnienie/transfer od korzystania z informacji. Wariant C nie ryzykuje nadmiernego rozszerzenia wyjątków, lecz pozostawia je nieoperacyjne. Żaden wariant nie uzasadnia ogólnego zwolnienia z tajemnicy.", "question": "Jaki dokładnie zakres informacji i czynności obejmują wyjątki wskazane w art. 3 ust. 6 u.r.p. przez odesłanie do przepisów AML i Ordynacji podatkowej oraz jak odnoszą się one do zastrzeżenia art. 16 KERP o skorzystaniu z informacji w interesie własnym lub innej osoby? Czy bez tekstów tych przepisów należy pozostać przy samym odesłaniu i nie rozszerzać wyjątku?", "needed": "Teksty przepisów cross-referenced lub stanowisko eksperckie co do ich zakresu, z odrębnym ujęciem ujawnienia/transferu i skorzystania z informacji."
        }
    ],
    "self_check": "Przeczytano brief, zakres partii, odebrane_zakresy oraz relewantne fragmenty wszystkich dziewięciu źródeł; SRC-08 i SRC-09 przejrzano w całości. Cytaty w nowych rekordach pobrano programowo z dosłownych wierszy manifestu. Nie powielono art. 15 i 17 KERP z OBS-007-R02 ani ogólnej przesłanki konfliktu tajemnicy ze SP-R11. Zachowano wyjątki art. 16 KERP i dokładne ograniczenie art. 3 ust. 6 u.r.p.; nie deklarowano aktualności ustawy ani nie rekonstruowano procedury zwolnienia. Opisy orzeczeń pozostawiono jako relacje wtórne bez uogólniania. Operator status OCZEKUJE; odbiór należy do Astry."
}

out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out)

sys.path.insert(0, str(ROOT / "narzedzia" / "kolejka_pojec"))
import kolejka
state = kolejka.load(ROOT / "baza_wiedzy" / "kolejka_79")
task = kolejka.get_job(state, result["concept_id"])
kolejka.validate_result(state, task, result)
print("validate_result: OK (bez zapisu do kolejki)")
