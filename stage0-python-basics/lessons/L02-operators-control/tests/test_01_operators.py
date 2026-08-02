"""测试 L02 Part 1: 运算符。"""


def test_arithmetic_operators():
    """测试算术运算符。"""
    assert 10 + 5 == 15
    assert 10 - 5 == 5
    assert 10 * 5 == 50
    assert 10 / 5 == 2.0
    assert 10 // 3 == 3
    assert 10 % 3 == 1
    assert 2**3 == 8


def test_comparison_operators():
    """测试比较运算符。"""
    assert (10 == 10) is True
    assert (10 != 5) is True
    assert (10 > 5) is True
    assert (5 < 10) is True
    assert (10 >= 10) is True
    assert (5 <= 10) is True


def test_logical_operators():
    """测试逻辑运算符。"""
    assert (True and True) is True
    assert (True and False) is False
    assert (True or False) is True
    assert (False or False) is False
    assert (not True) is False
    assert (not False) is True


def test_logical_short_circuit():
    """测试逻辑运算符的短路特性。"""
    # and: 第一个为假，不计算第二个
    result = False and (1 / 0)  # 不会报错
    assert result is False

    # or: 第一个为真，不计算第二个
    result = True or (1 / 0)  # 不会报错
    assert result is True


def test_bitwise_operators():
    """测试位运算符。"""
    assert 5 & 3 == 1  # 按位与
    assert 5 | 3 == 7  # 按位或
    assert 5 ^ 3 == 6  # 按位异或
    assert ~5 == -6  # 按位取反
    assert 5 << 1 == 10  # 左移
    assert 5 >> 1 == 2  # 右移


def test_assignment_operators():
    """测试赋值运算符。"""
    x = 10
    x += 5
    assert x == 15

    x -= 3
    assert x == 12

    x *= 2
    assert x == 24

    x //= 4
    assert x == 6

    x %= 4
    assert x == 2


def test_operator_precedence():
    """测试运算符优先级。"""
    # 乘法优先于加法
    assert 2 + 3 * 4 == 14

    # 幂运算优先于乘法
    assert 2 * 3**2 == 18

    # 括号改变优先级
    assert (2 + 3) * 4 == 20


def test_division_types():
    """测试除法类型。"""
    # 普通除法（返回浮点数）
    assert 10 / 3 == 10 / 3
    assert isinstance(10 / 3, float)

    # 整除（向下取整）
    assert 10 // 3 == 3
    assert isinstance(10 // 3, int)

    # 负数整除
    assert -10 // 3 == -4  # 向下取整


def test_modulo_operator():
    """测试取模运算符。"""
    assert 10 % 3 == 1
    assert 7 % 2 == 1
    assert 8 % 4 == 0

    # 负数取模
    assert -10 % 3 == 2


def test_power_operator():
    """测试幂运算符。"""
    assert 2**3 == 8
    assert 10**2 == 100
    assert 2**10 == 1024

    # 浮点数幂
    assert 4**0.5 == 2.0  # 平方根
