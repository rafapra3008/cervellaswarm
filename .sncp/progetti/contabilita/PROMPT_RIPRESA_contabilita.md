# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 22 Febbraio 2026 - Sessione 133
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - FASE L COMPLETATA! Reconcile 3/3 Hotel ATTIVI

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | LIVE - Transformer v1.4.0 + Reconcile endpoint v1.0.0 |
| **3 Hotel Sync** | TUTTI ATTIVI (NL WM4007, SHE WM21651, HP WM24352) HC.io+TG 1h |
| **Reconcile NL** | ATTIVO S132! HC.io VERDE, 0 anomalie, window=30 |
| **Reconcile SHE** | ATTIVO S133! HC.io 94015357, Scheduler 05:00, window=1 |
| **Reconcile HP** | ATTIVO S133! HC.io 99c24a24, Scheduler 05:00, window=1 |
| **Lab v2** | INTOCCATO, frozen S87 |
| **Test** | **1709 PASS** (1399 portale + 310 agent, 0 fail) |
| **FASE K** | COMPLETATA S129-S130 - 24/24 finding fixati |
| **FASE L** | **COMPLETATA S131-S133** - Reconcile 3/3 hotel ATTIVI! |
| **Subroadmap** | `docs/SUBROADMAP_S128_DIAMANTE.md` |
| **Prossimo** | **FASE M** - SPRING Discovery + **monitoraggio reconcile SHE+HP** |

---

## S131 - FASE L.1+L.2: Reconcile Backend + Agent (commit 4c16545)

**L.1 - Backend Portale:**
- GET /api/v3/reconcile-stats (5 query SQLite, auth Bearer)
- Dati: ultimo_reconcile, count_anomalie, total_ericsoft, total_portale, delta
- 16 test nuovi, Guardiana 9.5/10

**L.2 - Agent Python (6 moduli):**
- reconcile_config.py - Configurazione da .env
- reconcile_reader.py - Lettura Ericsoft SQL Server (pymssql/pyodbc)
- reconcile_api.py - Comunicazione con portale V3
- reconcile_comparator.py - Confronto count + dettaglio per-giorno
- reconcile_notifier.py - Alert Telegram + HC.io ping
- reconcile.py - Entry point CLI (--hotel, --env, --dry-run, --verbose)
- 26 test nuovi, Guardiana 9.2/10

## S132 - FASE L.3 NL: Deploy + Test Reale (commit ae152e3)

**Prep (commit 64ace9c):**
- 3 .bat (nl/she/hp) per Task Scheduler Windows, 05:00 AM, log rotation 30gg
- Guardiana prep 9.5/10 (F1+F2+F6+F8 fixati)

**Fix compatibilita NL (commit ae152e3):**
- reconcile_config.py: _safe_int_env locale (config.py hotel vecchio non ce l'ha)
- reconcile_reader.py: getattr driver fallback per pymssql vecchio
- reconcile_nl.bat: .env path corretto (agent/.env, non root per NL)

**Risultato NL:**
- Dry-run: RECONCILE OK, 0 anomalie
- Test reale: RECONCILE OK, 0 anomalie, HC.io VERDE
- Task Scheduler: ContabilitaReconcile-NL, 05:00 AM daily

---

## S133 - FASE L.3 SHE+HP: Deploy Reconcile

**SHE:** HC.io 94015357, 7 file copiati, window=1, Scheduler 05:00, Guardiane 9.7+9.3/10
**HP:** HC.io 99c24a24, 7 file copiati, window=1, Scheduler 05:00, Guardiana 9.3/10
**Piano window:** =1 ora, =7 tra 1 sett, =30 tra 1 mese
**P2 aperto:** File Desktop pre-fix S132, copiare dal repo lab-v3 al prossimo VPN

---

## Subroadmap "Il Diamante" - Progresso

```
FASE K - QA Fix                              COMPLETATA!
  K.1  Fix P1+P2 critici (5 fix)           S129 (9.6/10)
  K.2  Fix P2 backend+logic (2 fix)        S130 (9.6/10)
  K.3  Fix P3 tutti (15 fix)               S130 (9.6/10)

FASE L - Agent Prova Reale                   COMPLETATA!
  L.1  Endpoint backend + 16 test          S131 (9.5/10) FATTO
  L.2  6 moduli Python + 26 test           S131 (9.2/10) FATTO
  L.3  Deploy NL + test reale              S132 (9.5/10) FATTO
  L.3  Deploy SHE + HP                     S133 (9.3/10) FATTO

FASE M - SPRING Discovery                   PENDING
  M.1  Discovery read-only DB SISTEMI
  M.2  Ottimizzare file Excel import

FASE N - Sync DB                             PENDING
  N.1  Allineare HP/SHE lab vs prod (NL ok)
```

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
                            Reconcile endpoint v1.0.0
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
```

---

## Lezioni Apprese (Sessione S131-S132)

### Cosa ha funzionato bene
- Design modulare reconcile (6 file separati) = testabile, facile debug
- Fix compat hotel NL specifici (config.py vecchio vs nuovo) risolti al primo tentativo
- Strategia "fix + Guardiana per ogni step" confermata: 3 Guardiane (9.5+9.2+9.5)/10

### Cosa non ha funzionato
- Crash Bun (segfault) ha perso aggiornamento NORD/PROMPT (fix: documentare SUBITO dopo ogni step)

### Pattern candidato
- "Preparare file deploy su Desktop per hotel" = Rafa copia con drag&drop via VPN -> CONFERMATO (S98+S132)

---

*S133: FASE L COMPLETATA! Reconcile ATTIVO su tutti e 3 gli hotel (NL+SHE+HP). 81 round QA totali.*
