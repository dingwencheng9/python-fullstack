"""L08 魔术方法与协议 - 学员练习测试

测试 exercises/ 目录下学员编写的代码。
"""

from __future__ import annotations

import importlib.util
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
def fraction_module():
    """加载 exercises/01_fraction.py"""
    return _load_exercise_module("_test_fraction", EXERCISES_DIR / "01_fraction.py")


@pytest.fixture(scope="module")
def set_class_module():
    """加载 exercises/02_set_class.py"""
    return _load_exercise_module("_test_set_class", EXERCISES_DIR / "02_set_class.py")


@pytest.fixture(scope="module")
def callable_module():
    """加载 exercises/03_callable.py"""
    return _load_exercise_module("_test_callable", EXERCISES_DIR / "03_callable.py")


# ============================================================
# 01_fraction.py 测试
# ============================================================


class TestFraction:
    """测试 Fraction 类"""

    def test_fraction_creation(self, fraction_module) -> None:
        """测试分数创建"""
        cls = getattr(fraction_module, "Fraction", None)
        assert cls is not None, "请定义 Fraction 类"

        f = cls(1, 2)
        assert f.numerator == 1
        assert f.denominator == 2

    def test_fraction_reduction(self, fraction_module) -> None:
        """测试分数约分"""
        cls = getattr(fraction_module, "Fraction", None)
        f = cls(2, 4)
        assert f.numerator == 1
        assert f.denominator == 2

    def test_fraction_negative(self, fraction_module) -> None:
        """测试负分数"""
        cls = getattr(fraction_module, "Fraction", None)
        f = cls(-1, 2)
        assert f.numerator == -1
        assert f.denominator == 2

        f2 = cls(1, -2)
        assert f2.numerator == -1
        assert f2.denominator == 2

    def test_fraction_repr(self, fraction_module) -> None:
        """测试 __repr__"""
        cls = getattr(fraction_module, "Fraction", None)
        f = cls(1, 2)
        assert "Fraction" in repr(f)
        assert "1" in repr(f)

    def test_fraction_str(self, fraction_module) -> None:
        """测试 __str__"""
        cls = getattr(fraction_module, "Fraction", None)
        f = cls(1, 2)
        assert str(f) == "1/2"

    def test_fraction_eq(self, fraction_module) -> None:
        """测试 __eq__"""
        cls = getattr(fraction_module, "Fraction", None)
        f1 = cls(1, 2)
        f2 = cls(2, 4)
        assert f1 == f2

    def test_fraction_add(self, fraction_module) -> None:
        """测试 __add__"""
        cls = getattr(fraction_module, "Fraction", None)
        f1 = cls(1, 3)
        f2 = cls(1, 6)
        result = f1 + f2
        assert result == cls(1, 2)  # 1/3 + 1/6 = 1/2


# ============================================================
# 02_set_class.py 测试
# ============================================================


class TestSetClass:
    """测试 Set 类"""

    def test_set_creation(self, set_class_module) -> None:
        """测试集合创建"""
        cls = getattr(set_class_module, "Set", None)
        assert cls is not None, "请定义 Set 类"

        s = cls()
        assert len(s) == 0

    def test_set_add(self, set_class_module) -> None:
        """测试添加元素"""
        cls = getattr(set_class_module, "Set", None)
        s = cls()
        s.add("apple")
        assert len(s) == 1

        # 重复添加不应增加大小
        s.add("apple")
        assert len(s) == 1

    def test_set_remove(self, set_class_module) -> None:
        """测试移除元素"""
        cls = getattr(set_class_module, "Set", None)
        s = cls()
        s.add("apple")
        s.add("banana")

        assert s.remove("apple") is True
        assert len(s) == 1
        assert "apple" not in s

        # 移除不存在的元素应返回 False
        assert s.remove("orange") is False

    def test_set_contains(self, set_class_module) -> None:
        """测试 __contains__"""
        cls = getattr(set_class_module, "Set", None)
        s = cls()
        s.add("apple")

        assert "apple" in s
        assert "banana" not in s

    def test_set_iter(self, set_class_module) -> None:
        """测试 __iter__"""
        cls = getattr(set_class_module, "Set", None)
        s = cls()
        s.add("apple")
        s.add("banana")

        items = list(s)
        assert len(items) == 2


# ============================================================
# 03_callable.py 测试
# ============================================================


class TestCallable:
    """测试 Multiplier 类（实现 __call__）"""

    def test_multiplier_callable(self, callable_module) -> None:
        """测试 Multiplier 可调用"""
        cls = getattr(callable_module, "Multiplier", None)
        assert cls is not None, "请定义 Multiplier 类"

        doubler = cls(2)
        assert callable(doubler)
        assert doubler(5) == 10

    def test_multiplier_call(self, callable_module) -> None:
        """测试乘法调用"""
        cls = getattr(callable_module, "Multiplier", None)
        tripler = cls(3)
        assert tripler(5) == 15

    def test_multiplier_repr(self, callable_module) -> None:
        """测试 __repr__"""
        cls = getattr(callable_module, "Multiplier", None)
        m = cls(5)
        assert "Multiplier" in repr(m)
        assert "5" in repr(m)
