"""Small per-process rate limiter for public finder entry.

The production deployment should move this state to a shared edge/Redis limiter;
this module still prevents accidental and local-demo abuse without adding a
second persistence subsystem to the MVP.
"""

from __future__ import annotations

import threading
import time

from .errors import RateLimitError


class RateLimiter:
    def __init__(self):
        self._lock = threading.Lock()
        self._windows: dict[str, tuple[float, int]] = {}

    def check(self, key: str, limit: int, window_seconds: int) -> None:
        current = time.monotonic()
        with self._lock:
            started, count = self._windows.get(key, (current, 0))
            if current - started >= window_seconds:
                started, count = current, 0
            count += 1
            self._windows[key] = (started, count)
            if count > limit:
                retry_after = max(1, int(window_seconds - (current - started)))
                raise RateLimitError(retry_after)
