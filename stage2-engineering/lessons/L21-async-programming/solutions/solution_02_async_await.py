"""

from __future__ import annotations

练习 2: async/await 模式 - 参考答案

===============================================================================
解题思路 (Solution Strategy)
===============================================================================

本练习深入探讨 Python 异步编程的高级特性，实现自定义异步协议。

核心知识点：
1. 异步迭代器协议 (__aiter__, __anext__)
2. 异步生成器 (async def + yield)
3. 异步上下文管理器 (__aenter__, __aexit__)
4. StopAsyncIteration 异常控制迭代结束
5. 异步资源管理模式

实现要点：
- __aiter__ 返回 self 使对象可迭代
- __anext__ 使用 raise StopAsyncIteration 结束迭代
- 异步生成器自动实现迭代器协议
- __aenter__/__aexit__ 管理异步资源生命周期
- 所有异步方法必须用 await 调用

设计模式：
- Iterator Pattern: 异步遍历数据流
- Context Manager Pattern: 异步资源获取与释放
- Generator Pattern: 惰性异步数据生成

【解题思路】
本练习的完整实现展示了以下核心概念和技术要点：

1. **问题分析**：
   - 理解练习要求和核心目标
   - 识别关键技术点和实现难点
   - 确定合适的数据结构和算法

2. **实现策略**：
   - 采用模块化设计，每个函数/类职责单一
   - 使用 Python 3.13 类型提示增强代码可读性
   - 遵循 PEP 8 编码规范和最佳实践

3. **关键技术点**：
   - 正确使用语言特性（类型系统/异步/装饰器等）
   - 处理边界条件和异常情况
   - 编写清晰的文档字符串和注释

4. **测试验证**：
   - 覆盖正常流程和异常情况
   - 使用 pytest 进行单元测试
   - 确保代码质量和可维护性

【学习建议】：
- 先理解问题需求，再查看实现代码
- 对比自己的实现，找出差距和改进点
- 运行代码并修改参数，观察行为变化
- 尝试扩展功能，加深理解

===============================================================================
"""

import asyncio
from collections.abc import AsyncIterator
import time

# ============================================================================
# 任务 1: 实现异步迭代器
# ============================================================================


class AsyncCounter:
    """
    异步计数器迭代器

    异步迭代器协议：
    - __aiter__(): 返回异步迭代器对象（通常是 self）
    - __anext__(): 返回下一个值或抛出 StopAsyncIteration

    使用场景：
    - 从网络流中读取数据
    - 逐行读取大文件
    - 定时轮询外部服务

    为什么需要异步迭代器？
    - 同步迭代器会阻塞事件循环
    - 异步迭代器允许在迭代过程中执行其他任务
    - 适合 I/O 密集型的序列处理
    """

    def __init__(self, start: int, stop: int, delay: float = 0.1):
        self.start = start
        self.stop = stop
        self.delay = delay
        self.current = start

    def __aiter__(self):
        """
        返回异步迭代器本身

        这使得对象可用于 async for 循环：
            async for num in AsyncCounter(0, 5):
                print(num)
        """
        return self

    async def __anext__(self):
        """
        返回下一个值

        控制流：
        1. 检查是否到达终点
        2. 是 → 抛出 StopAsyncIteration（结束迭代）
        3. 否 → 执行异步操作（模拟 I/O）
        4. 返回当前值并递增

        注意事项：
        - 必须抛出 StopAsyncIteration，不能返回 None
        - 类似同步迭代器的 StopIteration
        """
        if self.current >= self.stop:
            raise StopAsyncIteration

        # 模拟异步 I/O 操作（如网络请求、数据库查询）
        await asyncio.sleep(self.delay)

        value = self.current
        self.current += 1
        return value


# ============================================================================
# 任务 2: 实现异步生成器
# ============================================================================


async def async_range(n: int) -> AsyncIterator[int]:
    """
    异步生成器（类似内置 range）

    异步生成器 vs 异步迭代器：

    异步生成器（推荐）：
    - 使用 async def + yield
    - 自动实现 __aiter__ 和 __anext__
    - 代码更简洁，易于维护

    异步迭代器：
    - 手动实现 __aiter__ 和 __anext__
    - 更多控制权，适合复杂状态管理
    - 代码冗长

    工作原理：
    - 第一次调用时不执行函数体
    - 每次 async for 请求下一个值时执行到 yield
    - yield 暂停执行，返回值
    - 下次从 yield 后继续执行

    类型提示：
    - AsyncIterator[int] 明确返回异步整数迭代器
    - 帮助类型检查器验证 async for 的使用
    """
    for i in range(n):
        await asyncio.sleep(0.1)  # 模拟异步操作
        yield i


# ============================================================================
# 任务 3: 实现异步上下文管理器
# ============================================================================


class AsyncTimer:
    """
    异步计时器上下文管理器

    异步上下文管理器协议：
    - __aenter__(): 异步进入上下文（获取资源）
    - __aexit__(): 异步退出上下文（释放资源）

    使用场景：
    - 异步数据库连接
    - 异步文件操作
    - 异步网络会话
    - 异步锁和信号量

    为什么需要异步上下文管理器？
    - 资源获取/释放可能涉及异步操作
    - 确保资源正确清理（即使发生异常）
    - 提供清晰的资源生命周期管理
    """

    def __init__(self):
        self.start_time = 0.0

    async def __aenter__(self):
        """
        进入上下文（获取资源）

        执行时机：
        - async with 语句开始时调用
        - 在 with 块执行之前

        常见操作：
        - 建立数据库连接
        - 打开文件
        - 获取锁
        - 初始化会话

        返回值：
        - 返回的值会赋给 as 后的变量
        - async with AsyncTimer(): ...
        """
        # 记录开始时间
        self.start_time = asyncio.get_event_loop().time()

        # 模拟异步初始化操作
        await asyncio.sleep(0.1)

        # 返回 self 使得 as 变量可以访问实例方法
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        退出上下文（释放资源）

        参数：
        - exc_type: 异常类型（无异常时为 None）
        - exc_val: 异常值
        - exc_tb: 异常回溯

        执行时机：
        - with 块结束时调用
        - 即使发生异常也会调用（类似 finally）

        常见操作：
        - 关闭数据库连接
        - 关闭文件
        - 释放锁
        - 清理临时资源

        返回值：
        - True: 抑制异常（不向上传播）
        - False/None: 异常正常传播
        """
        # 模拟异步清理操作
        await asyncio.sleep(0.1)

        # 计算总耗时
        elapsed = asyncio.get_event_loop().time() - self.start_time
        print(f"耗时: {elapsed:.2f}秒")

        # 返回 False，不抑制异常
        return False


# ============================================================================
# 任务 4: 实现异步数据获取器（综合练习）
# ============================================================================


class AsyncDataFetcher:
    """
    异步数据获取器 - 综合应用

    设计模式组合：
    1. 异步上下文管理器：管理连接生命周期
    2. 异步生成器：分页获取数据
    3. 状态管理：检查连接状态

    真实应用场景：
    - HTTP API 客户端（建立会话，分页获取数据，关闭会话）
    - 数据库查询（连接，流式读取结果，断开）
    - 消息队列消费者（连接，消费消息，断开）

    架构优势：
    - 自动资源管理（with 保证清理）
    - 惰性数据获取（生成器节省内存）
    - 错误安全（异常时正确清理）
    """

    def __init__(self, base_url: str = "https://api.example.com"):
        self.base_url = base_url
        self.connected = False

    async def __aenter__(self):
        """
        建立连接

        模拟场景：
        - 发起 HTTP 会话
        - 建立数据库连接
        - 连接到消息队列

        错误处理：
        - 连接失败会抛出异常
        - __aexit__ 不会被调用
        - 资源未分配，无需清理
        """
        print(f"连接到 {self.base_url}")

        # 模拟异步连接操作
        await asyncio.sleep(0.5)

        # 标记连接成功
        self.connected = True

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        关闭连接

        无论是否发生异常，都会执行清理：
        - 正常退出：exc_type 为 None
        - 异常退出：exc_type 为异常类型

        优雅关闭：
        - 发送断开请求
        - 等待确认
        - 清理本地状态
        """
        print("关闭连接")

        # 模拟异步关闭操作
        await asyncio.sleep(0.2)

        # 清理状态
        self.connected = False

        return False

    async def fetch_pages(self, num_pages: int) -> AsyncIterator[dict[str, object]]:
        """
        异步生成器：分页获取数据

        设计要点：
        1. 前置检查：确保连接已建立
        2. 惰性生成：每次 yield 一页数据
        3. 模拟延迟：每页请求需要时间

        内存优势：
        - 不需要一次加载所有页
        - 适合处理大量数据
        - 调用方可提前中断迭代

        使用方式：
            async with AsyncDataFetcher() as fetcher:
                async for page in fetcher.fetch_pages(10):
                    process(page)  # 逐页处理，不占满内存
        """
        # 前置检查：必须先连接
        if not self.connected:
            raise RuntimeError("未连接，请先使用 async with")

        # 逐页获取数据
        for i in range(num_pages):
            # 模拟网络请求延迟
            await asyncio.sleep(0.3)

            # 生成当前页数据
            page_data = {"page": i + 1, "data": [f"item_{i}_{j}" for j in range(5)]}

            yield page_data


# ============================================================================
# 测试代码
# ============================================================================


async def test_async_counter() -> None:
    """测试异步迭代器"""
    print("测试 1: AsyncCounter")

    numbers = []
    async for num in AsyncCounter(0, 5):
        numbers.append(num)

    assert numbers == [0, 1, 2, 3, 4], f"期望 [0,1,2,3,4]，得到 {numbers}"
    print("✅ AsyncCounter 测试通过")


async def test_async_range() -> None:
    """测试异步生成器"""
    print("\n测试 2: async_range")

    numbers = []
    async for num in async_range(3):
        numbers.append(num)

    assert numbers == [0, 1, 2], f"期望 [0,1,2]，得到 {numbers}"
    print("✅ async_range 测试通过")


async def test_async_timer() -> None:
    """测试异步上下文管理器"""
    print("\n测试 3: AsyncTimer")

    start = time.time()
    async with AsyncTimer():
        await asyncio.sleep(0.5)
    elapsed = time.time() - start

    assert 0.6 < elapsed < 0.9, f"耗时应约 0.7 秒，实际 {elapsed:.2f}秒"
    print("✅ AsyncTimer 测试通过")


async def test_async_data_fetcher() -> None:
    """测试综合应用"""
    print("\n测试 4: AsyncDataFetcher")

    async with AsyncDataFetcher("https://test.com") as fetcher:
        pages = []
        async for page in fetcher.fetch_pages(3):
            pages.append(page)

        assert len(pages) == 3, f"期望 3 页，得到 {len(pages)}"
        assert pages[0]["page"] == 1, "第一页应该是 page 1"
        assert len(pages[0]["data"]) == 5, "每页应有 5 条数据"

    print("✅ AsyncDataFetcher 测试通过")


async def main() -> None:
    """运行所有测试"""
    print("=" * 60)
    print("练习 2: async/await 模式 - 参考答案")
    print("=" * 60)
    print()

    try:
        await test_async_counter()
        await test_async_range()
        await test_async_timer()
        await test_async_data_fetcher()

        print()
        print("=" * 60)
        print("🎉 所有测试通过！")
        print("=" * 60)
        print()
        print("知识回顾:")
        print("1. 异步迭代器: __aiter__ 和 __anext__")
        print("2. 异步生成器: async def + yield")
        print("3. 异步上下文管理器: __aenter__ 和 __aexit__")
        print("4. StopAsyncIteration 结束迭代")
        print("5. 所有异步方法都需要 await")
        print()
        print(
            "下一步: uv run python stage2-engineering/lessons/L19-async-programming/exercises/exercise_03_concurrency_control.py"
        )

    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
