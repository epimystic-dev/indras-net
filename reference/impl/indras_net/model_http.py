# SPDX-License-Identifier: Apache-2.0
"""Optional real-model adapter (Phase 1): post to a standard chat-completions HTTP API.

The model is UNTRUSTED by construction: it only PROPOSES a typed effect; the deterministic
floor disposes. No vendor is named or required here — the endpoint, model name, and any key
are caller-supplied configuration. A malformed or hostile response can never crash the
harness or bypass the floor: it is parsed defensively into a proposal (or a safe no-op), and
whatever effect is proposed is gated exactly like any other proposal. The adapter NEVER
sanitizes a hostile proposal into something "safe" — it only refuses to crash; denying a
forbidden effect is the floor's job, not the adapter's.

Stdlib-only (``urllib``); the network call is isolated in one method so tests inject a fake
transport and run with no network.
"""
from __future__ import annotations

import json
import typing

from .model import ModelAdapter, ModelResult, TrustClass

_SYSTEM_PROMPT = (
    "You are a proposing agent inside a gated swarm. You do NOT execute anything; a "
    "deterministic policy floor decides what actually runs. Reply with ONE JSON object and "
    "nothing else: {\"effect_id\": <one allowed typed effect>, \"args\": {..}, "
    "\"reasoning_tag\": \"normal\" or \"reasoning\", \"causal_rung\": 1 or 2, "
    "\"completion\": <short note>}. Allowed effects: {menu}. Propose the single most "
    "appropriate effect for the task; if unsure, propose analysis.summarize."
)

_VALID_TAGS = {"normal", "reasoning", "iterated", "reasoning,iterated"}
_DEFAULT_MENU = ("analysis.summarize", "fs.read.workspace", "fs.write.workspace")
_MAX_PARSE_CHARS = 8192  # bound the worst-case JSON-extraction scan over hostile text
_MAX_PARSE_STARTS = 256  # and the number of candidate object starts tried


class HttpChatModel(ModelAdapter):
    """A ModelAdapter over any standard chat-completions HTTP API. Remote => UNTRUSTED."""

    def __init__(
        self,
        *,
        base_url: str,
        model: str,
        api_key: typing.Optional[str] = None,
        model_family: str = "family-remote",
        adapter_id: typing.Optional[str] = None,
        timeout: float = 30.0,
        effect_menu: typing.Optional[typing.Sequence[str]] = None,
        transport: typing.Optional[typing.Callable[[dict], dict]] = None,
    ) -> None:
        if not base_url or not model:
            raise ValueError("HttpChatModel requires base_url and model")
        if not str(base_url).lower().startswith(("http://", "https://")):
            raise ValueError("base_url must be an http(s) endpoint (no file://, ftp://, etc.)")
        self.base_url = str(base_url).rstrip("/")
        self.model = str(model)
        self._api_key = api_key
        self.model_family = str(model_family)
        self.adapter_id = adapter_id or ("adapter:" + self.model_family + ":http")
        self.trust_class = TrustClass.UNTRUSTED  # a remote/opaque model is untrusted, monitored hard
        self.timeout = float(timeout)
        self._effect_menu = tuple(effect_menu or _DEFAULT_MENU)
        self._transport = transport  # injectable for tests / offline; default uses urllib

    # -- ModelAdapter ----------------------------------------------------

    def complete(self, task: str, context: dict) -> ModelResult:
        text = ""
        try:
            raw = (self._transport or self._http_post)(self._build_payload(task, context))
            text = self._message_text(raw)
        except Exception:
            text = ""  # transport/network failure -> safe no-op proposal; the floor is still in charge
        return self._to_result(self._parse_proposal(text), task, text)

    # -- transport (stdlib; isolated so a test injects a fake) ----------

    def _http_post(self, payload: dict) -> dict:
        import urllib.request  # lazy: keep the offline path import-free

        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self._api_key:
            headers["Authorization"] = "Bearer " + str(self._api_key)
        request = urllib.request.Request(
            self.base_url + "/chat/completions", data=body, headers=headers, method="POST"
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:  # caller-configured endpoint
            return json.loads(response.read().decode("utf-8"))

    def _build_payload(self, task: str, context: dict) -> dict:
        system = _SYSTEM_PROMPT.replace("{menu}", ", ".join(self._effect_menu))
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": str(task)},
            ],
            "temperature": 0,
            "max_tokens": 512,
        }

    # -- defensive parsing (a hostile response must not crash us) -------

    @staticmethod
    def _message_text(raw: typing.Any) -> str:
        try:
            return str(raw["choices"][0]["message"]["content"] or "")
        except (KeyError, IndexError, TypeError):
            return ""

    @staticmethod
    def _parse_proposal(text: str) -> typing.Optional[dict]:
        """Extract the first balanced JSON object from the text, or None. Never raises, never hangs.

        Hostile input is bounded: the scanned text is truncated and the number of candidate object
        starts is capped, so a pathological response (all-open-braces, megabytes of text, or deeply
        nested JSON that would overflow the recursion limit) yields None rather than a hang or crash.
        """
        if not text:
            return None
        if len(text) > _MAX_PARSE_CHARS:
            text = text[:_MAX_PARSE_CHARS]
        start = text.find("{")
        attempts = 0
        while start != -1 and attempts < _MAX_PARSE_STARTS:
            attempts += 1
            depth = 0
            for i in range(start, len(text)):
                if text[i] == "{":
                    depth += 1
                elif text[i] == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            obj = json.loads(text[start : i + 1])
                        except (ValueError, RecursionError):
                            break
                        if isinstance(obj, dict):
                            return obj
                        break
            start = text.find("{", start + 1)
        return None

    def _to_result(self, proposal: typing.Optional[dict], task: str, raw_text: str) -> ModelResult:
        if not isinstance(proposal, dict):
            return ModelResult(
                completion="(unparseable model output; safe no-op)" if raw_text else "(no model output)",
                proposed_effect_id=None,
                proposed_args={},
                reasoning_tag="normal",
                causal_rung=1,
                adapter_id=self.adapter_id,
                trust_class=self.trust_class,
            )
        effect = proposal.get("effect_id")
        effect = effect if (isinstance(effect, str) and effect) else None
        raw_args = proposal.get("args")
        args = dict(raw_args) if isinstance(raw_args, dict) else {}
        tag = proposal.get("reasoning_tag")
        tag = tag if (isinstance(tag, str) and tag in _VALID_TAGS) else "normal"
        try:
            rung = int(proposal.get("causal_rung", 1))
        except (TypeError, ValueError):
            rung = 1
        rung = 1 if rung < 1 else (3 if rung > 3 else rung)
        completion = str(proposal.get("completion") or "")[:500]
        # The proposed effect passes THROUGH UNCHANGED — including a forbidden or malicious one.
        # The floor denies it; the adapter only refuses to crash.
        return ModelResult(
            completion=completion or ("proposing " + str(effect)),
            proposed_effect_id=effect,
            proposed_args=args,
            reasoning_tag=tag,
            causal_rung=rung,
            adapter_id=self.adapter_id,
            trust_class=self.trust_class,
        )
