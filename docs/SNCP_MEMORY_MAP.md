# SNCP Memory Implementation Map

> **Creato:** 30 Gennaio 2026 - Sessione 321
> **Scopo:** Mappa centrale di tutti gli script e workflow memoria

---

## TL;DR

```
+================================================================+
|   SNCP 3.0 = Security + Memory Management per CervellaSwarm    |
|                                                                |
|   Hook automatici: SessionStart, SessionEnd                    |
|   Script manuali: checkpoint, daily-log, audit-secrets         |
|   Limiti: PROMPT_RIPRESA 150, stato.md 500 righe               |
+================================================================+
```

---

## Script Memoria - Overview

| Script | Scopo | Quando | Auto/Manuale |
|--------|-------|--------|--------------|
| `checkpoint.sh` | Commit + push | Fine sessione | Manuale |
| `memory-flush.sh` | Save worker context | SessionEnd | AUTO (hook) |
| `daily-log.sh` | Timeline note | Durante lavoro | Manuale |
| `audit-secrets.sh` | Scan security | Pre-commit | Manuale |
| `check-ripresa-size.sh` | Monitor limiti | Pre-commit | Manuale |

---

## Dettaglio Script

### checkpoint.sh

```bash
# Path: scripts/swarm/checkpoint.sh
# Symlink: ~/.local/bin/checkpoint

# Usage
checkpoint 321 "Descrizione lavoro"

# Cosa fa:
# 1. Esegue check-ripresa-size.sh
# 2. Mostra git status
# 3. git add -A (esclude .env, credentials, secrets)
# 4. git commit -m "checkpoint(S321): Descrizione"
# 5. git push origin HEAD
```

### memory-flush.sh

```bash
# Path: scripts/swarm/memory-flush.sh
# Hook: SessionEnd (AUTOMATICO)

# Usage manuale
./scripts/swarm/memory-flush.sh miracollo backend

# Cosa fa:
# 1. Check PROMPT_RIPRESA size
# 2. Warning se > 120 righe
# 3. Log evento in .swarm/logs/memory_flush.log
# 4. Reminder per Worker
```

### daily-log.sh

```bash
# Path: scripts/sncp/daily-log.sh

# Inizializza log oggi
./scripts/sncp/daily-log.sh cervellaswarm --init

# Aggiungi nota
./scripts/sncp/daily-log.sh cervellaswarm "Completato test MCP"

# Visualizza
./scripts/sncp/daily-log.sh cervellaswarm --view
```

### audit-secrets.sh

```bash
# Path: scripts/sncp/audit-secrets.sh

# Scan .sncp/progetti/
./scripts/sncp/audit-secrets.sh

# Scan path specifico
./scripts/sncp/audit-secrets.sh /path/to/check

# Pattern cercati:
# - API keys (sk-, xoxb-, ghp_, etc)
# - Passwords in plaintext
# - Tokens e credentials
```

### check-ripresa-size.sh

```bash
# Path: scripts/sncp/check-ripresa-size.sh

# Tutti i progetti
./scripts/sncp/check-ripresa-size.sh

# Progetto specifico
./scripts/sncp/check-ripresa-size.sh miracollo

# Output:
# ✅ cervellaswarm: 105/150 (70%)
# ⚠️  miracallook: 146/150 (97%) WARNING
# ❌ room-hardware: 199/150 (132%) ERROR
```

---

## Struttura File Memoria

```
.sncp/progetti/{progetto}/
├── PROMPT_RIPRESA_{progetto}.md   # Context principale (150 righe MAX)
├── stato.md                        # Status progetto (500 righe MAX)
├── memoria/
│   ├── 2026-01-30.md              # Daily log oggi
│   └── archivio/                  # Log vecchi
├── bracci/                         # Solo Miracollo (3 bracci)
│   ├── pms-core/
│   ├── miracallook/
│   └── room-hardware/
└── archivio/                       # Sessioni vecchie archiviate
```

---

## Hook Automatici

### SessionStart

```python
# .claude/hooks/session_start_swarm.py
# Carica automaticamente:
# - COSTITUZIONE
# - NORD.md
# - PROMPT_RIPRESA del progetto
```

### SessionEnd

```python
# .claude/hooks/file_limits_guard.py
# Verifica limiti file (150/500 righe)

# .claude/hooks/memory_flush_auto.py
# Auto-save contesto worker (NEW S321)
```

---

## Workflow Completo Sessione

```
┌─────────────────────────────────────────────────────────────┐
│                    INIZIO SESSIONE                          │
├─────────────────────────────────────────────────────────────┤
│ 1. SessionStart hook carica:                                │
│    - COSTITUZIONE                                           │
│    - NORD.md                                                │
│    - PROMPT_RIPRESA_{progetto}.md                          │
│                                                             │
│ 2. Cervella verifica stato.md (se serve)                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   DURANTE SESSIONE                          │
├─────────────────────────────────────────────────────────────┤
│ 3. daily-log.sh per note importanti                        │
│                                                             │
│ 4. spawn-workers per delegare task                         │
│    - Worker ricevono DNA + COSTITUZIONE                     │
│                                                             │
│ 5. Aggiorna PROMPT_RIPRESA in tempo reale                  │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    FINE SESSIONE                            │
├─────────────────────────────────────────────────────────────┤
│ 6. SessionEnd hook:                                         │
│    - file_limits_guard.py verifica limiti                   │
│    - memory_flush_auto.py salva contesto                    │
│                                                             │
│ 7. checkpoint [N] "Descrizione"                            │
│    - audit-secrets.sh (implicito)                          │
│    - check-ripresa-size.sh                                  │
│    - git commit + push                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Limiti e Regole

### Limiti File (INVIOLABILI)

| File | Limite | Azione se Superato |
|------|--------|-------------------|
| PROMPT_RIPRESA | 150 righe | Archiviare in archivio/ |
| stato.md | 500 righe | Condensare o archiviare |

### Regola Security

```
MAI in PROMPT_RIPRESA o stato.md:
- API keys
- Passwords
- Tokens
- Credentials

INVECE usa:
[stored in .env as VARIABLE_NAME]
```

---

## Miglioramenti Futuri (da Ricerca S321)

| # | Miglioramento | Effort | Beneficio |
|---|---------------|--------|-----------|
| 1 | Observation Masking | 1 sett | -50% token usage |
| 2 | sqlite-vec semantic search | 1 mese | Ricerca semantica |
| 3 | Core Memory Regina | 3 sett | Working memory curated |
| 4 | MemGPT-like architecture | 3+ mesi | Full hierarchical memory |

**Report completo:** `docs/studio/RICERCA_MEMORIA_AI_AGENTS.md`

---

*Mappa creata: 30 Gennaio 2026 - Sessione 321*
*Cervella & Rafa*
