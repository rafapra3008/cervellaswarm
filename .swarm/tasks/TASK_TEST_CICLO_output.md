# Report: task_manager.py

**Analizzato da:** cervella-backend
**Data:** 2026-01-03

## Funzioni Trovate

- **validate_task_id(task_id)**: Valida task_id per sicurezza, previene path traversal
- **ensure_tasks_dir()**: Crea directory .swarm/tasks/ se non esiste
- **create_task(task_id, agent, description, risk_level)**: Crea nuovo task con template
- **list_tasks()**: Lista tutti i task con status, ACK e agent assegnato
- **mark_ready(task_id)**: Segna task pronto per lavorazione (.ready)
- **mark_working(task_id)**: Segna task in lavorazione (.working)
- **mark_done(task_id)**: Segna task completato (.done)
- **ack_received(task_id)**: Conferma ricezione task da worker
- **ack_understood(task_id)**: Conferma comprensione task da worker
- **get_task_status(task_id)**: Ritorna stato (done/working/ready/created)
- **get_ack_status(task_id)**: Ritorna stringa ACK "R/U/D" con checkmark
- **cleanup_task(task_id)**: Rimuove tutti i marker files

## Note

- Versione: 1.1.0 (2026-01-03)
- Usa file marker per sincronizzazione tra finestre (.ready, .working, .done)
- Include validazione sicurezza contro path traversal
- CLI completa con comandi: list, create, ready, working, done, status, cleanup
