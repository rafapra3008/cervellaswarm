#!/usr/bin/env python3
"""
CervellaSwarm Dashboard - Data Layer
Funzioni per raccolta dati da task manager e heartbeat.
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import task_manager dal sistema
try:
    from task_manager import TASKS_DIR
except ImportError:
    # Fallback se non siamo nella directory giusta
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from task_manager import TASKS_DIR


def get_worker_status(worker_name: str, tasks: List[Dict]) -> Dict:
    """
    Determina lo stato di un worker basandosi sui task assegnati.

    Args:
        worker_name: Nome del worker
        tasks: Lista di tutti i task

    Returns:
        Dict con: status ('active', 'idle'), current_task, task_count
    """
    worker_tasks = [t for t in tasks if t['agent'] == worker_name]

    # Cerca task in working
    working_tasks = [t for t in worker_tasks if t['status'] == 'working']
    if working_tasks:
        task = working_tasks[0]  # Prendi il primo task working
        return {
            'status': 'active',
            'current_task': f"{task['task_id']}: {get_task_description(task['task_id'])}",
            'task_count': len(worker_tasks)
        }

    # Cerca task ready
    ready_tasks = [t for t in worker_tasks if t['status'] == 'ready']
    if ready_tasks:
        return {
            'status': 'ready',
            'current_task': f"{len(ready_tasks)} task pending",
            'task_count': len(worker_tasks)
        }

    # Altrimenti idle
    return {
        'status': 'idle',
        'current_task': '-',
        'task_count': len(worker_tasks)
    }


def get_task_description(task_id: str) -> str:
    """
    Estrae la descrizione breve di un task dal file.

    Args:
        task_id: ID del task

    Returns:
        Descrizione breve (prime 40 char del titolo)
    """
    try:
        task_file = Path(TASKS_DIR) / f"{task_id}.md"
        if not task_file.exists():
            return "Unknown task"

        content = task_file.read_text()
        lines = content.split('\n')

        # Prima riga dovrebbe essere "# TASK: Descrizione"
        if lines and lines[0].startswith('# TASK:'):
            desc = lines[0].replace('# TASK:', '').strip()
            # Tronca a 40 caratteri
            if len(desc) > 40:
                desc = desc[:37] + '...'
            return desc

        return "No description"
    except Exception:
        return "Error reading task"


def get_task_queue_stats(tasks: List[Dict]) -> Dict:
    """
    Calcola statistiche della task queue.

    Args:
        tasks: Lista di tutti i task

    Returns:
        Dict con: pending, in_progress, completed, failed
    """
    stats = {
        'pending': 0,
        'ready': 0,
        'in_progress': 0,
        'completed': 0,
        'failed': 0
    }

    for task in tasks:
        status = task['status']
        if status == 'created':
            stats['pending'] += 1
        elif status == 'ready':
            stats['ready'] += 1
        elif status == 'working':
            stats['in_progress'] += 1
        elif status == 'done':
            stats['completed'] += 1
        # Non abbiamo status 'failed' nel task_manager, ma lo teniamo per futuro

    return stats


def get_recent_activity(tasks: List[Dict], limit: int = 5) -> List[Dict]:
    """
    Ottiene l'attivita recente dai file task.

    Args:
        tasks: Lista di tutti i task
        limit: Numero massimo di eventi da mostrare

    Returns:
        Lista di dict con: timestamp, agent, action, task_id
    """
    activities = []

    tasks_path = Path(TASKS_DIR)

    # Raccogli tutti i file marker con timestamp
    for task_file in tasks_path.glob("TASK_*"):
        if task_file.suffix in ['.done', '.working', '.ready', '.ack_received', '.ack_understood']:
            task_id = task_file.stem
            if task_file.suffix in ['.ack_received', '.ack_understood']:
                # Rimuovi il suffisso per ottenere task_id
                task_id = task_file.name.replace('.ack_received', '').replace('.ack_understood', '')

            action_map = {
                '.done': 'Completed',
                '.working': 'Started',
                '.ready': 'Ready',
                '.ack_received': 'Received',
                '.ack_understood': 'Understood'
            }

            # Cerca agent dal task
            agent = 'unknown'
            for t in tasks:
                if t['task_id'] == task_id:
                    agent = t['agent'].replace('cervella-', '')
                    break

            activities.append({
                'timestamp': task_file.stat().st_mtime,
                'agent': agent,
                'action': action_map.get(task_file.suffix, 'Unknown'),
                'task_id': task_id
            })

    # Ordina per timestamp decrescente e prendi solo limit
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    return activities[:limit]


def calculate_session_duration() -> str:
    """
    Calcola la durata della sessione corrente.

    Returns:
        Stringa con durata (es. "45m")
    """
    # Per ora ritorniamo un valore fisso
    # In futuro potremmo leggere da un file di session start
    return "N/A"


def get_live_activity_from_heartbeat() -> List[Dict]:
    """
    Legge heartbeat files e mostra attivita live dei worker.

    Returns:
        Lista di dict con: worker, timestamp, task, action, is_active, age
    """
    activities = []
    status_dir = Path('.swarm/status')

    if not status_dir.exists():
        return activities

    for hb_file in status_dir.glob('heartbeat_*.log'):
        try:
            content = hb_file.read_text().strip()
            if not content:
                continue

            lines = content.split('\n')
            last_line = lines[-1]
            parts = last_line.split('|')

            if len(parts) >= 3:
                timestamp = int(parts[0])
                task = parts[1]
                action = parts[2]

                age = int(time.time()) - timestamp
                is_active = age < 120  # Active se heartbeat < 2 minuti

                activities.append({
                    'worker': hb_file.stem.replace('heartbeat_', ''),
                    'timestamp': timestamp,
                    'task': task,
                    'action': action,
                    'age': age,
                    'is_active': is_active
                })
        except Exception:
            continue

    return activities
