# TECHNICAL DEBT REPORT - CervellaSwarm
**Data:** 04 Febbraio 2026  
**Analista:** Cervella Ingegnera  
**Health Score:** 5/10 - ⚠️ MEDIO/CRITICO

---

## EXECUTIVE SUMMARY

**Status:** Refactoring necessario su alcune funzioni CRITICHE  
**Issues Totali:** 196 (esclusi docs e file generati)  

### Breakdown per Severità
- 🔴 **CRITICO:** 42 (file >1000 righe o funzioni >100 righe)
- 🟠 **ALTO:** 154 (file >500 righe o funzioni >50 righe)  
- 🟡 **MEDIO:** 2 (TODO/FIXME nel codice)

---

## TOP 5 ISSUES CRITICI

### 1. 🔴 generate_retro() - 450 righe
**File:** `scripts/memory/weekly_retro.py:142`  
**Problema:** Funzione troppo lunga, difficile manutenzione  
**Azione:** Estrai helper functions (target: <100 righe)

### 2. 🔴 full_name() - 416 righe  
**File:** `cervella/agents/loader.py:26`  
**Problema:** Logica complessa tutta in una funzione  
**Azione:** Split in multiple funzioni

### 3. 🔴 create_test_db() - 202 righe
**File:** `archived/docker/exporter/test_exporter.py:14`  
**Problema:** Setup DB troppo complesso  
**Azione:** Estrai steps separati

### 4. 🔴 cleanup_old_records() - 192 righe
**File:** `test-hardtests/src/api/cleanup.py:133`  
**Problema:** Logica pulizia non modulare  
**Azione:** Split per tipo di record

### 5. 🔴 cmd_retro() - 184 righe
**File:** `scripts/memory/analytics.py:590`  
**Problema:** Command handler troppo grande  
**Azione:** Estrai sub-commands

---

## ARCHITETTURA packages/

### ✅ Punti di Forza
- Struttura directory CONSISTENTE (`src/`, `dist/`, `test/`)
- Buona separazione: `api`, `cli`, `core`, `mcp-server`
- Tutti i package usano `@cervellaswarm/core` ✓

### ⚠️ Inconsistenze
1. **CLI in JavaScript** (unico package non TypeScript)
   - `api/`: TypeScript ✓
   - `cli/`: JavaScript ✗
   - `core/`: TypeScript ✓
   - `mcp-server/`: TypeScript ✓
   
   **Raccomandazione:** Migrare CLI a TypeScript per coerenza

---

## FILE DUPLICATI

**Totale:** 15 gruppi (severità BASSA)

### Top 3
1. `scripts/__init__.py`, `scripts/tools/__init__.py`, `scripts/utils/__init__.py` (3 identici)
2. `scripts/sncp/smart-search.py`, `scripts/sncp/smart_search.py` (2 identici)
3. `.pytest_cache/README.md` (4 identici in varie dir)

**Azione:** Consolidare (non urgente)

---

## RACCOMANDAZIONI PRIORITIZZATE

### 🔴 PRIORITÀ 1 (Questa settimana)
- [ ] Refactor `generate_retro()` (450 righe → <100)
- [ ] Refactor `full_name()` (416 righe → <100)
- [ ] Analizzare se `archived/` può essere rimosso

### 🟠 PRIORITÀ 2 (Prossimo sprint)
- [ ] File grandi: `analytics.py` (847 righe), `weekly_retro.py` (673 righe)
- [ ] Valutare migrazione CLI a TypeScript
- [ ] Split test file grandi (`test_e2e_sncp_4.py` - 773 righe)

### 🟡 PRIORITÀ 3 (Backlog)
- [ ] Risolvi 2 TODO/FIXME nel codice
- [ ] Consolida file duplicati
- [ ] Code review settimanale per prevenire accumulo

---

## NOTE DOCUMENTAZIONE

**83 file .md > 1000 righe** - Questo è NORMALE per ricerche approfondite.  
NON richiede azione (a meno che non siano PROMPT_RIPRESA).

---

## PROSSIMI STEP

1. **ORA:** Identifica quale funzione CRITICA refactorare prima (propongo `generate_retro`)
2. **DOMANI:** Assegna task a cervella-backend per il refactor
3. **QUESTA SETTIMANA:** Risolvi top 3 CRITICI
4. **PROSSIMO SPRINT:** Pianifica migrazione CLI a TypeScript

---

**Report dettagliato:** `reports/engineer_report_20260204_163701.json`  
**Script usato:** `scripts/engineer/analyze_codebase.py`

