-- Migration 003: Error Patterns Table
-- Crea la tabella per tracciare pattern di errori ricorrenti
-- Data: 2026-01-02

-- ===== TABELLA ERROR_PATTERNS =====
CREATE TABLE IF NOT EXISTS error_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_name TEXT UNIQUE NOT NULL,
    pattern_type TEXT NOT NULL,
    first_seen TEXT NOT NULL,
    last_seen TEXT NOT NULL,
    occurrence_count INTEGER DEFAULT 1,
    severity_level TEXT DEFAULT 'MEDIUM',
    error_signature TEXT,
    affected_agents TEXT,
    affected_files TEXT,
    root_cause_hypothesis TEXT,
    mitigation_applied INTEGER DEFAULT 0,
    mitigation_description TEXT,
    status TEXT DEFAULT 'ACTIVE'
);

-- ===== INDICI PER ERROR_PATTERNS =====
CREATE INDEX IF NOT EXISTS idx_patterns_severity ON error_patterns(severity_level);
CREATE INDEX IF NOT EXISTS idx_patterns_status ON error_patterns(status);
