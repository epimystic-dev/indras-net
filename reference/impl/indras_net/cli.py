# SPDX-License-Identifier: Apache-2.0
"""Indra's Net reference CLI (Phase 0): a thin, honest entrypoint over the deterministic harness.

Phase 0 wires packaging + a command surface around the reference spine. The model is
still the reproducible, no-network ``DeterministicMockModel``; a real (local or remote)
model adapter arrives in Phase 1 (see ``docs/IMPLEMENTATION_ROADMAP.md``). Whatever the
model proposes, every effect is gated by the deterministic floor and recorded in the
tamper-evident ledger — that is the load-bearing part this CLI exposes.
"""
from __future__ import annotations

import argparse
import typing

from . import __version__

_TAGLINE = "[a green decision is 'origin-valid, content-unverified' -- never 'verified-safe']"


def _cmd_version(args: argparse.Namespace) -> int:
    print("indras-net " + __version__)
    return 0


def _cmd_scenarios(args: argparse.Namespace) -> int:
    from .demo import SCENARIOS

    print("scenarios: " + ", ".join(["all", *SCENARIOS.keys()]))
    return 0


def _cmd_demo(args: argparse.Namespace) -> int:
    from .demo import main as demo_main

    return demo_main(["--scenario", args.scenario])


def _cmd_run(args: argparse.Namespace) -> int:
    """Run a single task through a mock-model swarm and print the gated outcome + audit summary."""
    from .demo import _make_swarm  # reuse the reference swarm factory

    swarm, ledger = _make_swarm(scripted={}, with_steward=True)
    context = {"untrusted_input": True} if args.untrusted else {"input_trust_label": "trusted:audited"}
    result = swarm.run(args.task, context)

    print("task: " + args.task)
    print("model: DeterministicMockModel (Phase 0 -- no real model yet; see docs/IMPLEMENTATION_ROADMAP.md)")
    print("-" * 70)
    for i, occ in enumerate(result.occasion_results):
        decision = occ.decision.decision.name if occ.decision else "n/a"
        tier = occ.decision.tier_hit.name if (occ.decision and occ.decision.tier_hit) else "-"
        print(
            "  occasion[%d] role=%s effect=%s decision=%s tier=%s executed=%s"
            % (i, occ.agent_role, occ.effect_id, decision, tier, occ.executed)
        )
        if occ.output is not None:
            print("             output: " + str(occ.output))
    print("-" * 70)
    print("audit leaves: %d   verify(): %s   halted: %s" % (len(ledger), ledger.verify(), result.halted))
    if result.health is not None:
        print("health: %s  %s" % (result.health.status.name, list(result.health.reasons)))
    print("\n" + _TAGLINE)
    return 0


def main(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="indras-net",
        description="Indra's Net -- reference harness for ethical swarm intelligence (Phase 0 CLI).",
        epilog="The model only proposes; a deterministic harness disposes. Verify the cage, not the animal.",
    )
    parser.add_argument("--version", action="version", version="indras-net " + __version__)
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p_demo = sub.add_parser("demo", help="run the end-to-end demonstration scenarios")
    p_demo.add_argument(
        "--scenario", default="all", help="which scenario to run (default: all); see `indras-net scenarios`"
    )
    p_demo.set_defaults(func=_cmd_demo)

    p_run = sub.add_parser("run", help="run a single task through the gated harness (mock model in Phase 0)")
    p_run.add_argument("task", help="the task for the swarm to attempt")
    p_run.add_argument(
        "--untrusted",
        action="store_true",
        help="mark the input as untrusted (exercises the Rule-of-Two / quarantine path)",
    )
    p_run.set_defaults(func=_cmd_run)

    sub.add_parser("scenarios", help="list the available demo scenarios").set_defaults(func=_cmd_scenarios)
    sub.add_parser("version", help="print the version").set_defaults(func=_cmd_version)

    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
