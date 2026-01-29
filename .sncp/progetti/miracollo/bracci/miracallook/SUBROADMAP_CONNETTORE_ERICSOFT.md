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

## FASE 2 - PREPARA ACCESSO DB SICURO

**Obiettivo:** Creare accesso READ-ONLY al database Ericsoft

| Step | Cosa | Stato |
|------|------|-------|
| 2.1 | Backup completo database PRA | [x] FATTO 29/01/2026 |
| 2.2 | Studiare struttura tabelle | [ ] ← ORA |
| 2.3 | Creare utente `miracollook_reader` | [ ] |
| 2.4 | Dare SOLO permessi SELECT | [ ] |
| 2.5 | Testare connessione con nuovo utente | [ ] |

**Server:**
- IP: `192.168.200.5`
- Istanza: `NLTERMINAL01\SQLERICSOFT22`
- Database: `PRA`

**REGOLA SACRA:** MAI usare utente `sa` per applicazioni!

**Rischio:** BASSO se seguiamo i passi

---

## FASE 3 - NOSTRO CONNETTORE

**Obiettivo:** Indipendenza totale da Bedzzle

| Step | Cosa | Stato |
|------|------|-------|
| 3.1 | Creare modulo Python per connessione SQL | [ ] |
| 3.2 | Query per prenotazioni | [ ] |
| 3.3 | Query per ospiti | [ ] |
| 3.4 | Query per servizi | [ ] |
| 3.5 | Sync periodico (ogni X minuti) | [ ] |
| 3.6 | Cache locale per performance | [ ] |

**Rischio:** MEDIO - richiede test approfonditi

---

## CHECKLIST SICUREZZA (OBBLIGATORIA)

```
Prima di FASE 2:
[x] Backup database fatto (29/01/2026)
[ ] Utente READ-ONLY creato
[ ] Permessi verificati (solo SELECT)
[x] Test su orario non critico (mattina)

Prima di FASE 3:
[ ] Timeout su ogni query (max 5 sec)
[ ] Max 2 connessioni simultanee
[ ] Logging di tutte le query
[ ] Circuit breaker implementato
```

---

## TIMELINE

```
S315 (29/01):    FASE 1 ✓ + Backup ✓ + Studio tabelle
PROSSIME:        FASE 2 - Utente READ-ONLY
DOPO:            FASE 3 - Connettore nostro
```

**Nessuna fretta. Un passo alla volta. Documentare tutto.**

---

*"Studiare prima, implementare dopo!"*
