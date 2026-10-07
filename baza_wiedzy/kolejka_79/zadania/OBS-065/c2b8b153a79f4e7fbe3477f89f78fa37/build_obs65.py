import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
TASK_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "OBSIL" / "narzedzia" / "kolejka_pojec"))
import kolejka

state = kolejka.load(ROOT / "OBSIL" / "baza_wiedzy" / "kolejka_79")
job = kolejka.get_job(state, "OBS-065")
attempt = job["attempts"][-1]

result = {
    "task_id": attempt["id"],
    "concept_id": "OBS-065",
    "label": "udział w rozstrzygnięciu sprawy",
    "points": ["S1-K2-03"],
    "scope": (
        "Zakres ograniczono do art. 27 pkt 3: udziału osoby najbliższej albo osoby pozostającej z jakichkolwiek przyczyn w stosunku zależności z radcą w rozstrzygnięciu sprawy. "
        "Norma i pogląd autora o węższym zakresie pkt 3 względem udziału radcy w sprawie z pkt 1 są już pokryte przez ON-R03 i ON-R07. Autor wskazuje, że chodzi o osobę najbliższą lub zależną od radcy, a nie o udział samego radcy. "
        "Przejrzane materiały nie wyznaczają pozytywnego testu rodzaju lub stopnia czynności tej osoby, które stanowią udział w rozstrzygnięciu. Pytanie OBS-065-Q01 dotyczy tylko tego elementu czynnościowego. Nie powtarza OBS-058-Q01 o cechach i kierunku zależności ani ON-P02 o bliskoznaczności kategorii. "
        "Korpus nie daje podstaw do automatycznego przeniesienia szerokich przykładów udziału radcy z pkt 1 na pkt 3. Opracowanie jest częściowe i opiera się na wskazanych niżej zakresach, nie na pełnej lekturze wszystkich dokumentów."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": ["ON-R03", "ON-R07"],
    "coverage": [
        {"source_id": "SRC-01", "status": "SPRAWDZONY", "read_ranges": "816-836", "notes": "Nowe lustro komentarza. Wczytano akapit o szerokim udziale z pkt 1, podział sytuacji z art. 27, fragment o bliskoznaczności oraz akapit 832 o węższym pkt 3 i kierunku zależności. Wnioski autora nie są tekstem normy."},
        {"source_id": "SRC-02", "status": "CZESCIOWY", "read_ranges": "1-112", "notes": "Przejrzano wybór orzeczeń; nie stwierdzono przytoczonego rozstrzygnięcia ani pozytywnego testu udziału osoby zależnej w rozstrzygnięciu z pkt 3. Wybór nie zastępuje oryginałów orzeczeń."},
        {"source_id": "SRC-03", "status": "SPRAWDZONY", "read_ranges": "754-784", "notes": "Autor wylicza treść pkt 3 i objaśnia ogólny zakres art. 27. Fragment nie określa cech czynności udziału osoby z pkt 3. Ten sam autor co SRC-01, brak niezależnego potwierdzenia."},
        {"source_id": "SRC-04", "status": "SPRAWDZONY", "read_ranges": "169-185", "notes": "Sprawdzono brzmienie art. 27 w otoczeniu pkt 3. Przepis formułuje przesłankę, ale nie definiuje rodzaju czynności będących udziałem w rozstrzygnięciu."},
        {"source_id": "SRC-05", "status": "CZESCIOWY", "read_ranges": "461-462; wyszukanie odesłań do art. 27", "notes": "Sprawdzono wskazane odesłanie w u.r.p.; nie jest źródłem testu czynności z art. 27 pkt 3. Pozostałe przepisy ustawy nie były czytane w całości."},
        {"source_id": "SRC-06", "status": "SPRAWDZONY", "read_ranges": "99-114", "notes": "Zestawienie tekstu art. 27 potwierdza brzmienie pkt 3, bez jego objaśnienia. Nie jest odrębną opinią interpretacyjną."},
        {"source_id": "SRC-07", "status": "CZESCIOWY", "read_ranges": "63-83, w szczególności 79-81", "notes": "Przejrzano wpis do art. 27 pkt 1 o udziale samego radcy. Wpis pokazuje odrębny kontekst pkt 1, nie rozstrzyga czynnościowej granicy pkt 3 i nie został przeniesiony na tę przesłankę."},
        {"source_id": "SRC-08", "status": "SPRAWDZONY", "read_ranges": "1-35", "notes": "Przeczytano cały krótki słownik sprawy tej samej/związanej; nie dotyczy testu udziału w rozstrzygnięciu z pkt 3."},
        {"source_id": "SRC-09", "status": "SPRAWDZONY", "read_ranges": "1-37", "notes": "Przeczytano cały krótki słownik klienta aktualnego/byłego; nie dotyczy testu udziału w rozstrzygnięciu z pkt 3."}
    ],
    "meanings": [
        {
            "id": "OBS-065-M01",
            "context": "Bezwzględna przesłanka art. 27 pkt 3, gdy w rozstrzygnięciu sprawy uczestniczy osoba najbliższa radcy albo osoba pozostająca z jakichkolwiek przyczyn w stosunku zależności z radcą.",
            "description": "Normatywne brzmienie przesłanki należy odczytywać według ON-R03. Pogląd autora z ON-R07 ogranicza rozumienie udziału z pkt 3 względem udziału w sprawie z pkt 1, ponieważ pkt 3 dotyczy udziału osoby najbliższej lub zależnej od radcy, a nie samego radcy. Te istniejące tezy nie podają jednak dodatnich kryteriów rodzaju lub stopnia czynności tej osoby, które wystarczają do uznania udziału w rozstrzygnięciu. Przykłady przygotowania, czynności technicznych i kontroli z pkt 1 dotyczą udziału radcy i nie stanowią same przez się testu pkt 3.",
            "record_ids": ["ON-R03", "ON-R07"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [
        {
            "id": "OBS-065-G01",
            "issue": "Nie ustalono, jakie rodzaje działań lub jaki stopień wpływu osoby najbliższej albo zależnej oznaczają udział w rozstrzygnięciu sprawy z art. 27 pkt 3. Autor wyjaśnia, że pkt 3 jest węższy od udziału radcy w sprawie z pkt 1, lecz nie formułuje dodatniego testu. Przejrzany wybór orzeczeń nie dostarczył takiego testu.",
            "needed": "Ekspercka wykładnia lub bezpośrednio dotyczące pkt 3 źródła określające, czy i kiedy znaczenie ma udział w samym podejmowaniu decyzji, jej przygotowaniu albo inna postać oddziaływania. Należy zachować rozdział od pytania OBS-058-Q01 o zależność oraz od przykładów pkt 1."
        }
    ],
    "questions": [
        {
            "id": "OBS-065-Q01",
            "record_ids": ["ON-R03", "ON-R07"],
            "understanding": "Art. 27 pkt 3 wymaga udziału w rozstrzygnięciu sprawy osoby najbliższej albo osoby zależnej od radcy. Autor odróżnia tę przesłankę od szerszego udziału samego radcy w sprawie z pkt 1, ale przejrzany materiał nie podaje dodatniego testu czynnościowego dla pkt 3.",
            "variants": "Do rozstrzygnięcia pozostaje, czy przesłankę wiązać z udziałem w samym podejmowaniu decyzji, także z jej przygotowaniem lub innym oddziaływaniem, czy z węższą kategorią działań. Są to warianty pytania, nie stanowiska przypisane źródłom; przykłady odnoszące się do radcy w pkt 1 nie przesądzają odpowiedzi dla osoby z pkt 3.",
            "consequences": "Przyjęte kryterium określa, jakie fakty o roli osoby trzeciej trzeba ustalać obok jej relacji z radcą i może zmieniać zakres przypadków wyłączonych na podstawie art. 27 pkt 3.",
            "question": "Jakie konkretne czynności lub poziom udziału osoby najbliższej albo zależnej od radcy należy uznać za udział w rozstrzygnięciu sprawy w rozumieniu art. 27 pkt 3? Czy obejmuje to udział w przygotowaniu decyzji albo inne oddziaływanie, a jeśli tak, jakie są granice tego kryterium?",
            "needed": "Źródła lub wykładnia ekspercka bezpośrednio odnoszące się do czynnościowego zakresu art. 27 pkt 3. Pytanie jest odrębne od OBS-058-Q01 o kryteria zależności i ON-P02 o relacje między kategoriami osób."
        }
    ],
    "self_check": "Wynik mapuje normę na ON-R03 i pogląd autora na ON-R07 bez tworzenia powtórnego rekordu. Rozdzielono test udziału w rozstrzygnięciu od testu zależności (OBS-058-Q01) i historycznego pytania ON-P02. Nie przeniesiono przykładów szerokiego udziału radcy z pkt 1 na pkt 3. Zakres pokrycia źródeł podano według rzeczywiście sprawdzonych fragmentów; brak źródeł definiujących czynnościowy test został ujawniony. Walidacja techniczna nie jest odbiorem Astry. Operator pozostaje OCZEKUJE."
}

validated = kolejka.validate_result(state, job, result)
target = TASK_DIR / "wynik.json"
target.write_text(json.dumps(validated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"OK: {target}")
