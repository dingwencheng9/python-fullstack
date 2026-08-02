"""共享模块 - 提供课程扫描、日志、颜色输出等通用功能"""

from __future__ import annotations

__version__ = "1.0.0"

# 导出公共接口
from common.colors import (
    Color,
    colorize,
    print_error,
    print_info,
    print_success,
    print_warning,
)
from common.course_scanner import (
    iter_all_lessons,
    iter_lessons,
    iter_stages,
    scan_lessons,
)
from common.logger import logger, setup_logger

__all__ = [
    # 颜色输出
    "Color",
    "colorize",
    "iter_all_lessons",
    "iter_lessons",
    # 课程扫描器
    "iter_stages",
    # 日志
    "logger",
    "print_error",
    "print_info",
    "print_success",
    "print_warning",
    "scan_lessons",
    "setup_logger",
]
