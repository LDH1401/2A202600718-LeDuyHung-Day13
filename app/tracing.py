from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()

def tracing_enabled() -> bool:
    return bool(os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"))


def _noop_observe(*args: Any, **kwargs: Any):
    def decorator(func):
        return func
    return decorator


class _DummyContext:
    def update_current_trace(self, **kwargs: Any) -> None:
        return None

    def update_current_observation(self, **kwargs: Any) -> None:
        return None


if tracing_enabled():
    try:
        from langfuse.decorators import observe, langfuse_context
    except Exception:  # pragma: no cover
        observe = _noop_observe
        langfuse_context = _DummyContext()
else:
    observe = _noop_observe
    langfuse_context = _DummyContext()
