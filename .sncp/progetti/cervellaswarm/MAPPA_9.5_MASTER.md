# MAPPA MASTER - CervellaSwarm verso 9.5

> **Data:** 14 Gennaio 2026 - Sessione 202 (AGGIORNATA!)
> **Obiettivo:** Portare TUTTI gli score a 9.5 minimo
> **Filosofia:** "Se documentiamo = facciamo!"

---

## DASHBOARD SCORE

```
+================================================================+
|                                                                |
|   CERVELLASWARM - STATO ATTUALE vs TARGET                      |
|                                                                |
|   SNCP (Memoria)      [########--]  7.5/10  -->  9.5  (+0.5!)  |
|   SISTEMA LOG         [#######---]  7.0/10  -->  9.5  (+1.0!)   |
|   AGENTI (Cervelle)   [########--]  8.2/10  -->  9.5  (+0.4!)  |
|   INFRASTRUTTURA      [#########-]  8.5/10  -->  9.5  (+0.5!)  |
|                                                                |
|   MEDIA ATTUALE:      7.5/10  (era 7.2)                        |
|   TARGET:             9.5/10                                   |
|   GAP:                2.0 punti (era 2.3)                      |
|                                                                |
+================================================================+
```

### Progressi Sessione 201

```
+================================================================+
|   QUICK WINS COMPLETATI!                                       |
|                                                                |
|   [x] oggi.md compaction      1078 -> 186 righe (-83%)         |
|   [x] Merge typo cartella     miracallook -> miracollook       |
|   [x] RUOLI_CHEAT_SHEET.md    Chi fa cosa (docs/)              |
|   [x] Cron weekly_retro       Ogni lunedi alle 8:00            |
|                                                                |
|   COMMIT: f09092c | PUSH: OK                                   |
+================================================================+
```

---

## 1. SNCP (MEMORIA) - 7.5/10 --> 9.5

### Stato Attuale (AGGIORNATO)
- **Struttura:** OTTIMA (progetti separati, archivio mensile)
- **Formato:** PERFETTO (Markdown + YAML frontmatter)
- **Pattern:** ALLINEATI con industry standard
- **oggi.md:** PULITO! (186 righe vs 1078)
- **Typo cartelle:** RISOLTO (miracollook unificato)

### Problemi Rimanenti
| Problema | Impatto | Fix | Status |
|----------|---------|-----|--------|
| ~~oggi.md = 950 righe~~ | ~~CRITICO~~ | ~~Compaction~~ | DONE! |
| ~~Typo miracallook~~ | ~~ALTO~~ | ~~Merge~~ | DONE! |
| 80% file obsoleti | ALTO | Automazione updates | TODO |
| Worker non usano SNCP | ALTO | Integrazione spawn | TODO |
| Zero visibility | MEDIO | Dashboard health | TODO |

### Roadmap 9.5 (4 Sprint rimanenti)
```
Sprint 1: File Size Control     COMPLETATO!  --> 7.5 DONE
Sprint 2: Automazione Base      8h   --> 9.0
Sprint 3: Adoption/Integration  6h   --> 9.2
Sprint 4: Dashboard/Monitoring  6h   --> 9.4
Sprint 5: Polish/Documentation  6h   --> 9.5
```

### Report Dettagliato
`.sncp/progetti/cervellaswarm/reports/STUDIO_SNCP_9.5.md`

---

## 2. SISTEMA LOG - 7.0/10 --> 9.5

### Stato Attuale (AGGIORNATO Sessione 201!)
- **SwarmLogger v2.0.0:** ECCELLENTE con Distributed Tracing!
  - trace_id, span_id, parent_span_id
  - Context manager span() per nesting
  - child_logger() per worker
  - get_trace() per debugging
- **Log Rotation:** Cron ogni 3:00 (46 worker logs puliti!)
- **Database:** BUONA base (4.6MB, 4158 eventi)
- **Heartbeat:** FUNZIONANTE

### Problemi Rimanenti
| Problema | Impatto | Fix | Status |
|----------|---------|-----|--------|
| ~~NO distributed tracing~~ | ~~CRITICO~~ | ~~trace_id, span_id~~ | DONE! |
| ~~Log rotation manuale~~ | ~~ALTO~~ | ~~Cron 3:00~~ | DONE! |
| NO alerting system | CRITICO | Pattern detector + Slack | NEXT! |
| Retention non definita | ALTO | ILM automation | TODO |
| Dashboard statico | ALTO | Real-time SSE | TODO |

### Roadmap 9.5 (3 Sprint rimanenti)
```
Sprint 1: Tracing + Rotation    COMPLETATO!  --> 7.0 DONE
Sprint 2: Alerting + Dashboard  4d   --> 8.0  <-- PROSSIMO
Sprint 3: Error types + PII     3d   --> 9.0
Sprint 4: Cost tracking + OTel  2d   --> 9.5
```

### Quick Win PROSSIMO
- [ ] Aggiungere trace_id a SwarmLogger
- [ ] Setup log-rotate.sh in cron (heartbeat grande)

---

## 3. AGENTI (CERVELLE) - 8.2/10 --> 9.5

### Stato Attuale (AGGIORNATO)
- **16 agenti** tutti operativi
- **Formato YAML:** ECCELLENTE (parseable, versionato)
- **Gerarchia Regina/Guardiane/Worker:** SOLIDA
- **SNCP integration:** OTTIMA
- **RUOLI_CHEAT_SHEET.md:** CREATO!

### Problemi Rimanenti
| Problema | Impatto | Fix | Status |
|----------|---------|-----|--------|
| ~~Researcher vs Scienziata~~ | ~~ALTO~~ | ~~Chiarire ruoli~~ | DONE! |
| ~~No CHEAT_SHEET~~ | ~~ALTO~~ | ~~Creare doc~~ | DONE! |
| Output testo libero | MEDIO | JSON schema validato | TODO |
| Solo sequential | MEDIO | Orchestrazione parallela | TODO |
| Protocolli duplicati | BASSO | Refactor condiviso | TODO |

### Roadmap 9.5 (3 FASI rimanenti)
```
FASE 1: Ruoli Cristallini       COMPLETATO!  --> 8.2 DONE
FASE 2: Comunicazione JSON      2 sprint  --> 9.0
FASE 3: Orchestrazione Avanzata 3 sprint  --> 9.3
FASE 4: Validazione Automatica  2 sprint  --> 9.5
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

## PRIORITA GLOBALE (AGGIORNATA Sessione 202)

### COMPLETATI (Sessione 201)
- [x] **SNCP:** Pulire oggi.md (1078-->186 righe)
- [x] **SNCP:** Merge miracallook typo
- [x] **AGENTI:** RUOLI_CHEAT_SHEET.md
- [x] **INFRA:** Cron weekly_retro
- [x] **LOG:** SwarmLogger v2.0.0 (trace_id, span_id, parent_span_id!)
- [x] **LOG:** Log rotation cron (ogni 3:00, 46 file puliti)

### P1 - ALTO (IN CORSO - Sessione 202)
1. **SNCP:** Automazione updates (Sprint 2) <-- IN CORSO
2. **LOG:** Basic alerting (Slack)
3. **AGENTI:** JSON manifests top 5

### P2 - MEDIO (prossimo mese)
6. **SNCP:** Dashboard health
7. **LOG:** Real-time dashboard
8. **AGENTI:** JSON schema output

### P3 - BASSO (quando c'e tempo)
9. **SNCP:** Semantic search (ChromaDB)
10. **LOG:** Cost tracking + OTel
11. **AGENTI:** Orchestrazione parallela
12. **INFRA:** RAG Qdrant

---

## EFFORT RIMANENTE

```
+================================================================+
|                                                                |
|   COMPLETATO:   ~6h (Quick Wins)                               |
|                                                                |
|   RIMANENTE:                                                   |
|   SNCP:      24h  (4 sprint rimanenti)                         |
|   LOG:       12d  (4 sprint)                                   |
|   AGENTI:    6-10 settimane (3 fasi rimanenti)                 |
|   INFRA:     2h   (quick fixes rimanenti)                      |
|                                                                |
|   TOTALE:    ~70-90 ore lavoro                                 |
|              (distribuito su 2-3 mesi)                          |
|                                                                |
+================================================================+
```

---

## PROSSIMO STEP (Sessione 202)

```
+================================================================+
|                                                                |
|   P1 IN CORSO: SNCP Sprint 2 - Automazione Base                |
|                                                                |
|   COSA: Scripts automazione SNCP                               |
|   - pre-session-check.sh (avviso se stato.md obsoleto)         |
|   - post-session-update.sh (prompt aggiornamento)              |
|   - health-check.sh (dashboard ASCII)                          |
|   - Worker templates con SNCP output                           |
|                                                                |
|   PERCHE: Score SNCP da 7.5 a 9.0 (automazione!)               |
|   EFFORT: ~4-6 ore                                             |
|                                                                |
+================================================================+
```

---

*"Il nostro sistema e la nostra anima, cuore, cervello"*
*"Se documentiamo = facciamo!"*
*"Non abbiamo fretta. Un po' ogni giorno fino al 100000%!"*

**Sessione 201 - 14 Gennaio 2026**
