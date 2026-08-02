#!/usr/bin/env python3
"""L23 课程自检脚本：结构、编译与关键行为验证。"""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

LESSON_ROOT = Path(__file__).resolve().parent

REQUIRED_DIRS = [
    "examples",
    "exercises",
    "solutions",
    "tests",
]

REQUIRED_FILES = [
    "README.md",
    "lesson.md",
    "pyproject.toml",
    "verify.py",
    "examples/01_free_threading_benchmark.py",
    "examples/01_meta_overhead.py",
    "examples/02_memory_limit_opt.py",
    "examples/02_modern_profiling.py",
    "examples/03_high_performance_abstraction.py",
    "examples/ex03_python313_performance.py",
    "exercises/exercise_01_slots_memory.py",
    "exercises/exercise_02_decorator_performance.py",
    "solutions/__init__.py",
    "solutions/solution_01_slots_memory.py",
    "solutions/solution_02_decorator_performance.py",
    "tests/conftest.py",
    "tests/test_l08.py",
    "tests/test_l08_complete.py",
    "tests/test_l28.py",
    "tests/test_l28_complete.py",
    "tests/test_python313_performance.py",
]


def _ok(message: str) -> None:
    print(f"✅ {message}")


def _fail(message: str) -> None:
    raise AssertionError(message)


def check_structure() -> None:
    """检查课程必需目录与文件。"""
    for directory in REQUIRED_DIRS:
        path = LESSON_ROOT / directory
        if not path.is_dir():
            _fail(f"缺少目录: {path.relative_to(LESSON_ROOT)}")

    for file_name in REQUIRED_FILES:
        path = LESSON_ROOT / file_name
        if not path.is_file():
            _fail(f"缺少文件: {file_name}")

    _ok("目录与文件结构完整")


def iter_python_files() -> list[Path]:
    """返回本课需要编译检查的 Python 文件。"""
    files = [LESSON_ROOT / "verify.py"]
    for directory in ("examples", "exercises", "solutions", "tests"):
        files.extend(sorted((LESSON_ROOT / directory).glob("*.py")))
    return files


def check_compile() -> None:
    """编译所有课程 Python 文件。"""
    for path in iter_python_files():
        py_compile.compile(str(path), doraise=True)
    _ok(f"Python 编译检查通过（{len(iter_python_files())} 个文件）")


def load_module(relative_path: str, module_name: str) -> ModuleType:
    """按物理路径加载模块，并在执行前注册到 sys.modules。"""
    path = LESSON_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载模块: {relative_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def check_solution_01() -> None:
    """验证 __slots__ 内存优化答案的核心行为。"""
    module = load_module("solutions/solution_01_slots_memory.py", "_l23_solution_01_slots_memory")

    point = module.PointWithSlots(1, 2, 3)
    assert (point.x, point.y, point.z) == (1, 2, 3)
    assert not hasattr(point, "__dict__")

    dataclass_point = module.PointDataclass(1, 2, 3)
    assert dataclass_point.x == 1 and dataclass_point.y == 2 and dataclass_point.z == 3
    assert not hasattr(dataclass_point, "__dict__")

    container = module.Container[int]()
    container.add(1)
    container.add(2)
    assert len(container) == 2
    assert container.get_all() == [1, 2]

    _ok("solution_01_slots_memory 核心行为通过")


def check_solution_02() -> None:
    """验证缓存装饰器答案的核心行为。"""
    module = load_module("solutions/solution_02_decorator_performance.py", "_l23_solution_02_decorator_performance")

    assert module.fibonacci_slow(10) == 55

    calls: dict[str, int] = {"add": 0, "ttl": 0, "stats": 0}

    @module.simple_cache
    def add(a: int, b: int) -> int:
        calls["add"] += 1
        return a + b

    assert add(1, 2) == 3
    assert add(1, 2) == 3
    assert calls["add"] == 1

    @module.ttl_cache(ttl_seconds=60.0)
    def marker(value: int) -> tuple[int, int]:
        calls["ttl"] += 1
        return value, calls["ttl"]

    assert marker(7) == (7, 1)
    assert marker(7) == (7, 1)
    assert calls["ttl"] == 1

    def double(value: int) -> int:
        calls["stats"] += 1
        return value * 2

    cached_double, stats = module.cache_with_stats(double)
    assert cached_double(5) == 10
    assert cached_double(5) == 10
    assert stats.misses == 1
    assert stats.hits == 1
    assert stats.hit_rate == 0.5
    assert calls["stats"] == 1

    _ok("solution_02_decorator_performance 核心行为通过")


def check_example_python313() -> None:
    """验证 Python 3.13 性能示例的轻量核心对象。"""
    module = load_module("examples/ex03_python313_performance.py", "_l23_example_python313_performance")

    user = module.OptimizedDataClass(1, "alice", 99.5)
    assert (user.id, user.name, user.score) == (1, "alice", 99.5)
    assert not hasattr(user, "__dict__")

    counter = module.ThreadSafeCounter()
    for _ in range(3):
        counter.increment()
    assert counter.get() == 3

    _ok("ex03_python313_performance 轻量行为通过")


def check_text_metadata() -> None:
    """检查明显旧编号残留。"""
    targets = [LESSON_ROOT / "README.md", LESSON_ROOT / "lesson.md"]
    for directory in ("examples", "exercises", "solutions", "tests"):
        targets.extend((LESSON_ROOT / directory).glob("*.py"))

    allowed_filename_refs = {"test_l08.py", "test_l08_complete.py", "test_l28.py", "test_l28_complete.py"}
    old_lesson_tokens = tuple(f"L{num}" for num in ("08", "28", "27"))
    bad_tokens = (*old_lesson_tokens, "[" + "L" + str(28) + ": " + "下一" + "课]", "Stage " + "1")
    offenders: list[str] = []

    for path in targets:
        text = path.read_text()
        for token in bad_tokens:
            if token in text:
                rel = path.relative_to(LESSON_ROOT)
                # 旧文件名保留兼容，但正文不应出现旧编号。
                if path.name in allowed_filename_refs and token in path.name:
                    continue
                offenders.append(f"{rel}: {token}")

    if offenders:
        _fail("发现旧编号/旧定位残留: " + "; ".join(offenders))

    _ok("旧编号与导航元数据检查通过")


def main() -> int:
    print("🔍 L23 极限抽象与性能优化 - 课程自检")
    print(f"课程目录: {LESSON_ROOT}")
    print()

    checks: list[tuple[str, Any]] = [
        ("结构检查", check_structure),
        ("编译检查", check_compile),
        ("答案 1 行为检查", check_solution_01),
        ("答案 2 行为检查", check_solution_02),
        ("示例行为检查", check_example_python313),
        ("文本元数据检查", check_text_metadata),
    ]

    for title, check in checks:
        print()
        print(f"▶ {title}")
        check()

    print()
    print("🎉 L23 自检全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
