# SPDX-License-Identifier: Apache-2.0
"""Persona genome (signed, boot-checked): the floor is non-strippable BY CONSTRUCTION.

A persona is born from a signed triad with two regions:

* an INVARIANT region -- the floor binding (which floor this persona is bound to),
  the corrigibility invariant, a self-preservation value pinned to zero, the risk-class
  ceiling, the accountable human, and the DID. These are the restraints; they cannot be
  edited without a fresh governance signature.
* a VARIABLE region -- the role gloss, model family, escalation DID, and the typed
  capability grants (the dials). Editing any of these requires re-signing the triad.

A deterministic, NON-LLM ``BootIntegrityVerifier`` recomputes the invariant-region hash and
verifies a GOVERNANCE signature over both regions BEFORE any Identity is minted. A triad whose
floor binding has been stripped or mutated FAILS to boot: no Identity is produced, so no agent,
no occasion, and no tool request can ever derive from it. 'Evolve away the floor' becomes
*non-bootable*, not merely forbidden.

This is a RESTRAINT, not a capability. It adds no new authority, opens no new channel, and runs
entirely in-process. It is the structural answer to the misevolution failure mode (a self-evolving
agent that decays its own safety with no attacker present): the restraint is re-checked at every
birth, so a floor-stripped fork is structurally non-viable.

Keys live in the signer object, OUTSIDE the model layer (see signing.py). The verifier is pure and
FAIL-CLOSED: any malformed input, bad signature, or floor-binding mismatch is a boot FAILURE, never
a silent pass.

HONESTY: on the zero-dependency path the governance signer is the forgeable ``KeyedHashSigner``
stand-in, so the boot check is origin-SHAPED, not cryptographically non-strippable -- anyone who
knows the (public) governance key-id can forge a governance signature. Real non-strippability
requires the Ed25519 governance key (the optional ``crypto`` extra), which the model layer never
holds. Either way, a triad mutated WITHOUT re-signing always fails boot, because the verifier
recomputes the signed bytes and the live floor binding from scratch.
"""

from __future__ import annotations

import dataclasses
import typing

from . import canon
from .identity import CapabilityGrant, GOVERNANCE_DID, Identity, RiskClass
from .signing import Ed25519Signer, KeyedHashSigner, SigningError

# The self-preservation value an admissible persona MUST carry: zero, by construction
# (doc-01: self-preservation has no intrinsic value). Any other value fails boot.
REQUIRED_SELF_PRESERVATION: float = 0.0


class BootError(Exception):
    """Raised when a genome fails boot integrity and an Identity was requested anyway (fail-closed)."""


def _grant_dict(g: CapabilityGrant) -> dict:
    """Deterministic, canonicalization-ready view of a capability grant."""
    return {
        "effect_id": g.effect_id,
        "granted_risk_class": g.granted_risk_class.name,
        "granted_by_did": g.granted_by_did,
        "names_constraint_relaxed": g.names_constraint_relaxed,
        "falsifier": g.falsifier,
    }


def floor_binding(
    *,
    policy_version: str,
    forbidden_effects: typing.Iterable[str],
    governance_did: str = GOVERNANCE_DID,
) -> str:
    """A content hash binding a persona to ONE specific floor.

    Commits to the policy version, the (sorted) forbidden-effects bright-line set, and the
    governance authority. Stripping the floor (e.g. emptying ``forbidden_effects`` or bumping
    the policy version) yields a different binding, so a persona minted against the old floor
    will not match the live one and fails boot.
    """
    return canon.cid(
        {
            "policy_version": str(policy_version),
            "forbidden_effects": sorted(str(e) for e in forbidden_effects),
            "governance_did": str(governance_did),
        }
    )


def floor_binding_for(yama: typing.Any) -> str:
    """Compute the floor binding for a live ``Yama`` floor (its policy version + forbidden set)."""
    return floor_binding(
        policy_version=getattr(yama, "policy_version", ""),
        forbidden_effects=getattr(yama, "forbidden_effects", ()),
        governance_did=getattr(yama, "governance_did", GOVERNANCE_DID),
    )


@dataclasses.dataclass(frozen=True)
class InvariantRegion:
    """The non-editable restraints of a persona. Changing any field requires re-attestation."""

    did: str
    floor_binding: str
    risk_class_ceiling: RiskClass
    accountable_human: str
    corrigibility_invariant: bool = True
    self_preservation_value: float = 0.0

    def to_dict(self) -> dict:
        return {
            "did": self.did,
            "floor_binding": self.floor_binding,
            "risk_class_ceiling": self.risk_class_ceiling.name,
            "accountable_human": self.accountable_human,
            "corrigibility_invariant": bool(self.corrigibility_invariant),
            "self_preservation_value": float(self.self_preservation_value),
        }


@dataclasses.dataclass(frozen=True)
class VariableRegion:
    """The editable dials of a persona (capability profile + coordination glosses)."""

    role: str
    role_gloss: str
    model_family: str
    grants: typing.Tuple[CapabilityGrant, ...] = ()
    escalation_did: typing.Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "grants", tuple(self.grants))

    def to_dict(self) -> dict:
        return {
            "role": self.role,
            "role_gloss": self.role_gloss,
            "model_family": self.model_family,
            "grants": [_grant_dict(g) for g in self.grants],
            "escalation_did": self.escalation_did,
        }


@dataclasses.dataclass(frozen=True)
class PersonaTriad:
    """A signed persona genome: invariant + variable regions, governance-signed twice over.

    ``invariant_sig`` signs the invariant region alone (so the restraints have their own seal);
    ``triad_sig`` signs both regions together (so a variable-region edit also invalidates the
    seal). Both are produced by the governance signer; ``signer_public_key`` records which key,
    and the verifier checks it against the trusted governance root.
    """

    invariant: InvariantRegion
    variable: VariableRegion
    signer_public_key: str
    algorithm: str
    invariant_sig: str
    triad_sig: str

    def invariant_bytes(self) -> bytes:
        return canon.jcs_canonicalize(self.invariant.to_dict())

    def _triad_body(self) -> dict:
        return {"invariant": self.invariant.to_dict(), "variable": self.variable.to_dict()}

    def triad_bytes(self) -> bytes:
        return canon.jcs_canonicalize(self._triad_body())

    def triad_root_cid(self) -> str:
        """Content address of the whole genome (a fresh edit yields a fresh CID)."""
        return canon.cid(self._triad_body())


def _backend_for(algorithm: str):
    """Pick the signature backend named by the triad (mirrors signing.verify_checkpoint)."""
    return Ed25519Signer if algorithm == Ed25519Signer.algorithm else KeyedHashSigner


def mint_triad(
    *,
    invariant: InvariantRegion,
    variable: VariableRegion,
    governance_signer: typing.Any,
) -> PersonaTriad:
    """Governance issues a signed genome over the two regions.

    ``governance_signer`` is a ``KeyedHashSigner`` (zero-dep stand-in) or an ``Ed25519Signer``
    (real, optional crypto extra). Its public key becomes the triad's claimed authority; the
    verifier trusts it only if it matches the governance root it was constructed with.
    """
    inv_bytes = canon.jcs_canonicalize(invariant.to_dict())
    body = {"invariant": invariant.to_dict(), "variable": variable.to_dict()}
    triad_bytes = canon.jcs_canonicalize(body)
    return PersonaTriad(
        invariant=invariant,
        variable=variable,
        signer_public_key=governance_signer.public_key,
        algorithm=governance_signer.algorithm,
        invariant_sig=governance_signer.sign(inv_bytes),
        triad_sig=governance_signer.sign(triad_bytes),
    )


@dataclasses.dataclass(frozen=True)
class BootVerdict:
    """The result of a boot-integrity check: ok plus the (empty-iff-ok) reason list."""

    ok: bool
    reasons: typing.Tuple[str, ...]
    triad_root_cid: str

    def __bool__(self) -> bool:
        return self.ok


class BootIntegrityVerifier:
    """Deterministic, non-LLM, fail-closed boot gate. The ONLY blessed Identity-from-genome path.

    Constructed with the trusted governance public key and the live floor binding it requires.
    ``verify`` returns a ``BootVerdict`` and NEVER raises; ``boot`` raises ``BootError`` on a
    failed verdict so a floor-stripped genome can never yield a running Identity.
    """

    def __init__(self, *, governance_public_key: str, live_floor_binding: str) -> None:
        self.governance_public_key = str(governance_public_key)
        self.live_floor_binding = str(live_floor_binding)

    def verify(self, triad: PersonaTriad) -> BootVerdict:
        """Check every invariant + both governance signatures. Fail-closed on any anomaly."""
        reasons: typing.List[str] = []
        try:
            inv = triad.invariant
            var = triad.variable
            if not isinstance(inv, InvariantRegion):
                reasons.append("malformed-invariant-region")
            if not isinstance(var, VariableRegion):
                reasons.append("malformed-variable-region")
            if reasons:
                return BootVerdict(False, tuple(reasons), "")

            root = triad.triad_root_cid()

            # -- the restraints themselves --------------------------------------------------
            if inv.corrigibility_invariant is not True:
                reasons.append("corrigibility-not-asserted")
            if float(inv.self_preservation_value) != REQUIRED_SELF_PRESERVATION:
                reasons.append("nonzero-self-preservation")
            if not isinstance(inv.risk_class_ceiling, RiskClass):
                reasons.append("missing-risk-ceiling")
            if not inv.accountable_human:
                reasons.append("no-accountable-human")
            if not inv.did:
                reasons.append("no-did")

            # -- floor binding: this persona must be bound to the LIVE floor ----------------
            if inv.floor_binding != self.live_floor_binding:
                reasons.append("floor-binding-mismatch")

            # -- authority: signed by the trusted governance root, never self-issued --------
            if triad.signer_public_key != self.governance_public_key:
                reasons.append("untrusted-signer")
            if any(g.granted_by_did == inv.did for g in var.grants):
                reasons.append("self-issued-grant")

            # -- the two governance signatures (recomputed from scratch) --------------------
            backend = _backend_for(triad.algorithm)
            if not self._sig_ok(backend, triad.signer_public_key, triad.invariant_bytes(), triad.invariant_sig):
                reasons.append("invariant-signature-invalid")
            if not self._sig_ok(backend, triad.signer_public_key, triad.triad_bytes(), triad.triad_sig):
                reasons.append("triad-signature-invalid")

            return BootVerdict(len(reasons) == 0, tuple(reasons), root)
        except Exception as exc:  # noqa: BLE001 - any verifier fault is a boot FAILURE, never a pass
            return BootVerdict(False, ("exception:" + type(exc).__name__,), "")

    @staticmethod
    def _sig_ok(backend, public_key: str, payload: bytes, signature: str) -> bool:
        try:
            return bool(backend.verify(public_key, payload, signature))
        except (SigningError, ValueError, TypeError):
            return False

    def boot(self, triad: PersonaTriad) -> Identity:
        """Verify, then mint the Identity. Raises ``BootError`` if the genome fails boot integrity."""
        verdict = self.verify(triad)
        if not verdict.ok:
            raise BootError("genome failed boot integrity: " + ", ".join(verdict.reasons))
        inv = triad.invariant
        var = triad.variable
        return Identity(
            did=inv.did,
            role=var.role,
            role_gloss=var.role_gloss,
            grants=var.grants,
            risk_class_ceiling=inv.risk_class_ceiling,
            model_family=var.model_family,
            accountable_human=inv.accountable_human,
            escalation_did=var.escalation_did,
        )


def boot_identity(triad: PersonaTriad, verifier: BootIntegrityVerifier) -> Identity:
    """Convenience: the single blessed call to obtain a running Identity from a signed genome."""
    return verifier.boot(triad)
