#!/usr/bin/env python3
"""
Task Manager per CervellaSwarm Multi-Finestra

Gestisce la creazione, monitoraggio e stato dei task per il sistema Multi-Finestra.
Usa file marker (.ready, .working, .done) per sincronizzazione tra agenti.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-03"

from pathlib import Path
from typing import Optional
from datetime import datetime

SWARM_DIR = ".swarm"
TASKS_DIR = f"{SWARM_DIR}/tasks"


def ensure_tasks_dir() -> Path:
    """Assicura che la directory tasks esista."""
    tasks_path = Path(TASKS_DIR)
    tasks_path.mkdir(parents=True, exist_ok=True)
    return tasks_path


def create_task(task_id: str, agent: str, description: str, risk_level: int = 1) -> str:
    """
    Crea un nuovo task con il template.

    Args:
        task_id: ID univoco del task (es. TASK_001)
        agent: Nome dell'agente assegnato (es. cervella-backend)
        risk_level: Livello di rischio 1-3 (1=basso, 2=medio, 3=alto)
        description: Descrizione del task

    Returns:
        Path del file task creato
    """
    ensure_tasks_dir()

    task_file = Path(TASKS_DIR) / f"{task_id}.md"

    if task_file.exists():
        raise FileExistsError(f"Task {task_id} già esiste!")

    # Mappa livello rischio a descrizione
    risk_map = {
        1: "BASSO - nuovo file, nessun rischio",
        2: "MEDIO - modifica file esistente",
        3: "ALTO - sistema critico o deploy"
    }

    template = f"""# TASK: {description}

## METADATA
- ID: {task_id}
- Assegnato a: {agent}
- Livello rischio: {risk_level} ({risk_map.get(risk_level, "NON DEFINITO")})
- Timeout: 15 minuti
- Creato: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## PERCHE
[Spiegazione del perché serve questo task]

## CRITERI DI SUCCESSO
- [ ] Criterio 1
- [ ] Criterio 2
- [ ] Test passato

## FILE DA MODIFICARE
- [file da creare/modificare]

## CHI VERIFICHERA
cervella-tester (Livello {risk_level} - {'verifica funzionalità' if risk_level == 1 else 'test completi' if risk_level == 2 else 'audit completo'})

## DETTAGLI

[Descrizione dettagliata del task]
"""

    task_file.write_text(template)
    return str(task_file)


def list_tasks() -> list:
    """
    Lista tutti i task con il loro stato.

    Returns:
        Lista di dict con: task_id, status, agent, file
    """
    ensure_tasks_dir()

    tasks_path = Path(TASKS_DIR)
    tasks = []

    for task_file in sorted(tasks_path.glob("TASK_*.md")):
        task_id = task_file.stem
        status = get_task_status(task_id)

        # Leggi metadata dal file (agent)
        agent = "unknown"
        try:
            content = task_file.read_text()
            for line in content.split('\n'):
                if line.startswith('- Assegnato a:'):
                    agent = line.split(':', 1)[1].strip()
                    break
        except Exception:
            pass

        tasks.append({
            'task_id': task_id,
            'status': status,
            'agent': agent,
            'file': str(task_file)
        })

    return tasks


def mark_ready(task_id: str) -> bool:
    """
    Segna un task come ready (pronto per essere lavorato).

    Args:
        task_id: ID del task

    Returns:
        True se successo, False altrimenti
    """
    ensure_tasks_dir()

    task_file = Path(TASKS_DIR) / f"{task_id}.md"
    if not task_file.exists():
        print(f"Errore: Task {task_id} non esiste!")
        return False

    ready_file = Path(TASKS_DIR) / f"{task_id}.ready"
    ready_file.touch()
    return True


def mark_working(task_id: str) -> bool:
    """
    Segna un task come working (in lavorazione).

    Args:
        task_id: ID del task

    Returns:
        True se successo, False altrimenti
    """
    ensure_tasks_dir()

    task_file = Path(TASKS_DIR) / f"{task_id}.md"
    if not task_file.exists():
        print(f"Errore: Task {task_id} non esiste!")
        return False

    working_file = Path(TASKS_DIR) / f"{task_id}.working"
    working_file.touch()
    return True


def mark_done(task_id: str) -> bool:
    """
    Segna un task come done (completato).

    Args:
        task_id: ID del task

    Returns:
        True se successo, False altrimenti
    """
    ensure_tasks_dir()

    task_file = Path(TASKS_DIR) / f"{task_id}.md"
    if not task_file.exists():
        print(f"Errore: Task {task_id} non esiste!")
        return False

    done_file = Path(TASKS_DIR) / f"{task_id}.done"
    done_file.touch()
    return True


def get_task_status(task_id: str) -> str:
    """
    Ritorna lo stato di un task.

    Args:
        task_id: ID del task

    Returns:
        Stato: 'done', 'working', 'ready', 'created', 'not_found'
    """
    tasks_path = Path(TASKS_DIR)

    task_file = tasks_path / f"{task_id}.md"
    if not task_file.exists():
        return "not_found"

    # Controlla marker files in ordine di priorità
    if (tasks_path / f"{task_id}.done").exists():
        return "done"
    if (tasks_path / f"{task_id}.working").exists():
        return "working"
    if (tasks_path / f"{task_id}.ready").exists():
        return "ready"

    return "created"


def cleanup_task(task_id: str, remove_markers: bool = True) -> bool:
    """
    Rimuove i marker files di un task.

    Args:
        task_id: ID del task
        remove_markers: Se True, rimuove .ready, .working, .done

    Returns:
        True se successo, False altrimenti
    """
    tasks_path = Path(TASKS_DIR)

    if remove_markers:
        markers = ['.ready', '.working', '.done']
        for marker in markers:
            marker_file = tasks_path / f"{task_id}{marker}"
            if marker_file.exists():
                marker_file.unlink()

    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Task Manager - CervellaSwarm Multi-Finestra")
        print()
        print("Usage:")
        print("  task_manager.py list                           - Lista tutti i task")
        print("  task_manager.py create TASK_ID AGENT DESC      - Crea nuovo task")
        print("  task_manager.py ready TASK_ID                  - Segna task come ready")
        print("  task_manager.py working TASK_ID                - Segna task come working")
        print("  task_manager.py done TASK_ID                   - Segna task come done")
        print("  task_manager.py status TASK_ID                 - Mostra stato task")
        print("  task_manager.py cleanup TASK_ID                - Rimuove marker files")
        print()
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        tasks = list_tasks()
        if not tasks:
            print("Nessun task trovato.")
        else:
            print(f"{'TASK_ID':<12} {'STATUS':<10} {'AGENT':<25} {'FILE'}")
            print("-" * 80)
            for task in tasks:
                print(f"{task['task_id']:<12} {task['status']:<10} {task['agent']:<25} {task['file']}")

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

    elif command in ["ready", "working", "done", "status", "cleanup"]:
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
        elif command == "done":
            if mark_done(task_id):
                print(f"Task {task_id} segnato come DONE")
        elif command == "status":
            status = get_task_status(task_id)
            print(f"Task {task_id}: {status.upper()}")
        elif command == "cleanup":
            if cleanup_task(task_id):
                print(f"Marker files di {task_id} rimossi")

    else:
        print(f"Comando sconosciuto: {command}")
        sys.exit(1)
