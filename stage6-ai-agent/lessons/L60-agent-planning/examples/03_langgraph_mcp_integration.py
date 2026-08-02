"""
L57 示例 3: LangGraph ToolNode 集成 MCP Server

将 examples/02_mcp_server.py 的 MCP Server 接入 LangGraph ToolNode，
演示大模型通过 MCP 协议安全读取本地文件进行 Plan-and-Execute 任务规划。

核心架构:
    ┌──────────────┐     MCP stdio      ┌───────────────────────┐
    │ LangGraph    │ ──────────────────→│ MCP File System Server │
    │ ToolNode     │← ──────────────────│ (examples/02_mcp_server)│
    └──────────────┘   JSON-RPC 响应     └───────────────────────┘
           │
           ↓ 调用工具
    ┌──────────────┐
    │ LLM (Ollama) │
    └──────────────┘
"""

from __future__ import annotations

import asyncio
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ---------------------------------------------------------------------------
# LangGraph State
# ---------------------------------------------------------------------------


@dataclass
class PlanningState:
    """Plan-and-Execute 状态机状态。"""

    task: str
    plan: list[str] = field(default_factory=list)
    executed: list[str] = field(default_factory=list)
    results: list[str] = field(default_factory=list)
    response: str = ""


# ---------------------------------------------------------------------------
# MCP Client（上下文管理器，自动管理生命周期）
# ---------------------------------------------------------------------------


class MCPFileSystemClient:
    """
    MCP 文件系统客户端，封装 stdio 连接生命周期。

    使用方式:
        async with MCPFileSystemClient("examples/02_mcp_server.py") as client:
            result = await client.list_directory("src")
    """

    def __init__(self, server_script: str) -> None:
        self.server_script = server_script
        self._session: ClientSession | None = None
        self._client: stdio_client | None = None

    async def __aenter__(self) -> MCPFileSystemClient:
        params = StdioServerParameters(
            command=_python_executable(),
            args=[self.server_script],
        )
        self._client = stdio_client(params)
        read, write = await self._client.__aenter__()
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        if self._session:
            await self._session.__aexit__(*exc_info)
            self._session = None
        if self._client:
            await self._client.__aexit__(*exc_info)
            self._client = None

    async def list_directory(self, path: str) -> str:
        """列出目录内容。"""
        if not self._session:
            raise RuntimeError("客户端未连接，请使用 async with 上下文")
        result = await self._session.call_tool("list_directory", {"path": path})
        return result.content[0].text

    async def read_file(self, path: str) -> str:
        """读取文件内容。"""
        if not self._session:
            raise RuntimeError("客户端未连接，请使用 async with 上下文")
        result = await self._session.call_tool("read_file", {"path": path})
        return result.content[0].text

    async def search_files(self, path: str, keyword: str) -> str:
        """搜索文件名。"""
        if not self._session:
            raise RuntimeError("客户端未连接，请使用 async with 上下文")
        result = await self._session.call_tool("search_files", {"path": path, "keyword": keyword})
        return result.content[0].text


def _python_executable() -> str:
    return sys.executable


# ---------------------------------------------------------------------------
# LangGraph 节点（异步）
# ---------------------------------------------------------------------------

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0.3,
    base_url="http://localhost:11434",
)


async def planner_node(state: PlanningState) -> PlanningState:
    """
    规划节点：调用 LLM 将复杂任务分解为步骤。

    提示 LLM 生成可执行的步骤计划，每步对应一个 MCP 工具调用。
    """
    system = SystemMessage(
        content="""你是一个任务规划助手。
将用户的任务分解为具体的执行步骤，每步描述要使用的工具和参数。

可用工具（通过 MCP 协议调用）:
- list_directory(path): 列出目录内容
- read_file(path): 读取文件内容（限 64KB 文本）
- search_files(path, keyword): 递归搜索文件名

输出格式：每行一个步骤，格式为 "步骤N: 描述 [工具名: 参数]"

示例:
步骤1: 查看项目结构 [list_directory: .]
步骤2: 找到核心逻辑文件 [search_files: src, langgraph]
步骤3: 读取文件内容 [read_file: src/core.py]
"""
    )
    human = HumanMessage(content=f"任务: {state.task}\n\n请分解任务:")
    response = await llm.ainvoke([system, human])
    raw = response.content.strip()
    lines = [ln.strip() for ln in raw.split("\n") if ln.strip() and "步骤" in ln]
    if not lines:
        lines = [f"执行: {state.task}"]
    return PlanningState(
        task=state.task,
        plan=lines,
        executed=state.executed,
        results=state.results,
    )


async def executor_node(state: PlanningState) -> PlanningState:
    """
    执行节点：通过 MCP 协议调用本地文件工具。

    从计划中取出第一步，解析工具名和参数，通过 MCP Client 执行，
    将结果追加到已执行列表和结果列表。
    """
    if not state.plan:
        return state

    step = state.plan[0]
    # 从步骤文本中解析 [工具名: 参数]
    tool_name, args = _parse_step(step)

    # 使用 MCP Client（通过 subprocess stdio 连接）
    server_script = _resolve_server_path()
    try:
        async with MCPFileSystemClient(server_script) as client:
            match tool_name:
                case "list_directory":
                    output = await client.list_directory(args)
                case "read_file":
                    output = await client.read_file(args)
                case "search_files":
                    path_kw = _split_args(args)
                    output = await client.search_files(path_kw[0], path_kw[1])
                case _:
                    output = f"(未知工具 {tool_name!r})"
    except Exception as exc:  # 捕获连接失败、超时等
        output = f"执行失败: {exc}"

    return PlanningState(
        task=state.task,
        plan=state.plan[1:],
        executed=state.executed + [step],
        results=state.results + [f"[{tool_name}] {output[:200]}"],
    )


def should_continue(state: PlanningState) -> Literal["execute", "summarize"]:
    """条件边：计划非空则继续执行，否则汇总。"""
    return "execute" if state.plan else "summarize"


async def summarize_node(state: PlanningState) -> PlanningState:
    """汇总节点：整理执行结果生成最终响应。"""
    system = SystemMessage(content="你是一个任务执行报告助手。根据执行结果生成简洁报告。")
    result_lines = "\n".join(f"  {i + 1}. {r}" for i, r in enumerate(state.results))
    human = HumanMessage(content=f"任务: {state.task}\n\n执行结果:\n{result_lines}\n\n生成最终报告:")
    response = await llm.ainvoke([system, human])
    return PlanningState(
        task=state.task,
        plan=[],
        executed=state.executed,
        results=state.results,
        response=response.content,
    )


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def _parse_step(step: str) -> tuple[str, str]:
    """从步骤文本解析工具名和参数。"""
    if "[" in step and "]" in step:
        inner = step[step.index("[") + 1 : step.index("]")]
        if ":" in inner:
            tool, args = inner.split(":", 1)
            return tool.strip(), args.strip()
    return "list_directory", "."  # 默认


def _split_args(args: str) -> list[str]:
    parts = [p.strip() for p in args.split(",")]
    while len(parts) < 2:
        parts.append("")
    return parts[:2]


def _resolve_server_path() -> str:
    """解析 MCP Server 脚本路径（相对于本文件位置）。"""
    return str(Path(__file__).parent / "02_mcp_server.py")


# ---------------------------------------------------------------------------
# 图构建
# ---------------------------------------------------------------------------


def build_planning_graph() -> StateGraph:
    """构建 Plan-and-Execute 状态机图。"""
    graph = StateGraph(PlanningState)
    graph.add_node("planner", planner_node)
    graph.add_node("execute", executor_node)
    graph.add_node("summarize", summarize_node)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "execute")
    graph.add_conditional_edges("execute", should_continue)
    graph.add_edge("summarize", END)
    return graph.compile()


# ---------------------------------------------------------------------------
# 演示
# ---------------------------------------------------------------------------


async def demo() -> None:
    """演示：让 LLM 通过 MCP 协议读取本地文件进行任务规划。"""
    print("=" * 60)
    print("MCP + LangGraph Plan-and-Execute 演示")
    print("=" * 60)

    app = build_planning_graph()
    task = "分析当前项目的目录结构，找到 stage6-ai-agent 下的课程数量，然后读取 L57 的 lesson.md 前 20 行内容"

    print(f"\n📋 任务: {task}\n")

    async for chunk in app.astream(
        PlanningState(task=task),
        stream_mode="values",
    ):
        if chunk.plan:
            print("🗺️  计划:")
            for step in chunk.plan:
                print(f"   {step}")
        if chunk.executed:
            print(f"\n⚙️   执行 ({len(chunk.executed)}/{len(chunk.executed) + len(chunk.plan)}):")
            print(f"   → {chunk.executed[-1][:80]}")
        if chunk.response:
            print(f"\n📊 最终报告:\n{chunk.response[:300]}")

    print("\n✅ 演示完成")


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n已取消")
    except Exception as exc:
        print(f"\n❌ 错误: {exc}", file=sys.stderr)
        raise
