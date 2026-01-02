-- Migration 002: Lessons Learned Extended Schema
-- Aggiunge colonne avanzate alla tabella lessons_learned
-- Data: 2026-01-02

-- ===== COLONNE AGGIUNTIVE PER LESSONS_LEARNED =====

-- Categorizzazione
ALTER TABLE lessons_learned ADD COLUMN category TEXT;
ALTER TABLE lessons_learned ADD COLUMN severity TEXT DEFAULT 'MEDIUM';

-- Analisi root cause
ALTER TABLE lessons_learned ADD COLUMN root_cause TEXT;
ALTER TABLE lessons_learned ADD COLUMN prevention TEXT;

-- Metriche
ALTER TABLE lessons_learned ADD COLUMN time_wasted_minutes INTEGER;
ALTER TABLE lessons_learned ADD COLUMN occurrence_count INTEGER DEFAULT 1;

-- Stato e relazioni
ALTER TABLE lessons_learned ADD COLUMN status TEXT DEFAULT 'ACTIVE';
ALTER TABLE lessons_learned ADD COLUMN related_pattern_id INTEGER;
ALTER TABLE lessons_learned ADD COLUMN project TEXT;

-- v1.2.0 - Continuous Learning
ALTER TABLE lessons_learned ADD COLUMN trigger TEXT;
ALTER TABLE lessons_learned ADD COLUMN example TEXT;
ALTER TABLE lessons_learned ADD COLUMN tags TEXT;
ALTER TABLE lessons_learned ADD COLUMN related_patterns TEXT;
ALTER TABLE lessons_learned ADD COLUMN auto_generated INTEGER DEFAULT 0;
ALTER TABLE lessons_learned ADD COLUMN last_applied TEXT;

-- ===== INDICI PER CONTINUOUS LEARNING =====
CREATE INDEX IF NOT EXISTS idx_lessons_tags ON lessons_learned(tags);
CREATE INDEX IF NOT EXISTS idx_lessons_trigger ON lessons_learned(trigger);
