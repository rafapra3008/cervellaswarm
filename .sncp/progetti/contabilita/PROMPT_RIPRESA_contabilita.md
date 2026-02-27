# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 27 Febbraio 2026 - Sessione 194
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S194 (Step 13+14+15b+16a+17a + P3 FATTI)

| Cosa | Stato |
|------|-------|
| **Produzione V2** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | main.py v1.15.0 + pdf_parser v1.14.1 + 8 file frontend S188 |
| **Agent NL/SHE/HP** | v2.1.0 LIVE + reconcile v1.1.0 DEPLOYATO S184 |
| **HC.io** | **11 check** - TUTTI VERDI S184 |
| **Test portale** | **1559 PASS** (lab-v3) |
| **Test agent** | 362 PASS |
| **Lab-v2** | INTATTO, frozen da S87 |
| **Subroadmap audit** | **21/35 step** (15 pre-S194 + 6 S194) |
| **Guardiana score** | 14 audit, media 9.5+/10 |

---

## S194 - Cosa abbiamo fatto

### Valutazione completa piano (35 step) - 4 falsi positivi eliminati
Prima di codificare: lettura di TUTTI i file coinvolti, verifica ogni finding.
- **ELIMINATI**: Content-Type annullamenti (apiFetch gestisce), body 3x (corretto), will-change (non esiste), .notification 3x (dark mode variant = corretto)
- **RICLASSIFICATI**: ESC handler da P1 a P2 (cleanup esiste), displayData guard da P2 a P3

### Step 13: ESC handler + POS ESC (Guardiana 9.5/10)
- **13a**: Guard anti-leak contabilizzata-check.js - rimuovi vecchio handler prima di aggiungerne uno nuovo. Rimossa auto-rimozione ridondante (closeContabilizzataModal gestisce)
- **13b**: **BUG SERIO pos.js** - ESC non cancellava! `cell.textContent = currentValue` triggerava blur -> commit(). Fix: `input.removeEventListener('blur', commit)` PRIMA di textContent
- **File**: contabilizzata-check.js, pos.js

### Step 14: ESC blur editing.js + 3 guard (Guardiana 9.6/10)
- **14a P2**: **STESSO BUG di pos.js** trovato dalla Guardiana in editing.js! `cancelEdit()` non disarmava blur -> commitEdit() su ESC. Fix: `blurHandler` estratto + removeEventListener in cancelEdit()
- **14b P3**: Guard `typeof displayData === 'function'` + `typeof updateFiltersStuckState` in app-init.js
- **14c P3**: Guard `newKey.includes('_')` prima di split('_') in editing.js
- **14d P3**: Guard `!window.closedSeasons ||` prima di .size in seasons.js
- **File**: editing.js, app-init.js, seasons.js

### Step 15b+16a+17a: CSS fix (Guardiana 9.5/10)
- **15b**: `rgba(var(--accent-primary), 0.1)` invalido -> `rgba(var(--accent-primary-rgb, 46,125,50), 0.1)`
- **16a**: `.badge-small color: var(--text-inverse)` -> `color: white` (coerenza con .badge)
- **17a**: `.btn-header-secondary` 2 definizioni sparse -> merge in una sola + hover
- **Extra**: Wizard fallback blu Tailwind `59,130,246` -> verde NL `46,125,50` (P2 trovato dalla Guardiana)
- **File**: style.css

### P3 completati
- **P3-1**: Dead CSS `body.editor-mode-active` rimosso (~18 righe, zero JS toggling confermato)
- **P3-4**: `parseDateDDMMYYYY` estratta in config.js (DRY: era in export.js + pos.js)
- **P3-6**: `exportPosToExcel` ora usa `getFilteredPosData()` (coerenza con renderPosTable)

---

## Progresso Subroadmap (21/35 step)

| Fase | Step | Cosa | Stato | Sessione |
|------|------|------|-------|----------|
| **1 P0 CRASH** | 1 | JS null-checks (3 file) | **FATTO 9.5/10** | S190 |
| **1 P0 CRASH** | 2 | BE save_pareggi commit+count | **FATTO 9.6/10** | S191 |
| **2 SECURITY P1** | 3 | IDOR POS (4 endpoint) | **FATTO 9.5/10** | S191 |
| **2 SECURITY P1** | 4 | 401 handler chain | **FATTO 9.5/10** | S192 |
| **3 JS P1** | 5 | Dead code data.js | **FATTO 9.5/10** | S192 |
| **3 JS P1** | 6 | Race condition ticket.js | **FATTO 9.5/10** | S192 |
| **4 CSS P1** | 7-9 | Duplicati + fallback CSS | **FATTO 9.5/10** | S192 |
| **4b CSS** | 7b | 4 classi dead CSS rimosse | **FATTO 9.5/10** | S193 |
| **4b CSS** | 8b | 3 duplicati CSS unificati | **FATTO 9.5/10** | S193 |
| **5 BE P1** | 10-11 | file size limit + init_db | **FATTO 9.5/10** | S192 |
| **5b BE** | 11b | Cap limit admin.py | **FATTO 9.7/10** | S193 |
| **6 JS P2** | 12 | Sort POS + double fetch | **FATTO 9.6/10** | S193 |
| **6 JS P2** | 13 | ESC handler + POS ESC blur | **FATTO 9.5/10** | S194 |
| **6 JS P2** | 14 | ESC blur editing.js + 3 guard | **FATTO 9.6/10** | S194 |
| **7 CSS P2** | 15b | rgba(var()) invalido (1 caso) | **FATTO 9.5/10** | S194 |
| **7 CSS P2** | 16a | .badge-small color coerenza | **FATTO 9.5/10** | S194 |
| **7 CSS P2** | 17a | .btn-header-secondary merge | **FATTO 9.5/10** | S194 |
| **P3** | P3-1 | Dead CSS editor-mode-active | **FATTO** | S194 |
| **P3** | P3-4 | parseDateDDMMYYYY DRY | **FATTO** | S194 |
| **P3** | P3-6 | exportPosToExcel filtro stagione | **FATTO** | S194 |
| **Extra** | - | Wizard fallback blu -> verde | **FATTO** | S194 |

### Step rimanenti (14/35)

| Step | Cosa | Sev | File |
|------|------|-----|------|
| **15a** | zoom:0.9 (delicato, potrebbe cambiare layout) | P2 | style.css |
| **18-22** | Backend P2 + Security P2 | P2 | vari |
| **23-35** | P3 vari (JS dead code, CSS print/responsive, BE robustezza) | P3 | vari |

### P3 in coda (9 finding da Guardiane S193-S194)
pareggi-fase4 inline cssText, refreshPareggiStatus return, TOCTOU pareggio (mitigato), parking if vuoto, editing.js catch+dead branch, export.js docstring+revoke, .editable 2x, 9 var `-rgb` senza definizione

---

## Mappa Deploy - 22 file da portare su VM V3

> DELTA rispetto alla VM V3 (ultimo sync S188, commit `160f7fc`)
> Verificato con `git diff --name-only 160f7fc..HEAD -- frontend/ backend/`

### Frontend (17 file)
| # | File | Sessione |
|---|------|----------|
| 1 | `frontend/css/style.css` | S189+S192+S193+S194 |
| 2 | `frontend/index.html` | S189 |
| 3 | `frontend/js/data.js` | S189 |
| 4 | `frontend/js/pareggi-core.js` | S189 |
| 5 | `frontend/js/pareggi-puzzle.js` | S189 |
| 6 | `frontend/js/pos.js` | S189+S194 |
| 7 | `frontend/js/tabs.js` | S189 |
| 8 | `frontend/js/ticket.js` | S189 |
| 9 | `frontend/js/app-init.js` | S190+S194 |
| 10 | `frontend/js/pareggi-parking.js` | S190 |
| 11 | `frontend/js/pareggi-fase4.js` | S190 |
| 12 | `frontend/js/config.js` | S192+S194 |
| 13 | `frontend/js/ui.js` | S192 |
| 14 | `frontend/js/export.js` | S193+S194 |
| 15 | `frontend/js/editing.js` | S194 |
| 16 | `frontend/js/contabilizzata-check.js` | S194 |
| 17 | `frontend/js/seasons.js` | S194 |

### Backend (5 file)
| # | File | Sessione |
|---|------|----------|
| 18 | `backend/database/pareggi.py` | S191 |
| 19 | `backend/routers/transactions.py` | S191 |
| 20 | `backend/routers/export.py` | S192 |
| 21 | `backend/database/core.py` | S192 |
| 22 | `backend/routers/admin.py` | S193 |

**Totale: 22 file** (17 frontend + 5 backend). Deploy DOPO completamento step P2 rimanenti.

---

## Lezioni Apprese (Sessione 194)

### Cosa ha funzionato bene
- **Verifica OGNI finding prima di implementare**: su 35 step, 4 erano falsi positivi. Risparmiato tempo e evitato fix inutili
- **Guardiana trova bug collaterali**: editing.js aveva lo STESSO bug di pos.js (ESC non cancellava). Trovato dalla Guardiana durante audit Step 13
- **Net negativo di righe = qualita'**: -18 righe net. Codice piu' pulito, meno dead code

### Cosa non ha funzionato
- Niente di grave. Il piano originale aveva 4 falsi positivi - la verifica preventiva li ha scoperti

### Pattern candidato
- **Verifica finding contro codice reale PRIMA di classificare**: Evidenza S173, S190, S194. PROMUOVERE.

*S194: 6 step + 3 P3 + 1 extra. 3 audit 9.5+. 21/35. "Ultrapassar os proprios limites!"*
