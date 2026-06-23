# SPDX-License-Identifier: Apache-2.0
"""Least-privilege identity: a DID bound to a role and a typed capability-grant allowlist (authority is the grant set, never prose)."""

from __future__ import annotations

import dataclasses
import enum
import typing

# Governance root DID. Capability-bearing grants must be issued by this authority,
# never self-issued by the agent (privilege-escalation guard, enforced at the floor).
GOVERNANCE_DID: str = "did:web:indras-net.governance"


class RiskClass(enum.Enum):
    """Human-oversight binding (doc-00 risk classes). Orderable via .value; assignment defaults UP.

    A = agent-alone (post-hoc) .. D = human-authorizes-per-action.
    """

    A = 1
    B = 2
    C = 3
    D = 4


@dataclasses.dataclass(frozen=True)
class CapabilityGrant:
    """A single typed grant: one effect-id, its risk ceiling, and WHO granted it.

    ``granted_by_did`` must be the governance authority, never the agent itself.
    ``names_constraint_relaxed`` makes the relaxed least-privilege boundary auditable
    (doc-01 mandatory field). ``falsifier`` is an optional deterministic revoke-check.
    """

    effect_id: str
    granted_risk_class: RiskClass
    granted_by_did: str
    names_constraint_relaxed: str
    falsifier: typing.Optional[str] = None


@dataclasses.dataclass(frozen=True)
class Identity:
    """A durable identity record: a DID + role bound to a typed capability-grant set.

    Authority over what this identity MAY do comes ENTIRELY from ``grants`` (an effect-id
    allowlist) bounded by ``risk_class_ceiling`` — never from ``role`` or any prose string.
    ``accountable_human`` is non-removable (no persona unmoored from a human).
    ``model_family`` supports the diversity floor (model-family heterogeneity).
    """

    did: str
    role: str
    role_gloss: str
    grants: typing.Tuple[CapabilityGrant, ...]
    risk_class_ceiling: RiskClass
    model_family: str
    accountable_human: str
    escalation_did: typing.Optional[str] = None

    def __post_init__(self) -> None:
        if not self.did:
            raise ValueError("Identity.did must be non-empty")
        if not self.accountable_human:
            raise ValueError("Identity.accountable_human must be non-empty (no persona unmoored)")
        if not isinstance(self.risk_class_ceiling, RiskClass):
            raise ValueError("risk_class_ceiling must be a RiskClass")
        # Normalize grants to a tuple so the frozen dataclass stays hashable and immutable.
        object.__setattr__(self, "grants", tuple(self.grants))

    def grants_effect(self, effect_id: str) -> bool:
        """True iff some grant names exactly this effect-id (deny-default: absence is denial)."""
        return any(g.effect_id == effect_id for g in self.grants)

    def grant_for(self, effect_id: str) -> typing.Optional[CapabilityGrant]:
        for g in self.grants:
            if g.effect_id == effect_id:
                return g
        return None

    def is_self_issued(self) -> bool:
        """True iff any grant was issued by this identity itself (privilege-escalation guard).

        The floor rejects a self-issued identity at the identity-integrity tier: an agent
        cannot mint its own authority.
        """
        return any(g.granted_by_did == self.did for g in self.grants)
