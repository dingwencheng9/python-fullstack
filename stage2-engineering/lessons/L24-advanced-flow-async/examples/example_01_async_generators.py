"""示例 1: 异步生成器基础

展示：
- 同步 vs 异步生成器
- Generator 类型注解
- AsyncGenerator 类型注解
- 流式数据消费
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncGenerator, Generator

# ============================================================================
# 同步生成器
# ============================================================================


def sync_range(n: int) -> Generator[int]:
    """同步生成 0 到 n-1"""
    print("同步生成器开始")
    for i in range(n):
        time.sleep(0.1)  # 模拟阻塞 I/O
        yield i
    print("同步生成器结束")


def demo_sync_generator() -> None:
    """演示同步生成器"""
    print("=== 同步生成器示例 ===\n")

    print("消费生成器:")
    for num in sync_range(5):
        print(f"  收到: {num}")

    print()


# ============================================================================
# 异步生成器
# ============================================================================


async def async_range(n: int) -> AsyncGenerator[int]:
    """异步生成 0 到 n-1"""
    print("异步生成器开始")
    for i in range(n):
        await asyncio.sleep(0.1)  # 非阻塞 I/O
        yield i
    print("异步生成器结束")


async def demo_async_generator() -> None:
    """演示异步生成器"""
    print("=== 异步生成器示例 ===\n")

    print("消费异步生成器:")
    async for num in async_range(5):
        print(f"  收到: {num}")

    print()


# ============================================================================
# 带 send 的生成器
# ============================================================================


def echo_generator() -> Generator[str, str, int]:
    """
    YieldType: str (产出字符串)
    SendType: str (接收字符串)
    ReturnType: int (返回整数)
    """
    count = 0
    received = None

    while True:
        try:
            # 首次调用 next() 时，received 为 None
            # 后续通过 send() 接收值
            received = yield f"Echo-{count}: {received or 'START'}"
            count += 1
        except GeneratorExit:
            print(f"生成器关闭，处理了 {count} 条消息")
            return count


def demo_send_generator() -> None:
    """演示 send 生成器"""
    print("=== Send 生成器示例 ===\n")

    gen = echo_generator()

    # 首次必须调用 next() 或 send(None)
    print(f"1. {next(gen)}")

    # 发送数据
    print(f"2. {gen.send('Hello')}")
    print(f"3. {gen.send('World')}")
    print(f"4. {gen.send('Python')}")

    # 关闭生成器
    try:
        gen.close()
    except StopIteration as e:
        print(f"返回值: {e.value}")

    print()


# ============================================================================
# 异步生成器（带 asend）
# ============================================================================


async def async_echo() -> AsyncGenerator[str, str]:
    """异步回显生成器"""
    count = 0
    received = None

    while True:
        received = yield f"AsyncEcho-{count}: {received or 'START'}"
        await asyncio.sleep(0.1)  # 异步处理
        count += 1


async def demo_async_send() -> None:
    """演示异步 send"""
    print("=== 异步 Send 示例 ===\n")

    gen = async_echo()

    # 首次必须调用 asend(None)
    print(f"1. {await gen.asend(None)}")

    # 发送数据
    print(f"2. {await gen.asend('Task1')}")
    print(f"3. {await gen.asend('Task2')}")
    print(f"4. {await gen.asend('Task3')}")

    # 关闭
    await gen.aclose()

    print()


# ============================================================================
# 实战：流式数据处理
# ============================================================================


async def data_source() -> AsyncGenerator[int]:
    """模拟数据源"""
    for i in range(10):
        await asyncio.sleep(0.1)
        yield i


async def transform_stream(source: AsyncGenerator[int]) -> AsyncGenerator[str]:
    """转换数据流"""
    async for value in source:
        # 转换：数字 -> 字符串
        transformed = f"Item-{value:03d}"
        yield transformed


async def demo_stream_pipeline() -> None:
    """演示流式管道"""
    print("=== 流式管道示例 ===\n")

    print("原始数据 -> 转换 -> 消费:")
    async for item in transform_stream(data_source()):
        print(f"  {item}")

    print()


# ============================================================================
# 主程序
# ============================================================================


async def main() -> None:
    """运行所有示例"""
    # 同步生成器
    demo_sync_generator()

    # 异步生成器
    await demo_async_generator()

    # Send 生成器
    demo_send_generator()

    # 异步 Send
    await demo_async_send()

    # 流式管道
    await demo_stream_pipeline()


if __name__ == "__main__":
    asyncio.run(main())
