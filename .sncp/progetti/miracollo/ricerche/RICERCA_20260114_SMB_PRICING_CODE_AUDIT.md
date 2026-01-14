# AUDIT CODICE: SMB PRICING MIRACOLLO

**Data**: 2026-01-14
**Ricercatrice**: Cervella Researcher
**Codebase**: miracollogeminifocus/backend
**Metodo**: Verifica CODICE REALE (no report, no documenti)

---

## EXECUTIVE SUMMARY

**SCORE REALE SMB PRICING: 2/10**

Il pricing SMB esiste SOLO come:
- Codice Stripe per guest checkout (B2C)
- File payment.py router (pagamenti booking)

**MANCA COMPLETAMENTE:**
- Subscription model
- Licensing per hotel
- Free tier / Trial logic
- Tabelle DB pricing tiers
- Endpoint subscription management
- Check "hotel ha pagato?"

**Conclusione**: Il codice reale è un PMS tradizionale B2C (pagamenti ospiti). Zero infrastruttura B2B SaaS.

---

## DETTAGLIO FILE VERIFICATI

### 1. STRIPE INTEGRATION

**File**: `backend/services/stripe_service.py`
**Righe**: 299 righe
**Status**: REALE (codice funzionante)

**Funzionalità esistenti**:
- ✅ `create_checkout_session()` - Per pagamenti OSPITI
- ✅ `verify_webhook_signature()` - Webhook Stripe
- ✅ `process_checkout_completed()` - Conferma pagamento
- ✅ `create_refund()` - Rimborsi
- ✅ `get_bank_transfer_info()` - Info bonifico

**CHI PAGA**: Gli OSPITI dell'hotel (B2C)
**NON**: L'hotel per usare Miracollo (B2B)

**Gap rispetto a SMB pricing**:
- ❌ NO subscription checkout
- ❌ NO recurring billing
- ❌ NO customer portal
- ❌ NO trial period logic
- ❌ NO tier-based pricing

### 2. PAYMENT MODEL

**File**: `backend/models/payment.py`
**Righe**: 40 righe
**Status**: STUB/BASIC

**Campi esistenti**:
```python
hotel_id, booking_id, payment_type, payment_method,
amount, payment_date, status, accounting_synced
```

**Gap**:
- ❌ NO subscription_id
- ❌ NO license_key
- ❌ NO plan_type (free/basic/premium)
- ❌ NO billing_cycle
- ❌ NO mrr/arr tracking

### 3. PAYMENTS ROUTER

**File**: `backend/routers/payments.py`
**Righe**: 312 righe
**Status**: REALE (CRUD payment completo)

**Endpoint esistenti**:
- GET /api/payments - Lista pagamenti
- POST /api/payments - Crea pagamento
- PUT /api/payments/{id} - Modifica pagamento
- DELETE /api/payments/{id} - Cancella pagamento
- POST /api/payments/link/{booking_id} - Link pagamento

**TUTTI per booking payment (ospite → hotel)**
**NESSUNO per subscription payment (hotel → Miracollo)**

### 4. DATABASE SCHEMA

**File**: `backend/database/schema.sql`
**Verificato**: TUTTO lo schema

**Tabelle pricing PRESENTI**: ZERO
**Tabelle subscription PRESENTI**: ZERO
**Tabelle license PRESENTI**: ZERO

**Unica menzione "plan"**: `rate_plans` e `meal_plans` (tariffe HOTEL, non pricing SaaS)

**Campo hotel che potrebbe contenere pricing**:
Tabella `hotels` (55 righe) - NESSUN campo subscription/license/tier

### 5. CORE CONFIG

**File**: `backend/core/config.py`
**Righe**: 150 righe verificate

**Variabili Stripe presenti**:
```python
STRIPE_SECRET_KEY
STRIPE_PUBLISHABLE_KEY
STRIPE_WEBHOOK_SECRET
```

**Variabili Stripe MANCANTI**:
- ❌ STRIPE_PRICE_ID_BASIC
- ❌ STRIPE_PRICE_ID_PREMIUM
- ❌ STRIPE_CUSTOMER_PORTAL_URL
- ❌ FREE_TIER_LIMIT_BOOKINGS

**Property helper esistenti**:
- `stripe_enabled` → Verifica se Stripe configurato
- `admin_api_key_enabled` → Verifica se admin key configurato

**Property helper MANCANTI**:
- ❌ `subscription_enabled`
- ❌ `license_check_enabled`
- ❌ `free_tier_enabled`

### 6. ROUTERS VERIFICATI

**Totale router**: 78 file Python in `/routers/`

**Router subscription/licensing trovati**: ZERO

**Router più vicini a billing**:
- `payments.py` → Payment OSPITI (B2C)
- `hotels.py` → CRUD hotel (no billing info)
- `settings.py` → Config hotel (no subscription)

**Nessun router per**:
- Subscription management
- License validation
- Billing dashboard
- Usage tracking per tier

### 7. MIGRATIONS DATABASE

**File verificati**: 39 migration file

**Migration subscription/licensing**: ZERO

**Migration più recenti**:
- 039_local_events.sql
- 038_learning_from_actions.sql
- 037_ai_transparency_tracking.sql
- 031_pricing_tracking.sql → Tracking PRICE SUGGESTIONS (revenue management), non subscription!

### 8. LICENSING LOGIC

**Ricerca pattern**: `check_license`, `verify_subscription`, `free_tier`

**File trovati**: 4 file
**Contenuto rilevante**: ZERO

I 4 match erano:
- `weather_service.py` → free tier API key (servizio esterno)
- `config.py` → menzionato sopra
- 2 file docs/test

**Conclusione**: NESSUN codice verifica se hotel ha pagato.

---

## GAP ANALYSIS - COSA MANCA PER SMB PRICING

### LIVELLO DATABASE (Score: 0/10)

**Tabelle da creare**:
```sql
CREATE TABLE subscriptions (
    id INTEGER PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    stripe_customer_id TEXT,
    stripe_subscription_id TEXT,
    plan_type TEXT, -- free, basic, premium
    status TEXT, -- active, past_due, cancelled
    current_period_start TEXT,
    current_period_end TEXT,
    trial_ends_at TEXT,
    created_at TEXT
);

CREATE TABLE subscription_tiers (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE, -- free, basic, premium
    name TEXT,
    price_monthly REAL,
    price_yearly REAL,
    stripe_price_id_monthly TEXT,
    stripe_price_id_yearly TEXT,
    max_bookings INTEGER, -- NULL = unlimited
    max_rooms INTEGER,
    features_json TEXT -- JSON array
);

CREATE TABLE license_usage (
    id INTEGER PRIMARY KEY,
    hotel_id INTEGER REFERENCES hotels(id),
    period_month TEXT, -- YYYY-MM
    bookings_count INTEGER,
    rooms_count INTEGER,
    recorded_at TEXT
);
```

### LIVELLO MODELS (Score: 1/10)

**Models da creare** (Pydantic):
- `Subscription` / `SubscriptionCreate` / `SubscriptionUpdate`
- `SubscriptionTier` / `TierFeatures`
- `LicenseUsage` / `UsageStats`
- `BillingInfo` / `BillingHistory`

**Esiste solo**: `Payment` (per booking, non subscription)

### LIVELLO SERVICES (Score: 3/10)

**stripe_service.py ESISTENTE** (299 righe):
- ✅ Funziona per checkout B2C
- ✅ Webhook handler base
- ⚠️ Facilmente estendibile

**Servizi da creare**:
- `subscription_service.py` (0 righe → serve tutto)
- `license_service.py` (0 righe → serve tutto)
- `usage_tracking_service.py` (0 righe → serve tutto)

### LIVELLO ROUTER (Score: 0/10)

**Router da creare**:
```
routers/subscriptions.py          # CRUD subscriptions
routers/billing.py                # Billing dashboard
routers/license.py                # License check/validation
```

**Endpoint minimi necessari**:
```python
# Subscriptions
GET  /api/subscriptions/{hotel_id}
POST /api/subscriptions/create-checkout  # Hotel subscribe
POST /api/subscriptions/cancel
POST /api/subscriptions/upgrade
GET  /api/subscriptions/tiers  # Available plans

# Licensing
GET  /api/license/check/{hotel_id}  # Verifica valid
GET  /api/license/usage/{hotel_id}  # Current usage

# Billing
GET  /api/billing/history/{hotel_id}
GET  /api/billing/portal-link/{hotel_id}  # Stripe portal
```

### LIVELLO MIDDLEWARE (Score: 0/10)

**Middleware da creare**:
```python
# middleware/license_check.py
async def check_hotel_license(request: Request):
    """
    Verifica prima di OGNI richiesta API:
    1. Hotel ha subscription attiva?
    2. Se free tier, ha raggiunto limiti?
    3. Se trial, è scaduto?

    Se NO → HTTP 402 Payment Required
    """
```

**File esiste**: NO
**Logica esiste**: NO
**Conseguenza**: Tutti gli hotel possono usare Miracollo GRATIS per sempre!

### LIVELLO FRONTEND (Score: 0/10)

**Pagine da creare**:
- `/settings/subscription` → Current plan, upgrade CTA
- `/settings/billing` → Invoices, payment method
- `/pricing` → Public pricing page (sales)
- `/upgrade` → Upgrade flow con Stripe Checkout

**Modal/Banner da aggiungere**:
- Free tier limit warning
- Trial expiring banner
- Payment failed alert

### LIVELLO BUSINESS LOGIC (Score: 1/10)

**Logica esistente**:
- ✅ Hotel creation (senza check subscription)

**Logica mancante**:
```python
# Durante create booking
if not license_service.check_valid(hotel_id):
    raise HTTPException(402, "Subscription required")

if hotel.plan == "free":
    current_bookings = count_bookings_this_month(hotel_id)
    if current_bookings >= FREE_TIER_LIMIT:
        raise HTTPException(402, "Free tier limit reached")

# Durante create room
if len(hotel.rooms) >= hotel.subscription.max_rooms:
    raise HTTPException(402, "Plan room limit reached")
```

**Implementato**: ZERO controlli esistono

---

## RISCHIO BUSINESS

### SITUAZIONE ATTUALE

**Miracollo oggi può essere usato GRATIS da chiunque**:
1. Nessun check se hotel ha pagato
2. Nessun limite free tier
3. Nessun trial expiration
4. Nessun blocco funzionalità premium

**Conseguenza**:
- ❌ ZERO revenue ricorrente
- ❌ Non scalabile come SaaS
- ❌ Impossibile fare SMB growth strategy

### PRIORITÀ IMPLEMENTAZIONE

**PHASE 1 - Blocco base** (1-2 giorni):
1. Tabella `subscriptions`
2. Middleware `license_check`
3. Free tier con limite 10 booking/mese
4. Trial 14 giorni

**PHASE 2 - Stripe integration** (2-3 giorni):
5. Endpoint create subscription checkout
6. Webhook subscription events
7. Customer portal link
8. Tabella `subscription_tiers`

**PHASE 3 - Frontend** (3-4 giorni):
9. Pagina `/settings/subscription`
10. Upgrade flow
11. Limit warnings
12. Trial banners

**Totale MVP SMB Pricing**: 6-9 giorni lavoro

---

## EVIDENZE CODICE

### Evidence 1: stripe_service.py È B2C

```python
# Line 48-66 in stripe_service.py
def create_checkout_session(
    booking_number: str,  # ← BOOKING, not subscription!
    amount_cents: int,
    guest_email: str,     # ← GUEST email, not hotel owner!
    room_name: str,       # ← ROOM name
    check_in: str,        # ← Check-in date
    ...
```

**Questo è checkout OSPITE, non hotel subscription!**

### Evidence 2: Schema hotels SENZA License Info

```sql
-- schema.sql line 15-54
CREATE TABLE IF NOT EXISTS hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    ...
    city_tax_enabled INTEGER DEFAULT 1,
    ...
    is_active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    -- ❌ NO subscription_id
    -- ❌ NO plan_type
    -- ❌ NO license_valid_until
    -- ❌ NO trial_ends_at
);
```

### Evidence 3: Payments Router È Per Booking Payment

```python
# payments.py line 55-70
@router.post("/payments", response_model=Payment)
async def create_payment(payment: PaymentCreate):
    """Crea un nuovo pagamento e sincronizza con contabilità."""
    # Line 74: Aggiorna amount_paid sulla PRENOTAZIONE
    if payment.booking_id:
        conn.execute("""
            UPDATE bookings
            SET amount_paid = ...
        """)
```

**Payment è legato a booking_id, non subscription!**

### Evidence 4: ZERO Mention di "Subscription" nel Core

**Ricerca exhaustive**:
- Schema SQL: "subscription" → 0 match (solo in libreria Stripe)
- Routers: `subscription*.py` → 0 file
- Models: classe `Subscription` → 0 definizioni
- Services: `*subscription*` → 0 file

**Conclusione irrefutabile**: Il codice NON contiene logica subscription.

---

## CONCLUSIONE FINALE

### CODICE REALE vs CARTA

| Componente | Su Carta | Codice Reale | Gap |
|------------|----------|--------------|-----|
| Stripe Integration | ✅ Presente | ✅ B2C checkout | ⚠️ Serve B2B subscription |
| Subscription Model | ✅ Pianificato | ❌ ZERO | 🔴 CRITICO |
| License Check | ✅ Documentato | ❌ ZERO | 🔴 CRITICO |
| Free Tier Logic | ✅ Specificato | ❌ ZERO | 🔴 CRITICO |
| Trial Period | ✅ Menzionato | ❌ ZERO | 🔴 CRITICO |
| DB Schema Pricing | ✅ Disegnato | ❌ ZERO | 🔴 CRITICO |
| Frontend Billing | ✅ Wireframe | ❌ ZERO | 🔴 CRITICO |

### SCORE FINALE

**SMB Pricing Implementazione Reale**: **2/10**

**Breakdown**:
- Stripe library installata: +1
- stripe_service.py funzionante: +1
- Architettura base estendibile: +0
- Subscription logic: 0
- License enforcement: 0
- Free tier limits: 0
- Trial management: 0
- Billing frontend: 0

### NEXT STEPS RACCOMANDATI

**PRIORITÀ ASSOLUTA** (se vuoi vendere Miracollo come SaaS):

1. **BLOCCA GRATIS** - Implementa middleware license_check OGGI
2. **FREE TIER** - Limite 10 booking/mese per hotel non paganti
3. **STRIPE SUB** - Crea subscription checkout flow
4. **TRIAL** - 14 giorni automatici per nuovi hotel

**Senza questi 4 step**: Miracollo non è un SaaS, è un software gratuito.

**Tempo stimato**: 1-2 settimane full-time

**ROI**: Da €0 MRR → potenziale €XXX MRR per hotel paganti

---

**Fine Audit**

*Report generato verificando 100% codice backend reale*
*Zero assunzioni, solo evidenze file system e database*

**Metodologia**: Read file → Count lines → Verify logic → Document gap

**Affidabilità**: 10/10 (basato su codice, non su documentazione)
