#!/usr/bin/env python3
"""CLI entry point for Task Manager.

Extracted from task_manager.py (S342) to keep library under 500 lines.
"""

import sys
from pathlib import Path

# Aggiungi root al path per import
_root = Path(__file__).parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from scripts.swarm.task_manager import (
    __version__,
    create_task, list_tasks, mark_ready, mark_working,
    mark_done, ack_received, ack_understood,
    get_task_status, get_ack_status, cleanup_task
)


def print_usage():
    """Stampa l'help del task manager."""
    print("Task Manager - CervellaSwarm Multi-Finestra")
    print(f"Versione: {__version__}")
    print()
    print("Usage:")
    print("  task_manager.py list                           - Lista tutti i task")
    print("  task_manager.py create TASK_ID AGENT DESC      - Crea nuovo task")
    print("  task_manager.py ready TASK_ID                  - Segna task come ready")
    print("  task_manager.py working TASK_ID                - Segna task come working")
    print("  task_manager.py ack-received TASK_ID           - Segna ACK_RECEIVED")
    print("  task_manager.py ack-understood TASK_ID         - Segna ACK_UNDERSTOOD")
    print("  task_manager.py done TASK_ID                   - Segna task come done")
    print("  task_manager.py status TASK_ID                 - Mostra stato task")
    print("  task_manager.py cleanup TASK_ID                - Rimuove marker files")
    print("  task_manager.py --help                         - Mostra questo help")
    print("  task_manager.py --version                      - Mostra versione")
    print()


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["--help", "-h", "help"]:
        print_usage()
        sys.exit(0 if len(sys.argv) > 1 else 1)

    if sys.argv[1] in ["--version", "-v"]:
        print(f"task_manager.py v{__version__}")
        sys.exit(0)

    command = sys.argv[1]

    if command == "list":
        tasks = list_tasks()
        if not tasks:
            print("Nessun task trovato.")
        else:
            print(f"{'TASK_ID':<12} {'STATUS':<10} {'ACK':<7} {'AGENT':<25} {'FILE'}")
            print("-" * 90)
            for task in tasks:
                print(f"{task['task_id']:<12} {task['status']:<10} {task['ack']:<7} {task['agent']:<25} {task['file']}")

    elif command == "create":
        if len(sys.argv) < 5:
            print("Uso: task_manager.py create TASK_ID AGENT DESCRIPTION [RISK_LEVEL]")
            sys.exit(1)

        task_id = sys.argv[2]
        agent = sys.argv[3]
        description = sys.argv[4]
        risk_level = int(sys.argv[5]) if len(sys.argv) > 5 else 1

        try:
            file_path = create_task(task_id, agent, description, risk_level)
            print(f"Task creato: {file_path}")
        except FileExistsError as e:
            print(f"Errore: {e}")
            sys.exit(1)

    elif command in ["ready", "working", "done", "ack-received", "ack-understood", "status", "cleanup"]:
        if len(sys.argv) < 3:
            print(f"Uso: task_manager.py {command} TASK_ID")
            sys.exit(1)

        task_id = sys.argv[2]

        if command == "ready":
            if mark_ready(task_id):
                print(f"Task {task_id} segnato come READY")
        elif command == "working":
            if mark_working(task_id):
                print(f"Task {task_id} segnato come WORKING")
        elif command == "ack-received":
            if ack_received(task_id):
                print(f"Task {task_id} - ACK_RECEIVED confermato")
        elif command == "ack-understood":
            if ack_understood(task_id):
                print(f"Task {task_id} - ACK_UNDERSTOOD confermato")
        elif command == "done":
            if mark_done(task_id):
                print(f"Task {task_id} segnato come DONE")
        elif command == "status":
            status = get_task_status(task_id)
            ack = get_ack_status(task_id)
            print(f"Task {task_id}:")
            print(f"  Status: {status.upper()}")
            print(f"  ACK: {ack} (R=Received, U=Understood, D=Done)")
        elif command == "cleanup":
            if cleanup_task(task_id):
                print(f"Marker files di {task_id} rimossi")

    else:
        print(f"Comando sconosciuto: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
