"""
L11: 生成器与迭代器 - 生成器练习

使用生成器函数实现数据处理管道。
"""


def count_up(n: int):
    """从 1 数到 n。"""
    for value in range(1, n + 1):
        yield value


def squares(n: int):
    """生成前 n 个非负整数的平方。"""
    for value in range(n):
        yield value * value


def chain(*iterables):
    """链式迭代多个可迭代对象。"""
    for iterable in iterables:
        # L12 预告: yield from 可以简化此循环
        for item in iterable:
            yield item


def chunked(iterable, size: int):
    """将可迭代对象分块，最后一块可以不足 size。"""
    if size <= 0:
        raise ValueError("size 必须为正整数")
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk


def flatten(nested: list) -> list:
    """扁平化嵌套列表。"""

    def _flatten(items):
        for item in items:
            if isinstance(item, list):
                # L12 预告: yield from 可以简化递归扁平化
                # 当前使用显式嵌套循环
                for sub_item in _flatten(item):
                    yield sub_item
            else:
                yield item

    return list(_flatten(nested))


# === 验证 ===

if __name__ == "__main__":
    # 测试 count_up
    assert list(count_up(5)) == [1, 2, 3, 4, 5]

    # 测试 squares
    assert list(squares(5)) == [0, 1, 4, 9, 16]

    # 测试 chain
    assert list(chain([1, 2], [3, 4], [5])) == [1, 2, 3, 4, 5]

    # 测试 chunked
    assert list(chunked(range(10), 3)) == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    # 测试 flatten
    assert flatten([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]

    print("✅ 所有测试通过！")
