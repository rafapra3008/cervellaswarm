#!/usr/bin/env python3
"""
Endpoint API: Countdown Evento
Calcola i giorni rimanenti fino a un evento specifico.
"""

__version__ = "1.0.0"
__version_date__ = "2026-01-01"

from datetime import datetime, date
import json


def get_countdown(target_date: str, event_name: str = "Evento") -> dict:
    """
    Calcola i giorni rimanenti fino a una data target.

    Args:
        target_date (str): Data target in formato "YYYY-MM-DD"
        event_name (str): Nome dell'evento (default: "Evento")

    Returns:
        dict: {
            "days_remaining": int,     # Negativo se data passata
            "target_date": str,        # Data formattata "YYYY-MM-DD"
            "event_name": str,         # Nome evento
            "is_past": bool,           # True se data passata
            "is_today": bool           # True se data è oggi
        }

    Raises:
        ValueError: Se target_date non è in formato valido "YYYY-MM-DD"
    """
    try:
        # Parse della data target
        target = datetime.strptime(target_date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            f"Data invalida '{target_date}'. Formato richiesto: YYYY-MM-DD"
        )

    # Data corrente (senza ora)
    today = date.today()

    # Calcola differenza in giorni
    delta = target - today
    days_remaining = delta.days

    # Determina stato
    is_past = days_remaining < 0
    is_today = days_remaining == 0

    return {
        "days_remaining": days_remaining,
        "target_date": target_date,
        "event_name": event_name,
        "is_past": is_past,
        "is_today": is_today
    }


def handle_request(target_date: str = None, event_name: str = "Evento") -> str:
    """
    Handler principale per l'endpoint GET /api/countdown.

    Args:
        target_date (str): Data target in formato "YYYY-MM-DD"
        event_name (str): Nome dell'evento (default: "Evento")

    Returns:
        str: JSON response con dati countdown

    Example Response:
        {
            "status": "success",
            "data": {
                "days_remaining": 364,
                "target_date": "2026-12-31",
                "event_name": "Fine Anno",
                "is_past": false,
                "is_today": false
            }
        }
    """
    try:
        # Validazione input
        if not target_date:
            raise ValueError("Parametro 'target_date' obbligatorio")

        # Calcola countdown
        result = get_countdown(target_date, event_name)

        # Response di successo
        response = {
            "status": "success",
            "data": result
        }
        return json.dumps(response, ensure_ascii=False, indent=2)

    except Exception as e:
        # Response di errore
        error_response = {
            "status": "error",
            "message": str(e)
        }
        return json.dumps(error_response, ensure_ascii=False, indent=2)


# Test manuale (esegui questo file direttamente)
if __name__ == "__main__":
    print("=== Test Endpoint Countdown ===\n")

    # Test casi principali
    test_cases = [
        # (target_date, event_name, descrizione)
        ("2026-12-31", "Fine Anno 2026", "Evento futuro"),
        ("2026-01-01", "Oggi", "Evento oggi"),
        ("2025-12-31", "Fine Anno 2025", "Evento passato"),
        ("2026-06-15", "Metà Anno", "Evento tra qualche mese"),
    ]

    for target_date, event_name, descrizione in test_cases:
        print(f"--- {descrizione} ---")
        response = handle_request(target_date, event_name)
        print(response)
        print()

    # Test caso errore (data invalida)
    print("--- Test Errore: Data Invalida ---")
    response = handle_request("invalid-date", "Test Errore")
    print(response)
    print()

    # Test caso errore (target_date mancante)
    print("--- Test Errore: Parametro Mancante ---")
    response = handle_request(None, "Test Errore")
    print(response)
