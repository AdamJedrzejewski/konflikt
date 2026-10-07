import json
from pathlib import Path

task_dir = Path(__file__).parent
root = Path(r"C:\Users\adamj\Desktop\_KANCELARIA\OBSIL")
prior_path = root / "baza_wiedzy/kolejka_79/zadania/OBS-012/ac2eb027d2dc416bb60de826297ae6b5/wynik.json"
prior = json.loads(prior_path.read_text(encoding="utf-8"))
coverage = prior["coverage"]
for item in coverage:
    if item["source_id"] == "SRC-01":
        item["notes"] = "Ponownie wykorzystana lektura z OBS-012: komentarz autora do art. 30 ust. 1 (wiersze 1272-1276); odniesienie do interesu radcy/osoby najbliższej jest poglądem autora, a nie definicją dla wszystkich zawodów prawniczych."
    elif item["source_id"] == "SRC-03":
        item["notes"] = "Ponownie wykorzystana lektura z OBS-012: poradnik autora objaśnia relację interesów i próg ryzyka w art. 30 ust. 1 (wiersze 723-730); ten sam autor co SRC-01."
    elif item["source_id"] == "SRC-04":
        item["notes"] = "Ponownie wykorzystana lektura z OBS-012: lokalne brzmienie art. 30 ust. 1 (wiersz 209) wskazuje radcę i osobę najbliższą; nie rozszerzam go na inne zawody."

result = {
    "task_id": "76f7d3c8bc7e450298a220db8baf3e69",
    "concept_id": "OBS-017",
    "label": "interes prawnika",
    "points": ["S1-K1-00"],
    "scope": (
        "Punkt S1-K1-00 mapuję do lokalnego art. 30 ust. 1 KERP. W tym przepisie podmiotem jest radca prawny, a przepis osobno "
        "uwzględnia interes osoby mu najbliższej. Etykieta schematu „interes prawnika” nie stanowi podstawy do uogólnienia na "
        "adwokata, doradcę podatkowego ani inne zawody. OBS-012 odrębnie opisuje konfigurację interesu radcy wobec klienta oraz "
        "interesu osoby najbliższej wobec klienta; zachowuję ten podział. W zakresie interesu własnego radcy art. 15 u.r.p. wymienia "
        "własną sprawę jako podstawę wyłączenia, a komentarz łączy art. 30 z tym przepisem tylko „w pewnym zakresie” (OBS-018-R01/R02), "
        "nie jako pełną definicję. Znaczenie osoby najbliższej bierze się z art. 5 pkt 7 KERP (ON-R01); jej zastosowanie do art. 30 "
        "jest objaśnione przez autora (ON-R08), podczas gdy ON-R05 odtwarza samą normę art. 30. Nie powielam istniejącej interpretacji "
        "materialnej sprzeczności ani pytania o znaczne ryzyko z OBS-057-R03/OBS-057-Q01. Coverage wykorzystuje lekturę źródeł i kart "
        "w OBS-012 oraz wskazane tam konteksty; wynik pozostaje częściowy i nie ustala ogólnego znaczenia „interesu prawnika” poza "
        "zakresem radcy prawnego w lokalnym KERP."
    ),
    "completeness": "partial",
    "operator_status": "OCZEKUJE",
    "existing_record_refs": [
        "SP-R08", "ON-R05", "ON-R01", "ON-R08",
        "OBS-057-R03", "OBS-018-R01", "OBS-018-R02"
    ],
    "coverage": coverage,
    "meanings": [
        {
            "id": "OBS-017-M01",
            "context": "S1-K1-00, interes radcy prawnego wobec klienta, art. 30 ust. 1 KERP",
            "description": (
                "W lokalnym art. 30 ust. 1 interes własny wskazany w konfiguracji to interes radcy prawnego wobec klienta. "
                "Komentarz autora wiąże ten konflikt z oceną zbliżoną do materialnej sprzeczności, obejmującą konflikt rzeczywisty "
                "i potencjalny przy znacznym ryzyku; granice i nierozstrzygnięte kryteria są już opisane w OBS-057-R03 oraz "
                "OBS-057-Q01. Art. 15 u.r.p. i komentarz o jego częściowym dookreśleniu przez art. 30 nie ustanawiają pełnej, "
                "uniwersalnej definicji interesu prawnika (OBS-018-R01/R02). Zakres obejmuje radcę w KERP, nie inne zawody."
            ),
            "record_ids": ["SP-R08", "OBS-057-R03", "OBS-018-R01", "OBS-018-R02"]
        },
        {
            "id": "OBS-017-M02",
            "context": "S1-K1-00, odrębna konfiguracja interesu osoby najbliższej radcy wobec klienta",
            "description": (
                "Art. 30 ust. 1 obejmuje obok interesu radcy interes osoby mu najbliższej. Nie utożsamiam tych konfiguracji: "
                "ON-R01 odtwarza definicję osoby najbliższej z art. 5 pkt 7, ON-R08 zachowuje autorskie odniesienie tej definicji "
                "do art. 30, a ON-R05 odtwarza normę art. 30. Wspólny komentarzowy test konfliktu i znacznego ryzyka ma granice "
                "wskazane w OBS-057-R03/Q01. Etykieta „interes prawnika” nie przekształca interesu osoby najbliższej w interes "
                "samego radcy ani w ogólną kategorię dla innych zawodów."
            ),
            "record_ids": ["ON-R01", "ON-R08", "ON-R05", "OBS-057-R03"]
        }
    ],
    "records": [],
    "relations": [],
    "gaps": [],
    "questions": [],
    "self_check": (
        "Punkt S1-K1-00 mapuje do art. 30 ust. 1 KERP bez uogólniania na wszystkie zawody prawnicze. Zachowałem odrębnie interes radcy "
        "i interes osoby najbliższej, z właściwym przypisaniem definicji do ON-R01, objaśnienia do ON-R08 i normy do ON-R05. Wykorzystałem "
        "istniejące tezy OBS-012, OBS-018 i OBS-057, bez kopiowania rekordów lub pytań. Coverage odwołuje się do lektury z OBS-012. "
        "Status pozostaje OCZEKUJE na odbiór Astry."
    )
}

(task_dir / "wynik.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"written": "wynik.json", "records": 0, "questions": 0, "meanings": len(result["meanings"]), "sources": len(coverage)}))
