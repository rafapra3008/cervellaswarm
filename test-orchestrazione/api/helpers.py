"""
Helpers module - Funzioni di utilita per l'API.

Questo modulo contiene funzioni helper riutilizzabili
per formattazione e manipolazione dati.
"""

import re
import unicodedata
from datetime import datetime


def format_date(date: datetime) -> str:
    """
    Formatta una data nel formato DD/MM/YYYY.

    Args:
        date: Oggetto datetime da formattare

    Returns:
        Stringa con data formattata come "DD/MM/YYYY"

    Examples:
        >>> from datetime import datetime
        >>> format_date(datetime(2026, 1, 4))
        '04/01/2026'
        >>> format_date(datetime(2025, 12, 25))
        '25/12/2025'
    """
    return date.strftime("%d/%m/%Y")


def format_currency(amount: float, symbol: str = "EUR") -> str:
    """
    Formatta un importo monetario con simbolo valuta.

    Usa il formato europeo: punto per migliaia, virgola per decimali.

    Args:
        amount: Importo numerico da formattare
        symbol: Simbolo valuta (default: "EUR")

    Returns:
        Stringa formattata come "SYMBOL X.XXX,XX"

    Examples:
        >>> format_currency(1234.56)
        'EUR 1.234,56'
        >>> format_currency(1000000, "USD")
        'USD 1.000.000,00'
        >>> format_currency(99.9, "GBP")
        'GBP 99,90'
    """
    # Formatta con 2 decimali
    formatted = f"{amount:,.2f}"
    # Converti da formato US (1,234.56) a formato EU (1.234,56)
    # Prima sostituisci virgole con placeholder, poi punti con virgole, poi placeholder con punti
    formatted = formatted.replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{symbol} {formatted}"


def truncate_string(text: str, max_length: int = 50) -> str:
    """
    Tronca una stringa aggiungendo "..." se supera la lunghezza massima.

    Args:
        text: Testo da troncare
        max_length: Lunghezza massima (default: 50)

    Returns:
        Stringa troncata con "..." se necessario, altrimenti originale

    Examples:
        >>> truncate_string("Hello World", 50)
        'Hello World'
        >>> truncate_string("Hello World", 5)
        'Hello...'
        >>> truncate_string("Test", 4)
        'Test'
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def capitalize_words(text: str) -> str:
    """
    Rende maiuscola la prima lettera di ogni parola.

    Args:
        text: Testo da trasformare

    Returns:
        Stringa con prima lettera di ogni parola maiuscola

    Examples:
        >>> capitalize_words("hello world")
        'Hello World'
        >>> capitalize_words("MARIO ROSSI")
        'Mario Rossi'
        >>> capitalize_words("anna-maria")
        'Anna-Maria'
    """
    # Usa title() ma gestisce anche i trattini
    return "-".join(word.title() for word in text.split("-"))


def slugify(text: str) -> str:
    """
    Converte una stringa in slug URL-friendly.

    Trasforma in lowercase, rimuove accenti, sostituisce spazi e
    caratteri speciali con trattini.

    Args:
        text: Testo da convertire in slug

    Returns:
        Slug URL-friendly (lowercase, solo lettere/numeri/trattini)

    Examples:
        >>> slugify("Hello World")
        'hello-world'
        >>> slugify("Caffè Italiano!")
        'caffe-italiano'
        >>> slugify("  Multiple   Spaces  ")
        'multiple-spaces'
        >>> slugify("Test@#$%Special")
        'test-special'
    """
    # Normalizza unicode (rimuove accenti)
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Converti in lowercase
    text = text.lower()

    # Sostituisci tutto cio che non e lettera/numero con trattino
    text = re.sub(r'[^a-z0-9]+', '-', text)

    # Rimuovi trattini multipli
    text = re.sub(r'-+', '-', text)

    # Rimuovi trattini iniziali e finali
    text = text.strip('-')

    return text
