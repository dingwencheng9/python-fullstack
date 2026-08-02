"""

from __future__ import annotations

L61 示例 3: Human-in-the-Loop

演示 LangGraph 原生的 Human-in-the-Loop 机制：
1. Agent 执行节点生成内容
2. 在 approval 节点触发 interrupt 暂停
3. 人类通过 Command 注入反馈
4. 图从中断点恢复，继续执行

核心概念:
- interrupt(): 在节点中触发中断
- Command: 携带人类输入恢复执行
- MemorySaver: 保存工作流状态
- thread_id: 用于恢复特定会话

运行方式:
    python examples/human_in_the_loop_03.py

参考文档:
- https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
"""

import operator
import logging
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, BaseMessage

# 解决 Python 3.13 get_type_hints() 无法解析 Annotated 的问题
# LangGraph 调用 get_type_hints 时需要能在命名空间中找到 Annotated
Annotated = Annotated  # noqa: F841


# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ============================================================================
# 第一步: 定义状态结构
# ============================================================================
class WritingState(TypedDict):
    """
    写作工作流状态

    Attributes:
        messages: 消息历史
        draft_content: 当前草稿内容
        human_feedback: 人类反馈（通过 Command 注入）
        revision_count: 修订次数
        approved: 是否已批准
    """

    messages: Annotated[list[BaseMessage], operator.add]
    draft_content: str
    human_feedback: str
    revision_count: int
    approved: bool


# ============================================================================
# 第二步: 定义节点函数
# ============================================================================
def writer_node(state: WritingState) -> dict[str, list[BaseMessage] | str | int]:
    """
    Writer Agent：生成或修订内容

    根据 revision_count 决定生成初稿还是修订：
    - revision_count == 0: 创建关于 "Python 异步编程" 的初稿
    - revision_count > 0: 根据 human_feedback 改进内容

    Args:
        state: 当前状态

    Returns:
        状态更新，包含新的草稿内容
    """
    try:
        revision_count = state["revision_count"]
        logger.info(f"Writer节点开始执行，当前修订次数: {revision_count}")

        if revision_count == 0:
            print("\n✍️  Writer Agent: 生成初稿...")
            draft = """
# Python 异步编程最佳实践

## 概述
异步编程是 Python 3.5+ 引入的重要特性，使用 async/await 语法。

## 核心概念
1. Event Loop: 事件循环
2. Coroutine: 协程函数
3. Task: 并发任务

## 示例代码
```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return "Data fetched"

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```
"""
        else:
            # 根据反馈修订
            feedback = state.get("human_feedback", "")
            print(f"\n✍️  Writer Agent: 根据反馈修订（第 {revision_count} 次）...")
            print(f"   人类反馈: {feedback}")

            draft = f"""
# Python 异步编程最佳实践（修订版 {revision_count}）

{feedback}

## 改进内容
根据审稿人的反馈，本次修订主要改进了以下方面：
1. 补充了更详细的示例代码
2. 优化了概念解释的清晰度
3. 增加了最佳实践建议

## 核心概念（优化版）
1. Event Loop: 异步事件循环机制
2. Coroutine: 协程函数与对象
3. Task: 并发任务管理
4. Future: 异步操作的结果容器

## 完整示例
```python
import asyncio
import aiohttp

async def fetch_url(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    urls = ['https://example.com', 'https://python.org']
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for url, content in zip(urls, results):
        print(f"{{url}}: {{len(content)}} bytes")

asyncio.run(main())
```

## 最佳实践
1. 使用 `asyncio.gather()` 并发执行多个协程
2. 使用 `async with` 管理异步资源
3. 避免在异步函数中使用阻塞 I/O
4. 使用 `asyncio.create_task()` 创建后台任务
"""

        writer_message = AIMessage(
            content=f"已生成{'初稿' if revision_count == 0 else f'第 {revision_count} 次修订'}",
            name="writer",
            additional_kwargs={"agent": "writer"},
        )

        return {
            "messages": [writer_message],
            "draft_content": draft,
            "revision_count": revision_count + 1,
        }

    except Exception as e:
        logger.error(f"Writer节点执行失败: {str(e)}")
        error_message = AIMessage(
            content=f"[错误] 写作失败: {str(e)}",
            name="writer",
            additional_kwargs={"agent": "writer"},
        )
        return {"messages": [error_message]}


def approval_node(state: WritingState) -> dict[str, bool]:
    """
    审核节点：评估人类反馈并决定是否批准

    此节点是 Human-in-the-Loop 的关键中断点。
    当检测到需要人工审核时，触发 interrupt 暂停工作流。

    批准逻辑：
    - 如果 human_feedback 包含批准关键词，返回 approved=True
    - 否则触发 interrupt，等待人类注入新的反馈

    Args:
        state: 当前状态

    Returns:
        状态更新，包含批准结果
    """
    try:
        feedback = state.get("human_feedback", "")
        feedback_lower = feedback.lower() if feedback else ""

        # 中文批准关键词
        chinese_approve_keywords = ["批准", "通过", "可以"]
        # 英文批准关键词
        english_approve_keywords = ["ok", "approve", "good", "yes", "pass"]

        # 检查是否包含批准关键词
        is_approved = bool(feedback) and (
            any(kw in feedback_lower for kw in english_approve_keywords)
            or any(kw in feedback for kw in chinese_approve_keywords)
        )

        if is_approved:
            print("✅  审核通过！")
            return {"approved": True}
        else:
            print("⚠️  审核未通过，需要修订")
            # 不触发中断，让路由决定下一步

        return {"approved": False}

    except Exception as e:
        logger.error(f"Approval节点执行失败: {str(e)}")
        return {"approved": False}


def should_interrupt(state: WritingState) -> Literal["interrupt", "writer", "__end__"]:
    """
    条件路由：决定工作流是否中断等待人类输入

    规则:
    - 如果 revision_count == 0 (刚生成初稿)，中断等待审核
    - 如果已批准，返回 END
    - 如果修订次数 >= 3，强制结束
    - 否则返回 writer 继续修订

    Args:
        state: 当前状态

    Returns:
        下一节点名称或 interrupt
    """
    # 刚生成初稿或修订稿，等待人类审核
    if state.get("revision_count", 0) >= 1 and not state.get("approved", False):
        return "interrupt"

    # 如果已批准
    if state.get("approved", False):
        return "__end__"

    # 如果修订次数过多
    if state.get("revision_count", 0) >= 3:
        return "__end__"

    return "writer"


def should_continue(state: WritingState) -> Literal["writer", "__end__"]:
    """
    条件路由：决定修订流程是否继续

    Args:
        state: 当前状态

    Returns:
        下一节点名称或 END
    """
    if state.get("approved", False):
        return "__end__"
    if state.get("revision_count", 0) >= 3:
        return "__end__"
    return "writer"


# ============================================================================
# 第三步: 构建工作流图
# ============================================================================
try:
    from langgraph.graph import END, StateGraph
    from langgraph.types import Command, interrupt
    from langgraph.checkpoint.memory import MemorySaver

    def human_review_interrupt(state: WritingState) -> Command[Literal["__end__"]]:
        """
        中断节点：触发 Human-in-the-Loop 暂停

        此节点抛出 Interrupt，LangGraph 会：
        1. 保存当前状态到 checkpointer
        2. 暂停执行
        3. 等待人类通过 Command 恢复

        人类需要调用：
        ```python
        graph.invoke(Command(resume={"human_feedback": "批准"}), config)
        ```
        """
        print("\n" + "=" * 50)
        print("⏸️  工作流已暂停，等待人类审核...")
        print("=" * 50)
        print(f"当前草稿长度: {len(state.get('draft_content', ''))} 字符")
        print("\n请通过 Command 注入反馈:")
        print('  graph.invoke(Command(resume={"human_feedback": "批准"}), config)')
        print("=" * 50)

        # 触发中断，等待人类输入
        # interrupt() 会暂停工作流并将控制权交给外部
        interrupt("human_review: 请审核草稿并通过 Command.resume 注入反馈")

        # 这行代码不会执行，因为 interrupt() 会暂停工作流
        return Command(goto=END)

    def create_hitl_graph():
        """
        创建 Human-in-the-Loop 工作流图

        流程:
        writer -> approval -> [interrupt | writer | END]

        - writer: 生成或修订内容
        - approval: 评估是否批准
        - interrupt: 等待人类输入的中断点
        """
        workflow = StateGraph(WritingState)

        # 注册节点
        workflow.add_node("writer", writer_node)
        workflow.add_node("approval", approval_node)
        workflow.add_node("human_review", human_review_interrupt)

        # 设置入口点
        workflow.set_entry_point("writer")

        # writer -> approval
        workflow.add_edge("writer", "approval")

        # approval 节点后的条件路由
        # 第一次审核 -> human_review 中断
        # 已批准 -> END
        # 修订 -> writer
        workflow.add_conditional_edges(
            "approval",
            _approval_router,
            {
                "human_review": "human_review",
                "writer": "writer",
                "__end__": END,
            },
        )

        # human_review 中断后回到 approval（等待新反馈）
        workflow.add_edge("human_review", "approval")

        # 使用 MemorySaver 实现状态持久化
        # 这允许通过 thread_id 恢复特定会话
        memory = MemorySaver()

        return workflow.compile(checkpointer=memory)

    def _approval_router(state: WritingState) -> Literal["human_review", "writer", "__end__"]:
        """
        approval 节点后的路由逻辑

        Args:
            state: 当前状态

        Returns:
            - human_review: 需要人类审核（首次或修订后）
            - writer: 需要继续修订
            - __end__: 结束工作流
        """
        # 如果 revision_count == 1（刚生成初稿），等待审核
        if state.get("revision_count", 0) == 1 and not state.get("approved", False):
            return "human_review"

        # 如果已批准
        if state.get("approved", False):
            return "__end__"

        # 如果修订次数过多
        if state.get("revision_count", 0) >= 3:
            return "__end__"

        # 否则继续修订
        return "writer"

    # LangGraph 可用时的运行函数
    def run_hitl_example():
        """运行 Human-in-the-Loop 示例"""
        print("=" * 60)
        print("L61 示例 3: Human-in-the-Loop 工作流")
        print("=" * 60)

        graph = create_hitl_graph()
        config = {"configurable": {"thread_id": "demo_session"}}

        # 初始状态
        from langchain_core.messages import HumanMessage

        initial_state: WritingState = {
            "messages": [HumanMessage(content="请写一篇关于 Python 异步编程的文章")],
            "draft_content": "",
            "human_feedback": "",
            "revision_count": 0,
            "approved": False,
        }

        # 第一轮：生成初稿并中断等待审核
        print("\n📝 第一轮：生成初稿")
        try:
            result = graph.invoke(initial_state, config)
            print(f"修订次数: {result['revision_count']}")
            print(f"草稿长度: {len(result['draft_content'])} 字符")
        except Exception as e:
            print(f"预期的中断: {e}")

        # 第二轮：注入修改建议并继续
        print("\n📝 第二轮：注入反馈")
        try:
            result = graph.invoke(
                Command(resume={"human_feedback": "请添加更多关于 asyncio.gather 的示例"}),
                config,
            )
            print(f"修订次数: {result['revision_count']}")
        except Exception as e:
            print(f"预期的中断: {e}")

        # 第三轮：批准
        print("\n📝 第三轮：批准")
        try:
            result = graph.invoke(
                Command(resume={"human_feedback": "批准"}),
                config,
            )
            print(f"修订次数: {result['revision_count']}")
            print(f"是否批准: {result['approved']}")
        except Exception as e:
            print(f"预期的中断: {e}")

    if __name__ == "__main__":
        run_hitl_example()

    def create_hitl_graph_for_test():
        """用于测试的简化版本（不使用 interrupt）"""
        workflow = StateGraph(WritingState)

        workflow.add_node("writer", writer_node)
        workflow.add_node("approval", approval_node)

        workflow.set_entry_point("writer")
        workflow.add_edge("writer", "approval")

        workflow.add_conditional_edges(
            "approval",
            should_continue,
            {
                "writer": "writer",
                "__end__": END,
            },
        )

        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

except ImportError:
    print("=" * 60)
    print("注意: LangGraph 未安装")
    print("安装命令: uv add langgraph")
    print("=" * 60)

    def create_hitl_graph():
        return None

    def create_hitl_graph_for_test():
        return None
