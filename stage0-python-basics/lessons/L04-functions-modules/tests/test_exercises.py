"""测试文件：L04 函数与模块 - Exercises 直接测试

直接测试 exercises/01_functions.py 和 exercises/02_modules.py 中的函数实现。
"""

import importlib.util
from pathlib import Path

import pytest


# 直接加载 exercises 模块（不依赖 sys.path 注入）
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
def functions_module():
    """加载 exercises/01_functions.py"""
    return _load_exercise_module("_test_01_functions", EXERCISES_DIR / "01_functions.py")


@pytest.fixture(scope="module")
def modules_module():
    """加载 exercises/02_modules.py"""
    return _load_exercise_module("_test_02_modules", EXERCISES_DIR / "02_modules.py")


class TestFactorial:
    """测试 factorial 函数"""

    def test_positive_cases(self, functions_module) -> None:
        """测试正整数阶乘"""
        assert functions_module.factorial(0) == 1
        assert functions_module.factorial(1) == 1
        assert functions_module.factorial(5) == 120
        assert functions_module.factorial(10) == 3628800

    def test_negative_raises_error(self, functions_module) -> None:
        """测试负数抛出 ValueError"""
        with pytest.raises(ValueError, match="非负整数"):
            functions_module.factorial(-1)

    def test_float_result(self, functions_module) -> None:
        """测试浮点数（Python 递归支持浮点，返回实数阶乘）"""
        # Python 递归函数对浮点数不抛异常，返回实数阶乘
        result = functions_module.factorial(3.5)
        assert result == 13.125


class TestFibonacci:
    """测试 fibonacci 函数"""

    def test_sequence_values(self, functions_module) -> None:
        """测试斐波那契数列值"""
        # 斐波那契数列: F(0)=0, F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, F(6)=8, F(7)=13, F(8)=21, F(9)=34
        assert functions_module.fibonacci(0) == 0
        assert functions_module.fibonacci(1) == 1
        assert functions_module.fibonacci(2) == 1
        assert functions_module.fibonacci(3) == 2
        assert functions_module.fibonacci(4) == 3
        assert functions_module.fibonacci(5) == 5
        assert functions_module.fibonacci(6) == 8
        assert functions_module.fibonacci(7) == 13
        assert functions_module.fibonacci(8) == 21
        assert functions_module.fibonacci(9) == 34

    def test_negative_raises_error(self, functions_module) -> None:
        """测试负数抛出 ValueError"""
        with pytest.raises(ValueError, match="非负整数"):
            functions_module.fibonacci(-1)


class TestFindMax:
    """测试 find_max 函数"""

    def test_normal_list(self, functions_module) -> None:
        """测试普通列表"""
        assert functions_module.find_max([3, 1, 4, 1, 5, 9, 2, 6]) == 9
        assert functions_module.find_max([1, 2, 3, 4, 5]) == 5
        assert functions_module.find_max([-5, -2, -8, -1]) == -1

    def test_empty_list(self, functions_module) -> None:
        """测试空列表返回 None"""
        assert functions_module.find_max([]) is None

    def test_single_element(self, functions_module) -> None:
        """测试单元素列表"""
        assert functions_module.find_max([42]) == 42


class TestFilterEven:
    """测试 filter_even 函数"""

    def test_mixed_list(self, functions_module) -> None:
        """测试混合列表"""
        result = functions_module.filter_even([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        assert result == [2, 4, 6, 8, 10]

    def test_all_even(self, functions_module) -> None:
        """测试全偶数列表"""
        result = functions_module.filter_even([2, 4, 6, 8])
        assert result == [2, 4, 6, 8]

    def test_all_odd(self, functions_module) -> None:
        """测试全奇数列表"""
        result = functions_module.filter_even([1, 3, 5, 7])
        assert result == []

    def test_empty_list(self, functions_module) -> None:
        """测试空列表"""
        assert functions_module.filter_even([]) == []


class TestCalculateAverage:
    """测试 calculate_average 函数"""

    def test_normal_list(self, modules_module) -> None:
        """测试普通列表"""
        assert modules_module.calculate_average([1, 2, 3, 4, 5]) == 3.0
        assert modules_module.calculate_average([10, 20, 30]) == 20.0

    def test_empty_list(self, modules_module) -> None:
        """测试空列表返回 None"""
        assert modules_module.calculate_average([]) is None

    def test_single_element(self, modules_module) -> None:
        """测试单元素列表"""
        assert modules_module.calculate_average([42]) == 42.0


class TestPublicAPI:
    """测试 public_api 函数"""

    def test_returns_dict_with_count_and_data(self, modules_module) -> None:
        """测试返回包含 count 和 data 的字典"""
        data = ["a", "b", "c"]
        result = modules_module.public_api(data)
        assert isinstance(result, dict)
        assert result["count"] == 3
        assert result["data"] == ["a", "b", "c"]

    def test_empty_list(self, modules_module) -> None:
        """测试空列表"""
        result = modules_module.public_api([])
        assert result["count"] == 0
        assert result["data"] == []


class TestPrivateHelper:
    """测试 _private_helper 函数（内部函数）"""

    def test_doubles_value(self, modules_module) -> None:
        """测试私有函数功能"""
        assert modules_module._private_helper(5) == 10
        assert modules_module._private_helper(0) == 0
        assert modules_module._private_helper(-3) == -6


class TestCalculateTotal:
    """测试 calculate_total 函数"""

    def test_normal_cases(self, modules_module) -> None:
        """测试正常情况（每个商品 10 元）"""
        assert modules_module.calculate_total(["item1", "item2", "item3"]) == 30
        assert modules_module.calculate_total([]) == 0
        assert modules_module.calculate_total(["only_one"]) == 10


class TestAppConfig:
    """测试 AppConfig dataclass"""

    def test_create_config(self, modules_module) -> None:
        """测试创建配置"""
        config = modules_module.create_config("MyApp", "1.0.0", debug=True)
        assert config.name == "MyApp"
        assert config.version == "1.0.0"
        assert config.debug is True

    def test_default_values(self, modules_module) -> None:
        """测试默认值"""
        config = modules_module.create_config("TestApp", "2.0.0")
        assert config.name == "TestApp"
        assert config.version == "2.0.0"
        assert config.debug is False


class TestFormatUsername:
    """测试 format_username 函数"""

    def test_lowercase_and_strip(self, modules_module) -> None:
        """测试转小写和去除空格"""
        assert modules_module.format_username("  Alice123  ") == "alice123"
        assert modules_module.format_username("BOB") == "bob"
        assert modules_module.format_username("UsErNaMe") == "username"


class TestValidateLength:
    """测试 validate_length 函数"""

    def test_valid_length(self, modules_module) -> None:
        """测试有效长度"""
        assert modules_module.validate_length("hello") is True
        assert modules_module.validate_length("hi") is False  # 太短

    def test_with_min_max_params(self, modules_module) -> None:
        """测试自定义 min/max 参数"""
        assert modules_module.validate_length("hello", min_len=3, max_len=10) is True
        assert modules_module.validate_length("hi", min_len=3, max_len=10) is False


class TestProcessUserInput:
    """测试 process_user_input 函数"""

    def test_valid_username(self, modules_module) -> None:
        """测试有效用户名"""
        success, msg = modules_module.process_user_input("  Alice123  ")
        assert success is True
        assert "alice123" in msg

    def test_empty_username(self, modules_module) -> None:
        """测试空用户名"""
        success, msg = modules_module.process_user_input("")
        assert success is False
        assert "不能为空" in msg

    def test_too_short_username(self, modules_module) -> None:
        """测试太短的用户名"""
        success, msg = modules_module.process_user_input("ab")
        assert success is False
        assert "长度" in msg

    def test_too_long_username(self, modules_module) -> None:
        """测试太长的用户名"""
        long_name = "a" * 25
        success, msg = modules_module.process_user_input(long_name)
        assert success is False
        assert "长度" in msg
