"""

from __future__ import annotations

L18 示例 2: pyproject.toml 配置示例

展示现代 Python 项目的配置最佳实践。
"""

import tomllib
from pathlib import Path

# 完整的 pyproject.toml 配置示例
SAMPLE_PYPROJECT = """
[project]
name = "my-fullstack-app"
version = "0.1.0"
description = "现代化 Python 全栈应用"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
readme = "README.md"
requires-python = ">=3.13"  # 关键：Python 3.13+ 现代化环境

dependencies = [
    "fastapi>=0.136.0",
    "uvicorn[standard]>=0.30.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.10.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.8.0",
    "mypy>=1.13.0",
]

tools = [
    "pre-commit>=4.0.0",
    "mkdocs>=1.6.0",
]

[project.scripts]
dev = "uvicorn main:app --reload"
test = "pytest tests/"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Ruff 配置
[tool.ruff]
target-version = "py313"  # Python 3.13 标准检查
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = ["S101"]  # 测试中允许 assert

# mypy 配置
[tool.mypy]
python_version = "3.13"  # Python 3.13 类型检查
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# pytest 配置
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]

# 覆盖率配置
[tool.coverage.run]
source = ["src"]
omit = ["tests/*", "**/__pycache__/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
"""


def parse_and_explain(content: str) -> None:
    """解析并解释配置"""

    print("🔍 pyproject.toml 配置解析")
    print("=" * 80)

    # 解析 TOML
    config = tomllib.loads(content)

    # 1. 项目基本信息
    print("\n📦 项目信息")
    print("-" * 80)
    project = config["project"]
    print(f"  名称: {project['name']}")
    print(f"  版本: {project['version']}")
    print(f"  描述: {project['description']}")
    print(f"  Python 要求: {project['requires-python']}")
    print("\n  💡 关键点: requires-python = '>=3.13'")
    print("     - Python 3.13 现代化环境")
    print("     - 使用 3.13 最新特性")
    print("     - 工具按 3.13 标准检查")

    # 2. 核心依赖
    print("\n📚 核心依赖")
    print("-" * 80)
    for dep in project["dependencies"]:
        print(f"  • {dep}")

    # 3. 开发依赖
    print("\n🛠️  开发依赖")
    print("-" * 80)
    for dep in project["optional-dependencies"]["dev"]:
        print(f"  • {dep}")

    # 4. Ruff 配置
    print("\n🧹 Ruff 配置（代码质量）")
    print("-" * 80)
    ruff = config["tool"]["ruff"]
    print(f"  目标版本: {ruff['target-version']}")
    print(f"  行长度: {ruff['line-length']}")
    print(f"  启用规则: {', '.join(ruff['select'])}")
    print(f"  忽略规则: {', '.join(ruff['ignore'])}")

    # 5. mypy 配置
    print("\n🔍 mypy 配置（类型检查）")
    print("-" * 80)
    mypy = config["tool"]["mypy"]
    print(f"  Python 版本: {mypy['python_version']}")
    print(f"  Strict 模式: {mypy['strict']}")
    print(f"  警告未使用配置: {mypy['warn_unused_configs']}")

    # 6. pytest 配置
    print("\n🧪 pytest 配置（测试）")
    print("-" * 80)
    pytest_cfg = config["tool"]["pytest"]["ini_options"]
    print(f"  测试目录: {pytest_cfg['testpaths']}")
    print(f"  测试文件: {pytest_cfg['python_files']}")
    print(f"  附加选项: {', '.join(pytest_cfg['addopts'])}")

    print("\n" + "=" * 80)


def demonstrate_version_constraint() -> None:
    """演示版本约束的作用"""

    print("\n\n🎯 Python 3.13 现代化环境演示")
    print("=" * 80)

    print("\n场景：你使用 Python 3.13 环境")
    print("─" * 80)

    print("\n✅ 允许的操作：")
    print("  • 运行 Python 3.13 解释器")
    print("  • 使用 3.11+ 的语法（如 tomllib）")
    print("  • 使用 3.12+ 的语法（如 type 语句）")
    print("  • 使用 3.13 的新特性（Free-threading）")

    print("\n🚫 工具的约束：")
    print("  • mypy --python-version 3.13")
    print("    → 按 3.13 检查类型")
    print("  • ruff --target-version py313")
    print("    → 按 3.13 检查语法")
    print("  • requires-python = '>=3.13'")
    print("    → 依赖必须兼容 3.13")

    print("\n💡 结果：")
    print("  代码在 3.13 运行，充分利用最新特性")
    print("  这是现代化 Python 开发的关键！")


def show_best_practices() -> None:
    """展示最佳实践"""

    print("\n\n📋 配置最佳实践")
    print("=" * 80)

    practices = [
        ("1. 明确 Python 版本约束", "requires-python = '>=3.13'"),
        ("2. 使用 optional-dependencies", "分离核心依赖和开发依赖"),
        ("3. 配置工具版本", "ruff target-version, mypy python_version"),
        ("4. 启用 strict 模式", "mypy strict = true 捕获更多错误"),
        ("5. 配置测试覆盖率", "pytest --cov 确保代码质量"),
        ("6. 使用 project.scripts", "定义常用命令简化工作流"),
    ]

    for title, desc in practices:
        print(f"\n✅ {title}")
        print(f"   {desc}")


def main() -> None:
    """主函数"""

    # 1. 解析配置
    parse_and_explain(SAMPLE_PYPROJECT)

    # 2. 演示版本约束
    demonstrate_version_constraint()

    # 3. 展示最佳实践
    show_best_practices()

    # 4. 保存示例文件
    output_path = Path("sample_pyproject.toml")
    output_path.write_text(SAMPLE_PYPROJECT)
    print(f"\n\n💾 示例配置已保存到: {output_path}")
    print("\n✨ 你可以将此配置作为新项目的起点！")


if __name__ == "__main__":
    main()
