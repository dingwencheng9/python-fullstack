"""共享的课程结构扫描器

提供统一的课程目录扫描接口，消除重复的目录遍历逻辑。
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Generator


def iter_stages(root: Path | None = None) -> Generator[Path]:
    """迭代所有 stage 目录

    Args:
        root: 项目根目录，默认为当前目录

    Yields:
        Path: stage 目录路径

    Example:
        >>> for stage_dir in iter_stages():
        ...     print(stage_dir.name)
        stage0-python-basics
        stage1-intermediate
        ...
    """
    if root is None:
        root = Path.cwd()

    try:
        stage_dirs = sorted(root.glob("stage*"))
    except (OSError, PermissionError):
        return

    for stage_dir in stage_dirs:
        if stage_dir.is_dir():
            yield stage_dir


def iter_lessons(stage_dir: Path) -> Generator[Path]:
    """迭代 stage 中的所有 lesson 目录

    Args:
        stage_dir: stage 目录路径

    Yields:
        Path: lesson 目录路径

    Example:
        >>> stage = Path("stage1-intermediate")
        >>> for lesson_dir in iter_lessons(stage):
        ...     print(lesson_dir.name)
        L12-modules-packages
        L13-file-operations
        ...
    """
    lessons_dir = stage_dir / "lessons"
    if not lessons_dir.exists() or not lessons_dir.is_dir():
        return

    try:
        lesson_dirs = sorted(lessons_dir.glob("L*"))
    except (OSError, PermissionError):
        return

    for lesson_dir in lesson_dirs:
        if lesson_dir.is_dir():
            yield lesson_dir


def iter_all_lessons(root: Path | None = None) -> Generator[tuple[Path, Path]]:
    """迭代所有 stage 和 lesson

    Args:
        root: 项目根目录，默认为当前目录

    Yields:
        tuple[Path, Path]: (stage_dir, lesson_dir) 元组

    Example:
        >>> for stage_dir, lesson_dir in iter_all_lessons():
        ...     print(f"{stage_dir.name}/{lesson_dir.name}")
        stage0-python-basics/L01-introduction
        stage0-python-basics/L02-variables-types
        ...
    """
    if root is None:
        root = Path.cwd()

    for stage_dir in iter_stages(root):
        for lesson_dir in iter_lessons(stage_dir):
            yield stage_dir, lesson_dir


def scan_lessons(
    root: Path | None = None,
    callback: Callable[[Path, Path], dict | None] | None = None,
) -> list[dict]:
    """扫描所有课程并应用回调函数

    Args:
        root: 项目根目录，默认为当前目录
        callback: 对每个 lesson 应用的回调函数，接收 (stage_dir, lesson_dir)，
                 返回 dict 或 None。返回 None 时该 lesson 会被跳过。

    Returns:
        list[dict]: 回调函数返回的结果列表（跳过 None 值）

    Example:
        >>> def analyze_lesson(stage_dir: Path, lesson_dir: Path) -> dict:
        ...     return {
        ...         "stage": stage_dir.name,
        ...         "lesson": lesson_dir.name,
        ...         "has_tests": (lesson_dir / "tests").exists(),
        ...     }
        >>> results = scan_lessons(callback=analyze_lesson)
        >>> print(f"Found {len(results)} lessons")
    """
    if root is None:
        root = Path.cwd()

    results = []
    for stage_dir, lesson_dir in iter_all_lessons(root):
        if callback:
            try:
                result = callback(stage_dir, lesson_dir)
                if result is not None:
                    results.append(result)
            except Exception:
                # 静默跳过错误的 lesson，继续扫描其他
                continue

    return results


def count_lessons(root: Path | None = None) -> dict[str, int]:
    """统计课程数量

    Args:
        root: 项目根目录，默认为当前目录

    Returns:
        dict: 包含 total_stages, total_lessons 的统计信息

    Example:
        >>> stats = count_lessons()
        >>> print(f"Total: {stats['total_stages']} stages, {stats['total_lessons']} lessons")
    """
    if root is None:
        root = Path.cwd()

    stage_count = 0
    lesson_count = 0

    for stage_dir in iter_stages(root):
        stage_count += 1
        for _ in iter_lessons(stage_dir):
            lesson_count += 1

    return {
        "total_stages": stage_count,
        "total_lessons": lesson_count,
    }
