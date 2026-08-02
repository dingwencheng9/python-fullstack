"""L60 示例 5: MCP SDK Client"""

from __future__ import annotations

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_params = StdioServerParameters(
        command="python",
        args=["examples/04_mcp_sdk_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()

            # 列出工具
            tools_response = await session.list_tools()
            print("可用工具:")
            for tool in tools_response.tools:
                print(f"  - {tool.name}: {tool.description}")

            # 调用工具
            print("\n调用 add(10, 5):")
            result = await session.call_tool("add", arguments={"a": 10, "b": 5})
            print(f"  结果: {result.content[0].text}")

            print("\n调用 search_docs('Python'):")
            result = await session.call_tool(
                "search_docs", arguments={"query": "Python", "limit": 3}
            )
            print(f"  结果: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
