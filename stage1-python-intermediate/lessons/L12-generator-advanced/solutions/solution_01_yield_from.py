"""L12 练习1: yield from 实现"""

from typing import Iterator


def flatten(nested):
    """展平嵌套列表"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def traverse_tree(root):
    """遍历二叉树（先序遍历）"""
    if root is None:
        return
    yield root.get('val')
    yield from traverse_tree(root.get('left'))
    yield from traverse_tree(root.get('right'))


def merge_sorted(*iterables):
    """合并多个有序列表"""
    import heapq
    heap = []
    for i, iterable in enumerate(iterables):
        it = iter(iterable)
        try:
            first = next(it)
            heap.append((first, i, it))
        except StopIteration:
            pass
    heapq.heapify(heap)

    while heap:
        value, i, it = heapq.heappop(heap)
        yield value
        try:
            next_val = next(it)
            heapq.heappush(heap, (next_val, i, it))
        except StopIteration:
            pass


def chain_iterables(*iterables):
    """串联多个可迭代对象"""
    for iterable in iterables:
        yield from iterable


def walk_directory(paths):
    """递归遍历目录结构"""
    for path in paths:
        if isinstance(path, list):
            yield from walk_directory(path)
        else:
            yield path


def interleave(*iterables):
    """交替合并多个迭代器"""
    iterators = [iter(it) for it in iterables]
    while iterators:
        new_iterators = []
        for it in iterators:
            try:
                yield next(it)
                new_iterators.append(it)
            except StopIteration:
                pass
        iterators = new_iterators


if __name__ == "__main__":
    # 测试 flatten
    nested = [[1, 2], [3, 4], [5, [6, 7]]]
    result = list(flatten(nested))
    print(f"flatten({nested}) = {result}")
    assert result == [1, 2, 3, 4, 5, 6, 7]

    # 测试 traverse_tree
    tree = {'val': 1, 'left': {'val': 2, 'left': {'val': 4}}, 'right': {'val': 3}}
    result = list(traverse_tree(tree))
    print(f"traverse_tree(tree) = {result}")
    assert result == [1, 2, 4, 3]

    # 测试 merge_sorted
    result = list(merge_sorted([1, 3, 5], [2, 4, 6], [0, 7]))
    print(f"merge_sorted([1,3,5], [2,4,6], [0,7]) = {result}")
    assert result == [0, 1, 2, 3, 4, 5, 6, 7]

    # 测试 chain_iterables
    result = list(chain_iterables([1, 2], 'ab', (3, 4)))
    print(f"chain_iterables([1,2], 'ab', (3,4)) = {result}")
    assert result == [1, 2, 'a', 'b', 3, 4]

    # 测试 walk_directory
    paths = ['file1.txt', ['dir1', ['file2.txt', 'file3.txt']], 'file4.txt']
    result = list(walk_directory(paths))
    print(f"walk_directory(paths) = {result}")
    assert result == ['file1.txt', 'dir1', 'file2.txt', 'file3.txt', 'file4.txt']

    # 测试 interleave
    result = list(interleave([1, 2], [3, 4], [5, 6]))
    print(f"interleave([1,2], [3,4], [5,6]) = {result}")
    assert result == [1, 3, 5, 2, 4, 6]

    print("\n所有测试通过!")
