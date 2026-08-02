"""

from __future__ import annotations

L21 示例 1: 基础 Agent 节点

演示 LangGraph 的核心概念：
1. 使用 TypedDict 定义状态结构
2. 添加处理节点（node）
3. 添加确定性边（edge）
4. 编译并执行图

运行方式:
    python examples/01_basic_agent_node.py
"""

import operator
from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph


# ============================================================================
# 第一步: 定义状态结构
# ============================================================================
class AgentState(TypedDict):
    """
    Agent 状态定义

    使用 Annotated 和 operator.add 实现消息列表的累加语义：
    - 每次更新会将新消息追加到列表末尾，而非覆盖整个列表
    """

    messages: Annotated[list[BaseMessage], operator.add]
    task_completed: bool


# ============================================================================
# 第二步: 定义节点函数
# ============================================================================
def agent_node(state: AgentState) -> dict[str, list[BaseMessage] | bool]:
    """
    Agent 节点：处理用户输入并生成回复

    在真实场景中，这里会调用 LLM (如 ChatOpenAI)
    为了演示，我们使用模拟的固定回复

    Args:
        state: 当前状态，包含消息历史

    Returns:
        状态更新字典，包含新消息和完成标志
    """
    print("🤖 Agent 节点执行中...")

    # 获取最后一条用户消息
    last_message = state["messages"][-1]
    user_input = (
        last_message.content
        if hasattr(last_message, "content") and last_message.content
        else str(last_message)
    )

    # 模拟 LLM 响应（生产环境中替换为真实 LLM 调用）
    # 示例: llm = ChatOpenAI(model="gpt-4")
    #       response = llm.invoke(state["messages"])
    response_content = f"我理解了您的任务: '{user_input}'. 这是我的分析结果..."

    # 创建 AI 消息
    ai_message = AIMessage(content=response_content)

    # 返回状态更新
    # 注意: messages 使用 operator.add，所以新消息会追加到列表
    return {
        "messages": [ai_message],
        "task_completed": True,
    }


# ============================================================================
# 第三步: 构建状态图
# ============================================================================
def create_agent_graph() -> StateGraph:
    """
    创建简单的单节点 Agent 图

    流程:
        START → agent_node → END

    Returns:
        编译后的可执行图
    """
    # 1. 初始化状态图
    workflow = StateGraph(AgentState)

    # 2. 添加节点
    workflow.add_node("agent", agent_node)

    # 3. 添加边
    workflow.add_edge(START, "agent")  # 从起点到 agent 节点
    workflow.add_edge("agent", END)  # 从 agent 节点到终点

    # 4. 编译图
    return workflow.compile()


# ============================================================================
# 第四步: 执行图
# ============================================================================
def main() -> None:
    """主函数：演示基础 Agent 节点的执行"""
    print("=" * 60)
    print("L21 示例 1: 基础 Agent 节点")
    print("=" * 60)

    # 创建图
    graph = create_agent_graph()

    # 准备初始状态
    initial_state: AgentState = {
        "messages": [HumanMessage(content="分析 Python 异步编程的最佳实践")],
        "task_completed": False,
    }

    print("\n📥 初始状态:")
    print(f"  用户消息: {initial_state['messages'][0].content}")
    print(f"  任务状态: {'未完成' if not initial_state['task_completed'] else '已完成'}")

    # 执行图
    print("\n🚀 开始执行...")
    try:
        final_state = graph.invoke(initial_state)
    except Exception as e:
        print(f"\n❌ 执行过程中发生错误: {str(e)}")
        return

    # 输出结果
    print("\n✅ 执行完成！")
    print("\n📤 最终状态:")
    print(f"  消息数量: {len(final_state['messages'])}")
    print(f"  任务状态: {'已完成' if final_state['task_completed'] else '未完成'}")
    print("\n💬 Agent 回复:")
    print(f"  {final_state['messages'][-1].content}")

    print("\n" + "=" * 60)
    print("✨ 关键知识点总结:")
    print("  1. TypedDict 定义状态结构")
    print("  2. Annotated[list, operator.add] 实现消息累加")
    print("  3. add_node() 添加处理函数")
    print("  4. add_edge() 连接节点")
    print("  5. compile() 生成可执行图")
    print("=" * 60)


if __name__ == "__main__":
    main()
