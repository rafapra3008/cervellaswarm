# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 24 Febbraio 2026 - Sessione 143
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S143 FASE N.2 COMPLETATA

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | v3.contabilitafamigliapra.it LIVE |
| **3 Hotel Agent** | TUTTI v2.0.0 daily_closed (deployato S139). Fix N.2 locali, deploy in N.6 |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1413 portale** + **346 agent** = **1759 PASS** |
| **Round QA** | **100** (Guardiana S143: 9.5/10) |
| **FASE N.1** | COMPLETATA (S141-S142) - 4 step bug Rafa |
| **FASE N.2** | **COMPLETATA (S143)** - 5 step Agent Fix |
| **Subroadmap** | `docs/SUBROADMAP_S140_LUCIDATURA.md` (N.1+N.2 FATTE, 12 step rimanenti) |

---

## S143 - Cosa e' stato fatto (FASE N.2 - Agent Fix)

### Step 4: HC.io logica incompleta - COMPLETATO
- **Bug 1**: `all_invalid` -> return senza ping (falso alert dead man's switch)
- **Bug 2**: Errori parziali (inserted>0, errors>0) -> ping verde (problema mascherato)
- **Fix**: `ping_healthcheck()` accetta `signal=""` o `signal="/fail"`. 3 scenari:
  - `all_invalid` -> ping `/fail` (agent ha girato, dati invalidi)
  - Errori parziali -> ping `/fail` (qualcosa inserito, qualcosa fallito)
  - Tutti falliti -> NESSUN ping (dead man's switch alert)
- **File**: `agent/agent.py:215-220`, `agent/http_sender.py:158-183`

### Step 5: 429 rate limit + circuit breaker - COMPLETATO
- **Bug**: 429 (rate limit) contava come CB failure -> accumulo apriva CB 30 min
- **Fix**: Nuova `HTTPError429(retry_after)`. In `_request_with_retry`: sleep(Retry-After), poi retry. In agent.py: catch 429 SENZA `cb.record_failure()`
- **Dettagli**: Retry-After cappato a 60s, default 5s se header assente
- **File**: `agent/http_sender.py:49-53,195-207`, `agent/agent.py:279-282`

### Step 6: Watermark gap reconcile SHE/HP - COMPLETATO
- **Bug**: Check C3 usava `max_id_global` -> gap permanente per SHE/HP (ID alti: 21600+/24300+)
- **Fix**: Usa `max_id_in_window` (nella finestra temporale). Rimossa condizione `p_max_id > 0`
- **Summary**: ora include sia `watermark_ericsoft_global` che `watermark_ericsoft_window`
- **File**: `agent/reconcile_comparator.py:121-133`

### Step 7: Watermark multi-batch - COMPLETATO
- **Bug**: `max_inserted_id` avanzava solo su `inserted > 0`, ignorava duplicati (skipped)
- **Fix**: Avanza su `batch_processed > 0 AND batch_errors == 0` (inserted + skipped = OK)
- **Logica**: Duplicati gia' nel portale -> watermark DEVE avanzare (altrimenti re-invio perpetuo)
- **File**: `agent/agent.py:261-265`

### Step 8: Safety net full-sync - COMPLETATO
- **Bug**: VM down + no cache = watermark=0 = full sync 20K+ record senza alert
- **Fix 1**: Log CRITICAL + HC.io `/fail` quando watermark=0 per assenza VM+cache
- **Fix 2**: Safety net 90 giorni: se watermark=0 e nessun date_cutoff -> forza cutoff 90gg
- **File**: `agent/agent.py:117-125,148-154`

### Guardiana S143: 9.5/10 APPROVED (100esimo round QA!)

---

## Subroadmap "La Lucidatura" - Mappa Sessioni

| Fase | Cosa | Step | Status |
|------|------|------|--------|
| **N.1** | Bug Rafa + batch duplicati | 4 | **COMPLETATA S141-S142** |
| **N.2** | Agent Fix (affidabilita) | 5 | **COMPLETATA S143** |
| **N.3** | Backend Fix (robustezza) | 3 | PENDING - Prossima sessione |
| **N.4** | Frontend Fix (UX) | 3 | PENDING |
| **N.5** | Security Hardening | 3 | PENDING |
| **N.6** | Deploy VM + Guardiana | 3 | PENDING - DOPO tutti i fix |

**Dettagli completi**: `docs/SUBROADMAP_S140_LUCIDATURA.md`

---

## Prossimi Step (S144+)

### S144: FASE N.3 - Backend Fix (3 step)
- **Step 9**: cleanup_orphan_pareggi -> scheduler (non ogni GET)
- **Step 10**: pre_close_stats cross-stagione
- **Step 11**: health deep auth
- **File**: `backend/routers/transactions.py`, `backend/processors/pareggi_background.py`, `backend/routers/admin.py`

### S145: FASE N.4 - Frontend Fix (3 step)
- Step 12-14: _undoData, initAnnullamenti, NOLOCK importo=0

### S146-S147: FASI N.5-N.6
- Security + Deploy VM + Agent Hotel + Guardiana finale 9.5+

---

## File modificati S143 (NON su VM - deploy in N.6)

| File | Modifica |
|------|----------|
| `agent/agent.py` | HC.io /fail + 429 no CB + watermark multi-batch + safety net 90gg |
| `agent/http_sender.py` | signal param + HTTPError429 + 429 retry con Retry-After |
| `agent/reconcile_comparator.py` | max_id_in_window + rimossa condizione p_max_id>0 |
| `agent/tests/test_agent_e2e.py` | 7 test nuovi + 4 aggiornati |
| `agent/tests/test_http_sender.py` | 3 test nuovi (429 + signal) |
| `agent/tests/test_reconcile.py` | 3 test nuovi (watermark window) |

---

## Dove leggere

| Cosa | File |
|------|------|
| Subroadmap completa | `docs/SUBROADMAP_S140_LUCIDATURA.md` |
| HC.io /fail logica | `agent/agent.py:215-220` (all_invalid) + `:305-316` (post-batch) |
| HTTPError429 | `agent/http_sender.py:49-53` (eccezione) + `:195-207` (handling) |
| Watermark window | `agent/reconcile_comparator.py:121-133` (C3) |
| Safety net | `agent/agent.py:117-125` (alert) + `:148-154` (90gg cutoff) |

---

## Lezioni Apprese (Sessione 143)

### Cosa ha funzionato bene
- Step-by-step mirato: 5 fix in sequenza, ognuno testato prima del successivo
- Guardiana dopo tutti i 5 step -> score 9.5 al primo tentativo
- Watermark multi-batch: riflettere sulla logica (skipped = duplicati GIA' nel portale) prima di fixare

### Cosa non ha funzionato
- Nulla di critico. Sessione fluida.

### Pattern candidato
- "Rifletti prima di fixare" - Step 7 watermark: il fix ovvio (solo inserted) era sbagliato. I duplicati sono gia' nel portale, watermark DEVE avanzare. - Evidenza: S143. Azione: MONITORARE

---

*S143: FASE N.2 COMPLETATA (5 step). 13 test nuovi (346 agent PASS). 100 round QA. Prossimo: FASE N.3 Backend Fix.*
