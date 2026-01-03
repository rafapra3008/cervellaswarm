# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 3 Gennaio 2026 - Sessione 70 - STUDIO COMUNICAZIONE COMPLETATO!

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
|   FASE ATTUALE: FASE 9 - APPLE STYLE                            |
|   STATO: Studio COMPLETATO! Pronta per IMPLEMENTARE!            |
|                                                                  |
|   "Nulla e' complesso - solo non ancora studiato!"              |
|   E noi l'abbiamo STUDIATO!                                     |
|                                                                  |
+------------------------------------------------------------------+
```

---

## IL MOMENTO ATTUALE (Sessione 70)

```
+------------------------------------------------------------------+
|                                                                  |
|   STUDIO COMUNICAZIONE COMPLETATO!                              |
|                                                                  |
|   Abbiamo studiato TUTTO:                                        |
|   - 7 domande fondamentali RISPOSTE                             |
|   - 2000+ righe di documentazione consolidate                   |
|   - BLEND con STUDIO_APPLE_STYLE.md fatto                       |
|   - Pattern Apple Style integrati                               |
|                                                                  |
|   RISULTATO:                                                     |
|   docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md (870+ righe!)  |
|                                                                  |
|   PRONTO per implementare i 4 CRITICI!                          |
|                                                                  |
+------------------------------------------------------------------+
```

---

## FILO DEL DISCORSO (Sessione 70) - LEGGI BENE!

### Cosa e' Successo

1. **STUDIATO SISTEMA ESISTENTE**
   - Letto .swarm/ (struttura, flag files, task_manager.py)
   - Letto spawn-workers.sh (375 righe - LA MAGIA!)
   - Letto GUIDA_COMUNICAZIONE.md (729 righe)
   - Scoperto che avevamo GIA' molto di piu' di quanto pensavamo!

2. **TROVATO I 3 FILE TESORO**
   Rafa ha suggerito: "abbiamo fatto un file ottimo qualche sessione fa..."
   Trovati:
   - `docs/guide/GUIDA_COMPACT_PROTEZIONE.md` (109 righe)
   - `docs/studio/RICERCA_PROTEZIONE_COMPACT.md` (146 righe)
   - `docs/studio/STUDIO_MULTI_FINESTRA_COMUNICAZIONE.md` (401 righe!)

   Questi file avevano GIA' molte risposte!

3. **RISPOSTO ALLE 7 DOMANDE FONDAMENTALI**

   | # | Domanda | Risposta |
   |---|---------|----------|
   | 1 | Cosa deve sapere worker? | Template TASK completo |
   | 2 | Cosa torna alla Regina? | Template OUTPUT completo |
   | 3 | Se worker ha dubbi? | Template DUBBI (NUOVO!) |
   | 4 | Se Regina fa compact? | Pattern HANDOFF |
   | 5 | Se worker fa compact? | Template PARTIAL (NUOVO!) |
   | 6 | Come Guardiana verifica? | Flusso completo |
   | 7 | Come mantenere MOMENTUM? | AUTO-HANDOFF pattern |

4. **FATTO BLEND CON STUDIO_APPLE_STYLE.md**
   Integrati i pattern migliori:
   - Triple ACK (ACK_RECEIVED -> ACK_UNDERSTOOD -> ACK_COMPLETED)
   - Quality Gates (4 livelli con timing)
   - Circuit Breaker + Retry Backoff
   - Graceful Shutdown Sequence (7 step)
   - Dashboard ASCII
   - Escalation Matrix
   - 10 Quick Wins prioritizzati (~8 ore totali)

5. **CREATO STUDIO DEFINITIVO**
   `docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md` (870+ righe!)

   Questo file consolida TUTTO. E' IL RIFERIMENTO.

6. **CHECKPOINT PER SICUREZZA**
   Rafa: "io me preocupo di iniziare implementare e arrivare un compact.."
   L'ironia! Stavamo creando ANTI-COMPACT e rischiavamo compact!
   Quindi: CHECKPOINT prima di implementare.

---

## COSA DEVI FARE (PROSSIMO STEP)

```
+------------------------------------------------------------------+
|                                                                  |
|   IMPLEMENTARE I 4 CRITICI                                       |
|                                                                  |
|   1. Template DUBBI                                              |
|      File: .swarm/tasks/TEMPLATE_DUBBI.md                       |
|      Definito in: STUDIO_COMUNICAZIONE_DEFINITIVO.md            |
|                                                                  |
|   2. Template PARTIAL                                            |
|      File: .swarm/tasks/TEMPLATE_PARTIAL.md                     |
|      Per quando worker fa compact                                |
|                                                                  |
|   3. Spawn Guardiane                                             |
|      File: scripts/swarm/spawn-workers.sh                       |
|      Aggiungere: --guardiana-qualita, --guardiana-ops, etc.     |
|                                                                  |
|   4. Triple ACK flag files                                       |
|      .ack_received, .ack_understood, .done                      |
|                                                                  |
|   TEMPO STIMATO: ~2 ore                                          |
|                                                                  |
+------------------------------------------------------------------+
```

### DOPO i 4 Critici

5. Shutdown sequence script
6. Quality Gates checklist
7. Test con caso REALE (spawn finestre, crea task, verifica flusso)

---

## IL DOCUMENTO DI RIFERIMENTO

```
docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md (870+ righe!)

Contiene TUTTO:
- Le 7 domande con risposte complete
- Template per ogni scenario
- Pattern Apple Style integrati
- 10 Quick Wins prioritizzati
- Architettura completa
- Flusso con compact handling
```

**SE HAI DUBBI -> LEGGI QUEL FILE!**

---

## COSA ESISTE GIA (funziona!)

| Cosa | Status |
|------|--------|
| 16 Agents in ~/.claude/agents/ | FUNZIONANTE |
| Sistema Memoria SQLite | FUNZIONANTE |
| 10 Hooks globali | FUNZIONANTE |
| SWARM_RULES v1.4.0 | FUNZIONANTE |
| Pattern Catalog (3 pattern) | FUNZIONANTE |
| GUIDA_COMUNICAZIONE v2.0 | FUNZIONANTE |
| Flusso Guardiane (3 livelli) | TESTATO! |
| HARDTESTS Comunicazione (3/3) | PASSATI! |
| HARDTESTS Swarm V3 (4/4) | PASSATI! |
| spawn-workers.sh | LA MAGIA! |
| task_manager.py | FUNZIONANTE |
| .swarm/ struttura | FUNZIONANTE |

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

---

## FILE IMPORTANTI

| File | Cosa Contiene |
|------|---------------|
| `docs/studio/STUDIO_COMUNICAZIONE_DEFINITIVO.md` | **IL RIFERIMENTO!** 870+ righe |
| `docs/studio/STUDIO_APPLE_STYLE.md` | 8 Domande Sacre + Quick Wins |
| `NORD.md` | Dove siamo, prossimo obiettivo |
| `docs/roadmap/FASE_9_APPLE_STYLE.md` | ROADMAP completa FASE 9 |
| `.swarm/README.md` | Come funziona il sistema multi-finestra |
| `scripts/swarm/spawn-workers.sh` | LA MAGIA! Apre finestre worker |
| `SWARM_RULES.md` | Le 12 regole dello sciame |

---

## GIT

```
Branch:   main
Versione: v27.4.0
Stato:    FASE 9 - Studio completato, pronta per implementare
```

---

## LE NOSTRE FRASI

```
"Lavoriamo in pace! Senza casino! Dipende da noi!"

"Nulla e' complesso - solo non ancora studiato!"

"L'abbiamo STUDIATO! Ora IMPLEMENTIAMO!"

"L'ironia e' FORTISSIMA - stiamo creando ANTI-COMPACT e rischiamo compact!" - Rafa

"Fatto BENE > Fatto VELOCE"

"E' il nostro team! La nostra famiglia digitale!"
```

---

## LA STORIA (come siamo arrivati qui)

| Sessione | Cosa | Risultato |
|----------|------|-----------|
| 60 | LA SCOPERTA | N finestre = N contesti! |
| 61 | MVP Multi-Finestra | .swarm/ funzionante |
| 62 | CODE REVIEW | 8.5/10 OTTIMO! |
| 63 | INSIGHT CERVELLO | Studio neuroscientifico |
| 64 | HARDTESTS CREATI | 1256 righe di test |
| 65 | HARDTESTS PASSATI | 4/4 PASS! |
| 66 | LA MAGIA! | spawn-workers.sh |
| 67 | CODE REVIEW + ROADMAP | 9.0/10 + FASE 9! |
| 68 | SPRINT 9.1 RICERCA | 8 Domande RISPOSTE! |
| 69 | INSIGHT COMUNICAZIONE | Task tool vs Multi-finestra! |
| **70** | **STUDIO COMPLETATO!** | **BLEND fatto! 870+ righe!** |

---

```
+------------------------------------------------------------------+
|                                                                  |
|   CARA PROSSIMA CERVELLA                                         |
|                                                                  |
|   Lo studio e' FATTO.                                            |
|   Il documento di riferimento e' PRONTO.                        |
|   I pattern sono DEFINITI.                                       |
|                                                                  |
|   Ora implementa i 4 CRITICI:                                    |
|   1. Template DUBBI                                              |
|   2. Template PARTIAL                                            |
|   3. Spawn Guardiane                                             |
|   4. Triple ACK                                                  |
|                                                                  |
|   "L'abbiamo STUDIATO! Ora IMPLEMENTIAMO!"                      |
|                                                                  |
+------------------------------------------------------------------+
```

---

## PROMPT_RIPRESA 10000%!

```
+------------------------------------------------------------------+
|                                                                  |
|   Questo file e' scritto con CURA.                              |
|                                                                  |
|   La prossima Cervella non sa NULLA.                            |
|   Questo file e' la sua UNICA memoria.                          |
|                                                                  |
|   Per questo:                                                    |
|   - FILO DEL DISCORSO (perche', non solo cosa)                  |
|   - LE FRASI DI RAFA (le sue parole esatte!)                    |
|   - DECISIONI PRESE (cosa abbiamo scelto e perche')             |
|   - PROSSIMI STEP (cosa fare dopo)                              |
|   - FILE IMPORTANTI (dove trovare tutto)                        |
|                                                                  |
|   L'insight di questa sessione:                                  |
|   "L'ironia e' FORTISSIMA - stiamo creando ANTI-COMPACT         |
|    e rischiamo di perderlo per un compact!" - Rafa              |
|                                                                  |
|   Per questo abbiamo fatto CHECKPOINT prima di implementare!    |
|   Tutto salvato. Tutto pronto. La prossima Cervella continua.   |
|                                                                  |
|   "Non e' sempre come immaginiamo...                            |
|    ma alla fine e' il 100000%!"                                 |
|                                                                  |
+------------------------------------------------------------------+
```

---

*Scritto con CURA e PRECISIONE.*

*"Nulla e' complesso - solo non ancora studiato!"*

*E noi l'abbiamo STUDIATO!*

Cervella & Rafa

---

**VERSIONE:** v27.4.0
**SESSIONE:** 70
**DATA:** 3 Gennaio 2026
