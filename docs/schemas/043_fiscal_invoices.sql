-- ============================================
-- Migration 043: Fiscal Invoices (Fatture XML)
-- ============================================
-- Sessione 268 - 19 Gennaio 2026
--
-- Sistema per Fatture Elettroniche FatturaPA
-- 1. fiscal_invoices - fatture generate
-- 2. fiscal_sequences - numerazione progressiva (opzionale)
-- 3. Indici per performance e integrità
--
-- NOTA: XML generato con python-a38, export verso SPRING
-- ============================================

-- ============================================
-- 1. FISCAL_INVOICES - Fatture Elettroniche
-- ============================================

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

-- ============================================
-- 2. INDICI
-- ============================================

-- Prevenire duplicati numero fattura (CRITICO per concorrenza)
CREATE UNIQUE INDEX IF NOT EXISTS idx_fiscal_invoices_number_sezionale
    ON fiscal_invoices(invoice_number, sezionale, fiscal_year);

-- Performance query
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

-- ============================================
-- 3. TRIGGER: Auto-update timestamp
-- ============================================

CREATE TRIGGER IF NOT EXISTS fiscal_invoices_update_timestamp
AFTER UPDATE ON fiscal_invoices
FOR EACH ROW
BEGIN
    UPDATE fiscal_invoices
    SET updated_at = datetime('now')
    WHERE id = OLD.id;
END;

-- ============================================
-- 4. FISCAL_SEQUENCES (Opzionale)
-- ============================================
-- Tabella per gestione atomica sequenze
-- Usare SOLO se si preferisce sequence table vs optimistic locking

CREATE TABLE IF NOT EXISTS fiscal_sequences (
    sezionale TEXT NOT NULL,
    fiscal_year INTEGER NOT NULL,
    last_number INTEGER DEFAULT 0,
    version INTEGER DEFAULT 1,

    PRIMARY KEY (sezionale, fiscal_year)
);

-- Seed sezionale NL per 2026
INSERT OR IGNORE INTO fiscal_sequences (sezionale, fiscal_year, last_number)
VALUES ('NL', 2026, 199);  -- Partirà da 200

-- ============================================
-- 5. VIEW: Invoice Dashboard
-- ============================================

CREATE VIEW IF NOT EXISTS v_fiscal_invoices_dashboard AS
SELECT
    fi.id,
    fi.invoice_number,
    fi.sezionale,
    fi.invoice_date,
    fi.customer_name,
    fi.customer_vat,
    fi.total_amount,
    fi.status,
    fi.sdi_status,
    fi.voided,

    -- Link booking (se presente)
    b.confirmation_code,
    b.check_in_date,
    b.check_out_date,

    -- Link payment (se presente)
    p.payment_method,
    p.payment_date

FROM fiscal_invoices fi
LEFT JOIN bookings b ON fi.booking_id = b.id
LEFT JOIN payments p ON fi.payment_id = p.id
WHERE fi.voided = 0
ORDER BY fi.invoice_date DESC, fi.invoice_number DESC;

-- ============================================
-- DONE!
-- ============================================
