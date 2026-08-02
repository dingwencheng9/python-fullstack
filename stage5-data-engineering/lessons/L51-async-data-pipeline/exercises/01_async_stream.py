"""

from __future__ import annotations

练习 1: 异步数据管道构建

任务：
实现一个异步数据处理管道，支持数据采集、转换、过滤和汇总。

学习目标：
- 理解异步生成器（async generator）
- 实现管道式数据处理
- 掌握异步迭代器模式
- 实现背压控制

预计时间: 60 分钟
难度: ⭐⭐⭐⭐☆
"""

from collections.abc import AsyncGenerator, Callable
from typing import TypeVar

T = TypeVar("T")


# ============================================================================
# TODO 1: 定义数据模型
# ============================================================================

# TODO: 创建数据事件模型
# @dataclass
# class DataEvent:
#     id: int
#     value: float
#     timestamp: float
#     source: str


# ============================================================================
# TODO 2: 实现数据源（异步生成器）
# ============================================================================


async def data_source(count: int, delay: float = 0.1) -> AsyncGenerator[DataEvent]:
    """模拟数据源（异步生成器）"""
    # TODO:
    # 1. 循环生成 count 个数据事件
    # 2. 每次生成后等待 delay 秒
    # 3. 使用 yield 返回数据


# ============================================================================
# TODO 3: 实现管道操作符
# ============================================================================


async def pipe_map[T](source: AsyncGenerator[T], transform: Callable[[T], T]) -> AsyncGenerator[T]:
    """映射转换"""
    # TODO:
    # 1. 异步迭代源数据
    # 2. 应用转换函数
    # 3. yield 转换后的数据


async def pipe_filter[T](source: AsyncGenerator[T], predicate: Callable[[T], bool]) -> AsyncGenerator[T]:
    """过滤数据"""
    # TODO:
    # 1. 异步迭代源数据
    # 2. 检查谓词条件
    # 3. 只 yield 符合条件的数据


async def pipe_batch[T](source: AsyncGenerator[T], batch_size: int) -> AsyncGenerator[list[T]]:
    """批处理"""
    # TODO:
    # 1. 累积数据到批次大小
    # 2. yield 批次数据
    # 3. 处理剩余数据


# ============================================================================
# TODO 4: 实现数据汇聚
# ============================================================================


async def collect[T](source: AsyncGenerator[T]) -> list[T]:
    """收集所有数据"""
    # TODO:
    # 1. 异步迭代源数据
    # 2. 收集到列表
    # 3. 返回列表


async def reduce[T](source: AsyncGenerator[T], reducer: Callable[[T, T], T], initial: T) -> T:
    """归约操作"""
    # TODO:
    # 1. 从初始值开始
    # 2. 异步迭代源数据
    # 3. 应用归约函数
    # 4. 返回最终结果


# ============================================================================
# TODO 5: 实现完整管道
# ============================================================================


class DataPipeline:
    """数据管道"""

    def __init__(self, source: AsyncGenerator):
        # TODO: 保存数据源
        self.source = source

    def map(self, transform: Callable) -> "DataPipeline":
        """映射转换"""
        # TODO:
        # 1. 应用 pipe_map
        # 2. 返回新的 DataPipeline

    def filter(self, predicate: Callable) -> "DataPipeline":
        """过滤数据"""
        # TODO:
        # 1. 应用 pipe_filter
        # 2. 返回新的 DataPipeline

    def batch(self, size: int) -> "DataPipeline":
        """批处理"""
        # TODO:
        # 1. 应用 pipe_batch
        # 2. 返回新的 DataPipeline

    async def collect(self) -> list:
        """收集结果"""
        # TODO: 调用 collect 函数

    async def reduce(self, reducer: Callable, initial) -> any:
        """归约"""
        # TODO: 调用 reduce 函数


# ============================================================================
# TODO 6: 测试管道
# ============================================================================


async def test_pipeline():
    """测试数据管道"""
    # TODO:
    # 1. 创建数据源
    # 2. 构建管道（map, filter, batch）
    # 3. 收集结果
    # 4. 打印结果


# ============================================================================
# 运行说明
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("练习 1: 异步数据管道构建")
    print("=" * 70)
    print("\n任务：")
    print("  1. 实现异步数据源（生成器）")
    print("  2. 实现管道操作符（map, filter, batch）")
    print("  3. 实现数据汇聚（collect, reduce）")
    print("  4. 构建完整管道类")
    print("  5. 测试管道功能")
    print("\n核心概念：")
    print("  - AsyncGenerator: 异步生成器")
    print("  - async for: 异步迭代")
    print("  - yield: 惰性生成数据")
    print("  - Pipeline: 链式操作")
    print("\n提示：")
    print("  - 使用 async def 定义异步函数")
    print("  - 使用 await 等待异步操作")
    print("  - 使用 async for 迭代异步生成器")
    print("  - 管道操作应该是惰性的（不立即执行）")
    print()

    # asyncio.run(test_pipeline())
