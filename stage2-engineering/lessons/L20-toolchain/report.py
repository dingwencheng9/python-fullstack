#!/usr/bin/env python3
"""L18 现代化工具链课程概览报告。"""

from __future__ import annotations

from pathlib import Path

LESSON_ROOT = Path(__file__).resolve().parent


def count_py(dirname: str) -> int:
    path = LESSON_ROOT / dirname
    return len([p for p in path.glob("*.py") if p.name != "__init__.py"])


def generate_report() -> None:
    print("=" * 70)
    print("L18 现代化工具链 - 课程概览报告")
    print("=" * 70)

    print("\n📁 扁平化目录结构:")
    print("-" * 70)
    for dirname, label in {
        "examples": "示例代码",
        "exercises": "练习题",
        "solutions": "参考答案",
        "tests": "测试用例",
    }.items():
        path = LESSON_ROOT / dirname
        status = "✅" if path.is_dir() else "❌"
        count = count_py(dirname) if path.exists() else 0
        print(f"  {status} {dirname:<12} {label:<10} ({count} 文件)")

    print("\n📄 关键文件:")
    print("-" * 70)
    for file_path in ["lesson.md", "README.md", "pyproject.toml", "examples/README.md", "verify.py"]:
        path = LESSON_ROOT / file_path
        if path.exists():
            print(f"  ✅ {file_path:<24} ({path.stat().st_size:,} bytes)")
        else:
            print(f"  ❌ {file_path:<24} (缺失)")

    print("\n📚 课程模块:")
    print("-" * 70)
    for code, title, time in [
        ("Part A", "从脚本到工程", "2h"),
        ("Part B", "Git 工作流实战", "3h"),
        ("Part C", "uv 包管理器", "2.5h"),
        ("Part D", "Ruff 代码质量工具", "3h"),
        ("Part E", "mypy 静态类型检查", "3h"),
        ("Part F", "pytest 深入", "2h"),
        ("Part G", "CI/CD 入门", "1.5h"),
        ("Part H", "Docker 容器化", "1h"),
    ]:
        print(f"  {code}: {title:<20} ({time})")

    total_py = len([p for p in LESSON_ROOT.rglob("*.py") if "__pycache__" not in p.parts])
    total_md = len(list(LESSON_ROOT.rglob("*.md")))
    lesson_lines = len((LESSON_ROOT / "lesson.md").read_text(encoding="utf-8").splitlines())
    print("\n📊 内容统计:")
    print("-" * 70)
    print(f"  总计: {total_py} 个 Python 文件, {total_md} 个 Markdown 文件")
    print(f"  lesson.md: {lesson_lines:,} 行")

    print("\n🚀 建议命令:")
    print("-" * 70)
    print("  uv run python stage2-engineering/lessons/L18-toolchain/verify.py")
    print("  uv run python stage2-engineering/lessons/L18-toolchain/examples/example_02_pyproject_config.py")
    print("  uv run python stage2-engineering/lessons/L18-toolchain/exercises/exercise_02_intermediate.py")
    print("  uv run pytest stage2-engineering/lessons/L18-toolchain/tests -q")

    print("\n" + "=" * 70)
    print("✅ L18 现代化工具链课程概览生成完成")
    print("=" * 70)


if __name__ == "__main__":
    generate_report()
