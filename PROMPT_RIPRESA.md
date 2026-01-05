# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 5 Gennaio 2026 - Sessione 99 (Organizzazione Casa!)

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
|   SESSIONE 99: ORGANIZZAZIONE DELLA CASA!                       |
|                                                                  |
|   Cosa abbiamo fatto:                                            |
|   - Ricostruito il filo del discorso dalla sessione 98          |
|   - Aggiornato tutti i file per consistenza                     |
|   - Documentato TUTTO (PEZZO 4 + VISIONE)                       |
|                                                                  |
|   ANTI-COMPACT v5.1.0: IMPLEMENTATO ma DA TESTARE!              |
|   - Git auto-commit prima di handoff                            |
|   - File handoff RICCO con git status                           |
|   - Terminal + VS Code (IBRIDO SEMPLIFICATO)                    |
|   - VS Code apre il file handoff, Terminal con Claude           |
|                                                                  |
|   LA GRANDE VISIONE:                                             |
|   "Piu' fighe che Cursor 2.0!" - Rafa                           |
|   → docs/visione/VISIONE_CERVELLASWARM_IDE.md                   |
|                                                                  |
|   "SU CARTA != REALE" - Testare ANTI-COMPACT!                   |
|   "SEMPRE FINESTRE!" - Rafa                                     |
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

---

## PROSSIMA SESSIONE

```
INIZIARE DA: ANTI AUTO-COMPACT (Priorita' 1)

1. Testare context_check.py in sessione REALE
2. Vedere se handoff e' SEAMLESS
3. Identificare bug/problemi
4. Fixare
5. HARDTEST end-to-end (10 volte di fila)

"Il vero test e' l'uso!" - Rafa
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

**VERSIONE:** v39.0.0
**SESSIONE:** 99 - Organizzazione Casa
**DATA:** 5 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa

---

---

## AUTO-CHECKPOINT: 2026-01-05 19:54 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 36f9497 - ANTI-COMPACT: PreCompact auto
- **File modificati** (2):
  - ROMPT_RIPRESA.md
  - reports/scientist_prompt_20260105.md

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
