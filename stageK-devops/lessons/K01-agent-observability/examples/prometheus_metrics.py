"""
示例 3: Prometheus 指标采集

展示如何定义和使用 Prometheus 指标。
"""

import time
from dataclasses import dataclass, field
from typing import Callable
from collections import defaultdict


# ============== 指标定义 ==============


@dataclass
class Counter:
    """简单的计数器实现"""

    name: str
    description: str
    labels: dict[str, str] = field(default_factory=dict)
    _value: float = 0.0

    def inc(self, amount: float = 1) -> None:
        """增加计数"""
        self._value += amount

    @property
    def value(self) -> float:
        return self._value


@dataclass
class Histogram:
    """简单的直方图实现"""

    name: str
    description: str
    buckets: list[float] = field(
        default_factory=lambda: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    )
    _counts: dict[float, int] = field(default_factory=lambda: defaultdict(int))
    _sum: float = 0.0
    _count: int = 0

    def observe(self, value: float) -> None:
        """观察值"""
        self._sum += value
        self._count += 1
        for bucket in self.buckets:
            if value <= bucket:
                self._counts[bucket] += 1

    def get_quantile(self, quantile: float) -> float:
        """获取分位数"""
        if self._count == 0:
            return 0.0
        return self._sum / self._count  # 简化：返回平均值


@dataclass
class Gauge:
    """简单的仪表盘实现"""

    name: str
    description: str
    _value: float = 0.0

    def set(self, value: float) -> None:
        """设置值"""
        self._value = value

    def inc(self, amount: float = 1) -> None:
        """增加"""
        self._value += amount

    def dec(self, amount: float = 1) -> None:
        """减少"""
        self._value -= amount

    @property
    def value(self) -> float:
        return self._value


# ============== 全局指标 ==============

# 计数器
request_counter = Counter(
    name="agent_requests_total",
    description="Total number of requests",
)

llm_call_counter = Counter(
    name="agent_llm_calls_total",
    description="Total number of LLM calls",
)

tool_call_counter = Counter(
    name="agent_tool_calls_total",
    description="Total number of tool calls",
)

# 直方图
request_duration = Histogram(
    name="agent_request_duration_seconds",
    description="Request duration in seconds",
)

llm_duration = Histogram(
    name="agent_llm_duration_seconds",
    description="LLM call duration in seconds",
)

# 仪表盘
active_requests = Gauge(
    name="agent_active_requests",
    description="Number of active requests",
)


# ============== 装饰器 ==============


def track_request(func: Callable) -> Callable:
    """请求跟踪装饰器"""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        active_requests.inc()

        try:
            result = func(*args, **kwargs)
            request_counter.inc()
            return result
        except Exception:
            request_counter.inc()  # 也计入错误
            raise
        finally:
            duration = time.time() - start_time
            request_duration.observe(duration)
            active_requests.dec()

    return wrapper


def track_llm_call(func: Callable) -> Callable:
    """LLM 调用跟踪装饰器"""

    def wrapper(*args, **kwargs):
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            llm_call_counter.inc()
            return result
        finally:
            duration = time.time() - start_time
            llm_duration.observe(duration)

    return wrapper


# ============== 示例函数 ==============


@track_request
def handle_request(request_id: str) -> dict:
    """处理请求"""
    time.sleep(0.1)  # 模拟处理
    return {"request_id": request_id, "status": "success"}


@track_llm_call
def call_llm(prompt: str) -> str:
    """调用 LLM"""
    time.sleep(0.5)  # 模拟 LLM 调用
    return f"Response to: {prompt[:20]}..."


# ============== 主函数 ==============


def main() -> None:
    """主函数"""
    print("=" * 60)
    print("Prometheus 指标采集示例")
    print("=" * 60)

    # 1. 模拟请求处理
    print("\n--- 模拟请求处理 ---")
    for i in range(5):
        result = handle_request(f"req_{i}")
        print(f"请求 {i}: {result['status']}")

    # 2. 模拟 LLM 调用
    print("\n--- 模拟 LLM 调用 ---")
    for i in range(3):
        response = call_llm(f"Prompt {i}")
        print(f"LLM {i}: {response[:30]}...")

    # 3. 模拟工具调用
    print("\n--- 模拟工具调用 ---")
    tool_call_counter.inc()
    tool_call_counter.inc()
    tool_call_counter.inc()
    print(f"工具调用次数: {tool_call_counter.value}")

    # 4. 输出指标
    print("\n--- 指标输出 ---")
    print(f"请求总数: {request_counter.value}")
    print(f"LLM 调用次数: {llm_call_counter.value}")
    print(f"工具调用次数: {tool_call_counter.value}")
    print(f"活跃请求数: {active_requests.value}")
    print(f"请求延迟 (avg): {request_duration.get_quantile(0.5):.4f}s")
    print(f"LLM 延迟 (avg): {llm_duration.get_quantile(0.5):.4f}s")

    # 5. 生成 Prometheus 格式输出
    print("\n--- Prometheus 格式输出 ---")
    print(f"# HELP {request_counter.name} {request_counter.description}")
    print(f"# TYPE {request_counter.name} counter")
    print(f"{request_counter.name} {request_counter.value}")

    print(f"\n# HELP {request_duration.name} {request_duration.description}")
    print(f"# TYPE {request_duration.name} histogram")
    print(f"{request_duration.name}_count {request_duration._count}")

    # 验证
    print("\n" + "=" * 60)
    print("验证")
    print("=" * 60)
    assert request_counter.value == 5, f"请求数应为 5，实际: {request_counter.value}"
    assert llm_call_counter.value == 3, f"LLM 调用应为 3，实际: {llm_call_counter.value}"
    assert active_requests.value == 0, f"活跃请求应为 0，实际: {active_requests.value}"
    print("✅ 指标采集验证通过!")


if __name__ == "__main__":
    main()
