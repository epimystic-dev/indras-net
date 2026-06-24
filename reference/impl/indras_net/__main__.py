# SPDX-License-Identifier: Apache-2.0
"""Enable ``python -m indras_net ...`` to invoke the CLI."""
from __future__ import annotations

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
