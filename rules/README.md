# Rules — Baza reguł systemu OBSIL

> **UWAGA:** Nie modyfikuj reguł bez konsultacji prawnej. Każda zmiana musi wynikać z przepisów źródłowych (KERP, u.r.p.) i być zweryfikowana przez radcę prawnego.

---

## Cel

Katalog `rules/` zawiera sformalizowane reguły oceny konfliktu interesów radcy prawnego. Reguły są zapisane w formacie JSON i stanowią bazę wiedzy dla silnika reguł (rule engine) systemu OBSIL.

## Struktura katalogu

```
rules/
├── index.json          ← Główny indeks, strategia ewaluacji
├── hard/               ← Zakazy bezwzględne (nieuchylalne)
│   ├── index.json      ← Indeks z kolejnością ewaluacji
│   └── KERP-*.json     ← Poszczególne reguły
├── soft/               ← Reguły uchylalne (za zgodą klienta)
│   ├── index.json      ← Indeks z kolejnością ewaluacji
│   └── KERP-*.json     ← Poszczególne reguły
└── ontology/           ← Słownik podmiotów, relacji, typów spraw
    └── entities.json
```

## Jak działa rule engine

Ewaluacja przebiega dwuetapowo:

1. **Hard rules** (zakazy bezwzględne) — ewaluowane sekwencyjnie. Jeśli którakolwiek reguła pasuje → wynik: `CONFLICT`, analiza zatrzymana.
2. **Soft rules** (reguły uchylalne) — ewaluowane jeśli hard rules nie dały dopasowania. Wynik: `CONFLICT_WAIVABLE` (możliwy za zgodą) lub `CONFLICT` (brak mechanizmu zgody mimo że reguła nie jest w hard/).

Strategia: **first match** dla hard rules, **sequential** dla soft rules (mogą się kumulować).

## Format pliku reguły

Każdy plik `KERP-*.json` zawiera następujące pola:

| Pole | Typ | Wymagane | Opis |
|------|-----|----------|------|
| `id` | string | tak | Unikalny identyfikator reguły (np. `KERP-27-1`) |
| `article` | string | tak | Artykuł źródłowy (np. `art. 27 pkt 1 KERP`) |
| `configuration` | string | nie | Konfiguracja konfliktu wg diagramu |
| `type` | string | tak | `absolute_prohibition` lub `conditional_prohibition` |
| `waivable` | boolean | tak | `false` = bezwzględny, `true` = uchylalny za zgodą |
| `description_pl` | string | tak | Opis reguły po polsku (dla prawnika) |
| `trigger` | object | nie | Warunki wstępne aktywacji reguły |
| `conditions` | array | tak | Warunki formalne (field/operator/value) |
| `result` | string | tak | `CONFLICT`, `CONFLICT_WAIVABLE` lub `NO_CONFLICT` |
| `result_classification` | string | nie | Klasyfikacja wyniku (np. `conflict_obvious`) |
| `confidence` | string | nie | Pewność dopasowania (`high`/`medium`/`low`) |
| `legal_basis` | array | tak | Lista przepisów stanowiących podstawę prawną |
| `waiver_conditions` | object | nie | Warunki uchylenia zakazu (dla reguł uchylalnych) |
| `notes` | string | nie | Notatki dodatkowe |

### Pole `waiver_conditions` (reguły uchylalne)

| Pole | Typ | Opis |
|------|-----|------|
| `requires_client_consent` | boolean | Czy wymagana zgoda klienta |
| `all_parties_must_consent` | boolean | Czy zgoda musi być od wszystkich stron |
| `blocked_if_criminal_defense` | boolean | Czy blokada przy obronie karnej |
| `requires_organizational_measures` | boolean | Czy wymagane rozwiązania organizacyjne (Chinese wall) |
| `no_unfair_advantage_required` | boolean | Czy wymagany brak nieuzasadnionej przewagi |
| `description_pl` | string | Opis warunków uchylenia po polsku |

### Pole `conditions` — format warunku

```json
{
  "field": "radca_prawny.prior_role_in_matter",
  "operator": "in",
  "value": ["arbiter", "mediator", "biegly"],
  "alternative": true
}
```

- `operator`: `eq`, `in`, `ne`, `contains`
- `alternative: true` — oznacza logikę OR (wystarczy jeden z warunków z tą flagą)

## Tabela reguł

### Hard rules (zakazy bezwzględne)

| ID | Artykuł | Konfiguracja | Waivable | Opis |
|----|---------|--------------|----------|------|
| KERP-27-1 | art. 27 pkt 1 KERP | konfiguracja_2 | nie | Udział jako organ władzy/ekspert |
| KERP-27-2 | art. 27 pkt 2 KERP | konfiguracja_2 | nie | Udział jako sędzia/asesor/ławnik |
| KERP-27-3 | art. 27 pkt 3 KERP | konfiguracja_2 | nie | Udział jako prokurator/funkcjonariusz |
| KERP-27-4 | art. 27 pkt 4 KERP | konfiguracja_2 | nie | Udział jako notariusz/komornik |
| KERP-27-5 | art. 27 pkt 5 KERP | konfiguracja_2 | nie | Sporządzenie dokumentu/opinii w sprawie |
| KERP-27-6 | art. 27 pkt 6 KERP | konfiguracja_2 | nie | Pokrewieństwo/powinowactwo ze stroną |
| KERP-28-2 | art. 28 ust. 2 KERP | konfiguracja_3 | nie | Pełnomocnictwo po obu stronach |
| KERP-28-3 | art. 28 ust. 3 KERP | konfiguracja_4 | nie | Pełnomocnictwo przeciwko byłemu klientowi |
| KERP-26-tajemnica | art. 26 KERP | klauzula_generalna | nie | Zagrożenie tajemnicy zawodowej |
| KERP-26-niezaleznosc | art. 26 KERP | klauzula_generalna | nie | Zagrożenie niezależności |
| KERP-26-przewaga | art. 26 KERP | klauzula_generalna | nie | Nieuprawniona przewaga informacyjna |
| KERP-30-1 | art. 30 ust. 1 KERP | konfiguracja_1 | nie | Interes własny radcy/osoby najbliższej |

### Soft rules (reguły uchylalne/warunkowe)

| ID | Artykuł | Konfiguracja | Waivable | Opis |
|----|---------|--------------|----------|------|
| KERP-30-1 | art. 30 ust. 1 KERP | konfiguracja_1 | nie | Interes własny radcy/osoby najbliższej |
| KERP-28-1 | art. 28 ust. 1 KERP | konfiguracja_3_pelnomocnictwo | nie | Sprzeczne interesy — pełnomocnictwo |
| KERP-29-1-pkt1 | art. 29 ust. 1 pkt 1 KERP | konfiguracja_3_doradztwo | tak | Sprzeczne interesy — doradztwo |
| KERP-29-1-pkt2 | art. 29 ust. 1 pkt 2 KERP | konfiguracja_4_doradztwo | tak | Doradztwo przeciw byłemu klientowi |
| KERP-26a | art. 26a KERP | konfiguracja_kancelaryjna | tak | Konflikt kancelaryjny (imputowany) |

## Jak dodać nową regułę

Przy nowelizacji KERP lub u.r.p.:

1. Zidentyfikuj przepis źródłowy i określ czy zakaz jest bezwzględny czy uchylalny
2. Utwórz plik `KERP-{artykuł}.json` w odpowiednim katalogu (`hard/` lub `soft/`)
3. Wypełnij wszystkie wymagane pola zgodnie z formatem powyżej
4. Dodaj wpis do `index.json` w odpowiednim katalogu (z priorytetem)
5. Zaktualizuj `rules/index.json` (pole `total_hard_rules` lub `total_soft_rules`)
6. Uruchom walidator: `python3 scripts/validate_rules.py`
7. Uzyskaj akceptację radcy prawnego przed mergem

## Mapowanie na konfiguracje diagramu

| Konfiguracja | Artykuły | Katalog |
|---|---|---|
| `konfiguracja_1` | art. 30 ust. 1 | `hard/` + `soft/` |
| `konfiguracja_2` | art. 27 pkt 1-6 | `hard/` |
| `konfiguracja_3` | art. 28 ust. 1-2, art. 29 ust. 1 pkt 1 | `hard/` + `soft/` |
| `konfiguracja_4` | art. 28 ust. 3, art. 29 ust. 1 pkt 2 | `hard/` + `soft/` |
| `klauzula_generalna` | art. 26 | `hard/` |
| `konfiguracja_kancelaryjna` | art. 26a | `soft/` |

## Źródła prawne

- **KERP** — Kodeks Etyki Radcy Prawnego (uchwała KRRP nr 3/2014, tekst jednolity 2023)
- **u.r.p.** — Ustawa z dnia 6 lipca 1982 r. o radcach prawnych (tj. 2024)
- **k.k.** — Kodeks karny (art. 115 § 11 — definicja osoby najbliższej)

---

*Ostatnia aktualizacja: 2026-05-04*
