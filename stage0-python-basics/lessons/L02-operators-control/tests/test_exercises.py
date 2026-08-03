"""L02 运算符与控制流 - 学员练习测试

测试 exercises/ 目录下学员编写的代码。
"""

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
def arithmetic_module():
    """加载 exercises/01_arithmetic_conditions.py"""
    return _load_exercise_module("_test_arithmetic", EXERCISES_DIR / "01_arithmetic_conditions.py")


@pytest.fixture(scope="module")
def logical_module():
    """加载 exercises/02_logical_operators.py"""
    return _load_exercise_module("_test_logical", EXERCISES_DIR / "02_logical_operators.py")


@pytest.fixture(scope="module")
def loops_module():
    """加载 exercises/04_loops.py"""
    return _load_exercise_module("_test_loops", EXERCISES_DIR / "04_loops.py")


@pytest.fixture(scope="module")
def match_module():
    """加载 exercises/05_match_case.py"""
    return _load_exercise_module("_test_match", EXERCISES_DIR / "05_match_case.py")


# ============================================================
# 01_arithmetic_conditions.py 测试
# ============================================================


class TestArithmeticConditions:
    """测试 01_arithmetic_conditions.py"""

    def test_calculate_bmi(self, arithmetic_module) -> None:
        """测试 BMI 计算"""
        func = getattr(arithmetic_module, "calculate_bmi", None)
        assert func is not None, "请定义 calculate_bmi 函数"

        # 测试正常情况
        bmi, level = func(70, 1.75)
        assert 22 <= bmi <= 23, f"BMI 应在 22-23 之间，实际得到 {bmi}"
        assert level == "正常"

        # 测试偏瘦
        bmi, level = func(45, 1.8)
        assert level == "偏瘦"

        # 测试肥胖
        bmi, level = func(90, 1.7)
        assert level == "肥胖"

    def test_calculate_grade(self, arithmetic_module) -> None:
        """测试成绩等级计算"""
        func = getattr(arithmetic_module, "calculate_grade", None)
        assert func is not None, "请定义 calculate_grade 函数"

        assert func(95) == "S"
        assert func(88) == "A"
        assert func(75) == "B"
        assert func(65) == "C"
        assert func(45) == "D"


# ============================================================
# 02_logical_operators.py 测试
# ============================================================


class TestLogicalOperators:
    """测试 02_logical_operators.py"""

    def test_safe_get(self, logical_module) -> None:
        """测试安全字典访问"""
        func = getattr(logical_module, "safe_get", None)
        assert func is not None, "请定义 safe_get 函数"

        assert func({"name": "Alice"}, "name") == "Alice"
        assert func(None, "name", "Unknown") == "Unknown"
        assert func({}, "name", "N/A") == "N/A"

    def test_validate_age(self, logical_module) -> None:
        """测试年龄验证"""
        func = getattr(logical_module, "validate_age", None)
        assert func is not None, "请定义 validate_age 函数"

        assert "有效" in func(25)
        assert "未提供" in func(None)
        assert "大于0" in func(0)

    def test_get_user_status(self, logical_module) -> None:
        """测试用户状态判断"""
        func = getattr(logical_module, "get_user_status", None)
        assert func is not None, "请定义 get_user_status 函数"

        assert func(False, False, False) == "游客"
        assert func(True, False, False) == "普通用户"
        assert func(True, True, False) == "VIP 用户"


# ============================================================
# 04_loops.py 测试
# ============================================================


class TestLoops:
    """测试 04_loops.py"""

    def test_find_first_negative(self, loops_module) -> None:
        """测试查找第一个负数"""
        func = getattr(loops_module, "find_first_negative", None)
        assert func is not None, "请定义 find_first_negative 函数"

        assert func([1, 2, -3, 4]) == -3
        assert func([1, 2, 3]) is None

    def test_sum_until_negative(self, loops_module) -> None:
        """测试累加到负数"""
        func = getattr(loops_module, "sum_until_negative", None)
        assert func is not None, "请定义 sum_until_negative 函数"

        assert func([1, 2, 3, 4, 5]) == 15
        assert func([1, 2, -3, 4]) == 3

    def test_skip_zeros(self, loops_module) -> None:
        """测试跳过零"""
        func = getattr(loops_module, "skip_zeros", None)
        assert func is not None, "请定义 skip_zeros 函数"

        assert func([1, 0, 2, 0, 3]) == [1, 4, 9]

    def test_countdown(self, loops_module) -> None:
        """测试倒计时"""
        func = getattr(loops_module, "countdown", None)
        assert func is not None, "请定义 countdown 函数"

        assert func(5) == [5, 4, 3, 2, 1]
        assert func(1) == [1]
        assert func(0) == []

    def test_fibonacci(self, loops_module) -> None:
        """测试斐波那契数列"""
        func = getattr(loops_module, "fibonacci", None)
        assert func is not None, "请定义 fibonacci 函数"

        assert func(7) == [1, 1, 2, 3, 5, 8, 13]
        assert func(1) == [1]
        assert func(0) == []


# ============================================================
# 05_match_case.py 测试
# ============================================================


class TestMatchCase:
    """测试 05_match_case.py"""

    def test_describe_http_status(self, match_module) -> None:
        """测试 HTTP 状态码描述"""
        func = getattr(match_module, "describe_http_status", None)
        assert func is not None, "请定义 describe_http_status 函数"

        assert "请求成功" in func(200)
        assert "资源不存在" in func(404)
        assert "服务器错误" in func(500)
        assert "Unknown" in func(418)

    def test_parse_command(self, match_module) -> None:
        """测试命令解析"""
        func = getattr(match_module, "parse_command", None)
        assert func is not None, "请定义 parse_command 函数"

        assert "status" in func("git status")
        assert "checkout" in func("git checkout main")
        assert "npm" in func("npm install")

    def test_classify_point(self, match_module) -> None:
        """测试坐标分类"""
        func = getattr(match_module, "classify_point", None)
        assert func is not None, "请定义 classify_point 函数"

        assert func(0, 0) == "原点"
        assert func(3, 4) == "第一象限"
        assert func(-2, 5) == "第二象限"
        assert func(5, 0) == "x轴正半轴"
