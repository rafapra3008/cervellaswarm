#!/usr/bin/env python3
"""
HARDTEST per W3-B Day 5 - Struttura Agent e Template

Verifica che:
1. cervella-architect.md abbia sezioni obbligatorie
2. PLAN_TEMPLATE.md abbia tutte le sezioni necessarie
3. File siano ben formattati
"""

import pytest
from pathlib import Path


# ============================================================================
# TEST: cervella-architect.md structure
# ============================================================================
def test_architect_agent_has_required_sections():
    """
    Verifica che cervella-architect.md abbia le sezioni chiave.
    """
    agent_file = Path.home() / ".claude/agents/cervella-architect.md"
    assert agent_file.exists(), "cervella-architect.md non trovato"

    content = agent_file.read_text()

    # Sezioni obbligatorie
    required_sections = [
        "# Cervella Architect",
        "## Il Mio Ruolo",
        "## Quando Vengo Attivata",
        "## REGOLA FONDAMENTALE",
        "## Come Lavoro (4 Fasi)",
        "### Phase 1: Understanding",
        "### Phase 2: Design",
        "### Phase 3: Review",
        "### Phase 4: Final Plan",
        "## Output: PLAN.md",
        "## Limiti",
    ]

    for section in required_sections:
        assert section in content, f"Sezione mancante: {section}"


def test_architect_agent_metadata():
    """
    Verifica che l'agent abbia metadata YAML all'inizio.
    """
    agent_file = Path.home() / ".claude/agents/cervella-architect.md"
    content = agent_file.read_text()

    # Deve iniziare con ---
    assert content.startswith("---"), "Metadata YAML mancante"

    # Campi obbligatori nel metadata
    metadata_fields = [
        "name: cervella-architect",
        "version:",
        "model: opus",
        "tools:",
    ]

    for field in metadata_fields:
        assert field in content, f"Metadata field mancante: {field}"


def test_architect_no_write_tools():
    """
    Verifica che architect NON abbia tool Write/Edit/Bash.
    """
    agent_file = Path.home() / ".claude/agents/cervella-architect.md"
    content = agent_file.read_text()

    # Tool permessi
    assert "Read" in content or "tools:" in content

    # Tool VIETATI - verifica che la regola sia presente
    assert "Tool VIETATI: Write, Edit, Bash" in content or \
           "IO NON SCRIVO CODICE" in content, \
           "Regola tool vietati non trovata"


# ============================================================================
# TEST: PLAN_TEMPLATE.md structure
# ============================================================================
def test_plan_template_has_all_phases():
    """
    Verifica che PLAN_TEMPLATE.md abbia tutte le 4 fasi.
    """
    template_file = Path(__file__).parent.parent.parent / ".swarm/templates/PLAN_TEMPLATE.md"
    assert template_file.exists(), "PLAN_TEMPLATE.md non trovato"

    content = template_file.read_text()

    # Le 4 fasi obbligatorie
    phases = [
        "## Phase 1: Understanding",
        "## Phase 2: Design",
        "## Phase 3: Review",
        "## Phase 4: Final Plan",
    ]

    for phase in phases:
        assert phase in content, f"Fase mancante: {phase}"


def test_plan_template_metadata_section():
    """
    Verifica che ci sia sezione Metadata con tutti i campi.
    """
    template_file = Path(__file__).parent.parent.parent / ".swarm/templates/PLAN_TEMPLATE.md"
    content = template_file.read_text()

    assert "## Metadata" in content

    # Campi metadata
    metadata_fields = [
        "Task ID",
        "Architect",
        "Created",
        "Complexity",
        "Files Affected",
        "Risk Score",
    ]

    for field in metadata_fields:
        assert field in content, f"Campo Metadata mancante: {field}"


def test_plan_template_success_criteria_section():
    """
    Verifica che ci sia sezione Success Criteria in Phase 4.
    """
    template_file = Path(__file__).parent.parent.parent / ".swarm/templates/PLAN_TEMPLATE.md"
    content = template_file.read_text()

    assert "### Success Criteria" in content
    # Deve avere formato tabella o checklist
    assert "Come Verificare" in content or "[ ]" in content


def test_plan_template_execution_order_section():
    """
    Verifica che ci sia sezione Execution Order in Phase 4.
    """
    template_file = Path(__file__).parent.parent.parent / ".swarm/templates/PLAN_TEMPLATE.md"
    content = template_file.read_text()

    assert "### Execution Order" in content
    # Deve contenere struttura step
    assert "Worker:" in content
    assert "Files:" in content


def test_plan_template_risks_section():
    """
    Verifica che Phase 2 abbia sezione Risks & Mitigations.
    """
    template_file = Path(__file__).parent.parent.parent / ".swarm/templates/PLAN_TEMPLATE.md"
    content = template_file.read_text()

    assert "### Risks" in content or "Risks & Mitigations" in content
    assert "Mitigazione" in content or "Mitigation" in content


def test_plan_template_has_approval_section():
    """
    Verifica che ci sia sezione Approval per tracking.
    """
    template_file = Path(__file__).parent.parent.parent / ".swarm/templates/PLAN_TEMPLATE.md"
    content = template_file.read_text()

    assert "## Approval" in content
    assert "WAITING_APPROVAL" in content or "Status" in content


# ============================================================================
# TEST: Format validation
# ============================================================================
def test_architect_no_malformed_sections():
    """
    Verifica che non ci siano sezioni malformate.
    """
    agent_file = Path.home() / ".claude/agents/cervella-architect.md"
    content = agent_file.read_text()

    lines = content.split("\n")

    for i, line in enumerate(lines):
        # Le sezioni markdown devono avere spazio dopo #
        if line.startswith("#") and not line.startswith("---"):
            if len(line) > 1 and line[1] != " " and line[1] != "#":
                pytest.fail(f"Riga {i+1}: Sezione malformata '{line}'")


def test_template_no_empty_sections():
    """
    Verifica che le sezioni del template non siano vuote.
    """
    template_file = Path(__file__).parent.parent.parent / ".swarm/templates/PLAN_TEMPLATE.md"
    content = template_file.read_text()

    # Ogni ## deve essere seguito da contenuto entro 5 righe
    lines = content.split("\n")

    for i, line in enumerate(lines):
        if line.startswith("## "):
            # Controlla che entro 5 righe ci sia contenuto non vuoto
            has_content = False
            for j in range(i+1, min(i+6, len(lines))):
                if lines[j].strip() and not lines[j].startswith("#"):
                    has_content = True
                    break

            if not has_content:
                pytest.fail(f"Sezione vuota rilevata: {line}")


# ============================================================================
# TEST: Integration check
# ============================================================================
def test_architect_references_template():
    """
    Verifica che architect.md menzioni PLAN_TEMPLATE o il path dei plan.
    """
    agent_file = Path.home() / ".claude/agents/cervella-architect.md"
    content = agent_file.read_text()

    # Deve riferire .swarm/plans/ per output
    assert ".swarm/plans/" in content or "PLAN_" in content


# ============================================================================
# RUN TESTS
# ============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
