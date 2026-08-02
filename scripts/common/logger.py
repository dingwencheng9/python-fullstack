"""共享的日志配置

提供统一的日志记录器，支持多级别日志和格式化输出。
"""

from __future__ import annotations

import logging
import sys
from typing import Literal

# 日志级别类型
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def setup_logger(
    name: str = "scripts",
    level: str = "INFO",
    format_str: str = "%(message)s",
) -> logging.Logger:
    """设置标准日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        format_str: 日志格式字符串

    Returns:
        logging.Logger: 配置好的日志记录器

    Example:
        >>> logger = setup_logger("my_script", level="DEBUG")
        >>> logger.info("Processing...")
        Processing...
    """
    logger = logging.getLogger(name)
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # 避免重复添加 handler
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(format_str))
        logger.addHandler(handler)

    # 防止日志传播到根记录器
    logger.propagate = False

    return logger


def setup_verbose_logger(name: str = "scripts") -> logging.Logger:
    """设置详细的日志记录器（包含时间和级别）

    Args:
        name: 日志记录器名称

    Returns:
        logging.Logger: 配置好的日志记录器

    Example:
        >>> logger = setup_verbose_logger()
        >>> logger.info("Processing...")
        2024-01-01 10:00:00 - INFO - Processing...
    """
    return setup_logger(
        name=name,
        level="DEBUG",
        format_str="%(asctime)s - %(levelname)s - %(message)s",
    )


# 默认日志记录器（简洁模式）
logger = setup_logger()


# 便捷的日志函数
def log_debug(message: str, *args: object) -> None:
    """记录调试日志

    Args:
        message: 日志消息（支持 % 格式化）
        *args: 格式化参数
    """
    logger.debug(message, *args)


def log_info(message: str, *args: object) -> None:
    """记录信息日志

    Args:
        message: 日志消息（支持 % 格式化）
        *args: 格式化参数
    """
    logger.info(message, *args)


def log_warning(message: str, *args: object) -> None:
    """记录警告日志

    Args:
        message: 日志消息（支持 % 格式化）
        *args: 格式化参数
    """
    logger.warning(message, *args)


def log_error(message: str, *args: object) -> None:
    """记录错误日志

    Args:
        message: 日志消息（支持 % 格式化）
        *args: 格式化参数
    """
    logger.error(message, *args)


def log_exception(message: str, *args: object) -> None:
    """记录异常日志（包含堆栈信息）

    Args:
        message: 日志消息（支持 % 格式化）
        *args: 格式化参数

    Note:
        应该在 except 块中调用，会自动记录异常堆栈
    """
    logger.exception(message, *args)


# 导出公共接口
__all__ = [
    "LogLevel",
    "log_debug",
    "log_error",
    "log_exception",
    "log_info",
    "log_warning",
    "logger",
    "setup_logger",
    "setup_verbose_logger",
]
