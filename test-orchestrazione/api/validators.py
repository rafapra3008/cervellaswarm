"""
Validators module - Funzioni di validazione per l'API.

Questo modulo contiene funzioni di validazione riutilizzabili
per input utente e dati API.
"""

import re


def validate_name(name: str) -> bool:
    """
    Valida un nome secondo i criteri standard.

    Criteri di validazione:
    - Nome non deve essere vuoto o contenere solo spazi
    - Nome non deve superare 100 caratteri
    - Nome deve contenere solo lettere, spazi e trattini

    Args:
        name: Il nome da validare

    Returns:
        True se il nome e valido, False altrimenti

    Examples:
        >>> validate_name("Mario Rossi")
        True
        >>> validate_name("Anna-Maria")
        True
        >>> validate_name("")
        False
        >>> validate_name("John123")
        False
        >>> validate_name("A" * 101)
        False
    """
    # Check: nome non vuoto
    if not name or not name.strip():
        return False

    # Check: lunghezza max 100 caratteri
    if len(name) > 100:
        return False

    # Check: solo lettere (incluse accentate), spazi e trattini
    # Pattern: lettere unicode, spazi, trattini
    pattern = r'^[a-zA-ZàèéìòùÀÈÉÌÒÙäëïöüÄËÏÖÜáéíóúÁÉÍÓÚñÑçÇ\s\-]+$'
    if not re.match(pattern, name):
        return False

    return True
