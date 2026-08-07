"""L12 示例1: yield from 委托机制

本示例演示 yield from 的基本用法和委托机制。
"""

from typing import Iterator


def gen_a() -> Iterator[int]:
    """第一个生成器"""
    yield 1
    yield 2


def gen_b() -> Iterator[int]:
    """第二个生成器"""
    yield 3
    yield 4


def delegated_generator() -> Iterator[int]:
    """委托给其他生成器"""
    yield from gen_a()  # 委托给 gen_a
    yield from gen_b()  # 委托给 gen_b


def equivalent_generator() -> Iterator[int]:
    """与 yield from 等价的显式实现"""
    for item in gen_a():
        yield item
    for item in gen_b():
        yield item


def chain_iterables(*iterables) -> Iterator:
    """串联多个可迭代对象"""
    for iterable in iterables:
        yield from iterable


def flatten(nested: list) -> Iterator:
    """展平嵌套列表（递归版）"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)  # 递归展平
        else:
            yield item


def flatten_iterative(nested: list) -> Iterator:
    """展平嵌套列表（迭代版）"""
    stack = list(reversed(nested))
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))
        else:
            yield item


def inner_generator():
    """返回值的子生成器"""
    yield 1
    yield 2
    return "done"


def outer_with_return() -> Iterator:
    """yield from 传播返回值"""
    result = yield from inner_generator()
    print(f"[outer] inner 返回: {result}")
    yield result


def merge_sorted(*iterables: list) -> Iterator:
    """合并多个有序列表"""
    heap = []
    for i, iterable in enumerate(iterables):
        it = iter(iterable)
        try:
            first = next(it)
            heap.append((first, i, it, first))
        except StopIteration:
            pass

    import heapq
    heapq.heapify(heap)

    while heap:
        value, i, it, _ = heapq.heappop(heap)
        yield value
        try:
            next_val = next(it)
            heapq.heappush(heap, (next_val, i, it, next_val))
        except StopIteration:
            pass


if __name__ == "__main__":
    print("=" * 60)
    print("1. 基本委托示例")
    print("=" * 60)

    print(f"delegated_generator(): {list(delegated_generator())}")
    print(f"equivalent_generator(): {list(equivalent_generator())}")
    print(f"两者相等: {list(delegated_generator()) == list(equivalent_generator())}")

    print("\n" + "=" * 60)
    print("2. 串联可迭代对象")
    print("=" * 60)

    result = list(chain_iterables([1, 2], [3, 4], [5, 6]))
    print(f"chain_iterables([1,2], [3,4], [5,6]): {result}")

    print("\n" + "=" * 60)
    print("3. 递归展平")
    print("=" * 60)

    nested = [1, [2, 3], [4, [5, [6]]]]
    print(f"嵌套列表: {nested}")
    print(f"flatten(): {list(flatten(nested))}")
    print(f"flatten_iterative(): {list(flatten_iterative(nested))}")

    print("\n" + "=" * 60)
    print("4. yield from 传播返回值")
    print("=" * 60)

    gen = outer_with_return()
    print(next(gen))  # 1
    print(next(gen))  # 2
    print(next(gen))  # 打印 "inner 返回: done"，yield "done"

    print("\n" + "=" * 60)
    print("5. 合并有序列表")
    print("=" * 60)

    merged = list(merge_sorted([1, 3, 5], [2, 4, 6], [0, 7]))
    print(f"merge_sorted([1,3,5], [2,4,6], [0,7]): {merged}")
