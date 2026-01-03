# TASK: Creare task_manager.py per gestione task

## METADATA
- ID: TASK_001
- Assegnato a: cervella-backend
- Livello rischio: 1 (BASSO - nuovo file, nessun rischio)
- Timeout: 15 minuti
- Creato: 2026-01-03 14:15

## PERCHE
Abbiamo bisogno di uno script Python per gestire i task del sistema Multi-Finestra.
Lo script bash funziona per monitoring, ma Python ci da piu flessibilita.

## CRITERI DI SUCCESSO
- [ ] File scripts/swarm/task_manager.py creato
- [ ] Funzione create_task(task_id, agent, description) implementata
- [ ] Funzione list_tasks() implementata
- [ ] Funzione mark_ready(task_id) implementata
- [ ] Funzione mark_done(task_id) implementata
- [ ] Test manuale passato

## FILE DA MODIFICARE
- scripts/swarm/task_manager.py (CREARE)

## CHI VERIFICHERA
cervella-tester (Livello 1 - verifica funzionalita)

## DETTAGLI

Creare `scripts/swarm/task_manager.py` con:

```python
#!/usr/bin/env python3
"""
Task Manager per CervellaSwarm Multi-Finestra
"""

SWARM_DIR = ".swarm"
TASKS_DIR = f"{SWARM_DIR}/tasks"

def create_task(task_id: str, agent: str, description: str, risk_level: int = 1) -> str:
    """Crea un nuovo task con il template"""
    pass

def list_tasks() -> list:
    """Lista tutti i task con il loro stato"""
    pass

def mark_ready(task_id: str) -> bool:
    """Segna un task come ready"""
    pass

def mark_working(task_id: str) -> bool:
    """Segna un task come working"""
    pass

def mark_done(task_id: str) -> bool:
    """Segna un task come done"""
    pass

def get_task_status(task_id: str) -> str:
    """Ritorna lo stato di un task"""
    pass

if __name__ == "__main__":
    # CLI interface
    import sys
    if len(sys.argv) < 2:
        print("Usage: task_manager.py [list|create|ready|done] ...")
    # etc.
```

Usa Path per i percorsi. Mantieni il codice semplice e pulito.
