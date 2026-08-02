"""
练习题 2: 自定义业务指标

创建 Agent 业务指标，追踪以下内容：
1. 会话开始/结束
2. Token 使用量
3. 工具调用统计
4. 成本累积

要求：
- 实现 Counter、Gauge、Histogram 指标
- 提供 record_* 方法记录指标
- 计算成本（gpt-4o-mini: $0.15/1M tokens 输入, $0.60/1M tokens 输出）
"""

from dataclasses import dataclass
from collections import defaultdict


@dataclass
class AgentMetrics:
    """
    Agent 业务指标收集器

    追踪指标：
    - 会话数
    - Token 使用量
    - 工具调用
    - 成本
    """

    # 模型定价（每百万 tokens）
    MODEL_PRICING = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},  # $/1M tokens
        "gpt-4o": {"input": 5.00, "output": 15.00},
        "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    }

    def __init__(self):
        # 指标存储
        self.conversations_started: int = 0
        self.conversations_completed: int = 0
        self.active_conversations: int = 0

        self.token_usage: dict[str, dict] = defaultdict(
            lambda: {"prompt": 0, "completion": 0, "total": 0}
        )
        self.tool_calls: dict[str, dict] = defaultdict(lambda: {"success": 0, "failure": 0})
        self.cost_by_user: dict[str, float] = defaultdict(float)
        self.total_cost: float = 0.0

    # TODO: 实现以下方法

    def record_conversation_start(self, user_id: str, source: str = "api") -> None:
        """记录会话开始"""
        raise NotImplementedError("需要实现")

    def record_conversation_end(self, user_id: str, turns: int, outcome: str = "success") -> None:
        """记录会话结束"""
        raise NotImplementedError("需要实现")

    def record_token_usage(
        self, user_id: str, model: str, prompt_tokens: int, completion_tokens: int
    ) -> None:
        """记录 Token 使用量"""
        raise NotImplementedError("需要实现")

    def record_tool_call(self, tool_name: str, success: bool, duration_ms: float) -> None:
        """记录工具调用"""
        raise NotImplementedError("需要实现")

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """计算成本（美元）"""
        # 公式: (prompt_tokens / 1_000_000) * input_price + (completion_tokens / 1_000_000) * output_price
        raise NotImplementedError("需要实现")

    def get_summary(self) -> dict:
        """获取指标摘要"""
        raise NotImplementedError("需要实现")


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("练习题 2: 自定义业务指标")
    print("=" * 60)

    # 创建指标收集器（完成后取消注释测试代码）
    _metrics = AgentMetrics()

    print("\n任务：")
    print("1. 实现 AgentMetrics 类的方法")
    print("2. 追踪会话、Token、工具调用和成本")
    print("3. 计算模型使用成本")

    print("\n提示：")
    print("- 使用 defaultdict 简化计数")
    print("- 成本 = (tokens / 1_000_000) * price")
    print("- MODEL_PRICING 字典提供定价信息")

    # 测试代码（完成后取消注释）
    """
    # 记录会话
    metrics.record_conversation_start("user_123", "api")
    metrics.record_conversation_start("user_456", "web")

    # 模拟 Token 使用
    metrics.record_token_usage("user_123", "gpt-4o-mini", 100, 50)
    metrics.record_token_usage("user_456", "gpt-4o-mini", 200, 100)

    # 模拟工具调用
    metrics.record_tool_call("search", True, 150.0)
    metrics.record_tool_call("calculator", True, 50.0)
    metrics.record_tool_call("search", False, 200.0)

    # 结束会话
    metrics.record_conversation_end("user_123", turns=5, outcome="success")
    metrics.record_conversation_end("user_456", turns=3, outcome="success")

    # 输出摘要
    summary = metrics.get_summary()
    print(f"会话统计: {summary['conversations']}")
    print(f"Token 使用: {summary['token_usage']}")
    print(f"工具调用: {summary['tool_calls']}")
    print(f"总成本: ${summary['total_cost']:.4f}")
    """


if __name__ == "__main__":
    main()
