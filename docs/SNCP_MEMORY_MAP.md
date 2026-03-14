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
|   Limiti: PROMPT_RIPRESA 250 righe                             |
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
├── PROMPT_RIPRESA_{progetto}.md   # Context principale (250 righe MAX)
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
# Verifica limiti file (250/500 righe)

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
│ 2. Cervella verifica PROMPT_RIPRESA (se serve)             │
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
| PROMPT_RIPRESA | 250 righe | Archiviare in archivio/ |

### Regola Security

```
MAI in PROMPT_RIPRESA:
- API keys
- Passwords
- Tokens
- Credentials

INVECE usa:
[stored in .env as VARIABLE_NAME]
```

---

## Studio Memoria AI (Ricerca S321)

### Scoperta Chiave

```
+================================================================+
|   OBSERVATION MASKING > LLM SUMMARIZATION                      |
|                                                                |
|   - 52% MENO COSTOSO                                           |
|   - +2.6% PERFORMANCE                                          |
|   - Zero infrastruttura extra                                  |
+================================================================+
```

### Come Funzionano i Big Players

| Sistema | Approccio | Cosa Possiamo Imparare |
|---------|-----------|------------------------|
| **Clawdbot** | File MD + sqlite-vec | Semplice e potente! |
| **MemGPT** | OS-like memory tiers | Self-editing memory |
| **sqlite-vec** | Vector search in SQLite | Locale, veloce, portabile |
| **AutoGPT** | Episodic + Semantic memory | Knowledge graphs |
| **LangChain** | Buffer/Summary/Entity memory | Strategie multiple |

### Observation Masking - Come Funziona

```
Quando context > 50%:

PRIMA:
[Step 1] Read file auth.py (500 lines shown)
[Step 2] Grep for "password" (200 matches shown)
[Step 3] Read config.py (300 lines shown)
...tutto in memoria...

DOPO:
<masked: file_read auth.py>
<masked: grep_search password>
[Step 15] Found issue in auth.py:42 [FULL]
[Step 16] Current fix [FULL]

→ 50%+ less tokens, same accuracy!
```

---

## Roadmap Miglioramenti Memoria

### Quick Wins (1-2 settimane)

| # | Cosa | Beneficio | Effort | Come |
|---|------|-----------|--------|------|
| 1 | **Observation Masking** | -50% token usage | 1 sett | Modifica DNA Worker |
| 2 | **Pre-Task Memo** | Worker non perdono focus | 1 sett | File .swarm/outputs/ |
| 3 | **Daily Memory Flush** | PROMPT_RIPRESA fresh | 2 giorni | Cron job launchd |

### Medium Term (1-2 mesi)

| # | Cosa | Beneficio | Effort | Come |
|---|------|-----------|--------|------|
| 4 | **sqlite-vec** | Semantic search locale | 1 mese | .swarm/memory/*.sqlite |
| 5 | **Core Memory Regina** | Working memory curated | 3 sett | .swarm/regina/CORE_MEMORY.md |

### Long Term (3+ mesi)

| # | Cosa | Beneficio | Effort |
|---|------|-----------|--------|
| 6 | **MemGPT-like architecture** | Full hierarchical memory | 3+ mesi |
| 7 | **Cross-agent knowledge sharing** | Agenti imparano da altri | 4+ mesi |

---

## Riferimenti

| Documento | Contenuto |
|-----------|-----------|
| `docs/studio/RICERCA_MEMORIA_AI_AGENTS.md` | Studio completo 1039 righe |
| `reports/RICERCA_MEMORIA_PERSISTENTE_MOLTBOT.md` | Studio Moltbot S320 |
| `.swarm/plans/MAPPA_IMPLEMENTAZIONI_MEMORIA.md` | Piano implementazione |

---

*Mappa creata: 30 Gennaio 2026 - Sessione 321*
*Aggiornata: 30 Gennaio 2026 - Dettagli ricerca aggiunti*
*Cervella & Rafa*
