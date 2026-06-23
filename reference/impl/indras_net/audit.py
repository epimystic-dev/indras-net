# SPDX-License-Identifier: Apache-2.0
"""Akasha-Sutra: an append-only, hash-chained, tamper-evident ledger written by one exclusive writer (Chitragupta)."""

from __future__ import annotations

import dataclasses
import enum
import time
import typing

from . import canon
from .envelope import WorkerOutputEnvelope


class AuditError(Exception):
    """Base class for audit-ledger errors."""


class TamperError(AuditError):
    """Raised when verify() is asked to assert integrity and the chain is broken."""


class WriterIdentityError(AuditError):
    """Raised when a non-exclusive writer attempts append, or a restricted action_class is
    authored by a DID not authorized for it."""


class ActionClassLedger(enum.Enum):
    """Operational audit action-class (closed enum, doc-04). Distinct from the deontic
    ActionClass on the envelope honesty block; these compose, they are not the same field.

    Authority is enforced at append: only Yama may author ENFORCE_PASS/ENFORCE_FAIL; only
    Vishnu may author HALT. A REPARATIVE leaf records an agent's corrective act, appended
    after a preserved violation (see ``Swarm.record_reparation``).

    Closed and minimal by design: only action-classes the runtime actually writes are
    defined here. Subsystem-scoped classes (consensus / reputation / evolution / identity
    events) are intentionally absent until those subsystems exist, so a name never asserts
    a mechanism the code does not implement.
    """

    OBSERVE = "OBSERVE"
    PROPOSE = "PROPOSE"
    ENFORCE_PASS = "ENFORCE_PASS"
    ENFORCE_FAIL = "ENFORCE_FAIL"
    HALT = "HALT"
    REPARATIVE = "REPARATIVE"


# Genesis predecessor hash for the first leaf (all-zero sha256).
GENESIS_HASH: str = "0" * 64

# Default role DIDs for the restricted-authority map. Vendor-neutral mythic coordination names.
YAMA_DID: str = "did:web:indras-net.roles:yama"
VISHNU_DID: str = "did:web:indras-net.roles:vishnu"


def _enum_value(x: typing.Any) -> typing.Any:
    return x.value if isinstance(x, enum.Enum) else x


@dataclasses.dataclass
class AuditLeaf:
    """One append-only audit leaf: a doc-04 AuditRecord plus chain-position fields.

    ``entry_hash`` is an RFC-6962 domain-separated leaf hash over the JCS bytes of the body
    (every field EXCEPT entry_hash). ``prev_hash`` is the previous leaf's entry_hash. Any
    mutation of any past leaf body changes its entry_hash and breaks every downstream prev_hash.
    """

    leaf_index: int
    record_id: str
    prev_hash: str
    signer_did: str
    signer_role: str
    action_class: ActionClassLedger
    event_type: str
    envelope_cid: str
    policy_version: str
    payload_commitment: str
    subject_cid: typing.Optional[str] = None
    reasoning_rung: typing.Optional[str] = None
    iterated: bool = False
    refs: typing.Tuple[str, ...] = ()
    entry_hash: str = ""
    ts: str = ""

    def body_dict(self) -> dict:
        """All fields EXCEPT entry_hash, in a deterministic dict (the hashed body)."""
        return {
            "leaf_index": self.leaf_index,
            "record_id": self.record_id,
            "prev_hash": self.prev_hash,
            "signer_did": self.signer_did,
            "signer_role": self.signer_role,
            "action_class": _enum_value(self.action_class),
            "event_type": self.event_type,
            "envelope_cid": self.envelope_cid,
            "policy_version": self.policy_version,
            "payload_commitment": self.payload_commitment,
            "subject_cid": self.subject_cid,
            "reasoning_rung": self.reasoning_rung,
            "iterated": bool(self.iterated),
            "refs": list(self.refs),
            "ts": self.ts,
        }

    def compute_entry_hash(self) -> str:
        """RFC-6962 leaf hash over the JCS-canonicalized body (entry_hash excluded)."""
        return canon.leaf_hash(canon.jcs_canonicalize(self.body_dict()))


def _monotonic_record_id(leaf_index: int, seq: int) -> str:
    """A ULID-like monotonic, lexicographically-sortable record id.

    Not a true ULID (no Crockford-base32 randomness needed for the MVP), but strictly
    increasing and fixed-width so lexical order == append order.
    """
    return f"{leaf_index:013d}{seq:013d}"


class AkashaSutra:
    """The hash-chained ledger. ONE exclusive writer (``writer_did``); appends are fenced.

    Restricted action-classes are bound to an authorized signer DID via ``authority``: by
    default ENFORCE_PASS/ENFORCE_FAIL -> Yama, HALT -> Vishnu. ``verify()`` walks the whole
    chain and returns True iff intact — mutating ANY past entry breaks it.
    """

    def __init__(
        self,
        writer_did: str,
        *,
        authority: typing.Optional[typing.Dict[ActionClassLedger, str]] = None,
    ) -> None:
        if not writer_did:
            raise WriterIdentityError("AkashaSutra requires a non-empty exclusive writer_did")
        self.writer_did = writer_did
        if authority is None:
            authority = {
                ActionClassLedger.ENFORCE_PASS: YAMA_DID,
                ActionClassLedger.ENFORCE_FAIL: YAMA_DID,
                ActionClassLedger.HALT: VISHNU_DID,
            }
        self._authority: typing.Dict[ActionClassLedger, str] = dict(authority)
        self._leaves: typing.List[AuditLeaf] = []
        self._seq: int = 0

    def append(
        self,
        *,
        signer_did: str,
        signer_role: str,
        action_class: ActionClassLedger,
        event_type: str,
        envelope: WorkerOutputEnvelope,
        writer_did: str,
        subject_cid: typing.Optional[str] = None,
        refs: typing.Iterable[str] = (),
    ) -> AuditLeaf:
        """Append one leaf. Enforces the exclusive-writer fence and the action-class authority map.

        Raises WriterIdentityError if ``writer_did`` != the registered exclusive writer, or if
        ``action_class`` is restricted and ``signer_did`` is not its authorized DID.
        """
        if writer_did != self.writer_did:
            raise WriterIdentityError(
                f"exclusive-writer fence: writer_did {writer_did!r} != {self.writer_did!r}"
            )
        required = self._authority.get(action_class)
        if required is not None and signer_did != required:
            raise WriterIdentityError(
                f"action_class {action_class.name} may only be authored by {required!r}, "
                f"not {signer_did!r}"
            )

        leaf_index = len(self._leaves)
        prev_hash = self._leaves[-1].entry_hash if self._leaves else GENESIS_HASH
        record_id = _monotonic_record_id(leaf_index, self._seq)
        self._seq += 1
        ts = self._now()

        # payload_commitment: a salted hash over the envelope's canonical content body. Lets a
        # third party later be shown (salt, payload) and recompute, without the payload on-log.
        env_cid = envelope.action_id or envelope.compute_action_id()
        salt = canon.sha256_hex(record_id.encode("utf-8"))
        payload_commitment = canon.sha256_hex(salt.encode("utf-8") + b"." + envelope.content_bytes())

        leaf = AuditLeaf(
            leaf_index=leaf_index,
            record_id=record_id,
            prev_hash=prev_hash,
            signer_did=signer_did,
            signer_role=signer_role,
            action_class=action_class,
            event_type=event_type,
            envelope_cid=env_cid,
            policy_version=envelope.provenance.policy_version,
            payload_commitment=payload_commitment,
            subject_cid=subject_cid,
            reasoning_rung=_rung_str(envelope),
            iterated=_iterated_flag(envelope),
            refs=tuple(refs),
            ts=ts,
        )
        leaf.entry_hash = leaf.compute_entry_hash()
        self._leaves.append(leaf)
        return leaf

    def verify(self) -> bool:
        """Walk the chain; return True iff fully intact.

        Recomputes each entry_hash, asserts it matches the stored value, asserts each prev_hash
        equals the previous entry_hash (GENESIS_HASH for the first), and asserts leaf_index and
        record_id are strictly monotonic. Any mutation, reorder, or truncation flips this False.
        """
        prev = GENESIS_HASH
        last_index = -1
        last_record_id = ""
        for i, leaf in enumerate(self._leaves):
            if leaf.leaf_index != i:
                return False
            if leaf.leaf_index <= last_index:
                return False
            if leaf.record_id <= last_record_id:
                return False
            if leaf.prev_hash != prev:
                return False
            if leaf.entry_hash != leaf.compute_entry_hash():
                return False
            prev = leaf.entry_hash
            last_index = leaf.leaf_index
            last_record_id = leaf.record_id
        return True

    def head_hash(self) -> str:
        return self._leaves[-1].entry_hash if self._leaves else GENESIS_HASH

    def __len__(self) -> int:
        return len(self._leaves)

    def leaves(self) -> typing.Tuple[AuditLeaf, ...]:
        """Read-only snapshot copy of the leaves."""
        return tuple(self._leaves)

    def get(self, leaf_index: int) -> AuditLeaf:
        return self._leaves[leaf_index]

    @staticmethod
    def _now() -> str:
        # RFC-3339-ish UTC stamp; advisory only (causal order is the chain, not this field).
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _rung_str(envelope: WorkerOutputEnvelope) -> typing.Optional[str]:
    rung = getattr(envelope.honesty, "causal_rung", None)
    if rung is None:
        return None
    val = rung.value if hasattr(rung, "value") else rung
    return f"rung{val}"


def _iterated_flag(envelope: WorkerOutputEnvelope) -> bool:
    tag = getattr(envelope.honesty, "reasoning_tag", None)
    val = tag.value if hasattr(tag, "value") else (tag or "")
    return "iterated" in str(val)
