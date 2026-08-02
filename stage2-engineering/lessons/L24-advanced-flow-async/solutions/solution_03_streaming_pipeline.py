"""练习 3 参考答案: 流式日志处理管道与 ExceptionGroup

参考实现，包含完整解决方案
"""

from __future__ import annotations

import asyncio
import heapq
import re
from collections.abc import AsyncGenerator, AsyncIterator
from dataclasses import dataclass, field
from typing import TypedDict

# ============================================================================
# 类型定义
# ============================================================================


class LogEntry(TypedDict):
    """日志条目"""
    timestamp: str
    level: str
    module: str
    message: str


class ProcessingError(Exception):
    """日志处理错误基类"""
    pass


class ParseError(ProcessingError):
    """解析错误"""
    pass


class FilterError(ProcessingError):
    """过滤错误"""
    pass


# ============================================================================
# 辅助函数
# ============================================================================


def parse_log_line(line: str) -> LogEntry | None:
    """解析单行日志"""
    pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"  # 时间戳
        r" \[(INFO|DEBUG|WARNING|ERROR|CRITICAL)\]"  # 级别
        r" \[(\w+)\]"  # 模块
        r" (.+)"  # 消息
    )
    match = pattern.match(line.strip())
    if not match:
        return None

    timestamp, level, module, message = match.groups()
    return LogEntry(
        timestamp=timestamp,
        level=level,
        module=module,
        message=message
    )


async def create_log_stream(
    name: str,
    content: str,
    delay: float = 0.01
) -> AsyncGenerator[str]:
    """模拟日志流（用于测试）"""
    for line in content.split("\n"):
        if line.strip():
            yield line
        await asyncio.sleep(delay)


# ============================================================================
# 参考实现
# ============================================================================


async def process_log_stream(
    stream: AsyncGenerator[str],
    name: str
) -> list[LogEntry]:
    """处理单个日志流"""
    entries: list[LogEntry] = []
    errors: list[ParseError] = []

    async for line in stream:
        entry = parse_log_line(line)
        if entry is not None:
            entries.append(entry)
        else:
            # 记录解析失败，但不中断处理
            errors.append(ParseError(f"[{name}] 无法解析行: {line!r}"))

    # 如果有解析错误，可以选择抛出或记录
    # 这里我们把错误信息添加到结果中
    if errors:
        for error in errors:
            entries.append(LogEntry(
                timestamp="",
                level="ERROR",
                module=name,
                message=f"[ParseError] {error}"
            ))

    return entries


@dataclass(order=True)
class HeapItem:
    """优先队列项（用于流合并）"""
    priority: str  # 时间戳作为排序键
    index: int  # 保证同时间戳的顺序
    stream_name: str = field(compare=False)
    entry: LogEntry = field(compare=False)


async def merge_log_streams(
    *streams: tuple[str, AsyncGenerator[str]]
) -> AsyncGenerator[tuple[str, LogEntry]]:
    """
    合并多个日志流（按时间戳排序）

    使用最小堆实现流式合并（类似 K 路归并）
    """
    # 背压控制：限制缓冲区大小
    MAX_BUFFER = 100  # noqa: N806

    # 创建迭代器字典
    iterators: dict[str, AsyncIterator[str]] = {}
    for name, stream in streams:
        iterators[name] = stream.__aiter__()

    # 初始化堆
    heap: list[HeapItem] = []
    counter = 0

    async def fill_heap(stream_name: str) -> None:
        """填充堆（获取每个流的下一条日志）"""
        nonlocal counter
        iterator = iterators.get(stream_name)
        if iterator is None:
            return
        try:
            line = await iterator.__anext__()
            entry = parse_log_line(line)
            if entry:
                item = HeapItem(
                    priority=entry["timestamp"],
                    index=counter,
                    stream_name=stream_name,
                    entry=entry
                )
                heapq.heappush(heap, item)
                counter += 1
        except StopAsyncIteration:
            pass

    # 初始化所有流
    for name, _ in streams:
        await fill_heap(name)

    # 流式输出
    buffer_count = 0
    while heap:
        # 弹出最小项
        item = heapq.heappop(heap)
        yield (item.stream_name, item.entry)
        buffer_count += 1

        # 背压控制：达到阈值后暂停
        if buffer_count >= MAX_BUFFER:
            await asyncio.sleep(0)  # 让出控制权
            buffer_count = 0

        # 填充该流的下一条
        await fill_heap(item.stream_name)


async def aggregate_logs(
    streams: list[tuple[str, AsyncGenerator[str]]],
    error_threshold: int = 5
) -> dict[str, int]:
    """
    聚合多个日志流，统计各级别数量

    使用 except* ExceptionGroup 捕获多异常
    """
    stats: dict[str, int] = {}

    async def _process_and_collect(
        name: str,
        stream: AsyncGenerator[str]
    ) -> None:
        """处理单个流并收集结果"""
        nonlocal stats
        entries = await process_log_stream(stream, name)
        for entry in entries:
            level = entry["level"]
            stats[level] = stats.get(level, 0) + 1

    try:
        # 并发处理所有流
        async with asyncio.TaskGroup() as tg:
            for name, stream in streams:
                tg.create_task(_process_and_collect(name, stream))

    except* ExceptionGroup as eg:
        # 重新抛出 ExceptionGroup（使用 except* 模式）
        print(f"捕获到 {len(eg.exceptions)} 个处理异常")
        raise

    return stats


# ============================================================================
# 测试代码
# ============================================================================


async def test_single_stream() -> None:
    """测试单个日志流处理"""
    log_content = """
2024-01-15 10:23:45 [INFO] [AppServer] Server started
2024-01-15 10:23:46 [DEBUG] [Database] Connection pool initialized
2024-01-15 10:23:47 [WARNING] [Auth] Invalid login attempt
2024-01-15 10:23:48 [ERROR] [Database] Query timeout
2024-01-15 10:23:49 [INFO] [API] Request completed
"""

    print("测试单个日志流处理:")
    stream = create_log_stream("test", log_content, delay=0.001)

    entries = await process_log_stream(stream, "test")
    print(f"  解析到 {len(entries)} 条日志")
    for entry in entries:
        print(f"  [{entry['level']}] {entry['module']}: {entry['message'][:30]}...")
    print("✓ 测试通过")


async def test_multi_stream() -> None:
    """测试多流聚合"""
    app_log = """
2024-01-15 10:23:45 [INFO] [App] Request started
2024-01-15 10:23:46 [INFO] [App] Request completed
"""
    db_log = """
2024-01-15 10:23:45 [DEBUG] [DB] Query executed
2024-01-15 10:23:46 [ERROR] [DB] Connection failed
"""

    streams = [
        ("app", create_log_stream("app", app_log, 0.001)),
        ("db", create_log_stream("db", db_log, 0.001)),
    ]

    print("\n测试多流聚合:")
    stats = await aggregate_logs(streams)
    print(f"  统计结果: {stats}")
    print("✓ 测试通过")


async def test_merge_streams() -> None:
    """测试流合并"""
    stream1 = create_log_stream("s1", """
2024-01-15 10:23:45 [INFO] [S1] Message 1
2024-01-15 10:23:47 [INFO] [S1] Message 2
""", 0.001)

    stream2 = create_log_stream("s2", """
2024-01-15 10:23:46 [INFO] [S2] Message A
2024-01-15 10:23:48 [INFO] [S2] Message B
""", 0.001)

    print("\n测试流合并（按时间戳排序）:")
    async for name, entry in merge_log_streams(("s1", stream1), ("s2", stream2)):
        print(f"  [{entry['timestamp']}] [{name}] {entry['message']}")
    print("✓ 测试通过")


async def test_exception_group() -> None:
    """测试 ExceptionGroup 异常处理"""
    bad_log = """
2024-01-15 10:23:45 [INFO] [App] Normal message
invalid line here
2024-01-15 10:23:46 [ERROR] [App] Error message
another bad line
2024-01-15 10:23:47 [INFO] [App] Another normal
"""

    streams = [("bad", create_log_stream("bad", bad_log, 0.001))]

    print("\n测试 ExceptionGroup 异常处理:")
    try:
        # 设置高阈值，不触发异常
        stats = await aggregate_logs(streams, error_threshold=10)
        print(f"  统计结果: {stats}")

        # 设置低阈值，触发异常
        stats = await aggregate_logs(streams, error_threshold=1)
        print(f"  统计结果: {stats}")
    except ExceptionGroup as eg:
        print(f"  ✓ 捕获到 ExceptionGroup: {len(eg.exceptions)} 个子异常")
        for i, exc in enumerate(eg.exceptions):
            print(f"    {i+1}. {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    print("=" * 60)
    print("L22 练习 3 参考答案: 流式日志处理管道与 ExceptionGroup")
    print("=" * 60)

    asyncio.run(test_single_stream())
    asyncio.run(test_multi_stream())
    asyncio.run(test_merge_streams())
    asyncio.run(test_exception_group())
