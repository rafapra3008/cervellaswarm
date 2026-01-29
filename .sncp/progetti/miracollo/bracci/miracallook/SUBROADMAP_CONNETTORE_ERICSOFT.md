# SUBROADMAP - Connettore Ericsoft

> **Creata:** 29 Gennaio 2026 - Sessione 315
> **Obiettivo:** Connettere Miracollook ai dati Ericsoft in modo SICURO

---

## LA STRATEGIA: IBRIDA

```
+================================================================+
|   FASE 1: Impara da Bedzzle (OGGI)                             |
|   FASE 2: Prepara accesso DB sicuro                            |
|   FASE 3: Nostro connettore indipendente                       |
+================================================================+
```

---

## FASE 1 - IMPARA DA BEDZZLE

**Obiettivo:** Capire come funziona l'API, quali dati arrivano

| Step | Cosa | Stato |
|------|------|-------|
| 1.1 | Test chiamata API Bedzzle | [x] Testato S315 |
| 1.2 | Documentare endpoint disponibili | [x] Dati da Ericsoft |
| 1.3 | Mappare struttura dati JSON | [x] Vedi MyReception |
| 1.4 | Capire autenticazione (3 chiavi) | [x] 3 chiavi documentate |

**Credenziali:**
- URL: `https://connect.bedzzle.com/oapi/v1/marketplace`
- PublicKey: `AIzaSyBmH1GN1M1Bs36oJaS0gEoNLqMERmKoClQ`
- PrivateKey: `803ca5c21c482907346927a3a4efa60b`
- ProductKey: `9af72bea-1e03-48d1-859b-db15d8b0f159`

**Rischio:** ZERO - solo lettura API esterna

---

## FASE 2 - PREPARA ACCESSO DB SICURO ✓ COMPLETATA S316

**Obiettivo:** Creare accesso READ-ONLY al database Ericsoft

| Step | Cosa | Stato |
|------|------|-------|
| 2.1 | Backup completo database PRA | [x] FATTO 29/01/2026 |
| 2.2 | Studiare struttura tabelle | [x] COMPLETATO S316 |
| 2.3 | Creare utente `miracollook_reader` | [x] COMPLETATO S316 |
| 2.4 | Dare SOLO permessi SELECT (5 tabelle) | [x] GRANT + DENY testato |
| 2.5 | Testare connessione con nuovo utente | [x] Test permessi OK |

**Server:**
- IP: `192.168.200.5`
- Istanza: `NLTERMINAL01\SQLERICSOFT22`
- Database: `PRA`
- **User:** `miracollook_reader` (credenziali in .env)

**REGOLA SACRA:** MAI usare utente `sa` per applicazioni!

**Rischio:** COMPLETATO CON SUCCESSO

---

## FASE 3 - NOSTRO CONNETTORE

**Obiettivo:** Indipendenza totale da Bedzzle

| Step | Cosa | Stato |
|------|------|-------|
| 3.1 | Creare modulo Python per connessione SQL | [x] S317 |
| 3.2 | Test connessione reale (da rete hotel) | [ ] |
| 3.3 | Integrazione email enrichment | [ ] |
| 3.4 | Query per servizi | [ ] |
| 3.5 | Sync periodico (ogni X minuti) | [ ] |
| 3.6 | Cache locale per performance | [ ] |

**S317:** Modulo `backend/ericsoft/` creato con circuit breaker, semaphore, logging. Audit Guardiana 9/10.

**Rischio:** MEDIO - richiede test approfonditi

---

## CHECKLIST SICUREZZA (OBBLIGATORIA)

```
FASE 2 COMPLETATA:
[x] Backup database fatto (29/01/2026)
[x] Utente READ-ONLY creato (miracollook_reader)
[x] Permessi verificati (solo SELECT su 5 tabelle)
[x] Test su orario non critico (13:30)
[x] DENY INSERT/UPDATE/DELETE verificato

FASE 3.1 COMPLETATA (S317):
[x] Timeout su ogni query (max 5 sec) - connector.py
[x] Max 2 connessioni simultanee - asyncio.Semaphore
[x] Logging di tutte le query - structlog
[x] Circuit breaker implementato - 3 failures → 60s block
```

---

## TIMELINE

```
S315 (29/01):    FASE 1 ✓ + Backup ✓
S316 (29/01):    FASE 2 ✓ COMPLETATA! Schema + Utente
S317 (29/01):    FASE 3.1 ✓ COMPLETATA! Modulo Python + Audit 9/10
S318:            FASE 3.2 - Test connessione reale (da rete hotel)
```

**Nessuna fretta. Un passo alla volta. Documentare tutto.**

---

*"Studiare prima, implementare dopo!"*
