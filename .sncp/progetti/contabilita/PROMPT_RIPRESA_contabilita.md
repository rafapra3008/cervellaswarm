# PROMPT RIPRESA - Contabilita Antigravity

> **Ultimo aggiornamento:** 26 Febbraio 2026 - Sessione 170
> **Branch attivo:** lab-v3 (sviluppo V3) + lab-v2 (intoccato) + main (produzione)
> **Versione canonica:** `CervellaSwarm/.sncp/progetti/contabilita/PROMPT_RIPRESA_contabilita.md`

---

## Stato Attuale

| Cosa | Stato |
|------|-------|
| **Produzione** | v2.11.0 LIVE su contabilitafamigliapra.it (INTATTA) |
| **V3 VM** | Frontend S165 + Backend v1.6.0 (security fix S169-S170 NON ancora deployati) |
| **Agent NL/SHE/HP** | **v2.1.0 LIVE** - 3/3 attivi |
| **Test** | **1888 PASS** (1532 portale + 356 agent, 1 fail pre-esistente) |
| **Security Fix** | **AUDITATO R159+R160** - 8 fix S169 + audit codice + IDOR query param completato |
| **Commit** | `054efbb` pushato su lab-v3 - PRONTO per deploy |

---

## PROSSIMO: Deploy VM Security Fix (S171)

```
+====================================================================+
|  DEPLOY VM - MAPPA COMPLETA                                         |
+====================================================================+

  FILE DA DEPLOYARE SU VM (/opt/contabilita-v3/)

  +---------------------------------------------------+
  | 1. backend/dependencies.py    IDOR cross-portal   |
  | 2. backend/main.py            CORS + HSTS + auth  |
  | 3. backend/routers/auth.py    Portal codes env    |
  | 4. backend/routers/ericsoft.py Watermark auth     |
  | 5. backend/routers/spring.py  Magic bytes + %s    |
  +---------------------------------------------------+

  FILE DA DEPLOYARE SU AGENT (Windows, Rafa VPN)

  +---------------------------------------------------+
  | 6. agent/http_sender.py       Auth su watermark   |
  +---------------------------------------------------+

  OPERAZIONI AGGIUNTIVE

  +---------------------------------------------------+
  | 7. Migration v15 (sync_metrics) - run su VM DB    |
  | 8. .env V3: aggiungere PORTAL_CODE_NL/HP/SHE     |
  +---------------------------------------------------+
```

### Ordine Deploy FORTEZZA MODE

1. Snapshot pre-deploy
2. Deploy 5 file backend su VM
3. Aggiungere variabili PORTAL_CODE_* al .env V3
4. Restart service contabilita-v3
5. Test health + endpoint critici
6. Migration v15 (sync_metrics)
7. Agent: Rafa copia http_sender.py su Windows via VPN
8. Test agent watermark (dry-run)

### ATTENZIONE DEPLOY

- **Watermark endpoint ora richiede auth** -> agent DEVE avere http_sender.py aggiornato
- Se deploy agent PRIMA di backend: agent ottiene 401 su watermark (non critico, fallback a full sync)
- Se deploy backend PRIMA di agent: agent vecchio chiama watermark senza auth -> 401 -> fallback a full sync
- **Entrambi gli ordini sono safe** grazie al fallback, ma idealmente backend + agent insieme

---

## Security Fix Deployati (S169-S170)

| # | Fix | Audit |
|---|-----|-------|
| 1 | IDOR cross-portal: path + header + query param protetti | R159 F1 fixato |
| 2 | CORS wildcard bloccato in produzione (hard block) | R159 OK |
| 3 | Watermark: auth API key richiesta | R159 OK + test 401 (F4) |
| 4 | Agent http_sender: auth header su GET watermark | R159 OK |
| 5 | Magic bytes ZIP su upload SPRING | R159 OK + test vuoto/corto (F9) |
| 6 | Portal codes da environment | R159 OK |
| 7 | X-Response-Time rimosso in produzione | R159 OK |
| 8 | HSTS con preload | R159 OK |

**Guardiana R159: 9.3/10 -> fix -> R160: 9.6/10 APPROVED**

---

## Dove leggere

| Cosa | File (lab-v3) |
|------|---------------|
| IDOR fix completo | `backend/dependencies.py:60-95` (3 check points) |
| IDOR middleware injection | `backend/main.py:314` (authenticated_portal) |
| CORS hard block prod | `backend/main.py:136-148` |
| Watermark auth | `backend/routers/ericsoft.py:397-407` |
| Portal codes da env | `backend/routers/auth.py:29-33` |
| Magic bytes SPRING | `backend/routers/spring.py:253-258` |
| Test IDOR (9 test) | `tests/test_idor_prevention.py` (NUOVO) |

---

## Lezioni Apprese (Sessione 170)

### Cosa ha funzionato bene
- **Audit CODICE dei fix separato dall'audit dei finding**: Guardiana R159 ha trovato F1 (IDOR query param non protetto!) che era sfuggito
- **Deploy su sessione fresh**: Rafa ha deciso di NON deployare nella stessa sessione dell'audit - piu sicuro

### Cosa non ha funzionato
- **Safety check lab-v2 ancora necessario**: alias .zshrc puntava a lab-v2. Fixato: ora `contabilita` apre lab-v3

### Pattern candidato
- **Audit codice DEI FIX prima del deploy**: non basta auditare i finding, serve auditare anche il codice che li fixa. Evidenza: S170 F1 IDOR. PROMUOVERE.

---

*S170: Audit codice fix R159 (9.3) + fix finding R160 (9.6). IDOR completo su 3 vettori. 12 nuovi test. Pronto per deploy VM.*

---

## AUTO-CHECKPOINT: 2026-02-26 06:06 (unknown)

### Stato Git
- **Branch**: lab-v2
- **Ultimo commit**: eb48d09 - ANTI-COMPACT: PreCompact auto
- **File modificati**: Nessuno (git pulito)

### Note
- Checkpoint automatico generato da hook
- Trigger: unknown

---
