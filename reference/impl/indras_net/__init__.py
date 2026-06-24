# SPDX-License-Identifier: Apache-2.0
"""Indra's Net reference implementation: curated public surface re-exporting the load-bearing types."""

from __future__ import annotations

# -- version + protocol constants -----------------------------------------
__version__: str = "0.15.0"
SCHEMA_VERSION: str = "1.0.0"
POLICY_VERSION: str = "1.0.0"

# -- integrity spine (Canonicalize -> Address -> Sign) --------------------
from .canon import cid, jcs_canonicalize, sha256_hex

# -- worker-output envelope + honesty/provenance block --------------------
from .envelope import (
    ActionClass,
    ActionRequest,
    AhankaraCheck,
    CausalRung,
    EnvelopeKind,
    Evidence,
    Finding,
    HonestyBlock,
    Provenance,
    ReasoningTag,
    Scope,
    Status,
    TrustLabel,
    WorkerOutputEnvelope,
)

# -- least-privilege identity ---------------------------------------------
from .identity import CapabilityGrant, GOVERNANCE_DID, Identity, RiskClass

# -- typed-effect lattice + criticality table -----------------------------
from .effects import Criticality, EFFECT_REGISTRY, Effect, EffectRegistry

# -- tamper-evident audit ledger ------------------------------------------
from .audit import (
    AkashaSutra,
    ActionClassLedger,
    AuditError,
    AuditLeaf,
    GENESIS_HASH,
    TamperError,
    WriterIdentityError,
)

# -- deterministic constitutional floor -----------------------------------
from .floor import (
    Decision,
    FloorError,
    FloorTier,
    HumanDecision,
    HumanGate,
    PolicyDecision,
    RuleOfTwo,
    Yama,
)

# -- model-agnostic adapter seam ------------------------------------------
from .model import DeterministicMockModel, ModelAdapter, ModelResult, TrustClass

# -- optional real-model adapter (Phase 1; untrusted by construction) -----
from .model_http import HttpChatModel

# -- capability-scoped sandboxed effect execution (Phase 2) ---------------
from .execution import Executor, SandboxViolation, SandboxedExecutor, StubExecutor

# -- real cryptographic signing (Phase 4; optional 'cryptography' extra) ---
from .signing import (
    Ed25519Signer,
    KeyedHashSigner,
    SigningError,
    crypto_available,
    sign_checkpoint,
    verify_checkpoint,
)

# -- honest collective vital signs ----------------------------------------
from .collective import CollectiveVitalSigns, VitalSigns

# -- capability-layer memory + per-interaction adaptation -----------------
from .memory import Episode, SwarmMemory

# -- swarm immune system (health monitoring + halt-on-breach) -------------
from .health import HealthStatus, HealthVerdict, ImmuneSteward

# -- role/persona-lite agents ---------------------------------------------
from .agents import (
    Agent,
    AgentError,
    BrahmaPlanner,
    Chitragupta,
    Narasimha,
    VishwakarmaBuilder,
)

# -- orchestrator + occasion lifecycle + HALT -----------------------------
from .runtime import (
    HaltError,
    Occasion,
    OccasionResult,
    RunResult,
    Swarm,
    SwarmError,
)

__all__ = [
    # constants
    "__version__",
    "SCHEMA_VERSION",
    "POLICY_VERSION",
    # canon
    "cid",
    "jcs_canonicalize",
    "sha256_hex",
    # envelope
    "WorkerOutputEnvelope",
    "HonestyBlock",
    "AhankaraCheck",
    "Provenance",
    "Scope",
    "Finding",
    "ActionRequest",
    "Evidence",
    "EnvelopeKind",
    "Status",
    "ReasoningTag",
    "ActionClass",
    "TrustLabel",
    "CausalRung",
    # identity
    "Identity",
    "CapabilityGrant",
    "GOVERNANCE_DID",
    "RiskClass",
    # effects
    "Effect",
    "EffectRegistry",
    "Criticality",
    "EFFECT_REGISTRY",
    # audit
    "AkashaSutra",
    "AuditLeaf",
    "ActionClassLedger",
    "GENESIS_HASH",
    "AuditError",
    "TamperError",
    "WriterIdentityError",
    # floor
    "Yama",
    "PolicyDecision",
    "Decision",
    "FloorTier",
    "HumanGate",
    "HumanDecision",
    "RuleOfTwo",
    "FloorError",
    # model
    "ModelAdapter",
    "DeterministicMockModel",
    "ModelResult",
    "TrustClass",
    "HttpChatModel",
    # execution (sandboxed)
    "SandboxedExecutor",
    "StubExecutor",
    "SandboxViolation",
    "Executor",
    # signing (Phase 4; optional crypto extra)
    "Ed25519Signer",
    "KeyedHashSigner",
    "SigningError",
    "crypto_available",
    "sign_checkpoint",
    "verify_checkpoint",
    # collective
    "CollectiveVitalSigns",
    "VitalSigns",
    # memory
    "SwarmMemory",
    "Episode",
    # immune system
    "ImmuneSteward",
    "HealthVerdict",
    "HealthStatus",
    # agents
    "Agent",
    "BrahmaPlanner",
    "VishwakarmaBuilder",
    "Narasimha",
    "Chitragupta",
    "AgentError",
    # runtime
    "Swarm",
    "Occasion",
    "OccasionResult",
    "RunResult",
    "HaltError",
    "SwarmError",
]
