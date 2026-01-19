# Output: Schema Database Fatture XML

## Status
✅ PROPOSTA SCHEMA COMPLETO

## Contesto Analizzato

**Stack esistente:**
- SQLite + raw SQL (nessun ORM)
- Payment system esistente
- fiscal_receipts (scontrini RT) già implementato
- Optimistic locking su bookings (versioning)

**Requisiti chiariti:**
- Numerazione: progressivo globale + sezionale (es: 200/NL)
- NO reset annuale
- Sezionale "NL" per North Lodge
- SPRING gestisce invio SDI (noi solo XML)

---

## 1. SCHEMA PROPOSTO

### Tabella: fiscal_invoices

```sql
-- ============================================
-- FISCAL_INVOICES - Fatture Elettroniche XML
-- ============================================
-- Gestione fatture FatturaPA (fase 3 modulo fiscale)
-- Connessione a SPRING per invio SDI

CREATE TABLE IF NOT EXISTS fiscal_invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),

    -- NUMERAZIONE (con optimistic locking)
    invoice_number INTEGER NOT NULL,           -- Progressivo globale (200, 201, 202...)
    sezionale TEXT NOT NULL DEFAULT 'NL',      -- Sezionale (NL per North Lodge)
    fiscal_year INTEGER NOT NULL,              -- Anno fiscale (per audit, NO reset)
    invoice_date TEXT NOT NULL,                -- Data emissione (YYYY-MM-DD)

    version INTEGER DEFAULT 1,                 -- Optimistic locking (come bookings)

    -- COLLEGAMENTO
    booking_id INTEGER REFERENCES bookings(id),
    payment_id INTEGER REFERENCES payments(id),

    -- CLIENTE (dati per FatturaPA)
    customer_type TEXT NOT NULL,               -- 'individual', 'business', 'pa'
    customer_vat TEXT,                         -- P.IVA (11 cifre, no IT)
    customer_cf TEXT,                          -- Codice Fiscale (16 caratteri)
    customer_name TEXT NOT NULL,               -- Denominazione/Nome completo
    customer_address TEXT,                     -- Indirizzo (obbligatorio se B2B)
    customer_cap TEXT,
    customer_city TEXT,
    customer_province TEXT,                    -- 2 lettere (RM, MI, etc)
    customer_country TEXT DEFAULT 'IT',        -- ISO 3166 (IT, DE, etc)

    sdi_code TEXT DEFAULT '0000000',           -- Codice destinatario SDI (7 caratteri)
    pec_email TEXT,                            -- PEC (opzionale)

    -- IMPORTI
    subtotal REAL NOT NULL,                    -- Imponibile
    vat_amount REAL NOT NULL,                  -- IVA (tipicamente 10%)
    total_amount REAL NOT NULL,                -- Totale documento

    -- DETTAGLIO RIGHE (JSON)
    items_json TEXT NOT NULL,                  -- Array righe fattura
                                               -- [{"desc": "Pernottamento 3 notti",
                                               --   "qty": 3, "price": 100, "vat_rate": 10}]

    -- DATI HOTEL (snapshot per immutabilità)
    hotel_vat TEXT NOT NULL,                   -- P.IVA hotel (snapshot)
    hotel_cf TEXT,                             -- CF hotel
    hotel_name TEXT NOT NULL,                  -- Denominazione
    hotel_address_json TEXT,                   -- Indirizzo completo JSON

    -- XML GENERATO
    xml_content TEXT,                          -- XML FatturaPA completo
    xml_filename TEXT,                         -- Nome file (IT01234567890_00001.xml)

    -- EXPORT SPRING
    export_path TEXT,                          -- Path cartella export (/srv/spring/inbox)
    exported_at TEXT,                          -- Timestamp export

    -- STATO
    status TEXT DEFAULT 'draft',               -- draft, exported, confirmed, error
    error_message TEXT,

    -- SDI (gestito da SPRING, non da noi)
    sdi_status TEXT,                           -- accepted, rejected (ricevuto da SPRING)
    sdi_message_id TEXT,                       -- ID messaggio SDI
    sdi_date TEXT,                             -- Data accettazione/rifiuto

    -- ANNULLAMENTO
    voided INTEGER DEFAULT 0,                  -- Flag annullamento
    voided_at TEXT,
    voided_by TEXT,                            -- Email operatore
    void_reason TEXT,

    -- AUDIT
    created_at TEXT DEFAULT (datetime('now')),
    created_by TEXT,                           -- Email operatore
    updated_at TEXT
);

-- INDICI
CREATE UNIQUE INDEX IF NOT EXISTS idx_fiscal_invoices_number_sezionale
    ON fiscal_invoices(invoice_number, sezionale, fiscal_year);

CREATE INDEX IF NOT EXISTS idx_fiscal_invoices_hotel
    ON fiscal_invoices(hotel_id);

CREATE INDEX IF NOT EXISTS idx_fiscal_invoices_booking
    ON fiscal_invoices(booking_id);

CREATE INDEX IF NOT EXISTS idx_fiscal_invoices_payment
    ON fiscal_invoices(payment_id);

CREATE INDEX IF NOT EXISTS idx_fiscal_invoices_date
    ON fiscal_invoices(invoice_date DESC);

CREATE INDEX IF NOT EXISTS idx_fiscal_invoices_status
    ON fiscal_invoices(status);

CREATE INDEX IF NOT EXISTS idx_fiscal_invoices_customer_vat
    ON fiscal_invoices(customer_vat);

-- TRIGGER: auto-update updated_at
CREATE TRIGGER IF NOT EXISTS fiscal_invoices_update_timestamp
AFTER UPDATE ON fiscal_invoices
FOR EACH ROW
BEGIN
    UPDATE fiscal_invoices
    SET updated_at = datetime('now')
    WHERE id = OLD.id;
END;
```

---

## 2. GESTIONE CONCORRENZA

### Problema
Due operatori creano fattura simultanea → stesso numero progressivo.

### Soluzione 1: Optimistic Locking (RACCOMANDATO)

```sql
-- PROCEDURA:
-- 1. SELECT MAX per trovare prossimo numero
BEGIN TRANSACTION;

SELECT MAX(invoice_number) FROM fiscal_invoices
WHERE sezionale = 'NL' AND fiscal_year = 2026;
-- Risultato: 200

-- 2. INSERT con numero incrementato
INSERT INTO fiscal_invoices (
    invoice_number, sezionale, fiscal_year, ...
) VALUES (201, 'NL', 2026, ...);

-- 3. COMMIT
-- Se UNIQUE constraint violation → retry con SAVEPOINT
COMMIT;
```

**Vantaggio:** UNIQUE INDEX cattura duplicati.
**Gestione errore:** Retry automatico (max 3 tentativi).

### Soluzione 2: Sequence Table (alternative)

```sql
CREATE TABLE fiscal_sequences (
    sezionale TEXT PRIMARY KEY,
    last_number INTEGER DEFAULT 0,
    fiscal_year INTEGER,
    version INTEGER DEFAULT 1
);

-- INSERT or UPDATE atomico
UPDATE fiscal_sequences
SET last_number = last_number + 1, version = version + 1
WHERE sezionale = 'NL' AND version = ?
RETURNING last_number;
```

**Vantaggio:** Zero race conditions.
**Svantaggio:** Complessità aggiuntiva.

**RACCOMANDAZIONE:** Soluzione 1 (più semplice, indice UNIQUE è sufficiente).

---

## 3. CAMPI OBBLIGATORI vs OPZIONALI

### OBBLIGATORI (NOT NULL)
```
✅ invoice_number         (progressivo)
✅ sezionale              (default 'NL')
✅ fiscal_year            (anno)
✅ invoice_date           (data emissione)
✅ customer_type          ('individual', 'business', 'pa')
✅ customer_name          (denominazione cliente)
✅ subtotal, vat_amount, total_amount
✅ items_json             (righe fattura)
✅ hotel_vat, hotel_name  (dati cedente)
```

### OPZIONALI (NULL ok)
```
⚪ customer_vat           (obbligatorio solo se B2B)
⚪ customer_cf            (obbligatorio solo se IT individual)
⚪ customer_address       (obbligatorio solo se B2B)
⚪ pec_email              (raramente fornito)
⚪ xml_content            (generato dopo)
⚪ sdi_status             (ricevuto da SPRING)
```

### VALIDAZIONE APPLICATIVA

```python
# In backend/services/fiscal/invoice_validator.py

def validate_invoice_data(customer_type, data):
    if customer_type == 'business':
        assert data['customer_vat'], "P.IVA obbligatoria per B2B"
        assert data['customer_address'], "Indirizzo obbligatorio per B2B"

    if customer_type == 'individual' and data['customer_country'] == 'IT':
        assert data['customer_cf'], "CF obbligatorio per privati IT"

    # Validazione formato P.IVA (11 cifre numeriche)
    if data.get('customer_vat'):
        assert len(data['customer_vat']) == 11, "P.IVA: 11 cifre"
```

---

## 4. INDICI CONSIGLIATI

### Performance Query

| Indice | Motivo |
|--------|--------|
| `(invoice_number, sezionale, fiscal_year)` UNIQUE | Prevenire duplicati + lookup veloce |
| `(hotel_id)` | Filter per hotel |
| `(booking_id)` | Link booking → fattura |
| `(payment_id)` | Link pagamento → fattura |
| `(invoice_date DESC)` | Ordinamento cronologico |
| `(status)` | Filter per status (draft, exported) |
| `(customer_vat)` | Ricerca fatture cliente |

### Query Tipiche

```sql
-- Dashboard: fatture recenti
SELECT * FROM fiscal_invoices
WHERE hotel_id = 1 AND status = 'exported'
ORDER BY invoice_date DESC LIMIT 20;
-- USA: idx_fiscal_invoices_hotel + idx_fiscal_invoices_date

-- Cerca fatture cliente
SELECT * FROM fiscal_invoices
WHERE customer_vat = '12345678901';
-- USA: idx_fiscal_invoices_customer_vat

-- Prossimo numero
SELECT MAX(invoice_number) FROM fiscal_invoices
WHERE sezionale = 'NL' AND fiscal_year = 2026;
-- USA: idx_fiscal_invoices_number_sezionale (UNIQUE)
```

---

## 5. ESEMPIO DATI

```sql
INSERT INTO fiscal_invoices (
    hotel_id,
    invoice_number, sezionale, fiscal_year, invoice_date,
    customer_type, customer_vat, customer_name,
    customer_address, customer_cap, customer_city, customer_province,
    sdi_code,
    subtotal, vat_amount, total_amount,
    items_json,
    hotel_vat, hotel_name,
    status, created_by
) VALUES (
    1,                          -- hotel_id (Sesto Grado)
    200, 'NL', 2026, '2026-01-19',
    'business', '12345678901', 'Agenzia Viaggi Example Srl',
    'Via Roma 10', '00100', 'Roma', 'RM',
    '0000000',
    300.00, 30.00, 330.00,
    '[{"description": "Pernottamento 3 notti camera doppia", "quantity": 3, "unit_price": 100.00, "vat_rate": 10}]',
    '98765432109', 'North Lodge Srl',
    'draft', 'admin@sestogrado.it'
);
```

---

## 6. MIGRATION FILE

**Path:** `backend/database/migrations/043_fiscal_invoices.sql`

---

## Perf
- UNIQUE index su (invoice_number, sezionale, year) → O(log n) per INSERT
- SELECT MAX → O(log n) con indice UNIQUE
- Concorrenza gestita da SQLite transaction + retry

---

## Next

**SE approvato:**
1. Creare migration `043_fiscal_invoices.sql`
2. Implementare validator (`invoice_validator.py`)
3. Implementare sequence manager con retry logic
4. Test concorrenza (2 INSERT simultanei)

**Domande per Rafa:**
- Path cartella export SPRING? (es: `/srv/spring/inbox/`)
- Dati hotel (P.IVA, CF, indirizzo) → da settings o hardcoded?
- Gestione sezionali multipli futuri? (es: NL, BAR, SPA)
