"""
CervellaSwarm Compaction - Configurazione per ruolo.

Ogni ruolo dello swarm ha configurazioni di compaction diverse
basate su quanto context tipicamente consumano.

Versione: 1.0.0
Data: 2026-02-10 - Sessione 339 (FASE 3.1)

NOTA: Compaction API e' BETA (compact-2026-01-12), solo Opus 4.6.
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-10"

from typing import Optional, Literal

Role = Literal["regina", "guardiana", "worker", "architect", "ingegnera", "security"]

BETA_HEADER = "compact-2026-01-12"
COMPACTION_TYPE = "compact_20260112"

# Istruzioni custom per ogni ruolo - preservano info critiche
REGINA_INSTRUCTIONS = """Crea un summary COMPLETO preservando:
1. DECISIONI PRESE - con motivazioni (PERCHE')
2. FILE MODIFICATI - path + cosa cambiato
3. STATO TASK - completati, in corso, bloccati
4. PROBLEMI RISOLTI - bug + soluzioni
5. PROSSIMI STEP - azioni rimanenti
6. PATTERN IMPORTANTI - scope, architetture, convenzioni

Formato: <summary></summary> block.
Scrivi come se la prossima Cervella non sapesse NULLA della sessione."""

GUARDIANA_INSTRUCTIONS = """Crea summary preservando:
1. SCOPE del task ricevuto
2. VALIDAZIONI eseguite (pass/fail + perche')
3. FILE analizzati e problemi trovati
4. RACCOMANDAZIONI date
5. FEEDBACK sulla qualita'

Stile conciso, bullet points. <summary></summary> block."""

ARCHITECT_INSTRUCTIONS = """Crea summary preservando:
1. ANALISI completata (file, moduli, dipendenze)
2. PIANO proposto con PERCHE'
3. RISCHI identificati
4. DECISIONI architetturali
5. PROSSIMI STEP implementativi

Include snippet di codice chiave. <summary></summary> block."""

SECURITY_INSTRUCTIONS = """Crea summary preservando:
1. VULNERABILITA' trovate (severity + path)
2. FIX raccomandati
3. FILE analizzati
4. COMPLIANCE check risultati
5. AUDIT trail

Nessun dato sensibile nel summary! <summary></summary> block."""

# Configurazione per ruolo
COMPACTION_CONFIG = {
    "regina": {
        "enabled": True,
        "trigger": 100_000,
        "pause_after": True,
        "instructions": REGINA_INSTRUCTIONS,
    },
    "guardiana": {
        "enabled": True,
        "trigger": 80_000,
        "pause_after": False,
        "instructions": GUARDIANA_INSTRUCTIONS,
    },
    "worker": {
        "enabled": False,  # Sonnet non supporta compaction
    },
    "architect": {
        "enabled": True,
        "trigger": 120_000,
        "pause_after": True,
        "instructions": ARCHITECT_INSTRUCTIONS,
    },
    "ingegnera": {
        "enabled": True,
        "trigger": 80_000,
        "pause_after": False,
        "instructions": GUARDIANA_INSTRUCTIONS,  # Simile a guardiana
    },
    "security": {
        "enabled": True,
        "trigger": 80_000,
        "pause_after": False,
        "instructions": SECURITY_INSTRUCTIONS,
    },
}


def get_compaction_config(role: Role) -> Optional[dict]:
    """Crea context_management config per il ruolo.

    Args:
        role: Ruolo dello swarm agent

    Returns:
        dict con context_management config, o None se disabilitato
    """
    config = COMPACTION_CONFIG.get(role)
    if not config or not config.get("enabled"):
        return None

    return {
        "edits": [
            {
                "type": COMPACTION_TYPE,
                "trigger": {"type": "input_tokens", "value": config["trigger"]},
                "pause_after_compaction": config["pause_after"],
                "instructions": config["instructions"],
            }
        ]
    }


def get_beta_headers() -> list:
    """Ritorna i beta headers necessari per compaction."""
    return [BETA_HEADER]
