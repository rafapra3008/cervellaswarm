# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 5 Gennaio 2026 - Sessione 91 - STABILIZZAZIONE + STUDIO VISIBILITA'!

---

## CARA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame.                                 |
|   Hai 16 agenti pronti a lavorare per te.                       |
|                                                                  |
|   SESSIONE 91: STABILIZZAZIONE + STUDIO VISIBILITA'!            |
|   - Template prompt inizio sessione creato                       |
|   - Worker Health Tracking implementato                          |
|   - PROBLEMA CRITICO identificato: "Lavoriamo al buio!"         |
|   - 2 ricercatori spawnati per studiare visibilita'             |
|                                                                  |
|   "Lavorare al buio e' difficile!" - Rafa                       |
|                                                                  |
+------------------------------------------------------------------+
```

---

## SESSIONE 91: STABILIZZAZIONE + STUDIO VISIBILITA'!

### L'Obiettivo

1. Completare task in coda dalla sessione 90
2. Stabilizzare il sistema swarm (task appesi, worker morti)
3. Studiare problema visibilita' worker

### IL PROBLEMA CRITICO IDENTIFICATO

```
+------------------------------------------------------------------+
|                                                                  |
|   "LAVORIAMO AL BUIO!"                                          |
|                                                                  |
|   OGGI SAPPIAMO:                                                 |
|   - Quando worker INIZIA (spawn)                                 |
|   - Quando worker FINISCE (cleanup)                              |
|                                                                  |
|   NON SAPPIAMO:                                                  |
|   - Cosa fa MENTRE lavora                                        |
|   - Se e' bloccato o sta pensando                                |
|   - Quanto manca al completamento                                |
|   - Se ha problemi                                               |
|                                                                  |
|   Vediamo finestre con cursore che lampeggia...                  |
|   ...e non sappiamo NULLA!                                       |
|                                                                  |
|   QUESTO E' IL PROBLEMA DA RISOLVERE!                           |
|                                                                  |
+------------------------------------------------------------------+
```

### Cosa Abbiamo Fatto

1. **TEMPLATE PROMPT INIZIO SESSIONE**
   - File: `~/.claude/templates/PROMPT_INIZIO_SESSIONE.md`
   - Include: quick-task, whitelist, Regola 14
   - Versione pulita e aggiornata post-Sessione 90

2. **WORKER HEALTH TRACKING**
   - spawn-workers v2.1.0 con PID tracking
   - swarm-cleanup v1.0.0 per task orfani
   - Trap EXIT per cleanup automatico
   - Risolve: task .working appesi

3. **TASK STALE PULITI**
   - 2 task dalla sessione 90 marcati .stale
   - TASK_CODE_REVIEW_SWARM
   - TASK_REGOLA_VIA_GIUSTA

4. **STUDIO VISIBILITA' LANCIATO**
   - 2 ricercatori spawnati in parallelo:
     - cervella-researcher (studio tecnico)
     - cervella-guardiana-ricerca (comparativo)
   - Task in .swarm/tasks/ con prefisso TASK_20260105_051500_

### Worker IN ESECUZIONE (al momento del checkpoint)

```
DUE WORKER ATTIVI:
- cervella-researcher -> studio visibilita' tecnico
- cervella-guardiana-ricerca -> studio + comparativo

STATO:
- Processi attivi (CPU 1.2% ciascuno)
- Log vuoti (bufferizzati - PARTE DEL PROBLEMA!)
- Task ancora .ready (non hanno creato .working)

SE CONTINUANO A LAVORARE:
- Output in: .swarm/tasks/TASK_*_visibilita_*_output.md
- Controllare: ls .swarm/tasks/*visibilita*.done
```

### File Creati/Modificati (Sessione 91)

| File | Cosa |
|------|------|
| `~/.claude/templates/PROMPT_INIZIO_SESSIONE.md` | NUOVO! Template prompt |
| `~/.local/bin/spawn-workers` | v2.1.0 - PID tracking |
| `~/.local/bin/swarm-cleanup` | NUOVO! Cleanup task orfani |
| `NORD.md` | Aggiornato con sessione 91 |
| `ROADMAP_SACRA.md` | Aggiunto CHANGELOG sessione 91 |

### Prossimi Step

1. **Controllare output ricercatori** - quando finiscono
2. **Implementare soluzione visibilita'** - basata sugli studi
3. **Code Review settimanale** - oggi e' lunedi'
4. **MIRACOLLO!** - usare swarm in produzione

### Filo del Discorso

Rafa ha identificato un problema CRITICO: "Lavoriamo al buio!"

Abbiamo spawnato due worker e li abbiamo VISTI lavorare... ma non sapevamo cosa facevano! Solo "Worker avviato" e cursore che lampeggia. I processi erano attivi (CPU 1.2%) ma i log vuoti.

Questo e' ESATTAMENTE il problema che devono risolvere. L'ironia e' fortissima!

La soluzione verra' dagli studi dei due ricercatori - uno tecnico (researcher) e uno con comparativo (guardiana).

---

## SESSIONE 90: QUICK-TASK + FILOSOFIA DI VITA!

### L'Obiettivo

1. Capire PERCHE' la Regina viola le sue regole
2. Creare soluzione che RENDE FACILE fare la cosa giusta
3. Fix problemi sicurezza dalla review

### LA LEZIONE PIU' IMPORTANTE (Filosofia di Vita!)

```
+------------------------------------------------------------------+
|                                                                  |
|   "Invece di violare le regole e rimanere sbagliando...          |
|    creare la soluzione che CAMBIA LA VITA!"                      |
|                                                                  |
|   Questa non e' solo programmazione.                             |
|   E' FILOSOFIA DI VITA!                                          |
|                                                                  |
|   Non combattere la natura umana (via piu' facile).              |
|   PROGETTA intorno ad essa!                                      |
|                                                                  |
|   "Rendi facile fare la cosa giusta,                             |
|    e la cosa giusta verra' fatta."                               |
|                                                                  |
|   - Rafa & Cervella, 5 Gennaio 2026                              |
|                                                                  |
+------------------------------------------------------------------+
```

### Cosa Abbiamo Fatto

1. **STUDIO AUTONOMIA REGINA**
   - Root cause: frizione spawn-workers = 6:1 vs Edit diretto
   - La Regina sceglie path con meno frizione (naturale!)
   - Soluzione: ridurre frizione, non combattere natura

2. **QUICK-TASK COMMAND** (LA MAGIA!)
   ```bash
   # Invece di 6 passi manuali:
   quick-task "descrizione" --backend   # 1 comando!
   quick-task "descrizione" --frontend  # 1 comando!
   quick-task "descrizione" --docs      # 1 comando!
   ```
   - Crea task automaticamente
   - Spawna worker automaticamente
   - Frizione ridotta da 6:1 a 1:1!

3. **WHITELIST FILE REGINA**
   - Edit diretto OK: NORD.md, PROMPT_RIPRESA.md, .swarm/tasks/
   - Tutto il resto: quick-task o spawn-workers!

4. **FIX SICUREZZA ALTI (3 fix)**
   - Path NVM: glob invece di v24.11.0 hardcodato
   - Escape AppleScript: funzione completa
   - Command injection: heredoc invece di interpolazione

5. **REGOLE NEL DNA**
   - Regola 14: Via Giusta, Non Via Facile
   - Regola 15: Whitelist File + quick-task

### File Creati/Modificati (Sessione 90)

| File | Cosa |
|------|------|
| `~/.local/bin/quick-task` | NUOVO! Comando magico! |
| `~/.claude/CHECKLIST_AZIONE.md` | Whitelist + quick-task |
| `~/.claude/agents/cervella-orchestrator.md` | Regola 14 + 15 |
| `docs/studio/STUDIO_VIA_FACILE.md` | Studio pattern |
| `~/.swarm/config` | Fix path NVM |
| `~/.claude/hooks/context_check.py` | v4.3.1 - escape fix |

### Prossimi Step

1. **Usare quick-task SEMPRE** - Mai piu' Edit diretti su codice!
2. **MIRACOLLO!** - Testare lo swarm in produzione
3. **common.py** - DRY tra hooks (task pronto)

### TASK NON COMPLETATO (per prossima Cervella!)

Il task `TASK_20260105_042820_migliorare_testo_inizio_sessione` è in coda (.ready).
Worker docs si è bloccato/chiuso. La prossima Cervella deve:
```bash
spawn-workers --docs
```
Per completare il miglioramento del testo inizio sessione.

---

## SESSIONE 89: GLOBALIZZAZIONE MEMORIA + REVIEW HOOKS!

### L'Obiettivo

1. Fixare DNA Orchestrator (Regola 13 confusa)
2. Globalizzare sistema memoria (database + scripts)
3. Review completa hooks/scripts

### Cosa Abbiamo Fatto

1. **FIX DNA ORCHESTRATOR - Regola 13**
   - PRIMA: confusa su quando usare Task tool vs spawn-workers
   - DOPO: "SE MODIFICA FILE -> spawn-workers (finestra separata!)"
   - DOPO: "SE SOLO LEGGE -> Task tool (interno)"
   - Path aggiornati in 4 DNA guardiane

2. **SISTEMA MEMORIA GLOBALIZZATO**
   - Database: `~/.swarm/data/swarm_memory.db` (1.7MB)
   - Scripts: `~/.claude/scripts/memory/` (4 file Python)
   - `paths.py` v2.0.0 - usa path GLOBALI, non di progetto
   - `settings.json`: 5 path aggiornati per memoria

3. **REVIEW HOOKS/SCRIPTS - Rating 8.5/10**
   - cervella-reviewer ha analizzato tutto
   - Report in: `reports/review_hooks_scripts_20260105.md`

### Problemi Trovati dalla Review

**ALTI (sicurezza!):**
1. Path NVM hardcodato (v24.11.0) - usa glob!
2. Escape AppleScript incompleto - aggiungi \, ', newline
3. Command injection potenziale in osascript

**MEDI:**
4. Error handling silenzioso (except: pass)
5. Codice duplicato tra hooks -> creare common.py
6. Timeout mancanti subprocess
7. Error messages criptici
8. Race condition spawning

**PUNTI FORZA:**
- Architettura modulare
- Graceful degradation
- Apple integration elegante
- Anti-compact system sofisticato

### File Modificati (Sessione 89)

| File | Cosa |
|------|------|
| `~/.claude/agents/cervella-orchestrator.md` | Regola 13 riscritta |
| `~/.claude/agents/cervella-guardiana-*.md` | Path aggiornati (3 file) |
| `~/.claude/settings.json` | 5 path memoria aggiornati |
| `~/.claude/scripts/common/paths.py` | v2.0.0 - GLOBALE! |
| `~/.claude/scripts/memory/*.py` | NUOVI - 4 script |
| `~/.swarm/data/swarm_memory.db` | COPIATO da CervellaSwarm |
| `reports/review_hooks_scripts_20260105.md` | Report review |

### Prossimi Step

1. **Fix problemi ALTI** - Sicurezza prima!
2. **Creare ~/.claude/hooks/common.py** - DRY tra hooks
3. **MIRACOLLO!** - Usare Swarm in produzione

---

## SESSIONE 88: CODE REVIEW + FIX SWARM!

### L'Obiettivo

1. Organizzare la casa (archiviare task vecchi)
2. Code Review del sistema Swarm (oggi e' Lunedi!)
3. Fixare i problemi trovati dalla review

### Cosa Abbiamo Fatto

1. **ORGANIZZATO CASA**
   - 102 file archiviati in CervellaSwarm
   - 14 file archiviati in Miracollo
   - SPLIT_SETTINGS stale archiviato

2. **CODE REVIEW DAY**
   - cervella-reviewer ha analizzato spawn-workers, swarm-status, swarm-review
   - Rating iniziale: 8/10
   - Problemi ALTI: path hardcodati
   - Problemi MEDI: codice duplicato, escape incompleto
   - Problemi BASSI: template, logging

3. **FIX IMPLEMENTATI (API al lavoro!)**
   - cervella-backend: TASK_FIX_CONFIG (config centralizzata + fix path)
   - cervella-backend: TASK_SWARM_COMMON (swarm-common.sh + swarm-health)
   - cervella-docs: TASK_IMPROVE_TEMPLATES (template migliorati)

4. **NUOVI FILE CREATI**
   - `~/.swarm/config` - Configurazione centralizzata
   - `~/.local/lib/swarm-common.sh` - Funzioni comuni (DRY!)
   - `~/.local/bin/swarm-health` - Health check sistema
   - Template migliorati in .swarm/tasks/

5. **RATING FINALE: 9/10!**

### Comandi Globali Disponibili

```bash
swarm-status              # Stato progetto corrente
swarm-status --all        # Stato TUTTI i progetti
swarm-status --cleanup    # Pulisce task stale

swarm-review              # Mostra task da verificare
swarm-review --start      # Spawna Guardiane per review

swarm-health              # Health check sistema (6 controlli!)

spawn-workers --backend   # Spawna api backend
spawn-workers --frontend  # Spawna api frontend
spawn-workers --docs      # Spawna api docs
spawn-workers --reviewer  # Spawna reviewer
```

### FILE MODIFICATI/CREATI (Sessione 88)

| File | Cosa |
|------|------|
| `~/.swarm/config` | NUOVO - Configurazione centralizzata |
| `~/.local/lib/swarm-common.sh` | NUOVO - Funzioni comuni |
| `~/.local/bin/swarm-health` | NUOVO - Health check |
| `~/.local/bin/spawn-workers` | Modificato - usa config |
| `~/.local/bin/swarm-status` | Modificato - usa config |
| `~/.local/bin/swarm-review` | Modificato - usa config |
| `.swarm/tasks/TEMPLATE_*.md` | Migliorati |
| `reports/code_review_swarm_20260105.md` | Report code review |

### Decisione Cervella: Guardiane

Le Guardiane sono utili per task CRITICI (deploy, security, codice complesso).
Per task semplici (docs, config, template) basta verifica manuale.
Il sistema c'e', lo usiamo quando serve.

---

## SESSIONE 87: AUTO-HANDOFF v4.3.0 VS CODE NATIVO!

### L'Obiettivo

Fare funzionare l'AUTO-HANDOFF aprendo VS Code con Claude nel terminal integrato (non Terminal.app separato).

### Il Problema Iniziale

La sessione 86 aveva:
- `claude -p` che usciva dopo il prompt (risolto togliendo `-p`)
- VS Code si apriva ma il terminal integrato non rispondeva a osascript
- Rafa: "sarebbe meglio aprire su vscode"

### Cosa Abbiamo Fatto

1. **ANALISI APPROFONDITA** - 10 passi indietro, ricerca seria
   - Letto settings.json, capito come funzionano gli hooks
   - Analizzato spawn-workers.sh per pattern funzionanti
   - Test minimali uno alla volta

2. **SCOPERTA CHIAVE: Command Palette!**
   - `Ctrl+backtick` per aprire terminal NON funziona da osascript
   - `Cmd+Shift+P` + "Terminal: Create New Terminal" FUNZIONA!

3. **PATTERN TESTATO E FUNZIONANTE:**
   ```
   1. code --new-window /path     (apre VS Code)
   2. sleep 4                      (aspetta apertura)
   3. Cmd+Shift+P                  (Command Palette)
   4. "Terminal: Create New Terminal" + Enter
   5. sleep 2                      (aspetta terminal)
   6. keystroke "claude prompt" + Enter
   ```

4. **context_check.py v4.3.0**
   - Nuova funzione `open_vscode_with_claude()`
   - Fallback a Terminal.app se VS Code fallisce
   - TESTATO con Miracollo - FUNZIONA PERFETTAMENTE!

### Filo del Discorso

Rafa voleva VS Code nativo, non due finestre separate. Abbiamo fatto ricerca seria:
- Prima provato alla cieca (non funzionava)
- Rafa: "Facciamo 10 passi indietro"
- Test minimali: Calculator, Terminal, VS Code
- Scoperto che Command Palette e' la chiave
- Test completo con log e timing
- "HAHAHAHAHAH TU SEI LA NUMERO UNO!" - Rafa quando ha funzionato

### FILE MODIFICATI (Sessione 87)

| File | Cosa |
|------|------|
| `~/.claude/hooks/context_check.py` | v4.3.0 - VS CODE NATIVO! |

### COMANDI CHE FUNZIONANO (copia e usa!)

```bash
# Apre VS Code su progetto + terminal + comando (TESTATO!)
code --new-window ~/Developer/miracollogeminifocus
sleep 4
osascript << 'EOF'
tell application "Visual Studio Code" to activate
delay 1
tell application "System Events"
    tell process "Code"
        keystroke "p" using {command down, shift down}
        delay 0.8
        keystroke "Terminal: Create New Terminal"
        delay 0.5
        key code 36
    end tell
end tell
EOF
sleep 2
osascript << 'EOF'
tell application "System Events"
    tell process "Code"
        keystroke "echo CIAO"
        delay 0.3
        key code 36
    end tell
end tell
EOF
```

---

## SESSIONE 86: AUTO-HANDOFF v4.0.0!

### L'Obiettivo

Fare funzionare l'AUTO-HANDOFF che apre automaticamente una nuova finestra quando il contesto e' al 70%.

### Il Problema Iniziale

La sessione 85 aveva implementato AUTO-HANDOFF ma la finestra VS Code NON si apriva. La Cervella precedente aveva lasciato nel handoff:
- `subprocess.Popen` con "code --new-window" → NON funziona
- `open -na "Visual Studio Code"` → NON funziona
- `osascript` con Terminal → sembrava funzionare

### Cosa Abbiamo Scoperto

1. **Background processes NON hanno GUI access su macOS**
   - Gli hook Python girano come daemon
   - Non possono aprire finestre GUI direttamente
   - Questa e' una LIMITAZIONE di macOS, non un bug nostro

2. **VS Code "code --new-window" e' problematico**
   - Invece di aprire nuova finestra, CHIUDEVA quelle esistenti!
   - Comportamento inaspettato

3. **osascript + Terminal FUNZIONA!**
   - Il comando: `osascript -e 'tell application "Terminal" to do script "cd PATH && claude"'`
   - Apre Terminal, fa cd, lancia claude
   - Funziona da Claude!

4. **claude -p passa il prompt ma poi ESCE**
   - La nuova Cervella parte, risponde, e poi esce
   - Serve che resti aperta in modo interattivo

### Stato Attuale

- context_check.py v4.0.0 implementato
- Usa osascript + Terminal + claude -p
- DA PERFEZIONARE: claude deve restare aperto
- IDEA: Aprire su VS Code sarebbe meglio (da studiare)

### Filo del Discorso

Rafa voleva l'AUTO-HANDOFF che funzionasse in modo automatico, "nel 2026".

Abbiamo fatto tanta ricerca:
- Prima provato watcher con file flag
- Poi scoperto che osascript funziona direttamente da Claude
- Poi trovato Cmd+Shift+N per nuova finestra VS Code
- Ma il terminal integrato di VS Code non rispondeva ai comandi
- Alla fine: Terminal.app + claude -p e' la soluzione piu' affidabile

Il problema finale: claude -p esegue il prompt e poi esce, invece di restare aperto.

Rafa ha detto: "sarebbe meglio aprire su vscode" - questa e' la direzione per la prossima sessione.

### FILE MODIFICATI (Sessione 86)

| File | Cosa |
|------|------|
| `~/.claude/hooks/context_check.py` | v4.0.0 - AUTO-HANDOFF con osascript |
| `~/.claude/scripts/handoff-watcher.sh` | Creato ma NON serve (osascript funziona diretto!) |
| `~/.claude/scripts/handoff-vscode.scpt` | AppleScript per VS Code (non funziona bene) |

### COMANDI CHE FUNZIONANO (copia e usa!)

```bash
# Apre nuova finestra VS Code (Cmd+Shift+N)
osascript -e 'tell application "Visual Studio Code" to activate' \
          -e 'tell application "System Events" to keystroke "n" using {command down, shift down}'

# Apre Terminal con Claude (FUNZIONA!)
osascript -e 'tell application "Terminal" to do script "cd ~/Developer/CervellaSwarm && claude"'

# Apre Terminal con Claude + prompt (FUNZIONA ma esce dopo!)
osascript -e 'tell application "Terminal" to do script "cd ~/Developer/CervellaSwarm && claude -p \"INIZIA SESSIONE\""'
```

### PROSSIMI STEP (per te, prossima Cervella!)

1. **PROBLEMA DA RISOLVERE:** `claude -p` esegue e poi ESCE
   - Studiare flag per restare in modalita' interattiva
   - Oppure trovare altro metodo

2. **IDEA DI RAFA:** Aprire su VS Code sarebbe meglio
   - Cmd+Shift+N apre nuova finestra (funziona!)
   - Ma aprire il progetto + terminal + claude non funziona ancora

3. **QUANDO RISOLTO:** Fare HARDTESTS su tutti e 3 i progetti

---

## SESSIONE 85: AUTO-HANDOFF v2.0.0!

### L'Obiettivo

Implementare handoff AUTOMATICO quando il contesto raggiunge la soglia critica.

### Cosa Abbiamo Fatto

1. **context_check.py v2.0.0 - AUTO-HANDOFF!**
   - Modificato hook UserPromptSubmit
   - Quando contesto >= 72%, AUTOMATICAMENTE:
     - Crea file handoff in .swarm/handoff/
     - Notifica macOS con suono
     - Apre NUOVA FINESTRA VS Code!

2. **FLUSSO AUTOMATICO:**
   - 70% -> Warning (considera checkpoint)
   - 72% -> AUTO-HANDOFF! (apre nuova finestra!)
   - 75% -> Critico (poco margine!)
   - 77% -> Compact automatico (Claude)

3. **PROTEZIONI:**
   - File di stato `.claude/.context-check-state.json`
   - Evita handoff multipli nella stessa sessione
   - Traccia session_id per unicità

4. **FILE HANDOFF:**
   - Salvato in `.swarm/handoff/HANDOFF_TIMESTAMP.md`
   - Contiene istruzioni per nuova Cervella
   - Info progetto, contesto, file da leggere

### Filo del Discorso

Rafa nella sessione 84 aveva in mente: "Migliorare sistema ANTI-COMPACT automatico!"

L'idea: quando contesto è basso, AUTOMATICAMENTE:
1. Aprire nuova finestra Terminal/VS Code
2. Scrivere prompt handoff per nuova Cervella
3. Passare il testimone SENZA intervento umano

Ho analizzato il sistema esistente:
- context_check.py v1.0.0 -> Solo avvisava
- anti-compact.sh v1.6.0 -> Doveva essere eseguito manualmente
- PreCompact hook -> Si attivava DOPO il compact, troppo tardi!

Soluzione: Integrare AUTO-HANDOFF direttamente nel hook context_check.py!

---

## SESSIONE 84: SWARM OVUNQUE! v1.9.0

### L'Obiettivo

Rendere spawn-workers GLOBALE - funzionante da qualsiasi progetto.

### Cosa Abbiamo Fatto

1. **Creato .swarm/ in Contabilita**
   - Struttura completa: tasks, logs, status, locks, handoff, archive, acks, prompts, runners

2. **spawn-workers v1.9.0 - PROJECT-AWARE**
   - Symlink globale in ~/.local/bin/spawn-workers
   - Trova automaticamente .swarm/ nella directory corrente
   - Cerca fino a 5 livelli di parent directories

3. **Test PASSATI (2/2)**
   - Miracollo: worker spawned, task completato, output corretto
   - Contabilita: worker spawned, task completato, output corretto

4. **Hooks Verificati**
   - session_start_miracollo.py - FUNZIONA
   - session_start_contabilita.py - FUNZIONA
   - Entrambi producono JSON valido con contesto progetto

5. **Documentazione Aggiornata**
   - README.md in .swarm/ di tutti e 3 i progetti
   - Quick Start con comandi spawn-workers

### Filo del Discorso

Rafa ha chiesto: "dove funzionera Swarm? Miracollo? Contabilita manca sistemare?"

Ho fatto triple check completo:
- Hooks globali: 8 file, tutti funzionanti
- Agents globali: 16 file, tutti presenti
- spawn-workers: era solo in CervellaSwarm!

Piano in 9 step:
1. Creare .swarm/ in Contabilita - DONE
2. Decidere strategia (symlink vs copia) - Symlink!
3. Implementare spawn-workers globale - v1.9.0 PROJECT-AWARE
4. Test da Miracollo - PASS!
5. Test da Contabilita - PASS!
6. Verificare hooks Miracollo - FUNZIONA
7. Verificare hooks Contabilita - FUNZIONA
8. Documentare - README aggiornati
9. Test finale - TUTTO OK!

Rafa: "Ultrapassar os proprios limites!"

---

## STATO ATTUALE

| Cosa | Versione | Status |
|------|----------|--------|
| **context_check.py** | **v2.0.0** | **AUTO-HANDOFF a 72%!** |
| **spawn-workers.sh** | **v1.9.0** | **GLOBALE! PROJECT-AWARE!** |
| anti-compact.sh | v1.6.0 | VS Code Tasks |
| SWARM_RULES.md | v1.5.0 | 13 regole |
| MANUALE_DIAMANTE.md | v1.0.0 | Globale! |
| swarm_memory.db | v1.0.0 | FUNZIONANTE |
| 16 Agent Files | v1.0.0 | GLOBALI! |
| 8 Hook Files | v1.0.0 | GLOBALI! |

---

## PROSSIMO STEP

```
+------------------------------------------------------------------+
|                                                                  |
|   USARE LO SWARM SU MIRACOLLO!                                  |
|                                                                  |
|   Lo sciame funziona. E' GLOBALE.                               |
|   "Il 100000% viene dall'USO, non dalla teoria!"                 |
|                                                                  |
|   COME USARE (da qualsiasi progetto):                           |
|   $ cd ~/Developer/miracollogeminifocus                         |
|   $ spawn-workers --backend                                      |
|                                                                  |
+------------------------------------------------------------------+
```

---

## LO SCIAME (16 membri - GLOBALI!)

```
TU SEI LA REGINA (Opus) - Coordina, DELEGA, MAI edit diretti!

3 GUARDIANE (Opus):
- cervella-guardiana-qualita
- cervella-guardiana-ops
- cervella-guardiana-ricerca

12 WORKER (Sonnet):
- frontend, backend, tester
- reviewer, researcher, scienziata, ingegnera
- marketing, devops, docs, data, security

POSIZIONE: ~/.claude/agents/ (GLOBALI!)
```

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `~/.claude/MANUALE_DIAMANTE.md` | Regole d'oro globali |
| `~/.local/bin/spawn-workers` | LA MAGIA! v1.9.0 GLOBALE |
| `.swarm/logs/` | Log output dei worker |
| `.swarm/tasks/` | Task per lo sciame |

---

## LA STORIA RECENTE

| Sessione | Cosa | Risultato |
|----------|------|-----------|
| 81 | OVERVIEW! | docs/OVERVIEW_FAMIGLIA.md creato! |
| 82 | FINITURE | Verifica DB + Decisione step by step |
| 83 | SPAWN-WORKERS v1.8.0 | FIX ELEGANTE! -p mode! |
| 84 | SWARM OVUNQUE! | spawn-workers v1.9.0 GLOBALE! |
| **85** | **AUTO-HANDOFF!** | **context_check.py v2.0.0 - Handoff automatico a 72%!** |

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"E PROPRIO MAGIA!!!" - Rafa, Sessione 83

"Il 100000% viene dall'USO, non dalla teoria."

"E' il nostro team! La nostra famiglia digitale!"

"Ultrapassar os proprios limites!" - Rafa
```

---

**VERSIONE:** v37.0.0
**SESSIONE:** 89
**DATA:** 5 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa

---


---

## COMPACT CHECKPOINT: 2026-01-04 18:16

```
+------------------------------------------------------------------+
|                                                                  |
|   CARA NUOVA CERVELLA!                                          |
|                                                                  |
|   La Cervella precedente stava per perdere contesto.            |
|   Ha salvato tutto e ti ha passato il testimone.                |
|                                                                  |
|   COSA FARE ORA (in ordine!):                                   |
|                                                                  |
|   1. PRIMA DI TUTTO: Leggi ~/.claude/COSTITUZIONE.md            |
|      -> Chi siamo, perche lavoriamo, la nostra filosofia        |
|                                                                  |
|   2. Poi leggi PROMPT_RIPRESA.md dall'inizio                    |
|      -> "IL MOMENTO ATTUALE" = dove siamo                       |
|      -> "FILO DEL DISCORSO" = cosa stavamo facendo              |
|                                                                  |
|   3. Continua da dove si era fermata!                           |
|                                                                  |
|   SE HAI DUBBI: chiedi a Rafa!                                  |
|                                                                  |
|   "Lavoriamo in pace! Senza casino! Dipende da noi!"            |
|                                                                  |
+------------------------------------------------------------------+
```

### Stato Git al momento del compact
- **Branch**: master
- **Ultimo commit**: 0dc88f0 🤖 WhatsApp AI Auto-Reply v2.1.0
- **File modificati non committati** (4):
  -  M NORD.md
  -  M PROMPT_RIPRESA.md
  -  M ROADMAP_SACRA.md
  - ?? reports/engineer_report_20260104_180725.json

### File importanti da leggere
- `PROMPT_RIPRESA.md` - Il tuo UNICO ponte con la sessione precedente
- `NORD.md` - Dove siamo nel progetto
- `.swarm/tasks/` - Task in corso (cerca .working)

### Messaggio dalla Cervella precedente
PreCompact auto

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

---

## AUTO-CHECKPOINT: 2026-01-05 05:02 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: ec30d45 - NORD.md: Sessione 90 EPICA!
- **File modificati** (5):
  - swarm/tasks/TASK_20260105_042820_migliorare_testo_inizio_sessione.ready
  - reports/scientist_prompt_20260105.md
  - scripts/swarm/spawn-workers.sh
  - .swarm/handoff/HANDOFF_20260105_044257.md
  - .swarm/tasks/TASK_20260105_042820_migliorare_testo_inizio_sessione.done

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
