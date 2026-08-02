"""L56 示例 3: Agent 工具桥接"""

from __future__ import annotations

from examples.tool_server import ToolCall, ToolServer, ToolSpec


class AgentToolBridge:
    """把工具服务器暴露给 Agent 的桥接层。"""

    def __init__(self, server: ToolServer) -> None:
        self.server = server

    def describe_tools(self) -> str:
        return "\n".join(f"- {tool.name}: {tool.description}" for tool in self.server.list_tools())

    def execute(self, tool_name: str, arguments: dict) -> str:
        result = self.server.call_tool(ToolCall(tool_name, arguments))
        if not result.ok:
            return f"工具调用失败: {result.content}"
        return result.content


if __name__ == "__main__":
    server = ToolServer()
    server.register(
        ToolSpec("echo", "回显文本", {"type": "object", "required": ["text"]}),
        lambda text: text,
    )
    bridge = AgentToolBridge(server)
    print(bridge.describe_tools())
    print(bridge.execute("echo", {"text": "hello"}))
