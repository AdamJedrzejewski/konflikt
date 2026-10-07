# ADR-005: Przepływ analizy — model dwufazowy

**Data:** 2026-05-04  
**Status:** SUPERSEDED przez [ADR-006](ADR-006-single-shot-context.md) (2026-05-14)

> ⚠️ Decyzja wycofana. Model dwufazowy (schematyczna + niezależna + komparator) okazał się wolny (~85–130 s) i kruchy. Zastąpiony przez single-shot LLM — szczegóły i uzasadnienie w ADR-006. Dokument zachowany jako zapis historyczny.

## Decyzja

Analiza przebiega w 5 etapach z **dwiema równoległymi ścieżkami analizy** (schematyczna + niezależna) i mechanizmem porównania wyników.

## Przepływ (szczegółowy)

```
Etap 1: Opis stanu faktycznego (swobodna forma)
   ↓
Etap 2: LLM — analiza wstępna
   - Identyfikacja braków
   - Pytania uzupełniające (max 5)
   ↓
Etap 3: Analiza właściwa (dwufazowa, równoległa)
   ┌──────────────────────────────────────────┐
   │ 3.1 Analiza schematyczna                  │
   │     Przejście przez drzewo decyzyjne KIRP │
   │     (diagram konfliktu interesów)          │
   ├──────────────────────────────────────────┤
   │ 3.2 Analiza niezależna                    │
   │     LLM ocenia na podstawie KERP + u.r.p. │
   │     bez sztywnego schematu                │
   └──────────────────────────────────────────┘
   ↓
Etap 4: Porównanie wyników
   ├── Zgodne → Odpowiedź końcowa
   └── Rozbieżne → Identyfikacja przyczyny
                   Pytania dodatkowe (max 2)
                   Powtórzenie analizy
                   ├── Zgodne → Odpowiedź końcowa
                   └── Nadal rozbieżne → Etap 5
   ↓
Etap 5: Odpowiedź z niepewnością
   - Wskazanie obszarów ryzyka
   - Rekomendacje dalszych działań
```

## Format odpowiedzi końcowej

1. **Opis stanu faktycznego** — zsyntetyzowany przez LLM
2. **Pytania i odpowiedzi** — pełna lista
3. **Ocena** — tak / nie / potencjalny konflikt
4. **Zastrzeżenia** — niepewności, obszary ryzyka
5. **Podstawa prawna** — przepisy KERP + u.r.p.
6. **Rekomendacje** — co ustalić, jeśli brak jednoznaczności

## Implikacje architektoniczne

- Orchestrator musi obsługiwać **stan sesji** (kontekst między etapami)
- Dwa osobne wywołania LLM w etapie 3 (lub jeden prompt z instrukcją dwutorową)
- Moduł porównania wyników = deterministyczny (nie LLM)
- Limit pytań = hard limit w kodzie (5 + 2), nie w promptach
- "Akceptowalna niepewność" = osobna klasyfikacja wyniku, nie błąd

## Konsekwencje dla prompts (Faza 4)

Potrzebne 3 typy system promptów:
1. `prompt_extraction.txt` — Etap 2, generowanie pytań uzupełniających
2. `prompt_schematic.txt` — Etap 3.1, analiza wg drzewa decyzyjnego
3. `prompt_independent.txt` — Etap 3.2, analiza autonomiczna na podstawie przepisów
