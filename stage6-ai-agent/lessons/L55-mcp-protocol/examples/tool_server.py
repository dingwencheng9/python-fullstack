"""L56 示例 1: 极简工具服务器"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    input_schema: dict[str, Any]


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, Any]


@dataclass(frozen=True)
class ToolResult:
    content: str
    ok: bool = True


class ToolServer:
    def __init__(self) -> None:
        self.tools: dict[str, Callable] = {}
        self.specs: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec, handler: Callable) -> None:
        self.specs[spec.name] = spec
        self.tools[spec.name] = handler

    def list_tools(self) -> list[ToolSpec]:
        return list(self.specs.values())

    def call_tool(self, call: ToolCall) -> ToolResult:
        if call.name not in self.tools:
            return ToolResult(f"unknown tool: {call.name}", ok=False)
        result = self.tools[call.name](**call.arguments)
        return ToolResult(str(result))


if __name__ == "__main__":
    server = ToolServer()
    server.register(
        ToolSpec(
            name="echo",
            description="回显输入文本",
            input_schema={"type": "object", "properties": {"text": {"type": "string"}}},
        ),
        lambda text: text,
    )
    print(server.call_tool(ToolCall("echo", {"text": "hello"})))
