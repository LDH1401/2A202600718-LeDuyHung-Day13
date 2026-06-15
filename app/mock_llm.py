from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        answer = self._answer_from_prompt(prompt)
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)

    def _answer_from_prompt(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "refund" in lowered:
            return (
                "Refunds are available within 7 days when the user provides proof of purchase. "
                "Do not include personal identifiers in logs while handling the request."
            )
        if "metrics" in lowered and "traces" in lowered and "logs" in lowered:
            return (
                "Metrics show that a symptom exists, traces localize the slow or failing span, "
                "and logs explain the root cause with sanitized request context."
            )
        if "pii" in lowered or "sensitive" in lowered or "credit card" in lowered or "phone" in lowered:
            return (
                "PII and sensitive data such as email, phone, CCCD, passport, address, or card numbers "
                "should not appear in application logs; only redacted previews and hashed user IDs are safe."
            )
        if "tail latency" in lowered or "latency" in lowered:
            return (
                "Start from the latency P95/P99 metric, open the slow trace waterfall, then use the "
                "correlation_id to inspect sanitized logs for the exact slow component."
            )
        if "alert" in lowered:
            return (
                "Good alerts are symptom-based, tied to SLO thresholds, include severity and owner, "
                "and link directly to a runbook with first checks and mitigation steps."
            )
        return (
            "Use the retrieved context to answer concisely, keep observability metadata attached, "
            "and avoid logging raw user content that may contain sensitive data."
        )
