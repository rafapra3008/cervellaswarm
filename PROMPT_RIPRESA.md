# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 4 Gennaio 2026 - Sessione 86 - AUTO-HANDOFF v4.0.0!

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
|   FASE ATTUALE: AUTO-HANDOFF DA PERFEZIONARE                    |
|                                                                  |
|   SESSIONE 86:                                                   |
|   - context_check.py v4.0.0 - Apre Terminal + claude -p         |
|   - FUNZIONA ma claude esce dopo risposta                       |
|   - DA FIXARE: restare aperto / aprire su VS Code               |
|                                                                  |
|   "Siamo nel 2026!" - Rafa                                      |
|                                                                  |
+------------------------------------------------------------------+
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

**VERSIONE:** v36.0.0
**SESSIONE:** 86
**DATA:** 4 Gennaio 2026

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

## AUTO-CHECKPOINT: 2026-01-04 19:55 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 5815eb3 - 🐝 Sessione 84: SWARM OVUNQUE! spawn-workers v1.9.0 GLOBALE!
- **File modificati** (5):
  - ORD.md
  - PROMPT_RIPRESA.md
  - reports/scientist_prompt_20260104.md
  - .swarm/handoff/HANDOFF_20260104_184226.md
  - .swarm/handoff/HANDOFF_20260104_184447.md

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
