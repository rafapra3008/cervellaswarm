# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 6 Gennaio 2026 - Sessione 109
> **Versione:** v1.4.0

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
|   SESSIONE 109: IL MIRACOLO È REALE!                            |
|                                                                  |
|   LO SCIAME E' OPERATIVO E REALE!                               |
|   - 16 agenti specializzati                                      |
|   - 20+ comandi swarm-* FUNZIONANTI                             |
|   - Supporto attivo a Miracollo                                  |
|                                                                  |
|   🎉 MIRACOLLO - IL PONTE FUNZIONA!                             |
|   - Prenotazione BeSync arriva AUTOMATICAMENTE!                  |
|   - Email → Parser → API → Database → Planning!                 |
|   - Testato con prenotazione VERA: BEXP_501443797               |
|   - Badge CM rosso visibile nel planning!                        |
|   - FASE 1.5 definita con 7 dettagli da studiare                |
|                                                                  |
|   "Non è sempre come immaginiamo...                             |
|    ma alla fine è il 100000%!"                                  |
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

## FILO DEL DISCORSO (Sessioni 104-109)

### Sessione 109: IL MIRACOLO È REALE! (ATTUALE)

**Mix Miracollo + CervellaSwarm**
- Fix API Key deployato (docker rebuild su VM)
- TEST con prenotazione VERA: BEXP_501443797
- IL PONTE BESYNC → MIRACOLLO FUNZIONA!
- Prenotazione visibile nel planning con badge CM rosso
- CHECKPOINT COMPLETO:
  - SUB_ROADMAP_CHANNEL_MANAGER.md aggiornata (v2.0.0)
  - NORD.md aggiornato
  - ROADMAP_SACRA.md aggiornata (v5.37.0)
  - FASE 1.5 definita con 7 dettagli da studiare

**FASE 1.5 - Dettagli Miracollo (prossime sessioni):**
- Mapping room_type → room_id
- Test notifica WhatsApp
- Test cancellazioni/modifiche BeSync
- Strategia email già lette
- UX pannello CM

---

### Sessione 108: Organizzazione Documentazione

**Handoff da sessione 107**
- Ricostruito filo sessioni 104-107 (erano rimaste indietro!)
- Verificato fix cervella-backend su Miracollo (API key - PRONTO)
- Organizzazione casa: documentazione al 100000%

---

### Sessione 107: Mix Miracollo+CervellaSwarm

- Letto MANUALE DIAMANTE (capito FORTEZZA MODE)
- Usato sistema SWARM con cervella-devops
- FORTEZZA MODE v2.0.0 completato su Miracollo
- Handoff automatico funzionante

---

### Sessione 106: Scoperto Problema PATH

- cervella-frontend ha fixato 11 file con URL hardcoded
- **SCOPERTA:** rsync andava su path sbagliato!
  - Nginx serve: `/app/frontend` → `/app/miracollo/frontend`
  - rsync andava su: `~/app/frontend/` (DIVERSO!)
- Risolto: deploy su `/app/miracollo/frontend/`

---

### Sessione 105: Deploy Multi-Mailbox Miracollo

- Rsync backend su VM completato
- Variabili `EMAIL_SECONDARY_*` aggiunte
- Container rebuilt e avviato
- **Verifica OK:** `mailbox_count: 2`

---

### Sessione 104: Sciame in Azione + Feedback

**LO SCIAME HA FUNZIONATO!**
- cervella-backend ha creato `cm_poller_scheduler.py` (~250 righe)
- Task completato in ~5 minuti
- Qualita' eccellente (pattern coerente con codebase)

**Feedback sullo sciame:**
| Cosa | Valutazione |
|------|-------------|
| spawn-workers | PERFETTO |
| Watcher AUTO-SVEGLIA | FUNZIONA |
| Task file .md | EFFICACE |

**Idee future:**
- Progress live durante esecuzione
- Retry automatico se worker fallisce

---

### Sessioni 98-103 (Archivio)

**Sessione 103:** SU CARTA → REALE! 4 comandi creati (swarm-help, task-new, swarm-report, swarm-session-check)
**Sessione 102:** La Sessione Monumentale - Documentazione 10000%
**Sessione 101:** La Grande Sessione - Context 30%→10%, 6 nuovi comandi
**Sessione 100:** Code Review + Parcheggio Anti-Compact
**Sessione 99:** Organizzazione Casa
**Sessione 98:** Il Grande Reset + LA GRANDE VISIONE (CervellaSwarm IDE)

*Per dettagli sessioni precedenti: vedi git log*

---

## STATO ATTUALE

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   CERVELLASWARM E' 100% OPERATIVO E REALE!                    ║
║                                                                ║
║   ✅ 16 agenti specializzati                                  ║
║   ✅ 20+ comandi swarm-* (TUTTI REALI!)                       ║
║   ✅ Sistema completo, documentato e FUNZIONANTE!             ║
║   ✅ Supporto attivo a Miracollo (sessioni 104-107)           ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║   MIRACOLLO - STATO ATTUALE:                                  ║
║   ✅ Parser email funziona PERFETTAMENTE!                     ║
║   ✅ Frontend deployato su path corretto                      ║
║   ✅ FORTEZZA MODE v2.0.0 completato                          ║
║   ⏳ Fix API key (cervella-backend PRONTO) → da deployare     ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║   PARCHEGGIATO:                                               ║
║   ⏸️ Anti Auto-Compact (funziona al 70%)                      ║
║                                                                ║
║   FUTURO:                                                      ║
║   💭 CervellaSwarm IDE ("Piu' fighe che Cursor 2.0!")         ║
║   💭 Dashboard web live                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
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

**VERSIONE:** v1.3.0
**SESSIONE:** 108 - Organizzazione Documentazione
**DATA:** 6 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa

---

---

## AUTO-CHECKPOINT: 2026-01-06 18:13 (unknown)

### Stato Git
- **Branch**: main
- **Ultimo commit**: 65288ae - 📍 HANDOFF Sessione 108: Supporto Miracollo
- **File modificati** (1):
  - reports/engineer_report_20260106_181245.json

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
