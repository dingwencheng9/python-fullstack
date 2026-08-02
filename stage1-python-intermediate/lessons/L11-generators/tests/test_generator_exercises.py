"""
L11: 生成器与迭代器 - 生成器练习测试

模块由 conftest.py autouse fixture 动态注入，无需显式导入。
"""

# noqa: F821  # conftest.py autouse fixture 注入模块到命名空间


def test_fibonacci_generator():
    """测试斐波那契生成器"""
    result = list(generator_exercises.fibonacci(10))
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert result == expected


def test_fibonacci_limit_0():
    """测试边界条件"""
    result = list(generator_exercises.fibonacci(0))
    assert result == []


def test_flatten_simple():
    """测试简单列表展平"""
    nested = [1, [2, 3], [4, [5, 6]]]
    result = list(generator_exercises.flatten(nested))
    assert result == [1, 2, 3, 4, 5, 6]


def test_flatten_empty():
    """测试空列表"""
    result = list(generator_exercises.flatten([]))
    assert result == []


def test_flatten_no_nesting():
    """测试无嵌套列表"""
    result = list(generator_exercises.flatten([1, 2, 3]))
    assert result == [1, 2, 3]


def test_chunked():
    """测试分块"""
    data = [1, 2, 3, 4, 5, 6, 7]
    result = list(generator_exercises.chunked(data, 3))
    assert result == [[1, 2, 3], [4, 5, 6], [7]]


def test_chunked_exact():
    """测试完全分割"""
    data = [1, 2, 3, 4]
    result = list(generator_exercises.chunked(data, 2))
    assert result == [[1, 2], [3, 4]]


def test_prime_numbers():
    """测试素数生成"""
    primes = list(generator_exercises.prime_numbers(30))
    expected = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert primes == expected


def test_pairwise():
    """测试相邻元素对"""
    data = [1, 2, 3, 4]
    result = list(generator_exercises.pairwise(data))
    assert result == [(1, 2), (2, 3), (3, 4)]


def test_pairwise_single():
    """测试单元素列表"""
    result = list(generator_exercises.pairwise([1]))
    assert result == []


def test_sliding_window():
    """测试滑动窗口"""
    data = [1, 2, 3, 4, 5]
    result = list(generator_exercises.sliding_window(data, 3))
    assert result == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
