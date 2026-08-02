"""

from __future__ import annotations

练习 1: 异步数据管道构建 - 参考答案

【Python 3.13 新特性展示】

1. PEP 695 泛型语法：
   - pipe_map[T, R]: 泛型管道映射函数
   - pipe_filter[T]: 泛型过滤函数
   - DataPipeline[T]: 泛型管道类
   - 类型参数直接在函数/类定义中声明

2. asyncio.TaskGroup 并发：
   - 并行数据处理
   - 多工作者并发执行
   - 自动管理任务生命周期

3. match/case 模式匹配：
   - 管道操作类型匹配
   - 数据状态处理
   - 错误类型分类

4. Free-threading 线程安全：
   - 异步队列的线程安全说明
   - 共享状态的并发访问注释

【解题思路】

1. 异步生成器模式：
   - 使用 async def + yield 创建异步生成器
   - 支持惰性计算，按需生成数据
   - 内存友好，适合大数据流

2. 管道操作符设计：
   - Map: 一对一转换
   - Filter: 过滤数据
   - Batch: 批处理聚合
   - Reduce: 归约操作

3. 链式调用：
   - 使用方法链接构建管道
   - 每个操作返回新的 Pipeline 对象
   - 惰性执行，直到调用 collect/reduce

4. 背压控制：
   - 异步迭代自动处理背压
   - 慢消费者会阻塞快生产者
   - 避免内存溢出

5. 生产优化：
   - 添加错误处理和重试
   - 实现并行处理（多个worker）
   - 添加监控和指标
   - 实现断点续传

【关键知识点】

- AsyncGenerator（异步生成器）
- async for（异步迭代）
- yield（惰性生成）
- Pipeline（管道模式）
- Backpressure（背压控制）
"""

import asyncio
import time
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")
R = TypeVar("R")


# ============================================================================
# 1. 定义数据模型
# ============================================================================


@dataclass
class DataEvent:
    """数据事件

    🔒 Free-threading 线程安全说明:
    - dataclass 实例在创建后应视为不可变
    - 如需在多线程环境中共享，建议使用 frozen=True
    """

    id: int
    value: float
    timestamp: float
    source: str


# ============================================================================
# 2. 实现数据源（异步生成器）
# ============================================================================


async def data_source(count: int, delay: float = 0.1) -> AsyncGenerator[DataEvent]:
    """模拟数据源（异步生成器）"""
    for i in range(count):
        event = DataEvent(id=i, value=float(i * 10), timestamp=time.time(), source="sensor_1")
        yield event
        await asyncio.sleep(delay)


# ============================================================================
# 3. 实现管道操作符
# ============================================================================


async def pipe_map[T, R](source: AsyncGenerator[T], transform: Callable[[T], R]) -> AsyncGenerator[R]:
    """映射转换"""
    async for item in source:
        yield transform(item)


async def pipe_filter[T](source: AsyncGenerator[T], predicate: Callable[[T], bool]) -> AsyncGenerator[T]:
    """过滤数据"""
    async for item in source:
        if predicate(item):
            yield item


async def pipe_batch[T](source: AsyncGenerator[T], batch_size: int) -> AsyncGenerator[list[T]]:
    """批处理"""
    batch = []

    async for item in source:
        batch.append(item)

        if len(batch) >= batch_size:
            yield batch
            batch = []

    # 处理剩余数据
    if batch:
        yield batch


# ============================================================================
# 4. 实现数据汇聚
# ============================================================================


async def collect[T](source: AsyncGenerator[T]) -> list[T]:
    """收集所有数据"""
    result = []
    async for item in source:
        result.append(item)
    return result


async def reduce[T](source: AsyncGenerator[T], reducer: Callable[[T, T], T], initial: T) -> T:
    """归约操作"""
    result = initial
    async for item in source:
        result = reducer(result, item)
    return result


# ============================================================================
# 5. 实现完整管道
# ============================================================================


class DataPipeline[T]:
    """数据管道（PEP 695 泛型）

    泛型参数 T 表示管道中传输的数据类型。

    🔒 Free-threading 线程安全说明:
    - source 是异步生成器，本身是协程安全的
    - 不应在多线程中共享同一个 Pipeline 实例
    - 如需并发处理，应为每个任务创建独立的 Pipeline
    """

    def __init__(self, source: AsyncGenerator[T]) -> None:
        self.source = source

    def map[R](self, transform: Callable[[T], R]) -> "DataPipeline[R]":
        """映射转换"""
        return DataPipeline(pipe_map(self.source, transform))

    def filter(self, predicate: Callable[[T], bool]) -> "DataPipeline[T]":
        """过滤数据"""
        return DataPipeline(pipe_filter(self.source, predicate))

    def batch(self, size: int) -> "DataPipeline[list[T]]":
        """批处理"""
        return DataPipeline(pipe_batch(self.source, size))

    async def collect(self) -> list[T]:
        """收集结果"""
        return await collect(self.source)

    async def reduce(self, reducer: Callable[[T, T], T], initial: T) -> T:
        """归约"""
        return await reduce(self.source, reducer, initial)


# ============================================================================
# 6. 测试管道
# ============================================================================


async def process_data_event(event: DataEvent, operation: str) -> float | None:
    """处理数据事件（使用 match/case 选择操作）"""
    match operation:
        case "double":
            return event.value * 2
        case "square":
            return event.value**2
        case "half":
            return event.value / 2
        case "negate":
            return -event.value
        case _:
            # 默认返回原值
            return event.value


async def test_pipeline():
    """测试数据管道"""
    print("=" * 70)
    print("异步数据管道测试")
    print("=" * 70)

    # 测试 1: 基础管道
    print("\n测试 1: Map + Filter")
    print("-" * 70)

    pipeline = DataPipeline(data_source(10, delay=0.05))
    result = await (
        pipeline.map(lambda e: e.value)  # 提取 value
        .filter(lambda v: v >= 50)  # 过滤 >= 50
        .collect()
    )
    print(f"结果: {result}")
    print(f"数量: {len(result)}")

    # 测试 2: 批处理
    print("\n测试 2: Batch Processing")
    print("-" * 70)

    pipeline = DataPipeline(data_source(10, delay=0.05))
    batches = await pipeline.batch(3).collect()  # 每3个一批
    print(f"批次数: {len(batches)}")
    for i, batch in enumerate(batches):
        print(f"  批次 {i + 1}: {len(batch)} 个事件")

    # 测试 3: 复杂管道
    print("\n测试 3: 复杂管道（Map + Filter + Batch）")
    print("-" * 70)

    pipeline = DataPipeline(data_source(15, delay=0.05))
    result = await (
        pipeline.map(lambda e: e.value * 2)  # 值翻倍
        .filter(lambda v: v % 40 == 0)  # 只保留40的倍数
        .batch(2)  # 每2个一批
        .collect()
    )
    print(f"结果批次: {result}")

    # 测试 4: Reduce 操作
    print("\n测试 4: Reduce (求和)")
    print("-" * 70)

    pipeline = DataPipeline(data_source(10, delay=0.05))
    total = await pipeline.map(lambda e: e.value).reduce(lambda a, b: a + b, 0.0)
    print(f"总和: {total}")

    # 测试 5: 数据转换
    print("\n测试 5: 数据转换")
    print("-" * 70)

    pipeline = DataPipeline(data_source(5, delay=0.05))
    result = await pipeline.map(
        lambda e: {
            "id": e.id,
            "value": e.value,
            "doubled": e.value * 2,
        }
    ).collect()
    for item in result:
        print(f"  {item}")

    # 测试 6: match/case 操作选择
    print("\n测试 6: match/case 操作选择")
    print("-" * 70)

    operations = ["double", "square", "half", "unknown"]
    pipeline = DataPipeline(data_source(5, delay=0.05))
    events = await pipeline.collect()

    for op in operations:
        results = [await process_data_event(event, op) for event in events]
        print(f"操作 '{op}': {results[:3]}...")  # 只显示前3个

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)


# ============================================================================
# 高级示例：并行处理
# ============================================================================


async def parallel_process[T, R](source: AsyncGenerator[T], processor: Callable[[T], R], workers: int = 3) -> AsyncGenerator[R]:
    """并行处理（使用 asyncio.TaskGroup）

    🔒 Free-threading 线程安全说明:
    - asyncio.Queue 在协程间是安全的
    - 不应在多线程中使用，除非使用 run_coroutine_threadsafe
    """
    queue: asyncio.Queue[T | None] = asyncio.Queue(maxsize=workers * 2)
    results: asyncio.Queue[R] = asyncio.Queue()

    async def producer() -> None:
        """生产者：从源读取数据"""
        async for item in source:
            await queue.put(item)
        # 发送结束信号
        for _ in range(workers):
            await queue.put(None)

    async def worker() -> None:
        """工作者：处理数据"""
        while True:
            item = await queue.get()
            if item is None:
                break
            result = await processor(item) if asyncio.iscoroutinefunction(processor) else processor(item)
            await results.put(result)

    # 使用 asyncio.TaskGroup 管理所有任务
    async def run_workers() -> None:
        async with asyncio.TaskGroup() as tg:
            # 启动生产者
            tg.create_task(producer())
            # 启动工作者
            for _ in range(workers):
                tg.create_task(worker())

    # 启动工作任务（在后台运行）
    worker_task = asyncio.create_task(run_workers())

    # 生成结果
    processed_count = 0
    async for _item in source:
        # 计算预期的结果数量
        processed_count += 1

    # 等待所有工作完成
    await worker_task

    # 收集所有结果
    while not results.empty():
        yield await results.get()


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 1 参考答案: 异步数据管道构建")
    print("=" * 70)
    print("\n【Python 3.13 新特性】")
    print("  ✅ PEP 695 泛型: DataPipeline[T], pipe_map[T, R]")
    print("  ✅ asyncio.TaskGroup: 并行数据处理")
    print("  ✅ match/case: 操作类型选择")
    print("  ✅ Free-threading: 线程安全注释")
    print("\n实现要点：")
    print("  ✅ 异步生成器（async def + yield）")
    print("  ✅ 管道操作符（map, filter, batch）")
    print("  ✅ 数据汇聚（collect, reduce）")
    print("  ✅ 链式调用")
    print("  ✅ 惰性执行")
    print("\n核心优势：")
    print("  - 内存高效（惰性计算）")
    print("  - 自动背压控制")
    print("  - 代码清晰（函数式风格）")
    print("  - 易于组合")
    print("\n生产环境建议：")
    print("  - 添加错误处理和重试")
    print("  - 实现并行处理")
    print("  - 添加监控指标")
    print("  - 使用专业框架（如 aiokafka）")
    print()

    asyncio.run(test_pipeline())
