import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
TASK = ROOT / "baza_wiedzy" / "kolejka_79" / "zadania" / "OBS-037" / "b3e19a5142624a5387546e7c65eba012"
sys.path.insert(0, str(ROOT / "narzedzia" / "kolejka_pojec"))
import kolejka

state = kolejka.load(ROOT / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, "OBS-037")
attempt_id = job["attempts"][-1]["id"]

result = {
    "task_id": attempt_id,
    "concept_id": "OBS-037",
    "label": "osoba zainteresowana rozstrzygnięciem",
    "points": ["S1-K2-05"],
    "scope": "S1-K2-05 wymaga, aby radca był lub pozostawał w bliskich stosunkach z jedną z dwóch alternatywnych osób: przeciwnikiem klienta albo osobą zainteresowaną niekorzystnym dla klienta rozstrzygnięciem; norma jest już ujęta w OBS-043-R01. OBS-043-Q01 dotyczy granicy pojęcia przeciwnika, procesowego kontekstu i relacji do drugiej alternatywy. OBS-005-Q01 pyta o pozytywne cechy bliskich stosunków, a OBS-009-Q01 o ich czasowy aspekt. Nie ponawiam tych kwestii. Osobny brak dotyczy tego, jakie zainteresowanie wynikiem czyni inną osobę „zainteresowaną” w rozumieniu art. 27 pkt 5. D 43/2016 opisuje relację S (2) z obwinioną, ale nie ustala, że S (2) była zainteresowana niekorzystnym wynikiem dla klientów obwinionej (OBS-005-R01). Wzmianka o bezpośrednim zainteresowaniu radcy w WO-87/21 dotyczy jego własnego interesu w kontekście art. 30, nie daje automatycznie definicji osoby z art. 27 pkt 5. Pytanie o samo pojęcie niekorzystnego rozstrzygnięcia może być skoordynowane z następnym OBS-027, lecz tutaj ograniczam je do cech interesu osoby. Karta jest częściowa, ponieważ przejrzane materiały nie podają pozytywnego testu tej alternatywy.",
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["OBS-043-R01", "OBS-005-R01"],
    "coverage": [
        {"source_id": "SRC-01", "status": "CZESCIOWY", "read_ranges": "792; 804-828; 848-860; 1240-1244", "notes": "W. 792 zawiera komentowany zapis normy; w. 804–828 ogólne objaśnienie art. 27 i pogląd o bliskoznaczności, bez dodatniego testu zainteresowania. W. 848–860 wtórnie opisuje D 43/2016 i D 33/18; D 43 nie kwalifikuje S (2) jako osoby zainteresowanej. W. 1240–1244 relacjonuje interes G sp. z o.o. w odrębnej sprawie, bez tezy o art. 27 pkt 5."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "110-112", "notes": "WO-87/21: fragment opisuje bezpośrednie zainteresowanie samego radcy w konfiguracji art. 30. Nie traktuję go jako wykładni drugiej alternatywy art. 27 pkt 5; atrybucja relacjonowanych zdań pozostaje ograniczona."},
        {"source_id": "SRC-03", "status": "CZESCIOWY", "read_ranges": "754-784", "notes": "Odczytano wykaz art. 27 i ogólny opis oddziaływania przez inną osobę; tekst nie objaśnia dodatnich cech jej zainteresowania wynikiem. Jest to opracowanie tego samego autora co SRC-01."},
        {"source_id": "SRC-04", "status": "CZESCIOWY", "read_ranges": "183", "notes": "Lokalny tekst art. 27 pkt 5 wymienia alternatywnie przeciwnika klienta i osobę zainteresowaną niekorzystnym dla klienta rozstrzygnięciem, ale nie definiuje zainteresowania."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "47; 93-123", "notes": "Wcześniej sprawdzony kontekst ustawowej pomocy prawnej i wykonywania zawodu; w tych zakresach nie znaleziono definicji osoby zainteresowanej wynikiem w art. 27 pkt 5."},
        {"source_id": "SRC-06", "status": "CZESCIOWY", "read_ranges": "111", "notes": "Wtórne zestawienie powtarza brzmienie pkt 5 bez objaśnienia kryterium zainteresowania."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "185-189", "notes": "Wtórne omówienie WO-87/21 mówi o bezpośrednim zainteresowaniu samego obwinionego przy jego własnym interesie; nie jest to definicja z art. 27 pkt 5."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Cały krótki glosariusz sprawy tej samej i związanej; nie zawiera testu zainteresowania osoby wynikiem."},
        {"source_id": "SRC-09", "status": "CZESCIOWY", "read_ranges": "9-20", "notes": "Odczytano fragmenty o klientach byłych i ochronie po zakończeniu współpracy, które dotyczą innego kontekstu. Nie określają zainteresowania osoby z art. 27 pkt 5."}
    ],
    "meanings": [
        {
            "id": "OBS-037-M01",
            "context": "S1-K2-05, art. 27 pkt 5 KERP: druga alternatywa obok przeciwnika klienta",
            "description": "Norma odrębnie wymienia osobę zainteresowaną niekorzystnym dla klienta rozstrzygnięciem (OBS-043-R01). Sam status strony, osoby najbliższej, osoby mającej interes własny radcy albo osoby powiązanej z klientem nie przesądza, że spełnia ona tę alternatywę. Przejrzane przykłady nie dostarczają dodatniego testu: w D 43/2016 nie ustalono zainteresowania S (2) niekorzystnym wynikiem dla obsługiwanych klientów (OBS-005-R01), a zainteresowanie radcy we własnej sprawie z WO-87/21 dotyczy odrębnego kontekstu art. 30. OBS-043-Q01 zachowuje pytanie o przeciwnika i relację między alternatywami; niniejsze pytanie dotyczy pozytywnych cech zainteresowania.",
            "record_ids": ["OBS-043-R01", "OBS-005-R01"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {"id": "OBS-037-G01", "issue": "Lokalny art. 27 pkt 5 i przejrzane objaśnienia nie określają, jakie fakty lub rodzaj interesu czynią osobę zainteresowaną niekorzystnym dla klienta rozstrzygnięciem. D 43/2016 nie kwalifikuje S (2) w ten sposób; WO-87/21 odnosi się do bezpośredniego interesu samego radcy przy art. 30 i nie wypełnia tej luki.", "needed": "Ekspercka wykładnia kryterium zainteresowania innej osoby w art. 27 pkt 5, odrębnie od pojęcia przeciwnika klienta, cech bliskich stosunków i samej niekorzystności wyniku."}
    ],
    "questions": [
        {
            "id": "OBS-037-Q01",
            "record_ids": ["OBS-043-R01", "OBS-005-R01"],
            "understanding": "Art. 27 pkt 5 wymienia osobę zainteresowaną niekorzystnym wynikiem jako alternatywę wobec przeciwnika klienta. Materiał nie wyjaśnia, jakie powiązanie z wynikiem lub interes tej osoby jest wystarczające. D 43/2016 nie wskazuje, że S (2) miała taki status. OBS-043-Q01 dotyczy przede wszystkim znaczenia przeciwnika i granicy między alternatywami, a OBS-005-Q01 dotyczy bliskości, więc nie rozstrzygają dodatniego testu zainteresowania.",
            "variants": "Do rozważenia pozostaje, czy wymagana jest bezpośrednia, osobista lub prawna korzyść/strata tej osoby, czy wystarczy także inna, w tym pośrednia, więź z wynikiem. Materiał nie określa, czy zainteresowanie ma być obiektywne, aktualne lub bezpośrednie; nie przyjmuję żadnego z tych wymogów jako gotowej reguły.",
            "consequences": "Odpowiedź pozwoli ustalić, kto poza przeciwnikiem klienta może wejść w drugą alternatywę art. 27 pkt 5, bez utożsamiania jej z interesem samego radcy z art. 30 ani z testem bliskich stosunków.",
            "question": "Jakie cechy związku osoby z wynikiem sprawy pozwalają uznać ją za „zainteresowaną niekorzystnym dla klienta rozstrzygnięciem” w art. 27 pkt 5? Czy potrzebny jest interes bezpośredni i osobisty, czy może wystarczyć interes pośredni lub innego rodzaju, i jak odróżnić tę kategorię od przeciwnika klienta? Proszę oddzielić kryterium zainteresowania od znaczenia samej niekorzystności rozstrzygnięcia.",
            "needed": "Ekspercka wykładnia drugiej alternatywy art. 27 pkt 5 oraz, jeśli potrzebne, przykłady graniczne inne niż nieustalony status S (2) w D 43/2016. Definicja „niekorzystnego rozstrzygnięcia” może być koordynowana z OBS-027, bez utożsamienia obu pytań."
        }
    ],
    "self_check": "Nie utworzyłem nowych rekordów, ponieważ literalna alternatywa jest już ujęta w OBS-043-R01, a przejrzane źródła nie dostarczyły nowego dodatniego testu. Pytanie jest ograniczone do statusu osoby zainteresowanej i nie powtarza pytania o pozytywne cechy bliskości ani o znaczenie przeciwnika. D 43/2016 i WO-87/21 zachowałem jako przykłady z odrębnych, nieprzesądzających kontekstów. Pokrycie dziewięciu źródeł i ograniczenia lektury wskazano w coverage. To samokontrola wykonawcy, nie odbiór Astry."
}

out = TASK / "wynik.json"
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
kolejka.validate_result(state, job, result)
print(json.dumps({"validated": True, "path": str(out), "records": len(result["records"]), "questions": len(result["questions"]), "gaps": len(result["gaps"]), "attempt_id": attempt_id}, ensure_ascii=False))
