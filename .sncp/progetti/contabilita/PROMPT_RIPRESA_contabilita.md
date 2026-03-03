# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 3 Marzo 2026 - Sessione 268 (SPRING-019 Step 1-2 backend + audit piano)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

## Quick Status S268

| Cosa | Stato |
|------|-------|
| **Produzione MAIN** | **V3 LIVE v1.16.1 su contabilitafamigliapra.it** |
| **SPRING-019** | **IN PROGRESS - Step 1-2 DONE, Step 3-9 TODO** |
| **Test** | **2335 portale + 362 agent + 298 verify = 2995 totali** |
| **MAPPA** | **`docs/MAPPA_MIGLIORAMENTI_S262.md` - 20 item (13 TODO, 1 IN_PROGRESS, 1 BLOCCATO, 5 DONE)** |
| **Piano** | **`docs/PLAN_SPRING_019_MATCHING_MANUALE.md` - aggiornato con decisioni S268** |

## Cosa Ha Fatto S268

### Audit piano SPRING-019 (2 Cervelle in parallelo)
- **Guardiana Qualita: 9.1/10** APPROVED w/riserve
  - F1 P1: specifica `conferma_annullamento_manuale()` - RISOLTO (decisione architetturale presa)
  - F2 P1: "Segna Parziale" non definito - RISOLTO (caparra resta attiva, solo RES collegata)
  - F7 P2: formato response cambiato - RISOLTO (backward compat con campo `coppie`)
  - F13 P3: `event-delegation.js` mancava dalla lista file - AGGIUNTO
  - 5 P2 + 6 P3 documentati nel piano (sezione 4b)
- **Guardiana Ops: 8.5/10** APPROVED con condizioni
  - GO-S019-001 P2: caparra annullata prima di SPRING - RISOLTO (per parziali la caparra resta attiva)
  - GO-S019-003 P3: stato DB per parziali - RISOLTO (decisione Rafa: caparra resta attiva)
  - Deploy: 6 file VM, singolo batch, snapshot obbligatorio, ZERO impatto SPRING pipeline

### Decisione architetturale chiave (confermata da Rafa)
**Due percorsi per annullamento manuale:**
1. **Annullamento completo** (|importo| uguali): caparra → annullata, RES → ref_id (come esistente, senza vincolo nome)
2. **Collegamento parziale** (importi diversi): caparra RESTA ATTIVA, solo RES → ref_id. Perche: i 975 EUR residui devono ancora matchare un GIR.

### Step 1: extract_booking_info() - DONE
- Funzione statica in `TransactionsMixin` per parsing nome caparra
- Regex: `^(NL|HP|SHE)\s+(\d+)\s` -> hotel, booking_id, guest_name, circuito
- **16 test PASS** (standard NL/SHE/HP, No Show, eccezioni SHE, dati reali)
- File: `backend/database/transactions.py` riga 1359

### Step 2: get_coppie_annullamento() esteso - DONE
- Ritorna Dict con 4 chiavi: `exact`, `suggested`, `orphans`, `coppie` (backward compat)
- PASS 1: match esatto nome+importo (come SPRING-018)
- PASS 2: match per booking ID (LIKE query: `NL 6667 %`)
- `_build_orphan_dict()` helper per RES senza match
- Router aggiornato: response include `exact/suggested/orphans/count_suggested/count_orphans`
- **7 nuovi test** (booking ID match, parziale, metodo diverso, orphan, priorita, mix)
- **57/57 test PASS** (tutti annullamento + SPRING-018 + SPRING-019, zero regressioni)
- File: `backend/database/transactions.py` + `backend/routers/transactions.py`

## Prossimi Step

### PRIORITA #1: SPRING-019 Implementazione (Step 3-9 restanti, ~11h)
Piano dettagliato in `docs/PLAN_SPRING_019_MATCHING_MANUALE.md` (sezione 4b aggiornata S268).

| Step | Cosa | Stato |
|------|------|:-----:|
| 1 | `extract_booking_info()` + 16 test | **DONE S268** |
| 2 | `get_coppie_annullamento()` esteso + 7 test + router | **DONE S268** |
| 3 | Endpoint `cerca-candidati` + test | TODO |
| 4 | `conferma_annullamento_manuale()` + `ripristina_collegamento()` + endpoint + test | TODO |
| 5 | Frontend: pannello esteso (sezione "da collegare") | TODO |
| 6 | Frontend: espansione inline sotto RES orfana | TODO |
| 7 | Frontend: ricerca caparra + collegamento | TODO |
| 8 | CSS + dark mode + accessibilita + event-delegation.js | TODO |
| 9 | Test integrazione + audit Guardiana | TODO |

**Prossimo step: Step 3** (endpoint cerca-candidati). Backend-first, frontend dopo.

### File da deployare VM (quando tutto DONE):
1. `backend/database/transactions.py`
2. `backend/routers/transactions.py`
3. `frontend/js/annullamenti.js`
4. `frontend/js/data.js`
5. `frontend/js/event-delegation.js`
6. `frontend/css/style.css`

### Dopo SPRING-019
1. **QC-004** (P2, 2-3h): test per telegram_notifier e scheduler
2. **AGENT-005** (P3, 30 min): pulizia file duplicati/vecchi sui PC hotel
3. **MON-003~005** (P3): backup DB audit, pipeline 0-doc, scheduler HC.io

## Bloccato

1. **SPRING-014** HP attivazione - accordo DIAMANTE Sig. Sergio

## Lezioni Apprese (Sessione 268)

### Cosa ha funzionato bene
- **Audit piano PRIMA di implementare**: 2 Guardiane in parallelo, 2 P1 trovati e risolti subito. Senza audit, avremmo implementato "Segna Parziale" senza sapere cosa fa nel DB.
- **Decisione architetturale chiara**: Due percorsi (completo vs parziale) con logica contabile chiara. Rafa ha confermato immediatamente.
- **Step 1+2 backend puliti**: 57/57 test, zero regressioni, backward compat mantenuto.

### Pattern candidato
- **Audit piano + decisione architetturale PRIMA del coding**: Guardiana trova gap (F1+F2), Regina propone soluzione, Rafa conferma, poi si implementa. Previene rifacimenti. 6a evidenza dopo S228.cv, S229, S230, S265, S266, S268. PROMUOVERE.

---

*"Lavoriamo in pace! Senza casino! Dipende da noi!"*
