#!/usr/bin/env python3
"""
Architect Flow - Orchestrazione del pattern Architect per CervellaSwarm

W3-B Day 6: Flow Integration
- REQ-15: Regina routing (task -> architect?)
- REQ-16: Plan validation logic
- REQ-17: Fallback se plan rifiutato 2x
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional
import json
import re

# Import dal Day 5
import sys
from pathlib import Path

# Aggiungi root al path per import
_root = Path(__file__).parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from scripts.swarm.task_classifier import (
    classify_task,
    should_use_architect,
    TaskComplexity,
    ClassificationResult
)


class PlanStatus(Enum):
    """Stati possibili di un plan."""
    DRAFT = "draft"
    WAITING_APPROVAL = "waiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_1 = "revision_1"
    REVISION_2 = "revision_2"
    FALLBACK = "fallback"  # Dopo 2 rejection


class WorkerType(Enum):
    """Tipi di worker disponibili."""
    BACKEND = "cervella-backend"
    FRONTEND = "cervella-frontend"
    TESTER = "cervella-tester"
    DEVOPS = "cervella-devops"
    DOCS = "cervella-docs"
    DATA = "cervella-data"
    RESEARCHER = "cervella-researcher"
    SECURITY = "cervella-security"


@dataclass
class PlanValidationResult:
    """Risultato validazione di un plan."""
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    score: float = 0.0  # 0.0 - 10.0


@dataclass
class RoutingDecision:
    """Decisione di routing della Regina."""
    use_architect: bool
    classification: ClassificationResult
    reason: str
    suggested_workers: list[WorkerType] = field(default_factory=list)


@dataclass
class ArchitectSession:
    """Sessione di planning con l'Architect."""
    task_id: str
    task_description: str
    status: PlanStatus = PlanStatus.DRAFT
    plan_path: Optional[Path] = None
    revision_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    rejection_reasons: list[str] = field(default_factory=list)


# =============================================================================
# REQ-15: Regina Routing
# =============================================================================

def route_task(
    task_description: str,
    task_id: Optional[str] = None,
    force_architect: bool = False,
    force_direct: bool = False
) -> RoutingDecision:
    """
    Decide se un task deve passare per l'Architect o andare diretto ai Worker.

    Args:
        task_description: Descrizione del task
        task_id: ID univoco del task (generato se None)
        force_architect: Forza uso architect
        force_direct: Forza bypass architect (va diretto ai worker)

    Returns:
        RoutingDecision con la decisione e motivazione
    """
    # Force overrides
    if force_direct:
        return RoutingDecision(
            use_architect=False,
            classification=classify_task(task_description),
            reason="Bypass architect forzato (force_direct=True)",
            suggested_workers=_suggest_workers(task_description)
        )

    if force_architect:
        return RoutingDecision(
            use_architect=True,
            classification=classify_task(task_description, force_architect=True),
            reason="Architect forzato (force_architect=True)",
            suggested_workers=[]
        )

    # Classificazione automatica
    classification = classify_task(task_description)

    # Decisione basata su classification
    if classification.should_architect:
        return RoutingDecision(
            use_architect=True,
            classification=classification,
            reason=f"Task {classification.complexity.value}: {classification.reasoning}",
            suggested_workers=[]  # Architect decidera
        )
    else:
        return RoutingDecision(
            use_architect=False,
            classification=classification,
            reason=f"Task {classification.complexity.value}: procedi diretto",
            suggested_workers=_suggest_workers(task_description)
        )


def _suggest_workers(task_description: str) -> list[WorkerType]:
    """
    Suggerisce worker appropriati basandosi sulla descrizione.

    Returns:
        Lista di WorkerType suggeriti (ordine = priorita)
    """
    desc_lower = task_description.lower()
    workers = []

    # Backend keywords
    if any(kw in desc_lower for kw in ["api", "endpoint", "database", "python", "fastapi", "backend", "server"]):
        workers.append(WorkerType.BACKEND)

    # Frontend keywords
    if any(kw in desc_lower for kw in ["ui", "frontend", "react", "css", "component", "button", "page", "style"]):
        workers.append(WorkerType.FRONTEND)

    # Tester keywords
    if any(kw in desc_lower for kw in ["test", "verify", "check", "bug", "fix", "debug"]):
        workers.append(WorkerType.TESTER)

    # DevOps keywords
    if any(kw in desc_lower for kw in ["deploy", "docker", "ci", "cd", "infra", "server", "nginx"]):
        workers.append(WorkerType.DEVOPS)

    # Docs keywords
    if any(kw in desc_lower for kw in ["doc", "readme", "guide", "tutorial", "comment"]):
        workers.append(WorkerType.DOCS)

    # Data keywords
    if any(kw in desc_lower for kw in ["data", "query", "sql", "analytics", "report", "etl"]):
        workers.append(WorkerType.DATA)

    # Security keywords
    if any(kw in desc_lower for kw in ["security", "auth", "permission", "vulnerability", "audit"]):
        workers.append(WorkerType.SECURITY)

    # Default: backend se nessun match
    if not workers:
        workers.append(WorkerType.BACKEND)

    return workers


# =============================================================================
# REQ-16: Plan Validation Logic
# =============================================================================

# Sezioni obbligatorie nel plan
REQUIRED_PLAN_SECTIONS = [
    "## Metadata",
    "## Phase 1: Understanding",
    "## Phase 2: Design",
    "## Phase 3: Review",
    "## Phase 4: Final Plan",
]

# Campi obbligatori in metadata
REQUIRED_METADATA_FIELDS = [
    "Task ID",
    "Complexity",
    "Files Affected",
]

# Pattern per success criteria
SUCCESS_CRITERIA_PATTERN = r"###\s*Success Criteria"


def validate_plan(plan_content: str) -> PlanValidationResult:
    """
    Valida il contenuto di un plan generato dall'Architect.

    Args:
        plan_content: Contenuto markdown del plan

    Returns:
        PlanValidationResult con validita, errori e score
    """
    errors = []
    warnings = []
    score = 10.0

    # Check sezioni obbligatorie
    for section in REQUIRED_PLAN_SECTIONS:
        if section not in plan_content:
            errors.append(f"Sezione mancante: {section}")
            score -= 1.5

    # Check metadata fields
    metadata_section = _extract_section(plan_content, "## Metadata", "## Phase 1")
    if metadata_section:
        for field in REQUIRED_METADATA_FIELDS:
            if field not in metadata_section:
                errors.append(f"Campo metadata mancante: {field}")
                score -= 0.5
    else:
        errors.append("Sezione Metadata non trovata o malformata")
        score -= 2.0

    # Check success criteria
    if not re.search(SUCCESS_CRITERIA_PATTERN, plan_content, re.IGNORECASE):
        errors.append("Success Criteria non definiti")
        score -= 1.0

    # Check execution order
    if "### Execution Order" not in plan_content and "Execution Order" not in plan_content:
        warnings.append("Execution Order non esplicito")
        score -= 0.5

    # Check file list
    if not re.search(r"`[^`]+\.(py|ts|js|md|json|yaml)`", plan_content):
        warnings.append("Nessun file specifico menzionato nel plan")
        score -= 0.5

    # Check plan non troppo corto
    if len(plan_content) < 500:
        warnings.append("Plan troppo breve (< 500 chars)")
        score -= 1.0

    # Check plan non troppo lungo
    if len(plan_content) > 10000:
        warnings.append("Plan troppo lungo (> 10000 chars)")
        score -= 0.5

    # Normalizza score
    score = max(0.0, min(10.0, score))

    return PlanValidationResult(
        is_valid=len(errors) == 0 and score >= 7.0,
        errors=errors,
        warnings=warnings,
        score=score
    )


def validate_plan_file(plan_path: Path) -> PlanValidationResult:
    """
    Valida un file plan.

    Args:
        plan_path: Path al file plan.md

    Returns:
        PlanValidationResult
    """
    if not plan_path.exists():
        return PlanValidationResult(
            is_valid=False,
            errors=[f"File non trovato: {plan_path}"],
            score=0.0
        )

    content = plan_path.read_text()
    return validate_plan(content)


def _extract_section(content: str, start_marker: str, end_marker: str) -> Optional[str]:
    """Estrae una sezione tra due marker."""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return None

    end_idx = content.find(end_marker, start_idx + len(start_marker))
    if end_idx == -1:
        end_idx = len(content)

    return content[start_idx:end_idx]


# =============================================================================
# REQ-17: Fallback Logic
# =============================================================================

MAX_REVISIONS = 2  # Dopo 2 rejection -> fallback


def handle_plan_rejection(
    session: ArchitectSession,
    rejection_reason: str
) -> tuple[ArchitectSession, str]:
    """
    Gestisce il rifiuto di un plan.

    Args:
        session: Sessione architect corrente
        rejection_reason: Motivo del rifiuto

    Returns:
        (session aggiornata, azione da intraprendere)
    """
    session.rejection_reasons.append(rejection_reason)
    session.revision_count += 1

    if session.revision_count == 1:
        session.status = PlanStatus.REVISION_1
        action = "REQUEST_REVISION"
        message = f"Plan rifiutato (1/2). Motivo: {rejection_reason}. Richiedi revisione."

    elif session.revision_count == 2:
        session.status = PlanStatus.REVISION_2
        action = "REQUEST_REVISION"
        message = f"Plan rifiutato (2/2). Motivo: {rejection_reason}. ULTIMA revisione."

    else:  # revision_count > 2
        session.status = PlanStatus.FALLBACK
        action = "FALLBACK_TO_WORKER"
        message = f"Plan rifiutato 3 volte. FALLBACK: procedi senza plan dettagliato."

    return session, action


def should_fallback(session: ArchitectSession) -> bool:
    """
    Verifica se la sessione deve andare in fallback.

    Returns:
        True se deve usare fallback (troppe rejection)
    """
    return session.revision_count > MAX_REVISIONS


def create_fallback_instruction(session: ArchitectSession) -> str:
    """
    Crea istruzioni per il worker quando si va in fallback.

    Args:
        session: Sessione con i dettagli del task

    Returns:
        Istruzioni markdown per il worker
    """
    reasons = "\n".join(f"- {r}" for r in session.rejection_reasons)

    return f"""# Fallback Mode - Task {session.task_id}

> **ATTENZIONE:** Plan non approvato dopo {session.revision_count} tentativi.
> Procedi con cautela, un passo alla volta.

## Task
{session.task_description}

## Rejection History
{reasons}

## Istruzioni Fallback
1. **Inizia PICCOLO** - modifica minima possibile
2. **Chiedi conferma** - dopo ogni step significativo
3. **Testa subito** - verifica che funzioni prima di continuare
4. **Documenta** - scrivi cosa hai fatto e perche

## Warning
Il plan e stato rifiutato. Procedi con:
- Modifiche incrementali
- Frequenti checkpoint
- Nessun refactoring ampio senza approvazione

---
*Fallback generato da architect_flow.py*
"""


# =============================================================================
# Session Management
# =============================================================================

def create_session(task_id: str, task_description: str) -> ArchitectSession:
    """Crea una nuova sessione architect."""
    return ArchitectSession(
        task_id=task_id,
        task_description=task_description,
        status=PlanStatus.DRAFT
    )


def approve_plan(session: ArchitectSession, approved_by: str = "Regina") -> ArchitectSession:
    """Approva un plan."""
    session.status = PlanStatus.APPROVED
    session.approved_at = datetime.now()
    session.approved_by = approved_by
    return session


def get_plan_path(task_id: str) -> Path:
    """Ritorna il path standard per un plan."""
    return Path(f".swarm/plans/PLAN_{task_id}.md")


def save_session_state(session: ArchitectSession, output_dir: Path = Path(".swarm/sessions")) -> Path:
    """
    Salva lo stato della sessione su disco.

    Returns:
        Path del file salvato
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"session_{session.task_id}.json"

    state = {
        "task_id": session.task_id,
        "task_description": session.task_description,
        "status": session.status.value,
        "plan_path": str(session.plan_path) if session.plan_path else None,
        "revision_count": session.revision_count,
        "created_at": session.created_at.isoformat(),
        "approved_at": session.approved_at.isoformat() if session.approved_at else None,
        "approved_by": session.approved_by,
        "rejection_reasons": session.rejection_reasons,
    }

    output_path.write_text(json.dumps(state, indent=2))
    return output_path


# =============================================================================
# CLI Interface
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python architect_flow.py route '<task description>'")
        print("  python architect_flow.py validate <plan.md>")
        print("\nExamples:")
        print("  python architect_flow.py route 'refactor auth module'")
        print("  python architect_flow.py validate .swarm/plans/PLAN_001.md")
        sys.exit(1)

    command = sys.argv[1]

    if command == "route":
        if len(sys.argv) < 3:
            print("Error: task description required")
            sys.exit(1)

        task = " ".join(sys.argv[2:])
        decision = route_task(task)

        print(f"\nTask: {task}")
        print(f"{'='*60}")
        print(f"Use Architect:    {decision.use_architect}")
        print(f"Complexity:       {decision.classification.complexity.value}")
        print(f"Confidence:       {decision.classification.confidence:.2f}")
        print(f"Reason:           {decision.reason}")
        if decision.suggested_workers:
            workers = [w.value for w in decision.suggested_workers]
            print(f"Suggested Workers: {', '.join(workers)}")

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Error: plan path required")
            sys.exit(1)

        plan_path = Path(sys.argv[2])
        result = validate_plan_file(plan_path)

        print(f"\nValidating: {plan_path}")
        print(f"{'='*60}")
        print(f"Valid:    {result.is_valid}")
        print(f"Score:    {result.score:.1f}/10")

        if result.errors:
            print(f"\nErrors:")
            for e in result.errors:
                print(f"  - {e}")

        if result.warnings:
            print(f"\nWarnings:")
            for w in result.warnings:
                print(f"  - {w}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
