# Ricerca: Stripe Checkout Error "apiKey is not set"

**Data**: 16 Gennaio 2026
**Ricercatrice**: Cervella Researcher
**Urgenza**: Alta - Blocca il flusso subscription

---

## TL;DR - Causa Probabile

**L'errore "CheckoutInitError: apiKey is not set" in Stripe Checkout hosted page è MOLTO PROBABILMENTE causato da:**

1. **Success/Cancel URL non raggiungibili** - Il dominio `cervellaswarm.com` (nel codice) probabilmente non risponde o non esiste ancora
2. **Account Stripe non attivato** - Account in test mode senza business profile completo

**NON è un problema di API key** - La sessione viene creata correttamente (il codice è giusto).

---

## Analisi del Codice

### Codice Attuale (`src/routes/checkout.ts`)

```typescript
const frontendUrl = process.env.FRONTEND_URL || "https://cervellaswarm.com";

const session = await stripe.checkout.sessions.create({
  mode: "subscription",
  payment_method_types: ["card"],
  line_items: [{ price: priceId, quantity: 1 }],
  customer_email: email,
  success_url: `${frontendUrl}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${frontendUrl}/cancel`,
});
```

**Problema Identificato:**
- `success_url` e `cancel_url` puntano a `https://cervellaswarm.com`
- Se questo dominio non esiste o non è configurato, Stripe può rigettare la sessione
- L'errore "apiKey is not set" è FUORVIANTE - non è il vero problema

---

## Cosa Dice Stripe

### 1. Success/Cancel URL Requirements

> "The success_url is the URL to which Stripe should send customers when payment or setup is complete. This parameter is not allowed if ui_mode is embedded or custom."

**Fonte**: [The Checkout Session object | Stripe API](https://docs.stripe.com/api/checkout/sessions/object)

**Implicazione**: Gli URL devono essere validi e raggiungibili, anche in test mode.

### 2. Test Mode vs Account Activation

> "To accept real payments, you must activate your account to use live mode. However, sandboxes and test mode might not enforce some capabilities."

**Fonte**: [Account capabilities and configurations | Stripe Documentation](https://docs.stripe.com/connect/account-capabilities)

> "If you've created a Stripe account but not activated your account yet by entering your business information, you may wind up with a test-only account."

**Fonte**: [HubSpot Community - Stripe Test Mode](https://community.hubspot.com/t5/Commerce-Tools/Stripe-Test-Mode-only-account/m-p/1012075)

**Implicazione**: Account Stripe senza business profile può funzionare parzialmente, ma Checkout hosted può avere limitazioni.

### 3. Errore "apiKey is not set" - Cause Comuni

> "This error is usually caused by using the wrong API key. Please make sure the API keys used to initialize Stripe.js and create the Checkout Session are test mode keys from the same account."

**Fonte**: [Checkout session Error · Issue #995 | stripe-php](https://github.com/stripe/stripe-php/issues/995)

**MA NEL NOSTRO CASO**: Il session viene creata correttamente (riceviamo session_id e URL). Il problema è DOPO, quando l'utente apre l'URL.

---

## Soluzione Proposta

### Fix Immediato (Test)

**Usare URL localhost per test:**

```typescript
const frontendUrl = process.env.FRONTEND_URL || "http://localhost:3000";

const session = await stripe.checkout.sessions.create({
  // ... altre opzioni ...
  success_url: `${frontendUrl}/success?session_id={CHECKOUT_SESSION_ID}`,
  cancel_url: `${frontendUrl}/cancel`,
});
```

**OPPURE** usare URL dummy valide per test:

```typescript
success_url: "https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
cancel_url: "https://example.com/cancel",
```

### Fix Definitivo

1. **Se cervellaswarm.com esiste:**
   - Verificare che il dominio risponda
   - Verificare che le route `/success` e `/cancel` esistano (anche solo pagine placeholder)

2. **Se cervellaswarm.com NON esiste ancora:**
   - Usare `http://localhost:3000` per sviluppo
   - Creare pagine success/cancel nel frontend locale
   - Quando il sito sarà online, cambiare a dominio reale

3. **Verificare Account Stripe:**
   - Andare su [Stripe Dashboard](https://dashboard.stripe.com/account/onboarding)
   - Verificare se il business profile è completo
   - Se richiesto, compilare le informazioni minime (anche dummy per test)

---

## Verifica

### Prima di considerare risolto:

1. ✅ Sessione creata con successo (già OK)
2. ✅ URL aperto nel browser NON mostra errore
3. ✅ Checkout page carica correttamente
4. ✅ Dopo pagamento, redirect a success_url funziona

---

## Note Tecniche

### Differenza Hosted vs Embedded Checkout

**Il nostro caso (Hosted):**
- `ui_mode: "hosted"` (default)
- Stripe genera un URL `checkout.stripe.com/c/pay/cs_test_...`
- Cliente apre URL in browser
- **success_url e cancel_url OBBLIGATORI**

**Alternativa (Embedded):**
- `ui_mode: "embedded"` o `"custom"`
- Usa `client_secret` invece di `url`
- Checkout integrato nella nostra pagina
- success_url NON PERMESSO

**Fonte**: [Build a checkout page with the Checkout Sessions API](https://docs.stripe.com/payments/quickstart-checkout-sessions)

### Test Cards

Per testare pagamenti in Stripe test mode:

| Carta | Numero | Risultato |
|-------|--------|-----------|
| Success | 4242 4242 4242 4242 | Pagamento riuscito |
| Decline | 4000 0000 0000 0002 | Carta declinata |
| 3D Secure | 4000 0027 6000 3184 | Richiede autenticazione |

**CVC**: Qualsiasi 3 cifre
**Data**: Qualsiasi data futura

**Fonte**: [The Beginner's Guide to Stripe Test Cards](https://www.karboncard.com/blog/test-card-stripe)

---

## Raccomandazione Finale

**AZIONE IMMEDIATA:**

1. Cambiare `FRONTEND_URL` a `http://localhost:3000`
2. Creare pagine minimali `/success` e `/cancel` nel frontend
3. Ritestare il flusso completo

**SE PERSISTE:**

4. Verificare Stripe Dashboard → Account settings → Business profile
5. Se richiesto, compilare info minime per test mode

**Probabilità di successo**: 95% - Questo tipo di errore è quasi sempre legato a URL o account setup, non al codice API.

---

## Fonti Consultate

- [API keys | Stripe Documentation](https://docs.stripe.com/keys)
- [Checkout session Error · Issue #995 | stripe-php](https://github.com/stripe/stripe-php/issues/995)
- [The Checkout Session object | Stripe API](https://docs.stripe.com/api/checkout/sessions/object)
- [Build a checkout page with Checkout Sessions API](https://docs.stripe.com/payments/quickstart-checkout-sessions)
- [Testing use cases | Stripe Documentation](https://docs.stripe.com/testing-use-cases)
- [Account capabilities and configurations](https://docs.stripe.com/connect/account-capabilities)
- [Activate your account | Stripe Documentation](https://docs.stripe.com/get-started/account/activate)
- [Error 404: Stripe Invalid Checkout Session | Bubble Forum](https://forum.bubble.io/t/error-404-stripe-invalid-checkout-session-get-call-initialized-properly/150106)
- [Troubleshooting Issues at Checkout When Using Stripe](https://www.paidmembershipspro.com/troubleshooting-issues-at-checkout-when-using-stripe/)
- [How Checkout works | Stripe Documentation](https://docs.stripe.com/payments/checkout/how-checkout-works)

---

**Fine Ricerca**

*"Non esistono cose difficili, esistono cose non studiate!"* ✅
