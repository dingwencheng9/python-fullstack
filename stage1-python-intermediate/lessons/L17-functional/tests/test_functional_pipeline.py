"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L15: 函数式编程 - 函数式管道测试
"""


def test_process_data():
    """测试数据处理管道"""
    result = functional_pipeline.process_data([1, 2, 3, 4, 5, 6])
    # 过滤偶数: [2, 4, 6]
    # 平方: [4, 16, 36]
    # 求和: 56
    assert result == 56


def test_process_data_empty():
    """测试空列表"""
    result = functional_pipeline.process_data([])
    assert result == 0


def test_transform_strings():
    """测试字符串转换"""
    strings = ["", "hello", "", "world", "python"]
    result = functional_pipeline.transform_strings(strings)
    assert result == ["HELLO", "PYTHON", "WORLD"]


def test_transform_strings_all_empty():
    """测试全空字符串"""
    result = functional_pipeline.transform_strings(["", ""])
    assert result == []


def test_compose():
    """测试函数组合"""
    double = lambda x: x * 2
    add_one = lambda x: x + 1
    square = lambda x: x**2

    f = functional_pipeline.compose(double, add_one)
    assert f(5) == 12  # double(add_one(5)) = double(6) = 12

    g = functional_pipeline.compose(square, add_one)
    assert g(5) == 36  # square(add_one(5)) = square(6) = 36


def test_compose_single():
    """测试单函数组合"""
    f = functional_pipeline.compose(lambda x: x * 2)
    assert f(5) == 10


def test_compose_three():
    """测试三个函数组合"""
    add = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x**2

    f = functional_pipeline.compose(double, add, square)
    # compose(f, g, h)(x) = f(g(h(x)))
    # compose(double, add, square)(5) = double(add(square(5))) = double(add(25)) = double(26) = 52
    assert f(5) == 52


def test_pipe():
    """测试管道组合"""
    double = lambda x: x * 2
    add_one = lambda x: x + 1

    p = functional_pipeline.pipe(add_one, double)
    assert p(5) == 12  # double(add_one(5)) = 12


def test_pipe_three():
    """测试三个函数管道"""
    add = lambda x: x + 1
    double = lambda x: x * 2
    square = lambda x: x**2

    p = functional_pipeline.pipe(add, double, square)
    # pipe(f, g, h)(x) = h(g(f(x)))
    # pipe(add, double, square)(5) = square(double(add(5))) = square(double(6)) = square(12) = 144
    assert p(5) == 144
