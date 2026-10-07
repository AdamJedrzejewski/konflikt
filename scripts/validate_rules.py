#!/usr/bin/env python3
"""Walidator reguł OBSIL — sprawdza poprawność plików JSON w rules/."""

import json
import os
import sys

RULES_DIR = os.path.join(os.path.dirname(__file__), "..", "rules")

REQUIRED_FIELDS = ["id", "article", "type", "waivable", "description_pl", "conditions", "result", "legal_basis"]
VALID_RESULTS = ["CONFLICT", "CONFLICT_WAIVABLE", "NO_CONFLICT"]


def validate_rule_file(filepath):
    """Waliduje pojedynczy plik reguły. Zwraca listę błędów."""
    errors = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Niepoprawny JSON: {e}"]

    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"Brak wymaganego pola: {field}")

    if "result" in data and data["result"] not in VALID_RESULTS:
        errors.append(f"Niepoprawna wartość result: '{data['result']}' (dozwolone: {VALID_RESULTS})")

    return errors


def validate_index_references(index_path, rules_dir):
    """Sprawdza czy pliki z index.json faktycznie istnieją."""
    errors = []
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return [f"Nie można wczytać index.json: {e}"]

    for rule_entry in index.get("rules", []):
        rule_file = rule_entry.get("file", "")
        rule_path = os.path.join(rules_dir, rule_file)
        if not os.path.isfile(rule_path):
            errors.append(f"Plik z index.json nie istnieje: {rule_file}")

    return errors


def main():
    errors_found = False
    total_rules = 0
    total_ok = 0

    print("=" * 60)
    print("OBSIL — Walidacja reguł")
    print("=" * 60)

    # Walidacja plików reguł w hard/ i soft/
    for subdir in ["hard", "soft"]:
        dir_path = os.path.join(RULES_DIR, subdir)
        if not os.path.isdir(dir_path):
            print(f"\n[BŁĄD] Katalog nie istnieje: {subdir}/")
            errors_found = True
            continue

        print(f"\n--- {subdir}/ ---")

        # Walidacja index.json
        index_path = os.path.join(dir_path, "index.json")
        if os.path.isfile(index_path):
            index_errors = validate_index_references(index_path, dir_path)
            if index_errors:
                errors_found = True
                for err in index_errors:
                    print(f"  [BŁĄD] index.json: {err}")
            else:
                print(f"  [OK] index.json — wszystkie referencje poprawne")
        else:
            print(f"  [BŁĄD] Brak index.json w {subdir}/")
            errors_found = True

        # Walidacja poszczególnych reguł
        for filename in sorted(os.listdir(dir_path)):
            if filename == "index.json" or not filename.endswith(".json"):
                continue

            filepath = os.path.join(dir_path, filename)
            total_rules += 1
            rule_errors = validate_rule_file(filepath)

            if rule_errors:
                errors_found = True
                for err in rule_errors:
                    print(f"  [BŁĄD] {filename}: {err}")
            else:
                total_ok += 1
                print(f"  [OK] {filename}")

    # Sprawdzenie ontologii
    print(f"\n--- ontology/ ---")
    ontology_path = os.path.join(RULES_DIR, "ontology", "entities.json")
    if os.path.isfile(ontology_path):
        print(f"  [OK] entities.json istnieje")
    else:
        print(f"  [BŁĄD] Brak entities.json")
        errors_found = True

    # Podsumowanie
    print(f"\n{'=' * 60}")
    print(f"PODSUMOWANIE: {total_ok}/{total_rules} reguł poprawnych")
    if errors_found:
        print("STATUS: BŁĘDY WYKRYTE")
        sys.exit(1)
    else:
        print("STATUS: WSZYSTKO OK")
        sys.exit(0)


if __name__ == "__main__":
    main()
