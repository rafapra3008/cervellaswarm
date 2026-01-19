"""Pytest configuration for test suite.

Author: Cervella Tester
Date: 2026-01-19
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
