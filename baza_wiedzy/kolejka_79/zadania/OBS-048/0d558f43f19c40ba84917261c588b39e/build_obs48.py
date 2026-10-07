import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK = ROOT / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-048" / "0d558f43f19c40ba84917261c588b39e"
sys.path.insert(0, str(ROOT / "narzedzia" / "kolejka_pojec"))
import kolejka

state = kolejka.load(ROOT / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, "OBS-048")
attempt_id = job["attempts"][-1]["id"]

def source_lines(source_id):
    info = next(s for s in state["sources"] if s["id"] == source_id)
    return (ROOT / info["text"]).read_text(encoding="utf-8-sig").splitlines()

src01 = source_lines("SRC-01")

def exact(source_id, start, end):
    lines = source_lines(source_id)
    return "\n".join(lines[start - 1:end])

records = [
    {
        "id": "OBS-048-R01",
        "kind": "pogląd_autora",
        "claim": "Autor komentarza dzieli art. 27 KERP na dwie grupy: pkt 1 i 2 dotyczą wcześniejszego udziału samego radcy w sprawie w wymienionej roli lub zeznawania jako świadka, a pkt 3–6 dotyczą określonych relacji radcy z inną osobą, za której pośrednictwem mógł wyrobić sobie stosunek do sprawy lub mieć na nią wpływ.",
        "speaker": "P. Skuczyński",
        "role": "autor komentarza do KERP",
        "context": "Objaśnienie struktury art. 27 KERP; tekst komentarza w roboczym lustrze z oznaczeniami redakcyjnymi.",
        "court_treatment": "nie_dotyczy; jest to pogląd autora komentarza, nie stanowisko sądu ani odrębna norma",
        "source_status": "SRC-01 to nowe lustro komentarza do korekty autorskiej. SRC-03 w. 754–784 przedstawia analogiczny podział/ogólny opis tego samego autora, nie niezależne potwierdzenie. Nie weryfikowano oryginalnych publikacji wskazanych w komentarzu.",
        "evidence": [
            {"source_id": "SRC-01", "line_start": 812, "line_end": 812, "quote": exact("SRC-01", 812, 812)},
            {"source_id": "SRC-01", "line_start": 824, "line_end": 824, "quote": exact("SRC-01", 824, 824)},
        ],
        "limits": "Podział porządkuje różne mechanizmy, ale nie zastępuje odrębnego odczytania przesłanek każdego punktu. W pkt 3 chodzi o udział innej osoby w rozstrzygnięciu, w pkt 4 obowiązują warunki samego przepisu, a pkt 5 i 6 wskazują inne role osób po drugiej stronie relacji. Nie wynika z tego wspólna definicja relacji osobistej ani zależności. Autor przyznaje pkt 3 węższy zakres udziału niż pkt 1 (SRC-01 w. 832; ON-R07).",
    },
    {
        "id": "OBS-048-R02",
        "kind": "pogląd_autora",
        "claim": "Autor komentarza odczytuje art. 27 KERP tak, że wystąpienie wymienionej w nim okoliczności wyklucza świadczenie pomocy bez dalszej oceny i bez rozróżnienia na konflikt potencjalny i aktualny; w pkt 4 nadal trzeba najpierw spełnić jego literalne warunki.",
        "speaker": "P. Skuczyński",
        "role": "autor komentarza do KERP",
        "context": "Autorska ocena skutku okoliczności wymienionych w art. 27, zestawiona z literalnymi warunkami jego poszczególnych punktów.",
        "court_treatment": "nie_dotyczy; komentarz nie relacjonuje w tym miejscu rozstrzygnięcia sądu",
        "source_status": "Komentarz redakcyjny w wersji do korekty. Podobne ujęcie w SRC-03 w. 781–784 pochodzi od tego samego autora i nie jest niezależnym potwierdzeniem. Nie przedstawiam tego odczytania jako dosłownego brzmienia przepisu ani jako zaakceptowanej reguły operatora.",
        "evidence": [
            {"source_id": "SRC-01", "line_start": 808, "line_end": 808, "quote": exact("SRC-01", 808, 808)},
        ],
        "limits": "To stanowisko autora, a nie odrębna norma źródłowa ani wynik orzeczenia. Nie uchyla warunków zapisanych w samym art. 27, w tym warunku jednoczesnego wykonywania czynności zawodowych na rzecz tego samego klienta z pkt 4. Teza nie stanowi definicji osoby najbliższej, zależności lub bliskich stosunków i nie rozstrzyga, kiedy ich przesłanki zachodzą.",
    },
]

meanings = [
    {
        "id": "OBS-048-M01",
        "context": "S1-K2-00, art. 27 pkt 1–2 KERP: wcześniejszy udział samego radcy w sprawie lub zeznawanie jako świadek",
        "description": "Punkt zbiorczy obejmuje tu odrębną konfigurację osobistego udziału radcy w sprawie, nie relację rodzinną lub zależność innej osoby. Autor ujmuje pkt 1 i 2 jako pierwszą grupę (OBS-048-R01); literalne przypadki opisuje lokalny tekst KERP. Nie przenoszę na tę grupę alternatyw dotyczących innej osoby z pkt 3, 5 i 6.",
        "record_ids": ["OBS-048-R01", "OBS-048-R02"],
    },
    {
        "id": "OBS-048-M02",
        "context": "S1-K2-00, art. 27 pkt 3 KERP: osoba najbliższa albo osoba zależna od radcy uczestnicząca w rozstrzygnięciu",
        "description": "Norma wymienia alternatywnie osobę najbliższą oraz osobę pozostającą z jakichkolwiek przyczyn w stosunku zależności z radcą, jeżeli brała lub bierze udział w rozstrzygnięciu sprawy (ON-R03). Autor odrębnie uznaje określenia z pkt 3, 5 i 6 za bliskoznaczne (ON-R06), ale opisuje udział w rozstrzygnięciu jako węższy od udziału w sprawie z pkt 1 (ON-R07). Nie wyprowadzam z tego pozytywnego testu zależności; OBS-058-Q01 już pyta o ten test i kierunek zależności.",
        "record_ids": ["ON-R03", "ON-R06", "ON-R07", "OBS-048-R01", "OBS-048-R02"],
    },
    {
        "id": "OBS-048-M03",
        "context": "S1-K2-00, art. 27 pkt 4 KERP: sprawa dotycząca radcy lub osoby, z którą może wspólnie wykonywać zawód",
        "description": "Wymagana jest sprawa dotycząca radcy, adwokata lub innej osoby, z którą radca może na podstawie prawa wspólnie wykonywać zawód, oraz wykonywanie czynności zawodowych w tym samym czasie na rzecz tego samego klienta. Są to warunki literalnej normy ujętej w OBS-008-R01; pkt 4 nie sprowadza się do samej relacji zawodowej. OBS-008-G01 pozostaje właściwym miejscem dla nierozstrzygniętej granicy zastosowania tych warunków.",
        "record_ids": ["OBS-008-R01", "OBS-048-R01", "OBS-048-R02"],
    },
    {
        "id": "OBS-048-M04",
        "context": "S1-K2-00, art. 27 pkt 5 KERP: obecne albo byłe bliskie stosunki radcy z przeciwnikiem klienta albo osobą zainteresowaną niekorzystnym rozstrzygnięciem",
        "description": "Norma zawiera dwie alternatywne osoby oraz obejmuje stosunki, które były albo pozostają aktualne (OBS-043-R01). Pogląd o bliskoznaczności pozostaje tezą autora, nie pozytywnym testem (ON-R06). D 43/2016 to ograniczony opis faktów bez widocznego rozstrzygnięcia i bez ustalenia, że osoba bliska była przeciwnikiem klienta lub osobą zainteresowaną niekorzystnym wynikiem (OBS-005-R01). Dodatnie cechy bliskich stosunków obejmuje już OBS-005-Q01; znaczenia przeciwnika i osoby zainteresowanej dotyczy OBS-043-Q01.",
        "record_ids": ["OBS-043-R01", "OBS-043-R02", "ON-R06", "OBS-005-R01", "OBS-048-R01", "OBS-048-R02"],
    },
    {
        "id": "OBS-048-M05",
        "context": "S1-K2-00, art. 27 pkt 6 KERP: osoba najbliższa radcy po stronie przeciwnej w tej sprawie",
        "description": "Przesłanka dotyczy wyłącznie osoby najbliższej radcy, która jest pełnomocnikiem strony przeciwnej albo wykonywała na jej rzecz inną pomoc prawną w tej sprawie (ON-R04). Nie przenoszę tu alternatywy zależności z pkt 3 ani stosunków bliskości z pkt 5. ON-P02 i OBS-043-Q01 obejmują już odrębne kwestie bliskoznaczności i znaczenia stron.",
        "record_ids": ["ON-R04", "ON-R06", "OBS-043-R02", "OBS-048-R01", "OBS-048-R02"],
    },
]

result = {
    "task_id": attempt_id,
    "concept_id": "OBS-048",
    "label": "relacja osobista lub zależność",
    "points": ["S1-K2-00"],
    "scope": "S1-K2-00 jest zbiorczą etykietą, nie jedną normą rodzinną. Mapuję ją na art. 27 pkt 1–6 KERP, zachowując podział komentatora na własny wcześniejszy udział radcy/wystąpienie w roli z pkt 1–2 oraz relację przez inną osobę w pkt 3–6 (OBS-048-R01). Art. 27 pkt 3 dotyczy osoby najbliższej albo osoby zależnej od radcy uczestniczącej w rozstrzygnięciu; pkt 4 wymaga jednocześnie sprawy dotyczącej wskazanej osoby, dopuszczalnej wspólnej pracy zawodowej, tego samego czasu i tego samego klienta; pkt 5 wymienia byłe lub obecne bliskie stosunki z przeciwnikiem klienta albo osobą zainteresowaną niekorzystnym rozstrzygnięciem; pkt 6 dotyczy osoby najbliższej będącej pełnomocnikiem strony przeciwnej lub świadczącej jej inną pomoc w tej sprawie. Wykładnia autora o braku dalszej oceny z art. 27 jest oddzielona od treści normy i nie uchyla szczególnych warunków pkt 4 (OBS-048-R02). Nie powielam ON-P02 (bliskoznaczność), OBS-005-Q01 (dodatnie cechy bliskich stosunków), OBS-043-Q01 (przeciwnik/osoba zainteresowana), OBS-058-Q01 (test i kierunek zależności) ani OBS-008-G01 (granice pkt 4); odsyłam do tych miejsc. Nie utożsamiam zależności innej osoby od radcy z zależnością radcy od wpływów opisanych przy art. 26 lub art. 7 (OBS-029-R05). Karta częściowa: mapa opiera się na lokalnym tekście KERP i komentarzu roboczym, a nierozstrzygnięte testy i granice pozostają w istniejących konsultacjach.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "ON-R03", "ON-R04", "ON-R06", "ON-R07",
        "OBS-008-R01", "OBS-029-R05",
        "OBS-043-R01", "OBS-043-R02", "OBS-005-R01"
    ],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "804-840", "notes": "Nowe lustro komentarza, odczytano bloki z kontekstem: w. 804 konfiguracja art. 27, w. 808 pogląd o skutku, w. 812 i 824 podział na grupy, w. 828–832 relacje i odrębność udziału w rozstrzygnięciu. W. 828 to pogląd autora o bliskoznaczności, nie definicja."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "110-112", "notes": "Wcześniej odczytany fragment WO-87/21 dotyczy przypisanego czynu, nie ustanawia ogólnej wykładni art. 27. Oryginału orzeczenia brak; nie stanowi niezależnego potwierdzenia niniejszego podziału."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "754-784", "notes": "Odczytano wykaz pkt 1–6 i otaczające objaśnienie o pośrednictwie innej osoby oraz bezwyjątkowym skutku w ujęciu autora. To ten sam autor co SRC-01, więc nie jest to niezależne potwierdzenie."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "173-185", "notes": "Lokalny tekst art. 27 pkt 1–6; sprawdzono wszystkie alternatywy i warunek jednoczesnych czynności dla tego samego klienta w pkt 4."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "47; 93-123", "notes": "Wcześniej sprawdzony kontekst ustawy o pomocy prawnej i wykonywaniu zawodu; nie stanowi odrębnej definicji relacji osobistej lub zależności z art. 27."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "104-113", "notes": "Wtórna lista konfiguracji art. 27 pkt 2–6, użyta jako kontrola orientacyjna; nie jest niezależnym źródłem wykładni."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "175-190", "notes": "Wcześniej odczytane wtórne omówienie pojedynczego WO-87/21 przy art. 30; nie dostarcza ogólnego testu bliskości lub zależności z art. 27."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały krótki glosariusz sprawy tej samej i związanej, użyty jedynie jako kontekst; nie rozstrzyga znaczeń relacji w art. 27."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Cały krótki glosariusz klienta aktualnego i byłego, użyty jako kontekst odróżniający; nie stanowi testu art. 27."}
    ],
    "meanings": meanings,
    "records": records,
    "relations": [],
    "gaps": [
        {"id": "OBS-048-G01", "issue": "Brak ekspertckiego rozstrzygnięcia, czy komentatorskie ujęcie art. 27 jako wyłączenia bez dalszej oceny należy przyjąć, przy zachowaniu literalnych elementów poszczególnych punktów. Nie rozstrzygam tego poglądu. Otwarte pytania o bliskoznaczność, pozytywne cechy bliskich stosunków i zależność znajdują się już w ON-P02, OBS-005-Q01 i OBS-058-Q01.", "needed": "Odpowiedź eksperta dotycząca statusu i zakresu argumentu komentatora, bez zastępowania przesłanek z art. 27 wspólną definicją relacji."}
    ],
    "questions": [],
    "self_check": "Opracowałem mapę punktu S1-K2-00 i rozdzieliłem dwie nowe, źródłowo udokumentowane tezy komentatora od normy art. 27. Każdy cytat w nowych rekordach pobrano bezpośrednio z dokładnie wskazanych wierszy SRC-01. Sprawdziłem dziewięć pozycji manifestu w zakresach podanych w coverage; zakresy inne niż SRC-01, SRC-03 i SRC-04 są wcześniejszą, ograniczoną lekturą i nie służą jako samodzielne dowody nowych tez. Pytania o relacje i warunki pkt 4 odsyłam do istniejących kart, nie powielam. Oryginałów cytowanych publikacji autora ani WO-87/21 nie weryfikowałem; brak tego oryginału nie jest nowym pytaniem tej karty. To samokontrola wykonawcy, nie odbiór Astry."
}

out = TASK / "wynik.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
kolejka.validate_result(state, job, result)
print(json.dumps({"validated": True, "path": str(out), "records": len(records), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "attempt_id": attempt_id}, ensure_ascii=False))
