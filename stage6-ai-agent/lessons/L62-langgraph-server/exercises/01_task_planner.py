"""
L55 练习: 任务规划 Agent

练习目标:
使用 LangGraph 构建一个 Plan-and-Execute 风格的规划执行循环。

任务描述:
1. planner_node: 将用户任务分解为步骤列表
2. executor_node: 执行当前步骤
3. should_continue: 判断是否继续执行
4. 循环直到所有步骤完成

TODO 模板 — 请补全函数逻辑。
"""

from __future__ import annotations

from typing import Literal


# --- 状态定义 ---
class PlanState(dict):
    """规划执行状态。"""

    input: str  # 用户原始输入
    plan: list[str]  # 剩余计划步骤
    past_steps: list[str]  # 已完成步骤
    result: str  # 最终结果


def planner_node(state: PlanState) -> PlanState:
    """将用户任务分解为步骤列表。

    TODO: 实现任务分解逻辑
    提示：解析 state["input"]，按序号（如 "1. xxx"）拆分为步骤列表
    """
    state["input"]
    # 提示：简单实现可以按换行符分割，再过滤空行
    raise NotImplementedError("请实现 planner_node，将用户输入分解为步骤列表")


def executor_node(state: PlanState) -> PlanState:
    """执行当前第一个步骤。

    TODO: 实现步骤执行逻辑
    提示：从 state["plan"] 取第一个步骤，将结果追加到 past_steps，plan 移除该步骤
    """
    raise NotImplementedError("请实现 executor_node，执行当前步骤并更新状态")


def should_continue(state: PlanState) -> Literal["execute", "end"]:
    """判断是否继续执行。

    TODO: 实现路由逻辑
    提示：state["plan"] 非空 → "execute"，否则 → "end"
    """
    raise NotImplementedError("请实现 should_continue 路由函数")


def summarize_node(state: PlanState) -> PlanState:
    """汇总执行结果。

    TODO: 实现结果汇总
    提示：将 state["past_steps"] 格式化为最终输出
    """
    raise NotImplementedError("请实现 summarize_node，汇总执行结果")


# --- 构建图结构（伪代码，用于理解）---
def describe_graph() -> str:
    """返回图的文字描述。"""
    return """
    LangGraph Plan-and-Execute 图结构:

    START
      │
      ▼
    planner ──→ [plan: [...], input: "...", past_steps: [], result: ""]
      │
      ▼
    execute ◄──────────────────────────────────────────┐
      │                                                 │
      ▼                                                 │
    [plan 非空?] ── 是 ──→ (返回 execute)                │
      │                                                 │
      否                                                │
      ▼                                                 │
   summarize ──→ END ◄─────────────────────────────────┘
    """
