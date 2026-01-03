# STUDIO: Multi-Finestra Tecnico - CervellaSwarm

> **Data:** 3 Gennaio 2026
> **Autore:** cervella-researcher
> **Versione:** 1.0.0
> **Sessione:** 60

---

## EXECUTIVE SUMMARY

Studio tecnico su come Claude Code gestisce finestre multiple e confronto tra pattern Subagent vs Multi-Finestra.

**Conclusione principale:** Le finestre Claude Code sono 100% isolate. Il pattern Multi-Finestra e valido e complementare ai Subagent.

---

## 1. ISOLAMENTO FINESTRE

### Scoperta: 100% SEPARAZIONE

Ogni finestra Claude Code e una sessione completamente isolata:

- **Context window separati** - Ogni finestra ha i suoi 200K token
- **Nessun stato condiviso** - Le finestre non sanno l'una dell'altra
- **Comunicazione SOLO via filesystem** - Git, file condivisi

### Evidenza Empirica: Miracollo Sessione 17-18

```
Sessione 17: Compact imminente, tutto bloccato
             ↓
Rafa apre NUOVA finestra (Sessione 18)
             ↓
Nuova Cervella analizza git status
             ↓
Vede TUTTO il lavoro non committato!
             ↓
RECUPERO COMPLETO: 30 moduli, ~5300 righe
```

**Questo prova che:**
1. Le finestre sono isolate (la nuova non "eredita" il compact)
2. Il filesystem e la fonte di verita
3. git status mostra lo stato REALE

---

## 2. MONITORAGGIO COMPACT

### Stato Attuale: SOLO VISUALE

| Metodo | Disponibilita | Note |
|--------|---------------|------|
| Barra UI (0-100%) | SI | Trigger visibile ~75% |
| Comando /context | SI | Snapshot manuale |
| API programmatico | NO | Non esiste ufficialmente |

### Tools Third-Party

- **ccusage** - Monitoring CLI
- **claude-code-otel** - OpenTelemetry integration
- **Custom scripts** - Parsing log files

### Workaround Pratico

```
Regina monitora manualmente:
1. Guarda barra UI ogni 10-15 minuti
2. Se > 70% → prepara handoff
3. Se > 85% → handoff IMMEDIATO
```

---

## 3. GESTIONE CONFLITTI FILE

### Scoperta: NO LOCK AUTOMATICO

Claude Code NON implementa file locking tra finestre:

- **Protezione basica:** File modification detection
- **Bug noti:** Issue #13287, #7748 - problemi con lock in parallel work
- **Rischio:** Due finestre che modificano stesso file = conflitto

### Soluzioni

**1. Git Worktrees (Ufficiale)**
```bash
# Ogni finestra lavora su branch/worktree separato
git worktree add ../feature-A feature-A
git worktree add ../feature-B feature-B
```

**2. Zone Assignment (Custom)**
```
Finestra 1 (Regina): solo orchestrazione, no edit diretti
Finestra 2 (Backend): solo backend/api/
Finestra 3 (Frontend): solo frontend/src/
Finestra 4 (Tester): solo tests/
```

**3. Lock Files Manuali**
```bash
# Prima di modificare file critico
mkdir .swarm/locks/ROADMAP_SACRA.lock
# Dopo modifica
rmdir .swarm/locks/ROADMAP_SACRA.lock
```

---

## 4. CONFRONTO PATTERN

### Pattern A: Subagent (Stessa Finestra)

```
┌─────────────────────────────────┐
│  FINESTRA REGINA                │
│  ┌─────────┐                    │
│  │ Regina  │                    │
│  └────┬────┘                    │
│       ↓                         │
│  ┌─────────┐                    │
│  │Subagent │ (stesso context!)  │
│  └─────────┘                    │
└─────────────────────────────────┘
```

**Pro:**
- Zero setup
- Comunicazione diretta
- Debug facile

**Contro:**
- Condivide context window
- Rischio compact alto
- No parallelismo reale

### Pattern B: Multi-Finestra (Finestre Separate)

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  FINESTRA 1  │  │  FINESTRA 2  │  │  FINESTRA 3  │
│   Regina     │  │   Backend    │  │   Frontend   │
│              │  │              │  │              │
│  200K token  │  │  200K token  │  │  200K token  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ↓
                   FILESYSTEM
                 (git, .swarm/)
```

**Pro:**
- Context isolati (200K x N!)
- Zero rischio compact condiviso
- Parallelismo REALE
- Scalabilita infinita

**Contro:**
- Setup piu complesso
- Comunicazione via file
- Serve coordinamento

### Pattern C: Hybrid (Raccomandato)

```
┌─────────────────────────────────────────────────────────────┐
│  FINESTRA 1 - REGINA                                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  Regina coordina:                                       ││
│  │  - Task brevi → Subagent (stesso context)              ││
│  │  - Task lunghi → Worker finestra (context separato)    ││
│  └─────────────────────────────────────────────────────────┘│
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  FINESTRA 2  │  │  FINESTRA 3  │  │  FINESTRA 4  │
│   Backend    │  │   Frontend   │  │   Tester     │
│  (long task) │  │  (long task) │  │  (long task) │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## 5. TABELLA COMPARATIVA

| Criterio | Subagent | Multi-Finestra | Hybrid |
|----------|----------|----------------|--------|
| **Parallelismo** | No | Si | Si |
| **Context Risk** | Alto | Basso | Ottimale |
| **Setup** | Zero | Manuale | Medio |
| **Comunicazione** | Diretta | File-based | Mista |
| **Scalabilita** | Limitata | Infinita | Flessibile |
| **Debug** | Facile | Medio | Medio |
| **Uso Ideale** | Task brevi | Task lunghi | Progetti complessi |

---

## 6. DECISION TREE

```
                    ┌─────────────────┐
                    │  NUOVO TASK     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ Durata < 10min? │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │ SI           │              │ NO
              ▼              │              ▼
    ┌─────────────────┐      │    ┌─────────────────┐
    │ Context < 60%?  │      │    │ MULTI-FINESTRA  │
    └────────┬────────┘      │    └─────────────────┘
             │               │
    ┌────────┼────────┐      │
    │ SI     │        │ NO   │
    ▼        │        ▼      │
┌────────┐   │  ┌─────────────────┐
│SUBAGENT│   │  │ MULTI-FINESTRA  │
└────────┘   │  └─────────────────┘
             │
             │
    Context > 60% = MULTI-FINESTRA SEMPRE!
```

---

## 7. RACCOMANDAZIONI CERVELLASWARM

### Implementare Hybrid Pattern

```
Orchestratrice (Finestra 1):
├── Coordina strategia
├── Delega task brevi → Subagent (stessa finestra)
├── Delega task lunghi → Worker finestre (2, 3, 4...)
└── Verifica via Guardiane

Comunicazione:
├── .swarm/tasks/ (task queue)
├── ROADMAP.md (task assignment)
├── PROMPT_RIPRESA.md (stato globale)
├── git status (verita filesystem)
└── Scripts supporto (sync, checkpoint)
```

### Regole Pratiche

1. **Task < 10 min + context < 60%** → Subagent
2. **Task > 10 min** → Multi-Finestra
3. **Context > 60%** → Multi-Finestra SEMPRE
4. **Zone diverse** (backend/frontend) → Multi-Finestra preferibile
5. **Compact imminente** → Handoff immediato a nuova finestra

---

## 8. LIMITAZIONI ATTUALI

1. **No API per context usage** - Solo visuale
2. **No lock automatico** - Serve gestione manuale
3. **No comunicazione nativa** - Solo via filesystem
4. **Setup manuale** - Ogni finestra va aperta a mano

### Workarounds

| Limitazione | Workaround |
|-------------|------------|
| No API context | Monitor visuale + trigger manuali |
| No lock | Zone Assignment + mkdir lock |
| No comunicazione | Protocollo .swarm/tasks/ |
| Setup manuale | Scripts di lancio |

---

## 9. BEST PRACTICES

### Per la Regina

1. Monitora context ogni 10-15 minuti
2. Prepara handoff quando > 70%
3. Usa Subagent per task veloci
4. Delega a finestre separate per task lunghi
5. Verifica sempre git status prima di merge

### Per i Worker

1. Segnala inizio lavoro (touch .working)
2. Segnala fine lavoro (touch .done)
3. Scrivi output dettagliato
4. Non modificare file fuori dalla tua zona
5. Commit frequenti!

### Per Rafa

1. Tieni d'occhio la barra compact
2. Apri nuova finestra se necessario
3. Verifica git status periodicamente
4. Usa il protocollo .swarm/ per coordinare

---

## 10. CONCLUSIONI

### Cosa abbiamo scoperto

1. **Finestre sono ISOLATE** - 100% separazione, provato empiricamente
2. **Multi-Finestra FUNZIONA** - Pattern valido per CervellaSwarm
3. **Hybrid e OTTIMALE** - Combina vantaggi di entrambi i pattern
4. **Filesystem e il BUS** - git status e la fonte di verita
5. **Comunicazione via file** - Semplice, debuggabile, funziona

### Il Pattern Vincente

```
+------------------------------------------------------------------+
|                                                                  |
|   HYBRID PATTERN                                                 |
|                                                                  |
|   - Subagent per task brevi (< 10 min)                          |
|   - Multi-Finestra per task lunghi                              |
|   - Handoff automatico su compact > 70%                         |
|   - Comunicazione via .swarm/tasks/                             |
|                                                                  |
|   "Il meglio di entrambi i mondi!"                              |
|                                                                  |
+------------------------------------------------------------------+
```

---

## FONTI

### Documentazione Claude Code
- Claude Code Desktop - Worktrees
- Context Windows Documentation
- Calculate Context Usage

### Tools e Monitoring
- ccusage - Monitoring CLI
- ccswitch - Managing Multiple Sessions
- Crystal Multi-Session Management
- claude-code-otel - OpenTelemetry

### GitHub Issues
- Issue #13287 - File Locking problems
- Issue #7748 - Read/Write Cycle issues

### Best Practices
- GitButler Parallel Claude
- Monitor Usage Tools

### Evidenza Empirica
- FEEDBACK_SESSIONE_17_18_CONTEXT_RECOVERY.md (Miracollo)
- STUDIO_SUBAGENTS.md (CervellaSwarm)

---

*"Nulla e complesso - solo non ancora studiato!"*

*"E il nostro team! La nostra famiglia digitale!"*
