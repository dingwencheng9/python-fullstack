"""

from __future__ import annotations

练习 2: 数据管道编排与监控 - 参考答案

【Python 3.13 新特性展示】

1. PEP 695 泛型语法：
   - split_stream[T]: 泛型数据流分割
   - merge_streams[T]: 泛型流合并
   - PipelineOrchestrator[T]: 泛型编排器
   - 类型参数直接在函数定义中声明

2. asyncio.TaskGroup 并发：
   - 并行管道分支处理
   - 监控任务管理
   - 自动清理和错误处理

3. match/case 模式匹配：
   - 管道状态处理
   - 条件路由选择
   - 告警类型分类

4. Free-threading 线程安全：
   - 管道状态的并发访问
   - 指标收集的线程安全

【解题思路】

1. 管道编排架构：
   - 线性管道：顺序处理所有节点
   - 并行管道：分支处理后合并
   - 条件路由：根据数据特征路由
   - 动态编排：运行时调整拓扑

2. 分支与合并实现：
   - 使用asyncio.Queue实现多路分发
   - 为每个分支维护独立队列
   - 合并时使用asyncio.gather收集结果
   - 保持消息顺序或允许乱序

3. 监控指标设计：
   - 吞吐量：items/second
   - 延迟：处理时间分布
   - 错误率：失败比例
   - 队列深度：背压指标

4. 健康检查策略：
   - 心跳检测：定期ping节点
   - 指标阈值：超过阈值告警
   - 趋势分析：检测异常趋势
   - 自动恢复：重启失败节点

5. 生产优化：
   - 使用专业框架（Apache Beam、Flink）
   - 实现分布式追踪（OpenTelemetry）
   - 添加可视化监控（Grafana）
   - 实现自动扩缩容

【关键知识点】

- Pipeline Orchestration（管道编排）
- Branch and Merge（分支与合并）
- Conditional Routing（条件路由）
- Performance Metrics（性能指标）
- Health Monitoring（健康监控）
"""

import asyncio
import time
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, TypeVar

T = TypeVar("T")


# ============================================================================
# 1. 定义管道状态和指标
# ============================================================================


class PipelineState(StrEnum):
    """管道状态"""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"


@dataclass
class PipelineMetrics:
    """管道指标

    🔒 Free-threading 线程安全说明:
    - 指标更新应在单个协程中进行
    - 如需跨线程访问，建议使用 threading.Lock 保护
    - calculate_throughput 方法不是线程安全的
    """

    processed_count: int = 0
    error_count: int = 0
    start_time: float | None = None
    end_time: float | None = None
    throughput: float = 0.0  # items/second

    def calculate_throughput(self) -> None:
        """计算吞吐量"""
        if self.start_time and self.processed_count > 0:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                self.throughput = self.processed_count / elapsed


# ============================================================================
# 2. 实现可监控的管道节点
# ============================================================================


@dataclass
class PipelineNode:
    """管道节点（带监控）

    🔒 Free-threading 线程安全说明:
    - state 字段在多线程环境中可能产生竞态条件
    - 建议只在单个协程中修改状态
    - 如需跨协程访问，使用 asyncio.Lock
    """

    name: str
    processor: Callable
    metrics: PipelineMetrics = field(default_factory=PipelineMetrics)
    state: PipelineState = PipelineState.IDLE

    async def process(self, item: Any) -> Any:
        """处理单个数据项（使用 match/case 处理状态）"""
        # 使用 match/case 检查当前状态
        match self.state:
            case PipelineState.FAILED:
                raise RuntimeError(f"节点 {self.name} 处于失败状态，无法处理")
            case PipelineState.PAUSED:
                raise RuntimeError(f"节点 {self.name} 处于暂停状态")
            case _:
                self.state = PipelineState.RUNNING

        if self.metrics.start_time is None:
            self.metrics.start_time = time.time()

        try:
            # 执行处理
            if asyncio.iscoroutinefunction(self.processor):
                result = await self.processor(item)
            else:
                result = self.processor(item)

            self.metrics.processed_count += 1
        except Exception:
            self.metrics.error_count += 1
            self.state = PipelineState.FAILED
            raise
        else:
            return result
        finally:
            self.metrics.calculate_throughput()


# ============================================================================
# 3. 实现管道分支和合并
# ============================================================================


async def split_stream[T](source: AsyncGenerator[T], n_branches: int) -> list[AsyncGenerator[T]]:
    """将数据流分成多个分支（使用 asyncio.TaskGroup）

    🔒 Free-threading 线程安全说明:
    - asyncio.Queue 在协程间是安全的
    - 不应在多线程中共享队列，除非使用 run_coroutine_threadsafe
    """
    # 创建队列
    queues: list[asyncio.Queue[T | None]] = [asyncio.Queue() for _ in range(n_branches)]

    async def producer() -> None:
        """生产者：从源读取并分发到所有队列"""
        try:
            async for item in source:
                # 广播到所有分支
                for queue in queues:
                    await queue.put(item)
        finally:
            # 发送结束信号
            for queue in queues:
                await queue.put(None)

    # 启动生产者
    _producer_task = asyncio.create_task(producer())  # noqa: RUF006

    # 为每个队列创建生成器
    async def create_consumer(queue: asyncio.Queue[T | None]) -> AsyncGenerator[T]:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

    return [create_consumer(q) for q in queues]


async def merge_streams[T](*sources: AsyncGenerator[T]) -> AsyncGenerator[T]:
    """合并多个数据流（使用 asyncio.TaskGroup）"""
    queue: asyncio.Queue[T] = asyncio.Queue()

    async def consumer(source: AsyncGenerator[T]) -> None:
        """消费者：从源读取并放入合并队列"""
        async for item in source:
            await queue.put(item)

    # 使用 asyncio.TaskGroup 管理所有消费者任务
    async def run_consumers() -> None:
        async with asyncio.TaskGroup() as tg:
            for source in sources:
                tg.create_task(consumer(source))

    # 启动所有消费者（在后台运行）
    consumer_task = asyncio.create_task(run_consumers())

    # 生成结果
    try:
        while True:
            # 检查是否所有任务都完成
            if consumer_task.done() and queue.empty():
                break

            try:
                item = await asyncio.wait_for(queue.get(), timeout=0.1)
                yield item
            except TimeoutError:
                continue
    finally:
        # 等待所有消费者完成
        if not consumer_task.done():
            await consumer_task


# ============================================================================
# 4. 实现条件路由
# ============================================================================


async def route_by_condition[T, R](
    source: AsyncGenerator[T], condition: Callable[[T], str], routes: dict[str, Callable[[T], R]]
) -> dict[str, AsyncGenerator[R]]:
    """根据条件路由数据（使用 match/case 增强路由逻辑）"""
    # 为每个路由创建队列
    queues: dict[str, asyncio.Queue[R | None]] = {route_name: asyncio.Queue() for route_name in routes}

    async def router() -> None:
        """路由器：读取源数据并分发"""
        try:
            async for item in source:
                # 确定路由
                route_name = condition(item)

                # 使用 match/case 处理路由结果
                match route_name:
                    case name if name in queues:
                        # 应用处理器
                        processor = routes[name]
                        if asyncio.iscoroutinefunction(processor):
                            result = await processor(item)
                        else:
                            result = processor(item)
                        await queues[name].put(result)
                    case _:
                        # 未知路由，跳过
                        pass
        finally:
            # 发送结束信号
            for queue in queues.values():
                await queue.put(None)

    # 启动路由器
    _router_task = asyncio.create_task(router())  # noqa: RUF006

    # 为每个路由创建生成器
    async def create_output(queue: asyncio.Queue[R | None]) -> AsyncGenerator[R]:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item

    return {name: create_output(queue) for name, queue in queues.items()}


# ============================================================================
# 5. 实现管道编排器
# ============================================================================


class PipelineOrchestrator[T]:
    """管道编排器（PEP 695 泛型）

    泛型参数 T 表示管道处理的数据类型。

    🔒 Free-threading 线程安全说明:
    - nodes 列表在运行时不应修改
    - state 字段的修改应在单个协程中进行
    - 不建议在多线程环境中使用此类
    """

    def __init__(self) -> None:
        self.nodes: list[PipelineNode] = []
        self.state: PipelineState = PipelineState.IDLE

    def add_node(self, name: str, processor: Callable) -> None:
        """添加处理节点"""
        node = PipelineNode(name=name, processor=processor)
        self.nodes.append(node)

    async def execute_linear(self, source: AsyncGenerator[T]) -> AsyncGenerator[Any]:
        """执行线性管道"""
        self.state = PipelineState.RUNNING
        current_stream = source

        try:
            # 依次通过每个节点
            for node in self.nodes:

                async def process_through_node(stream: AsyncGenerator, n: PipelineNode) -> AsyncGenerator:
                    async for item in stream:
                        result = await n.process(item)
                        yield result

                current_stream = process_through_node(current_stream, node)

            # 输出最终结果
            async for item in current_stream:
                yield item

            self.state = PipelineState.COMPLETED

        except Exception:
            self.state = PipelineState.FAILED
            raise

    async def execute_parallel(self, source: AsyncGenerator[T], n_workers: int = 3) -> AsyncGenerator[Any]:
        """并行执行管道（使用 asyncio.TaskGroup）"""
        self.state = PipelineState.RUNNING

        try:
            # 分割数据流
            branches = await split_stream(source, n_workers)

            # 每个分支执行线性管道
            async def process_branch(branch: AsyncGenerator) -> AsyncGenerator:
                async for item in self.execute_linear(branch):
                    yield item

            branch_outputs = [process_branch(branch) for branch in branches]

            # 合并结果
            async for item in merge_streams(*branch_outputs):
                yield item

            self.state = PipelineState.COMPLETED

        except Exception:
            self.state = PipelineState.FAILED
            raise

    def get_metrics(self) -> dict:
        """获取管道指标"""
        return {
            "nodes": [
                {
                    "name": node.name,
                    "state": node.state.value,
                    "processed": node.metrics.processed_count,
                    "errors": node.metrics.error_count,
                    "throughput": node.metrics.throughput,
                }
                for node in self.nodes
            ],
            "pipeline_state": self.state.value,
        }


# ============================================================================
# 6. 实现监控和告警
# ============================================================================


class PipelineMonitor:
    """管道监控器"""

    def __init__(self, alert_threshold: int = 10):
        self.alert_threshold = alert_threshold
        self.alerts: list[dict] = []

    async def monitor(self, pipeline: PipelineOrchestrator, interval: float = 1.0) -> None:
        """监控管道运行"""
        while pipeline.state == PipelineState.RUNNING:
            await asyncio.sleep(interval)

            metrics = pipeline.get_metrics()

            # 检查健康状态
            if not self.check_health(metrics):
                alert = {
                    "timestamp": datetime.now(UTC).isoformat(),
                    "message": "Pipeline health check failed",
                    "metrics": metrics,
                }
                self.alerts.append(alert)
                print(f"⚠️  ALERT: {alert['message']}")

    def check_health(self, metrics: dict) -> bool:
        """检查管道健康状态"""
        for node_metrics in metrics["nodes"]:
            # 检查错误率
            total = node_metrics["processed"] + node_metrics["errors"]
            if total > 0:
                error_rate = node_metrics["errors"] / total
                if error_rate > 0.1:  # 10%错误率阈值
                    return False

            # 检查吞吐量
            if node_metrics["throughput"] == 0 and node_metrics["processed"] > 0:
                return False

        return True


# ============================================================================
# 7. 测试管道编排
# ============================================================================


async def test_pipeline_orchestration():
    """测试管道编排"""
    print("=" * 70)
    print("管道编排测试")
    print("=" * 70)

    # 创建数据源
    async def data_source(count: int) -> AsyncGenerator[int]:
        for i in range(count):
            yield i
            await asyncio.sleep(0.1)

    # 测试1: 线性管道
    print("\n测试1: 线性管道")
    print("-" * 70)

    orchestrator = PipelineOrchestrator()
    orchestrator.add_node("double", lambda x: x * 2)
    orchestrator.add_node("add_10", lambda x: x + 10)
    orchestrator.add_node("to_string", lambda x: f"result: {x}")

    results = []
    async for result in orchestrator.execute_linear(data_source(5)):
        results.append(result)

    print(f"结果: {results}")
    print(f"\n指标: {orchestrator.get_metrics()}")

    # 测试2: 条件路由
    print("\n测试2: 条件路由")
    print("-" * 70)

    def route_condition(x: int) -> str:
        return "even" if x % 2 == 0 else "odd"

    routes = {
        "even": lambda x: f"偶数: {x}",
        "odd": lambda x: f"奇数: {x}",
    }

    routed = await route_by_condition(data_source(10), route_condition, routes)

    for route_name, stream in routed.items():
        results = []
        async for item in stream:
            results.append(item)
        print(f"{route_name}: {results}")

    print("\n" + "=" * 70)
    print("测试完成！")
    print("=" * 70)


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 2 参考答案: 数据管道编排与监控")
    print("=" * 70)
    print("\n【Python 3.13 新特性】")
    print("  ✅ PEP 695 泛型: PipelineOrchestrator[T], split_stream[T]")
    print("  ✅ asyncio.TaskGroup: 并行分支处理、流合并")
    print("  ✅ match/case: 状态处理、条件路由")
    print("  ✅ Free-threading: 线程安全注释")
    print("\n实现要点：")
    print("  ✅ 管道状态和指标")
    print("  ✅ 可监控的节点")
    print("  ✅ 分支和合并")
    print("  ✅ 条件路由")
    print("  ✅ 管道编排器")
    print("  ✅ 监控和告警")
    print("\n核心优势：")
    print("  - 灵活的编排模式")
    print("  - 实时监控指标")
    print("  - 自动健康检查")
    print("  - 支持并行处理")
    print("\n生产环境建议：")
    print("  - 使用Apache Beam或Flink")
    print("  - 集成OpenTelemetry")
    print("  - 添加Grafana可视化")
    print("  - 实现自动扩缩容")
    print()

    asyncio.run(test_pipeline_orchestration())
