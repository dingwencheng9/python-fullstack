"""共享的颜色输出工具

提供统一的终端颜色输出接口，自动检测终端支持。
"""

from __future__ import annotations

from enum import Enum
import sys


class Color(Enum):
    """ANSI 颜色代码枚举"""

    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    MAGENTA = "\033[0;35m"
    WHITE = "\033[1;37m"
    GRAY = "\033[0;90m"
    NC = "\033[0m"  # No Color


def supports_color() -> bool:
    """检测终端是否支持颜色输出

    Returns:
        bool: 如果终端支持颜色则返回 True

    Note:
        - Windows 终端（非 WSL）默认不支持 ANSI 颜色
        - 管道输出（如重定向到文件）会自动禁用颜色
    """
    # 检查是否是交互式终端
    if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
        return False

    # Windows 原生终端不支持 ANSI（除非是 Windows Terminal 或 WSL）
    if sys.platform == "win32":
        # 检查是否在 Windows Terminal 或支持 ANSI 的环境中
        import os

        return os.environ.get("WT_SESSION") is not None or os.environ.get("TERM") is not None

    return True


def colorize(text: str, color: Color) -> str:
    """给文本添加颜色

    Args:
        text: 要着色的文本
        color: 颜色枚举

    Returns:
        str: 着色后的文本（如果终端不支持则返回原文本）

    Example:
        >>> print(colorize("Success!", Color.GREEN))
        Success!  # 绿色显示
    """
    if not supports_color():
        return text
    return f"{color.value}{text}{Color.NC.value}"


def print_success(text: str) -> None:
    """打印成功消息（绿色）

    Args:
        text: 消息内容

    Example:
        >>> print_success("所有测试通过")
        ✅ 所有测试通过  # 绿色
    """
    print(colorize(f"✅ {text}", Color.GREEN))


def print_error(text: str) -> None:
    """打印错误消息（红色）

    Args:
        text: 消息内容

    Example:
        >>> print_error("测试失败")
        ❌ 测试失败  # 红色
    """
    print(colorize(f"❌ {text}", Color.RED))


def print_warning(text: str) -> None:
    """打印警告消息（黄色）

    Args:
        text: 消息内容

    Example:
        >>> print_warning("发现潜在问题")
        ⚠️  发现潜在问题  # 黄色
    """
    print(colorize(f"⚠️  {text}", Color.YELLOW))


def print_info(text: str) -> None:
    """打印信息消息（蓝色）

    Args:
        text: 消息内容

    Example:
        >>> print_info("正在扫描课程...")
        ℹ️  正在扫描课程...  # 蓝色
    """
    print(colorize(f"ℹ️  {text}", Color.BLUE))


def print_section(text: str) -> None:
    """打印章节标题（青色）

    Args:
        text: 标题内容

    Example:
        >>> print_section("开始质量检查")
        ═══════════════════════════════
        开始质量检查
        ═══════════════════════════════
    """
    separator = "═" * len(text)
    print(colorize(f"\n{separator}", Color.CYAN))
    print(colorize(text, Color.CYAN))
    print(colorize(separator, Color.CYAN))


def print_header(text: str) -> None:
    """打印顶级标题（白色加粗）

    Args:
        text: 标题内容

    Example:
        >>> print_header("课程质量报告")

        ╔════════════════════════════════╗
        ║     课程质量报告               ║
        ╚════════════════════════════════╝
    """
    width = len(text) + 4
    top = "╔" + "═" * (width - 2) + "╗"
    middle = f"║  {text}  ║"
    bottom = "╚" + "═" * (width - 2) + "╝"

    print(colorize(f"\n{top}", Color.WHITE))
    print(colorize(middle, Color.WHITE))
    print(colorize(bottom, Color.WHITE))
