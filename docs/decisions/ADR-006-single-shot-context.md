# ADR-006: Przepływ analizy — single-shot LLM + warstwa kontekstu stałego

**Data:** 2026-05-14
**Status:** ACCEPTED
**Zastępuje:** [ADR-005](ADR-005-analysis-flow.md) (model dwufazowy)

## Kontekst

Pipeline 2.0 (ADR-005, później rozwinięty o sekwencyjną ewaluację per artykuł) opierał się na wielu wywołaniach LLM: ekstrakcja → rule engine → analiza schematyczna + niezależna → komparator. W praktyce:

- był wolny — pełna analiza trwała ~85–130 s,
- był kruchy — do 9 niezależnych wywołań LLM per analiza, każde mogło zawieść,
- rule engine (keyword guardrails) generował false-positive rozbieżności, które komparator musiał tłumić.

## Decyzja

Analiza przebiega w **jednym wywołaniu LLM** (single-shot). Model otrzymuje w jednym prompcie pełny katalog 9 artykułów KERP wraz z przesłankami i zwraca komplet wyniku (encje, role, ewaluacja per artykuł, agregacja klasyfikacji/ryzyka/pewności).

Jakość analizy nie jest budowana przez orkiestrację wielu wywołań, lecz przez **warstwę kontekstu stałego** wstrzykiwaną do promptu. Budżet tokenów Gemini 2.5 Flash jest praktycznie nieograniczający (~4,3 tys. input przy >1 mln limitu), więc optymalizujemy pod jakość, nie pod koszt.

Docelowo kontekst stały tworzą 4 warstwy (zob. `CLAUDE.md` → „Architektura kontekstu LLM"):
1. **W1** — przepisy źródłowe (KERP + wybrane u.r.p./KK),
2. **W2** — glosariusz pojęć (karty z sekcją „Wykładnia OSD"), źródło: `docs/legal/Orzecznictwo-WSD-konflikt-interesow.md`,
3. **W3** — algorytm decyzyjny,
4. **W4** — przykłady few-shot.

## Konsekwencje

- Czas analizy spadł do ~25–31 s.
- Orchestrator nie utrzymuje stanu sesji między etapami (znika złożoność `clarify` w pętli).
- Pole `mode` w `final_result`: `llm_only` (domyślny), `error_fallback` (wyjątek → czytelny wynik zamiast zawieszenia), `anchored` (legacy, nieużywany).
- Braki informacyjne zwracane w `missing_information[]` zamiast pętli pytań uzupełniających.
- **Dług techniczny:** martwy kod pipeline 2.0 (`comparator.py`, `rules/engine.py`, sekwencyjna ewaluacja, stare prompty) pozostaje tymczasowo na wypadek rollbacku — sprzątanie w osobnym PR (Etap B roadmapy).
- **Nowy obszar pracy:** budowa warstwy kontekstu stałego (glosariusz) staje się głównym wektorem poprawy jakości.
