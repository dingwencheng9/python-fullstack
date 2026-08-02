"""

from __future__ import annotations

练习 2: 数据管道编排与监控

任务：
实现复杂的数据管道编排系统，支持分支、合并、条件路由和监控。

学习目标：
- 实现管道分支和合并
- 添加条件路由逻辑
- 实现管道监控和指标
- 处理管道异常和恢复

预计时间: 60 分钟
难度: ⭐⭐⭐⭐⭐
"""

from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass
from typing import Any, TypeVar

T = TypeVar("T")


# ============================================================================
# TODO 1: 定义管道状态和指标
# ============================================================================

# TODO: 创建管道状态枚举
# class PipelineState(str, Enum):
#     IDLE = "idle"
#     RUNNING = "running"
#     PAUSED = "paused"
#     FAILED = "failed"
#     COMPLETED = "completed"


# TODO: 创建管道指标模型
# @dataclass
# class PipelineMetrics:
#     processed_count: int = 0
#     error_count: int = 0
#     start_time: float | None = None
#     end_time: float | None = None
#     throughput: float = 0.0  # items/second


# ============================================================================
# TODO 2: 实现可监控的管道节点
# ============================================================================


@dataclass
class PipelineNode:
    """管道节点（带监控）"""

    name: str
    processor: Callable
    metrics: Any = None  # TODO: 使用 PipelineMetrics
    state: Any = None  # TODO: 使用 PipelineState

    async def process(self, item: Any) -> Any:
        """处理单个数据项"""
        # TODO:
        # 1. 更新状态为 RUNNING
        # 2. 记录开始时间
        # 3. 执行处理
        # 4. 更新指标
        # 5. 处理异常


# ============================================================================
# TODO 3: 实现管道分支和合并
# ============================================================================


async def split_stream[T](source: AsyncGenerator[T], n_branches: int) -> list[AsyncGenerator[T]]:
    """将数据流分成多个分支"""
    # TODO:
    # 1. 创建 n 个队列
    # 2. 异步读取源数据
    # 3. 将每个数据项放入所有队列
    # 4. 为每个队列创建生成器


async def merge_streams[T](*sources: AsyncGenerator[T]) -> AsyncGenerator[T]:
    """合并多个数据流"""
    # TODO:
    # 1. 为每个源创建任务
    # 2. 使用 asyncio.Queue 收集结果
    # 3. 按到达顺序 yield


# ============================================================================
# TODO 4: 实现条件路由
# ============================================================================


async def route_by_condition[T](
    source: AsyncGenerator[T], condition: Callable[[T], str], routes: dict[str, Callable]
) -> dict[str, AsyncGenerator[Any]]:
    """根据条件路由数据"""
    # TODO:
    # 1. 为每个路由创建队列
    # 2. 读取源数据
    # 3. 根据 condition 决定路由
    # 4. 应用对应的处理器
    # 5. 返回多个生成器


# ============================================================================
# TODO 5: 实现管道编排器
# ============================================================================


class PipelineOrchestrator:
    """管道编排器"""

    def __init__(self):
        # TODO: 初始化
        self.nodes: list[PipelineNode] = []
        self.metrics: dict[str, Any] = {}
        self.state: Any = None  # TODO: PipelineState

    def add_node(self, name: str, processor: Callable) -> None:
        """添加处理节点"""
        # TODO: 创建并添加 PipelineNode

    async def execute_linear(self, source: AsyncGenerator[T]) -> AsyncGenerator[Any]:
        """执行线性管道"""
        # TODO:
        # 1. 依次通过每个节点
        # 2. 更新状态和指标
        # 3. 处理异常

    async def execute_parallel(self, source: AsyncGenerator[T], n_workers: int = 3) -> AsyncGenerator[Any]:
        """并行执行管道"""
        # TODO:
        # 1. 分割数据流
        # 2. 并行处理
        # 3. 合并结果

    def get_metrics(self) -> dict:
        """获取管道指标"""
        # TODO: 返回所有节点的指标


# ============================================================================
# TODO 6: 实现监控和告警
# ============================================================================


class PipelineMonitor:
    """管道监控器"""

    def __init__(self, alert_threshold: int = 10):
        # TODO: 初始化
        self.alert_threshold = alert_threshold
        self.alerts: list[dict] = []

    async def monitor(self, pipeline: PipelineOrchestrator) -> None:
        """监控管道运行"""
        # TODO:
        # 1. 定期检查指标
        # 2. 检测异常（错误率过高）
        # 3. 发送告警

    def check_health(self, metrics: dict) -> bool:
        """检查管道健康状态"""
        # TODO:
        # 1. 检查错误率
        # 2. 检查吞吐量
        # 3. 返回健康状态


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 2: 数据管道编排与监控")
    print("=" * 70)
    print("\n任务：")
    print("  1. 实现管道状态和指标")
    print("  2. 创建可监控的管道节点")
    print("  3. 实现分支和合并")
    print("  4. 实现条件路由")
    print("  5. 构建管道编排器")
    print("  6. 添加监控和告警")
    print("\n核心概念：")
    print("  - Branch: 数据流分支")
    print("  - Merge: 数据流合并")
    print("  - Routing: 条件路由")
    print("  - Monitoring: 管道监控")
    print("  - Metrics: 性能指标")
    print("\n提示：")
    print("  - 使用 asyncio.Queue 实现分支")
    print("  - 使用 asyncio.gather 合并结果")
    print("  - 记录详细的指标便于调试")
    print("  - 实现健康检查和告警")
    print()
