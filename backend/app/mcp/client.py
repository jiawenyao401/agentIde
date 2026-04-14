from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolSchema:
    name: str
    description: str


class MCPClient:
    """Lazy tool-schema loading MCP client for local and remote servers."""

    def __init__(self) -> None:
        self._registry: dict[str, Callable[..., Any]] = {}
        self._schema_loaders: dict[str, Callable[[], ToolSchema]] = {}
        self._loaded_schemas: dict[str, ToolSchema] = {}

    def register_tool(self, name: str, handler: Callable[..., Any], schema_loader: Callable[[], ToolSchema]) -> None:
        self._registry[name] = handler
        self._schema_loaders[name] = schema_loader

    def list_tools(self) -> list[ToolSchema]:
        schemas: list[ToolSchema] = []
        for name in self._registry:
            if name not in self._loaded_schemas:
                self._loaded_schemas[name] = self._schema_loaders[name]()
            schemas.append(self._loaded_schemas[name])
        return schemas

    def get_tool_schema(self, name: str) -> ToolSchema:
        if name not in self._loaded_schemas:
            self._loaded_schemas[name] = self._schema_loaders[name]()
        return self._loaded_schemas[name]

    def call_tool(self, name: str, tool_input: dict) -> Any:
        if name not in self._registry:
            raise KeyError(f"Tool not found: {name}")
        _ = self.get_tool_schema(name)
        return self._registry[name](**tool_input)
