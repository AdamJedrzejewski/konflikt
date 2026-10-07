import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK_DIR = ROOT / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-069" / "9aa4b35470a94a92853d772bf0b155a0"
MANIFEST = json.loads((TASK_DIR / "zlecenie.json").read_text(encoding="utf-8"))
SRC04 = (ROOT / next(s["text"] for s in MANIFEST["sources"] if s["id"] == "SRC-04")).read_text(encoding="utf-8-sig").splitlines()
quote_art42 = "\n".join(SRC04[356:377])

result = {
    "task_id": "9aa4b35470a94a92853d772bf0b155a0",
    "concept_id": "OBS-069",
    "label": "wielość klientów",
    "points": ["S2-K3-00"],
    "scope": "Punktem wyjścia pozostaje KL-R01: klientem jest podmiot, na rzecz którego świadczona jest pomoc prawna. Wykorzystuję odebrane przykłady KL-R05/R06/R07 dotyczące pośrednika, wyodrębnionej administracji osiedla oraz stałej współpracy, a także OBS-002-R03/R04/R07 dotyczące zakresu usługi, umowy i rozbieżności między szerokim pełnomocnictwem a uzgodnionym wykorzystaniem. Nowe uzupełnienie dotyczy art. 42 KERP: warunków jego zastosowania do klienta będącego osobą prawną lub innej jednostki, zakazu utożsamiania interesów, wskazywania uprawnionych odbiorców stanowisk oraz umownego rozszerzenia usług na innych klientów grupy. Art. 42 porządkuje interesy i zakres umownych usług, ale sam nie stanowi reguły, że każdy organ lub podmiot z grupy jest odrębnym klientem. Nie liczę automatycznie osób albo jednostek na podstawie ich nazwy lub przynależności do grupy. Pokrycie jest częściowe.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["KL-R01", "KL-R05", "KL-R06", "KL-R07", "KL-R11", "OBS-002-R03", "OBS-002-R04", "OBS-002-R05", "OBS-002-R07", "OBS-040-R01"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "168-180; 904-916; 964-992", "notes": "Komentarz roboczy, w tym relacja o zleceniu pośrednim i statusie odbiorców, oraz fragmenty o rodzajach czynności. Relacjonowane stanowisko OSD nie jest oryginałem rozstrzygnięcia."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "28-34; 70-80", "notes": "Fragmenty WO-226/24 i WO-173/22 w wyborze; zachowano niepewne autorstwo fragmentu WO-226/24 i brak weryfikacji z oryginałami."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "422-441; 105-175; 1340-1450", "notes": "Fragmenty dotyczące klientów/rejestru, działalności i świadczenia pomocy; wtórne opracowanie, bez uogólniania przypadków."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "39-57; 353-377", "notes": "Definicja klienta w lokalnym tekście oraz cały art. 42 z otoczeniem. Art. 42 odczytany z uwzględnieniem warunków ust. 1, grupy w ust. 3 i odpowiedniego stosowania z ust. 6."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "47; 93-123", "notes": "Art. 4, 6 i fragmenty art. 8 u.r.p. jako kontekst pojęcia pomocy i umowy; nie określają samodzielnie tożsamości każdego klienta w grupie."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "119-179; 293-321", "notes": "Teksty źródłowe i zestawienie relacji przepisów konfliktowych; zakres kontekstowy."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "31-58; 122-135", "notes": "Wtórne zestawienie fragmentów orzeczeń o kliencie i reprezentacji, bez oryginałów; nie użyto do nowej tezy."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały plik, sprawa ta sama lub związana; kontekst ewidencji relacji do spraw."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Cały plik, klient aktualny i były; kontekst ewidencji relacji klienta."}
    ],
    "meanings": [
        {"id": "OBS-069-M01", "context": "Ustalenie wielu klientów i rzeczywistego odbiorcy pomocy, punkt S2-K3-00", "description": "Odrębność klienta ustala się według tego, na czyją rzecz jest świadczona pomoc prawna, zgodnie z KL-R01, i w świetle konkretnego układu faktycznego. Odebrane przykłady ostrzegają, że samo skierowanie zlecenia przez pośrednika, umowna komparycja, przynależność podmiotu do grupy albo nazwanie organu nie przesądzają automatycznie, kto jest klientem; liczą się faktyczny beneficjent oraz zakres uzgodnionej i wykonywanej pomocy. Art. 42 KERP reguluje odrębność interesów klienta-osoby prawnej od interesów organów i grupy oraz pozwala umownie świadczyć usługi na rzecz innych klientów grupy, lecz nie zastępuje ustalenia, komu konkretnie pomoc jest udzielana.", "record_ids": ["OBS-069-R01", "KL-R01", "KL-R05", "KL-R06", "KL-R07", "OBS-002-R03", "OBS-002-R04", "OBS-002-R07"]}
    ],
    "records": [
        {"id": "OBS-069-R01", "kind": "przepis", "claim": "Art. 42 KERP w ust. 1-2 dotyczy radcy pracującego na podstawie umowy o pracę albo umowy o stałą pomoc klientowi będącemu osobą prawną; nakazuje nie utożsamiać interesu klienta z interesem organów lub podmiotów jego grupy oraz przewiduje wskazanie organów i osób uprawnionych do uzyskiwania stanowiska i wyrażania zgody. Ust. 3 pozwala umownie przewidzieć świadczenie czynności na rzecz innych klientów z grupy i uwzględnianie interesu grupy, a ust. 6 nakazuje odpowiednio stosować ust. 1-5 do jednostki niebędącej osobą prawną.", "speaker": "Kodeks Etyki Radcy Prawnego, art. 42 w lokalnym tekście SRC-04", "role": "tekst normatywny lokalnej kopii", "context": "Pomoc prawna na rzecz osoby prawnej lub innej jednostki organizacyjnej; rozdzielenie interesu klienta od interesów organów i jednostek grupy oraz możliwość kontraktowego świadczenia na rzecz innych klientów grupy.", "court_treatment": "nie_dotyczy", "source_status": "lokalna kopia KERP z manifestu; nie potwierdza aktualności przepisu", "evidence": [{"source_id": "SRC-04", "line_start": 357, "line_end": 377, "quote": quote_art42}], "limits": "Przepis określa warunki odnoszące się do określonego sposobu wykonywania zawodu wobec osoby prawnej lub innej jednostki oraz do treści umowy. Rozróżnienie interesów organów, grupy i klienta nie przesądza samo w sobie, że każdy organ, członek organu lub każdy podmiot grupy jest osobnym klientem. Ust. 3 mówi o innych klientach grupy i możliwości umownego objęcia ich usługami, nie o automatycznym statusie wszystkich spółek w grupie. Tożsamość klienta nadal wymaga ustalenia beneficjenta pomocy, z uwzględnieniem KL-R01 i konkretnych okoliczności."}
    ],
    "relations": [],
    "gaps": [
        {"id": "OBS-069-G01", "issue": "Art. 42 KERP odróżnia interes osoby prawnej, organów i grupy oraz pozwala na umowne usługi na rzecz innych klientów grupy, ale nie daje kompletnego testu, kiedy organ lub powiązany podmiot jest samodzielnym beneficjentem pomocy.", "needed": "Fakty konkretnej relacji: komu skierowano usługę, w czyim interesie ją wykonywano, jaki był uzgodniony zakres umowy oraz czy usługi były faktycznie świadczone także innym jednostkom."}
    ],
    "questions": [
        {"id": "OBS-069-Q01", "record_ids": ["OBS-069-R01", "KL-R01", "KL-R05", "KL-R06"], "understanding": "KL-R01 wskazuje beneficjenta pomocy jako klienta. Art. 42 rozdziela interes osoby prawnej od interesów organów i grupy, wskazuje osoby uprawnione do uzyskiwania stanowisk, a umowa może przewidzieć świadczenia na rzecz innych klientów grupy. Tekst nie mówi, że samo upoważnienie organu lub sama przynależność do grupy tworzą status odrębnego klienta.", "variants": "A: organ lub osoba upoważniona działa w sprawach klienta-osoby prawnej i nie staje się klientem bez pomocy świadczonej na jej własną rzecz. B: status odrębnego klienta może wynikać z rzeczywistej pomocy świadczonej organowi lub podmiotowi grupy jako osobnemu beneficjentowi, przy uwzględnieniu warunków umowy z art. 42. C: wymaga oceny konkretnej usługi, jej odbiorcy, celu i uzgodnionego zakresu, bez domniemania z samej funkcji lub przynależności organizacyjnej.", "consequences": "A zapobiega automatycznemu mnożeniu klientów przez organy i spółki powiązane. B/C pozwalają uwzględnić odrębnych beneficjentów i umownie rozszerzone usługi, ale wymagają identyfikacji rzeczywiście świadczonej pomocy. Inna kwalifikacja zmienia zakres badania konfliktu i ewidencji klientów.", "question": "Czy samo upoważnienie organu lub osoby do uzyskiwania stanowiska co do prawa na podstawie art. 42 ust. 2 oznacza, że jest ona odrębnym klientem, czy status ten wymaga ustalenia, że pomoc jest świadczona na jej własną rzecz? Jak w tym badaniu rozumieć umowne przewidzenie usług dla innych klientów grupy z ust. 3?", "needed": "Wykładnia art. 5 pkt 4 KERP w związku z art. 42 KERP oraz kryteria ustalania rzeczywistego beneficjenta przy obsłudze osoby prawnej, jej organów i grupy kapitałowej."}
    ],
    "self_check": "Coverage obejmuje dziewięć źródeł w zakresach podanych osobno; pełny odczyt zadeklarowano wyłącznie dla SRC-08 i SRC-09. Cytat nowego rekordu pobrano programowo z całych wierszy art. 42 SRC-04 i zachowuje brzmienie lokalnej kopii, łącznie z jej redakcyjnym zapisem. KL-R01 oraz opisane przykłady KL-R05/R06/R07 i OBS-002 wykorzystano jako istniejące refs, bez powielania. Zachowano rozróżnienie interesów od ustalenia liczby klientów. Status pozostaje OCZEKUJE; odbiór należy do Astry."
}

out = TASK_DIR / "wynik.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(out)

sys.path.insert(0, str(ROOT / "narzedzia" / "kolejka_pojec"))
import kolejka
state = kolejka.load(ROOT / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, result["concept_id"])
kolejka.validate_result(state, job, result)
print("validate_result: OK (bez zapisu do kolejki)")
