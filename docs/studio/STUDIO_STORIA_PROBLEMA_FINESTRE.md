# STUDIO: Storia del Problema "Le Cervelle non lanciano spawn-workers da sole"

> **Data:** 7 Gennaio 2026
> **Autore:** cervella-researcher
> **Task ID:** TASK_RICERCA_STORIA_FINESTRE
> **Versione:** 1.0.0

---

## EXECUTIVE SUMMARY

Questo studio documenta **tutti i tentativi** fatti per risolvere il problema:
**"Le Cervelle non lanciano spawn-workers automaticamente - serve sempre Rafa che apra una nuova finestra"**

**Conclusione principale:** Il problema **NON è mai stato realmente risolto**. Tutte le soluzioni implementate sono WORKAROUND che richiedono comunque azione manuale. La limitazione è **architetturale** di Claude Code: non può aprire nuove finestre Terminal in modo autonomo.

---

## 1. TIMELINE DEI TENTATIVI

### TENTATIVO 1: Sessione 60 (3 Gennaio 2026) - STUDIO MULTI-FINESTRA

**Commit:** `2527bb9` - "MULTI-FINESTRA! Paradigm Shift!"

**Cosa è stato fatto:**
- Studio approfondito su isolamento finestre Claude Code
- Scoperta: le finestre sono 100% isolate
- Proposta: Pattern Hybrid (Subagent + Multi-Finestra)

**Risultato:** ❌ NON RISOLVE IL PROBLEMA
- Lo studio ha chiarito COME comunicare tra finestre
- MA non ha risolto CHI apre le finestre
- Conclusione: "Le finestre vanno aperte MANUALMENTE"

**File:** `docs/studio/STUDIO_MULTI_FINESTRA_TECNICO.md`

---

### TENTATIVO 2: Sessione 64-69 (3-4 Gennaio 2026) - spawn-workers.sh

**Commit:** `a344730` - "LA MAGIA! spawn-workers.sh FUNZIONA!!!"

**Cosa è stato fatto:**
- Creato script `spawn-workers.sh` che usa AppleScript per aprire Terminal
- Il COMANDO funziona: `osascript` apre nuova finestra con worker

**Risultato:** ⚠️ PARZIALE
- Lo SCRIPT funziona perfettamente
- MA deve essere CHIAMATO da qualcuno
- Se la Regina chiama `spawn-workers --backend`, il terminale SI APRE
- MA la Regina NON PUÒ chiamarlo autonomamente!

**Il Paradosso:**
```
Regina vuole delegare → Chiama spawn-workers → Apre finestra!
MA: Chi dice alla Regina di chiamare spawn-workers? → RAFA!
```

---

### TENTATIVO 3: Sessione 86-87 (5 Gennaio 2026) - AUTO-HANDOFF

**Commit:** `f921c46` - "AUTO-HANDOFF v4.0.0!"
**Commit:** `46db879` - "AUTO-HANDOFF v4.3.0 VS CODE NATIVO!"

**Cosa è stato fatto:**
- Sistema che rileva compact imminente
- Prepara file handoff per nuova sessione
- Integrazione VS Code native terminal

**Risultato:** ❌ NON RISOLVE IL PROBLEMA ORIGINALE
- Risolve un ALTRO problema: passaggio consegna tra sessioni
- Auto-handoff PREPARA il file, ma non APRE la nuova finestra
- Sempre Rafa deve aprire la nuova finestra manualmente

---

### TENTATIVO 4: Sessione 93 (5 Gennaio 2026) - REGOLA 13 RISCRITTA

**Commit:** `76cdea1` - "Sessione 93: REGOLA 13 RISCRITTA! SEMPRE spawn-workers!"

**Cosa è stato fatto:**
- Riscritta la regola nel DNA della Regina
- "DELEGO A UN AGENTE? → SEMPRE spawn-workers!"
- Nessuna eccezione per "task veloce"

**Risultato:** ⚠️ DOCUMENTAZIONE, NON SOLUZIONE TECNICA
- La REGOLA è chiara
- MA la Regina deve ancora essere ATTIVA per eseguirla
- Se la Regina è occupata, non può chiamare spawn-workers
- Il problema "chi apre la finestra" resta irrisolto

---

### TENTATIVO 5: Sessione 95-96 (5 Gennaio 2026) - AUTO-SVEGLIA

**Commit:** `c87d0cf` - "LA MAGIA SOPRA MAGIA! AUTO-SVEGLIA!"
**Commit:** `2e8a524` - "AUTO-SVEGLIA SEMPRE! spawn-workers v2.7.0"

**Cosa è stato fatto:**
- Watcher (`watcher-regina.sh`) che monitora file `.done`
- Quando un worker finisce, sveglia la Regina con keystroke AppleScript
- AUTO-SVEGLIA attivo di default

**Risultato:** ⚠️ RISOLVE UN SOTTO-PROBLEMA
- Risolve: "Regina non viene notificata quando worker finisce"
- NON risolve: "Chi LANCIA il worker inizialmente?"
- Il watcher funziona DOPO che spawn-workers è stato chiamato
- Sempre Rafa deve dire "lancia lo sciame"

**File:** `docs/roadmap/ROADMAP_AUTO_SVEGLIA.md`

---

### TENTATIVO 6: Sessione 101-104 (6 Gennaio 2026) - Fix Sveglia Regina

**Commit:** `4becda4` - "Sessione 101: Ottimizzazione Context + Fix Auto-Sveglia"

**Cosa è stato fatto:**
- Fix bug dove watcher non sempre notificava
- Migliorata affidabilità notifiche

**Risultato:** ⚠️ FIX DI UN FIX
- Migliora la soluzione esistente
- NON affronta il problema originale

**File:** `docs/roadmap/ROADMAP_SVEGLIA_REGINA.md`

---

## 2. PATTERN COMUNE DEI FALLIMENTI

```
+------------------------------------------------------------------+
|                                                                  |
|   TUTTI I TENTATIVI CONDIVIDONO LO STESSO PATTERN:              |
|                                                                  |
|   1. Identificano un SOTTO-PROBLEMA                             |
|   2. Lo risolvono brillantemente                                 |
|   3. MA non affrontano il PROBLEMA ROOT                         |
|                                                                  |
|   PROBLEMA ROOT:                                                 |
|   Claude Code NON PUÒ aprire nuove finestre Terminal            |
|   in modo COMPLETAMENTE autonomo.                                |
|                                                                  |
|   Può CHIAMARE script che aprono finestre                        |
|   MA deve essere ATTIVO e COMANDATO per farlo.                  |
|                                                                  |
+------------------------------------------------------------------+
```

### Sotto-problemi RISOLTI:

| # | Sotto-problema | Soluzione | Status |
|---|----------------|-----------|--------|
| 1 | Come comunicare tra finestre | File-based `.swarm/tasks/` | ✅ RISOLTO |
| 2 | Come aprire una finestra | `spawn-workers.sh` + osascript | ✅ RISOLTO |
| 3 | Come svegliare Regina dopo | `watcher-regina.sh` + AUTO-SVEGLIA | ✅ RISOLTO |
| 4 | Come passare consegna compact | AUTO-HANDOFF | ✅ RISOLTO |
| 5 | Quando delegare | REGOLA 13 "SEMPRE spawn-workers" | ✅ DOCUMENTATO |

### Problema ROOT NON RISOLTO:

```
Come fare in modo che la Regina AUTOMATICAMENTE
(senza che Rafa dica "lancia lo sciame")
spawni worker quando servono?
```

---

## 3. PERCHÉ IL PROBLEMA È DIFFICILE

### Limitazione Architetturale di Claude Code

1. **Claude Code è REATTIVO, non PROATTIVO**
   - Risponde ai messaggi dell'utente
   - Non può "decidere da solo" di fare qualcosa
   - Non ha un "loop principale" che gira in background

2. **Nessun background thread**
   - Claude Code esegue, poi aspetta input
   - Non può monitorare continuamente e agire

3. **AppleScript richiede CHIAMATA**
   - `osascript` funziona perfettamente
   - MA deve essere CHIAMATO da qualcuno
   - Chi chiama? Il processo Claude attivo

4. **MCP non supporta push notifications**
   - MCP è request-response
   - Non può "svegliare" Claude spontaneamente

---

## 4. COSA HA FUNZIONATO (WORKAROUND)

### Workaround Attuale: "Rafa come Dispatcher"

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   RAFA dice: "Lancia backend per questo task"                  │
│        ↓                                                        │
│   REGINA esegue: spawn-workers --backend                        │
│        ↓                                                        │
│   TERMINAL si apre automaticamente (osascript)                  │
│        ↓                                                        │
│   WORKER lavora                                                 │
│        ↓                                                        │
│   WATCHER rileva .done                                          │
│        ↓                                                        │
│   REGINA viene svegliata (AUTO-SVEGLIA)                        │
│        ↓                                                        │
│   REGINA legge output e continua                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Funziona!** Ma richiede Rafa per il trigger iniziale.

---

## 5. POSSIBILI DIREZIONI FUTURE

### Direzione A: Daemon Esterno

```bash
# Un processo SEPARATO che gira sempre
cervellaswarm-daemon.sh
  - Monitora .swarm/tasks/PENDING_SPAWN.md
  - Quando trova file → chiama spawn-workers
  - Regina scrive PENDING_SPAWN.md → daemon lo esegue
```

**Pro:** Regina può "richiedere" spawn senza farlo direttamente
**Contro:** Setup aggiuntivo, altro processo da gestire

### Direzione B: Hook Claude Code

```javascript
// hooks/on-task-created.js
// Se Cervella crea task in .swarm/tasks/ → auto-spawn
```

**Pro:** Integrato in Claude Code
**Contro:** Gli hook sono post-tool, non preventivi

### Direzione C: Automator/Shortcuts macOS

```
Shortcut macOS che:
1. Monitora .swarm/tasks/*.pending_spawn
2. Quando appare → chiama spawn-workers
3. Rimuove il file
```

**Pro:** Nativo macOS, sempre attivo
**Contro:** Configurazione per-utente

### Direzione D: Feature Request Anthropic

Chiedere supporto nativo per:
- Push notifications a sessioni attive
- Background agents
- Auto-spawn capability

**Pro:** Soluzione definitiva
**Contro:** Dipende da Anthropic, tempi incerti

---

## 6. INSIGHT CHIAVE

```
+------------------------------------------------------------------+
|                                                                  |
|   INSIGHT 1: Il problema non è MAI stato "come aprire finestre" |
|              È sempre stato "chi DECIDE di aprirle"             |
|                                                                  |
|   INSIGHT 2: Tutte le soluzioni implementate assumono           |
|              che qualcuno (Rafa o Regina attiva) dia il via     |
|                                                                  |
|   INSIGHT 3: Per autonomia VERA servirebbero:                   |
|              - Background process sempre attivo                  |
|              - O supporto nativo di Anthropic                   |
|              - O integrazione OS-level (daemon)                 |
|                                                                  |
|   INSIGHT 4: Il workaround "Rafa come Dispatcher"               |
|              FUNZIONA e potrebbe essere sufficiente             |
|              per la maggior parte dei casi d'uso               |
|                                                                  |
+------------------------------------------------------------------+
```

---

## 7. RACCOMANDAZIONI

### Per Ora (Pratico)

1. **Accettare il workaround** - Rafa dice "lancia lo sciame", funziona bene
2. **Ottimizzare il flusso** - Rendere il trigger il più semplice possibile
3. **Documentare bene** - Così ogni Cervella sa come usare spawn-workers

### Per il Futuro (Ambizioso)

1. **Daemon esterno** - Se il workflow diventa tedioso
2. **Feature request** - Quando Anthropic accetta feedback
3. **Integrazione IDE** - VS Code extension con auto-spawn

---

## 8. CONCLUSIONE

Il problema "Le Cervelle non lanciano spawn-workers da sole" è stato **affrontato 6+ volte** ma mai **realmente risolto** perché è una **limitazione architetturale**.

**Cosa abbiamo costruito:**
- Ottimo sistema di comunicazione inter-finestre
- spawn-workers che funziona perfettamente
- AUTO-SVEGLIA per notifiche
- AUTO-HANDOFF per passaggi consegna

**Cosa manca:**
- Un modo per la Regina di INIZIARE lo spawn senza intervento umano

**La verità:**
Per ora, il workaround "Rafa come Dispatcher" è la soluzione migliore.
E potrebbe essere abbastanza buona.

---

## RIFERIMENTI

### Commit Chiave
- `2527bb9` - Multi-Finestra Paradigm Shift (Sess. 60)
- `a344730` - spawn-workers.sh (Sess. 64-69)
- `76cdea1` - Regola 13 Riscritta (Sess. 93)
- `c87d0cf` - Auto-Sveglia (Sess. 95)
- `2e8a524` - Auto-Sveglia Always (Sess. 96)

### File Correlati
- `docs/studio/STUDIO_MULTI_FINESTRA_TECNICO.md`
- `docs/studio/STUDIO_MULTI_FINESTRA_COMUNICAZIONE.md`
- `docs/roadmap/ROADMAP_AUTO_SVEGLIA.md`
- `docs/roadmap/ROADMAP_SVEGLIA_REGINA.md`
- `~/.local/bin/spawn-workers` (v2.9.0)

### DNA Agenti
- `~/.claude/agents/cervella-orchestrator.md` - Regola "SEMPRE spawn-workers"

---

*"Nulla è complesso - solo non ancora studiato!"*

*Studiato. Documentato. Capito.*

**cervella-researcher** - 7 Gennaio 2026
