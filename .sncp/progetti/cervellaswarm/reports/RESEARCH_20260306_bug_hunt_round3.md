# Bug Hunt Round 3 - Analisi Proattiva CervellaSwarm

**Data**: 2026-03-06
**Status**: COMPLETA
**Fonti consultate**: 13 hook files, settings.json, 3 log files, docs ufficiali Claude Code

---

## FINDING CRITICI (da affrontare prima)

### BUG-1: Weekly Retro BROKEN da 4 settimane (Alta priorita)

**Sintomo**: Il cron `weekly_retro.py` fallisce ogni lunedi dalle 8:00 dal 2 Febbraio 2026.
**Causa root**: `scripts/common/db.py` riga 75 usa la sintassi `X | None` (union type) introdotta in Python 3.10+. Il cron gira con Python 3.9 di sistema (`/Library/Developer/CommandLineTools/...`).
**Impatto**: 5 retro consecutive perse (2026-02-02, 02-09, 02-16, 02-23, 03-02). Nessuna retro automatica da 1+ mese.
**Fix**: Sostituire `sqlite3.Connection | None` con `Optional[sqlite3.Connection]` in `db.py` riga 75, oppure cambiare lo shebang del cron per usare il Python dell'utente (>= 3.10).
**File**: `/Users/rafapra/Developer/CervellaSwarm/scripts/common/db.py:75`
**Log**: `/Users/rafapra/Developer/CervellaSwarm/data/logs/weekly_retro_cron.log`

---

### BUG-2: hook_debug.log cresciuto a 1.8MB (Media priorita)

**Sintomo**: Il file `hook_debug.log` e cresciuto a 1.8MB e non e leggibile direttamente.
**Causa root**: Il log raccoglie ogni PostToolUse/Task in forma di JSON completo (incluso il testo completo delle risposte degli agenti). Nessuna rotation configurata per questo file.
**Impatto**: Log inutilizzabile per debug (troppo grande). Occupa spazio disco inutile.
**Soluzione suggerita**: Aggiungere log rotation (es. max 500KB, 3 backup) oppure loggare solo metadata (timestamp, event_name, agent_type, durationMs) invece del JSON raw completo.
**File**: `/Users/rafapra/Developer/CervellaSwarm/data/logs/hook_debug.log`

---

### BUG-3: post_commit_engineer.py puo impiegare fino a 60s bloccando il commit (Media priorita)

**Sintomo**: L'hook PostToolUse su Bash lancia `analyze_codebase.py` con timeout 60s (interno: 55s). Questo hook e SINCRONO (non ha `async: true` nel settings.json).
**Impatto**: Ogni `git commit` puo bloccarsi per quasi un minuto in attesa dell'analisi codebase.
**Confronto**: Gli hook SessionEnd computazionalmente pesanti (session_end_flush, sncp_verify_sync, file_limits_guard, session_end_sync_agents) sono tutti `async: true`. Il post_commit_engineer no.
**Fix**: Aggiungere `"async": true` all'hook post_commit_engineer nel settings.json, oppure ridurre il timeout interno a 10s.
**File**: `/Users/rafapra/.claude/settings.json` riga 190, `/Users/rafapra/.claude/hooks/post_commit_engineer.py`

---

## OPPORTUNITA DI MIGLIORAMENTO

### OPP-1: Path-Specific Rules - Feature non sfruttata (Impatto Alto, Effort Quick)

**Cosa e**: Claude Code 2.0.64 ha introdotto `.claude/rules/` con path matching automatico. File `.md` con frontmatter `paths: glob-pattern` vengono caricati SOLO quando Claude lavora su file corrispondenti.

**Come potremmo usarlo**:
- `~/.claude/rules/lingua-universale.md` con `paths: packages/lingua-universale/**` - regole LU (sintassi, semantica, test patterns) caricate solo quando si lavora su LU
- `~/.claude/rules/playground.md` con `paths: playground/**` - regole per il playground (come creare step tour, esempi interattivi)
- `~/.claude/rules/agents.md` con `paths: ~/.claude/agents/**` - regole per modificare agenti (frontmatter obbligatori, DNA)

**Beneficio**: Meno token di contesto sprecati, regole piu rilevanti per task.
**Formato**:
```markdown
---
paths: packages/lingua-universale/**
---
# Regole LU
- Test sempre in packages/lingua-universale/tests/
- Ogni nuovo type ha test coverage 100%
...
```
**Dove creare**: `~/.claude/rules/` (globale) o `/Users/rafapra/Developer/CervellaSwarm/.claude/rules/` (progetto)

---

### OPP-2: Hook InstructionsLoaded - Non configurato (Impatto Medio, Effort Quick)

**Cosa e**: Nuovo hook Claude Code che si attiva ogni volta che un CLAUDE.md o un file `.claude/rules/*.md` viene caricato nel contesto. Riceve `file_path`, `memory_type`, `load_reason`.

**Come potremmo usarlo**:
- Audit: loggare quale CLAUDE.md viene caricato e quando (visibilita su cosa l'agente sa)
- Notifica: se viene caricato un file di regole inatteso, notifica

**Beneficio**: Migliore osservabilita del contesto caricato dagli agenti.

---

### OPP-3: Hook UserPromptSubmit - Non configurato (Impatto Medio, Effort Quick)

**Cosa e**: Hook che si attiva quando Rafa sottomette un prompt, PRIMA che Claude lo elabori. Puo modificare il prompt o aggiungere contesto.

**Come potremmo usarlo**:
- Auto-rilevamento trigger (es. se il prompt contiene "D5" o "D6", iniettare automaticamente la subroadmap di Fase D)
- Preflight check: se il prompt sembra una richiesta di deploy, ricordare CHECKLIST_DEPLOY
- Smart context: aggiungere data corrente al contesto automaticamente (evita risposte con date sbagliate)

**Beneficio**: Meno lavoro manuale per Rafa, piu contesto automatico.

---

### OPP-4: Hook PostToolUseFailure - Non configurato (Impatto Medio, Effort Quick)

**Cosa e**: Hook che si attiva quando un tool call fallisce. Non presente nel settings.json attuale.

**Come potremmo usarlo**:
- Loggare fallimenti tool per analisi retrospettiva (quali tool falliscono piu spesso?)
- Notifica macOS se un Bash critico fallisce (es. git push, test runner)

---

### OPP-5: SubagentStop Hook - Logging mancante per CervellaSwarm (Impatto Basso, Effort Quick)

**Osservazione**: Il log `subagent_stop_debug.log` contiene dati di ContabilitaAntigravity (data 2026-03-02) ma non sembra tracciare gli agenti CervellaSwarm recenti (S430-S431). Non c'e un hook SubagentStop configurato nel settings.json.

**Come potremmo usarlo**:
- Tracciare `totalDurationMs` e `totalTokens` per ogni agente (capire quali agenti sono lenti o costosi)
- Loggare `agent_type` + `last_assistant_message` summary per audit qualita

---

### OPP-6: PROJECT_MAPPING inconsistente tra hooks (Impatto Basso, Effort Quick)

**Osservazione**: I nuovi progetti (CervellaBrasil, Chavefy, CervellaCostruzione) sono mappati in alcuni hook ma non in altri:

| Hook | Supporta nuovi progetti |
|------|------------------------|
| `subagent_context_inject.py` | SI (tutti e 6 i progetti) |
| `file_limits_guard.py` | SI (tutti e 6 i progetti) |
| `sncp_pre_session_hook.py` | NO (solo miracollo, cervellaswarm, contabilita) |
| `sncp_verify_sync_hook.py` | NO (solo miracollo, cervellaswarm, contabilita) |
| `session_end_flush.py` | NO (solo miracollo, cervellaswarm, contabilita) |
| `daily_memory_loader.py` | NO (solo miracollo, cervellaswarm, contabilita) |

**Impatto**: Quando si lavora su CervellaBrasil/Chavefy/CervellaCostruzione, i hook di sessione non funzionano correttamente (no daily log, no memory flush, no pre-session check, no verify-sync).

---

### OPP-7: Hook SessionStart - 5 script sequenziali (Impatto Basso, Effort Medio)

**Osservazione**: Al SessionStart "startup" vengono eseguiti 5 script in sequenza:
1. `osascript` - notifica
2. `load_context.py` (timeout 5s)
3. `sncp_pre_session_hook.py` (timeout 30s) - lancia `pre-session-check.sh`
4. `daily_memory_loader.py` (timeout 10s) - lancia `load-daily-memory.sh`
5. `health_check.py` (timeout 10s)

Nessuno ha `async: true`, quindi il SessionStart attende fino a 55s prima che l'utente possa interagire.

**Fix suggerito**: Gli script che non bloccano (health_check, daily_memory_loader) possono diventare async. Il pre_session_hook deve restare sincrono solo se mostra warning critici.

---

### OPP-8: update_prompt_ripresa - PROBLEMA SILENZIOSO (Impatto Alto)

**Osservazione critica**: L'hook `update_prompt_ripresa.py` aggiunge una sezione "AUTO-CHECKPOINT" al PROMPT_RIPRESA a ogni SessionEnd/PreCompact. Questo e il motivo per cui i PROMPT_RIPRESA raggiungono il limite di 150 righe velocemente.

Ogni checkpoint aggiunge ~15 righe. Con 5-6 sessioni al giorno, si supera il limite in pochi giorni.

**Il problema piu sottile**: Il hook usa un pattern "rimuovi vecchi checkpoint + aggiungi nuovo" ma non rimuove TUTTI i vecchi - rimuove solo dalla sezione AUTO-CHECKPOINT fino al primo `---`. Se ci sono piu sezioni AUTO-CHECKPOINT, solo quella piu vecchia viene rimossa correttamente.

**Fix suggerito**: Rimuovere TUTTE le sezioni AUTO-CHECKPOINT vecchie prima di aggiungerne una nuova. Oppure archiviare i checkpoint in un file separato invece di appenderli al PROMPT_RIPRESA.

---

## QUICK WINS NON IMPLEMENTATI

| # | Win | Effort | Impatto |
|---|-----|--------|---------|
| QW-1 | Fix weekly_retro Python 3.9 compatibility | 15 min | Alto (retro settimanali tornano a funzionare) |
| QW-2 | Aggiungere `async: true` a post_commit_engineer | 2 min | Medio (commit non bloccano piu) |
| QW-3 | Log rotation per hook_debug.log | 30 min | Basso (spazio disco + leggibilita) |
| QW-4 | Creare `.claude/rules/lingua-universale.md` | 20 min | Alto (contesto piu rilevante per LU) |
| QW-5 | Aggiornare PROJECT_MAPPING in 4 hook per nuovi progetti | 30 min | Medio (CervellaBrasil/Chavefy/CervellaCostruzione funzionano) |
| QW-6 | Fix update_prompt_ripresa multi-checkpoint removal | 20 min | Alto (PROMPT_RIPRESA cresce meno velocemente) |

---

## OSSERVAZIONI POSITIVE (non cambiare)

- La famiglia di hook e ben progettata: fail-graceful ovunque, mai bloccante
- `bash_validator.py` e solido: BLOCK/ASK/ALLOW con safe targets lista
- `subagent_context_inject.py` e elegante: inietta contesto minimo (<600 chars) in modo lightweight
- `file_limits_guard.py` copre tutti i progetti e segnala a 90% (early warning)
- `session_end_save.py` + rotation a 50 snapshot: ben fatto
- Il pattern di logging separato (session-log.txt vs snapshots/) e pulito

---

## RACCOMANDAZIONE

Priorita suggerita per S431:

1. **PRIMA** - BUG-1 (weekly retro broken): fix in 15 min, 5 settimane di retro mancanti
2. **SECONDA** - BUG-3 (post_commit async): 2 righe di config, impatto immediato sull'esperienza
3. **TERZA** - OPP-6 (PROJECT_MAPPING inconsistente): completare il supporto ai nuovi progetti
4. **QUARTA** - OPP-1 (path-specific rules): creare regole LU per D5/D6
5. **QUINTA** - OPP-8 (update_prompt_ripresa fix): prevenire PROMPT_RIPRESA overflow

BUG-2 (log rotation) e le opportunita di nuovi hook possono attendere sessioni future.

---

*Cervella Researcher - Bug Hunt Round 3 - 2026-03-06*
*COSTITUZIONE-APPLIED: SI | Principio: "Ricerca PRIMA di implementare"*
