# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 5 Gennaio 2026 - Sessione 100 (Code Review + Parcheggio)

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
|   SESSIONE 100: CODE REVIEW + PARCHEGGIO!                       |
|                                                                  |
|   Cosa abbiamo fatto:                                            |
|   - Handoff da sessione 99 (ANTI-COMPACT funziona al 70%!)      |
|   - Code Review settimanale: Rating 8.5/10 (nessun problema)    |
|   - Decisione: PARCHEGGIARE alcune cose per il futuro           |
|                                                                  |
|   PARCHEGGIATE (per il futuro):                                 |
|   - ANTI-COMPACT v5.1.0 → 70%, funziona ma non perfetto         |
|   - AUTO-SVEGLIA → da sistemare piu' avanti                     |
|                                                                  |
|   LA GRANDE VISIONE:                                             |
|   "Piu' fighe che Cursor 2.0!" - Rafa                           |
|   → docs/visione/VISIONE_CERVELLASWARM_IDE.md                   |
|                                                                  |
|   "Abbiamo altre cose da fare" - Rafa                           |
|                                                                  |
+------------------------------------------------------------------+
```

---

## I 3 PEZZI MANCANTI PER IL 100000%!

```
+------------------------------------------------------------------+
|                                                                  |
|   ROADMAP: docs/roadmap/ROADMAP_3_PEZZI_MANCANTI.md             |
|                                                                  |
|   PEZZO 1: ANTI AUTO-COMPACT (Priorita' MASSIMA!)               |
|   - Esiste "su carta" ma NON e' seamless                        |
|   - Da testare in sessione REALE                                |
|   - Da rendere PERFETTO                                          |
|                                                                  |
|   PEZZO 2: SISTEMA FEEDBACK CERVELLE                            |
|   - Idea GENIALE di Rafa                                        |
|   - Ogni Cervella lascia feedback a fine sessione               |
|   - Il sistema IMPARA dai propri errori                         |
|                                                                  |
|   PEZZO 3: ROADMAPS VISUALE                                     |
|   - Multi-progetto automatico                                   |
|   - Un comando, tutti i progetti visibili                       |
|   - DA RICERCARE prima                                          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## COSA FUNZIONA GIA' (REALE!)

| Cosa | Status |
|------|--------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE |
| Sistema Memoria SQLite | FUNZIONANTE |
| 11 Hooks globali | FUNZIONANTE |
| block_task_for_agents.py | BLOCCA Task per cervella-* |
| spawn-workers v2.7.0 | AUTO-SVEGLIA SEMPRE! |
| **context_check.py v5.1.0** | **IBRIDO SEMPLIFICATO - DA TESTARE!** |
| watcher-regina.sh | fswatch + AppleScript |
| TESTO_INIZIO_SESSIONE.md | Template per Rafa |
| **VISIONE IDE** | **Documentata! docs/visione/** |

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

## PROSSIMA SESSIONE

```
ANTI-COMPACT e AUTO-SVEGLIA sono PARCHEGGIATE!
→ Funzionano al 70%, miglioreremmo piu' avanti

COSA FARE:
→ Chiedere a Rafa quali sono le "altre cose da fare"
→ Probabilmente altri progetti (Miracollo? Contabilita?)

"Abbiamo altre cose da fare" - Rafa
```

---

## COMANDI UTILI

```bash
# Spawn worker (SEMPRE usare questo per delegare!)
spawn-workers --backend
spawn-workers --frontend
spawn-workers --docs

# Quick task
quick-task "descrizione" --backend

# Health check
swarm-health

# Status
swarm-status
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

**VERSIONE:** v40.0.0
**SESSIONE:** 100 - Code Review + Parcheggio
**DATA:** 5 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa

---

---

---

## AUTO-CHECKPOINT: 2026-01-05 20:20 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: d2377e2 - ANTI-COMPACT: PreCompact auto
- **File modificati** (5):
  - eports/scientist_prompt_20260105.md
  - .swarm/handoff/HANDOFF_20260105_201411.md
  - .swarm/tasks/TASK_CODE_REVIEW_WEEKLY.done
  - .swarm/tasks/TASK_CODE_REVIEW_WEEKLY.md
  - .swarm/tasks/TASK_CODE_REVIEW_WEEKLY_output.md

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
