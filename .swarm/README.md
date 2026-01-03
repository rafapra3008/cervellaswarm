# .swarm/ - Sistema Multi-Finestra CervellaSwarm

Questa directory contiene il sistema di comunicazione tra finestre Claude Code.

## Struttura
- `tasks/` - Task queue con flag files
- `status/` - Stato delle finestre attive
- `locks/` - Lock per file critici
- `handoff/` - File per handoff su compact
- `logs/` - Log operazioni
- `archive/` - Task completati (archiviati)

## Flag Files
- `.ready` - Task pronto per essere preso
- `.working` - Task in lavorazione
- `.done` - Task completato
- `.error` - Task fallito

## Come Usare
1. Regina crea TASK_XXX.md
2. Regina fa `touch TASK_XXX.ready`
3. Worker vede .ready, legge task
4. Worker fa `touch TASK_XXX.working`
5. Worker completa, scrive output
6. Worker fa `touch TASK_XXX.done`
7. Regina legge output

## Script
- `scripts/swarm/monitor-status.sh` - Monitora stato tasks
