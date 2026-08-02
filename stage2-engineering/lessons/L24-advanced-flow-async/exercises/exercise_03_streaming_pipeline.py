"""练习 3: 流式日志处理管道与 ExceptionGroup

任务：
实现一个流式日志处理管道，支持多源并发读取和异常聚合

要求：
1. 使用 asyncio.StreamReader 异步读取日志流
2. 使用 except* ExceptionGroup 捕获多异常
3. 使用 ExitStack 管理多个资源
4. 实现背压控制（backpressure）
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator
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
# 辅助函数（已提供）
# ============================================================================


def parse_log_line(line: str) -> LogEntry | None:
    """解析单行日志"""
    import re

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
# TODO: 学生需要实现的部分
# ============================================================================


async def process_log_stream(
    stream: AsyncGenerator[str],
    name: str
) -> list[LogEntry]:
    """
    处理单个日志流

    TODO: 实现以下功能
    1. 异步遍历日志流
    2. 解析每行日志
    3. 收集解析成功的日志条目
    4. 记录解析失败（返回 LogEntry，错误信息在 message 中标记）

    参数:
        stream: 日志流
        name: 流名称（用于错误标记）

    返回:
        处理后的日志列表
    """
    # TODO: 实现
    raise NotImplementedError("请实现 process_log_stream")


async def merge_log_streams(
    *streams: tuple[str, AsyncGenerator[str]]
) -> AsyncGenerator[tuple[str, LogEntry]]:
    """
    合并多个日志流（按时间戳排序）

    TODO: 实现以下功能
    1. 并发读取多个流
    2. 使用优先队列按时间戳排序
    3. yield (流名称, LogEntry) 元组
    4. 实现背压控制（限制缓冲区大小）

    参数:
        streams: (流名称, 日志流) 元组列表

    示例:
        async for name, entry in merge_log_streams(
            ("app", app_stream),
            ("db", db_stream)
        ):
            print(f"[{name}] {entry}")
    """
    # TODO: 实现
    raise NotImplementedError("请实现 merge_log_streams")


async def aggregate_logs(
    streams: list[tuple[str, AsyncGenerator[str]]],
    error_threshold: int = 5
) -> dict[str, int]:
    """
    聚合多个日志流，统计各级别数量

    TODO: 实现以下功能
    1. 并发处理所有流
    2. 使用 except* ExceptionGroup 捕获多异常
    3. 统计各日志级别数量
    4. 如果错误数量超过阈值，抛出聚合异常

    参数:
        streams: (流名称, 日志流) 列表
        error_threshold: 错误阈值

    返回:
        级别统计字典

    异常:
        错误数量超过阈值时抛出异常
    """
    # TODO: 实现
    raise NotImplementedError("请实现 aggregate_logs")


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

    try:
        entries = await process_log_stream(stream, "test")
        print(f"  解析到 {len(entries)} 条日志")
        for entry in entries:
            print(f"  [{entry['level']}] {entry['module']}: {entry['message'][:30]}...")
        print("✓ 测试通过")
    except NotImplementedError:
        print("✗ 请先实现 process_log_stream")


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
    try:
        stats = await aggregate_logs(streams)
        print(f"  统计结果: {stats}")
        print("✓ 测试通过")
    except NotImplementedError:
        print("✗ 请先实现 aggregate_logs")


async def test_exception_group() -> None:
    """测试 ExceptionGroup 异常处理"""
    # 模拟包含解析错误的日志流
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
        # 设置低阈值以触发异常
        stats = await aggregate_logs(streams, error_threshold=1)
        print(f"  统计结果: {stats}")
    except ExceptionGroup as eg:
        print(f"  ✓ 捕获到 ExceptionGroup: {len(eg.exceptions)} 个子异常")
        for i, exc in enumerate(eg.exceptions):
            print(f"    {i+1}. {type(exc).__name__}: {exc}")
    except NotImplementedError:
        print("✗ 请先实现 aggregate_logs")


if __name__ == "__main__":
    print("=" * 60)
    print("L22 练习 3: 流式日志处理管道与 ExceptionGroup")
    print("=" * 60)

    asyncio.run(test_single_stream())
    asyncio.run(test_multi_stream())
    asyncio.run(test_exception_group())
