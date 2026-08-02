"""
练习题 2 参考解答: 自定义业务指标
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
        self.conversation_turns: list[int] = []

        self.token_usage: dict[str, dict] = defaultdict(
            lambda: {"prompt": 0, "completion": 0, "total": 0}
        )
        self.tool_calls: dict[str, dict] = defaultdict(
            lambda: {"success": 0, "failure": 0, "total_duration_ms": 0.0}
        )
        self.cost_by_user: dict[str, float] = defaultdict(float)
        self.total_cost: float = 0.0
        self.total_tokens: int = 0

    def record_conversation_start(self, user_id: str, source: str = "api") -> None:
        """记录会话开始"""
        self.conversations_started += 1
        self.active_conversations += 1

    def record_conversation_end(self, user_id: str, turns: int, outcome: str = "success") -> None:
        """记录会话结束"""
        self.conversations_completed += 1
        self.active_conversations = max(0, self.active_conversations - 1)
        self.conversation_turns.append(turns)

    def record_token_usage(
        self, user_id: str, model: str, prompt_tokens: int, completion_tokens: int
    ) -> None:
        """记录 Token 使用量"""
        self.token_usage[model]["prompt"] += prompt_tokens
        self.token_usage[model]["completion"] += completion_tokens
        self.token_usage[model]["total"] += prompt_tokens + completion_tokens
        self.total_tokens += prompt_tokens + completion_tokens

        # 计算成本
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        self.cost_by_user[user_id] += cost
        self.total_cost += cost

    def record_tool_call(self, tool_name: str, success: bool, duration_ms: float) -> None:
        """记录工具调用"""
        if success:
            self.tool_calls[tool_name]["success"] += 1
        else:
            self.tool_calls[tool_name]["failure"] += 1
        self.tool_calls[tool_name]["total_duration_ms"] += duration_ms

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """计算成本（美元）"""
        pricing = self.MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})

        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    def get_summary(self) -> dict:
        """获取指标摘要"""
        # 平均会话轮次
        avg_turns = (
            sum(self.conversation_turns) / len(self.conversation_turns)
            if self.conversation_turns
            else 0
        )

        return {
            "conversations": {
                "started": self.conversations_started,
                "completed": self.conversations_completed,
                "active": self.active_conversations,
                "avg_turns": round(avg_turns, 2),
            },
            "token_usage": dict(self.token_usage),
            "total_tokens": self.total_tokens,
            "tool_calls": {
                tool: {
                    "success": data["success"],
                    "failure": data["failure"],
                    "total": data["success"] + data["failure"],
                    "avg_duration_ms": round(
                        data["total_duration_ms"] / max(1, data["success"] + data["failure"]), 2
                    ),
                }
                for tool, data in self.tool_calls.items()
            },
            "cost": {
                "total_usd": round(self.total_cost, 6),
                "by_user": {k: round(v, 6) for k, v in self.cost_by_user.items()},
            },
        }


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("练习题 2 参考解答: 自定义业务指标")
    print("=" * 60)

    # 创建指标收集器
    metrics = AgentMetrics()

    # 记录会话
    print("\n--- 模拟数据 ---")
    print("会话开始...")
    metrics.record_conversation_start("user_123", "api")
    metrics.record_conversation_start("user_456", "web")

    # 模拟 Token 使用
    print("Token 使用...")
    metrics.record_token_usage("user_123", "gpt-4o-mini", 100, 50)
    metrics.record_token_usage("user_456", "gpt-4o-mini", 200, 100)
    metrics.record_token_usage("user_123", "gpt-4o", 300, 150)

    # 模拟工具调用
    print("工具调用...")
    metrics.record_tool_call("search", True, 150.0)
    metrics.record_tool_call("calculator", True, 50.0)
    metrics.record_tool_call("search", False, 200.0)
    metrics.record_tool_call("search", True, 120.0)

    # 结束会话
    print("会话结束...")
    metrics.record_conversation_end("user_123", turns=5, outcome="success")
    metrics.record_conversation_end("user_456", turns=3, outcome="success")

    # 输出摘要
    print("\n--- 指标摘要 ---")
    summary = metrics.get_summary()

    print("\n会话统计:")
    conv = summary["conversations"]
    print(f"  开始: {conv['started']}")
    print(f"  完成: {conv['completed']}")
    print(f"  活跃: {conv['active']}")
    print(f"  平均轮次: {conv['avg_turns']}")

    print("\nToken 使用:")
    for model, usage in summary["token_usage"].items():
        print(
            f"  {model}: {usage['total']} tokens (prompt: {usage['prompt']}, completion: {usage['completion']})"
        )

    print("\n工具调用:")
    for tool, stats in summary["tool_calls"].items():
        print(
            f"  {tool}: {stats['total']} calls (success: {stats['success']}, failure: {stats['failure']})"
        )

    print("\n成本:")
    print(f"  总成本: ${summary['cost']['total_usd']:.6f}")
    for user, cost in summary["cost"]["by_user"].items():
        print(f"  {user}: ${cost:.6f}")

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert metrics.conversations_started == 2
    assert metrics.conversations_completed == 2
    assert metrics.total_tokens == 800  # 100+50+200+100+300+150
    assert metrics.total_cost > 0
    print("✅ 业务指标验证通过!")


if __name__ == "__main__":
    main()
