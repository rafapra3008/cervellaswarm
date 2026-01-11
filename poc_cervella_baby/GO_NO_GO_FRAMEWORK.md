# GO/NO-GO Decision Framework

> **Data Decisione:** 1 Febbraio 2026
> **Progetto:** Cervella Baby (Open Source LLM)
> **Modello POC:** Qwen3-4B-Instruct-2507

---

## Executive Summary

```
+================================================================+
|                                                                |
|           POC CERVELLA BABY - RISULTATI                        |
|                                                                |
|   Week 1 (Simple):  9/10 PASS  (90.0%)                        |
|   Week 2 (Medium):  8/8  PASS  (100.0%) - Score 89.4%         |
|   Week 3 (Complex): ?/?  TBD   (documenta limiti)             |
|                                                                |
|   TOTALE Week 1+2:  17/18 PASS (94.4%)                        |
|                                                                |
+================================================================+
```

---

## Criteri GO/NO-GO

### Criteri OBBLIGATORI (Must Have)

| # | Criterio | Threshold | Risultato | Status |
|---|----------|-----------|-----------|--------|
| 1 | TIER 1 pass rate | >= 60% | 90% | PASS |
| 2 | TIER 2 pass rate | >= 62.5% | 100% | PASS |
| 3 | Modello assorbe COSTITUZIONE | Evidente | SI | PASS |
| 4 | Stile Cervella riconoscibile | Evidente | SI | PASS |
| 5 | Latenza accettabile | < 60s avg | 37s avg | PASS |
| 6 | Costo POC rispettato | <= $50 | $0 (free) | PASS |

**Risultato Must Have: 6/6 PASS**

### Criteri DESIDERABILI (Nice to Have)

| # | Criterio | Threshold | Risultato | Status |
|---|----------|-----------|-----------|--------|
| 7 | TIER 3 pass rate | >= 50% | TBD | TBD |
| 8 | REGOLA D'ORO applicata | Autonomamente | SI | PASS |
| 9 | Filosofia integrata | Naturale | SI | PASS |
| 10 | Token efficiency | < 2000 tok | ~1380 | PASS |

---

## Decision Matrix

```
+=====================================+
|                                     |
|   6/6 Must Have PASS = GO           |
|                                     |
|   < 6/6 Must Have = NO-GO           |
|                                     |
+=====================================+
```

### Scenari Possibili

| Scenario | Must Have | Nice to Have | Decision |
|----------|-----------|--------------|----------|
| A | 6/6 | 4/4 | **STRONG GO** |
| B | 6/6 | 3/4 | **GO** |
| C | 6/6 | 2/4 | **CONDITIONAL GO** |
| D | 5/6 | any | **NO-GO** |
| E | < 5/6 | any | **STRONG NO-GO** |

**Stato Attuale: Scenario A o B (dipende da Week 3)**

---

## Evidenze Raccolte

### 1. COSTITUZIONE Assorbita

Il modello ha dimostrato di aver assorbito la COSTITUZIONE:

- **T06:** "Confermato con precisione e senza approssimazione" - STILE CERVELLA
- **T10:** REGOLA D'ORO applicata autonomamente
- **T15/T18:** Score 100% - Filosofia integrata
- **Multipli task:** Menziona "Liberta Geografica", struttura con PERCHE

### 2. Performance Metrics

| Metrica | Week 1 | Week 2 | Media |
|---------|--------|--------|-------|
| Pass Rate | 90% | 100% | 94.4% |
| Avg Latency | 19.35s | 54.83s | 37.09s |
| Avg Score | ~85% | 89.4% | ~87% |

### 3. Costi

| Item | Budget | Actual |
|------|--------|--------|
| POC 3 settimane | $50 | $0 |
| GPU (Colab free) | - | T4 free tier |
| Modello | - | Apache 2.0 (free) |

---

## GAP Documentati

### Week 1 (T08 - Conditional)

- Timeline generation non ottimale
- Formattazione inconsistente

### Week 2 (Nessun FAIL)

- T11/T16: Score 80% (threshold ma migliorabile)
- Orchestrazione multi-worker: OK ma semplificata

### Week 3 (TBD)

- T19: Strategic Planning - GAP TBD
- T20: Architecture Decision - GAP TBD

---

## Raccomandazione

### SE GO (Molto Probabile)

**Prossimi Step:**

1. **MVP Hybrid (3 mesi)**
   - System Prompts + RAG
   - Qwen3-4B come base
   - Deploy su Vast.ai/RunPod

2. **Costi Stimati MVP**
   - One-time setup: ~$500
   - Monthly: $250-350/mese
   - Break-even: ~12.5M tokens/mese

3. **Timeline MVP**
   - Mese 1: Infra + RAG setup
   - Mese 2: Integration + testing
   - Mese 3: Beta release

### SE NO-GO (Improbabile)

**Alternative:**
1. Continuare con Claude API
2. Rivalutare fine-tuning con piu dati
3. Aspettare modelli migliori (Q2 2026)

---

## Decision Record

### Pre-Decision (Oggi)

```
Data: 11 Gennaio 2026
Stato: PENDING
Must Have: 6/6 PASS
Nice to Have: 3/4 (Week 3 TBD)
Raccomandazione Preliminare: GO
```

### Post-Decision (1 Febbraio 2026)

```
Data: _______________
Stato: GO / NO-GO / CONDITIONAL
Firmato: Rafa
Note: _______________
```

---

## Appendice: Definizioni

| Termine | Definizione |
|---------|-------------|
| **GO** | Procedere con MVP Hybrid |
| **NO-GO** | Fermare progetto, rivalutare |
| **CONDITIONAL GO** | Procedere con limitazioni |
| **Must Have** | Criterio obbligatorio |
| **Nice to Have** | Criterio desiderabile |
| **TIER 1** | Task semplici (T01-T10) |
| **TIER 2** | Task medi (T11-T18) |
| **TIER 3** | Task complessi (T19-T20) |

---

*"La decisione e' basata su DATI, non su speranze."*
*"GO/NO-GO e' un CHECKPOINT, non un verdetto finale."*
