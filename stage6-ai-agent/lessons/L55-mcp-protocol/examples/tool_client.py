"""L56 示例 2: 工具客户端"""

from __future__ import annotations

from examples.tool_server import ToolCall, ToolServer, ToolSpec


def build_server() -> ToolServer:
    server = ToolServer()
    server.register(
        ToolSpec(
            name="add",
            description="两个整数相加",
            input_schema={"type": "object", "required": ["a", "b"]},
        ),
        lambda a, b: a + b,
    )
    return server


if __name__ == "__main__":
    server = build_server()
    print("可用工具:")
    for tool in server.list_tools():
        print(f"- {tool.name}: {tool.description}")
    print("结果:", server.call_tool(ToolCall("add", {"a": 2, "b": 3})).content)
