"""
CervellaSwarm Weekly Retrospective - Modular Edition

Moduli:
- sections: Funzioni di estrazione dati (metriche, pattern, lezioni)
- output: Funzioni di rendering (rich/plain/markdown)
- suggestions: suggest_new_lessons()
- cli: Entry point CLI e generate_retro()
"""

__version__ = "2.2.0"
__version_date__ = "2026-02-04"

from .suggestions import suggest_new_lessons
from .cli import generate_retro, save_report

__all__ = [
    "generate_retro",
    "suggest_new_lessons",
    "save_report",
]
