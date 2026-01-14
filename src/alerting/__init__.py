"""
CervellaSwarm Alerting System
=============================

Sistema di alerting per monitoraggio errori e pattern critici.

Componenti:
- alert_system.py: Core del sistema
- detectors.py: Pattern detection
- notifiers/: Canali di notifica (console, file, slack)

Uso:
    from src.alerting import AlertSystem

    alerts = AlertSystem()
    alerts.check_recent_errors()  # Check ultimi errori
    alerts.start_monitoring()     # Avvia monitoring continuo

Versione: 1.0.0
Data: 14 Gennaio 2026
"""

from .alert_system import AlertSystem
from .detectors import PatternDetector

__all__ = ['AlertSystem', 'PatternDetector']
__version__ = '1.0.0'
