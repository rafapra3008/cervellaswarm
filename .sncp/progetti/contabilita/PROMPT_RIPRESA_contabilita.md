# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 22 Febbraio 2026 - Sessione 134
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S134 Checkout Date Fix DEPLOYATO

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | LIVE - EricsoftTransformer v1.5.0 (checkout primario) + Reconcile v1.0.0 |
| **S134 Checkout** | **DEPLOYATO!** 9 file su VM, colonna Check Out = data partenza |
| **3 Hotel Sync** | TUTTI ATTIVI (NL WM4007, SHE WM21651, HP WM24352) HC.io+TG 1h |
| **Reconcile** | 3/3 ATTIVI (NL win=30, SHE+HP win=1) |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1705 PASS** (1395 portale + 310 agent, 0 fail) |
| **Round QA** | 88 totali (81 S133 + 7 S134) |
| **Subroadmap** | `docs/SUBROADMAP_S128_DIAMANTE.md` + `docs/SUBROADMAP_CHECKOUT_DATE.md` |
| **Prossimo** | Deploy agent.py su hotel (VPN) + **FASE M** SPRING Discovery |

---

## S134 - Checkout Date Fix (commit 08f359a + d58c752)

### Problema
La colonna "Check Out" nella UI mostrava il campo `check_in` (data di ARRIVO).
Rafa ha visto caparre inserite oggi con date checkin - per controllo stagione e matching giroconti serve checkout.

### Soluzione Implementata
- **UI**: colonna "Check Out" mostra `tx.checkout_date` (data PARTENZA)
- **Stagione**: chain `checkout_date (primario) > check_in (fallback)`
- **Rimosso**: fallback note_ericsoft, fallback stagione agent, fallback data_movimento
- **Edit inline**: checkout_date editabile con ricalcolo stagione automatico

### File Modificati (11 + 2 test)

| File | Modifica |
|------|----------|
| backend/database/transactions.py | checkout_date in allowed_fields + edit branch + create_transaction |
| backend/database/pareggi.py | Suggerimento pareggio usa checkout_date primario |
| backend/processors/ericsoft_transformer.py | Chain stagione invertita, rimosso import re |
| backend/routers/transactions.py | Pydantic model + routing + season guard |
| backend/security.py | Validazione checkout_date DD/MM/YYYY |
| frontend/js/data.js | Display tx.checkout_date + merge |
| frontend/js/config.js | FIELD_CONFIG checkout_date |
| frontend/js/editing.js | 5 punti edit inline + ricalcolo stagione |
| frontend/index.html | Cache bust ?v=202602221700 |
| agent/agent.py | Chain checkout > check_in |
| tests/ + agent/tests/ | 15+ test riscritti per nuova priorita |

### Dati Reali VM (pre-deploy)

| Hotel | CAP | CON checkout | SENZA | % |
|-------|-----|-------------|-------|---|
| NL | 1943 | 1927 | 16 | 99.2% |
| SHE | 8 | 7 | 1 | 87.5% |
| HP | 6 | 5 | 1 | 83.3% |

### QA Totale S134
- 7 Guardiane: 9.6 + 9.6 + 9.3 + 9.3 + 9.5 (finale) + 9.5 (pre-deploy) + Bug Hunt
- Double-triple check: trovato 1 P1 + 3 P2, tutti FIXATI prima del deploy
- 1395/1395 test PASS

### Deploy VM (commit d58c752)
- 9 file deployati su /opt/contabilita-v3/
- Backup con timestamp _20260222_HHMM
- Cache bust JS aggiornato
- contabilita-v3 service: active

---

## TODO Prossime Sessioni

1. **Verifica UI**: Rafa apre v3.contabilitafamigliapra.it -> colonna Check Out mostra data partenza
2. **Deploy agent.py**: Al prossimo VPN, copiare agent.py su NL/SHE/HP (stagione da checkout)
3. **Window reconcile**: Tra 1 sett -> RECONCILE_WINDOW_DAYS=7 su SHE+HP
4. **FASE M**: SPRING Discovery (read-only DB SISTEMI HP)
5. **FASE N**: Sync DB (allineare HP/SHE lab vs prod)

---

## Mappa Sistema

```
                    PRODUZIONE (INTATTA)
                    contabilitafamigliapra.it:443
                    v2.11.0, porta 8000
                    |
    VM Google Cloud (cervello-contabilita)
    35.193.39.185, e2-medium, $28/mese
                    |
        +-----------+-----------+
        |                       |
    LAB V2                  V3 (lab-v3)
    INTOCCATO               v3.contabilita...
    frozen S87              porta 8003
                            Transformer v1.5.0 (checkout!)
                            Reconcile v1.0.0
                            |
                +-----------+-----------+
                |           |           |
            Hotel NL    Hotel SHE   Hotel HP
            SYNC+REC    SYNC+REC    SYNC+REC
            WM 4007     WM 21651    WM 24352
            HC.io+TG    HC.io+TG    HC.io+TG
            1h sync     1h sync     1h sync
            5AM recon   5AM recon   5AM recon
            win=30      win=1       win=1
            agent 1.3   agent 1.3   agent 1.3
            TODO: 1.4   TODO: 1.4   TODO: 1.4
```

---

## Lezioni Apprese (Sessione S134)

### Cosa ha funzionato bene
- "Double-triple check pre-deploy" = trovato 1 P1 + 3 P2 che 5 audit precedenti avevano mancato
- "Guardiana dopo ogni step" confermata: 7 Guardiane, score medio 9.46/10
- Ricerca in parallelo con 3 Cervelle all'inizio = analisi completa in 1 round

### Cosa non ha funzionato
- Deploy SCP: nomi file duplicati (transactions.py DB vs router) causava sovrascrittura. Fix: nomi univoci

### Pattern candidato
- "Double-triple check con Bug Hunter prima del deploy" -> CONFERMATO (P1 trovato!) -> PROMUOVERE

---

*S134: Checkout Date Fix DEPLOYATO! 88 round QA totali. "Ultrapassar os proprios limites!"*
