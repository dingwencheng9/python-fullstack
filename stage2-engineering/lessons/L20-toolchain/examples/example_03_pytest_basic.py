"""

from __future__ import annotations

L18 示例 3: pytest 测试基础

展示 pytest 的核心功能和测试最佳实践。
"""

import pytest

# ============================================================================
# 被测试的代码
# ============================================================================


class Calculator:
    """简单的计算器类"""

    def add(self, a: float, b: float) -> float:
        """加法"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """减法"""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """乘法"""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """除法"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class UserValidator:
    """用户验证器"""

    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        return "@" in email and "." in email.split("@")[1]

    @staticmethod
    def validate_age(age: int) -> bool:
        """验证年龄"""
        return 0 < age < 150


# ============================================================================
# 测试 1: 基础测试
# ============================================================================


def test_calculator_add():
    """测试加法"""
    calc = Calculator()
    assert calc.add(2, 3) == 5
    assert calc.add(-1, 1) == 0
    assert calc.add(0.1, 0.2) == pytest.approx(0.3)  # 浮点数比较


def test_calculator_subtract():
    """测试减法"""
    calc = Calculator()
    assert calc.subtract(5, 3) == 2
    assert calc.subtract(0, 5) == -5


def test_calculator_multiply():
    """测试乘法"""
    calc = Calculator()
    assert calc.multiply(3, 4) == 12
    assert calc.multiply(-2, 3) == -6


# ============================================================================
# 测试 2: 异常测试
# ============================================================================


def test_calculator_divide():
    """测试除法"""
    calc = Calculator()
    assert calc.divide(10, 2) == 5
    assert calc.divide(7, 2) == pytest.approx(3.5)


def test_calculator_divide_by_zero():
    """测试除以零"""
    calc = Calculator()

    # 使用 pytest.raises 测试异常
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calc.divide(10, 0)


# ============================================================================
# 测试 3: 参数化测试
# ============================================================================


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
    ],
)
def test_add_parametrized(a, b, expected):
    """参数化测试加法"""
    calc = Calculator()
    assert calc.add(a, b) == expected


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("user@example.com", True),
        ("invalid", False),
        ("no-at.com", False),
        ("no-dot@example", False),
        ("valid@sub.example.com", True),
    ],
)
def test_email_validation(email, expected):
    """参数化测试邮箱验证"""
    assert UserValidator.validate_email(email) == expected


# ============================================================================
# 测试 4: Fixture 使用
# ============================================================================


@pytest.fixture
def calculator():
    """创建 Calculator 实例的 fixture"""
    print("\n  [Setup] Creating calculator")
    calc = Calculator()
    yield calc
    print("\n  [Teardown] Cleaning up calculator")


def test_with_fixture(calculator):
    """使用 fixture 的测试"""
    assert calculator.add(1, 1) == 2
    assert calculator.multiply(2, 3) == 6


@pytest.fixture
def sample_users():
    """示例用户数据"""
    return [
        {"name": "Alice", "age": 25, "email": "alice@example.com"},
        {"name": "Bob", "age": 30, "email": "bob@example.com"},
    ]


def test_user_data(sample_users):
    """测试用户数据"""
    assert len(sample_users) == 2
    assert sample_users[0]["name"] == "Alice"


# ============================================================================
# 测试 5: 标记（Markers）
# ============================================================================


@pytest.mark.slow
def test_slow_operation():
    """标记为慢速测试"""
    import time

    time.sleep(0.1)
    assert True


@pytest.mark.skip(reason="Not implemented yet")
def test_feature_not_ready():
    """跳过未实现的测试"""
    raise AssertionError


@pytest.mark.skipif(pytest.__version__ < "8.0", reason="Requires pytest 8.0+")
def test_new_feature():
    """条件跳过测试"""
    assert True


@pytest.mark.xfail(reason="Known bug")
def test_known_bug():
    """标记为预期失败"""
    assert 1 == 2  # 这个测试会失败，但不会影响测试套件


# ============================================================================
# 测试 6: 测试类
# ============================================================================


class TestCalculator:
    """计算器测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试方法前自动运行"""
        self.calc = Calculator()

    def test_add(self):
        """测试加法"""
        assert self.calc.add(2, 2) == 4

    def test_subtract(self):
        """测试减法"""
        assert self.calc.subtract(5, 3) == 2


# ============================================================================
# 演示函数
# ============================================================================


def show_pytest_commands():
    """展示 pytest 命令"""

    print("\n🧪 pytest 常用命令")
    print("=" * 70)

    commands = [
        ("pytest", "运行所有测试"),
        ("pytest test_file.py", "运行指定文件"),
        ("pytest test_file.py::test_func", "运行指定测试"),
        ("pytest -v", "详细模式"),
        ("pytest -s", "显示 print 输出"),
        ("pytest -x", "遇到失败立即停止"),
        ("pytest --lf", "只运行上次失败的测试"),
        ("pytest -k 'add'", "运行名称包含 'add' 的测试"),
        ("pytest -m slow", "只运行标记为 slow 的测试"),
        ("pytest --cov=src", "生成覆盖率报告"),
    ]

    for cmd, desc in commands:
        print(f"\n  $ {cmd}")
        print(f"    → {desc}")


def show_pytest_config():
    """展示 pytest 配置"""

    print("\n\n⚙️  pytest 配置示例")
    print("=" * 70)

    config = """
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
]

# 自定义标记
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
"""

    print(config)


def show_best_practices():
    """展示最佳实践"""

    print("\n\n💡 pytest 最佳实践")
    print("=" * 70)

    practices = [
        "1. 测试文件以 test_ 开头或 _test 结尾",
        "2. 测试函数以 test_ 开头",
        "3. 使用 assert 进行断言，简单清晰",
        "4. 使用 parametrize 减少重复代码",
        "5. 使用 fixture 管理测试数据和状态",
        "6. 使用标记（markers）组织测试",
        "7. 保持测试独立，不依赖执行顺序",
        "8. 一个测试只验证一个行为",
        "9. 使用有意义的测试名称",
        "10. 保持测试覆盖率 > 80%",
    ]

    for practice in practices:
        print(f"  {practice}")


if __name__ == "__main__":
    print("🧪 pytest 测试基础演示")
    print("=" * 70)
    print("\n这个文件包含完整的 pytest 示例。")
    print("\n运行测试:")
    print("  $ pytest example_03_pytest_basic.py -v")

    show_pytest_commands()
    show_pytest_config()
    show_best_practices()

    print("\n\n✨ 提示：直接运行 pytest 查看测试结果")
