#!/usr/bin/env python3
"""L18 现代化工具链环境验证脚本。"""

from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

LESSON_ROOT = Path(__file__).resolve().parent


def display(path: Path) -> str:
    """返回相对于课程根目录的展示路径。"""
    try:
        return path.relative_to(LESSON_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def check_python_version() -> bool:
    """检查 Python 版本。"""
    print("🐍 检查 Python 版本...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 13:
        print(f"  ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    print(f"  ❌ Python {version.major}.{version.minor}.{version.micro} (需要 3.13+)")
    return False


def check_directory_structure() -> bool:
    """检查扁平化目录结构。"""
    print("\n📁 检查目录结构...")
    required_dirs = ["examples", "exercises", "solutions", "tests"]

    all_exist = True
    for dir_path in required_dirs:
        path = LESSON_ROOT / dir_path
        if path.is_dir():
            py_count = len([p for p in path.glob("*.py") if p.name != "__init__.py"])
            print(f"  ✅ {dir_path}/ ({py_count} 个 Python 文件)")
        else:
            print(f"  ❌ {dir_path}/ (缺失)")
            all_exist = False

    return all_exist


def check_files() -> bool:
    """检查关键文件。"""
    print("\n📄 检查关键文件...")
    required_files = [
        "lesson.md",
        "README.md",
        "pyproject.toml",
        "examples/README.md",
        "verify.py",
    ]

    all_exist = True
    for file_path in required_files:
        path = LESSON_ROOT / file_path
        if path.is_file():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} (缺失)")
            all_exist = False

    return all_exist


def count_files() -> None:
    """统计课程文件数量。"""
    print("\n📊 统计文件...")
    for dirname, label in {
        "examples": "示例",
        "exercises": "练习",
        "solutions": "答案",
        "tests": "测试",
    }.items():
        path = LESSON_ROOT / dirname
        if path.exists():
            py_files = [p for p in path.glob("*.py") if p.name != "__init__.py"]
            print(f"  {label}: {len(py_files)} 个 Python 文件")

    total_py = len([p for p in LESSON_ROOT.rglob("*.py") if "__pycache__" not in p.parts])
    total_md = len(list(LESSON_ROOT.rglob("*.md")))
    print(f"  总计: {total_py} 个 Python 文件, {total_md} 个 Markdown 文件")


def check_dependencies() -> bool:
    """检查关键依赖或 CLI 是否可用。"""
    print("\n📦 检查依赖包/命令...")
    checks = {
        "pytest": importlib.util.find_spec("pytest") is not None,
        "tomli": importlib.util.find_spec("tomli") is not None,
        "tomli_w": importlib.util.find_spec("tomli_w") is not None,
        "ruff CLI": shutil.which("ruff") is not None,
        "mypy CLI": shutil.which("mypy") is not None,
    }

    for name, ok in checks.items():
        print(f"  {'✅' if ok else '❌'} {name}")

    return all(checks.values())


def main() -> int:
    """运行全部验证。"""
    print("=" * 60)
    print("L18 现代化工具链 - 环境验证")
    print(f"课程目录: {display(LESSON_ROOT)}")
    print("=" * 60)

    results = [
        ("Python 版本", check_python_version()),
        ("目录结构", check_directory_structure()),
        ("关键文件", check_files()),
    ]
    count_files()
    results.append(("依赖包/命令", check_dependencies()))

    print("\n" + "=" * 60)
    print("验证结果:")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        print(f"{name}: {'✅ 通过' if passed else '❌ 失败'}")
        all_passed = all_passed and passed

    print("=" * 60)
    if all_passed:
        print("\n🎉 所有检查通过！L18 工具链环境配置正确。")
        print("\n下一步:")
        print("  1. 阅读 lesson.md 学习课程内容")
        print("  2. 运行示例: uv run python examples/example_02_pyproject_config.py")
        print("  3. 完成练习: uv run python exercises/exercise_02_intermediate.py")
        print("  4. 运行测试: uv run pytest tests -q")
        return 0

    print("\n⚠️  部分检查未通过，请先修复环境。")
    print("\n修复建议:")
    print("  - 确认使用 Python 3.13+")
    print("  - 在仓库根目录运行: uv sync")
    print("  - 再运行: uv run python stage2-engineering/lessons/L18-toolchain/verify.py")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
