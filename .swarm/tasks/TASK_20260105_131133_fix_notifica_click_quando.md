# Task: FIX NOTIFICA CLICK: Quando clicchi sulla notifica, deve aprire il file _output.md del task invece del .log. PROBLEMA: Ora apre .log con Console.app (sbagliato!). SOLUZIONE: 1) Nel runner script, passare TASK_NAME come variabile. 2) Nel trap EXIT, costruire path: ${SWARM_DIR}/tasks/${TASK_NAME}_output.md. 3) Usare quello per terminal-notifier -open. 4) Fallback a .txt se output non esiste. File da modificare: scripts/swarm/spawn-workers.sh (righe 467-520 circa). Versione: 2.4.0 -> 2.5.0

**Assegnato a:** cervella-backend
**Stato:** ready
**Priorita:** MEDIA
**Data:** 05 January 2026
**Generato da:** quick-task v1.0.0

---

## Obiettivo

FIX NOTIFICA CLICK: Quando clicchi sulla notifica, deve aprire il file _output.md del task invece del .log. PROBLEMA: Ora apre .log con Console.app (sbagliato!). SOLUZIONE: 1) Nel runner script, passare TASK_NAME come variabile. 2) Nel trap EXIT, costruire path: ${SWARM_DIR}/tasks/${TASK_NAME}_output.md. 3) Usare quello per terminal-notifier -open. 4) Fallback a .txt se output non esiste. File da modificare: scripts/swarm/spawn-workers.sh (righe 467-520 circa). Versione: 2.4.0 -> 2.5.0

---

## Note

Task creato automaticamente dalla Regina via quick-task.
Completare e scrivere output in TASK_20260105_131133_fix_notifica_click_quando_output.md.

---

## Checklist Verifica

- [ ] Obiettivo raggiunto
- [ ] Output scritto in _output.md
- [ ] File .done creato

---

*Quick-task v1.0.0*
