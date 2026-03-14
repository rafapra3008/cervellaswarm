# ANALISI SNCP - Stato di Salute e Raccomandazioni

> **Autore:** Cervella Ingegnera
> **Data:** 14 Marzo 2026
> **Scope:** Intero sistema SNCP + Hook + Script + overlap con auto-memory Claude Code
> **Health Score:** 6.5/10

---

## Executive Summary

SNCP (Sistema Nervoso Cervella Persistente) e un sistema maturo, costruito in 459 sessioni, che ha servito bene il progetto durante la crescita. Tuttavia, l'evoluzione organica ha lasciato stratificazioni significative: 5 "versioni" dichiarate (SNCP 2.0, 3.0, 4.0, 5.0, e ora il README dice "v5.0" ma descrive "v4.0"), limiti incoerenti tra documenti, directory fantasma, script obsoleti, e un overlap crescente con il sistema auto-memory nativo di Claude Code.

Il cuore funziona: PROMPT_RIPRESA, NORD.md, hook, subagent injection. Ma il contorno e cresciuto senza potatura.

---

## 1. INVENTARIO ATTUALE

### 1.1 File e Dimensioni

| Componente | File | Dimensione | Note |
|-----------|------|-----------|------|
| `.sncp/` totale | 1,492 | 19 MB | |
| `.sncp/archivio/` | 294+ | 4.0 MB | Accumulo storico |
| `.sncp/progetti/` | 907 | 13 MB | Cuore del sistema |
| `.sncp/reports/` | ~100+ | 448 KB | Daily reports + archivio |
| `.sncp/roadmaps/` | 37 | 400 KB | Molte completate |
| `.sncp/handoff/` | 157 (132 archivio) | 700 KB | Solo 25 attivi |
| Hook Python | 16 attivi + 9 archiviati | ~70 KB | In `~/.claude/hooks/` |
| Script SNCP bash | 20 | ~100 KB | In `scripts/sncp/` |
| Auto-memory Claude Code | 20 file | ~30 KB | In `~/.claude-insiders/.../memory/` |

### 1.2 PROMPT_RIPRESA - Stato Dimensioni

| File | Righe | Limite CLAUDE.md | Limite README | Limite MASTER | Limite Hook |
|------|-------|-----------------|---------------|---------------|-------------|
| cervellaswarm | 139 | 250 | 150 | 150 | 250 |
| miracollo | 145 | 250 | 150 | 150 | 250 |
| contabilita | 92 | 250 | 150 | 150 | 250 |
| MASTER | 54 | 250 | 50 | 50 | 250 |
| NORD.md | 281 | n/a | n/a | n/a | n/a |

---

## 2. PROBLEMI TROVATI

### P1 - CRITICO (richiede azione immediata)

#### P1-1: Incoerenza limiti PROMPT_RIPRESA tra documenti

**4 fonti diverse dichiarano 3 limiti diversi:**

| Fonte | Limite dichiarato |
|-------|------------------|
| `~/.claude/CLAUDE.md` (CLAUDE.md globale) | MAX 250 RIGHE |
| `file_limits_guard.py` (hook che ENFORZA) | 250 |
| `.sncp/README.md` (documentazione SNCP) | 150 |
| `PROMPT_RIPRESA_MASTER.md` (dentro il file) | 150 |
| `pre-session-check.sh` (script bash) | 150 |
| `health-check.sh` (script bash) | 150 |
| `consolidate-ripresa.sh` (script bash) | 150 |

**Impatto:** Lo script `pre-session-check.sh` (chiamato dal hook `sncp_pre_session_hook.py`) SEGNA come errore i file sopra 150 righe, mentre il sistema reale (`file_limits_guard.py`) accetta fino a 250. Miracollo con 145 righe sarebbe segnalato come "quasi al limite" dall'hook, ma il guard lo considererebbe OK. Confusione garantita.

**Root cause:** Il limite e stato aggiornato a 250 nella S452 (1M context era) nel hook e in CLAUDE.md, ma NON negli script bash e nella documentazione SNCP.

#### P1-2: `.sncp/README.md` gravemente obsoleto

Il README dice:
- "Versione SNCP: 5.0" ma descrive "STRUTTURA REALE (v4.0)"
- Riferisce directory che NON ESISTONO: `stato/`, `memoria/`, `idee/`, `validazioni/`, `sessioni_parallele/`
- Riferisce "SNCP 2.0" nel changelog ma il sistema e alla 4.0/5.0
- Lista automazioni con hook name sbagliato (`session_start_swarm.py` non esiste)
- Dice "PROMPT_RIPRESA max 150 righe" (sbagliato, e 250)
- Non menziona auto-memory di Claude Code

#### P1-3: `PROMPT_RIPRESA_MASTER.md` stale

- Ultimo aggiornamento: "Sessione 451" (S459 e la corrente)
- CervellaSwarm TL;DR: "S451: Checkpoint+handoff, 3684 test, v0.3.3, next=T3.5 VS Code" -- il VS Code e DONE da S453, siamo a 2/5 showcase LIVE
- Dice "max 150 righe" per PROMPT_RIPRESA (dovrebbe dire 250)
- Non menziona miracollo S30-S31 (14 Marzo, stessa data di oggi)

### P2 - ALTO (da risolvere presto)

#### P2-1: `health-check.sh` cerca `stato.md` (eliminato in SNCP 4.0)

Lo script `health-check.sh` fa:
- `get_line_count "$project_dir/stato.md"` -- stato.md non esiste piu per i progetti principali
- Controlla "stato.md size" e deduce score basandosi su un file inesistente
- Dice "SNCP 2.0" nel footer e nel score ("SCORE SNCP 2.0")

Esistono ancora 3 `stato.md` residui in sotto-bracci miracollo (miracollook, pms-core, room-hardware) -- reliquie non pulite.

#### P2-2: Script bash SNCP in gran parte inutilizzati o ridondanti

| Script | Stato | Motivo |
|--------|-------|--------|
| `compact-state.sh.DISABLED` | Disabilitato | Gia disabilitato esplicitamente |
| `post-session-update.sh.DISABLED` | Disabilitato | Sostituito da hook Python |
| `consolidate-ripresa.sh` | Ridondante | Logica di archiviazione fatta manualmente, limite sbagliato (150) |
| `health-check.sh` | Rotto | Cerca stato.md, score basato su SNCP 2.0 |
| `auto-summary.sh` | Non chiaro | Non referenziato da nessun hook |
| `compliance-check.sh` | Non chiaro | Non referenziato da nessun hook |
| `expand-daily.sh` | Non chiaro | Non referenziato da nessun hook |
| `load-daily-memory.sh` | Usato | Chiamato da `daily_memory_loader.py` |
| `memory-persist.sh` | Non chiaro | Non referenziato da nessun hook |
| `sncp-init.sh` | Usato raramente | Wizard nuovo progetto (raro) |
| `sync-agents.sh` | Usato | Chiamato da `session_end_sync_agents.py` |
| `verify-sync.sh` | Usato | Chiamato da `sncp_verify_sync_hook.py` |
| `pre-session-check.sh` | Usato | Chiamato da `sncp_pre_session_hook.py`, ma limite sbagliato |
| `quality-check.py` | Non chiaro | Non referenziato da nessun hook |
| `verify-hooks.py/.sh` | Non chiaro | Hook verification standalone |
| `audit-secrets.sh` | Usato manualmente | Security scan, utile |
| `daily-log.sh` | Usato | Chiamato da `daily_memory_loader.py` e `session_end_flush.py` |
| `rotate-reports.sh` | Usato | Rotazione periodica |

Almeno 6-7 script sono zombie: mai chiamati, con logica obsoleta.

#### P2-3: NORD.md a 281 righe -- nessun limite definito ma molto lungo

NORD.md contiene informazioni storiche accumulate (tutte le fasi W1-W6, Open Source F0-F4, Fase A-E dettagliata). Gran parte e storia completata. Solo la sezione SHOWCASE (righe 166-170) e i PUNTATORI sono realmente utili per la sessione corrente.

#### P2-4: 11 directory vuote in SNCP

Directory create dalla struttura template ma mai usate:
- `contabilita/roadmaps/`, `contabilita/decisioni/`, `contabilita/memoria/archivio/`
- `cervellacostruzione/decisioni/`
- `cervellaswarm/memoria/archivio/`
- `miracollo/memoria/archivio/`, `miracollo/rateboard/decisioni/`, `miracollo/archivio/2026-01-pre188/`
- `archivio/legacy_sncp3/idee/scartate/`, `archivio/2026-01/perne/attive/`, `archivio/2026-01/perne/archivio/`

### P3 - MEDIO (da considerare)

#### P3-1: Overlap significativo SNCP <-> Claude Code auto-memory

**Il sistema ha DUE memorie persistenti per la stessa informazione:**

| Tipo informazione | Dove in SNCP | Dove in auto-memory |
|------------------|-------------|-------------------|
| Decisioni tecniche | PROMPT_RIPRESA, reports/ | MEMORY.md (packages, bug-patterns, etc.) |
| Lezioni apprese | PROMPT_RIPRESA "Lezioni Apprese" | MEMORY.md (30+ entries inline) |
| Bug patterns | reports/ | `memory/bug-patterns.md`, `memory/bug-hunt-cli-mcp.md` |
| Configurazione packages | reports/ | `memory/packages.md` |
| CI/CD patterns | reports/ | `memory/ci_patterns_s443.md` |
| Feedback utente | Non catturato | `memory/feedback_*.md` (proattiva, no anxiety) |
| Visione progetto | NORD.md | `memory/vision_lu_for_ai.md` |
| Hook comuni | reports/ | `memory/hooks_common_module.md` |

L'auto-memory MEMORY.md ha 200+ righe di contenuto inline (non solo indice). E di fatto una copia parallela di informazioni gia in SNCP.

#### P3-2: Naming inconsistente directory

- `cervellaswarm/ricerche/` vs `cervellaswarm/research/` vs `cervellaswarm/studi/` vs `cervellaswarm/studio/` -- 4 directory con scopo simile
- `miracollo/ricerca/` vs `miracollo/ricerche/` -- duplicato
- `cervellaswarm/valutazioni/` vs `cervellaswarm/analisi/` -- overlap concettuale

#### P3-3: 89 daily reports accumulati

I daily reports in `.sncp/reports/daily/` accumulano. `rotate-reports.sh` esiste ma il threshold/la politica non sono chiari.

#### P3-4: Handoff system non piu usato

157 file handoff (132 in archivio, 25 "attivi"), ma il sistema handoff e stato effettivamente sostituito da PROMPT_RIPRESA + subagent_context_inject. Nessun handoff creato da sessioni recenti (S438+). Sistema morto.

#### P3-5: 37 roadmap accumulate

Molte subroadmap sono per fasi COMPLETATE (W2.5, W3, W4, W5, W6, SNCP 4.0, SNCP 5.0, Casa Pulita, ecc.). Non pulite o archiviate.

#### P3-6: `context-monitor.py` triggera `memory-flush.sh` a soglie alte

Il context-monitor triggera `memory-flush.sh` al 85% di context. Con 1M, il 85% = 850K token. Ragionevole, ma il flush stesso scrive su disco e chiama daily-log -- e un side effect implicito dalla statusline.

---

## 3. HOOK ANALYSIS

### 3.1 Mappa completa hook attivi

| Evento | Hook | Funzione | Necessario? |
|--------|------|----------|-------------|
| **SessionStart (startup)** | osascript notification | Notifica "Cervella pronta" | Utile |
| | load_context.py | Carica context iniziale | Da verificare |
| | sncp_pre_session_hook.py | Check SNCP health | Utile MA script bash sottostante ha limiti sbagliati |
| | daily_memory_loader.py | Daily logs | Marginale con 1M + auto-memory |
| | mcp/health_check.py | Health check MCP | Utile |
| **SessionStart (resume)** | osascript notification | Notifica ripresa | Utile |
| | load_context.py | Context reload | Da verificare |
| | daily_memory_loader.py | Daily logs | Marginale |
| **PreCompact (manual+auto)** | pre_compact_save.py | Snapshot JSON | Utile come backup |
| | update_prompt_ripresa.py | Auto-checkpoint | Utile |
| **SessionEnd** | session_end_save.py | Snapshot JSON | Utile come backup |
| | update_prompt_ripresa.py | Auto-checkpoint | Utile |
| | session_end_flush.py (async) | Memory flush | Ridondante con auto-memory |
| | sncp_verify_sync_hook.py (async) | Verify sync | Utile MA script bash problematico |
| | file_limits_guard.py (async) | Check limiti | Utile, limiti corretti |
| | session_end_sync_agents.py (async) | Sync agenti | Utile |
| | observability_hook.py (async) | Token tracking | Utile |
| **PreToolUse (Bash)** | bash_validator.py | Valida comandi bash | Utile |
| **PostToolUse (Task)** | debug_hook.py | Debug | Marginale |
| | log_event.py | Log eventi | Marginale |
| **PostToolUse (Bash)** | post_commit_engineer.py (async) | Post-commit check | Utile |
| **SubagentStart** | subagent_context_inject.py | Inietta PROMPT_RIPRESA | Utile, ben fatto |
| **Stop** | git_reminder.py | Ricorda commit | Utile |
| **StatusLine** | context-monitor.py | Mostra CTX% | Utile |

### 3.2 Valutazione Hook

**Ben fatto:**
- `cervella_hooks_common.py` -- singola fonte di verita per progetti, DRY, v1.2.0
- `subagent_context_inject.py` -- inject pulito, v2.0.0, fail-graceful
- `file_limits_guard.py` -- semplice, corretto, limiti aggiornati a 250
- `observability_hook.py` -- tracking token non invasivo, security-conscious
- `bash_validator.py` -- protezione comandi pericolosi

**Problematici:**
- `sncp_pre_session_hook.py` -- wrapper Python per script bash con limiti sbagliati
- `daily_memory_loader.py` -- overlap con auto-memory
- `session_end_flush.py` -- chiama `memory-flush.sh`, overlap con auto-memory

**Ridondanti:**
- `update_prompt_ripresa.py` appende auto-checkpoint, ma con 1M context la compaction e rara. Genera rumore nel file.

---

## 4. OVERLAP SNCP vs AUTO-MEMORY

### 4.1 Cosa fa Claude Code auto-memory

- `MEMORY.md` -- indice a 200 righe (max) caricato automaticamente nel context
- File `.md` individuali con frontmatter (type: user/feedback/project/reference)
- Caricato SEMPRE, senza hook, senza script
- Persistente tra conversazioni
- Puo essere aggiornato dall'AI stessa

### 4.2 Cosa fa SNCP

- `PROMPT_RIPRESA` -- stato sessione, iniettato via hook in subagent
- `NORD.md` -- visione strategica
- `reports/` -- output analisi dettagliate
- Daily logs -- cronologia giornaliera
- Handoff -- passaggio tra sessioni (non piu usato)
- Roadmap -- piani (molte completate)

### 4.3 Verdetto overlap

| Funzione | SNCP | Auto-memory | Chi vince |
|----------|------|-------------|-----------|
| Ripresa sessione per agenti | PROMPT_RIPRESA + hook | Non iniettato in subagent | **SNCP** |
| Lezioni apprese generali | PROMPT_RIPRESA | MEMORY.md | **Auto-memory** (piu persistente) |
| Bug patterns specifici | reports/ | memory/bug-patterns.md | **Duplicato** -- semplificare |
| Package versions | reports/ | memory/packages.md | **Duplicato** -- derivabile da codice |
| Feedback utente | Non catturato | memory/feedback_*.md | **Auto-memory** |
| Visione progetto | NORD.md | memory/vision_lu_for_ai.md | **Duplicato** -- NORD basta |
| Daily logs | .sncp/reports/daily/ | Non presente | **SNCP** -- ma valore marginale |
| Report analisi | .sncp/reports/ | Non presente | **SNCP** -- valore alto |
| Direzione strategica | NORD.md | Non presente | **SNCP** |

---

## 5. RACCOMANDAZIONI

### KEEP (funziona bene, non toccare)

1. **PROMPT_RIPRESA pattern** -- cuore del sistema, ben scritto, disciplinato
2. **cervella_hooks_common.py** -- DRY, singola fonte di verita, ben fatto
3. **subagent_context_inject.py** -- essenziale per swarm, ben fatto
4. **file_limits_guard.py** -- semplice e corretto
5. **observability_hook.py** -- tracking utile
6. **bash_validator.py** -- protezione importante
7. **reports/** -- output persistente di valore
8. **NORD.md** -- bussola strategica (ma serve potatura)

### FIX (azione richiesta)

1. **P1-1: Allineare limiti a 250 ovunque**
   - `pre-session-check.sh`: riga 102, cambiare `150` -> `250`
   - `health-check.sh`: righe 215, 265, cambiare `150` -> `250` e rimuovere riferimenti a stato.md
   - `consolidate-ripresa.sh`: riga 27, cambiare `LIMIT=150` -> `LIMIT=250`
   - `PROMPT_RIPRESA_MASTER.md`: riga 39, cambiare `150` -> `250`
   - `.sncp/README.md`: riga 70, cambiare `150` -> `250`

2. **P1-2: Riscrivere `.sncp/README.md`**
   - Rimuovere directory inesistenti dalla struttura
   - Allineare versione (e SNCP 4.0 di fatto)
   - Aggiornare lista automazioni con nomi hook corretti
   - Menzionare auto-memory come sistema complementare

3. **P1-3: Aggiornare PROMPT_RIPRESA_MASTER.md**
   - TL;DR CervellaSwarm: "S459: 2/5 showcase LIVE, VS Code v0.2.0, PyPI v0.3.3"
   - Limite: "max 250 righe"

### REMOVE (da eliminare)

1. **Script zombie** -- non referenziati da nessun hook:
   - `compact-state.sh.DISABLED` -- gia disabilitato, eliminare
   - `post-session-update.sh.DISABLED` -- gia disabilitato, eliminare
   - `auto-summary.sh` -- non usato
   - `expand-daily.sh` -- non usato
   - `memory-persist.sh` -- non usato
   - `compliance-check.sh` -- non usato (se non c'e un cron che lo chiama)

2. **Directory vuote** -- 11 directory vuote, eliminare

3. **stato.md residui** -- 3 file in sotto-bracci miracollo, archiviare o eliminare

4. **Handoff system** -- 25 file "attivi" non piu usati. Archiviare tutto.

5. **Roadmap completate** -- 20+ subroadmap di fasi completate, archiviare in `.sncp/archivio/`

### SIMPLIFY (con 1M + auto-memory)

1. **Daily logs (`.sncp/reports/daily/`)** -- 89 file. Con auto-memory il valore e marginale. Considerare:
   - Ridurre frequenza (settimanale vs giornaliero)
   - O eliminare: le informazioni importanti sono gia in PROMPT_RIPRESA e auto-memory

2. **daily_memory_loader.py** -- candidato a eliminazione. Auto-memory carica il contesto automaticamente.

3. **session_end_flush.py** -- candidato a eliminazione. Memory flush e un concetto pre-auto-memory.

4. **NORD.md** -- potare le sezioni completate (W1-W6, F0-F4 Open Source, Fasi A-D). Tenere solo: Visione, Stato corrente, Puntatori, Obiettivo finale. Target: 150 righe (da 281).

5. **Auto-memory MEMORY.md** -- eliminare entries duplicate con SNCP:
   - `memory/vision_lu_for_ai.md` -- gia in NORD.md
   - `memory/packages.md` -- derivabile da `pyproject.toml`
   - `memory/hooks_common_module.md` -- derivabile dal codice

### ADD (cosa manca)

1. **Checklist "audit SNCP" periodica** -- un comando o script che verifica:
   - Coerenza limiti tra tutti i documenti
   - Directory vuote
   - File stale (>60 giorni senza modifica in `progetti/`)
   - Roadmap completate non archiviate

2. **Singola fonte di verita per limiti** -- una variabile in `cervella_hooks_common.py` (tipo `PROMPT_RIPRESA_LIMIT = 250`) usata da TUTTI i consumer (script bash inclusi).

---

## 6. PROPOSTA DI SEMPLIFICAZIONE

### Stato attuale (complessita alta)

```
PROMPT_RIPRESA (3 file attivi) -- OK
NORD.md (1 file, 281 righe) -- troppo lungo
MASTER (1 file) -- stale
README (1 file) -- obsoleto
Daily logs (89 file) -- marginale
Handoff (157 file) -- morto
Roadmaps (37 file) -- 20+ completate
Reports (120+ file) -- OK, valore alto
Hook Python (16 attivi) -- 3-4 ridondanti
Script bash (20) -- 6-7 zombie
Auto-memory (20 file) -- overlap con SNCP
```

### Stato proposto (complessita dimezzata)

```
PROMPT_RIPRESA (3 file attivi) -- KEEP, fonte primaria per subagent
NORD.md (1 file, ~150 righe) -- TRIM, solo visione + stato + puntatori
MASTER (1 file) -- FIX, aggiornare
README -- REWRITE, 100 righe massimo
Daily logs -- ELIMINATE o ridurre a settimanale
Handoff -- ARCHIVE tutto
Roadmaps completate -- ARCHIVE (20+ file in archivio)
Reports -- KEEP, rotazione automatica OK
Hook Python -- REMOVE 3 (daily_loader, session_end_flush, PostToolUse/Task hooks)
Script bash -- REMOVE 6 zombie, FIX 3 limiti
Auto-memory -- PRUNE 3 duplicate, lasciare il resto come complemento
```

### Principio guida

> **SNCP = stato sessione per subagent + report persistenti + roadmap attive**
> **Auto-memory = lezioni apprese + feedback utente + pattern cross-session**
> **Non duplicare. Non accumulare. Non complicare.**

---

## 7. SCORE FINALE

| Area | Score | Note |
|------|-------|------|
| PROMPT_RIPRESA (cuore) | 9/10 | Ben scritti, entro limiti, aggiornati |
| Hook Python | 7/10 | Buona architettura, qualche ridondante |
| cervella_hooks_common.py | 9/10 | DRY, singola fonte, pulito |
| Script bash | 4/10 | Limiti sbagliati, molti zombie |
| Documentazione SNCP | 3/10 | README obsoleto, limiti incoerenti |
| Pulizia/igiene | 5/10 | Dir vuote, handoff morto, roadmap accumulate |
| Coerenza con auto-memory | 5/10 | Overlap non gestito |
| Subagent injection | 9/10 | Perfetto |
| Valore complessivo | 8/10 | Il sistema FUNZIONA, ma ha debito di manutenzione |

**Health complessivo: 6.5/10**

Il motore funziona bene (PROMPT_RIPRESA, hook, subagent inject = 9/10).
La carrozzeria ha bisogno di lavoro (docs, script, pulizia = 4/10).

---

## 8. PRIORITA DI AZIONE

| # | Azione | Effort | Impatto |
|---|--------|--------|---------|
| 1 | Fix limiti 150->250 in 5 file | 10 min | P1 - elimina confusione |
| 2 | Aggiorna PROMPT_RIPRESA_MASTER.md | 5 min | P1 - dati corretti |
| 3 | Riscrivi .sncp/README.md | 20 min | P1 - documentazione corretta |
| 4 | Fix health-check.sh (rimuovi stato.md) | 15 min | P2 - script funzionante |
| 5 | Elimina 6 script zombie | 5 min | P2 - meno rumore |
| 6 | Archivia handoff + roadmap completate | 15 min | P3 - pulizia |
| 7 | Elimina directory vuote | 2 min | P3 - pulizia |
| 8 | Trim NORD.md a ~150 righe | 20 min | P2 - meno bloat |
| 9 | Prune auto-memory duplicati | 10 min | P3 - meno overlap |
| 10 | Rimuovi hook ridondanti | 10 min | P3 - meno overhead |

**Effort totale stimato: ~2 ore per tutti e 10 i punti.**

---

*"Analizza prima, proponi poi."*
*"Il debito tecnico si paga con interessi."*

COSTITUZIONE-APPLIED: SI | Principio: "Fatto BENE > Fatto VELOCE"
