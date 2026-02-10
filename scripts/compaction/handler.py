"""
CervellaSwarm Compaction - Handler per compaction responses.

Gestisce il flusso di compaction: detect, preserve, continue.

Versione: 1.0.0
Data: 2026-02-10 - Sessione 339 (FASE 3.1)
"""

__version__ = "1.0.0"
__version_date__ = "2026-02-10"

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def handle_compaction_response(response, messages: list, preserve_last_n: int = 2) -> list:
    """Gestisce una response con compaction block.

    Se la response ha stop_reason == "compaction":
    1. Estrae il compaction block
    2. Preserva gli ultimi N messaggi
    3. Ricostruisce la lista messaggi

    Args:
        response: Response dalla API Anthropic
        messages: Lista messaggi corrente
        preserve_last_n: Quanti messaggi recenti preservare

    Returns:
        Lista messaggi aggiornata (compacted + preserved)
    """
    if response.stop_reason != "compaction":
        # Nessuna compaction, appendi normalmente
        messages.append({"role": "assistant", "content": response.content})
        return messages

    logger.info("Compaction detected! Rebuilding message list...")

    # Estrai compaction block
    compaction_block = response.content[0]

    # Preserva ultimi N messaggi
    preserved = messages[-preserve_last_n:] if len(messages) >= preserve_last_n else messages[:]

    # Ricostruisci: compaction + preserved
    new_messages = [
        {"role": "assistant", "content": [compaction_block]},
        *preserved,
    ]

    logger.info(
        "Compaction complete: %d messages -> %d messages (%d preserved)",
        len(messages),
        len(new_messages),
        len(preserved),
    )

    return new_messages


def extract_compaction_usage(response) -> Optional[dict]:
    """Estrae le metriche di usage dalla compaction.

    Returns:
        Dict con metriche, o None se no compaction
    """
    usage = response.usage
    if not hasattr(usage, "iterations"):
        return None

    iterations = usage.iterations or []
    compaction_iters = [i for i in iterations if i.get("type") == "compaction"]
    message_iters = [i for i in iterations if i.get("type") == "message"]

    if not compaction_iters:
        return None

    total_input = sum(i.get("input_tokens", 0) for i in iterations)
    total_output = sum(i.get("output_tokens", 0) for i in iterations)

    return {
        "compaction_count": len(compaction_iters),
        "compaction_input_tokens": sum(i.get("input_tokens", 0) for i in compaction_iters),
        "compaction_output_tokens": sum(i.get("output_tokens", 0) for i in compaction_iters),
        "message_input_tokens": sum(i.get("input_tokens", 0) for i in message_iters),
        "message_output_tokens": sum(i.get("output_tokens", 0) for i in message_iters),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
    }
