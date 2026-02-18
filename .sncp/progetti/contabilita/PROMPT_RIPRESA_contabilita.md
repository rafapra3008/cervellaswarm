# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 19 Febbraio 2026 - Sessione 81
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)

---

## Stato Attuale - FASE B Studio Trasformazione COMPLETATA

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA, zero modifiche) |
| **Lab v2 VM** | v1.13.0 LIVE su lab.contabilitafamigliapra.it (HTTPS, DB v10) |
| **Lab v2 locale** | INTOCCATO, 1079/1079 PASS, branch lab-v2, porta 8001 |
| **Lab V3 locale** | branch lab-v3, porta 8003, Docker healthy, 1079/1079 PASS |
| **Prerequisiti NL** | 4/4 PASS (admin, HTTPS Google, HTTPS sito, V3 endpoint) |
| **FASE B** | COMPLETATA - Studio Trasformazione (mappatura + architettura) |

---

## Sessione 81 - FASE B Studio Trasformazione

### Step 4: Mappatura Formati Ericsoft -> Portale (Guardiana 9.2/10)

Documento completo: `docs/V3_FASE_B_STUDIO_TRASFORMAZIONE.md` (370 righe, 12 sezioni)

Mappatura copre:
- **6 tipi movimento**: CAP->caparra, INC->gir, RES->caparra negativa, CAPAT/RAC->skip, CAP-MR->caparra
- **13 codici pagamento NL**: BK->MASTERCARD/BOOKING, CON->CONTANTI, POS->POS, BONC->BONIFICO Cortina, BONU->BONIFICO Unicredit, U100V->VISA/Unicredit100, U100M->MASTERCARD/Unicredit100, VOU->VOUCHER, etc.
- **Conversioni date**: ISO (2026-01-24) -> DDMMYYYY (24012026) e DD/MM/YYYY (24/01/2026)
- **Nome ospite**: "{PORTAL} {SCHEDA_ID} {COGNOME} {NOME} - {CIRCUITO}"
- **Stagione**: calcolata da check_in (CAP/RES) o data_movimento (INC)
- **Casi speciali**: multi-ospite, soft-delete, INC 2 dettagli, CAP senza nome, pagamenti sconosciuti

P2 fixati: totale TEXT (non REAL), checkout_date aggiunto, nota ericsoft_transformer.py NUOVO modulo

### Step 5: Decisione Architettura (Guardiana 9.0/10)

**3 opzioni valutate, Option C SCELTA:**

| Opzione | Verdict |
|---------|---------|
| A: Transform & Insert (no source) | SCARTATA - confronto impossibile |
| B: Tabelle separate | SCARTATA - troppo costosa (DRY violation) |
| **C: Source column + ericsoft_ref_id** | **SCELTA** - confronto, zero duplicazione, transizione pulita |

Colonne nuove:
- `source TEXT DEFAULT 'pdf'` su caparra + gir (valori: 'pdf', 'ericsoft', 'manual', 'merged')
- `ericsoft_ref_id INTEGER` su caparra + gir (FK verso movimenti_ericsoft)

P2 fixati: totale normalizzazione, 3 INSERT point mancanti aggiunti al piano

---

## Piano FASE C - Implementazione (7 step)

1. **Migration v12**: source + ericsoft_ref_id + UNIQUE con source + indici
2. **ericsoft_transformer.py** (NUOVO): lookup pagamento, date ISO->portale, nome, stagione
3. **EricsoftMixin.ingest_to_portale()**: trasforma + inserisce con source='ericsoft'
4. **add_transactions()**: source='pdf' (retrocompatibile)
5. **create_transaction()**: source='manual'
6. **merge_transactions()**: eredita source
7. **find_duplicates()**: source nel GROUP BY

### File da modificare

| File | Cosa |
|------|------|
| `backend/migrations.py` | v12: colonne + UNIQUE + indici |
| `backend/processors/ericsoft_transformer.py` | NUOVO modulo |
| `backend/database/ericsoft.py` | ingest_to_portale() |
| `backend/database/transactions.py` | source in tutti INSERT |
| `backend/database/core.py` | UNIQUE update |

---

## Subroadmap V3 - Ericsoft -> Portale

| Fase | Step | Cosa | Status |
|------|------|------|--------|
| **A** | 1-3 | Setup Lab V3 locale | **COMPLETATA S80** |
| **B** | 4-5 | Studio Trasformazione | **COMPLETATA S81** |
| **C** | 6-8 | Transformer + Migration v12 + Test | PROSSIMA |
| **D** | 9-11 | Agent Python + Delta sync + Test reali NL | PENDING |
| **E** | 12-14 | Deploy VM + Agent su NL + E2E | PENDING |
| **F** | 15-16 | Confronto Ericsoft vs PDF + Decisione | PENDING |

---

## 4 ambienti locali

| Porta | Ambiente | Branch | Status |
|-------|----------|--------|--------|
| 8000 | Produzione locale | main (baked) | healthy |
| 8001 | Lab v2 | lab-v2 (mount) | healthy, INTOCCATO |
| 8003 | Lab V3 | lab-v3 (mount) | healthy |
| VM:8000 | Produzione LIVE | main | INTATTA |
| VM:8001 | Lab v2 VM | lab-v2 | LIVE |

---

## Decisioni Rafa (S80, confermato S81)

- **Strategia**: Aggiungere Ericsoft al portale gradualmente, poi decidere cosa tenere
- **Ambiente**: Lab V3 SEPARATO (lab-v2 intoccato)
- **Approccio**: NL prima, HP+SHE dopo
- **Architettura**: Option C (source column) - confronto PDF vs Ericsoft

---

*"Ultrapassar os proprios limites!" - FASE B completata, la strada verso FASE C e' tracciata!*
