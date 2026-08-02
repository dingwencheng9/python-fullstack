"""日志配置（使用 Loguru 实现结构化日志）。

from __future__ import annotations

生产环境日志格式：
- JSON 结构化输出
- 包含 trace_id、request_id 等上下文
- 自动捕获异常堆栈
"""

from __future__ import annotations

import sys
from typing import Any

from loguru import logger

# 移除默认的 logger（避免重复输出）
logger.remove()


def configure_logging(
    level: str = "INFO",
    json_logs: bool = False,
) -> None:
    """配置应用日志。

    Args:
        level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        json_logs: 是否使用 JSON 格式（生产环境建议 True）
    """
    if json_logs:
        # 生产环境：JSON 格式（适用于 ELK/Loki 日志聚合）
        logger.add(
            sys.stderr,
            level=level,
            format="{message}",
            serialize=True,  # 输出 JSON
            backtrace=True,
            diagnose=True,
        )
    else:
        # 开发环境：人类可读格式
        logger.add(
            sys.stderr,
            level=level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>",
            colorize=True,
            backtrace=True,
            diagnose=True,
        )


def get_logger(name: str | None = None) -> Any:
    """获取 logger 实例。

    Args:
        name: 模块名称（用于日志过滤）

    Returns:
        配置好的 logger 实例
    """
    if name:
        return logger.bind(module=name)
    return logger


# 默认配置（开发环境）
configure_logging(level="INFO", json_logs=False)
