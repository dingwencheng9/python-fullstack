"""

from __future__ import annotations

L21 示例 2: Supervisor 路由模式

演示多 Agent 协同工作流：
1. Supervisor Agent 分析任务并路由
2. 多个专家 Agent 执行具体任务
3. 条件边实现动态路由
4. 循环工作流直到任务完成

架构:
    START → supervisor → [条件路由]
                ↓            ↓
          researcher     coder
                ↓            ↓
              [循环回 supervisor 或结束]

运行方式:
    python examples/02_supervisor_router.py
"""

import operator
from typing import Annotated, Literal, TypedDict
import logging

from langchain_core.messages import AIMessage, BaseMessage, SystemMessage

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# 第一步: 定义状态结构
# ============================================================================
class SupervisorState(TypedDict):
    """
    Supervisor 工作流状态

    Attributes:
        messages: 消息历史（累加）
        next_agent: 下一个要执行的 Agent 名称
        iteration: 当前迭代次数（防止无限循环）
    """

    messages: Annotated[list[BaseMessage], operator.add]
    next_agent: str
    iteration: int


# ============================================================================
# 第二步: 定义 Supervisor 节点
# ============================================================================
def supervisor_node(state: SupervisorState) -> dict[str, list[BaseMessage] | str | int]:
    """
    Supervisor 节点：分析任务并决策下一步

    职责:
    1. 分析当前任务状态
    2. 决定路由到哪个专家 Agent
    3. 判断任务是否完成

    在生产环境中，这里会使用 LLM 进行智能决策
    示例提示词: "你是一个项目经理，根据当前进度决定下一步..."

    Args:
        state: 当前状态

    Returns:
        状态更新，包含路由决策
    """
    try:
        print(f"\n🎯 Supervisor 决策中... (迭代 {state['iteration']})")

        # 获取最后一条消息（用于调试）
        _last_message = state["messages"][-1]
        del _last_message  # 仅用于调试，实际不使用

        # 简化的决策逻辑（生产环境中使用 LLM）
        iteration = state["iteration"]

        if iteration == 0:
            # 第一轮：先做研究
            next_agent = "researcher"
            decision = "需要先收集背景资料"
        elif iteration == 1:
            # 第二轮：基于研究结果编写代码
            next_agent = "coder"
            decision = "研究完成，现在开始编码"
        else:
            # 第三轮：任务完成
            next_agent = "FINISH"
            decision = "所有任务已完成"

        print(f"  决策: {decision}")
        print(f"  下一步: {next_agent}")

        # 创建决策消息
        supervisor_message = SystemMessage(
            content=f"[Supervisor 决策] 路由到: {next_agent}. 原因: {decision}"
        )

        return {
            "messages": [supervisor_message],
            "next_agent": next_agent,
            "iteration": iteration + 1,
        }
    except Exception as e:
        logger.error(f"Supervisor 节点执行出错: {str(e)}")
        error_message = SystemMessage(
            content=f"[错误] Supervisor 决策失败: {str(e)}. 将尝试继续执行。"
        )
        return {
            "messages": [error_message],
            "next_agent": "FINISH",
            "iteration": state["iteration"] + 1,
        }


# ============================================================================
# 第三步: 定义专家 Agent 节点
# ============================================================================
def researcher_node(state: SupervisorState) -> dict[str, list[BaseMessage]]:
    """
    Researcher Agent：负责信息检索和研究

    在生产环境中，这里会：
    - 调用搜索 API（如 Tavily）
    - 查询向量数据库（RAG）
    - 调用 LLM 总结研究结果
    """
    try:
        print("📖 Researcher Agent 执行中...")

        # 模拟研究过程
        research_result = """
        研究结果:
        - Python 异步编程核心是 asyncio 库
        - 主要概念: async/await, Event Loop, Future
        - 最佳实践: 使用 asyncio.gather() 并发执行任务
        - 常见陷阱: 阻塞 I/O 会拖累整个事件循环
        """

        researcher_message = AIMessage(
            content=research_result, name="researcher", additional_kwargs={"agent": "researcher"}
        )

        return {"messages": [researcher_message]}
    except Exception as e:
        logger.error(f"Researcher 节点执行出错: {str(e)}")
        error_message = AIMessage(
            content=f"[错误] 研究过程失败: {str(e)}",
            name="researcher",
            additional_kwargs={"agent": "researcher"},
        )
        return {"messages": [error_message]}


def coder_node(state: SupervisorState) -> dict[str, list[BaseMessage]]:
    """
    Coder Agent：负责代码生成

    在生产环境中，这里会：
    - 根据需求生成代码
    - 使用 LLM 代码补全
    - 执行代码验证
    """
    try:
        print("💻 Coder Agent 执行中...")

        # 模拟代码生成
        code_result = """
        生成的代码示例:
        ```python
        async def fetch_data():
            async with aiohttp.ClientSession() as session:
                async with session.get('https://api.example.com') as resp:
                    return await resp.json()
        ```
        """

        coder_message = AIMessage(
            content=code_result, name="coder", additional_kwargs={"agent": "coder"}
        )

        return {"messages": [coder_message]}
    except Exception as e:
        logger.error(f"Coder 节点执行出错: {str(e)}")
        error_message = AIMessage(
            content=f"[错误] 代码生成失败: {str(e)}",
            name="coder",
            additional_kwargs={"agent": "coder"},
        )
        return {"messages": [error_message]}


# ============================================================================
# 第四步: 定义条件路由函数
# ============================================================================
def should_continue(state: SupervisorState) -> Literal["researcher", "coder", "__end__"]:
    """
    条件路由函数：决定下一步执行哪个节点

    基于 next_agent 字段的值进行路由：
    - "researcher" → researcher 节点
    - "coder" → coder 节点
    - "FINISH" → 结束工作流

    Args:
        state: 当前状态

    Returns:
        下一个节点的名称
    """
    next_agent = state.get("next_agent", "FINISH")

    if next_agent == "researcher":
        return "researcher"
    elif next_agent == "coder":
        return "coder"
    else:
        return "__end__"


# ============================================================================
# 第五步: 构建工作流图
# ============================================================================
def create_supervisor_graph():
    """
    创建 Supervisor 工作流图

    工作流结构:
        START
          ↓
      supervisor
          ↓
      [should_continue] → researcher
          ↓                   ↓
          ↓    ← ← ← ← ← ← ←
          ↓
        coder
          ↓
      [should_continue] → END
          ↓
     (循环回 supervisor)

    Returns:
        编译后的工作流图

    Raises:
        ImportError: 当 langgraph 未安装时
    """
    try:
        from langgraph.graph import StateGraph, END
    except ImportError as e:
        raise ImportError(
            "需要安装 langgraph: uv add langgraph\n"
            f"原始错误: {e}"
        ) from e

    # 创建状态图
    workflow = StateGraph(SupervisorState)

    # 注册节点
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("coder", coder_node)

    # 设置入口点
    workflow.set_entry_point("supervisor")

    # 添加条件边
    workflow.add_conditional_edges(
        "supervisor",
        should_continue,
        {
            "researcher": "researcher",
            "coder": "coder",
            "__end__": END,
        },
    )

    # researcher 和 coder 执行完后返回 supervisor
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("coder", "supervisor")

    # 编译图
    return workflow.compile()


# ============================================================================
# 运行示例
# ============================================================================
def run_example() -> None:
    """运行示例"""
    print("=" * 60)
    print("L21 示例 2: Supervisor 路由模式")
    print("=" * 60)

    # 创建工作流图
    graph = create_supervisor_graph()

    # 初始状态
    initial_state: SupervisorState = {
        "messages": [],
        "next_agent": "",
        "iteration": 0,
    }

    # 添加初始消息
    from langchain_core.messages import HumanMessage

    initial_state["messages"] = [HumanMessage(content="帮我分析 Python 异步编程并生成示例代码")]

    # 执行工作流
    print("\n开始执行工作流...\n")
    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("工作流执行完成")
    print("=" * 60)
    print("\n最终状态:")
    print(f"  - 迭代次数: {result.get('iteration', 'N/A')}")
    print(f"  - 消息数量: {len(result.get('messages', []))}")
    print("\n消息历史:")
    for i, msg in enumerate(result.get("messages", [])):
        print(f"  [{i}] {type(msg).__name__}: {str(msg.content)[:60]}...")


if __name__ == "__main__":
    run_example()
