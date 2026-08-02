"""
L15: 函数式编程 - 函数式管道练习

使用 map/filter/reduce 实现数据处理。
"""

from functools import reduce


def process_data(data: list[int]) -> int:
    """过滤偶数 -> 平方 -> 求和。"""
    return reduce(
        lambda total, value: total + value,
        map(lambda value: value**2, filter(lambda value: value % 2 == 0, data)),
        0,
    )


def transform_strings(strings: list[str]) -> list[str]:
    """过滤空字符串 -> 转大写 -> 排序。"""
    return sorted(map(str.upper, filter(bool, strings)))


def compose(*functions):
    """函数组合: f ∘ g，从右到左执行。"""

    def composed(value):
        result = value
        for func in reversed(functions):
            result = func(result)
        return result

    return composed


def pipe(*functions):
    """管道组合: f | g，从左到右执行。"""

    def piped(value):
        result = value
        for func in functions:
            result = func(result)
        return result

    return piped


# === 验证 ===

if __name__ == "__main__":
    # 测试数据处理
    assert process_data([1, 2, 3, 4, 5, 6]) == 56  # 2² + 4² + 6²

    # 测试字符串处理
    strings = ["", "hello", "", "world", "python"]
    result = transform_strings(strings)
    assert result == ["HELLO", "PYTHON", "WORLD"]

    # 测试函数组合
    double = lambda x: x * 2
    add_one = lambda x: x + 1
    square = lambda x: x**2

    f = compose(double, add_one)
    assert f(5) == 12  # double(add_one(5)) = double(6) = 12

    p = pipe(add_one, double)
    assert p(5) == 12  # double(add_one(5)) = 12

    print("✅ 所有测试通过！")
