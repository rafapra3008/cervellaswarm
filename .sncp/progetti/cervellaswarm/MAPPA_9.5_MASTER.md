# MAPPA MASTER - CervellaSwarm verso 9.5

> **Data:** 14 Gennaio 2026 - Sessione 203 (AGGIORNATA!)
> **Obiettivo:** Portare TUTTI gli score a 9.5 minimo
> **Filosofia:** "Su carta != Reale" - Solo cose USATE contano!

---

## DASHBOARD SCORE

```
+================================================================+
|                                                                |
|   CERVELLASWARM - STATO REALE POST-SESSIONE 202                |
|                                                                |
|   SNCP (Memoria)      [########--]  8.0/10  -->  9.5  GAP 1.5  |
|   SISTEMA LOG         [########--]  7.5/10  -->  9.5  GAP 2.0  |
|   AGENTI (Cervelle)   [#########-]  8.5/10  -->  9.5  GAP 1.0  |
|   INFRASTRUTTURA      [#########-]  8.5/10  -->  9.5  GAP 1.0  |
|                                                                |
|   MEDIA ATTUALE:      7.8/10  (era 7.5)                        |
|   TARGET:             9.5/10                                   |
|   GAP:                1.7 punti                                |
|                                                                |
+================================================================+
```

### Progressi Sessione 202-203

```
+================================================================+
|   SESSIONE 202: SNCP + Alerting + JSON Schema                  |
|                                                                |
|   [x] 4 script SNCP automazione (TESTATI sessione 203!)        |
|   [x] AlertSystem completo (PARCHEGGIATO - pronto se serve)    |
|   [x] JSON schema 5 agenti (PARCHEGGIATO - completare se serve)|
|   [x] miracollo/stato.md compattato (576 -> 208 righe)         |
|                                                                |
|   COMMIT: 6868187 | PUSH: OK                                   |
+================================================================+
```

---

## REALE vs PARCHEGGIATO (Sessione 203)

```
+================================================================+
|                                                                |
|   "SU CARTA" != "REALE"                                        |
|   Solo cose USATE portano alla LIBERTA GEOGRAFICA!             |
|                                                                |
+================================================================+
```

### REALE (Lo usiamo ogni sessione)

| Cosa | Status | Come lo usiamo |
|------|--------|----------------|
| Script SNCP | ATTIVO | health-check inizio sessione |
| Compact-state | ATTIVO | Quando file > 300 righe |
| SwarmLogger | ATTIVO | Tutti i worker lo usano |
| 16 Agenti | ATTIVO | Spawn-workers quotidiano |

### PARCHEGGIATO (Pronto, ma non prioritario)

| Cosa | Perche parcheggiato | Quando riattivare |
|------|---------------------|-------------------|
| AlertSystem | Monitoriamo manualmente | Se troppe sessioni sfuggono |
| JSON Schema x16 | 5 bastano per ora | Se serve validazione |
| Dashboard real-time | Overkill per 1-2 sessioni/giorno | Se scale up |
| Slack notifier | Non usiamo Slack | Mai (o Telegram) |

### DA DECIDERE

| Cosa | Domanda |
|------|---------|
| Telegram alerting | Serve notifica fine worker? |
| RAG/Semantic search | Serve cercare in SNCP? |

---

## 1. SNCP (MEMORIA) - 8.0/10 --> 9.5

### Stato Attuale (Sessione 203)
- **Struttura:** OTTIMA (progetti separati, archivio mensile)
- **Automazione:** 4 SCRIPT FUNZIONANTI E TESTATI!
  - `health-check.sh` - Dashboard ASCII (score 90/100)
  - `pre-session-check.sh` - Verifica inizio sessione
  - `post-session-update.sh` - Checklist fine sessione
  - `compact-state.sh` - Compattazione automatica
- **oggi.md:** 253 righe (sotto controllo)
- **stato.md progetti:** Tutti < 300 righe

### Cosa Funziona REALE
| Cosa | Status | Testato |
|------|--------|---------|
| health-check.sh | ATTIVO | Sessione 203 |
| compact-state.sh | ATTIVO | miracollo 576->208 |
| Archivio backup | ATTIVO | .sncp/archivio/2026-01/ |

### Cosa Manca per 9.5
| Gap | Impatto | Azione |
|-----|---------|--------|
| Usare script ogni sessione | ALTO | Abitudine! |
| Worker output in SNCP | MEDIO | Template gia pronti |

### Roadmap Semplificata
```
Sprint 1-2: COMPLETATI (8.0)
Sprint 3: ADOZIONE - Usare ogni sessione     --> 8.5
Sprint 4: VERIFICA - Funziona davvero?       --> 9.0
Sprint 5: POLISH - Solo se serve             --> 9.5
```

---

## 2. SISTEMA LOG - 7.5/10 --> 9.5

### Stato Attuale (Sessione 203)
- **SwarmLogger v2.0.0:** ECCELLENTE con Distributed Tracing!
- **Log Rotation:** Cron ogni 3:00 (ATTIVO)
- **AlertSystem:** PRONTO ma PARCHEGGIATO
  - PatternDetector (keywords, spikes, stuck agents)
  - Notifiers (Console, File, Slack ready)

### Cosa Funziona REALE
| Cosa | Status | Note |
|------|--------|------|
| SwarmLogger | ATTIVO | Tutti worker lo usano |
| Log rotation | ATTIVO | Cron 3:00 |
| Database eventi | ATTIVO | ~4.6MB |

### PARCHEGGIATO (pronto se serve)
| Cosa | Perche | Riattivare quando |
|------|--------|-------------------|
| AlertSystem | Monitoriamo manualmente | Se perdiamo errori |
| Slack notifier | Non usiamo Slack | Mai |
| Dashboard SSE | Overkill | Se scale up |

### Cosa Manca per 9.5
| Gap | Impatto | Decisione |
|-----|---------|-----------|
| Alerting automatico | MEDIO | PARCHEGGIATO |
| Telegram notifiche | BASSO | DA DECIDERE |

### Roadmap Semplificata
```
Sprint 1-2: COMPLETATI (7.5)
Sprint 3: TELEGRAM? - Se serve notifiche     --> 8.0
Sprint 4: Solo se serve davvero              --> 9.0+
```

---

## 3. AGENTI (CERVELLE) - 8.5/10 --> 9.5

### Stato Attuale (Sessione 203)
- **16 agenti** tutti operativi e USATI quotidianamente
- **Gerarchia:** Regina + 3 Guardiane (Opus) + 12 Worker (Sonnet)
- **RUOLI_CHEAT_SHEET.md:** Chi fa cosa (chiaro!)
- **JSON Schema:** 5 agenti top hanno output_schema v1.1.0

### Cosa Funziona REALE
| Cosa | Status | Note |
|------|--------|------|
| 16 agenti | ATTIVI | Spawn-workers quotidiano |
| Gerarchia 3 livelli | ATTIVA | Regina delega sempre |
| SNCP integration | ATTIVA | Worker scrivono in .sncp |

### PARCHEGGIATO
| Cosa | Perche | Riattivare quando |
|------|--------|-------------------|
| JSON Schema x16 | 5 bastano | Se serve validazione strict |
| Orchestrazione parallela | Sequenziale funziona | Se bottleneck |

### Cosa Manca per 9.5
| Gap | Impatto | Decisione |
|-----|---------|-----------|
| JSON altri 11 agenti | BASSO | PARCHEGGIATO |
| Validazione output | BASSO | Solo se errori |

### Roadmap Semplificata
```
FASE 1-2: COMPLETATE (8.5)
FASE 3: USARE - Delegare sempre, mai edit diretti  --> 9.0
FASE 4: Solo se serve davvero                      --> 9.5
```

---

## 4. INFRASTRUTTURA - 8.5/10 --> 9.5

### Stato Attuale (AGGIORNATO)
- **Scripts:** 40+ tutti funzionanti
- **Database:** Attivo (4.6MB, 4158 eventi)
- **Test Suite:** 12/12 PASS
- **Task System:** 170+ task gestiti
- **Handoff:** 91 file attivi
- **Cron weekly_retro:** INSTALLATO!

### Problemi Rimanenti
| Problema | Impatto | Fix | Status |
|----------|---------|-----|--------|
| ~~Cron non installato~~ | ~~MEDIO~~ | ~~Setup weekly_retro~~ | DONE! |
| hooks/ directory mancante | BASSO | Decidere se serve | TODO |
| RAG non configurato | BASSO | Valutare Qdrant | TODO |
| Heartbeat log grande | BASSO | Schedule log-rotate | TODO |

---

## PRIORITA GLOBALE (Sessione 203 - RESET!)

### COMPLETATI (Sessioni 201-202)
- [x] **SNCP:** 4 script automazione TESTATI!
- [x] **SNCP:** Compaction miracollo (576->208)
- [x] **LOG:** AlertSystem pronto (PARCHEGGIATO)
- [x] **AGENTI:** JSON schema 5 top (PARCHEGGIATO)

### FOCUS: 3 COSE REALI

```
+================================================================+
|                                                                |
|   INVECE DI AGGIUNGERE "SU CARTA"...                           |
|   USIAMO QUELLO CHE ABBIAMO!                                   |
|                                                                |
|   1. health-check.sh ogni INIZIO sessione                      |
|   2. compact-state.sh quando file > 300 righe                  |
|   3. Delegare SEMPRE (mai edit diretti Regina)                 |
|                                                                |
+================================================================+
```

### PARCHEGGIATO (pronto se serve)
- AlertSystem automatico
- JSON Schema altri 11 agenti
- Dashboard real-time SSE
- Semantic search ChromaDB
- RAG Qdrant

### DA DECIDERE (con Rafa)
- Telegram notifiche fine worker?
- Serve altro per 9.5 o basta USARE?

---

## LA VERITA SUL 9.5

```
+================================================================+
|                                                                |
|   COME ARRIVIAMO A 9.5?                                        |
|                                                                |
|   NON aggiungendo piu "su carta"!                              |
|   MA usando quello che abbiamo OGNI GIORNO!                    |
|                                                                |
|   SNCP 8.0 -> 9.5:  Usare script ogni sessione                 |
|   LOG 7.5 -> 9.5:   Gia funziona, solo decidere Telegram       |
|   AGENTI 8.5 -> 9.5: Delegare sempre, zero edit diretti        |
|   INFRA 8.5 -> 9.5: Gia funziona!                              |
|                                                                |
|   Il 9.5 non e FARE DI PIU.                                    |
|   Il 9.5 e USARE BENE quello che c'e!                          |
|                                                                |
+================================================================+
```

---

## PROSSIMO STEP (Sessione 203)

```
+================================================================+
|                                                                |
|   ZERO NUOVE FEATURE!                                          |
|                                                                |
|   Solo 3 abitudini:                                            |
|   1. health-check.sh a INIZIO sessione                         |
|   2. compact-state.sh se file > 300 righe                      |
|   3. Delegare SEMPRE ai worker                                 |
|                                                                |
|   DA DECIDERE con Rafa:                                        |
|   - Telegram notifiche? (si/no)                                |
|   - Serve altro? (probabilmente no!)                           |
|                                                                |
+================================================================+
```

---

*"Su carta != Reale"*
*"Solo cose USATE portano alla LIBERTA GEOGRAFICA!"*
*"Un po' ogni giorno fino al 100000%!"*

**Sessione 203 - 14 Gennaio 2026**
