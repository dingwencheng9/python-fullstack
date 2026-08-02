"""
测试 Python 3.13 工具链配置

验证 tests/03_python313_toolchain_config.py 的功能（展平后）
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# 动态导入模块（展平后直接放在 tests/ 目录）
module_path = Path(__file__).parent / "03_python313_toolchain_config.py"


def test_module_importable() -> None:
    """测试模块可以导入"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 验证模块包含关键函数
    assert hasattr(module, "show_ruff_py313_config")
    assert hasattr(module, "show_mypy_py313_config")
    assert hasattr(module, "show_pytest_py313_config")
    assert hasattr(module, "show_complete_pyproject_toml")
    assert hasattr(module, "show_free_threading_test_practices")
    assert hasattr(module, "show_toolchain_versions")


def test_ruff_config_output(capsys: pytest.CaptureFixture[str]) -> None:
    """测试 Ruff 配置输出"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.show_ruff_py313_config()
    captured = capsys.readouterr()

    # 验证输出包含关键内容
    assert "Ruff" in captured.out
    assert "target-version" in captured.out
    assert "py313" in captured.out
    assert "pyupgrade" in captured.out


def test_mypy_config_output(capsys: pytest.CaptureFixture[str]) -> None:
    """测试 mypy 配置输出"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.show_mypy_py313_config()
    captured = capsys.readouterr()

    # 验证输出包含关键内容
    assert "mypy" in captured.out
    assert "python_version" in captured.out
    assert "3.13" in captured.out
    assert "strict" in captured.out


def test_pytest_config_output(capsys: pytest.CaptureFixture[str]) -> None:
    """测试 pytest 配置输出"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.show_pytest_py313_config()
    captured = capsys.readouterr()

    # 验证输出包含关键内容
    assert "pytest" in captured.out
    assert "Free-threading" in captured.out
    assert "parallel" in captured.out


def test_complete_pyproject_output(capsys: pytest.CaptureFixture[str]) -> None:
    """测试完整 pyproject.toml 输出"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.show_complete_pyproject_toml()
    captured = capsys.readouterr()

    # 验证输出包含关键配置
    assert "pyproject.toml" in captured.out
    assert "requires-python" in captured.out
    assert ">=3.13" in captured.out
    assert "[tool.ruff]" in captured.out
    assert "[tool.mypy]" in captured.out
    assert "[tool.pytest.ini_options]" in captured.out


def test_free_threading_practices_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """测试 Free-threading 实践输出"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.show_free_threading_test_practices()
    captured = capsys.readouterr()

    # 验证输出包含关键内容
    assert "Free-threading" in captured.out
    assert "测试隔离" in captured.out
    assert "并发测试" in captured.out
    assert "线程安全" in captured.out
    assert "ThreadSafeCounter" in captured.out


def test_toolchain_versions_output(capsys: pytest.CaptureFixture[str]) -> None:
    """测试工具链版本输出"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    module.show_toolchain_versions()
    captured = capsys.readouterr()

    # 验证输出包含关键工具
    assert "Python" in captured.out
    assert "ruff" in captured.out.lower()  # 大小写不敏感
    assert "mypy" in captured.out.lower()
    assert "pytest" in captured.out.lower()
    assert "3.13.0+" in captured.out


def test_python_version_check() -> None:
    """测试 Python 版本检查"""
    # 验证运行环境
    assert sys.version_info.major == 3
    # 课程要求 Python 3.13，但测试可以在 3.12+ 运行
    assert sys.version_info.minor >= 12


def test_config_completeness() -> None:
    """测试配置完整性"""
    import importlib.util

    spec = importlib.util.spec_from_file_location("toolchain_config", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 验证所有必需函数存在
    required_functions = [
        "show_ruff_py313_config",
        "show_mypy_py313_config",
        "show_pytest_py313_config",
        "show_complete_pyproject_toml",
        "show_free_threading_test_practices",
        "show_toolchain_versions",
        "main",
    ]

    for func_name in required_functions:
        assert hasattr(module, func_name)
        assert callable(getattr(module, func_name))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
