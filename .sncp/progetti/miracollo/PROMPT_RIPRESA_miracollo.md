# PROMPT RIPRESA - Miracollo

> **Ultimo aggiornamento:** 18 Gennaio 2026 - Sessione 259
> **Status:** PRODUZIONE STABILE - Planning funziona!

---

## SESSIONE 259: FIX DEPLOY + SUBROADMAP

### Cosa Abbiamo Fatto

```
3 PROBLEMI RISOLTI:

1. Planning 404
   - Causa: Conflitto naming (planning.py vs planning/ cartella)
   - Fix: planning.py → planning_core.py
   - Commit: 7c2867f

2. Prenotazioni appaiono/spariscono
   - Causa: 2 container backend con stesso alias DNS "backend"
   - Fix: Rimosso container rogue, aggiunto name:miracollo
   - Commit: 2436923

3. Migration DB mancante
   - Causa: Colonna 'imported' non esisteva
   - Fix: Eseguita migration 025 sulla VM
```

### Subroadmap DEPLOY_BLINDATO Creata

```
Path: CervellaSwarm/.sncp/roadmaps/SUBROADMAP_DEPLOY_BLINDATO.md

FASE 1: Fix immediato          ✓ COMPLETATA
FASE 2: Guardrail tecnici      ← PROSSIMO (wrapper docker run)
FASE 3: Un solo entry point    (4 comandi invece di 93 script)
FASE 4: Wizard interattivo     (non puoi saltare step)
FASE 5: Monitoraggio           (alert automatici)

Principio: "PATH CORRETTO più FACILE del path sbagliato"
```

---

## ARCHITETTURA 3 BRACCI

```
MIRACOLLO
├── PMS CORE (:8001)        90% - STABILE!
├── MIRACOLLOOK (:8002)     60% - Non toccato
└── ROOM HARDWARE (:8003)   10% - Attesa hardware
```

---

## MODULO VCC (DA TESTARE)

```
IMPLEMENTATO nella sessione 258:
- Backend: charge_vcc_payment() in stripe_service.py
- Backend: POST /api/payments/charge-vcc
- Frontend: Stripe Elements in modal-payment.js v2.0
- Frontend: Bottone "VCC Booking" (blu)

Stripe Sandbox: acct_1Sqrxk7aXUHP1bna
Carta test: 4242 4242 4242 4242

STATUS: Codice completo, DA TESTARE nel browser!
```

---

## PROSSIMI STEP

```
PRIORITÀ 1: Test VCC
- Aprire prenotazione nel browser
- Click "Pagamento" → "VCC Booking"
- Testare con carta 4242 4242 4242 4242

PRIORITÀ 2: FASE 2 subroadmap
- Wrapper bash su VM che blocca "docker run"
- 10 minuti di lavoro

PRIORITÀ 3: Documentazione
- Documentare VCC in docs/
```

---

## STATO INFRASTRUTTURA

```
VM MIRACOLLO:
- 1 container backend: miracollo-backend-1 (healthy)
- 1 container nginx: miracollo-nginx (healthy)
- DB: ~/app/backend/data/miracollo.db
- docker-compose.yml ha name:miracollo (previene duplicati)

LOCALE:
- Container: miracollo-backend-local
- Funziona correttamente
```

---

*"Fatto BENE > Fatto veloce"*
