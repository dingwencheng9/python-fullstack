#!/usr/bin/env python3
"""
L20: 装饰器深度探索 - 课程验证脚本。

验证课程目录结构、Python 版本、源码语法和关键模块可导入性，确保本课可以
作为 Stage 2 工程化课程链路中的独立学习单元运行。
"""

from __future__ import annotations

import importlib.util
import py_compile
import sys
import traceback
from pathlib import Path
from types import ModuleType

COURSE_ID = "L20"
COURSE_NAME = "装饰器深度探索"
LESSON_ROOT = Path(__file__).resolve().parent
MIN_PYTHON_VERSION = (3, 13)

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
    "examples/01_detailed_basics.py",
    "examples/06_practical_decorators.py",
    "examples/async_decorators_modern.py",
    "examples/demo_decorators.py",
    "examples/python313_decorators.py",
    "exercises/__init__.py",
    "exercises/exercise_01_basic_decorators.py",
    "exercises/exercise_02_parameterized_decorators.py",
    "exercises/exercise_03_class_decorators.py",
    "exercises/exercise_04_basic_practice.py",
    "exercises/exercise_05_advanced_decorators.py",
    "exercises/exercise_06_practical_decorators.py",
    "solutions/__init__.py",
    "solutions/solution_01_basic_decorators.py",
    "solutions/solution_02_parameterized_decorators.py",
    "solutions/solution_03_class_decorators.py",
    "solutions/solution_04_advanced_decorators.py",
    "solutions/solution_05_practical_decorators.py",
    "tests/conftest.py",
    "tests/test_async_decorators.py",
    "tests/test_python313_features.py",
    "tests/test_solutions_01_basic_decorators.py",
    "tests/test_solutions_02_parameterized_decorators.py",
    "tests/test_solutions_03_class_decorators.py",
    "tests/test_solutions_04_advanced_decorators.py",
    "tests/test_solutions_05_practical_decorators.py",
]

IMPORT_TARGETS = [
    "examples/01_detailed_basics.py",
    "examples/06_practical_decorators.py",
    "examples/async_decorators_modern.py",
    "examples/demo_decorators.py",
    "examples/python313_decorators.py",
    "exercises/exercise_01_basic_decorators.py",
    "exercises/exercise_02_parameterized_decorators.py",
    "exercises/exercise_03_class_decorators.py",
    "exercises/exercise_04_basic_practice.py",
    "exercises/exercise_05_advanced_decorators.py",
    "exercises/exercise_06_practical_decorators.py",
    "solutions/solution_01_basic_decorators.py",
    "solutions/solution_02_parameterized_decorators.py",
    "solutions/solution_03_class_decorators.py",
    "solutions/solution_04_advanced_decorators.py",
    "solutions/solution_05_practical_decorators.py",
]


def print_header(title: str) -> None:
    """打印分节标题。"""
    print(f"\n{title}")
    print("-" * 60)


def check_python_version() -> bool:
    """检查 Python 版本。"""
    version = sys.version_info
    version_text = f"{version.major}.{version.minor}.{version.micro}"
    if version >= MIN_PYTHON_VERSION:
        print(f"  ✅ Python 版本: {version_text}")
        return True
    print(f"  ❌ Python 版本: {version_text}")
    print(f"     本课建议使用 Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+")
    return False


def check_structure() -> bool:
    """检查目录和文件结构。"""
    ok = True

    for rel_dir in REQUIRED_DIRS:
        path = LESSON_ROOT / rel_dir
        if path.is_dir():
            print(f"  ✅ 目录存在: {rel_dir}/")
        else:
            print(f"  ❌ 目录缺失: {rel_dir}/")
            ok = False

    for rel_file in REQUIRED_FILES:
        path = LESSON_ROOT / rel_file
        if path.is_file():
            print(f"  ✅ 文件存在: {rel_file}")
        else:
            print(f"  ❌ 文件缺失: {rel_file}")
            ok = False

    return ok


def iter_python_files() -> list[Path]:
    """列出本课需要语法检查的 Python 文件。"""
    excluded_parts = {"__pycache__", ".pytest_cache", ".ruff_cache"}
    return sorted(
        path
        for path in LESSON_ROOT.rglob("*.py")
        if not excluded_parts.intersection(path.parts)
    )


def check_compile() -> bool:
    """检查所有 Python 文件可编译。"""
    ok = True
    for path in iter_python_files():
        rel = path.relative_to(LESSON_ROOT)
        try:
            py_compile.compile(str(path), doraise=True)
            print(f"  ✅ 语法通过: {rel}")
        except py_compile.PyCompileError as exc:
            print(f"  ❌ 语法失败: {rel}")
            print(f"     {exc.msg}")
            ok = False
    return ok


def load_module(rel_path: str) -> ModuleType:
    """按物理路径加载模块，避免依赖 sys.path。"""
    file_path = LESSON_ROOT / rel_path
    module_name = "_l20_verify_" + rel_path.replace("/", "_").replace(".", "_")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {rel_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_imports() -> bool:
    """检查关键示例、练习与参考答案可导入。"""
    ok = True
    for rel_path in IMPORT_TARGETS:
        try:
            load_module(rel_path)
            print(f"  ✅ 可导入: {rel_path}")
        except Exception as exc:  # pragma: no cover - verify 输出诊断信息
            print(f"  ❌ 导入失败: {rel_path}")
            print(f"     {type(exc).__name__}: {exc}")
            traceback.print_exc(limit=1)
            ok = False
    return ok


def check_core_behavior() -> bool:
    """轻量验证若干核心装饰器行为。"""
    ok = True

    try:
        basic = load_module("solutions/solution_01_basic_decorators.py")

        @basic.timer
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        assert greet("L20") == "Hello, L20!"
        assert greet.__name__ == "greet"
        print("  ✅ timer 装饰器保留返回值与元数据")
    except Exception as exc:
        print(f"  ❌ timer 行为验证失败: {exc}")
        ok = False

    try:
        parameterized = load_module("solutions/solution_02_parameterized_decorators.py")

        @parameterized.validate_input(lambda value: 0 <= value <= 10, "out of range")
        def identity(value: int) -> int:
            return value

        assert identity(5) == 5
        try:
            identity(11)
        except ValueError:
            pass
        else:
            raise AssertionError("validate_input 未拒绝越界值")
        print("  ✅ 参数化装饰器 validate_input 行为正常")
    except Exception as exc:
        print(f"  ❌ 参数化装饰器行为验证失败: {exc}")
        ok = False

    try:
        practical = load_module("solutions/solution_05_practical_decorators.py")
        monitor = practical.PerformanceMonitor()

        @monitor.timer
        def add(a: int, b: int) -> int:
            return a + b

        assert add(2, 3) == 5
        assert monitor.stats["add"]["calls"] == 1
        print("  ✅ 实用装饰器 PerformanceMonitor 行为正常")
    except Exception as exc:
        print(f"  ❌ 实用装饰器行为验证失败: {exc}")
        ok = False

    return ok


def main() -> int:
    """执行课程验证。"""
    print("=" * 60)
    print(f"{COURSE_ID}: {COURSE_NAME} - 课程验证")
    print("=" * 60)
    print(f"课程目录: {LESSON_ROOT}")

    checks = [
        ("测试 1: Python 环境", check_python_version),
        ("测试 2: 文件结构", check_structure),
        ("测试 3: Python 语法", check_compile),
        ("测试 4: 关键模块导入", check_imports),
        ("测试 5: 核心行为抽检", check_core_behavior),
    ]

    results: list[tuple[str, bool]] = []
    for title, check in checks:
        print_header(title)
        results.append((title, check()))

    print("\n" + "=" * 60)
    print("验证结果汇总")
    print("=" * 60)
    for title, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{title:<24}: {status}")

    if all(passed for _, passed in results):
        print("\n🎉 L20 课程验证通过！")
        print("\n建议继续执行:")
        print("1. uv run pytest stage2-engineering/lessons/L20-decorators/tests -q")
        print(
            "2. uv run python stage2-engineering/lessons/L20-decorators/examples/demo_decorators.py"
        )
        print(
            "3. uv run python stage2-engineering/lessons/L20-decorators/exercises/exercise_01_basic_decorators.py"
        )
        return 0

    print("\n❌ L20 课程验证未通过，请根据上方诊断修复。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
