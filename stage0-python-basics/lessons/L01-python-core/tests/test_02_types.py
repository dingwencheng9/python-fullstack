"""测试 L01 Part 2: 变量与数据类型。

测试变量引用模型、基本数据类型、类型转换等。
"""


def test_variable_assignment():
    """测试变量赋值。"""
    x = 100
    assert x == 100

    y = x
    assert y == 100
    assert x == y


def test_basic_types():
    """测试基本数据类型。"""
    # 整数
    age: int = 25
    assert isinstance(age, int)
    assert age == 25

    # 浮点数
    height: float = 1.75
    assert isinstance(height, float)
    assert height == 1.75

    # 字符串
    name: str = "Alice"
    assert isinstance(name, str)
    assert name == "Alice"

    # 布尔值
    is_active: bool = True
    assert isinstance(is_active, bool)
    assert is_active is True


def test_none_type():
    """测试 None 类型。"""
    result = None
    assert result is None
    assert type(result) is type(None)

    # is None 判断
    assert result is None  # 直接断言，无需 if/else 分支


def test_type_annotations():
    """测试类型注解（运行时不强制）。"""
    name: str = "Bob"
    age: int = 30

    assert isinstance(name, str)
    assert isinstance(age, int)

    # 类型注解不强制类型
    x: int = "hello"  # 运行时不报错
    assert isinstance(x, str)  # 实际类型是 str


def test_type_conversion():
    """测试类型转换。"""
    # 字符串转整数
    assert int("123") == 123
    assert int("100") == 100

    # 字符串转浮点数
    assert float("3.14") == 3.14
    assert float("99.99") == 99.99

    # 整数转字符串
    assert str(100) == "100"
    assert str(25) == "25"

    # 浮点数转整数（截断）
    assert int(3.14) == 3
    assert int(9.99) == 9

    # 转换为布尔值
    assert bool(1) is True
    assert bool(0) is False
    assert bool("hello") is True
    assert bool("") is False
    assert bool(None) is False


def test_isinstance():
    """测试 isinstance() 类型检查。"""
    assert isinstance(100, int)
    assert isinstance(3.14, float)
    assert isinstance("hello", str)
    assert isinstance(True, bool)

    # 多类型检查
    assert isinstance(100, (int, float))
    assert isinstance(3.14, (int, float))


def test_immutability():
    """测试不可变性。"""
    # 整数不可变
    x = 100
    y = x
    x = 200  # x 指向新对象

    assert x == 200
    assert y == 100  # y 不变

    # 字符串不可变
    s = "hello"
    original_s = s
    s_upper = s.upper()  # 返回新字符串

    assert s == "hello"  # 原字符串不变
    assert s_upper == "HELLO"
    assert s is original_s


def test_fstring_formatting():
    """测试 f-string 格式化。"""
    name = "Alice"
    age = 25

    # 基本 f-string
    result = f"我是 {name}，今年 {age} 岁"
    assert result == "我是 Alice，今年 25 岁"

    # 表达式
    result2 = f"明年我 {age + 1} 岁"
    assert result2 == "明年我 26 岁"

    # 格式化数字
    pi = 3.14159
    result3 = f"π ≈ {pi:.2f}"
    assert result3 == "π ≈ 3.14"


def test_fstring_debug_mode():
    """测试 f-string 调试模式（Python 3.8+）。"""
    x = 100

    # = 会显示变量名和值
    result = f"{x=}"
    assert "x=" in result
    assert "100" in result


def test_string_methods():
    """测试字符串方法。"""
    text = "  Python  "

    assert text.strip() == "Python"
    assert text.upper().strip() == "PYTHON"
    assert text.lower().strip() == "python"
    assert "Python".startswith("Py")
    assert "Python".endswith("on")
    assert "Python".replace("P", "J") == "Jython"


def test_numeric_operations():
    """测试数值操作。"""
    # 整数运算
    assert 10 + 5 == 15
    assert 10 - 5 == 5
    assert 10 * 5 == 50
    assert 10 // 5 == 2

    # 浮点数运算
    assert 10.0 / 3.0 == 10.0 / 3.0  # 浮点除法
    assert abs(10.0 / 3.0 - 3.333333) < 0.00001

    # 幂运算
    assert 2**3 == 8
    assert 10**2 == 100
