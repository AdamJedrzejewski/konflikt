# Rule Engine

Moduł ładuje reguły z katalogu `rules/` i ewaluuje je na ekstrakcji JSON ze stanu faktycznego.

## Jak działa

1. **Inicjalizacja** — `RuleEngine` wczytuje reguły z `rules/hard/index.json` i `rules/soft/index.json` w kolejności `priority`.
2. **Ewaluacja** (`evaluate(extraction)`) — sprawdza ekstrakcję przez reguły:
   - **Hard rules** — sprawdzane po kolei. Pierwszy match z `waivable=false` kończy ewaluację z wynikiem `CONFLICT`.
   - **Soft rules** — sprawdzane po kolei. Wyniki agregowane.
3. **Wynik** — `EngineResult` z informacją o znalezionych konfliktach.

## Matching warunków

Każda reguła ma tablicę `conditions`. Warunki dzielą się na:
- **Wymagane** (AND) — wszystkie muszą być spełnione
- **Alternatywne** (`alternative: true`) — wystarczy jeden z grupy (OR)

### Operatory

| Operator   | Znaczenie                                      |
|------------|------------------------------------------------|
| `eq`       | `extraction[field] == value`                   |
| `in`       | `extraction[field]` jest jednym z `value` (lista) |
| `contains` | `value` zawiera się w `extraction[field]`      |
| `exists`   | pole istnieje i nie jest None/puste            |

### Dot notation

Pola obsługują zagnieżdżenia: `radca_prawny.prior_role_in_matter` → `extraction["radca_prawny"]["prior_role_in_matter"]`.

Tablice są automatycznie rozwijane — jeśli na ścieżce jest lista obiektów, warunek sprawdzany jest dla każdego elementu.

## Debugowanie

```python
from backend.app.rules.engine import RuleEngine

engine = RuleEngine()
result = engine.evaluate(extraction_dict)

# Sprawdź które reguły dopasowano
for rm in result.matched_hard + result.matched_soft:
    print(f"{rm.rule_id}: {rm.matched_conditions}")
```
