# Output: TASK_SWARM_COMMON

**Completato da:** cervella-backend
**Data:** 2026-01-05 03:20

## Cosa e' stato fatto

### 1. Creato ~/.local/lib/swarm-common.sh (v1.0.0)

Libreria condivisa con funzioni comuni:

**Funzioni Output:**
- `print_success()` - Output verde [OK]
- `print_error()` - Output rosso [ERROR]
- `print_warning()` - Output giallo [WARN]
- `print_info()` - Output blu [i]

**Funzioni Utility:**
- `find_project_root()` - Trova root progetto cercando .swarm/
- `time_ago()` - Converte timestamp in "Xm fa", "Xh fa"
- `time_ago_short()` - Versione breve (solo numero + unita)
- `get_assigned_to()` - Estrae "Assegnato a:" da task file
- `get_guardian_for_agent()` - Mappa agente -> guardiana appropriata

**Funzioni Configurazione:**
- `load_config()` - Carica ~/.swarm/config con defaults
- `get_claude_bin()` - Trova Claude CLI con fallback chain

**Funzioni Notifiche:**
- `notify()` - Invia notifica macOS

### 2. Creato swarm-health (v1.0.0)

Nuovo comando per verificare salute del sistema:

```bash
swarm-health              # Check completo (6 verifiche)
swarm-health --quick      # Solo check essenziali (3 verifiche)
```

**Check effettuati:**
1. Claude CLI - Verifica presenza e versione
2. Configurazione - Verifica ~/.swarm/config
3. Progetti - Verifica esistenza progetti configurati
4. Task Stale - Cerca task .working vecchi
5. Spazio Disco - Verifica spazio disponibile
6. Script Swarm - Verifica spawn-workers, swarm-status, swarm-review

**Riepilogo finale:**
- Task in coda
- Task in lavorazione
- Task completati

## Verifica

- [x] `swarm-health` funziona e mostra stato completo
- [x] `swarm-health --quick` funziona (check essenziali)
- [x] `swarm-status` funziona ancora
- [x] `swarm-review` funziona ancora
- [x] `spawn-workers --list` funziona ancora

## File Creati/Modificati

| File | Versione | Tipo |
|------|----------|------|
| ~/.local/lib/swarm-common.sh | 1.0.0 | NUOVO |
| ~/.local/bin/swarm-health | 1.0.0 | NUOVO |

## Note

La libreria `swarm-common.sh` e' pronta per essere usata dagli altri script.
Per ora gli script esistenti (swarm-status, swarm-review, spawn-workers) non sono stati modificati per usarla, per evitare di introdurre breaking changes.

In futuro si potrebbe fare un refactoring per rimuovere le funzioni duplicate e usare swarm-common.sh in tutti gli script.
