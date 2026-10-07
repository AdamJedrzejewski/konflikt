# Moduł badania konfliktu interesów – założenia funkcjonalne

> **Aktualizacja 2026-05-29** — dokument zsynchronizowany z pipeline 3.0 (single-shot LLM). Wcześniejsza wersja opisywała model dwufazowy (schematyczna + niezależna analiza + komparator) z pipeline 2.0; został on wycofany — powody w `ADR-006`.

## 1. Cel modułu
Moduł służy wsparciu radcy prawnego w ocenie istnienia konfliktu interesów, w szczególności w stanach faktycznych o niejednoznacznym charakterze. Narzędzie ma charakter **decision-support** — radca prawny pozostaje decydentem.

Założeniem jest:
- uporządkowanie opisu stanu faktycznego,
- ocena stanu faktycznego względem pełnego katalogu artykułów KERP dotyczących konfliktu interesów (art. 26–30a),
- ograniczenie ryzyka błędnej kwalifikacji wynikającej z nieprecyzyjnych odpowiedzi.

---

## 2. Struktura procesu (pipeline 3.0 — single-shot)

Filozofia: **jedno wywołanie LLM z pełnym katalogiem KERP w prompcie**. Bez etapu ekstrakcji, bez rule engine, bez sekwencyjnej ewaluacji per artykuł, bez komparatora dwóch ścieżek.

### Etap 1 – wprowadzenie danych
Użytkownik wprowadza opis stanu faktycznego (swobodna forma, min. 50 znaków).

### Etap 2 – analiza (LLM, single-shot)
Model otrzymuje w jednym prompcie:
- instrukcje systemowe (rola, klasyfikacja, poziom ryzyka i pewności),
- pełny katalog 9 artykułów KERP (tekst + przesłanki stosowania),
- **warstwę kontekstu stałego** (glosariusz pojęć, wybrane przepisy źródłowe, algorytm i przykłady — zob. sekcja 4, w budowie),
- stan faktyczny użytkownika.

Model w jednej odpowiedzi zwraca: identyfikację stron i relacji, ewaluację każdego z 9 artykułów (`article_evaluations`) oraz agregację (klasyfikacja, ryzyko, pewność, uzasadnienie, podstawa prawna, braki informacyjne).

### Etap 3 – prezentacja wyniku
Frontend pobiera wynik (polling) i prezentuje klasyfikację wraz z uzasadnieniem. W razie wyjątku w pipeline status nadal kończy się jako `complete`, a wynik zawiera czytelny komunikat błędu (`mode = error_fallback`) — frontend nigdy nie „wisi".

> **Braki informacyjne:** model nie pauzuje na pytania uzupełniające — zwraca listę `missing_information[]` od razu w wyniku. Endpoint `/clarify` istnieje, ale w pipeline 3.0 nie jest triggerowany.

---

## 3. Format odpowiedzi końcowej

Odpowiedź prezentowana użytkownikowi zawiera:

1. **Opis stanu faktycznego** — uporządkowana wersja opisu użytkownika (encje, role, relacje).
2. **Ocena** — klasyfikacja: `CONFLICT` / `CONFLICT_WAIVABLE` / `NO_CONFLICT`.
3. **Poziom ryzyka** — krytyczny / umiarkowane / niskie.
4. **Poziom pewności** — wysoki / umiarkowany / niski.
5. **Uzasadnienie** — z odwołaniami do konkretnych artykułów KERP w nawiasach kwadratowych `[art. X KERP]`.
6. **Podstawa prawna** — lista przepisów KERP/u.r.p.
7. **Ewaluacja per artykuł** — dla każdego z 9 artykułów: czy ma zastosowanie, przesłanki spełnione/niespełnione, uzasadnienie.
8. **Braki informacyjne** — kwestie wymagające doprecyzowania (`missing_information`).

---

## 4. Architektura kontekstu stałego dla LLM (warstwa wiedzy)

Jakość single-shot analizy zależy od **stałego kontekstu** wstrzykiwanego do promptu obok katalogu artykułów. Budżet tokenów Gemini 2.5 Flash jest praktycznie nieograniczający (~4,3 tys. tokenów input przy >1 mln limitu) — optymalizujemy pod **jakość analizy, nie pod budżet**.

Docelowa architektura — **4 warstwy** (pełny opis w `CLAUDE.md` → „Architektura kontekstu LLM"):

| Warstwa | Zawartość | Status |
|---|---|---|
| W1 — Przepisy źródłowe | KERP (9 art. — `articles_catalog.json`), wybrane art. u.r.p., odwołania do KK (art. 115 § 11) | KERP gotowe; u.r.p./KK TODO |
| W2 — **Glosariusz pojęć** | ~10 kart definicyjnych pojęć ocennych/spornych, każda z sekcją „Wykładnia OSD (tezy zanonimizowane)" | **w budowie** — `backend/app/adapters/prompts/glossary/` |
| W3 — Algorytm decyzyjny | kolejność sprawdzania artykułów + reguły rozstrzygania | TODO |
| W4 — Przykłady (few-shot) | 1× CONFLICT, 1× CONFLICT_WAIVABLE, 1× NO_CONFLICT z pułapką | TODO |

### Baza orzecznicza jako źródło W2 i W4
Zanonimizowane orzeczenia Wyższego Sądu Dyscyplinarnego (2020–2025) zebrane w `docs/legal/Orzecznictwo-WSD-konflikt-interesow.md` są **materiałem źródłowym**, z którego destylowane są:
- tezy interpretacyjne do sekcji „Wykładnia OSD" w kartach glosariusza (W2),
- kandydaci na przykłady few-shot, w tym uniewinnienia jako granice negatywne pojęć (W4).

Pełne uzasadnienia pozostają w bazie źródłowej; do promptu trafiają wyłącznie zdestylowane karty (≤ 1 strona A4) i przykłady.

---

## 5. Kluczowe założenia projektowe

- użytkownik pozostaje decydentem – system ma charakter wspierający,
- szczególny nacisk na przypadki „szare" (niejednoznaczne) — stąd inwestycja w warstwę kontekstu stałego (glosariusz pojęć ocennych),
- pełny katalog artykułów oceniany w jednym przebiegu (spójność, krótki czas analizy ~25–31 s),
- przewidywalne ramy interpretacyjne zaszczepione przez glosariusz i wykładnię OSD,
- odporność na błędy: każdy wynik prezentowany użytkownikowi (fallback zamiast zawieszenia).
