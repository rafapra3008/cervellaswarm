# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 25 Febbraio 2026 - Sessione 153
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale - S153 Deploy + Bug Faldone Trovato

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | v3.contabilitafamigliapra.it - **7 file deployati S153** (FORTEZZA v2.0.0, 12/12 OK) |
| **Stagioni NL** | INVERNO 2024-2025 + ESTATE 2025 **CHIUSE** (Rafa le ha richiuse, ma pareggi mancanti) |
| **3 Hotel Agent** | TUTTI v2.0.1, NL+SHE+HP scheduler ON |
| **Test** | 1441 portale + 348 agent = **1789 PASS** |
| **Round QA** | **125** + 1 Ops + 1 Caccia Bug |
| **Backup DB** | `contabilita_nl.db.backup_pre_reopen_20260225_101439` |

---

## HANDOFF S153 -> S154: Due Problemi da Risolvere

### Problema 1: BUG nel codice faldone storico (TROVATO in S153)

**File:** `backend/database/seasons.py` - metodo `get_season_history()`
**Riga:** ~331-337 (query caparre)

**Il bug:** Quando si chiude una stagione, le caparre NON pareggiate vengono migrate alla stagione successiva (carry-forward). Il faldone poi cerca `WHERE stagione = ?` e NON trova le caparre migrate. Il conteggio caparre nella tabella del faldone risulta incompleto.

**Il fix (1 riga):**
```python
# PRIMA (bug):
'SELECT ... FROM transactions_caparra WHERE stagione = ?'

# DOPO (fix):
'SELECT ... FROM transactions_caparra WHERE stagione = ? OR originated_from_season = ?'
```

**Nota:** I box statistiche in alto (CAPARRE, GIR, PAREGGI) leggono da `closed_stats` (snapshot JSON al momento della chiusura) e sono CORRETTI. La tabella espandibile sotto legge query live ed e' quella con il bug.

### Problema 2: Matching non rifatto per le 2 stagioni

**Causa:** Dopo la riapertura S153, le caparre e GIR ci sono tutti nel DB, ma i pareggi (match tra caparra e giroconto) NON sono stati ricreati. Rafa ha richiuso le stagioni senza fare il matching, quindi il faldone mostra pochi pareggi.

**Dati DB attuali (VM):**

| Stagione | Caparre | GIR | Pareggi ORA | Pareggi ATTESI |
|----------|---------|-----|-------------|----------------|
| INVERNO 2024-2025 | 305 | 296 | ~4 | ~289 |
| ESTATE 2025 | 1197 | 1172 | ~7 | ~1150 |
| INVERNO 2025-2026 | 432 | 382 | 369 | 369 (OK) |

---

## Piano S154 (Ordine Preciso)

### Fase 1: Fix il bug (codice)
1. Fix `get_season_history()` in `backend/database/seasons.py` - aggiungere `OR originated_from_season = ?`
2. Scrivere test per verificare il fix
3. Guardiana audit
4. Deploy il fix su VM (1 solo file: `backend/database/seasons.py`)

### Fase 2: Riapertura + Matching + Chiusura
5. Riaprire le 2 stagioni (stesso processo S153: backup -> stop service -> transazione -> start)
6. Rafa fa matching per **INVERNO 2024-2025** dalla UI (tab Pareggi)
7. Rafa chiude INVERNO 2024-2025 dalla UI
8. Rafa fa matching per **ESTATE 2025** dalla UI
9. Rafa chiude ESTATE 2025 dalla UI
10. Verifica faldone storico - numeri corretti

### Note importanti per S154
- Il matching e' GLOBALE (tocca tutte le stagioni aperte). I pareggi gia' confermati sono SAFE
- Fare UNA stagione alla volta: match -> chiudi -> poi la successiva
- Prima la piu' vecchia (INVERNO 2024-2025), poi ESTATE 2025
- Lo script riapertura e' lo STESSO di S153 (provato e funzionante)

---

## Dove leggere

| Cosa | File |
|------|------|
| **Bug faldone** | `backend/database/seasons.py` - `get_season_history()` ~riga 331 |
| Subroadmap Diamante Finale | `docs/SUBROADMAP_S153_DIAMANTE_FINALE.md` |
| Piano deploy S152 | `docs/PIANO_DEPLOY_S152.md` |
| NORD.md (bussola) | `NORD.md` (lab-v3 worktree) |

---

## Lezioni Apprese (Sessione 153)

### Cosa ha funzionato bene
- **FORTEZZA v2.0.0 impeccabile**: 12/12 step, MD5 match, prod+lab-v2 intatti
- **Guardiana dopo ogni step**: 5 audit in 1 sessione, nessun finding perso
- **Stop service + BEGIN TRANSACTION**: zero inconsistenze per operazioni DB
- **Caccia Bug prima di agire**: ha trovato il bug faldone PRIMA di sprecare tempo

### Cosa non ha funzionato
- **Riapertura senza matching**: le stagioni sono state riaperte e richiuse senza rifare i pareggi
- **Non verificato il faldone in locale prima**: avremmo visto il problema subito

### Pattern candidato
- **Caccia Bug OBBLIGATORIA prima di operazioni DB**: Evidenza: S153. Azione: PROMUOVERE

---

*S153: Deploy 7 file OK. Bug faldone trovato (get_season_history manca originated_from_season). Matching da rifare. Piano S154 scritto.*

---

## AUTO-CHECKPOINT: 2026-02-25 12:11 (unknown)

### Stato Git
- **Branch**: lab-v2
- **Ultimo commit**: eb48d09 - ANTI-COMPACT: PreCompact auto
- **File modificati**: Nessuno (git pulito)

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
