"""L01 Python 核心语法 - 学员练习测试

测试 exercises/ 目录下学员编写的代码。
采用与 L04 相同的 importlib 模式，不污染 sys.path。
"""

import importlib.util
from pathlib import Path

import pytest


# 通过物理路径加载 exercises 模块
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
def hello_module():
    """加载 exercises/01_hello_practice.py"""
    return _load_exercise_module("_test_hello", EXERCISES_DIR / "01_hello_practice.py")


@pytest.fixture(scope="module")
def io_module():
    """加载 exercises/02_io_practice.py"""
    return _load_exercise_module("_test_io", EXERCISES_DIR / "02_io_practice.py")


@pytest.fixture(scope="module")
def types_module():
    """加载 exercises/03_type_basics.py"""
    return _load_exercise_module("_test_types", EXERCISES_DIR / "03_type_basics.py")


@pytest.fixture(scope="module")
def conversion_module():
    """加载 exercises/04_type_conversion.py"""
    return _load_exercise_module("_test_conversion", EXERCISES_DIR / "04_type_conversion.py")


@pytest.fixture(scope="module")
def fstring_module():
    """加载 exercises/05_fstring_practice.py"""
    return _load_exercise_module("_test_fstring", EXERCISES_DIR / "05_fstring_practice.py")


# ============================================================
# 01_hello_practice.py 测试
# ============================================================


class TestHelloPractice:
    """测试 01_hello_practice.py"""

    def test_module_exists(self, hello_module) -> None:
        """验证模块可加载"""
        assert hello_module is not None

    def test_has_print_greeting_function(self, hello_module) -> None:
        """验证模块定义了 print_greeting 函数"""
        assert hasattr(hello_module, "print_greeting"), "请定义 print_greeting 函数"

    def test_print_greeting_accepts_arguments(self, hello_module, capsys) -> None:
        """测试 print_greeting 能接受姓名、年龄、城市、爱好参数"""
        func = getattr(hello_module, "print_greeting", None)
        assert func is not None, "请定义 print_greeting 函数"

        # 调用函数并捕获输出
        func("张三", 25, "北京", "编程")
        captured = capsys.readouterr()

        # 验证输出包含关键信息
        assert "张三" in captured.out, "输出应包含姓名"
        assert "北京" in captured.out, "输出应包含城市"


# ============================================================
# 02_io_practice.py 测试
# ============================================================


class TestIOPractice:
    """测试 02_io_practice.py"""

    def test_module_exists(self, io_module) -> None:
        """验证模块可加载"""
        assert io_module is not None

    def test_has_interactive_input(self, io_module, monkeypatch, capsys) -> None:
        """测试交互式输入输出"""
        # 模拟用户输入
        inputs = iter(["Alice", "30"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        if hasattr(io_module, "interactive_greeting"):
            io_module.interactive_greeting()
            captured = capsys.readouterr()
            assert "Alice" in captured.out or "30" in captured.out


# ============================================================
# 03_type_basics.py 测试
# ============================================================


class TestTypeBasics:
    """测试 03_type_basics.py"""

    def test_module_exists(self, types_module) -> None:
        """验证模块可加载"""
        assert types_module is not None

    def test_has_calculate_total_function(self, types_module) -> None:
        """验证定义了 calculate_total 函数"""
        assert hasattr(types_module, "calculate_total"), "请定义 calculate_total 函数"

    def test_calculate_total_returns_correct_value(self, types_module) -> None:
        """测试 calculate_total 返回正确结果"""
        func = getattr(types_module, "calculate_total", None)
        assert func is not None, "请定义 calculate_total 函数"

        # 测试几个典型用例
        result = func(100, 50, 25)
        assert result == 175, f"calculate_total(100, 50, 25) 应返回 175，实际得到 {result}"

        result = func(10, 20, 30)
        assert result == 60, f"calculate_total(10, 20, 30) 应返回 60，实际得到 {result}"


# ============================================================
# 04_type_conversion.py 测试
# ============================================================


class TestTypeConversion:
    """测试 04_type_conversion.py"""

    def test_module_exists(self, conversion_module) -> None:
        """验证模块可加载"""
        assert conversion_module is not None

    def test_has_safe_divide_function(self, conversion_module) -> None:
        """验证定义了 safe_divide 函数"""
        assert hasattr(conversion_module, "safe_divide"), "请定义 safe_divide 函数"

    def test_safe_divide_normal_cases(self, conversion_module) -> None:
        """测试 safe_divide 正常情况"""
        func = getattr(conversion_module, "safe_divide", None)
        assert func is not None, "请定义 safe_divide 函数"

        assert func(10, 2) == 5.0, "10 / 2 = 5.0"
        assert func(7, 2) == 3.5, "7 / 2 = 3.5"
        assert func(-10, 2) == -5.0, "-10 / 2 = -5.0"

    def test_safe_divide_by_zero(self, conversion_module) -> None:
        """测试除数为零时返回 None"""
        func = getattr(conversion_module, "safe_divide", None)
        assert func is not None, "请定义 safe_divide 函数"

        result = func(10, 0)
        assert result is None, "除数为零时应返回 None"


# ============================================================
# 05_fstring_practice.py 测试
# ============================================================


class TestFStringPractice:
    """测试 05_fstring_practice.py"""

    def test_module_exists(self, fstring_module) -> None:
        """验证模块可加载"""
        assert fstring_module is not None

    def test_has_format_user_info_function(self, fstring_module) -> None:
        """验证定义了 format_user_info 函数"""
        assert hasattr(fstring_module, "format_user_info"), "请定义 format_user_info 函数"

    def test_format_user_info_returns_string(self, fstring_module) -> None:
        """测试 format_user_info 返回格式化字符串"""
        func = getattr(fstring_module, "format_user_info", None)
        assert func is not None, "请定义 format_user_info 函数"

        result = func("张三", 25, "北京")
        assert isinstance(result, str), "应返回字符串"
        assert "张三" in result, "应包含姓名"
        assert "25" in result, "应包含年龄"
        assert "北京" in result, "应包含城市"

    def test_format_user_info_with_fstring(self, fstring_module) -> None:
        """测试使用了 f-string 格式化"""
        func = getattr(fstring_module, "format_user_info", None)
        assert func is not None, "请定义 format_user_info 函数"

        # 验证能正确处理中文
        result = func("李四", 30, "上海")
        assert "李四" in result
        assert "30" in result
        assert "上海" in result
