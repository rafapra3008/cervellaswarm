-- Migration 001: Initial Schema
-- Crea le tabelle base del sistema memoria CervellaSwarm
-- Data: 2026-01-02

-- ===== TABELLA SWARM_EVENTS =====
CREATE TABLE IF NOT EXISTS swarm_events (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    session_id TEXT,
    event_type TEXT NOT NULL,

    -- Agent info
    agent_name TEXT,
    agent_role TEXT,

    -- Task info
    task_id TEXT,
    parent_task_id TEXT,
    task_description TEXT,
    task_status TEXT,

    -- Execution
    duration_ms INTEGER,
    success INTEGER,
    error_message TEXT,

    -- Context
    project TEXT,
    files_modified TEXT,

    -- Metadata
    tags TEXT,
    notes TEXT,

    created_at TEXT DEFAULT (datetime('now'))
);

-- ===== INDICI PER SWARM_EVENTS =====
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON swarm_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_events_agent ON swarm_events(agent_name);
CREATE INDEX IF NOT EXISTS idx_events_project ON swarm_events(project);
CREATE INDEX IF NOT EXISTS idx_events_task_status ON swarm_events(task_status);
CREATE INDEX IF NOT EXISTS idx_events_session ON swarm_events(session_id);

-- ===== TABELLA LESSONS_LEARNED (BASE) =====
CREATE TABLE IF NOT EXISTS lessons_learned (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    context TEXT,
    problem TEXT,
    solution TEXT,
    pattern TEXT,
    agents_involved TEXT,
    confidence REAL DEFAULT 0.5,
    times_applied INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

-- ===== INDICI PER LESSONS_LEARNED =====
CREATE INDEX IF NOT EXISTS idx_lessons_confidence ON lessons_learned(confidence DESC);
CREATE INDEX IF NOT EXISTS idx_lessons_pattern ON lessons_learned(pattern);
