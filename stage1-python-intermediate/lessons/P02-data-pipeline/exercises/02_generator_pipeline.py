"""P02 练习 2: 生成器数据处理管道

课程编号: P02
所属课程: Stage 1 - Python 进阶
练习编号: 02
难度: ⭐⭐⭐⭐
知识点: yield + yield from + send()

任务：
1. 实现 generator_pipeline 函数，组合多个生成器
2. 实现 batch_generator 分批 yield
3. 实现 yield_from_chain 链接多个迭代器
4. 使用 send() 实现进度追踪

运行方式:
    python exercises/02_generator_pipeline.py

预期行为：
    def counter():
        total = 0
        while True:
            increment = yield total
            total += increment or 1

    c = counter()
    next(c)  # 初始化
    c.send(5)  # 返回 5
    c.send(3)  # 返回 8
"""

from typing import Iterator, Callable, Generator, TypeVar

T = TypeVar("T")


# ============================================================
# 1. generator_pipeline
# ============================================================

# TODO: 实现 generator_pipeline
def generator_pipeline(
    source: Iterator[T],
    *transformers: Callable[[Iterator[T]], Iterator[T]]
) -> Iterator[T]:
    """组合多个转换生成器

    预期行为:
        def double(items):
            for x in items:
                yield x * 2

        source = iter([1, 2, 3])
        result = list(generator_pipeline(source, double))
        assert result == [2, 4, 6]
    """
    # TODO: 依次应用每个 transformer，最后 yield from 结果
    pass


# ============================================================
# 2. batch_generator
# ============================================================

# TODO: 实现 batch_generator
def batch_generator(items: Iterator[T], batch_size: int) -> Generator[list[T], None, None]:
    """分批 yield 数据

    预期行为:
        items = range(10)
        batches = list(batch_generator(items, batch_size=3))
        assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
    """
    # TODO: 收集 batch_size 个元素后 yield，最后 yield 剩余元素
    pass


# ============================================================
# 3. yield from 链
# ============================================================

# TODO: 实现 flatten
def flatten(nested_iterators: Iterator[Iterator[T]]) -> Iterator[T]:
    """展平嵌套迭代器

    预期行为:
        nested = [[1, 2], [3, 4], [5]]
        result = list(flatten(iter(nested)))
        assert result == [1, 2, 3, 4, 5]
    """
    # TODO: 使用 yield from 展平嵌套迭代器
    pass


# ============================================================
# 4. send() 进度追踪
# ============================================================

# TODO: 实现 progress_tracker
def progress_tracker(total: int) -> Generator[int, int | None, int]:
    """进度追踪生成器

    使用 send() 双向通信：
    - next(tracker) 初始化
    - tracker.send(value) 累加进度，返回当前进度
    - 生成器结束时返回 final value

    预期行为:
        tracker = progress_tracker(100)
        next(tracker)  # 初始化
        assert tracker.send(10) == 10   # 进度 10
        assert tracker.send(20) == 30  # 进度 30
        assert tracker.send(5) == 35   # 进度 35
        # 当进度 >= total 时，send(0) 触发 StopIteration，返回最终进度
    """
    # TODO: 实现带 send() 的进度追踪器
    pass


# ============================================================
# 5. 高级: transform_generator
# ============================================================

# TODO: 实现 transform_generator（可选挑战）
def transform_generator(
    items: Iterator[T],
    *transforms: Callable[[T], T]
) -> Iterator[T]:
    """应用多个转换函数到每个元素

    预期行为:
        data = [1, 2, 3]
        result = list(transform_generator(
            iter(data),
            lambda x: x * 2,  # 翻倍
            lambda x: x + 1,  # 加一
        ))
        assert result == [3, 5, 7]  # (1*2+1), (2*2+1), (3*2+1)
    """
    # TODO: 对每个元素依次应用所有 transforms
    pass


# ============================================================
# 测试
# ============================================================

def test_batch_generator():
    """测试分批生成器"""
    items = range(10)
    batches = list(batch_generator(items, batch_size=3))
    assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]], f"实际: {batches}"
    print("✓ batch_generator 测试通过")


def test_flatten():
    """测试嵌套迭代器展平"""
    nested = [[1, 2], [3, 4], [5]]
    result = list(flatten(iter(nested)))
    assert result == [1, 2, 3, 4, 5], f"实际: {result}"
    print("✓ flatten 测试通过")


def test_progress_tracker():
    """测试进度追踪器"""
    tracker = progress_tracker(100)
    next(tracker)  # 初始化

    progress = tracker.send(10)
    assert progress == 10, f"实际: {progress}"

    progress = tracker.send(20)
    assert progress == 30, f"实际: {progress}"

    progress = tracker.send(5)
    assert progress == 35, f"实际: {progress}"
    print("✓ progress_tracker 测试通过")


def test_generator_pipeline():
    """测试生成器管道"""
    def double(items):
        for x in items:
            yield x * 2

    def filter_even(items):
        for x in items:
            if x % 4 == 0:
                yield x

    source = iter([1, 2, 3, 4, 5])
    result = list(generator_pipeline(source, double, filter_even))
    assert result == [4, 8], f"实际: {result}"
    print("✓ generator_pipeline 测试通过")


def test_transform_generator():
    """测试变换生成器"""
    data = [1, 2, 3]
    result = list(transform_generator(
        iter(data),
        lambda x: x * 2,
        lambda x: x + 1,
    ))
    assert result == [3, 5, 7], f"实际: {result}"
    print("✓ transform_generator 测试通过")


def main():
    """运行所有测试"""
    print("=" * 50)
    print("P02 练习 2: 生成器管道")
    print("=" * 50)

    try:
        test_batch_generator()
        test_flatten()
        test_progress_tracker()
        test_generator_pipeline()
        test_transform_generator()
        print("\n🎉 所有测试通过!")
    except (AssertionError, NotImplementedError) as e:
        print(f"\n❌ 测试失败: {e}")
        print("请实现 TODO 部分")


if __name__ == "__main__":
    main()
