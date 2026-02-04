#!/usr/bin/env python3
"""
CervellaSwarm Output Validator - Reflection Pattern

Valida output dei worker e suggerisce retry se necessario.
Parte del sistema di auto-validazione per migliorare qualità output sciame.

Usage:
    python3 output_validator.py --last-output              # Valida ultimo output creato
    python3 output_validator.py --file TASK_ID_output.md   # Valida file specifico
    python3 output_validator.py --task TASK_ID             # Valida output di un task

Exit codes:
    0 = VALID (output OK)
    1 = INVALID (errori trovati)
    2 = ERROR (validazione fallita)

Versione: 1.0.0
Data: 2026-02-04
Sessione: 336
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-04"

from pathlib import Path
from typing import Dict, List, Optional
import re
import sys
import json
import argparse
from datetime import datetime

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

SWARM_DIR = Path(".swarm")
TASKS_DIR = SWARM_DIR / "tasks"
LOGS_DIR = SWARM_DIR / "logs"

# Marker di errore da cercare nei log
ERROR_MARKERS = [
    "Error:",
    "ERROR:",
    "Traceback",
    "FAILED",
    "Exception:",
    "RuntimeError:",
    "ValueError:",
    "TypeError:",
    "SyntaxError:",
    "fatal:",
]

# Marker di incompletezza da cercare nell'output
INCOMPLETE_MARKERS = [
    "TODO:",
    "FIXME:",
    "XXX:",
    "HACK:",
    "...",  # Ellipsis spesso indica placeholder
]

# Minima lunghezza output valido (caratteri)
MIN_OUTPUT_LENGTH = 100


# ============================================================================
# FUNZIONI VALIDAZIONE
# ============================================================================

def validate_output(output_file: Path) -> Dict:
    """
    Valida un file di output worker.

    Checks:
    1. File esiste e non vuoto
    2. Nessun error marker nel contenuto
    3. Nessun marker di incompletezza
    4. Lunghezza minima raggiunta
    5. (Opzionale) Log corrispondente non ha errori

    Args:
        output_file: Path al file _output.md

    Returns:
        {
            'valid': bool,
            'errors': List[str],       # Errori bloccanti
            'warnings': List[str],      # Warning non bloccanti
            'retry_needed': bool,
            'retry_context': str,       # Contesto aggiuntivo per retry
            'score': int                # 0-100 score qualità
        }
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'retry_needed': False,
        'retry_context': '',
        'score': 100
    }

    # CHECK 1: File esiste
    if not output_file.exists():
        result['valid'] = False
        result['errors'].append(f"Output file non esiste: {output_file}")
        result['retry_needed'] = True
        result['retry_context'] = "Worker non ha creato file output. Verifica completamento task."
        result['score'] = 0
        return result

    # CHECK 2: File non vuoto
    try:
        content = output_file.read_text()
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"Impossibile leggere output: {e}")
        result['retry_needed'] = True
        result['retry_context'] = "File output corrotto o inaccessibile."
        result['score'] = 0
        return result

    if len(content.strip()) == 0:
        result['valid'] = False
        result['errors'].append("Output vuoto!")
        result['retry_needed'] = True
        result['retry_context'] = "Worker ha creato file output ma è vuoto. Task non completato?"
        result['score'] = 0
        return result

    # CHECK 3: Lunghezza minima
    if len(content) < MIN_OUTPUT_LENGTH:
        result['warnings'].append(f"Output molto corto ({len(content)} caratteri < {MIN_OUTPUT_LENGTH})")
        result['score'] -= 10

    # CHECK 4: Error markers nel contenuto
    error_found = []
    for marker in ERROR_MARKERS:
        if marker in content:
            error_found.append(marker)

    if error_found:
        result['valid'] = False
        result['errors'].append(f"Error markers trovati: {', '.join(error_found)}")
        result['retry_needed'] = True
        result['retry_context'] = "Output contiene messaggi di errore. Task fallito?"
        result['score'] -= 40

    # CHECK 5: Marker di incompletezza
    incomplete_found = []
    for marker in INCOMPLETE_MARKERS:
        # Ignora marker nei code block (potrebbero essere legittimi)
        # Semplice euristica: se c'è "```" prima del marker, skippa
        if marker in content:
            # Check se in code block
            before_marker = content.split(marker)[0]
            code_blocks = before_marker.count("```")
            if code_blocks % 2 == 0:  # Numero pari = fuori da code block
                incomplete_found.append(marker)

    if incomplete_found:
        result['warnings'].append(f"Marker incompletezza: {', '.join(incomplete_found)}")
        result['score'] -= 15

    # CHECK 6: Success indicators (bonus score)
    success_indicators = ["✓", "DONE", "Completato", "Success", "OK"]
    success_count = sum(1 for indicator in success_indicators if indicator in content)

    if success_count > 0:
        result['score'] = min(100, result['score'] + 5)  # Bonus

    # CHECK 7: Log corrispondente (se esiste)
    log_check = _check_corresponding_log(output_file)
    if log_check['has_errors']:
        result['warnings'].append(f"Log contiene errori: {log_check['error_summary']}")
        result['score'] -= 10

    # Decide retry_needed basato su score finale
    if result['score'] < 50:
        result['retry_needed'] = True
        result['retry_context'] = f"Qualità output bassa (score: {result['score']}). Review consigliata."

    # Adjust valid flag
    if result['errors']:
        result['valid'] = False

    return result


def _check_corresponding_log(output_file: Path) -> Dict:
    """
    Cerca log corrispondente all'output e controlla errori.

    Args:
        output_file: Path al file _output.md

    Returns:
        {
            'has_errors': bool,
            'error_summary': str,
            'log_file': Optional[Path]
        }
    """
    result = {
        'has_errors': False,
        'error_summary': '',
        'log_file': None
    }

    # Estrai task_id dal filename: TASK_123_output.md -> TASK_123
    task_id = output_file.stem.replace('_output', '')

    # Cerca log più recente contenente il task_id
    # Log format: worker_YYYYMMDD_HHMMSS.log
    if not LOGS_DIR.exists():
        return result

    matching_logs = []
    for log_file in LOGS_DIR.glob("worker_*.log"):
        # Check se log contiene il task_id
        try:
            log_content = log_file.read_text()
            if task_id in log_content:
                matching_logs.append((log_file, log_file.stat().st_mtime))
        except (OSError, IOError, PermissionError):
            continue

    if not matching_logs:
        return result

    # Prendi log più recente
    latest_log = max(matching_logs, key=lambda x: x[1])[0]
    result['log_file'] = latest_log

    # Check errori nel log
    try:
        log_content = latest_log.read_text()
        errors_found = []
        for marker in ERROR_MARKERS:
            if marker in log_content:
                errors_found.append(marker)

        if errors_found:
            result['has_errors'] = True
            result['error_summary'] = f"{len(errors_found)} error markers in log"
    except (OSError, IOError, PermissionError):
        pass

    return result


def find_last_output() -> Optional[Path]:
    """
    Trova l'ultimo file _output.md creato.

    Returns:
        Path al file o None se non trovato
    """
    if not TASKS_DIR.exists():
        return None

    output_files = list(TASKS_DIR.glob("*_output.md"))
    if not output_files:
        return None

    # Ordina per modification time
    output_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    return output_files[0]


def find_task_output(task_id: str) -> Optional[Path]:
    """
    Trova file output per un task_id specifico.

    Args:
        task_id: ID del task (es. TASK_001)

    Returns:
        Path al file o None se non trovato
    """
    output_file = TASKS_DIR / f"{task_id}_output.md"
    return output_file if output_file.exists() else None


# ============================================================================
# CLI
# ============================================================================

def print_validation_result(result: Dict, output_file: Path, verbose: bool = False):
    """Stampa risultato validazione in formato human-readable."""
    status = "✓ VALID" if result['valid'] else "✗ INVALID"
    print(f"\n{status} - {output_file.name}")
    print(f"Score: {result['score']}/100")

    if result['errors']:
        print("\nERRORS:")
        for error in result['errors']:
            print(f"  - {error}")

    if result['warnings']:
        print("\nWARNINGS:")
        for warning in result['warnings']:
            print(f"  - {warning}")

    if result['retry_needed']:
        print(f"\n⚠️  RETRY SUGGESTED")
        if result['retry_context']:
            print(f"Context: {result['retry_context']}")

    if verbose:
        print(f"\nFull result:")
        print(json.dumps(result, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Output Validator - Reflection Pattern"
    )
    parser.add_argument(
        '--last-output',
        action='store_true',
        help='Valida ultimo output creato'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Valida file specifico'
    )
    parser.add_argument(
        '--task',
        type=str,
        help='Valida output di un task (es. TASK_001)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in formato JSON'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Output verboso'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'output_validator.py v{__version__}'
    )

    args = parser.parse_args()

    # Determina quale file validare
    output_file = None

    if args.last_output:
        output_file = find_last_output()
        if not output_file:
            print("ERROR: Nessun output trovato!", file=sys.stderr)
            sys.exit(2)
    elif args.file:
        output_file = Path(args.file)
        # Se path relativo, prima prova come-is, poi dentro TASKS_DIR
        if not output_file.is_absolute() and not output_file.exists():
            output_file = TASKS_DIR / args.file
    elif args.task:
        output_file = find_task_output(args.task)
        if not output_file:
            print(f"ERROR: Output non trovato per task {args.task}", file=sys.stderr)
            sys.exit(2)
    else:
        parser.print_help()
        sys.exit(0)

    # Valida
    result = validate_output(output_file)

    # Output
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_validation_result(result, output_file, verbose=args.verbose)

    # Exit code
    if result['valid']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
