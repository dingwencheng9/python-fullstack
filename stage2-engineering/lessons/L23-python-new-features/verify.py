#!/usr/bin/env python3
"""
L21: Python 3.13 体验课程 - 验证脚本。

验证课程目录结构、Python 版本、源码语法和关键模块可导入性。Python 3.14
补充内容在 3.13 环境下只做文件与语法检查；完整行为测试由 tests/ 中的 skip
标记按解释器版本自动控制。
"""

from __future__ import annotations

import importlib.util
import os
import py_compile
import sys
import traceback
from pathlib import Path
from types import ModuleType

COURSE_ID = "L21"
COURSE_NAME = "Python 3.13 体验课程"
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
    "examples/example_01_colorful_errors.py",
    "examples/example_02_repl_improvements.py",
    "examples/example_03_pep695_generics.py",
    "examples/example_04_match_case.py",
    "examples/example_05_python314_pep649.py",
    "examples/example_06_python314_tstring.py",
    "exercises/exercise_01_error_handling.py",
    "exercises/exercise_02_interactive_debug.py",
    "exercises/exercise_03_benchmark.py",
    "exercises/exercise_04_pep695_generics.py",
    "exercises/exercise_05_pep649_annotations.py",
    "exercises/exercise_06_tstring_shell_safe.py",
    "solutions/solution_01_error_handling.py",
    "solutions/solution_02_interactive_debug.py",
    "solutions/solution_03_benchmark.py",
    "solutions/solution_04_pep695_generics.py",
    "solutions/solution_05_pep649_annotations.py",
    "solutions/solution_06_tstring_shell_safe.py",
    "tests/conftest.py",
    "tests/test_features.py",
    "tests/test_new_features.py",
    "tests/test_python314_features.py",
]

IMPORT_TARGETS = [
    "examples/example_01_colorful_errors.py",
    "examples/example_02_repl_improvements.py",
    "examples/example_03_pep695_generics.py",
    "examples/example_04_match_case.py",
    "examples/example_05_python314_pep649.py",
    "examples/example_06_python314_tstring.py",
    "exercises/exercise_01_error_handling.py",
    "exercises/exercise_02_interactive_debug.py",
    "exercises/exercise_03_benchmark.py",
    "exercises/exercise_04_pep695_generics.py",
    "exercises/exercise_05_pep649_annotations.py",
    "exercises/exercise_06_tstring_shell_safe.py",
    "solutions/solution_01_error_handling.py",
    "solutions/solution_02_interactive_debug.py",
    "solutions/solution_03_benchmark.py",
    "solutions/solution_04_pep695_generics.py",
    "solutions/solution_05_pep649_annotations.py",
    "solutions/solution_06_tstring_shell_safe.py",
]


def print_header(title: str) -> None:
    """打印分节标题。"""
    print(f"\n{title}")
    print("-" * 70)


def check_python_version() -> bool:
    """检查 Python 版本。"""
    version = sys.version_info
    version_text = f"{version.major}.{version.minor}.{version.micro}"
    if version >= MIN_PYTHON_VERSION:
        print(f"  ✅ Python 版本: {version_text}")
        return True
    print(f"  ❌ Python 版本: {version_text}")
    print(f"     本课基线需要 Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+")
    return False


def check_color_environment() -> bool:
    """报告彩色错误提示相关环境变量；不因 NO_COLOR 而失败。"""
    no_color = os.environ.get("NO_COLOR")
    force_color = os.environ.get("FORCE_COLOR")
    if no_color:
        print("  ⚠️  NO_COLOR 已设置：终端彩色输出会被禁用，但课程代码仍可运行")
    elif force_color:
        print("  ✅ FORCE_COLOR 已设置：终端会尽量强制彩色输出")
    else:
        print("  ✅ 未设置 NO_COLOR，支持彩色的终端可显示彩色 traceback")
    return True


def check_structure() -> bool:
    """检查目录和关键文件结构。"""
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
    return sorted(path for path in LESSON_ROOT.rglob("*.py") if not excluded_parts.intersection(path.parts))


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
    """按物理路径加载模块，避免依赖当前工作目录。"""
    file_path = LESSON_ROOT / rel_path
    module_name = "_l21_verify_" + rel_path.replace("/", "_").replace(".", "_")
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
    """轻量验证若干 Python 3.13 主题的核心行为。"""
    ok = True

    try:
        generics = load_module("solutions/solution_04_pep695_generics.py")
        assert generics.map_list([1, 2, 3], str) == ["1", "2", "3"]
        assert generics.reduce_list([1, 2, 3], lambda acc, value: acc + value, 0) == 6
        queue = generics.Queue[int]()
        queue.enqueue(10)
        queue.enqueue(20)
        assert queue.dequeue() == 10
        assert queue.size() == 1
        print("  ✅ PEP 695 泛型函数与泛型队列行为正常")
    except Exception as exc:
        print(f"  ❌ PEP 695 行为验证失败: {exc}")
        ok = False

    try:
        match_case = load_module("examples/example_04_match_case.py")
        assert match_case.handle_http_status(200) == "成功"
        assert "未知" in match_case.handle_http_status(999)
        assert "类型错误" in match_case.handle_error_with_match(TypeError("boom"))
        print("  ✅ match/case 示例核心行为正常")
    except Exception as exc:
        print(f"  ❌ match/case 行为验证失败: {exc}")
        ok = False

    try:
        benchmark = load_module("solutions/solution_03_benchmark.py")
        assert benchmark.fibonacci_iterative(10) == 55
        print("  ✅ 性能基准参考答案核心函数行为正常")
    except Exception as exc:
        print(f"  ❌ 性能基准行为验证失败: {exc}")
        ok = False

    return ok


def main() -> int:
    """执行课程验证。"""
    print("=" * 70)
    print(f"{COURSE_ID}: {COURSE_NAME} - 课程验证")
    print("=" * 70)
    print(f"课程目录: {LESSON_ROOT}")

    checks = [
        ("测试 1: Python 环境", check_python_version),
        ("测试 2: 彩色输出环境", check_color_environment),
        ("测试 3: 文件结构", check_structure),
        ("测试 4: Python 语法", check_compile),
        ("测试 5: 关键模块导入", check_imports),
        ("测试 6: 核心行为抽检", check_core_behavior),
    ]

    results: list[tuple[str, bool]] = []
    for title, check in checks:
        print_header(title)
        results.append((title, check()))

    print("\n" + "=" * 70)
    print("验证结果汇总")
    print("=" * 70)
    for title, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{title:<24}: {status}")

    if all(passed for _, passed in results):
        print("\n🎉 L21 课程验证通过！")
        print("\n建议继续执行:")
        print("1. uv run pytest stage2-engineering/lessons/L21-python313-experience/tests -q")
        print("2. uv run python stage2-engineering/lessons/L21-python313-experience/examples/example_01_colorful_errors.py")
        print("3. uv run python stage2-engineering/lessons/L21-python313-experience/solutions/solution_04_pep695_generics.py")
        return 0

    print("\n❌ L21 课程验证未通过，请根据上方诊断修复。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
