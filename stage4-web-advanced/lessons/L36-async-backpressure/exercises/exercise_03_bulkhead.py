"""练习 3：舱壁隔离模式（Bulkhead Pattern）

目标：实现舱壁隔离模式，保护系统不被单点故障拖垮

场景：
一个订单系统依赖三个外部服务：
- 支付服务（慢，延迟 500ms-2s）
- 库存服务（快，延迟 <50ms）
- 通知服务（中等，延迟 100-300ms）

如果支付服务变慢，不应该影响库存服务和通知服务的响应。

要求：
1. 实现 Bulkhead 类，实现舱壁隔离
2. 每个服务有独立的并发限制
3. 当某个服务达到并发上限时，返回特定错误而不是排队等待
4. 提供服务健康状态检查

提示：
- 舱壁模式：将系统分割成独立的隔间，单个隔间故障不影响其他隔间
- 每个服务使用独立的 Semaphore
- 记录每个服务的当前并发数
"""

import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import TypedDict


class ServiceStatus(Enum):
    """服务状态"""

    HEALTHY = "healthy"  # 健康
    DEGRADED = "degraded"  # 降级（并发高）
    OVERLOADED = "overloaded"  # 过载（达到上限）


class ServiceError(Exception):
    """服务错误基类"""


class ServiceOverloadedError(ServiceError):
    """服务过载错误"""


class ServiceResult(TypedDict):
    service: str
    success: bool
    latency_ms: float
    error: str | None


@dataclass
class ServiceMetrics:
    """服务指标"""

    total_requests: int = 0
    success_count: int = 0
    rejected_count: int = 0
    total_latency_ms: float = 0.0
    current_concurrency: int = 0


class Bulkhead:
    """舱壁隔离模式实现

    将不同服务隔离到独立的"舱室"中，
    单个服务的故障不会影响其他服务。
    """

    def __init__(self, service_configs: dict[str, int]):
        """初始化舱壁

        Args:
            service_configs: {服务名: 最大并发数}
        """
        # TODO: 为每个服务创建独立的 Semaphore 和指标

    async def call(
        self,
        service_name: str,
        coro: asyncio.coroutine,
        timeout: float = 5.0,
    ) -> ServiceResult:
        """调用服务（带舱壁保护）

        Args:
            service_name: 服务名称
            coro: 协程（实际的服务调用）
            timeout: 超时时间

        Returns:
            包含调用结果的字典
        """
        # TODO: 实现带舱壁保护的服务调用

    def get_metrics(self, service_name: str) -> ServiceMetrics:
        """获取服务指标"""
        # TODO: 返回服务指标

    def get_status(self, service_name: str) -> ServiceStatus:
        """获取服务状态"""
        # TODO: 根据指标判断服务状态

    def is_healthy(self) -> bool:
        """检查整体健康状态"""
        # TODO: 检查是否有服务过载


# ============ 测试代码 ============


async def mock_payment_service(amount: float) -> dict:
    """模拟支付服务（慢）"""
    await asyncio.sleep(0.5)  # 模拟 500ms 延迟
    return {"status": "paid", "amount": amount}


async def mock_inventory_service(product_id: str) -> dict:
    """模拟库存服务（快）"""
    await asyncio.sleep(0.05)  # 模拟 50ms 延迟
    return {"product_id": product_id, "stock": 100}


async def mock_notification_service(user_id: str, message: str) -> dict:
    """模拟通知服务（中等）"""
    await asyncio.sleep(0.2)  # 模拟 200ms 延迟
    return {"user_id": user_id, "sent": True}


async def test_bulkhead_basic():
    """测试舱壁基本功能"""
    bulkhead = Bulkhead(
        {
            "payment": 2,  # 支付服务最多 2 并发
            "inventory": 10,  # 库存服务最多 10 并发
            "notification": 5,  # 通知服务最多 5 并发
        }
    )

    # 测试正常调用
    result = await bulkhead.call(
        "inventory",
        mock_inventory_service("product_001"),
    )
    assert result["success"], f"调用应成功: {result}"
    assert result["latency_ms"] < 100, f"库存服务应快速: {result['latency_ms']}ms"

    print("✅ 舱壁基本功能测试通过")


async def test_bulkhead_isolation():
    """测试舱壁隔离效果"""
    bulkhead = Bulkhead(
        {
            "payment": 2,
            "inventory": 10,
            "notification": 5,
        }
    )

    # 同时调用多个服务
    start = asyncio.get_event_loop().time()

    # 支付服务：2 个并发调用（各 500ms）
    payment_tasks = [bulkhead.call("payment", mock_payment_service(100.0)) for _ in range(2)]

    # 库存服务：10 个并发调用（各 50ms）
    inventory_tasks = [bulkhead.call("inventory", mock_inventory_service(f"p_{i}")) for i in range(10)]

    all_tasks = payment_tasks + inventory_tasks
    results = await asyncio.gather(*all_tasks)

    elapsed = asyncio.get_event_loop().time() - start

    # 库存服务应该独立快速完成，不受支付服务影响
    inventory_results = [r for r in results if r["service"] == "inventory"]
    for r in inventory_results:
        assert r["success"], f"库存服务应成功: {r}"
        assert r["latency_ms"] < 100, f"库存服务应快速完成: {r['latency_ms']}ms"

    print(f"✅ 舱壁隔离测试通过（总耗时: {elapsed:.2f}s）")


async def test_bulkhead_overload():
    """测试服务过载保护"""
    bulkhead = Bulkhead(
        {
            "payment": 2,
        }
    )

    # 触发过载：创建超过限制的并发调用
    tasks = [
        bulkhead.call("payment", mock_payment_service(100.0))
        for _ in range(5)  # 5 个调用，但限制是 2
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 应该有部分调用被拒绝或超时
    successful = [r for r in results if isinstance(r, dict) and r.get("success")]
    assert len(successful) <= 2, f"成功数不应超过限制: {len(successful)}"

    # 检查指标
    metrics = bulkhead.get_metrics("payment")
    assert metrics.rejected_count > 0 or metrics.total_requests == 5

    print("✅ 舱壁过载保护测试通过")


async def test_bulkhead_health_status():
    """测试健康状态检查"""
    bulkhead = Bulkhead(
        {
            "payment": 2,
            "inventory": 10,
        }
    )

    # 初始状态应健康
    assert bulkhead.is_healthy(), "初始应健康"

    # 触发支付服务过载
    tasks = [bulkhead.call("payment", mock_payment_service(100.0)) for _ in range(5)]
    await asyncio.gather(*tasks, return_exceptions=True)

    # 检查状态
    status = bulkhead.get_status("payment")
    metrics = bulkhead.get_metrics("payment")

    # 状态应根据并发情况变化
    print(f"支付服务状态: {status}, 指标: {metrics}")

    print("✅ 舱壁健康状态检查测试通过")


async def run_all_tests():
    """运行所有测试"""
    await test_bulkhead_basic()
    await test_bulkhead_isolation()
    await test_bulkhead_overload()
    await test_bulkhead_health_status()
    print("\n🎉 所有测试通过!")


if __name__ == "__main__":
    asyncio.run(run_all_tests())
