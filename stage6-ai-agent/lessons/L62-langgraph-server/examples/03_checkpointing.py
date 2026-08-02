"""
L55 示例: 状态持久化与检查点

学习目标:
- MemorySaver（内存）和模拟 PostgreSQLSaver 的 API
- 带 thread_id 的状态恢复
- Human-in-the-Loop 中断模拟
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class Checkpoint:
    """简化版检查点对象，模拟 langgraph.checkpoint.base.Checkpoint。"""

    thread_id: str
    step: int
    values: dict
    next_node: str | None = None
    timestamp: float = field(default_factory=time.time)


class MemorySaver:
    """简化版 MemorySaver，线程安全地存储检查点。"""

    def __init__(self) -> None:
        self._checkpoints: dict[str, list[Checkpoint]] = {}

    def put(self, thread_id: str, checkpoint: Checkpoint) -> None:
        if thread_id not in self._checkpoints:
            self._checkpoints[thread_id] = []
        self._checkpoints[thread_id].append(checkpoint)

    def get(self, thread_id: str) -> Checkpoint | None:
        history = self._checkpoints.get(thread_id, [])
        return history[-1] if history else None

    def get_history(self, thread_id: str) -> list[Checkpoint]:
        return list(self._checkpoints.get(thread_id, []))


class InterruptManager:
    """简化版中断管理器，模拟 interrupt_before / interrupt_after。"""

    def __init__(self) -> None:
        self._pending: dict[str, bool] = {}

    def should_interrupt(self, thread_id: str, before_node: str) -> bool:
        return self._pending.get(thread_id, False)

    def pause(self, thread_id: str) -> None:
        self._pending[thread_id] = True

    def resume(self, thread_id: str) -> None:
        self._pending[thread_id] = False


# --- 模拟 LangGraph 检查点工作流 ---
def simulate_workflow_with_checkpoint() -> dict:
    """模拟带 MemorySaver 的工作流执行。"""
    saver = MemorySaver()
    thread_id = "user-123"
    steps = ["agent", "tools", "agent", "tools", "agent"]

    for i, node in enumerate(steps):
        state = {"messages": [f"[step {i}] {node} executed"], "iteration": i}
        saver.put(thread_id, Checkpoint(thread_id=thread_id, step=i, values=state, next_node=steps[i + 1] if i + 1 < len(steps) else None))

    latest = saver.get(thread_id)
    history = saver.get_history(thread_id)
    return {
        "latest_step": latest.step if latest else None,
        "history_length": len(history),
        "can_resume": latest is not None,
    }


def simulate_human_in_the_loop() -> dict:
    """模拟 Human-in-the-Loop 中断工作流。"""
    interrupt_mgr = InterruptManager()
    thread_id = "workflow-1"

    # 步骤 1: Agent 生成内容
    agent_output = {"messages": ["[agent] 生成了代码方案，请审批"], "draft": "x = 1"}

    # 步骤 2: 中断等待人类审批
    should_pause = interrupt_mgr.should_interrupt(thread_id, "human_review")
    interrupt_mgr.pause(thread_id)

    # 步骤 3: 人类审批
    human_approved = True

    # 步骤 4: 恢复执行
    if human_approved:
        interrupt_mgr.resume(thread_id)
        final_output = {**agent_output, "approved": True}
    else:
        final_output = {**agent_output, "approved": False, "messages": agent_output["messages"] + ["[agent] 请修改后重新提交"]}

    return {
        "step1_paused": should_pause,
        "human_approved": human_approved,
        "final_messages": final_output["messages"],
    }


# --- 演示运行 ---
if __name__ == "__main__":
    print("=== 1. 检查点保存与恢复 ===")
    result = simulate_workflow_with_checkpoint()
    print(f"  最新步骤: {result['latest_step']}")
    print(f"  历史长度: {result['history_length']}")
    print(f"  可恢复: {result['can_resume']}")

    print("\n=== 2. Human-in-the-Loop ===")
    hitl = simulate_human_in_the_loop()
    print(f"  初始中断: {hitl['step1_paused']}")
    print(f"  人类批准: {hitl['human_approved']}")
    for msg in hitl["final_messages"]:
        print(f"  {msg}")
