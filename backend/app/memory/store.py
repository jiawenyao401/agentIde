from __future__ import annotations

import uuid
from typing import Iterable

import chromadb

from app.memory.models import MemoryItem, MemoryType


class MemoryStore:
    """Three-layer long-term memory backed by ChromaDB."""

    def __init__(self, persist_directory: str = "./.chroma") -> None:
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collections = {
            MemoryType.episodic: self.client.get_or_create_collection("episodic"),
            MemoryType.semantic: self.client.get_or_create_collection("semantic"),
            MemoryType.personality: self.client.get_or_create_collection("personality"),
        }

    def add(self, memory_type: MemoryType, content: str, metadata: dict | None = None) -> MemoryItem:
        memory_id = str(uuid.uuid4())
        collection = self.collections[memory_type]
        safe_metadata = self._safe_metadata(memory_type, metadata)
        collection.add(ids=[memory_id], documents=[content], metadatas=[safe_metadata])
        return MemoryItem(memory_id=memory_id, memory_type=memory_type, content=content, metadata=safe_metadata)

    def search(self, memory_type: MemoryType, query: str, n_results: int = 3) -> list[MemoryItem]:
        collection = self.collections[memory_type]
        result = collection.query(query_texts=[query], n_results=n_results)
        ids: Iterable[str] = result.get("ids", [[]])[0]
        docs: Iterable[str] = result.get("documents", [[]])[0]
        metas: Iterable[dict] = result.get("metadatas", [[]])[0]
        return [
            MemoryItem(memory_id=memory_id, memory_type=memory_type, content=doc, metadata=meta or {})
            for memory_id, doc, meta in zip(ids, docs, metas)
        ]

    @staticmethod
    def _safe_metadata(memory_type: MemoryType, metadata: dict | None) -> dict:
        """Chroma requires metadata to be a non-empty dict."""
        if metadata:
            return metadata
        return {"memory_type": memory_type.value, "source": "agent-core"}
