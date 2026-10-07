# System wspomagania oceny konfliktu interesów (radcowie prawni)

## Koncepcja architektoniczna — podejście hybrydowe (LLM + model formalny)

---

## 1. Założenia wstępne

Projekt dotyczy stworzenia narzędzia wspomagającego radców prawnych w ocenie, czy dany stan faktyczny może prowadzić do konfliktu interesów.

### Kluczowe założenia:

- Użytkownikiem jest **profesjonalista (radca prawny)**:
  - posiada świadomość prawną,
  - zna przepisy:
    - ustawy o radcach prawnych,
    - kodeksu etyki radcy prawnego.
- Narzędzie ma charakter:
  - **wspomagający (decision-support)**, nie autonomiczny,
  - ukierunkowany na **analizę i ocenę ryzyka**, nie tylko binarne rozstrzygnięcia.
- System powinien:
  - rozpoznawać przypadki **oczywiste (zero-jedynkowe)**,
  - identyfikować przypadki **ryzykowne / niejednoznaczne**,
  - wskazywać **braki danych i konieczność dalszej analizy**.

---

## 2. Problem podejścia „if-then"

Dotychczasowy model oparty na logice:

> „jeśli A, to B"

jest niewystarczający, ponieważ:

- zakłada zamknięty katalog przypadków,
- nie radzi sobie z:
  - relacjami między podmiotami,
  - kontekstem czasowym,
  - stopniem powiązań,
  - niepełnością danych,
- prowadzi do:
  - sztucznego dopasowywania odpowiedzi przez użytkownika,
  - utraty jakości danych wejściowych.

---

## 3. Docelowe podejście: model hybrydowy

System powinien łączyć:

### 3.1. Warstwę językową (LLM)

- analiza swobodnego opisu,
- strukturyzacja danych,
- generowanie hipotezy.

### 3.2. Warstwę formalną (model kryteriów)

- walidacja kompletności analizy,
- kontrola logiczna,
- ocena poziomu ryzyka.

---

## 4. Architektura systemu

### 4.1. Warstwa wejścia

Użytkownik może:

- wprowadzić:
  - swobodny opis stanu faktycznego,
- opcjonalnie:
  - odpowiedzieć na pytania pomocnicze.

> Brak sztywnego formularza jako jedynej ścieżki.

---

### 4.2. Warstwa ekstrakcji (LLM)

Model przekształca opis w strukturę danych:

- podmioty i ich role,
- relacje między podmiotami,
- typ sprawy,
- historia relacji,
- potencjalne źródła informacji poufnych,
- stopień powiązania spraw,
- elementy nieustalone.

---

### 4.3. Warstwa pytań uzupełniających

System generuje:

- pytania opcjonalne,
- pytania ukierunkowane na:
  - kluczowe luki informacyjne,
  - elementy decyzyjne.

Zasada:

- brak odpowiedzi ≠ błąd,
- brak odpowiedzi = czynnik ryzyka.

---

### 4.4. Warstwa wstępnej oceny (LLM)

Model generuje:

- wstępną kwalifikację:
  - brak konfliktu / ryzyko / konflikt,
- uzasadnienie,
- listę przesłanek,
- poziom pewności,
- wskazanie braków.

---

### 4.5. Warstwa walidacji (model formalny)

Kluczowy komponent systemu.

Nie ocenia „czy odpowiedź jest prawdziwa", tylko:

- czy analiza jest:
  - kompletna,
  - logiczna,
  - spójna.

Sprawdza m.in.:

- pokrycie wszystkich kategorii analizy,
- brak sprzeczności,
- brak „halucynowanych" faktów,
- poprawne oznaczenie braków danych,
- zgodność wniosku z przesłankami.

---

### 4.6. Pętla iteracyjna

Jeśli walidacja nie przejdzie:

- system:
  - wskazuje braki,
  - generuje dodatkowe pytania,
- użytkownik:
  - uzupełnia dane (opcjonalnie),
- proces jest powtarzany.

> System musi dopuszczać stan „akceptowalnej niepewności".

---

### 4.7. Warstwa wyniku

Użytkownik otrzymuje:

- klasyfikację:
  - brak konfliktu,
  - potencjalny konflikt,
  - wysoki poziom ryzyka,
  - konflikt (przypadek oczywisty),
- uzasadnienie,
- kluczowe przesłanki,
- brakujące dane,
- rekomendację dalszych działań.

---

## 5. Obsługa przypadków zero-jedynkowych

### 5.1. Baza twardych reguł

Źródła:

- przepisy prawa,
- kodeks etyki,
- orzecznictwo dyscyplinarne.

Zastosowanie:

- automatyczne oznaczenie:
  - „konflikt istnieje",
  - „niedopuszczalne działanie".

> Priorytet nad analizą LLM.

---

### 5.2. Warstwa analogii (LLM + baza przypadków)

- dopasowanie do znanych stanów faktycznych,
- wskazanie podobieństw.

---

## 6. Struktura odpowiedzi (klucz do skalowalności i badań)

Odpowiedź musi być **ustrukturyzowana i porównywalna**.

### Schemat danych wyjściowych:

```json
{
  "entities": [],
  "roles": [],
  "relationships": [],
  "matter_type": "",
  "confidential_information_risk": "",
  "adversity_risk": "",
  "successive_representation_risk": "",
  "organizational_barriers": "",
  "missing_information": [],
  "analysis_completeness": "",
  "risk_level": "",
  "conflict_classification": "",
  "justification": "",
  "confidence_level": ""
}
```

### Opis pól:

| Pole | Opis | Typ |
|---|---|---|
| `entities` | Lista podmiotów zidentyfikowanych w stanie faktycznym (radca, klienci, osoby najbliższe, strony przeciwne, wspólnicy kancelarii) | `array<Entity>` |
| `roles` | Role przypisane podmiotom (klient aktualny, klient były, pełnomocnik, obrońca, doradca, strona przeciwna, mediator, biegły, świadek, osoba najbliższa) | `array<Role>` |
| `relationships` | Relacje między podmiotami (powiązanie rodzinne, zawodowe, zależność, bliskie stosunki, przeciwnik procesowy, wspólnik kancelarii) | `array<Relationship>` |
| `matter_type` | Typ sprawy (karna, cywilna, administracyjna, rodzinna, korporacyjna, dyscyplinarna, inne) | `string` |
| `confidential_information_risk` | Ocena ryzyka naruszenia tajemnicy zawodowej — odwołanie do art. 26 ust. 1 KERP, art. 3 ust. 3–5 u.r.p. | `string \| enum` |
| `adversity_risk` | Ocena ryzyka sprzeczności interesów w sensie materialnym — odwołanie do art. 28–30 KERP | `string \| enum` |
| `successive_representation_risk` | Ocena ryzyka wynikającego z uprzedniego świadczenia pomocy prawnej — odwołanie do art. 28 ust. 3, art. 29 ust. 1 pkt 2 KERP | `string \| enum` |
| `organizational_barriers` | Ocena istnienia barier organizacyjnych (chinese wall) — odwołanie do art. 26a ust. 2 KERP | `string \| enum` |
| `missing_information` | Lista brakujących informacji kluczowych dla oceny | `array<string>` |
| `analysis_completeness` | Stopień kompletności analizy (pełna / częściowa / niedostateczna) | `enum` |
| `risk_level` | Zagregowany poziom ryzyka (brak / niski / średni / wysoki / krytyczny) | `enum` |
| `conflict_classification` | Klasyfikacja końcowa (brak konfliktu / potencjalny konflikt / wysoki poziom ryzyka / konflikt oczywisty) | `enum` |
| `justification` | Uzasadnienie tekstowe z odwołaniem do przepisów | `string` |
| `confidence_level` | Poziom pewności analizy (wysoki / średni / niski) | `enum` |

---

## 7. Diagram przepływu systemu

```
┌─────────────────────────────────────────────────────┐
│                 WARSTWA WEJŚCIA                     │
│  Swobodny opis stanu faktycznego                   │
│  + opcjonalne odpowiedzi na pytania pomocnicze      │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│              WARSTWA EKSTRAKCJI (LLM)               │
│  Identyfikacja: podmioty, role, relacje, typ sprawy │
│  Strukturyzacja danych → JSON                       │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│         TWARDE REGUŁY (priorytet)                   │
│  art. 27 pkt 1–6   → zakaz bezwzględny              │
│  art. 28 ust. 2    → zakaz bezwzględny              │
│  art. 28 ust. 3    → zakaz bezwzględny              │
│  Jeśli dopasowanie → KONFLIKT (oczywisty)           │
└──────────┬──────────────────────┬───────────────────┘
           │ TAK                  │ NIE / NIEJEDNOZNACZNE
           ▼                      ▼
┌──────────────────┐  ┌──────────────────────────────┐
│ WYNIK: KONFLIKT  │  │  WARSTWA WSTĘPNEJ OCENY (LLM)│
│ (przypadek       │  │  Analiza: art. 26, 28 ust.1, │
│  oczywisty)      │  │  29, 30, 26a KERP            │
└──────────────────┘  │  Generowanie hipotezy        │
                      └──────────────┬───────────────┘
                                     │
                                     ▼
                      ┌──────────────────────────────┐
                      │  WARSTWA WALIDACJI (formalny) │
                      │  Kompletność? Spójność?       │
                      │  Brak halucynacji?             │
                      └──────┬───────────┬───────────┘
                             │ OK        │ BRAKI
                             ▼           ▼
                      ┌────────────┐ ┌──────────────┐
                      │   WYNIK    │ │   PĘTLA      │
                      │  KOŃCOWY   │ │  ITERACYJNA  │
                      │            │ │  Pytania     │◄──┐
                      └────────────┘ │  uzupełniające│   │
                                     └──────┬───────┘   │
                                            │           │
                                            ▼           │
                                     Użytkownik ────────┘
                                     uzupełnia dane
                                     (opcjonalnie)
```

---

## 8. Mapowanie warstw na przepisy

| Warstwa systemu | Przepisy KERP | Przepisy u.r.p. |
|---|---|---|
| Twarde reguły — zakazy bezwzględne | art. 27 pkt 1–6, art. 28 ust. 2–3 | art. 15, art. 26 |
| Ocena tajemnicy zawodowej | art. 9, 15–16, 26 ust. 1 | art. 3 ust. 3–6 |
| Ocena niezależności | art. 7, 26 ust. 1 | art. 13 |
| Ocena sprzeczności interesów | art. 28 ust. 1, art. 29, art. 30 | — |
| Ocena bariery organizacyjnej | art. 26a ust. 2 | art. 8 (formy) |
| Mechanizm zgody klienta | art. 5 pkt 9, art. 29 ust. 2, art. 26a ust. 2 | — |
| Obowiązek proceduralny (badanie) | art. 30a ust. 1–3 | art. 22 ust. 1–2 |
| Odpowiedzialność za naruszenie | art. 3 ust. 1 | art. 64–65 |

---

## 9. Wymagania warstwy LLM — hosting i adapter

### 9.1. Wymaganie EU-hosting (RODO)

Dane wejściowe do systemu (opisy stanów faktycznych, dane podmiotów) są danymi osobowymi w rozumieniu RODO. Model LLM wywołany przez system musi być hostowany na serwerach zlokalizowanych w UE.

**Niedopuszczalne:** przekazywanie danych do modeli hostowanych poza UE bez umownych gwarancji data residency.

**Dopuszczalne konfiguracje:**

| Provider | Wariant | Region |
|---|---|---|
| OpenAI | GPT Enterprise | EU (umowa data residency) |
| Microsoft Azure | Azure OpenAI Service | EU (West Europe, North Europe i in.) |
| Amazon AWS | Bedrock + modele Anthropic | EU (np. eu-west-1) |
| Mistral AI | API / wdrożenie | Francja (UE) |

---

### 9.2. Adapter provider-agnostic

Warstwa LLM jest oddzielona od logiki aplikacji przez interfejs/adapter. Żadna część kodu poza adapterem nie zna konkretnego providera.

**Interfejs adaptera** (pseudokod):

```python
class LLMAdapter:
    def extract(self, system_prompt: str, user_input: str) -> dict: ...
    def evaluate(self, system_prompt: str, structured_input: dict) -> dict: ...
```

**Fabryka:**

```python
client = LLMClient.create(provider=os.getenv("LLM_PROVIDER"))
```

**Konfiguracja środowiskowa:**

```
LLM_PROVIDER=openai          # openai | azure | bedrock | mistral
LLM_API_KEY=...
LLM_MODEL_NAME=gpt-4o
LLM_ENDPOINT_URL=...         # wymagane dla Azure i Bedrock
```

---

### 9.3. Wymagania dla systemu promptów (etap 4)

- Prompty nie mogą zakładać API-specyficznych mechanizmów (np. OpenAI function calling) bez jawnego fallbacku dla innych providerów.
- Output zawsze w formacie JSON zgodnym ze schematem z sekcji 6 — niezależnie od providera.
- Zestaw testów (etap 4.4) musi być uruchamialny na minimum dwóch różnych providerach przed uznaniem promptu za gotowy.
