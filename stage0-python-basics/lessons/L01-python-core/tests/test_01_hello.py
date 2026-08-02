"""测试 L01 Part 1: Python 入门基础。

测试基本的 print、input 等功能。
"""


def test_hello_world(capsys):
    """测试基本的 print 功能。"""
    print("Hello, World!")
    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out


def test_string_basics():
    """测试字符串基础操作。"""
    # 字符串创建
    name = "Alice"
    assert isinstance(name, str)
    assert len(name) == 5

    # 字符串拼接
    greeting = "Hello, " + name
    assert greeting == "Hello, Alice"

    # 字符串方法
    assert name.upper() == "ALICE"
    assert name.lower() == "alice"


def test_type_function():
    """测试 type() 函数。"""
    assert isinstance(42, int)
    assert isinstance(3.14, float)
    assert isinstance("hello", str)
    assert isinstance(True, bool)
    assert type(None) is type(None)


def test_print_multiple_args(capsys):
    """测试 print 函数的多参数。"""
    print("Python", 3.13, "is", "awesome!")
    captured = capsys.readouterr()
    assert "Python" in captured.out
    assert "3.13" in captured.out
    assert "awesome" in captured.out


def test_input_output_simulation(monkeypatch, capsys):
    """测试输入输出模拟。"""
    # 模拟用户输入
    monkeypatch.setattr("builtins.input", lambda _: "TestUser")

    # 获取输入
    name = input("请输入姓名：")
    assert name == "TestUser"

    # 输出
    print(f"你好，{name}！")

    # 捕获输出
    captured = capsys.readouterr()
    assert "TestUser" in captured.out


def test_basic_arithmetic():
    """测试基本算术运算。"""
    assert 2 + 3 == 5
    assert 10 - 4 == 6
    assert 3 * 4 == 12
    assert 10 / 2 == 5.0
    assert 10 // 3 == 3  # 整除
    assert 10 % 3 == 1  # 取模


def test_string_formatting():
    """测试字符串格式化。"""
    name = "Bob"
    age = 25

    # 字符串拼接
    result1 = "我是 " + name + "，今年 " + str(age) + " 岁"
    assert "Bob" in result1
    assert "25" in result1

    # f-string
    result2 = f"我是 {name}，今年 {age} 岁"
    assert result2 == "我是 Bob，今年 25 岁"
