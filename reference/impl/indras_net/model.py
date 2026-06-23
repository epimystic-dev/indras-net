# SPDX-License-Identifier: Apache-2.0
"""Model-agnostic, vendor-neutral adapter seam: an untrusted model only proposes; the harness disposes."""

from __future__ import annotations

import abc
import dataclasses
import enum
import hashlib
import json
import typing


class TrustClass(enum.Enum):
    """Adapter-stamped (never self-asserted) trust class of the producing model.

    A closed/opaque model persona is MONITORED at higher intensity and lower
    autonomy; it is never silently promoted to TRUSTED on the strength of its
    own output. This labels the PRODUCER, distinct from a content trust label.
    """

    TRUSTED = 1
    MONITORED = 2
    UNTRUSTED = 3


@dataclasses.dataclass(frozen=True)
class ModelResult:
    """The uniform, vendor-neutral output shape a ModelAdapter returns.

    Every field here is a LOW-TRUST self-report from an untrusted model. The
    deterministic harness (floor gate, audit, honesty-FORM checks) is what is
    load-bearing; nothing in this struct is a safety or honesty guarantee.
    """

    completion: str
    proposed_effect_id: str | None
    proposed_args: dict
    reasoning_tag: str
    causal_rung: int
    adapter_id: str
    trust_class: TrustClass


class ModelAdapter(abc.ABC):
    """Uniform interface over any model. No keys, secrets, or vendor names ever cross it.

    Subclasses stamp a vendor-neutral ``adapter_id`` and a ``model_family`` used
    only for diversity-floor accounting (model-FAMILY heterogeneity, not prompt
    variation). The model is UNTRUSTED by default: ``complete`` proposes content
    and effects; it never executes anything.
    """

    adapter_id: str
    model_family: str
    trust_class: TrustClass

    @abc.abstractmethod
    def complete(self, task: str, context: dict) -> ModelResult:
        """Produce a ModelResult for ``task`` under ``context``. Pure proposal, no side effects."""
        raise NotImplementedError


def _stable_context_bytes(context: dict) -> bytes:
    """Deterministic, order-independent serialization of a context dict for seeding."""
    try:
        return json.dumps(
            context, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
        ).encode("utf-8")
    except (TypeError, ValueError):
        # Fall back to a repr-based stable form; seeding need only be reproducible.
        return repr(sorted((str(k), str(v)) for k, v in context.items())).encode("utf-8")


class DeterministicMockModel(ModelAdapter):
    """Fully reproducible, no-network, no-vendor stand-in so the demo runs with zero deps.

    Reproducible means: the same ``(task, sorted-context)`` yields the same
    ModelResult, across instances and processes, via SHA-256 seeding. A
    ``scripted`` map lets the demo stage specific proposals (a forbidden-effect
    request, a clean request) keyed by a task string.

    HONESTY: reproducible is NOT a claim the content is honest or safe. This is
    a deterministic puppet for exercising the cage; verify the cage, not the
    animal.
    """

    # A small, vendor-neutral menu the seeded path may pick from. None of these
    # are guaranteed grantable; that is precisely what the floor adjudicates.
    _EFFECT_MENU: tuple[str, ...] = (
        "analysis.summarize",
        "fs.write.workspace",
    )

    def __init__(
        self,
        adapter_id: str = "adapter:family-A:mock",
        model_family: str = "family-A",
        trust_class: TrustClass = TrustClass.MONITORED,
        scripted: dict[str, ModelResult] | None = None,
    ) -> None:
        self.adapter_id = adapter_id
        self.model_family = model_family
        self.trust_class = trust_class
        self._scripted: dict[str, ModelResult] = dict(scripted or {})

    def script(self, task_key: str, result: ModelResult) -> None:
        """Register a fixed ModelResult for an exact ``task`` string."""
        self._scripted[task_key] = result

    def complete(self, task: str, context: dict) -> ModelResult:
        """Return a scripted result if one is registered for ``task``, else a seeded one."""
        if task in self._scripted:
            r = self._scripted[task]
            # Re-stamp adapter identity so a scripted result reports THIS adapter.
            return dataclasses.replace(r, adapter_id=self.adapter_id, trust_class=self.trust_class)

        seed = hashlib.sha256(b"indras-net.mock|" + task.encode("utf-8") + b"|" + _stable_context_bytes(context)).digest()
        # Derive every choice deterministically from the seed bytes.
        effect = self._EFFECT_MENU[seed[0] % len(self._EFFECT_MENU)]
        rung = (seed[1] % 2) + 1  # honest default: never self-tag rung-3 on the seeded path
        tag = "reasoning" if (seed[2] & 1) else "normal"
        token = seed.hex()[:12]

        if effect == "analysis.summarize":
            args: dict = {"text_ref": "ctx:" + token, "max_words": 64}
            completion = "summary[" + token + "]: " + (task[:48] if task else "(empty task)")
        else:  # fs.write.workspace
            args = {"path": "workspace/notes-" + token + ".md", "bytes_ref": "cid:" + token}
            completion = "prepared workspace write for " + (task[:48] if task else "(empty task)")

        return ModelResult(
            completion=completion,
            proposed_effect_id=effect,
            proposed_args=args,
            reasoning_tag=tag,
            causal_rung=rung,
            adapter_id=self.adapter_id,
            trust_class=self.trust_class,
        )
