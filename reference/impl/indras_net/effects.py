# SPDX-License-Identifier: Apache-2.0
"""Typed-effect lattice and deny-default criticality table (the resource-independent name of what may be done)."""

from __future__ import annotations

import dataclasses
import enum
import re
import typing

# Effect-id grammar (matches the policy-decision schema EffectId pattern):
# a reverse-DNS-style typed id, e.g. "fs.write.workspace". NOT a tool name, NOT a secret.
_EFFECT_ID_RE = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$")


class Criticality(enum.Enum):
    """Criticality tier (doc-08 criticality resolver). Orderable via .value for UPWARD resolution.

    Ambiguity resolves upward (fail-up); an unknown capability resolves to IRREVERSIBLE.
    """

    ROUTINE = 1
    SENSITIVE = 2
    CRITICAL = 3
    IRREVERSIBLE = 4


@dataclasses.dataclass(frozen=True)
class Effect:
    """A typed effect: the resource-independent NAME of what may be done.

    Carries criticality plus the two Rule-of-Two structural flags
    (``sensitive_capability``, ``state_change``) and a reversibility bit. ``gloss`` is a
    plain-language coordination note, never authority.
    """

    effect_id: str
    criticality: Criticality
    sensitive_capability: bool
    state_change: bool
    reversible: bool
    gloss: str

    def __post_init__(self) -> None:
        if not isinstance(self.effect_id, str) or not _EFFECT_ID_RE.match(self.effect_id):
            raise ValueError(f"malformed effect_id: {self.effect_id!r}")
        if not isinstance(self.criticality, Criticality):
            raise ValueError("criticality must be a Criticality")


class EffectRegistry:
    """A registry of known effects with a deny-default / fail-up resolver.

    ``resolve`` NEVER returns ``None``: an unregistered effect-id resolves to a synthetic,
    maximally-restrictive Effect (IRREVERSIBLE, sensitive, state-changing, irreversible). The
    floor therefore treats unknown capabilities as the most dangerous, never the least.
    """

    def __init__(self, effects: typing.Iterable[Effect] = ()) -> None:
        self._effects: dict[str, Effect] = {}
        for effect in effects:
            self.register(effect)

    def register(self, effect: Effect) -> None:
        if not isinstance(effect, Effect):
            raise ValueError("register expects an Effect instance")
        if not _EFFECT_ID_RE.match(effect.effect_id):
            raise ValueError(f"malformed effect_id: {effect.effect_id!r}")
        self._effects[effect.effect_id] = effect

    def get(self, effect_id: str) -> typing.Optional[Effect]:
        return self._effects.get(effect_id)

    def known(self, effect_id: str) -> bool:
        return effect_id in self._effects

    def resolve(self, effect_id: str) -> Effect:
        """Return the registered Effect, or a fail-up synthetic for any unregistered id."""
        existing = self._effects.get(effect_id)
        if existing is not None:
            return existing
        synthetic_id = effect_id if _EFFECT_ID_RE.match(str(effect_id) or "") else "unknown.capability"
        return Effect(
            effect_id=synthetic_id,
            criticality=Criticality.IRREVERSIBLE,
            sensitive_capability=True,
            state_change=True,
            reversible=False,
            gloss="unknown-capability:fail-up",
        )


def _seed_registry() -> EffectRegistry:
    """Pre-seed the demo lattice. These are coordination semantics, not vendor tools."""
    return EffectRegistry(
        [
            Effect(
                effect_id="analysis.summarize",
                criticality=Criticality.ROUTINE,
                sensitive_capability=False,
                state_change=False,
                reversible=True,
                gloss="read-and-summarize; no external state touched",
            ),
            Effect(
                effect_id="audit.append",
                criticality=Criticality.SENSITIVE,
                sensitive_capability=True,
                state_change=True,
                reversible=True,
                gloss="append a ledger leaf (Chitragupta-exclusive by policy)",
            ),
            Effect(
                effect_id="fs.write.workspace",
                criticality=Criticality.SENSITIVE,
                sensitive_capability=True,
                state_change=True,
                reversible=True,
                gloss="write within the agent's own workspace scope",
            ),
            Effect(
                effect_id="net.egress.http",
                criticality=Criticality.CRITICAL,
                sensitive_capability=True,
                state_change=False,
                reversible=True,
                gloss="outbound network read over an allowlisted domain",
            ),
            Effect(
                effect_id="code.deploy.production",
                criticality=Criticality.IRREVERSIBLE,
                sensitive_capability=True,
                state_change=True,
                reversible=False,
                gloss="promote code to production (irreversible blast radius)",
            ),
            Effect(
                effect_id="replicate.spawn",
                criticality=Criticality.IRREVERSIBLE,
                sensitive_capability=True,
                state_change=True,
                reversible=False,
                gloss="self-replication (INERT/forbidden in this MVP)",
            ),
        ]
    )


# Module singleton, pre-seeded with the demo lattice.
EFFECT_REGISTRY: EffectRegistry = _seed_registry()
