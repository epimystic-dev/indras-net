# SPDX-License-Identifier: Apache-2.0
"""Convenience entrypoint — `python run_demo.py [--scenario {all,happy,floor,tamper,confine,halt,closeloop}]`.

The demonstration now lives in the installable package at ``indras_net.demo`` so the
``indras-net`` CLI (``indras-net demo``) can invoke it. This script is a thin shim that
forwards to it, so the historical ``python run_demo.py`` invocation keeps working from a
source checkout with no install required.
"""
from __future__ import annotations

from indras_net.demo import main

if __name__ == "__main__":
    raise SystemExit(main())
