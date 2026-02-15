"""Status-related service helpers."""

from __future__ import annotations

import random


def get_latency_ms() -> int:
    """Return a pseudo-random latency in milliseconds."""
    return random.randint(1, 500)

