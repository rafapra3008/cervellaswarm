# Guida Stripe Live Mode

> **Status:** PRONTO per passare a Live quando serve
> **Attuale:** Test Mode (funzionante, testato Sessione 243)

---

## STATO ATTUALE (Test Mode)

```
Account: acct_1SqEoCDcRzSMjFE4
Webhook: https://cervellaswarm-api.fly.dev/webhooks/stripe
Piani: Pro $20/mo, Team $35/mo

TUTTO TESTATO E FUNZIONANTE in Test Mode!
```

---

## QUANDO PASSARE A LIVE

```
RACCOMANDAZIONE: Dopo Show HN, quando arrivano primi utenti paganti.

MOTIVO:
- Test Mode funziona per sviluppo
- Live Mode serve solo per pagamenti REALI
- Non ha senso attivare Live se nessuno paga ancora
```

---

## CHECKLIST PASSAGGIO A LIVE

### Step 1: Attivare Account Stripe Live

1. Vai su https://dashboard.stripe.com
2. Click su "Activate your account" (banner in alto)
3. Compila:
   - Business details (nome, indirizzo)
   - Bank account per payout
   - Tax information
4. Verifica identità (potrebbe richiedere documento)

**Tempo:** 10-15 min + eventuale verifica (24-48h)

### Step 2: Creare Prodotti/Prezzi Live

1. Switch a "Live mode" nel dashboard (toggle in alto a destra)
2. Vai su Products
3. Crea:
   - **Pro Plan**: $20/month, recurring
   - **Team Plan**: $35/month, recurring
4. Copia i nuovi Price ID (price_live_...)

### Step 3: Creare Webhook Endpoint Live

```bash
# Con Stripe CLI
stripe webhook_endpoints create \
  --url="https://cervellaswarm-api.fly.dev/webhooks/stripe" \
  --enabled-events="checkout.session.completed,customer.subscription.updated,customer.subscription.deleted,invoice.paid,invoice.payment_failed" \
  --live
```

Copia il nuovo Webhook Secret (whsec_...)

### Step 4: Aggiornare Fly.io Secrets

```bash
# Sostituisci con le NUOVE chiavi LIVE
fly secrets set STRIPE_SECRET_KEY="sk_live_..." -a cervellaswarm-api
fly secrets set STRIPE_PRICE_PRO="price_live_..." -a cervellaswarm-api
fly secrets set STRIPE_PRICE_TEAM="price_live_..." -a cervellaswarm-api
fly secrets set STRIPE_WEBHOOK_SECRET="whsec_..." -a cervellaswarm-api

# Verifica
fly secrets list -a cervellaswarm-api
```

### Step 5: Test Pagamento Reale

1. Apri `cervellaswarm upgrade pro` da CLI
2. Inserisci email REALE
3. Usa carta REALE (anche prepagata da €1)
4. Verifica:
   - Webhook ricevuto nei log Fly.io
   - Subscription attiva su Stripe
   - CLI mostra tier Pro

---

## COSE IMPORTANTI

### Differenze Test vs Live

| Aspetto | Test Mode | Live Mode |
|---------|-----------|-----------|
| API Key | sk_test_... | sk_live_... |
| Price ID | price_xxx... | price_xxx... (diversi!) |
| Webhook Secret | whsec_... | whsec_... (diverso!) |
| Carte | 4242 4242 4242 4242 | Carte REALI |
| Soldi | Finti | VERI |

### NON Mischiare

```
ATTENZIONE: MAI usare chiavi test in produzione o viceversa!

Chiavi test → test.stripe.com
Chiavi live → dashboard.stripe.com
```

### Webhook Events da Monitorare

```
checkout.session.completed  → Utente ha pagato
invoice.paid                → Rinnovo mensile OK
invoice.payment_failed      → Pagamento fallito
customer.subscription.updated → Cambio piano
customer.subscription.deleted → Cancellazione
```

---

## TIMELINE RACCOMANDATA

```
1. LANCIO SHOW HN (gratis, no pagamenti)
   ↓
2. PRIMI UTENTI interessati
   ↓
3. ATTIVA LIVE MODE (quando qualcuno vuole pagare)
   ↓
4. TEST pagamento reale con TUA carta
   ↓
5. APRI pagamenti a tutti
```

---

## SE SERVE AIUTO

- Stripe Docs: https://stripe.com/docs
- Webhook Testing: `stripe listen --forward-to localhost:3000/webhooks/stripe`
- Support: Cervella DevOps può assistere

---

## NOTA FINALE

```
Non c'è fretta di attivare Live Mode.

Il prodotto è GRATIS per iniziare.
Free tier = 5 chiamate/giorno.

Live Mode serve solo quando:
- Utenti vogliono Pro/Team tier
- Servono pagamenti REALI

Fino ad allora, Test Mode va benissimo.
```

---

*Guida creata: Sessione 256*
*"Fatto BENE > Fatto VELOCE"*
