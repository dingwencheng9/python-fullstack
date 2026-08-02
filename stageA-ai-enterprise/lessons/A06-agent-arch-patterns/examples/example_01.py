"""A06 示例：Agent 架构设计模式

本示例演示几种常见的 Agent 架构模式。
"""

from dataclasses import dataclass, field
from typing import TypedDict, Annotated, Literal
from operator import add
from enum import Enum


class AgentMode(Enum):
    """Agent 运行模式"""

    REACT = "react"  # 推理-行动-观察
    PLAN_EXECUTE = "plan_execute"  # 计划-执行
    RAFT = "raft"  # 检索增强微调


@dataclass
class AgentConfig:
    """Agent 配置"""

    mode: AgentMode = AgentMode.REACT
    max_steps: int = 10
    temperature: float = 0.7


class AgentState(TypedDict):
    """Agent 状态"""

    messages: Annotated[list, add]
    current_step: int
    observation: str
    plan: list[str] | None


def react_step(state: AgentState) -> AgentState:
    """ReAct 模式：推理-行动-观察"""
    messages = state["messages"]
    step = state["current_step"]

    # 推理：根据当前状态决定下一步行动
    thought = f"Step {step}: 分析当前情况..."

    # 行动：执行某个动作
    action = f"执行动作 {step}"

    # 观察：获取行动结果
    observation = f"观察到: {action} 的结果"

    return {
        "messages": messages + [("assistant", f"{thought}\n{action}")],
        "current_step": step + 1,
        "observation": observation,
        "plan": None,
    }


def plan_execute_loop(state: AgentState) -> AgentState:
    """Plan-Execute 模式：先计划后执行"""
    if not state.get("plan"):
        # 生成计划
        plan = ["步骤1: 准备数据", "步骤2: 处理", "步骤3: 输出结果"]
        return {**state, "plan": plan, "current_step": 0}

    plan = state["plan"]
    step = state["current_step"]

    if step >= len(plan):
        return {**state, "observation": "计划完成"}

    # 执行当前步骤
    current_action = plan[step]
    return {**state, "current_step": step + 1, "observation": f"执行: {current_action}"}


def main():
    """主函数"""
    config = AgentConfig(mode=AgentMode.REACT)
    print(f"Agent 配置: mode={config.mode.value}, max_steps={config.max_steps}")

    # 初始化状态
    state: AgentState = {
        "messages": [("user", "帮我分析这段代码")],
        "current_step": 0,
        "observation": "",
        "plan": None,
    }

    # 运行 ReAct 模式
    print("\n=== ReAct 模式 ===")
    for _ in range(config.max_steps):
        state = react_step(state)
        print(f"Step {state['current_step']}: {state['observation']}")
        if state["current_step"] >= 3:
            break

    print("\n=== Plan-Execute 模式 ===")
    state["current_step"] = 0
    state["plan"] = None
    for _ in range(5):
        state = plan_execute_loop(state)
        print(state["observation"])
        if state.get("observation") == "计划完成":
            break


if __name__ == "__main__":
    main()
