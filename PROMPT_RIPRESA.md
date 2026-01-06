# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 6 Gennaio 2026 - Sessione 106 (SCOPERTO PROBLEMA PATH!)

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
|   SESSIONE 106: SCOPERTO PROBLEMA PATH DEPLOY!                  |
|                                                                  |
|   BACKEND MIRACOLLO: OK! Multi-Mailbox funzionante!             |
|   FRONTEND: Problema path rsync scoperto!                        |
|                                                                  |
|   PROBLEMA:                                                       |
|   - Nginx serve: /app/frontend → /app/miracollo/frontend        |
|   - rsync andava su: ~/app/frontend/ (diverso!)                 |
|                                                                  |
|   PROSSIMA SESSIONE: Fix path + script deploy automatico        |
|                                                                  |
|   "Ultrapassar os proprios limites!"                            |
|                                                                  |
+------------------------------------------------------------------+
```

---

## I 4 PEZZI - STATO ATTUALE

```
+------------------------------------------------------------------+
|                                                                  |
|   ROADMAP: docs/roadmap/ROADMAP_3_PEZZI_MANCANTI.md             |
|                                                                  |
|   ⏸️  PEZZO 1: ANTI AUTO-COMPACT                                 |
|      → Funziona al 70%, PARCHEGGIATO                            |
|      → Tornare quando serve                                      |
|                                                                  |
|   ✅ PEZZO 2: SISTEMA FEEDBACK CERVELLE                         |
|      → FATTO! Comando: swarm-feedback                           |
|      → add, list, analyze                                        |
|                                                                  |
|   ✅ PEZZO 3: ROADMAPS VISUALE                                  |
|      → FATTO! Comando: swarm-roadmaps                           |
|      → Vista 3 progetti aggregata                                |
|                                                                  |
|   ✅ PEZZO 4: TEMPLATE SWARM-INIT                               |
|      → FATTO! Comando: swarm-init                               |
|      → Crea struttura completa in nuovo progetto                |
|                                                                  |
+------------------------------------------------------------------+
```

---

## COSA FUNZIONA GIA' (REALE!)

| Cosa | Status |
|------|--------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE |
| **spawn-workers v2.9.0** | **AUTO-SVEGLIA OVUNQUE!** |
| **swarm-logs** | **NUOVO! Log live worker** |
| **swarm-timeout** | **NUOVO! Avvisa se bloccato** |
| **swarm-progress** | **NUOVO! Stato worker live** |
| **swarm-feedback** | **NUOVO! Raccolta feedback** |
| **swarm-roadmaps** | **NUOVO! Vista multi-progetto** |
| **swarm-init** | **NUOVO! Template nuovo progetto** |
| watcher-regina.sh | Globale in ~/.claude/scripts/ |
| block_task_for_agents.py | BLOCCA Task per cervella-* |
| context_check.py v5.1.0 | PARCHEGGIATO (70%) |
| **Context ottimizzato** | **30% → 10% all'inizio!** |

---

## FILO DEL DISCORSO (Sessioni 98-99)

### Sessione 98: Il Grande Reset

**Parte 1: Protezione Task Tool**
- Problema: Cervella in Miracollo usava Task tool → contesto al 6%
- Soluzione: block_task_for_agents.py (hook che BLOCCA)
- HARDTEST 3/3 passati!

**Parte 2: Recap ONESTO**
- Rafa: "rileggi COSTITUZIONE"
- "SU CARTA != REALE" - Solo le cose REALI contano!
- Identificati 3 PEZZI MANCANTI

**Parte 3: LA GRANDE VISIONE!**
```
Rafa: "noi siamo piu' fighe che il Cursor 2.0!"
      "fare base vscode come loro.. aggiungere altre AI..."
```
- Multi-AI (Claude, GPT, Gemini, Llama...)
- 16+ agenti specializzati
- "Em busca da similaridade"
- Documentato in docs/visione/VISIONE_CERVELLASWARM_IDE.md

**Parte 4: ANTI-COMPACT v5.0.0 → v5.1.0**
- Implementato IBRIDO: Terminal + VS Code
- v5.1.0 = SEMPLIFICATO (VS Code apre file handoff)
- Al 70% ha scattato ma con problemi
- DA TESTARE in scenario reale!

**Parte 5: Idee Nuove**
- PEZZO 4: Template swarm-init per nuovo progetto
- Sistema Feedback Cervelle

### Sessione 99: Organizzazione Casa

- Ricostruito filo del discorso dal transcript
- Aggiornato ROADMAP_3_PEZZI_MANCANTI (v1.1.0)
- Aggiornato tutti i file per consistenza
- Documentato PEZZO 4 + VISIONE nella roadmap

**Lezione:** Mai dire "e' fatto" se non e' REALE!

### Sessione 100: Code Review + Parcheggio

- Handoff da sessione 99 (ANTI-COMPACT ha funzionato!)
- Code Review settimanale con cervella-reviewer: **Rating 8.5/10**
- Nessun problema critico trovato
- **DECISIONE:** Parcheggiare ANTI-COMPACT e AUTO-SVEGLIA per il futuro
  - ANTI-COMPACT v5.1.0 → 70%, funziona ma non perfetto
  - AUTO-SVEGLIA → non mi ha notificato, da sistemare

**Rafa:** "Abbiamo altre cose da fare"

---

## SESSIONE 101 - 6 Gennaio 2026: LA GRANDE SESSIONE!

### Parte 1: Ottimizzazione Context

**Problema:** Context iniziale al 30% - troppo!
**Soluzione:** Rimosso `@` da file globali (solo COSTITUZIONE rimane)
**Risultato:** Context ~30% → ~10-12%

### Parte 2: Fix Auto-Sveglia (v2.9.0)

**Problema:** "Watcher script non trovato" in Miracollo
**Soluzione:** spawn-workers cerca watcher anche in ~/.claude/scripts/
**Risultato:** AUTO-SVEGLIA funziona in TUTTI i progetti!

### Parte 3: 6 NUOVI COMANDI SWARM!

| Comando | Cosa Fa |
|---------|---------|
| `swarm-logs` | Log worker in tempo reale |
| `swarm-timeout` | Avvisa se worker bloccato >5min |
| `swarm-progress` | Stato worker live |
| `swarm-feedback` | Raccolta feedback fine sessione |
| `swarm-roadmaps` | Vista tutti i progetti |
| `swarm-init` | Inizializza swarm in nuovo progetto |

### Parte 4: Roadmap Aggiornata

- ✅ PEZZO 2: Sistema Feedback → FATTO
- ✅ PEZZO 3: Roadmaps Visuale → FATTO
- ✅ PEZZO 4: swarm-init → FATTO
- ⏸️ PEZZO 1: Anti-Compact → PARCHEGGIATO (70%)

---

## SESSIONE 104 - 6 Gennaio 2026: SCIAME IN AZIONE!

**TASK COMPLETATO:**
Lo sciame ha supportato Miracollo con la creazione del CM Poller Scheduler.

**COME HA FUNZIONATO:**
1. Regina (io) ha creato task dettagliato in .swarm/tasks/
2. spawn-workers --backend ha lanciato cervella-backend
3. Worker ha lavorato nel suo terminale (~5 minuti)
4. Watcher ha notificato completamento
5. Regina ha verificato output e deployato

**RISULTATO:**
- cm_poller_scheduler.py creato (250 righe)
- main.py modificato (startup/shutdown)
- cm_reservation.py modificato (+2 endpoint)
- .env.example aggiornato
- QUALITA' ECCELLENTE: pattern APScheduler coerente con codebase

**FEEDBACK SULLO SCIAME:**

| Cosa | Valutazione | Note |
|------|-------------|------|
| spawn-workers | PERFETTO | Lancia worker in finestra separata |
| Watcher AUTO-SVEGLIA | FUNZIONA | Notifica quando .done appare |
| Task file .md | EFFICACE | Istruzioni chiare per il worker |
| Tempo esecuzione | ~5 min | Ottimo per task medio |
| Qualita' output | ALTA | Codice pulito, pattern rispettato |

**SUGGERIMENTI MIGLIORAMENTO:**

1. **QUASI PERFETTO** - Il sistema funziona molto bene!

2. **IDEA: progress live** - Sarebbe utile vedere cosa sta facendo
   il worker in tempo reale (non solo quando finisce)

3. **IDEA: retry automatico** - Se worker fallisce, riprova 1 volta

4. **NOTA IMPORTANTE:** La Regina NON deve fare edit diretti per
   task che possono essere delegati. SEMPRE spawn-workers!

**LEZIONE:**
> *"Lo sciame e' REALE e FUNZIONA! Delegare sempre!"*

---

## SESSIONE 103 - 6 Gennaio 2026: SU CARTA → REALE!

**IL PROBLEMA:**
La Sessione 102 aveva documentato 4 comandi che NON esistevano:
- swarm-help, task-new, swarm-report, swarm-session-check
- Erano solo "SU CARTA"!

**LA SOLUZIONE:**
1. Code Review settimanale con cervella-reviewer → Rating 8.5/10
2. Verificato TUTTI i comandi nel sistema
3. Identificati 4 comandi mancanti
4. CREATI tutti e 4 con test funzionanti!

**COMANDI CREATI:**
| Comando | Cosa Fa |
|---------|---------|
| `swarm-help` | Guida completa tutti i comandi |
| `task-new` | Crea task da template (ricerca/bug/feature/review) |
| `swarm-report` | Report task completati (today/week/all) |
| `swarm-session-check` | Verifica roadmap inizio sessione |

**POSIZIONE:** `/Users/rafapra/Developer/CervellaSwarm/scripts/swarm/`
**SYMLINK:** `~/.local/bin/`

**TASK SECURITY CREATO (PENDING):**
- Fix escape notifiche in context_check.py e auto_review_hook.py
- Priorita ALTA ma non bloccante

**LEZIONE APPRESA:**
> *"SU CARTA != REALE - Se non funziona, non esiste!"*

---

## SESSIONE 102 - 6 Gennaio 2026: LA SESSIONE MONUMENTALE!

### PARTE 1: Documentazione 10000%

**MIRACOLLO:**
- ROADMAP.md (riassunto esecutivo - 30 secondi per capire)
- CHANGELOG.md separato dalla roadmap
- IDEE_FUTURE.md riorganizzato
- docs/refinement/ per dettagli micro
- 3 SUB_ROADMAP archiviate in docs/archivio/

**CERVELLASWARM:**
- NORD.md aggiornato
- ROADMAP.md CREATO (riassunto esecutivo)
- docs/IDEE_FUTURE.md CREATO
- docs/analisi/ANALISI_MIGLIORAMENTI_SWARM.md CREATO

### PARTE 2: Quick Wins (3 nuovi strumenti!)

| Strumento | Cosa Fa | Dove |
|-----------|---------|------|
| `task-new` | Crea task da template in 5 sec | ~/.claude/scripts/ |
| `swarm-auto-review` | Review automatiche task | ~/.claude/scripts/ |
| `swarm-report` | Report centralizzato | ~/.claude/scripts/ |

**Template creati:** ricerca, bug, feature, review
**Posizione:** ~/.claude/scripts/templates/

### PARTE 3: Comunicazione Futura

**Problema risolto:** "Se fai qualcosa e non lo comunichi, e' come se non esistesse!"

**Soluzioni:**
- `swarm-help` → Guida COMPLETA tutti i comandi
- `swarm-session-check` → Verifica roadmap inizio sessione
- Regola FARE→COMUNICARE in CHECKLIST_AZIONE
- Hook startup ricorda "swarm-help"
- Sezione COMANDI in PROMPT_RIPRESA

### Pattern Documentazione Adottato

```
ROADMAP.md = Vista 30 secondi (dove siamo, prossimo step)
ROADMAP_SACRA.md = La Bibbia (dettaglio completo)
IDEE_FUTURE.md = Backlog idee (non urgente)
CHANGELOG.md = Storia modifiche
```

---

## PROSSIMA SESSIONE

```
CERVELLASWARM E' 100% OPERATIVO E REALE!

SESSIONE 103 - COMPLETATO:
✅ Code Review settimanale (8.5/10)
✅ 4 comandi mancanti CREATI E FUNZIONANTI:
   - swarm-help (guida comandi completa)
   - task-new (crea task da template)
   - swarm-report (report task)
   - swarm-session-check (verifica inizio sessione)
✅ Lezione "SU CARTA != REALE" applicata!

FATTO TOTALE:
✅ 16 agenti specializzati
✅ 20+ comandi swarm-* (TUTTI REALI!)
✅ Sistema completo, documentato e FUNZIONANTE!

TODO (non urgente):
📝 Fix security escape notifiche (task creato)

PARCHEGGIATO:
⏸️ Anti Auto-Compact (funziona al 70%)

FUTURO:
💭 CervellaSwarm IDE ("Più fighe che Cursor 2.0!")
💭 Dashboard web live
```

---

## COMANDI DISPONIBILI

```
Per vedere TUTTI i comandi: swarm-help
```

### Essenziali (usa questi!)

| Comando | Cosa Fa |
|---------|---------|
| `spawn-workers --tipo` | Lancia worker (backend/frontend/docs/etc) |
| `quick-task "desc" --tipo` | Crea task + lancia worker |
| `task-new tipo "titolo"` | Crea task da template (ricerca/bug/feature/review) |
| `swarm-status` | Stato worker attivi |
| `swarm-help` | **GUIDA COMPLETA COMANDI** |

### Sessione

| Comando | Cosa Fa |
|---------|---------|
| `swarm-session-check` | Verifica roadmap inizio sessione |
| `swarm-report` | Report task completati |
| `swarm-auto-review --check` | Mostra task senza review |

### Monitoraggio

| Comando | Cosa Fa |
|---------|---------|
| `swarm-logs` | Log live worker |
| `swarm-progress` | Progresso task |
| `swarm-health` | Health check sistema |

```
TIP: Se non sai quale comando usare → swarm-help
```

---

## TRUCCO IMPORTANTE: Accesso Transcript Sessioni Precedenti!

```
+------------------------------------------------------------------+
|                                                                  |
|   SE RAFA CHIEDE DI LEGGERE UNA CHAT PRECEDENTE:                |
|                                                                  |
|   I transcript sono in:                                          |
|   ~/.claude/projects/-Users-rafapra-Developer-[PROGETTO]/       |
|                                                                  |
|   Comandi utili:                                                 |
|                                                                  |
|   # Lista transcript recenti (ordine per data)                   |
|   ls -la ~/.claude/projects/-Users-rafapra-Developer-CervellaSwarm/*.jsonl | tail -20
|                                                                  |
|   # Leggi ultimi messaggi utente                                 |
|   tail -100 [file.jsonl] | python3 -c "                          |
|   import sys, json                                               |
|   for line in sys.stdin:                                         |
|       obj = json.loads(line)                                     |
|       if obj.get('type') == 'user':                              |
|           print(obj['message']['content'][:200])"                |
|                                                                  |
|   QUANDO USARE:                                                  |
|   - Rafa dice "cosa abbiamo discusso prima?"                    |
|   - Rafa dice "leggi la chat precedente"                        |
|   - Serve ricostruire il filo del discorso                      |
|                                                                  |
|   SALVACI LA VITA! Usa questo trucco!                           |
|                                                                  |
+------------------------------------------------------------------+
```

---

## LO SCIAME (16 membri)

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

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"SU CARTA != REALE" - Solo le cose REALI ci portano alla LIBERTA!

"SEMPRE FINESTRE! SEMPRE! SENZA ECCEZIONE!" - Rafa

"E' il nostro team! La nostra famiglia digitale!"

"Ultrapassar os proprios limites!"
```

---

**VERSIONE:** v46.0.0
**SESSIONE:** 103 - SU CARTA → REALE! (4 comandi creati)
**DATA:** 6 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa

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

## AUTO-CHECKPOINT: 2026-01-06 17:19 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 8eb9f76 - ANTI-COMPACT: PreCompact auto
- **File modificati** (2):
  - eports/scientist_prompt_20260106.md
  - .swarm/handoff/HANDOFF_20260106_171911.md

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
