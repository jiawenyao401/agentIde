from contextlib import contextmanager
from dataclasses import dataclass, field
from time import perf_counter
from typing import Any


@dataclass
class TraceEvent:
    name: str
    duration_ms: float
    metadata: dict[str, Any] = field(default_factory=dict)


class TraceCollector:
    def __init__(self) -> None:
        self.events: list[TraceEvent] = []

    @contextmanager
    def span(self, name: str, metadata: dict[str, Any] | None = None):
        start = perf_counter()
        try:
            yield
        finally:
            elapsed = (perf_counter() - start) * 1000
            self.events.append(TraceEvent(name=name, duration_ms=elapsed, metadata=metadata or {}))
