# Output: TASK_FIX_CONFIG

**Completato da:** cervella-backend
**Data:** 2026-01-05 03:15

## Cosa e' stato fatto

### 1. Creato ~/.swarm/config
File di configurazione centralizzata con:
- `SWARM_PROJECTS` - Lista progetti da monitorare
- `CLAUDE_BIN` - Path Claude CLI (auto-detect se vuoto)
- `STALE_THRESHOLD` - Timeout task stale (1800s default)
- `NOTIFICATIONS_ENABLED` - Notifiche macOS
- `NOTIFICATION_SOUND` - Suono notifiche

### 2. Modificato swarm-status (v1.1.0)
- Aggiunto source di ~/.swarm/config
- Rimosso array PROJECTS hardcodato
- Usa SWARM_PROJECTS da config con fallback a defaults

### 3. Modificato swarm-review (v1.1.0)
- Aggiunto source di ~/.swarm/config
- Rimosso array PROJECTS hardcodato
- Usa SWARM_PROJECTS da config con fallback a defaults

### 4. Modificato spawn-workers (v2.0.0)
- Aggiunto source di ~/.swarm/config
- Aggiunta funzione get_claude_bin() per auto-detect
- Rimosso path NVM hardcodato (/Users/rafapra/.nvm/...)
- Usa CLAUDE_BIN da config con fallback chain:
  1. CLAUDE_BIN dalla config
  2. `which claude` nel PATH
  3. Path NVM noto come ultimo fallback

## Verifica

- [x] `swarm-status` funziona
- [x] `swarm-status --all` funziona
- [x] `spawn-workers --list` funziona
- [x] Config file creato in ~/.swarm/
- [x] Path hardcodati rimossi

## File Modificati

| File | Versione | Modifiche |
|------|----------|-----------|
| ~/.swarm/config | 1.0.0 | NUOVO |
| ~/.local/bin/swarm-status | 1.1.0 | Config centralizzata |
| ~/.local/bin/swarm-review | 1.1.0 | Config centralizzata |
| ~/.local/bin/spawn-workers | 2.0.0 | Config + get_claude_bin |
