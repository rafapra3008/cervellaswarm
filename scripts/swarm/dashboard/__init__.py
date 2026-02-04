"""
CervellaSwarm Dashboard - Package
Monitoring in tempo reale dello sciame.
"""

__version__ = "2.3.0"
__version_date__ = "2026-02-04"

from .data import (
    get_worker_status,
    get_task_description,
    get_task_queue_stats,
    get_recent_activity,
    calculate_session_duration,
    get_live_activity_from_heartbeat,
    get_system_resources,
    get_stuck_workers,
)

from .render import (
    render_header,
    render_workers,
    render_stats,
    render_activity,
    render_heartbeat,
    render_resources,
    render_alerts,
    render_footer,
    render_dashboard,
    render_json,
)

from .cli import (
    main,
    clear_screen,
)

__all__ = [
    # Data layer
    'get_worker_status',
    'get_task_description',
    'get_task_queue_stats',
    'get_recent_activity',
    'calculate_session_duration',
    'get_live_activity_from_heartbeat',
    'get_system_resources',
    'get_stuck_workers',
    # Render layer
    'render_header',
    'render_workers',
    'render_stats',
    'render_activity',
    'render_heartbeat',
    'render_resources',
    'render_alerts',
    'render_footer',
    'render_dashboard',
    'render_json',
    # CLI layer
    'main',
    'clear_screen',
]
