"""L60 示例 4: MCP SDK Server（FastMCP）"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo-tools")


@mcp.tool()
def add(a: int, b: int) -> int:
    """两数相加"""
    return a + b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """两数相乘"""
    return a * b


@mcp.tool()
def search_docs(query: str, limit: int = 5) -> list[str]:
    """搜索文档（模拟）"""
    return [f"文档 {i}: 关于 '{query}' 的结果" for i in range(1, limit + 1)]


if __name__ == "__main__":
    # stdio 模式运行
    mcp.run()
