"""
TPay SDK Trace Module
"""

import contextvars
import logging

logger = logging.getLogger(__name__)

class TraceStore:
    def __init__(self):
        self._store = contextvars.ContextVar("agent_trace", default={})

    def set(self, key, value):
        current = self._store.get()
        updated = {**current, key: value}
        self._store.set(updated)

    def get(self, key):
        return self._store.get().get(key)

    def get_all(self):
        return self._store.get()

trace_store = TraceStore()