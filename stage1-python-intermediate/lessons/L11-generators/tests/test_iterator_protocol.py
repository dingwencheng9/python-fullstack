"""

# noqa: F821  # conftest.py autouse fixture 动态注入模块到命名空间
L11: 生成器与迭代器 - 迭代器协议测试
"""


def test_fibonacci_iterator():
    """测试斐波那契迭代器"""
    fib = iterator_protocol.FibonacciIterator(limit=10)
    result = list(fib)
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert result == expected


def test_fibonacci_iterator_limit_0():
    """测试边界条件：limit=0"""
    fib = iterator_protocol.FibonacciIterator(limit=0)
    assert list(fib) == []


def test_custom_range_positive():
    """测试自定义 Range（正向）"""
    r = iterator_protocol.Range(start=0, stop=5, step=1)
    assert list(r) == [0, 1, 2, 3, 4]


def test_custom_range_negative():
    """测试自定义 Range（负向）"""
    r = iterator_protocol.Range(start=5, stop=0, step=-1)
    assert list(r) == [5, 4, 3, 2, 1]


def test_custom_range_default_step():
    """测试默认步长"""
    r = iterator_protocol.Range(start=0, stop=3)
    assert list(r) == [0, 1, 2]


def test_counter():
    """测试计数器"""
    counter = iterator_protocol.Counter(max_val=5)
    assert list(counter) == [1, 2, 3, 4, 5]


def test_counter_with_start():
    """测试带起始值的计数器"""
    counter = iterator_protocol.Counter(max_val=15, start=10)
    assert list(counter) == [11, 12, 13, 14, 15]
