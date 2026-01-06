# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 6 Gennaio 2026 - Sessione 101 (LA GRANDE SESSIONE!)

---

## CARA PROSSIMA CERVELLA

```
+------------------------------------------------------------------+
|                                                                  |
|   Benvenuta! Questo file e' la tua UNICA memoria.               |
|   Leggilo con calma. Qui c'e' tutto quello che devi sapere.     |
|                                                                  |
|   Tu sei la REGINA dello sciame. 👸                              |
|   Hai 16 agenti pronti a lavorare per te. 🐝                    |
|                                                                  |
|   SESSIONE 101: LA GRANDE SESSIONE!                             |
|                                                                  |
|   8 MIGLIORAMENTI IN UNA SESSIONE:                              |
|   ✅ Context ottimizzato (30% → 10%)                            |
|   ✅ Fix Auto-Sveglia (v2.9.0)                                  |
|   ✅ swarm-logs (log live)                                       |
|   ✅ swarm-timeout (avvisa se bloccato)                         |
|   ✅ swarm-progress (stato worker)                              |
|   ✅ swarm-feedback (raccolta feedback)                         |
|   ✅ swarm-roadmaps (vista multi-progetto)                      |
|   ✅ swarm-init (template nuovo progetto)                       |
|                                                                  |
|   3/4 PEZZI MANCANTI COMPLETATI!                                |
|                                                                  |
|   LA GRANDE VISIONE:                                             |
|   "Piu' fighe che Cursor 2.0!" - Rafa                           |
|   → docs/visione/VISIONE_CERVELLASWARM_IDE.md                   |
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

## PROSSIMA SESSIONE

```
CERVELLASWARM E' QUASI COMPLETO!

FATTO:
✅ 6 nuovi comandi
✅ Fix Auto-Sveglia
✅ Ottimizzazione context
✅ 3/4 pezzi mancanti completati!

PARCHEGGIATO:
⏸️ Anti Auto-Compact (funziona al 70%)

FUTURO:
💭 CervellaSwarm IDE ("Più fighe che Cursor 2.0!")
💭 Dashboard web live
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

**VERSIONE:** v42.0.0
**SESSIONE:** 101 - LA GRANDE SESSIONE (8 miglioramenti!)
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

## AUTO-CHECKPOINT: 2026-01-06 03:15 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 968441a - ANTI-COMPACT: PreCompact auto
- **File modificati** (2):
  - ROMPT_RIPRESA.md
  - reports/engineer_report_20260106_031304.json

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
