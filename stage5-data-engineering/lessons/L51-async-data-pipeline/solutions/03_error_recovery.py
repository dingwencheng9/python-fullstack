"""

from __future__ import annotations

练习 3: 错误处理与恢复 - 参考答案

【Python 3.13 新特性展示】

1. PEP 695 泛型语法：
   - ResilientPipeline[T]: 泛型容错管道
   - DeadLetterQueue[T]: 泛型死信队列
   - 类型参数直接在类定义中声明

2. asyncio.TaskGroup 并发：
   - 并行重试处理
   - 批量断点保存
   - 优雅关闭任务管理

3. match/case 模式匹配：
   - 错误类型分类
   - 重试策略选择
   - 恢复状态处理

4. Free-threading 线程安全：
   - 死信队列的线程安全
   - 断点状态的并发保护

【解题思路】

1. 重试策略设计：
   - 指数退避：delay = base * (2^retry_count)
   - 最大延迟限制：防止无限等待
   - 抖动（Jitter）：避免惊群效应
   - 选择性重试：区分可重试和不可重试错误

2. 死信队列（DLQ）：
   - 隔离失败项：不阻塞正常流程
   - 保留错误信息：便于调试
   - 支持重试：修复后重新处理
   - 限制大小：防止内存溢出

3. 断点续传实现：
   - 定期保存状态：每N个或每N秒
   - 幂等性设计：重复处理不影响结果
   - 位置标记：记录已处理的位置
   - 快速恢复：从断点处继续

4. 优雅关闭策略：
   - 停止接收新任务
   - 等待当前任务完成
   - 保存断点
   - 释放资源

5. 生产优化：
   - 使用分布式协调（ZooKeeper、Consul）
   - 实现At-Least-Once或Exactly-Once语义
   - 添加可观测性（日志、追踪、指标）
   - 实现自动故障转移

【关键知识点】

- Exponential Backoff（指数退避）
- Dead Letter Queue（死信队列）
- Checkpoint（断点续传）
- Graceful Shutdown（优雅关闭）
- Idempotency（幂等性）
"""

import asyncio
import json
import random
import time
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass
from typing import Any, TypeVar

T = TypeVar("T")


# ============================================================================
# 1. 定义错误和重试策略
# ============================================================================


@dataclass
class RetryConfig:
    """重试策略配置"""

    max_retries: int = 3
    base_delay: float = 1.0  # seconds
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True  # 添加随机抖动


@dataclass
class ErrorRecord:
    """错误记录

    🔒 Free-threading 线程安全说明:
    - 记录创建后应视为不可变
    - retry_count 的修改应在单个协程中进行
    """

    item: Any
    error: Exception
    timestamp: float
    retry_count: int = 0
    error_type: str = ""

    def __post_init__(self) -> None:
        self.error_type = type(self.error).__name__


# ============================================================================
# 2. 实现重试机制
# ============================================================================


async def retry_with_backoff[T, R](func: Callable[[T], R], item: T, config: RetryConfig) -> tuple[bool, R | None, Exception | None]:
    """带指数退避的重试（使用 match/case 处理错误类型）"""
    last_error = None

    for attempt in range(config.max_retries + 1):
        try:
            # 执行函数
            if asyncio.iscoroutinefunction(func):
                result = await func(item)
            else:
                result = func(item)

        except Exception as e:
            last_error = e

            # 使用 match/case 判断错误类型（可扩展为不同的重试策略）
            match type(e).__name__:
                case "ValueError" | "TypeError":
                    # 这些错误通常不可重试
                    return False, None, e
                case "ConnectionError" | "TimeoutError":
                    # 网络错误，适合重试
                    pass
                case _:
                    # 其他错误，默认重试
                    pass

            # 最后一次尝试失败
            if attempt == config.max_retries:
                return False, None, e

            # 计算延迟时间（指数退避）
            delay = min(config.base_delay * (config.exponential_base**attempt), config.max_delay)

            # 添加随机抖动
            if config.jitter:
                delay = delay * (0.5 + random.random())

            print(f"  ⚠️  重试 {attempt + 1}/{config.max_retries}，等待 {delay:.2f}秒...")
            await asyncio.sleep(delay)
        else:
            return True, result, None

    return False, None, last_error


# ============================================================================
# 3. 实现死信队列
# ============================================================================


class DeadLetterQueue[T]:
    """死信队列（DLQ）- PEP 695 泛型

    泛型参数 T 表示队列中存储的数据项类型。

    🔒 Free-threading 线程安全说明:
    - items 列表的修改应在单个协程中进行
    - 如需跨线程访问，使用 threading.Lock 保护
    - 批量操作（retry_all）不是线程安全的
    """

    def __init__(self, max_size: int = 1000) -> None:
        self.items: list[ErrorRecord] = []
        self.max_size = max_size

    def add(self, error_record: ErrorRecord) -> None:
        """添加失败项到DLQ"""
        # 如果队列满了，移除最旧的
        if len(self.items) >= self.max_size:
            self.items.pop(0)

        self.items.append(error_record)

    def get_failed_items(self) -> list[ErrorRecord]:
        """获取所有失败项"""
        return self.items.copy()

    def get_by_error_type(self, error_type: str) -> list[ErrorRecord]:
        """按错误类型筛选（使用 match/case）"""
        result = []
        for item in self.items:
            match item.error_type:
                case et if et == error_type:
                    result.append(item)
        return result

    async def retry_all(self, processor: Callable, config: RetryConfig) -> tuple[int, int]:
        """重试所有失败项（使用 asyncio.TaskGroup 并行重试）"""
        success_count = 0
        failed_count = 0

        items_to_retry = self.items.copy()
        self.items.clear()

        # 使用 asyncio.TaskGroup 并行重试
        async def retry_item(error_record: ErrorRecord) -> tuple[bool, ErrorRecord | None]:
            success, _result, error = await retry_with_backoff(processor, error_record.item, config)
            if success:
                return True, None
            # 更新重试次数
            error_record.retry_count += config.max_retries
            error_record.error = error if error else error_record.error
            error_record.timestamp = time.time()
            return False, error_record

        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(retry_item(record)) for record in items_to_retry]

        # 收集结果
        for task in tasks:
            success, failed_record = task.result()
            if success:
                success_count += 1
            else:
                failed_count += 1
                if failed_record:
                    self.items.append(failed_record)

        return success_count, failed_count

    def clear(self) -> None:
        """清空DLQ"""
        self.items.clear()


# ============================================================================
# 4. 实现断点续传
# ============================================================================


class Checkpoint:
    """断点管理"""

    def __init__(self, checkpoint_file: str = "pipeline_checkpoint.json"):
        self.checkpoint_file = checkpoint_file
        self.last_processed_id: str | None = None
        self.processed_count: int = 0
        self.save_interval: int = 10  # 每10个保存一次

    def save(self) -> None:
        """保存断点"""
        state = {
            "last_processed_id": self.last_processed_id,
            "processed_count": self.processed_count,
            "timestamp": time.time(),
        }

        try:
            with open(self.checkpoint_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            print(f"⚠️  保存断点失败: {e}")

    def load(self) -> dict:
        """加载断点"""
        try:
            with open(self.checkpoint_file) as f:
                state = json.load(f)
                self.last_processed_id = state.get("last_processed_id")
                self.processed_count = state.get("processed_count", 0)
                return state
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"⚠️  加载断点失败: {e}")
            return {}

    def mark_processed(self, item_id: str) -> None:
        """标记已处理"""
        self.last_processed_id = item_id
        self.processed_count += 1

        # 定期保存
        if self.processed_count % self.save_interval == 0:
            self.save()

    def should_skip(self, item_id: str) -> bool:
        """检查是否应该跳过（已处理）"""
        if self.last_processed_id is None:
            return False

        # 简化比较：假设ID是递增的
        try:
            return int(item_id) <= int(self.last_processed_id)
        except (ValueError, TypeError):
            return False


# ============================================================================
# 5. 实现容错管道
# ============================================================================


class ResilientPipeline[T, R]:
    """容错管道（PEP 695 泛型）

    泛型参数:
    - T: 输入数据类型
    - R: 输出结果类型

    🔒 Free-threading 线程安全说明:
    - success_count 和 failure_count 应在单个协程中更新
    - checkpoint 保存不是线程安全的
    - 不建议在多线程环境中共享实例
    """

    def __init__(
        self,
        processor: Callable[[T], R],
        retry_config: RetryConfig | None = None,
        enable_dlq: bool = True,
        enable_checkpoint: bool = True,
    ) -> None:
        self.processor = processor
        self.retry_config = retry_config or RetryConfig()
        self.dlq: DeadLetterQueue[T] | None = DeadLetterQueue() if enable_dlq else None
        self.checkpoint = Checkpoint() if enable_checkpoint else None
        self.success_count = 0
        self.failure_count = 0

    async def process_with_retry(self, source: AsyncGenerator[T]) -> AsyncGenerator[tuple[bool, R | None]]:
        """带重试的处理"""
        # 加载断点
        if self.checkpoint:
            self.checkpoint.load()
            print(f"✅ 从断点恢复: 已处理 {self.checkpoint.processed_count} 个")

        async for item in source:
            # 提取item_id（假设item有id属性或是字典）
            item_id = self._get_item_id(item)

            # 跳过已处理的项
            if self.checkpoint and self.checkpoint.should_skip(item_id):
                print(f"⏭️  跳过已处理项: {item_id}")
                continue

            # 处理项
            success, result, _error = await self.process_item(item)

            # 标记已处理
            if self.checkpoint:
                self.checkpoint.mark_processed(item_id)

            yield success, result

        # 最终保存
        if self.checkpoint:
            self.checkpoint.save()

    async def process_item(self, item: Any) -> tuple[bool, Any, Exception | None]:
        """处理单个项"""
        success, result, error = await retry_with_backoff(self.processor, item, self.retry_config)

        if success:
            self.success_count += 1
        else:
            self.failure_count += 1

            # 加入DLQ
            if self.dlq:
                error_record = ErrorRecord(
                    item=item,
                    error=error,
                    timestamp=time.time(),
                    retry_count=self.retry_config.max_retries,
                )
                self.dlq.add(error_record)

        return success, result, error

    def _get_item_id(self, item: Any) -> str:
        """提取item ID"""
        if hasattr(item, "id"):
            return str(item.id)
        if isinstance(item, dict) and "id" in item:
            return str(item["id"])
        return str(hash(str(item)))

    def get_statistics(self) -> dict:
        """获取处理统计"""
        return {
            "success": self.success_count,
            "failed": self.failure_count,
            "dlq_size": len(self.dlq.items) if self.dlq else 0,
            "checkpoint": {
                "last_id": self.checkpoint.last_processed_id if self.checkpoint else None,
                "processed": self.checkpoint.processed_count if self.checkpoint else 0,
            },
        }


# ============================================================================
# 6. 实现优雅关闭
# ============================================================================


class GracefulShutdown:
    """优雅关闭管理"""

    def __init__(self):
        self.shutdown_requested = False
        self.tasks: list[asyncio.Task] = []

    def request_shutdown(self) -> None:
        """请求关闭"""
        self.shutdown_requested = True
        print("\n🛑 收到关闭请求，等待任务完成...")

    async def wait_for_completion(self, timeout: float = 30.0) -> bool:
        """等待任务完成"""
        if not self.tasks:
            return True

        try:
            # 等待所有任务完成
            await asyncio.wait_for(asyncio.gather(*self.tasks, return_exceptions=True), timeout=timeout)
            print("✅ 所有任务已完成")
        except TimeoutError:
            print(f"⚠️  超时 {timeout}秒，强制取消任务")

            # 强制取消
            for task in self.tasks:
                if not task.done():
                    task.cancel()

            return False
        else:
            return True

    def register_task(self, task: asyncio.Task) -> None:
        """注册任务"""
        self.tasks.append(task)


# ============================================================================
# 7. 测试容错管道
# ============================================================================


async def test_resilient_pipeline():
    """测试容错管道"""
    print("=" * 70)
    print("容错管道测试")
    print("=" * 70)

    # 模拟数据源
    async def data_source(count: int) -> AsyncGenerator[dict]:
        for i in range(count):
            yield {"id": i, "value": i * 10}
            await asyncio.sleep(0.1)

    # 模拟不稳定的处理器（30%失败率）
    def unstable_processor(item: dict) -> dict:
        if random.random() < 0.3:
            raise ValueError(f"处理失败: {item}")
        return {"id": item["id"], "result": item["value"] * 2}

    # 测试容错管道
    print("\n测试: 容错管道")
    print("-" * 70)

    pipeline = ResilientPipeline(
        processor=unstable_processor,
        retry_config=RetryConfig(max_retries=2, base_delay=0.5),
        enable_dlq=True,
        enable_checkpoint=True,
    )

    results = []
    async for success, result in pipeline.process_with_retry(data_source(10)):
        if success:
            results.append(result)

    stats = pipeline.get_statistics()
    print("\n统计:")
    print(f"  成功: {stats['success']}")
    print(f"  失败: {stats['failed']}")
    print(f"  DLQ大小: {stats['dlq_size']}")

    # 重试DLQ
    if pipeline.dlq and pipeline.dlq.items:
        print(f"\n重试DLQ中的 {len(pipeline.dlq.items)} 个失败项...")
        success, failed = await pipeline.dlq.retry_all(unstable_processor, pipeline.retry_config)
        print(f"  重试成功: {success}")
        print(f"  重试失败: {failed}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 3 参考答案: 错误处理与恢复")
    print("=" * 70)
    print("\n【Python 3.13 新特性】")
    print("  ✅ PEP 695 泛型: ResilientPipeline[T, R], DeadLetterQueue[T]")
    print("  ✅ asyncio.TaskGroup: 并行重试处理")
    print("  ✅ match/case: 错误类型分类、状态处理")
    print("  ✅ Free-threading: 线程安全注释")
    print("\n实现要点：")
    print("  ✅ 指数退避重试")
    print("  ✅ 死信队列（DLQ）")
    print("  ✅ 断点续传")
    print("  ✅ 容错管道")
    print("  ✅ 优雅关闭")
    print("\n核心优势：")
    print("  - 自动重试失败项")
    print("  - 隔离持续失败项")
    print("  - 支持中断恢复")
    print("  - 安全关闭流程")
    print("\n生产环境建议：")
    print("  - 使用分布式协调服务")
    print("  - 实现Exactly-Once语义")
    print("  - 添加完整可观测性")
    print("  - 实现自动故障转移")
    print()

    asyncio.run(test_resilient_pipeline())
