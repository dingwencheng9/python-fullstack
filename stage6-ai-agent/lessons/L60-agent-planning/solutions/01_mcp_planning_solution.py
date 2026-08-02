"""
L57 参考答案: MCP Server + LangGraph ToolNode 集成

包含：
1. MCP EnvServer：提供 get_env 和 run_expression 两个工具
2. MCPEnvClient：异步上下文管理器 MCP 客户端
3. LangGraph Plan-and-Execute 图：planner → execute → summarize

运行方式:
    python examples/03_langgraph_mcp_integration.py   # 演示 MCP File System
    # 或使用本文件的 MCP Client 连接自己的 Server:
    python solutions/01_mcp_planning_solution.py
"""

from __future__ import annotations

import ast
import asyncio
import operator
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import CallToolResult, ListToolsResult, TextContent, Tool


# ===========================================================================
# Part 1: MCP EnvServer
# ===========================================================================

SERVER = Server("l57-env-server")

# 安全运算符白名单（用于 run_expression）
SAFE_OPERATORS: dict[str, object] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "**": operator.pow,
}


@SERVER.list_tools()
async def list_env_tools() -> ListToolsResult:
    return ListToolsResult(
        tools=[
            Tool(
                name="get_env",
                description="获取指定环境变量的值。变量不存在时返回 NOT_SET。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "key": {
                            "type": "string",
                            "description": "环境变量名（如 PATH、HOME、PYTHONPATH）",
                        }
                    },
                    "required": ["key"],
                },
            ),
            Tool(
                name="run_expression",
                description="在当前 Python 环境中安全地执行简单的数学表达式。",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "expr": {
                            "type": "string",
                            "description": "数学表达式，仅支持 + - * / ** ( ) 和数字",
                        }
                    },
                    "required": ["expr"],
                },
            ),
        ]
    )


@SERVER.call_tool()
async def call_env_tool(name: str, arguments: dict) -> CallToolResult:
    try:
        match name:
            case "get_env":
                return await _get_env(arguments["key"])
            case "run_expression":
                return await _run_expression(arguments["expr"])
            case _:
                raise ValueError(f"未知工具: {name!r}")
    except PermissionError as exc:
        return CallToolResult(
            content=[TextContent(type="text", text=f"权限错误: {exc}")],
            isError=True,
        )
    except FileNotFoundError as exc:
        return CallToolResult(
            content=[TextContent(type="text", text=f"文件未找到: {exc}")],
            isError=True,
        )
    except OSError as exc:
        return CallToolResult(
            content=[TextContent(type="text", text=f"系统错误: {exc}")],
            isError=True,
        )
    except UnicodeDecodeError as exc:
        return CallToolResult(
            content=[TextContent(type="text", text=f"编码错误: {exc}")],
            isError=True,
        )
    except Exception as exc:
        raise RuntimeError(f"工具 {name!r} 执行失败: {exc}") from exc


async def _get_env(key: str) -> CallToolResult:
    value = os.environ.get(key, "NOT_SET")
    return CallToolResult(content=[TextContent(type="text", text=value)])


async def _run_expression(expr: str) -> CallToolResult:
    try:
        node = ast.parse(expr, mode="eval")
        # 仅允许常量（数字）和二元运算
        for n in ast.walk(node):
            if not isinstance(
                n,
                (
                    ast.Expression,
                    ast.BinOp,
                    ast.UnaryOp,
                    ast.Add,
                    ast.Sub,
                    ast.Mult,
                    ast.Div,
                    ast.Pow,
                    ast.FloorDiv,
                    ast.Mod,
                    ast.USub,
                    ast.UAdd,
                    ast.Constant,
                ),
            ):
                return CallToolResult(
                    content=[TextContent(type="text", text=f"ERROR: 不支持的语法 {type(n).__name__}")],
                    isError=True,
                )
        result = eval(compile(node, "<expr>", "eval"), {"__builtins__": {}}, SAFE_OPERATORS)
        return CallToolResult(content=[TextContent(type="text", text=str(result))])
    except ZeroDivisionError:
        return CallToolResult(content=[TextContent(type="text", text="ERROR: 除数不能为零")], isError=True)
    except SyntaxError:
        return CallToolResult(content=[TextContent(type="text", text="ERROR: 语法错误")], isError=True)
    except Exception as exc:
        return CallToolResult(content=[TextContent(type="text", text=f"ERROR: {exc}")], isError=True)


# ===========================================================================
# Part 2: MCP EnvClient
# ===========================================================================


class MCPEnvClient:
    """MCP 环境变量客户端，上下文管理器自动管理生命周期。"""

    def __init__(self, server_script: str) -> None:
        self.server_script = server_script
        self._session: ClientSession | None = None
        self._client: stdio_client | None = None

    async def __aenter__(self) -> MCPEnvClient:
        params = StdioServerParameters(command=sys.executable, args=[self.server_script])
        self._client = stdio_client(params)
        read, write = await self._client.__aenter__()
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        if self._session:
            await self._session.__aexit__(*exc_info)
        if self._client:
            await self._client.__aexit__(*exc_info)

    async def get_env(self, key: str) -> str:
        if not self._session:
            raise RuntimeError("客户端未连接")
        result = await self._session.call_tool("get_env", {"key": key})
        return result.content[0].text

    async def run_expression(self, expr: str) -> str:
        if not self._session:
            raise RuntimeError("客户端未连接")
        result = await self._session.call_tool("run_expression", {"expr": expr})
        return result.content[0].text


# ===========================================================================
# Part 3: LangGraph Plan-and-Execute
# ===========================================================================


@dataclass
class TaskState:
    task: str
    plan: list[str] = field(default_factory=list)
    executed: list[str] = field(default_factory=list)
    results: list[str] = field(default_factory=list)
    response: str = ""


llm = ChatOllama(model="qwen2.5:7b", temperature=0.3, base_url="http://localhost:11434")


async def planner_node(state: TaskState) -> TaskState:
    system = SystemMessage(
        content=(
            "你是一个任务规划助手。"
            "将任务分解为调用 MCP 工具的步骤。\n\n"
            "可用工具:\n"
            "- get_env(key): 读取环境变量（如 PATH、HOME）\n"
            "- run_expression(expr): 执行数学表达式（如「2**10」）\n\n"
            "输出格式：每行一个步骤，格式为「步骤N: 描述 [工具名: 参数]」"
        )
    )
    human = HumanMessage(content=f"任务: {state.task}\n\n分解步骤:")
    response = await llm.ainvoke([system, human])
    raw_lines = response.content.strip().split("\n")
    lines = [ln.strip() for ln in raw_lines if "步骤" in ln]
    if not lines:
        lines = [f"执行: {state.task}"]
    return TaskState(task=state.task, plan=lines, executed=[], results=[])


def _parse_tool_call(step: str) -> tuple[str, str]:
    if "[" in step and "]" in step:
        inner = step[step.index("[") + 1 : step.index("]")]
        if ":" in inner:
            tool, args = inner.split(":", 1)
            return tool.strip(), args.strip()
    return "get_env", "PATH"


async def executor_node(state: TaskState) -> TaskState:
    if not state.plan:
        return state
    step = state.plan[0]
    tool, args = _parse_tool_call(step)
    server = str(Path(__file__).parent.parent / "exercises" / "01_mcp_planning_exercise.py")
    if not Path(server).exists():
        server = str(Path(__file__))
    try:
        async with MCPEnvClient(server) as client:
            if tool == "get_env":
                output = await client.get_env(args)
            elif tool == "run_expression":
                output = await client.run_expression(args)
            else:
                output = "(未知工具)"
    except Exception as exc:
        output = f"ERROR: {exc}"
    return TaskState(
        task=state.task,
        plan=state.plan[1:],
        executed=state.executed + [step],
        results=state.results + [f"[{tool}] {args!r} → {output}"],
    )


def should_continue(state: TaskState) -> Literal["execute", "summarize"]:
    return "execute" if state.plan else "summarize"


async def summarize_node(state: TaskState) -> TaskState:
    system = SystemMessage(content="根据执行结果生成简洁报告。")
    lines = "\n".join(f"  {i + 1}. {r}" for i, r in enumerate(state.results))
    human = HumanMessage(content=f"任务: {state.task}\n结果:\n{lines}\n生成报告:")
    response = await llm.ainvoke([system, human])
    return TaskState(task=state.task, plan=[], executed=[], results=state.results, response=response.content)


# ===========================================================================
# 演示
# ===========================================================================


async def demo() -> None:
    print("=" * 60)
    print("MCP EnvServer + LangGraph 演示")
    print("=" * 60)
    graph = StateGraph(TaskState)
    graph.add_node("planner", planner_node)
    graph.add_node("execute", executor_node)
    graph.add_node("summarize", summarize_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "execute")
    graph.add_conditional_edges("execute", should_continue)
    graph.add_edge("summarize", END)
    app = graph.compile()
    task = "查看 Python 版本，计算 2 的 10 次方"
    print(f"\n📋 任务: {task}\n")
    async for chunk in app.astream(TaskState(task=task), stream_mode="values"):
        if chunk.plan:
            print("🗺️  计划:", chunk.plan)
        if chunk.results:
            print(f"⚙️   执行: {chunk.results[-1]}")
        if chunk.response:
            print(f"📊 报告:\n{chunk.response}")


async def main() -> None:
    """MCP EnvServer 独立运行入口（stdio 模式）。"""
    async with stdio_server() as (read, write):
        await SERVER.run(read, write, SERVER.create_initialization_options())


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--server":
        asyncio.run(main())
    else:
        asyncio.run(demo())
