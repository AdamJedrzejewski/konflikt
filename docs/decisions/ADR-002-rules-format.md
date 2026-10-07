# ADR-002: Format bazy twardych reguł

**Data:** 2026-05-04  
**Status:** ACCEPTED

## Decyzja

Format: **JSON Schema** (pliki `.json` w `rules/hard/` i `rules/soft/`)

## Uzasadnienie

- Czytelny dla prawnika bez znajomości programowania
- Łatwy do edytowania przy nowelizacji KERP/u.r.p.
- Prosty w parsowaniu przez rule engine (Python `json` stdlib)
- Datalog — overkill na tym etapie; można migrować jeśli zajdzie potrzeba

## Struktura pliku reguły

```json
{
  "id": "KERP-27-1",
  "article": "art. 27 pkt 1 KERP",
  "type": "absolute_prohibition",
  "description": "...",
  "conditions": [...],
  "result": "CONFLICT",
  "confidence": "high"
}
```
