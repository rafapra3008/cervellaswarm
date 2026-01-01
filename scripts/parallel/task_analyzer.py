#!/usr/bin/env python3
"""
Task Analyzer per CervellaSwarm.
Analizza task e decide strategia di esecuzione: Sequential vs Parallel vs Worktrees.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ExecutionStrategy(Enum):
    """Strategia di esecuzione possibile."""
    SEQUENTIAL = "sequential"      # Una 🐝 alla volta
    PARALLEL = "parallel"          # 3-5 🐝 in parallelo
    WORKTREES = "worktrees"        # Isolamento completo con git worktrees

class Domain(Enum):
    """Domini riconosciuti nel codebase."""
    FRONTEND = "frontend"
    BACKEND = "backend"
    DATABASE = "database"
    TEST = "test"
    DOCS = "docs"
    CONFIG = "config"
    UNKNOWN = "unknown"

# Pattern per riconoscere domini
DOMAIN_PATTERNS = {
    Domain.FRONTEND: [
        r"\.jsx$", r"\.tsx$", r"\.css$", r"\.scss$",
        r"components/", r"pages/", r"src/ui/", r"styles/"
    ],
    Domain.BACKEND: [
        r"\.py$", r"api/", r"services/", r"router",
        r"endpoints/", r"handlers/"
    ],
    Domain.DATABASE: [
        r"\.sql$", r"migrations/", r"alembic/",
        r"models/", r"schema"
    ],
    Domain.TEST: [
        r"test_", r"\.test\.", r"__tests__/",
        r"tests/", r"spec\.", r"\.spec\."
    ],
    Domain.DOCS: [
        r"\.md$", r"docs/", r"README", r"CHANGELOG"
    ],
    Domain.CONFIG: [
        r"\.json$", r"\.yaml$", r"\.yml$", r"\.toml$",
        r"\.env", r"config/"
    ]
}

# Mapping dominio -> agente
DOMAIN_TO_AGENT = {
    Domain.FRONTEND: "cervella-frontend",
    Domain.BACKEND: "cervella-backend",
    Domain.DATABASE: "cervella-data",
    Domain.TEST: "cervella-tester",
    Domain.DOCS: "cervella-docs",
    Domain.CONFIG: "cervella-devops"
}

@dataclass
class FileAnalysis:
    """Analisi di un singolo file."""
    path: str
    domain: Domain
    agent: str
    dependencies: List[str]  # Altri file da cui dipende

@dataclass
class TaskAnalysis:
    """Risultato completo analisi task."""
    files: List[FileAnalysis]
    strategy: ExecutionStrategy
    strategy_reason: str
    domain_distribution: Dict[str, int]
    suggested_agents: List[str]
    parallel_groups: List[List[str]]  # Gruppi di file parallelizzabili
    estimated_speedup: float  # Moltiplicatore velocità atteso

def detect_domain(file_path: str) -> Domain:
    """Rileva il dominio di un file dal suo path."""
    # Check TEST domain first (has priority over BACKEND for test_*.py files)
    for pattern in DOMAIN_PATTERNS[Domain.TEST]:
        if re.search(pattern, file_path, re.IGNORECASE):
            return Domain.TEST

    # Check other domains
    for domain, patterns in DOMAIN_PATTERNS.items():
        if domain == Domain.TEST:
            continue  # Already checked
        for pattern in patterns:
            if re.search(pattern, file_path, re.IGNORECASE):
                return domain
    return Domain.UNKNOWN

def extract_dependencies(file_path: str, content: Optional[str] = None) -> List[str]:
    """
    Estrae dipendenze da un file.
    Analizza import/require/from statements.
    """
    if content is None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return []

    dependencies = []

    # Python imports
    python_imports = re.findall(r'^(?:from|import)\s+([^\s]+)', content, re.MULTILINE)
    dependencies.extend(python_imports)

    # JavaScript imports/requires
    js_imports = re.findall(r"(?:import|require)\s*\(?['\"]([^'\"]+)['\"]", content)
    dependencies.extend(js_imports)

    # Filter to local files only (non package imports)
    local_deps = [d for d in dependencies if d.startswith('.') or d.startswith('/')]

    return local_deps

def analyze_files(file_paths: List[str]) -> List[FileAnalysis]:
    """Analizza lista di file."""
    analyses = []

    for path in file_paths:
        domain = detect_domain(path)
        agent = DOMAIN_TO_AGENT.get(domain, "cervella-orchestrator")
        dependencies = extract_dependencies(path)

        analyses.append(FileAnalysis(
            path=path,
            domain=domain,
            agent=agent,
            dependencies=dependencies
        ))

    return analyses

def calculate_domain_distribution(analyses: List[FileAnalysis]) -> Dict[str, int]:
    """Calcola distribuzione file per dominio."""
    distribution = {}
    for analysis in analyses:
        domain_name = analysis.domain.value
        distribution[domain_name] = distribution.get(domain_name, 0) + 1
    return distribution

def determine_strategy(
    file_count: int,
    domain_count: int,
    has_dependencies: bool,
    estimated_time_minutes: int = 30
) -> Tuple[ExecutionStrategy, str]:
    """
    Determina la strategia ottimale basandosi sui criteri.

    Decision Matrix:
    | Files | Domains | Dependencies | Time | → Strategy |
    |-------|---------|--------------|------|------------|
    | 1-2   | any     | any          | <30  | SEQUENTIAL |
    | 3-5   | diverse | low          | any  | PARALLEL   |
    | 3-5   | same    | high         | any  | SEQUENTIAL |
    | 6+    | diverse | low          | >60  | WORKTREES  |
    | 6+    | diverse | high         | any  | SEQUENTIAL + Split |
    """

    # 1-2 file: sempre sequential
    if file_count <= 2:
        return ExecutionStrategy.SEQUENTIAL, "Pochi file, overhead parallelizzazione non giustificato"

    # 3-5 file con domini diversi e basse dipendenze: parallel
    if 3 <= file_count <= 5 and domain_count >= 2 and not has_dependencies:
        return ExecutionStrategy.PARALLEL, "Sweet spot: 3-5 file, domini diversi, basse dipendenze"

    # 3-5 file stesso dominio o alte dipendenze: sequential
    if 3 <= file_count <= 5 and (domain_count == 1 or has_dependencies):
        return ExecutionStrategy.SEQUENTIAL, "File correlati o alte dipendenze, meglio sequenziale"

    # 6+ file domini diversi basse dipendenze: worktrees
    if file_count >= 6 and domain_count >= 2 and not has_dependencies:
        return ExecutionStrategy.WORKTREES, "Molti file indipendenti, isolamento via worktrees raccomandato"

    # Default: sequential (sicuro)
    return ExecutionStrategy.SEQUENTIAL, "Default sicuro per task complesso"

def group_parallel_files(analyses: List[FileAnalysis]) -> List[List[str]]:
    """
    Raggruppa file che possono essere lavorati in parallelo.
    File dello stesso dominio nello stesso gruppo.
    """
    groups_by_domain = {}

    for analysis in analyses:
        domain = analysis.domain.value
        if domain not in groups_by_domain:
            groups_by_domain[domain] = []
        groups_by_domain[domain].append(analysis.path)

    return list(groups_by_domain.values())

def calculate_speedup(strategy: ExecutionStrategy, parallel_groups: int) -> float:
    """Calcola speedup atteso."""
    if strategy == ExecutionStrategy.SEQUENTIAL:
        return 1.0
    elif strategy == ExecutionStrategy.PARALLEL:
        # Speedup tipico del 36% per parallel (da benchmark)
        return min(1.36, 1 + (parallel_groups - 1) * 0.2)
    elif strategy == ExecutionStrategy.WORKTREES:
        # Worktrees ha overhead setup ma parallelismo reale
        return min(2.0, 1 + (parallel_groups - 1) * 0.3)
    return 1.0

def analyze_task(file_paths: List[str], estimated_time: int = 30) -> TaskAnalysis:
    """
    Analisi completa di un task.

    Args:
        file_paths: Lista di file coinvolti nel task
        estimated_time: Tempo stimato in minuti

    Returns:
        TaskAnalysis con strategia raccomandata
    """
    # Analizza ogni file
    file_analyses = analyze_files(file_paths)

    # Calcola distribuzione domini
    domain_distribution = calculate_domain_distribution(file_analyses)

    # Check dipendenze
    has_dependencies = any(len(f.dependencies) > 0 for f in file_analyses)

    # Determina strategia
    strategy, reason = determine_strategy(
        file_count=len(file_paths),
        domain_count=len(domain_distribution),
        has_dependencies=has_dependencies,
        estimated_time_minutes=estimated_time
    )

    # Raggruppa per parallelismo
    parallel_groups = group_parallel_files(file_analyses)

    # Agenti suggeriti
    suggested_agents = list(set(f.agent for f in file_analyses))

    # Speedup atteso
    speedup = calculate_speedup(strategy, len(parallel_groups))

    return TaskAnalysis(
        files=file_analyses,
        strategy=strategy,
        strategy_reason=reason,
        domain_distribution=domain_distribution,
        suggested_agents=suggested_agents,
        parallel_groups=parallel_groups,
        estimated_speedup=speedup
    )

def format_analysis(analysis: TaskAnalysis) -> str:
    """Formatta analisi per output."""
    strategy_icons = {
        ExecutionStrategy.SEQUENTIAL: "➡️",
        ExecutionStrategy.PARALLEL: "🔀",
        ExecutionStrategy.WORKTREES: "🌳"
    }

    lines = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║  🧠 TASK ANALYSIS RESULT                                        ║",
        "╠══════════════════════════════════════════════════════════════════╣",
        f"║  {strategy_icons[analysis.strategy]} Strategia: {analysis.strategy.value.upper()}",
        f"║  📝 Motivo: {analysis.strategy_reason}",
        f"║  ⚡ Speedup atteso: {analysis.estimated_speedup:.2f}x",
        "║",
        "║  📂 DISTRIBUZIONE DOMINI:",
    ]

    for domain, count in analysis.domain_distribution.items():
        lines.append(f"║     • {domain}: {count} file")

    lines.append("║")
    lines.append("║  🐝 AGENTI SUGGERITI:")
    for agent in analysis.suggested_agents:
        lines.append(f"║     • {agent}")

    if analysis.strategy == ExecutionStrategy.PARALLEL:
        lines.append("║")
        lines.append("║  🔀 GRUPPI PARALLELI:")
        for i, group in enumerate(analysis.parallel_groups, 1):
            lines.append(f"║     Gruppo {i}: {', '.join(Path(p).name for p in group)}")

    lines.append("╚══════════════════════════════════════════════════════════════════╝")

    return "\n".join(lines)

def main():
    """Entry point CLI."""
    import argparse

    parser = argparse.ArgumentParser(description="CervellaSwarm Task Analyzer")
    parser.add_argument("files", nargs="*", help="File da analizzare")
    parser.add_argument("--time", "-t", type=int, default=30, help="Tempo stimato (minuti)")
    parser.add_argument("--json", "-j", action="store_true", help="Output JSON")
    args = parser.parse_args()

    print(f"🧠 CervellaSwarm Task Analyzer v{__version__}", file=sys.stderr)
    print("-" * 60, file=sys.stderr)

    if not args.files:
        parser.print_help()
        sys.exit(1)

    analysis = analyze_task(args.files, args.time)

    if args.json:
        output = {
            "strategy": analysis.strategy.value,
            "strategy_reason": analysis.strategy_reason,
            "estimated_speedup": analysis.estimated_speedup,
            "domain_distribution": analysis.domain_distribution,
            "suggested_agents": analysis.suggested_agents,
            "parallel_groups": analysis.parallel_groups,
            "files": [
                {
                    "path": f.path,
                    "domain": f.domain.value,
                    "agent": f.agent,
                    "dependencies": f.dependencies
                }
                for f in analysis.files
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(format_analysis(analysis))

if __name__ == "__main__":
    main()
