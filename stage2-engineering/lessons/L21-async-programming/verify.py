#!/usr/bin/env python3
"""L19: 异步编程核心 - 课程验证脚本."""

from __future__ import annotations

import importlib.util
import py_compile
import sys
from pathlib import Path

COURSE_ID = "L19"
COURSE_NAME = "异步编程核心"
MIN_PYTHON_VERSION = (3, 13)
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
    "examples/demo_async.py",
    "examples/05_async_http_client.py",
    "examples/06_producer_consumer.py",
    "examples/07_async_http_real.py",
    "examples/08_modern_taskgroup.py",
    "examples/ex09_pep695_async_generics.py",
    "exercises/exercise_01_asyncio_basics.py",
    "exercises/exercise_02_async_await.py",
    "exercises/exercise_03_concurrency_control.py",
    "exercises/exercise_04_async_context.py",
    "exercises/exercise_05_async_patterns.py",
    "solutions/README.md",
    "solutions/__init__.py",
    "solutions/solution_01_asyncio_basics.py",
    "solutions/solution_02_async_await.py",
    "solutions/solution_03_concurrency_control.py",
    "solutions/solution_04_async_context.py",
    "solutions/solution_05_async_patterns.py",
    "tests/conftest.py",
    "tests/test_pep695_async_generics.py",
    "tests/test_solutions_04_05.py",
]

IMPORT_CHECKS = [
    "solutions/solution_01_asyncio_basics.py",
    "solutions/solution_02_async_await.py",
    "solutions/solution_03_concurrency_control.py",
    "solutions/solution_04_async_context.py",
    "solutions/solution_05_async_patterns.py",
    "examples/ex09_pep695_async_generics.py",
]


def rel_path(path: Path) -> str:
    """Return a readable path relative to the lesson root."""
    return str(path.relative_to(LESSON_ROOT))


def check_python_version() -> bool:
    """检查 Python 版本。"""
    print("🐍 检查 Python 版本...")
    current = sys.version_info[:2]
    if current < MIN_PYTHON_VERSION:
        print(
            f"❌ Python 版本过低: {current[0]}.{current[1]} "
            f"(需要 {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+)"
        )
        return False
    print(f"✅ Python {current[0]}.{current[1]} 满足要求")
    return True


def check_directories() -> bool:
    """检查必需目录。"""
    print("\n📁 检查目录结构...")
    ok = True
    for directory in REQUIRED_DIRS:
        path = LESSON_ROOT / directory
        if path.is_dir():
            print(f"✅ {directory}/")
        else:
            print(f"❌ 缺少目录: {directory}/")
            ok = False
    return ok


def check_required_files() -> bool:
    """检查必需文件。"""
    print("\n📄 检查课程文件...")
    ok = True
    for file_name in REQUIRED_FILES:
        path = LESSON_ROOT / file_name
        if path.is_file():
            print(f"✅ {file_name}")
        else:
            print(f"❌ 缺少文件: {file_name}")
            ok = False
    return ok


def check_python_files_compile() -> bool:
    """编译检查全部 Python 文件。"""
    print("\n🔎 编译检查 Python 文件...")
    ok = True
    for path in sorted(LESSON_ROOT.rglob("*.py")):
        if any(
            part in {"__pycache__", ".pytest_cache", ".ruff_cache"}
            for part in path.parts
        ):
            continue
        try:
            py_compile.compile(str(path), doraise=True)
            print(f"✅ {rel_path(path)}")
        except py_compile.PyCompileError as exc:
            print(f"❌ {rel_path(path)}: {exc.msg}")
            ok = False
    return ok


def import_module_from_path(module_name: str, path: Path) -> object:
    """通过文件路径导入模块，避免依赖当前工作目录。"""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法创建导入规格: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_imports() -> bool:
    """检查关键参考答案和示例可导入。"""
    print("\n📦 检查关键模块导入...")
    ok = True
    for index, relative in enumerate(IMPORT_CHECKS, start=1):
        path = LESSON_ROOT / relative
        module_name = f"l19_verify_{index}"
        try:
            import_module_from_path(module_name, path)
            print(f"✅ {relative}")
        except Exception as exc:  # noqa: BLE001 - 验证脚本需要展示导入失败原因
            print(f"❌ {relative}: {exc}")
            ok = False
    return ok


def print_next_steps() -> None:
    """打印建议命令。"""
    print("\n下一步建议：")
    print("1. 运行测试：")
    print("   uv run pytest stage2-engineering/lessons/L19-async-programming/tests -q")
    print("2. 运行练习自检：")
    print(
        "   uv run python stage2-engineering/lessons/L19-async-programming/exercises/exercise_01_asyncio_basics.py"
    )
    print("3. 阅读下一课：")
    print("   stage2-engineering/lessons/L20-decorators/README.md")


def main() -> int:
    """执行课程验证。"""
    print("=" * 60)
    print(f"{COURSE_ID}: {COURSE_NAME} - 课程验证")
    print("=" * 60)

    checks = [
        check_python_version(),
        check_directories(),
        check_required_files(),
        check_python_files_compile(),
        check_imports(),
    ]

    print("\n" + "=" * 60)
    if all(checks):
        print("🎉 验证通过：L19 课程结构与关键代码状态正常")
        print_next_steps()
        return 0

    print("❌ 验证失败：请根据上方输出修复缺失文件或代码问题")
    print_next_steps()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
