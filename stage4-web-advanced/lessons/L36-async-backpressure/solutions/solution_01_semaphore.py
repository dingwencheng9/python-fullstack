"""参考答案 1：Semaphore 信号量控制并发

基于 exercise_01_semaphore.py 的参考答案
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
        # 为每个供应商创建独立的 Semaphore 和统计
        self._semaphores: dict[str, asyncio.Semaphore] = {}
        self._stats: dict[str, SupplierStats] = {}
        self._max_concurrent = max_concurrent

    def _get_or_create_supplier(self, supplier_id: str) -> None:
        """获取或创建供应商的信号量和统计"""
        if supplier_id not in self._semaphores:
            self._semaphores[supplier_id] = asyncio.Semaphore(self._max_concurrent)
            self._stats[supplier_id] = SupplierStats()

    async def call_supplier(
        self,
        supplier_id: str,
        product_id: str,
        timeout: float = 5.0,
    ) -> RequestResult:
        """调用供应商 API"""
        self._get_or_create_supplier(supplier_id)
        semaphore = self._semaphores[supplier_id]
        stats = self._stats[supplier_id]

        start_time = asyncio.get_event_loop().time()
        try:
            async with asyncio.timeout(timeout):
                async with semaphore:
                    # 模拟 API 调用
                    wait_time = asyncio.get_event_loop().time() - start_time
                    # 更新统计
                    async with stats.lock:
                        stats.success_count += 1
                        stats.total_wait_time += wait_time
                    return RequestResult(
                        supplier=supplier_id, success=True, wait_time=wait_time
                    )
        except asyncio.TimeoutError:
            async with stats.lock:
                stats.failed_count += 1
            return RequestResult(
                supplier=supplier_id,
                success=False,
                wait_time=timeout,
            )

    def get_stats(self, supplier_id: str) -> dict:
        """获取供应商统计信息"""
        if supplier_id not in self._stats:
            return {"success_count": 0, "failed_count": 0, "total_wait_time": 0.0}
        stats = self._stats[supplier_id]
        return {
            "success_count": stats.success_count,
            "failed_count": stats.failed_count,
            "total_wait_time": stats.total_wait_time,
        }

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
        tasks = [self.call_supplier(supplier_id, product_id) for supplier_id, product_id in calls]
        return await asyncio.gather(*tasks)


# ============ 测试代码 ============


async def test_semaphore_controlled_client():
    """测试 SemaphoreControlledClient"""
    client = SemaphoreControlledClient(max_concurrent=5)

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
