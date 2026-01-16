# PROMPT RIPRESA - CervellaSwarm

> **Ultimo aggiornamento:** 16 Gennaio 2026 - Sessione 242
> **FASE ATTUALE:** Sprint 3 Stripe - BUG RISOLTO con Payment Links!

---

## SESSIONE 242 - BUG STRIPE RISOLTO

```
+================================================================+
|   PROBLEMA IDENTIFICATO E RISOLTO                              |
|                                                                |
|   BUG: "CheckoutInitError: apiKey is not set"                  |
|   CAUSA: Checkout Sessions (checkout.stripe.com) non funziona  |
|          con questo tipo di account Stripe                     |
|                                                                |
|   SOLUZIONE: Usare Payment Links API invece!                   |
|   - Payment Links (buy.stripe.com) FUNZIONANO                  |
|   - Cambiato codice da checkout.sessions.create()              |
|     a paymentLinks.create()                                    |
|                                                                |
|   INOLTRE SCOPERTO:                                            |
|   - Sandbox != Test Mode (sono diversi!)                       |
|   - Migrato da Sandbox a Test Mode standard                    |
|   - Ricreati prodotti in Test Mode                             |
+================================================================+
```

---

## CREDENZIALI AGGIORNATE (TEST MODE - NON Sandbox!)

```
STRIPE (Test Mode):
- Account: acct_1SqEoCDcRzSMjFE4
- Secret Key: sk_test_51SqEoCDcRzSMjFE4... (in Fly secrets)
- Pro Price: price_1SqJ5FDcRzSMjFE4cyZcqWs4 ($20/month)
- Team Price: price_1SqJ5nDcRzSMjFE4n6bK07k5 ($35/month)

FLY.IO:
- App: cervellaswarm-api
- URL: https://cervellaswarm-api.fly.dev
- Secrets AGGIORNATI con nuove chiavi Test Mode
```

---

## MAPPA SESSIONI

```
238: Sprint 1 BYOK COMPLETATO
 |
239: Sprint 2 Metering COMPLETATO
 |
240: Sprint 3 Stripe backend + CLI (70%)
 |
241: Sprint 3 Deploy OK, bug checkout
 |
242: Sprint 3 BUG RISOLTO!  <-- OGGI
 |
243: Sprint 3 test e2e → COMPLETATO!
```

---

## ROADMAP

```
Sprint 1: BYOK Polish              [COMPLETATO]
Sprint 2: Metering & Limits        [COMPLETATO]
Sprint 3: Stripe Integration       [95% - test e2e da fare]
Sprint 4: Sampling Implementation  [PROSSIMO]
Sprint 5: Polish
```

---

## PROSSIMA SESSIONE (243)

1. Testare checkout completo (Pro e Team)
2. Verificare webhook riceve eventi
3. Test end-to-end da CLI
4. Sprint 3 COMPLETATO!

---

## TL;DR

**Sessione 242:** Bug "apiKey is not set" RISOLTO!
- Causa: Checkout Sessions non compatibili con account
- Fix: Usato Payment Links API (buy.stripe.com)
- Migrato da Sandbox a Test Mode standard

**Prossimo (243):** Test e2e, Sprint 3 completato!

*"Non esistono cose difficili, esistono cose non studiate!"*
