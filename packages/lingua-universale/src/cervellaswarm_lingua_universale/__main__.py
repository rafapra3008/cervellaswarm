# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 CervellaSwarm Contributors

"""Allow ``python -m cervellaswarm_lingua_universale`` to invoke the CLI."""

import sys

from ._cli import main

sys.exit(main())
