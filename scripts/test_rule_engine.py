#!/usr/bin/env python3
"""
Skrypt testowy rule engine — bez pytest, czysty Python.
Uruchomienie: python3 scripts/test_rule_engine.py (z katalogu obsil/)
"""
import sys
from pathlib import Path

# Dodaj root projektu do sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.app.rules.engine import RuleEngine


def test_tc001_mediator_conflict():
    """TC-001: Mediator chce reprezentować stronę → CONFLICT (KERP-27-1)"""
    extraction = {
        "radca_prawny": {
            "prior_role_in_matter": "mediator",
        },
        "matter": {
            "is_same_or_related": True,
        },
    }

    engine = RuleEngine()
    result = engine.evaluate(extraction)

    print("=" * 60)
    print("TC-001: Mediator chce reprezentować stronę")
    print("=" * 60)
    print(f"  overall_result:       {result.overall_result}")
    print(f"  has_absolute_conflict: {result.has_absolute_conflict}")
    print(f"  stop_reason:          {result.stop_reason}")
    print(f"  matched_hard:         {len(result.matched_hard)}")
    for rm in result.matched_hard:
        print(f"    - {rm.rule_id} ({rm.article})")
        print(f"      waivable: {rm.waivable}")
        print(f"      conditions: {rm.matched_conditions}")
    print(f"  matched_soft:         {len(result.matched_soft)}")

    assert result.overall_result == "CONFLICT", (
        f"Expected CONFLICT, got {result.overall_result}"
    )
    assert result.has_absolute_conflict is True
    assert result.stop_reason == "art. 27 pkt 1 KERP"
    assert len(result.matched_hard) == 1
    assert result.matched_hard[0].rule_id == "KERP-27-1"
    print("  ✓ TC-001 PASSED\n")


def test_tc010_advisory_waivable():
    """TC-010: Doradztwo dwóm klientom o sprzecznych interesach → CONFLICT_WAIVABLE (KERP-29-1-pkt1)"""
    extraction = {
        "clients": {
            "interests_are_conflicting": True,
        },
        "matter": {
            "is_same_or_related": True,
        },
        "radca_prawny": {
            "role": "doradca",
        },
    }

    engine = RuleEngine()
    result = engine.evaluate(extraction)

    print("=" * 60)
    print("TC-010: Doradztwo dwóm klientom — sprzeczne interesy")
    print("=" * 60)
    print(f"  overall_result:        {result.overall_result}")
    print(f"  has_absolute_conflict: {result.has_absolute_conflict}")
    print(f"  has_waivable_conflict: {result.has_waivable_conflict}")
    print(f"  matched_hard:          {len(result.matched_hard)}")
    print(f"  matched_soft:          {len(result.matched_soft)}")
    for rm in result.matched_soft:
        print(f"    - {rm.rule_id} ({rm.article})")
        print(f"      waivable: {rm.waivable}")
        print(f"      result: {rm.result}")
        print(f"      conditions: {rm.matched_conditions}")

    assert result.overall_result == "CONFLICT_WAIVABLE", (
        f"Expected CONFLICT_WAIVABLE, got {result.overall_result}"
    )
    assert result.has_waivable_conflict is True
    assert result.has_absolute_conflict is False
    assert any(rm.rule_id == "KERP-29-1-pkt1" for rm in result.matched_soft)
    print("  ✓ TC-010 PASSED\n")


def test_no_conflict():
    """Ekstrakcja bez konfliktu → NO_CONFLICT"""
    extraction = {
        "radca_prawny": {
            "prior_role_in_matter": None,
            "role": "doradca",
        },
        "matter": {
            "is_same_or_related": False,
        },
    }

    engine = RuleEngine()
    result = engine.evaluate(extraction)

    print("=" * 60)
    print("Bonus: Brak konfliktu")
    print("=" * 60)
    print(f"  overall_result:       {result.overall_result}")
    print(f"  matched_hard:         {len(result.matched_hard)}")
    print(f"  matched_soft:         {len(result.matched_soft)}")

    assert result.overall_result == "NO_CONFLICT", (
        f"Expected NO_CONFLICT, got {result.overall_result}"
    )
    assert not result.matched_hard
    assert not result.matched_soft
    print("  ✓ NO_CONFLICT PASSED\n")


if __name__ == "__main__":
    print("\n🔍 Rule Engine — Testy\n")

    try:
        engine = RuleEngine()
        print(f"Załadowano {len(engine._hard_rules)} hard rules")
        print(f"Załadowano {len(engine._soft_rules)} soft rules\n")
    except Exception as e:
        print(f"BŁĄD ładowania reguł: {e}")
        sys.exit(1)

    passed = 0
    failed = 0

    for test_fn in [test_tc001_mediator_conflict, test_tc010_advisory_waivable, test_no_conflict]:
        try:
            test_fn()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"Wynik: {passed} passed, {failed} failed")
    print("=" * 60)
    sys.exit(0 if failed == 0 else 1)
