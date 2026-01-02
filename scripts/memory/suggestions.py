#!/usr/bin/env python3
"""
CervellaSwarm Suggestions - Sistema Suggerimenti Automatici

Genera suggerimenti basati su lezioni apprese e pattern di errori rilevati.
Aiuta gli agenti a evitare errori comuni e migliorare continuamente.

Usage:
    # Come modulo
    from suggestions import get_suggestions, get_context_aware_suggestions

    suggestions = get_suggestions(project='miracollo', limit=5)

    # CLI standalone
    python suggestions.py                    # Tutti i suggerimenti
    python suggestions.py -p miracollo       # Solo progetto Miracollo
    python suggestions.py -a frontend        # Solo agente frontend
    python suggestions.py --json             # Output JSON
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import sqlite3
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


# === COLORI ANSI (senza Rich) ===

class Colors:
    """Colori ANSI base per output CLI."""
    RED = '\033[91m'
    ORANGE = '\033[93m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


# === DATABASE CONNECTION ===

# Import centralizzato path management
sys.path.insert(0, str(Path(__file__).parent.parent))
from common.paths import get_db_path


def connect_db() -> sqlite3.Connection:
    """Connessione al database con gestione errori."""
    db_path = get_db_path()

    if not db_path.exists():
        print(f"❌ Database non trovato: {db_path}", file=sys.stderr)
        sys.exit(1)

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"❌ Errore connessione database: {e}", file=sys.stderr)
        sys.exit(1)


# === CORE FUNCTIONS ===

def get_suggestions(
    project: Optional[str] = None,
    agent: Optional[str] = None,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Ritorna lista di suggerimenti rilevanti basati su lezioni e pattern.

    Args:
        project: Filtra per progetto (es. 'miracollo', 'contabilita')
        agent: Filtra per agente (es. 'frontend', 'backend')
        limit: Numero massimo di suggerimenti (default: 5)

    Returns:
        Lista di dizionari con suggerimenti ordinati per severità
    """
    conn = connect_db()
    cursor = conn.cursor()

    suggestions = []

    # === LEZIONI APPRESE ===
    query_lessons = """
        SELECT
            'lesson' as source_type,
            pattern,
            category,
            severity,
            prevention,
            occurrence_count,
            project
        FROM lessons_learned
        WHERE status = 'ACTIVE'
    """

    params_lessons = []

    if project:
        query_lessons += " AND (project = ? OR project IS NULL)"
        params_lessons.append(project)

    if agent:
        query_lessons += " AND (agents_involved LIKE ? OR agents_involved IS NULL)"
        params_lessons.append(f"%{agent}%")

    query_lessons += " ORDER BY CASE severity "
    query_lessons += "WHEN 'CRITICAL' THEN 0 "
    query_lessons += "WHEN 'HIGH' THEN 1 "
    query_lessons += "WHEN 'MEDIUM' THEN 2 "
    query_lessons += "ELSE 3 END, occurrence_count DESC"

    cursor.execute(query_lessons, params_lessons)
    lessons = cursor.fetchall()

    for lesson in lessons:
        suggestions.append({
            'source': 'lesson',
            'pattern': lesson['pattern'],
            'category': lesson['category'],
            'severity': lesson['severity'] or 'MEDIUM',
            'prevention': lesson['prevention'],
            'occurrence_count': lesson['occurrence_count'] or 1,
            'project': lesson['project']
        })

    # === ERROR PATTERNS ===
    query_patterns = """
        SELECT
            'pattern' as source_type,
            pattern_name,
            pattern_type,
            severity_level,
            occurrence_count,
            mitigation_description
        FROM error_patterns
        WHERE status = 'ACTIVE'
    """

    # Pattern non hanno filtro progetto specifico (sono generici)
    query_patterns += " ORDER BY CASE severity_level "
    query_patterns += "WHEN 'CRITICAL' THEN 0 "
    query_patterns += "WHEN 'HIGH' THEN 1 "
    query_patterns += "WHEN 'MEDIUM' THEN 2 "
    query_patterns += "ELSE 3 END, occurrence_count DESC"

    cursor.execute(query_patterns)
    patterns = cursor.fetchall()

    for pattern in patterns:
        suggestions.append({
            'source': 'error_pattern',
            'pattern': pattern['pattern_name'],
            'category': pattern['pattern_type'],
            'severity': pattern['severity_level'] or 'MEDIUM',
            'prevention': pattern['mitigation_description'],
            'occurrence_count': pattern['occurrence_count'] or 1,
            'project': None  # Pattern sono cross-project
        })

    conn.close()

    # Ordina per severità e occorrenze (già ordinati nelle query, ma merge qui)
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    suggestions.sort(
        key=lambda s: (severity_order.get(s['severity'], 4), -s['occurrence_count'])
    )

    # Applica limite
    return suggestions[:limit]


def format_suggestion(suggestion: Dict[str, Any]) -> str:
    """
    Formatta un suggerimento per output CLI con colori ANSI.

    Args:
        suggestion: Dizionario con chiavi: severity, pattern, prevention

    Returns:
        Stringa formattata con emoji e colori
    """
    severity = suggestion.get('severity', 'MEDIUM')
    pattern = suggestion.get('pattern', 'Unknown')
    prevention = suggestion.get('prevention', 'N/A')
    count = suggestion.get('occurrence_count', 1)
    category = suggestion.get('category', '')

    # Emoji per severity
    emoji_map = {
        'CRITICAL': '🔴',
        'HIGH': '🟠',
        'MEDIUM': '🟡',
        'LOW': '🟢'
    }
    emoji = emoji_map.get(severity, '⚪')

    # Colore per severity
    color_map = {
        'CRITICAL': Colors.RED,
        'HIGH': Colors.ORANGE,
        'MEDIUM': Colors.YELLOW,
        'LOW': Colors.GREEN
    }
    color = color_map.get(severity, '')

    # Formattazione
    output = f"{emoji} {color}[{severity}]{Colors.RESET} {pattern}"

    if category:
        output += f" ({category})"

    if prevention:
        output += f"\n   → {prevention}"

    if count > 1:
        output += f"\n   📊 Ripetuto {count}x"

    return output


def get_context_aware_suggestions(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Ritorna suggerimenti contestuali basati sulla directory corrente.

    Rileva automaticamente il progetto dal CWD e ritorna suggerimenti rilevanti.

    Args:
        limit: Numero massimo di suggerimenti (default: 5)

    Returns:
        Lista di suggerimenti contestuali
    """
    cwd = Path.cwd()

    # Prova a rilevare il progetto dal path
    project = None

    if 'miracollo' in str(cwd).lower():
        project = 'miracollo'
    elif 'contabilita' in str(cwd).lower():
        project = 'contabilita'
    elif 'libertaio' in str(cwd).lower():
        project = 'libertaio'

    # Ritorna suggerimenti filtrati per progetto (se rilevato)
    return get_suggestions(project=project, limit=limit)


# === CLI INTERFACE ===

def format_json_output(suggestions: List[Dict[str, Any]]) -> str:
    """Formatta suggerimenti come JSON."""
    return json.dumps({
        'count': len(suggestions),
        'suggestions': suggestions
    }, indent=2, ensure_ascii=False)


def format_text_output(suggestions: List[Dict[str, Any]]) -> str:
    """Formatta suggerimenti come testo colorato."""
    if not suggestions:
        return f"{Colors.GREEN}✅ Nessun suggerimento attivo! Sistema pulito.{Colors.RESET}"

    output = []
    output.append(f"\n{Colors.BOLD}💡 SUGGERIMENTI ATTIVI ({len(suggestions)}){Colors.RESET}")
    output.append("─" * 60)

    for suggestion in suggestions:
        output.append(format_suggestion(suggestion))
        output.append("")  # Riga vuota tra suggerimenti

    return "\n".join(output)


def main():
    """Entry point per CLI standalone."""
    parser = argparse.ArgumentParser(
        description="CervellaSwarm Suggestions - Suggerimenti automatici basati su lezioni"
    )

    parser.add_argument(
        '-p', '--project',
        type=str,
        help='Filtra per progetto (es. miracollo, contabilita)'
    )

    parser.add_argument(
        '-a', '--agent',
        type=str,
        help='Filtra per agente (es. frontend, backend, tester)'
    )

    parser.add_argument(
        '-l', '--limit',
        type=int,
        default=5,
        help='Numero massimo di suggerimenti (default: 5)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output in formato JSON'
    )

    args = parser.parse_args()

    # Ottieni suggerimenti
    suggestions = get_suggestions(
        project=args.project,
        agent=args.agent,
        limit=args.limit
    )

    # Output
    if args.json:
        print(format_json_output(suggestions))
    else:
        print(format_text_output(suggestions))


if __name__ == '__main__':
    main()
