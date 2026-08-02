"""
L55 练习参考答案: 任务规划 Agent

参考实现（不唯一）：
- 支持按自然语言任务自动分解
- 支持顺序执行步骤
- 支持循环终止判断
"""

from __future__ import annotations

from typing import Literal
import re


class PlanState(dict):
    """规划执行状态。"""

    input: str
    plan: list[str]
    past_steps: list[str]
    result: str


def planner_node(state: PlanState) -> PlanState:
    """将用户任务分解为步骤列表（简化版：按行拆分）。"""
    user_input = state["input"]
    # 按换行拆分，提取带序号或"步骤"的行
    lines = user_input.strip().split("\n")
    steps = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 移除常见前缀：1. 2. - * 步骤X:
        cleaned = re.sub(r"^(?:\d+[.)]|[-*]\s*|步骤\d+[:：]\s*)", "", line)
        if cleaned:
            steps.append(cleaned)
    if not steps:
        steps = [f"处理任务: {user_input}"]
    return {
        "input": state["input"],
        "plan": steps,
        "past_steps": [],
        "result": "",
    }


def executor_node(state: PlanState) -> PlanState:
    """执行当前第一个步骤。"""
    if not state["plan"]:
        return state
    current = state["plan"][0]
    result = f"[执行] {current}"
    return {
        "input": state["input"],
        "plan": state["plan"][1:],
        "past_steps": state["past_steps"] + [result],
        "result": "",
    }


def should_continue(state: PlanState) -> Literal["execute", "end"]:
    """plan 非空则继续，否则结束。"""
    return "execute" if state["plan"] else "end"


def summarize_node(state: PlanState) -> PlanState:
    """汇总执行结果。"""
    summary = "\n".join(f"  ✓ {step}" for step in state["past_steps"])
    return {
        "input": state["input"],
        "plan": [],
        "past_steps": state["past_steps"],
        "result": f"任务完成，共 {len(state['past_steps'])} 个步骤:\n{summary}",
    }


# --- 模拟执行 ---
def run_workflow(task: str) -> str:
    """模拟完整工作流执行。"""
    state: PlanState = {
        "input": task,
        "plan": [],
        "past_steps": [],
        "result": "",
    }
    state = planner_node(state)
    while True:
        route = should_continue(state)
        if route == "end":
            break
        state = executor_node(state)
    state = summarize_node(state)
    return state["result"]


if __name__ == "__main__":
    task = """
    1. 分析需求
    2. 设计架构
    3. 编写代码
    4. 测试验证
    """
    print(run_workflow(task))
