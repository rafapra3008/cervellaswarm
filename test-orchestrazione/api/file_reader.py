"""
File reader module for CervellaSwarm test orchestration.

This module demonstrates graceful error handling when attempting
to read files that may not exist.
"""

import json
from typing import Any


def read_config(path: str = "/path/che/non/esiste/config.json") -> dict[str, Any]:
    """
    Attempt to read a JSON config file with graceful error handling.

    This function tries to read a JSON configuration file from the specified
    path. If the file does not exist or cannot be read, it returns a fallback
    configuration instead of crashing.

    Args:
        path: The path to the config file. Defaults to a non-existent path
              for testing purposes.

    Returns:
        dict: The parsed JSON config if successful, or a fallback dict with:
            - "error": Description of what went wrong
            - "fallback": Indicator that default config is being used

    Example:
        >>> result = read_config()  # File doesn't exist
        >>> result["error"]
        'File not found'
        >>> result["fallback"]
        'default_config'

        >>> result = read_config("/path/to/real/config.json")  # If file exists
        >>> # Returns parsed JSON content
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": "File not found", "fallback": "default_config"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON format", "fallback": "default_config"}
    except PermissionError:
        return {"error": "Permission denied", "fallback": "default_config"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "fallback": "default_config"}
