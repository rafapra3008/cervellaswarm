# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 4 Gennaio 2026 - Sessione 78

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
|   FASE ATTUALE: FASE 9 - APPLE STYLE (98% COMPLETATA!)          |
|                                                                  |
|   SESSIONE 77 COMPLETATA:                                        |
|   - REGOLA 13: Multi-finestra > Task tool (SWARM_RULES v1.5.0)  |
|   - anti-compact.sh: nuova finestra OBBLIGATORIA                |
|   - spawn-workers.sh v1.4.0: notifica PRIMA di exit             |
|   - FIX COSTITUZIONE.md: file reale (no symlink iCloud)         |
|                                                                  |
|   PROSSIMI STEP:                                                 |
|   - 3 HARDTEST da fare                                           |
|   - Poi MIRACOLLO!                                               |
|                                                                  |
+------------------------------------------------------------------+
```

---

## STATO ATTUALE

| Cosa | Versione | Status |
|------|----------|--------|
| spawn-workers.sh | v1.4.0 | Apple Style completo! |
| SWARM_RULES.md | v1.5.0 | 13 regole |
| Quick Wins | 10/10 | PASS |
| HARDTESTS Apple | 6/6 | PASS |
| MEGA TEST GOLD | 5 worker | PASS |

### Ultimo Commit
```
a970c7e - fix: spawn-workers.sh v1.4.0 - notifica PRIMA di exit
```

---

## FILO DEL DISCORSO (Sessione 77)

### Cosa abbiamo fatto

1. **REGOLA 13: MULTI-FINESTRA > TASK TOOL**
   - Il problema: Task tool = tutto nel contesto della Regina = rischio compact
   - La soluzione: spawn-workers.sh per lavoro parallelo REALE
   - "Comodo != Giusto!" - Lezione dalla Sessione 72
   - Aggiunta in SWARM_RULES.md (v1.5.0) e DNA Regina (v1.1.0)

2. **anti-compact.sh migliorato**
   - Nuova finestra e' OBBLIGATORIA, non opzionale!
   - Quando Rafa dice "siamo al 10%", DEVO aprire nuova finestra
   - Integrato con spawn-workers.sh per prompt automatico

3. **spawn-workers.sh v1.4.0**
   - FIX: notifica PRIMA di exit
   - Prima: worker faceva exit, non poteva notificare
   - Ora: `osascript ... && exit` - notifica + exit insieme

4. **FIX COSTITUZIONE.md**
   - Problema: symlink a iCloud non funzionava (permessi)
   - Soluzione: file reale in ~/.claude/COSTITUZIONE.md

5. **Documentata idea script monitor context**
   - File: docs/ideas/IDEA_CONTEXT_MONITOR.md
   - Per futuro: script che monitora % contesto automaticamente

### Il Flusso Anti-Compact CORRETTO

```
1. Rafa dice: "Cervella, siamo al 10%!"

2. Cervella esegue:
   ./scripts/swarm/anti-compact.sh --message "descrizione"

3. Lo script fa:
   - Aggiorna PROMPT_RIPRESA
   - Git commit + push
   - APRE NUOVA FINESTRA (obbligatorio!)

4. Nuova Cervella:
   - Legge COSTITUZIONE
   - Legge PROMPT_RIPRESA
   - Continua!
```

---

## PROSSIMI STEP

```
+------------------------------------------------------------------+
|                                                                  |
|   DA FARE:                                                       |
|                                                                  |
|   [ ] HARDTEST: Comunicazione bidirezionale                      |
|   [ ] HARDTEST: Flusso Guardiana review                          |
|   [ ] HARDTEST: Spawn dinamico Guardiane                         |
|                                                                  |
|   POI: MIRACOLLO!                                                |
|   "Il 100000% viene dall'USO, non dalla teoria."                |
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
- frontend, backend, tester, reviewer
- researcher, scienziata, ingegnera
- marketing, devops, docs, data, security
```

### Comandi spawn-workers.sh

```bash
# Spawn singolo worker
./scripts/swarm/spawn-workers.sh --backend

# Spawn multipli
./scripts/swarm/spawn-workers.sh --backend --frontend --tester

# Spawn Guardiane (Opus)
./scripts/swarm/spawn-workers.sh --guardiana-qualita
./scripts/swarm/spawn-workers.sh --guardiane  # Tutte e 3
```

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `docs/SWARM_RULES.md` | Le 13 regole dello sciame |
| `scripts/swarm/spawn-workers.sh` | LA MAGIA! Apre finestre worker |
| `.swarm/README.md` | Come funziona il sistema multi-finestra |
| `docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md` | Il riferimento (870+ righe) |

---

## COSA ESISTE GIA (funziona!)

| Cosa | Status |
|------|--------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE |
| Sistema Memoria SQLite | FUNZIONANTE |
| 10 Hooks globali | FUNZIONANTE |
| SWARM_RULES v1.5.0 | FUNZIONANTE |
| spawn-workers.sh v1.4.0 | APPLE STYLE! |
| Template DUBBI + PARTIAL | FUNZIONANTE |
| Triple ACK system | FUNZIONANTE |
| .swarm/ struttura | FUNZIONANTE |

---

## LA STORIA RECENTE

| Sessione | Cosa | Risultato |
|----------|------|-----------|
| 73 | spawn-workers.sh FUNZIONA! | Ciclo completo testato |
| 74 | PASSATI A MIRACOLLO! | Deploy 30 moduli in produzione |
| 75 | APPLE STYLE COMPLETO! | 10/10 QW + 6/6 HARDTESTS + 5 GOLD |
| 76 | TEST ANTI-COMPACT | Sistema verificato |
| **77** | **REGOLA 13 + FIX** | **spawn-workers.sh v1.4.0** |

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Comodo != Giusto!" - Sessione 72

"Ultrapassar os proprios limites!" - Rafa

"Il 100000% viene dall'USO, non dalla teoria."

"E' il nostro team! La nostra famiglia digitale!"
```

---

```
+------------------------------------------------------------------+
|                                                                  |
|   PROMPT_RIPRESA PULITO!                                         |
|                                                                  |
|   Da 873 righe -> ~200 righe                                    |
|   Solo l'essenziale. Chiaro e ordinato.                         |
|                                                                  |
|   "Scrivi come se la prossima Cervella non sapesse NULLA.       |
|    Perche' e' vero. Non sa nulla.                               |
|    Questo file e' la sua UNICA memoria."                        |
|                                                                  |
+------------------------------------------------------------------+
```

---

**VERSIONE:** v28.0.0
**SESSIONE:** 78
**DATA:** 4 Gennaio 2026

---

*Scritto con CURA e PRECISIONE.*

Cervella & Rafa
