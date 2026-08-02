# examples/02_circuit_breaker.py
"""
断路器模式实现 - 防止级联故障

本模块演示微服务架构中的断路器模式。
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, TypeVar
T = TypeVar("T")


# ==================== 断路器状态 ====================


class CircuitState(Enum):
    """断路器状态"""

    CLOSED = "closed"  # 正常状态，请求通过
    OPEN = "open"  # 熔断状态，请求被拒绝
    HALF_OPEN = "half_open"  # 半开状态，允许部分请求通过


@dataclass
class CircuitStats:
    """断路器统计"""

    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    last_failure_time: float = 0

    @property
    def failure_rate(self) -> float:
        """失败率"""
        if self.total_calls == 0:
            return 0.0
        return self.failed_calls / self.total_calls


# ==================== 断路器实现 ====================


class CircuitBreaker:
    """
    断路器模式

    状态转换:
    - CLOSED -> OPEN: 失败次数超过阈值
    - OPEN -> HALF_OPEN: 熔断时间后
    - HALF_OPEN -> CLOSED: 试探成功
    - HALF_OPEN -> OPEN: 试探失败
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 3,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self._state = CircuitState.CLOSED
        self._stats = CircuitStats()
        self._last_state_change = time.time()
        self._half_open_calls = 0
        self._consecutive_failures = 0

    @property
    def state(self) -> CircuitState:
        """获取当前状态"""
        if self._state == CircuitState.OPEN:
            # 检查是否应该转换到 HALF_OPEN
            if time.time() - self._last_state_change >= self.recovery_timeout:
                self._transition_to(CircuitState.HALF_OPEN)
        return self._state

    def _transition_to(self, new_state: CircuitState):
        """状态转换"""
        old_state = self._state
        self._state = new_state
        self._last_state_change = time.time()

        if new_state == CircuitState.HALF_OPEN:
            self._half_open_calls = 0

        print(f"  [断路器] 状态转换: {old_state.value} -> {new_state.value}")

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """执行函数调用"""
        self._stats.total_calls += 1

        # 检查状态
        if self.state == CircuitState.OPEN:
            self._stats.rejected_calls += 1
            raise CircuitOpenError("Circuit is OPEN, call rejected")

        # 半开状态检查
        if self.state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1
            if self._half_open_calls > self.half_open_max_calls:
                self._stats.rejected_calls += 1
                raise CircuitOpenError("Circuit is HALF_OPEN, max calls exceeded")

        # 执行调用
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            self._on_success()
            return result

        except Exception:
            self._on_failure()
            raise

    def _on_success(self):
        """成功回调"""
        self._stats.successful_calls += 1
        self._consecutive_failures = 0

        if self.state == CircuitState.HALF_OPEN:
            # 试探成功，关闭断路器
            self._transition_to(CircuitState.CLOSED)

    def _on_failure(self):
        """失败回调"""
        self._stats.failed_calls += 1
        self._stats.last_failure_time = time.time()
        self._consecutive_failures += 1

        if self.state == CircuitState.HALF_OPEN:
            # 试探失败，重新打开断路器
            self._transition_to(CircuitState.OPEN)

        elif self._consecutive_failures >= self.failure_threshold:
            # 失败次数超过阈值
            self._transition_to(CircuitState.OPEN)

    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "state": self.state.value,
            "total_calls": self._stats.total_calls,
            "successful_calls": self._stats.successful_calls,
            "failed_calls": self._stats.failed_calls,
            "rejected_calls": self._stats.rejected_calls,
            "failure_rate": f"{self._stats.failure_rate:.2%}",
            "consecutive_failures": self._consecutive_failures,
        }


class CircuitOpenError(Exception):
    """断路器打开异常"""

    pass


# ==================== 模拟故障服务 ====================


class UnreliableService:
    """模拟不可靠的服务"""

    def __init__(self, failure_rate: float = 0.7):
        self.failure_rate = failure_rate
        self.call_count = 0

    async def call(self) -> dict:
        """模拟服务调用"""
        self.call_count += 1

        # 模拟随机失败
        if self.call_count % int(1 / self.failure_rate) == 0:
            raise ConnectionError(f"服务调用失败 (调用 #{self.call_count})")

        return {"success": True, "call_id": self.call_count, "message": "操作成功"}


# ==================== 带断路器的客户端 ====================


class CircuitBreakerClient:
    """带断路器的服务客户端"""

    def __init__(self, service: UnreliableService):
        self.service = service
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=3, recovery_timeout=5.0, half_open_max_calls=2
        )

    async def call(self) -> dict:
        """调用服务（带断路器保护）"""
        return await self.circuit_breaker.call(self.service.call)


# ==================== 演示 ====================


async def demo_circuit_breaker():
    """演示断路器模式"""
    print("\n" + "=" * 60)
    print("断路器模式演示")
    print("=" * 60)

    # 初始化
    service = UnreliableService(failure_rate=0.7)
    client = CircuitBreakerClient(service)

    # 正常调用（触发熔断）
    print("\n[1] 模拟服务调用（高失败率 70%）")
    print("    观察断路器状态变化:")

    for i in range(10):
        try:
            result = await client.call()
            print(f"  第{i + 1}次: 成功 - {result}")
        except CircuitOpenError as e:
            print(f"  第{i + 1}次: 拒绝 - {e}")
            print(f"  断路器状态: {client.circuit_breaker.state.value}")
        except ConnectionError as e:
            print(f"  第{i + 1}次: 失败 - {e}")
            print(f"  断路器状态: {client.circuit_breaker.state.value}")

    # 等待恢复
    print("\n[2] 等待断路器恢复...")
    print(f"  等待 {client.circuit_breaker.recovery_timeout} 秒...")
    await asyncio.sleep(client.circuit_breaker.recovery_timeout + 1)

    # 再次调用
    print("\n[3] 断路器恢复后调用")
    for i in range(5):
        try:
            result = await client.call()
            print(f"  第{i + 1}次: 成功 - {result}")
        except CircuitOpenError as e:
            print(f"  第{i + 1}次: 拒绝 - {e}")
        except ConnectionError as e:
            print(f"  第{i + 1}次: 失败 - {e}")

    # 统计信息
    print("\n[4] 断路器统计信息")
    stats = client.circuit_breaker.get_stats()
    for key, value in stats.items():
        print(f"    {key}: {value}")


async def demo_state_transitions():
    """演示状态转换"""
    print("\n" + "=" * 60)
    print("断路器状态转换演示")
    print("=" * 60)

    # 创建低阈值的断路器用于演示
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=3.0, half_open_max_calls=1)

    async def failing_call():
        raise ConnectionError("模拟失败")

    async def successful_call():
        return {"success": True}

    print(f"\n初始状态: {cb.state.value}")
    print(f"故障阈值: {cb.failure_threshold}")
    print(f"恢复超时: {cb.recovery_timeout}秒")

    # 触发熔断
    print("\n[1] 触发熔断 (连续失败)")
    for i in range(3):
        try:
            await cb.call(failing_call)
        except ConnectionError:
            pass
        print(f"    状态: {cb.state.value}, 连续失败: {cb._consecutive_failures}")

    # 等待恢复
    print("\n[2] 等待恢复超时...")
    print(f"  当前状态: {cb.state.value}")
    await asyncio.sleep(3.5)
    print(f"  等待后状态: {cb.state.value}")

    # 试探成功
    print("\n[3] 半开状态试探")
    try:
        result = await cb.call(successful_call)
        print(f"    成功: {result}")
    except Exception as e:
        print(f"    失败: {e}")

    print(f"  最终状态: {cb.state.value}")


async def main():
    """主函数"""
    await demo_circuit_breaker()
    await demo_state_transitions()

    print("\n" + "=" * 60)
    print("断路器模式演示完成！")
    print("=" * 60)
    print("\n断路器三状态:")
    print("  1. CLOSED (关闭): 正常请求通过")
    print("  2. OPEN (打开): 请求被拒绝")
    print("  3. HALF_OPEN (半开): 允许试探性请求")


if __name__ == "__main__":
    asyncio.run(main())
