"""练习 1：Semaphore 信号量控制并发

目标：使用 asyncio.Semaphore 实现带并发限制的 API 调用

场景：
一家电商系统需要调用多个供应商的库存接口。
每个供应商最多同时处理 5 个请求，超过的请求需要等待。

要求：
1. 实现 SemaphoreControlledClient 类
2. 限制每个供应商最多 5 个并发请求
3. 当并发满时，请求应该等待而不是被拒绝
4. 统计每个供应商的成功/失败/等待请求数

提示：
- 使用 asyncio.Semaphore 控制并发
- 使用 asyncio.Lock 保护统计数据的更新
- 考虑使用 asyncio.wait_for 添加超时
"""

import asyncio
from dataclasses import dataclass, field
from typing import TypedDict


class RequestResult(TypedDict):
    supplier: str
    success: bool
    wait_time: float


@dataclass
class SupplierStats:
    """供应商请求统计"""

    success_count: int = 0
    failed_count: int = 0
    total_wait_time: float = 0.0
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)


class SemaphoreControlledClient:
    """带 Semaphore 并发控制的 API 客户端"""

    def __init__(self, max_concurrent: int = 5):
        # TODO: 初始化 Semaphore 和各供应商的统计
        pass

    async def call_supplier(
        self,
        supplier_id: str,
        product_id: str,
        timeout: float = 5.0,
    ) -> RequestResult:
        """调用供应商 API

        Args:
            supplier_id: 供应商 ID
            product_id: 产品 ID
            timeout: 超时时间（秒）

        Returns:
            包含调用结果的字典
        """
        # TODO: 实现带 Semaphore 的调用逻辑

    def get_stats(self, supplier_id: str) -> dict:
        """获取供应商统计信息"""
        # TODO: 返回统计信息

    async def batch_call(
        self,
        calls: list[tuple[str, str]],
    ) -> list[RequestResult]:
        """批量调用多个供应商

        Args:
            calls: [(supplier_id, product_id), ...]

        Returns:
            所有调用结果
        """
        # TODO: 并发执行所有调用


# ============ 测试代码 ============


async def test_semaphore_controlled_client():
    """测试 SemaphoreControlledClient"""
    client = SemaphoreControlledClient(max_concurrent=5)

    # 模拟供应商 API
    async def mock_supplier_api(supplier_id: str, product_id: str) -> dict:
        await asyncio.sleep(0.1)  # 模拟网络延迟
        return {"supplier": supplier_id, "stock": 100, "price": 99.9}

    # 测试单个调用
    result = await client.call_supplier("supplier_a", "product_001")
    assert result["success"], f"调用失败: {result}"
    assert client.get_stats("supplier_a")["success_count"] == 1

    # 测试并发调用（验证 Semaphore 生效）
    calls = [("supplier_b", f"product_{i:03d}") for i in range(10)]
    results = await client.batch_call(calls)

    # 验证所有调用都成功
    success_count = sum(1 for r in results if r["success"])
    assert success_count == 10, f"预期 10 个成功，实际 {success_count} 个"

    # 验证统计正确
    stats = client.get_stats("supplier_b")
    assert stats["success_count"] == 10, f"统计失败: {stats}"

    print("✅ 所有测试通过")


if __name__ == "__main__":
    asyncio.run(test_semaphore_controlled_client())
