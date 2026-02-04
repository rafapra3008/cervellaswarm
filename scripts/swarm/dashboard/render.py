"""
CervellaSwarm Dashboard - Rendering Layer

Funzioni per renderizzare la dashboard ASCII e output JSON.
Separato dal data layer per migliore manutenibilità.

Responsabilità:
- Rendering dashboard ASCII
- Rendering JSON output
- Formattazione colori e allineamento
- Layout e struttura visiva
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

import json
from datetime import datetime
from typing import Dict, List

# Import dal data layer
from .data import (
    get_worker_status,
    get_task_queue_stats,
    get_recent_activity,
    calculate_session_duration,
    get_live_activity_from_heartbeat,
)

# Import colors
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from common.colors import Colors, colorize


# ========== WORKERS CONFIGURAZIONE ==========

WORKERS = [
    {'name': 'cervella-orchestrator', 'emoji': '👑', 'type': 'regina'},
    {'name': 'cervella-guardiana-qualita', 'emoji': '🛡️', 'type': 'guardiana'},
    {'name': 'cervella-guardiana-ops', 'emoji': '🛡️', 'type': 'guardiana'},
    {'name': 'cervella-guardiana-ricerca', 'emoji': '🛡️', 'type': 'guardiana'},
    {'name': 'cervella-backend', 'emoji': '⚙️', 'type': 'worker'},
    {'name': 'cervella-frontend', 'emoji': '🎨', 'type': 'worker'},
    {'name': 'cervella-tester', 'emoji': '🧪', 'type': 'worker'},
    {'name': 'cervella-reviewer', 'emoji': '📋', 'type': 'worker'},
    {'name': 'cervella-researcher', 'emoji': '🔬', 'type': 'worker'},
    {'name': 'cervella-scienziata', 'emoji': '🔬', 'type': 'worker'},
    {'name': 'cervella-ingegnera', 'emoji': '👷‍♀️', 'type': 'worker'},
    {'name': 'cervella-marketing', 'emoji': '📈', 'type': 'worker'},
    {'name': 'cervella-devops', 'emoji': '🚀', 'type': 'worker'},
    {'name': 'cervella-docs', 'emoji': '📝', 'type': 'worker'},
    {'name': 'cervella-data', 'emoji': '📊', 'type': 'worker'},
    {'name': 'cervella-security', 'emoji': '🔒', 'type': 'worker'},
]


# ========== RENDERING DASHBOARD ==========

def render_header() -> str:
    """Renderizza l'header della dashboard."""
    lines = []
    lines.append("╔══════════════════════════════════════════════════════════════════════════════════════╗")
    lines.append("║" + colorize("                         🐝 CERVELLASWARM DASHBOARD                                  ", Colors.BOLD) + "║")
    lines.append("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    return '\n'.join(lines)


def render_workers(tasks: List[Dict]) -> str:
    """Renderizza la tabella workers."""
    lines = []
    lines.append("║                                                                                      ║")
    lines.append("║  " + colorize("WORKERS STATUS", Colors.BOLD) + "                                                                      ║")
    lines.append("║  ┌────────────────────────────┬──────────┬─────────────────────────────────────────┐ ║")
    lines.append("║  │ Worker                     │ Status   │ Current Task                            │ ║")
    lines.append("║  ├────────────────────────────┼──────────┼─────────────────────────────────────────┤ ║")

    for worker in WORKERS:
        status_info = get_worker_status(worker['name'], tasks)

        # Formatta nome worker con emoji
        worker_display = f"{worker['emoji']} {worker['name'].replace('cervella-', '')}"

        # Formatta status con colore
        status = status_info['status']
        if status == 'active':
            status_display = colorize("● ACTIVE", Colors.BRIGHT_GREEN)
        elif status == 'ready':
            status_display = colorize("◐ READY ", Colors.BRIGHT_YELLOW)
        else:
            status_display = colorize("○ IDLE  ", Colors.BRIGHT_BLACK)

        # Tronca current_task a 40 caratteri
        current_task = status_info['current_task']
        if len(current_task) > 40:
            current_task = current_task[:37] + '...'

        # Calcola padding per allineare colonne
        # Nota: dobbiamo considerare i codici colore ANSI nel calcolo
        worker_clean = Colors.strip(worker_display)
        status_clean = Colors.strip(status_display)

        worker_pad = 27 - len(worker_clean)
        status_pad = 9 - len(status_clean)
        task_pad = 40 - len(current_task)

        line = f"║  │ {worker_display}{' ' * worker_pad}│ {status_display}{' ' * status_pad}│ {current_task}{' ' * task_pad}│ ║"
        lines.append(line)

    lines.append("║  └────────────────────────────┴──────────┴─────────────────────────────────────────┘ ║")
    return '\n'.join(lines)


def render_stats(tasks: List[Dict]) -> str:
    """Renderizza le statistiche task queue e metrics."""
    lines = []

    stats = get_task_queue_stats(tasks)
    duration = calculate_session_duration()

    lines.append("║                                                                                      ║")
    lines.append("║  " + colorize("TASK QUEUE", Colors.BOLD) + "                          " + colorize("METRICS", Colors.BOLD) + "                                      ║")
    lines.append("║  ┌──────────────────────┐           ┌──────────────────────┐                        ║")

    # Task Queue
    pending = colorize(f"{stats['pending'] + stats['ready']}", Colors.BRIGHT_YELLOW)
    in_progress = colorize(f"{stats['in_progress']}", Colors.BRIGHT_GREEN)
    completed = colorize(f"{stats['completed']}", Colors.BRIGHT_CYAN)

    # Metrics
    failed = colorize(f"{stats['failed']}", Colors.BRIGHT_RED if stats['failed'] > 0 else Colors.BRIGHT_GREEN)

    # Calcola padding
    pending_clean = Colors.strip(pending)
    in_progress_clean = Colors.strip(in_progress)
    completed_clean_left = Colors.strip(completed)
    completed_clean_right = Colors.strip(completed)
    failed_clean = Colors.strip(failed)

    pending_pad = 3 - len(pending_clean)
    in_progress_pad = 2 - len(in_progress_clean)
    completed_pad_left = 2 - len(completed_clean_left)
    completed_pad_right = 2 - len(completed_clean_right)
    failed_pad = 4 - len(failed_clean)

    lines.append(f"║  │ Pending:    {pending}{' ' * pending_pad}        │           │ Completed: {completed}{' ' * completed_pad_right}        │                        ║")
    lines.append(f"║  │ In Progress: {in_progress}{' ' * in_progress_pad}       │           │ Failed:    {failed}{' ' * failed_pad}        │                        ║")
    lines.append(f"║  │ Completed:  {completed}{' ' * completed_pad_left}        │           │ Duration:  {duration}        │                        ║")
    lines.append("║  └──────────────────────┘           └──────────────────────┘                        ║")

    return '\n'.join(lines)


def render_activity(tasks: List[Dict]) -> str:
    """Renderizza l'attività recente."""
    lines = []

    lines.append("║                                                                                      ║")
    lines.append("║  " + colorize("LAST ACTIVITY", Colors.BOLD) + "                                                                        ║")

    activities = get_recent_activity(tasks, limit=5)

    if not activities:
        lines.append("║  " + colorize("No recent activity", Colors.DIM) + "                                                                         ║")
    else:
        for activity in activities:
            # Formatta timestamp
            dt = datetime.fromtimestamp(activity['timestamp'])
            time_str = dt.strftime("%H:%M:%S")

            # Formatta agent (massimo 12 caratteri)
            agent = activity['agent'][:12]

            # Formatta action con colore
            action = activity['action']
            if action == 'Completed':
                action_display = colorize(action, Colors.BRIGHT_GREEN)
            elif action == 'Started':
                action_display = colorize(action, Colors.BRIGHT_YELLOW)
            else:
                action_display = colorize(action, Colors.BRIGHT_CYAN)

            # Formatta messaggio
            message = f"{activity['task_id']}"

            # Calcola padding
            action_clean = Colors.strip(action_display)
            agent_pad = 12 - len(agent)
            action_pad = 12 - len(action_clean)

            line = f"║  {time_str} | {agent}{' ' * agent_pad}| {action_display}{' ' * action_pad}| {message}"

            # Padding finale per allineamento
            line_clean = Colors.strip(line)
            final_pad = 86 - len(line_clean)
            line += ' ' * final_pad + "║"

            lines.append(line)

    return '\n'.join(lines)


def render_heartbeat() -> str:
    """Renderizza la sezione heartbeat live."""
    lines = []

    lines.append("║                                                                                      ║")
    lines.append("║  " + colorize("LIVE HEARTBEAT", Colors.BOLD) + "                                                                       ║")

    activities = get_live_activity_from_heartbeat()

    if not activities:
        lines.append("║  " + colorize("Nessun heartbeat - i worker non hanno ancora scritto", Colors.DIM) + "                          ║")
    else:
        for activity in activities:
            worker = activity['worker'][:12]
            action = activity['action'][:40] if activity['action'] else '-'
            age = activity['age']

            # Formatta age
            if age < 60:
                age_str = f"{age}s"
            else:
                age_str = f"{age // 60}m"

            # Status con colore
            if activity['is_active']:
                status = colorize("ACTIVE", Colors.BRIGHT_GREEN)
            else:
                status = colorize("STALE ", Colors.BRIGHT_YELLOW)

            # Padding
            worker_pad = 12 - len(worker)
            age_pad = 5 - len(age_str)
            action_pad = 40 - len(action)

            line = f"║  {worker}{' ' * worker_pad} {status} ({age_str}{' ' * age_pad}) {action}{' ' * action_pad}   ║"
            lines.append(line)

    return '\n'.join(lines)


def render_footer() -> str:
    """Renderizza il footer della dashboard."""
    lines = []
    lines.append("║                                                                                      ║")
    lines.append("╚══════════════════════════════════════════════════════════════════════════════════════╝")
    return '\n'.join(lines)


def render_dashboard(tasks: List[Dict]) -> str:
    """
    Renderizza la dashboard completa.

    Args:
        tasks: Lista di tutti i task

    Returns:
        Stringa con dashboard ASCII completa
    """
    sections = [
        render_header(),
        render_workers(tasks),
        render_stats(tasks),
        render_heartbeat(),
        render_activity(tasks),
        render_footer()
    ]

    return '\n'.join(sections)


# ========== OUTPUT JSON ==========

def render_json(tasks: List[Dict]) -> str:
    """
    Renderizza output in formato JSON.

    Args:
        tasks: Lista di tutti i task

    Returns:
        Stringa JSON
    """
    workers_status = []
    for worker in WORKERS:
        status_info = get_worker_status(worker['name'], tasks)
        workers_status.append({
            'name': worker['name'],
            'emoji': worker['emoji'],
            'type': worker['type'],
            'status': status_info['status'],
            'current_task': status_info['current_task'],
            'task_count': status_info['task_count']
        })

    stats = get_task_queue_stats(tasks)
    activities = get_recent_activity(tasks, limit=10)

    # Formatta activities per JSON
    activities_formatted = []
    for activity in activities:
        activities_formatted.append({
            'timestamp': datetime.fromtimestamp(activity['timestamp']).isoformat(),
            'agent': activity['agent'],
            'action': activity['action'],
            'task_id': activity['task_id']
        })

    data = {
        'timestamp': datetime.now().isoformat(),
        'workers': workers_status,
        'queue_stats': stats,
        'recent_activity': activities_formatted
    }

    return json.dumps(data, indent=2)
