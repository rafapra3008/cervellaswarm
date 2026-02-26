# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 26 Febbraio 2026 - Sessione 184
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - POST S184 (Deploy agent HP+NL + fix .env tutti)

| Cosa | Stato |
|------|-------|
| **Produzione V2** | v2.11.0 LIVE su contabilitafamigliapra.it |
| **PDF Parser** | v1.14.0 DEPLOYATO S182 - tutti e 3 i servizi VM + locale :8000 |
| **V3 VM** | 10 file deployati S176, pdf_parser v1.14.0 S182 |
| **Agent NL/SHE/HP** | v2.1.0 LIVE + reconcile v1.1.0 **DEPLOYATO S184 su tutti e 3** |
| **Reconcile** | v1.1.0 - window 7gg, START_DATE=26 Feb (HP+SHE), NL senza start |
| **HC.io** | **TUTTI VERDI** (11 check: 3 sync + 3 reconcile + 3 backup + 2 altro) |
| **Test** | **1928 PASS** (1566 portale + 362 agent) |
| **Lab-v2** | INTATTO, frozen da S87 |
| **Backup 3-Layer** | V2 OK, V3 locale OK, **GCS V3 vuoto (da fixare)** |

---

## S184 - Deploy Agent HP+NL + Fix .env + HC.io Verde

### Cosa abbiamo fatto

| # | Azione | Risultato |
|---|--------|-----------|
| 1 | Deploy 16 file .py su HP | HPTERMINAL01, tutti copiati via VPN |
| 2 | Deploy 16 file .py su NL | NLTERMINAL01, tutti copiati via VPN |
| 3 | Fix .env HP | WINDOW=7, START_DATE=2026-02-26, HC_URL reconcile |
| 4 | Fix .env NL | WINDOW 30→7, trovato/fixato doppio .env (root+agent) |
| 5 | Fix .env SHE | Completato vars reconcile (TG, HC, START_DATE=2026-02-26) |
| 6 | Test manuale NL | Reconcile OK, 0 anomalie, HC.io pingato → VERDE |
| 7 | Test manuale HP | Reconcile 4 anomalie (attese: dati misti), Telegram OK |
| 8 | Test manuale SHE | Reconcile 5 anomalie (attese: dati misti), Telegram OK |
| 9 | START_DATE aggiornato 26 Feb | HP+SHE partono puliti da oggi, zero rumore storico |
| 10 | HC.io tutti VERDI | NL ping reale, HP+SHE ping manuale |

### Mappa Deploy Agent Finale

```
                NL              SHE             HP
                ----            ----            ----
16 file .py:    FATTO S184      FATTO S183      FATTO S184
.env WINDOW=7:  FATTO           FATTO           FATTO
.env START:     non serve       2026-02-26      2026-02-26
.env HC_URL:    OK              FIXATO S184     OK
.env TG:        OK              FIXATO S184     OK
Test manuale:   OK (0 anom)     OK (5 anom att) OK (4 anom att)
HC.io:          VERDE           VERDE           VERDE
Schedule sync:  11:30           11:40           11:50
Schedule rec:   14:00           14:10           14:20
```

### Problema trovato: doppio .env

NL e SHE avevano DUE file .env:
- `C:\contabilita-agent\.env` (root) - usato dal sync
- `C:\contabilita-agent\agent\.env` (legacy) - usato dal reconcile NL bat

Il reconcile NL leggeva il vecchio `agent\.env` con WINDOW=30 invece del root con WINDOW=7.
Risolto aggiornando entrambi. P3 per pulizia definitiva.

### Decisione: START_DATE = oggi (Rafa S184)

I delta HP/SHE (4-5 anomalie) sono rumore del periodo transizione (dati misti PDF + Ericsoft).
Rafa decide: "iniziare da oggi in poi". START_DATE=2026-02-26 su entrambi.
Da domani il reconcile controlla SOLO dati 100% agent-sourced.

---

## DA FARE (Prossima Sessione S185)

### Verifica (P2)
| # | Cosa | Note |
|---|------|------|
| 1 | Verificare HC.io dopo run schedulato 27 Feb | NL 14:00, SHE 14:10, HP 14:20 - devono restare VERDI |
| 2 | Verificare Telegram 27 Feb | Nessun alert = tutto OK |

### Cleanup (P3)
| # | Cosa | Note |
|---|------|------|
| 3 | Pulire doppio .env NL+SHE | Unificare a root `.env`, fix bat reconcile_nl.bat |
| 4 | Cancellare cartelle deploy Desktop | deploy_agent_s177/ + deploy_agent_s183/ |

### Backlog (da S182)
| # | Cosa | Note |
|---|------|------|
| 5 | GO-BK-006: Test restore da GCS | Scaricare DB, integrity_check |
| 6 | Fix backup V3 su GCS | Cartella vuota, offsite non copre V3 |
| 7 | Subroadmap allineamento VM | MD5 tutti i file VM vs repo |
| 8 | Migration v15 deploy su VM | sync_metrics pronta |
| 9 | Bug load_dotenv() ordine | Fix in conftest.py o main.py |

---

## Dove leggere

| Cosa | Path |
|------|------|
| Agent code (16 file) | `agent/` (lab-v3 worktree) |
| Reconcile config | `agent/reconcile_config.py` |
| Deploy folder (cancellabile) | `~/Desktop/deploy_agent_s183/ALL/` |
| .env NL | `C:\contabilita-agent\.env` + `agent\.env` su NLTERMINAL01 |
| .env HP | `C:\contabilita-agent\.env` su HPTERMINAL01 |
| .env SHE | `C:\contabilita-agent\.env` + `agent\.env` su SHETERMINAL02 |

---

## Lezioni Apprese (Sessione 184)

### Cosa ha funzionato bene
- **Guida step-by-step**: Rafa guidato passo passo, ogni hotel testato individualmente
- **Dry-run prima di run reale**: cattura problemi senza effetti collaterali
- **Decisione pragmatica START_DATE=oggi**: evita investigazione inutile su dati transizione

### Cosa non ha funzionato
- **Doppio .env non rilevato**: NL aveva WINDOW=30 nel vecchio `agent\.env`, ci siamo accorti solo dal log
- **SHE .env incompleto**: mancavano TG+HC+START_DATE, deploy S183 non li aveva aggiunti tutti

### Pattern candidato
- **Doppio .env = trappola silenziosa**: SEMPRE verificare QUALE .env viene letto (controllare log!). Evidenza: S184 NL+SHE. PROMUOVERE.
- **Ping manuale HC.io per sbloccare**: quando reconcile skippa legitimamente, ping manuale OK. Non complica il codice.

---

*S184: Deploy completo 3 hotel, fix .env, HC.io tutti verdi, START_DATE=26 Feb per partenza pulita.*
