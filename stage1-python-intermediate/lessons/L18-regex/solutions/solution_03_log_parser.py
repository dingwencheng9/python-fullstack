"""L16 正则表达式练习 3：日志解析实战 参考答案"""

import re
from dataclasses import dataclass
from typing import TypedDict


class LogEntry(TypedDict):
    """日志条目类型"""
    timestamp: str
    level: str
    module: str
    message: str


# 日志格式的正则模式
LOG_PATTERN = re.compile(
    r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"  # 时间戳
    r" \[(INFO|DEBUG|WARNING|ERROR|CRITICAL)\]"  # 级别
    r" \[(\w+)\]"  # 模块名
    r" (.+)"  # 消息
)


def parse_log_line(line: str) -> LogEntry | None:
    """解析单行日志

    Args:
        line: 日志行

    Returns:
        解析后的字典，解析失败返回 None
    """
    match = LOG_PATTERN.match(line.strip())
    if not match:
        return None

    timestamp, level, module, message = match.groups()
    return LogEntry(
        timestamp=timestamp,
        level=level,
        module=module,
        message=message
    )


def filter_by_level(logs: list[LogEntry], level: str) -> list[LogEntry]:
    """按日志级别过滤

    Args:
        logs: 日志列表
        level: 要过滤的级别（如 "ERROR"）

    Returns:
        过滤后的日志列表
    """
    return [log for log in logs if log["level"] == level]


def count_by_level(logs: list[LogEntry]) -> dict[str, int]:
    """统计各级别日志数量

    Args:
        logs: 日志列表

    Returns:
        级别 -> 数量的字典
    """
    counts: dict[str, int] = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def parse_logs(content: str) -> list[LogEntry]:
    """解析多行日志内容

    Args:
        content: 日志文本内容

    Returns:
        解析后的日志列表
    """
    return [
        log for line in content.strip().split("\n")
        if (log := parse_log_line(line)) is not None
    ]


# 测试代码
if __name__ == "__main__":
    sample_logs = """
2024-01-15 10:23:45 [INFO] [AppServer] Server started on port 8080
2024-01-15 10:23:46 [DEBUG] [Database] Connection pool initialized: 10 connections
2024-01-15 10:23:47 [WARNING] [Auth] Invalid login attempt from 192.168.1.100
2024-01-15 10:23:48 [ERROR] [Database] Query timeout after 30s: SELECT * FROM users
2024-01-15 10:23:49 [INFO] [API] Request completed: GET /api/users 200 OK 45ms
2024-01-15 10:23:50 [ERROR] [API] Failed to process request: Connection refused
2024-01-15 10:23:51 [INFO] [AppServer] Graceful shutdown initiated
"""

    # 解析所有日志
    logs = parse_logs(sample_logs)
    print(f"解析到 {len(logs)} 条日志\n")

    # 按级别统计
    counts = count_by_level(logs)
    print("日志级别统计:")
    for level, count in sorted(counts.items()):
        print(f"  {level}: {count}")

    # 过滤错误日志
    errors = filter_by_level(logs, "ERROR")
    print(f"\n错误日志 ({len(errors)} 条):")
    for error in errors:
        print(f"  [{error['timestamp']}] {error['module']}: {error['message']}")
