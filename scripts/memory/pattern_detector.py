#!/usr/bin/env python3
"""
CervellaSwarm Pattern Detector - Sistema di Rilevamento Pattern Errori

Analizza errori nel database swarm_memory.db e rileva pattern ricorrenti
usando algoritmo di similarità basato su difflib.SequenceMatcher.

Usage:
    from pattern_detector import detect_error_patterns

    patterns = detect_error_patterns(
        errors=error_list,
        similarity_threshold=0.7,
        min_occurrences=3
    )
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

import sqlite3
import sys
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional


def get_db_path() -> Path:
    """Ritorna il path al database swarm_memory.db."""
    script_dir = Path(__file__).parent
    db_path = script_dir / "../../data/swarm_memory.db"
    return db_path.resolve()


def connect_db() -> sqlite3.Connection:
    """Connessione al database con gestione errori."""
    db_path = get_db_path()

    if not db_path.exists():
        print(f"❌ Database non trovato: {db_path}")
        sys.exit(1)

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"❌ Errore connessione database: {e}")
        sys.exit(1)


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calcola la similarità tra due stringhe usando SequenceMatcher.

    Args:
        text1: Prima stringa
        text2: Seconda stringa

    Returns:
        float: Similarità da 0.0 a 1.0 (1.0 = identiche)
    """
    if not text1 or not text2:
        return 0.0

    # Normalizza: lowercase e strip whitespace
    t1 = text1.lower().strip()
    t2 = text2.lower().strip()

    # SequenceMatcher per calcolare ratio
    matcher = SequenceMatcher(None, t1, t2)
    return matcher.ratio()


def group_similar_errors(
    errors: List[Dict[str, Any]],
    similarity_threshold: float = 0.7
) -> List[List[Dict[str, Any]]]:
    """
    Raggruppa errori simili in cluster.

    Args:
        errors: Lista di dizionari con chiave 'error_message'
        similarity_threshold: Soglia di similarità (default: 0.7)

    Returns:
        Lista di gruppi (ogni gruppo è una lista di errori simili)
    """
    if not errors:
        return []

    groups = []
    processed = set()

    for i, error in enumerate(errors):
        if i in processed:
            continue

        # Crea nuovo gruppo con questo errore
        current_group = [error]
        processed.add(i)

        # Trova errori simili
        for j, other_error in enumerate(errors):
            if j in processed or j <= i:
                continue

            # Calcola similarità
            similarity = calculate_similarity(
                error.get('error_message', ''),
                other_error.get('error_message', '')
            )

            # Se supera la soglia, aggiungi al gruppo
            if similarity >= similarity_threshold:
                current_group.append(other_error)
                processed.add(j)

        groups.append(current_group)

    return groups


def extract_pattern_name(error_group: List[Dict[str, Any]]) -> str:
    """
    Estrae un nome rappresentativo per il pattern dal gruppo di errori.

    Usa il messaggio più comune o il primo se tutti diversi.

    Args:
        error_group: Lista di errori simili

    Returns:
        str: Nome del pattern (max 100 chars)
    """
    if not error_group:
        return "Unknown Pattern"

    # Prendi il primo errore come rappresentante
    representative = error_group[0].get('error_message', 'Unknown Error')

    # Tronca se troppo lungo
    max_len = 100
    if len(representative) > max_len:
        representative = representative[:max_len-3] + "..."

    return representative


def infer_severity(occurrence_count: int) -> str:
    """
    Inferisce la severity basandosi sul numero di occorrenze.

    Args:
        occurrence_count: Numero di volte che il pattern si è ripetuto

    Returns:
        str: CRITICAL | HIGH | MEDIUM | LOW
    """
    if occurrence_count >= 10:
        return "CRITICAL"
    elif occurrence_count >= 5:
        return "HIGH"
    elif occurrence_count >= 3:
        return "MEDIUM"
    else:
        return "LOW"


def detect_error_patterns(
    errors: List[Dict[str, Any]],
    similarity_threshold: float = 0.7,
    min_occurrences: int = 3
) -> List[Dict[str, Any]]:
    """
    Rileva pattern di errori ricorrenti da una lista di errori.

    Args:
        errors: Lista di dizionari con almeno chiave 'error_message'
        similarity_threshold: Soglia di similarità (0.0-1.0, default: 0.7)
        min_occurrences: Minimo numero di occorrenze per considerare un pattern

    Returns:
        Lista di pattern rilevati (dizionari con metadati)
    """
    if not errors:
        return []

    # Step 1: Raggruppa errori simili
    groups = group_similar_errors(errors, similarity_threshold)

    # Step 2: Filtra gruppi con occorrenze >= min_occurrences
    patterns = []

    for group in groups:
        occurrence_count = len(group)

        if occurrence_count < min_occurrences:
            continue  # Salta pattern con poche occorrenze

        # Estrai metadati dal gruppo
        pattern_name = extract_pattern_name(group)
        severity = infer_severity(occurrence_count)

        # Trova ultimo timestamp
        last_seen = None
        for error in group:
            if 'timestamp' in error and error['timestamp']:
                if not last_seen or error['timestamp'] > last_seen:
                    last_seen = error['timestamp']

        # Trova tipo di errore più comune
        error_types = [e.get('event_type', 'UNKNOWN') for e in group]
        pattern_type = max(set(error_types), key=error_types.count)

        # Costruisci dizionario pattern
        pattern = {
            'pattern_name': pattern_name,
            'pattern_type': pattern_type,
            'severity_level': severity,
            'occurrence_count': occurrence_count,
            'last_seen': last_seen or datetime.now().isoformat(),
            'status': 'ACTIVE',
            'root_cause_hypothesis': None,  # Da analizzare manualmente
            'mitigation_description': None,  # Da definire manualmente
            'error_ids': [e.get('id') for e in group if 'id' in e]  # Per riferimento
        }

        patterns.append(pattern)

    # Step 3: Ordina per severity e occurrence_count
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    patterns.sort(
        key=lambda p: (severity_order.get(p['severity_level'], 4), -p['occurrence_count'])
    )

    return patterns


def save_patterns_to_db(patterns: List[Dict[str, Any]]) -> Tuple[int, int]:
    """
    Salva i pattern rilevati nel database.

    Se un pattern con lo stesso nome esiste già:
    - Aggiorna occurrence_count
    - Aggiorna last_seen

    Altrimenti:
    - Inserisce nuovo pattern

    Args:
        patterns: Lista di pattern da salvare

    Returns:
        Tuple (new_patterns, updated_patterns)
    """
    if not patterns:
        return (0, 0)

    conn = connect_db()
    cursor = conn.cursor()

    new_count = 0
    updated_count = 0

    for pattern in patterns:
        # Controlla se esiste già
        cursor.execute("""
            SELECT id, occurrence_count
            FROM error_patterns
            WHERE pattern_name = ?
        """, (pattern['pattern_name'],))

        existing = cursor.fetchone()

        if existing:
            # AGGIORNA pattern esistente
            new_occurrence = existing['occurrence_count'] + pattern['occurrence_count']

            cursor.execute("""
                UPDATE error_patterns
                SET occurrence_count = ?,
                    last_seen = ?,
                    severity_level = ?
                WHERE id = ?
            """, (
                new_occurrence,
                pattern['last_seen'],
                pattern['severity_level'],
                existing['id']
            ))

            updated_count += 1
        else:
            # INSERISCI nuovo pattern
            cursor.execute("""
                INSERT INTO error_patterns (
                    pattern_name, pattern_type, severity_level,
                    occurrence_count, last_seen, status,
                    root_cause_hypothesis, mitigation_description
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                pattern['pattern_name'],
                pattern['pattern_type'],
                pattern['severity_level'],
                pattern['occurrence_count'],
                pattern['last_seen'],
                pattern['status'],
                pattern['root_cause_hypothesis'],
                pattern['mitigation_description']
            ))

            new_count += 1

    conn.commit()
    conn.close()

    return (new_count, updated_count)


def fetch_recent_errors(days: int = 7) -> List[Dict[str, Any]]:
    """
    Recupera errori recenti dal database (ultimi N giorni).

    Args:
        days: Numero di giorni da analizzare (default: 7)

    Returns:
        Lista di errori (dizionari)
    """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(f"""
        SELECT
            id,
            event_type,
            error_message,
            timestamp,
            agent_name,
            project
        FROM swarm_events
        WHERE success = 0
          AND error_message IS NOT NULL
          AND datetime(timestamp) >= datetime('now', '-{days} days')
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    # Converti Row in dict
    errors = [dict(row) for row in rows]

    return errors


# === MAIN (per testing standalone) ===

def main():
    """Entry point per testing del pattern detector."""
    print("🔍 CervellaSwarm Pattern Detector")
    print(f"   Version: {__version__} ({__version_date__})")
    print()

    # Fetch errori recenti (ultimi 30 giorni)
    print("📊 Recupero errori recenti (ultimi 30 giorni)...")
    errors = fetch_recent_errors(days=30)

    if not errors:
        print("✅ Nessun errore trovato! Sistema stabile.")
        return

    print(f"   Trovati {len(errors)} errori")
    print()

    # Rileva pattern
    print("🔎 Rilevamento pattern in corso...")
    patterns = detect_error_patterns(
        errors=errors,
        similarity_threshold=0.7,
        min_occurrences=3
    )

    if not patterns:
        print("✅ Nessun pattern ricorrente rilevato (soglia: 3+ occorrenze)")
        return

    print(f"   Rilevati {len(patterns)} pattern")
    print()

    # Salva nel database
    print("💾 Salvataggio pattern nel database...")
    new, updated = save_patterns_to_db(patterns)
    print(f"   ✅ Nuovi: {new} | Aggiornati: {updated}")
    print()

    # Mostra riepilogo
    print("📋 RIEPILOGO PATTERN RILEVATI:")
    print("-" * 60)

    for i, pattern in enumerate(patterns, 1):
        severity_emoji = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }.get(pattern['severity_level'], '⚪')

        print(f"{i}. {severity_emoji} [{pattern['severity_level']}] {pattern['pattern_name'][:50]}")
        print(f"   Occorrenze: {pattern['occurrence_count']} | Tipo: {pattern['pattern_type']}")
        print()

    print("✅ Pattern detection completato!")


if __name__ == '__main__':
    main()
