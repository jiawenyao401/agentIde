from dataclasses import dataclass
from enum import Enum


class MemoryType(str, Enum):
    episodic = "episodic"
    semantic = "semantic"
    personality = "personality"


@dataclass
class MemoryItem:
    memory_id: str
    memory_type: MemoryType
    content: str
    metadata: dict
