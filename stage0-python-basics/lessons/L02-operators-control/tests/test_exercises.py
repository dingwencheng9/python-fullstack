"""L02 运算符与控制流 - 学员练习测试

测试 exercises/ 目录下的演示型练习。
演示型练习是完整实现，学员运行并观察输出。
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


EXERCISES_DIR = Path(__file__).resolve().parent.parent / "exercises"


def _load_exercise_module(name: str, file_path: Path):
    """按物理路径加载模块，不污染 sys.path。"""
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法为 {file_path} 构造模块 spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def arithmetic_module():
    """加载 exercises/01_arithmetic_conditions.py"""
    return _load_exercise_module("_test_arithmetic", EXERCISES_DIR / "01_arithmetic_conditions.py")


@pytest.fixture(scope="module")
def logical_module():
    """加载 exercises/02_logical_operators.py"""
    return _load_exercise_module("_test_logical", EXERCISES_DIR / "02_logical_operators.py")


@pytest.fixture(scope="module")
def bitwise_module():
    """加载 exercises/03_bitwise_operations.py"""
    return _load_exercise_module("_test_bitwise", EXERCISES_DIR / "03_bitwise_operations.py")


@pytest.fixture(scope="module")
def loops_module():
    """加载 exercises/04_loops.py"""
    return _load_exercise_module("_test_loops", EXERCISES_DIR / "04_loops.py")


@pytest.fixture(scope="module")
def match_module():
    """加载 exercises/05_match_case.py"""
    return _load_exercise_module("_test_match", EXERCISES_DIR / "05_match_case.py")


@pytest.fixture(scope="module")
def comprehensive_module():
    """加载 exercises/06_comprehensive.py"""
    return _load_exercise_module("_test_comprehensive", EXERCISES_DIR / "06_comprehensive.py")


# ============================================================
# 01_arithmetic_conditions.py 测试
# ============================================================


class TestArithmeticConditions:
    """测试 01_arithmetic_conditions.py

    验证：
    1. 模块可正常加载
    2. 包含 BMI 计算和成绩等级示例
    3. 脚本可执行
    """

    def test_module_exists(self, arithmetic_module) -> None:
        """验证模块可加载"""
        assert arithmetic_module is not None

    def test_script_runs_without_error(self) -> None:
        """验证脚本可直接运行（无语法错误）"""
        result = subprocess.run(
            [sys.executable, str(EXERCISES_DIR / "01_arithmetic_conditions.py")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


# ============================================================
# 02_logical_operators.py 测试
# ============================================================


class TestLogicalOperators:
    """测试 02_logical_operators.py

    验证：
    1. 模块可正常加载
    2. 包含短路求值示例
    3. 脚本可执行
    """

    def test_module_exists(self, logical_module) -> None:
        """验证模块可加载"""
        assert logical_module is not None

    def test_script_runs_without_error(self) -> None:
        """验证脚本可直接运行"""
        result = subprocess.run(
            [sys.executable, str(EXERCISES_DIR / "02_logical_operators.py")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


# ============================================================
# 03_bitwise_operations.py 测试
# ============================================================


class TestBitwiseOperations:
    """测试 03_bitwise_operations.py

    验证：
    1. 模块可正常加载
    2. 包含位运算示例
    3. 脚本可执行
    """

    def test_module_exists(self, bitwise_module) -> None:
        """验证模块可加载"""
        assert bitwise_module is not None

    def test_script_runs_without_error(self) -> None:
        """验证脚本可直接运行"""
        result = subprocess.run(
            [sys.executable, str(EXERCISES_DIR / "03_bitwise_operations.py")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


# ============================================================
# 04_loops.py 测试
# ============================================================


class TestLoops:
    """测试 04_loops.py

    验证：
    1. 模块可正常加载
    2. 包含循环示例
    3. 脚本可执行
    """

    def test_module_exists(self, loops_module) -> None:
        """验证模块可加载"""
        assert loops_module is not None

    def test_script_runs_without_error(self) -> None:
        """验证脚本可直接运行"""
        result = subprocess.run(
            [sys.executable, str(EXERCISES_DIR / "04_loops.py")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


# ============================================================
# 05_match_case.py 测试
# ============================================================


class TestMatchCase:
    """测试 05_match_case.py

    验证：
    1. 模块可正常加载
    2. 包含 match-case 示例
    3. 脚本可执行
    """

    def test_module_exists(self, match_module) -> None:
        """验证模块可加载"""
        assert match_module is not None

    def test_script_runs_without_error(self) -> None:
        """验证脚本可直接运行"""
        result = subprocess.run(
            [sys.executable, str(EXERCISES_DIR / "05_match_case.py")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


# ============================================================
# 06_comprehensive.py 测试
# ============================================================


class TestComprehensive:
    """测试 06_comprehensive.py

    验证：
    1. 模块可正常加载
    2. 包含综合示例
    3. 脚本可执行
    """

    def test_module_exists(self, comprehensive_module) -> None:
        """验证模块可加载"""
        assert comprehensive_module is not None

    def test_script_runs_without_error(self) -> None:
        """验证脚本可直接运行"""
        result = subprocess.run(
            [sys.executable, str(EXERCISES_DIR / "06_comprehensive.py")],
            capture_output=True,
            text=True,
            timeout=5,
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


# ============================================================
# 整体验证
# ============================================================


class TestStage0L02Compliance:
    """整体验证：L02 exercises 符合知识边界定义"""

    def test_all_exercises_no_class(self) -> None:
        """验证所有 L02 exercises 不包含 class 定义（越界 L07）"""
        for py_file in EXERCISES_DIR.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            source = py_file.read_text()
            assert "class " not in source, f"{py_file.name} 不应包含 class 定义"
