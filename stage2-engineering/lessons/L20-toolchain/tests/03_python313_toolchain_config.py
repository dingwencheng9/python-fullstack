"""
Python 3.13 工具链配置模块

展示 Python 3.13 相关的工具链配置，包括 Ruff、mypy、pytest 等。
"""

from __future__ import annotations


def show_ruff_py313_config() -> str:
    """显示 Python 3.13 的 Ruff 配置"""
    print("Ruff 配置:")
    config = """[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = [
    "E",     # pycodestyle errors
    "W",     # pycodestyle warnings
    "F",     # Pyflakes
    "I",     # isort
    "UP",    # pyupgrade
    "B",     # flake8-bugbear
    "C4",    # flake8-comprehensions
]
"""
    print(config)
    return config


def show_mypy_py313_config() -> str:
    """显示 Python 3.13 的 mypy 配置"""
    config = """[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.mypy.overrides]
module = ["tests.*"]
strict_optional = false
"""
    print(config)
    return config


def show_pytest_py313_config() -> str:
    """显示 Python 3.13 的 pytest 配置"""
    config = """[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
asyncio_mode = "auto"
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
addopts = "-v --tb=short"

# pytest Free-threading 支持
# 使用 python3.13t 或 python3.14t 运行并行测试 (parallel)
"""
    print(config)
    return config


def show_complete_pyproject_toml() -> str:
    """显示完整的 pyproject.toml 配置"""
    config = """[project]
name = "py313-project"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[tool.ruff]
target-version = "py313"
line-length = 100

[tool.mypy]
python_version = "3.13"
strict = true

[tool.pytest.ini_options]
minversion = "8.0"
asyncio_mode = "auto"
"""
    print("pyproject.toml:")
    print(config)
    return config


def show_free_threading_test_practices() -> str:
    """显示 free-threading 测试实践"""
    practices = """Free-threading 测试实践:

1. 使用 python3.13t 或 python3.14t 运行测试
2. 检查线程安全的数据结构
3. 使用 PYTHON_GIL=0 环境变量
4. 测试并发访问共享资源
5. 测试隔离：每个测试用例独立运行
6. 并发测试：使用 ThreadPoolExecutor 模拟并发场景
7. 线程安全：验证 ThreadSafeCounter 等线程安全工具
"""
    print(practices)
    return practices


def show_toolchain_versions() -> str:
    """显示工具链版本信息"""
    versions = """Python: 3.13.0+
Ruff: 0.8+
Mypy: 1.13+
Pytest: 8.0+
"""
    print("工具链版本:")
    print(versions)
    return versions


def main() -> None:
    """主函数：展示所有配置"""
    print("=== Python 3.13 工具链配置 ===\n")
    show_ruff_py313_config()
    print()
    show_mypy_py313_config()
    print()
    show_pytest_py313_config()
    print()
    show_complete_pyproject_toml()
    print()
    show_free_threading_test_practices()
    print()
    show_toolchain_versions()


if __name__ == "__main__":
    main()
