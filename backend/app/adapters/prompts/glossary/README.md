# Glosariusz pojęć kluczowych (Warstwa 2 kontekstu LLM)

Karty definicyjne pojęć ocennych i spornych z KERP, wstrzykiwane do promptu single-shot obok katalogu artykułów (`../articles_catalog.json`). Cel: zaszczepić modelowi **przewidywalne ramy interpretacyjne** dla pojęć, które najczęściej decydują o kwalifikacji konfliktu interesów.

## Zasady kart

- Jedno pojęcie = jeden plik `.md`, docelowo ≤ 1 strona A4 (~700 tokenów).
- Struktura wg wzorca z `CLAUDE.md` → „Wzorzec karty glosariusza": Definicja → Wykładnia OSD (tezy zanonimizowane) → Granice pojęcia (Obejmuje / Nie obejmuje) → Nie mylić z → Praktyczna wskazówka.
- Tezy w sekcji „Wykładnia OSD" są **destylowane z** `docs/legal/Orzecznictwo-WSD-konflikt-interesow.md`. Każda teza wskazuje sygnaturę orzeczenia (sygnatura nie jest daną osobową — służy resowalności).
- Uniewinnienia są cenne jako **granice negatywne** pojęcia (co NIE wypełnia znamion).

## Integracja (TODO)

Funkcja `_build_simple_payload` w `../../llm_adapter.py` doczyta wszystkie karty z tego katalogu i wklei je do promptu (warstwa W2). Do czasu implementacji karty są materiałem redakcyjnym.

## Spis kart

| # | Pojęcie | Plik | Występuje w | Priorytet* |
|---|---------|------|-------------|-----------|
| 01 | Sprawa ta sama / sprawa z nią związana | `01-sprawa-ta-sama-zwiazana.md` | art. 28 ust. 1 i 3, 29, 30 | 1 |
| 02 | Nieuzasadniona przewaga | `02-nieuzasadniona-przewaga.md` | art. 26 | 2 |
| 03 | Klient — pojęcie, aktualny vs były | `03-klient-aktualny-vs-byly.md` | art. 5 pkt 4, 28, 29 | 5 |

\* Priorytet wg tabeli „Glosariusz — priorytety" w `CLAUDE.md`. Kolejne karty (osoba najbliższa/bliskie stosunki, pomoc prawna vs doradztwo, tajemnica zawodowa, niezależność, konflikt interesów, wspólne wykonywanie zawodu) — w kolejce.
