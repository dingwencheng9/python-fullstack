"""
A06: Agent 架构设计模式 - 核心实现

本模块实现了几种常见的 Agent 架构设计模式：
1. ReAct 模式：推理-行动-观察循环
2. Plan-Execute 模式：计划-执行分离
3. RAFT 模式：检索增强微调

参考论文：
- ReAct: Synergizing Reasoning and Acting in Language Models
- Plan-Then-Execute: 自动驾驶仪模式
- RAFT: Reward rAnked FineTuning
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, Generic, TypeVar
from typing_extensions import override

ToolFunc = Callable[[dict[str, Any]], str]

T = TypeVar("T")


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
    timeout: int = 30


@dataclass
class StepResult:
    """步骤执行结果"""

    step: int
    thought: str  # 推理过程
    action: str  # 执行的动作
    observation: str  # 观察结果
    timestamp: datetime = field(default_factory=datetime.now)


class AgentArchPatterns(ABC):
    """
    Agent 架构模式基类

    提供统一的接口和通用功能：
    - 状态管理
    - 步骤追踪
    - 错误处理
    """

    def __init__(self, name: str, config: AgentConfig | None = None):
        """
        初始化 Agent

        Args:
            name: Agent 名称
            config: Agent 配置
        """
        self.name = name
        self.config = config or AgentConfig()
        self.steps: list[StepResult] = []
        self.memory: list[dict[str, Any]] = []

    @abstractmethod
    def think(self, state: dict[str, Any]) -> str:
        """
        推理：分析当前状态，决定下一步行动

        Args:
            state: 当前状态

        Returns:
            推理结果
        """
        pass

    @abstractmethod
    def act(self, thought: str, state: dict[str, Any]) -> str:
        """
        行动：执行推理决定的行动

        Args:
            thought: 推理结果
            state: 当前状态

        Returns:
            行动结果
        """
        pass

    @abstractmethod
    def observe(self, action_result: str, state: dict[str, Any]) -> dict[str, Any]:
        """
        观察：处理行动结果，更新状态

        Args:
            action_result: 行动结果
            state: 当前状态

        Returns:
            更新后的状态
        """
        pass

    def run(self, initial_state: dict[str, Any]) -> dict[str, Any]:
        """
        运行 Agent

        Args:
            initial_state: 初始状态

        Returns:
            最终状态
        """
        state = initial_state.copy()
        max_steps = self.config.max_steps

        for step in range(max_steps):
            # 推理
            thought = self.think(state)
            self.steps.append(StepResult(step=step, thought=thought, action="", observation=""))

            # 行动
            action_result = self.act(thought, state)
            self.steps[-1].action = action_result

            # 观察
            state = self.observe(action_result, state)
            self.steps[-1].observation = str(state)

            # 检查是否完成
            if self._is_complete(state):
                break

        return state

    def _is_complete(self, state: dict[str, Any]) -> bool:
        """检查是否完成"""
        complete: bool = state.get("complete", False)
        done: bool = state.get("done", False)
        return complete or done

    def get_history(self) -> list[StepResult]:
        """获取执行历史"""
        return self.steps.copy()


# ============================================================================
# ReAct 模式实现
# ============================================================================
class ReactAgent(AgentArchPatterns):
    """
    ReAct Agent: 推理-行动-观察循环

    核心思想：
    1. 推理（Reasoning）：分析当前情况
    2. 行动（Acting）：执行相应动作
    3. 观察（Observing）：获取反馈，更新认知
    """

    def __init__(self, name: str, tools: list[ToolFunc] | None = None, config: AgentConfig | None = None):
        super().__init__(name, config)
        self.tools: list[ToolFunc] = tools or []

    @override
    def think(self, state: dict[str, Any]) -> str:
        """推理过程"""
        context = state.get("context", "")
        history = "\n".join([f"Step {s.step}: {s.thought[:50]}..." for s in self.steps[-3:]])

        return f"分析当前情况: {context[:100]}... 历史: {history}"

    @override
    def act(self, thought: str, state: dict[str, Any]) -> str:
        """执行行动"""
        if not self.tools:
            return f"[模拟执行] {thought[:50]}..."

        # 选择工具执行
        for tool in self.tools:
            result: str = tool(state)
            return result

        return "[无工具可用]"

    @override
    def observe(self, action_result: str, state: dict[str, Any]) -> dict[str, Any]:
        """更新状态"""
        new_state = state.copy()
        new_state["last_result"] = action_result
        new_state["step_count"] = len(self.steps)

        # 简单完成条件
        if "完成" in action_result or "success" in action_result.lower():
            new_state["complete"] = True

        return new_state


# ============================================================================
# Plan-Execute 模式实现
# ============================================================================
class PlanExecuteAgent(AgentArchPatterns):
    """
    Plan-Execute Agent: 计划-执行分离

    核心思想：
    1. 先制定完整计划
    2. 按计划逐步执行
    3. 可在执行中调整计划
    """

    def __init__(self, name: str, config: AgentConfig | None = None):
        super().__init__(name, config)
        self.current_plan: list[str] = []

    @override
    def think(self, state: dict[str, Any]) -> str:
        """制定或更新计划"""
        if not self.current_plan:
            # 生成计划
            task = state.get("task", "")
            self.current_plan = [
                f"步骤1: 分析任务 - {task[:50]}",
                "步骤2: 准备资源",
                "步骤3: 执行核心逻辑",
                "步骤4: 验证结果",
            ]
            return "制定计划中..."

        # 返回当前计划状态
        current_step = len([s for s in self.steps if s.action])
        if current_step < len(self.current_plan):
            return f"执行计划: {self.current_plan[current_step]}"

        return "计划完成"

    @override
    def act(self, thought: str, state: dict[str, Any]) -> str:
        """执行计划步骤"""
        current_step = len([s for s in self.steps if s.action])

        if current_step < len(self.current_plan):
            return f"执行中: {self.current_plan[current_step]}"

        return "所有计划步骤已完成"

    @override
    def observe(self, action_result: str, state: dict[str, Any]) -> dict[str, Any]:
        """更新状态"""
        new_state = state.copy()
        new_state["plan"] = self.current_plan
        new_state["executed_steps"] = len([s for s in self.steps if s.action])

        # 检查是否完成
        if len(self.current_plan) > 0 and len([s for s in self.steps if s.action]) >= len(self.current_plan):
            new_state["complete"] = True

        return new_state


# ============================================================================
# 主函数
# ============================================================================
def main() -> None:
    """演示各种 Agent 模式"""
    print("=" * 60)
    print("A06: Agent 架构设计模式演示")
    print("=" * 60)

    # ReAct Agent
    print("\n### ReAct Agent ###")
    react = ReactAgent("研究助手", config=AgentConfig(max_steps=3))
    result = react.run({"context": "研究 Python 异步编程", "task": "async"})
    print(f"结果: {result}")

    # Plan-Execute Agent
    print("\n### Plan-Execute Agent ###")
    planner = PlanExecuteAgent("任务规划助手", config=AgentConfig(max_steps=5))
    result = planner.run({"task": "完成数据分析报告"})
    print(f"计划: {planner.current_plan}")
    print(f"结果: {result}")

    print("\n" + "=" * 60)
    print("演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
