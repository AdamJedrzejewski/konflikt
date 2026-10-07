# ADR-001: LLM Provider — wybór tymczasowy i docelowy

**Data:** 2026-05-04  
**Status:** ACCEPTED

## Decyzja

**Tymczasowo (faza 3–4, dev/beta):** Anthropic Claude — przez OpenClaw/direct API.  
**Docelowo (produkcja):** Provider-agnostic adapter; priorytet: Azure OpenAI EU lub AWS Bedrock eu-west-1 (Claude) — wymaga EU data residency.

## Uzasadnienie

- Claude ma najlepszą jakość reasoning dla złożonych stanów faktycznych w języku prawniczym
- Na etapie dev nie potrzebujemy EU residency — dane testowe, nie produkcyjne
- Adapter provider-agnostic (sekcja 9.2 architektury) pozwala zamienić provider bez refaktoryzacji logiki
- Na produkcji: AWS Bedrock eu-west-1 + Claude = EU residency + ta sama jakość modelu

## Zmienne środowiskowe

```
LLM_PROVIDER=anthropic   # dev/beta
LLM_API_KEY=...
LLM_MODEL_NAME=claude-sonnet-4-5
```

## Konsekwencje

- Etap 4: testy promptów na Claude + drugi provider (np. Mistral AI)
- Przed etapem 9 (prod): zmiana LLM_PROVIDER bez zmian kodu
