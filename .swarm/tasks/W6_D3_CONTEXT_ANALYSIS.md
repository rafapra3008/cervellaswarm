# W6 Day 3 - Analisi --with-context Default

> **Data:** 20 Gennaio 2026 - Sessione 293
> **Task:** Decidere se --with-context deve essere default in spawn-workers

---

## BENCHMARK PERFORMANCE

| Scenario | Tempo |
|----------|-------|
| CON context (1500 token) | **2.37 secondi** |
| SENZA context | **0 secondi** |

**Overhead:** +2.37s per spawn con context abilitato.
**Target:** < 3 secondi = PASS

---

## ANALISI PER TIPO WORKER

| Worker | Modifica Codice | Beneficio | Raccomandazione |
|--------|-----------------|-----------|-----------------|
| backend | SI | ALTO | ON |
| frontend | SI | ALTO | ON |
| tester | SI (test) | MEDIO | ON |
| reviewer | SI (review) | ALTO | ON |
| ingegnera | SI (refactor) | ALTO | ON |
| security | SI (audit) | MEDIO | ON |
| architect | NO (piano) | ALTO | ON |
| guardiana-qualita | NO (verifica) | ALTO | ON |
| docs | NO | BASSO | OFF |
| researcher | NO | BASSO | OFF |
| scienziata | NO | BASSO | OFF |
| marketing | NO | BASSO | OFF |
| guardiana-ricerca | NO | BASSO | OFF |
| data | MAYBE (SQL) | MEDIO | MAYBE |
| devops | MAYBE (IaC) | MEDIO | MAYBE |
| guardiana-ops | NO | BASSO | OFF |

**Risultato:** 8 worker ON, 6 worker OFF, 2 MAYBE

---

## RACCOMANDAZIONE

### OPZIONE SCELTA: Auto-Context Selettivo

**NON abilitare di default per TUTTI.**
**Abilitare AUTOMATICAMENTE per worker code-aware.**

### Implementazione

```bash
# Lista worker che beneficiano dal context
AUTO_CONTEXT_WORKERS="backend frontend tester reviewer ingegnera security architect guardiana-qualita"

# In spawn_worker_headless():
# Se worker e' nella lista -> context ON automatico
# Altrimenti -> context OFF
# Override sempre possibile con --with-context / --no-context
```

### Comportamento Risultante

| Comando | Context |
|---------|---------|
| `spawn-workers --backend` | AUTO ON |
| `spawn-workers --researcher` | AUTO OFF |
| `spawn-workers --backend --no-context` | FORCE OFF |
| `spawn-workers --researcher --with-context` | FORCE ON |

---

## DECISIONE

**RACCOMANDAZIONE FINALE:** Implementare Auto-Context Selettivo

**Perche:**
1. Worker code-aware ottengono context senza flag manuale
2. Worker non-code risparmiano 2.4s per spawn
3. Override manuale sempre disponibile
4. Zero breaking change (default globale resta OFF)

**ATTESA APPROVAZIONE RAFA**

---

*W6 Day 3 - Cervella*
