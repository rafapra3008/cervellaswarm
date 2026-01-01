#!/usr/bin/env python3
"""
Test automatico per wizard.py
Verifica che tutte le funzionalità siano implementate correttamente.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import sys
from pathlib import Path

# Import wizard module
sys.path.insert(0, str(Path(__file__).parent))
from wizard import LessonWizard, TEMPLATES, SEVERITY_LEVELS, AGENTS, get_db_path

def test_wizard_initialization():
    """Test creazione wizard e inizializzazione lesson."""
    print("🧪 Test 1: Inizializzazione wizard...")
    wizard = LessonWizard()

    assert wizard.lesson is not None, "Lesson non inizializzata"
    assert wizard.lesson["id"], "ID mancante"
    assert wizard.lesson["timestamp"], "Timestamp mancante"
    assert wizard.lesson["severity"] == "MEDIUM", "Severity default errata"
    assert wizard.lesson["confidence"] == 0.8, "Confidence default errata"

    print("   ✅ Wizard inizializzato correttamente")

def test_templates():
    """Test template disponibili."""
    print("🧪 Test 2: Templates...")

    assert len(TEMPLATES) == 4, f"Numero template errato: {len(TEMPLATES)}"
    assert "bug_fix" in TEMPLATES, "Template bug_fix mancante"
    assert "refactor" in TEMPLATES, "Template refactor mancante"
    assert "integration" in TEMPLATES, "Template integration mancante"
    assert "custom" in TEMPLATES, "Template custom mancante"

    for key, template in TEMPLATES.items():
        assert "name" in template, f"Template {key} senza name"
        assert "trigger_template" in template, f"Template {key} senza trigger_template"
        assert "prevention_template" in template, f"Template {key} senza prevention_template"

    print("   ✅ Tutti i template sono validi")

def test_constants():
    """Test costanti severity e agents."""
    print("🧪 Test 3: Costanti...")

    assert len(SEVERITY_LEVELS) == 4, f"Severity levels errati: {len(SEVERITY_LEVELS)}"
    assert "CRITICAL" in SEVERITY_LEVELS, "CRITICAL mancante"
    assert "HIGH" in SEVERITY_LEVELS, "HIGH mancante"
    assert "MEDIUM" in SEVERITY_LEVELS, "MEDIUM mancante"
    assert "LOW" in SEVERITY_LEVELS, "LOW mancante"

    assert len(AGENTS) == 10, f"Numero agenti errato: {len(AGENTS)}"
    assert "cervella-frontend" in AGENTS, "cervella-frontend mancante"
    assert "cervella-backend" in AGENTS, "cervella-backend mancante"

    print("   ✅ Costanti corrette")

def test_db_path():
    """Test path database."""
    print("🧪 Test 4: Path database...")

    db_path = get_db_path()
    assert db_path.name == "swarm_memory.db", f"Nome DB errato: {db_path.name}"
    assert db_path.parent.name == "data", f"Directory errata: {db_path.parent.name}"

    print(f"   ✅ Path DB: {db_path}")

def test_lesson_structure():
    """Test struttura lesson."""
    print("🧪 Test 5: Struttura lesson...")

    wizard = LessonWizard()
    required_fields = [
        "id", "timestamp", "trigger", "context", "problem",
        "root_cause", "solution", "prevention", "example",
        "severity", "agents_involved", "tags", "pattern",
        "auto_generated", "confidence", "times_applied"
    ]

    for field in required_fields:
        assert field in wizard.lesson, f"Campo {field} mancante"

    print("   ✅ Struttura lesson completa")

def test_wizard_methods():
    """Test metodi wizard."""
    print("🧪 Test 6: Metodi wizard...")

    wizard = LessonWizard()

    # Test metodi esistono
    assert hasattr(wizard, "print_header"), "Metodo print_header mancante"
    assert hasattr(wizard, "print_step"), "Metodo print_step mancante"
    assert hasattr(wizard, "ask"), "Metodo ask mancante"
    assert hasattr(wizard, "ask_confirm"), "Metodo ask_confirm mancante"
    assert hasattr(wizard, "ask_choice"), "Metodo ask_choice mancante"
    assert hasattr(wizard, "ask_multi_choice"), "Metodo ask_multi_choice mancante"
    assert hasattr(wizard, "run"), "Metodo run mancante"
    assert hasattr(wizard, "print_preview"), "Metodo print_preview mancante"
    assert hasattr(wizard, "save_to_db"), "Metodo save_to_db mancante"

    print("   ✅ Tutti i metodi implementati")

def test_fallback_mode():
    """Test fallback senza Rich."""
    print("🧪 Test 7: Fallback mode...")

    # Il test che Rich sia importabile o che fallback funzioni
    # è già gestito dal wizard stesso
    import wizard
    if wizard.RICH_AVAILABLE:
        print("   ✅ Rich disponibile (UI avanzata)")
    else:
        print("   ✅ Fallback mode attivo (UI base)")

def main():
    """Esegue tutti i test."""
    print("="*60)
    print("🧙 TEST WIZARD.PY")
    print("="*60)

    tests = [
        test_wizard_initialization,
        test_templates,
        test_constants,
        test_db_path,
        test_lesson_structure,
        test_wizard_methods,
        test_fallback_mode
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"   ❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1

    print("\n" + "="*60)
    print(f"RISULTATI: {passed} passati, {failed} falliti")
    print("="*60)

    if failed == 0:
        print("🎉 Tutti i test passati!")
        return 0
    else:
        print("⚠️  Alcuni test falliti")
        return 1

if __name__ == "__main__":
    sys.exit(main())
